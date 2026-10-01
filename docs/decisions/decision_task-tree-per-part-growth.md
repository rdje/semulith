# Raising the `docs/tasks/` per-part bound — the director authorizes task-tree growth

- **Type:** `decision`
- **Date:** `2026-10-01`
- **Status:** `active`
- **Owner / source:** **director ruling, `2026-10-01`** — "You should allow increasing the size of
  task-trees!", delivered mid-flight during `P3-BREADTH.6` slice 2.
  `doctrine/readme_routes.tsv` requires a reviewed decision before any ceiling moves; the ruling
  is the review. Supersedes the per-part row of
  [`decision_task-tree-family-bound-rederivation.md`](decision_task-tree-family-bound-rederivation.md)
  (`2026-09-28`), which held the per-part at 64 KiB ("the bound that bites … bit correctly").

## What was happening when the ruling arrived

`P3-BREADTH.md` crossed the 64 KiB per-part bound **six times in one day** (`2026-10-01`), each
crossing forcing a verbatim archive operation mid-flight, during active slices:

1. `.2`/`.4` checklists → `archive/P3-BREADTH.md` (the initial split);
2. `.5` slices 1–2 checklists (slice-2 bookkeeping);
3. `.5` slice 3's checklist (slice-3 bookkeeping);
4. `.7` slice 1's checklist (slice-1 bookkeeping);
5. `.7` slice 3's checklist **and the tree's Design Discussions** (`.6` slice-1 bookkeeping);
6. `.6` slice 1's checklist **and `.7`'s slice narratives** (`.6` slice-2 bookkeeping) — the `.7`
   narratives were archived **the same day they were written**.

## Why the old argument no longer holds

The `2026-09-28` record's case for an unmoving per-part was that it "bit correctly": it forced
the `P1-LAB` split, and the split was judged healthy. That judgement predates the multi-slice
tree. Measured against `2026-10-01`:

- **The bound now taxes active work, not completed evidence.** Every crossing above fired while
  a slice was mid-flight, and two of them archived *active* content — the `.7` slice narratives
  and the tree's design discussions — within hours of authorship. The lifecycle the family row
  describes ("completed-leaf evidence archived in-tree") had inverted: the live tree was no
  longer the place a reader meets the current work.
- **The archiving itself became the overhead.** Six archive operations in one day, each with its
  pointer bookkeeping, in slices that were otherwise about the BREADTH milestone — pressure of
  the instrument, not of the content. The content is mandated narrative (per-slice records,
  checklists, lessons), already condensed by rule; there was nothing left to compact.
- **The bound was calibrated to a smaller tree.** At adoption the largest member was
  `P0-PROFILE.md` at 50,097 B; an active multi-slice tree now carries 70–80 KB of mandated
  narrative before its first leaf closes.

The director's ruling resolves it directly: task-tree growth is **allowed**. The per-part is the
axis that answers "may one tree grow", and the answer changed.

## The new bound

| Axis | Was | Now | Derivation |
| --- | --- | --- | --- |
| per-part bytes | 65,536 (64 KiB) | **131,072 (128 KiB)** | 2× — the house re-derivation shape (`decision_profiles-family-two-units`, `decision_changelog-family-aggregate-rederivation`); ~1.7× the largest unarchived tree measured this day, with headroom for a full milestone tree's mandated narrative |
| ceiling files / aggregate bytes | 96 / 1,572,864 | unchanged | the aggregate answers "how many lanes does the project track" — that question did not change (the `2026-09-28` record's own axis split) |

## What does not change

- **The archives stay, and the option stays.** The splits already made (`P0-PROFILE`,
  `SOT-FORMAT`, `MODEL-METHOD`, `P1-LAB`, `P3-BREADTH`) are legitimate lifecycle and are NOT
  undone; a tree that grows past readability may still archive completed evidence by the same
  precedent. The difference is that 64 KiB no longer *forces* the split mid-flight.
- **The aggregate bound and its review discipline** — raising any bound still needs a reviewed
  decision; this record is the per-part's.
- **The mandated content rules** — per-slice records, checklists with tool output in each box,
  lessons with promotion verdicts. Growth is permitted; padding is not licensed.

Related: [[decision_task-tree-family-bound]],
[[decision_task-tree-family-bound-rederivation]], [[decision_readme-routing-closure]].
