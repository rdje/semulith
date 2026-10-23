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
- active_work_unit: `RUSTDOC.3` next (missing-docs ratchet), then `XTASK.1` (delegation-only front door;
  `decision_rust-native-tooling.md`: incrementally, extreme care, nothing breaks). `P4-SYSTEM.14`'s crediting act
  (a42az) waits on the director's ruling; `ARTIFACT-CLEANUP.27` after 2026-10-24T10:15Z (create AC0084 first).
- pnt_status: running (resumed `2026-10-20` on the director's instruction);
  continue until the activities are exhausted or the director pauses it.
- last_unit: `SEMULITH-RDOC-0002` — RUSTDOC.2: `make book` builds the rustdoc reference into the book output;
  chapter "The API reference"; UNIT-BOOKS verifies book links into it without scanning rustdoc's pages.
- next_action: `RUSTDOC.3` — count undocumented public items per crate (`missing_docs` via rustdoc) and refuse
  any rise (a ratchet like TABLE-ARITY), fired RED with a staged undocumented item. Containment: docs/toolbox/
  governance.md is at 16,302 of 16,384 B — partition before adding a governance row. Then XTASK.1. The crediting
  act (a42az) is the DIRECTOR'S decision: (a) who signs, (b) whether one finite case suffices.
- in_flight_uncommitted: none after the normal commit workflow.
- blockers: none. Gate cost ~45 min to 3 h per commit (longer when other repositories' gates share the
  machine); the gate's self-test refused silently twice (2026-10-21, 2026-10-23) and passed on rerun —
  since a42ax the gate keeps the self-test output at target/profile-consistency-selftest.log: on the
  next REFUSED, read it first. Open for the director: the crediting act's authority and sufficiency
  (decision_credit-is-a-catalogue-record.md); the normative text it rests on is retained since a42bb.
  Raise a structural blocker (a cap, a rule whose cost dominates the work) in the first reply with
  numbers and options; it is a team decision, not a workaround.
- evidence: `docs/tasks/P4-SYSTEM.md` .14 a42ba, a42ay, a42ax; `target/p4-system-14/a42ba` (move.log, checks.log),
  `target/p4-system-14/a42ay` (design.md, retention-scope.md, smoke-reader.log, probe-*.log, seams-*.log, real-tree.log);
  cleanup act `target/artifact-cleanup/AC0082` (`docs/ARTIFACT_CLEANUP.md` last run `2026-10-22T08:12Z`).
- continuity: historical plans/ledger bytes, immutable task/history terminals and
  the original capture remain preserved. Read the task tree and `LIVE_STATUS.md`
  for canonical progress.
- environment: use `target/tmp` as TMPDIR. Read cleanup currency from
  `docs/ARTIFACT_CLEANUP.md` (next ~24 h after its last run);
  derive push cadence with `scripts/check_push_cadence.sh --status`.
