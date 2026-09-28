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
//! - `semulith run <elf> [--steps N] [--base ADDR] [--size BYTES]` — execute a
//!   freestanding guest under the laboratory environment (`P1-LAB.8`, T006):
//!   load the ELF's PT_LOAD segments into the declared region, run the
//!   definitional interpreter for at most `steps` steps, and print one
//!   normalized observation per step — the same `(pc, word, writes, trap)`
//!   vocabulary `scripts/compare_traces.py` reduces the reference models to,
//!   so every model is compared through the one parser. Exit codes: 0 — the
//!   run stopped on a trap or the step budget (a target observation, not an
//!   error); 1 — the model reported a model error or an undefined case; 2 —
//!   usage, unreadable inputs, or an ELF the loader refuses.

use std::path::{Path, PathBuf};
use std::process::ExitCode;

use semulith_core::definition::decode;
use semulith_verify::elf;
use semulith_verify::fixtures::FlatMemory;
use semulith_verify::graph::{check_bundle, Bundle};
use semulith_verify::json::{self, Json};
use semulith_verify::run::Stop;
use semulith_verify::schema;

const USAGE: &str = "semulith — the laboratory control surface\n\
                     usage: semulith check-examples [--root DIR]\n\
                     \x20       semulith run <elf> [--steps N] [--base ADDR] [--size BYTES]\n";

/// The platform's declared MainMemory region: base and size from the matched
/// profile (`reference/sail-rv64i-lab-v0.override.sexp` names the same region).
const DEFAULT_BASE: u64 = 0x8000_0000;
const DEFAULT_SIZE: u64 = 0x8000_0000;
const DEFAULT_STEPS: usize = 1_000_000;

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
        Some("run") => run_guest(&args[1..]),
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

fn run_guest(args: &[String]) -> ExitCode {
    let mut elf_path: Option<&str> = None;
    let mut steps = DEFAULT_STEPS;
    let mut base = DEFAULT_BASE;
    let mut size = DEFAULT_SIZE;
    for arg in args {
        if let Some(n) = arg.strip_prefix("--steps=") {
            steps = match n.parse() {
                Ok(v) => v,
                Err(_) => return usage("run: --steps wants an integer"),
            };
        } else if let Some(v) = arg.strip_prefix("--base=") {
            base = match parse_u64(v) {
                Ok(v) => v,
                Err(_) => return usage("run: --base wants an address"),
            };
        } else if let Some(v) = arg.strip_prefix("--size=") {
            size = match parse_u64(v) {
                Ok(v) => v,
                Err(_) => return usage("run: --size wants a byte count"),
            };
        } else if arg.starts_with("--") {
            return usage(&format!("run: unknown option {arg}"));
        } else if elf_path.is_none() {
            elf_path = Some(arg);
        } else {
            return usage("run: more than one ELF operand");
        }
    }
    let Some(elf_path) = elf_path else {
        return usage("run: an ELF operand is required");
    };
    let bytes = match std::fs::read(elf_path) {
        Ok(b) => b,
        Err(e) => {
            eprintln!("run: cannot read {elf_path}: {e}");
            return ExitCode::from(2);
        }
    };
    let image = match elf::parse(&bytes) {
        Ok(image) => image,
        Err(why) => {
            eprintln!("run: {elf_path}: refused — {why}");
            return ExitCode::from(2);
        }
    };
    let Some(top) = base.checked_add(size) else {
        eprintln!("run: the region [{base:#018x}, +{size:#x}) wraps the address space");
        return ExitCode::from(2);
    };
    let mut env = FlatMemory::new(base, size as usize);
    for seg in &image.segments {
        let seg_end = seg.paddr.saturating_add(seg.memsz);
        if seg.paddr < base || seg_end > top {
            eprintln!(
                "run: segment at {:#018x} ({} byte(s)) lies outside the declared region [{:#018x}, {:#018x})",
                seg.paddr, seg.memsz, base, top
            );
            return ExitCode::from(2);
        }
        env.load_image(
            (seg.paddr - base) as usize,
            &bytes[seg.offset..seg.offset + seg.filesz],
        );
    }
    let (trace, _crossings) = semulith_verify::run::run(&mut env, image.entry, steps);
    let mut out = String::new();
    for (n, s) in trace.steps.iter().enumerate() {
        let name = decode(s.word).map_or("<undecodable>", |insn| insn.name);
        out.push_str(&format!(
            "[{n}] [M]: 0x{:016x} (0x{:08x}) {name}\n",
            s.pc, s.word
        ));
        for (reg, value) in &s.writes {
            out.push_str(&format!("x{reg} <- 0x{value:016x}\n"));
        }
        if let Some((cause, tval)) = s.trap {
            out.push_str(&format!("trap cause=0x{cause:02x} tval=0x{tval:016x}\n"));
        }
    }
    print!("{out}");
    match trace.stop {
        Stop::Budget | Stop::Trap => ExitCode::from(0),
        Stop::FetchFault { at } => {
            eprintln!("run: fetch access fault at {at:#018x}; no observation recorded");
            ExitCode::from(0)
        }
        Stop::Failed(error) => {
            eprintln!("run: model error: {error:?}");
            ExitCode::from(1)
        }
        Stop::Undefined(case) => {
            eprintln!("run: undefined case: {case:?}");
            ExitCode::from(1)
        }
    }
}

fn parse_u64(text: &str) -> Result<u64, std::num::ParseIntError> {
    if let Some(hex) = text.strip_prefix("0x") {
        u64::from_str_radix(hex, 16)
    } else {
        text.parse()
    }
}

fn usage(why: &str) -> ExitCode {
    eprintln!("{why}\n{USAGE}");
    ExitCode::from(2)
}
