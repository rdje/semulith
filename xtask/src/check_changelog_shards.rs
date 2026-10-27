//! The `SHARD-FREEZE` doctrine's driver, ported from `scripts/check_changelog_shards.sh` (`XTASK.6` slice `6ad`), which
//! is now a shim of `cargo xtask check-changelog-shards`.
//!
//! The sharded history (`docs/changelog/shard-*.md`, its manifest `SHARDS.sha256`, the two live heads `CHANGELOG.md` and
//! `DEV_NOTES.md`, the archive descriptor) is frozen: committed rows never change or vanish, every shard is manifested
//! and every manifested shard exists, no entry lives twice, the archive's identity and retrieval hold, the predecessor
//! chain is complete. `scripts/check_history_partition.py` judges the partition against the committed manifest and
//! archive descriptor taken through `git show`, `scripts/history_predecessor.py` the chain; both run as the driver ran
//! them and are not ported. The controls write the script's synthetic shards, heads and manifests and run its archive
//! and predecessor probe mutations. Each self-test arm is one `tally.arm(` call, the idiom the `DERIVED-COUNTS` arm
//! total counts.

use std::fs;
use std::path::{Path, PathBuf};
use std::process::{Command, ExitCode, Stdio};

use crate::harness::{combined, locale_sorted, scratch, Hasher};

/// `check_shards <root> <shard dir> <manifest> <previous manifest or ""> <heads…>`, the committed archive descriptor's
/// path (or "") first, as `check_history_partition.py` takes them.
fn check_shards(repo: &Path, previous_archives: &str, args: &[&str], both: bool) -> (i32, String) {
    let mut command = Command::new("python3");
    command
        .arg(repo.join("scripts/check_history_partition.py"))
        .arg(previous_archives)
        .args(args)
        .current_dir(repo);
    if both {
        return combined(&mut command);
    }
    match command
        .stdin(Stdio::null())
        .stderr(Stdio::inherit())
        .output()
    {
        Ok(o) => (
            o.status.code().unwrap_or(-1),
            String::from_utf8_lossy(&o.stdout).into_owned(),
        ),
        Err(e) => (-1, e.to_string()),
    }
}

/// The shell's `$(…)`: every trailing newline removed.
fn captured(text: &str) -> &str {
    text.trim_end_matches('\n')
}

fn write(path: &Path, text: &str) {
    if let Some(parent) = path.parent() {
        let _ = fs::create_dir_all(parent);
    }
    let _ = fs::write(path, text);
}

/// Which control an arm runs: the partition judge over the scratch tree, an archive probe mutation, or a predecessor
/// probe run (plain, optimized, or a mutation plain or optimized) — the script's `PREDECESSOR_CONTROL`,
/// `PREDECESSOR_OPTIMIZED` and `ARCHIVE_CONTROL` variables.
#[derive(Clone)]
enum Control {
    Shards,
    Archive(String),
    Predecessor {
        mutation: Option<String>,
        optimized: bool,
    },
}

struct Tally<'a> {
    repo: &'a Path,
    root: &'a Path,
    control: Control,
    pass: u32,
    fail: u32,
    verbose: bool,
}

impl Tally<'_> {
    /// The script's `run`.
    fn run(&self) -> (i32, String) {
        match &self.control {
            Control::Predecessor {
                mutation,
                optimized,
            } => {
                let mut command = Command::new("python3");
                if *optimized {
                    command.arg("-O");
                }
                command.arg("scripts/probe_history_predecessor.py");
                if let Some(m) = mutation {
                    command.args(["--mutation", m]);
                }
                combined(command.current_dir(self.repo))
            }
            Control::Archive(mutation) => combined(
                Command::new("python3")
                    .args(["scripts/probe_history_archive.py", "--mutation", mutation])
                    .current_dir(self.repo),
            ),
            Control::Shards => {
                let prev = self.root.join("prev.sha256");
                let prev = if prev.is_file() {
                    prev.display().to_string()
                } else {
                    String::new()
                };
                check_shards(
                    self.repo,
                    "",
                    &[
                        &self.root.display().to_string(),
                        "docs/changelog",
                        "docs/changelog/SHARDS.sha256",
                        &prev,
                        "CHANGELOG.md",
                        "DEV_NOTES.md",
                    ],
                    true,
                )
            }
        }
    }

    /// One arm: the control's run must exit `expected` and contain `want`.
    fn arm(&mut self, name: &str, expected: i32, want: &str) {
        let (rc, out) = self.run();
        let out = captured(&out);
        if rc != expected {
            self.fail += 1;
            if self.verbose {
                eprintln!(
                    "SHARD-FREEZE self-test MISS: {name} expected rc={expected} got rc={rc}\n{out}"
                );
            }
        } else if !out.contains(want) {
            self.fail += 1;
            if self.verbose {
                eprintln!("SHARD-FREEZE self-test MISS: {name} right verdict, wrong reason (no {want})\n{out}");
            }
        } else {
            self.pass += 1;
        }
    }
}

/// `sha256sum "$SDIR"/*.md | sed "s|$t/||"`: one manifest row per shard, in the glob's order.
fn shard_rows(t: &Path, hasher: Option<&Hasher>) -> Vec<String> {
    let dir = t.join("docs/changelog");
    let names: Vec<String> = fs::read_dir(&dir)
        .map(|entries| {
            entries
                .flatten()
                .map(|e| e.file_name().to_string_lossy().into_owned())
                .filter(|n| n.ends_with(".md"))
                .collect()
        })
        .unwrap_or_default();
    locale_sorted(names)
        .into_iter()
        .map(|n| {
            let digest = hasher.map(|h| h.digest(&dir.join(&n))).unwrap_or_default();
            format!("{digest}  docs/changelog/{n}")
        })
        .collect()
}

/// The RED/GREEN controls over the script's synthetic shards, heads and manifests, then its archive and predecessor
/// probe runs.
fn self_test(repo: &Path, verbose: bool) -> bool {
    let Ok(t) = scratch(repo, "target/doctrine-selftest", "shardfreeze") else {
        eprintln!("SHARD-FREEZE self-test: cannot create a scratch directory under target/doctrine-selftest");
        return false;
    };
    let _ = fs::create_dir_all(t.join("docs/changelog"));
    let hasher = Hasher::find();
    let sdir = t.join("docs/changelog");
    let man = sdir.join("SHARDS.sha256");
    let head = t.join("CHANGELOG.md");
    let head2 = t.join("DEV_NOTES.md");
    let prev_path = t.join("prev.sha256");
    let fake64 = "a".repeat(64);
    let digest = |name: &str| {
        hasher
            .as_ref()
            .map(|h| h.digest(&sdir.join(name)))
            .unwrap_or_default()
    };
    let shard1 = || {
        write(
            &sdir.join("2026-09-a.md"),
            "# shard\n\n## entry-old\nbody\n",
        )
    };
    let shard2 = || {
        write(
            &sdir.join("shard-0001.md"),
            "# shard\n\n## entry-older\nbody\n",
        )
    };
    let headf = || {
        write(&head, "# CHANGELOG.md\n\n## entry-new\nbody\n");
        write(&head2, "# DEV_NOTES.md\n\n## entry-live\nbody\n");
    };
    let manifest = |extra: &[&str]| {
        let _ = fs::remove_file(&prev_path);
        let mut rows = shard_rows(&t, hasher.as_ref());
        rows.extend(extra.iter().map(|e| (*e).to_owned()));
        let mut text = rows.join("\n");
        text.push('\n');
        write(&man, &text);
    };
    let mut tally = Tally {
        repo,
        root: &t,
        control: Control::Shards,
        pass: 0,
        fail: 0,
        verbose,
    };
    let _ = fs::remove_file(&prev_path);
    shard1();
    shard2();
    headf();
    manifest(&[]);
    tally.arm(
        "GREEN frozen shards and a true manifest",
        0,
        "__CHECKED__ 2",
    );
    shard1();
    shard2();
    headf();
    manifest(&[]);
    let mut edited = fs::read(sdir.join("shard-0001.md")).unwrap_or_default();
    edited.push(b'x');
    let _ = fs::write(sdir.join("shard-0001.md"), edited);
    tally.arm("RED   a shard edited after the event", 1, "THAWED");
    shard1();
    shard2();
    headf();
    manifest(&[]);
    // `prev`: the first shard's true row, then the second's digest with its first character replaced by `0`.
    let second = digest("shard-0001.md");
    let _ = fs::write(
        &prev_path,
        format!(
            "{}  docs/changelog/2026-09-a.md\n0{}  docs/changelog/shard-0001.md",
            digest("2026-09-a.md"),
            second.get(1..).unwrap_or("")
        ),
    );
    tally.arm("RED   a committed row's content changed", 1, "MODIFIED ROW");
    shard1();
    shard2();
    headf();
    write(
        &sdir.join("shard-0002.md"),
        "# shard\n\n## entry-oldest\nbody\n",
    );
    manifest(&[]); // 3 rows
    let _ = fs::copy(&man, &prev_path); // the committed manifest
    let _ = fs::remove_file(sdir.join("shard-0002.md"));
    let mut text = shard_rows(&t, hasher.as_ref()).join("\n");
    text.push('\n');
    write(&man, &text); // 2 rows, prev untouched
    tally.arm("RED   a committed row removed", 1, "REMOVED ROW");
    shard1();
    shard2();
    headf();
    manifest(&[]);
    let _ = fs::remove_file(sdir.join("shard-0001.md"));
    tally.arm("RED   a manifested shard deleted", 1, "MISSING");
    shard1();
    shard2();
    headf();
    manifest(&[]);
    let _ = fs::remove_file(&man);
    tally.arm("RED   shards nothing manifests", 1, "UNMANIFESTED");
    shard1();
    shard2();
    headf();
    manifest(&[&format!("{fake64}  docs/changelog/ghost.md")]);
    tally.arm("RED   a row for a file that does not exist", 1, "MISSING");
    shard1();
    shard2();
    headf();
    manifest(&[&format!("{fake64}  docs/other.md")]);
    write(&t.join("docs/other.md"), "x\n");
    tally.arm("RED   a row escaping the shard directory", 1, "NOT A SHARD");
    shard1();
    shard2();
    headf();
    manifest(&["not-a-hash row"]);
    tally.arm("RED   a malformed manifest line", 1, "MALFORMED");
    shard1();
    shard2();
    headf();
    manifest(&[&format!(
        "{}  docs/changelog/2026-09-a.md",
        digest("2026-09-a.md")
    )]);
    tally.arm("RED   the same shard manifested twice", 1, "DUPLICATE ROW");
    shard1();
    shard2();
    headf();
    write(&head, "# CHANGELOG.md\n\n## entry-old\nalso here\n");
    manifest(&[]);
    tally.arm(
        "RED   an entry duplicated across head and shard",
        1,
        "DUPLICATED ENTRY",
    );
    shard1();
    shard2();
    headf();
    manifest(&[]);
    tally.arm(
        "GREEN two live heads share one frozen partition",
        0,
        "__CHECKED__ 2",
    );
    shard1();
    shard2();
    headf();
    write(
        &sdir.join("shard-0002.md"),
        "# DEV_NOTES shard — probe\n\n## entry-live\nstolen from the live head\n",
    );
    manifest(&[]);
    tally.arm(
        "RED   a shard carrying either live head's entry",
        1,
        "DUPLICATED ENTRY",
    );
    let _ = fs::remove_file(sdir.join("shard-0002.md"));
    shard1();
    shard2();
    headf();
    manifest(&[]);
    let _ = fs::copy(&man, &prev_path);
    tally.arm(
        "GREEN committed rows unchanged under an append-only manifest",
        0,
        "__CHECKED__ 2",
    );
    tally.control = Control::Archive("green".to_owned());
    tally.arm(
        "GREEN archive green",
        0,
        "identity/retrieval/predecessor/numbering passed",
    );
    tally.control = Control::Archive("missing-object".to_owned());
    tally.arm(
        "RED archive missing-object",
        1,
        "archive object coverage differs",
    );
    tally.control = Control::Archive("object-digest".to_owned());
    tally.arm(
        "RED archive object-digest",
        1,
        "archive object digest differs",
    );
    tally.control = Control::Archive("unknown-field".to_owned());
    tally.arm(
        "RED archive unknown-field",
        1,
        "unknown archive descriptor fields",
    );
    tally.control = Control::Archive("unsafe-path".to_owned());
    tally.arm("RED archive unsafe-path", 1, "unsafe archive path");
    tally.control = Control::Archive("string-count".to_owned());
    tally.arm(
        "RED archive string-count",
        1,
        "archive counts must be positive integers",
    );
    tally.control = Control::Archive("duplicate-key".to_owned());
    tally.arm("RED archive duplicate-key", 1, "duplicate descriptor key");
    tally.control = Control::Archive("oversized-index".to_owned());
    tally.arm(
        "RED archive oversized-index",
        1,
        "archive index exceeds bound",
    );
    tally.control = Control::Archive("duplicate-member".to_owned());
    tally.arm(
        "RED archive duplicate-member",
        1,
        "duplicate archive member",
    );
    tally.control = Control::Archive("extra-member".to_owned());
    tally.arm("RED archive extra-member", 1, "extra archive member");
    tally.control = Control::Archive("unsafe-member".to_owned());
    tally.arm("RED archive unsafe-member", 1, "unsafe archive member path");
    tally.control = Control::Archive("shard-digest".to_owned());
    tally.arm(
        "RED archive shard-digest",
        1,
        "archived shard digest differs",
    );
    tally.control = Control::Archive("expansion-bound".to_owned());
    tally.arm(
        "RED archive expansion-bound",
        1,
        "archive expansion exceeds bound",
    );
    tally.control = Control::Archive("missing-index".to_owned());
    tally.arm("RED archive missing-index", 1, "missing archive index");
    tally.control = Control::Archive("previous-descriptor".to_owned());
    tally.arm(
        "RED archive previous-descriptor",
        1,
        "changed or removed committed archive descriptor",
    );
    tally.control = Control::Archive("duplicate-heading".to_owned());
    tally.arm("RED archive duplicate-heading", 1, "DUPLICATED ENTRY");
    tally.control = Control::Archive("duplicate-location".to_owned());
    tally.arm(
        "RED archive duplicate-location",
        1,
        "DUPLICATE ARCHIVED PATH",
    );
    tally.control = Control::Archive("invalid-deflate".to_owned());
    tally.arm(
        "RED archive invalid-deflate",
        1,
        "unreadable archive object (public normal/optimized)",
    );
    tally.control = Control::Predecessor {
        mutation: None,
        optimized: false,
    };
    tally.arm("GREEN complete predecessor controls", 0, "OK");
    tally.control = Control::Predecessor {
        mutation: None,
        optimized: true,
    };
    tally.arm("GREEN optimized predecessor controls", 0, "OK");
    tally.control = Control::Predecessor {
        mutation: Some("no-predecessor".to_owned()),
        optimized: false,
    };
    tally.arm("RED omitted no-predecessor", 1, "FAILED (failures=");
    tally.control = Control::Predecessor {
        mutation: Some("no-predecessor".to_owned()),
        optimized: true,
    };
    tally.arm(
        "RED optimized omitted no-predecessor",
        1,
        "FAILED (failures=",
    );
    tally.control = Control::Predecessor {
        mutation: Some("no-order".to_owned()),
        optimized: false,
    };
    tally.arm("RED omitted no-order", 1, "FAILED (failures=");
    tally.control = Control::Predecessor {
        mutation: Some("no-order".to_owned()),
        optimized: true,
    };
    tally.arm("RED optimized omitted no-order", 1, "FAILED (failures=");
    tally.control = Control::Predecessor {
        mutation: Some("no-staged-partition".to_owned()),
        optimized: false,
    };
    tally.arm("RED omitted no-staged-partition", 1, "FAILED (failures=");
    tally.control = Control::Predecessor {
        mutation: Some("no-staged-partition".to_owned()),
        optimized: true,
    };
    tally.arm(
        "RED optimized omitted no-staged-partition",
        1,
        "FAILED (failures=",
    );
    tally.control = Control::Predecessor {
        mutation: Some("ignore-git-error".to_owned()),
        optimized: false,
    };
    tally.arm("RED omitted ignore-git-error", 1, "FAILED (failures=");
    tally.control = Control::Predecessor {
        mutation: Some("ignore-git-error".to_owned()),
        optimized: true,
    };
    tally.arm(
        "RED optimized omitted ignore-git-error",
        1,
        "FAILED (failures=",
    );
    tally.control = Control::Predecessor {
        mutation: Some("no-shard-wrapper".to_owned()),
        optimized: false,
    };
    tally.arm("RED omitted no-shard-wrapper", 1, "FAILED (failures=");
    tally.control = Control::Predecessor {
        mutation: Some("no-shard-wrapper".to_owned()),
        optimized: true,
    };
    tally.arm(
        "RED optimized omitted no-shard-wrapper",
        1,
        "FAILED (failures=",
    );
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "SHARD-FREEZE --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}

/// `git show HEAD:<path> > <file>`, or no file when the object is not there (the shell's `2>/dev/null` kept).
fn committed(root: &Path, object: &str, file: &Path) -> Option<PathBuf> {
    let shown = Command::new("git")
        .args(["show", &format!("HEAD:{object}")])
        .current_dir(root)
        .stdin(Stdio::null())
        .stderr(Stdio::null())
        .output();
    match shown {
        Ok(o) if o.status.success() && fs::write(file, &o.stdout).is_ok() => {
            Some(file.to_path_buf())
        }
        _ => {
            let _ = fs::remove_file(file);
            None
        }
    }
}

/// `cargo xtask check-changelog-shards [--self-test]`: the shell driver's verdict lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    if !root.join("CHANGELOG.md").is_file() {
        println!("SHARD-FREEZE: ok (no CHANGELOG.md yet)");
        return ExitCode::SUCCESS;
    }
    if !self_test(root, false) {
        eprintln!("SHARD-FREEZE: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    let dir = root.join("target/history-check");
    let _ = fs::create_dir_all(&dir);
    let stamp = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map_or(0, |d| d.as_nanos());
    let pid = std::process::id();
    let prev_file = dir.join(format!("previous.{pid}-{stamp}"));
    let archives_file = dir.join(format!("archives.{pid}-{stamp}"));
    let archives = committed(root, "docs/history/archives.json", &archives_file)
        .map(|p| p.display().to_string())
        .unwrap_or_default();
    let prev = committed(root, "docs/changelog/SHARDS.sha256", &prev_file)
        .map(|p| p.display().to_string())
        .unwrap_or_default();
    let (rc, out) = check_shards(
        root,
        &archives,
        &[
            &root.display().to_string(),
            "docs/changelog",
            "docs/changelog/SHARDS.sha256",
            &prev,
            "CHANGELOG.md",
            "DEV_NOTES.md",
        ],
        false,
    );
    let _ = fs::remove_file(&prev_file);
    let _ = fs::remove_file(&archives_file);
    let out = captured(&out);
    let count = out
        .lines()
        .find_map(|l| l.strip_prefix("__CHECKED__ "))
        .unwrap_or("0");
    let body: Vec<&str> = out
        .lines()
        .filter(|l| !l.starts_with("__CHECKED__ "))
        .collect();
    if rc == 2 {
        eprintln!("SHARD-FREEZE: REFUSED — the shard corpus could not be read, so the freeze cannot be judged.");
        for line in &body {
            eprintln!("  {line}");
        }
        return ExitCode::from(2);
    }
    if rc != 0 {
        eprintln!("SHARD-FREEZE: the sharded history is thawed, incomplete, or rewritten.");
        for line in &body {
            eprintln!("  {line}");
        }
        eprintln!("  Live and archived shards are authoritative. Restore the bytes and committed descriptor");
        eprintln!(
            "  to make the check pass; shard_history.py grows the partition, it never rewrites it."
        );
        return ExitCode::from(1);
    }
    // `predecessor="$(python3 scripts/history_predecessor.py)"`: stdout captured, stderr through.
    let predecessor = Command::new("python3")
        .arg("scripts/history_predecessor.py")
        .current_dir(root)
        .stdin(Stdio::null())
        .stderr(Stdio::inherit())
        .output();
    let (prc, ptext) = match predecessor {
        Ok(o) => (
            o.status.code().unwrap_or(-1),
            String::from_utf8_lossy(&o.stdout).into_owned(),
        ),
        Err(e) => (127, e.to_string()),
    };
    let ptext = captured(&ptext);
    if prc != 0 {
        eprintln!("{ptext}");
        return ExitCode::from(u8::try_from(prc).unwrap_or(1));
    }
    println!("{ptext}");
    println!("SHARD-FREEZE: ok ({count} shard row(s) frozen, 2 heads + shards append-only, exactly partitioned)");
    ExitCode::SUCCESS
}
