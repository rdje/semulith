# Orphan incremental sessions: disposable target directories for altered builds, and a recorded class for the backlog

- **Type:** `decision`
- **Date:** `2026-10-26`
- **Status:** `active`
- **Owner / source:** the workflow under [`decision_four-rulings-delegated.md`](decision_four-rulings-delegated.md);
  the open question of `docs/tasks/ARTIFACT-CLEANUP.md` (.25, 2026-10-22) whose deferral ended at
  `ARTIFACT-CLEANUP.27` (2026-10-26: 83 sessions, 247 files, 770,724,553 B, from 67 files three days before).
answers: What happens to Cargo incremental sessions that no later successful build will ever collect?

## The fact / decision

1. **Prevention (a procedure rule, in force now).** Any build of the workspace under altered sources or
   flags — a RED measurement, a mutation copy, a bogus-flag probe — uses a disposable target directory
   (`--target-dir` or `CARGO_TARGET_DIR` under `target/tmp/<unit>` or the unit's evidence directory) that
   the unit removes. Measured 2026-10-26: no gate driver builds altered sources into the shared target
   directory (`PORT-WEB` and `API-DOCS` self-tests already use their own `--target-dir` inside their
   scratch); the growth came from the XTASK slices' before/after measurements. The rule joins `XTASK`'s
   acceptance criteria and the knowledge card
   `docs/knowledge/an-empty-scratch-path-falls-back-to-the-repository.md`'s neighbour on scratch hygiene.
2. **The backlog and any future orphan (a recorded class).** Strict selection gains the class
   `orphan incremental session`: a crate-hash directory under an `incremental/` directory, inside the
   directive's cargo scope, every one of whose session directories is a plan candidate and which holds no
   session outside the plan. The class is approved as a group, recorded in the selection record beside
   `approved` and `unrecorded` as `orphan`, with probe arms fired RED (a hash directory with one live
   session is never approved; a file outside the cargo scope is never approved; the census still binds
   before the guarded core unlinks). Executed by `ARTIFACT-CLEANUP.29`, after `XTASK.6` slice `6f`; the
   next recurring cleanup that runs with the class removes the 83 sessions.
3. **No size cap.** A cap would only restate the need for 2 at a threshold; the class removes the need.

## Why

- A session in a crate-hash directory with no live sibling is garbage by construction: rustc collects old
  sessions only on a successful build of the same configuration, and these configurations (altered sources,
  altered flags, a copied crate path) are never built again. The directive's enumerated scope already
  names `target/debug/incremental` `.bin` files as deletable; what was missing was a recorded, mechanical
  definition strict selection could approve without a captured record.
- The 83 sessions are 770 MB on the repository volume today and would grow with every measured slice;
  prevention stops the growth, the class clears what exists.

## How to apply

- Before a measurement that builds the workspace under altered sources or flags, set the disposable target
  directory first; the acceptance row names it.
- The class's definition lives in the selection tool and its probes, never in prose alone; a cleanup record
  reports `orphan` counts and bytes beside the other two groups.
