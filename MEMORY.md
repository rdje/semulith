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
- active_work_unit: 5 FEATURES : 1 XTASK (director 2026-10-26, `decision_alternate-port-and-features.md`); the count restarted at XTASK-0079 (XTASK.13 b6, taken at 4 of 5 because the rest wait on the director's pick);
  `ARTIFACT-CLEANUP.37` once due (after 2026-11-06T00:16Z); `ARTIFACT-CLEANUP.29` class C was ruled (2026-10-28) and waits for its unit.
- pnt_status: RUNNING since `2026-11-05` on the director's word ("Go in full PNT mode until all work is exhausted"); continue until the activities are exhausted or the director pauses it.
- last_unit: `SEMULITH-P4-0350` (P4-SYSTEM.14 a45-1, feature 1 of 5 after XTASK-0079) — eight stranded requirements rebound, rule 16. Open for the director: `decision_sstc-delivery-needs-the-pinned-window.md` (recommendation: open the window; a43e-0 proved it, 10 of 10 legs) and the per-case configuration (decision_reference-config-per-case.md).
- next_action: SSTC's case waits for the director's pick; on A: the decision record's four units (target/p4-system-14/a43e/pinned-edits.patch, prototype.sh; case draft target/p4-system-14/a43d-3). Do not add P4 credits before the pick: each one raises the window's cost. Meanwhile: `ARTIFACT-CLEANUP.29` class C (design: target/artifact-cleanup/AC29/design.md), then `ARTIFACT-CLEANUP.37` once due (after 2026-11-06T00:16Z). LAB-BENCH.2 waits for user feedback by its own non-goal; XTASK.13's BOOK-INDEX at the next turn.
  GS regen after `git add` (`gate_report.py rv64gc-lab-v0 --gate GS`), model fragments `gen_model_book.py --unit rv64gc-lab-v0`; chain: target/xtask/xt0002/commit-chain.sh <dir>; prechecks + `cargo fmt --check` + check_requirements, check_materials_bill, check_gate_report, and any moved probe's seams first.
- in_flight_uncommitted: none after the normal commit workflow. CHANGELOG.md sharded again in P4-0328 (shard-0422).
- blockers: none. Gate cost ~8–19 min per commit since XTASK.8's pool (2026-10-28 chain logs; longer under
  load); the gate's self-test refused silently twice (2026-10-21, 2026-10-23) and passed on rerun —
  since a42ax the gate keeps the self-test output at target/profile-consistency-selftest.log: on the
  next REFUSED, read it first. Open for the director: the crediting act's authority and sufficiency
  (decision_credit-is-a-catalogue-record.md); the normative text it rests on is retained since a42bb.
  Raise a structural blocker (a cap, a rule whose cost dominates the work) in the first reply with
  numbers and options; it is a team decision, not a workaround.
- evidence: `docs/tasks/P4-SYSTEM.md` .14 a45-1, a43e-0, a43b-c1, a43d-3, a43d-2, a43c-5, a43c-4, a43c-1 (`target/p4-system-14/a45-1`, `…/a43e`, `…/a43b-c1`, `…/a43d-3`, `…/a43d-2`, `…/a43c-5`, `…/a43c-4`, `…/a43c`); archive part 27 a43b-3h … a43b-3d, part 26 a43b-3c, 3b, 3a; `docs/tasks/XTASK.md` XTASK.13 b6, b5 (`target/xtask/xt0079`, `target/xtask/xt0078`);
  `docs/tasks/XTASK.md` XTASK.6 slices 6a–6i (`target/xtask/xt0005` … `xt0010`, `xt0013` … `xt0015`: before/, after/);
  XTASK.4 slice 4a and the inventories (`target/xtask/xt0004`: inventory.md, drivers.md, findings.md);
  `docs/tasks/P4-SYSTEM.md` .14 a42ba, a42ay, a42ax;
  cleanup act `target/artifact-cleanup/AC0092` (`docs/ARTIFACT_CLEANUP.md` last run `2026-11-05T00:16Z`).
- continuity: historical plans/ledger bytes, immutable task/history terminals and
  the original capture remain preserved. Read the task tree and `LIVE_STATUS.md`
  for canonical progress.
- environment: use `target/tmp` as TMPDIR. Read cleanup currency from
  `docs/ARTIFACT_CLEANUP.md` (next ~24 h after its last run);
  derive push cadence with `scripts/check_push_cadence.sh --status`.
