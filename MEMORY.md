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
- active_work_unit: 5 FEATURES : 1 XTASK (director 2026-10-26, `decision_alternate-port-and-features.md`). **After XTASK-0092: `.20` d was feature 1, e (`0412`) 2, f1 (`0414`) 3; f2 and f3 are 4 and 5, then the XTASK turn** (`XTASK.13`'s `probe_retained_sail_identity.py`), then g and h. Briefs and maintenance count as neither.
  `ARTIFACT-CLEANUP.42` once due (24 h after 2026-11-13T20:58Z), the orphan act before its four.
- pnt_status: RUNNING since 2026-11-05 on the director's word ("Go in full PNT mode until all work is exhausted."). 4 credits current (42 retired by `.20` a until f); CPU-SYSTEM `passed` for version 0 at `194437d6` (`decision_release-rv64gc-lab-v0.md`), `incomplete` in version 1's window, 6 axes owned; not yet published (a push is the director's).
- last_unit: `SEMULITH-P4-0414` (`.20` f1: the 42 declared under `rv64gc-lab-env-v4`; 40 predecessors and 40 reference files retired, listed on `retired-cases.md` from `228c9d76`, 25 holders re-pointed; `m-forms-v7` and `csr-set-v3` kept until f3 (the effect probe replays csr-set-v3's trace: the brief's finding 4 corrected); 12 probes re-stated (`WINDOW_RETAINED` in the policy probe); walk tool's refusal carries stderr; four book pages marked as version 0's). Before it `0413` (f's brief).
- next_action: `.20` f2, feature 4 of 5: from the f1 commit, `python3 -B scripts/capture_guarded.py --case <each of the 42 in target/p4-system-20/f1/table.txt> --declaration-commit <f1>` once; `compare_git.py` (target/p4-system-20/f-brief) against `228c9d76`, stop on any trace/stdout/guest/expectation difference; then `measure_config_effect.py` for the 12 successors with effects and `measure_walk_trace.py --case rv64gc-walk-implicit-v2`; restate the probes for captured successors (effect probe's RETAINED gains the 12 rows of `228c9d76`'s table under new ids, the input census `1 + 46 * 22`, the status rows `pending`); `target/p4-system-20/f1/rehearse.sh` is the template. Move closed `.20` records to an archive part first: P4-SYSTEM.md is 126 KB of 131,072. f3: `credit.py` (from `a88b01a0`), G-TRACE rows from `228c9d76`, defaults to `m-forms-v8`, `m-forms-v7` and `csr-set-v3` retired and listed, `WINDOW_RETAINED` emptied with the groups renamed, the book's examples measured again, the catalogue header rewritten. Prechecks every slice: task acceptance, seam integrity, frontier sync, tree claims, docpaths, gap claims, table arity, DERIVED-COUNTS, routes, knowledge map. `EVIDENCE_POLICY.md` stays untouched. `LIVE-CONTAINMENT.5` before any new tool row, `.6` before the next decision record (the index has 23 B left), D79 (`LIVE-CONTAINMENT.4`).
  GS regen after `git add` (`gate_report.py <unit> --gate GS`), model fragments `gen_model_book.py --unit <unit>`; chain: `cargo xtask commit-unit <dir>` (~20 min with scripts touched); run `cargo xtask check-profile-consistency` first: probes' mutation counts are exact. A clone that builds with cargo needs `.app-data/vendor` linked in (cargo exits 101 without it).
- in_flight_uncommitted: none after the normal commit workflow. CHANGELOG.md sharded again in LC-0056 (shard-0425).
- blockers: none. Gate cost ~8–19 min per commit since XTASK.8's pool (2026-10-28 chain logs; longer under
  load); the gate's self-test refused silently twice (2026-10-21, 2026-10-23) and passed on rerun —
  since a42ax the gate keeps the self-test output at target/profile-consistency-selftest.log: on the
  next REFUSED, read it first. Open for the director: the crediting act's authority and sufficiency
  (decision_credit-is-a-catalogue-record.md); the normative text it rests on is retained since a42bb.
  Raise a structural blocker (a cap, a rule whose cost dominates the work) in the first reply with
  numbers and options; it is a team decision, not a workaround.
- evidence: `docs/tasks/P4-SYSTEM.md` .20 f1 (`target/p4-system-20/f1`), f brief (`target/p4-system-20/f-brief`), .20 e (`target/p4-system-20/e`), e brief (`target/p4-system-20/e-brief`); `docs/tasks/XTASK.md` XTASK.18 (`target/xtask/xt0091`); `docs/tasks/P4-SYSTEM.md` .20 brief (`target/p4-system-20/brief`); `docs/tasks/P5-BOARD.md` .13 brief (`target/p5-board-13/brief`); `docs/tasks/P4-SYSTEM.md` .19 a (`target/p4-system-19/a`), .18 c2b and c2a (`target/p4-system-18/c2`), .18 c1 (`target/p4-system-18/c`), .18 b (`target/p4-system-18/b`, `target/hosted-matrix/42418631491`), .18 a, .14 a51-14, a51-13, a51-9, a51-8, a51-7, a51-6, a51-5, a51-4, a51-3, a51-2, a51-1, a51-0, a50-c2, a50-c1, a50-4, a50-3, a50-2, a50-1, a49-4, a49-3, a49-2, a49-1, a49-0, a48-1, a47-3, a47-2, a47-1, a46-4, a46-3, a46-2, a46-1, a46-0, a43e-5, a43e-4, a43e-3, a43e-c1, a43e-2, a43e-1, a45-1, a43e-0, a43b-c1, a43d-3, a43d-2, a43c-5, a43c-4, a43c-1 (`target/p4-system-14/a49-3`, `…/a49-2`, `…/a49-1`, `…/a49-0`, `…/a48-1`, `…/a47-3`, `…/a47-2`, `…/a47-1`, `…/a46-4`, `…/a46-3`, `…/a46-2`, `…/a46-1`, `…/a46-0`, `…/a43e-5`, `…/a43e-4`, `…/a43e-3`, `…/a43e-c1`, `…/a43e-2`, `…/a43e-1`, `…/a45-1`, `…/a43e`, `…/a43b-c1`, `…/a43d-3`, `…/a43d-2`, `…/a43c-5`, `…/a43c-4`, `…/a43c`); archive part 30 a43e-0, a43b-c1, a43d-3; part 27 a43b-3h … a43b-3d, part 26 a43b-3c, 3b, 3a; `docs/tasks/XTASK.md` XTASK.13 e, d, c, b6, b5 (`target/xtask/xt0082`, `xt0081`, `xt0080`, `xt0079`, `xt0078`);
  `docs/tasks/XTASK.md` XTASK.6 slices 6a–6i (`target/xtask/xt0005` … `xt0010`, `xt0013` … `xt0015`: before/, after/);
  XTASK.4 slice 4a and the inventories (`target/xtask/xt0004`: inventory.md, drivers.md, findings.md);
  `docs/tasks/P4-SYSTEM.md` .14 a42ba, a42ay, a42ax;
  usage-text fix `target/artifact-cleanup/AC0099`; rollover `target/artifact-cleanup/AC0098`; cleanup act `target/artifact-cleanup/AC0097` (`docs/ARTIFACT_CLEANUP.md` last run `2026-11-13T20:58Z`).
- continuity: historical plans/ledger bytes, immutable task/history terminals and
  the original capture remain preserved. Read the task tree and `LIVE_STATUS.md`
  for canonical progress.
- environment: use `target/tmp` as TMPDIR. Read cleanup currency from
  `docs/ARTIFACT_CLEANUP.md` (next ~24 h after its last run);
  derive push cadence with `scripts/check_push_cadence.sh --status`.
