# The `docs/knowledge/` bounds re-derived a second time — the health line fired four slices ago and the ceiling caught the fifth card

- **Type:** `decision`
- **Date:** `2026-10-27`
- **Status:** `active`
- **Owner / source:** `XTASK.6` slice 6r (its card, the lesson promoted as `LESSON-PROMOTION` requires, is the
  family's 41st file), `SEMULITH-XTASK-0031`. Precedent and rule: [`decision_knowledge-family-first-rederivation.md`](decision_knowledge-family-first-rederivation.md)
  (2026-10-22 — "the next re-derivation is due when the health line fires (34 files or 114,688 B), raised before the
  ceiling by the leaf whose promoted lesson reaches it"; "a promoted lesson is never dropped to stay under a ceiling").
answers: Why did the knowledge-card family's ceiling fire again five days after its first re-derivation, and what bounds hold now?

## What was measured

Measured with `git ls-tree -r -l HEAD docs/knowledge/` on `f3b3e612` (the 6r commit) and the staged card:

| When | Files | Bytes | Against 40 files / 131,072 B |
| --- | --- | --- | --- |
| first re-derivation staged (2026-10-22, a42au) | 31 | 98,585 | 0.775× / 0.752× |
| `f3b3e612` (2026-10-27), before the 6r card | 40 | 130,475 | **1.000×** / 0.995× |
| the 6r card (2,647 B) and its index row (288 B) staged | 41 | 133,410 | **1.025× / 1.018× — over** on both axes |

Ten cards arrived in the five days since the first re-derivation (1, 1, 1, 2, 5 on 2026-10-22, -23, -24, -26, -27), one per
promoted lesson, as the tooling port measured one driver per slice and found something in most. The health line (34 files,
114,688 B) fired at the 35th card on 2026-10-23 and printed on every gate since; four slices added cards above it without
re-deriving — the rule said the leaf whose lesson reaches the line raises the ceiling before it, and none did. The ceiling
caught the fifth (the 6r card, `README-ROUTES: OVER CEILING docs/knowledge/: 133410 aggregate bytes > 131072`), and the
card was deferred for one unit rather than dropped. This record is that late raise.

## The re-derived bounds

| Axis | Was | Now | At staging |
| --- | --- | --- | --- |
| `ceiling_lines` (file count) | 40 | **56** | 41: 0.732× |
| `health_lines` | 34 | **48** | below: the line fires again seven cards before the ceiling |
| `ceiling_bytes` (aggregate) | 131,072 (128 KiB) | **180,224** (176 KiB) | 133,410: 0.740× |
| `health_bytes` | 114,688 (112 KiB) | **157,696** (154 KiB) | 0.846× of it |
| `ceiling_part_bytes` | 16,384 | **16,384** | unchanged; the largest member is the index at 10,716 B |

Fourteen more cards of the median size (3.2 KB) fit under the byte ceiling; the file ceiling admits fifteen. The health
targets keep the standing ratios of their ceilings (0.857 and 0.875) and the family is below both, which is what makes
them warnings again. The headroom (0.73×) is the precedent's (0.75×), not more: a card family that gains two cards a
day under a measuring port will reach the next line in weeks, and the rule stands — the leaf that reaches it raises.

## Why re-derive, and what the director may still choose

- The registry's rule is that a ceiling moves only by a reviewed decision in a task leaf; this record is that decision,
  owned by the leaf whose promoted lesson caused the crossing, as the precedent was.
- The family is `author_overflow` / `partitioned`: lessons are routed into it on purpose, and the routes check walks the
  directory recursively, so a sub-directory partition would not move the aggregate; a sibling family would need its own
  route row and would split the index `LESSON-PROMOTION` requires. A raise is the mechanism the registry gives this
  class; the director's alternative (the aggregate and count ungoverned, per-part kept —
  [`decision_containment-reset.md`](decision_containment-reset.md)) applies on the director's word only.
- The late raise is recorded, not hidden: the health line is advisory and printed; it was read as noise. **How to apply**
  below makes it a check the slice runner performs.

## How to apply

- The next re-derivation is due when the health line fires (48 files or 157,696 B), raised before the ceiling by the leaf
  whose promoted lesson reaches it — and a slice that adds a card reads `bash scripts/check_readme_routes.sh`'s
  `health: docs/knowledge/` lines in its prechecks, not only its verdict.
- A promoted lesson is never dropped to stay under a ceiling; a card deferred for the raise lands with the raise.
- Related: [[knowledge-family-first-rederivation]], [[containment-reset]], [[profiles-family-corpus-second-rederivation]].
