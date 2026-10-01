//! The runner: execute one difftest case on the Semulith model and print the canonical
//! end-state dump — the Semulith side of the differential comparison.
//!
//! Usage: `semulith-dsp56300 <guest.lod> <case.meta> [--dump-mem] [--dump-stack]`
//!
//! Exit codes: 0 = the case ran to its stop pc and the dump was printed; 2 = a typed
//! `ModelStop` (an out-of-subset instruction, an out-of-window access, a stack overflow,
//! an exhausted budget, or an unsupported input) — named on stderr, never a guessed
//! behaviour. There is deliberately no exit-1 path: a mismatch is the COMPARATOR's
//! verdict, not the runner's.

use semulith_dsp56300::lod::{load_lod, parse_meta};
use semulith_dsp56300::{dump, exec, Machine, ModelStop};

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let dump_mem = args.iter().any(|a| a == "--dump-mem");
    let dump_stack = args.iter().any(|a| a == "--dump-stack");
    let positional: Vec<&String> = args.iter().filter(|a| !a.starts_with("--")).collect();
    if positional.len() != 2 {
        eprintln!("usage: semulith-dsp56300 <guest.lod> <case.meta> [--dump-mem] [--dump-stack]");
        std::process::exit(2);
    }
    match run(positional[0], positional[1], dump_mem, dump_stack) {
        Ok(dump_text) => print!("{dump_text}"),
        Err(stop) => {
            eprintln!("model stop: {stop}");
            std::process::exit(2);
        }
    }
}

fn run(
    lod_path: &str,
    meta_path: &str,
    dump_mem: bool,
    dump_stack: bool,
) -> Result<String, ModelStop> {
    let lod = std::fs::read_to_string(lod_path)
        .map_err(|e| ModelStop::Input(format!("cannot read {lod_path}: {e}")))?;
    let meta = std::fs::read_to_string(meta_path)
        .map_err(|e| ModelStop::Input(format!("cannot read {meta_path}: {e}")))?;
    let case = parse_meta(&meta)?;

    let mut m = Machine::new();
    load_lod(&mut m, &lod)?;
    let init = m.reset_image();
    m.pc = case.load;

    while m.pc != case.stop {
        if m.steps >= case.budget {
            return Err(ModelStop::BudgetExhausted {
                budget: case.budget,
            });
        }
        exec::step(&mut m)?;
        m.steps += 1;
    }

    let mut out = format!("case {}\n", case.name);
    dump::dump_registers(&mut out, &m);
    if dump_mem {
        dump::dump_memory_deviations(&mut out, &m, &init);
    }
    if dump_stack {
        dump::dump_stack_deviations(&mut out, &m);
    }
    out.push_str("end\n");
    Ok(out)
}
