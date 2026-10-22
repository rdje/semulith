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
- active_work_unit: `P4-SYSTEM.14` — next slice a42av (capture the m-forms case);
  `ARTIFACT-CLEANUP.26` when the record is ~24 h old (after 2026-10-23T08:12Z).
- pnt_status: running (resumed `2026-10-20` on the director's instruction);
  continue until the activities are exhausted or the director pauses it.
- last_unit: `P4-SYSTEM.14` a42au / `SEMULITH-P4-0289` — `rv64gc-m-forms-v3` declared: four prepared
  inputs (`scripts/prepare_div_inputs.py`), three native declarations (`capture_div.py --declare --case`),
  the evidence family re-derived for two cases (43 files / 32 MiB), the status derivation reporting a
  declared case and reading properties under `verification` (a defect fixed). No capture, no credit.
- next_action: `P4-SYSTEM.14` a42av — capture the m-forms case: `python3 -B scripts/capture_div.py
  --capture --case rv64gc-m-forms-v3` needs the pinned Sail binary under `target/refs/` (the a42am route),
  the retained pointers switched to v3 beforehand (`P.CASE_ID`, `review_div_method.py`'s measured pin and
  commit constants, `review_div_policy.py`'s `CASE_ID`, `capture_div.PREFIX/PREPARED` follow) so the
  evaluation binds the m-forms case; commit the twelve observations and two results; then
  `review_div_policy.py` should measure `satisfied` with all ten legs, still `credited: false`.
- in_flight_uncommitted: none after the normal commit workflow.
- blockers: none. Gate cost ~45 min to 2 h per commit; the self-test refusal of 2026-10-21 stays
  unexplained (.14 a42ar). Open question for the director (a42at record): only the DIV statement is a
  retained excerpt; the multiply and Table 1 statements are cited, not retained.
  Raise a structural blocker (a cap, a rule whose cost dominates the work) in the first reply with
  numbers and options; it is a team decision, not a workaround.
- evidence: `docs/tasks/P4-SYSTEM.md` .14 a42au, a42at; `target/p4-system-14/a42au` (reproduce.log,
  prepare-tool.log, declare-v3.json, probes-fast.log, probes-long.log, seams-status.log, focused-checks.json);
  cleanup act `target/artifact-cleanup/AC0082` (`docs/ARTIFACT_CLEANUP.md` last run `2026-10-22T08:12Z`).
- continuity: historical plans/ledger bytes, immutable task/history terminals and
  the original capture remain preserved. Read the task tree and `LIVE_STATUS.md`
  for canonical progress.
- environment: use `target/tmp` as TMPDIR. Read cleanup currency from
  `docs/ARTIFACT_CLEANUP.md` (next ~24 h after its last run);
  derive push cadence with `scripts/check_push_cadence.sh --status`.
