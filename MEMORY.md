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
- active_work_unit: `P4-SYSTEM.14` → complete source/risk/feature policy and status integration.
- **Active trees:** `CITATION-ACCURACY`, `LIVE-CONTAINMENT`, `LAB-BENCH`, `ARTIFACT-CLEANUP`, `P5-BOARD`, `P4-SYSTEM`.
- next_action: after0281 normal COMMIT/brief0/exact postconditions/host census,
  own the next finite policy-adequacy slice on clean state. Read P4-SYSTEM.14,
  EVIDENCE_POLICY.md and model canonical-division/capture-plan teaching. Preserve
  b160c66e native declarations and all actual retained observations/results.
  Do not rerun canonical capture or overwrite historical data. Complete policy/
  qualification, status derivation and remaining evidence stay open; no CPU credit.
- in_flight_uncommitted: verify Git state on read;0281 owns unfinished commit
  workflow under target/p4-system-14/a42am. Capture_calls=1: never retry after reset.
- blockers: none requiring director input. Canonical capture complete, independent
  and copied offline checks pass. D79/D80 remain in LIVE-CONTAINMENT.4;
  runtime P2 in P4 a42ab. No push below300 without director's act (COMMIT.md).
