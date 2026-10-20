# The `docs/decisions/` family bound re-derived a second time — the byte axis fired again, and the cap was already withholding records

- **Type:** `decision`
- **Date:** `2026-10-20`
- **Status:** `active`
- **Owner / source:** `LIVE-CONTAINMENT.4` slice (k), `SEMULITH-LC-0050`; routed in by
  `ARTIFACT-CLEANUP.23` (`SEMULITH-AC-0077`), whose own record was drafted and withdrawn when
  `README-ROUTING-CLOSURE` reported `OVER CEILING docs/decisions/: 262242 aggregate bytes > 262144`
  with only its index row added. Precedent:
  [`decision_decisions-family-aggregate-rederivation.md`](decision_decisions-family-aggregate-rederivation.md)
  (`2026-10-02`, the first firing: 36 files / 131,911 B → 80 files / 262,144 B).

## What fired

At `b70b2f5` the family holds 61 files / 262,031 B — 59 records, the index and the template —
with 113 B of headroom. This record (3,020 B) and its index row (256 B) land it at
62 files / 265,307 B, over the ceiling. Measured velocity (`git log --diff-filter=A`): 26
records between `2026-10-02` and `2026-10-12`, then none for eight days while the family sat
within 540 B of the ceiling — `SEMULITH-AC-0077` withdrew a record and `SEMULITH-P4-0283`
edited two existing ones to fit. A cap that makes authors withhold durable facts is the
anti-pattern the containment doctrine names ("tightening to pass a cap"), not a healthy survivor.

## The alternatives the routing demanded, measured

- **Superseded-record partition.** Status census over the 59 records: 55 `active`,
  1 `fulfilled`, 2 `superseded` — and both are superseded *in part* (5,400 B and 3,429 B),
  their standing halves still cited. Retiring them would free at most 8,829 B once, needs a
  new terminal family of its own, and buys about four records at the measured velocity.
- **A finite terminal for closed records.** This family IS memory layer C: a second location
  is a second memory, and every record is addressed by the INDEX row MEMORY-ARCH gates. The
  first record's grounds stand.
- **Duplicates.** None proved: FACT-OWNERSHIP and the INDEX gate are green over the family.

## The re-derived bound

The family's own 2× precedent, per-part untouched:

- `ceiling_lines` (files): 80 → **160**; `ceiling_bytes`: 262,144 → **524,288**.
- `health_lines`: 48 → **64**; `health_bytes`: 163,840 → **278,528** — just above the
  measured 62 files / 265,307 B, because a health target below the measurement is a
  warning that can never clear.
- `ceiling_part_bytes`: **16,384, unchanged**. The index is the member to watch: 13,234 B at
  59 rows, about 130 B per row, so it reaches the per-part ceiling near 83 rows. That bite is
  the signal for an index partition — its own transition, never a reason to raise the part.

## How to apply

The row in `doctrine/readme_routes.tsv` lands with this record in one commit, under
`LIVE-CONTAINMENT.4` slice (k). The next re-derivation waits for the next measured firing,
never ahead of it; the index partition lands when the per-part bites.
