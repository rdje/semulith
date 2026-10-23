//! `cargo xtask` — SEMULITH's automation front door (tree `XTASK`).
//!
//! The director's direction (`decision_rust-native-tooling.md`, 2026-10-23): move to cargo xtask
//! incrementally and with extreme care, never breaking anything.
//!
//! - `cargo xtask <args>` runs `make <args>` from the repository root with the same environment,
//!   the same standard streams and the same exit status (`XTASK.1`), so every Makefile target keeps
//!   exactly one definition — the Makefile — until a later leaf moves one, shim first. `cargo xtask`
//!   alone runs `make help`.
//! - `cargo xtask focused [--out DIR]` runs the focused check set every unit runs before its gated
//!   commit (`XTASK.2`): each check in order, its output kept in `DIR` (default `target/focused`),
//!   one line per check, a summary and a JSON record, exit 1 if any check is red. It never commits.
//!
//! One definition per target (`XTASK.3`): a command is either native here, named in `NATIVE`, or
//! the Makefile's — never both. A unit test reads the Makefile and refuses a native name that is
//! also a Makefile target.

use std::fmt::Write as _;
use std::fs;
use std::path::{Path, PathBuf};
use std::process::{Command, ExitCode, Stdio};
use std::time::{SystemTime, UNIX_EPOCH};

/// The focused check set, in the order the commit workflow has run it since 2026-10-22: the
/// repository-wide documentation, routing, task-tree, history and record checks, then the book.
/// Before `XTASK.2` this list lived only in per-unit scratch scripts under `target/`.
const FOCUSED: &[&[&str]] = &[
    &["bash", "scripts/check_memory_architecture.sh"],
    &["bash", "scripts/check_readme_routes.sh"],
    &["bash", "scripts/check_registry_mirror.sh"],
    &["bash", "scripts/check_tree_claims.sh"],
    &["bash", "scripts/check_derived_counts.sh"],
    &["bash", "scripts/check_frontier_sync.sh"],
    &["bash", "scripts/check_book_index.sh"],
    &["bash", "scripts/check_task_history.sh"],
    &["bash", "knowledge-map/scripts/check_knowledge_map.sh"],
    &["bash", "scripts/check_live_doc_currency.sh"],
    &["bash", "scripts/check_docpaths.sh"],
    &["bash", "scripts/check_seam_integrity.sh"],
    &["bash", "scripts/check_lesson_promotion.sh"],
    &["bash", "scripts/check_routing_evidence.sh"],
    &["bash", "scripts/check_gap_claims.sh"],
    &["bash", "scripts/check_waiver_routing.sh"],
    &["bash", "scripts/check_source_format.sh"],
    &["bash", "scripts/check_unit_books.sh"],
    &["bash", "scripts/check_materials_bill.sh"],
    &["bash", "scripts/check_changelog_shards.sh"],
    &["bash", "scripts/check_task_acceptance.sh"],
    &["bash", "scripts/check_table_arity.sh"],
    &["bash", "scripts/check_fixture_fingerprints.sh"],
    &["bash", "scripts/check_gate_report.sh"],
    &["bash", "scripts/check_requirements.sh"],
    &["make", "book"],
];

/// The subcommands xtask implements itself; every other argument list is the Makefile's.
const NATIVE: &[&str] = &["focused"];

/// Dispatches a native subcommand here and every other argument list to `make`.
fn main() -> ExitCode {
    let mut args: Vec<String> = std::env::args().skip(1).collect();
    let root = repository_root();
    if let Some(name) = args.first().filter(|arg| NATIVE.contains(&arg.as_str())) {
        return match name.as_str() {
            "focused" => focused(&root, &args[1..]),
            other => {
                eprintln!("xtask: native subcommand {other} has no implementation");
                ExitCode::from(2)
            }
        };
    }
    if args.is_empty() {
        args.push("help".to_owned());
    }
    // Run from the root rather than `make -C`, which would add "Entering directory" lines.
    match Command::new("make").args(&args).current_dir(&root).status() {
        Ok(status) => exit_code(status.code()),
        Err(error) => {
            eprintln!("xtask: cannot run make: {error}");
            ExitCode::from(127)
        }
    }
}

/// The repository root: this crate's parent directory, fixed at build time, so the front door
/// behaves the same from any working directory.
fn repository_root() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap_or_else(|| Path::new("."))
        .to_path_buf()
}

/// A child's exit status as ours; a signal (no code) is never reported as success.
fn exit_code(code: Option<i32>) -> ExitCode {
    match code {
        Some(code) => ExitCode::from(u8::try_from(code).unwrap_or(1)),
        None => ExitCode::from(1),
    }
}

/// The log name of a focused check: its script's stem, or `book` for `make book`.
fn log_name(command: &[&str]) -> String {
    let last = command.last().copied().unwrap_or("check");
    let file = last.rsplit('/').next().unwrap_or(last);
    file.strip_suffix(".sh").unwrap_or(file).to_owned()
}

/// `HH:MM:SS` in UTC for a number of seconds since the Unix epoch.
fn utc_clock(seconds: u64) -> String {
    let day = seconds % 86_400;
    format!("{:02}:{:02}:{:02}", day / 3600, day % 3600 / 60, day % 60)
}

/// The last non-empty line of a check's output, as the one-line verdict.
fn last_line(output: &str) -> &str {
    output
        .lines()
        .rev()
        .find(|line| !line.trim().is_empty())
        .unwrap_or("")
}

/// Runs the focused set, keeping each check's output, and reports red checks by exit status.
fn focused(root: &Path, args: &[String]) -> ExitCode {
    let out = match args {
        [] => root.join("target/focused"),
        [flag, dir] if flag == "--out" => root.join(dir),
        _ => {
            eprintln!("usage: cargo xtask focused [--out DIR]");
            return ExitCode::from(2);
        }
    };
    if let Err(error) = fs::create_dir_all(&out) {
        eprintln!("xtask focused: cannot create {}: {error}", out.display());
        return ExitCode::from(2);
    }
    let mut red = 0;
    let mut record = String::from("[\n");
    for (index, command) in FOCUSED.iter().enumerate() {
        let (program, rest) = command
            .split_first()
            .expect("a focused command is never empty");
        let result = Command::new(program)
            .args(rest)
            .current_dir(root)
            .stdin(Stdio::null())
            .output();
        let (code, text) = match result {
            Ok(output) => {
                let mut text = String::from_utf8_lossy(&output.stdout).into_owned();
                text.push_str(&String::from_utf8_lossy(&output.stderr));
                (output.status.code(), text)
            }
            Err(error) => (
                None,
                format!("xtask focused: cannot run {program}: {error}\n"),
            ),
        };
        let shown = code.map_or_else(|| "signal".to_owned(), |c| c.to_string());
        if code != Some(0) {
            red += 1;
        }
        let log = out.join(format!("{}.log", log_name(command)));
        if let Err(error) = fs::write(&log, &text) {
            eprintln!("xtask focused: cannot write {}: {error}", log.display());
            return ExitCode::from(2);
        }
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map_or(0, |d| d.as_secs());
        let verdict: String = last_line(&text).chars().take(160).collect();
        println!(
            "{} {} rc={shown}: {verdict}",
            utc_clock(now),
            command.join(" ")
        );
        let quoted: Vec<String> = command.iter().map(|part| format!("\"{part}\"")).collect();
        let separator = if index + 1 < FOCUSED.len() { "," } else { "" };
        let _ = writeln!(record, "  [[{}], {shown}]{separator}", quoted.join(", "));
    }
    record.push_str("]\n");
    if let Err(error) = fs::write(out.join("focused-checks.json"), record) {
        eprintln!("xtask focused: cannot write the record: {error}");
        return ExitCode::from(2);
    }
    println!("focused: {red} red of {}", FOCUSED.len());
    if red == 0 {
        ExitCode::SUCCESS
    } else {
        ExitCode::from(1)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    /// The rule names a Makefile defines (`name:` at the start of a line, not a variable).
    fn makefile_rules(text: &str) -> Vec<String> {
        text.lines()
            .filter(|line| !line.starts_with(['\t', '#', '.', ' ']))
            .filter_map(|line| line.split_once(':').map(|(name, _)| name))
            .filter(|name| !name.is_empty() && !name.contains([' ', '=', '$']))
            .map(str::to_owned)
            .collect()
    }

    #[test]
    fn a_native_subcommand_is_never_also_a_makefile_target() {
        let makefile =
            fs::read_to_string(repository_root().join("Makefile")).expect("the Makefile");
        let rules = makefile_rules(&makefile);
        assert!(
            rules.len() >= 10,
            "the Makefile parse found too few rules: {rules:?}"
        );
        let phony = makefile
            .lines()
            .find_map(|line| line.strip_prefix(".PHONY:"))
            .expect("a .PHONY line");
        let mut declared: Vec<&str> = phony.split_whitespace().collect();
        let mut defined: Vec<&str> = rules.iter().map(String::as_str).collect();
        declared.sort_unstable();
        defined.sort_unstable();
        assert_eq!(
            declared, defined,
            "every rule is .PHONY and every .PHONY name a rule"
        );
        for name in NATIVE {
            assert!(
                !rules.iter().any(|rule| rule == name),
                "{name} is defined twice"
            );
        }
    }

    #[test]
    fn the_makefile_rule_parse_ignores_variables_recipes_and_comments() {
        let text = "SHELL := /usr/bin/env bash\n.PHONY: a b\n# c: comment\na:\n\techo x: y\nb: a\n";
        assert_eq!(makefile_rules(text), vec!["a", "b"]);
    }

    #[test]
    fn every_focused_check_exists_in_the_repository() {
        let root = repository_root();
        for command in FOCUSED {
            if command[0] == "bash" {
                assert!(
                    root.join(command[1]).is_file(),
                    "missing focused check {}",
                    command[1]
                );
            }
        }
        assert_eq!(FOCUSED.len(), 26);
    }

    #[test]
    fn log_names_are_unique_and_readable() {
        let names: Vec<String> = FOCUSED.iter().map(|c| log_name(c)).collect();
        let mut sorted = names.clone();
        sorted.sort();
        sorted.dedup();
        assert_eq!(sorted.len(), names.len());
        assert_eq!(log_name(&["make", "book"]), "book");
        assert_eq!(
            log_name(&["bash", "scripts/check_docpaths.sh"]),
            "check_docpaths"
        );
    }

    #[test]
    fn clock_and_verdict_helpers() {
        assert_eq!(utc_clock(0), "00:00:00");
        assert_eq!(utc_clock(86_399), "23:59:59");
        assert_eq!(utc_clock(86_400 + 3_661), "01:01:01");
        assert_eq!(last_line("a\nb\n\n"), "b");
        assert_eq!(last_line(""), "");
    }
}
