//! The scalar minimizer — `P1-LAB.10`, task card T008. It implements the
//! replay/reduction retention check in `docs/EVIDENCE_AND_GATES.md` §6.
//!
//! The deletion domain is the guest's fixed-width u32 image encodings. Dynamic
//! execution can revisit or skip words: a word count is not a step count. Each
//! candidate reruns both tables with the same entry, memory size and step budget.
//! Retention is exact equality of the original [`run::Divergence`]: the aligned
//! step and the complete formatted field description, including reported values.
//! The reducer does not infer an unchanged execution prefix from the step index.
//!
//! Delta debugging removes chunks only when that property retains. The final
//! witness is re-derived from the retained words. A completed single-word deletion
//! pass establishes 1-minimality in this deletion domain, not a global minimum.
//!
//! Named boundary: a case whose observations do not first-diverge has nothing to retain
//! and is refused [`ReduceError::NoDivergence`] — the `.9` suite's phantom-load arm is
//! the standing example (the architectural trace *agrees*; only the crossing census sees
//! the wrong behaviour). Observation reduction cannot retain what observations do not
//! carry; census-class wrong behaviour reduces on the census, not on the trace.

use semulith_core::definition::InsnDef;

use crate::fixtures::FlatMemory;
use crate::replay::image_bytes;
use crate::run::{self, Divergence, Trace};

/// Runaway guard for the outer candidate-evaluation loop. Guest sizes vary;
/// accepted removals retain the original property even if the search stops early.
const EVALUATION_CAP: usize = 100_000;

/// The differential under reduction: the model under test (e.g. a `.9` mutant table) and
/// the reference it is compared against (production `INSNS`), plus the laboratory
/// platform facts the run needs.
pub struct Case<'a> {
    pub model: &'a [InsnDef],
    pub reference: &'a [InsnDef],
    pub entry: u64,
    pub region_size: usize,
    pub budget: usize,
}

/// The minimized artifact: the retained divergence, re-derived from the minimized words,
/// and how many candidate evaluations the search spent.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Reduction {
    pub words: Vec<u32>,
    pub retained: Divergence,
    pub evaluations: usize,
}

/// Why a reduction could not run.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum ReduceError {
    /// The original input has no first-divergence to retain (the traces agree, or one
    /// side could not run) — nothing to minimize. Census-class wrong behaviour (the
    /// phantom-load arm) lands here by design: the observation vocabulary cannot see it.
    NoDivergence,
}

/// Minimize `words` against the case's differential, retaining the original first
/// divergence exactly. Returns the minimized words with the divergence re-derived from
/// them. `Err` when the original input does not first-diverge.
pub fn reduce(case: &Case, words: &[u32]) -> Result<Reduction, ReduceError> {
    let original = divergence(case, words).ok_or(ReduceError::NoDivergence)?;
    let mut current: Vec<u32> = words.to_vec();
    let mut evaluations = 1;
    let mut chunks = 2usize;
    while current.len() >= 2 && evaluations < EVALUATION_CAP {
        let width = current.len().div_ceil(chunks);
        let mut removed = false;
        let mut start = 0;
        while start < current.len() {
            let end = (start + width).min(current.len());
            let candidate: Vec<u32> = current[..start]
                .iter()
                .chain(&current[end..])
                .cloned()
                .collect();
            evaluations += 1;
            if retains(case, &candidate, &original) {
                current = candidate;
                chunks = chunks.saturating_sub(1).max(2);
                removed = true;
                break;
            }
            start = end;
        }
        if !removed {
            if width == 1 {
                break; // no single-word removal retains: the candidate is 1-minimal
            }
            chunks = (chunks * 2).min(current.len());
        }
    }
    let retained =
        divergence(case, &current).expect("the invariant: only retaining candidates were accepted");
    Ok(Reduction {
        words: current,
        retained,
        evaluations,
    })
}

/// Does the candidate still produce the original first divergence — same step, same
/// field description?
fn retains(case: &Case, candidate: &[u32], original: &Divergence) -> bool {
    match divergence(case, candidate) {
        Some(d) => d == *original,
        None => false,
    }
}

/// The candidate's first divergence between the reference and the model under test, in
/// the fixed report naming the retention comparison uses.
fn divergence(case: &Case, words: &[u32]) -> Option<Divergence> {
    if words.is_empty() {
        return None;
    }
    let model = trace(case, case.model, words);
    let reference = trace(case, case.reference, words);
    match run::compare(&reference.steps, &model.steps, ("reference", "model")) {
        Ok(run::Verdict::Divergence(d)) => Some(d),
        _ => None,
    }
}

fn trace(case: &Case, table: &[InsnDef], words: &[u32]) -> Trace {
    let mut env = FlatMemory::new(case.entry, case.region_size);
    env.load_image(0, &image_bytes(words));
    run::run_over(&mut env, case.entry, case.budget, table).0
}

#[cfg(test)]
mod tests;
