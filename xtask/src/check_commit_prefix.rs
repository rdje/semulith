//! The `COMMIT-PREFIX` doctrine (`PREFIX-DISCIPLINE.1`), ported from `scripts/check_commit_prefix.sh`
//! (`XTASK.6` slice `6b`), which is now a shim of `cargo xtask check-commit-prefix`.
//!
//! The director ruled 2026-09-30: the work-unit prefix is SEMULITH, never SEMILITH. History is immutable,
//! so the doctrine watches the boundary where new subjects enter: `.githooks/commit-msg` must refuse a
//! subject whose leading work-unit id does not begin with `SEMULITH-`, naming SEMULITH, and must accept one
//! that does. The hook is a neutral scaffold file, so a scaffold sync reverts the pin silently; this probe
//! makes that loud at the next commit. It is behavioural, never textual: it runs the hook on two synthetic
//! messages and judges what the hook does. Each self-test arm is one `tally.arm(` call, the idiom the
//! `DERIVED-COUNTS` arm total counts in a shim's module.

use std::fs;
use std::path::Path;
use std::process::{Command, ExitCode};

use crate::harness::{combined, scratch};

/// The hook whose behaviour the doctrine watches.
const HOOK: &str = ".githooks/commit-msg";
/// The pinned work-unit prefix.
const PINNED: &str = "SEMULITH-";
/// The misspelling the pin refuses.
const MISSPELLED: &str = "SEMILITH-";

/// Runs the doctrine: `--self-test` as the first argument runs the arms; anything else runs the check.
/// Exit 0 ok, 1 the hook does not pin the prefix, 2 refused.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    if !self_test(root, false) {
        eprintln!("COMMIT-PREFIX: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    if !root.join(HOOK).is_file() {
        eprintln!(
            "COMMIT-PREFIX: REFUSED — {HOOK} does not exist; the boundary this doctrine watches is gone."
        );
        return ExitCode::from(2);
    }
    let (findings, _) = probe(root, Path::new(HOOK));
    if !findings.is_empty() {
        eprintln!(
            "COMMIT-PREFIX: the commit-msg hook does not pin the SEMULITH- work-unit prefix."
        );
        for finding in &findings {
            eprintln!("  {finding}");
        }
        eprintln!("  The prefix is SEMULITH, never SEMILITH (director ruling 2026-09-30,");
        eprintln!(
            "  decision_work-unit-prefix-semulith). If a scaffold sync reverted the neutral hook,"
        );
        eprintln!("  restore the pin — the ruling stands.");
        return ExitCode::from(1);
    }
    println!("COMMIT-PREFIX: ok (the hook refuses SEMILITH- naming SEMULITH, accepts SEMULITH-)");
    ExitCode::SUCCESS
}

/// Runs `hook` (relative to the root, or absolute) on a misspelled and a pinned synthetic subject. Returns
/// one finding per breach and the probe's text as the script printed it (the findings, then
/// `__CHECKED__ 2`).
fn probe(root: &Path, hook: &Path) -> (Vec<String>, String) {
    let shown = hook.display();
    let mut findings = Vec::new();
    let outcome = scratch(root, "target/doctrine_scratch", "commit-prefix").and_then(|d| {
        let bad = d.join("msg-bad");
        let good = d.join("msg-good");
        fs::write(
            &bad,
            format!("{MISSPELLED}PX-0001 (leaf PREFIX-DISCIPLINE.1): a misspelled prefix\n"),
        )?;
        fs::write(
            &good,
            format!("{PINNED}PX-0001 (leaf PREFIX-DISCIPLINE.1): the pinned prefix\n"),
        )?;
        let hook_run = |message: &Path| {
            combined(
                Command::new("bash")
                    .arg(hook)
                    .arg(message)
                    .current_dir(root),
            )
        };
        let results = (hook_run(&bad), hook_run(&good));
        fs::remove_dir_all(&d)?;
        Ok(results)
    });
    let ((rc_bad, out_bad), (rc_good, _)) = match outcome {
        Ok(results) => results,
        Err(error) => {
            let reason = format!("PROBE FAILED: cannot write the synthetic messages: {error}");
            return (vec![reason.clone()], format!("{reason}\n__CHECKED__ 2"));
        }
    };
    if rc_bad == 0 {
        findings.push(format!(
            "NOT REFUSED: a {MISSPELLED} subject passed {shown} — the pin is absent or dead"
        ));
    } else if !out_bad.contains("SEMULITH") {
        findings.push(format!("WRONG REASON: the {MISSPELLED} subject was refused but the refusal does not name SEMULITH — red for nothing is not the pin"));
    }
    if rc_good != 0 {
        findings.push(format!("OVER-TIGHT: a {PINNED} subject is refused by {shown} — the pin rejects the spelling it exists to protect"));
    }
    let mut text: Vec<String> = findings.clone();
    text.push("__CHECKED__ 2".to_owned());
    (findings, text.join("\n"))
}

/// The self-test's pass and fail counts; `verbose` prints misses on stderr and the summary on stdout.
struct Tally {
    pass: u32,
    fail: u32,
    verbose: bool,
}

impl Tally {
    /// One arm: probing `fixture` must give the verdict `expected` (0 no finding, 1 a finding) and its text
    /// must contain `want`.
    fn arm(&mut self, root: &Path, fixture: &Path, name: &str, expected: i32, want: &str) {
        let (findings, out) = probe(root, fixture);
        let rc = i32::from(!findings.is_empty());
        if rc != expected {
            self.fail += 1;
            if self.verbose {
                eprintln!("COMMIT-PREFIX self-test MISS: {name} expected rc={expected} got rc={rc}\n{out}");
            }
        } else if !out.contains(want) {
            self.fail += 1;
            if self.verbose {
                eprintln!("COMMIT-PREFIX self-test MISS: {name} right verdict, wrong reason (no {want})\n{out}");
            }
        } else {
            self.pass += 1;
        }
    }
}

/// The pre-pin hook — identifier-shape check only, no prefix pin: what a scaffold sync restores.
const HOOK_UNPINNED: &str = r#"#!/usr/bin/env bash
subject="$(head -1 "$1")"
if ! printf '%s' "$subject" | grep -Eq '^[A-Za-z][A-Za-z0-9._-]+'; then
  echo "commit-msg: subject must begin with an identifier-shaped work-unit id" >&2
  exit 1
fi
exit 0
"#;
/// An always-refusing hook — red, but for no reason; it refuses the pinned spelling too.
const HOOK_REFUSE_ALL: &str = "#!/usr/bin/env bash\necho \"commit-msg: no\" >&2\nexit 1\n";
/// An over-tight hook — refuses everything, naming SEMULITH: the right reason, the wrong reach.
const HOOK_OVER_TIGHT: &str = "#!/usr/bin/env bash\necho \"commit-msg: the work-unit id must begin with SEMULITH-\" >&2\nexit 1\n";
/// A correctly pinned minimal hook — the check is coupled to behaviour, not text.
const HOOK_PINNED: &str = r#"#!/usr/bin/env bash
subject="$(head -1 "$1")"
if ! printf '%s' "$subject" | grep -Eq '^SEMULITH-'; then
  echo "commit-msg: the work-unit id must begin with the pinned project prefix 'SEMULITH-'" >&2
  exit 1
fi
exit 0
"#;

/// The four arms, each against a synthetic hook. Returns whether every arm held.
fn self_test(root: &Path, verbose: bool) -> bool {
    let mut tally = Tally {
        pass: 0,
        fail: 0,
        verbose,
    };
    let t = match scratch(root, "target/doctrine-selftest", "commit-prefix") {
        Ok(dir) => dir,
        Err(error) => {
            if verbose {
                eprintln!("COMMIT-PREFIX self-test: cannot create a scratch directory: {error}");
            }
            return false;
        }
    };
    let fixture = |name: &str, text: &str| {
        let path = t.join(name);
        fs::write(&path, text).map(|()| path)
    };
    let fixtures = [
        fixture("hook-unpinned", HOOK_UNPINNED),
        fixture("hook-refuse-all", HOOK_REFUSE_ALL),
        fixture("hook-over-tight", HOOK_OVER_TIGHT),
        fixture("hook-pinned", HOOK_PINNED),
    ];
    let [Ok(unpinned), Ok(refuse_all), Ok(over_tight), Ok(pinned)] = fixtures else {
        if verbose {
            eprintln!("COMMIT-PREFIX self-test: cannot write the fixture hooks");
        }
        let _ = fs::remove_dir_all(&t);
        return false;
    };
    tally.arm(
        root,
        &unpinned,
        "RED   an unpinned hook (the scaffold-sync revert)",
        1,
        "NOT REFUSED",
    );
    tally.arm(
        root,
        &refuse_all,
        "RED   an always-refusing hook (red without the reason)",
        1,
        "WRONG REASON",
    );
    tally.arm(
        root,
        &over_tight,
        "RED   an over-tight hook (refuses SEMULITH- too)",
        1,
        "OVER-TIGHT",
    );
    tally.arm(
        root,
        &pinned,
        "GREEN a correctly pinned hook",
        0,
        "__CHECKED__ 2",
    );
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "COMMIT-PREFIX --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}
