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
- active_work_unit: `P4-SYSTEM.14` — next slice a42ar (the crediting capture's
  predeclaration); `ARTIFACT-CLEANUP.25` when the record is ~24 h old (after 2026-10-21T22:11Z).
- pnt_status: running (resumed `2026-10-20` on the director's instruction);
  continue until the activities are exhausted or the director pauses it.
- last_unit: `P4-SYSTEM.14` a42aq / `SEMULITH-P4-0285` — the retained case's ten policy legs
  measured by scripts/review_div_policy.py under PROFILE-CONSISTENCY: 8 of 10 satisfied, pending
  boundary-fixtures and form-coverage; no credit; a42ap's rows retired (verify-p4.py in
  target/p4-system-14/a42aq checks the live inverse for each tree's newest section only).
- next_action: `P4-SYSTEM.14` a42ar — predeclare the crediting capture (v3) the measurement
  names: a guest covering all 13 M forms with one property per Table 1 row and per form,
  expectations from the pinned chapter, fresh native declarations through capture_div.py's
  generator, then the three-run capture under the collector; review_div_policy must measure
  `satisfied` before any crediting record exists (qualification stays the only crediting
  word). Retire a42aq's whole rows into task-claims-2.md first (retain pattern in the a42aq
  workdir). EVIDENCE_POLICY.md is pinned: edit it only inside that re-capture. A fresh
  session suits this; the P4 tree has ~2 KB of record room.
- in_flight_uncommitted: none after the normal commit workflow.
- blockers: none requiring director input. Open containment pressure: docs/tasks aggregate
  ~3,142,000 of 3,145,728 B → LIVE-CONTAINMENT.4 slice (m), a second task-history seal (the
  kind the director approved directly before); docs/book aggregate 524,247 of 524,288 B (a
  book re-derivation or seal is due before any chapter grows); the decisions INDEX.md part
  near 84 rows; the cleanup tree's live narrative 10,041 of 12,288 B.
- evidence: `docs/tasks/P4-SYSTEM.md` .14 a42aq; `target/p4-system-14/a42aq`;
  cleanup act `target/artifact-cleanup/AC0081`; real ledger
  `target/artifact-cleanup/output-provenance.json`.
- continuity: historical plans/ledger bytes, immutable task/history terminals and
  the original capture remain preserved. Read the task tree and `LIVE_STATUS.md`
  for canonical progress.
- environment: use `target/tmp` as TMPDIR. Read cleanup currency from
  `docs/ARTIFACT_CLEANUP.md` (last run `2026-10-20T22:11Z`, next ~24 h later);
  derive push cadence with `scripts/check_push_cadence.sh --status`.
