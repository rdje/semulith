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
- active_work_unit: `P4-SYSTEM.14` — next slice a42aw (capture the m-forms case);
  `ARTIFACT-CLEANUP.26` when the record is ~24 h old (after 2026-10-23T08:12Z).
- pnt_status: running (resumed `2026-10-20` on the director's instruction);
  continue until the activities are exhausted or the director pauses it.
- last_unit: `P4-SYSTEM.14` a42av / `SEMULITH-P4-0290` — the evaluation, the combined collector, the
  adequacy and method reviews take the case explicitly (`case_id`; retained case the default; the method
  review's `RETAINED_CASE_ID` lives outside the pinned modules); the m-forms declaration re-emitted once
  over the three edited pinned modules (pins only). No capture, no credit.
- next_action: `P4-SYSTEM.14` a42aw — capture the m-forms case: the pinned Sail binary is present
  (`target/refs/sail-riscv-Mac-arm64/bin/sail_riscv_sim`, digest equals the retained identity); run
  `python3 -B scripts/capture_div.py --capture --case rv64gc-m-forms-v3` (30 s per process, as a42am),
  retain the twelve observations, write `measured-experiment.sexp` and `verification.json` through a
  tracked receipt writer (the a42am receipt was written by hand: make the writer a deliverable), then
  switch `review_div_method.RETAINED_CASE_ID` + its measured pins/commits and `review_div_policy.CASE_ID`
  to v3 and confirm `review_div_policy.py` measures all ten legs `satisfied`, `credited: false`; commit.
- in_flight_uncommitted: none after the normal commit workflow.
- blockers: none. Gate cost ~45 min to 2 h per commit; the self-test refusal of 2026-10-21 stays
  unexplained (.14 a42ar). Open question for the director (a42at record): only the DIV statement is a
  retained excerpt; the multiply and Table 1 statements are cited, not retained.
  Raise a structural blocker (a cap, a rule whose cost dominates the work) in the first reply with
  numbers and options; it is a team decision, not a workaround.
- evidence: `docs/tasks/P4-SYSTEM.md` .14 a42av, a42au; `target/p4-system-14/a42av` (reproduce.log,
  redeclare.log, declare-v3.json, seams-*.log, probes-long.log, focused-checks.json);
  cleanup act `target/artifact-cleanup/AC0082` (`docs/ARTIFACT_CLEANUP.md` last run `2026-10-22T08:12Z`).
- continuity: historical plans/ledger bytes, immutable task/history terminals and
  the original capture remain preserved. Read the task tree and `LIVE_STATUS.md`
  for canonical progress.
- environment: use `target/tmp` as TMPDIR. Read cleanup currency from
  `docs/ARTIFACT_CLEANUP.md` (next ~24 h after its last run);
  derive push cadence with `scripts/check_push_cadence.sh --status`.
