# FP model-layer qualification — measured outputs and finite limits

- **Type:** `reference`
- **Date:** `2026-10-06`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.7` e3 historical qualification; corrected scope by
  `P4-SYSTEM.14` a6, `SEMULITH-P4-0197`, on `2026-10-10`

## Implemented surface and current checks

The selected `rustc_apfloat` dependency resolves in `Cargo.lock` to
`0.2.3+llvm-462a31f5a5ab`. The model layer `crates/semulith-core/src/fp.rs`
owns the selected RISC-V rounding, NaN, flag and conversion policies. The
experimental processor implements 30 F forms and 32 D forms. This is a feature
qualification, with separate CPU-profile acceptance requirements still open.

`FP-VECTORS` regenerates 230 directed vectors and 3,168 fixture rows from the
tracked `scripts/specfp.py` exact-rational producer and checks its RNE outputs
against host IEEE hardware. The instruction author and vector generator share
that producer, so they add no second numeric derivation. The complete finite
F/D execution witnesses exercise the governed rows and instruction/state/refusal
behavior; the FP book states their inputs, controls and limits. These checks
establish their measured outputs, not universal conformance or reference ancestry.

## Dated qualification receipts

The earlier record reports a 63,752-case scratch corpus with zero disagreements
against the exact-rational producer. It reports 24 signaling-NaN conversion
differences against the original MPFR oracle, attributed by the d3 amendment to
that oracle. The maintained qualification decision retains the two genuine
backend flag deviations and the withdrawn third allegation.

The e3 record also reports 24 Sail agreements over 927 steps for the original
F/D and FP-state guests. Those are finite public input/output observations under
the recorded match and comparison. The former claim about Sail's internal FP
implementation supplies no lineage credit and is withdrawn. The old 125-guest
checkpoint is dated history; current corpus scope is derived by its own gates.

The recorded host benchmark measured an arithmetic-core cost of 2.8–6.9 times
the raw backend for the model layer's exact overflow/underflow judgment. This is
the named historical host/run, not a current cross-host performance guarantee.
Neither that benchmark nor the large scratch corpus is claimed freshly replayed
by this documentation repair.

All original numeric timings, counts and assertions remain byte-verbatim in
`docs/tasks/archive/P4-SYSTEM-reference-a6.md` (`fp-acceptance`). Current public
FP-state, numeric, transfer and refusal examples are in
`docs/book/src/plan/p4/floating-point.md`; the qualification decision remains
`docs/decisions/decision_fp-backend-qualification.md`. Reference lineage limits
are stated in `reference_softfloat-shared-ancestry.md`.
