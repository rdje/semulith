//! The `TASK-HISTORY` doctrine's driver, ported from `scripts/check_task_history.sh` (`XTASK.6` slice `6ac`), which is
//! now a shim of `cargo xtask check-task-history`.
//!
//! The task family's sealed history — the archive terminal, its descriptor, the navigation stubs, the qualification and
//! cleanup histories, the links into retained narrative — is preserved exactly: the Python judges
//! (`task_history_archive.py` against the committed descriptor, the three preservation judges, the links judge) run as
//! the driver ran them, their output and exit statuses passing straight through, not ported. The controls are the
//! script's fifty-two probe runs, each a case of `probe_task_history.py` or one of the three probe suites; each is one
//! `tally.arm(` call, the idiom the `DERIVED-COUNTS` arm total counts.

use std::fs;
use std::path::Path;
use std::process::{Command, ExitCode, Stdio};

use crate::harness::combined;

struct Tally<'a> {
    repo: &'a Path,
    pass: u32,
    fail: u32,
    verbose: bool,
}

impl Tally<'_> {
    /// One arm: the probe run for `case` must exit `expected` and print `want` (stdout and stderr together).
    fn arm(&mut self, case: &str, expected: i32, want: &str) {
        let mut command = Command::new("python3");
        match case {
            "ordinary-normal" => command.arg("scripts/probe_task_history_preservation.py"),
            "ordinary-optimized" => {
                command.args(["-O", "scripts/probe_task_history_preservation.py"])
            }
            "qualification-normal" => command.arg("scripts/probe_qualification_history.py"),
            "qualification-optimized" => {
                command.args(["-O", "scripts/probe_qualification_history.py"])
            }
            "cleanup-normal" => command.args(["-B", "scripts/probe_artifact_task_history.py"]),
            "cleanup-optimized" => {
                command.args(["-O", "-B", "scripts/probe_artifact_task_history.py"])
            }
            other => command.args(["scripts/probe_task_history.py", "--case", other]),
        };
        let (rc, out) = combined(command.current_dir(self.repo));
        if rc == expected && out.contains(want) {
            self.pass += 1;
        } else {
            self.fail += 1;
            if self.verbose {
                eprintln!(
                    "TASK-HISTORY self-test MISS: {case} expected rc={expected} reason={want} got rc={rc}\n{}",
                    out.trim_end_matches('\n')
                );
            }
        }
    }
}

/// The script's fifty-two probe runs, in its order.
fn self_test(repo: &Path, verbose: bool) -> bool {
    let mut tally = Tally {
        repo,
        pass: 0,
        fail: 0,
        verbose,
    };
    tally.arm(
        "green",
        0,
        "all12 Python/tar originals exact; no Git/extraction; navigation/freeze exact",
    );
    tally.arm("missing-descriptor", 1, "descriptor.json");
    tally.arm("unknown-field", 1, "unknown descriptor fields");
    tally.arm("duplicate-key", 1, "duplicate JSON key");
    tally.arm("oversized-descriptor", 1, "archive file exceeds bound");
    tally.arm(
        "string-count",
        1,
        "descriptor count exceeds bound or is not an integer",
    );
    tally.arm(
        "bool-count",
        1,
        "descriptor count exceeds bound or is not an integer",
    );
    tally.arm("unsafe-object", 1, "unsafe archive object path");
    tally.arm(
        "changed-descriptor",
        1,
        "approved descriptor identity differs",
    );
    tally.arm("previous-descriptor", 1, "changed committed descriptor");
    tally.arm("missing-object", 1, "finite terminal coverage differs");
    tally.arm("object-digest", 1, "object digest differs");
    tally.arm("extra-file", 1, "finite terminal coverage differs");
    tally.arm("terminal-symlink", 1, "symlink in archive terminal");
    tally.arm("parent-symlink", 1, "symlink in archive path");
    tally.arm("changed-stub", 1, "navigation stub differs");
    tally.arm("missing-stub", 1, "P4-SYSTEM-12.md");
    tally.arm("unknown-read", 1, "unknown archived logical path");
    tally.arm("escaping-read", 1, "unknown archived logical path");
    tally.arm("expansion-bound", 1, "archive expansion exceeds bound");
    tally.arm("truncated-gzip", 1, "unreadable archive object");
    tally.arm(
        "nonregular-member",
        1,
        "archive member must be a plain regular file",
    );
    tally.arm("duplicate-member", 1, "duplicate archive member");
    tally.arm("extra-member", 1, "unknown or unsafe archive member");
    tally.arm("unsafe-member", 1, "unknown or unsafe archive member");
    tally.arm("missing-member", 1, "archive member census differs");
    tally.arm("oversized-member", 1, "archive member exceeds bound");
    tally.arm("noncanonical-tar", 1, "noncanonical tar encoding");
    tally.arm("manifest-identity", 1, "manifest identity differs");
    tally.arm("member-identity", 1, "original member identity differs");
    tally.arm("source-bytes", 1, "source byte count differs");
    tally.arm("source-lines", 1, "source line count differs");
    tally.arm("manifest-fields", 1, "unknown manifest fields");
    tally.arm("manifest-duplicate", 1, "duplicate manifest member");
    tally.arm("manifest-path", 1, "unknown manifest member path");
    tally.arm(
        "manifest-string-count",
        1,
        "malformed manifest member identity",
    );
    tally.arm("malformed-json", 1, "malformed archive JSON");
    tally.arm("non-utf8", 1, "original member is not UTF-8");
    tally.arm("manifest-capture", 1, "manifest capture differs");
    tally.arm("oversized-json-integer", 1, "malformed archive JSON");
    tally.arm("front-bound", 1, "archive file exceeds bound");
    tally.arm("extra-directory", 1, "unknown terminal directory");
    tally.arm("corrupt-read", 1, "object digest differs");
    tally.arm("links-green", 0, "incoming history path/anchor resolves");
    tally.arm("links-anchor", 1, "unretained history link anchor");
    tally.arm("links-include", 1, "sealed narrative used as live include");
    tally.arm("ordinary-normal", 0, "43 tests / 0 failures / 0 errors");
    tally.arm("ordinary-optimized", 0, "43 tests / 0 failures / 0 errors");
    tally.arm(
        "qualification-normal",
        0,
        "32 tests / 0 failures / 0 errors",
    );
    tally.arm(
        "qualification-optimized",
        0,
        "32 tests / 0 failures / 0 errors",
    );
    tally.arm("cleanup-normal", 0, "45 tests / 0 failures / 0 errors");
    tally.arm("cleanup-optimized", 0, "45 tests / 0 failures / 0 errors");
    if verbose {
        println!(
            "TASK-HISTORY --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}

/// A judge run from the root with inherited stdio: its exit status, `2` when it cannot start (the shell's `|| exit`).
fn judge(root: &Path, program: &str, args: &[&str]) -> i32 {
    Command::new(program)
        .args(args)
        .current_dir(root)
        .stdin(Stdio::null())
        .status()
        .map(|s| s.code().unwrap_or(1))
        .unwrap_or(2)
}

/// `cargo xtask check-task-history [--self-test]`: the shell driver's judges and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    if !args.is_empty() {
        eprintln!("TASK-HISTORY: unknown arguments");
        return ExitCode::from(2);
    }
    if !self_test(root, false) {
        eprintln!("TASK-HISTORY: REFUSED — self-test stopped discriminating");
        return ExitCode::from(2);
    }
    let dir = root.join("target/history-check");
    let _ = fs::create_dir_all(&dir);
    let stamp = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map_or(0, |d| d.as_nanos());
    let previous = dir.join(format!("tasks.{}-{stamp}", std::process::id()));
    let code = (|| {
        let tracked = Command::new("git")
            .args([
                "ls-tree",
                "--name-only",
                "HEAD",
                "--",
                "docs/task-history/descriptor.json",
            ])
            .current_dir(root)
            .stdin(Stdio::null())
            .stderr(Stdio::inherit())
            .output();
        let Ok(tracked) = tracked else {
            return 2;
        };
        if !tracked.status.success() {
            return 2;
        }
        if !tracked.stdout.is_empty() {
            let shown = Command::new("git")
                .args(["show", "HEAD:docs/task-history/descriptor.json"])
                .current_dir(root)
                .stdin(Stdio::null())
                .stderr(Stdio::inherit())
                .output();
            match shown {
                Ok(o) if o.status.success() => {
                    if fs::write(&previous, &o.stdout).is_err() {
                        return 2;
                    }
                }
                _ => return 2,
            }
            let rc = judge(
                root,
                "python3",
                &[
                    "scripts/task_history_archive.py",
                    "--previous",
                    &previous.display().to_string(),
                ],
            );
            if rc != 0 {
                return rc;
            }
        } else {
            let rc = judge(root, "python3", &["scripts/task_history_archive.py"]);
            if rc != 0 {
                return rc;
            }
        }
        for args in [
            &["scripts/task_history_preservation.py"][..],
            &["scripts/qualification_history_preservation.py"][..],
            &["-B", "scripts/artifact_task_history_preservation.py"][..],
        ] {
            let rc = judge(root, "python3", args);
            if rc != 0 {
                return rc;
            }
        }
        judge(root, "python3", &["scripts/check_task_history_links.py"])
    })();
    let _ = fs::remove_file(&previous);
    if code == 0 {
        ExitCode::SUCCESS
    } else {
        ExitCode::from(u8::try_from(code).unwrap_or(1))
    }
}
