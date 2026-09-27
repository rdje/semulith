//! The verification harness: fixtures and evidence machinery around
//! `semulith-core`.
//!
//! Owns the controlled memory, fault and event fixtures that implement the
//! core environment boundary for tests, and the source/evidence graph,
//! adapters, comparators and reducer (`docs/ARCHITECTURE.md` §4).
//!
//! Boundary rule: this crate **implements** `semulith-core`'s boundary for
//! tests and **never supplies production instruction semantics**.

pub mod fixtures;
