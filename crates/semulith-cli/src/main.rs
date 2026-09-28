//! User commands and report presentation (`docs/ARCHITECTURE.md` §4): this
//! binary calls the core and verification APIs and never duplicates behaviour
//! they own.
//!
//! Commands:
//!
//! - `semulith check-examples [--root DIR]` — run the graph and report checker
//!   (`P1-LAB.7`, T004) over the frozen `examples/` JSONL records: schema
//!   validation (the PACKAGE_CHECKS rows re-derived in Rust per RUST-01) and
//!   then the `docs/EVIDENCE_AND_GATES.md` §3 graph invariants. Prints the
//!   verdict report. Exit codes: 0 — no defects (the gate line reads `passed`
//!   or `incomplete`; `incomplete` is the honest state of the deliberately
//!   `planned` fixture evidence); 1 — the bundle is rejected, every finding
//!   named; 2 — the command could not run (usage, unreadable inputs).
//!
//! The execution-slice commands land with `P1-LAB.8`; the wiring below is real
//! from day one.

use std::path::{Path, PathBuf};
use std::process::ExitCode;

use semulith_core as _;
use semulith_verify::graph::{check_bundle, Bundle};
use semulith_verify::json::{self, Json};
use semulith_verify::schema;

const USAGE: &str = "semulith — the laboratory control surface\n\
                     usage: semulith check-examples [--root DIR]\n";

fn main() -> ExitCode {
    let args: Vec<String> = std::env::args().skip(1).collect();
    match args.first().map(String::as_str) {
        Some("check-examples") => {
            let root = args
                .get(1)
                .map(String::as_str)
                .and_then(|a| a.strip_prefix("--root="))
                .map_or_else(|| PathBuf::from("."), PathBuf::from);
            check_examples(&root)
        }
        _ => {
            eprint!("{USAGE}");
            ExitCode::from(2)
        }
    }
}

fn read(root: &Path, rel: &str) -> Result<String, String> {
    std::fs::read_to_string(root.join(rel)).map_err(|e| format!("cannot read {rel}: {e}"))
}

fn read_records(root: &Path, rel: &str) -> Result<Vec<Json>, String> {
    let text = read(root, rel)?;
    let mut records = Vec::new();
    for (i, line) in text.lines().enumerate() {
        if line.trim().is_empty() {
            continue;
        }
        let record = json::parse(line).map_err(|e| format!("{rel}: line {}: {e}", i + 1))?;
        records.push(record);
    }
    if records.is_empty() {
        return Err(format!("{rel}: the document contains no records"));
    }
    Ok(records)
}

fn check_examples(root: &Path) -> ExitCode {
    let run = (|| -> Result<(String, bool), String> {
        let examples = root.join("examples");
        let catalogues = [
            (
                "examples/requirements.jsonl",
                "schemas/requirement.schema.json",
            ),
            ("examples/evidence.jsonl", "schemas/evidence.schema.json"),
            (
                "examples/contract-obligations.jsonl",
                "schemas/contract-obligation.schema.json",
            ),
        ];

        // phase 1 — schema validity, the re-derived PACKAGE_CHECKS rows
        let mut schema_errors: Vec<String> = Vec::new();
        for (records_rel, schema_rel) in catalogues {
            let schema_text = read(root, schema_rel)?;
            let schema_doc = json::parse(&schema_text).map_err(|e| format!("{schema_rel}: {e}"))?;
            let schema = schema::validate_jsonl(&read(root, records_rel)?, &schema_doc)
                .map_err(|r| format!("{schema_rel}: {r}"))?;
            schema_errors.extend(schema.into_iter().map(|e| format!("{records_rel}: {e}")));
        }
        if !schema_errors.is_empty() {
            return Ok((
                format!("schema: {} error(s)\n", schema_errors.len())
                    + &schema_errors
                        .iter()
                        .map(|e| format!("  SCHEMA {e}\n"))
                        .collect::<String>(),
                false,
            ));
        }

        // phase 2 — the graph invariants over the parsed bundle
        let bundle = Bundle {
            requirements: read_records(root, "examples/requirements.jsonl")?,
            evidence: read_records(root, "examples/evidence.jsonl")?,
            obligations: read_records(root, "examples/contract-obligations.jsonl")?,
            context: json::parse(&read(root, "examples/fixture-context.json")?)
                .map_err(|e| format!("examples/fixture-context.json: {e}"))?,
            sources: json::parse(&read(root, "examples/sources.json")?)
                .map_err(|e| format!("examples/sources.json: {e}"))?,
        };
        let resolver = |path: &str| std::fs::read(examples.join(path)).ok();
        let report = check_bundle(&bundle, &resolver);
        Ok((report.render(&bundle), report.findings.is_empty()))
    })();

    match run {
        Ok((text, accepted)) => {
            print!("{text}");
            if accepted {
                ExitCode::from(0)
            } else {
                ExitCode::from(1)
            }
        }
        Err(why) => {
            eprintln!("check-examples: {why}");
            ExitCode::from(2)
        }
    }
}
