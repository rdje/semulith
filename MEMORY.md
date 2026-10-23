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
- active_work_unit: `P4-SYSTEM.14` — next slice a42ay (the crediting act for `REQ-GC-M`: authority, mechanism,
  retained excerpts); `ARTIFACT-CLEANUP.26` when the record is ~24 h old (after 2026-10-23T08:12Z).
- pnt_status: running (resumed `2026-10-20` on the director's instruction);
  continue until the activities are exhausted or the director pauses it.
- last_unit: `P4-SYSTEM.14` a42ax / `SEMULITH-P4-0292` — the retained reviews read `rv64gc-m-forms-v3`
  (consumers only, no pinned module moved): method `satisfied` (85 files / 1,076,834 B, 40,438 snapshot),
  `DIV-POLICY: satisfied — 10 of 10 legs`, `credited` false, `REQ-GC-M` planned with both cases pending;
  the first case is `invalidated` history (`decision_ten-legs-satisfied-credit-separate.md`).
- next_action: `P4-SYSTEM.14` a42ay — the crediting act for `REQ-GC-M`, a separately owned record: settle
  (1) the authority (who credits, on which retained normative excerpts — only the DIV statement is retained
  today; the multiply and Table 1 statements are cited, not retained: a retention slice like a42z first?),
  (2) the mechanism (`requirement_status.credited()` reads a receipt's `qualification`, but a retained receipt
  is never replaced — a new record the derivation reads, not a rewrite), (3) the status move `planned` →
  the policy's credited disposition with its probe seams; read `decision_policy-legs-measured-two-pending.md`
  and `decision_ten-legs-satisfied-credit-separate.md` first. Also due: LIVE_STATUS.md bounded-snapshot
  re-derivation (6,137 of 6,144 B), `ARTIFACT-CLEANUP.26` after 2026-10-23T08:12Z.
- in_flight_uncommitted: none after the normal commit workflow.
- blockers: none. Gate cost ~45 min to 3 h per commit (longer when other repositories' gates share the
  machine); the gate's self-test refused silently twice (2026-10-21, 2026-10-23) and passed on rerun —
  since a42ax the gate keeps the self-test output at target/profile-consistency-selftest.log: on the
  next REFUSED, read it first. Open question for the director (a42at, a42ax records): only the DIV
  statement is a retained excerpt; the multiply and Table 1 statements are cited, not retained.
  Raise a structural blocker (a cap, a rule whose cost dominates the work) in the first reply with
  numbers and options; it is a team decision, not a workaround.
- evidence: `docs/tasks/P4-SYSTEM.md` .14 a42ax, a42aw; `target/p4-system-14/a42ax` (reproduce.log,
  review-method.json, policy-legs-v3-detail.log, probe-*.log, seams-*.log, focused-checks.json);
  cleanup act `target/artifact-cleanup/AC0082` (`docs/ARTIFACT_CLEANUP.md` last run `2026-10-22T08:12Z`).
- continuity: historical plans/ledger bytes, immutable task/history terminals and
  the original capture remain preserved. Read the task tree and `LIVE_STATUS.md`
  for canonical progress.
- environment: use `target/tmp` as TMPDIR. Read cleanup currency from
  `docs/ARTIFACT_CLEANUP.md` (next ~24 h after its last run);
  derive push cadence with `scripts/check_push_cadence.sh --status`.
