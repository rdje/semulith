# The `profiles/` family bound re-derived for two units — the second profile is the designed growth, not bloat

- **Type:** `decision`
- **Date:** `2026-10-01`
- **Status:** `active`
- **Owner / source:** `README-ROUTING-CLOSURE` fired at `SEMULITH-BR-0010`'s commit;
  `doctrine/readme_routes.tsv` requires a reviewed decision before any ceiling moves.
  Precedent: [`decision_task-tree-family-bound-rederivation.md`](decision_task-tree-family-bound-rederivation.md).

## What fired

```
OVER CEILING profiles/: 123 files > 120
```

Caused by `P3-BREADTH.4` slice 2 staging the second unit's dossier — 3 files
(`profiles/dsp56300-lab-v0/{DOSSIER.md,sources.sexp,references.sexp}`) onto the first
profile's 120. The family's own row states the contract: *"one directory per profile"* — so
a ceiling calibrated to exactly one profile's file count (120 measured on
`rv64i-lab-v0`) left zero headroom for the second profile the roadmap (P3) always planned.
That is a miscalibrated bound meeting the family's designed growth, not slack.

## Why the honest answer is not "compact something"

- The 120 rv64 files are the dossier the gates mandate: 49 guest pairs (98 files), the
  ledgers, reports, the act4 record — each exists because a doctrine requires it.
- The 3 new files are the minimal validating dossier slice 2 could land (the schema-deferred
  documents are recorded deferrals, not omissions). Nothing in the family is duplicative;
  FACT-OWNERSHIP is green over it.
- The aggregate-bytes axis (503,933 of 573,440) did NOT fire — but the same arithmetic
  applies to it: one full profile measures ~487 KiB, so a one-profile ceiling has no room
  for the second. Re-derived on the same basis below.

Rejected alternatives, with reasons: **deferring the dossier** (the leaf acceptance needs the
ledger now; parking tracked work to dodge a bound is the pressure moving underground);
**shrinking rv64's dossier** (its files are doctrine-mandated; deleting mandated evidence to
fit a miscalibrated count inverts the point of the count).

## The re-derived bound

Per-profile budget = the old family ceiling, which fit one full profile with headroom:
**120 files / 573,440 bytes**. The family now holds two units by design:

- `ceiling_lines`: 120 → **240** (2 × 120)
- `health_lines`: 118 → **236** (the old health/ceiling ratio, 0.983)
- `ceiling_bytes`: 573,440 → **1,146,880** (2 × 573,440)
- `health_bytes`: 490,000 → **980,000** (the old ratio, ~0.854)
- `ceiling_part_bytes`: **32,768, unchanged** — the per-part is the bound that bites; a
  single dossier member growing past 32 KiB is still the monolith signal, and the dsp56300
  `references.sexp` (10,659 B) is nowhere near it.

A third unit re-derives again by the same arithmetic, with a record like this one — the
bound scales with the measured unit count, never ahead of it.
