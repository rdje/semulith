//! Semulith's bounded, EXPERIMENTAL DSP56300 model — unit `dsp56300-lab-v0`, subset v0.
//!
//! This crate is a deliberate sibling of `semulith-core`, not a second unit inside it
//! (`decision_dsp56300-lab-v0-subset`): the S-expression generator pipeline refuses a
//! second unit by name, and generalizing it is `P3-BREADTH.5`'s reviewed work with this
//! crate as the measured input. Every decode mask and semantic rule here is derived from
//! the pinned family manual — DSP56300FM Rev. 5, pinned in
//! `profiles/dsp56300-lab-v0/sources.sexp` — with per-form citations in the modules, and
//! NEVER from the reference emulator's decoder tables, so that the differential comparison
//! against `mborgerson/dsp56300`'s difftest remains a second opinion (EVD-04).
//!
//! Subset v0 (the claim names exactly this — the exclusions are load-bearing):
//! non-parallel moves including the A2/B2 extension readout, the immediate/register
//! data-ALU core, signed `mpy`/`mac`, `nop/jmp/jsr/rts`, `do`/`enddo`/`rep`, linear
//! addressing only. Anything outside the subset is a typed `ModelStop`, never a guessed
//! translation (`docs/ARCHITECTURE.md` §2's rule, applied by hand here until the generator
//! learns it). No timing is modelled: the reference's `cyc` is informational
//! (LIMITATIONS §4) and this model emits none.
//!
//! The comparison surface is the reference harness's canonical per-case end-state dump
//! (`dump`): registers, deviation-encoded X/Y/P memory windows, and the 15 hardware stack
//! slots — checkpoint-level field-exact equality, `steps` compared, `cyc` never.

pub mod decode;
pub mod dump;
pub mod exec;
pub mod lod;
pub mod machine;

pub use machine::{Machine, ModelStop, ResetImage};
