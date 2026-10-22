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
- active_work_unit: `P4-SYSTEM.14` — next slice a42au (declare the m-forms case `rv64gc-m-forms-v3`);
  `ARTIFACT-CLEANUP.26` when the record is ~24 h old (after 2026-10-23T08:12Z).
- pnt_status: running (resumed `2026-10-20` on the director's instruction);
  continue until the activities are exhausted or the director pauses it.
- last_unit: `P4-SYSTEM.14` a42at / `SEMULITH-P4-0288` — the property binding owns a case table:
  v2 keeps one property, `rv64gc-m-forms-v3` declares 25 (13 forms, 12 Table 1 cells) over m-forms.s
  with all 33 words reviewed and re-derived independently; the relation plan carries every declared
  property and the control's; every predeclared value is held to the source derivation. The retained
  v2 case is `invalidated` (its pinned binding moved; a42as) and nothing is credited.
- next_action: `P4-SYSTEM.14` a42au — declare the m-forms case: give `scripts/capture_div.py` and
  `scripts/review_div_capture.py` a case selector (the retained pointer `P.CASE_ID` stays v2 for the
  method/policy reviews), prepare the fresh inputs under `evidence/rv64gc-m-forms-v3/` (guest.elf,
  reference-config.json, baseline and control expectations with boundary 12 x15 −3 → −4), run
  `capture_div.py --declare` for the case and commit the three declarations with the inputs; then a42av
  captures the three runs, switches the retained pointers and lets `review_div_policy` measure `satisfied`.
- in_flight_uncommitted: none after the normal commit workflow.
- blockers: none. Gate cost ~45 min to 2 h per commit; the self-test refusal of 2026-10-21 stays
  unexplained (.14 a42ar). Open question for the director (a42at record): only the DIV statement is a
  retained excerpt; the multiply and Table 1 statements are cited, not retained.
  Raise a structural blocker (a cap, a rule whose cost dominates the work) in the first reply with
  numbers and options; it is a team decision, not a workaround.
- evidence: `docs/tasks/P4-SYSTEM.md` .14 a42at; `target/p4-system-14/a42at` (reproduce-*.log,
  independent-m-forms.log, binding-smoke.log, reviews-after.log, seams-*.log, focused-checks.json);
  cleanup act `target/artifact-cleanup/AC0082` (`docs/ARTIFACT_CLEANUP.md` last run `2026-10-22T08:12Z`).
- continuity: historical plans/ledger bytes, immutable task/history terminals and
  the original capture remain preserved. Read the task tree and `LIVE_STATUS.md`
  for canonical progress.
- environment: use `target/tmp` as TMPDIR. Read cleanup currency from
  `docs/ARTIFACT_CLEANUP.md` (next ~24 h after its last run);
  derive push cadence with `scripts/check_push_cadence.sh --status`.
