# A candidate-landscape census entry is a lead, not a measurement — the crate's own documents are the measurement surface

**Short answer:** web research over a crate landscape ("maintained, feature X, license Y")
is a lead, never a fact. The measurement surface is the fetched artifact: the crates.io
version record for maintenance state, the extracted crate's LICENSE files for the license
text (metadata fields are routinely empty), and `grep` over its `src/` for the capability
surface — because a README's claim and the code's reality differ exactly where a decision
depends on them. Measured at P4-SYSTEM.7 slice (a) (2026-10-06): the census's version and
license claims for both FP-backend candidates held, but its capability claims needed the
sources — `softfloat`'s "no rounding modes, no exception flags, no FMA, no 64-bit int
conversions" is invisible in any metadata and decisive against ARCHITECTURE.md §6, and its
"TestFloat-verified upstream" claim is unverifiable from the crate's own documents
(recorded as unverified, not counted). The same slice's MPFR vector generator needed FOUR
measured corrections to MPFR's own semantics (the DON'T-USE MPFR_RNDNA, the
exponent-range-shaped OF/UF flags, the NaN canonicalization, the NAN-flag-is-not-NV
mapping) — a third-lineage reference is also a thing to measure, not a fixture to trust.

## The pattern that works

- Re-measure every load-bearing claim of a landscape census at execution: version,
  maintenance, license TEXT (from the extracted artifact), capability (from the source),
  purity (unsafe / global state / no_std, from the source).
- The negatives too: "X is C FFI" / "Y descends from Z" is cheap to re-confirm from the
  metadata and prevents a stale landscape from silently pruning a candidate.
- When the measurement surface is a reference library's semantics (MPFR above), probe its
  documented quirks with directed micro-cases first — the expected-value generator is
  itself derived work and needs its own falsification.

## Evidence

- `docs/decisions/decision_fp-backend-qualification.md` — the full measured record
  (capability table, correctness tables, timing, licenses, the MPFR path).
- The scratch harness: `target/p4-system-7/` (probe/ + mpfr/vec_gen.c + candidates/).
