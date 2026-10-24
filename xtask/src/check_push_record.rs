//! The `PUSH-RECORD` doctrine (`PUSH-DISCIPLINE.3`), ported from `scripts/check_push_record.sh` (`XTASK.6`
//! slice `6e`), which is now a shim of `cargo xtask check-push-record`.
//!
//! The approval ledger (`docs/push-approvals.md`) is the tracked, append-only record of exceptional pushes:
//! who approved, when, why, and what range of commits the push carried. Append-only is enforced, not hoped:
//! a staged change must leave HEAD's content a prefix of the new content (history is never rewritten), and
//! every `## SEMULITH-PUSH-NNNN — <timestamp>` entry carries the required fields, its id the next in the
//! sequence that starts at 0001. The script's inline Python is ported with it; its two regular expressions
//! are matched by hand (no new crate), with ASCII digits for `\d` (a ledger heading written in another
//! script's digits is not one). Each self-test arm is one `tally.arm(` call, the idiom the `DERIVED-COUNTS`
//! arm total counts.

use std::fs;
use std::path::Path;
use std::process::{Command, ExitCode, Stdio};

use crate::harness::scratch;

/// The ledger, relative to a repository root.
const LEDGER: &str = "docs/push-approvals.md";

/// Runs the doctrine: `--self-test` as the first argument runs the arms; anything else runs the check.
/// Exit 0 ok, 1 the ledger was rewritten or misshapen, 2 refused.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    if !self_test(root, false) {
        eprintln!("PUSH-RECORD: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    let (findings, count) = check_ledger(root);
    if !findings.is_empty() {
        eprintln!("PUSH-RECORD: the approval ledger was rewritten or misshapen.");
        for finding in &findings {
            eprintln!("  {finding}");
        }
        eprintln!("  The ledger is append-only: a correction is a new entry, never an edit.");
        return ExitCode::from(1);
    }
    let noun = if count == 1 { "y" } else { "ies" };
    println!("PUSH-RECORD: ok (the ledger is append-only; {count} entr{noun} well-formed)");
    ExitCode::SUCCESS
}

/// The entry headings, as `(?m)^## (SEMULITH-PUSH-\d{4}) — \S+` found them: each id and the byte offset of
/// its line.
fn entries(text: &str) -> Vec<(String, usize)> {
    let mut found = Vec::new();
    let mut offset = 0;
    for line in text.split_inclusive('\n') {
        let body = line.strip_suffix('\n').unwrap_or(line);
        if let Some(rest) = body.strip_prefix("## SEMULITH-PUSH-") {
            let digits: String = rest.chars().take(4).collect();
            let after = rest.get(digits.len()..).unwrap_or("");
            let heading = digits.chars().count() == 4
                && digits.chars().all(|c| c.is_ascii_digit())
                && after
                    .strip_prefix(" — ")
                    .and_then(|tail| tail.chars().next())
                    .is_some_and(|c| !c.is_whitespace());
            if heading {
                found.push((format!("SEMULITH-PUSH-{digits}"), offset));
            }
        }
        offset += line.len();
    }
    found
}

/// Whether `body` holds `**Range:**` followed, as `\*\*Range:\*\*\s+(\S+)\.\.([0-9a-f]{40})\s+—\s+(\d+)`
/// required, by `<upstream>..<40 hex> — <digits>`.
fn range_ok(body: &str) -> bool {
    body.match_indices("**Range:**").any(|(at, marker)| {
        let rest = &body[at + marker.len()..];
        let token_start = rest.len() - rest.trim_start().len();
        if token_start == 0 {
            return false; // \s+ needs at least one whitespace character
        }
        let rest = &rest[token_start..];
        let token_end = rest.find(char::is_whitespace).unwrap_or(rest.len());
        let token = &rest[..token_end];
        let shaped = token.len() >= 43
            && token.is_char_boundary(token.len() - 42)
            && &token[token.len() - 42..token.len() - 40] == ".."
            && token[token.len() - 40..]
                .chars()
                .all(|c| c.is_ascii_digit() || ('a'..='f').contains(&c));
        if !shaped {
            return false;
        }
        let tail = &rest[token_end..];
        let spaced = tail.trim_start();
        if spaced.len() == tail.len() {
            return false;
        }
        let Some(after_dash) = spaced.strip_prefix('—') else {
            return false;
        };
        let digits = after_dash.trim_start();
        digits.len() < after_dash.len() && digits.chars().next().is_some_and(|c| c.is_ascii_digit())
    })
}

/// A git command's success and standard output, run from `root`.
fn git(root: &Path, args: &[&str]) -> (bool, String) {
    match Command::new("git")
        .args(args)
        .current_dir(root)
        .stdin(Stdio::null())
        .stderr(Stdio::null())
        .output()
    {
        Ok(output) => (
            output.status.success(),
            String::from_utf8_lossy(&output.stdout).into_owned(),
        ),
        Err(_) => (false, String::new()),
    }
}

/// The ledger's findings under `root` and its entry count (the script's Python `check_ledger`).
fn check_ledger(root: &Path) -> (Vec<String>, usize) {
    let ledger = root.join(LEDGER);
    let text = if ledger.is_file() {
        fs::read_to_string(&ledger).unwrap_or_default()
    } else {
        String::new()
    };
    let mut findings = Vec::new();
    let found = entries(&text);
    for (i, (id, start)) in found.iter().enumerate() {
        let want = format!("SEMULITH-PUSH-{:04}", i + 1);
        if *id != want {
            findings.push(format!(
                "NONSEQUENTIAL {id}: the {}(th) entry must be {want} — a gap or a renumbering is a rewritten history wearing append-only's clothes",
                i + 1
            ));
        }
        let end = found.get(i + 1).map_or(text.len(), |next| next.1);
        let body = &text[*start..end];
        for field in ["Approved by:", "Reason:", "Range:", "Suite:"] {
            if !body.contains(&format!("**{field}**")) {
                findings.push(format!(
                    "MISSING FIELD {id}: no '{field}' — an entry without it is an assertion without its evidence"
                ));
            }
        }
        if !range_ok(body) {
            findings.push(format!(
                "BAD RANGE {id}: the Range field is not '<upstream>..<sha> — N'"
            ));
        }
    }
    let (_, staged) = git(root, &["diff", "--cached", "--name-only", "--", LEDGER]);
    if !staged.trim().is_empty() {
        let (head_ok, head) = git(root, &["show", &format!("HEAD:{LEDGER}")]);
        let (index_ok, index) = git(root, &["show", &format!(":{LEDGER}")]);
        if !index_ok {
            findings.push("NOT STAGED push-approvals.md: the ledger is named in the diff but has no index content — cannot judge; the check refuses rather than guess".to_owned());
        } else if head_ok && !index.starts_with(&head) {
            findings.push("REWRITTEN push-approvals.md: the staged ledger does not begin with HEAD's content — append-only means append-ONLY. A correction is a new entry, never an edit.".to_owned());
        }
    }
    (findings, found.len())
}

/// The self-test's pass and fail counts; `verbose` prints misses on stderr and the summary on stdout.
struct Tally {
    pass: u32,
    fail: u32,
    verbose: bool,
}

impl Tally {
    /// One arm: checking the fixture repository must give `expected` (0 no finding, 1 a finding) and its
    /// text (the findings, then `__CHECKED__ N`) must contain `want`.
    fn arm(&mut self, repo: &Path, name: &str, expected: i32, want: &str) {
        let (findings, count) = check_ledger(repo);
        let rc = i32::from(!findings.is_empty());
        let mut out = findings;
        out.push(format!("__CHECKED__ {count}"));
        let out = out.join("\n");
        if rc != expected {
            self.fail += 1;
            if self.verbose {
                eprintln!(
                    "PUSH-RECORD self-test MISS: {name} expected rc={expected} got rc={rc}\n{out}"
                );
            }
        } else if !out.contains(want) {
            self.fail += 1;
            if self.verbose {
                eprintln!("PUSH-RECORD self-test MISS: {name} right verdict, wrong reason (no {want})\n{out}");
            }
        } else {
            self.pass += 1;
        }
    }
}

/// An entry with the fields the self-test varies.
fn entry(id: &str, at: &str, reason: Option<&str>, sha: &str, commits: u32) -> String {
    let reason = reason.map_or(String::new(), |r| format!("- **Reason:** {r}\n"));
    format!(
        "\n## SEMULITH-PUSH-{id} — {at}\n\n- **Approved by:** the director\n{reason}- **Range:** origin/main..{sha} — {commits} commit(s) since the last push, plus this record commit\n- **Suite:** `make ci` green at {sha} before this record was written\n"
    )
}

/// The six arms over a scratch repository. Returns whether every arm held.
fn self_test(root: &Path, verbose: bool) -> bool {
    let mut tally = Tally {
        pass: 0,
        fail: 0,
        verbose,
    };
    let Ok(t) = scratch(root, "target/doctrine-selftest", "push-record") else {
        if verbose {
            eprintln!("PUSH-RECORD self-test: cannot create a scratch directory");
        }
        return false;
    };
    let ledger = t.join(LEDGER);
    let quiet = |args: &[&str]| git(&t, args).0;
    let append = |text: &str| -> std::io::Result<()> {
        let mut current = fs::read_to_string(&ledger)?;
        current.push_str(text);
        fs::write(&ledger, current)
    };
    let zero = "0123456789012345678901234567890123456789";
    let a40 = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
    let ready = fs::create_dir_all(t.join("docs")).is_ok()
        && quiet(&["init", "-q"])
        && quiet(&["config", "user.email", "t@t"])
        && quiet(&["config", "user.name", "t"])
        && fs::write(&ledger, "# Push approvals\n").is_ok()
        && quiet(&["add", "-A"])
        && quiet(&["commit", "-q", "-m", "base"]);
    if !ready {
        if verbose {
            eprintln!("PUSH-RECORD self-test: cannot build the fixture repository");
        }
        let _ = fs::remove_dir_all(&t);
        return false;
    }
    tally.arm(&t, "GREEN the header-only ledger", 0, "__CHECKED__ 0");
    // a pure append is permitted
    let _ = append(&entry(
        "0001",
        "2026-09-29T00:00:00+0000",
        Some("ship the reviewed slice"),
        zero,
        3,
    ));
    quiet(&["add", LEDGER]);
    tally.arm(&t, "GREEN a pure append", 0, "__CHECKED__ 1");
    quiet(&["commit", "-q", "-m", "first entry"]);
    // a second pure append is permitted
    let _ = append(&entry(
        "0002",
        "2026-09-29T01:00:00+0000",
        Some("the second slice"),
        a40,
        2,
    ));
    quiet(&["add", LEDGER]);
    tally.arm(&t, "GREEN a second pure append", 0, "__CHECKED__ 2");
    quiet(&["commit", "-q", "-m", "second entry"]);
    // editing an old entry is refused
    let edited = fs::read_to_string(&ledger)
        .unwrap_or_default()
        .replace("the second slice", "a rewritten reason");
    let _ = fs::write(&ledger, edited);
    quiet(&["add", LEDGER]);
    tally.arm(
        &t,
        "RED   an edited old entry (history rewritten)",
        1,
        "REWRITTEN",
    );
    quiet(&["checkout", "-q", "--", LEDGER]);
    // an entry missing a required field is refused
    let _ = append(&entry("0002", "2026-09-29T01:00:00+0000", None, a40, 2));
    quiet(&["add", LEDGER]);
    tally.arm(&t, "RED   an entry missing its Reason", 1, "MISSING FIELD");
    quiet(&["checkout", "-q", "--", LEDGER]);
    // a gap in the sequence is refused
    let _ = append(&entry(
        "0007",
        "2026-09-29T01:00:00+0000",
        Some("a skipped number"),
        a40,
        2,
    ));
    quiet(&["add", LEDGER]);
    tally.arm(&t, "RED   a skipped sequence number", 1, "NONSEQUENTIAL");
    quiet(&["checkout", "-q", "--", LEDGER]);
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "PUSH-RECORD --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}
