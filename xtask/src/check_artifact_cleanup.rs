//! The `ARTIFACT-COHORT` doctrine's driver, ported from `scripts/check_artifact_cleanup.sh` (`XTASK.6` slice `6af`), which
//! is now a shim of `cargo xtask check-artifact-cleanup`.
//!
//! The recurring artifact cleanup's instrument and its controls — planning and checking, the historical helper, the
//! attempt journal, output provenance, the Cargo boundary, strict selection, the guarded core, the operator act — must
//! keep discriminating: every probe suite green and every one of its mutations caught, in the plain and the optimized
//! interpreter, and every instrument and control tracked. No real cleanup runs here. The probes run as the driver ran
//! them (`python3 -B [-O] scripts/probe_*.py [--mutation …]`) and are not ported; each scoring is one `tally.score(`
//! line, the idiom the `DERIVED-COUNTS` arm total counts beside `tally.arm(`, sixteen lines as the script has sixteen.

use std::path::Path;
use std::process::{Command, ExitCode, Stdio};

use crate::harness::combined;

/// The instruments and controls the doctrine requires tracked, in the script's order.
const TRACKED: [&str; 18] = [
    "scripts/artifact_cleanup.py",
    "scripts/probe_artifact_cleanup.py",
    "scripts/probe_legacy_artifact_cleanup.py",
    "scripts/fixtures/artifact_cleanup_0067.py.txt",
    "scripts/artifact_cleanup_journal.py",
    "scripts/probe_artifact_cleanup_journal.py",
    "scripts/artifact_output_provenance.py",
    "scripts/probe_artifact_output_provenance.py",
    "scripts/artifact_cargo.py",
    "scripts/probe_artifact_cargo.py",
    "scripts/artifact_cleanup_selection.py",
    "scripts/probe_artifact_cleanup_selection.py",
    "scripts/artifact_cleanup_guarded.py",
    "scripts/probe_artifact_cleanup_guarded.py",
    "scripts/artifact_cleanup_operator.py",
    "scripts/probe_artifact_cleanup_operator.py",
    "scripts/probe_c_engine.py",
    "scripts/probe_c_guest_image.py",
];

struct Tally<'a> {
    repo: &'a Path,
    optimized: bool,
    pass: u32,
    fail: u32,
}

impl Tally<'_> {
    /// `"${python[@]}" scripts/<probe> [--mutation <m>] 2>&1`: the probe's exit status and output together.
    fn probe(&self, script: &str, mutation: Option<&str>) -> (i32, String) {
        let mut command = Command::new("python3");
        command.arg("-B");
        if self.optimized {
            command.arg("-O");
        }
        command.arg(script);
        if let Some(m) = mutation {
            command.args(["--mutation", m]);
        }
        combined(command.current_dir(self.repo))
    }

    /// The script's `score`: the run's exit status must be `expected` and its output must contain `want`; a miss is
    /// printed as the script printed it (the self-test's output is visible in the main run too).
    fn score(&mut self, name: &str, rc: i32, expected: i32, out: &str, want: &str) {
        if rc == expected && out.contains(want) {
            self.pass += 1;
        } else {
            self.fail += 1;
            eprintln!(
                "ARTIFACT-COHORT self-test MISS: {name} expected rc={expected} reason={want} got rc={rc}\n{}",
                out.trim_end_matches('\n')
            );
        }
    }
}

const ONE_RED: &str = "1 tests / 1 failures / 0 errors";

/// The script's controls, in its order, in the plain and the optimized interpreter.
fn self_test(repo: &Path) -> bool {
    let (mut pass, mut fail) = (0u32, 0u32);
    for mode in ["normal", "optimized"] {
        let mut tally = Tally {
            repo,
            optimized: mode == "optimized",
            pass: 0,
            fail: 0,
        };
        let (rc, out) = tally.probe("scripts/probe_artifact_cleanup.py", None);
        tally.score(
            &format!("GREEN {mode} cohort controls"),
            rc,
            0,
            &out,
            "27 tests / 0 failures / 0 errors",
        );
        for mutation in [
            "release-strays",
            "tracked-ownership",
            "hash-budget",
            "root-binding",
            "plan-shape",
            "exclusive-output",
            "head-inventory",
            "directory-recheck",
            "volume-before-open",
            "git-volume-before-read",
        ] {
            let (rc, out) = tally.probe("scripts/probe_artifact_cleanup.py", Some(mutation));
            tally.score(&format!("RED {mode} {mutation}"), rc, 1, &out, ONE_RED);
        }
        let (rc, out) = tally.probe("scripts/probe_legacy_artifact_cleanup.py", None);
        tally.score(
            &format!("GREEN {mode} historical helper"),
            rc,
            0,
            &out,
            "5 tests / 0 failures / 0 errors",
        );
        let (rc, out) = tally.probe(
            "scripts/probe_legacy_artifact_cleanup.py",
            Some("source-pin"),
        );
        tally.score(
            &format!("RED {mode} historical source pin"),
            rc,
            1,
            &out,
            ONE_RED,
        );
        let (rc, out) = tally.probe("scripts/probe_artifact_cleanup_journal.py", None);
        tally.score(
            &format!("GREEN {mode} attempt journal"),
            rc,
            0,
            &out,
            "29 tests / 0 failures / 0 errors",
        );
        for mutation in [
            "plan-binding",
            "intent-sequence",
            "terminal",
            "exclusive",
            "parent",
            "file",
            "barrier",
            "poison",
            "byte-bound",
            "terminal-tail",
            "approved-range",
        ] {
            let (rc, out) =
                tally.probe("scripts/probe_artifact_cleanup_journal.py", Some(mutation));
            tally.score(
                &format!("RED {mode} journal {mutation}"),
                rc,
                1,
                &out,
                ONE_RED,
            );
        }
        let (rc, out) = tally.probe("scripts/probe_artifact_output_provenance.py", None);
        tally.score(
            &format!("GREEN {mode} output provenance"),
            rc,
            0,
            &out,
            "42 tests / 0 failures / 0 errors",
        );
        for mutation in [
            "changed-digest",
            "successful-build",
            "command-root",
            "recorder-pin",
            "producer-pin",
            "current-fact",
            "tracked-alias",
            "closed-fields",
            "byte-bound",
            "root-binding",
            "root-mapping",
            "return-root",
            "profile-binding",
            "captured-binding",
            "support-pin",
            "support-objects",
            "census-class",
            "observe-unchanged",
            "observe-tracked",
            "publish-lock",
            "publish-pins",
            "publish-readback",
        ] {
            let (rc, out) = tally.probe(
                "scripts/probe_artifact_output_provenance.py",
                Some(mutation),
            );
            tally.score(
                &format!("RED {mode} provenance {mutation}"),
                rc,
                1,
                &out,
                ONE_RED,
            );
        }
        let (rc, out) = tally.probe("scripts/probe_artifact_cargo.py", None);
        tally.score(
            &format!("GREEN {mode} Cargo boundary"),
            rc,
            0,
            &out,
            "24 tests / 0 failures / 0 errors",
        );
        for mutation in [
            "build-root",
            "environment",
            "root-binding",
            "source-recheck",
            "manifest-recheck",
            "pipe-bound",
            "group-join",
            "group-kill",
            "stop-zombie",
            "capture-success",
            "capture-version",
            "incremental-binding",
        ] {
            let (rc, out) = tally.probe("scripts/probe_artifact_cargo.py", Some(mutation));
            tally.score(
                &format!("RED {mode} Cargo {mutation}"),
                rc,
                1,
                &out,
                ONE_RED,
            );
        }
        let (rc, out) = tally.probe("scripts/probe_artifact_cleanup_selection.py", None);
        tally.score(
            &format!("GREEN {mode} strict selection"),
            rc,
            0,
            &out,
            "11 tests / 0 failures / 0 errors",
        );
        for mutation in [
            "select-strict",
            "select-stale",
            "select-exclusive",
            "select-binding",
            "select-partition",
        ] {
            let (rc, out) = tally.probe(
                "scripts/probe_artifact_cleanup_selection.py",
                Some(mutation),
            );
            tally.score(
                &format!("RED {mode} selection {mutation}"),
                rc,
                1,
                &out,
                ONE_RED,
            );
        }
        let (rc, out) = tally.probe("scripts/probe_artifact_cleanup_guarded.py", None);
        tally.score(
            &format!("GREEN {mode} guarded core"),
            rc,
            0,
            &out,
            "12 tests / 0 failures / 0 errors",
        );
        for mutation in [
            "guard-revalidate",
            "guard-residue",
            "guard-postcheck",
            "guard-intent",
        ] {
            let (rc, out) =
                tally.probe("scripts/probe_artifact_cleanup_guarded.py", Some(mutation));
            tally.score(
                &format!("RED {mode} guarded {mutation}"),
                rc,
                1,
                &out,
                ONE_RED,
            );
        }
        let (rc, out) = tally.probe("scripts/probe_artifact_cleanup_operator.py", None);
        tally.score(
            &format!("GREEN {mode} operator act"),
            rc,
            0,
            &out,
            "10 tests / 0 failures / 0 errors",
        );
        for mutation in ["op-census-run", "op-census-rc", "op-census-verdict"] {
            let (rc, out) =
                tally.probe("scripts/probe_artifact_cleanup_operator.py", Some(mutation));
            tally.score(
                &format!("RED {mode} operator {mutation}"),
                rc,
                1,
                &out,
                ONE_RED,
            );
        }
        pass += tally.pass;
        fail += tally.fail;
    }
    println!("ARTIFACT-COHORT --self-test: {pass} pass / {fail} fail");
    fail == 0
}

/// `cargo xtask check-artifact-cleanup [--self-test]`: the shell driver's lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    if args.len() == 1 && args[0] == "--self-test" {
        return if self_test(root) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    if !args.is_empty() {
        eprintln!("ARTIFACT-COHORT: unknown arguments");
        return ExitCode::from(2);
    }
    if !self_test(root) {
        eprintln!("ARTIFACT-COHORT: REFUSED — self-test stopped discriminating");
        return ExitCode::from(2);
    }
    let tracked = Command::new("git")
        .args(["ls-files", "--error-unmatch", "--"])
        .args(TRACKED)
        .current_dir(root)
        .stdin(Stdio::null())
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .status()
        .is_ok_and(|s| s.success());
    if !tracked {
        eprintln!("ARTIFACT-COHORT: REFUSED — instrument and controls must be tracked");
        return ExitCode::from(2);
    }
    println!("ARTIFACT-COHORT: bounded planning/checking controls green; no real cleanup");
    ExitCode::SUCCESS
}
