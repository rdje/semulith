//! Bounded, mixed-width RV64GC reduction (P4-SYSTEM.16).
//!
//! The deletion domain is two-byte image chunks, plus a final single data byte if
//! present. These are encoding boundaries, not dynamic instruction observations.
//! Each candidate runs both complete tables from cold reset under the same budget
//! and typed fault policy. Retention means the exact original first paired step
//! difference: its index and both complete PC/mode/GPR-change observations.
//! This is the replay/reduction check in `docs/EVIDENCE_AND_GATES.md` §6, not
//! independent evidence that either model implements the ISA correctly.

use semulith_core::state_rv64gc::ArchitecturalState;

use crate::fixtures::FlatMemory;
use crate::guests_rv64gc::Refusal;
use crate::json::{self, Json};
use crate::model_rv64gc::Model;
use crate::replay::int_usize;
use crate::replay_rv64gc::{BundleRv64gc, ReplayRv64gc};
use crate::run_rv64gc::{self, Step, Trace};
use crate::sha256::sha256_hex;
use crate::snapshot_rv64gc::{check_json_limits, SnapshotRv64gc};

const FORMAT: &str = "semulith-rv64gc-reduction-v1";
/// Reduction is deliberately narrower than general snapshot/replay.
pub const MEMORY_BYTES: usize = 64 * 1024;
pub const MAX_STEPS: usize = 1000;
/// Includes the original property evaluation and a reserved final verification.
pub const MAX_EVALUATIONS: usize = 512;
pub const MAX_JSON_BYTES: usize = 16 * 1024 * 1024;

pub struct Case<'a> {
    pub entry: u64,
    pub budget: usize,
    pub refusals: &'a [Refusal],
    pub model: Model,
    pub evaluation_limit: usize,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Difference {
    pub at: usize,
    pub reference: Step,
    pub model: Step,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Reduction {
    pub image: Vec<u8>,
    pub retained: Difference,
    /// Property evaluations, including empty candidates and final verification.
    pub evaluations: usize,
    /// No single chunk deletion retains; this is not a global minimum claim.
    pub one_minimal: bool,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum ReduceError {
    Invalid(String),
    NoPairedDifference,
    ModelFailure(String),
}
impl std::fmt::Display for ReduceError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Invalid(why) => write!(f, "RV64GC reduction: {why}"),
            Self::NoPairedDifference => write!(f, "RV64GC reduction: no paired step difference to retain; error, length, fetch and final-state-only differences are outside this property"),
            Self::ModelFailure(why) => write!(f, "RV64GC reduction: model execution failed: {why}"),
        }
    }
}

fn checkpoint(case: &Case, image: &[u8]) -> Result<SnapshotRv64gc, ReduceError> {
    if image.len() > MEMORY_BYTES
        || case.budget > MAX_STEPS
        || !(2..=MAX_EVALUATIONS).contains(&case.evaluation_limit)
    {
        return Err(ReduceError::Invalid(
            "limits: image <=65536 bytes, steps <=1000, evaluations 2..=512".into(),
        ));
    }
    case.model.table().map_err(ReduceError::Invalid)?;
    let mut memory = FlatMemory::with_fetch_align(case.entry, MEMORY_BYTES, 2);
    memory.load_image(0, image);
    SnapshotRv64gc::capture(
        &memory,
        &mut ArchitecturalState::zeroed_at(case.entry),
        case.entry,
        0,
        case.budget,
        case.refusals,
    )
    .map_err(ReduceError::Invalid)
}

fn trace(case: &Case, image: &[u8], model: Model) -> Result<Trace, ReduceError> {
    let mut memory = FlatMemory::with_fetch_align(case.entry, MEMORY_BYTES, 2);
    memory.load_image(0, image);
    let mut state = ArchitecturalState::zeroed_at(case.entry);
    let trace =
        run_rv64gc::run_from_with_model(&mut memory, &mut state, case.budget, case.refusals, model)
            .map_err(ReduceError::Invalid)?;
    if let Some(error) = &trace.failed {
        return Err(ReduceError::ModelFailure(error.clone()));
    }
    Ok(trace)
}

fn paired_difference(reference: &Trace, model: &Trace) -> Option<Difference> {
    reference
        .steps
        .iter()
        .zip(&model.steps)
        .enumerate()
        .find(|(_, (a, b))| a != b)
        .map(|(at, (a, b))| Difference {
            at,
            reference: a.clone(),
            model: b.clone(),
        })
}

fn difference(case: &Case, image: &[u8]) -> Result<Option<Difference>, ReduceError> {
    if image.is_empty() {
        return Ok(None);
    }
    let reference = trace(case, image, Model::Production)?;
    let model = trace(case, image, case.model)?;
    Ok(paired_difference(&reference, &model))
}

/// Deterministic ddmin over image chunks. A capped search returns a retaining
/// candidate with `one_minimal=false`; it never reports an untested minimality claim.
pub fn reduce(case: &Case, image: &[u8]) -> Result<Reduction, ReduceError> {
    checkpoint(case, image)?;
    let original = difference(case, image)?.ok_or(ReduceError::NoPairedDifference)?;
    let mut current = image.to_vec();
    let mut evaluations = 1;
    let mut partitions = 2;
    let mut one_minimal = false;
    'search: loop {
        let chunks = current.len().div_ceil(2);
        let width = chunks.div_ceil(partitions);
        let mut removed = false;
        for start in (0..chunks).step_by(width) {
            // Always reserve one evaluation to re-derive the final witness.
            if evaluations >= case.evaluation_limit - 1 {
                break 'search;
            }
            let a = start * 2;
            let b = ((start + width) * 2).min(current.len());
            let candidate: Vec<_> = current[..a].iter().chain(&current[b..]).copied().collect();
            evaluations += 1;
            let retains = match difference(case, &candidate) {
                Ok(found) => found.as_ref() == Some(&original),
                Err(ReduceError::ModelFailure(_)) => false,
                Err(error) => return Err(error),
            };
            if retains {
                current = candidate;
                partitions = partitions.saturating_sub(1).max(2);
                removed = true;
                break;
            }
        }
        if !removed {
            if width == 1 {
                one_minimal = true;
                break;
            }
            partitions = (partitions * 2).min(chunks);
        }
    }
    evaluations += 1;
    let retained = difference(case, &current)?.ok_or_else(|| {
        ReduceError::Invalid("final verification lost the retained difference".into())
    })?;
    if retained != original {
        return Err(ReduceError::Invalid("final difference changed".into()));
    }
    Ok(Reduction {
        image: current,
        retained,
        evaluations,
        one_minimal,
    })
}

/// The original bytes, deterministic search receipt, and both complete reduced-run
/// bundles. Replay reruns the search as well as every child bundle receipt.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Reproducer {
    reducer_sha256: String,
    original_image: Vec<u8>,
    image_len: usize,
    evaluation_limit: usize,
    evaluations: usize,
    one_minimal: bool,
    reference: BundleRv64gc,
    model: BundleRv64gc,
}
fn reducer_identity() -> &'static str {
    static IDENTITY: std::sync::OnceLock<String> = std::sync::OnceLock::new();
    IDENTITY.get_or_init(|| sha256_hex(include_str!("reduce_rv64gc.rs").as_bytes()))
}

impl Reproducer {
    pub fn record(case: &Case, image: &[u8]) -> Result<(Self, Reduction), ReduceError> {
        let reduction = reduce(case, image)?;
        let input = checkpoint(case, &reduction.image)?;
        let reference = BundleRv64gc::record(input.clone()).map_err(ReduceError::Invalid)?;
        let model =
            BundleRv64gc::record_with_model(input, case.model).map_err(ReduceError::Invalid)?;
        let record = Self {
            reducer_sha256: reducer_identity().into(),
            original_image: image.to_vec(),
            image_len: reduction.image.len(),
            evaluation_limit: case.evaluation_limit,
            evaluations: reduction.evaluations,
            one_minimal: reduction.one_minimal,
            reference,
            model,
        };
        Ok((record, reduction))
    }

    /// Identity failures refuse; altered search or run receipts return a mismatch.
    /// Success returns the re-derived, exact original/reduced paired-step difference.
    pub fn replay(&self) -> Result<Difference, String> {
        if self.reducer_sha256 != reducer_identity() {
            return Err("RV64GC reduction: reducer identity mismatch".into());
        }
        self.check_shape()?;
        let cold = self
            .reference
            .input()
            .cold_image(MEMORY_BYTES, self.image_len)?;
        let case = Case {
            entry: cold.entry,
            budget: cold.budget,
            refusals: &cold.refusals,
            model: self.model.model(),
            evaluation_limit: self.evaluation_limit,
        };
        let reduction = reduce(&case, &self.original_image).map_err(|e| e.to_string())?;
        if reduction.image != cold.image
            || reduction.evaluations != self.evaluations
            || reduction.one_minimal != self.one_minimal
        {
            return Err("RV64GC reduction: search receipt mismatch".into());
        }
        for (name, bundle) in [("reference", &self.reference), ("model", &self.model)] {
            if bundle.replay()? != ReplayRv64gc::Identical {
                return Err(format!("RV64GC reduction: {name} run receipt mismatch"));
            }
        }
        if paired_difference(self.reference.recorded_trace(), self.model.recorded_trace())
            != Some(reduction.retained.clone())
        {
            return Err("RV64GC reduction: original/reduced difference mismatch".into());
        }
        Ok(reduction.retained)
    }

    fn check_shape(&self) -> Result<(), String> {
        if self.image_len > MEMORY_BYTES
            || self.original_image.len() > MEMORY_BYTES
            || self.reference.model() != Model::Production
            || self.model.model() == Model::Production
            || self.reference.input() != self.model.input()
            || self.reference.input().remaining_steps() > MAX_STEPS
            || !(2..=MAX_EVALUATIONS).contains(&self.evaluation_limit)
            || !(2..=self.evaluation_limit).contains(&self.evaluations)
        {
            return Err("RV64GC reduction: invalid bounds, model choice or paired input".into());
        }
        Ok(())
    }

    #[must_use]
    pub fn to_json(&self) -> String {
        let mut out = format!(
            "{{\"format\":\"{FORMAT}\",\"reducer_sha256\":\"{}\",\"original_image\":\"",
            self.reducer_sha256
        );
        for byte in &self.original_image {
            out.push_str(&format!("{byte:02x}"));
        }
        out.push_str(&format!(
            "\",\"image_len\":{},\"evaluation_limit\":{},\"evaluations\":{},\"one_minimal\":{},\"reference\":{},\"model\":{}}}",
            self.image_len, self.evaluation_limit, self.evaluations, self.one_minimal,
            self.reference.to_json(), self.model.to_json()
        ));
        out
    }

    pub fn parse(text: &str) -> Result<Self, String> {
        check_json_limits(text, MAX_JSON_BYTES, 2_000_000, "RV64GC reduction")?;
        let doc = json::parse(text).map_err(|e| format!("RV64GC reduction: {e}"))?;
        Self::from_json(&doc)
    }

    fn from_json(doc: &Json) -> Result<Self, String> {
        if field(doc, "format")?.as_str() != Some(FORMAT) {
            return Err("RV64GC reduction: unsupported format".into());
        }
        let original = field(doc, "original_image")?
            .as_str()
            .filter(|s| s.len() <= MEMORY_BYTES * 2 && s.len() % 2 == 0 && s.is_ascii())
            .ok_or("RV64GC reduction: invalid original image hex/length")?;
        let mut original_image = Vec::with_capacity(original.len() / 2);
        for at in (0..original.len()).step_by(2) {
            original_image.push(
                u8::from_str_radix(&original[at..at + 2], 16)
                    .map_err(|_| "RV64GC reduction: invalid original image hex")?,
            );
        }
        let reducer_sha256 = field(doc, "reducer_sha256")?
            .as_str()
            .filter(|s| s.len() == 64 && s.bytes().all(|b| b.is_ascii_hexdigit()))
            .ok_or("RV64GC reduction: invalid reducer SHA256")?
            .to_owned();
        let one_minimal = match field(doc, "one_minimal")? {
            Json::Bool(value) => *value,
            _ => return Err("RV64GC reduction: one_minimal must be boolean".into()),
        };
        let record = Self {
            reducer_sha256,
            original_image,
            image_len: int_usize(field(doc, "image_len")?, "image_len")?,
            evaluation_limit: int_usize(field(doc, "evaluation_limit")?, "evaluation_limit")?,
            evaluations: int_usize(field(doc, "evaluations")?, "evaluations")?,
            one_minimal,
            reference: BundleRv64gc::from_json(field(doc, "reference")?)?,
            model: BundleRv64gc::from_json(field(doc, "model")?)?,
        };
        record.check_shape()?;
        Ok(record)
    }
}
fn field<'a>(doc: &'a Json, name: &str) -> Result<&'a Json, String> {
    doc.get(name)
        .ok_or_else(|| format!("RV64GC reduction: missing '{name}'"))
}

/// CLI dispatch uses the parsed root format, never a substring search. The common
/// replay guard precedes parsing; reductions then apply their narrower byte bound.
#[derive(Debug)]
pub enum ReplayRecord {
    Run(Box<BundleRv64gc>),
    Reduced(Box<Reproducer>),
}
impl ReplayRecord {
    pub fn parse(text: &str) -> Result<Self, String> {
        check_json_limits(
            text,
            crate::replay_rv64gc::MAX_JSON_BYTES,
            2_000_000,
            "RV64GC replay",
        )?;
        let doc = json::parse(text).map_err(|e| format!("RV64GC replay: {e}"))?;
        if doc.get("format").and_then(Json::as_str) == Some(FORMAT) {
            if text.len() > MAX_JSON_BYTES {
                return Err("RV64GC reduction: JSON exceeds 16 MiB".into());
            }
            Ok(Self::Reduced(Box::new(Reproducer::from_json(&doc)?)))
        } else {
            Ok(Self::Run(Box::new(BundleRv64gc::from_json(&doc)?)))
        }
    }
}

#[cfg(test)]
mod tests;
