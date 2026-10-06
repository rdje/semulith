# An oracle can share the convention it judges — check its rule text against the spec sentence

**Short answer:** an independent implementation is only an independent OPINION where its
rules were written independently. When you build an oracle, every rule you write into it —
when a flag fires, what a boundary case returns — must be traced to the specification's own
sentence, never to "what the thing under test does" or "what the obvious encoding suggests".
An oracle that encodes the backend's convention agrees with the backend by construction, and
its agreement is silence, not evidence.

Measured at P4-SYSTEM.7 slice (c4) (2026-10-06): slice (a) qualified the FP backend against
MPFR — a third lineage, neither SoftFloat nor LLVM — and recorded zero arithmetic
disagreements and a short list of named flag deviations. Writing the model layer against a
second oracle (exact rationals, rules quoted from IEEE 754-2008) showed the MPFR generator
had judged OVERFLOW on the exact magnitude (IEEE judges the unbounded-exponent ROUNDED
result: 72 false overflows) and UNDERFLOW on the delivered result (IEEE judges tininess
before the subnormal rounding — the backend's convention, so a real deviation was invisible).
Both lineages were genuinely independent code; the shared thing was the RULE.

## The pattern that works

- Write each oracle rule beside the sentence it implements (§7.4's "were the exponent range
  unbounded", §7.5's tininess, RVI-F §20.1.4's "after rounding") — and check boundary cases
  the rule distinguishes (MAX+1 under RTZ; 2^-126·(1−2^-24) rounding up to the smallest
  normal). A random corpus almost never visits them.
- Judge the oracle itself against an independent physical reference where one exists (the
  host's hardware IEEE in RNE), with directed cases for the rules random inputs miss.
- When two references agree on everything, ask what they could BOTH be wrong about — the
  shared ancestor may be a convention, not code (EVD-04's sibling).

## The starkest form — an oracle that cannot represent the case (2026-10-06, slice d3)

The same record named a second backend deviation: "an sNaN through a format conversion gets
no NV flag", 24 cases. Writing the model layer's patch for it, the unit vectors passed with
the patch BYPASSED — dead code — so the backend was probed instead of trusted to the record:
it raises INVALID_OP for a signaling NaN through `convert_r`, both directions. All 24 recorded
disagreements read `apfloat NV, mpfr -`. MPFR has ONE NaN kind; an oracle with no signaling
NaN cannot raise invalid for one, and its silence had been booked against the backend.

- Before writing a patch for a recorded deviation, re-measure the deviation at its source; a
  patch the tests cannot tell from its absence is evidence the deviation is not there.
- For every disagreement, ask which side CAN express the case. A disagreement on a case one
  side cannot represent belongs to that side.
- A prose sweep that copies a record's count inherits the record's error: slice (c6) had
  "corrected" a schema comment from two deviations to three on the record's word.

## Evidence

- `docs/decisions/decision_fp-backend-qualification.md` — the `2026-10-06` amendment.
- `scripts/specfp.py`, `scripts/check_fp_vectors.sh` (FP-VECTORS: the reference is re-checked
  against the hardware on directed ties every run — a half-up mutation is caught).
- The record's second amendment (`2026-10-06`, slice d3) and `fp.rs::convert`.
