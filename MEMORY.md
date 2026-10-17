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
- active_work_unit: `P4-SYSTEM.16` → its Current Frontier.
- **Active trees:** `CITATION-ACCURACY`, `LIVE-CONTAINMENT`, `LAB-BENCH`, `ARTIFACT-CLEANUP`, `P5-BOARD`, `P4-SYSTEM`.
- next_action: after P4-0249 normal COMMIT, continue RV64GC replay-bundle/reduction
  in P4-SYSTEM.16; JSON snapshot/resume and the snapshot evidence kind are delivered.
  P4.14 evidence qualification stays owned/open; CPU-SYSTEM remains incomplete.
  Priority correction/captured D79 receipt: docs/tasks/LIVE-CONTAINMENT.md,
  Delivery priority and capture handoff. Maintenance is scheduled separately.
- in_flight_uncommitted: none after P4-0249 normal COMMIT/postcheck.
- blockers: no terminal authorization needed; packet-20261017T225917Z-fbcd89
  captured480observations/155525packets,0unjudgeable. D79 causal analysis/LC0046
  D80 remain owned in LIVE-CONTAINMENT.4; no capture rerun is needed.
  Do not push below300commits without the director's act (`COMMIT.md`).
