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
- next_action: LC.4i2b4 — qualify index/query expansion after LC0030 COMMIT.
  D65/D68 fixed; full graph/adoption and CPU qualification remain open.
  Owner: docs/tasks/LIVE-CONTAINMENT.md current frontier.
  Resume P4-SYSTEM.14 a42 adequacy after the containment prerequisite.
- in_flight_uncommitted: none after LC0030 normal COMMIT; full adoption remains LC.4.
- blockers: none. Do not push below the 300-commit cadence without the
  director's act; authority and procedure: `COMMIT.md`.
