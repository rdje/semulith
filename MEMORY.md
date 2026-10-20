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
- active_work_unit: `P4-SYSTEM` → `.14` slice a42ap (full policy/status); `ARTIFACT-CLEANUP.25`
  when the record is ~24 h old (after 2026-10-21T22:11Z).
- pnt_status: running (resumed `2026-10-20` on the director's instruction);
  continue until the activities are exhausted or the director pauses it.
- last_unit: `ARTIFACT-CLEANUP.24` / `SEMULITH-AC-0081` — first cleanup event through the act.
- next_action: `P4-SYSTEM.14` a42ap — derive each requirement's implementation_status
  from the evidence graph under profiles/rv64gc-lab-v0/EVIDENCE_POLICY.md ("Status and
  supersession") with a drift gate; today one experiment (DIV v2, adequacy pending) so the
  honest derivation is 48 planned / 0 drift. Read the P4 tree's a42ao record, gate_report.py
  G-OBLIGATIONS, capture_div/matched_gpr_evaluation and the P4 record-retention transition
  first (the P4 tree file is 183 B under its ceiling). A fresh session suits this pivot.
- in_flight_uncommitted: none after the normal commit workflow.
- blockers: none requiring director input. The cleanup tree's live narrative is
  10,041 B of a 12,288 B warning line; the next cleanup leaf will need a third
  ledger generation through the .23 transition contract.
- evidence: `docs/tasks/ARTIFACT-CLEANUP.md`; cleanup act `target/artifact-cleanup/AC0081`;
  the real ledger is `target/artifact-cleanup/output-provenance.json`.
- continuity: historical plans/ledger bytes, immutable task/history terminals and
  the original capture remain preserved. Read the task tree and `LIVE_STATUS.md`
  for canonical progress; return to P4 full policy/status after cleanup readiness.
- environment: use `target/tmp` as TMPDIR. Read cleanup currency from
  `docs/ARTIFACT_CLEANUP.md` (last run `2026-10-20T22:11Z`, next ~24 h later);
  derive push cadence with `scripts/check_push_cadence.sh --status`.
