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
- active_work_unit: `P4-SYSTEM.14` — next slice a42aq (full policy adequacy of the retained
  case); `ARTIFACT-CLEANUP.25` when the record is ~24 h old (after 2026-10-21T22:11Z).
- pnt_status: running (resumed `2026-10-20` on the director's instruction);
  continue until the activities are exhausted or the director pauses it.
- last_unit: `P4-SYSTEM.14` a42ap / `SEMULITH-P4-0284` — requirement status derived from the
  evidence graph and drift-checked under PROFILE-CONSISTENCY (48+28 planned, 0 drift);
  a42ao's whole rows retired into task-claims-2.md (verify-p4.py in target/p4-system-14/a42ap).
- next_action: `P4-SYSTEM.14` a42aq — full source/risk/feature adequacy of the one retained
  case (rv64gc-signed-div-truncation-v2, medium risk, category `defined`): name the legs the
  policy requires (source-located expectations, boundary fixtures, repeated execution, a
  discriminating control, matched reference comparison), measure which the retained bytes
  already satisfy, and either produce the crediting disposition (receipt `qualification`
  true → REQ-GC-M derives `partial`) or an honest `pending` naming the missing legs. Retire
  a42ap's whole rows into task-claims-2.md first (retain pattern in the a42ap workdir).
  EVIDENCE_POLICY.md is one of the case's 64 pinned inputs: edit it only inside a re-capture.
  A fresh session suits this; the P4 tree has ~3 KB of record room.
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
