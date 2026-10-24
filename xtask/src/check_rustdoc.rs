//! The `API-DOCS` doctrine, ported from `scripts/check_rustdoc.sh` (`XTASK.6` slice `6d`), which is now a
//! shim of `cargo xtask check-rustdoc`.
//!
//! The director's direction (`decision_rust-native-tooling`, 2026-10-23): SEMULITH's API reference is
//! produced by rustdoc from the code (tree `RUSTDOC`). A reference whose intra-doc links point nowhere,
//! point at private items a reader cannot open, or whose prose swallows text into an unclosed HTML tag is a
//! reference that lies quietly. The check builds the workspace's docs offline with exactly three rustdoc lints
//! denied — `broken_intra_doc_links`, `private_intra_doc_links`, `invalid_html_tags` — and refuses any
//! occurrence, naming file, line and lint.
//!
//! Missing documentation is a ratchet, not a denial (`RUSTDOC.3`): the same build warns on `missing_docs`,
//! the check counts the undocumented public items per crate directory and compares each count with
//! `doctrine/undocumented_items.tsv`; a rise is refused with the crate's items listed, a fall until the row is
//! lowered. Each self-test arm is one `tally.arm(` call, the idiom the `DERIVED-COUNTS` arm total counts.

use std::collections::{BTreeSet, HashMap};
use std::fs;
use std::path::Path;
use std::process::{Command, ExitCode};

use crate::harness::{combined, locale_sorted, scratch};

/// The three denied rustdoc lints.
const LINTS: &str =
    "-D rustdoc::broken_intra_doc_links -D rustdoc::private_intra_doc_links -D rustdoc::invalid_html_tags";
/// The per-crate record of undocumented public items.
const RECORD: &str = "doctrine/undocumented_items.tsv";

/// Runs the doctrine: `--self-test` as the first argument runs the arms; anything else runs the check.
/// Exit 0 ok, 1 a link or HTML defect or a ratchet breach, 2 refused.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    // Re-run the controls before judging: a check that no longer discriminates must refuse, not pass.
    if !self_test(root, false) {
        eprintln!("API-DOCS: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    let (rc, out) = combined(
        Command::new("cargo")
            .args(["doc", "--workspace", "--no-deps", "--offline"])
            .env("RUSTDOCFLAGS", format!("{LINTS} -W missing_docs"))
            .current_dir(root),
    );
    if rc != 0 {
        eprintln!(
            "API-DOCS: FAIL — the workspace's rustdoc carries link or HTML defects (decision_rust-native-tooling):"
        );
        for line in defects(&out) {
            eprintln!("{line}");
        }
        eprintln!("  Fix the doc comment (or its generator) — never allow the lint.");
        return ExitCode::from(1);
    }
    // Count crates from the workspace's crate directories: a fresh build prints no "Documenting" line,
    // while cargo replays the cached warnings, so the ratchet's count is the same either way.
    let mut dirs = crate_dirs(root);
    if root.join("xtask/Cargo.toml").is_file() {
        dirs.push("xtask".to_owned()); // the automation front door is a workspace member too (XTASK.1)
    }
    let names: Vec<&str> = dirs.iter().map(String::as_str).collect();
    let (vrc, verdict) = ratchet(&root.join(RECORD), RECORD, &names, &out);
    match vrc {
        2 => {
            eprintln!("API-DOCS: REFUSED — {RECORD} cannot be judged: {verdict}");
            ExitCode::from(2)
        }
        0 => {
            println!(
                "API-DOCS: ok ({} crate(s) documented; no broken or private intra-doc link, no invalid HTML; {verdict} undocumented public item(s), each crate at its recorded count)",
                dirs.len()
            );
            ExitCode::SUCCESS
        }
        _ => {
            eprintln!(
                "API-DOCS: FAIL — the undocumented public items no longer match {RECORD} (the RUSTDOC.3 ratchet):"
            );
            for line in verdict.split('\n') {
                eprintln!("  {line}");
            }
            ExitCode::from(1)
        }
    }
}

/// The crate directories under `crates/` that hold a `Cargo.toml`, in the order the script's
/// `crates/*/` glob listed them (the locale's collation).
fn crate_dirs(root: &Path) -> Vec<String> {
    let Ok(entries) = fs::read_dir(root.join("crates")) else {
        return Vec::new();
    };
    let names = entries
        .filter_map(Result::ok)
        .filter(|entry| entry.path().join("Cargo.toml").is_file())
        .filter_map(|entry| entry.file_name().into_string().ok())
        .filter(|name| !name.starts_with('.'))
        .collect();
    locale_sorted(names)
}

/// One line per denied diagnostic (an `error:` other than "could not document"): its location, then its
/// message, at most 60 (the script's awk and `head -60`). Warnings are excluded: listing the
/// missing-docs warnings buried the one error that failed the build (`XTASK.3`'s gate refusal).
fn defects(out: &str) -> Vec<String> {
    let mut lines = Vec::new();
    let mut message: Option<String> = None;
    for line in out.split('\n') {
        if let Some(rest) = line.strip_prefix("error: ") {
            if !line.contains("could not document") {
                message = Some(rest.to_owned());
                continue;
            }
        }
        if let Some(text) = &message {
            let trimmed = line.trim_start_matches(' ');
            if let Some(location) = trimmed.strip_prefix("--> ") {
                lines.push(format!("  {location}  {text}"));
                message = None;
            }
        }
    }
    lines.truncate(60);
    lines
}

/// Python's `repr` of a string, as the script's ratchet printed a malformed row.
fn py_repr(text: &str) -> String {
    let quote = if text.contains('\'') && !text.contains('"') {
        '"'
    } else {
        '\''
    };
    let mut out = String::from(quote);
    for c in text.chars() {
        match c {
            '\\' => out.push_str("\\\\"),
            '\n' => out.push_str("\\n"),
            '\r' => out.push_str("\\r"),
            '\t' => out.push_str("\\t"),
            c if c == quote => {
                out.push('\\');
                out.push(c);
            }
            c if (c as u32) < 0x20 || c as u32 == 0x7f => {
                out.push_str(&format!("\\x{:02x}", c as u32))
            }
            c => out.push(c),
        }
    }
    out.push(quote);
    out
}

/// Python's `str` of an `OSError` for a path, as the script's ratchet printed an unreadable record.
fn py_os_error(error: &std::io::Error, path: &str) -> String {
    let code = error.raw_os_error().unwrap_or(0);
    let text = error.to_string();
    let reason = text.split(" (os error").next().unwrap_or(&text).to_owned();
    format!("[Errno {code}] {reason}: {}", py_repr(path))
}

/// The ratchet: the undocumented public items per crate in `log` against the record at `record` (`shown`
/// in messages). Returns the script's exit code and its text: the total (0), the problems (1), or why the
/// record cannot be judged (2).
fn ratchet(record: &Path, shown: &str, crates: &[&str], log: &str) -> (i32, String) {
    let log: Vec<&str> = log.split('\n').collect();
    let mut counts: HashMap<&str, u64> = crates.iter().map(|c| (*c, 0)).collect();
    let mut where_: HashMap<&str, Vec<String>> = crates.iter().map(|c| (*c, Vec::new())).collect();
    let mut stray: Vec<String> = Vec::new();
    for (i, line) in log.iter().enumerate() {
        if !line.starts_with("warning: missing documentation for") {
            continue;
        }
        let location = log[i + 1..log.len().min(i + 4)]
            .iter()
            .map(|x| x.trim())
            .find(|x| x.starts_with("-->"))
            .map(|x| x.chars().skip(4).collect::<String>())
            .unwrap_or_default();
        let krate = location
            .strip_prefix("crates/")
            .and_then(|rest| rest.split_once('/').map(|(name, _)| name))
            .filter(|name| !name.is_empty())
            .or_else(|| location.strip_prefix("xtask/").map(|_| "xtask"));
        match krate.and_then(|name| crates.iter().find(|c| **c == name)) {
            Some(name) => {
                *counts.get_mut(name).expect("counted") += 1;
                let warning = line.strip_prefix("warning: ").unwrap_or(line);
                where_
                    .get_mut(name)
                    .expect("listed")
                    .push(format!("{location}  {warning}"));
            }
            None => stray.push(if location.is_empty() {
                "?".to_owned()
            } else {
                location
            }),
        }
    }
    let text = match fs::read_to_string(record) {
        Ok(text) => text,
        Err(error) => {
            return (
                2,
                format!("unreadable record: {}", py_os_error(&error, shown)),
            )
        }
    };
    let mut rows: HashMap<String, u64> = HashMap::new();
    for line in text.split('\n') {
        if line.trim().is_empty() || line.starts_with('#') {
            continue;
        }
        let parts: Vec<&str> = line.split('\t').collect();
        let digits = parts.len() == 2
            && !parts[1].is_empty()
            && parts[1].chars().all(|c| c.is_ascii_digit());
        if !digits || rows.contains_key(parts[0]) {
            return (2, format!("malformed record row: {}", py_repr(line)));
        }
        rows.insert(parts[0].to_owned(), parts[1].parse().unwrap_or(u64::MAX));
    }
    let mut problems: Vec<String> = Vec::new();
    if !stray.is_empty() {
        let shown: Vec<String> = stray.iter().take(3).map(|s| py_repr(s)).collect();
        problems.push(format!(
            "{} undocumented item(s) outside a workspace crate directory: [{}]",
            stray.len(),
            shown.join(", ")
        ));
    }
    let listed: BTreeSet<&str> = crates.iter().copied().collect();
    let mut extra: Vec<&String> = rows
        .keys()
        .filter(|row| !listed.contains(row.as_str()))
        .collect();
    extra.sort();
    for krate in extra {
        problems.push(format!(
            "{krate}: recorded, but not a workspace crate directory"
        ));
    }
    for krate in crates {
        let count = counts[krate];
        match rows.get(*krate) {
            None => problems.push(format!("{krate}: no recorded count (measured {count})")),
            Some(&row) if count > row => {
                let items: String = where_[krate].iter().take(20).map(|w| format!("\n    {w}")).collect();
                problems.push(format!(
                    "{krate}: {count} undocumented > recorded {row}; document the new item(s):{items}"
                ));
            }
            Some(&row) if count < row => problems.push(format!(
                "{krate}: {count} undocumented < recorded {row}; lower the record to {count} (the ratchet only tightens)"
            )),
            Some(_) => {}
        }
    }
    if problems.is_empty() {
        (0, counts.values().sum::<u64>().to_string())
    } else {
        (1, problems.join("\n"))
    }
}

/// bash's `printf %q` for the plain strings the arms use: a backslash before each character a shell
/// would read specially.
fn shell_quote(text: &str) -> String {
    text.chars()
        .flat_map(|c| {
            let plain = c.is_ascii_alphanumeric() || "-_./:=,+@%^".contains(c);
            (!plain)
                .then_some('\\')
                .into_iter()
                .chain(std::iter::once(c))
        })
        .collect()
}

/// The self-test's pass and fail counts; `verbose` prints misses on stderr and the summary on stdout.
struct Tally {
    pass: u32,
    fail: u32,
    verbose: bool,
}

impl Tally {
    /// One arm: `rc` must equal `expected`, and `want` must occur in `out` (`-` asserts no reason; a
    /// leading `!` asserts the rest is absent).
    fn arm(&mut self, name: &str, result: &(i32, String), expected: i32, want: &str) {
        let (rc, out) = (result.0, result.1.as_str());
        let held = match want.strip_prefix('!') {
            Some(absent) => rc == expected && !out.contains(absent),
            None => rc == expected && (want == "-" || out.contains(want)),
        };
        if held {
            self.pass += 1;
            return;
        }
        self.fail += 1;
        if self.verbose {
            match want.strip_prefix('!') {
                Some(absent) => eprintln!(
                    "API-DOCS self-test MISS: {name} — expected rc={expected} WITHOUT {}, got rc={rc}\n{out}",
                    shell_quote(absent)
                ),
                None => eprintln!(
                    "API-DOCS self-test MISS: {name} — expected rc={expected} (reason: {want}), got rc={rc}\n{out}"
                ),
            }
        }
    }
}

/// Writes a one-file crate with its own `[workspace]`.
fn make_crate(dir: &Path, name: &str, source: &str) -> std::io::Result<()> {
    fs::create_dir_all(dir.join("src"))?;
    fs::write(
        dir.join("Cargo.toml"),
        format!("[package]\nname = \"{name}\"\nversion = \"0.1.0\"\nedition = \"2021\"\n\n[workspace]\n"),
    )?;
    fs::write(dir.join("src/lib.rs"), format!("{source}\n"))
}

/// Documents a scratch crate inside the scratch directory with `flags` as `RUSTDOCFLAGS`, applied after
/// `inherited` (an environment the caller passes in): an inherited value must never decide a verdict.
fn doc_crate(dir: &Path, flags: &str, inherited: &[(&str, &str)]) -> (i32, String) {
    let mut command = Command::new("cargo");
    command
        .args(["doc", "--offline", "--no-deps", "--target-dir"])
        .arg(dir.join(".wt"))
        .current_dir(dir);
    for (key, value) in inherited {
        command.env(key, value);
    }
    command.env("RUSTDOCFLAGS", flags);
    combined(&mut command)
}

/// The fifteen arms. Returns whether every arm held.
fn self_test(root: &Path, verbose: bool) -> bool {
    let mut tally = Tally {
        pass: 0,
        fail: 0,
        verbose,
    };
    let t = match scratch(root, "target/doctrine-selftest", "api-docs") {
        Ok(dir) => dir,
        Err(error) => {
            if verbose {
                eprintln!("API-DOCS self-test: cannot create a scratch directory: {error}");
            }
            return false;
        }
    };
    let built = |dir: &str, name: &str, source: &str, flags: &str, inherited: &[(&str, &str)]| {
        let path = t.join(dir);
        match make_crate(&path, name, source) {
            Ok(()) => doc_crate(&path, flags, inherited),
            Err(error) => (-1, format!("cannot write the scratch crate: {error}")),
        }
    };
    let good = "//! A documented crate.\n/// Returns [`ANSWER`].\npub fn probe() -> u32 { ANSWER }\n/// The answer.\npub const ANSWER: u32 = 42;";
    tally.arm(
        "GREEN a crate whose links resolve and whose prose is sound",
        &built("good", "probe-good", good, LINTS, &[]),
        0,
        "-",
    );
    tally.arm(
        "RED an intra-doc link to nothing is refused, naming the lint",
        &built(
            "broken",
            "probe-broken",
            "/// See [`nowhere`].\npub fn probe() -> u32 { 42 }",
            LINTS,
            &[],
        ),
        101,
        "rustdoc::broken-intra-doc-links",
    );
    tally.arm(
        "RED a public doc linking a private item is refused, naming the lint",
        &built("private", "probe-private", "/// Delegates to [`helper`].\npub fn probe() -> u32 { helper() }\nfn helper() -> u32 { 42 }", LINTS, &[]),
        101,
        "rustdoc::private-intra-doc-links",
    );
    tally.arm(
        "RED an unclosed HTML tag in prose is refused, naming the lint",
        &built(
            "html",
            "probe-html",
            "/// Takes a Vec<u8> of bytes.\npub fn probe() -> u32 { 42 }",
            LINTS,
            &[],
        ),
        101,
        "rustdoc::invalid-html-tags",
    );
    tally.arm(
        "GREEN missing docs alone are not this check's business (RUSTDOC.3 owns them)",
        &built(
            "undocumented",
            "probe-undocumented",
            "pub fn probe() -> u32 { 42 }",
            LINTS,
            &[],
        ),
        0,
        "-",
    );
    tally.arm(
        "REFUSE a failure with an unrelated cause is not read as a link defect",
        &built("syntax", "probe-syntax", "pub fn broken( {", LINTS, &[]),
        101,
        "!rustdoc::",
    );
    tally.arm(
        "GREEN an inherited RUSTDOCFLAGS does not leak into the verdict",
        &doc_crate(
            &t.join("undocumented"),
            LINTS,
            &[("RUSTDOCFLAGS", "-D missing_docs")],
        ),
        0,
        "-",
    );
    // The failure listing names the denied defect even among many missing-docs warnings.
    let mut noisy = String::from("//! Noisy.\n");
    for i in 1..=80 {
        noisy.push_str(&format!("pub fn f{i}() {{}}\n"));
    }
    noisy.push_str("/// See [`nowhere`].\npub fn last() {}");
    let (rc, out) = built(
        "noisy",
        "probe-noisy",
        &noisy,
        &format!("{LINTS} -W missing_docs"),
        &[],
    );
    let listed = (rc, defects(&out).join("\n"));
    tally.arm(
        "RED the build fails and the listing names the denied link, not the 80 warnings",
        &listed,
        101,
        "unresolved link to `nowhere`",
    );
    tally.arm(
        "RED the failure listing carries no warning line",
        &listed,
        101,
        "!missing documentation",
    );
    // The ratchet, on a two-crate workspace laid out as crates/<dir>/: one crate with two undocumented
    // public items (a function and a struct field), one fully documented.
    let ws = t.join("ws");
    let files = [
        ("Cargo.toml", "[workspace]\nresolver = \"2\"\nmembers = [\"crates/probe\", \"crates/clean\"]\n"),
        ("crates/probe/Cargo.toml", "[package]\nname = \"probe\"\nversion = \"0.1.0\"\nedition = \"2021\"\n"),
        ("crates/clean/Cargo.toml", "[package]\nname = \"clean\"\nversion = \"0.1.0\"\nedition = \"2021\"\n"),
        ("crates/probe/src/lib.rs", "//! A probe.\npub fn bare() {}\n/// Documented.\npub struct S {\n    pub field: u8,\n}\n"),
        ("crates/clean/src/lib.rs", "//! Clean.\n/// One.\npub fn one() {}\n"),
    ];
    let written = files.iter().try_for_each(|(rel, text)| {
        let path = ws.join(rel);
        fs::create_dir_all(path.parent().expect("a parent")).and_then(|()| fs::write(path, text))
    });
    let doc = match written {
        Ok(()) => {
            combined(
                Command::new("cargo")
                    .args([
                        "doc",
                        "--workspace",
                        "--offline",
                        "--no-deps",
                        "--target-dir",
                    ])
                    .arg(ws.join(".wt"))
                    .env("RUSTDOCFLAGS", format!("{LINTS} -W missing_docs"))
                    .current_dir(&ws),
            )
            .1
        }
        Err(error) => format!("cannot write the scratch workspace: {error}"),
    };
    let record = t.join("rec.tsv");
    let shown = record.display().to_string();
    let judged = |text: &str| {
        let _ = fs::write(&record, text);
        ratchet(&record, &shown, &["probe", "clean"], &doc)
    };
    tally.arm(
        "GREEN the ratchet holds when every crate's count equals its row",
        &judged("probe\t2\nclean\t0\n"),
        0,
        "2",
    );
    tally.arm(
        "RED a rise is refused, listing the crate's undocumented items",
        &judged("probe\t1\nclean\t0\n"),
        1,
        "document the new item(s)",
    );
    tally.arm(
        "RED a fall is refused until the row is lowered",
        &judged("probe\t3\nclean\t0\n"),
        1,
        "lower the record to 2",
    );
    tally.arm(
        "RED a crate without a row is refused",
        &judged("probe\t2\n"),
        1,
        "clean: no recorded count",
    );
    tally.arm(
        "RED a row naming no workspace crate is refused",
        &judged("probe\t2\nclean\t0\nghost\t0\n"),
        1,
        "ghost: recorded, but not a workspace crate directory",
    );
    tally.arm(
        "REFUSE a malformed record cannot be judged",
        &judged("probe 2\n"),
        2,
        "malformed record row",
    );
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "API-DOCS --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}
