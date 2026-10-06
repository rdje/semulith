//! Semulith's canonical model core.
//!
//! This crate owns what every backend and harness derives from
//! (`docs/ARCHITECTURE.md` §4): profiles and typed values, generated state,
//! decode and semantics, the definitional interpreter that evaluates them
//! (`exec`), the privileged-state machinery (`privilege` — trap delivery, xret,
//! the CSR permission model and legalization over the generated tables,
//! `P4-SYSTEM.2`), the environment request/response contract, and execution
//! control with explicit progress and stop types.
//!
//! Ownership rule: `semulith-core` depends on **neither** `semulith-verify`
//! **nor** `semulith-cli`. The verification harness and the CLI consume this
//! crate; never the reverse. Behaviour lands leaf by leaf under `P1-LAB`; the
//! skeleton exists so the boundary holds from the first commit.

pub mod arith;
pub mod definition;
pub mod definition_rv64gc;
pub mod env;
pub mod exec;
pub mod exec_rv64gc;
pub mod fp;
pub mod interrupts;
pub mod muldiv;
pub mod outcome;
pub mod privilege;
pub mod reservation;
pub mod state;
pub mod state_rv64gc;
pub mod timekeeping;
pub mod translation;
pub mod wait;

/// The qualified FP backend (`P4-SYSTEM.7` slice (a), measured in
/// `docs/decisions/decision_fp-backend-qualification.md`) — pinned exact; the model
/// layer [`fp`] (slice (c4)) is its only consumer of record — an evaluator arm never
/// calls it directly. Re-exported so a harness can name the exact backend version.
pub use rustc_apfloat;
