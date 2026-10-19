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
- next_action: after0283 normal COMMIT/brief0/exact postconditions/host census,
  own the next finite policy/status slice on clean state. Read P4-SYSTEM.14,
  EVIDENCE_POLICY and method-adequacy model chapter. review_div_method checks
  finite method satisfied, full policy pending/replay not checked; original lower
  evaluator remains pending. Preserve original37 producer modules, native3 and
  the one actual capture. Never rerun or overwrite historical observations.
- in_flight_uncommitted: verify Git on read;0283 owns normal commit workflow
  under target/p4-system-14/a42ao. No reference process; all fixtures on-volume.
- blockers: none requiring director input. CPU14/18,board10/12,GC replay4/4green.
  D79/D80 remain LIVE-CONTAINMENT.4; runtime P2 in P4 a42ab. No push below300
  without director's act (COMMIT.md). Always use repository target/tmp as TMPDIR.
  Cleanup next due2026-10-19T23:00:27Z; run at the next clean boundary when due.
