# Raising the `docs/tasks/` count bound — the partition lifecycle and the evidence archives are the family's designed file growth

- **Type:** `decision`
- **Date:** `2026-10-01`
- **Status:** `active`
- **Owner / source:** `README-ROUTING-CLOSURE` fired at `SEMULITH-BR-0015`'s commit;
  `doctrine/readme_routes.tsv` requires a reviewed decision before any ceiling moves.
  Precedents: [`decision_task-tree-family-bound.md`](decision_task-tree-family-bound.md)
  (`2026-09-20`),
  [`decision_task-tree-family-bound-rederivation.md`](decision_task-tree-family-bound-rederivation.md)
  (`2026-09-28`), and the `2026-09-30` aggregate re-derivation recorded in the registry row's
  comment (`SEMULITH-DR-0090`).

## What fired

```
OVER CEILING docs/tasks/: 61 files > 60
```

At the `SEMULITH-BR-0015` (leaf `P3-BREADTH.5` slice 2) commit. The firing files are three:
`docs/tasks/archive/P3-BREADTH.md` — the archive the per-part ceiling FORCED in the same
commit (the tree crossed 64 KiB and split, exactly as designed) — and the two drafted DSP
dossier documents under `docs/tasks/artifacts/p3-breadth/dsp56300-dossier/`, the family's
designed evidence growth. **The count axis must count the partition lifecycle itself: every
per-part split adds a file to the family, by design.**

## Composition, measured

`git ls-files docs/tasks | wc -l` → **61** at the firing commit: **28** live tree files,
**9** archive parts (`P0-PROFILE`, `SOT-FORMAT`, `MODEL-METHOD`, `P1-LAB` ×2, `P2-SCALAR` ×2,
`MODEL-BOOKS`, `P3-BREADTH`), **24** evidence-artifact files (probe drivers, surveys, census
records, the dossier drafts). The `2026-09-30` derivation counted 43 files — the growth since
is 9 archive parts and artifact documents, i.e. the two designed mechanisms, not prose.

## Why the honest answer is not "compact something"

- The archives are unedited mandated checklists split out by the per-part rule — the family's
  own row describes this lifecycle ("completed-leaf evidence archived in-tree"). Each was
  examined at its split for duplication (complementary to its live tree, never a copy).
- The artifacts are the per-leaf evidence the acceptance doctrine mandates; the drafts are
  `P3-BREADTH.5` slice 2's measured content, waiting to land governed.
- Rejected alternatives, with reasons: **moving the artifacts or archives out of the family**
  (an unbounded destination is the dodge the checker's header names); **folding the two draft
  documents into one file** (they are two schema documents for two schemas — a false economy
  that the landing slice would immediately undo); **raising the per-part** (it bit correctly
  again today — the `P3-BREADTH` split is the sixth proof; the per-part answers "has one tree
  become a monolith" and nothing about that question changed).

## The new bounds, derived rather than padded

| Axis | Was | Now | Derivation |
| --- | --- | --- | --- |
| health files | 48 | 64 | the two-thirds band below the new ceiling, the ratio that has fired usefully |
| ceiling files | 60 | 96 | 28 live trees + one archive part per tree as each crosses 64 KiB (28, nine exist today) + ~40 evidence-artifact files at the measured accumulation (24 today; six milestone trees unstarted, and `P3-BREADTH` alone holds 15) |
| health bytes | 1.1 MiB | unchanged | the byte axis did not fire (1.21 MB against the 1.5 MiB ceiling) |
| ceiling bytes | 1.5 MiB | unchanged | the byte axis did not fire |
| **per-part** | 64 KiB | **64 KiB — unchanged** | the bound that bites; it bit correctly today (the `P3-BREADTH` split) |

⛔ **The per-part ceiling does not move.** Only the count axis's answer changed — "how many
lanes, archive parts, and evidence artifacts the project tracks" grew by design.

## How to apply

- A tree that crosses **64 KiB** is still split, exactly as the six existing archives were.
  That rule is untouched.
- If the count axis fires again **without the tree/archive/artifact composition having
  grown**, the answer is compaction, not another raise — the composition line above is the
  baseline that makes the difference visible.

Related: [[decision_task-tree-family-bound]],
[[decision_task-tree-family-bound-rederivation]],
[[decision_changelog-family-aggregate-rederivation]].
