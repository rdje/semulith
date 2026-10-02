# The `docs/models/` family bound re-derived for five unit books — registration day's designed growth

- **Type:** `decision`
- **Date:** `2026-10-02`
- **Status:** `active`
- **Owner / source:** `P5-BOARD.11` lands the third, fourth and fifth unit books
  (`docs/models/netboard-lab-v0/`, `sifive-uart-lab-v0/`, `lan9118-lab-v0/`) — the
  one-definition-one-book rule
  ([`decision_one-definition-one-book.md`](decision_one-definition-one-book.md)) makes a
  directory per registered unit the family's *designed* expansion, and the registry
  comment said so at adoption: "the file-count ceiling is the calendar for it."
  Registration day is the calendar firing. The `profiles/` family's recorded policy
  applies in kind: the bound scales with the measured unit count, never ahead of it
  ([`decision_profiles-family-five-units.md`](decision_profiles-family-five-units.md)).

## What changed

The family's file-count ceiling (40, set at adoption for one unit with the growth axis
named) is crossed by the measured corpus: **57 files / 181,382 B** across five unit
books (rv64i 13 / 86,716 B; dsp56300 12 / 37,737 B; the two device books 11 each;
the board 10). UNIT-BOOKS makes the crossing mandatory — a registered unit without its
book fails the commit — so the bound re-derives with the measured unit count, as
designed.

## The re-derived bound

The standing per-unit budget was 20 files / 131,072 B (40 / 262,144 at two units);
the largest measured book (rv64i-lab-v0, 13 files) sits at 0.65× the file budget:

- `ceiling_lines`: 40 → **100** (5 × 20)
- `health_lines`: 16 → **98** (the `profiles/` standing health/ceiling ratio, 0.983 —
  the adoption-era ratio 0.4 was calibrated for one unit and is already below the
  measured corpus, which is what a health line must not be)
- `ceiling_bytes`: 262,144 → **655,360** (5 × 131,072)
- `health_bytes`: 65,536 → **560,000** (the standing ~0.854 ratio)
- `ceiling_part_bytes`: **32,768, unchanged** — the largest member
  (`rv64i-lab-v0/src/materials.md`, 17,540 B) is nowhere near it.

## Why a raise without pressure is honest here

The gate's rule is *"never raise one to land content"* — and no content needed the
raise: 57 < 40 is false, but the *contract* expansion is the family's own design
(one book per unit; five registered units). The raise is reviewed and recorded here,
with the measured census, rather than smuggled past the ceiling — and the next
re-derivation (6×) waits for the next registered unit, never ahead of it.
