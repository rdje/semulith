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

- latest_commit: `git log -1`. ⛔ **Do not push** below the 300-commit cadence without the
  director's `scripts/approved_push.sh` act (`decision_push-cadence`) —
  `scripts/check_push_cadence.sh --status` says where we stand.
- **Active trees:** `LAB-BENCH` (1/2 — `.2` feedback-gated) · `ARTIFACT-CLEANUP` (recurring §8; last run `2026-10-02`) · `BOOK-APPARATUS` (1/2 — `.2` the reading-experience audit).
  Milestone frontier: `P5-BOARD` (proposed).
- next_action: `P5-BOARD.1` — the platform specification (gate `BOARD`): compose `rv64i-lab-v0`
  v0 (the EXPERIMENTAL release, `decision_release-rv64i-lab-v0`) with sourced devices; the five
  network-device candidates and five measured negatives are reconciled (`P5-BOARD.8`/`.9`);
  contract design starts now, board execution follows CPU validation (`ROADMAP.md` §P5). Then:
  `BOOK-APPARATUS.2`.
- in_flight_uncommitted: `BOOK-APPARATUS.1`'s files — the leaf is complete on disk; its commit
  was blocked by the append-head ceilings (sharded, `SEMULITH-DS-0004`) and lands next.
- blockers: none (0 open upstream issues — `scripts/upstream_exposure.py`; never patch the
  submodule, adopt by moving the pin).
