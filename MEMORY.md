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
- active_work_unit: `RUSTDOC.1` next (defects listed in target/rust-tooling/rustdoc1-defects.txt), then `XTASK.1` (trees registered 2026-10-23,
  `decision_rust-native-tooling.md`: xtask incrementally and with extreme care, nothing breaks). `P4-SYSTEM.14`'s
  crediting act (a42az) waits on the director's ruling; `ARTIFACT-CLEANUP.27` after 2026-10-24T10:15Z
  (create target/artifact-cleanup/AC0084 first).
- pnt_status: running (resumed `2026-10-20` on the director's instruction);
  continue until the activities are exhausted or the director pauses it.
- last_unit: `SEMULITH-LC-0054` — LIVE-CONTAINMENT's closed rows moved to docs/tasks/archive/LIVE-CONTAINMENT-rows.md
  (128,385 → 86,120 B); before it TOOL-0001 (RUSTDOC and XTASK registered), AC-0083, P4-0295 (a42bb).
- next_action: `RUSTDOC.1` — fix
  the 19 doc defects (9 unresolved links, 4 private links, 6 unclosed HTML tags; target/rustdoc-xtask-assessment/)
  and register a doctrine running `cargo doc --workspace --no-deps --offline` with those lints denied, fired RED
  first. The crediting act (a42az) is the DIRECTOR'S decision: (a) who signs, (b) whether one finite case of 25
  witnesses suffices for `implemented` on `REQ-GC-M`; the normative text is retained (a42z, a42bb).
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
