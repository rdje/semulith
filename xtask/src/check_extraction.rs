//! The `EXTRACTION` doctrine, ported from `scripts/check_extraction.sh` (`XTASK.6` slice `6q`), which is now a shim of
//! `cargo xtask check-extraction`.
//!
//! `MODEL-METHOD.10` turns "the engine can extract all it needs" from an intention into a verdict: every declared
//! instruction has an encoding AND semantics AND a requirement, every state element a reset, every obligation its
//! checks. `P1-LAB` cites this check as the precondition for writing model code — and a check that runs nowhere cannot
//! be cited. The doctrine discovers every tracked unit (`profiles/*/profile.sexp`) and runs the contract's judge on
//! each: `scripts/check_extraction.py`, the pinned Python judge, spawned exactly as the driver spawned it — this slice
//! ports the driver, not the judge. The self-test's record fixtures are written through the Rust record mapping
//! (`records::dump`), as the script wrote them through `records_sexp.dump`; each self-test arm is one `tally.arm(`
//! call, the idiom the `DERIVED-COUNTS` arm total counts, and the judge's own controls are scored once beside them.

use std::fs;
use std::path::{Path, PathBuf};
use std::process::{Command, ExitCode, Stdio};

use crate::harness::{combined, py_splitlines, py_strip, scratch};
use crate::records::{self, Value};

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

/// A command run from `repo` with stdin closed: its exit code (`-1` for a signal or a failure to start), stdout, stderr.
fn capture(repo: &Path, program: &str, args: &[&str]) -> (i32, String, String) {
    match Command::new(program)
        .args(args)
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

/// The inline Python, line for line: every unit judged by the pinned judge, spawned from the repository as the driver
/// spawned it (`python3 scripts/check_extraction.py <unit>`).
fn check_units(repo: &Path, root: &Path, mode: Mode) -> Verdict {
    let found = units(root, mode);
    if found.is_empty() {
        return Verdict {
            rc: 2,
            lines: vec![
                "EXTRACTION: REFUSED — no unit found; this check cannot judge an empty corpus"
                    .to_owned(),
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
        let (rc, stdout, stderr) = capture(
            repo,
            "python3",
            &["scripts/check_extraction.py", &u.display().to_string()],
        );
        if rc == 2 {
            findings.push(format!("CANNOT JUDGE {rel}: {}", py_strip(&stderr)));
        } else if rc != 0 {
            let gap = py_splitlines(&stderr)
                .into_iter()
                .rfind(|l| !py_strip(l).is_empty());
            findings.push(format!(
                "INSUFFICIENT {rel}: {}",
                gap.unwrap_or_else(|| py_strip(&stderr))
            ));
        } else {
            out.push(format!("  {rel}: {}", py_strip(&stdout)));
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
                eprintln!(
                    "EXTRACTION self-test MISS: {name} expected rc={expected} got rc={}\n{out}",
                    verdict.rc
                );
            }
        } else if !out.contains(want) {
            self.fail += 1;
            if self.verbose {
                eprintln!("EXTRACTION self-test MISS: {name} right verdict, wrong reason (no {want})\n{out}");
            }
        } else {
            self.pass += 1;
        }
    }

    /// `P4-SYSTEM.12` e2c: the Python contract controls run at the registered boundary — scored once, not an arm.
    fn score(&mut self, name: &str) {
        let (rc, out) = combined(
            Command::new("python3")
                .args(["scripts/check_extraction.py", "--self-test"])
                .current_dir(self.repo),
        );
        if rc == 0 && out.contains("check_extraction --self-test: 17 pass / 0 fail") {
            self.pass += 1;
        } else {
            self.fail += 1;
            if self.verbose {
                eprintln!("EXTRACTION self-test MISS: {name}\n{out}");
            }
        }
    }
}

fn write(path: &Path, text: &str) {
    let _ = fs::write(path, text);
}

fn s(text: &str) -> Value {
    Value::Str(text.to_owned())
}

fn strs(items: &[&str]) -> Value {
    Value::List(items.iter().map(|i| s(i)).collect())
}

fn obj(pairs: Vec<(&str, Value)>) -> Value {
    Value::Object(pairs.into_iter().map(|(k, v)| (k.to_owned(), v)).collect())
}

fn source_refs() -> Value {
    Value::List(vec![obj(vec![("source_id", s("S")), ("locator", s("§1"))])])
}

/// The script's `records_sexp.dump([record])`, through the Rust mapping.
fn write_record(path: &Path, record: Value) {
    if let Ok(text) = records::dump(&[record]) {
        write(path, &text);
    }
}

const RULE: &str =
    "(sem (insn add) (source \"S §1 — why\") (effect (set (reg rd) (add (reg rs1) (reg rs2)))))";
const RULE2: &str =
    "(sem (insn sub) (source \"S §2 — why\") (effect (set (reg rd) (sub (reg rs1) (reg rs2)))))";
const RESET: &str = "(reset \"0x00\")";

/// An instruction unit's documents: encoding, profile, a requirement and an obligation (through the mapping), state.
fn unit_docs(dir: &Path) {
    write(
        &dir.join("encoding.sexp"),
        "(encoding (profile \"p\") (ilen 32)\n  (compose (base \"riscv/t\") (extensions))\n  (fragment-root \"definitions\"))\n",
    );
    write(
        &dir.join("profile.sexp"),
        "(profile (id \"p\") (version \"0\") (status \"development\") (architecture \"R\")\n  (scope (count_base 2) (count_total 2) (demo \"ADD\" \"SUB\"))\n  (decision (id \"D-X\") (authority architecture) (statement \"s\") (source \"S §1\")))\n",
    );
    write_record(
        &dir.join("requirements.sexp"),
        obj(vec![
            ("id", s("REQ-D-X")),
            ("profile_ids", strs(&["p"])),
            ("kind", s("instruction")),
            ("statement", s("s")),
            ("insns", strs(&["add", "sub"])),
            ("source_refs", source_refs()),
            ("applicability", s("included")),
            ("research_status", s("resolved")),
            ("implementation_status", s("planned")),
            (
                "source_semantics",
                obj(vec![("category", s("defined")), ("detail", s("d"))]),
            ),
            ("risk", s("low")),
            ("obligation_ids", strs(&["OB-X"])),
            ("dependencies", Value::List(vec![])),
            ("implementation_refs", Value::List(vec![])),
            ("evidence_ids", Value::List(vec![])),
        ]),
    );
    write_record(
        &dir.join("contract-obligations.sexp"),
        obligation(
            "OB-X",
            "cpu-guarantee",
            "architecture",
            &["CHK-X-POS", "CHK-X-NEG"],
        ),
    );
    write(
        &dir.join("state.sexp"),
        "(state (profile_id \"p\") (xlen 64)\n  (integer_registers (count 32) (width_bits 64) (reset (value \"0\") (authority laboratory) (source \"S\") (statement \"r\"))))\n",
    );
}

fn obligation(id: &str, direction: &str, authority: &str, checks: &[&str]) -> Value {
    let profile = &id[id.len() - 1..].to_ascii_lowercase();
    obj(vec![
        ("id", s(id)),
        ("contract_id", s("c")),
        ("contract_version", s("0")),
        ("profile_ids", strs(&[profile])),
        ("direction", s(direction)),
        ("statement", s("s")),
        ("authority", s(authority)),
        ("source_refs", source_refs()),
        ("parameters", obj(vec![])),
        ("dependencies", Value::List(vec![])),
        ("required_checks", strs(checks)),
    ])
}

/// A device-model unit's documents: the declaration, one register with or without a reset, one obligation.
fn device_docs(dir: &Path, reset: &str, checks: &[&str]) {
    write(
        &dir.join("profile.sexp"),
        "(profile (id \"d\") (version \"0\") (status \"experimental\")\n  (vehicle (route device-model) (comparison register-expectations) (authority laboratory) (source \"s\"))\n  (scope (count_total 2) (authority platform) (source \"S §1\") (mmio_registers \"UART_RXDATA\" \"UART_TXDATA\"))\n  (decision (id \"D-X\") (authority laboratory) (statement \"s\") (source \"S §1\")))\n",
    );
    write(
        &dir.join("state.sexp"),
        &format!("(state (profile_id \"d\") (note \"n\")\n  (special_registers (register (id \"uart_rxdata\") (width_bits 8) (holds \"h\") (authority architecture) (source \"s\") {reset})))\n"),
    );
    write_record(
        &dir.join("contract-obligations.sexp"),
        obligation("OB-D", "device-guarantee", "platform", checks),
    );
}

fn encoding(dir: &Path, profile: &str, ilen: u32) {
    write(
        &dir.join("encoding.sexp"),
        &format!("(encoding (profile \"{profile}\") (ilen {ilen})\n  (compose (base \"riscv/t\") (extensions))\n  (fragment-root \"definitions\"))\n"),
    );
}

/// The RED/GREEN controls: a scratch corpus of two instruction units, then the sibling-crate, device-model and
/// profile-resolution legs, as the script built them.
fn self_test(repo: &Path, verbose: bool) -> bool {
    let Ok(t) = scratch(repo, "target/doctrine-selftest", "extraction") else {
        eprintln!("EXTRACTION self-test: cannot create a scratch directory under target/doctrine-selftest");
        return false;
    };
    for d in ["definitions/riscv", "profiles/good", "profiles/bad"] {
        let _ = fs::create_dir_all(t.join(d));
    }
    let frag = || {
        write(
            &t.join("definitions/riscv/t.sexp"),
            "(fragment (id \"riscv/t\") (kind extension)\n(insn (name add) (fixed (6 2 0x13) (1 0 0x3)) (operands rd rs1 rs2))\n(insn (name sub) (fixed (6 2 0x13) (1 0 0x3)) (operands rd rs1 rs2)))\n",
        )
    };
    let sem = |rules: &str| {
        write(
            &t.join("definitions/riscv/t.sem.sexp"),
            &format!("(semantics (fragment \"riscv/t\") (xlen 64)\n{rules}\n)\n"),
        )
    };
    let both = format!("{RULE}\n{RULE2}");
    let mut tally = Tally {
        repo,
        root: &t,
        pass: 0,
        fail: 0,
        verbose,
    };
    frag();
    sem(&both);
    unit_docs(&t.join("profiles/good"));
    sem(&both);
    unit_docs(&t.join("profiles/bad"));
    tally.score("Python extraction/expansion controls discriminate");
    tally.arm(
        "GREEN a sufficient unit is discovered and judged",
        0,
        "SUFFICIENT",
    );
    sem(RULE);
    unit_docs(&t.join("profiles/bad")); // bad loses sub's semantics
    tally.arm(
        "RED   a unit missing one instruction's semantics",
        1,
        "does not cover: sub",
    );
    // ── the sibling-crate leg (P3-BREADTH.7, case dsp56300-lab-v0) ──
    sem(&both); // restore the shared fragment's full semantics — good/bad are green again
    let sibling = t.join("profiles/sibling");
    let _ = fs::create_dir_all(&sibling);
    write(
        &sibling.join("profile.sexp"),
        "(profile (id \"s\") (version \"0\") (status \"experimental\") (architecture \"D\")\n  (vehicle (route sibling-crate) (comparison checkpoint-end-state) (authority laboratory) (source \"s\"))\n  (scope (count_base 2) (count_total 2) (demo \"MOV\" \"NOP\"))\n  (decision (id \"D-X\") (authority laboratory) (statement \"s\") (source \"S §1\")))\n",
    );
    tally.arm(
        "GREEN a declared sibling-crate unit is reported by name",
        0,
        "sibling-crate route declared",
    );
    encoding(&sibling, "s", 24);
    tally.arm(
        "RED   a sibling-crate declaration contradicted by an encoding.sexp",
        1,
        "contradicts the documents",
    );
    let _ = fs::remove_dir_all(&sibling);
    // ── the device-model leg (P5-BOARD.2, case sifive-uart-lab-v0): no instruction pipeline, so the
    // encoding/semantics/integrative claim is n/a — but every state element carries a reset and every obligation
    // its checks, both ways.
    let device = t.join("profiles/device");
    let _ = fs::create_dir_all(&device);
    device_docs(&device, RESET, &["CHK-D-POS", "CHK-D-NEG"]);
    tally.arm(
        "GREEN a declared device-model unit: resets everywhere, obligations both ways",
        0,
        "device-model route declared",
    );
    encoding(&device, "d", 8);
    tally.arm(
        "RED   a device-model declaration contradicted by an encoding.sexp",
        1,
        "contradicts the documents",
    );
    let _ = fs::remove_file(device.join("encoding.sexp"));
    device_docs(&device, "", &["CHK-D-POS", "CHK-D-NEG"]);
    tally.arm(
        "RED   a device register without a reset",
        1,
        "carries no (reset …)",
    );
    device_docs(&device, RESET, &["CHK-D-POS"]);
    tally.arm(
        "RED   a device obligation with no negative fixture",
        1,
        "positive AND a negative",
    );
    let _ = fs::remove_dir_all(&device);
    // ── the profile-resolution leg (P4-SYSTEM.1, case rv64gc-lab-v0): the selection is resolved and citable; the
    // definition pipeline has not started. The obligation leg still applies; a definition-pipeline document beside
    // the declaration is a contradiction, refused.
    let resolution = t.join("profiles/resolution");
    let _ = fs::create_dir_all(&resolution);
    write(
        &resolution.join("profile.sexp"),
        "(profile (id \"r\") (version \"0\") (status \"development\")\n  (vehicle (route profile-resolution) (authority laboratory) (source \"s\"))\n  (scope (count_total 1) (authority architecture) (source \"S §1\") (base_op \"ADD\"))\n  (decision (id \"D-X\") (authority laboratory) (statement \"s\") (source \"S §1\")))\n",
    );
    write_record(
        &resolution.join("contract-obligations.sexp"),
        obligation(
            "OB-R",
            "cpu-guarantee",
            "laboratory",
            &["CHK-R-POS", "CHK-R-NEG"],
        ),
    );
    tally.arm(
        "GREEN a declared profile-resolution unit: obligations both ways, no pipeline yet",
        0,
        "profile-resolution route declared",
    );
    encoding(&resolution, "r", 32);
    tally.arm(
        "RED   a profile-resolution declaration contradicted by an encoding.sexp",
        1,
        "contradicts the documents",
    );
    let _ = fs::remove_dir_all(&resolution);
    let _ = fs::remove_dir_all(t.join("profiles/good"));
    let _ = fs::remove_dir_all(t.join("profiles/bad"));
    tally.arm("REFUSE an empty corpus, never pass it", 2, "cannot judge");
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "EXTRACTION --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}

/// `cargo xtask check-extraction [--self-test]`: the shell driver's verdict lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    if !self_test(root, false) {
        eprintln!("EXTRACTION: REFUSED — the check does not discriminate (self-test failed).");
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
            eprintln!("EXTRACTION: REFUSED — the unit corpus could not be read.");
            for line in &body {
                eprintln!("  {line}");
            }
            ExitCode::from(2)
        }
        0 => {
            println!("EXTRACTION: ok ({count} unit(s) sufficient — P1-LAB may cite this)");
            ExitCode::SUCCESS
        }
        _ => {
            eprintln!("EXTRACTION: a unit's definition is not sufficient for an engine.");
            for line in &body {
                eprintln!("  {line}");
            }
            eprintln!(
                "  The definition is the authority. Fix the corpus, or model code does not start."
            );
            ExitCode::from(1)
        }
    }
}
