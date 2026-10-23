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
- active_work_unit: `P4-SYSTEM.14` — a42ay (the crediting mechanism) and a42ba (archive part 21) committed; the
  act (a42az) waits on the director's ruling; `ARTIFACT-CLEANUP.26` when the record is ~24 h old (after 2026-10-23T08:12Z).
- pnt_status: running (resumed `2026-10-20` on the director's instruction);
  continue until the activities are exhausted or the director pauses it.
- last_unit: `P4-SYSTEM.14` a42ba / `SEMULITH-P4-0294` — the closed `.14` records a42aq–a42aw and rows
  a42ar–a42ax moved verbatim into docs/tasks/archive/P4-SYSTEM-21.md (live file 118,497 → 63,186 B); before it
  a42ay / `SEMULITH-P4-0293`, the crediting mechanism (`credits.sexp`, `scripts/credit_records.py`; real tree
  0 records, `REQ-GC-M` planned; `decision_credit-is-a-catalogue-record.md`).
- next_action: the crediting act (a42az) is the DIRECTOR'S decision, not the agent's: (a) who signs the record,
  (b) whether one finite case of 25 witnesses suffices for `implemented` on `REQ-GC-M`. (c) is done: a42bb
  retained the eleven other M statements and Table 1 (`RVI-M-STATEMENTS`, decision_m-statements-retained.md).
  Also due
  `ARTIFACT-CLEANUP.26` after 2026-10-23T08:12Z and the LIVE-CONTAINMENT tree's own archive move (its file
  ~128 KB of 131,072 B). LIVE_STATUS was trimmed to states by LC-0053 (4,771 of 6,144 B).
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
