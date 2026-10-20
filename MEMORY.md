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
- active_work_unit: `LIVE-CONTAINMENT.4` capacity chain → then `P4-SYSTEM.14` slice a42ap
  (full policy/status); `ARTIFACT-CLEANUP.25` when the record is ~24 h old (after
  2026-10-21T22:11Z).
- pnt_status: running (resumed `2026-10-20` on the director's instruction);
  continue until the activities are exhausted or the director pauses it.
- last_unit: `LIVE-CONTAINMENT.4k` / `SEMULITH-LC-0050` — decisions family re-derived 2×
  with its authority record; decision records can land again.
- next_action: P4 retention capacity. Measured: docs/tasks/P4-SYSTEM.md 130,889 and
  docs/tasks/artifacts/live-containment/task-claims.md 131,005 of 131,072 B; docs/tasks
  at 107/107 files (pooled 33+1+33+40, decision_task-family-six-activity-count); every
  archive terminal at its count. a42ap cannot record ~2 KB without a transition: author
  the reviewed authority (a second complete-records artifact or a sealed P4 generation),
  retire a42ao's whole records through it, then build the status-derivation checker
  (48 requirements, EVIDENCE_POLICY "Status and supersession"; one experiment, adequacy
  pending → 48 planned / 0 drift). A fresh session suits the P4 checker work.
- in_flight_uncommitted: none after the normal commit workflow.
- blockers: none requiring director input. Open containment pressure: the decisions
  INDEX.md (13,234 B) reaches its 16,384 B part near 83 rows; the cleanup tree's live
  narrative is 10,041 B of a 12,288 B warning line (third ledger generation next).
- evidence: `docs/tasks/LIVE-CONTAINMENT.md` .4k; `target/live-containment/lc0050`;
  cleanup act `target/artifact-cleanup/AC0081`; real ledger
  `target/artifact-cleanup/output-provenance.json`.
- continuity: historical plans/ledger bytes, immutable task/history terminals and
  the original capture remain preserved. Read the task tree and `LIVE_STATUS.md`
  for canonical progress.
- environment: use `target/tmp` as TMPDIR. Read cleanup currency from
  `docs/ARTIFACT_CLEANUP.md` (last run `2026-10-20T22:11Z`, next ~24 h later);
  derive push cadence with `scripts/check_push_cadence.sh --status`.
