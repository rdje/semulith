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
- active_work_unit: `XTASK.6` (slice 6d next); `ARTIFACT-CLEANUP.27` once due (after 2026-10-24T10:15Z; create
  AC0084 first; assess the 26 September/October leftovers in target/doctrine_scratch, not deleted yet).
  `XTASK.5` is blocked on the director (pinned `gate_report.py`); the crediting act (a42az) waits on the director.
- pnt_status: running (resumed `2026-10-20` on the director's instruction);
  continue until the activities are exhausted or the director pauses it.
- last_unit: `SEMULITH-XTASK-0007` — XTASK.6 slice 6c: `DELIVERY-PROVENANCE` is Rust behind a held shim (locality
  preamble kept), byte-identical on nine real-package paths; arm total 1672.
- next_action: `ARTIFACT-CLEANUP.27` first once due (quiet machine, `mkdir -m 700 target/artifact-cleanup/AC0084`);
  otherwise XTASK.6 slice 6d: the pure-bash drivers left are textually read or hook-coupled, so port a driver
  with a Python helper, or partition docs/toolbox/governance.md (16302 of 16384 B) first. Commit chain:
  target/xtask/xt0002/commit-chain.sh <evidence-dir>; run `bash scripts/check_rustdoc.sh` before a doc commit.
- in_flight_uncommitted: none after the normal commit workflow.
- blockers: none. Gate cost ~45 min to 3 h per commit (longer when other repositories' gates share the
  machine); the gate's self-test refused silently twice (2026-10-21, 2026-10-23) and passed on rerun —
  since a42ax the gate keeps the self-test output at target/profile-consistency-selftest.log: on the
  next REFUSED, read it first. Open for the director: the crediting act's authority and sufficiency
  (decision_credit-is-a-catalogue-record.md); the normative text it rests on is retained since a42bb.
  Raise a structural blocker (a cap, a rule whose cost dominates the work) in the first reply with
  numbers and options; it is a team decision, not a workaround.
- evidence: `docs/tasks/XTASK.md` XTASK.6 slices 6c, 6b, 6a (`target/xtask/xt0007`, `xt0006`, `xt0005`: before/after logs);
  XTASK.4 slice 4a and the inventories (`target/xtask/xt0004`: inventory.md, drivers.md, findings.md);
  `docs/tasks/P4-SYSTEM.md` .14 a42ba, a42ay, a42ax;
  cleanup act `target/artifact-cleanup/AC0082` (`docs/ARTIFACT_CLEANUP.md` last run `2026-10-22T08:12Z`).
- continuity: historical plans/ledger bytes, immutable task/history terminals and
  the original capture remain preserved. Read the task tree and `LIVE_STATUS.md`
  for canonical progress.
- environment: use `target/tmp` as TMPDIR. Read cleanup currency from
  `docs/ARTIFACT_CLEANUP.md` (next ~24 h after its last run);
  derive push cadence with `scripts/check_push_cadence.sh --status`.
