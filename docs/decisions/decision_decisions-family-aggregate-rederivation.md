# The `docs/decisions/` family bound re-derived — the aggregate byte axis fired, and the count axis is the same calendar

- **Type:** `decision`
- **Date:** `2026-10-02`
- **Status:** `active`
- **Owner / source:** `README-ROUTING-CLOSURE` fired at `P5-BOARD.1`'s commit:
  `OVER CEILING docs/decisions/: 131,911 aggregate bytes > 131,072`. Precedent:
  [`decision_changelog-family-aggregate-rederivation.md`](decision_changelog-family-aggregate-rederivation.md)
  (the byte axis re-derived when it fired, the count axis named the same calendar).

## What fired

`decision_profiles-family-three-units.md` (+2,447 B — the family's own designed growth,
one record per durable decision) landed the family at **36 files / 131,911 B**, 839 B
over the 131,072 aggregate ceiling. The count axis did not fire but stands at 36/40:
four records of headroom at decision velocity. The byte axis is the calendar the count
axis already was — the family grows one file per durable fact, at commit velocity, by
design.

## Why the honest answer is not "compact something"

- The records are ADR-style, one fact per file, each addressed by its own INDEX row.
  Merging records to fit the aggregate destroys the addressing the MEMORY-ARCH doctrine
  gates (INDEX row required per record).
- Moving records elsewhere forks retrieval: this family IS memory layer C, the one place
  durable facts are scanned for. A second location is a second memory.
- Nothing in the family is duplicative; FACT-OWNERSHIP and the INDEX gate are green
  over it.

## The re-derived bound

Both axes re-derived by the family's own 2× precedent; per-part untouched:

- `ceiling_lines` (files): 40 → **80** (2×; the same calendar, raised in the same record
  rather than waiting the four commits it would take to fire)
- `ceiling_bytes`: 131,072 → **262,144** (2×)
- `health_lines`: 15 → **48** · `health_bytes`: 24,576 → **163,840** (just above the
  measured 36 / 131,911 — a health target below the current measurement is a warning
  that can never clear, i.e. noise)
- `ceiling_part_bytes`: **16,384, unchanged** — the per-part is the bound that bites: a
  record growing past 16 KiB is the monolith signal. The largest member today is far
  under it.

After this record itself lands: ~37 files / ~135 KiB against the new bounds. The next
re-derivation waits for the next measured firing, never ahead of it.
