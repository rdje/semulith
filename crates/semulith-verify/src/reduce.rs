//! The minimizer — `P1-LAB.10`, task card T008 (EVD-02's minimized discrepancy form:
//! "every later difference may be a consequence of the first", so the retained artifact is
//! the smallest input that still produces the ORIGINAL first divergence). P2 consumes this
//! directly ("retain minimized discrepancies").
//!
//! The input domain is the guest word sequence: ILEN is 32 for this profile, so one word
//! is exactly one observation step, and a program is a `&[u32]`. The property under test
//! is the differential's: run the model under test and the reference over the candidate
//! and ask [`run::compare`] for the first divergence. **Retention is the original
//! divergence exactly** — same step, same field description. Same-step retention makes
//! the whole divergence byte-identical (the executed prefix is unchanged, so pc, values
//! and tval come along); a removal that merely shifts the divergence or changes its field
//! is correctly rejected, not mistaken for the retained case.
//!
//! The algorithm is classic delta debugging (ddmin, Zeller & Hildebrandt): partition the
//! remaining words into chunks, try removing each chunk, keep a removal only while the
//! property retains, shrink the chunks when no removal does. Every accepted removal
//! preserves the property by construction, so the result **always** retains the original
//! divergence — the invariant is structural, not hoped for, and [`Reduction::retained`]
//! is re-derived from the final words rather than assumed.
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

/// Runaway guard for the candidate-evaluation loop. The tracked guests are ≤ 13 words, so
/// ddmin finishes in tens of evaluations; the cap exists so a pathological future input
/// bounds its own cost. Hitting it is not an error: every accepted removal preserved the
/// property, so the current candidate retains regardless of why the loop stopped.
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
