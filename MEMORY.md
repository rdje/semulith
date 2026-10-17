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
- next_action: LC.4i2b5b2r.d2 / LC0045 — user runs the one terminal command
  `python3 scripts/capture_book_dependencies.py`; inspect its capture for D79.
  One sudo tcpdump on owned lo0 ports; D80 is LC0046 afterward.
  Owner: docs/tasks/LIVE-CONTAINMENT.md current frontier.
  Resume P4-SYSTEM.14 a42 adequacy after the containment prerequisite.
- in_flight_uncommitted: none after LC0047 normal COMMIT/postcheck; app blocker below.
- blockers: terminal-authorized capture/analysis pending; D79 unresolved. Do not push below
  300 commits without the director's act (`COMMIT.md`).
  Final census flags Kimi Code PID5950 reading AGENTS.md; release/director ruling
  required for clean handoff. App left untouched; LC0047 owns this runtime blocker.
