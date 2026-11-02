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
- active_work_unit: 5 FEATURES : 1 XTASK (director 2026-10-26, `decision_alternate-port-and-features.md`); the count
  restarted at XTASK-0075 (XTASK.13 b2); `ARTIFACT-CLEANUP.35` once due (after 2026-11-03T06:58Z); `ARTIFACT-CLEANUP.29` class C was ruled (2026-10-28,
  ruling 4) and waits for its implementation unit (design target/artifact-cleanup/AC29/design.md).
- pnt_status: running (resumed `2026-10-20` on the director's instruction);
  continue until the activities are exhausted or the director pauses it.
- last_unit: `SEMULITH-XTASK-0075` (XTASK.13 slice b2, the 5:1 turn) — GUEST-GEN's mirror and parcel-count arms judge a frozen
  pair; b3 (the parcel author's cold/legacy arms) at the next turn. Before it: P4-0330, v5 and xlen-v2 declared.
- next_action: features (1 of 5 after XTASK-0075): a43b-2d — `retain_div_capture.py --case <id> --declaration-commit <sha>`,
  sha = `git log -1 --format=%H --grep=SEMULITH-P4-0330`, once per case, each on a quiet host (a43a-2e's wait script:
  target/p4-system-14/a43a-2e/capture-when-quiet.sh), never retried; traces `cmp`-identical to v4's / xlen-v1's;
  RETAINED_CAPTURES rows v4/xlen-v1 → v5/xlen-v2 (review_div_method.py); family 105 → 133; both reviews 10 of 10. ⛔ Until
  then the 100 paths in target/xtask/xt0075/frozen-paths.txt must not move (re-check: `capture_div.py --declare --case`
  regenerates the committed declarations). Then 2e (CR-GC-M-3, CR-D-XLEN-2; derived-status pin 2 → 37). P4-SYSTEM.md
  115,676 B of 131,072: contain at 2e. GS regen after `git add`; chain: target/xtask/xt0002/commit-chain.sh <dir>.
- in_flight_uncommitted: none after the normal commit workflow. CHANGELOG.md sharded again in P4-0328 (shard-0422).
- blockers: none. Gate cost ~8–19 min per commit since XTASK.8's pool (2026-10-28 chain logs; longer under
  load); the gate's self-test refused silently twice (2026-10-21, 2026-10-23) and passed on rerun —
  since a42ax the gate keeps the self-test output at target/profile-consistency-selftest.log: on the
  next REFUSED, read it first. Open for the director: the crediting act's authority and sufficiency
  (decision_credit-is-a-catalogue-record.md); the normative text it rests on is retained since a42bb.
  Raise a structural blocker (a cap, a rule whose cost dominates the work) in the first reply with
  numbers and options; it is a team decision, not a workaround.
- evidence: `docs/tasks/XTASK.md` XTASK.13 b2 (`target/xtask/xt0075`: red-before.txt, frozen-paths.txt); P4-SYSTEM .14 a43b-2c, 2b;
  `docs/tasks/XTASK.md` XTASK.6 slices 6a–6i (`target/xtask/xt0005` … `xt0010`, `xt0013` … `xt0015`: before/, after/);
  XTASK.4 slice 4a and the inventories (`target/xtask/xt0004`: inventory.md, drivers.md, findings.md);
  `docs/tasks/P4-SYSTEM.md` .14 a42ba, a42ay, a42ax;
  cleanup act `target/artifact-cleanup/AC0090` (`docs/ARTIFACT_CLEANUP.md` last run `2026-11-02T06:58Z`).
- continuity: historical plans/ledger bytes, immutable task/history terminals and
  the original capture remain preserved. Read the task tree and `LIVE_STATUS.md`
  for canonical progress.
- environment: use `target/tmp` as TMPDIR. Read cleanup currency from
  `docs/ARTIFACT_CLEANUP.md` (next ~24 h after its last run);
  derive push cadence with `scripts/check_push_cadence.sh --status`.
