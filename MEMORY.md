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
- active_work_unit: `P4-SYSTEM.14` — next slice a42as (one case with many predeclared
  properties over `m-forms.s`); `ARTIFACT-CLEANUP.25` is DUE (the record passed 24 h at 2026-10-21T22:11Z); run it first.
- pnt_status: running (resumed `2026-10-20` on the director's instruction);
  continue until the activities are exhausted or the director pauses it.
- last_unit: `P4-SYSTEM.14` a42ar / `SEMULITH-P4-0286` — `m-forms.s`, the corpus program
  covering all 13 M forms and the 12 Table 1 cells with derived expectations; verify fixture
  regenerated; live Sail AGREE on 33 steps (an experiment, not a capture); P4's closed rows
  through a42aq moved into `docs/tasks/archive/P4-SYSTEM-20.md` (tree ~50 KB); the
  `profiles/` aggregates re-derived to 4 MiB / 800 files
  (`decision_profiles-family-corpus-second-rederivation.md`); the director may ungovern
  them instead.
- next_action: `P4-SYSTEM.14` a42as — give the property binding
  (`scripts/matched_gpr_property.py` and its consumers: relations, manifest, review_div_*,
  capture_div.py, check_profile_consistency.sh) one case with MANY predeclared properties,
  one per Table 1 cell and one per form over `m-forms.s`, keeping v2 untouched; then a42at
  declares the v3 case (`capture_div.py --declare`, fresh prepared inputs) and a42au captures
  the three runs under the collector so review_div_policy measures `satisfied`.
  EVIDENCE_POLICY.md is pinned by v2: edit it only inside a re-capture.
- in_flight_uncommitted: none after the normal commit workflow.
- blockers: a42as and P4-SYSTEM.15–.18 must edit paths the retained case v2 pins (`evidence/rv64gc-signed-div-truncation-v2/dependencies.sexp`: 64 inputs + 4 principals — 35 scripts incl. every `matched_gpr_*.py` and `capture_div.py`, all 20 `definitions/riscv/*.sexp`, six `profiles/rv64gc-lab-v0` files); any edit stales the finite method, `review_div_policy.py` exits 1 and PROFILE-CONSISTENCY refuses every commit.
  Raised to the director 2026-10-22 with four options (recommended: a stale method becomes an `invalidated` disposition with exit 0 in the unpinned `review_div_policy.py` unless the receipt claims qualification; then evolve and re-capture as v3). Do not start a42as before the director picks.
  Gate cost: ~2 h 10 min per commit; its PROFILE-CONSISTENCY self-test refused one commit on 2026-10-21 for a cause not identified (.14 a42ar record). Raise a structural blocker (a cap, a rule whose cost dominates the work)
  in the first reply with numbers and options; it is a team decision, not a workaround.
- evidence: `docs/tasks/P4-SYSTEM.md` .14 a42ar; `target/p4-system-14/a42ar`;
  `docs/tasks/LIVE-CONTAINMENT.md` .4m; `target/live-containment/lc0052`.
- continuity: historical plans/ledger bytes, immutable task/history terminals and
  the original capture remain preserved. Read the task tree and `LIVE_STATUS.md`
  for canonical progress.
- environment: use `target/tmp` as TMPDIR. Read cleanup currency from
  `docs/ARTIFACT_CLEANUP.md` (last run `2026-10-20T22:11Z`, next ~24 h later);
  derive push cadence with `scripts/check_push_cadence.sh --status`.
