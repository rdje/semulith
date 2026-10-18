# MEMORY — resume pointer (layer A; overwrite-only, keep ≤ ~50 lines)

> The bounded layer-A resume pointer (`MEMORY_ARCHITECTURE.md` §6). OVERWRITE "Current state"
> each update — never append. This file exists **solely to point at the next action** (director
> ruling `2026-10-02`, `decision_memory-next-action-pointer`); everything durable lives in the
> layers it points to.

## How to resume

1. Read `README.md`, `MEMORY_ARCHITECTURE.md`, `TOOLBOX.md`, `DOCTRINE_ENFORCEMENT.md`.
2. Open the active tree below → its Current Frontier → the next action.
3. Durable facts: `docs/decisions/INDEX.md`. Retrievable lessons: `docs/knowledge/INDEX.md`.

## Current state

- latest_commit: derive on read with `git log -1 --format='%H %s'`.
- active_work_unit: `P4-SYSTEM.14` → its Current Frontier.
- **Active trees:** `CITATION-ACCURACY`, `LIVE-CONTAINMENT`, `LAB-BENCH`, `ARTIFACT-CLEANUP`, `P5-BOARD`, `P4-SYSTEM`.
- next_action: P4-SYSTEM.14 source-value composition and producer/property
  binding. P4-0258 adds pure compare_source_expectation:23 controls/19 omissions,
  legacy52/14 exact,125 canonical matches/3794 steps;41 unsupported/one no-witness.
  Compose through authenticated retained baseline/source/image snapshots, with
  frozen producer/property authority before I/O. Keep unsupported event scope.
  Source/image, input/impact and snapshot author are implemented; do not repeat.
  Full canonical closure/review, property/collector adequacy, captures/retention
  and policy/status remain. Qualification closed; P4 14/18; replay4/4green.
- in_flight_uncommitted: none after P4-0258 normal COMMIT and postconditions.
- blockers: none for implementation; no terminal command needed.
  LIVE-CONTAINMENT.4 owns captured D79 analysis and D80; see that tree's
  Delivery priority and capture handoff. Maintenance remains scheduled separately.
  No push below300commits without the director's act (COMMIT.md).
