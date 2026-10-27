//! The `INTERACTION-MATRIX` doctrine's driver, ported from `scripts/check_interaction_matrix.sh` (`XTASK.6` slice `6y`),
//! which is now a shim of `cargo xtask check-interaction-matrix`.
//!
//! Every unit's declared interaction matrix (`profiles/*/interactions.sexp`) must cover every derived cell of its axes,
//! resolve every disposition (a guest with its expectations document, a mechanism in the closed registry, a declared
//! degeneracy, a difference the dossier records) and name every tracked guest. The doctrine discovers every tracked unit
//! and runs the judge on each — `scripts/check_interaction_matrix.py`, the pinned Python judge, spawned exactly as the
//! driver spawned it and not ported; a device-model or profile-resolution route with no matrix is n/a by declaration.
//! The self-test writes the script's synthetic unit (a profile, two guests, a references document, a matrix) through the
//! same fixture texts; each self-test arm is one `tally.arm(` call, the idiom the `DERIVED-COUNTS` arm total counts.

use std::fs;
use std::path::{Path, PathBuf};
use std::process::{Command, ExitCode, Stdio};

use crate::harness::{py_splitlines, py_strip, scratch};

#[derive(Clone, Copy, PartialEq, Eq)]
enum Mode {
    Git,
    Fs,
}

struct Verdict {
    rc: i32,
    lines: Vec<String>,
}

impl Verdict {
    fn text(&self) -> String {
        self.lines.join("\n")
    }
}

/// The units: the directory of every tracked `profiles/*/profile.sexp` under `git`, of every one on disk under `fs`.
fn units(root: &Path, mode: Mode) -> Vec<PathBuf> {
    match mode {
        Mode::Git => Command::new("git")
            .args(["ls-files", "--", "profiles/*/profile.sexp"])
            .current_dir(root)
            .output()
            .map(|o| {
                py_splitlines(&String::from_utf8_lossy(&o.stdout))
                    .into_iter()
                    .filter(|l| !py_strip(l).is_empty())
                    .filter_map(|l| root.join(l).parent().map(Path::to_path_buf))
                    .collect()
            })
            .unwrap_or_default(),
        Mode::Fs => {
            let mut found: Vec<PathBuf> = fs::read_dir(root.join("profiles"))
                .map(|entries| {
                    entries
                        .flatten()
                        .map(|e| e.path())
                        .filter(|p| p.join("profile.sexp").is_file())
                        .collect()
                })
                .unwrap_or_default();
            found.sort();
            found
        }
    }
}

fn relative(path: &Path, root: &Path) -> String {
    path.strip_prefix(root)
        .unwrap_or(path)
        .display()
        .to_string()
}

/// The judge, spawned as the driver spawned it (`python3 scripts/check_interaction_matrix.py <unit>` from the repo).
fn judge(repo: &Path, unit: &Path) -> (i32, String, String) {
    match Command::new("python3")
        .arg("scripts/check_interaction_matrix.py")
        .arg(unit)
        .current_dir(repo)
        .stdin(Stdio::null())
        .output()
    {
        Ok(o) => (
            o.status.code().unwrap_or(-1),
            String::from_utf8_lossy(&o.stdout).into_owned(),
            String::from_utf8_lossy(&o.stderr).into_owned(),
        ),
        Err(e) => (-1, String::new(), e.to_string()),
    }
}

/// The inline Python, line for line: every unit judged, its report lines prefixed with the unit, its findings kept.
fn check_units(repo: &Path, root: &Path, mode: Mode) -> Verdict {
    let found = units(root, mode);
    if found.is_empty() {
        return Verdict {
            rc: 2,
            lines: vec![
                "INTERACTION-MATRIX: REFUSED — no unit found; this check cannot judge an empty corpus".to_owned(),
                "__CHECKED__ 0".to_owned(),
            ],
        };
    }
    let mut out: Vec<String> = Vec::new();
    let mut findings: Vec<String> = Vec::new();
    let mut checked = 0u32;
    for u in &found {
        checked += 1;
        let rel = relative(u, root);
        let (rc, stdout, stderr) = judge(repo, u);
        if rc == 2 {
            findings.push(format!("CANNOT JUDGE {rel}: {}", py_strip(&stderr)));
        } else if rc != 0 {
            findings.extend(
                py_splitlines(&stderr)
                    .into_iter()
                    .filter(|l| !py_strip(l).is_empty())
                    .map(str::to_owned),
            );
        } else {
            for line in py_splitlines(&stdout) {
                if line.starts_with("  ") {
                    out.push(format!("{rel}{line}"));
                } else {
                    out.push(format!("  {rel}: {line}"));
                }
            }
        }
    }
    out.extend(findings.iter().cloned());
    out.push(format!("__CHECKED__ {checked}"));
    Verdict {
        rc: i32::from(!findings.is_empty()),
        lines: out,
    }
}

struct Tally<'a> {
    repo: &'a Path,
    root: &'a Path,
    pass: u32,
    fail: u32,
    verbose: bool,
}

impl Tally<'_> {
    /// One arm: judging the fixture tree must give `expected` and contain `want`.
    fn arm(&mut self, name: &str, expected: i32, want: &str) {
        let verdict = check_units(self.repo, self.root, Mode::Fs);
        let out = verdict.text();
        if verdict.rc != expected {
            self.fail += 1;
            if self.verbose {
                eprintln!("INTERACTION-MATRIX self-test MISS: {name} expected rc={expected} got rc={}\n{out}", verdict.rc);
            }
        } else if !out.contains(want) {
            self.fail += 1;
            if self.verbose {
                eprintln!("INTERACTION-MATRIX self-test MISS: {name} right verdict, wrong reason (no {want})\n{out}");
            }
        } else {
            self.pass += 1;
        }
    }
}

/// `printf '%s\n' … > file`.
fn write(path: &Path, text: &str) {
    let _ = fs::write(path, format!("{text}\n"));
}

const GOOD: &str = "(cell (axis \"alpha\") (axis \"alpha\") (guest \"g1\")) (cell (axis \"alpha\") (axis \"beta\") (guest \"g2\")) (cell (axis \"beta\") (axis \"beta\") (mechanism \"smoke-reproduce\"))";

/// The RED/GREEN controls over the script's synthetic unit `p`: a profile, two guests, a references document, a matrix.
fn self_test(repo: &Path, verbose: bool) -> bool {
    let Ok(t) = scratch(repo, "target/doctrine-selftest", "interactions") else {
        eprintln!("INTERACTION-MATRIX self-test: cannot create a scratch directory under target/doctrine-selftest");
        return false;
    };
    let unit = t.join("profiles/p");
    let _ = fs::create_dir_all(unit.join("guests"));
    let profile = || {
        write(
            &unit.join("profile.sexp"),
            "(profile (id \"p\") (version \"0\") (status \"development\"))",
        )
    };
    let guests = || {
        for g in ["g1", "g2"] {
            write(&unit.join(format!("guests/{g}.s")), &format!("# {g}"));
            write(
                &unit.join(format!("guests/{g}.expected.sexp")),
                &format!(
                    "(expectations (program \"{g}.s\") (entry \"0x80000000\") (instructions 0))"
                ),
            );
        }
    };
    let references = |differences: &str| {
        write(
            &unit.join("references.sexp"),
            &format!(
                "(references (profile \"p\") (retrieved \"d\") (work_dir \"w\") {differences})"
            ),
        )
    };
    let matrix = |cells: &str| {
        write(
            &unit.join("interactions.sexp"),
            &format!("(interactions (profile \"p\") (axis (id \"alpha\") (covers \"a\")) (axis (id \"beta\") (covers \"b\")) {cells})"),
        )
    };
    let mut tally = Tally {
        repo,
        root: &t,
        pass: 0,
        fail: 0,
        verbose,
    };
    tally.arm("REFUSE no unit at all", 2, "cannot judge");
    profile();
    guests();
    references("");
    matrix(GOOD);
    tally.arm("GREEN a complete matrix resolves", 0, "3 cells declared");
    matrix("(cell (axis \"alpha\") (axis \"alpha\") (guest \"g1\")) (cell (axis \"alpha\") (axis \"beta\") (guest \"g2\"))");
    tally.arm(
        "RED   an omitted cell fails, named",
        1,
        "OMITTED CELL p: beta×beta",
    );
    matrix(&format!(
        "{GOOD} (cell (axis \"beta\") (axis \"beta\") (guest \"g1\"))"
    ));
    tally.arm(
        "RED   a cell declared twice",
        1,
        "DUPLICATE CELL p: beta×beta",
    );
    matrix("(cell (axis \"alpha\") (axis \"gamma\") (guest \"g1\")) (cell (axis \"alpha\") (axis \"beta\") (guest \"g2\")) (cell (axis \"beta\") (axis \"beta\") (mechanism \"smoke-reproduce\"))");
    tally.arm(
        "RED   a cell naming an undeclared axis",
        1,
        "UNDECLARED AXIS",
    );
    matrix(GOOD);
    let _ = fs::remove_file(unit.join("guests/g2.expected.sexp"));
    tally.arm(
        "RED   a guest without its expectations document",
        1,
        "UNRESOLVED GUEST",
    );
    write(
        &unit.join("guests/g2.expected.sexp"),
        "(expectations (program \"g2.s\") (entry \"0x80000000\") (instructions 0))",
    );
    matrix("(cell (axis \"alpha\") (axis \"alpha\") (guest \"g1\")) (cell (axis \"alpha\") (axis \"beta\") (guest \"g2\")) (cell (axis \"beta\") (axis \"beta\") (mechanism \"wishful-thinking\"))");
    tally.arm(
        "RED   a mechanism outside the closed registry",
        1,
        "UNKNOWN MECHANISM",
    );
    matrix("(cell (axis \"alpha\") (axis \"alpha\") (guest \"g1\")) (cell (axis \"alpha\") (axis \"beta\") (guest \"g2\") (degenerate \"both\")) (cell (axis \"beta\") (axis \"beta\") (mechanism \"smoke-reproduce\"))");
    tally.arm(
        "RED   a degenerate cell that also names a guest",
        1,
        "DEGENERATE MIXED",
    );
    matrix(GOOD);
    write(
        &unit.join("guests/g3.expected.sexp"),
        "(expectations (program \"g3.s\") (entry \"0x80000000\") (instructions 0))",
    );
    tally.arm(
        "RED   a tracked guest no cell names",
        1,
        "ORPHAN GUEST p: 'g3'",
    );
    let _ = fs::remove_file(unit.join("guests/g3.expected.sexp"));
    matrix("(cell (axis \"alpha\") (axis \"alpha\") (guest \"g1\")) (cell (axis \"alpha\") (axis \"beta\") (guest \"g2\") (difference \"DIFF-GHOST\")) (cell (axis \"beta\") (axis \"beta\") (mechanism \"smoke-reproduce\"))");
    tally.arm(
        "RED   a difference id references.sexp does not record",
        1,
        "UNKNOWN DIFFERENCE",
    );
    references("(difference (id \"DIFF-X\") (kind \"k\") (observed \"o\") (resolution \"r\"))");
    matrix("(cell (axis \"alpha\") (axis \"alpha\") (guest \"g1\")) (cell (axis \"alpha\") (axis \"beta\") (guest \"g2\") (difference \"DIFF-X\")) (cell (axis \"beta\") (axis \"beta\") (mechanism \"smoke-reproduce\"))");
    tally.arm(
        "GREEN a named difference the dossier records",
        0,
        "3 cells declared",
    );
    let _ = fs::remove_file(unit.join("interactions.sexp"));
    tally.arm("RED   a unit with no declared matrix", 1, "NO MATRIX");
    write(
        &unit.join("profile.sexp"),
        "(profile (id \"p\") (version \"0\") (status \"experimental\") (vehicle (route device-model) (comparison register-expectations) (authority laboratory) (source \"s\")))",
    );
    tally.arm(
        "GREEN device-model route with no matrix is n/a by declaration",
        0,
        "device-model route declared",
    );
    matrix("(cell (axis \"alpha\") (axis \"alpha\") (guest \"g1\")) (cell (axis \"alpha\") (axis \"beta\") (guest \"g2\"))");
    tally.arm(
        "RED   a device unit whose matrix omits a cell answers the full contract",
        1,
        "OMITTED CELL p: beta×beta",
    );
    let _ = fs::remove_file(unit.join("interactions.sexp"));
    write(
        &unit.join("profile.sexp"),
        "(profile (id \"p\") (version \"0\") (status \"development\") (vehicle (route profile-resolution) (authority laboratory) (source \"s\")))",
    );
    tally.arm(
        "GREEN profile-resolution route with no matrix is n/a by declaration",
        0,
        "profile-resolution route declared",
    );
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "INTERACTION-MATRIX --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}

/// `cargo xtask check-interaction-matrix [--self-test]`: the shell driver's verdict lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    if !self_test(root, false) {
        eprintln!(
            "INTERACTION-MATRIX: REFUSED — the check does not discriminate (self-test failed)."
        );
        return ExitCode::from(2);
    }
    let verdict = check_units(root, root, Mode::Git);
    let count = verdict
        .lines
        .iter()
        .find_map(|l| l.strip_prefix("__CHECKED__ "))
        .unwrap_or("0");
    let body: Vec<&str> = verdict
        .lines
        .iter()
        .filter(|l| !l.starts_with("__CHECKED__ "))
        .map(String::as_str)
        .collect();
    match verdict.rc {
        2 => {
            eprintln!("INTERACTION-MATRIX: REFUSED — the unit corpus could not be read.");
            for line in &body {
                eprintln!("  {line}");
            }
            ExitCode::from(2)
        }
        0 => {
            // `printf '%s\n' "$body"`: the (possibly empty) body, then the verdict.
            println!("{}", body.join("\n"));
            println!("INTERACTION-MATRIX: ok ({count} unit(s) — every derived cell declared, every disposition resolved, no orphan guests)");
            ExitCode::SUCCESS
        }
        _ => {
            eprintln!("INTERACTION-MATRIX: the declared matrix does not hold.");
            for line in &body {
                eprintln!("  {line}");
            }
            eprintln!("  Declare every cell and resolve every disposition — unexercised cells are reported, not omitted.");
            ExitCode::from(1)
        }
    }
}
