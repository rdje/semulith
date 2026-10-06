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
//! mutation suite; [`replay`] (`P1-LAB.10`) is the recorded input bundle that
//! reproduces a result from its definitions, tools, inputs and event choices
//! (G-REPLAY), and [`reduce`] is the minimizer whose output retains the original
//! first divergence (EVD-02); [`bench`] (`P1-LAB.11`) is the performance-baseline
//! harness — the workload mixes, the three ARCHITECTURE §6 modes, the RUST-02
//! agreement check and the noise statistics (RUST-04); on the wasm target [`wasm`]
//! exports the bench's `extern "C"` surface (both demo surfaces run the same engine
//! the commit gate tests).

pub mod bench;
pub mod contract_checks_rv64gc;
pub mod elf;
pub mod fixtures;
pub mod graph;
pub mod guests;
pub mod guests_rv64gc;
pub mod json;
pub mod mutate;
pub mod pattern;
pub mod reduce;
pub mod replay;
pub mod report;
pub mod run;
pub mod run_rv64gc;
pub mod schema;
pub mod sha256;
pub mod snapshot;
#[cfg(target_arch = "wasm32")]
pub mod wasm;
