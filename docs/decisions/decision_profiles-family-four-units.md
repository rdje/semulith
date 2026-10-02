# The `profiles/` family bound re-derived for four units — the first device dossier lands inside the same arithmetic

- **Type:** `decision`
- **Date:** `2026-10-02`
- **Status:** `active`
- **Owner / source:** `P5-BOARD.2` stages the fourth unit directory
  (`profiles/sifive-uart-lab-v0/` — the first *device* dossier). The family's recorded
  policy: *"the bound scales with the measured unit count, never ahead of it"*
  ([`decision_profiles-family-three-units.md`](decision_profiles-family-three-units.md),
  [`decision_profiles-family-two-units.md`](decision_profiles-family-two-units.md)). The
  `.2` design brief (`docs/tasks/P5-BOARD.md`, Decisions, `2026-10-02`) named this
  re-derivation before execution, and the `.10` leaf re-derives 4× → 5× the same way.

## What changed

Nothing fired. Measured at staging: **147 files / ~609 KiB** tracked under `profiles/`
(142 prior + 5 `sifive-uart-lab-v0`: `DOSSIER.md`, `sources.sexp`, `requirements.sexp`,
`contract-obligations.sexp`, `state.sexp` — `profile.sexp` and the expected-results
document land with the same leaf and are inside this arithmetic's headroom) against the
3× bound of 360 files / 1,720,320 B. The fourth unit is the family's designed growth —
the roadmap's P5 always planned devices beside the board — so the provenance note "the
3× bound" would drift the moment the directory lands, even though the numbers still hold.

## The re-derived bound

The same arithmetic as the two- and three-units records: per-unit budget 120 files /
573,440 bytes, scaled by the measured unit count:

- `ceiling_lines`: 360 → **480** (4 × 120)
- `health_lines`: 354 → **472** (the standing health/ceiling ratio, 0.983)
- `ceiling_bytes`: 1,720,320 → **2,293,760** (4 × 573,440)
- `health_bytes`: 1,470,000 → **1,960,000** (the standing ratio, ~0.854)
- `ceiling_part_bytes`: **32,768, unchanged** — the per-part is the bound that bites; the
  largest new member (`contract-obligations.sexp`, 14,323 B) is nowhere near it.

## Why a raise without pressure is honest here

The gate's rule is *"never raise one to land content"* — and no content needs the raise:
147 < 360. What requires the reviewed decision is the **contract expansion**: the family's
row contract is *one directory per modelled unit*, and a device is a modelled unit — the
unit count it covers moved from three to four. The recorded policy ties the bound to the
measured unit count, so the re-derivation is mechanical, and the headroom it buys is
exactly the headroom the precedent bought the third unit. The next re-derivation (5×)
waits for the next measured unit — `lan9118-lab-v0`, `P5-BOARD.10` — never ahead of it.
