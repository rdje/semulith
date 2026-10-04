# Re-deriving the `docs/changelog/` file-count bound — the count axis is the calendar the byte axis already was

- **Type:** `decision`
- **Date:** `2026-10-04`
- **Status:** `active`
- **Owner / source:** `README-ROUTING-CLOSURE` fired at `SEMULITH-P4-0016`'s pre-commit;
  `doctrine/readme_routes.tsv` requires a reviewed decision before any ceiling moves.
  Precedents: [`decision_changelog-family-aggregate-rederivation.md`](decision_changelog-family-aggregate-rederivation.md)
  (the byte axis, eight days ago) and the registry row's own three earlier
  file-count re-derivations (`SEMILITH-PL-0001`/`-0012`, `SEMULITH-PS-0067`).

## What fired

```
OVER CEILING docs/changelog/: 161 files > 160
```

The commit in flight (`P4-SYSTEM.3` slice (b), `SEMULITH-P4-0016`) sharded both
append-history heads as `COMMIT.md` requires (shards 0157, 0158 — completeness printed
exact by `scripts/shard_history.py`), carrying the family from 159 to 161 members.

## The measurement

The 2026-10-01 aggregate re-derivation recorded the count at **97/160** with the note
"the count is not the firing axis". Three days later the count is 161: **~21 files/day**
at the current leaf velocity (the `P4-SYSTEM` leaf runs shard both heads per slice
commit, and 2026-10-03 ran eleven slice commits across two trees — `git log --since=
2026-10-02 -- docs/changelog/`). The byte axis is NOT under pressure: 580,654 / 786,432
aggregate bytes (74%) — the two axes measure different things, and today the count is
the calendar that fired, exactly the inversion of the 2026-10-01 firing.

## Why the honest answer is not "compact something"

- The family is **frozen append-history**: SHARD-FREEZE hashes every shard and refuses
  any post-event edit — shrinking a member is impossible by design, and merging shards
  is rewriting history the check exists to pin.
- Coarser shard granularity (more entries per event) was examined and rejected on the
  same ground the 2026-10-01 record stated it: granularity moves files between the
  count axis and the per-part axis, but it does not reduce CONTENT, and the per-part
  64 KiB bound is the monolith protection, not a knob.
- The growth is mandated content — per-leaf completion evidence and technical notes
  that `COMMIT.md` requires at every commit — arriving at commit velocity.

## The decision

File-count ceiling **160 → 320** (2×, the family's own doubling precedent; ~15 days of
headroom at the measured ~21 files/day — the next firing is expected and is the
discipline working, not failing). Aggregate byte ceiling **unchanged at 786,432**;
per-part **unchanged at 65,536**; health re-measured at 161 files / 580,654 B. The
invariants that protect content are unchanged and are the real bounds: **per-part
64 KiB** (no member becomes a monolith) and the **hash-pinned, append-only
partition** (SHARD-FREEZE: coverage, frozen, append-only, unique — the completeness
proof lives at the shard event, printed by the tool and recorded in the tree). The
registry row's comment records this re-derivation; the trigger discipline
(`decision_readme-routing-closure`) stays: re-derive by reviewed decision, never widen
quietly.

## How to apply

When `README-ROUTING-CLOSURE` reports the family over ceiling again: measure both axes,
check the compaction alternatives honestly, and re-derive by a record like this one.
Related: [[decision_readme-routing-closure]],
[[decision_changelog-family-aggregate-rederivation]],
[[decision_task-tree-family-aggregate-rederivation]].
