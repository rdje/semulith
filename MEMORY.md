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
- active_work_unit: 5 FEATURES : 1 XTASK (director 2026-10-26, `decision_alternate-port-and-features.md`): features
  1–3 done (a42bc; P4-SYSTEM.15 slices a, b) → features 4–5 (.15 slices c–d or a .14 act) → `XTASK.6` slice 6j (drafted);
  `ARTIFACT-CLEANUP.28` once due (after 2026-10-27T08:50Z); `ARTIFACT-CLEANUP.29` waits for a ruling on its
  measured finding (the .29 leaf: options A/B/C; design target/artifact-cleanup/AC29/design.md).
- pnt_status: running (resumed `2026-10-20` on the director's instruction);
  continue until the activities are exhausted or the director pauses it.
- last_unit: `SEMULITH-XTASK-0017` — XTASK.8 slice d: the docs-only gate path (six closures; a docs commit in 27 s).
  Before it P4-0301 (the GC validator-mutation campaign: 28 of 30, two gaps pinned), P4-0300, XTASK-0016 (the gate
  52–56 → 6.8 min), P4-0299. Run the three PROFILE-CONSISTENCY probes before a chain touching profiles/.
- next_action: the tooling slice (XTASK.8 slice d) landed → features 6–10: P4-SYSTEM.15 slice e (the two corpus
  gaps), the workload suite, the Misalign suites, …; then XTASK.6 slice 6j; `ARTIFACT-CLEANUP.28` once due (after 2026-10-27T08:50Z). Before
  ANY failure-injection probe or any fixture write, read the path it drives (the scratch-hygiene card:
  docs/knowledge/an-empty-scratch-path-falls-back-to-the-repository.md). Commit chain:
  target/xtask/xt0002/commit-chain.sh <evidence-dir>.
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
  cleanup act `target/artifact-cleanup/AC0084` (`docs/ARTIFACT_CLEANUP.md` last run `2026-10-26T08:50Z`).
- continuity: historical plans/ledger bytes, immutable task/history terminals and
  the original capture remain preserved. Read the task tree and `LIVE_STATUS.md`
  for canonical progress.
- environment: use `target/tmp` as TMPDIR. Read cleanup currency from
  `docs/ARTIFACT_CLEANUP.md` (next ~24 h after its last run);
  derive push cadence with `scripts/check_push_cadence.sh --status`.
