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
  `ARTIFACT-CLEANUP.31` once due (after 2026-10-29T09:49Z); `ARTIFACT-CLEANUP.29` waits for a ruling on its
  measured finding (the .29 leaf: options A/B/C; design target/artifact-cleanup/AC29/design.md).
- pnt_status: running (resumed `2026-10-20` on the director's instruction);
  continue until the activities are exhausted or the director pauses it.
- last_unit: `SEMULITH-P4-0325` (P4-SYSTEM.14 a43a-2e) — the XLEN case captured once (AGREE, AGREE, control DIVERGE at
  x31/24); this commit is its capture commit. Features 1-5 of 5 since XTASK-0073 done: the XTASK turn is next.
- next_action: XTASK.13 slice b (GUEST-GEN): a REDUCED frozen pair (the full rv64gc corpus is 171 guests, its fixture ~1 MB):
  drop the live in-sync arm (run judges live), the hand-edit and base-mirror arms on a small fixed subset; RED before/after on
  the real tree with a restore trap (target/xtask/xt0073/red.sh pattern). Then a43a-2f: review_div_method/policy over several
  retained cases (per-case pointers; boundary marker "(boundary"; form coverage for a state requirement; OB-XLEN feature
  disposition; PROFILE-CONSISTENCY's real run per case) and the credit CR-D-XLEN-1 (REQ-D-XLEN implemented).
  Watch hosted CI after every push; capture only on a quiet host (target/p4-system-14/a43a-2e/capture-when-quiet.sh);
  after a catalogue edit gen_model_book.py --unit; GS regen after `git add`; chain: target/xtask/xt0002/commit-chain.sh <dir>.
- in_flight_uncommitted: none after the normal commit workflow. CHANGELOG.md sharded again in P4-0315 (shard-0421).
- blockers: none. Gate cost ~8–19 min per commit since XTASK.8's pool (2026-10-28 chain logs; longer under
  load); the gate's self-test refused silently twice (2026-10-21, 2026-10-23) and passed on rerun —
  since a42ax the gate keeps the self-test output at target/profile-consistency-selftest.log: on the
  next REFUSED, read it first. Open for the director: the crediting act's authority and sufficiency
  (decision_credit-is-a-catalogue-record.md); the normative text it rests on is retained since a42bb.
  Raise a structural blocker (a cap, a rule whose cost dominates the work) in the first reply with
  numbers and options; it is a team decision, not a workaround.
- evidence: `docs/tasks/P4-SYSTEM.md` .14 a42az (`target/p4-system-14/a42az`: smoke, real-tree.log, red-*.log, st2.log);
  `docs/tasks/XTASK.md` XTASK.6 slices 6a–6i (`target/xtask/xt0005` … `xt0010`, `xt0013` … `xt0015`: before/, after/);
  XTASK.4 slice 4a and the inventories (`target/xtask/xt0004`: inventory.md, drivers.md, findings.md);
  `docs/tasks/P4-SYSTEM.md` .14 a42ba, a42ay, a42ax;
  cleanup act `target/artifact-cleanup/AC0086` (`docs/ARTIFACT_CLEANUP.md` last run `2026-10-28T09:49Z`).
- continuity: historical plans/ledger bytes, immutable task/history terminals and
  the original capture remain preserved. Read the task tree and `LIVE_STATUS.md`
  for canonical progress.
- environment: use `target/tmp` as TMPDIR. Read cleanup currency from
  `docs/ARTIFACT_CLEANUP.md` (next ~24 h after its last run);
  derive push cadence with `scripts/check_push_cadence.sh --status`.
