# Raising the `docs/tasks/` aggregate bound, and why that is not the reflex it looks like

- **Type:** `decision`
- **Date:** `2026-09-20`
- **Status:** `active`
- **Owner / source:** `README-ROUTING-CLOSURE` fired; `doctrine/readme_routes.tsv` requires a
  reviewed decision before any ceiling moves

## What fired

```
OVER CEILING docs/tasks/: 396273 aggregate bytes > 393216
```

Over by **3,057 bytes** — caused by the commit that was running when it fired.

## Why the honest answer is not "compact something"

Compaction was checked first, because raising a bound because it fired is exactly the reflex the
registry warns against:

- The three largest files are completed trees (`P0-PROFILE` 50,097 B, `MIRROR-DRIFT` 46,435 B,
  `SEMULITH-PKG` 40,140 B). Their content is completion evidence, not slack.
- `docs/tasks/archive/P0-PROFILE.md` was examined for duplication with its live tree and is
  **not** a duplicate — it is the evidence split out of it, complementary, under the same
  per-part rule.
- Moving completed trees into a subdirectory was considered and rejected **for a mechanical
  reason, not a preference**: `check_frontier_sync.sh` matches index links with
  `\(tasks/(?P<id>…)\.md\)`, a flat pattern. A subdirectory would break the mirror gate, and
  breaking a gate to satisfy a bound is a strictly worse trade.

## Why the contract genuinely expanded

The bound was derived at `SEMULITH-TREES.4`, when the family held **17 files / 133,074 B**. It
now holds **25 files / 396,273 B**, and the growth is in the number of *lanes the project tracks*,
not in verbosity per lane:

- two trees were created in this session alone on direct instruction — `PUSH-DISCIPLINE`
  (`2026-09-20`, push cadence) and `UPSTREAM-TRACK` (`2026-09-20`, upstream issues);
- `MODEL-METHOD` grew from 10 leaves to 13, `SOT-FORMAT` from 0 to 9, as the canonical-definition
  work found real defects that became owned leaves rather than notes.

⭐ **That is the contract expanding, which is the registry's own stated grounds for a raise.** A
bound derived when the project tracked 17 lanes does not describe a project that tracks 25.

## The new bounds, derived rather than padded

| Axis | Was | Now | Derivation |
| --- | --- | --- | --- |
| health files | 24 | 32 | today's 25 plus the seven milestone trees still `proposed`, which will each grow when started |
| health bytes | 192 KiB | 320 KiB | ~80% of the new ceiling, the band this registry's header prescribes for a hot family |
| ceiling files | 40 | 48 | 1.5× the health target, as before |
| ceiling bytes | 384 KiB | 640 KiB | 1.6× today's measurement — room for the seven unstarted milestones at the ~40 KiB a completed tree actually costs |
| **per-part** | 64 KiB | **64 KiB — unchanged** | this is the bound that bites, and it bit correctly once already (`P0-PROFILE` at 73,317 B, split on `2026-09-14`) |

⛔ **The per-part ceiling does not move.** The aggregate answers "how many lanes does this project
track"; the per-part answers "has one tree become a monolith". Only the first question changed.

## How to apply

- A tree that crosses **64 KiB** is still split, exactly as `P0-PROFILE` was. That rule is untouched.
- If the aggregate fires again without the number of tracked lanes having grown, the answer is
  compaction, not another raise — and this record is the baseline that makes the difference
  visible.

Related: [[decision_readme-routing-closure]].
