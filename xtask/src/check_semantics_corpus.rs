//! The `SEMANTICS` doctrine's driver, ported from `scripts/check_semantics_corpus.sh` (`XTASK.6` slice `6ah`), which
//! is now a shim of `cargo xtask check-semantics-corpus`.
//!
//! The execution authority's corpus must hold: every semantics document pairs with the fragment beside it and checks
//! against it (`scripts/check_semantics.py`, the pinned judge, spawned as the driver spawned it), every unit's composed
//! fragments refine without a silent redefinition (`check_semantics.compose`, run through `python3 -` as the inline
//! Python called it), and the citations arm judges the tracked corpus when the pinned pages are present or names its
//! skip. The encoding documents are read through the harness's own reader (`sexp.rs`, equal to the pinned
//! `scripts/sexp.py`); the controls write the script's synthetic fragments, semantics and unit. Each self-test arm is
//! one `tally.arm(` call, the idiom the `DERIVED-COUNTS` arm total counts.

use std::fs;
use std::io::Write;
use std::path::{Path, PathBuf};
use std::process::{Command, ExitCode, Stdio};

use crate::harness::{py_splitlines, py_strip, scratch};
use crate::sexp::{self, Sexp};

/// `SEM.compose(present)` with its stdout captured, as the inline Python ran it.
const COMPOSE: &str = r#"import contextlib, io, sys
from pathlib import Path
sys.path.insert(0, "scripts")
import check_semantics as SEM
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = SEM.compose([Path(p) for p in sys.argv[1:]])
sys.stdout.write(buf.getvalue())
sys.exit(rc)
"#;

/// `CIT.artifacts_available(root)` with the inline Python's exception tuple: 0 present, 1 absent, 2 refused (the text
/// on stdout).
const AVAILABILITY: &str = r#"import sys
from pathlib import Path
sys.path.insert(0, "scripts")
import sexp as _sexp
import check_citations as CIT
try:
    sys.exit(0 if CIT.artifacts_available(Path(sys.argv[1])) else 1)
except (CIT.CitationError, _sexp.SexpError, KeyError, OSError) as exc:
    print(exc)
    sys.exit(2)
"#;

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

/// `python3 - <args>` with `program` on stdin, from the repository: exit status, stdout, stderr.
fn python_program(repo: &Path, program: &str, args: &[&str]) -> (i32, String, String) {
    let mut command = Command::new("python3");
    command
        .arg("-")
        .args(args)
        .current_dir(repo)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped());
    let Ok(mut child) = command.spawn() else {
        return (-1, String::new(), "cannot run python3".to_owned());
    };
    if let Some(mut stdin) = child.stdin.take() {
        let _ = stdin.write_all(program.as_bytes());
    }
    match child.wait_with_output() {
        Ok(o) => (
            o.status.code().unwrap_or(-1),
            String::from_utf8_lossy(&o.stdout).into_owned(),
            String::from_utf8_lossy(&o.stderr).into_owned(),
        ),
        Err(e) => (-1, String::new(), e.to_string()),
    }
}

/// `python3 scripts/<script> <args>` from the repository: exit status, stdout, stderr.
fn python_script(repo: &Path, script: &str, args: &[&str]) -> (i32, String, String) {
    match Command::new("python3")
        .arg(script)
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

fn tracked(root: &Path, glob: &str) -> Vec<PathBuf> {
    Command::new("git")
        .args(["ls-files", "--", glob])
        .current_dir(root)
        .output()
        .map(|o| {
            py_splitlines(&String::from_utf8_lossy(&o.stdout))
                .into_iter()
                .filter(|l| !py_strip(l).is_empty())
                .map(|l| root.join(l))
                .collect()
        })
        .unwrap_or_default()
}

fn walk_sem(dir: &Path, out: &mut Vec<PathBuf>) {
    let Ok(entries) = fs::read_dir(dir) else {
        return;
    };
    for entry in entries.flatten() {
        let path = entry.path();
        if path.is_dir() {
            walk_sem(&path, out);
        } else if path
            .file_name()
            .is_some_and(|n| n.to_string_lossy().ends_with(".sem.sexp"))
        {
            out.push(path);
        }
    }
}

fn relative(path: &Path, root: &Path) -> String {
    path.strip_prefix(root)
        .unwrap_or(path)
        .display()
        .to_string()
}

/// Python's `str()` of a read value: a symbol's or string's text, else the reader's repr.
fn shown(value: &Sexp) -> String {
    value
        .text()
        .map_or_else(|| sexp::py_repr(value), str::to_owned)
}

/// The inline Python, line for line.
fn check_corpus(repo: &Path, root: &Path, mode: Mode) -> Verdict {
    let (mut sem_files, mut unit_docs) = match mode {
        Mode::Git => (
            tracked(root, "definitions/**/*.sem.sexp"),
            tracked(root, "profiles/*/encoding.sexp"),
        ),
        Mode::Fs => {
            let mut sems = Vec::new();
            walk_sem(&root.join("definitions"), &mut sems);
            let mut units: Vec<PathBuf> = fs::read_dir(root.join("profiles"))
                .map(|entries| {
                    entries
                        .flatten()
                        .map(|e| e.path().join("encoding.sexp"))
                        .filter(|p| p.is_file())
                        .collect()
                })
                .unwrap_or_default();
            sems.sort();
            units.sort();
            (sems, units)
        }
    };
    if mode == Mode::Git {
        // `tracked` keeps git's order, as the Python did.
        let _ = (&mut sem_files, &mut unit_docs);
    }
    let mut out: Vec<String> = Vec::new();
    let mut findings: Vec<String> = Vec::new();
    let mut notes: Vec<String> = Vec::new();
    let mut checked = 0u32;
    if sem_files.is_empty() {
        return Verdict {
            rc: 2,
            lines: vec![
                "SEMANTICS: REFUSED — no semantics document found; this check cannot judge"
                    .to_owned(),
                "__CHECKED__ 0".to_owned(),
            ],
        };
    }
    for sem_path in &sem_files {
        let name = sem_path
            .file_name()
            .map(|n| n.to_string_lossy().into_owned())
            .unwrap_or_default();
        let frag_name = name.replace(".sem.sexp", ".sexp");
        let frag_path = sem_path.with_file_name(&frag_name);
        checked += 1;
        let rel = relative(sem_path, root);
        if !frag_path.is_file() {
            findings.push(format!("ORPHAN {rel}: no fragment {frag_name} beside it — semantics without their encodings"));
            continue;
        }
        let (rc, stdout, stderr) = python_script(
            repo,
            "scripts/check_semantics.py",
            &[
                &frag_path.display().to_string(),
                &sem_path.display().to_string(),
            ],
        );
        if rc != 0 {
            let mut errs: Vec<String> = py_splitlines(&stdout)
                .into_iter()
                .filter(|l| l.starts_with("  "))
                .map(|l| py_strip(l).to_owned())
                .collect();
            if errs.is_empty() {
                errs.push(py_strip(&stderr).to_owned());
            }
            findings.push(format!(
                "INVALID {rel}: {}",
                errs.iter().take(2).cloned().collect::<Vec<_>>().join(" | ")
            ));
        } else {
            let last = py_splitlines(&stdout)
                .into_iter()
                .find(|l| l.contains("declared instruction(s) have checked semantics"))
                .map(|l| py_strip(l).to_owned());
            out.push(format!(
                "  PAIR {rel}: {}",
                last.unwrap_or_else(|| "ok".to_owned())
            ));
        }
    }
    for doc in &unit_docs {
        let rel = relative(doc, root);
        let shown_doc = doc.display().to_string();
        let read: Result<(Sexp, Vec<String>), sexp::SexpError> = (|| {
            let forms = sexp::read_file(doc)?;
            // `_sexp.read_file(doc)[0]` on a form-less document raised IndexError past the `try` (a traceback, status 1);
            // here it is an UNREADABLE finding — the second intended difference, on a path no corpus has.
            let enc = forms
                .into_iter()
                .next()
                .ok_or_else(|| sexp::SexpError(format!("{shown_doc}: no form in the document")))?;
            let comp = sexp::children(&enc, "compose")?;
            let Some(first) = comp.first() else {
                return Ok((enc, Vec::new()));
            };
            let mut names = vec![shown(sexp::field(first, "base", &shown_doc)?)];
            for e in sexp::children(first, "extensions")? {
                if let Sexp::List(items) = e {
                    names.extend(items.iter().skip(1).map(shown));
                }
            }
            Ok((enc, names))
        })();
        let (enc, names) = match read {
            Ok(v) => v,
            Err(e) => {
                findings.push(format!("UNREADABLE {rel}: {}", e.0));
                continue;
            }
        };
        if names.is_empty() {
            continue;
        }
        // `_sexp.field(enc, "fragment-root", str(doc))` outside the inline `try`: a missing root ended the Python with
        // a traceback (status 1); here it is reported as a finding — the one intended difference, on a path no corpus has.
        let frag_root = match sexp::field(&enc, "fragment-root", &shown_doc) {
            Ok(v) => doc
                .parent()
                .and_then(Path::parent)
                .and_then(Path::parent)
                .unwrap_or(root)
                .join(shown(v)),
            Err(e) => {
                findings.push(format!("UNREADABLE {rel}: {}", e.0));
                continue;
            }
        };
        let present: Vec<String> = names
            .iter()
            .map(|n| frag_root.join(format!("{n}.sem.sexp")))
            .filter(|p| p.is_file())
            .map(|p| p.display().to_string())
            .collect();
        checked += 1;
        if present.len() < 2 {
            continue;
        }
        let args: Vec<&str> = present.iter().map(String::as_str).collect();
        let (rc, stdout, _stderr) = python_program(repo, COMPOSE, &args);
        if rc != 0 {
            let joined: Vec<String> = py_splitlines(&stdout)
                .into_iter()
                .map(|l| py_strip(l).to_owned())
                .filter(|l| !l.is_empty())
                .collect();
            findings.push(format!("REFINEMENT {rel}: {}", joined.join(" | ")));
        }
    }
    if mode == Mode::Git {
        let (rc, stdout, _) = python_program(repo, AVAILABILITY, &[&root.display().to_string()]);
        match rc {
            0 => {
                checked += 1;
                let (crc, cout, cerr) = python_script(repo, "scripts/check_citations.py", &["--corpus"]);
                if crc != 0 {
                    let err_lines = py_splitlines(py_strip(&cerr));
                    let out_lines = py_splitlines(py_strip(&cout));
                    let last = if err_lines.is_empty() { out_lines.last().copied() } else { err_lines.last().copied() };
                    findings.push(format!("CITATIONS: {}", last.unwrap_or("")));
                }
            }
            1 => notes.push("CITATIONS: NAMED SKIP — neither the fetched working area nor the manifest-verified materials cache is present; locators cannot be judged offline. Run scripts/materials.py --fetch; a check that cannot judge never reports green.".to_owned()),
            _ => findings.push(format!("CITATIONS: REFUSED — {}", stdout.trim_end_matches('\n'))),
        }
    } else {
        notes.push("CITATIONS: NAMED SKIP — self-test mode judges synthetic locators never; the citation arm runs on the tracked corpus only.".to_owned());
    }
    out.extend(findings.iter().cloned());
    out.extend(notes);
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
        let verdict = check_corpus(self.repo, self.root, Mode::Fs);
        let out = verdict.text();
        if verdict.rc != expected {
            self.fail += 1;
            if self.verbose {
                eprintln!(
                    "SEMANTICS self-test MISS: {name} expected rc={expected} got rc={}\n{out}",
                    verdict.rc
                );
            }
        } else if !out.contains(want) {
            self.fail += 1;
            if self.verbose {
                eprintln!("SEMANTICS self-test MISS: {name} right verdict, wrong reason (no {want})\n{out}");
            }
        } else {
            self.pass += 1;
        }
    }
}

fn write(path: &Path, text: &str) {
    if let Some(parent) = path.parent() {
        let _ = fs::create_dir_all(parent);
    }
    let _ = fs::write(path, text);
}

const RULE: &str =
    "(sem (insn add) (source \"S §1 — why\") (effect (set (reg rd) (add (reg rs1) (reg rs2)))))";
const RULE2: &str =
    "(sem (insn mul) (source \"S §2 — why\") (effect (set (reg rd) (add (reg rs1) (reg rs2)))))";

/// The RED/GREEN controls over the script's synthetic fragment, semantics and unit.
fn self_test(repo: &Path, verbose: bool) -> bool {
    let Ok(t) = scratch(repo, "target/doctrine-selftest", "semantics") else {
        eprintln!(
            "SEMANTICS self-test: cannot create a scratch directory under target/doctrine-selftest"
        );
        return false;
    };
    let _ = fs::create_dir_all(t.join("definitions/riscv"));
    let _ = fs::create_dir_all(t.join("profiles/p"));
    let frag = || {
        write(
            &t.join("definitions/riscv/t.sexp"),
            "(fragment (id \"riscv/t\") (kind extension)\n(insn (name add) (fixed (31 25 0x0) (14 12 0x0) (6 2 0x13) (1 0 0x3)) (operands rd rs1 rs2))\n(insn (name mul) (fixed (31 25 0x0) (14 12 0x0) (6 2 0x13) (1 0 0x3)) (operands rd rs1 rs2)))\n",
        )
    };
    let sem = |rules: &str| {
        write(
            &t.join("definitions/riscv/t.sem.sexp"),
            &format!("(semantics (fragment \"riscv/t\") (xlen 64)\n{rules}\n)\n"),
        )
    };
    let unit = |extensions: &str| {
        write(
            &t.join("profiles/p/encoding.sexp"),
            &format!("(encoding (profile \"p\") (ilen 32)\n  (compose (base \"riscv/t\"){extensions})\n  (fragment-root \"definitions\"))\n"),
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
    unit("");
    tally.arm(
        "GREEN a complete, cited corpus composes",
        0,
        "have checked semantics",
    );
    frag();
    sem(RULE);
    unit("");
    tally.arm(
        "RED   an uncovered declared instruction",
        1,
        "have NO semantics",
    );
    frag();
    sem("(sem (insn add) (effect (nop)))");
    unit("");
    tally.arm(
        "RED   a rule citing nothing",
        1,
        "missing required field \"source\"",
    );
    frag();
    sem(&format!(
        "(sem (insn add) (source \"S §1\") (effect (widget rd)))\n{RULE2}"
    ));
    unit("");
    tally.arm(
        "RED   a form the language refuses, by name",
        1,
        "form head \"widget\" is not one of",
    );
    frag();
    sem(&both);
    write(
        &t.join("definitions/riscv/u.sexp"),
        "(fragment (id \"riscv/u\") (kind isa-extension) (requires \"riscv/t\"))\n",
    );
    write(
        &t.join("definitions/riscv/u.sem.sexp"),
        &format!("(semantics (fragment \"riscv/u\") (xlen 64)\n{RULE2}\n)\n"),
    );
    unit(" (extensions \"riscv/u\")");
    tally.arm(
        "RED   a silent override across a unit's fragments",
        1,
        "SILENT REDEFINITION",
    );
    let _ = fs::remove_file(t.join("definitions/riscv/u.sexp"));
    let _ = fs::remove_file(t.join("definitions/riscv/u.sem.sexp"));
    frag();
    sem(&both);
    write(
        &t.join("definitions/riscv/v.sexp"),
        "(fragment (id \"riscv/v\") (kind isa-extension) (requires \"riscv/t\"))\n",
    );
    write(
        &t.join("definitions/riscv/w.sexp"),
        "(fragment (id \"riscv/w\") (kind isa-extension) (requires \"riscv/t\"))\n",
    );
    write(
        &t.join("definitions/riscv/w.sem.sexp"),
        &format!("(semantics (fragment \"riscv/w\") (xlen 64)\n{RULE2}\n)\n"),
    );
    unit(" (extensions \"riscv/v\") (extensions \"riscv/w\")");
    tally.arm(
        "RED   a silent override in the SECOND extensions form (the dropped-form regression)",
        1,
        "SILENT REDEFINITION",
    );
    if let Ok(entries) = fs::read_dir(t.join("definitions/riscv")) {
        for e in entries.flatten() {
            if e.file_name().to_string_lossy().ends_with(".sem.sexp") {
                let _ = fs::remove_file(e.path());
            }
        }
    }
    unit("");
    tally.arm("REFUSE an empty corpus, never pass it", 2, "cannot judge");
    frag();
    sem(&both);
    unit("");
    tally.arm(
        "GREEN the citation arm names its skip when the cache is absent",
        0,
        "NAMED SKIP",
    );
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "SEMANTICS --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}

/// `cargo xtask check-semantics-corpus [--self-test]`: the shell driver's verdict lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    if !self_test(root, false) {
        eprintln!("SEMANTICS: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    let controls = Command::new("python3")
        .args(["scripts/check_citations.py", "--self-test"])
        .current_dir(root)
        .stdin(Stdio::null())
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .status()
        .is_ok_and(|s| s.success());
    if !controls {
        eprintln!("SEMANTICS: REFUSED — citation identity/locator controls failed.");
        return ExitCode::from(2);
    }
    let verdict = check_corpus(root, root, Mode::Git);
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
            eprintln!("SEMANTICS: REFUSED — the semantics corpus could not be read.");
            for line in &body {
                eprintln!("  {line}");
            }
            ExitCode::from(2)
        }
        0 => {
            println!("SEMANTICS: ok ({count} check(s) — pairs, refinement rule, citations)");
            ExitCode::SUCCESS
        }
        _ => {
            eprintln!("SEMANTICS: the execution authority's corpus does not hold.");
            for line in &body {
                eprintln!("  {line}");
            }
            eprintln!("  The corpus is authoritative. Fix the semantics, or they do not execute.");
            ExitCode::from(1)
        }
    }
}
