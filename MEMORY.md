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
- active_work_unit: `ARTIFACT-CLEANUP` → `.17` (pending; strict plan selection).
- pnt_status: running (resumed `2026-10-20` on the director's instruction);
  continue until the activities are exhausted or the director pauses it.
- last_unit: `.21` / `SEMULITH-AC-0076` — anchored capture, atomic publication.
- next_action: make the planner consult the published ledger through
  `authorize(require_captured=True)` so only recorded generated outputs become
  candidates (closes cleanup finding P1); historical plans stay readable with
  no new mutation authority; cover absent/stale/legacy ledgers, cold CLI,
  omissions normal/O. Read the tree's `.17` goal first; then `.16` core, `.14` CLI.
- in_flight_uncommitted: none after the normal commit workflow.
- blockers: none requiring director input. `.23` owns the live-narrative
  rollover when the reader's 75% warning fires.
- evidence: `docs/tasks/ARTIFACT-CLEANUP.md`; diagnostics `target/artifact-cleanup-0076`;
  the real ledger is `target/artifact-cleanup/output-provenance.json`.
- continuity: historical plans/ledger bytes, immutable task/history terminals and
  the original capture remain preserved. Read the task tree and `LIVE_STATUS.md`
  for canonical progress; return to P4 full policy/status after cleanup readiness.
- environment: use `target/tmp` as TMPDIR. Read cleanup currency from
  `docs/ARTIFACT_CLEANUP.md` (last run `2026-10-19T23:07:45Z`, due 24 h later);
  derive push cadence with `scripts/check_push_cadence.sh --status`.
