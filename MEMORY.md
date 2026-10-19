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
- next_action: after0282 normal COMMIT/brief0/exact postconditions/host census,
  own the next finite adequacy/policy slice on clean state. Read P4-SYSTEM.14,
  profiles/rv64gc-lab-v0/EVIDENCE_POLICY.md and canonical decision/model chapters.
  c91d08f5 retains the first actual DIV capture; teaching is synchronized. Preserve
  native declarations, all observations/results and historical records. Never rerun
  or overwrite that capture. Complete policy/qualification/status remain open.
- in_flight_uncommitted: verify Git state on read;0282 owns unfinished normal
  commit workflow under target/p4-system-14/a42an. No reference process this slice.
- blockers: none requiring director input. GC replay4/4green/.16 complete;
  CPU14/18 remains incomplete. D79/D80 remain in LIVE-CONTAINMENT.4; runtime P2
  in P4 a42ab. No push below300 without director's act (COMMIT.md).
  Cleanup next due2026-10-19T23:00:27Z.
