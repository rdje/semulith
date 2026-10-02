# The `profiles/` per-part bound re-derived for the first DERIVED member class — a composed unit's catalogues are the merge of bounded parts

- **Type:** `decision`
- **Date:** `2026-10-02`
- **Status:** `active`
- **Owner / source:** `P5-BOARD.3` stages the first composed unit directory
  (`profiles/netboard-lab-v0/` — the board's generated composition manifest, composed
  catalogues, hardware description and map). The family's recorded policy: *"the bound
  scales with the measured unit count, never ahead of it"*; the per-part raise follows
  the reviewed-raise precedent of
  [`decision_profiles-family-five-units.md`](decision_profiles-family-five-units.md),
  which named the rule: *"if a future device's catalogue approaches 64 KiB, that
  re-derivation is where the raise belongs, reviewed, never silent."*

## What changed

The per-part bound BITES a second time — and for the first time on a **derived** member,
not an authored dossier. The composed `contract-obligations.sexp` (the merge of the three
parts' obligations, materialized by `compose_units.compose_resolved`, drift-gated by
BOARD-GEN) is **104,372 B**, over the 65,536 bound; the composed `requirements.sexp` is
94,027 B. The cause is structural and was predicted by the five-units record's own
arithmetic: a composed catalogue carries the union of its parts' mirrored records (52 NIC
+ 19 UART + 36 CPU environment ≈ 107 obligations), so its size is the SUM of surfaces the
house's mirror discipline already mandates — the only way to shrink it is to compose
fewer units, not to mirror fewer facts.

The aggregates are untouched by the event. Measured at staging: **167 files /
1,051,283 B** tracked under `profiles/` (160 / 845,819 prior + 7 composed artifacts —
`composition.sexp`, the four catalogues, `hardware.sexp`, `map.md`), against the 5×
bound of 600 files / 2,867,200 B (0.28× files, 0.37× bytes). No aggregate move.

## The re-derived bound

- `ceiling_part_bytes`: 65,536 → **131,072** — the family's second per-part raise, the
  first for a derived member class. The largest member sits at **0.80×**
  (104,372 / 131,072); the second (`requirements.sexp`, 94,027 B) at 0.72×.
- Aggregates unchanged: `ceiling_lines` 600, `health_lines` 590,
  `ceiling_bytes` 2,867,200, `health_bytes` 2,450,000 (the 5× arithmetic of the
  five-units record).

## Why a raise under pressure is honest here

Same rule as the first bite, one new wrinkle: the content is not just measured, it is
**re-derived on every commit** (BOARD-GEN) — the file cannot silently grow a byte, so
the bound cannot be gamed by slow accretion; the only way it moves is a part's contract
moving, which is exactly the event the next re-derivation reviews. A composed unit's
catalogue is bounded by construction at the sum of its parts' catalogues, so the
doubling tracks the composition depth the roadmap implies (computer → board → soc →
{cpu, device}) with the margin stated in the open. The 6× aggregate re-derivation still
waits for the next measured unit — never ahead of it.
