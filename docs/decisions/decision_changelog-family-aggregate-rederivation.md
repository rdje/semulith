# Re-deriving the `docs/changelog/` aggregate bound — the shard family's content axis is a calendar too

- **Type:** `decision`
- **Date:** `2026-10-01`
- **Status:** `active`
- **Owner / source:** `README-ROUTING-CLOSURE` fired at `SEMULITH-BR-0012`'s pre-commit;
  `doctrine/readme_routes.tsv` requires a reviewed decision before any ceiling moves.
  Precedents: [`decision_task-tree-family-bound-rederivation.md`](decision_task-tree-family-bound-rederivation.md),
  [`decision_profiles-family-two-units.md`](decision_profiles-family-two-units.md), and the
  registry row's own three file-count re-derivations (`SEMILITH-PL-0001`/`-0012`,
  `SEMULITH-PS-0067`).

## What fired

```
OVER CEILING docs/changelog/: 396259 aggregate bytes > 393216
```

Over by **3,043 bytes**, caused by the commit in flight: `P3-BREADTH.4` slice 4's doc updates
pushed both append-history heads (CHANGELOG.md 66,441 > 65,536; DEV_NOTES.md 49,783 > 49,152)
over their ceilings in one commit, and the two resulting shard events (shards 0093, 0094 —
each one entry, completeness printed exact by `scripts/shard_history.py`) carried the frozen
family past its aggregate.

## Why the honest answer is not "compact something"

- The family is **frozen append-history**: SHARD-FREEZE hashes every shard and refuses any
  post-event edit, so shrinking a member is impossible by design, and merging shards is
  rewriting history the check exists to pin.
- The heads are separately capped (65,536 / 49,152 B) and shard when they fire — the family's
  input rate is governed there, not here.
- Batching more entries per shard event was examined and rejected **on the firing axis**:
  granularity moves bytes between the file-count axis and the per-part axis, but the aggregate
  measures content volume, which is invariant to how the partition is cut. The file-count axis
  has headroom (97/160) and is not the axis under pressure.
- The growth is mandated content — per-leaf completion evidence and technical notes that
  `COMMIT.md` requires at every commit — arriving at commit velocity.

## Why the contract genuinely expanded

The 384 KiB aggregate was calibrated `2026-09-27` against one head at adoption; the registry
row's own re-derivation comments named this day three times ("the next reader should watch the
AGGREGATE"). The family is the designed overflow for two capped append-only heads; both the
count axis and the byte axis are calendars for it. The invariants that protect content are
unchanged and are the real bounds: **per-part 64 KiB** (no member becomes a monolith) and the
**hash-pinned, append-only partition** (SHARD-FREEZE: coverage, frozen, append-only, unique —
the completeness proof lives at the shard event, printed by the tool and recorded in the tree).

## The decision

Aggregate ceiling **393,216 → 786,432 bytes** (2×, the family's own doubling precedent);
file-count ceiling **unchanged at 160** (97 now — the count is not the firing axis); per-part
**unchanged at 65,536**. The registry row's comment records this re-derivation. The next
reader should expect this axis to fire again at commit velocity — the trigger discipline
(`decision_readme-routing-closure`) stays: re-derive by reviewed decision, never widen quietly.

## How to apply

When `README-ROUTING-CLOSURE` reports the family over ceiling again: measure, check the
compaction alternatives honestly, and re-derive by a record like this one. Related:
[[decision_readme-routing-closure]], [[decision_task-tree-family-bound-rederivation]].
