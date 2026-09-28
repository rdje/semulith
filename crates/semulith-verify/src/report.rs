//! The demo and bench report — `LAB-BENCH.1`: run a tracked guest under a named mutation,
//! judge the trace against the pinned GUEST-GEN expectations, and (unless the model is the
//! real one) name the first divergence against the clean run. One serialization serves the
//! CLI (`semulith demo --json`) and the browser bench (the wasm export returns the same
//! bytes); presentation stays on each surface.
//!
//! The judgement here is the `.9` suite's anchor made reusable: step count, per-step writes,
//! and the `never_written` negative observations, re-derived from the generated fixture the
//! commit gate already tests — this module adds no new expectations of its own.

use crate::fixtures::FlatMemory;
use crate::guests::{Guest, GUESTS};
use crate::mutate::{self, table_for, MUTATIONS};
use crate::run::{compare, run, run_over, Divergence, Stop, Trace, Verdict};
use semulith_core::definition::decode;
use semulith_core::env::Request;

/// One reported run: the trace, its stop, the expectation verdict, the crossing-census
/// verdict, and — for mutated models — the first divergence against the clean run.
///
/// The two verdicts are deliberately separate: the phantom-load arm keeps the architectural
/// expectations (the trace agrees) while breaking the census — a detector that conflated them
/// could not tell that story.
#[derive(Debug)]
pub struct GuestRun {
    pub guest: &'static str,
    pub mutation: &'static str,
    pub entry: u64,
    pub trace: Trace,
    /// Data (non-fetch) boundary crossings — the census the phantom-load arm must move even
    /// though the architectural trace does not.
    pub data_crossings: usize,
    /// What [`mutate::pinned_census`] declares for this guest.
    pub census_pinned: usize,
    pub census_met: bool,
    pub expectations_met: bool,
    pub divergence: Option<Divergence>,
}

/// Run a tracked guest under a named [`MUTATIONS`] model over the laboratory fixture, and
/// judge it. `Err` names an unknown guest or mutation.
pub fn run_guest(guest_name: &str, mutation_name: &str) -> Result<GuestRun, String> {
    let guest = GUESTS
        .iter()
        .find(|g| g.name == guest_name)
        .ok_or_else(|| format!("unknown guest '{guest_name}'"))?;
    let mutation: &'static str = MUTATIONS
        .iter()
        .find(|(name, _)| *name == mutation_name)
        .map(|(name, _)| *name)
        .ok_or_else(|| format!("unknown mutation '{mutation_name}'"))?;
    let table = table_for(mutation).expect("MUTATIONS names are table_for's domain");
    let mut env = FlatMemory::new(guest.entry, 0x10000);
    load_image(&mut env, guest);
    let (trace, crossings) = run_over(&mut env, guest.entry, guest.executed_steps, &table);
    let data_crossings = crossings
        .iter()
        .filter(|c| !matches!(c.request, Request::Fetch { .. }))
        .count();
    let census_pinned = mutate::pinned_census(guest.name).len();
    let census_met = data_crossings == census_pinned;
    let expectations_met = check_expectations(guest, &trace);
    let divergence = if mutation_name == "none" {
        None
    } else {
        let mut clean_env = FlatMemory::new(guest.entry, 0x10000);
        load_image(&mut clean_env, guest);
        let (clean, _) = run(&mut clean_env, guest.entry, guest.executed_steps);
        match compare(&clean.steps, &trace.steps, ("clean", mutation_name)) {
            Ok(Verdict::Divergence(d)) => Some(d),
            Ok(_) => None,
            Err(_) => None,
        }
    };
    Ok(GuestRun {
        guest: guest.name,
        mutation,
        entry: guest.entry,
        trace,
        data_crossings,
        census_pinned,
        census_met,
        expectations_met,
        divergence,
    })
}

fn load_image(env: &mut FlatMemory, guest: &Guest) {
    let mut image = Vec::with_capacity(guest.words.len() * 4);
    for word in guest.words {
        image.extend_from_slice(&word.to_le_bytes());
    }
    env.load_image(0, &image);
}

/// The `.9` suite's GREEN anchor, reusable: the trace runs exactly the declared step count,
/// every step's writes match the specification-derived expectations, and no `never_written`
/// register was written.
fn check_expectations(guest: &Guest, trace: &Trace) -> bool {
    if trace.steps.len() != guest.executed_steps {
        return false;
    }
    for (i, expected) in guest.expected.iter().enumerate() {
        if trace.steps[i].writes != expected.writes {
            return false;
        }
    }
    let written: Vec<u8> = trace
        .steps
        .iter()
        .flat_map(|s| s.writes.iter().map(|(r, _)| *r))
        .collect();
    guest.never_written.iter().all(|reg| !written.contains(reg))
}

/// Serialize a run as JSON — the one shape the CLI and the wasm bench share. Hand-rolled:
/// the verify crate carries no dependencies, and the shape is small and fixed.
#[must_use]
pub fn to_json(run: &GuestRun) -> String {
    let mut out = String::with_capacity(1024);
    out.push_str("{\"guest\":\"");
    out.push_str(run.guest);
    out.push_str("\",\"mutation\":\"");
    out.push_str(run.mutation);
    out.push_str("\",\"entry\":\"0x");
    out.push_str(&format!("{:016x}", run.entry));
    out.push_str("\",\"data_crossings\":");
    out.push_str(&run.data_crossings.to_string());
    out.push_str(",\"data_crossings_pinned\":");
    out.push_str(&run.census_pinned.to_string());
    out.push_str(",\"census_met\":");
    out.push_str(if run.census_met { "true" } else { "false" });
    out.push_str(",\"expectations_met\":");
    out.push_str(if run.expectations_met {
        "true"
    } else {
        "false"
    });
    out.push_str(",\"stop\":");
    push_stop(&mut out, &run.trace.stop);
    out.push_str(",\"divergence\":");
    match &run.divergence {
        Some(d) => {
            out.push_str("{\"at\":");
            out.push_str(&d.at.to_string());
            out.push_str(",\"what\":\"");
            push_escaped(&mut out, &d.what);
            out.push_str("\"}");
        }
        None => out.push_str("null"),
    }
    out.push_str(",\"trace\":[");
    for (n, step) in run.trace.steps.iter().enumerate() {
        if n > 0 {
            out.push(',');
        }
        let insn = decode(step.word).map_or("<undecodable>", |i| i.name);
        out.push_str("{\"n\":");
        out.push_str(&n.to_string());
        out.push_str(",\"pc\":\"0x");
        out.push_str(&format!("{:016x}", step.pc));
        out.push_str("\",\"word\":\"0x");
        out.push_str(&format!("{:08x}", step.word));
        out.push_str("\",\"insn\":\"");
        out.push_str(insn);
        out.push_str("\",\"writes\":[");
        for (i, (reg, value)) in step.writes.iter().enumerate() {
            if i > 0 {
                out.push(',');
            }
            out.push_str(&format!("[{reg},\"0x{value:016x}\"]"));
        }
        out.push_str("],\"trap\":");
        match step.trap {
            Some((cause, tval)) => {
                out.push_str(&format!(
                    "{{\"cause\":\"0x{cause:02x}\",\"tval\":\"0x{tval:016x}\"}}"
                ));
            }
            None => out.push_str("null"),
        }
        out.push('}');
    }
    out.push_str("]}");
    out
}

fn push_stop(out: &mut String, stop: &Stop) {
    match stop {
        Stop::Budget => out.push_str("{\"kind\":\"budget\"}"),
        Stop::Trap => out.push_str("{\"kind\":\"trap\"}"),
        Stop::FetchFault { at } => {
            out.push_str(&format!(
                "{{\"kind\":\"fetch_fault\",\"at\":\"0x{at:016x}\"}}"
            ));
        }
        Stop::Failed(error) => {
            out.push_str("{\"kind\":\"failed\",\"error\":\"");
            push_escaped(out, &format!("{error:?}"));
            out.push_str("\"}");
        }
        Stop::Undefined(case) => {
            out.push_str("{\"kind\":\"undefined\",\"case\":\"");
            push_escaped(out, &format!("{case:?}"));
            out.push_str("\"}");
        }
    }
}

fn push_escaped(out: &mut String, text: &str) {
    for ch in text.chars() {
        match ch {
            '"' => out.push_str("\\\""),
            '\\' => out.push_str("\\\\"),
            c if (c as u32) < 0x20 => out.push_str(&format!("\\u{:04x}", c as u32)),
            c => out.push(c),
        }
    }
}

#[cfg(test)]
mod tests;
