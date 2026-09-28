# Raising the `docs/tasks/` aggregate bound again — lanes grew, and the evidence archives are the family's designed growth

- **Type:** `decision`
- **Date:** `2026-09-28`
- **Status:** `active`
- **Owner / source:** `README-ROUTING-CLOSURE` fired at `SEMILITH-PL-0009`; `doctrine/readme_routes.tsv` requires a reviewed decision before any ceiling moves. Precedent: [`decision_task-tree-family-bound.md`](decision_task-tree-family-bound.md) (`2026-09-20`).

## What fired

```
OVER CEILING docs/tasks/: 665577 aggregate bytes > 655360
```

Over by **10,217 bytes** — caused by the commit that was running when it fired. That commit also
obeyed the per-part ceiling for the first time on this tree: `P1-LAB.md` crossed 64 KiB and its
`.1`–`.8` acceptance checklists archived verbatim to `docs/tasks/archive/P1-LAB.md` (the
`SOT-FORMAT` precedent). **Both axes of the same family were under pressure in one commit —
the per-part did its job, and the aggregate then correctly reported that the family has grown.**

## Why the honest answer is not "compact something"

Compaction was checked first, because raising a bound because it fired is exactly the reflex the
registry warns against:

- The four largest live files are `P1-LAB` (61,187 B), `SOT-FORMAT` (60,335 B), `MODEL-METHOD`
  (57,839 B), `P0-PROFILE` (50,097 B). Their content is per-leaf completion evidence that
  `DOCTRINE_ENFORCEMENT.md` / `TASK-ACCEPTANCE` mandate per done leaf — not slack.
- The four `archive/` members (141,641 B of the family) are the unedited checklists split out of
  live trees by the per-part rule — the family's own row describes this as the designed
  lifecycle ("completed-leaf evidence archived in-tree"). Examined for duplication: each archive
  is complementary to its live tree, not a copy.
- At the parent commit of the firing commit, the family already measured **650,673 B** — 4,687
  bytes under the ceiling. Any leaf landing this week would have fired it; this leaf is the one
  that arrived when the tank was full. That is a miscalibrated bound, not a sudden bloat.

Rejected alternatives, with reasons: **moving the archives out of the family** (an unbounded
destination is the dodge the checker's own header warns about — "splitting a monolith without
bounding the resulting collection just moves the same append pressure one level down", and
`docs/provenance/` is frozen — never an overflow destination); **raising the per-part** (the
per-part is the bound that bites, and it bit correctly here — "an expanded contract re-derives
the count axis, never the per-part one").

## Why the contract genuinely expanded

The bound was re-derived at `UPSTREAM-TRACK.1` (`2026-09-20`), when the family held **25 files /
396,273 B**. It now holds **32 files / 665,577 B** (+28% files, +68% bytes), and the growth is
two designed mechanisms, not verbosity per lane:

- **Lanes were added after the derivation:** `ARTIFACT-CLEANUP` (`2026-09-26`), `DOC-SHARDING`,
  `ROADMAP-V3`, `PORT-WEB` (all `2026-09-27`), plus three new evidence archives
  (`SOT-FORMAT`, `MODEL-METHOD`, `P1-LAB`) and the `docs/tasks/artifacts/` probe drivers —
  seven files the `2026-09-20` derivation never counted.
- **Completed-leaf evidence accumulated inside existing lanes:** `P1-LAB` went from 8 to 9 done
  leaves between the two measurements and carries 61 KiB live + 31 KiB archived; `SOT-FORMAT`
  completed 10 leaves. Each done leaf's checklist is mandated evidence, so per-lane growth of
  this shape continues for every leaf of every active tree (`P1-LAB` has 3 leaves still open;
  six milestone trees are unstarted).

⭐ **The `2026-09-20` record's own test is met:** the lane count grew (25 → 32), and the growth
is in the number of lanes the project tracks plus their designed evidence lifecycle, not in
prose per lane. Its caveat is carried forward verbatim below.

## The new bounds, derived rather than padded

| Axis | Was | Now | Derivation |
| --- | --- | --- | --- |
| health files | 32 | 40 | today's 32 plus the trees still starting (`P2-SCALAR` opened with P1's gate; six milestones remain `proposed`) |
| health bytes | 320 KiB | 512 KiB | the `2026-09-20` ratio kept — health at half the ceiling, the band that fired usefully here (650 KiB against a 640 KiB ceiling warned nobody early enough, which this health row exists to fix) |
| ceiling files | 48 | 60 | headroom for the six unstarted milestone trees plus their evidence archives |
| ceiling bytes | 640 KiB | 1 MiB | today's 665,577 B plus ~380 KiB of designed growth — roughly five more completed trees/archives at the measured per-tree cost (~60–80 KiB live + archive) — forcing the next re-derivation around P2/P3, when the lane question is reviewed again rather than pre-authorized forever |
| **per-part** | 64 KiB | **64 KiB — unchanged** | this is the bound that bites, and it bit correctly on `2026-09-28` (the `P1-LAB` split it forced is the proof it works) |

⛔ **The per-part ceiling does not move.** The aggregate answers "how many lanes does this project
track"; the per-part answers "has one tree become a monolith". Only the first question changed.

## How to apply

- A tree that crosses **64 KiB** is still split, exactly as `P0-PROFILE`, `SOT-FORMAT`,
  `MODEL-METHOD`, and `P1-LAB` were. That rule is untouched.
- If the aggregate fires again **without the lane count having grown**, the answer is
  compaction, not another raise — and the `2026-09-20` record plus this one are the baselines
  that make the difference visible.

Related: [[decision_task-tree-family-bound]], [[decision_readme-routing-closure]].
