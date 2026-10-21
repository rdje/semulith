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
- active_work_unit: `P4-SYSTEM.14` slice a42ap (full policy/status), now unblocked;
  `ARTIFACT-CLEANUP.25` when the record is ~24 h old (after 2026-10-21T22:11Z).
- pnt_status: running (resumed `2026-10-20` on the director's instruction);
  continue until the activities are exhausted or the director pauses it.
- last_unit: `LIVE-CONTAINMENT.4l` / `SEMULITH-LC-0051` — task-family count 107 → 116 with
  its authority; the first complete-records continuation task-claims-2.md holds the .4j
  whole records (compact map + spans; verify.py in target/live-containment/lc0051).
- next_action: `P4-SYSTEM.14` a42ap. First retire a42ao's whole record, acceptance,
  verification and commit rows from docs/tasks/P4-SYSTEM.md (130,889 of 131,072 B) into
  docs/tasks/artifacts/live-containment/task-claims-2.md with the lc0051 retain pattern
  (insert + spans, source/owner/retired inverses), then build the status-derivation checker:
  each of the 48 rv64gc requirements' implementation_status derived from the evidence graph
  under profiles/rv64gc-lab-v0/EVIDENCE_POLICY.md ("Status and supersession") with a drift
  gate; one experiment (DIV v2, adequacy pending) → 48 planned / 0 drift. Read the a42ao
  record, gate_report.py G-OBLIGATIONS and matched_gpr_evaluation first. A fresh session
  suits the checker work.
- in_flight_uncommitted: none after the normal commit workflow.
- blockers: none requiring director input. Open containment pressure: docs/tasks aggregate
  3,134,069 of 3,145,728 B → LIVE-CONTAINMENT.4 slice (m), a second task-history seal (the
  kind the director approved directly before); the decisions INDEX.md part near 83 rows; the
  cleanup tree's live narrative 10,041 of 12,288 B (third ledger generation next).
- evidence: `docs/tasks/LIVE-CONTAINMENT.md` .4l; `target/live-containment/lc0051`;
  cleanup act `target/artifact-cleanup/AC0081`; real ledger
  `target/artifact-cleanup/output-provenance.json`.
- continuity: historical plans/ledger bytes, immutable task/history terminals and
  the original capture remain preserved. Read the task tree and `LIVE_STATUS.md`
  for canonical progress.
- environment: use `target/tmp` as TMPDIR. Read cleanup currency from
  `docs/ARTIFACT_CLEANUP.md` (last run `2026-10-20T22:11Z`, next ~24 h later);
  derive push cadence with `scripts/check_push_cadence.sh --status`.
