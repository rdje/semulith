# The `schema/` and `docs/decisions/` bounds re-derived — a schema per catalogue, an index row per record

- **Type:** `decision`
- **Date:** `2026-10-23`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a42ay, `SEMULITH-P4-0293` — the credit catalogue's schema
  `schema/credits.sexp` is the schema family's 25th file and the decision records of a42ax/a42ay (this one included) are
  the decisions index's 73rd to 75th rows: `bash scripts/check_readme_routes.sh` printed
  `OVER CEILING schema/: 25 files > 24` and `OVER CEILING docs/decisions/: part docs/decisions/INDEX.md`
  (`target/p4-system-14/a42ay/check_readme_routes.log`). Precedents and the rule for a raise under
  pressure: [`decision_knowledge-family-first-rederivation.md`](decision_knowledge-family-first-rederivation.md),
  [`decision_evidence-family-two-cases.md`](decision_evidence-family-two-cases.md) — reviewed, with the
  numbers, never silent.
answers: Why did the schema family's file ceiling and the decisions index's part ceiling fire on one slice, and what bounds hold now?

## What was measured

Measured with `git ls-tree -r -l HEAD` (commit `818b873`, 2026-10-23) and the working tree:

| Family | Axis | At HEAD | Staged (a42ay) | Old bound |
| --- | --- | --- | --- | --- |
| `schema/` | files | 24 | 25 | ceiling **24**, health 18 (passed 2026-10-02) |
| `schema/` | aggregate bytes | 135,259 | 137,197 | ceiling 524,288, health 131,072 (passed) |
| `schema/` | largest member | 28,465 (`semantics.sexp`) | unchanged | per-part 65,536 |
| `docs/decisions/` | files | 72 | 74 | ceiling 160, health 64 (passed) |
| `docs/decisions/` | aggregate bytes | 313,986 | 323,698 | ceiling 524,288, health 278,528 (passed) |
| `docs/decisions/` | `INDEX.md` | 16,127 | 16,537, then 16,869 with this record's row | per-part **16,384** |
| `docs/decisions/` | next largest members | 16,267 and 16,112 (two contract records the book includes verbatim) | unchanged | per-part 16,384 |

The schema family grew on seven days between 2026-09-26 and 2026-10-11 (1, 5, 1, 1, 3, 2, 1 files), one
schema per catalogue or source-of-truth family, and had sat exactly at its ceiling since; the index of
the decisions family grows by one row per record, so its per-part ceiling was an aggregate bound in
disguise, 257 B from firing at HEAD, with two records of their own 117 and 272 B from it.

## The re-derived bounds

| Row | Column | Was | Now | At staging |
| --- | --- | --- | --- | --- |
| `schema/` | `ceiling_lines` (files) | 24 | **32** | 25: 0.78× |
| `schema/` | `health_lines` | 18 | **27** | below: warns again, two schemas before the ceiling |
| `schema/` | `health_bytes` | 131,072 | **262,144** | 137,197: 0.52× |
| `schema/` | `ceiling_bytes` / `ceiling_part_bytes` | 524,288 / 65,536 | unchanged | 0.26× / 0.73× |
| `docs/decisions/` | `ceiling_part_bytes` | 16,384 | **32,768** | the index at 0.51×; the two contract records at 0.50× |
| `docs/decisions/` | `health_lines` (files) | 64 | **136** | 74: 0.54× |
| `docs/decisions/` | `health_bytes` | 278,528 | **458,752** | 323,698: 0.71× |
| `docs/decisions/` | `ceiling_lines` / `ceiling_bytes` | 160 / 524,288 | unchanged | 0.46× / 0.62× |

Seven more schemas fit under the file ceiling; the index admits about seventy more rows of today's
median length before its new part ceiling. Health targets sit at the standing ratio of their ceilings
(0.84–0.875) and both families are below them, which is what makes them warnings again.

## Why re-derive, and what the director may still choose

- A schema per catalogue is the schema layer's design (`SOT-FORMAT.1`: declaring a new construct is
  data in `schema/`); the 25th file is the credit catalogue the policy demands. A family ceiling that
  fires on the designed addition, with no health warning possible because the health line was passed
  three weeks earlier, is the miscalibration the registry's own note describes.
- The decisions index is the family's bounded index; its length is the record count. A per-part ceiling
  that the index reaches first governs the family's count through the wrong axis. Doubling it keeps every
  record and the index under one bound while the count ceiling (160) remains the governing one.
- The director's alternative stands one row away, as for the task family
  ([`decision_containment-reset.md`](decision_containment-reset.md)): aggregate and count ungoverned,
  per-part kept. It applies on the director's word only; this record does not extend it.

## How to apply

- `doctrine/readme_routes.tsv` rows `schema/` and `docs/decisions/` carry the bounds above; the
  registry mirror and `check_readme_routes.sh` enforce them on every commit.
- The next crossing of either family is a new measurement and a new record, not an edit to this one.
