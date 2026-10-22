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
- active_work_unit: `P4-SYSTEM.14` — next slice a42ax (switch the retained reviews to the m-forms capture);
  `ARTIFACT-CLEANUP.26` when the record is ~24 h old (after 2026-10-23T08:12Z).
- pnt_status: running (resumed `2026-10-20` on the director's instruction);
  continue until the activities are exhausted or the director pauses it.
- last_unit: `P4-SYSTEM.14` a42aw / `SEMULITH-P4-0291` — `rv64gc-m-forms-v3` captured once by the new
  tracked `scripts/retain_div_capture.py`: AGREE/AGREE/DIVERGE over 33 boundaries, 25 properties bound, all
  findings matched, 43 of 43 family files, qualification false, `REQ-GC-M` planned.
- next_action: `P4-SYSTEM.14` a42ax — switch the retained reviews to the m-forms capture:
  `review_div_method.RETAINED_CASE_ID`, `MEASURED_SHA256`/`MEASURED_BYTES` (16,942 B, fb22d5e5…),
  `SOURCE_DECLARATION_COMMIT` 4af5a68…, `RETAINED_CAPTURE_COMMIT` (the a42aw commit) and
  `review_div_policy.CASE_ID` to `rv64gc-m-forms-v3`; make `probe_div_method`'s fixture and the policy
  probe's real-tree arm follow the retained case (the policy should measure all ten legs `satisfied`,
  `credited: false`); update the policy-adequacy chapter and the toolbox rows; commit. Then the
  crediting decision for `REQ-GC-M` is a separately owned record (policy: a satisfied measurement is its input).
- in_flight_uncommitted: none after the normal commit workflow.
- blockers: none. Gate cost ~45 min to 2 h per commit; the self-test refusal of 2026-10-21 stays
  unexplained (.14 a42ar). Open question for the director (a42at record): only the DIV statement is a
  retained excerpt; the multiply and Table 1 statements are cited, not retained.
  Raise a structural blocker (a cap, a rule whose cost dominates the work) in the first reply with
  numbers and options; it is a team decision, not a workaround.
- evidence: `docs/tasks/P4-SYSTEM.md` .14 a42aw, a42av; `target/p4-system-14/a42aw` (reproduce.log,
  capture-report.json, offline-reevaluation.log, seams-retention.log, focused-checks.json);
  cleanup act `target/artifact-cleanup/AC0082` (`docs/ARTIFACT_CLEANUP.md` last run `2026-10-22T08:12Z`).
- continuity: historical plans/ledger bytes, immutable task/history terminals and
  the original capture remain preserved. Read the task tree and `LIVE_STATUS.md`
  for canonical progress.
- environment: use `target/tmp` as TMPDIR. Read cleanup currency from
  `docs/ARTIFACT_CLEANUP.md` (next ~24 h after its last run);
  derive push cadence with `scripts/check_push_cadence.sh --status`.
