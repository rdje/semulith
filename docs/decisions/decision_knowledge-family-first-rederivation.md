# The `docs/knowledge/` bounds re-derived — a card family grows by design, and its ceiling was exact

- **Type:** `decision`
- **Date:** `2026-10-22`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a42au, `SEMULITH-P4-0289` — the knowledge card
  `a-fixture-must-have-the-real-records-shape.md`, promoted from the a42au lesson as `LESSON-PROMOTION`
  requires, is the family's 31st file: `bash scripts/check_readme_routes.sh` prints
  `OVER CEILING docs/knowledge/: 31 files > 30` and `98585 aggregate bytes > 98304`
  (`target/p4-system-14/a42au/check_readme_routes.log`). Precedents and the rule for a raise under
  pressure: [`decision_profiles-family-corpus-second-rederivation.md`](decision_profiles-family-corpus-second-rederivation.md),
  [`decision_evidence-family-two-cases.md`](decision_evidence-family-two-cases.md) — reviewed, with the
  numbers, never silent.
answers: Why did the knowledge-card family's ceiling fire on a promoted lesson, and what bounds hold now?

## What was measured

Measured with `git ls-tree -r -l HEAD docs/knowledge/` and the working tree:

| When | Files | Bytes | Against 30 files / 98,304 B |
| --- | --- | --- | --- |
| adoption (the registry's own comment) | 4 | 6,834 | 0.133× / 0.070× |
| `830bdce` (2026-10-22), before a42au | 30 | 96,002 | **1.000×** / 0.977× |
| a42au staged: one card (2,326 B) and its index row (257 B) | 31 | 98,585 | **1.033× — over** on both axes |

The cards arrived in bursts on nine days between 2026-09-13 and 2026-10-06 (2, 7, 1, 5, 1, 1, 2, 4, 5),
one per promoted lesson. The health targets of 12 files and 20,480 B were passed in mid-September and
have printed on every run since; the ceilings sat exactly at the 2026-10-06 size. A health target the
family is above cannot warn, and a ceiling with no headroom fires on the first designed addition —
here on the very mechanism (`LESSON-PROMOTION`) the registry's own row names as the reason the
family exists.

## The re-derived bounds

| Axis | Was | Now | At staging |
| --- | --- | --- | --- |
| `ceiling_lines` (file count) | 30 | **40** | 31: 0.775× |
| `health_lines` | 12 | **34** | below: the line fires once more, three cards before the ceiling |
| `ceiling_bytes` (aggregate) | 98,304 (96 KiB) | **131,072** (128 KiB) | 98,585: 0.752× |
| `health_bytes` | 20,480 | **114,688** (112 KiB) | 0.860× of it |
| `ceiling_part_bytes` | 16,384 | **16,384** | unchanged; the largest member is the index at 6,719 B |

Nine more cards of the median size (3,2 KB) fit under the byte ceiling; the file ceiling admits nine.
The health targets sit at the standing ratio of their ceilings (0.85 and 0.875) and the family is
below both, which is what makes them warnings again.

## Why re-derive, and what the director may still choose

- The registry's rule is that a ceiling moves only by a reviewed decision in a task leaf; this record
  is that decision, owned by the leaf whose promoted lesson caused the crossing.
- A card family is `author_overflow`: lessons are routed into it on purpose, so its growth is the
  doctrine working. The registry's own calibration note says a hot-live target sits just above today's
  size and an append-history target near the ceiling; a card family behaves like the latter. The
  bounds above follow that reading.
- The director's alternative stands one row away, as for the task family
  ([`decision_containment-reset.md`](decision_containment-reset.md)): the aggregate and count ungoverned,
  per-part 16,384 kept. It applies on the director's word only; this record does not extend it.

## How to apply

- The next re-derivation is due when the health line fires (34 files or 114,688 B), raised before the
  ceiling by the leaf whose promoted lesson reaches it.
- A promoted lesson is never dropped to stay under a ceiling; the ceiling is the thing to review.
- Related: [[profiles-family-corpus-second-rederivation]], [[evidence-family-two-cases]],
  [[containment-reset]].
