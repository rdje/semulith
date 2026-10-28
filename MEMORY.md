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
- last_unit: `SEMULITH-P4-0314` — P4-SYSTEM.17 done: the hosted portability matrix (run 40713852362 on b917d1ba) agreed
  byte-identically for both units on real x86-64 and aarch64, Miri and cross-endian green. Before it P4-0313 (a44-2a: the
  declarations as data), AC-0087 (the cohort on Linux), P4-0312 (a44-1).
- next_action: P4-SYSTEM.14 a44-2b (a44-1's design): the pinned tools read the case files (matched_gpr_case.py), the in-code
  tables removed, the censuses (manifest population, reviewed modules/data paths, probes' seams and loss counts) re-derived,
  CR-GC-M-1 retired and REQ-GC-M planned for the one lapse; then a44-3 … a44-5. A push grant is asked (CI doctrines red). Tooling turns (5:1): the three doctrine controls, XTASK's close,
  ARTIFACT-CLEANUP.29 (class C + 24.1 GB); P4-SYSTEM.17 closes when the hosted runs of b917d1ba are green; `.31` after 2026-10-29T09:49Z.
  Probes before a chain touching profiles/; GS regen only after `git add`; acceptance boxes carry a signature token. Commit chain: target/xtask/xt0002/commit-chain.sh <evidence-dir>.
- in_flight_uncommitted: none after the normal commit workflow. CHANGELOG.md at 47 KB of 64 KiB (sharded in XTASK-0062).
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
