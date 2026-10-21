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
- last_unit: `LIVE-CONTAINMENT.4` slice (m) / `SEMULITH-LC-0052` — the containment reset the
  director ruled on `2026-10-21` (`docs/decisions/decision_containment-reset.md`): the book and
  unit books carry no size ceiling; the task family's aggregate and count are ungoverned, its
  128 KiB per-part cap kept; the second seal rejected; a unit is recorded once (tree record +
  acceptance rows, one changelog line, dev note only for a lesson).
- next_action: `P4-SYSTEM.14` a42ar — predeclare the crediting capture (v3) the a42aq
  measurement names: a guest covering all 13 M forms with one property per Table 1 row and per
  form, expectations from the pinned chapter, fresh native declarations through capture_div.py's
  generator, then the three-run capture under the collector; review_div_policy must measure
  `satisfied` before any crediting record exists. First make room in `docs/tasks/P4-SYSTEM.md`
  (129,884 of 131,072 B) the standing way: move its oldest closed records verbatim into
  `docs/tasks/archive/P4-SYSTEM-20.md` with stubs, no inverse script (the LC0052 move in
  `target/live-containment/lc0052/move.py` is the pattern). EVIDENCE_POLICY.md is pinned: edit
  it only inside that re-capture. A fresh session suits this.
- in_flight_uncommitted: none after the normal commit workflow.
- blockers: none. Raise a structural blocker (a cap, a rule whose cost dominates the work)
  in the first reply with numbers and options; it is a team decision, not a workaround.
- evidence: `docs/tasks/LIVE-CONTAINMENT.md` .4m; `target/live-containment/lc0052`;
  `docs/tasks/P4-SYSTEM.md` .14 a42aq; `target/p4-system-14/a42aq`.
- continuity: historical plans/ledger bytes, immutable task/history terminals and
  the original capture remain preserved. Read the task tree and `LIVE_STATUS.md`
  for canonical progress.
- environment: use `target/tmp` as TMPDIR. Read cleanup currency from
  `docs/ARTIFACT_CLEANUP.md` (last run `2026-10-20T22:11Z`, next ~24 h later);
  derive push cadence with `scripts/check_push_cadence.sh --status`.
