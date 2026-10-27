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
- active_work_unit: 5 FEATURES : 1 XTASK (director 2026-10-26, `decision_alternate-port-and-features.md`): cycle two complete
  (P4-0302 … P4-0306) and XTASK-0018 (slice 6j) landed → cycle three: the a43b-1/a43c-1/a43d-1 programs, then the XLEN declaration;
  `ARTIFACT-CLEANUP.30` once due (after 2026-10-28T09:33Z); `ARTIFACT-CLEANUP.29` waits for a ruling on its
  measured finding (the .29 leaf: options A/B/C; design target/artifact-cleanup/AC29/design.md).
- pnt_status: running (resumed `2026-10-20` on the director's instruction);
  continue until the activities are exhausted or the director pauses it.
- last_unit: `SEMULITH-XTASK-0031` — XTASK.6 slice 6r-b: the knowledge family's second re-derivation (56 files / 180,224 B; health 48 /
  157,696) and the deferred 6r card landed. Before it XTASK-0029 (6u), XTASK-0028 (6t), XTASK-0027 (6s), XTASK-0026 (6r), XTASK-0025
  (6q), XTASK-0024 (6p), XTASK-0023 (6o), XTASK-0022 (6n), XTASK-0021 (6m), XTASK-0020 (6l), XTASK-0019 (6k).
- next_action: RAISED to the director — no unblocked feature leaf remains (the `.14` declarations and the ZICNTR program wait on the
  pinned-tooling ruling, options A/B/C in the P4-0306 leaf; LAB-BENCH.2 on a user-feedback round; P5-BOARD.5 on the CPU's acceptance)
  and the workload kind's declaration; until a ruling lands the tooling slices continue: XTASK.6 slice 6v (`check_board_gen.sh` behind a
  held shim; eleven free drivers follow, then the three `sexp`-only callers over `sexp.rs`). `ARTIFACT-CLEANUP.30` once due (after
  2026-10-28T09:33Z). Probes before a chain touching profiles/; GS regen only after `git add`; acceptance boxes carry a signature token. Commit chain: target/xtask/xt0002/commit-chain.sh <evidence-dir>.
- in_flight_uncommitted: none after the normal commit workflow. CHANGELOG.md at 50 KB of 64 KiB (sharded in XTASK-0013).
- blockers: none. Gate cost ~45 min to 3 h per commit (longer when other repositories' gates share the
  machine); the gate's self-test refused silently twice (2026-10-21, 2026-10-23) and passed on rerun —
  since a42ax the gate keeps the self-test output at target/profile-consistency-selftest.log: on the
  next REFUSED, read it first. Open for the director: the crediting act's authority and sufficiency
  (decision_credit-is-a-catalogue-record.md); the normative text it rests on is retained since a42bb.
  Raise a structural blocker (a cap, a rule whose cost dominates the work) in the first reply with
  numbers and options; it is a team decision, not a workaround.
- evidence: `docs/tasks/P4-SYSTEM.md` .14 a42az (`target/p4-system-14/a42az`: smoke, real-tree.log, red-*.log, st2.log);
  `docs/tasks/XTASK.md` XTASK.6 slices 6a–6i (`target/xtask/xt0005` … `xt0010`, `xt0013` … `xt0015`: before/, after/);
  XTASK.4 slice 4a and the inventories (`target/xtask/xt0004`: inventory.md, drivers.md, findings.md);
  `docs/tasks/P4-SYSTEM.md` .14 a42ba, a42ay, a42ax;
  cleanup act `target/artifact-cleanup/AC0085` (`docs/ARTIFACT_CLEANUP.md` last run `2026-10-27T09:33Z`).
- continuity: historical plans/ledger bytes, immutable task/history terminals and
  the original capture remain preserved. Read the task tree and `LIVE_STATUS.md`
  for canonical progress.
- environment: use `target/tmp` as TMPDIR. Read cleanup currency from
  `docs/ARTIFACT_CLEANUP.md` (next ~24 h after its last run);
  derive push cadence with `scripts/check_push_cadence.sh --status`.
