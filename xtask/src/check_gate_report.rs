//! The `GATE-REPORT` doctrine's driver, ported from `scripts/check_gate_report.sh` (`XTASK.6` slice `6al`), which is now
//! a shim of `cargo xtask check-gate-report`.
//!
//! A gate report is the one document everything else is summarised INTO: every tracked `profiles/<id>/G?-REPORT.md` and
//! the repo-level cross-architecture report (`BREADTH` → `docs/BREADTH-REPORT.md`) must still be the function of its
//! inputs that `scripts/gate_report.py` computes — a hand-edited report is how a project comes to hold a verdict nothing
//! produced. The generator is spawned as the script spawned it (`--stdout`, stderr discarded), its own `--self-test` and the
//! runtime-root probe run as before; nothing of them is ported. The controls run against the REAL reports (a synthetic
//! profile would be a different function): determinism, the `**Verdict:` marker edit, the tamper's visibility. The two
//! bash arms are two `tally.arm(` calls inside the same two-mode loop, the idiom the `DERIVED-COUNTS` arm total counts.

use std::fs;
use std::path::{Path, PathBuf};
use std::process::{Command, ExitCode, Stdio};

use crate::harness::{on_path, scratch};

const GENERATOR: &str = "scripts/gate_report.py";
const PROBE: &str = "scripts/probe_gate_runtime_root.py";

/// `repo_reports`: gate and path of each repo-level (cross-architecture) report, as the script printed them.
const REPO_REPORTS: &[(&str, &str)] = &[("BREADTH", "docs/BREADTH-REPORT.md")];

/// The shell's `$(…)`: every trailing newline removed.
fn captured(text: &str) -> &str {
    text.trim_end_matches('\n')
}

/// `python3 scripts/gate_report.py [<profile>] --gate <gate> --stdout 2>/dev/null`: the generated report's raw stdout
/// (the process substitutions compared it with its trailing newline; `$(…)` callers strip it).
fn report(repo: &Path, profile: Option<&str>, gate: &str) -> Vec<u8> {
    let mut command = Command::new("python3");
    command.arg(GENERATOR);
    if let Some(profile) = profile {
        command.arg(profile);
    }
    command
        .arg("--gate")
        .arg(gate)
        .arg("--stdout")
        .current_dir(repo)
        .stdin(Stdio::null())
        .stderr(Stdio::null());
    command.output().map(|o| o.stdout).unwrap_or_default()
}

/// `python3 [-O] scripts/probe_gate_runtime_root.py [--mutation …] 2>&1`, captured.
fn probe(repo: &Path, optimized: bool, mutation: Option<&str>) -> (i32, String) {
    let mut command = Command::new("python3");
    if optimized {
        command.arg("-O");
    }
    command.arg(PROBE);
    if let Some(mutation) = mutation {
        command.arg("--mutation").arg(mutation);
    }
    match command.current_dir(repo).stdin(Stdio::null()).output() {
        Ok(o) => {
            let mut text = String::from_utf8_lossy(&o.stdout).into_owned();
            text.push_str(&String::from_utf8_lossy(&o.stderr));
            (o.status.code().unwrap_or(-1), text)
        }
        Err(e) => (-1, e.to_string()),
    }
}

/// `profiles/*/`: the profile directories in the glob's order.
fn profiles(repo: &Path) -> Vec<PathBuf> {
    let mut dirs: Vec<PathBuf> = fs::read_dir(repo.join("profiles"))
        .map(|entries| {
            entries
                .flatten()
                .map(|e| e.path())
                .filter(|p| p.is_dir())
                .collect()
        })
        .unwrap_or_default();
    dirs.sort();
    dirs
}

/// `"${p%/}"/G?-REPORT.md` with `[ -f … ]`: the profile's gate reports in the glob's order, each with its gate
/// (`basename | cut -d- -f1`).
fn gate_reports(profile: &Path) -> Vec<(String, PathBuf)> {
    let mut reports: Vec<PathBuf> = fs::read_dir(profile)
        .map(|entries| {
            entries
                .flatten()
                .map(|e| e.path())
                .filter(|p| {
                    p.is_file()
                        && p.file_name().and_then(|n| n.to_str()).is_some_and(|n| {
                            let mut chars = n.chars();
                            chars.next() == Some('G')
                                && chars.next().is_some()
                                && chars.as_str() == "-REPORT.md"
                        })
                })
                .collect()
        })
        .unwrap_or_default();
    reports.sort();
    reports
        .into_iter()
        .map(|p| {
            let name = p.file_name().and_then(|n| n.to_str()).unwrap_or_default();
            let gate = name.split('-').next().unwrap_or_default().to_owned();
            (gate, p)
        })
        .collect()
}

/// `sed 's/\*\*Verdict:/**Xerdict:/'`: the first occurrence on every line.
fn xerdict(text: &str) -> String {
    let mut out = String::with_capacity(text.len());
    for line in text.split_inclusive('\n') {
        out.push_str(&line.replacen("**Verdict:", "**Xerdict:", 1));
    }
    out
}

struct Tally {
    pass: u32,
    fail: u32,
    verbose: bool,
}

impl Tally {
    /// One arm: the exit status must be `expected` and the captured output must contain `want`.
    fn arm(&mut self, name: &str, rc: i32, expected: i32, out: &str, want: &str) {
        if rc == expected && out.contains(want) {
            self.pass += 1;
        } else {
            self.fail += 1;
            if self.verbose {
                eprintln!(
                    "GATE-REPORT self-test MISS: {name} — rc={rc}, expected {expected}\n{out}"
                );
            }
        }
    }

    /// A plain pass/fail control (the script's `if …; then pass=$((pass+1)) else fail=$((fail+1)); echo MISS`).
    fn control(&mut self, ok: bool, miss: &str) {
        if ok {
            self.pass += 1;
        } else {
            self.fail += 1;
            if self.verbose {
                eprintln!("GATE-REPORT self-test MISS: {miss}");
            }
        }
    }

    /// The three controls over one generated report: determinism, the marker edit alters the text, the tamper shows.
    fn report_controls(&mut self, generated: &str, again: &str, shown: &str) {
        self.control(generated == again, &format!("{shown} is not deterministic"));
        let tmp = xerdict(generated);
        self.control(
            tmp != generated,
            &format!("{shown} control did not alter the text"),
        );
        // `printf '%s' "$tmp" | diff -q - <(printf '%s' "$generated")`: the two texts differ.
        self.control(tmp != generated, &format!("{shown} tamper is undetectable"));
    }
}

/// The RED/GREEN controls, against the REAL reports — the generator reads a profile directory, and a synthetic one would
/// be a different function. Quiet unless `verbose` (the script ran it `>/dev/null 2>&1` before the real judgement).
fn self_test(repo: &Path, verbose: bool) -> bool {
    let mut tally = Tally {
        pass: 0,
        fail: 0,
        verbose,
    };
    // The CONTRACT MEASURE's own controls (P4-SYSTEM.10 slice a): every report's contract axis is this count, so a
    // measure that stopped discriminating would sync perfectly and still lie.
    let measure = Command::new("python3")
        .arg(GENERATOR)
        .arg("--self-test")
        .current_dir(repo)
        .stdin(Stdio::null())
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .status()
        .is_ok_and(|s| s.success());
    tally.control(
        measure,
        "the contract measure's controls failed (scripts/gate_report.py --self-test)",
    );
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        let (rc, out) = probe(repo, optimized, None);
        tally.arm(
            &format!("GREEN copied runtime root {mode}"),
            rc,
            0,
            captured(&out),
            "GATE-RUNTIME-ROOT: 6 tests / 0 failures / 0 errors; local authority, no capture credit",
        );
        let (rc, out) = probe(repo, optimized, Some("git-root"));
        tally.arm(
            &format!("RED parent Git root fallback {mode}"),
            rc,
            1,
            captured(&out),
            "GATE-RUNTIME-ROOT: 6 tests / 5 failures / 0 errors; local authority, no capture credit",
        );
    }
    // A profile with no report is skipped by the real run too, so it is not a control.
    for profile in profiles(repo) {
        let prof = profile
            .file_name()
            .and_then(|n| n.to_str())
            .unwrap_or_default()
            .to_owned();
        for (gate, _) in gate_reports(&profile) {
            let shown = format!("{prof}/{gate}");
            let generated = String::from_utf8_lossy(&report(repo, Some(&prof), &gate)).into_owned();
            let generated = captured(&generated);
            if generated.is_empty() {
                tally.control(false, &format!("{shown} generated nothing"));
                continue;
            }
            let again = String::from_utf8_lossy(&report(repo, Some(&prof), &gate)).into_owned();
            tally.report_controls(generated, captured(&again), &shown);
        }
    }
    // The repo-level reports (cross-architecture gates): the same three controls.
    for (rgate, rpath) in REPO_REPORTS {
        if !repo.join(rpath).is_file() {
            continue;
        }
        let generated = String::from_utf8_lossy(&report(repo, None, rgate)).into_owned();
        let generated = captured(&generated);
        if generated.is_empty() {
            tally.control(false, &format!("{rpath} generated nothing"));
            continue;
        }
        let again = String::from_utf8_lossy(&report(repo, None, rgate)).into_owned();
        tally.report_controls(generated, captured(&again), rpath);
    }
    if tally.pass == 0 {
        if verbose {
            eprintln!("GATE-REPORT self-test: no profile carried a report to test");
        }
        tally.fail += 1;
    }
    if verbose {
        println!(
            "GATE-REPORT --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}

/// One stale report, as the script explained it: the header, `diff <(generated) report | head -20` indented, the
/// regeneration command. `diff` is spawned on a scratch copy of the generated text, its normal format kept.
fn explain_stale(repo: &Path, generated: &[u8], report_path: &str, regenerate: &str) {
    eprintln!("GATE-REPORT: {report_path} is out of sync with the inputs it is generated from.");
    if let Ok(dir) = scratch(repo, "target/tmp", "gate-report") {
        let copy = dir.join("generated.md");
        let _ = fs::write(&copy, generated);
        if let Ok(o) = Command::new("diff")
            .arg(&copy)
            .arg(report_path)
            .current_dir(repo)
            .stdin(Stdio::null())
            .stderr(Stdio::null())
            .output()
        {
            for line in String::from_utf8_lossy(&o.stdout).lines().take(20) {
                eprintln!("    {line}");
            }
        }
        let _ = fs::remove_dir_all(&dir);
    }
    eprintln!("  Regenerate it — never edit it:");
    eprintln!("    {regenerate}");
    eprintln!(
        "  ⛔ A hand-edited gate report is how a project comes to hold a verdict nothing produced."
    );
}

/// `cargo xtask check-gate-report [--self-test]`: the shell driver's verdict lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    // `command -v python3`
    if !on_path("python3") {
        eprintln!("GATE-REPORT: REFUSED — python3 is not on PATH; this check cannot judge.");
        return ExitCode::from(2);
    }
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    if !root.join("profiles").is_dir() {
        println!("GATE-REPORT: ok (no profiles/ yet)");
        return ExitCode::SUCCESS;
    }
    if !self_test(root, false) {
        eprintln!("GATE-REPORT: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    let mut stale = 0u32;
    let mut checked = 0u32;
    for profile in profiles(root) {
        let prof = profile
            .file_name()
            .and_then(|n| n.to_str())
            .unwrap_or_default()
            .to_owned();
        for (gate, path) in gate_reports(&profile) {
            checked += 1;
            // `diff -q <(report_for "$prof" "$gate") "$report"`: the generator's raw stream against the file's bytes.
            let generated = report(root, Some(&prof), &gate);
            if fs::read(&path).ok().as_deref() != Some(generated.as_slice()) {
                let shown = format!(
                    "profiles/{prof}/{}",
                    path.file_name()
                        .and_then(|n| n.to_str())
                        .unwrap_or_default()
                );
                explain_stale(
                    root,
                    &generated,
                    &shown,
                    &format!("scripts/gate_report.py {prof} --gate {gate}"),
                );
                stale += 1;
            }
        }
    }
    // The repo-level reports (cross-architecture gates), same rule.
    for (rgate, rpath) in REPO_REPORTS {
        if !root.join(rpath).is_file() {
            continue;
        }
        checked += 1;
        let generated = report(root, None, rgate);
        if fs::read(root.join(rpath)).ok().as_deref() != Some(generated.as_slice()) {
            explain_stale(
                root,
                &generated,
                rpath,
                &format!("scripts/gate_report.py --gate {rgate}"),
            );
            stale += 1;
        }
    }
    if stale != 0 {
        return ExitCode::from(1);
    }
    println!("GATE-REPORT: ok ({checked} generated report(s) in sync with their inputs)");
    ExitCode::SUCCESS
}
