//! `cargo xtask commit-unit <evidence-dir>` and `cargo xtask sweep-scratch <evidence-dir>` (`XTASK.15`).
//!
//! Every unit lands through one chain: the focused set, then `git commit -F git_message_brief.txt` under the
//! pre-commit gate, then the message file emptied and the unit's scratch swept. Until this leaf the chain and
//! the sweep were shell files under `target/`, untracked: a fix to either lived on one disk, and removing
//! `target/` removed them. `ARTIFACT-CLEANUP.40` found the cost: the sweep looked for scratch clones only
//! inside `red-*` directories and had left 21 of them, 524,516 KiB.
//!
//! The chain decides nothing the hooks decide: the commit-msg hook still judges the subject and the
//! pre-commit hook still runs the gate. It refuses early what would waste a gate: an empty or misshapen
//! message (a chain once ran 52 minutes of gate on an empty one) and an evidence directory the sweep would
//! refuse afterwards.
//!
//! The sweep removes only what a landed unit may not keep (`XTASK.9`; rule 1 of
//! `decision_orphan-incremental-sessions.md`): a cargo target directory directly in the evidence directory,
//! known by its `CACHEDIR.TAG`, and a scratch repository one or two levels down. Every file stays. A scratch
//! repository is a real directory, never a symlink, that carries `.git` and inside which git names that
//! directory as its top level. A directory whose `.git` is broken makes git search upward into this
//! repository, so it is kept.

use std::fs;
use std::path::{Component, Path, PathBuf};
use std::process::{Command, ExitCode, Stdio};
use std::time::{SystemTime, UNIX_EPOCH};

use crate::harness::combined;

/// The message file every commit is made from (`COMMIT.md`): untracked, and emptied once the commit lands.
const MESSAGE: &str = "git_message_brief.txt";

/// The variables that tell git which repository, index and work tree to use. Inside a hook they name the
/// committing repository, and a git started for another directory would follow them there.
const REPOSITORY_VARIABLES: &[&str] = &[
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_INDEX_FILE",
    "GIT_COMMON_DIR",
    "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_NAMESPACE",
    "GIT_PREFIX",
];

/// `cargo xtask sweep-scratch <evidence-dir>`: exit 0 swept, 2 refused.
pub fn run_sweep(root: &Path, args: &[String]) -> ExitCode {
    let [dir] = args else {
        eprintln!("usage: cargo xtask sweep-scratch <evidence-dir>");
        return ExitCode::from(2);
    };
    match sweep(root, dir) {
        Ok(lines) => {
            for line in lines {
                println!("{line}");
            }
            ExitCode::SUCCESS
        }
        Err(why) => {
            eprintln!("sweep: refusing {dir}: {why}");
            ExitCode::from(2)
        }
    }
}

/// `cargo xtask commit-unit <evidence-dir>`: exit 0 the unit landed, 1 it did not, 2 usage.
pub fn run_commit(root: &Path, args: &[String]) -> ExitCode {
    let [dir] = args else {
        eprintln!("usage: cargo xtask commit-unit <evidence-dir>");
        return ExitCode::from(2);
    };
    let tmp = root.join("target/tmp");
    let focused = |out: &Path| crate::focused_set(root, out, Some(&tmp)) == Some(0);
    ExitCode::from(commit_unit(root, dir, &focused))
}

/// git in `dir`, deaf to the caller's repository variables.
fn git(dir: &Path) -> Command {
    let mut command = Command::new("git");
    command.current_dir(dir);
    for name in REPOSITORY_VARIABLES {
        command.env_remove(name);
    }
    command
}

/// Whether cargo set a variable to describe the package it is running, which is this one. The gate checks
/// every package, so `git commit` starts without them, as it does from a shell (measured, `XTASK.15`:
/// `cargo run` adds `CARGO_MANIFEST_DIR`, `CARGO_MANIFEST_PATH` and fourteen `CARGO_PKG_*`).
fn describes_this_package(name: &str) -> bool {
    name.starts_with("CARGO_PKG_")
        || matches!(
            name,
            "CARGO_MANIFEST_DIR"
                | "CARGO_MANIFEST_PATH"
                | "CARGO_CRATE_NAME"
                | "CARGO_BIN_NAME"
                | "CARGO_PRIMARY_PACKAGE"
        )
}

/// The evidence directory as a path, or why it is not one: relative, strictly below `target/`, with no `..`,
/// so nothing the chain or the sweep does reaches outside the build tree.
fn evidence_dir(root: &Path, dir: &str) -> Result<PathBuf, String> {
    let mut parts = Path::new(dir).components();
    let below_target = parts.next() == Some(Component::Normal("target".as_ref()));
    let rest: Vec<Component> = parts.collect();
    if !below_target || rest.is_empty() || !rest.iter().all(|p| matches!(p, Component::Normal(_))) {
        return Err("not a directory below target/".to_owned());
    }
    Ok(root.join(dir))
}

/// Whether a path is a directory itself, not a symlink to one.
fn real_dir(path: &Path) -> bool {
    fs::symlink_metadata(path).is_ok_and(|meta| meta.is_dir())
}

/// The real directories directly inside `dir`, by name.
fn real_subdirectories(dir: &Path) -> Vec<PathBuf> {
    let mut found: Vec<PathBuf> = fs::read_dir(dir)
        .map(|entries| entries.flatten().map(|entry| entry.path()).collect())
        .unwrap_or_default();
    found.retain(|path| real_dir(path));
    found.sort();
    found
}

/// Whether a real directory carries `.git` and is the top level git finds from inside it.
fn own_repository(path: &Path) -> bool {
    // A shortcut, not a guard: without `.git` git answers with a parent, never this directory. It saves one
    // process for every directory that is plainly not a repository.
    if fs::symlink_metadata(path.join(".git")).is_err() {
        return false;
    }
    let Ok(here) = fs::canonicalize(path) else {
        return false;
    };
    git(path)
        .args(["rev-parse", "--show-toplevel"])
        .stdin(Stdio::null())
        .stderr(Stdio::null())
        .output()
        .is_ok_and(|output| {
            let top = String::from_utf8_lossy(&output.stdout);
            output.status.success() && fs::canonicalize(top.trim_end()).is_ok_and(|top| top == here)
        })
}

/// Removes one directory, which must resolve strictly inside `<root>/target`, and reports it.
fn remove(root: &Path, path: &Path, what: &str, lines: &mut Vec<String>) -> Result<(), String> {
    let target = fs::canonicalize(root.join("target")).map_err(|error| error.to_string())?;
    let real = fs::canonicalize(path).map_err(|error| error.to_string())?;
    if real == target || !real.starts_with(&target) {
        return Err(format!("{} resolves outside target/", path.display()));
    }
    fs::remove_dir_all(path).map_err(|error| format!("{}: {error}", path.display()))?;
    let shown = path.strip_prefix(root).unwrap_or(path);
    lines.push(format!("sweep: removed {what} {}", shown.display()));
    Ok(())
}

/// Removes a landed unit's scratch below its evidence directory: one line per removal, then the total.
fn sweep(root: &Path, dir: &str) -> Result<Vec<String>, String> {
    let out = evidence_dir(root, dir)?;
    if !real_dir(&out) {
        return Err("not a directory".to_owned());
    }
    let mut lines = Vec::new();
    for path in real_subdirectories(&out) {
        if path.join("CACHEDIR.TAG").is_file() {
            remove(root, &path, "build directory", &mut lines)?;
        } else if own_repository(&path) {
            remove(root, &path, "scratch clone", &mut lines)?;
        } else {
            for inner in real_subdirectories(&path) {
                if own_repository(&inner) {
                    remove(root, &inner, "scratch clone", &mut lines)?;
                }
            }
        }
    }
    lines.push(format!("sweep: {} removed under {dir}", lines.len()));
    Ok(lines)
}

/// The subject shape the chain asks for, as its refusal prints it.
const SUBJECT_SHAPE: &str = "SEMULITH-<AREA>-<NNNN> followed by a space or a colon";

/// Whether a first line has the shape of a work-unit subject, `SEMULITH-<AREA>-<NNNN>` and then a space or a colon
/// (`COMMIT.md`; the push records use the colon). The commit-msg hook judges the subject; this only keeps the gate
/// from running on a message that cannot pass it (`XTASK.18`).
fn subject_shaped(line: &str) -> bool {
    let Some((area, rest)) = line
        .strip_prefix("SEMULITH-")
        .and_then(|rest| rest.split_once('-'))
    else {
        return false;
    };
    let number = rest.as_bytes();
    !area.is_empty()
        && area
            .bytes()
            .all(|b| b.is_ascii_uppercase() || b.is_ascii_digit())
        && number.len() > 4
        && number[..4].iter().all(u8::is_ascii_digit)
        && matches!(number[4], b' ' | b':')
}

/// The refusal for a message the chain will not commit: what it wants, and what the first line is.
fn malformed(first: &str) -> String {
    let got: String = first.chars().take(80).collect();
    let got = if got.is_empty() {
        "an empty first line".to_owned()
    } else {
        format!("`{got}`")
    };
    format!("EMPTY-OR-MALFORMED {MESSAGE}: not starting the gate; its first line must begin {SUBJECT_SHAPE}, and it is {got}")
}

/// `HH:MM:SS` in UTC, now.
fn clock() -> String {
    let now = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map_or(0, |elapsed| elapsed.as_secs());
    crate::utc_clock(now)
}

/// The chain. `focused` runs the focused set into the directory it is given and says whether every check was
/// green. Returns the exit status: 0 the unit landed, 1 it did not.
fn commit_unit(root: &Path, dir: &str, focused: &dyn Fn(&Path) -> bool) -> u8 {
    let message = root.join(MESSAGE);
    let text = fs::read_to_string(&message).unwrap_or_default();
    let first = text.lines().next().unwrap_or("");
    if !subject_shaped(first) {
        println!("{}", malformed(first));
        return 1;
    }
    let out = match evidence_dir(root, dir) {
        Ok(out) => out,
        Err(why) => {
            println!("commit-unit: refusing {dir}: {why}");
            return 1;
        }
    };
    if let Err(error) = fs::create_dir_all(&out) {
        println!("commit-unit: cannot create {dir}: {error}");
        return 1;
    }
    if !focused(&out.join("commit-focused")) {
        println!("FOCUSED-RED: not committing");
        return 1;
    }
    println!("{} commit begins (pre-commit gate)", clock());
    let mut commit = git(root);
    for (name, _) in std::env::vars_os() {
        if describes_this_package(&name.to_string_lossy()) {
            commit.env_remove(name);
        }
    }
    let (code, output) = combined(commit.args(["commit", "-F", MESSAGE]));
    if let Err(error) = fs::write(out.join("commit.log"), &output) {
        println!("commit-unit: cannot write {dir}/commit.log: {error}");
    }
    println!("{} git commit rc={code}", clock());
    let tail: Vec<&str> = output.lines().collect();
    for line in &tail[tail.len().saturating_sub(5)..] {
        println!("{line}");
    }
    if code != 0 {
        return 1;
    }
    if let Err(error) = fs::write(&message, "") {
        println!("commit-unit: the commit landed, and {MESSAGE} could not be emptied: {error}");
        return 1;
    }
    let (_, head) = combined(git(root).args(["log", "-1", "--format=%H %s"]));
    print!("{head}");
    match sweep(root, dir) {
        Ok(lines) => {
            for line in lines {
                println!("{line}");
            }
        }
        Err(why) => println!("sweep: refusing {dir}: {why}"),
    }
    0
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::harness::scratch;
    use std::cell::Cell;

    /// A scratch repository under this repository's `target/`, removed when dropped.
    struct Repo(PathBuf);

    impl Drop for Repo {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.0);
        }
    }

    fn run(dir: &Path, args: &[&str]) -> String {
        let (code, output) = combined(git(dir).args(args));
        assert_eq!(code, 0, "git {args:?} in {}: {output}", dir.display());
        output
    }

    fn init(dir: &Path) {
        fs::create_dir_all(dir).expect("the directory");
        run(dir, &["init", "-q"]);
    }

    /// A repository with one commit, its own identity, no signing and no hook of anyone's. The guard exists
    /// before anything can fail, so a setup that panics still removes its directory.
    fn repo() -> Repo {
        let repo = Repo(
            scratch(
                &crate::repository_root(),
                "target/doctrine-selftest",
                "commit-unit",
            )
            .expect("a scratch directory"),
        );
        let dir = repo.0.clone();
        init(&dir);
        fs::create_dir(dir.join("hooks")).expect("the hook directory");
        for (key, value) in [
            ("user.name", "scratch"),
            ("user.email", "scratch@invalid"),
            ("commit.gpgsign", "false"),
            ("core.hooksPath", "hooks"),
        ] {
            run(&dir, &["config", key, value]);
        }
        assert!(own_repository(&dir), "the scratch repository is its own");
        fs::write(dir.join("tracked.txt"), "one\n").expect("a file");
        run(&dir, &["add", "tracked.txt"]);
        run(
            &dir,
            &["commit", "-q", "-m", "SEMULITH-TEST-0000 the first commit"],
        );
        repo
    }

    fn head(dir: &Path) -> String {
        run(dir, &["log", "-1", "--format=%s"]).trim().to_owned()
    }

    /// Stages a change and writes the message file; the evidence directory holds one scratch clone.
    fn stage(dir: &Path, message: &str) {
        fs::write(dir.join("tracked.txt"), "two\n").expect("a change");
        run(dir, &["add", "tracked.txt"]);
        fs::write(dir.join(MESSAGE), message).expect("the message");
        init(&dir.join("target/unit/tree"));
    }

    #[test]
    fn the_sweep_removes_build_directories_and_scratch_repositories_and_keeps_every_file() {
        let repo = repo();
        let out = repo.0.join("target/unit");
        for clone in [
            "tree",
            "red/case",
            "red-1/x",
            "deep/a/b",
            "../outside/clone",
        ] {
            init(&out.join(clone));
        }
        for dir in ["broken/.git", "plain", "build"] {
            fs::create_dir_all(out.join(dir)).expect("a directory");
        }
        for file in ["build/CACHEDIR.TAG", "out.txt", "red/summary.txt"] {
            fs::write(out.join(file), "kept\n").expect("a file");
        }
        #[cfg(unix)]
        std::os::unix::fs::symlink("../outside", out.join("link")).expect("a symlink");

        let lines = sweep(&repo.0, "target/unit").expect("the sweep runs");
        assert_eq!(
            lines,
            [
                "sweep: removed build directory target/unit/build",
                "sweep: removed scratch clone target/unit/red/case",
                "sweep: removed scratch clone target/unit/red-1/x",
                "sweep: removed scratch clone target/unit/tree",
                "sweep: 4 removed under target/unit",
            ]
        );
        for kept in [
            "broken/.git",
            "plain",
            "out.txt",
            "red/summary.txt",
            "deep/a/b/.git",
            "../outside/clone/.git",
        ] {
            assert!(out.join(kept).exists(), "{kept} was removed");
        }
        // A second sweep finds nothing: what the first kept is not scratch.
        assert_eq!(
            sweep(&repo.0, "target/unit").expect("the sweep runs"),
            ["sweep: 0 removed under target/unit"]
        );
    }

    #[test]
    fn the_sweep_refuses_what_is_not_a_real_directory_below_target() {
        let repo = repo();
        fs::create_dir_all(repo.0.join("target/unit")).expect("the evidence directory");
        fs::create_dir_all(repo.0.join("docs")).expect("a directory outside target");
        for dir in [
            "docs",
            "target",
            "target/../docs",
            "/tmp",
            "",
            "target/unit/../../docs",
        ] {
            assert_eq!(
                sweep(&repo.0, dir),
                Err("not a directory below target/".to_owned()),
                "{dir:?}"
            );
        }
        assert_eq!(
            sweep(&repo.0, "target/absent"),
            Err("not a directory".to_owned())
        );
        #[cfg(unix)]
        {
            std::os::unix::fs::symlink("unit", repo.0.join("target/link")).expect("a symlink");
            assert_eq!(
                sweep(&repo.0, "target/link"),
                Err("not a directory".to_owned())
            );
        }
    }

    #[test]
    fn a_removal_that_would_leave_target_is_refused() {
        let repo = repo();
        fs::create_dir_all(repo.0.join("target/unit")).expect("the evidence directory");
        fs::create_dir_all(repo.0.join("docs")).expect("a directory outside target");
        let mut lines = Vec::new();
        let whole = remove(&repo.0, &repo.0.join("target"), "x", &mut lines);
        assert!(whole.is_err_and(|why| why.contains("resolves outside target/")));
        #[cfg(unix)]
        {
            let escape = repo.0.join("target/unit/escape");
            std::os::unix::fs::symlink("../../docs", &escape).expect("a symlink");
            let outside = remove(&repo.0, &escape, "x", &mut lines);
            assert!(outside.is_err_and(|why| why.contains("resolves outside target/")));
        }
        assert!(repo.0.join("docs").is_dir() && repo.0.join("target/unit").is_dir());
        assert!(lines.is_empty(), "nothing is reported removed");
    }

    #[test]
    fn a_message_that_cannot_pass_the_hook_never_starts_the_gate() {
        let repo = repo();
        let ran = Cell::new(false);
        let focused = |_: &Path| {
            ran.set(true);
            true
        };
        for message in [
            "",
            "\n",
            "fix things\n",
            "SEMILITH-P4-0001 a typo\n",
            "SEMULITH-P4-12 short\n",
        ] {
            stage(&repo.0, message);
            assert_eq!(
                commit_unit(&repo.0, "target/unit", &focused),
                1,
                "{message:?}"
            );
        }
        fs::remove_file(repo.0.join(MESSAGE)).expect("the message file");
        assert_eq!(
            commit_unit(&repo.0, "target/unit", &focused),
            1,
            "no message file"
        );
        fs::write(repo.0.join(MESSAGE), "SEMULITH-TEST-0001 a unit\n").expect("the message");
        for dir in ["docs/unit", "target", "target/../unit"] {
            assert_eq!(commit_unit(&repo.0, dir, &focused), 1, "{dir}");
        }
        assert!(!ran.get(), "the focused set ran");
        assert_eq!(head(&repo.0), "SEMULITH-TEST-0000 the first commit");
    }

    #[test]
    fn a_red_focused_set_does_not_commit() {
        let repo = repo();
        stage(&repo.0, "SEMULITH-TEST-0001 a unit\n");
        assert_eq!(commit_unit(&repo.0, "target/unit", &|_| false), 1);
        assert_eq!(head(&repo.0), "SEMULITH-TEST-0000 the first commit");
        let message = fs::read_to_string(repo.0.join(MESSAGE)).expect("the message");
        assert_eq!(
            message, "SEMULITH-TEST-0001 a unit\n",
            "the message is kept"
        );
        assert!(
            repo.0.join("target/unit/tree/.git").exists(),
            "the scratch is kept"
        );
    }

    #[test]
    fn a_green_unit_lands_and_its_message_is_emptied_and_its_scratch_swept() {
        let repo = repo();
        stage(&repo.0, "SEMULITH-TEST-0001 a unit\n\n- its body\n");
        let seen = Cell::new(PathBuf::new());
        let focused = |out: &Path| {
            seen.set(out.to_path_buf());
            true
        };
        assert_eq!(commit_unit(&repo.0, "target/unit", &focused), 0);
        assert_eq!(seen.take(), repo.0.join("target/unit/commit-focused"));
        assert_eq!(head(&repo.0), "SEMULITH-TEST-0001 a unit");
        let message = fs::read(repo.0.join(MESSAGE)).expect("the message file stays");
        assert!(message.is_empty(), "the message is emptied");
        assert!(
            repo.0.join("target/unit/commit.log").is_file(),
            "the commit's output is kept"
        );
        assert!(
            !repo.0.join("target/unit/tree").exists(),
            "the scratch clone is swept"
        );
        assert!(run(&repo.0, &["status", "--porcelain", "--untracked-files=no"]).is_empty());
    }

    #[cfg(unix)]
    #[test]
    fn a_commit_the_hook_refuses_keeps_the_message_and_the_scratch() {
        use std::os::unix::fs::PermissionsExt as _;
        let repo = repo();
        let hook = repo.0.join("hooks/pre-commit");
        fs::write(&hook, "#!/bin/sh\necho 'the gate refuses' >&2\nexit 1\n").expect("the hook");
        fs::set_permissions(&hook, fs::Permissions::from_mode(0o755)).expect("its mode");
        stage(&repo.0, "SEMULITH-TEST-0001 a unit\n");
        assert_eq!(commit_unit(&repo.0, "target/unit", &|_| true), 1);
        assert_eq!(head(&repo.0), "SEMULITH-TEST-0000 the first commit");
        let message = fs::read_to_string(repo.0.join(MESSAGE)).expect("the message");
        assert_eq!(
            message, "SEMULITH-TEST-0001 a unit\n",
            "the message is kept for the retry"
        );
        assert!(
            repo.0.join("target/unit/tree/.git").exists(),
            "the scratch is kept"
        );
        let log = fs::read_to_string(repo.0.join("target/unit/commit.log")).expect("the log");
        assert!(log.contains("the gate refuses"), "{log}");
    }

    #[cfg(unix)]
    #[test]
    fn the_gate_starts_without_the_variables_cargo_set_for_this_package() {
        use std::os::unix::fs::PermissionsExt as _;
        assert!(
            std::env::var_os("CARGO_MANIFEST_DIR").is_some() && std::env::var_os("PATH").is_some(),
            "cargo runs this test, so the variables are there to be dropped"
        );
        let repo = repo();
        let hook = repo.0.join("hooks/pre-commit");
        fs::write(&hook, "#!/bin/sh\nenv > hook-env.txt\n").expect("the hook");
        fs::set_permissions(&hook, fs::Permissions::from_mode(0o755)).expect("its mode");
        stage(&repo.0, "SEMULITH-TEST-0001 a unit\n");
        assert_eq!(commit_unit(&repo.0, "target/unit", &|_| true), 0);
        let seen = fs::read_to_string(repo.0.join("hook-env.txt")).expect("the hook ran");
        let names: Vec<&str> = seen
            .lines()
            .filter_map(|l| l.split_once('='))
            .map(|(n, _)| n)
            .collect();
        assert!(
            names.contains(&"PATH"),
            "the hook keeps the caller's environment"
        );
        let described: Vec<&&str> = names.iter().filter(|n| describes_this_package(n)).collect();
        assert!(described.is_empty(), "the hook saw {described:?}");
        assert!(!describes_this_package("CARGO") && !describes_this_package("CARGO_HOME"));
    }

    #[test]
    fn a_refusal_says_what_it_wants_and_what_it_got() {
        let empty = malformed("");
        assert!(
            empty.starts_with("EMPTY-OR-MALFORMED git_message_brief.txt: not starting the gate"),
            "{empty}"
        );
        assert!(
            empty.contains(SUBJECT_SHAPE) && empty.ends_with("an empty first line"),
            "{empty}"
        );
        let long = malformed(&"x".repeat(200));
        assert!(long.ends_with(&format!("`{}`", "x".repeat(80))), "{long}");
    }

    #[test]
    fn a_subject_has_the_work_unit_shape() {
        for good in [
            "SEMULITH-P4-0396 (leaf P4-SYSTEM.18 slice b): x",
            "SEMULITH-AC-0096 y",
            "SEMULITH-XTASK-0089 z",
            "SEMULITH-LC-0056: the colon the push records use",
        ] {
            assert!(subject_shaped(good), "{good}");
        }
        for bad in [
            "",
            "SEMULITH-P4-0396",
            "SEMULITH-P4-0396; another mark",
            "SEMULITH-p4-0396 lower",
            "SEMULITH--0396 no area",
            "SEMULITH-P4-039 short",
            "SEMULITH-P4-03966 long",
            "SEMULITH-P4-03X6 not a number",
            " SEMULITH-P4-0396 indented",
            "SEMILITH-P4-0396 the other spelling",
        ] {
            assert!(!subject_shaped(bad), "{bad}");
        }
    }

    #[test]
    fn git_never_follows_the_callers_repository_variables() {
        let command = git(Path::new("."));
        for name in REPOSITORY_VARIABLES {
            assert!(
                command
                    .get_envs()
                    .any(|(key, value)| key == *name && value.is_none()),
                "{name} is inherited"
            );
        }
        assert!(
            REPOSITORY_VARIABLES.contains(&"GIT_INDEX_FILE")
                && REPOSITORY_VARIABLES.contains(&"GIT_DIR")
        );
    }
}
