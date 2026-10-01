# The `profiles/` family bound re-derived for three units — the first board dossier lands inside the same arithmetic

- **Type:** `decision`
- **Date:** `2026-10-02`
- **Status:** `active`
- **Owner / source:** `P5-BOARD.1` stages the third unit directory
  (`profiles/netboard-lab-v0/` — the first *board* dossier). The family's own row records
  the policy: *"A third unit re-derives again by the same arithmetic, with a record like
  this one — the bound scales with the measured unit count, never ahead of it"*
  ([`decision_profiles-family-two-units.md`](decision_profiles-family-two-units.md)).
  Director-approved in principle `2026-10-02` (the `P5-BOARD` design brief's machinery
  census, `docs/tasks/P5-BOARD.md`).

## What changed

Nothing fired. Measured at staging: **142 files / ~565 KiB** tracked under `profiles/`
(120 `rv64i-lab-v0` + 20 `dsp56300-lab-v0` + 2 `netboard-lab-v0`) against the 2× bound of
240 files / 1,146,880 B. The third unit is the family's designed growth — the roadmap's P5
always planned a board — so the provenance note "the 2× bound" would drift the moment the
directory lands, even though the numbers still hold.

## The re-derived bound

The same arithmetic as the two-units record: per-unit budget 120 files / 573,440 bytes,
scaled by the measured unit count:

- `ceiling_lines`: 240 → **360** (3 × 120)
- `health_lines`: 236 → **354** (the standing health/ceiling ratio, 0.983)
- `ceiling_bytes`: 1,146,880 → **1,720,320** (3 × 573,440)
- `health_bytes`: 980,000 → **1,470,000** (the standing ratio, ~0.854)
- `ceiling_part_bytes`: **32,768, unchanged** — the per-part is the bound that bites; the
  largest new member (`board.sexp`, ~8 KiB) is nowhere near it.

## Why a raise without pressure is honest here

The gate's rule is *"never raise one to land content"* — and no content needs the raise:
142 < 240. What requires the reviewed decision is the **contract expansion**: the family's
row contract is *one directory per modelled unit*, and the unit count it covers moved from
two to three. The recorded policy ties the bound to the measured unit count, so the
re-derivation is mechanical, and the headroom it buys is exactly the headroom the
precedent bought the second unit. The board dossier's own growth (device-unit ledgers in
`P5-BOARD.2`, generated maps in `.3`) lands inside this budget; the next re-derivation
waits for the next measured unit, never ahead of it.
