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
//! - `semulith run <elf> [--steps N] [--base ADDR] [--size BYTES] [--trace-stores]` —
//!   execute a
//!   freestanding guest under the laboratory environment (`P1-LAB.8`, T006):
//!   load the ELF's PT_LOAD segments into the declared region, run the
//!   definitional interpreter for at most `steps` steps, and print one
//!   normalized observation per step — the same `(pc, word, writes, trap)`
//!   vocabulary `scripts/compare_traces.py` reduces the reference models to,
//!   so every model is compared through the one parser. With `--trace-stores`
//!   the step trace is followed by the run's data-store crossings, one
//!   `mem[W,0xADDR] <- 0xVALUE` line per successful store in execution order
//!   (the runner records every boundary crossing; the flag surfaces them — an
//!   observability option, not a semantics one; a faulted store wrote nothing
//!   and prints nothing, its trap already carried by the step). Exit codes: 0 — the
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
//! - `semulith snapshot <elf> --at N [--steps N] [--base ADDR] [--size BYTES]` —
//!   record the mid-execution state after N steps as a JSON snapshot record
//!   (`P2-SCALAR.7`, G-REPLAY's second half): the definition-identity pins, the
//!   region, the register file and pc, and the memory content sparse-encoded and
//!   digested. The pending-state census (`state.sexp`) measured every hidden-state
//!   candidate absent, so those three ARE the whole pending state for this profile;
//!   anything more is not offered. Exit codes: 0 — recorded; 2 — usage, unreadable
//!   inputs, or the run ended before N.
//! - `semulith resume <file.json>` — resume from a recorded snapshot: identity and
//!   memory digest checked first (a mismatch refuses by name), then the continuation
//!   runs and prints in the `run` trace format. Exit codes: 0 — resumed; 2 — usage,
//!   unreadable input, or a record refused.
//! - `semulith bench [--iterations N] [--reps R] [--warmup W]` — the performance
//!   baseline (`P1-LAB.11`, RUST-04): run the four workload mixes (arithmetic,
//!   control, memory, fault) in ARCHITECTURE §6's three modes (untraced,
//!   instrumented — static and dyn — and diagnostic) on this named host, with
//!   allocation counts, and print the noise table (min/median/max/spread per cell).
//!   RUST-02 is checked as it measures: the modes must agree on every observable or
//!   the run is refused. No regression threshold is set. Exit codes: 0 — measured
//!   and all modes agree; 1 — a mode disagreement (RUST-02 broken); 2 — usage, an
//!   escaped workload, or a harness refusal. This binary installs the counting
//!   allocator (`semulith_verify::bench::alloc`) as its process allocator — two
//!   relaxed atomic adds per allocation for every command, the price of RUST-03
//!   being a number.

use std::path::{Path, PathBuf};
use std::process::ExitCode;
use std::time::Instant;

use semulith_core::definition::{decode, INSNS};
use semulith_verify::bench::{self, Mix, Mode, Stats};
use semulith_verify::elf;

/// The running profile's instruction-address alignment in bits — rv64i-lab-v0 declares
/// (ialign 32). The CLI's definition is rv64i's until the rv64gc route flip
/// (P4-SYSTEM.2 slice h) makes the profile a runtime selection; the constant is the
/// profile's data, passed to the loader rather than assumed by it.
const IALIGN_BITS: u64 = 32;
use semulith_verify::fixtures::FlatMemory;
use semulith_verify::graph::{check_bundle, Bundle};
use semulith_verify::json::{self, Json};
use semulith_verify::mutate::{table_for, MUTATIONS};
use semulith_verify::reduce;
use semulith_verify::replay::{Bundle as ReplayBundle, CaseSpec, Replay};
use semulith_verify::report;
use semulith_verify::run::Stop;
use semulith_verify::schema;
use semulith_verify::snapshot::Snapshot;

const USAGE: &str = "semulith — the laboratory control surface\n\
                     usage: semulith check-examples [--root DIR]\n\
                     \x20       semulith run <elf> [--steps N] [--base ADDR] [--size BYTES] [--trace-stores]\n\
                     \x20       semulith demo [--guest NAME] [--mutate NAME] [--json]\n\
                     \x20       semulith bundle --guest NAME [--mutate NAME]\n\
                     \x20       semulith replay <file.json>\n\
                     \x20       semulith snapshot <elf> --at N [--steps N] [--base ADDR] [--size BYTES]\n\
                     \x20       semulith resume <file.json>\n\
                     \x20       semulith reduce --guest NAME --mutate NAME\n\
                     \x20       semulith bench [--iterations N] [--reps R] [--warmup W]\n";

/// The process-wide counting allocator (`P1-LAB.11`): allocation counts are measured
/// per benchmark cell by resetting around the timed run; for every other command the
/// cost is two relaxed atomic adds per allocation.
#[global_allocator]
static COUNTING: bench::alloc::Counting = bench::alloc::Counting;

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
        Some("snapshot") => snapshot_cmd(&args[1..]),
        Some("resume") => resume_cmd(&args[1..]),
        Some("reduce") => reduce_cmd(&args[1..]),
        Some("bench") => bench_cmd(&args[1..]),
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
    let mut trace_stores = false;
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
        } else if arg == "--trace-stores" {
            trace_stores = true;
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
    let image = match elf::parse(&bytes, IALIGN_BITS) {
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
    let (trace, crossings) = semulith_verify::run::run(&mut env, image.entry, steps);
    let mut out = format_steps(&trace.steps, 0);
    if trace_stores {
        // The store trace (P2-SCALAR.5 strand 2 — the ACT4 campaign's observation):
        // every successful data-store crossing, in execution order, spelled the way
        // sail's `--trace-mem` spells it so one extractor reads both models. A store
        // whose crossing failed (access fault / misaligned) wrote nothing and is absent
        // by construction — its observation is the step's trap line.
        for crossing in &crossings {
            if let semulith_verify::run::Crossing {
                request: semulith_core::env::Request::Store { width, addr, data },
                response: Ok(semulith_core::env::Response::StoreDone),
            } = crossing
            {
                let bytes = width.bytes();
                let masked = if bytes == 8 {
                    *data
                } else {
                    data & ((1 << (bytes * 8)) - 1)
                };
                out.push_str(&format!("mem[{bytes},0x{addr:016x}] <- 0x{masked:016x}\n"));
            }
        }
    }
    print!("{out}");
    match trace.stop {
        Stop::Budget | Stop::Trap => ExitCode::from(0),
        Stop::FetchFault { at } => {
            eprintln!(
                "run: fetch access fault at {at:#018x} (the final step carries the trap and no word)"
            );
            ExitCode::from(0)
        }
        Stop::Failed(error) => {
            eprintln!("run: model error: {error:?}");
            ExitCode::from(1)
        }
        Stop::Undefined(case) => {
            // The laboratory's D-RESERVED-DECODE policy converted the case into the
            // trace's final trap observation; the run did everything the profile
            // declares. The report keeps the case's source classification (SEM-07).
            eprintln!(
                "run: undefined case reported under the laboratory's reserved-decode policy: {case:?}"
            );
            ExitCode::from(0)
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

/// The one step-printing shape — the normalized observation vocabulary both `run` and
/// `resume` print (`resume` continues the step numbering at the snapshot's index).
fn format_steps(steps: &[semulith_verify::run::Step], first: usize) -> String {
    let mut out = String::new();
    for (i, s) in steps.iter().enumerate() {
        let n = first + i;
        match s.word {
            Some(word) => {
                let name = decode(word).map_or("<undecodable>", |insn| insn.name);
                out.push_str(&format!(
                    "[{n}] [M]: 0x{:016x} (0x{word:08x}) {name}\n",
                    s.pc
                ));
            }
            // The fetch-fault step: no word was fetched, so none is printed.
            None => out.push_str(&format!("[{n}] [M]: 0x{:016x} (fetch fault)\n", s.pc)),
        }
        for (reg, value) in &s.writes {
            out.push_str(&format!("x{reg} <- 0x{value:016x}\n"));
        }
        if let Some((cause, tval)) = s.trap {
            out.push_str(&format!("trap cause=0x{cause:02x} tval=0x{tval:016x}\n"));
        }
    }
    out
}

/// `semulith snapshot` — record the mid-execution state after `--at N` steps of a guest
/// ELF as a JSON snapshot record on stdout (`P2-SCALAR.7`). The record carries the whole
/// pending state this profile has — registers, pc, memory (the pinned hidden-state
/// census admits nothing else) — plus the definition identity pins.
fn snapshot_cmd(args: &[String]) -> ExitCode {
    let mut elf_path: Option<&str> = None;
    let mut steps = DEFAULT_STEPS;
    let mut at: Option<usize> = None;
    let mut base = DEFAULT_BASE;
    let mut size = DEFAULT_SIZE;
    for arg in args {
        if let Some(n) = arg.strip_prefix("--steps=") {
            steps = match n.parse() {
                Ok(v) => v,
                Err(_) => return usage("snapshot: --steps wants an integer"),
            };
        } else if let Some(n) = arg.strip_prefix("--at=") {
            at = match n.parse() {
                Ok(v) => Some(v),
                Err(_) => return usage("snapshot: --at wants an integer"),
            };
        } else if let Some(v) = arg.strip_prefix("--base=") {
            base = match parse_u64(v) {
                Ok(v) => v,
                Err(_) => return usage("snapshot: --base wants an address"),
            };
        } else if let Some(v) = arg.strip_prefix("--size=") {
            size = match parse_u64(v) {
                Ok(v) => v,
                Err(_) => return usage("snapshot: --size wants a byte count"),
            };
        } else if arg.starts_with("--") {
            return usage(&format!("snapshot: unknown option {arg}"));
        } else if elf_path.is_none() {
            elf_path = Some(arg);
        } else {
            return usage("snapshot: more than one ELF operand");
        }
    }
    let Some(elf_path) = elf_path else {
        return usage("snapshot: an ELF operand is required");
    };
    let Some(at) = at else {
        return usage("snapshot: --at N is required — the snapshot point");
    };
    if at > steps {
        return usage("snapshot: --at exceeds --steps — the run never reaches the point");
    }
    let bytes = match std::fs::read(elf_path) {
        Ok(b) => b,
        Err(e) => {
            eprintln!("snapshot: cannot read {elf_path}: {e}");
            return ExitCode::from(2);
        }
    };
    let image = match elf::parse(&bytes, IALIGN_BITS) {
        Ok(image) => image,
        Err(why) => {
            eprintln!("snapshot: {elf_path}: refused — {why}");
            return ExitCode::from(2);
        }
    };
    let Some(top) = base.checked_add(size) else {
        eprintln!("snapshot: the region [{base:#018x}, +{size:#x}) wraps the address space");
        return ExitCode::from(2);
    };
    let mut env = FlatMemory::new(base, size as usize);
    for seg in &image.segments {
        let seg_end = seg.paddr.saturating_add(seg.memsz);
        if seg.paddr < base || seg_end > top {
            eprintln!(
                "snapshot: segment at {:#018x} ({} byte(s)) lies outside the declared region [{:#018x}, {:#018x})",
                seg.paddr, seg.memsz, base, top
            );
            return ExitCode::from(2);
        }
        env.load_image(
            (seg.paddr - base) as usize,
            &bytes[seg.offset..seg.offset + seg.filesz],
        );
    }
    let (trace, _crossings, state) = semulith_verify::run::run_state(
        &mut env,
        semulith_core::state::ArchitecturalState::zeroed_at(image.entry),
        at,
    );
    if trace.steps.len() < at {
        eprintln!(
            "snapshot: the run ended at step {} ({:?}) before the snapshot point {at} —              there is no mid-execution state there",
            trace.steps.len(),
            trace.stop
        );
        return ExitCode::from(2);
    }
    let snap = Snapshot::capture(&env, &state, base, size, image.entry, at, steps);
    println!("{}", snap.to_json());
    ExitCode::from(0)
}

/// `semulith resume` — resume from a recorded snapshot: identity and memory digest
/// checked first (a mismatch refuses by name, never a mis-replay), then the continuation
/// runs and prints in the `run` trace format, numbered from the snapshot's step.
fn resume_cmd(args: &[String]) -> ExitCode {
    let mut file: Option<&str> = None;
    for arg in args {
        if arg.starts_with("--") {
            return usage(&format!("resume: unknown option {arg}"));
        } else if file.is_none() {
            file = Some(arg);
        } else {
            return usage("resume: more than one operand");
        }
    }
    let Some(file) = file else {
        return usage("resume: a snapshot file is required");
    };
    let text = match std::fs::read_to_string(file) {
        Ok(text) => text,
        Err(e) => {
            eprintln!("resume: cannot read {file}: {e}");
            return ExitCode::from(2);
        }
    };
    let snap = match Snapshot::parse(&text) {
        Ok(snap) => snap,
        Err(why) => {
            eprintln!("resume: {file}: refused — {why}");
            return ExitCode::from(2);
        }
    };
    match snap.resume() {
        Ok(resumed) => {
            print!("{}", format_steps(&resumed.trace.steps, snap.at_step));
            eprintln!(
                "resume: {} continuation step(s) from step {}, stop {:?}",
                resumed.trace.steps.len(),
                snap.at_step,
                resumed.trace.stop
            );
            ExitCode::from(0)
        }
        Err(why) => {
            eprintln!("resume: {file}: refused — {why}");
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

/// One measured cell: a mix in a mode — the noise summary, the per-step allocation
/// counts, and the last run's facts (kept for the cross-mode agreement check).
struct Cell {
    mode: Mode,
    stats: Stats,
    allocations: usize,
    bytes: usize,
    run: bench::ModeRun,
}

/// The host this baseline was measured on, named as the leaf requires: CPU brand where
/// the platform supplies one, kernel, and the rustc that built the binary. Best-effort
/// probes; a missing probe degrades the string, never the run.
fn host_identity() -> String {
    let probe = |program: &str, args: &[&str]| -> Option<String> {
        let out = std::process::Command::new(program)
            .args(args)
            .output()
            .ok()?;
        if !out.status.success() {
            return None;
        }
        let text = String::from_utf8_lossy(&out.stdout).trim().to_string();
        (!text.is_empty()).then_some(text)
    };
    let cpu = probe("sysctl", &["-n", "machdep.cpu.brand_string"])
        .or_else(|| probe("sysctl", &["-n", "hw.model"]))
        .unwrap_or_else(|| std::env::consts::ARCH.to_string());
    let kernel = probe("uname", &["-sr"]).unwrap_or_else(|| std::env::consts::OS.to_string());
    let rustc = probe("rustc", &["--version"]).unwrap_or_else(|| "rustc unknown".to_string());
    format!("{cpu}; {kernel}; {rustc}")
}

/// `semulith bench` — the performance baseline. Measures every mix in every mode with
/// warmup + repeated reps, checks RUST-02 (the modes must agree on every observable) as
/// it measures, and prints the noise table. No threshold is set: RUST-04 requires the
/// noise to be characterized first, and this report is that characterization.
fn bench_cmd(args: &[String]) -> ExitCode {
    let mut iterations = 10000u32;
    let mut reps = 12usize;
    let mut warmup = 2usize;
    for arg in args {
        if let Some(n) = arg.strip_prefix("--iterations=") {
            match n.parse::<u32>() {
                Ok(v) if (1..=bench::MAX_ITERATIONS).contains(&v) => iterations = v,
                _ => {
                    return usage(&format!(
                        "bench: --iterations wants 1..={}",
                        bench::MAX_ITERATIONS
                    ))
                }
            }
        } else if let Some(n) = arg.strip_prefix("--reps=") {
            match n.parse() {
                Ok(v) if v > 0 => reps = v,
                _ => return usage("bench: --reps wants a positive integer"),
            }
        } else if let Some(n) = arg.strip_prefix("--warmup=") {
            match n.parse() {
                Ok(v) => warmup = v,
                _ => return usage("bench: --warmup wants an integer"),
            }
        } else {
            return usage(&format!("bench: unknown option {arg}"));
        }
    }

    println!("semulith bench — the performance baseline (P1-LAB.11)");
    println!("host: {}", host_identity());
    println!(
        "config: iterations={iterations}, warmup={warmup}, reps={reps}; wall-clock per run (std::time::Instant); allocations via the process-wide counting allocator"
    );
    println!(
        "noise: spread = (max\u{2212}min)/median over the reps, characterized BEFORE any threshold (RUST-04) — no regression threshold is set or implied by this report"
    );

    let mut broken = false;
    for mix in Mix::ALL {
        let budget = bench::budget_for(mix, iterations);
        let mut cells: Vec<Cell> = Vec::new();
        for mode in Mode::ALL {
            let mut samples: Vec<u64> = Vec::with_capacity(reps);
            let mut allocations = 0;
            let mut bytes = 0;
            let mut last_run: Option<bench::ModeRun> = None;
            for rep in 0..(warmup + reps) {
                let (mut env, words) = bench::prepare(mix, iterations);
                bench::alloc::reset();
                let start = Instant::now();
                let run = match bench::run_mode(mode, &mut env, &words, budget) {
                    Ok(run) => run,
                    Err(why) => {
                        eprintln!("bench: {} / {}: {}", mix.name(), mode.name(), why.0);
                        return ExitCode::from(2);
                    }
                };
                let elapsed = start.elapsed();
                let counted = bench::alloc::counts();
                if run.facts.stop != Stop::Trap {
                    eprintln!(
                        "bench: {} / {} did not terminate on its trap (stop: {:?}) — the workload escaped its loop, a bench defect",
                        mix.name(),
                        mode.name(),
                        run.facts.stop
                    );
                    return ExitCode::from(2);
                }
                if rep >= warmup {
                    samples.push(u64::try_from(elapsed.as_nanos()).unwrap_or(u64::MAX));
                    allocations = counted.0;
                    bytes = counted.1;
                }
                last_run = Some(run);
            }
            cells.push(Cell {
                mode,
                stats: bench::stats(&samples),
                allocations,
                bytes,
                run: last_run.expect("reps > 0, so a run exists"),
            });
        }

        // RUST-02, checked as we measure: the untraced facts against every traced mode,
        // and the recorded streams identical among the traced modes.
        let pivot = &cells[0];
        for cell in &cells[1..] {
            if let Err(why) =
                bench::agree(&pivot.run, &cell.run, (pivot.mode.name(), cell.mode.name()))
            {
                println!(
                    "  RUST-02 DISAGREEMENT in {}: {} vs {} — {why}",
                    mix.name(),
                    pivot.mode.name(),
                    cell.mode.name()
                );
                broken = true;
            }
        }
        if let Err(why) = bench::agree(&cells[1].run, &cells[2].run, ("static", "dyn")) {
            println!(
                "  RUST-02 DISAGREEMENT in {}: static vs dyn — {why}",
                mix.name()
            );
            broken = true;
        }
        if let Err(why) = bench::agree(&cells[2].run, &cells[3].run, ("dyn", "diagnostic")) {
            println!(
                "  RUST-02 DISAGREEMENT in {}: dyn vs diagnostic — {why}",
                mix.name()
            );
            broken = true;
        }

        let facts = &cells[0].run.facts;
        let census = facts.census;
        println!(
            "\nmix: {} — {} steps; census: {} fetches, {} loads, {} stores, {} faults",
            mix.name(),
            facts.steps,
            census.fetches,
            census.loads,
            census.stores,
            census.faults
        );
        println!(
            "  {:<19} {:>10} {:>10} {:>10} {:>8} {:>13} {:>11}",
            "mode", "ns/step", "min", "max", "spread", "allocs/step", "bytes/step"
        );
        for cell in &cells {
            let steps = cell.run.facts.steps as f64;
            println!(
                "  {:<19} {:>10.1} {:>10.1} {:>10.1} {:>7.2}% {:>13.2} {:>11.1}",
                cell.mode.name(),
                cell.stats.median as f64 / steps,
                cell.stats.min as f64 / steps,
                cell.stats.max as f64 / steps,
                cell.stats.spread_ppm as f64 / 10_000.0,
                cell.allocations as f64 / steps,
                cell.bytes as f64 / steps,
            );
        }
        let ratio = cells[2].stats.median as f64 / cells[1].stats.median.max(1) as f64;
        println!(
            "  static vs dynamic observer dispatch: \u{d7}{ratio:.3} (instrumented vs instrumented (dyn), medians)"
        );
        if broken {
            println!("  agreement: BROKEN — see above");
        } else {
            println!(
                "  agreement: OK — all modes agree on steps, stop, final state and census; every recorded observation stream is identical (RUST-02)"
            );
        }
    }

    if broken {
        println!("\nbench: RUST-02 BROKEN — a traced run changed the observations");
        ExitCode::from(1)
    } else {
        println!("\nbench: measured; every mode agrees on every mix (RUST-02 holds)");
        ExitCode::from(0)
    }
}

/// The human rendering of one judged run: the trace, then the verdict story.
fn demo_text(run: &report::GuestRun) -> String {
    let mut out = format!(
        "== {} under '{}' (entry {:#018x}) ==\n",
        run.guest, run.mutation, run.entry
    );
    for (n, step) in run.trace.steps.iter().enumerate() {
        match step.word {
            Some(word) => {
                let name = decode(word).map_or("<undecodable>", |insn| insn.name);
                out.push_str(&format!(
                    "  [{n}] 0x{:016x} (0x{word:08x}) {:<10}",
                    step.pc, name
                ));
            }
            // The fetch-fault step carries no word.
            None => out.push_str(&format!("  [{n}] 0x{:016x} (fetch fault)  ", step.pc)),
        }
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
