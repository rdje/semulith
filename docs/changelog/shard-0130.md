# CHANGELOG shard — SEMULITH-DR-0089 … SEMULITH-DR-0085

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-DR-0089 (leaf DSP-REVIEW.4) — the predicted break, measured — twice

- The scalar step model breaks, measured: (1) the execute PACKET is the unit of progress
  (≤8 instructions, all operands read simultaneously at E1); (2) writeback is delayed and
  visible (load at i+4, no interlocks, early reads stale by design) with interrupts
  landing INSIDE the window (the manual's own LDW/ADD example computes incorrectly).
  `OB-ENV-PARTIAL-PROGRESS` is true for RV64I and false for C6000 — recorded so
  P3-BREADTH never inherits it silently.
- The census consequence: a DSP profile reopens the hidden-state census by its own rule
  (the pending-writes window + packet state). The §3.7.2/§3.8.2 contradiction recorded in
  both forms, C66x's resolved form beside them.
- Evidence: docs/tasks/artifacts/dsp-review/2026-09-30-packets-q9-q11.md.

## SEMULITH-DR-0088 (leaf DSP-REVIEW.3) — addressing and address spaces: units byte-compatible, the seams named

- The acceptance's exact check — units, not just widths: byte-addressed on BOTH sides,
  one 32-bit numbering (no word-addressed space exists — measured). The five seams that
  do NOT fit the flat lab shape, each measured with locators: the 32-bit space; two L1
  spaces with a program-only fetch port (D-FETCH-MAP is scalar-lab-shaped); fetch-packet
  alignment; the AMR control register (the lab has no CSR surface); circular addressing
  restricted to A4–A7/B4–B7. Measured absent: bit-reversed addressing (BITR is a data
  op), strided modes (0 hits ×3). A second core-version split pinned (the circular
  nonalignment floor). Four more manual defects recorded unresolved.
- Includes the gap filing's changelog (SEMULITH-DR-0087 carried none — folded here):
  GAP-DSP56K-FAMILY-MANUAL and GAP-ADI-SHARC-PRM filed through the two-way channel; the
  C55x want dissolved on measurement (already catalogued).
- Evidence: docs/tasks/artifacts/dsp-review/2026-09-30-addressing-q6-q8.md.

## SEMULITH-DR-0086 (leaf DSP-REVIEW.2) — rounding, saturation, sticky flags: the defined step sequences

- The ordering measured as the manuals' own step sequences (multiply → accumulate →
  round-add → shift/saturate → narrow; CMPYR1/DDOTPH2R/QSMPY32R1/DOTPNRSU2 quoted with
  locators) — the leaf's acceptance, never "a saturating add".
- Saturation is in-instruction AND per-lane AND an explicit transfer (SAT); the
  sticky-flag side effect is per-instruction DATA (SADD2 saturates but does not set SAT —
  printed in its own entry). CSR.SAT/SSR survive interrupts (the TSR tables prove it);
  the context-switch restore ORDER is documented; SAT sets one cycle after the result —
  the delayed-effect shape, routed as `.4`'s input.
- **Seven manual defects/ambiguities recorded, none resolved by intuition** (the CMPYR1
  typo in two manuals, the prose-vs-C ordering contradiction, the missing saturation
  clause, the core-version intermediate-width split…). Evidence:
  docs/tasks/artifacts/dsp-review/2026-09-30-rounding-saturation-q3-q5.md.

## SEMULITH-DR-0085 (leaf DSP-REVIEW.1) — widths and accumulator semantics, measured across the three TI manuals

- The first DSP review leaf: Q1/Q2 of the catalog's DSP questions answered from the
  catalogued C64x/C66x/C674x manuals by text extraction — every fact quoted with its
  printed page and section. Headlines: NO accumulator and NO guard bits anywhere
  (measured absent, the searches named); 40-bit "long" values in odd:even register pairs
  with a zero-fill rule (all three), 64-bit pairs (all three), 128-bit quadruplets (C66x
  only); Q-notation nearly absent (Q31 exactly once); scaling instruction-encoded (the
  S-family's <<1+saturate) — and the `s`-bit trap measured (it's the A/B side-select).
- The first classification for `.7`: register GROUPING with a width+fill rule is the one
  candidate abstraction change; no accumulator/guard state is needed for these targets.
  Evidence: docs/tasks/artifacts/dsp-review/2026-09-30-widths-q1-q2.md.
- The tree's stale G1 blocker repaired; the tree is active; LIVE_STATUS's P2 row (stale
  at 8/9 from a mid-flight script abort) corrected to Done 9/9.

