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
//! - `semulith demo [--guest NAME] [--mutate NAME] [--json]` — run a tracked guest
//!   under the real or a mutated model (`LAB-BENCH.1`) and print the full
//!   observation trace with the judgement: the pinned expectation verdict, and —
//!   for mutated models — the first divergence against the clean run. Text for
//!   humans; `--json` emits the same shape the browser bench consumes. Exit
//!   codes: 0 — expectations met; 1 — a designated mutant broke them (the
//!   detector working, not an error); 2 — usage or an unknown name.
//! - `semulith bundle --guest NAME [--mutate NAME]` — record the replay bundle
//!   (`P1-LAB.10`): run the guest under the named model and write the input bundle
//!   JSON (algorithm pins, platform, image digest, the recorded event choice, the
//!   step bound, and the recorded result) to stdout. Exit codes: 0 — recorded;
//!   2 — usage or an unknown name.
//! - `semulith replay <file.json>` — re-derive a recorded bundle's result from its
//!   recorded inputs (G-REPLAY). Identity is checked first — definition pins, then
//!   the image digest — and a drifted result is reported at the first differing
//!   observation. Exit codes: 0 — the replay is identical; 1 — a named mismatch or
//!   a refused identity; 2 — usage, unreadable input, or a malformed bundle.
//! - `semulith reduce --guest NAME --mutate NAME` — minimize the guest against the
//!   differential while retaining the original first divergence exactly (EVD-02),
//!   and print the minimized program with its retained divergence. Exit codes:
//!   0 — minimized; 1 — the case has no first-divergence to retain (the census
//!   class: a wrong behaviour observations cannot see); 2 — usage or an unknown
//!   name.

use std::path::{Path, PathBuf};
use std::process::ExitCode;

use semulith_core::definition::{decode, INSNS};
use semulith_verify::elf;
use semulith_verify::fixtures::FlatMemory;
use semulith_verify::graph::{check_bundle, Bundle};
use semulith_verify::json::{self, Json};
use semulith_verify::mutate::{table_for, MUTATIONS};
use semulith_verify::reduce;
use semulith_verify::replay::{Bundle as ReplayBundle, CaseSpec, Replay};
use semulith_verify::report;
use semulith_verify::run::Stop;
use semulith_verify::schema;

const USAGE: &str = "semulith — the laboratory control surface\n\
                     usage: semulith check-examples [--root DIR]\n\
                     \x20       semulith run <elf> [--steps N] [--base ADDR] [--size BYTES]\n\
                     \x20       semulith demo [--guest NAME] [--mutate NAME] [--json]\n\
                     \x20       semulith bundle --guest NAME [--mutate NAME]\n\
                     \x20       semulith replay <file.json>\n\
                     \x20       semulith reduce --guest NAME --mutate NAME\n";

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
        Some("demo") => demo(&args[1..]),
        Some("bundle") => bundle(&args[1..]),
        Some("replay") => replay(&args[1..]),
        Some("reduce") => reduce_cmd(&args[1..]),
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

/// `semulith demo` — run a tracked guest under the real or a mutated model and print the
/// trace with its judgement. The detector's verdicts are the exit code: a mutant that is
/// caught exits 1 on purpose — that is the tool working, not an error.
fn demo(args: &[String]) -> ExitCode {
    let mut guest: Option<&str> = None;
    let mut mutation = "none";
    let mut json_out = false;
    for arg in args {
        if let Some(name) = arg.strip_prefix("--guest=") {
            guest = Some(name);
        } else if let Some(name) = arg.strip_prefix("--mutate=") {
            mutation = name;
        } else if arg == "--json" {
            json_out = true;
        } else if arg.starts_with("--") {
            return usage(&format!("demo: unknown option {arg}"));
        } else {
            return usage("demo: unknown operand (options take --name=value form)");
        }
    }
    let guest = match guest {
        Some(name) => name,
        None => {
            return usage(&format!(
                "demo: --guest is required (one of: {}; mutations: {})",
                semulith_verify::guests::GUESTS
                    .iter()
                    .map(|g| g.name)
                    .collect::<Vec<_>>()
                    .join(", "),
                MUTATIONS
                    .iter()
                    .map(|(name, _)| *name)
                    .collect::<Vec<_>>()
                    .join(", ")
            ))
        }
    };
    let run = match report::run_guest(guest, mutation) {
        Ok(run) => run,
        Err(why) => {
            eprintln!("demo: {why}");
            return usage("demo: see --guest / --mutate");
        }
    };
    if json_out {
        println!("{}", report::to_json(&run));
    } else {
        print!("{}", demo_text(&run));
    }
    if run.expectations_met && run.census_met {
        ExitCode::from(0)
    } else {
        ExitCode::from(1)
    }
}

/// The bundle's model name for a demo-style mutation name: `none` is the production
/// model, everything else publishes as `mutant:<name>`.
fn bundle_model(mutation: &str) -> String {
    if mutation == "none" {
        "production".to_string()
    } else {
        format!("mutant:{mutation}")
    }
}

/// Resolve the tracked guest and mutation names the laboratory commands share.
fn tracked(
    guest_name: Option<&str>,
    mutation: &str,
) -> Result<&'static semulith_verify::guests::Guest, String> {
    let guest_name = guest_name.ok_or_else(|| {
        format!(
            "a --guest is required (one of: {})",
            semulith_verify::guests::GUESTS
                .iter()
                .map(|g| g.name)
                .collect::<Vec<_>>()
                .join(", ")
        )
    })?;
    let guest = semulith_verify::guests::GUESTS
        .iter()
        .find(|g| g.name == guest_name)
        .ok_or_else(|| format!("unknown guest '{guest_name}'"))?;
    if !MUTATIONS.iter().any(|(name, _)| *name == mutation) {
        return Err(format!("unknown mutation '{mutation}'"));
    }
    Ok(guest)
}

fn parse_guest_mutation(
    args: &[String],
    command: &str,
) -> Result<(&'static str, String), ExitCode> {
    let mut guest: Option<&str> = None;
    let mut mutation = "none";
    for arg in args {
        if let Some(name) = arg.strip_prefix("--guest=") {
            guest = Some(name);
        } else if let Some(name) = arg.strip_prefix("--mutate=") {
            mutation = name;
        } else if arg.starts_with("--") {
            return Err(usage(&format!("{command}: unknown option {arg}")));
        } else {
            return Err(usage(&format!(
                "{command}: unknown operand (options take --name=value form)"
            )));
        }
    }
    let guest = match tracked(guest, mutation) {
        Ok(guest) => guest,
        Err(why) => return Err(usage(&format!("{command}: {why}"))),
    };
    Ok((guest.name, mutation.to_string()))
}

/// `semulith bundle` — record the replay bundle for a tracked guest under a named model
/// and write it to stdout.
fn bundle(args: &[String]) -> ExitCode {
    let (guest_name, mutation) = match parse_guest_mutation(args, "bundle") {
        Ok(parsed) => parsed,
        Err(code) => return code,
    };
    let guest = semulith_verify::guests::GUESTS
        .iter()
        .find(|g| g.name == guest_name)
        .expect("tracked() returned a tracked guest");
    let spec = CaseSpec {
        model: bundle_model(&mutation),
        entry: guest.entry,
        base: guest.entry,
        size: 0x1_0000,
        budget: guest.executed_steps,
    };
    match ReplayBundle::record(&spec, guest.words) {
        Ok(bundle) => {
            println!("{}", bundle.to_json());
            ExitCode::from(0)
        }
        Err(why) => {
            eprintln!("bundle: {why}");
            ExitCode::from(2)
        }
    }
}

/// `semulith replay` — re-derive a recorded bundle's result from its recorded inputs.
fn replay(args: &[String]) -> ExitCode {
    let mut file: Option<&str> = None;
    for arg in args {
        if arg.starts_with("--") {
            return usage(&format!("replay: unknown option {arg}"));
        } else if file.is_none() {
            file = Some(arg);
        } else {
            return usage("replay: more than one operand");
        }
    }
    let Some(file) = file else {
        return usage("replay: a bundle file is required");
    };
    let text = match std::fs::read_to_string(file) {
        Ok(text) => text,
        Err(e) => {
            eprintln!("replay: cannot read {file}: {e}");
            return ExitCode::from(2);
        }
    };
    let bundle = match ReplayBundle::parse(&text) {
        Ok(bundle) => bundle,
        Err(why) => {
            eprintln!("replay: {file}: refused — {why}");
            return ExitCode::from(2);
        }
    };
    match bundle.replay() {
        Ok(Replay::Identical) => {
            println!(
                "replay: identical — {} step(s) and the stop '{}' re-derived from the recorded inputs",
                bundle.recorded.steps.len(),
                bundle.recorded.stop
            );
            ExitCode::from(0)
        }
        Ok(Replay::Mismatch(d)) => {
            println!(
                "replay: MISMATCH — recorded vs replay first diverge at aligned step {}: {}",
                d.at, d.what
            );
            ExitCode::from(1)
        }
        Ok(Replay::LengthMismatch { agreed, longer }) => {
            println!(
                "replay: LENGTH MISMATCH after {agreed} agreeing step(s) — {longer} continues; the recorded result does not reproduce"
            );
            ExitCode::from(1)
        }
        Err(why) => {
            println!("replay: refused — {why}");
            ExitCode::from(1)
        }
    }
}

/// `semulith reduce` — minimize a tracked guest against the differential, retaining the
/// original first divergence exactly.
fn reduce_cmd(args: &[String]) -> ExitCode {
    let (guest_name, mutation) = match parse_guest_mutation(args, "reduce") {
        Ok(parsed) => parsed,
        Err(code) => return code,
    };
    let guest = semulith_verify::guests::GUESTS
        .iter()
        .find(|g| g.name == guest_name)
        .expect("tracked() returned a tracked guest");
    let model = table_for(&mutation).expect("tracked() validated the mutation name");
    let case = reduce::Case {
        model: &model,
        reference: INSNS,
        entry: guest.entry,
        region_size: 0x1_0000,
        budget: guest.executed_steps,
    };
    match reduce::reduce(&case, guest.words) {
        Ok(reduction) => {
            println!(
                "reduce: {} under '{}' — {} → {} word(s) in {} evaluation(s)",
                guest.name,
                mutation,
                guest.words.len(),
                reduction.words.len(),
                reduction.evaluations
            );
            println!(
                "retained FIRST DIVERGENCE at aligned step {}: {}",
                reduction.retained.at, reduction.retained.what
            );
            println!("minimized program (entry {:#018x}):", guest.entry);
            for (n, word) in reduction.words.iter().enumerate() {
                println!("  [{n}] 0x{word:08x}");
            }
            ExitCode::from(0)
        }
        Err(reduce::ReduceError::NoDivergence) => {
            eprintln!(
                "reduce: no first-divergence to retain — {} under '{}' agrees on the observations; a census-class wrong behaviour is not reducible on the trace",
                guest.name, mutation
            );
            ExitCode::from(1)
        }
    }
}

/// The human rendering of one judged run: the trace, then the verdict story.
fn demo_text(run: &report::GuestRun) -> String {
    let mut out = format!(
        "== {} under '{}' (entry {:#018x}) ==\n",
        run.guest, run.mutation, run.entry
    );
    for (n, step) in run.trace.steps.iter().enumerate() {
        let name = decode(step.word).map_or("<undecodable>", |insn| insn.name);
        out.push_str(&format!(
            "  [{n}] 0x{:016x} (0x{:08x}) {:<10}",
            step.pc, step.word, name
        ));
        let mut notes = Vec::new();
        for (reg, value) in &step.writes {
            notes.push(format!("x{reg} <- 0x{value:016x}"));
        }
        if let Some((cause, tval)) = step.trap {
            notes.push(format!("trap cause=0x{cause:02x} tval=0x{tval:016x}"));
        }
        if !notes.is_empty() {
            out.push_str("   ");
            out.push_str(&notes.join(";  "));
        }
        out.push('\n');
    }
    out.push_str(&format!(
        "stop: {}   data crossings: {} (census pins {})\n",
        stop_name(&run.trace.stop),
        run.data_crossings,
        run.census_pinned
    ));
    if run.expectations_met {
        out.push_str("verdict: the pinned specification-derived expectations hold");
        if run.census_met {
            out.push_str("; the crossing census agrees\n");
        } else {
            out.push_str(
                "\nverdict: THE CROSSING CENSUS DISAGREES — the trace never betrayed it:\n",
            );
            out.push_str(&format!(
                "  {} data crossing(s) where the guest's source declares {} — an access the architectural observation vocabulary cannot see\n",
                run.data_crossings, run.census_pinned
            ));
        }
    } else {
        out.push_str("verdict: EXPECTATIONS BROKEN — the detector's answer:\n");
        match &run.divergence {
            Some(d) => out.push_str(&format!(
                "  FIRST DIVERGENCE at aligned step {}: {}\n",
                d.at, d.what
            )),
            None => out.push_str(&format!(
                "  the trace still agrees — caught by the crossing census ({} data crossing(s))\n",
                run.data_crossings
            )),
        }
    }
    out
}

fn stop_name(stop: &Stop) -> &'static str {
    match stop {
        Stop::Budget => "budget",
        Stop::Trap => "trap",
        Stop::FetchFault { .. } => "fetch fault",
        Stop::Failed(_) => "model error",
        Stop::Undefined(_) => "undefined case",
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
