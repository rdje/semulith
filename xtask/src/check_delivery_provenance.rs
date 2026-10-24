//! The `DELIVERY-PROVENANCE` doctrine, ported from `scripts/check_delivery_provenance.sh` (`XTASK.6` slice
//! `6c`), which is now a shim of `cargo xtask check-delivery-provenance`.
//!
//! A supplied package arrives with a `MANIFEST.sha256`, a record of what was delivered, and some of its rows
//! name files this repository exists to change. So every manifest row carries exactly one disposition,
//! declared as data in the package's `dispositions.tsv`, and the check re-derives the ones that must hold:
//! `frozen-in-place` (the delivered bytes at the delivered path, hash re-derived), `relocated` (the delivered
//! bytes moved to `current_path`, hash re-derived) and `live` (owned here now; existence only). A manifest row
//! with no disposition, or a disposition naming a path the manifest does not list, is a breach. Honest limit:
//! it proves the delivered bytes are still the bytes and every row's treatment was declared, not that the
//! delivered content was correct.
//!
//! Kept from the script on purpose: hashing through `sha256sum` or `shasum -a 256` (refusing when neither
//! exists), the locale's collation for the listed paths and the package order (through `sort`), and bash's
//! field split of a disposition row. Each self-test arm is one `tally.arm(` call (the `DERIVED-COUNTS` idiom).

use std::collections::HashMap;
use std::fs;
use std::path::Path;
use std::process::{Command, ExitCode, Stdio};

use crate::harness::{locale_sorted, scratch};

/// Runs the doctrine: `--self-test` as the first argument runs the arms; anything else runs the check.
/// Exit 0 ok, 1 a package no longer matches its dispositions, 2 refused.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    let Some(hasher) = Hasher::find() else {
        eprintln!("DELIVERY-PROVENANCE: REFUSED — no sha256sum or shasum on PATH; this check cannot judge.");
        return ExitCode::from(2);
    };
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, &hasher, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    let packages = packages(root);
    if packages.is_empty() {
        println!("DELIVERY-PROVENANCE: ok (no packages under docs/provenance/)");
        return ExitCode::SUCCESS;
    }
    if !self_test(root, &hasher, false) {
        eprintln!(
            "DELIVERY-PROVENANCE: REFUSED — the check does not discriminate (self-test failed)."
        );
        return ExitCode::from(2);
    }
    let mut failed = false;
    let mut report = String::new();
    for package in &packages {
        let (held, out) = verify_package(&hasher, &root.join(package), package, root);
        failed |= !held;
        report.push_str(&out);
        report.push('\n');
    }
    if failed {
        eprintln!(
            "DELIVERY-PROVENANCE: a delivered package no longer matches its declared dispositions."
        );
        eprint!("{report}");
        eprintln!("  Fix the tree, or change the row's disposition in dispositions.tsv AND say why in DELIVERY.md.");
        eprintln!("  Never edit a frozen record to make it agree with the tree.");
        return ExitCode::from(1);
    }
    print!("DELIVERY-PROVENANCE: ok\n{report}");
    ExitCode::SUCCESS
}

/// The hasher the script would pick: `sha256sum` when on `PATH`, else `shasum -a 256`.
struct Hasher {
    program: &'static str,
    args: &'static [&'static str],
}

impl Hasher {
    /// The first hasher that hashes `/dev/null` successfully, as the script's preflight required.
    fn find() -> Option<Self> {
        let candidates = [
            Hasher {
                program: "sha256sum",
                args: &[],
            },
            Hasher {
                program: "shasum",
                args: &["-a", "256"],
            },
        ];
        // The script chose by `command -v`, then required the chosen one to work: a hasher that exists but
        // fails is a refusal, not a fall-through to the next.
        let chosen = candidates.into_iter().find(|h| on_path(h.program))?;
        let works = Command::new(chosen.program)
            .args(chosen.args)
            .arg("/dev/null")
            .stdin(Stdio::null())
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .status()
            .is_ok_and(|status| status.success());
        works.then_some(chosen)
    }

    /// The first space-separated field of the hasher's first output line (the script's `cut -d' ' -f1`);
    /// the hasher's own errors pass through on stderr.
    fn digest(&self, path: &Path) -> String {
        Command::new(self.program)
            .args(self.args)
            .arg(path)
            .stdin(Stdio::null())
            .stderr(Stdio::inherit())
            .output()
            .map(|output| {
                let text = String::from_utf8_lossy(&output.stdout).into_owned();
                let line = text.lines().next().unwrap_or("");
                line.split(' ').next().unwrap_or("").to_owned()
            })
            .unwrap_or_default()
    }
}

/// Whether `program` is an executable file in a `PATH` directory (the script's `command -v`).
fn on_path(program: &str) -> bool {
    std::env::var_os("PATH").is_some_and(|path| {
        std::env::split_paths(&path).any(|dir| {
            fs::metadata(dir.join(program)).is_ok_and(|meta| meta.is_file() && executable(&meta))
        })
    })
}

/// Whether a file's mode lets someone execute it.
#[cfg(unix)]
fn executable(meta: &fs::Metadata) -> bool {
    use std::os::unix::fs::PermissionsExt as _;
    meta.permissions().mode() & 0o111 != 0
}

/// Without Unix modes (the wasm32 build of the workspace) a regular file is taken as executable.
#[cfg(not(unix))]
fn executable(_: &fs::Metadata) -> bool {
    true
}

/// The package directories under `docs/provenance/`, as the script's `docs/provenance/*/` glob listed them:
/// not hidden, directories or links to one, in collation order, relative to the root.
fn packages(root: &Path) -> Vec<String> {
    let Ok(entries) = fs::read_dir(root.join("docs/provenance")) else {
        return Vec::new();
    };
    let names = entries
        .filter_map(Result::ok)
        .filter(|entry| entry.path().is_dir())
        .filter_map(|entry| entry.file_name().into_string().ok())
        .filter(|name| !name.starts_with('.'))
        .map(|name| format!("docs/provenance/{name}"))
        .collect();
    locale_sorted(names)
}

/// The lines of `listed` not matched by a line of `removed`, each match used once (the script's
/// `comm -23` over two sorted lists), in `listed`'s order.
fn difference(listed: &[String], removed: &[String]) -> Vec<String> {
    let mut available: HashMap<&str, usize> = HashMap::new();
    for line in removed {
        *available.entry(line.as_str()).or_default() += 1;
    }
    listed
        .iter()
        .filter(|line| match available.get_mut(line.as_str()) {
            Some(count) if *count > 0 => {
                *count -= 1;
                false
            }
            _ => true,
        })
        .cloned()
        .collect()
}

/// A disposition row split as the script's `IFS=$'\x1f' read -r kind mpath cpath` split it: the third
/// field keeps the rest of the row, except that one trailing separator after a single field is dropped.
fn split_row(line: &str) -> (String, String, String) {
    let mut parts = line.splitn(3, '\t');
    let kind = parts.next().unwrap_or("").to_owned();
    let mpath = parts.next().unwrap_or("").to_owned();
    let mut rest = parts.next().unwrap_or("").replace('\t', "\u{1f}");
    if let Some(field) = rest.strip_suffix('\u{1f}') {
        if !field.contains('\u{1f}') {
            rest = field.to_owned();
        }
    }
    (kind, mpath, rest)
}

/// Verifies one package (`MANIFEST.sha256` plus `dispositions.tsv`), resolving its paths against `base`.
/// Returns whether it held and its findings and summary as the script printed them, `shown` naming it.
fn verify_package(hasher: &Hasher, package: &Path, shown: &str, base: &Path) -> (bool, String) {
    let manifest_path = package.join("MANIFEST.sha256");
    let disposition_path = package.join("dispositions.tsv");
    let mut out: Vec<String> = Vec::new();
    if !manifest_path.is_file() {
        return (false, format!("  MISSING {shown}/MANIFEST.sha256"));
    }
    if !disposition_path.is_file() {
        return (
            false,
            format!("  MISSING {shown}/dispositions.tsv (the dispositions are DATA, not prose)"),
        );
    }
    let manifest = fs::read_to_string(&manifest_path).unwrap_or_default();
    let dispositions = fs::read_to_string(&disposition_path).unwrap_or_default();
    // awk 'NF>=2 {print $2}' and awk -F'\t' '!/^#/ && NF>=3 {print $2}'
    let manifest_rows: Vec<Vec<&str>> = manifest
        .lines()
        .map(|line| line.split_whitespace().collect::<Vec<_>>())
        .filter(|fields| fields.len() >= 2)
        .collect();
    let manifest_paths = locale_sorted(manifest_rows.iter().map(|f| f[1].to_owned()).collect());
    let disposed_paths = locale_sorted(
        dispositions
            .lines()
            .filter(|line| !line.starts_with('#'))
            .map(|line| line.split('\t').collect::<Vec<_>>())
            .filter(|fields| fields.len() >= 3)
            .map(|fields| fields[1].to_owned())
            .collect(),
    );
    let mut bad = false;
    let undeclared = difference(&manifest_paths, &disposed_paths);
    let orphans = difference(&disposed_paths, &manifest_paths);
    if !undeclared.is_empty() {
        out.push(
            "  UNDECLARED manifest row(s) — no disposition, so their treatment is unstated:"
                .to_owned(),
        );
        out.extend(undeclared.iter().map(|path| format!("    {path}")));
        bad = true;
    }
    if !orphans.is_empty() {
        out.push(
            "  ORPHAN disposition(s) — declared for a path the manifest does not list:".to_owned(),
        );
        out.extend(orphans.iter().map(|path| format!("    {path}")));
        bad = true;
    }
    let (mut frozen, mut relocated, mut live) = (0u32, 0u32, 0u32);
    for line in dispositions.lines() {
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        let (kind, mpath, cpath) = split_row(line);
        if kind.is_empty() || kind.starts_with('#') {
            continue;
        }
        if cpath.is_empty() {
            out.push(format!(
                "  INCOMPLETE disposition row for '{mpath}' — no current_path"
            ));
            bad = true;
            continue;
        }
        let want = manifest_rows
            .iter()
            .filter(|fields| fields[1] == mpath)
            .map(|fields| fields[0])
            .collect::<Vec<_>>()
            .join("\n");
        let target = base.join(&cpath);
        match kind.as_str() {
            "frozen-in-place" | "relocated" => {
                if !target.is_file() {
                    out.push(format!("  MISSING ({kind}) {cpath}"));
                    bad = true;
                    continue;
                }
                let got = hasher.digest(&target);
                if got != want {
                    out.push(format!("  DRIFTED ({kind}) {cpath}"));
                    out.push(format!("    delivered {want}"));
                    out.push(format!("    current   {got}"));
                    bad = true;
                    continue;
                }
                if kind == "frozen-in-place" {
                    frozen += 1;
                } else {
                    relocated += 1;
                }
            }
            "live" => {
                if !target.is_file() {
                    out.push(format!("  MISSING (live) {cpath}"));
                    bad = true;
                    continue;
                }
                live += 1;
            }
            _ => {
                out.push(format!(
                    "  UNKNOWN disposition '{kind}' for {mpath} (expected frozen-in-place|relocated|live)"
                ));
                bad = true;
            }
        }
    }
    out.push(format!(
        "  {shown}: {frozen} frozen-in-place, {relocated} relocated re-derived; {live} live row(s) declared"
    ));
    (!bad, out.join("\n"))
}

/// The self-test's pass and fail counts; `verbose` prints misses on stderr and the summary on stdout.
struct Tally {
    pass: u32,
    fail: u32,
    verbose: bool,
}

impl Tally {
    /// One arm: verifying the fixture package must give `expected` (0 held, 1 breached) and its text must
    /// contain `want`.
    fn arm(&mut self, fixture: (&Hasher, &Path, &Path), name: &str, expected: i32, want: &str) {
        let (hasher, package, tree) = fixture;
        let shown = package.display().to_string();
        let (held, out) = verify_package(hasher, package, &shown, tree);
        let rc = i32::from(!held);
        if rc != expected {
            self.fail += 1;
            if self.verbose {
                eprintln!("DELIVERY-PROVENANCE self-test MISS: {name} expected rc={expected} got rc={rc}\n{out}");
            }
        } else if !out.contains(want) {
            self.fail += 1;
            if self.verbose {
                eprintln!(
                    "DELIVERY-PROVENANCE self-test MISS: {name} right verdict, wrong reason (no {want})\n{out}"
                );
            }
        } else {
            self.pass += 1;
        }
    }
}

/// The base dispositions of the self-test's package: one row of each kind.
const BASE_DISPOSITIONS: &str =
    "frozen-in-place\tfrozen.txt\tfrozen.txt\nrelocated\treloc.txt\tmoved/reloc.txt\nlive\tlive.txt\tlive.txt\n";

/// The base dispositions without the rows of one kind.
fn base_without(kind: &str) -> String {
    BASE_DISPOSITIONS
        .lines()
        .filter(|line| !line.starts_with(kind))
        .map(|line| format!("{line}\n"))
        .collect()
}

/// The nine arms over a synthetic package and tree. Returns whether every arm held.
fn self_test(root: &Path, hasher: &Hasher, verbose: bool) -> bool {
    let mut tally = Tally {
        pass: 0,
        fail: 0,
        verbose,
    };
    let Ok(t) = scratch(root, "target/doctrine-selftest", "delivery-provenance") else {
        if verbose {
            eprintln!("DELIVERY-PROVENANCE self-test: cannot create a scratch directory");
        }
        return false;
    };
    let (package, tree) = (t.join("pkg"), t.join("tree"));
    let write = |rel: &str, text: &str| fs::write(t.join(rel), text);
    let setup = fs::create_dir_all(&package)
        .and_then(|()| fs::create_dir_all(tree.join("moved")))
        .and_then(|()| write("tree/frozen.txt", "good\n"))
        .and_then(|()| write("tree/moved/reloc.txt", "good\n"))
        .and_then(|()| write("tree/live.txt", "anything\n"))
        .and_then(|()| {
            let good = hasher.digest(&tree.join("frozen.txt"));
            let live = hasher.digest(&tree.join("live.txt"));
            write(
                "pkg/MANIFEST.sha256",
                &format!("{good}  frozen.txt\n{good}  reloc.txt\n{live}  live.txt\n"),
            )
        })
        .and_then(|()| write("pkg/dispositions.tsv", BASE_DISPOSITIONS));
    if setup.is_err() {
        if verbose {
            eprintln!("DELIVERY-PROVENANCE self-test: cannot write the fixture package");
        }
        let _ = fs::remove_dir_all(&t);
        return false;
    }
    let fixture = (hasher, package.as_path(), tree.as_path());
    tally.arm(
        fixture,
        "GREEN all rows verify",
        0,
        "1 frozen-in-place, 1 relocated",
    );
    let _ = write("tree/frozen.txt", "tampered\n");
    tally.arm(
        fixture,
        "RED frozen row byte changed",
        1,
        "DRIFTED (frozen-in-place) frozen.txt",
    );
    let _ = write("tree/frozen.txt", "good\n");
    let _ = write("tree/moved/reloc.txt", "tampered\n");
    tally.arm(
        fixture,
        "RED relocated row byte changed",
        1,
        "DRIFTED (relocated) moved/reloc.txt",
    );
    let _ = write("tree/moved/reloc.txt", "good\n");
    let _ = write("tree/live.txt", "changed-freely\n");
    tally.arm(
        fixture,
        "GREEN live row may drift",
        0,
        "1 live row(s) declared",
    );
    let _ = write("pkg/dispositions.tsv", &base_without("frozen-in-place"));
    tally.arm(
        fixture,
        "RED manifest row undeclared",
        1,
        "UNDECLARED manifest row",
    );
    let _ = write(
        "pkg/dispositions.tsv",
        &format!("{BASE_DISPOSITIONS}frozen-in-place\tghost.txt\tghost.txt\n"),
    );
    tally.arm(fixture, "RED orphan disposition", 1, "ORPHAN disposition");
    let _ = write(
        "pkg/dispositions.tsv",
        &format!(
            "{}relocated\treloc.txt\tnowhere/reloc.txt\n",
            base_without("relocated")
        ),
    );
    tally.arm(
        fixture,
        "RED relocated target missing",
        1,
        "MISSING (relocated) nowhere/reloc.txt",
    );
    let _ = write(
        "pkg/dispositions.tsv",
        &BASE_DISPOSITIONS.replace("\nlive", "\ninvented"),
    );
    tally.arm(
        fixture,
        "RED unknown disposition name",
        1,
        "UNKNOWN disposition 'invented'",
    );
    // The empty-field arm: with `IFS=$'\t' read` this row silently parsed as a different row.
    let _ = write(
        "pkg/dispositions.tsv",
        &format!("{}live\tlive.txt\t\n", base_without("live")),
    );
    tally.arm(
        fixture,
        "RED disposition row incomplete",
        1,
        "INCOMPLETE disposition row for 'live.txt'",
    );
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "DELIVERY-PROVENANCE --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}
