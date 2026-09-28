//! The verification harness: fixtures and evidence machinery around
//! `semulith-core`.
//!
//! Owns the controlled memory, fault and event fixtures that implement the
//! core environment boundary for tests, and the source/evidence graph,
//! adapters, comparators and reducer (`docs/ARCHITECTURE.md` §4).
//!
//! Boundary rule: this crate **implements** `semulith-core`'s boundary for
//! tests and **never supplies production instruction semantics**.
//!
//! The evidence machinery ([`json`], [`pattern`], [`sha256`], [`schema`],
//! [`graph`]) is the T004 graph and report checker (`P1-LAB.7`): a dependency-free
//! re-derivation of the PACKAGE_CHECKS schema results in Rust (RUST-01) plus the
//! `docs/EVIDENCE_AND_GATES.md` §3 graph invariants over the frozen JSONL records.
//! The library is pure — evidence bytes arrive as `&[u8]` — so the workspace keeps
//! building for `wasm32-unknown-unknown` (PORT-WEB); filesystem access lives in the
//! CLI command and the tests. [`report`] (`LAB-BENCH.1`) is the demo/bench judgement
//! the CLI and the browser bench share; [`mutate`] (`P1-LAB.9`) is the validator
//! mutation suite, and on the wasm target [`wasm`] exports the bench's `extern "C"`
//! surface (both demo surfaces run the same engine the commit gate tests).

pub mod elf;
pub mod fixtures;
pub mod graph;
pub mod guests;
pub mod json;
pub mod mutate;
pub mod pattern;
pub mod report;
pub mod run;
pub mod schema;
pub mod sha256;
#[cfg(target_arch = "wasm32")]
pub mod wasm;
