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
- active_work_unit: `LIVE-CONTAINMENT.4` → its Current Frontier.
- **Active trees:** `CITATION-ACCURACY`, `LIVE-CONTAINMENT`, `LAB-BENCH`, `ARTIFACT-CLEANUP`, `P5-BOARD`, `P4-SYSTEM`.
- next_action: adopt the project-owned containment contract and measured
  inventory, then resolve task-family capacity under LC.4. Resume P4-SYSTEM.14
  a42 adequacy after that prerequisite. Read LC.4's frontier before choosing.
- in_flight_uncommitted: none after LC-0009 COMMIT; results and canonical
  routes are in `docs/tasks/LIVE-CONTAINMENT.md` .4f. D49 is committed in
  `docs/tasks/P4-SYSTEM.md` a42l2.
- blockers: none. Do not push below the 300-commit cadence without the
  director's act; authority and procedure: `COMMIT.md`.
