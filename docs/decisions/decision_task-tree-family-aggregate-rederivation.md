# Raising the `docs/tasks/` aggregate byte bound — an active multi-slice tree's mandated narrative is the designed growth

- **Type:** `decision`
- **Date:** `2026-10-03`
- **Status:** `active`
- **Owner / source:** `README-ROUTING-CLOSURE` fired at `SEMULITH-P4-0009`'s commit;
  `doctrine/readme_routes.tsv` requires a reviewed decision before any ceiling moves.
  Precedents: [`decision_task-tree-family-bound.md`](decision_task-tree-family-bound.md),
  [`decision_task-tree-family-bound-rederivation.md`](decision_task-tree-family-bound-rederivation.md),
  [`decision_task-tree-family-count-rederivation.md`](decision_task-tree-family-count-rederivation.md),
  [`decision_task-tree-per-part-growth.md`](decision_task-tree-per-part-growth.md)
  (the per-part raise to 128 KiB), and the registry row's comment trail.

## What fired

```
OVER CEILING docs/tasks/: 1575182 aggregate bytes > 1572864
```

## Composition, measured

`find docs/tasks -type f | wc -l` → **63**; the aggregate **1,575,182 B** (100.15% of the
1.5 MiB ceiling). The firing content is `P4-SYSTEM.md` at 103,222 B — an ACTIVE tree
carrying the mandated per-slice acceptance checklists (six boxes each, tool output in
every box) for slices (a)–(e) of `P4-SYSTEM.2`, landed the same day alongside the `.1`
resolution and two design briefs. The per-part ceiling did NOT fire (103,222 < 131,072,
and the largest member is an active tree, not a monolith). The count axis did NOT fire
(63 < 96).

## The re-derivation

The aggregate axis answers "how much tracked evidence the project carries" — that answer
grew by design: the P4-SYSTEM leaf's slice discipline is exactly the evidence the family
exists to hold, and the `.1` discipline (condense at write time) was already applied.
Following the house shape (the `2026-09-30` aggregate re-derivation and the changelog
family's): the aggregate re-derives 1.5 MiB → **3 MiB (3,145,728 B)**; per-part stays
131,072 B and the count axis stays 96 — they did not fire. The registry row's comment
trail records the firing measurement.

## What does not change

- The archives stay and the archive option stays — a tree that grows past readability may
  still shed completed-leaf evidence by the P2-SCALAR precedent; the per-part did not
  force it here.
- This is the aggregate's second firing; each firing gets its own measurement, never a
  running total.
