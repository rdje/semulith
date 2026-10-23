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

/// Property-evaluation budget, including original and final verification. Accepted
/// removals retain the original property even when the search stops early.
const EVALUATION_CAP: usize = 100_000;

/// The differential under reduction: the model under test (e.g. a `.9` mutant table) and
/// the reference it is compared against (production `INSNS`), plus the laboratory
/// platform facts the run needs.
pub struct Case<'a> {
    /// The instruction table under test.
    pub model: &'a [InsnDef],
    /// The instruction table it is compared against.
    pub reference: &'a [InsnDef],
    /// The entry point address.
    pub entry: u64,
    /// The size of the laboratory memory region, in bytes.
    pub region_size: usize,
    /// The step budget of each run.
    pub budget: usize,
}

/// A retaining artifact: the divergence re-derived from the retained words,
/// and how many candidate evaluations the search spent.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Reduction {
    /// The retained instruction words.
    pub words: Vec<u32>,
    /// The divergence those words still produce.
    pub retained: Divergence,
    /// Candidate evaluations the search spent.
    pub evaluations: usize,
    /// A complete single-word deletion pass found no retaining deletion. A capped
    /// search has no such witness; neither result claims a global minimum.
    pub one_minimal: bool,
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
    reduce_by(words, EVALUATION_CAP, |candidate| {
        divergence(case, candidate)
    })
}

// The property is injected only to test the search budget independently of CPU
// execution cost. Production always uses the exact differential above.
fn reduce_by(
    words: &[u32],
    evaluation_limit: usize,
    mut observe: impl FnMut(&[u32]) -> Option<Divergence>,
) -> Result<Reduction, ReduceError> {
    assert!(
        evaluation_limit >= 2,
        "reserve original and final evaluations"
    );
    if words.is_empty() {
        return Err(ReduceError::NoDivergence);
    }
    let original = observe(words).ok_or(ReduceError::NoDivergence)?;
    let mut current: Vec<u32> = words.to_vec();
    let mut evaluations = 1;
    let mut chunks = 2usize;
    let mut one_minimal = false;
    'search: loop {
        let width = current.len().div_ceil(chunks);
        let mut removed = false;
        let mut start = 0;
        while start < current.len() {
            if evaluations >= evaluation_limit - 1 {
                break 'search; // reserve the final retention verification
            }
            let end = (start + width).min(current.len());
            let candidate: Vec<u32> = current[..start]
                .iter()
                .chain(&current[end..])
                .cloned()
                .collect();
            evaluations += 1;
            let found = observe(&candidate);
            if !candidate.is_empty() && found.as_ref() == Some(&original) {
                current = candidate;
                chunks = chunks.saturating_sub(1).max(2);
                removed = true;
                break;
            }
            start = end;
        }
        if !removed {
            if width == 1 {
                one_minimal = true;
                break; // no single-word removal retains: the candidate is 1-minimal
            }
            chunks = (chunks * 2).min(current.len());
        }
    }
    evaluations += 1;
    let retained =
        observe(&current).expect("the invariant: only retaining candidates were accepted");
    assert_eq!(retained, original, "final verification must retain exactly");
    Ok(Reduction {
        words: current,
        retained,
        evaluations,
        one_minimal,
    })
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
