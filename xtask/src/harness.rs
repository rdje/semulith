//! What the doctrine modules ported from bash share (`XTASK.6`): a scratch directory under `target/` in
//! place of the scripts' `mktemp -d`, and a child's exit code with its combined output in place of their
//! `out="$(… 2>&1)"; rc=$?`, the system `sort` for the scripts' locale-collated order, and the external
//! hasher (`sha256sum`, else `shasum -a 256`) the scripts hashed with — no new crate.

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

/// The hasher the script would pick: `sha256sum` when on `PATH`, else `shasum -a 256`.
pub struct Hasher {
    program: &'static str,
    args: &'static [&'static str],
}

impl Hasher {
    /// The first hasher that hashes `/dev/null` successfully, as the script's preflight required.
    pub fn find() -> Option<Self> {
        let candidates = [
            Hasher {
                program: "sha256sum",
                args: &[],
            },
            Hasher {
                program: "shasum",
                args: &["-a", "256"],
            },
        ];
        // The script chose by `command -v`, then required the chosen one to work: a hasher that exists but
        // fails is a refusal, not a fall-through to the next.
        let chosen = candidates.into_iter().find(|h| on_path(h.program))?;
        let works = Command::new(chosen.program)
            .args(chosen.args)
            .arg("/dev/null")
            .stdin(Stdio::null())
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .status()
            .is_ok_and(|status| status.success());
        works.then_some(chosen)
    }

    /// The first space-separated field of the hasher's first output line (the script's `cut -d' ' -f1`);
    /// the hasher's own errors pass through on stderr.
    pub fn digest(&self, path: &Path) -> String {
        Command::new(self.program)
            .args(self.args)
            .arg(path)
            .stdin(Stdio::null())
            .stderr(Stdio::inherit())
            .output()
            .map(|output| {
                let text = String::from_utf8_lossy(&output.stdout).into_owned();
                let line = text.lines().next().unwrap_or("");
                line.split(' ').next().unwrap_or("").to_owned()
            })
            .unwrap_or_default()
    }
}

/// Whether `program` is an executable file in a `PATH` directory (the script's `command -v`).
pub fn on_path(program: &str) -> bool {
    std::env::var_os("PATH").is_some_and(|path| {
        std::env::split_paths(&path).any(|dir| {
            fs::metadata(dir.join(program)).is_ok_and(|meta| meta.is_file() && executable(&meta))
        })
    })
}

/// Whether a file's mode lets someone execute it.
#[cfg(unix)]
fn executable(meta: &fs::Metadata) -> bool {
    use std::os::unix::fs::PermissionsExt as _;
    meta.permissions().mode() & 0o111 != 0
}

/// Without Unix modes (the wasm32 build of the workspace) a regular file is taken as executable.
#[cfg(not(unix))]
fn executable(_: &fs::Metadata) -> bool {
    true
}
