//! The `SOURCE-FORMAT` doctrine, ported from `scripts/check_source_format.sh` (`XTASK.6` slice `6ag`), which is now a
//! shim of `cargo xtask check-source-format`.
//!
//! Every source of truth under the four families (`definitions/`, `schema/`, `profiles/`, `materials/`) is an
//! S-expression or it is refused: a `.toml`, `.json`, `.jsonl`, `.yaml` or `.yml` there is the retired format split
//! returning (`decision_one-format-every-source-of-truth`), a `.sexp` the one reader cannot parse is unreadable, and a
//! corpus without a single `.sexp` has nothing for the engine to extract. The driver's inline Python is ported over the
//! harness's own reader (`sexp.rs`, measured equal to the pinned `scripts/sexp.py`, refusal texts included); the
//! shared reader's refusal probe runs as the script ran it, scored plain and optimized. Each self-test arm is one
//! `tally.arm(` call and each probe scoring one `tally.score(` line, the idioms the `DERIVED-COUNTS` arm total counts.

use std::fs;
use std::path::{Path, PathBuf};
use std::process::{Command, ExitCode};

use crate::harness::{combined, scratch};
use crate::sexp;

const FAMILIES: [&str; 4] = ["definitions", "schema", "profiles", "materials"];
const RETIRED: [&str; 5] = [".toml", ".json", ".jsonl", ".yaml", ".yml"];

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

/// `retired.search(str(p))`: the path ends in one of the retired extensions (the `$` anchors it).
fn retired_extension(path: &str) -> Option<&'static str> {
    RETIRED.iter().copied().find(|ext| path.ends_with(ext))
}

fn walk(dir: &Path, out: &mut Vec<PathBuf>) {
    let Ok(entries) = fs::read_dir(dir) else {
        return;
    };
    for entry in entries.flatten() {
        let path = entry.path();
        if path.is_dir() {
            walk(&path, out);
        } else if path.is_file() {
            out.push(path);
        }
    }
}

/// The files of the four families: tracked ones under `git`, everything there under `fs`.
fn paths(root: &Path, mode: Mode) -> Vec<PathBuf> {
    let mut found: Vec<PathBuf> = match mode {
        Mode::Git => Command::new("git")
            .args(["ls-files", "--"])
            .args(FAMILIES)
            .current_dir(root)
            .output()
            .map(|o| {
                String::from_utf8_lossy(&o.stdout)
                    .lines()
                    .filter(|l| !l.trim().is_empty())
                    .map(|l| root.join(l))
                    .collect()
            })
            .unwrap_or_default(),
        Mode::Fs => {
            let mut all = Vec::new();
            for fam in FAMILIES {
                walk(&root.join(fam), &mut all);
            }
            all
        }
    };
    found.sort();
    found
}

/// The inline Python, line for line: every family file judged by its format, every `.sexp` by the one reader.
fn check_source_format(root: &Path, mode: Mode) -> Verdict {
    let all = paths(root, mode);
    let mut findings: Vec<String> = Vec::new();
    let mut corpus: Vec<(PathBuf, String)> = Vec::new();
    for p in &all {
        let shown = p.display().to_string();
        let rel = p
            .strip_prefix(root)
            .map_or_else(|_| shown.clone(), |r| r.display().to_string());
        if let Some(ext) = retired_extension(&shown) {
            findings.push(format!(
                "OUTSIDE FORMAT {rel}: a {ext} file inside a source-of-truth family — the format split is retired (decision_one-format-every-source-of-truth); a source of truth is S-expression or it is refused"
            ));
            continue;
        }
        if shown.ends_with(".sexp") {
            corpus.push((p.clone(), rel));
        }
    }
    if all.is_empty() {
        return Verdict {
            rc: 2,
            lines: vec![
                "SOURCE-FORMAT: REFUSED — no file at all under the source-of-truth families; this check cannot judge an empty corpus".to_owned(),
                "__CHECKED__ 0".to_owned(),
            ],
        };
    }
    if corpus.is_empty() {
        findings.push("NO SEXP SOURCE: not one .sexp under the source-of-truth families — the engine has nothing to extract from".to_owned());
    }
    for (p, rel) in &corpus {
        if let Err(e) = sexp::read_file(p) {
            findings.push(format!(
                "UNREADABLE {rel}: does not parse with scripts/sexp.py — {}",
                e.0
            ));
        }
    }
    let mut lines = findings.clone();
    lines.push(format!("__CHECKED__ {}", corpus.len()));
    Verdict {
        rc: i32::from(!findings.is_empty()),
        lines,
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
        let verdict = check_source_format(self.root, Mode::Fs);
        let out = verdict.text();
        if verdict.rc != expected {
            self.fail += 1;
            if self.verbose {
                eprintln!(
                    "SOURCE-FORMAT self-test MISS: {name} expected rc={expected} got rc={}\n{out}",
                    verdict.rc
                );
            }
        } else if !out.contains(want) {
            self.fail += 1;
            if self.verbose {
                eprintln!("SOURCE-FORMAT self-test MISS: {name} right verdict, wrong reason (no {want})\n{out}");
            }
        } else {
            self.pass += 1;
        }
    }

    /// The script's `score`: the shared reader's refusal probe, plain or optimized, with or without a mutation.
    fn score(
        &mut self,
        label: &str,
        optimized: bool,
        mutation: &str,
        want_rc: i32,
        signature: &str,
    ) {
        let mut command = Command::new("python3");
        if optimized {
            command.arg("-O");
        }
        command.arg(self.repo.join("scripts/probe_sexp_refusals.py"));
        if !mutation.is_empty() {
            command.args(["--mutation", mutation]);
        }
        let (rc, out) = combined(command.current_dir(self.repo));
        if rc != want_rc || !out.contains(signature) {
            self.fail += 1;
            if self.verbose {
                eprintln!(
                    "SOURCE-FORMAT reader MISS: {label} rc={rc} wanted={want_rc}\n{}",
                    out.trim_end_matches('\n')
                );
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

const CLEAN: &str = "SEXP-REFUSALS: 29 tests / 0 failures / 0 errors; fixtures cleaned";

/// The RED/GREEN controls over a scratch corpus, then the shared reader's refusal probe plain and optimized.
fn self_test(repo: &Path, verbose: bool) -> bool {
    let Ok(t) = scratch(repo, "target/doctrine-selftest", "sourceformat") else {
        eprintln!("SOURCE-FORMAT self-test: cannot create a scratch directory under target/doctrine-selftest");
        return false;
    };
    for d in ["definitions", "schema", "profiles/p", "materials"] {
        let _ = fs::create_dir_all(t.join(d));
    }
    let mut tally = Tally {
        repo,
        root: &t,
        pass: 0,
        fail: 0,
        verbose,
    };
    write(
        &t.join("definitions/x.sexp"),
        "(fragment (id \"riscv/x\") (kind extension) (requires \"riscv/rv64i\"))\n",
    );
    tally.arm("GREEN a corpus of well-formed .sexp", 0, "__CHECKED__ 1");
    write(
        &t.join("profiles/p/profile.toml"),
        "[profile]\nid = \"ghost\"\n",
    );
    tally.arm(
        "RED   the split returns: a .toml in a source-of-truth family",
        1,
        "OUTSIDE FORMAT",
    );
    write(
        &t.join("materials/requirements.jsonl"),
        "{\"id\":\"REQ-GHOST\"}\n",
    );
    tally.arm(
        "RED   a records-shaped .jsonl re-committed",
        1,
        "OUTSIDE FORMAT",
    );
    write(
        &t.join("profiles/p/sources.sexp"),
        "(sources (source (id \"A\"\n",
    );
    tally.arm("RED   a .sexp the one reader refuses", 1, "UNREADABLE");
    write(
        &t.join("profiles/p/DOSSIER.md"),
        "# dossier prose, not a source of truth\n",
    );
    write(&t.join("profiles/p/guests.s"), "    add a0, a1, a2\n");
    for f in [
        "profiles/p/profile.toml",
        "materials/requirements.jsonl",
        "profiles/p/sources.sexp",
    ] {
        let _ = fs::remove_file(t.join(f));
    }
    tally.arm(
        "GREEN dossier prose and guest programs are not refused",
        0,
        "__CHECKED__ 1",
    );
    let _ = fs::remove_file(t.join("definitions/x.sexp"));
    tally.arm(
        "RED   a corpus with no .sexp at all — the engine has nothing to extract from",
        1,
        "NO SEXP SOURCE",
    );
    let _ = fs::remove_file(t.join("profiles/p/DOSSIER.md"));
    let _ = fs::remove_file(t.join("profiles/p/guests.s"));
    tally.arm(
        "RED   an empty corpus is refused, not passed",
        2,
        "cannot judge",
    );
    tally.score("GREEN normal shared-reader refusals", false, "", 0, CLEAN);
    tally.score(
        "RED normal omitted reader guard integer-refusal",
        false,
        "integer-refusal",
        1,
        "SEXP-REFUSALS: 29 tests / 6 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted reader guard cli-head",
        false,
        "cli-head",
        1,
        "SEXP-REFUSALS: 29 tests / 3 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted reader guard head-diagnostic",
        false,
        "head-diagnostic",
        1,
        "SEXP-REFUSALS: 29 tests / 3 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted reader guard cli-io",
        false,
        "cli-io",
        1,
        "SEXP-REFUSALS: 29 tests / 3 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted reader guard cli-decode",
        false,
        "cli-decode",
        1,
        "SEXP-REFUSALS: 29 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted reader guard selftest-equality",
        false,
        "selftest-equality",
        1,
        "SEXP-REFUSALS: 29 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted reader guard selftest-arity",
        false,
        "selftest-arity",
        1,
        "SEXP-REFUSALS: 29 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted reader guard selftest-reason",
        false,
        "selftest-reason",
        1,
        "SEXP-REFUSALS: 29 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score("GREEN optimized shared-reader refusals", true, "", 0, CLEAN);
    tally.score(
        "RED optimized omitted reader guard integer-refusal",
        true,
        "integer-refusal",
        1,
        "SEXP-REFUSALS: 29 tests / 6 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted reader guard cli-head",
        true,
        "cli-head",
        1,
        "SEXP-REFUSALS: 29 tests / 3 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted reader guard head-diagnostic",
        true,
        "head-diagnostic",
        1,
        "SEXP-REFUSALS: 29 tests / 3 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted reader guard cli-io",
        true,
        "cli-io",
        1,
        "SEXP-REFUSALS: 29 tests / 3 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted reader guard cli-decode",
        true,
        "cli-decode",
        1,
        "SEXP-REFUSALS: 29 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted reader guard selftest-equality",
        true,
        "selftest-equality",
        1,
        "SEXP-REFUSALS: 29 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted reader guard selftest-arity",
        true,
        "selftest-arity",
        1,
        "SEXP-REFUSALS: 29 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted reader guard selftest-reason",
        true,
        "selftest-reason",
        1,
        "SEXP-REFUSALS: 29 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "SOURCE-FORMAT --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}

/// `cargo xtask check-source-format [--self-test]`: the shell driver's verdict lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    if !self_test(root, false) {
        eprintln!("SOURCE-FORMAT: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    let verdict = check_source_format(root, Mode::Git);
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
            eprintln!("SOURCE-FORMAT: REFUSED — the source-of-truth corpus could not be read.");
            for line in &body {
                eprintln!("  {line}");
            }
            ExitCode::from(2)
        }
        0 => {
            println!("SOURCE-FORMAT: ok ({count} source-of-truth file(s) under definitions/ schema/ profiles/ materials/, all in the one format)");
            ExitCode::SUCCESS
        }
        _ => {
            eprintln!("SOURCE-FORMAT: a source of truth lives outside the one format.");
            for line in &body {
                eprintln!("  {line}");
            }
            eprintln!(
                "  The format decision is authoritative. Convert the file, or it does not land."
            );
            ExitCode::from(1)
        }
    }
}
