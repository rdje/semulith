//! The `MATERIALS-BILL` doctrine's driver, ported from `scripts/check_materials_bill.sh` (`XTASK.6` slice `6am`), which
//! is now a shim of `cargo xtask check-materials-bill`.
//!
//! Every registered unit's book (`materials/units.sexp`, the one registration place) carries a materials bill whose
//! identity tables are GENERATED from the pinned dossier (DRIFT is refused, never patched) and whose prose states, for
//! every material the unit's declared shape enumerates, what it does NOT supply. The judge is the driver's inline Python
//! (`check_bills`, over the pinned `sexp`, `dossier_sexp` and `gen_model_book`); it runs verbatim through `python3 -`, as
//! the script ran it, and is not ported — nor are the generator (`scripts/gen_model_book.py`), its catalogue tests
//! (`scripts/test_gen_model_book.py`) or the four inline Python edits of the controls, each spawned as the script spawned
//! them. The controls re-root the REAL dossiers and book (the processor's, the UART's, the board's) into scratch, as the
//! script did. Each self-test arm is one `tally.arm(` call, the idiom the `DERIVED-COUNTS` arm total counts.

use std::fs;
use std::io::Write;
use std::path::Path;
use std::process::{Command, ExitCode, Stdio};

use crate::harness::{on_path, scratch};

/// The judge, verbatim: `python3 - <root>` from the repository root (`scripts/` on its path) — the per-unit lines,
/// the findings, `__CHECKED__ N`; exit 1 on a finding, 2 when it cannot judge.
const JUDGE: &str = r####"import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, "scripts")
import sexp as S
import dossier_sexp as D
import gen_model_book as G

units_path = root / "materials" / "units.sexp"
if not units_path.is_file():
    print("MATERIALS-BILL: REFUSED — materials/units.sexp is absent; the unit registry "
          "this check enumerates is gone")
    print("__CHECKED__ 0"); sys.exit(2)
units = S.read_file(units_path)
unit_forms = [u for u in units if isinstance(u, list) and u and str(u[0]) == "unit"]
if not unit_forms:
    print("MATERIALS-BILL: REFUSED — the unit registry is empty; a census over no units "
          "is a claim about nothing")
    print("__CHECKED__ 0"); sys.exit(2)

findings, checked = [], 0
for u in unit_forms:
    uid = str(S.field(u, "id", "units.sexp"))
    book_rel = str(S.field(u, "book", "units.sexp")).rstrip("/")
    profile_dir = root / "profiles" / uid
    book_dir = root / book_rel
    bill = book_dir / "src" / "materials.md"
    checked += 1
    before = len(findings)

    # ---- structure: the book exists and carries the bill -----------------------------
    if not (book_dir / "book.toml").is_file() or not (book_dir / "src" / "SUMMARY.md").is_file():
        findings.append(f"NO BOOK {uid}: {book_rel} lacks book.toml/src/SUMMARY.md — a "
                        f"unit whose materials are unreviewable is a unit unreviewed")
        continue
    if not bill.is_file():
        findings.append(f"NO BILL {uid}: {book_rel}/src/materials.md is absent — the "
                        f"materials bill is the deliverable, not an option")
        continue

    # ---- DRIFT: the fragments still equal the pinned data ------------------------------
    r = subprocess.run([sys.executable, "scripts/gen_model_book.py", "--check",
                        "--profile-dir", str(profile_dir), "--book-dir", str(book_dir)],
                       capture_output=True, text=True)
    if r.returncode == 2:
        findings.append(f"CANNOT JUDGE {uid}: {r.stderr.strip()}")
        continue
    if r.returncode != 0:
        findings.append(f"DRIFT {uid}: {r.stderr.strip()} — regenerate with "
                        f"`python3 scripts/gen_model_book.py`; never edit the fragments")

    # ---- COMPLETENESS: every material has its section AND its negative statement -------
    # P5-BOARD.11: the enumeration is keyed on the unit's DECLARED shape
    # (gen_model_book.unit_shape) — a device dossier has no references.sexp (no encoding
    # source, no reference candidates, by declaration) and a board dossier pins its
    # materials in board.sexp (the processor unit + the device material ids). An
    # undeclared absence stays CANNOT JUDGE.
    shape = G.unit_shape(profile_dir)
    required: list[str] = []
    if shape == "board":
        try:
            bdoc = S.read_file(profile_dir / "board.sexp")[0]
        except (S.SexpError, IndexError) as exc:
            findings.append(f"CANNOT JUDGE {uid}: the pinned dossier does not map — {exc}")
            continue
        bproc = S.children(bdoc, "processor")[0]
        required = [str(S.field(bproc, "unit", "board.sexp"))]
        required += [str(S.field(d, "material", "board.sexp"))
                     for d in S.children(bdoc, "device")]
    else:
        try:
            src = D.load_sources(profile_dir / "sources.sexp")
            required = [s["id"] for s in src.get("source", [])]
            if shape != "device-model":
                refs = D.load_references(profile_dir / "references.sexp")
                required += ([e["id"] for e in refs.get("encoding_source", [])]
                             + [c["id"] for c in refs.get("candidate", [])])
        except D.DossierError as exc:
            findings.append(f"CANNOT JUDGE {uid}: the pinned dossier does not map — {exc}")
            continue
    required += list(G.shape_contracts(shape))
    text = bill.read_text()
    # one section per `###` heading; a section runs to the next heading of any level
    heads = [(m.start(), m.group(1)) for m in re.finditer(r"(?m)^###\s+(.*)$", text)]
    bounds = [m.start() for m in re.finditer(r"(?m)^#{1,3}\s", text)]
    for mid in required:
        hit = None
        for pos, heading in heads:
            if mid in heading:
                hit = pos
                break
        if hit is None:
            findings.append(f"MISSING SECTION {uid}: the bill has no `###` section naming "
                            f"'{mid}' — a material the pinned data carries is omitted, "
                            f"and an omission reads as if the material does not exist")
            continue
        end = min((b for b in bounds if b > hit), default=len(text))
        section = text[hit:end]
        if not re.search(r"does not supply", section, re.I):
            findings.append(f"NO DOES-NOT-SUPPLY {uid}: the '{mid}' section never states "
                            f"what the material does NOT supply — a bill that lists only "
                            f"what things provide is the lie of omission this gate exists "
                            f"to refuse")
    if len(findings) == before:
        print(f"  {uid}: {len(required)} materials, every fragment matches the pinned "
              f"data, every section carries its does-not-supply")

for f in findings:
    print(f)
print(f"__CHECKED__ {checked}")
sys.exit(1 if findings else 0)
"####;

/// The controls' inline edits, verbatim: `python3 - <bill>` each.
const DROP_SPIKE_SECTION: &str = r####"import re, sys
p = sys.argv[1]
text = open(p).read()
i = text.index("### `spike`")
j = text.index("###", i + 5)
open(p, "w").write(text[:i] + text[j:])
"####;
const SUPPLIES_FURTHERMORE: &str = r####"import sys
p = sys.argv[1]
text = open(p).read()
i = text.index("### `spike`")
j = text.index("###", i + 5)
section = text[i:j].replace("**Does not supply:**", "**Supplies, furthermore:**")
open(p, "w").write(text[:i] + section + text[j:])
"####;
const DROP_EXPECTATIONS_SECTION: &str = r####"import sys
p = sys.argv[1]
text = open(p).read()
i = text.index("### `expectations/`")
j = text.index("###", i + 5) if "###" in text[i + 5:] else len(text)
open(p, "w").write(text[:i] + text[j:])
"####;
const DROP_LAN9118_SECTION: &str = r####"import sys
p = sys.argv[1]
text = open(p).read()
i = text.index("### `MICROCHIP-LAN9118`")
j = text.index("###", i + 5)
open(p, "w").write(text[:i] + text[j:])
"####;

/// The shell's `$(…)`: every trailing newline removed.
fn captured(text: &str) -> &str {
    text.trim_end_matches('\n')
}

/// `python3 - <arg> <<'…'`: a program on stdin, one argument, from the repository root. `merge_stderr` is the arms'
/// `2>&1`; otherwise stderr passes through when `through` (the self-test as the command, the real run's judge)
/// and is silenced when the script ran its controls `>/dev/null 2>&1`.
fn python_stdin(
    repo: &Path,
    program: &str,
    arg: &Path,
    merge_stderr: bool,
    through: bool,
) -> (i32, String) {
    let mut command = Command::new("python3");
    command
        .arg("-")
        .arg(arg)
        .current_dir(repo)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(if merge_stderr {
            Stdio::piped()
        } else if through {
            Stdio::inherit()
        } else {
            Stdio::null()
        });
    let Ok(mut child) = command.spawn() else {
        return (-1, "cannot run python3".to_owned());
    };
    if let Some(mut stdin) = child.stdin.take() {
        let _ = stdin.write_all(program.as_bytes());
    }
    match child.wait_with_output() {
        Ok(o) => {
            let mut text = String::from_utf8_lossy(&o.stdout).into_owned();
            if merge_stderr {
                text.push_str(&String::from_utf8_lossy(&o.stderr));
            }
            (o.status.code().unwrap_or(-1), text)
        }
        Err(e) => (-1, e.to_string()),
    }
}

/// `python3 scripts/gen_model_book.py --profile-dir … --book-dir … >/dev/null`: stderr through when the self-test is
/// the command (`--self-test`), silenced when the script ran its controls `>/dev/null 2>&1`.
fn generate(repo: &Path, profile_dir: &Path, book_dir: &Path, verbose: bool) {
    let _ = Command::new("python3")
        .arg("scripts/gen_model_book.py")
        .arg("--profile-dir")
        .arg(profile_dir)
        .arg("--book-dir")
        .arg(book_dir)
        .current_dir(repo)
        .stdin(Stdio::null())
        .stdout(Stdio::null())
        .stderr(if verbose {
            Stdio::inherit()
        } else {
            Stdio::null()
        })
        .status();
}

/// `cp -R src dst` with `dst` absent: the tree copied, symbolic links as links.
fn copy_dir(src: &Path, dst: &Path) {
    let _ = fs::create_dir_all(dst);
    let Ok(entries) = fs::read_dir(src) else {
        return;
    };
    for entry in entries.flatten() {
        let from = entry.path();
        let to = dst.join(entry.file_name());
        let Ok(meta) = fs::symlink_metadata(&from) else {
            continue;
        };
        if meta.file_type().is_symlink() {
            if let Ok(target) = fs::read_link(&from) {
                #[cfg(unix)]
                let _ = std::os::unix::fs::symlink(target, &to);
            }
        } else if meta.is_dir() {
            copy_dir(&from, &to);
        } else {
            let _ = fs::copy(&from, &to);
        }
    }
}

/// `printf '…' >> path`: the text appended.
fn append(path: &Path, text: &str) {
    if let Ok(mut file) = fs::OpenOptions::new().append(true).create(true).open(path) {
        let _ = file.write_all(text.as_bytes());
    }
}

/// A synthetic bill: `# Materials bill`, then one `###` section per material, each with its does-not-supply.
fn synthetic_bill(path: &Path, materials: &[&str]) {
    let mut text = String::from("# Materials bill\n\n");
    for m in materials {
        text.push_str(&format!(
            "### `{m}`\n\nWhat it is for.\n\n**Does not supply:** something.\n\n"
        ));
    }
    let _ = fs::write(path, text);
}

struct Tally<'a> {
    repo: &'a Path,
    t: &'a Path,
    pass: u32,
    fail: u32,
    verbose: bool,
    /// Every missed arm's report, for a quiet run's refusal (`XTASK.12`).
    misses: Vec<String>,
}

impl Tally<'_> {
    /// A missed arm's report: printed at once in a verbose run, kept for a quiet run's refusal (`XTASK.12`).
    fn report(&mut self, report: String) {
        if self.verbose {
            eprintln!("{report}");
        }
        self.misses.push(report);
    }
    /// One arm: `check_bills "$t" 2>&1` must exit `expected` and its output must contain `want`.
    fn arm(&mut self, name: &str, expected: i32, want: &str) {
        let (rc, raw) = python_stdin(self.repo, JUDGE, self.t, true, self.verbose);
        let out = captured(&raw);
        if rc != expected {
            self.fail += 1;
            self.report(format!(
                "MATERIALS-BILL self-test MISS: {name} expected rc={expected} got rc={rc}\n{out}"
            ));
        } else if !out.contains(want) {
            self.fail += 1;
            self.report(format!("MATERIALS-BILL self-test MISS: {name} right verdict, wrong reason (no {want})\n{out}"));
        } else {
            self.pass += 1;
        }
    }
}

/// The RED/GREEN controls over scratch re-rootings of the real dossiers and book. Quiet unless `verbose` (the script
/// ran it `>/dev/null 2>&1` before the real judgement).
fn self_test(repo: &Path, verbose: bool) -> bool {
    // Semantic catalogue controls complement the byte-drift controls below: `python3 scripts/test_gen_model_book.py || return 1`.
    let catalogue = Command::new("python3")
        .arg("scripts/test_gen_model_book.py")
        .current_dir(repo)
        .stdin(Stdio::null())
        .stdout(if verbose {
            Stdio::inherit()
        } else {
            Stdio::null()
        })
        .stderr(if verbose {
            Stdio::inherit()
        } else {
            Stdio::null()
        })
        .status();
    if !catalogue.is_ok_and(|s| s.success()) {
        return false;
    }
    let Ok(t) = scratch(repo, "target/doctrine-selftest", "materialsbill") else {
        if verbose {
            eprintln!("MATERIALS-BILL self-test: cannot create a scratch directory under target/doctrine-selftest");
        }
        return false;
    };
    let mut tally = Tally {
        repo,
        t: &t,
        pass: 0,
        fail: 0,
        verbose,
        misses: Vec::new(),
    };
    let units = t.join("materials/units.sexp");
    // A scratch corpus: the REAL profile dossier and book, re-rooted as unit "p" — the fragments are regenerated into
    // the fixture by the real generator.
    let fixture = |verbose: bool| {
        let _ = fs::remove_dir_all(t.join("profiles/p"));
        let _ = fs::remove_dir_all(t.join("books/p"));
        for d in ["profiles", "books", "materials"] {
            let _ = fs::create_dir_all(t.join(d));
        }
        copy_dir(&repo.join("profiles/rv64i-lab-v0"), &t.join("profiles/p"));
        copy_dir(&repo.join("docs/models/rv64i-lab-v0"), &t.join("books/p"));
        let _ = fs::write(
            &units,
            "(unit (id \"p\") (kind processor) (layer processor) (book \"books/p\"))\n",
        );
        generate(repo, &t.join("profiles/p"), &t.join("books/p"), verbose);
    };
    tally.arm("REFUSE no units registry at all", 2, "REFUSED");
    fixture(verbose);
    tally.arm(
        "GREEN the real bill over the real dossier",
        0,
        "every section carries its does-not-supply",
    );
    append(
        &t.join("books/p/src/materials/pinned-specifications.md"),
        "\n| `X` | hand-edited |\n",
    );
    tally.arm("RED   a hand-edited generated table", 1, "DRIFT");
    generate(repo, &t.join("profiles/p"), &t.join("books/p"), verbose);
    let bill = t.join("books/p/src/materials.md");
    let _ = python_stdin(repo, DROP_SPIKE_SECTION, &bill, false, verbose);
    tally.arm(
        "RED   a material with no section",
        1,
        "MISSING SECTION p: the bill has no `###` section naming 'spike'",
    );
    fixture(verbose);
    let _ = python_stdin(repo, SUPPLIES_FURTHERMORE, &bill, false, verbose);
    tally.arm(
        "RED   a section that never says what the material does NOT supply",
        1,
        "NO DOES-NOT-SUPPLY",
    );
    fixture(verbose);
    let _ = fs::remove_file(&bill);
    tally.arm("RED   a book with no bill chapter", 1, "NO BILL");
    let _ = fs::remove_file(t.join("books/p/book.toml"));
    tally.arm("RED   a book with no skeleton", 1, "NO BOOK");
    // P5-BOARD.11: the device and board shapes — the census follows the declaration. The fixtures re-root the REAL
    // dossiers (the UART's, the board's) exactly as the processor fixture does, and the bills name every material the
    // shape enumerates.
    let shaped = |id: &str, kind: &str, source: &str, materials: &[&str], verbose: bool| {
        let profile = t.join(format!("profiles/{id}"));
        let book = t.join(format!("books/{id}"));
        let _ = fs::remove_dir_all(&profile);
        let _ = fs::remove_dir_all(&book);
        let _ = fs::create_dir_all(book.join("src/materials"));
        copy_dir(&repo.join(format!("profiles/{source}")), &profile);
        let _ = fs::write(
            &units,
            format!("(unit (id \"{id}\") (kind {kind}) (layer {kind}) (book \"books/{id}\"))\n"),
        );
        let _ = fs::write(
            book.join("book.toml"),
            format!("[book]\ntitle = \"{id}\"\n"),
        );
        let _ = fs::write(
            book.join("src/SUMMARY.md"),
            "# Summary\n\n[materials](materials.md)\n",
        );
        generate(repo, &profile, &book, verbose);
        synthetic_bill(&book.join("src/materials.md"), materials);
    };
    const DEVICE: &[&str] = &[
        "SIFIVE-FU540-C000",
        "profile.sexp",
        "state.sexp",
        "requirements.sexp",
        "contract-obligations.sexp",
        "expectations/",
    ];
    shaped("d", "device", "sifive-uart-lab-v0", DEVICE, verbose);
    tally.arm(
        "GREEN a device-shaped bill — no references.sexp, expectations/ is the corpus",
        0,
        "every section carries its does-not-supply",
    );
    shaped("d", "device", "sifive-uart-lab-v0", DEVICE, verbose);
    let _ = python_stdin(
        repo,
        DROP_EXPECTATIONS_SECTION,
        &t.join("books/d/src/materials.md"),
        false,
        verbose,
    );
    tally.arm(
        "RED   a device bill omitting the expectations/ section",
        1,
        "MISSING SECTION d",
    );
    const BOARD: &[&str] = &[
        "rv64i-lab-v0",
        "SIFIVE-FU540-C000",
        "MICROCHIP-LAN9118",
        "board.sexp",
        "DOSSIER.md",
    ];
    shaped("b", "board", "netboard-lab-v0", BOARD, verbose);
    tally.arm(
        "GREEN a board-shaped bill — the composition pins are the materials",
        0,
        "every section carries its does-not-supply",
    );
    shaped("b", "board", "netboard-lab-v0", BOARD, verbose);
    let _ = python_stdin(
        repo,
        DROP_LAN9118_SECTION,
        &t.join("books/b/src/materials.md"),
        false,
        verbose,
    );
    tally.arm(
        "RED   a board bill omitting a device material pin",
        1,
        "MISSING SECTION b",
    );
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "MATERIALS-BILL --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    } else {
        // A quiet run names every missed arm before the caller's refusal line (`XTASK.12`).
        for report in &tally.misses {
            eprintln!("{report}");
        }
    }
    tally.fail == 0
}

/// `cargo xtask check-materials-bill [--self-test]`: the shell driver's verdict lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    // `command -v python3`
    if !on_path("python3") {
        eprintln!("MATERIALS-BILL: REFUSED — python3 is not on PATH; this check cannot judge.");
        return ExitCode::from(2);
    }
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    if !self_test(root, false) {
        eprintln!("MATERIALS-BILL: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    // `out="$(check_bills "$ROOT")"`: stdout captured, stderr through.
    let (rc, raw) = python_stdin(root, JUDGE, root, false, true);
    let out = captured(&raw);
    let count = out
        .lines()
        .filter_map(|line| line.strip_prefix("__CHECKED__ "))
        .collect::<Vec<_>>()
        .join("\n");
    let body = out
        .lines()
        .filter(|line| !line.starts_with("__CHECKED__ "))
        .collect::<Vec<_>>()
        .join("\n");
    let body = captured(&body);
    if rc == 2 {
        eprintln!("MATERIALS-BILL: REFUSED — the unit corpus could not be read.");
        for line in body.split('\n') {
            eprintln!("  {line}");
        }
        return ExitCode::from(2);
    }
    if rc != 0 {
        eprintln!("MATERIALS-BILL: a unit's materials bill does not hold.");
        for line in body.split('\n') {
            eprintln!("  {line}");
        }
        eprintln!(
            "  Regenerate the fragments (never edit them), and give every material its section"
        );
        eprintln!("  with its does-not-supply statement.");
        return ExitCode::from(1);
    }
    println!("{body}");
    let count = if count.is_empty() {
        "0"
    } else {
        count.as_str()
    };
    println!("MATERIALS-BILL: ok ({count} unit(s) — generated tables match the pinned data; every material states what it does not supply)");
    ExitCode::SUCCESS
}
