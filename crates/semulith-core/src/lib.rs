//! Semulith's canonical model core.
//!
//! This crate owns what every backend and harness derives from
//! (`docs/ARCHITECTURE.md` §4): profiles and typed values, generated state,
//! decode and semantics, the definitional interpreter that evaluates them
//! (`exec`), the environment request/response contract, and execution control
//! with explicit progress and stop types.
//!
//! Ownership rule: `semulith-core` depends on **neither** `semulith-verify`
//! **nor** `semulith-cli`. The verification harness and the CLI consume this
//! crate; never the reverse. Behaviour lands leaf by leaf under `P1-LAB`; the
//! skeleton exists so the boundary holds from the first commit.

pub mod arith;
pub mod definition;
pub mod env;
pub mod exec;
pub mod outcome;
pub mod state;
