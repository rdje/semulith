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
//! - `cargo xtask build-bench` builds the browser bench's wasm module and copies it next to the page
//!   (`XTASK.4` slice `4a`; formerly `scripts/build_bench.sh`, which `make bench` still runs and which is
//!   now a one-line shim to this subcommand).
//! - `cargo xtask check-wasm-build [--self-test]` is the `PORT-WEB` doctrine (`XTASK.6` slice `6a`;
//!   formerly `scripts/check_wasm_build.sh`, which the doctrine driver still runs, now a shim).
//! - `cargo xtask check-commit-prefix [--self-test]` is the `COMMIT-PREFIX` doctrine (`XTASK.6` slice
//!   `6b`; formerly `scripts/check_commit_prefix.sh`, now a shim). The doctrine modules share `harness`.
//! - `cargo xtask check-delivery-provenance [--self-test]` is the `DELIVERY-PROVENANCE` doctrine
//!   (`XTASK.6` slice `6c`; formerly `scripts/check_delivery_provenance.sh`, now a shim).
//! - `cargo xtask check-rustdoc [--self-test]` is the `API-DOCS` doctrine (`XTASK.6` slice `6d`; formerly
//!   `scripts/check_rustdoc.sh`, now a shim): the rustdoc check in Rust.
//! - `cargo xtask check-push-record [--self-test]` is the `PUSH-RECORD` doctrine (`XTASK.6` slice `6e`;
//!   formerly `scripts/check_push_record.sh`, now a shim).
//! - `cargo xtask check-fixture-fingerprints [--self-test]` is the `FIXTURE-FINGERPRINT` doctrine (`XTASK.6`
//!   slice `6g`; formerly `scripts/check_fixture_fingerprints.sh`, now a shim): every pinned `sha256` re-derived.
//! - `cargo xtask check-fact-ownership [--self-test]` is the `FACT-OWNERSHIP` doctrine (`XTASK.6` slice `6h`;
//!   formerly `scripts/check_fact_ownership.sh`, now a shim): one owner per fact kind, every mirror governed.
//! - `cargo xtask check-registry-mirror [--self-test]` is the `REGISTRY-MIRROR` doctrine (`XTASK.6` slice `6i`;
//!   formerly `scripts/check_registry_mirror.sh`, now a shim): the two documents list what the registry registers.
//! - `cargo xtask check-exercise-coverage [--self-test]` is the `EXERCISE-COVERAGE` doctrine (`XTASK.6` slice `6k`;
//!   formerly `scripts/check_exercise_coverage.sh`, now a shim): every declared scope form executed by a tracked
//!   guest, the composition closed through the one resolver — the first consumer of the Rust S-expression reader.
//! - `cargo xtask check-unit-composition [--self-test]` is the `UNIT-COMPOSITION` doctrine (`XTASK.6` slice `6n`;
//!   formerly `scripts/check_unit_composition.sh`, now a shim): every tracked unit composition decided through the
//!   one disjointness judge — the third unit of the port that began with the schema validator.
//! - `cargo xtask check-scope-coverage [--self-test]` is the `SCOPE-COVERAGE` doctrine (`XTASK.6` slice `6p`,
//!   `check_scope_coverage.rs`): every unit's declared scope against the census beside its registry, read through
//!   the Rust record mapping; `scripts/check_scope_coverage.sh` is its shim.
//! - `cargo xtask check-extraction [--self-test]` is the `EXTRACTION` doctrine (`XTASK.6` slice `6q`,
//!   `check_extraction.rs`): every tracked unit judged by the pinned Python judge `scripts/check_extraction.py`,
//!   spawned as the driver spawned it, the self-test's record fixtures written through the Rust record mapping;
//!   `scripts/check_extraction.sh` is its shim.
//! - `cargo xtask check-citation-quotes [--self-test]` is the `CITATION-QUOTES` doctrine's driver (`XTASK.6` slice
//!   `6r`, `check_citation_quotes.rs`): the pinned Python tool `scripts/check_citation_quotes.py` spawned as the driver
//!   spawned it, its two inline Python controls run verbatim; `scripts/check_citation_quotes.sh` is its shim.
//! - `cargo xtask check-m-vectors [--self-test]` is the `M-VECTORS` doctrine's driver (`XTASK.6` slice `6s`,
//!   `check_m_vectors.rs`): the table judged against its generator by the driver's inline Python judge, run verbatim;
//!   `scripts/check_m_vectors.sh` is its shim.
//! - `cargo xtask check-book-index [--self-test]` is the `BOOK-INDEX` doctrine's driver (`XTASK.6` slice `6t`,
//!   `check_book_index.rs`): the committed book index judged against a regeneration by `scripts/gen_book_index.py`,
//!   spawned as the driver spawned it; `scripts/check_book_index.sh` is its shim.
//! - `cargo xtask check-board-verdict [--self-test]` is the `BOARD-VERDICT` doctrine's driver (`XTASK.6` slice `6u`,
//!   `check_board_verdict.rs`): every tracked board's composition decided by `scripts/board_verdict.py`, spawned as the
//!   driver spawned it; `scripts/check_board_verdict.sh` is its shim.
//! - `cargo xtask check-board-gen [--self-test]` is the `BOARD-GEN` doctrine's driver (`XTASK.6` slice `6v`,
//!   `check_board_gen.rs`): every tracked board's generated artifacts judged against a regeneration by
//!   `scripts/gen_board.py`, spawned as the driver spawned it; `scripts/check_board_gen.sh` is its shim.
//! - `cargo xtask check-platform-gen [--self-test]` is the `PLATFORM-GEN` doctrine's driver (`XTASK.6` slice `6w`,
//!   `check_platform_gen.rs`): every tracked board's platform capability manifest judged against a regeneration by
//!   `scripts/gen_platform.py`, spawned as the driver spawned it; `scripts/check_platform_gen.sh` is its shim.
//! - `cargo xtask check-state-gen [--self-test]` is the `STATE-GEN` doctrine's driver (`XTASK.6` slice `6x`,
//!   `check_state_gen.rs`): the architectural-state modules judged against a regeneration from their descriptors by
//!   `scripts/gen_state.py`, spawned as the driver spawned it; `scripts/check_state_gen.sh` is its shim.
//! - `cargo xtask check-interaction-matrix [--self-test]` is the `INTERACTION-MATRIX` doctrine's driver (`XTASK.6`
//!   slice `6y`, `check_interaction_matrix.rs`): every tracked unit's declared matrix judged by
//!   `scripts/check_interaction_matrix.py`, spawned as the driver spawned it; `scripts/check_interaction_matrix.sh` is its shim.
//! - `cargo xtask check-unit-books [--self-test]` is the `UNIT-BOOKS` doctrine's driver (`XTASK.6` slice `6z`,
//!   `check_unit_books.rs`): every registered unit's model book judged over a fresh `mdbook` bundle by
//!   `scripts/unit_books.py`, spawned as the driver spawned it; `scripts/check_unit_books.sh` is its shim.
//! - `cargo xtask check-tree-claims [--self-test]` is the `TREE-CLAIMS` doctrine's driver (`XTASK.6` slice `6aa`,
//!   `check_tree_claims.rs`): every live document's tree facts re-derived by the driver's inline Python judge, run
//!   verbatim; `scripts/check_tree_claims.sh` is its shim.
//! - `cargo xtask check-encoding-disjoint <fragment…> | --self-test` judges a composition's instruction encodings
//!   pairwise disjoint (`XTASK.6` slice `6m`, `disjoint.rs`), measured equal to the pinned
//!   `scripts/check_encoding_disjoint.py` over every tracked encoding and fragment; the composition resolver both
//!   consumers share is `composition.rs`. The pinned judge stays.
//! - `cargo xtask check-sexp-schema <file.sexp> <schema.sexp> | --self-test` validates a source-of-truth file against
//!   its schema with the Rust validator (`XTASK.6` slice `6l`, `schema.rs`), measured equal to the pinned
//!   `scripts/check_sexp_schema.py` over every pair the project validates; the pinned validator stays.
//! - `cargo xtask records <catalogue.sexp> [--dump]` reads a record catalogue through the Rust record mapping
//!   (`XTASK.6` slice `6o`, `records.rs`), measured equal to the pinned `scripts/records_sexp.py` on every
//!   catalogue the project keeps; the pinned mapping stays.
//! - `cargo xtask sexp <file.sexp>` parses a file with the Rust S-expression reader (`XTASK.6` slice `6j`,
//!   `sexp.rs`), measured equal to the pinned `scripts/sexp.py` on the corpus; the pinned reader stays.
//!
//! One definition per target (`XTASK.3`): a command is either native here, named in `NATIVE`, or
//! the Makefile's — never both. A unit test reads the Makefile and refuses a native name that is
//! also a Makefile target. A script ported here stays as a shim that only runs its subcommand; a unit
//! test holds each shim, listed in `PORTED`, to exactly that — three commands, or the same with the
//! repository-volume scratch preamble that `probe_temporary_locality.py` requires of some scripts.

mod check_board_gen;
mod check_board_verdict;
mod check_book_index;
mod check_citation_quotes;
mod check_commit_prefix;
mod check_delivery_provenance;
mod check_exercise_coverage;
mod check_extraction;
mod check_fact_ownership;
mod check_fixture_fingerprints;
mod check_interaction_matrix;
mod check_m_vectors;
mod check_platform_gen;
mod check_push_record;
mod check_registry_mirror;
mod check_rustdoc;
mod check_scope_coverage;
mod check_state_gen;
mod check_tree_claims;
mod check_unit_books;
mod check_unit_composition;
mod check_wasm_build;
mod composition;
mod disjoint;
mod harness;
mod records;
mod schema;
mod sexp;

use std::fmt::Write as _;
use std::fs;
use std::path::{Path, PathBuf};
use std::process::{Command, ExitCode, Stdio};
use std::time::{SystemTime, UNIX_EPOCH};

/// The focused check set, in the order the commit workflow has run it since 2026-10-22 (API-DOCS since
/// 2026-10-26, `XTASK.7`): the
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
    // XTASK.7 (decision_focused-set-runs-api-docs.md): the rustdoc check before the book copies the reference.
    &["bash", "scripts/check_rustdoc.sh"],
    &["make", "book"],
];

/// The subcommands xtask implements itself; every other argument list is the Makefile's.
const NATIVE: &[&str] = &[
    "focused",
    "build-bench",
    "check-wasm-build",
    "check-commit-prefix",
    "check-delivery-provenance",
    "check-rustdoc",
    "check-push-record",
    "check-fixture-fingerprints",
    "check-fact-ownership",
    "check-registry-mirror",
    "check-exercise-coverage",
    "sexp",
    "check-sexp-schema",
    "records",
    "check-encoding-disjoint",
    "check-unit-composition",
    "check-scope-coverage",
    "check-extraction",
    "check-citation-quotes",
    "check-m-vectors",
    "check-book-index",
    "check-board-verdict",
    "check-board-gen",
    "check-platform-gen",
    "check-state-gen",
    "check-interaction-matrix",
    "check-unit-books",
    "check-tree-claims",
];

/// The scripts ported to a native subcommand, each kept as a shim that runs only that subcommand. Read by
/// the shim test only: dispatch needs the native names alone.
#[cfg(test)]
const PORTED: &[(&str, &str)] = &[
    ("check-tree-claims", "scripts/check_tree_claims.sh"),
    ("check-unit-books", "scripts/check_unit_books.sh"),
    (
        "check-interaction-matrix",
        "scripts/check_interaction_matrix.sh",
    ),
    ("check-state-gen", "scripts/check_state_gen.sh"),
    ("check-platform-gen", "scripts/check_platform_gen.sh"),
    ("check-board-gen", "scripts/check_board_gen.sh"),
    ("check-board-verdict", "scripts/check_board_verdict.sh"),
    ("check-book-index", "scripts/check_book_index.sh"),
    ("check-m-vectors", "scripts/check_m_vectors.sh"),
    ("build-bench", "scripts/build_bench.sh"),
    ("check-wasm-build", "scripts/check_wasm_build.sh"),
    ("check-commit-prefix", "scripts/check_commit_prefix.sh"),
    (
        "check-delivery-provenance",
        "scripts/check_delivery_provenance.sh",
    ),
    ("check-rustdoc", "scripts/check_rustdoc.sh"),
    ("check-push-record", "scripts/check_push_record.sh"),
    (
        "check-fixture-fingerprints",
        "scripts/check_fixture_fingerprints.sh",
    ),
    ("check-fact-ownership", "scripts/check_fact_ownership.sh"),
    ("check-registry-mirror", "scripts/check_registry_mirror.sh"),
    (
        "check-unit-composition",
        "scripts/check_unit_composition.sh",
    ),
    ("check-scope-coverage", "scripts/check_scope_coverage.sh"),
    ("check-extraction", "scripts/check_extraction.sh"),
    ("check-citation-quotes", "scripts/check_citation_quotes.sh"),
    (
        "check-exercise-coverage",
        "scripts/check_exercise_coverage.sh",
    ),
];

/// Dispatches a native subcommand here and every other argument list to `make`.
fn main() -> ExitCode {
    let mut args: Vec<String> = std::env::args().skip(1).collect();
    let root = repository_root();
    if let Some(name) = args.first().filter(|arg| NATIVE.contains(&arg.as_str())) {
        return match name.as_str() {
            "focused" => focused(&root, &args[1..]),
            "build-bench" => build_bench(&root),
            "check-wasm-build" => check_wasm_build::run(&root, &args[1..]),
            "check-commit-prefix" => check_commit_prefix::run(&root, &args[1..]),
            "check-delivery-provenance" => check_delivery_provenance::run(&root, &args[1..]),
            "check-rustdoc" => check_rustdoc::run(&root, &args[1..]),
            "check-push-record" => check_push_record::run(&root, &args[1..]),
            "check-fixture-fingerprints" => check_fixture_fingerprints::run(&root, &args[1..]),
            "check-fact-ownership" => check_fact_ownership::run(&root, &args[1..]),
            "check-registry-mirror" => check_registry_mirror::run(&root, &args[1..]),
            "check-exercise-coverage" => check_exercise_coverage::run(&root, &args[1..]),
            "sexp" => sexp::run(&args[1..]),
            "check-sexp-schema" => schema::run(&root, &args[1..]),
            "records" => records::run(&root, &args[1..]),
            "check-encoding-disjoint" => disjoint::run(&root, &args[1..]),
            "check-unit-composition" => check_unit_composition::run(&root, &args[1..]),
            "check-scope-coverage" => check_scope_coverage::run(&root, &args[1..]),
            "check-extraction" => check_extraction::run(&root, &args[1..]),
            "check-citation-quotes" => check_citation_quotes::run(&root, &args[1..]),
            "check-m-vectors" => check_m_vectors::run(&root, &args[1..]),
            "check-book-index" => check_book_index::run(&root, &args[1..]),
            "check-board-verdict" => check_board_verdict::run(&root, &args[1..]),
            "check-board-gen" => check_board_gen::run(&root, &args[1..]),
            "check-platform-gen" => check_platform_gen::run(&root, &args[1..]),
            "check-state-gen" => check_state_gen::run(&root, &args[1..]),
            "check-interaction-matrix" => check_interaction_matrix::run(&root, &args[1..]),
            "check-unit-books" => check_unit_books::run(&root, &args[1..]),
            "check-tree-claims" => check_tree_claims::run(&root, &args[1..]),
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

/// `cargo xtask build-bench`: builds the bench's wasm module, `semulith-verify`'s cdylib (`LAB-BENCH.1`),
/// and copies it to the gitignored `bench/semulith_verify.wasm`, the one way that copy appears. Ported
/// from `scripts/build_bench.sh` with its behaviour kept: arguments are ignored, cargo's own output and a
/// failed build's exit status pass through, a failed copy is exit 1, and success prints the same two lines.
fn build_bench(root: &Path) -> ExitCode {
    let build = Command::new("cargo")
        .args(["build", "--release", "-p", "semulith-verify"])
        .args(["--target", "wasm32-unknown-unknown"])
        .current_dir(root)
        .status();
    match build {
        Ok(status) if status.success() => {}
        Ok(status) => return exit_code(status.code()),
        Err(error) => {
            eprintln!("xtask build-bench: cannot run cargo: {error}");
            return ExitCode::from(127);
        }
    }
    let module = "bench/semulith_verify.wasm";
    let built = root.join("target/wasm32-unknown-unknown/release/semulith_verify.wasm");
    match fs::copy(built, root.join(module)) {
        Ok(bytes) => {
            println!("bench: {module} ({bytes} bytes)");
            println!(
                "bench: serve with 'python3 -m http.server -d bench 8000' and open http://localhost:8000/"
            );
            ExitCode::SUCCESS
        }
        Err(error) => {
            eprintln!("xtask build-bench: cannot copy the module to {module}: {error}");
            ExitCode::from(1)
        }
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
    fn a_ported_script_is_a_shim_that_only_runs_its_subcommand() {
        let root = repository_root();
        for (name, script) in PORTED {
            assert!(NATIVE.contains(name), "{name} is ported but not native");
            let text = fs::read_to_string(root.join(script)).expect("the ported script");
            let body: Vec<&str> = text
                .lines()
                .filter(|line| !line.trim().is_empty() && !line.starts_with('#'))
                .collect();
            let exec = format!("exec cargo xtask {name} \"$@\"");
            let plain = [
                "set -euo pipefail",
                "cd \"$(git rev-parse --show-toplevel)\"",
                exec.as_str(),
            ];
            // The same, keeping the scratch preamble probe_temporary_locality.py reads in some scripts.
            let local = [
                "set -euo pipefail",
                "ROOT=\"$(git rev-parse --show-toplevel)\" || exit 2; cd \"$ROOT\"",
                "mkdir -p \"$ROOT/target/tmp\" || exit 2",
                "export TMPDIR=\"$ROOT/target/tmp\"",
                exec.as_str(),
            ];
            assert!(
                body == plain || body == local,
                "{script} must stay a shim of cargo xtask {name}: {body:?}"
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
        assert_eq!(FOCUSED.len(), 27);
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
