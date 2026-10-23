//! Self-contained replay of the bounded RV64GC flat-memory laboratory (P4.16).
//!
//! The input is a complete checkpoint, including typed fault regions. The record
//! explicitly declares no external event stream; board/device replay is outside
//! this format. Trace differences identify their first boundary. Aggregate fetch,
//! error and complete final-state receipts are compared separately.

use semulith_core::privilege::PrivilegeMode;

use crate::json::{self, Json};
use crate::model_rv64gc::Model;
use crate::replay::{hex_u64, int_usize};
use crate::report::push_escaped;
use crate::run_rv64gc::{Step, Trace};
use crate::sha256::sha256_hex;
use crate::snapshot_rv64gc::{check_json_limits, SnapshotRv64gc};

const FORMAT: &str = "semulith-rv64gc-replay-v2";
const LEGACY_FORMAT: &str = "semulith-rv64gc-replay-v1";
const ENVIRONMENT: &str = "flat-memory-no-external-events-v1";
/// Replay records have a smaller continuation bound than standalone snapshots.
pub const MAX_BOUNDARIES: usize = 10_000;
/// Complete input checkpoint plus at most 16 MiB of observations and receipts.
pub const MAX_JSON_BYTES: usize = crate::snapshot_rv64gc::MAX_JSON_BYTES + 16 * 1024 * 1024;

/// A recorded RV64GC run: the producer's identity, the model, the input checkpoint, the
/// recorded trace and the final-state digest.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct BundleRv64gc {
    producer_sha256: String,
    model: Model,
    input: SnapshotRv64gc,
    recorded: Trace,
    final_sha256: String,
}

/// The outcome of replaying an RV64GC bundle.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum ReplayRv64gc {
    /// The replay reproduces the recorded trace and final state exactly.
    Identical,
    /// The replay differs from the record.
    Mismatch {
        /// Absolute boundary when trace observations locate the difference;
        /// `None` for an aggregate or final-state receipt.
        boundary: Option<usize>,
        /// What differs, named.
        what: String,
    },
}

fn producer_identity() -> &'static str {
    static IDENTITY: std::sync::OnceLock<String> = std::sync::OnceLock::new();
    IDENTITY.get_or_init(|| {
        let pins = format!(
            "{}{}{}",
            sha256_hex(include_str!("replay_rv64gc.rs").as_bytes()),
            sha256_hex(include_str!("report.rs").as_bytes()),
            sha256_hex(include_str!("model_rv64gc.rs").as_bytes())
        );
        sha256_hex(pins.as_bytes())
    })
}

impl BundleRv64gc {
    /// Execute the recorded checkpoint and retain the result, including model errors.
    /// Identity and memory integrity are checked before execution by the checkpoint.
    pub fn record(input: SnapshotRv64gc) -> Result<Self, String> {
        Self::record_with_model(input, Model::Production)
    }

    /// Record a declared, pinned control overlay over the same base-state inventory.
    pub fn record_with_model(input: SnapshotRv64gc, model: Model) -> Result<Self, String> {
        check_budget(&input)?;
        let mut result = input.resume_with_model(model)?;
        check_trace(&result.trace, input.remaining_steps())?;
        let final_sha256 = input.result_sha256(&mut result)?;
        Ok(Self {
            producer_sha256: producer_identity().into(),
            model,
            input,
            recorded: result.trace,
            final_sha256,
        })
    }

    /// How many steps the recorded trace holds.
    #[must_use]
    pub fn recorded_steps(&self) -> usize {
        self.recorded.steps.len()
    }

    /// The model the bundle was recorded with.
    #[must_use]
    pub fn model(&self) -> Model {
        self.model
    }

    pub(crate) fn input(&self) -> &SnapshotRv64gc {
        &self.input
    }

    pub(crate) fn recorded_trace(&self) -> &Trace {
        &self.recorded
    }

    /// Re-derive observations and every final CPU/memory owner from the saved input.
    pub fn replay(&self) -> Result<ReplayRv64gc, String> {
        if self.producer_sha256 != producer_identity() {
            return Err("RV64GC bundle: producer identity mismatch".into());
        }
        check_budget(&self.input)?;
        let mut result = self.input.resume_with_model(self.model)?;
        for (i, (recorded, actual)) in self
            .recorded
            .steps
            .iter()
            .zip(&result.trace.steps)
            .enumerate()
        {
            let field = if recorded.pc != actual.pc {
                Some("PC")
            } else if recorded.mode != actual.mode {
                Some("privilege mode")
            } else if recorded.writes != actual.writes {
                Some("GPR changes")
            } else {
                None
            };
            if let Some(what) = field {
                return Ok(ReplayRv64gc::Mismatch {
                    boundary: Some(self.input.at_step() + i),
                    what: what.into(),
                });
            }
        }
        if self.recorded.steps.len() != result.trace.steps.len() {
            return Ok(ReplayRv64gc::Mismatch {
                boundary: Some(
                    self.input.at_step() + self.recorded.steps.len().min(result.trace.steps.len()),
                ),
                what: "boundary count".into(),
            });
        }
        let field = if self.recorded.failed != result.trace.failed {
            Some("model error receipt")
        } else if self.recorded.fetches != result.trace.fetches {
            Some("fetch count receipt")
        } else if self.final_sha256 != self.input.result_sha256(&mut result)? {
            Some("final CPU/environment receipt")
        } else {
            None
        };
        Ok(match field {
            Some(what) => ReplayRv64gc::Mismatch {
                boundary: None,
                what: what.into(),
            },
            None => ReplayRv64gc::Identical,
        })
    }

    /// The bundle as a JSON record (`semulith-rv64gc-replay-v2`).
    #[must_use]
    pub fn to_json(&self) -> String {
        let mut out = format!(
            "{{\"format\":\"{FORMAT}\",\"model\":\"{}\",\"environment\":\"{ENVIRONMENT}\",\"producer_sha256\":\"",
            self.model.name()
        );
        push_escaped(&mut out, &self.producer_sha256);
        out.push_str(&format!(
            "\",\"input\":{},\"recorded\":{{\"steps\":[",
            self.input.to_json()
        ));
        for (i, step) in self.recorded.steps.iter().enumerate() {
            if i != 0 {
                out.push(',');
            }
            out.push_str(&format!(
                "{{\"pc\":\"0x{:016x}\",\"mode\":{},\"writes\":[",
                step.pc,
                step.mode.code()
            ));
            for (j, (register, value)) in step.writes.iter().enumerate() {
                if j != 0 {
                    out.push(',');
                }
                out.push_str(&format!("[{register},\"0x{value:016x}\"]"));
            }
            out.push_str("]}");
        }
        out.push_str(&format!(
            "],\"fetches\":\"0x{:016x}\",\"failed\":",
            self.recorded.fetches
        ));
        match &self.recorded.failed {
            Some(error) => {
                out.push('"');
                push_escaped(&mut out, error);
                out.push('"');
            }
            None => out.push_str("null"),
        }
        out.push_str("},\"final_sha256\":\"");
        push_escaped(&mut out, &self.final_sha256);
        out.push_str("\"}");
        out
    }

    /// Parse a bundle record, refusing one beyond `MAX_JSON_BYTES`.
    pub fn parse(text: &str) -> Result<Self, String> {
        check_json_limits(text, MAX_JSON_BYTES, 2_000_000, "RV64GC bundle")?;
        let doc = json::parse(text).map_err(|e| format!("RV64GC bundle: {e}"))?;
        Self::from_json(&doc)
    }

    pub(crate) fn from_json(doc: &Json) -> Result<Self, String> {
        let model = match field(doc, "format")?.as_str() {
            Some(FORMAT) => Model::from_name(
                field(doc, "model")?
                    .as_str()
                    .filter(|s| s.len() <= 64)
                    .ok_or("RV64GC bundle: model must be a bounded canonical name")?,
            )?,
            Some(LEGACY_FORMAT) => {
                if doc.get("model").is_some() {
                    return Err("RV64GC bundle: v1 has no model choice".into());
                }
                Model::Production
            }
            _ => return Err("RV64GC bundle: unsupported format".into()),
        };
        if field(doc, "environment")?.as_str() != Some(ENVIRONMENT) {
            return Err("RV64GC bundle: unsupported environment/event policy".into());
        }
        let input = SnapshotRv64gc::from_json(field(doc, "input")?)?;
        check_budget(&input)?;
        let raw = field(doc, "recorded")?;
        let nodes = field(raw, "steps")?
            .as_arr()
            .filter(|v| v.len() <= MAX_BOUNDARIES)
            .ok_or("RV64GC bundle: invalid steps array (maximum 10000)")?;
        let mut steps = Vec::with_capacity(nodes.len());
        for node in nodes {
            let mode = match int_usize(field(node, "mode")?, "mode")? {
                0 => PrivilegeMode::U,
                1 => PrivilegeMode::S,
                3 => PrivilegeMode::M,
                _ => return Err("RV64GC bundle: invalid mode".into()),
            };
            let values = field(node, "writes")?
                .as_arr()
                .filter(|v| v.len() <= 31)
                .ok_or("RV64GC bundle: invalid GPR changes array")?;
            let mut writes = Vec::with_capacity(values.len());
            let mut previous = 0;
            for value in values {
                let pair = value
                    .as_arr()
                    .filter(|v| v.len() == 2)
                    .ok_or("RV64GC bundle: invalid GPR change pair")?;
                let register = int_usize(&pair[0], "register")?;
                if register <= previous || register > 31 {
                    return Err("RV64GC bundle: GPR changes must be ordered unique x1..x31".into());
                }
                writes.push((register as u8, hex_u64(&pair[1], "GPR value")?));
                previous = register;
            }
            steps.push(Step {
                pc: hex_u64(field(node, "pc")?, "PC")?,
                mode,
                writes,
            });
        }
        let failed = match field(raw, "failed")? {
            Json::Null => None,
            Json::Str(error) if error.len() <= 4096 => Some(error.clone()),
            _ => return Err("RV64GC bundle: invalid model error receipt".into()),
        };
        let recorded = Trace {
            steps,
            failed,
            fetches: hex_u64(field(raw, "fetches")?, "fetches")?,
        };
        check_trace(&recorded, input.remaining_steps())?;
        Ok(Self {
            producer_sha256: digest(field(doc, "producer_sha256")?)?,
            model,
            input,
            recorded,
            final_sha256: digest(field(doc, "final_sha256")?)?,
        })
    }
}

fn check_budget(input: &SnapshotRv64gc) -> Result<(), String> {
    if input.remaining_steps() > MAX_BOUNDARIES {
        return Err("RV64GC bundle: continuation exceeds 10000 boundaries".into());
    }
    Ok(())
}
fn check_trace(trace: &Trace, budget: usize) -> Result<(), String> {
    if trace.steps.len() > budget || trace.failed.as_ref().is_some_and(|e| e.len() > 4096) {
        return Err("RV64GC bundle: result exceeds declared budget/receipt limits".into());
    }
    Ok(())
}
fn field<'a>(doc: &'a Json, name: &str) -> Result<&'a Json, String> {
    doc.get(name)
        .ok_or_else(|| format!("RV64GC bundle: missing '{name}'"))
}
fn digest(node: &Json) -> Result<String, String> {
    node.as_str()
        .filter(|s| s.len() == 64 && s.bytes().all(|b| b.is_ascii_hexdigit()))
        .map(str::to_owned)
        .ok_or("RV64GC bundle: expected SHA256 string".into())
}

#[cfg(test)]
mod tests;
