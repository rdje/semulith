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
- active_work_unit: `P4-SYSTEM.14` — next slice a42at (one case with many predeclared
  properties over `m-forms.s`); `ARTIFACT-CLEANUP.26` when the record is ~24 h old (after 2026-10-23T08:12Z).
- pnt_status: running (resumed `2026-10-20` on the director's instruction);
  continue until the activities are exhausted or the director pauses it.
- last_unit: `ARTIFACT-CLEANUP.25` / `SEMULITH-AC-0082` — second cleanup through the act: 6 outputs
  removed (15,766,472 B), 67 unrecorded mutation-build sessions (281 MB) measured as an open question.
  Before it, `P4-SYSTEM.14` a42as / `SEMULITH-P4-0287`: a stale finite method is `invalidated`, not a lock.
- next_action: `P4-SYSTEM.14` a42at — give the property
  binding (`scripts/matched_gpr_property.py` and its consumers: relations, manifest, evaluation,
  unit collector, adequacy, capture_div.py, the probes and gate arms) one case with MANY predeclared
  properties, one per Table 1 cell and one per form over `m-forms.s`; v2 becomes `invalidated` and
  that commit is allowed; then a42au declares the v3 case (`capture_div.py --declare`, fresh
  prepared inputs; commit) and a42av captures the three runs so review_div_policy measures `satisfied`.
- in_flight_uncommitted: none after the normal commit workflow.
- blockers: none. The pinned-input lock was resolved by a42as (2026-10-22, the director's pick). Gate
  cost ~45 min to 2 h per commit; the self-test refusal of 2026-10-21 stays unexplained (.14 a42ar).
  Raise a structural blocker (a cap, a rule whose cost dominates the work) in the first reply with
  numbers and options; it is a team decision, not a workaround.
- evidence: `docs/tasks/P4-SYSTEM.md` .14 a42as, a42ar; `target/p4-system-14/a42as`, `a42ar`;
  cleanup act `target/artifact-cleanup/AC0082` (`docs/ARTIFACT_CLEANUP.md` last run `2026-10-22T08:12Z`);
  `docs/tasks/LIVE-CONTAINMENT.md` .4m; `target/live-containment/lc0052`.
- continuity: historical plans/ledger bytes, immutable task/history terminals and
  the original capture remain preserved. Read the task tree and `LIVE_STATUS.md`
  for canonical progress.
- environment: use `target/tmp` as TMPDIR. Read cleanup currency from
  `docs/ARTIFACT_CLEANUP.md` (last run `2026-10-20T22:11Z`, next ~24 h later);
  derive push cadence with `scripts/check_push_cadence.sh --status`.
