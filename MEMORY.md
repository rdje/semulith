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
- active_work_unit: 5 FEATURES : 1 XTASK (director 2026-10-26, `decision_alternate-port-and-features.md`); the count restarted at XTASK-0081; the count restarted at XTASK-0082; a48-1 was feature 1 of 5; a48-2 is feature 2. **The window that opens SSTC closed 2026-11-05** (a43e-5; `decision_sstc-delivery-needs-the-pinned-window.md`).
  `ARTIFACT-CLEANUP.37` once due (24 h after 2026-11-05T10:24Z), the orphan act before its four; `.38` (the owned rollover) before any cleanup leaf with a checklist.
- pnt_status: RUNNING since 2026-11-05 on the director's word ("Go in full PNT mode until all work is exhausted."). 5 credits current, G-STATE 4 of 4, G-TRACE green; open axes G-OBLIGATIONS, G-RELEASE.
- last_unit: `SEMULITH-P4-0366` (a48-1: Batch II-b declared, rehearsed first). Before it `SEMULITH-XTASK-0082` (XTASK.13 e: PLATFORM-GEN judges a frozen tree), and before that `SEMULITH-P4-0365` (a47-3: Batch II-a credited, 19 implemented, 28 planned). Before it `SEMULITH-P4-0364` (a47-2: captured once each), `SEMULITH-P4-0363` (a47-1: declared, rehearsed first), `SEMULITH-P4-0362` (a46-4: Batch I credited, 14 implemented, 33 planned), `SEMULITH-XTASK-0081` (XTASK.13 d: BOARD-GEN judges a frozen tree), `SEMULITH-P4-0360` (a46-2: Batch I's nine programs and cases declared, rehearsed first). Before it `SEMULITH-P4-0359` (a46-1: case index generated, statements retained), `SEMULITH-P4-0358` (a46-0: G-OBLIGATIONS' other 42 routed), `SEMULITH-P4-0357` (a43e-5: five credits, G-STATE 4 of 4, G-TRACE read from `evidence/`, the window closed), `SEMULITH-P4-0356` (a43e-4: captured once each on the director's word, the four's traces byte-identical), `SEMULITH-XTASK-0080` (XTASK.13 c). Open for the director: the per-case configuration (decision_reference-config-per-case.md).
- next_action: a48-2: Batch II-b captured once each from the declaration commit P4-0366 (`target/p4-system-14/a47-2/capture.sh` pattern; frozen list from the four manifests, run in the background), then a48-3: `target/p4-system-14/a48-1/edit_review.py`, credits, 23 implemented. Then the tool for a declared alternative, the seven with a switch; 17 end at a director's ruling.
  GS regen after `git add` (`gate_report.py rv64gc-lab-v0 --gate GS`), model fragments `gen_model_book.py --unit rv64gc-lab-v0`; chain: target/xtask/xt0002/commit-chain.sh <dir>; prechecks + `cargo fmt --check` + check_requirements, check_materials_bill, check_gate_report, and any moved probe's seams first.
- in_flight_uncommitted: none after the normal commit workflow. CHANGELOG.md sharded again in P4-0328 (shard-0422).
- blockers: none. Gate cost ~8–19 min per commit since XTASK.8's pool (2026-10-28 chain logs; longer under
  load); the gate's self-test refused silently twice (2026-10-21, 2026-10-23) and passed on rerun —
  since a42ax the gate keeps the self-test output at target/profile-consistency-selftest.log: on the
  next REFUSED, read it first. Open for the director: the crediting act's authority and sufficiency
  (decision_credit-is-a-catalogue-record.md); the normative text it rests on is retained since a42bb.
  Raise a structural blocker (a cap, a rule whose cost dominates the work) in the first reply with
  numbers and options; it is a team decision, not a workaround.
- evidence: `docs/tasks/P4-SYSTEM.md` .14 a48-1, a47-3, a47-2, a47-1, a46-4, a46-3, a46-2, a46-1, a46-0, a43e-5, a43e-4, a43e-3, a43e-c1, a43e-2, a43e-1, a45-1, a43e-0, a43b-c1, a43d-3, a43d-2, a43c-5, a43c-4, a43c-1 (`target/p4-system-14/a48-1`, `…/a47-3`, `…/a47-2`, `…/a47-1`, `…/a46-4`, `…/a46-3`, `…/a46-2`, `…/a46-1`, `…/a46-0`, `…/a43e-5`, `…/a43e-4`, `…/a43e-3`, `…/a43e-c1`, `…/a43e-2`, `…/a43e-1`, `…/a45-1`, `…/a43e`, `…/a43b-c1`, `…/a43d-3`, `…/a43d-2`, `…/a43c-5`, `…/a43c-4`, `…/a43c`); archive part 30 a43e-0, a43b-c1, a43d-3; part 27 a43b-3h … a43b-3d, part 26 a43b-3c, 3b, 3a; `docs/tasks/XTASK.md` XTASK.13 e, d, c, b6, b5 (`target/xtask/xt0082`, `xt0081`, `xt0080`, `xt0079`, `xt0078`);
  `docs/tasks/XTASK.md` XTASK.6 slices 6a–6i (`target/xtask/xt0005` … `xt0010`, `xt0013` … `xt0015`: before/, after/);
  XTASK.4 slice 4a and the inventories (`target/xtask/xt0004`: inventory.md, drivers.md, findings.md);
  `docs/tasks/P4-SYSTEM.md` .14 a42ba, a42ay, a42ax;
  cleanup act `target/artifact-cleanup/AC29-act` (`docs/ARTIFACT_CLEANUP.md` last run `2026-11-05T10:24Z`).
- continuity: historical plans/ledger bytes, immutable task/history terminals and
  the original capture remain preserved. Read the task tree and `LIVE_STATUS.md`
  for canonical progress.
- environment: use `target/tmp` as TMPDIR. Read cleanup currency from
  `docs/ARTIFACT_CLEANUP.md` (next ~24 h after its last run);
  derive push cadence with `scripts/check_push_cadence.sh --status`.
