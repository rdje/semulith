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
- active_work_unit: 5 FEATURES : 1 XTASK (director 2026-10-26, `decision_alternate-port-and-features.md`). **Five features landed after XTASK-0089/0090: `.18` c2a, c2b, `.19` a, `P5-BOARD.13`'s brief, `.20`'s brief. One XTASK slice is next, then five features.**
  `ARTIFACT-CLEANUP.41` once due (24 h after 2026-11-09T23:59Z), the orphan act before its four; `.38` (the owned rollover) before any cleanup leaf with a checklist.
- pnt_status: RUNNING since 2026-11-05 on the director's word ("Go in full PNT mode until all work is exhausted."). 46 credits current; CPU-SYSTEM `passed` since 2026-11-10: `rv64gc-lab-v0` version 0 accepted (`decision_release-rv64gc-lab-v0.md`), not yet published (a push is the director's).
- last_unit: `SEMULITH-P4-0401` (`.20`'s brief, `decision_the-next-window-is-version-1.md`: author, state table and `profile.sexp` lapse 42 of 46; the label leaves `profile.sexp` first; slices a–h). Before it `SEMULITH-P5-0020` (`P5-BOARD.13` blocked on `.20`).
- next_action: one XTASK slice (`XTASK.13`'s PROFILE-CONSISTENCY probes, or `XTASK.17`, the ledger probe at the push boundary; read docs/tasks/XTASK.md's frontier). Then `.20` slice a, feature 1: the release identity out of `profile.sexp` (measure a new file against `gate.sexp`), and the claim pages name `194437d6` BEFORE any pinned input moves. `EVIDENCE_POLICY.md` stays untouched (it lapses all 46). `LIVE-CONTAINMENT.5` before any new tool row (10 B left in docs/toolbox/), and D79's causal analysis (`LIVE-CONTAINMENT.4`). Any dossier change to `rv64gc-lab-v0` lapses its decision, and any to `rv64i-lab-v0` re-pins the netboard: say so in the unit that makes it.
  GS regen after `git add` (`gate_report.py <unit> --gate GS`), model fragments `gen_model_book.py --unit <unit>`; chain: `cargo xtask commit-unit <dir>` (a commit with any path outside `DOCTRINE_LEDGER` in `scripts/doctrine_skip.sh` runs the six heavy checks, ~20 min; a ledger-only one ~2); prechecks + `cargo fmt --check` + check_requirements, check_materials_bill, check_gate_report, and any moved probe's seams first.
- in_flight_uncommitted: none after the normal commit workflow. CHANGELOG.md sharded again in LC-0056 (shard-0425).
- blockers: none. Gate cost ~8–19 min per commit since XTASK.8's pool (2026-10-28 chain logs; longer under
  load); the gate's self-test refused silently twice (2026-10-21, 2026-10-23) and passed on rerun —
  since a42ax the gate keeps the self-test output at target/profile-consistency-selftest.log: on the
  next REFUSED, read it first. Open for the director: the crediting act's authority and sufficiency
  (decision_credit-is-a-catalogue-record.md); the normative text it rests on is retained since a42bb.
  Raise a structural blocker (a cap, a rule whose cost dominates the work) in the first reply with
  numbers and options; it is a team decision, not a workaround.
- evidence: `docs/tasks/P4-SYSTEM.md` .20 brief (`target/p4-system-20/brief`); `docs/tasks/P5-BOARD.md` .13 brief (`target/p5-board-13/brief`); `docs/tasks/P4-SYSTEM.md` .19 a (`target/p4-system-19/a`), .18 c2b and c2a (`target/p4-system-18/c2`), .18 c1 (`target/p4-system-18/c`), .18 b (`target/p4-system-18/b`, `target/hosted-matrix/42418631491`), .18 a, .14 a51-14, a51-13, a51-9, a51-8, a51-7, a51-6, a51-5, a51-4, a51-3, a51-2, a51-1, a51-0, a50-c2, a50-c1, a50-4, a50-3, a50-2, a50-1, a49-4, a49-3, a49-2, a49-1, a49-0, a48-1, a47-3, a47-2, a47-1, a46-4, a46-3, a46-2, a46-1, a46-0, a43e-5, a43e-4, a43e-3, a43e-c1, a43e-2, a43e-1, a45-1, a43e-0, a43b-c1, a43d-3, a43d-2, a43c-5, a43c-4, a43c-1 (`target/p4-system-14/a49-3`, `…/a49-2`, `…/a49-1`, `…/a49-0`, `…/a48-1`, `…/a47-3`, `…/a47-2`, `…/a47-1`, `…/a46-4`, `…/a46-3`, `…/a46-2`, `…/a46-1`, `…/a46-0`, `…/a43e-5`, `…/a43e-4`, `…/a43e-3`, `…/a43e-c1`, `…/a43e-2`, `…/a43e-1`, `…/a45-1`, `…/a43e`, `…/a43b-c1`, `…/a43d-3`, `…/a43d-2`, `…/a43c-5`, `…/a43c-4`, `…/a43c`); archive part 30 a43e-0, a43b-c1, a43d-3; part 27 a43b-3h … a43b-3d, part 26 a43b-3c, 3b, 3a; `docs/tasks/XTASK.md` XTASK.13 e, d, c, b6, b5 (`target/xtask/xt0082`, `xt0081`, `xt0080`, `xt0079`, `xt0078`);
  `docs/tasks/XTASK.md` XTASK.6 slices 6a–6i (`target/xtask/xt0005` … `xt0010`, `xt0013` … `xt0015`: before/, after/);
  XTASK.4 slice 4a and the inventories (`target/xtask/xt0004`: inventory.md, drivers.md, findings.md);
  `docs/tasks/P4-SYSTEM.md` .14 a42ba, a42ay, a42ax;
  cleanup act `target/artifact-cleanup/AC0096` (`docs/ARTIFACT_CLEANUP.md` last run `2026-11-09T23:59Z`).
- continuity: historical plans/ledger bytes, immutable task/history terminals and
  the original capture remain preserved. Read the task tree and `LIVE_STATUS.md`
  for canonical progress.
- environment: use `target/tmp` as TMPDIR. Read cleanup currency from
  `docs/ARTIFACT_CLEANUP.md` (next ~24 h after its last run);
  derive push cadence with `scripts/check_push_cadence.sh --status`.
