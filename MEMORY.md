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
- active_work_unit: `ARTIFACT-CLEANUP` → `.24` (pending; next recurring cleanup, due after 2026-10-20T23:07Z); otherwise `P4-SYSTEM` → `.14`.
- pnt_status: running (resumed `2026-10-20` on the director's instruction);
  continue until the activities are exhausted or the director pauses it.
- last_unit: `.14` / `SEMULITH-AC-0080` — the supported act; priority1 activity closed.
- next_action: if `docs/ARTIFACT_CLEANUP.md` is older than 24 h, run `.24`: plan,
  select, `artifact_cleanup_operator.py --delete`, `--inspect` in one fresh
  work directory with the log inside it, overwrite the record, commit. Otherwise
  resume `P4-SYSTEM.14` (full source/risk/feature policy and status integration)
  from that tree's frontier and goal text.
- in_flight_uncommitted: none after the normal commit workflow.
- blockers: none requiring director input. The next narrative rollover is a
  new generation through the same transition contract.
- evidence: `docs/tasks/ARTIFACT-CLEANUP.md`; diagnostics `target/artifact-cleanup-0080`;
  the real ledger is `target/artifact-cleanup/output-provenance.json`.
- continuity: historical plans/ledger bytes, immutable task/history terminals and
  the original capture remain preserved. Read the task tree and `LIVE_STATUS.md`
  for canonical progress; return to P4 full policy/status after cleanup readiness.
- environment: use `target/tmp` as TMPDIR. Read cleanup currency from
  `docs/ARTIFACT_CLEANUP.md` (last run `2026-10-19T23:07:45Z`, due 24 h later);
  derive push cadence with `scripts/check_push_cadence.sh --status`.
