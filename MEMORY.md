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
- active_work_unit: 5 FEATURES : 1 XTASK (director 2026-10-26, `decision_alternate-port-and-features.md`); the count restarted at XTASK-0081; the count restarted at XTASK-0082; XTASK.13 slice f took the 5:1 turn after a49-3; **slice g took it after a50-4; a51-0 was feature 1 of 5, a51-1 feature 2, a51-2 feature 3, a51-3 feature 4, a51-4 feature 5; slice h took the turn after it; a51-5 was feature 1 of 5, a51-6 feature 2, a51-7 feature 3, a51-8 feature 4, a51-9 feature 5; slice i took the turn after it; a51-10 was feature 1 of 5**; a49-4 was feature 1 of 5, a50-1 (the tool for a declared alternative) feature 2, a50-2 (the seven declared) feature 3, a50-3 (their captures) feature 4, a50-4 (their credits) feature 5, so the XTASK turn is next. **The window that opens SSTC closed 2026-11-05** (a43e-5; `decision_sstc-delivery-needs-the-pinned-window.md`).
  `ARTIFACT-CLEANUP.40` once due (24 h after 2026-11-07T11:06Z), the orphan act before its four; `.38` (the owned rollover) before any cleanup leaf with a checklist.
- pnt_status: RUNNING since 2026-11-05 on the director's word ("Go in full PNT mode until all work is exhausted."). 5 credits current, G-STATE 4 of 4, G-TRACE green; open axes G-OBLIGATIONS, G-RELEASE.
- last_unit: `SEMULITH-AC-0095` (the twelfth recurring cleanup). Before it `SEMULITH-P4-0388` (a51-10: the four credited; 42 `implemented`, 4 `planned`). Before it `SEMULITH-XTASK-0087` (XTASK.13 i: RECORD-SCHEMA judges a frozen copy). Before it `SEMULITH-P4-0387` (a51-9: the four captured). Before it `SEMULITH-P4-0386` (a51-8: the four declared, a call corrected). Before it `SEMULITH-P4-0385` (a51-7: track 3's tools). Before it `SEMULITH-P4-0384` (a51-6: the two credited; 38 `implemented`, 8 `planned`). Before it `SEMULITH-P4-0383` (a51-5: the two captured). Before it `SEMULITH-XTASK-0086` (XTASK.13 h: CONTRACT-FREEZE judges a frozen unit). Before it `SEMULITH-P4-0382` (a51-4: the two with a switch declared). Before it `SEMULITH-P4-0381` (a51-3: six credited; 36 `implemented`, 10 `planned`). Before it `SEMULITH-P4-0380` (a51-2: six captured). Before it `SEMULITH-P4-0379` (a51-1: six declared). Before it `SEMULITH-P4-0378` (a51-0: the last 17 called; `decision_the-seventeen-called.md`). Before it `SEMULITH-XTASK-0085` (XTASK.13 g: EXERCISE-COVERAGE judges frozen fragments). Before it `SEMULITH-P4-0377` (a50-c2: the capture guard tracked). Before it `SEMULITH-P4-0376` (a50-c1: the CLI reads what its usage says). Before it `SEMULITH-P4-0375` (a50-4: the seven credited; 30 `implemented`, 17 `planned`). Earlier units: `git log`.
- next_action: track 4 of `decision_the-seventeen-called.md`: `REQ-D-ABI`, `REQ-D-FP-DEFER`, `REQ-D-ROUTE-FLIP`, `REQ-D-SCOPE-CENSUS` have nothing to run, so a credit with no case is the design to settle first (`credit_records.authenticate` and `requirement_status.credited` read cases). Then `G-OBLIGATIONS` closes and `P4-SYSTEM.18` gives the verdict.
  GS regen after `git add` (`gate_report.py rv64gc-lab-v0 --gate GS`), model fragments `gen_model_book.py --unit rv64gc-lab-v0`; chain: target/xtask/xt0002/commit-chain.sh <dir>; prechecks + `cargo fmt --check` + check_requirements, check_materials_bill, check_gate_report, and any moved probe's seams first.
- in_flight_uncommitted: none after the normal commit workflow. CHANGELOG.md sharded again in P4-0328 (shard-0422).
- blockers: none. Gate cost ~8–19 min per commit since XTASK.8's pool (2026-10-28 chain logs; longer under
  load); the gate's self-test refused silently twice (2026-10-21, 2026-10-23) and passed on rerun —
  since a42ax the gate keeps the self-test output at target/profile-consistency-selftest.log: on the
  next REFUSED, read it first. Open for the director: the crediting act's authority and sufficiency
  (decision_credit-is-a-catalogue-record.md); the normative text it rests on is retained since a42bb.
  Raise a structural blocker (a cap, a rule whose cost dominates the work) in the first reply with
  numbers and options; it is a team decision, not a workaround.
- evidence: `docs/tasks/P4-SYSTEM.md` .14 a51-10, a51-9, a51-8, a51-7, a51-6, a51-5, a51-4, a51-3, a51-2, a51-1, a51-0, a50-c2, a50-c1, a50-4, a50-3, a50-2, a50-1, a49-4, a49-3, a49-2, a49-1, a49-0, a48-1, a47-3, a47-2, a47-1, a46-4, a46-3, a46-2, a46-1, a46-0, a43e-5, a43e-4, a43e-3, a43e-c1, a43e-2, a43e-1, a45-1, a43e-0, a43b-c1, a43d-3, a43d-2, a43c-5, a43c-4, a43c-1 (`target/p4-system-14/a49-3`, `…/a49-2`, `…/a49-1`, `…/a49-0`, `…/a48-1`, `…/a47-3`, `…/a47-2`, `…/a47-1`, `…/a46-4`, `…/a46-3`, `…/a46-2`, `…/a46-1`, `…/a46-0`, `…/a43e-5`, `…/a43e-4`, `…/a43e-3`, `…/a43e-c1`, `…/a43e-2`, `…/a43e-1`, `…/a45-1`, `…/a43e`, `…/a43b-c1`, `…/a43d-3`, `…/a43d-2`, `…/a43c-5`, `…/a43c-4`, `…/a43c`); archive part 30 a43e-0, a43b-c1, a43d-3; part 27 a43b-3h … a43b-3d, part 26 a43b-3c, 3b, 3a; `docs/tasks/XTASK.md` XTASK.13 e, d, c, b6, b5 (`target/xtask/xt0082`, `xt0081`, `xt0080`, `xt0079`, `xt0078`);
  `docs/tasks/XTASK.md` XTASK.6 slices 6a–6i (`target/xtask/xt0005` … `xt0010`, `xt0013` … `xt0015`: before/, after/);
  XTASK.4 slice 4a and the inventories (`target/xtask/xt0004`: inventory.md, drivers.md, findings.md);
  `docs/tasks/P4-SYSTEM.md` .14 a42ba, a42ay, a42ax;
  cleanup act `target/artifact-cleanup/AC0095` (`docs/ARTIFACT_CLEANUP.md` last run `2026-11-07T11:06Z`).
- continuity: historical plans/ledger bytes, immutable task/history terminals and
  the original capture remain preserved. Read the task tree and `LIVE_STATUS.md`
  for canonical progress.
- environment: use `target/tmp` as TMPDIR. Read cleanup currency from
  `docs/ARTIFACT_CLEANUP.md` (next ~24 h after its last run);
  derive push cadence with `scripts/check_push_cadence.sh --status`.
