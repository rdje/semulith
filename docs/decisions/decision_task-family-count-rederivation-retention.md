# Raising the `docs/tasks/` count bound a fourth time — the retention continuation the per-part ceiling forced

- **Type:** `decision`
- **Date:** `2026-10-20`
- **Status:** `active`
- **Owner / source:** `LIVE-CONTAINMENT.4` slice (l), `SEMULITH-LC-0051`; `README-ROUTING-CLOSURE`
  reports `OVER CEILING docs/tasks/: 108 files > 107` when the first complete-records
  continuation artifact is added. Precedents:
  [`decision_task-tree-family-count-rederivation.md`](decision_task-tree-family-count-rederivation.md)
  (`2026-10-01`: the count axis counts the partition lifecycle) and
  [`decision_task-family-six-activity-count.md`](decision_task-family-six-activity-count.md)
  (`2026-10-12`: count 107 = 33 instances + 1 template + 33 archive allowance + 40 artifact envelope).

## What fired

At `a658e24` the family holds 107 files = 33 instances + 1 template + 42 archive parts +
31 artifacts — the ceiling, reached on `2026-10-12` itself, the day the 107 authority was
applied (nine `LIVE-CONTAINMENT` artifacts and two of its archive parts landed that day;
no file has joined the family in the eight days since). Three members sit at the per-part
ceiling: `P4-SYSTEM.md` 130,889 B, `task-claims.md` 131,005 B and
`reader-records-retention.md` 131,043 B of 131,072. Every retention destination is full: the
one complete-records artifact has 67 B left, the 42 archive parts are immutable under
TASK-PRESERVATION, and `docs/task-history/` (3 of 3) and `docs/history/` (4 of 4) stand at
their counts. The next P4 record (about 2 KB) and this tree's own next record cannot land.
The forced file is `task-claims-2.md`: the continuation of the complete-records artifact
that its per-part ceiling split — the partition lifecycle the count axis counts.

## Composition, measured — the 33 IDs rechecked

`git ls-files docs/tasks | wc -l` → **107**: the same 33 instance IDs as the `2026-10-12`
authority, TEMPLATE.md, 42 archive parts (nine above the 33 allowance, each forced by the
per-part rule), 31 artifacts (nine below the 40 envelope). Growth since the last authority is
+2 archive parts and +9 artifacts, both designed mechanisms, and it consumed the pooled 11.

## Why the honest answer is not "compact something"

- The six-activity record's own rule: a count firing *without* composition growth means
  compaction. The composition grew by the two designed mechanisms; the live trees are already
  pointer-level (the LC `.4h` records and the P4 `a` records are stubs over retained spans).
- Trimming the live narratives to fit is the containment doctrine's named anti-pattern, and
  the P4 unit `SEMULITH-P4-0283` already refused "count 108" and a frozen-part append; it fit
  only because 2,184 B of room remained in the one artifact. That room is gone.
- Moving artifacts or archives out of the family is the unbounded destination the registry's
  header names as the dodge.
- Sealing closed parts into `docs/task-history/` is the sustainable transition for the
  aggregate axis (3,128,989 of 3,145,728 B, 99.5 %) and is owned separately as
  `LIVE-CONTAINMENT.4` slice (m); it needs its own authority and does not remove the need for
  a live continuation artifact.

## The re-derived bound

| Axis | Was | Now | Derivation |
| --- | --- | --- | --- |
| ceiling files | 107 | **116** | 33 instances + 1 template + 42 measured archive parts + the reviewed 40-artifact envelope |
| health files | 64 | **64 — unchanged** | occupancy stays warning debt owned by `LIVE-CONTAINMENT.4` |
| ceiling bytes | 3,145,728 | **unchanged** | the aggregate did not fire; it is a seal's question (slice m), never a raise here |
| per-part | 131,072 | **unchanged** | it bit correctly: it forced this continuation |

## How to apply

The row lands with this record in one commit. A continuation artifact is cut only when the
previous one cannot hold the next whole record, and each cut retains source/owner/retired
inverses in the continuation itself. The next count firing without composition growth is
compaction; the aggregate axis is answered by the slice (m) seal before it fires.
