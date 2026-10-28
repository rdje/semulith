//! The `README-ROUTING-CLOSURE` doctrine's driver, ported from `scripts/check_readme_routes.sh` (`XTASK.6` slice
//! `6at`), which is now a shim of `cargo xtask check-readme-routes`.
//!
//! Moving content out of the landing page is not enough if the destination becomes an unbounded neighbouring sink, so
//! every destination the landing page links to and every path-shaped destination the README guard actually emits in
//! its failure guidance must be governed by a row of `doctrine/readme_routes.tsv`; every governed destination exists
//! and carries a known class; declared ceilings block and health targets are reported; a partitioned family's per-part
//! ceiling exempts a member only as a regeneration-gated mirror; and the registry owns the landing page's own caps,
//! applied by re-running the README guard with them. The three Python programs the script ran on `python3 -`'s stdin
//! (the link parser, the family measure, the registry reader) run verbatim, as before; `wc`, the README guard and the
//! hint extraction pipeline (`grep -oE | tr | sort -u` under `pipefail`) are spawned as the script spawned them, so
//! the controls' `PATH`-shadowed `git`, `wc`, `python3`, `sort` and `grep` meet the same calls: every child of a
//! fixture runs under that fixture's exported environment. The script's controls also redefined five shell functions
//! inside subshells (the family measure, the registry reader, the regeneration-set check, the hint producer, and the
//! row reader called alone); here those are `Seams` the self-test alone sets. Each self-test arm is one `tally.arm(`
//! call, the idiom the `DERIVED-COUNTS` arm total counts.

use std::fs;
use std::io::Write;
use std::path::{Path, PathBuf};
use std::process::{Command, ExitCode, Output, Stdio};

use crate::harness::scratch;

const REGISTRY: &str = "doctrine/readme_routes.tsv";
const KNOWN_LIFECYCLES: &[&str] = &[
    "hot_live",
    "partitioned",
    "generated_index",
    "append_history",
    "frozen",
    "normative",
    "archive_terminal",
];
/// The closed regeneration-doctrine set of the two-tier per-part rule (`decision_derived-members-of-bounded-families`).
const REGEN_GOVERNORS: &[&str] = &[
    "STATE-GEN",
    "DEF-GEN",
    "GUEST-GEN",
    "BOARD-GEN",
    "GATE-REPORT",
    "MATERIALS-BILL",
    "BOOK-INDEX",
    "PLATFORM-GEN",
];
const KNOWN_ROUTE_CLASSES: &[&str] = &["reader_navigation", "author_overflow", "both"];

/// `readme_link_targets`, verbatim: `python3 - <readme>` — the sorted relative link targets.
const LINK_TARGETS: &str = r####"import re, sys, pathlib
s = pathlib.Path(sys.argv[1]).read_text()
out = set()
for _, t in re.findall(r'\[([^\]]+)\]\(([^)]+)\)', s):
    if t.startswith(("http://", "https://", "#", "mailto:")):
        continue
    out.add(t.split("#")[0])
print("\n".join(sorted(x for x in out if x)))
"####;
/// `family_measure`, verbatim: `python3 - <base> <destination> <git|find>` — `@totals`, then one `size\tname` per member.
const FAMILY_MEASURE: &str = r####"import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys

base = Path(sys.argv[1])
dest, mode = sys.argv[2:]

def require(ok, reason):
    if not ok:
        raise ValueError(reason)

def safe(name):
    p = PurePosixPath(name)
    require(name != '.' and not p.is_absolute() and str(p) == name and '..' not in p.parts
            and '\\' not in name and all(32 <= ord(c) != 127 for c in name),
            'unsafe member path')
    return p

def owned(name):
    cursor = base
    for part in safe(name).parts:
        cursor /= part
        info = cursor.lstat()
        require(not stat.S_ISLNK(info.st_mode), 'symlink member or parent: ' + name)
        require(info.st_dev == device, 'off-volume member or parent: ' + name)
        marker = cursor / '.git'
        require(not marker.is_symlink() and not marker.exists(),
                'nested Git boundary: ' + name)
    return cursor, info

def identity(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_size,
            info.st_mtime_ns, info.st_ctime_ns)

def walk_error(error):
    raise error

try:
    device = base.stat().st_dev
    require(dest.endswith('/') and str(safe(dest[:-1])) == dest[:-1],
            'unsafe family destination')
    directory, info = owned(dest[:-1])
    require(stat.S_ISDIR(info.st_mode), 'family is not a directory')
    if mode == 'git':
        result = subprocess.run(['git', '-C', str(base), 'ls-files', '-z', '--', dest],
                                capture_output=True, timeout=30)
        require(result.returncode == 0 and not result.stderr,
                'Git inventory failed or wrote stderr (status ' + str(result.returncode) + ')')
        raw = result.stdout
        require(not raw or raw.endswith(b'\0'), 'incomplete NUL inventory')
        names = [v.decode('utf-8') for v in raw.split(b'\0')[:-1]]
    elif mode == 'find':
        names = []
        for parent, directories, files in os.walk(directory, onerror=walk_error):
            for child in directories:
                owned((Path(parent) / child).relative_to(base).as_posix())
            names.extend((Path(parent) / child).relative_to(base).as_posix()
                         for child in files)
    else:
        raise ValueError('unknown family listing mode')
    require(len(names) == len(set(names)), 'duplicate family member')
    measured = []
    for name in sorted(names):
        safe(name)
        require(name.startswith(dest), 'member outside family: ' + name)
        path, info = owned(name)
        require(stat.S_ISREG(info.st_mode), 'non-regular family member: ' + name)
        measured.append((name, path, identity(info), info.st_size))
    for name, path, before, size in measured:
        require(identity(path.lstat()) == before, 'member changed during measurement: ' + name)
    print('@totals\t' + str(len(measured)) + '\t' + str(sum(row[3] for row in measured)))
    for name, path, before, size in measured:
        print(str(size) + '\t' + name)
except (OSError, ValueError, subprocess.SubprocessError) as error:
    reason = error.strerror if isinstance(error, OSError) else str(error)
    print('  UNREADABLE family ' + dest + ': ' + reason, file=sys.stderr)
    sys.exit(2)
"####;
/// `registry_text`, verbatim: `python3 - <registry>` — the registry's text, or a refusal on binary or control data.
const REGISTRY_TEXT: &str = r####"from pathlib import Path
import sys
try:
    text = Path(sys.argv[1]).read_bytes().decode('utf-8').replace('\r\n', '\n')
    if any((ord(c) < 32 and c not in '\t\n') or ord(c) == 127 for c in text):
        raise ValueError('unexpected control character')
    sys.stdout.write(text)
except (OSError, UnicodeError, ValueError) as error:
    print('UNREADABLE registry text: ' + str(error), file=sys.stderr)
    sys.exit(2)
"####;
/// The hint extraction, as the script piped it under `set -o pipefail`; `$1` the guidance, `$2` the pattern, `$3` the
/// diagnostics file.
const HINT_PIPELINE: &str =
    "set -o pipefail; { printf '%s\\n' \"$1\" | grep -oE \"$2\" | tr -d ' ' | sort -u; } 2> \"$3\"";
const HINT_PATTERN: &str =
    "(^| )[A-Za-z_][A-Za-z0-9_.-]*(/[A-Za-z0-9_.-]*)+|(^| )[A-Z][A-Z0-9_]*\\.md";

/// The self-test's fixture scripts, verbatim.
const FX_GIT: &str = r####"#!/usr/bin/env python3
import os, sys
mode = os.environ['ROUTE_FIXTURE_MODE']
names = {
    'empty': [], 'duplicate': ['docs/inner.md', 'docs/inner.md'],
    'outside': ['KEEP.md'], 'traversal': ['docs/../KEEP.md'],
    'missing': ['docs/missing.md'], 'symlink': ['docs/link.md'],
    'directory': ['docs/subdir'], 'unicode': ['docs/café name.md'],
}.get(mode, ['docs/inner.md', 'docs/space name.md'])
if mode in {'failed', 'partial_stderr', 'failed_partial'}:
    sys.stderr.write('controlled inventory error\n')
if mode in {'failed', 'failed_silent'}: sys.exit(73)
if mode == 'partial_stderr': names = names[:1]
sys.stdout.buffer.write(b'\0'.join(n.encode() for n in names) + (b'\0' if names else b''))
if mode == 'malformed': sys.stdout.buffer.write(b'unterminated')
if mode == 'failed_partial': sys.exit(73)
"####;
const FX_WC: &str = r####"#!/bin/sh
if [ "$1" = -c ]; then
 case "$ROUTE_READ_MODE" in
 file_status) printf 'controlled measurement failure\n' >&2; exit 73 ;;
 file_silent) exit 73 ;;
 file_failed_value) "$ROUTE_READ_WC" "$@"; exit 73 ;;
 file_stderr) "$ROUTE_READ_WC" "$@"; printf 'controlled measurement diagnostic\n' >&2; exit 0 ;;
 file_bad) printf 'invalid\n'; exit 0 ;;
 file_extra) printf '1\n2\n'; exit 0 ;;
 esac
fi
if [ "$1" = -l ] && [ "$ROUTE_READ_MODE" = file_line_status ]; then exit 73; fi
exec "$ROUTE_READ_WC" "$@"
"####;
const FX_PYTHON: &str = r####"#!/bin/sh
if [ "$#" -eq 2 ] && [ "$1" = - ] && [ "$2" = "$ROUTE_READ_FIXTURE/README.md" ]; then
 case "$ROUTE_READ_MODE" in
 parser_status) printf 'controlled parser failure\n' >&2; exit 73 ;;
 parser_silent) exit 73 ;;
 parser_stderr) printf 'KEEP.md\n'; printf 'controlled partial parser\n' >&2; exit 0 ;;
 esac
fi
exec "$ROUTE_READ_PYTHON" "$@"
"####;
const FX_HINT: &str = r####"#!/bin/sh
case "$ROUTE_READ_MODE" in
 hint_empty) exit 1 ;;
 hint_no_contract) printf 'README_POLICY.md\n' >&2; exit 1 ;;
esac
printf 'Route the new detail to its canonical home\n' >&2
if [ "$ROUTE_READ_MODE" != hint_no_destinations ]; then printf 'README_POLICY.md\n' >&2; fi
case "$ROUTE_READ_MODE" in hint_status) exit 73 ;; hint_success) exit 0 ;; esac
exit 1
"####;
const FX_SORT: &str = r####"#!/bin/sh
case "$ROUTE_READ_MODE" in
 hint_sort_status) cat; exit 73 ;;
 hint_sort_stderr) cat; printf 'controlled extraction diagnostic\n' >&2; exit 0 ;;
esac
exec "$ROUTE_READ_SORT" "$@"
"####;
const FX_GREP: &str = r####"#!/bin/sh
if [ "$1" = -cE ]; then
 case "$ROUTE_READ_MODE" in
 date_status) printf '0\n'; exit 73 ;;
 date_stderr) printf '0\n'; printf 'controlled date diagnostic\n' >&2; exit 0 ;;
 date_empty) exit 0 ;;
 esac
fi
if [ "$1" = -cF ]; then
 case "$ROUTE_READ_MODE" in
 policy_status) printf '1\n'; exit 73 ;;
 policy_stderr) printf '1\n'; printf 'controlled policy diagnostic\n' >&2; exit 0 ;;
 policy_empty) exit 0 ;;
 esac
fi
exec "$ROUTE_READ_GREP" "$@"
"####;
const FX_README_GIT: &str = r####"#!/bin/sh
if [ "$#" -eq 2 ] && [ "$1" = rev-parse ] && [ "$2" = --show-toplevel ]; then
 printf '%s\n' "$ROUTE_READ_PROJECT"; exit 0
fi
exit 73
"####;

/// The script's shell functions a control redefined inside its subshell; production leaves them all unset.
#[derive(Clone, Copy, Default)]
struct Seams {
    /// `table_fixture`'s `family_measure`: `empty`, `bad_count` or `extra`.
    family_measure: Option<&'static str>,
    /// `registry_fixture`'s and `registry_main_fixture`'s `registry_text`: `status`, `diagnostic` or `silent`.
    registry_text: Option<&'static str>,
    /// `registry_main_fixture`'s `regen_set_registered` (succeeds) and `emitted_hint_targets` (`README_POLICY.md`).
    main_stubs: bool,
}

/// The shell the functions ran in: its working directory, `$ROOT`, the variables a fixture exported, the seams.
#[derive(Clone)]
struct Ctx {
    cwd: PathBuf,
    root: PathBuf,
    env: Vec<(String, String)>,
    seams: Seams,
}

impl Ctx {
    fn real(root: &Path) -> Self {
        Ctx {
            cwd: root.to_path_buf(),
            root: root.to_path_buf(),
            env: Vec::new(),
            seams: Seams::default(),
        }
    }

    /// A path as the shell resolved it: relative to the working directory.
    fn path(&self, p: &str) -> PathBuf {
        let q = Path::new(p);
        if q.is_absolute() {
            q.to_path_buf()
        } else {
            self.cwd.join(q)
        }
    }

    /// `PATH` lookup through the fixture's exported `PATH` when it set one — the shell's own resolution.
    fn which(&self, name: &str) -> PathBuf {
        let path = self
            .env
            .iter()
            .rev()
            .find(|(k, _)| k == "PATH")
            .map(|(_, v)| std::ffi::OsString::from(v))
            .or_else(|| std::env::var_os("PATH"))
            .unwrap_or_default();
        std::env::split_paths(&path)
            .map(|dir| dir.join(name))
            .find(|p| p.is_file())
            .unwrap_or_else(|| PathBuf::from(name))
    }

    /// A child as the shell spawned it: resolved through the fixture's `PATH`, in the working directory, under the
    /// exported variables, stdin closed.
    fn command(&self, program: &str) -> Command {
        let mut command = Command::new(self.which(program));
        command.current_dir(&self.cwd).stdin(Stdio::null());
        for (k, v) in &self.env {
            command.env(k, v);
        }
        command
    }

    /// `python3 - <args…>` with a program on stdin: stdout, stderr and the status, apart.
    fn python(&self, program: &str, args: &[&str]) -> (i32, String, String) {
        let mut command = self.command("python3");
        command
            .arg("-")
            .args(args)
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped());
        let Ok(mut child) = command.spawn() else {
            return (127, String::new(), "python3: not found\n".to_owned());
        };
        if let Some(mut stdin) = child.stdin.take() {
            let _ = stdin.write_all(program.as_bytes());
        }
        split(child.wait_with_output())
    }

    /// `"$@" 2>&1`: a command's merged output in write order (through `bash -c`, which joins the two streams), and its
    /// status.
    fn merged(&self, extra_env: &[(&str, &str)], args: &[&str]) -> (i32, String) {
        let mut command = self.command("bash");
        command.arg("-c").arg("\"$@\" 2>&1").arg("bash").args(args);
        for (k, v) in extra_env {
            command.env(k, v);
        }
        let (rc, out, _) = split(command.output());
        (rc, out)
    }
}

fn split(output: std::io::Result<Output>) -> (i32, String, String) {
    match output {
        Ok(o) => (
            o.status.code().unwrap_or(-1),
            String::from_utf8_lossy(&o.stdout).into_owned(),
            String::from_utf8_lossy(&o.stderr).into_owned(),
        ),
        Err(e) => (127, String::new(), format!("{e}\n")),
    }
}

/// The shell's `$(…)`: every trailing newline removed.
fn captured(text: &str) -> &str {
    text.trim_end_matches('\n')
}

/// The lines `while IFS= read -r line` sees: every newline-terminated line (a final unterminated one is not read).
fn read_lines(text: &str) -> Vec<&str> {
    text.split_inclusive('\n')
        .filter(|l| l.ends_with('\n'))
        .map(|l| l.trim_end_matches('\n'))
        .collect()
}

/// `<<< "$text"`: a here-string's lines (the shell appends the newline the last line lacks).
fn here_lines(text: &str) -> Vec<&str> {
    text.split('\n').collect()
}

/// `[[ "$v" =~ ^[0-9]+$ ]]`.
fn is_number(v: &str) -> bool {
    !v.is_empty() && v.bytes().all(|b| b.is_ascii_digit())
}

/// `[ "$a" -gt "$b" ]` on the decimal fields this script compares (validated, at most a signed 64-bit value).
fn gt(a: &str, b: &str) -> bool {
    match (a.parse::<u128>(), b.parse::<u128>()) {
        (Ok(x), Ok(y)) => x > y,
        _ => false,
    }
}

/// Output in the order the shell wrote it; `true` marks a line written to stderr.
#[derive(Default)]
struct Sink {
    items: Vec<(bool, String)>,
}

impl Sink {
    fn out(&mut self, line: impl AsRef<str>) {
        self.items.push((false, format!("{}\n", line.as_ref())));
    }
    fn err(&mut self, line: impl AsRef<str>) {
        self.items.push((true, format!("{}\n", line.as_ref())));
    }
    fn out_raw(&mut self, text: impl Into<String>) {
        self.items.push((false, text.into()));
    }
    /// `2>&1`: both streams, in write order.
    fn merged(&self) -> String {
        self.items.iter().map(|(_, s)| s.as_str()).collect()
    }
    fn stdout(&self) -> String {
        self.items
            .iter()
            .filter(|(e, _)| !e)
            .map(|(_, s)| s.as_str())
            .collect()
    }
    /// The real streams, in the order written (stdout is line-buffered, stderr unbuffered).
    fn replay(&self) {
        for (is_err, text) in &self.items {
            if *is_err {
                eprint!("{text}");
            } else {
                print!("{text}");
                let _ = std::io::stdout().flush();
            }
        }
    }
}

/// `regen_set_registered <driver>`: every regeneration-set member must be a registered project doctrine.
fn regen_set_registered(ctx: &Ctx, driver: &str) -> (i32, String) {
    let text = fs::read_to_string(ctx.path(driver)).unwrap_or_default();
    for g in REGEN_GOVERNORS {
        let head = format!("  \"{g}|");
        if !text.lines().any(|l| l.starts_with(&head)) {
            return (
                1,
                format!("  REGEN SET DRIFT: {g} is in the regeneration set but not registered in {driver}\n"),
            );
        }
    }
    (0, String::new())
}

/// `derived_exempt <member> <registry>`: a member is exempt only as a mirror whose governor is in the regeneration set.
fn derived_exempt(ctx: &Ctx, member: &str, registry: &str) -> bool {
    if registry.is_empty() {
        return false;
    }
    let path = ctx.path(registry);
    if !path.is_file() {
        return false;
    }
    let text = fs::read_to_string(path).unwrap_or_default();
    for line in read_lines(&text) {
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        let fields: Vec<&str> = line.splitn(4, '\t').collect();
        let mirror = fields.get(2).copied().unwrap_or("");
        let gov = fields
            .get(3)
            .map(|g| g.replace('\t', "\u{1f}"))
            .unwrap_or_default();
        if mirror != member {
            continue;
        }
        if REGEN_GOVERNORS.contains(&gov.as_str()) {
            return true;
        }
    }
    false
}

/// `governed <target> <destinations>`: an exact row, or a directory row that is a prefix.
fn governed(target: &str, destinations: &[String]) -> bool {
    destinations
        .iter()
        .filter(|d| !d.is_empty())
        .any(|d| target == d || (d.ends_with('/') && target.starts_with(d.as_str())))
}

/// `registry_text <file>`: the registry's text through the Python reader (or a control's redefinition).
fn registry_text(ctx: &Ctx, file: &str) -> (i32, String, String) {
    match ctx.seams.registry_text {
        Some(mode) => {
            let text = if mode == "silent" {
                String::new()
            } else {
                fs::read_to_string(ctx.path(file)).unwrap_or_default()
            };
            if mode == "diagnostic" {
                return (0, text, "controlled registry diagnostic\n".to_owned());
            }
            (73, text, String::new())
        }
        None => ctx.python(REGISTRY_TEXT, &[file]),
    }
}

/// `case "$dest" in ''|.|/*|./*|../*|*/../*|*/..|*/./*|*/.|*//*|*\\*)`.
fn unnormalized(dest: &str) -> bool {
    dest.is_empty()
        || dest == "."
        || dest.starts_with('/')
        || dest.starts_with("./")
        || dest.starts_with("../")
        || dest.contains("/../")
        || dest.ends_with("/..")
        || dest.contains("/./")
        || dest.ends_with("/.")
        || dest.contains("//")
        || dest.contains('\\')
}

/// `read_registry_rows <file>`: the complete registry, validated and normalized, or nothing at all (the refusal on
/// stderr). The returned text is what `printf '%s' "$output"` printed.
fn read_registry_rows(ctx: &Ctx, file: &str, sink: &mut Sink) -> Option<String> {
    let (rc, data, err) = registry_text(ctx, file);
    if rc != 0 || !err.is_empty() {
        sink.err("  UNREADABLE registry read: failed status or diagnostics");
        return None;
    }
    let mut output = String::new();
    let mut seen: Vec<String> = Vec::new();
    for line in here_lines(captured(&data)) {
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        if line.matches('\t').count() != 8 {
            sink.err("  UNREADABLE registry row: expected nine tab-separated fields");
            return None;
        }
        let f: Vec<&str> = line.split('\t').collect();
        let dest = f[0];
        if unnormalized(dest) {
            sink.err("  UNREADABLE registry row: destination must be a normalized relative path");
            return None;
        }
        if seen.iter().any(|s| s == dest) {
            sink.err("  UNREADABLE registry row: duplicate destination");
            return None;
        }
        seen.push(dest.to_owned());
        let mut normalized = Vec::new();
        for value in &f[4..9] {
            if !is_number(value) {
                sink.err("  UNREADABLE registry limits: expected nonnegative decimal integers");
                return None;
            }
            let trimmed = value.trim_start_matches('0');
            let value = if trimmed.is_empty() { "0" } else { trimmed };
            if value.len() > 19 || (value.len() == 19 && value > "9223372036854775807") {
                sink.err("  UNREADABLE registry limits: integer exceeds signed-64-bit range");
                return None;
            }
            normalized.push(value.to_owned());
        }
        output.push_str(&format!(
            "{}\t{}\t{}\t{}\t{}\n",
            dest,
            f[1],
            f[2],
            f[3],
            normalized.join("\t")
        ));
    }
    Some(output)
}

/// `read_scalar_count <root> 0 <command> < <file>`: one integer from a measuring command, or the refusal.
fn read_scalar_count(ctx: &Ctx, program: &str, flag: &str, file: &Path) -> Result<String, String> {
    let stdin = match fs::File::open(file) {
        Ok(f) => Stdio::from(f),
        Err(e) => return Err(format!("{}: {e}\n", file.display())),
    };
    let mut command = ctx.command(program);
    command.arg(flag).stdin(stdin);
    let (rc, out, err) = split(command.output());
    let value = captured(&out);
    let shape = {
        let core = value.trim_matches(|c: char| c.is_ascii_whitespace());
        is_number(core)
    };
    if rc != 0 || !err.is_empty() || !shape {
        return Err(format!(
            "UNREADABLE scalar count: {program} failed, wrote stderr or returned invalid data (status {rc}).\n"
        ));
    }
    Ok(value.chars().filter(|c| !c.is_ascii_whitespace()).collect())
}

/// `read_text_metrics <root> <file>` with `2>&1`: `lines\tbytes`, or the merged refusal.
fn read_text_metrics(ctx: &Ctx, file: &Path) -> Result<(String, String), String> {
    let mut values = Vec::new();
    for flag in ["-l", "-c"] {
        match read_scalar_count(ctx, "wc", flag, file) {
            Ok(v) => values.push(v),
            Err(message) => {
                return Err(format!(
                    "{message}UNREADABLE text measurement: wc {flag} unavailable.\n"
                ))
            }
        }
    }
    Ok((values[0].clone(), values[1].clone()))
}

/// `family_measure <base> <destination> <mode>`: stdout, stderr and the status (or a control's redefinition).
fn family_measure(ctx: &Ctx, base: &str, dest: &str, mode: &str) -> (i32, String, String) {
    match ctx.seams.family_measure {
        Some("bad_count") => (0, "@totals\tinvalid\t2\n".to_owned(), String::new()),
        Some("extra") => (0, "@totals\t1\t2\textra\n".to_owned(), String::new()),
        Some(_) => (0, String::new(), String::new()),
        None => ctx.python(FAMILY_MEASURE, &[base, dest, mode]),
    }
}

/// `IFS=$'\t' read -r tag n b`: the first line's three fields (tab is IFS whitespace: runs collapse, the ends trim,
/// the last field keeps the rest).
fn totals(parts: &str) -> Option<(String, String, String)> {
    let first = parts.split_inclusive('\n').next()?;
    if !first.ends_with('\n') {
        return None;
    }
    let line = first.trim_end_matches('\n').trim_matches('\t');
    let (tag, rest) = line.split_once('\t').unwrap_or((line, ""));
    let rest = rest.trim_start_matches('\t');
    let (n, b) = rest.split_once('\t').unwrap_or((rest, ""));
    Some((
        tag.to_owned(),
        n.to_owned(),
        b.trim_start_matches('\t').to_owned(),
    ))
}

/// `verify_routes <registry> <readme> <enforce> <base> <mode> <fact-ownership>`: the closure's verdict — 0, 1 for a
/// breach, 2 when an input cannot be read.
#[allow(clippy::too_many_arguments)]
fn verify_routes(
    ctx: &Ctx,
    registry: &str,
    readme: &str,
    enforce: bool,
    base: &str,
    mode: &str,
    fo: &str,
    sink: &mut Sink,
) -> i32 {
    let mut bad = 0;
    let mut unreadable = false;
    if !ctx.path(registry).is_file() {
        sink.out(format!("  MISSING registry {registry}"));
        return 1;
    }
    if !ctx.path(readme).is_file() {
        sink.out(format!("  MISSING landing page {readme}"));
        return 1;
    }
    let Some(rows) = read_registry_rows(ctx, registry, sink) else {
        return 2;
    };
    let rows = captured(&rows).to_owned();
    if rows.is_empty() {
        sink.out(format!("  EMPTY registry {registry}"));
        return 1;
    }
    let destinations: Vec<String> = here_lines(&rows)
        .iter()
        .map(|l| l.split('\t').next().unwrap_or("").to_owned())
        .collect();

    // (1) every linked destination is governed
    let (rc, links, errors) = ctx.python(LINK_TARGETS, &[readme]);
    if rc != 0 || !errors.is_empty() {
        sink.out("  UNREADABLE landing-page links");
        unreadable = true;
    } else {
        for t in read_lines(&links) {
            if t.is_empty() {
                continue;
            }
            if !governed(t, &destinations) {
                sink.out(format!("  UNGOVERNED link target '{t}' — no registry row"));
                bad = 1;
            }
        }
    }

    // (3)+(4) rows: existence, classes, ceilings, health
    for line in here_lines(&rows) {
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        let f: Vec<&str> = line.split('\t').collect();
        let (dest, rclass, life, owner) = (f[0], f[1], f[2], f[3]);
        let (hl, hb, cl, cb, cp) = (f[4], f[5], f[6], f[7], f[8]);
        if !KNOWN_ROUTE_CLASSES.contains(&rclass) {
            sink.out(format!("  UNKNOWN route_class '{rclass}' for {dest}"));
            bad = 1;
        }
        if !KNOWN_LIFECYCLES.contains(&life) {
            sink.out(format!("  UNKNOWN lifecycle '{life}' for {dest}"));
            bad = 1;
        }
        if owner.is_empty() {
            sink.out(format!("  NO OWNER declared for {dest}"));
            bad = 1;
        }
        let target = format!("{base}/{dest}");
        if dest.ends_with('/') {
            if !Path::new(&target).is_dir() {
                sink.out(format!("  MISSING destination directory {dest}"));
                bad = 1;
                continue;
            }
            if !enforce {
                continue;
            }
            let (rc, parts, errors) = family_measure(ctx, base, dest, mode);
            if rc != 0 {
                sink.out_raw(errors);
                unreadable = true;
                continue;
            }
            let Some((_, n, b)) = totals(&parts)
                .filter(|(tag, n, b)| tag == "@totals" && is_number(n) && is_number(b))
            else {
                sink.out(format!("  UNREADABLE family totals for {dest}"));
                unreadable = true;
                continue;
            };
            if gt(cl, "0") && gt(&n, cl) {
                sink.out(format!("  OVER CEILING {dest}: {n} files > {cl}"));
                bad = 1;
            }
            if gt(cb, "0") && gt(&b, cb) {
                sink.out(format!("  OVER CEILING {dest}: {b} aggregate bytes > {cb}"));
                bad = 1;
            }
            if gt(hl, "0") && gt(&n, hl) {
                sink.out(format!("  health: {dest} holds {n} files (target {hl})"));
            }
            if gt(hb, "0") && gt(&b, hb) {
                sink.out(format!(
                    "  health: {dest} holds {b} aggregate bytes (target {hb})"
                ));
            }
            if gt(cp, "0") {
                for big in read_lines(&parts) {
                    if big.starts_with("@totals\t") || big.is_empty() {
                        continue;
                    }
                    let (size, name) = big.split_once('\t').unwrap_or((big, big));
                    if !gt(size, cp) {
                        continue;
                    }
                    let rel = name.strip_prefix(&format!("{base}/")).unwrap_or(name);
                    if derived_exempt(ctx, rel, fo) {
                        sink.out(format!("  derived: {rel} ({size} bytes > {cp} authored per-part) is regeneration-gated — exempt (decision_derived-members-of-bounded-families)"));
                    } else {
                        sink.out(format!("  OVER CEILING {dest}: part {rel}"));
                        sink.out(format!("    {size} bytes > {cp}"));
                        bad = 1;
                    }
                }
            }
        } else {
            if !Path::new(&target).is_file() {
                sink.out(format!("  MISSING destination file {dest}"));
                bad = 1;
                continue;
            }
            if !enforce {
                continue;
            }
            let (n, b) = match read_text_metrics(ctx, Path::new(&target)) {
                Ok(v) => v,
                Err(metrics) => {
                    sink.out(format!("  {} ({dest})", captured(&metrics)));
                    unreadable = true;
                    continue;
                }
            };
            if gt(cl, "0") && gt(&n, cl) {
                sink.out(format!("  OVER CEILING {dest}: {n} lines > {cl}"));
                bad = 1;
            }
            if gt(cb, "0") && gt(&b, cb) {
                sink.out(format!("  OVER CEILING {dest}: {b} bytes > {cb}"));
                bad = 1;
            }
            if gt(hl, "0") && gt(&n, hl) {
                sink.out(format!("  health: {dest} is {n} lines (target {hl})"));
            }
            if gt(hb, "0") && gt(&b, hb) {
                sink.out(format!("  health: {dest} is {b} bytes (target {hb})"));
            }
        }
    }
    if unreadable {
        return 2;
    }
    bad
}

/// `emitted_hint_targets [producer]` with `2>&1`: the destinations the README guard's forced-red guidance names.
fn emitted_hint_targets(ctx: &Ctx, producer: &str) -> (i32, String) {
    let (status, raw) = ctx.merged(
        &[("README_LINE_CAP", "0"), ("README_BYTE_CAP", "0")],
        &[producer],
    );
    let raw = captured(&raw).to_owned();
    if status != 1 || !raw.contains("Route the new detail to its canonical home") {
        return (
            2,
            "UNREADABLE emitted-hint producer: expected a forced ceiling breach with routing guidance.\n"
                .to_owned(),
        );
    }
    let Ok(dir) = scratch(&ctx.root, "target/tmp", "hint-errors") else {
        return (2, String::new());
    };
    let errors = dir.join("errors");
    let errors_s = errors.display().to_string();
    let mut command = ctx.command("bash");
    command
        .arg("-c")
        .arg(HINT_PIPELINE)
        .arg("bash")
        .arg(&raw)
        .arg(HINT_PATTERN)
        .arg(&errors_s);
    let (status, targets, _) = split(command.output());
    let targets = captured(&targets).to_owned();
    let diagnostics = fs::metadata(&errors).map(|m| m.len()).unwrap_or(0);
    let _ = fs::remove_dir_all(&dir);
    if status != 0 || diagnostics > 0 || targets.is_empty() {
        return (2, "UNREADABLE emitted-hint destinations\n".to_owned());
    }
    (0, format!("{targets}\n"))
}

/// `main_routes`: the shared entry flow (the self-test runs this same body in an isolated fixture).
fn main_routes(ctx: &Ctx, registry: &str, sink: &mut Sink) -> i32 {
    let mut fail = false;
    let (rc, drift) = if ctx.seams.main_stubs {
        (0, String::new())
    } else {
        regen_set_registered(ctx, "scripts/check_doctrines.project.sh")
    };
    sink.out_raw(drift);
    if rc != 0 {
        sink.err("README-ROUTING-CLOSURE: REFUSED — the regeneration-doctrine set and the driver disagree.");
        return 2;
    }
    let Ok(work) = scratch(&ctx.root, "target/tmp", "registry-snapshot") else {
        return 2;
    };
    let status = main_routes_in(ctx, registry, &work, sink, &mut fail);
    let _ = fs::remove_dir_all(&work);
    status
}

fn main_routes_in(ctx: &Ctx, registry: &str, work: &Path, sink: &mut Sink, fail: &mut bool) -> i32 {
    let Some(rows) = read_registry_rows(ctx, registry, sink) else {
        sink.err("README-ROUTING-CLOSURE: REFUSED — registry inputs unavailable.");
        return 2;
    };
    let rows = captured(&rows).to_owned();
    let rows_file = work.join("rows");
    if fs::write(&rows_file, format!("{rows}\n")).is_err() {
        return 2;
    }
    let mut routes = Sink::default();
    let route_status = verify_routes(
        ctx,
        &rows_file.display().to_string(),
        "README.md",
        true,
        &ctx.root.display().to_string(),
        "git",
        "doctrine/fact_ownership.tsv",
        &mut routes,
    );
    // `out="$(verify_routes …)"`: stdout captured, stderr through.
    for (is_err, text) in &routes.items {
        if *is_err {
            sink.items.push((true, text.clone()));
        }
    }
    let mut out = captured(&routes.stdout()).to_owned();
    if route_status == 2 {
        sink.err(format!(
            "README-ROUTING-CLOSURE: REFUSED — routed inputs unavailable.\n{out}"
        ));
        return 2;
    }
    if route_status != 0 {
        *fail = true;
    }

    // (2) every path-shaped destination the guard actually emits must be governed
    let mut destinations = Vec::new();
    let (mut lc, mut bc) = ("0".to_owned(), "0".to_owned());
    let mut governed_count = 0;
    for line in here_lines(&rows) {
        if line.is_empty() {
            continue;
        }
        let f: Vec<&str> = line.split('\t').collect();
        destinations.push(f[0].to_owned());
        governed_count += 1;
        if f[0] == "README.md" {
            lc = f.get(6).copied().unwrap_or("").to_owned();
            bc = f.get(7).copied().unwrap_or("").to_owned();
        }
    }
    let (rc, hints) = if ctx.seams.main_stubs {
        (0, "README_POLICY.md\n".to_owned())
    } else {
        emitted_hint_targets(ctx, "scripts/check_readme_stability.sh")
    };
    let hints = captured(&hints).to_owned();
    if rc != 0 {
        sink.err(format!(
            "README-ROUTING-CLOSURE: REFUSED — emitted routing guidance unavailable.\n{hints}"
        ));
        return 2;
    }
    for t in here_lines(&hints) {
        if t.is_empty() {
            continue;
        }
        if !governed(t, &destinations) {
            out.push_str(&format!("\n  UNGOVERNED emitted-hint destination '{t}' — the guard routes authors there and nothing bounds it"));
            *fail = true;
        }
    }

    // (5) the registry owns the landing page's own caps
    if !lc.is_empty() && !bc.is_empty() && gt(&lc, "0") && gt(&bc, "0") {
        let (rc, capout) = ctx.merged(
            &[
                ("README_LINE_CAP", lc.as_str()),
                ("README_BYTE_CAP", bc.as_str()),
            ],
            &["scripts/check_readme_stability.sh"],
        );
        let capout = captured(&capout);
        if rc != 0 {
            out.push_str(&format!("\n  {capout}"));
            *fail = true;
        } else {
            out.push_str(&format!("\n  registry caps applied: {capout}"));
        }
    } else {
        out.push_str(
            "\n  README.md has no enforced caps in the registry — the landing page must be bounded",
        );
        *fail = true;
    }

    if *fail {
        sink.err("README-ROUTING-CLOSURE: a routed destination is ungoverned, missing, or over its ceiling.");
        for line in out.split('\n') {
            if !line.is_empty() {
                sink.err(line);
            }
        }
        sink.err(format!(
            "  Give it a row in {registry} with a class, an owner and a bound — or move the content."
        ));
        sink.err(
            "  Raising a ceiling needs a reviewed decision that the surface's contract expanded.",
        );
        return 1;
    }
    sink.out(format!(
        "README-ROUTING-CLOSURE: ok ({governed_count} governed destination(s))"
    ));
    for line in out.split('\n') {
        if line.starts_with("  health:")
            || line.starts_with("  derived:")
            || line.starts_with("  registry caps applied:")
        {
            sink.out(line);
        }
    }
    0
}

/// Write a fixture file; `chmod +x` when `exec`.
fn write(path: &Path, text: &str, exec: bool) {
    let _ = fs::write(path, text);
    if exec {
        #[cfg(unix)]
        {
            use std::os::unix::fs::PermissionsExt as _;
            let _ = fs::set_permissions(path, fs::Permissions::from_mode(0o755));
        }
    }
}

struct Tally {
    pass: u32,
    fail: u32,
    verbose: bool,
}

impl Tally {
    /// One arm: the command's status must be `expected` and its merged output must contain `want` (when given).
    fn arm(&mut self, name: &str, expected: i32, want: &str, (rc, raw): (i32, String)) {
        let out = captured(&raw);
        if rc != expected {
            self.fail += 1;
            if self.verbose {
                eprintln!("README-ROUTING-CLOSURE self-test MISS: {name} expected rc={expected} got rc={rc}\n{out}");
            }
        } else if !want.is_empty() && !out.contains(want) {
            self.fail += 1;
            if self.verbose {
                eprintln!("README-ROUTING-CLOSURE self-test MISS: {name} right verdict, wrong reason (no {want})\n{out}");
            }
        } else {
            self.pass += 1;
        }
    }
}

/// `verify_routes … 2>&1` under a context: the status and the merged output.
fn probe(
    ctx: &Ctx,
    registry: &Path,
    readme: &Path,
    base: &Path,
    mode: &str,
    fo: &Path,
) -> (i32, String) {
    let mut sink = Sink::default();
    let rc = verify_routes(
        ctx,
        &registry.display().to_string(),
        &readme.display().to_string(),
        true,
        &base.display().to_string(),
        mode,
        &fo.display().to_string(),
        &mut sink,
    );
    (rc, sink.merged())
}

/// The RED/GREEN controls against synthetic fixtures. Quiet unless `verbose` (the script ran them `>/dev/null 2>&1`
/// before the real judgement).
fn self_test(repo: &Path, verbose: bool) -> bool {
    let Ok(t) = scratch(repo, "target/doctrine-selftest", "readmeroutes") else {
        if verbose {
            eprintln!("README-ROUTING-CLOSURE self-test: cannot create a scratch directory under target/doctrine-selftest");
        }
        return false;
    };
    let real = Ctx::real(repo);
    let ts = t.display().to_string();
    let path_env = std::env::var("PATH").unwrap_or_default();
    let _ = fs::create_dir_all(t.join("docs"));
    write(
        &t.join("README.md"),
        "# L\n\nSee [a](docs/) and [b](KEEP.md).\n",
        false,
    );
    write(&t.join("KEEP.md"), "x\n", false);
    write(&t.join("docs/inner.md"), "y\n", false);
    let routes = t.join("routes.tsv");
    let readme = t.join("README.md");
    let fact = t.join("fact.tsv");
    let reg = |rows: &[&str]| {
        let text: String = rows.iter().map(|r| format!("{r}\n")).collect();
        write(&routes, &text, false);
    };
    const R_DOCS: &str = "docs/\treader_navigation\tpartitioned\towner\t0\t0\t0\t0\t0";
    const R_KEEP: &str = "KEEP.md\tboth\thot_live\towner\t0\t0\t5\t64\t0";
    let default = || probe(&real, &routes, &readme, &t, "find", &fact);
    let mut tally = Tally {
        pass: 0,
        fail: 0,
        verbose,
    };
    reg(&[R_DOCS, R_KEEP]);
    tally.arm("GREEN every route governed", 0, "", default());
    reg(&[R_DOCS]);
    tally.arm(
        "RED   link target ungoverned",
        1,
        "UNGOVERNED link target 'KEEP.md'",
        default(),
    );
    reg(&[
        R_DOCS,
        R_KEEP,
        "GONE.md\tboth\thot_live\towner\t0\t0\t0\t0\t0",
    ]);
    tally.arm(
        "RED   destination missing",
        1,
        "MISSING destination file GONE.md",
        default(),
    );
    reg(&[
        R_DOCS,
        R_KEEP,
        "nosuch/\tauthor_overflow\tpartitioned\towner\t0\t0\t0\t0\t0",
    ]);
    tally.arm(
        "RED   directory destination missing",
        1,
        "MISSING destination directory nosuch/",
        default(),
    );
    reg(&[
        "docs/\treader_navigation\tpartitioned\towner\t0\t0\t0\t1\t0",
        R_KEEP,
    ]);
    tally.arm(
        "RED   family over aggregate bytes",
        1,
        "OVER CEILING docs/: 2 aggregate bytes > 1",
        default(),
    );
    reg(&[
        "docs/\treader_navigation\tpartitioned\towner\t0\t0\t0\t0\t1",
        R_KEEP,
    ]);
    tally.arm(
        "RED   family part over per-part ceiling",
        1,
        "OVER CEILING docs/: part",
        default(),
    );
    // The two-tier per-part exemption (P5-BOARD.12): authored members keep the ceiling; a member registered in the
    // fact-ownership registry as a MIRROR with a regeneration governor is exempt as a checked property — everything else
    // over the ceiling fails.
    write(&t.join("docs/big.gen"), &"x".repeat(100), false);
    const R_CP50: &str = "docs/\treader_navigation\tpartitioned\towner\t0\t0\t0\t0\t50";
    write(
        &fact,
        "# fixture registry\nkind\tdocs/source.sexp\tdocs/big.gen\tBOARD-GEN\n",
        false,
    );
    reg(&[R_CP50, R_KEEP]);
    tally.arm(
        "GREEN an over-ceiling part registered as regeneration-gated is exempt, reported as proof",
        0,
        "derived: docs/big.gen",
        default(),
    );
    write(
        &fact,
        "# fixture registry\nkind\tdocs/source.sexp\tdocs/big.gen\tRECORD-SCHEMA\n",
        false,
    );
    reg(&[R_CP50, R_KEEP]);
    tally.arm(
        "RED   an over-ceiling part with a validation governor keeps the authored ceiling",
        1,
        "OVER CEILING docs/: part",
        default(),
    );
    write(
        &fact,
        "# fixture registry\nkind\tdocs/source.sexp\tdocs/other.gen\tBOARD-GEN\n",
        false,
    );
    reg(&[R_CP50, R_KEEP]);
    tally.arm(
        "RED   no exemption by adjacency — the registry row must name the member",
        1,
        "OVER CEILING docs/: part",
        default(),
    );
    let _ = fs::remove_file(&fact);
    let _ = fs::remove_file(t.join("docs/big.gen"));
    tally.arm(
        "GREEN the regen set agrees with the doctrine driver",
        0,
        "",
        regen_set_registered(&real, "scripts/check_doctrines.project.sh"),
    );
    write(&t.join("driver.sh"), "x\n", false);
    tally.arm(
        "RED   a set/driver disagreement refuses, naming the drift",
        1,
        "REGEN SET DRIFT",
        regen_set_registered(&real, &format!("{ts}/driver.sh")),
    );
    reg(&[
        "docs/\treader_navigation\tpartitioned\towner\t0\t0\t0\t0\t0",
        R_KEEP,
    ]);
    tally.arm("GREEN family within its bounds", 0, "", default());
    reg(&[R_DOCS, "KEEP.md\tinvented\thot_live\towner\t0\t0\t0\t0\t0"]);
    tally.arm(
        "RED   unknown route_class",
        1,
        "UNKNOWN route_class 'invented'",
        default(),
    );
    reg(&[R_DOCS, "KEEP.md\tboth\tinvented\towner\t0\t0\t0\t0\t0"]);
    tally.arm(
        "RED   unknown lifecycle",
        1,
        "UNKNOWN lifecycle 'invented'",
        default(),
    );
    reg(&[R_DOCS, "KEEP.md\tboth\thot_live\t\t0\t0\t0\t0\t0"]);
    tally.arm(
        "RED   no owner declared",
        1,
        "NO OWNER declared for KEEP.md",
        default(),
    );
    reg(&[R_DOCS, "KEEP.md\tboth\thot_live\towner\t0\t0\t0\t1\t0"]);
    tally.arm(
        "RED   byte ceiling exceeded",
        1,
        "OVER CEILING KEEP.md: 2 bytes > 1",
        default(),
    );
    write(&t.join("KEEP.md"), "x\nx\nx\n", false);
    reg(&[R_DOCS, "KEEP.md\tboth\thot_live\towner\t1\t0\t9\t0\t0"]);
    tally.arm(
        "GREEN health target only warns",
        0,
        "health: KEEP.md is 3 lines (target 1)",
        default(),
    );
    // Synthetic Git data exercises the real inventory subprocess without creating another repository or leaking PATH
    // into the caller (the fixture's context owns it).
    let _ = fs::create_dir_all(t.join("bin"));
    write(&t.join("bin/git"), FX_GIT, true);
    write(&t.join("docs/space name.md"), "xyz", false);
    write(&t.join("docs/café name.md"), "xy", false);
    let _ = fs::create_dir(t.join("docs/subdir"));
    #[cfg(unix)]
    let _ = std::os::unix::fs::symlink("../KEEP.md", t.join("docs/link.md"));
    let bin_path = format!("{ts}/bin:{path_env}");
    let git_fixture = |mode: &str| {
        let ctx = Ctx {
            env: vec![
                ("PATH".to_owned(), bin_path.clone()),
                ("ROUTE_FIXTURE_MODE".to_owned(), mode.to_owned()),
            ],
            ..Ctx::real(repo)
        };
        probe(&ctx, &routes, &readme, &t, "git", &fact)
    };
    const R_MEASURED: &str = "docs/\treader_navigation\tpartitioned\towner\t0\t0\t2\t5\t3";
    reg(&[R_MEASURED, R_KEEP]);
    tally.arm(
        "GREEN exact count/aggregate/part boundary and spaced member",
        0,
        "",
        git_fixture("baseline"),
    );
    tally.arm(
        "GREEN successful empty tracked family",
        0,
        "",
        git_fixture("empty"),
    );
    tally.arm(
        "RED failed empty inventory",
        2,
        "UNREADABLE family docs/: Git inventory failed",
        git_fixture("failed"),
    );
    tally.arm(
        "RED silent nonzero inventory status",
        2,
        "UNREADABLE family docs/: Git inventory failed",
        git_fixture("failed_silent"),
    );
    tally.arm(
        "RED partial listing with stderr and successful status",
        2,
        "UNREADABLE family docs/: Git inventory failed",
        git_fixture("partial_stderr"),
    );
    tally.arm(
        "RED failed nonempty inventory",
        2,
        "UNREADABLE family docs/: Git inventory failed",
        git_fixture("failed_partial"),
    );
    tally.arm(
        "RED unterminated NUL inventory",
        2,
        "incomplete NUL inventory",
        git_fixture("malformed"),
    );
    tally.arm(
        "RED duplicate inventory member",
        2,
        "duplicate family member",
        git_fixture("duplicate"),
    );
    tally.arm(
        "RED member outside family",
        2,
        "member outside family",
        git_fixture("outside"),
    );
    tally.arm(
        "RED traversal in member",
        2,
        "unsafe member path",
        git_fixture("traversal"),
    );
    tally.arm(
        "RED missing listed member",
        2,
        "UNREADABLE family docs/:",
        git_fixture("missing"),
    );
    tally.arm(
        "RED symlink member",
        2,
        "symlink member or parent",
        git_fixture("symlink"),
    );
    tally.arm(
        "RED directory listed as member",
        2,
        "non-regular family member",
        git_fixture("directory"),
    );
    tally.arm(
        "GREEN Unicode and spaced member",
        0,
        "",
        git_fixture("unicode"),
    );
    reg(&[
        "docs/\treader_navigation\tpartitioned\towner\t0\t0\t1\t5\t3",
        R_KEEP,
    ]);
    tally.arm(
        "RED one file beyond count boundary",
        1,
        "OVER CEILING docs/: 2 files > 1",
        git_fixture("baseline"),
    );
    // Remaining input paths: fixtures fail exactly one reader; no PATH changes escape their contexts. The README
    // provider runs its published CLI in a project-local fixture with a synthetic root lookup, not another Git repo.
    let _ = fs::remove_file(t.join("docs/link.md"));
    let _ = fs::remove_dir(t.join("docs/subdir"));
    let read_wc = real.which("wc").display().to_string();
    let read_python = real.which("python3").display().to_string();
    let read_sort = real.which("sort").display().to_string();
    let read_grep = real.which("grep").display().to_string();
    write(&t.join("bin/wc"), FX_WC, true);
    write(&t.join("bin/python3"), FX_PYTHON, true);
    write(&t.join("hint-provider"), FX_HINT, true);
    write(&t.join("bin/sort"), FX_SORT, true);
    write(&t.join("bin/grep"), FX_GREP, true);
    let input_fixture = |mode: &str, page: Option<&Path>| {
        let ctx = Ctx {
            env: vec![
                ("PATH".to_owned(), bin_path.clone()),
                ("ROUTE_READ_MODE".to_owned(), mode.to_owned()),
                ("ROUTE_READ_FIXTURE".to_owned(), ts.clone()),
                ("ROUTE_READ_WC".to_owned(), read_wc.clone()),
                ("ROUTE_READ_PYTHON".to_owned(), read_python.clone()),
                ("ROUTE_READ_GREP".to_owned(), read_grep.clone()),
            ],
            ..Ctx::real(repo)
        };
        probe(&ctx, &routes, page.unwrap_or(&readme), &t, "find", &fact)
    };
    let hint_fixture = |mode: &str| {
        let ctx = Ctx {
            env: vec![
                ("ROUTE_READ_MODE".to_owned(), mode.to_owned()),
                ("PATH".to_owned(), bin_path.clone()),
                ("ROUTE_READ_SORT".to_owned(), read_sort.clone()),
                ("ROUTE_READ_PYTHON".to_owned(), read_python.clone()),
                ("ROUTE_READ_WC".to_owned(), read_wc.clone()),
                ("ROUTE_READ_GREP".to_owned(), read_grep.clone()),
            ],
            ..Ctx::real(repo)
        };
        emitted_hint_targets(&ctx, &format!("{ts}/hint-provider"))
    };
    reg(&[R_DOCS, R_KEEP]);
    tally.arm(
        "GREEN all fixture input readers work",
        0,
        "",
        input_fixture("baseline", None),
    );
    tally.arm(
        "RED text byte measurement failed status",
        2,
        "UNREADABLE text measurement",
        input_fixture("file_status", None),
    );
    tally.arm(
        "RED text byte measurement silent failed status",
        2,
        "UNREADABLE text measurement",
        input_fixture("file_silent", None),
    );
    tally.arm(
        "RED failed measurement despite plausible numeric output",
        2,
        "UNREADABLE text measurement",
        input_fixture("file_failed_value", None),
    );
    tally.arm(
        "RED text byte measurement diagnostic",
        2,
        "UNREADABLE text measurement",
        input_fixture("file_stderr", None),
    );
    tally.arm(
        "RED text measurement invalid integer",
        2,
        "UNREADABLE text measurement",
        input_fixture("file_bad", None),
    );
    tally.arm(
        "RED text measurement extra integer",
        2,
        "UNREADABLE text measurement",
        input_fixture("file_extra", None),
    );
    tally.arm(
        "RED text line measurement silent failed status",
        2,
        "UNREADABLE text measurement",
        input_fixture("file_line_status", None),
    );
    tally.arm(
        "RED linked destination parser failed status",
        2,
        "UNREADABLE landing-page links",
        input_fixture("parser_status", None),
    );
    tally.arm(
        "RED linked destination parser silent failed status",
        2,
        "UNREADABLE landing-page links",
        input_fixture("parser_silent", None),
    );
    tally.arm(
        "RED linked destination parser partial diagnostic",
        2,
        "UNREADABLE landing-page links",
        input_fixture("parser_stderr", None),
    );
    let empty_readme = t.join("empty-readme.md");
    write(&empty_readme, "# Empty landing page\n", false);
    tally.arm(
        "GREEN successful link parse can have no links",
        0,
        "",
        input_fixture("baseline", Some(&empty_readme)),
    );
    tally.arm(
        "GREEN forced-red provider emits destinations",
        0,
        "README_POLICY.md",
        hint_fixture("baseline"),
    );
    tally.arm(
        "RED hint provider failed despite plausible guidance",
        2,
        "UNREADABLE emitted-hint producer",
        hint_fixture("hint_status"),
    );
    tally.arm(
        "RED hint provider unexpectedly successful despite guidance",
        2,
        "UNREADABLE emitted-hint producer",
        hint_fixture("hint_success"),
    );
    tally.arm(
        "RED hint provider returned no guidance",
        2,
        "UNREADABLE emitted-hint producer",
        hint_fixture("hint_empty"),
    );
    tally.arm(
        "RED hint provider returned paths without its guidance contract",
        2,
        "UNREADABLE emitted-hint producer",
        hint_fixture("hint_no_contract"),
    );
    tally.arm(
        "RED hint extraction returned no destinations",
        2,
        "UNREADABLE emitted-hint destinations",
        hint_fixture("hint_no_destinations"),
    );
    tally.arm(
        "RED extraction failed despite nonempty destinations",
        2,
        "UNREADABLE emitted-hint destinations",
        hint_fixture("hint_sort_status"),
    );
    tally.arm(
        "RED extraction emitted diagnostics with nonempty destinations",
        2,
        "UNREADABLE emitted-hint destinations",
        hint_fixture("hint_sort_stderr"),
    );

    let project = t.join("readme-project");
    let _ = fs::create_dir_all(project.join("scripts"));
    let _ = fs::create_dir_all(t.join("readme-bin"));
    let _ = fs::copy(
        repo.join("scripts/check_readme_stability.sh"),
        project.join("scripts/check_readme_stability.sh"),
    );
    let _ = fs::copy(
        repo.join("scripts/read_text_metrics.bash"),
        project.join("scripts/read_text_metrics.bash"),
    );
    write(&project.join("README.md"), "See README_POLICY.md\n", false);
    write(&project.join("README_POLICY.md"), "fixture policy\n", false);
    write(&t.join("readme-bin/git"), FX_README_GIT, true);
    let project_s = project.display().to_string();
    let readme_fixture = |mode: &str| {
        let ctx = Ctx {
            cwd: project.clone(),
            env: vec![
                (
                    "PATH".to_owned(),
                    format!("{ts}/readme-bin:{ts}/bin:{path_env}"),
                ),
                ("ROUTE_READ_MODE".to_owned(), mode.to_owned()),
                ("ROUTE_READ_WC".to_owned(), read_wc.clone()),
                ("ROUTE_READ_PYTHON".to_owned(), read_python.clone()),
                ("ROUTE_READ_GREP".to_owned(), read_grep.clone()),
                ("ROUTE_READ_FIXTURE".to_owned(), ts.clone()),
                ("ROUTE_READ_PROJECT".to_owned(), project_s.clone()),
            ],
            ..Ctx::real(repo)
        };
        let page = match mode {
            "policy_lookalike" => "See README_POLICYxmd\n",
            "policy_absent" => "See another policy\n",
            "dated_page" => "See README_POLICY.md on 2026-01-01\n",
            _ => "See README_POLICY.md\n",
        };
        write(&project.join("README.md"), page, false);
        ctx.merged(&[], &["bash", "scripts/check_readme_stability.sh"])
    };
    tally.arm(
        "GREEN standalone README CLI measures its page",
        0,
        "README-STABILITY: OK",
        readme_fixture("baseline"),
    );
    tally.arm(
        "RED standalone README CLI refuses byte failure",
        2,
        "README-STABILITY: REFUSED",
        readme_fixture("file_silent"),
    );
    tally.arm(
        "RED standalone README CLI refuses line failure",
        2,
        "README-STABILITY: REFUSED",
        readme_fixture("file_line_status"),
    );
    tally.arm(
        "RED standalone README CLI refuses measurement stderr",
        2,
        "README-STABILITY: REFUSED",
        readme_fixture("file_stderr"),
    );
    tally.arm(
        "RED standalone date count failed with plausible zero",
        2,
        "dated-annotation count unavailable",
        readme_fixture("date_status"),
    );
    tally.arm(
        "RED standalone date count reported diagnostics",
        2,
        "dated-annotation count unavailable",
        readme_fixture("date_stderr"),
    );
    tally.arm(
        "RED standalone date count returned no integer",
        2,
        "dated-annotation count unavailable",
        readme_fixture("date_empty"),
    );
    tally.arm(
        "RED standalone policy count failed with plausible integer",
        2,
        "policy-name count unavailable",
        readme_fixture("policy_status"),
    );
    tally.arm(
        "RED standalone policy count reported diagnostics",
        2,
        "policy-name count unavailable",
        readme_fixture("policy_stderr"),
    );
    tally.arm(
        "RED standalone policy count returned no integer",
        2,
        "policy-name count unavailable",
        readme_fixture("policy_empty"),
    );
    tally.arm(
        "RED policy lookalike is not its literal name",
        1,
        "no longer links README_POLICY.md",
        readme_fixture("policy_lookalike"),
    );
    tally.arm(
        "RED legitimate policy no-match remains a breach",
        1,
        "no longer links README_POLICY.md",
        readme_fixture("policy_absent"),
    );
    tally.arm(
        "RED legitimate dated annotation remains a breach",
        1,
        "date-stamped line(s)",
        readme_fixture("dated_page"),
    );

    let table_fixture = |mode: &'static str| {
        let ctx = Ctx {
            seams: Seams {
                family_measure: Some(mode),
                ..Seams::default()
            },
            ..Ctx::real(repo)
        };
        probe(&ctx, &routes, &readme, &t, "find", &fact)
    };
    tally.arm(
        "RED producer table missing its totals",
        2,
        "UNREADABLE family totals",
        table_fixture("empty"),
    );
    tally.arm(
        "RED producer table has invalid count",
        2,
        "UNREADABLE family totals",
        table_fixture("bad_count"),
    );
    tally.arm(
        "RED producer table has surplus totals field",
        2,
        "UNREADABLE family totals",
        table_fixture("extra"),
    );
    let registry_fixture = |mode: &'static str| {
        let case = t.join("registry-case.tsv");
        let page = t.join("registry-readme.md");
        write(&page, "See [keep](KEEP.md).\n", false);
        let mut row = "KEEP.md\treader_navigation\thot_live\tfixture\t0\t0\t5\t64\t0".to_owned();
        match mode {
            "invalid_line" => row = "KEEP.md\treader_navigation\thot_live\tfixture\t0\t0\tinvalid\t64\t0".to_owned(),
            "invalid_byte" => row = "KEEP.md\treader_navigation\thot_live\tfixture\t0\t0\t5\tinvalid\t0".to_owned(),
            "negative_health" => row = "KEEP.md\treader_navigation\thot_live\tfixture\t-1\t0\t5\t64\t0".to_owned(),
            "negative_ceiling" => row = "KEEP.md\treader_navigation\thot_live\tfixture\t0\t0\t-1\t64\t0".to_owned(),
            "overflow" => row = "KEEP.md\treader_navigation\thot_live\tfixture\t0\t0\t5\t99999999999999999999999999999999999\t0".to_owned(),
            "max_plus_one" => row = "KEEP.md\treader_navigation\thot_live\tfixture\t0\t0\t5\t9223372036854775808\t0".to_owned(),
            "max" => row = "KEEP.md\treader_navigation\thot_live\tfixture\t0\t0\t9223372036854775807\t9223372036854775807\t0".to_owned(),
            "zeros" => row = "KEEP.md\treader_navigation\thot_live\tfixture\t000\t000\t0000000000000000000000000000000000005\t00000000000000000000000000000000000064\t000".to_owned(),
            "extra" => row.push_str("\textra"),
            "missing" => {
                let cut = row.rfind('\t').unwrap_or(row.len());
                row.truncate(cut);
            }
            "unsafe" => row = "../KEEP.md\treader_navigation\thot_live\tfixture\t0\t0\t5\t64\t0".to_owned(),
            _ => {}
        }
        let mut bytes = format!("{row}\n").into_bytes();
        let mut seams = Seams::default();
        match mode {
            "duplicate" => bytes.extend_from_slice(format!("{row}\n").as_bytes()),
            "no_lf" => bytes = row.clone().into_bytes(),
            "crlf" => bytes = format!("{row}\r\n").into_bytes(),
            "nul" => bytes.push(0),
            "control" => bytes.push(0x1f),
            "invalid_utf8" => {
                bytes =
                    b"KEEP.md\treader_navigation\thot_live\tfi\xffxture\t0\t0\t5\t64\t0\n".to_vec();
            }
            "status" | "diagnostic" | "silent" => seams.registry_text = Some(mode),
            "no_partial" => bytes.extend_from_slice(
                b"extra.md\treader_navigation\thot_live\tfixture\t0\t0\tbad\t64\t0\n",
            ),
            _ => {}
        }
        let _ = fs::write(&case, &bytes);
        let ctx = Ctx {
            seams,
            ..Ctx::real(repo)
        };
        if mode == "no_partial" {
            let mut ignored = Sink::default();
            return match read_registry_rows(&ctx, &case.display().to_string(), &mut ignored) {
                None => (0, "invalid suffix publishes no rows\n".to_owned()),
                Some(_) => (1, String::new()),
            };
        }
        probe(&ctx, &case, &page, &t, "find", &fact)
    };
    tally.arm(
        "GREEN registry baseline retains existing semantics",
        0,
        "",
        registry_fixture("baseline"),
    );
    tally.arm(
        "RED registry producer failed despite healthy rows",
        2,
        "UNREADABLE registry read",
        registry_fixture("status"),
    );
    tally.arm(
        "RED registry producer diagnostic despite healthy rows",
        2,
        "UNREADABLE registry read",
        registry_fixture("diagnostic"),
    );
    tally.arm(
        "RED registry producer silent failure",
        2,
        "UNREADABLE registry read",
        registry_fixture("silent"),
    );
    tally.arm(
        "RED registry line limit is not an integer",
        2,
        "UNREADABLE registry limits",
        registry_fixture("invalid_line"),
    );
    tally.arm(
        "RED registry byte limit is not an integer",
        2,
        "UNREADABLE registry limits",
        registry_fixture("invalid_byte"),
    );
    tally.arm(
        "RED registry health limit is negative",
        2,
        "UNREADABLE registry limits",
        registry_fixture("negative_health"),
    );
    tally.arm(
        "RED registry ceiling is negative",
        2,
        "UNREADABLE registry limits",
        registry_fixture("negative_ceiling"),
    );
    tally.arm(
        "RED registry integer overflows Bash comparisons",
        2,
        "signed-64-bit range",
        registry_fixture("overflow"),
    );
    tally.arm(
        "RED registry integer one above maximum",
        2,
        "signed-64-bit range",
        registry_fixture("max_plus_one"),
    );
    tally.arm(
        "GREEN registry exact signed-64-bit maximum",
        0,
        "",
        registry_fixture("max"),
    );
    tally.arm(
        "GREEN registry decimal leading zeros normalize",
        0,
        "",
        registry_fixture("zeros"),
    );
    tally.arm(
        "RED registry surplus field",
        2,
        "nine tab-separated fields",
        registry_fixture("extra"),
    );
    tally.arm(
        "RED registry missing field",
        2,
        "nine tab-separated fields",
        registry_fixture("missing"),
    );
    tally.arm(
        "RED registry duplicate destination",
        2,
        "duplicate destination",
        registry_fixture("duplicate"),
    );
    tally.arm(
        "RED registry unsafe relative destination",
        2,
        "normalized relative path",
        registry_fixture("unsafe"),
    );
    tally.arm(
        "GREEN registry last row needs no LF",
        0,
        "",
        registry_fixture("no_lf"),
    );
    tally.arm(
        "GREEN registry CRLF normalizes",
        0,
        "",
        registry_fixture("crlf"),
    );
    tally.arm(
        "RED registry NUL cannot disappear in substitution",
        2,
        "UNREADABLE registry read",
        registry_fixture("nul"),
    );
    tally.arm(
        "RED registry separator control character",
        2,
        "UNREADABLE registry read",
        registry_fixture("control"),
    );
    tally.arm(
        "RED registry invalid UTF-8",
        2,
        "UNREADABLE registry read",
        registry_fixture("invalid_utf8"),
    );
    tally.arm(
        "GREEN invalid registry suffix publishes no prefix",
        0,
        "publishes no rows",
        registry_fixture("no_partial"),
    );
    let registry_main_fixture = |mode: &'static str| {
        let ctx = Ctx {
            cwd: project.clone(),
            root: project.clone(),
            env: vec![
                ("PATH".to_owned(), format!("{ts}/readme-bin:{path_env}")),
                ("ROUTE_READ_PROJECT".to_owned(), project_s.clone()),
            ],
            seams: Seams {
                main_stubs: true,
                registry_text: matches!(mode, "status" | "diagnostic").then_some(mode),
                ..Seams::default()
            },
        };
        let _ = fs::create_dir_all(project.join("target/tmp"));
        write(&project.join("README.md"), "See README_POLICY.md\n", false);
        write(&project.join("README_POLICY.md"), "fixture policy\n", false);
        let mut rows = "README.md\treader_navigation\thot_live\tfixture\t0\t0\t100\t65536\t0\nREADME_POLICY.md\treader_navigation\tnormative\tfixture\t0\t0\t0\t0\t0\n".to_owned();
        if mode == "malformed" {
            rows.push_str("extra.md\treader_navigation\tnormative\tfixture\t0\t0\tbad\t0\t0\n");
        }
        write(&project.join("routes.tsv"), &rows, false);
        let mut sink = Sink::default();
        let rc = main_routes(&ctx, "routes.tsv", &mut sink);
        (rc, sink.merged())
    };
    tally.arm(
        "GREEN entry flow derives exact destination count and README caps",
        0,
        "ok (2 governed destination(s))",
        registry_main_fixture("baseline"),
    );
    tally.arm(
        "RED entry flow propagates failed registry producer",
        2,
        "REFUSED — registry inputs unavailable",
        registry_main_fixture("status"),
    );
    tally.arm(
        "RED entry flow propagates registry diagnostics",
        2,
        "REFUSED — registry inputs unavailable",
        registry_main_fixture("diagnostic"),
    );
    tally.arm(
        "RED entry flow rejects malformed registry suffix",
        2,
        "REFUSED — registry inputs unavailable",
        registry_main_fixture("malformed"),
    );
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "README-ROUTING-CLOSURE --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}

/// `cargo xtask check-readme-routes [--self-test]`: the shell driver's verdict lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    let _ = fs::create_dir_all(root.join("target/tmp"));
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    if !self_test(root, false) {
        eprintln!(
            "README-ROUTING-CLOSURE: REFUSED — the check does not discriminate (self-test failed)."
        );
        return ExitCode::from(2);
    }
    let mut sink = Sink::default();
    let rc = main_routes(&Ctx::real(root), REGISTRY, &mut sink);
    sink.replay();
    ExitCode::from(u8::try_from(rc).unwrap_or(2))
}
