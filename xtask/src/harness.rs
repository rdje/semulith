//! What the doctrine modules ported from bash share (`XTASK.6`): a scratch directory under `target/` in
//! place of the scripts' `mktemp -d`, and a child's exit code with its combined output in place of their
//! `out="$(… 2>&1)"; rc=$?`, and the system `sort` for the scripts' locale-collated order.

use std::fs;
use std::io::Write as _;
use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};
use std::time::{SystemTime, UNIX_EPOCH};

/// A fresh directory `<root>/<under>/<prefix>.<unique>`, created empty, as the scripts' `mktemp -d` made.
pub fn scratch(root: &Path, under: &str, prefix: &str) -> std::io::Result<PathBuf> {
    let base = root.join(under);
    fs::create_dir_all(&base)?;
    let stamp = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map_or(0, |d| d.as_nanos());
    for attempt in 0..100u32 {
        let dir = base.join(format!("{prefix}.{}-{stamp}-{attempt}", std::process::id()));
        match fs::create_dir(&dir) {
            Ok(()) => return Ok(dir),
            Err(error) if error.kind() == std::io::ErrorKind::AlreadyExists => {}
            Err(error) => return Err(error),
        }
    }
    Err(std::io::Error::other("no free scratch directory"))
}

/// Runs a command with stdin closed and returns its exit code (`-1` for a signal or a failure to start)
/// and its standard output followed by its standard error.
pub fn combined(command: &mut Command) -> (i32, String) {
    match command.stdin(Stdio::null()).output() {
        Ok(output) => {
            let mut text = String::from_utf8_lossy(&output.stdout).into_owned();
            text.push_str(&String::from_utf8_lossy(&output.stderr));
            (output.status.code().unwrap_or(-1), text)
        }
        Err(error) => (
            -1,
            format!("cannot run {:?}: {error}", command.get_program()),
        ),
    }
}

/// Sorts lines with the system `sort`, so the order is the locale's collation, as the script's was.
pub fn locale_sorted(lines: Vec<String>) -> Vec<String> {
    if lines.is_empty() {
        return lines;
    }
    let child = Command::new("sort")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::null())
        .spawn();
    let Ok(mut child) = child else {
        return lines;
    };
    let mut input = lines.join("\n");
    input.push('\n');
    if let Some(mut stdin) = child.stdin.take() {
        let _ = stdin.write_all(input.as_bytes());
    }
    match child.wait_with_output() {
        Ok(output) if output.status.success() => String::from_utf8_lossy(&output.stdout)
            .lines()
            .map(str::to_owned)
            .collect(),
        _ => lines,
    }
}
