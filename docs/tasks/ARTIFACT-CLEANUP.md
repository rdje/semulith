# ARTIFACT-CLEANUP: generated artifacts never outlive their usefulness

## Metadata

- Tree ID: `ARTIFACT-CLEANUP`
- Status: `active`
- Roadmap lane: cross-cutting maintenance; session-directive §8 (cleanup ~every 24 h, tracked in `docs/ARTIFACT_CLEANUP.md`)
- Gate: none of its own — housekeeping kept honest by the doctrine enforcer and the census it records
- Created: `2026-09-26`
- Owner: repo-local workflow

## Goal

Keep generated artifacts from accumulating across sessions: roughly every 24 hours, census the
repository's artifact locations, delete only what is 100% safe (provably regenerable outputs, never
inputs), and record the run in `docs/ARTIFACT_CLEANUP.md` so the next session knows when the last
cleanup happened and what it removed.

## Non-Goals

- **Never tracked content.** Anything git tracks is out of scope by construction.
- **Never inputs, only outputs.** Dependency source data (crate test fixtures under
  `.app-data/cargo-home/`), the `.materials/` fetch cache (network-expensive to rebuild), and
  `vendor/` are inputs or caches of inputs — deleting any of them is not "cleanup", it is damage.
- **Not a space reclamation project.** The point is housekeeping and a verified procedure, not
  megabytes; a 1.3 MB regenerable evidence log can be worth more than the space it costs.

## Acceptance Criteria

1. A dated census (counts and bytes by directory) exists before any deletion, and the after-state
   is measured, not asserted.
2. Only items in the session-directive's enumerated safe scope — cargo incremental caches and
   stray `.bin`/`.log` in `target/release`, `target/debug/incremental`, `target/debug/deps` (and
   the same under the prescribed `.app-data/` build home) — are deleted, unless a later leaf
   extends the scope with per-class evidence.
3. `docs/ARTIFACT_CLEANUP.md` is overwritten with the date and a one-line summary each run; it
   never accumulates history.
4. The doctrine enforcer is green after every cleanup commit.

## Task Tree

- ID: `ARTIFACT-CLEANUP`
  Status: `active`
  Goal: bounded, evidenced artifact cleanup on a ~24 h cadence
  Children: `ARTIFACT-CLEANUP.1`, `ARTIFACT-CLEANUP.2`, `ARTIFACT-CLEANUP.3`, `ARTIFACT-CLEANUP.4`, `ARTIFACT-CLEANUP.5`

- ID: `ARTIFACT-CLEANUP.1` — **the first cleanup, the record, and the registry row**
  Status: `done`
  Goal: run the first §8 cleanup; create `docs/ARTIFACT_CLEANUP.md` (overwrite-only record);
  register the record as a governed live surface in `doctrine/readme_routes.tsv` in the same
  commit that creates it.
  Acceptance: census recorded in this leaf; only cargo incremental `.bin` caches deleted (40
  files expected from the pre-change census); record carries the date and a one-line summary;
  registry row added; `git status` clean apart from intended files; `check_doctrines.sh` green.
  Verification: `2026-09-26` — census, classification, post-delete re-census, gate; all in the
  Verification Log below.
  Commit: `SEMULITH-AC-0050`

- ID: `ARTIFACT-CLEANUP.2` — **the sanctioned-watcher exemption, data-owned**
  Status: `done`
  Goal: the director ruled (`2026-09-27`) that CHIPDOC's ChipdocWatcher — which holds an open
  handle on `materials/catalog.sexp` by design — "will stay there. It shouldn't bother you. Do
  not worry about it from now on." Encode the ruling so the handoff census stops crying wolf:
  a sanctioned-exemptions registry the check reads as data, with the detection itself untouched
  (the pattern-free census stays; only director-ruled standing processes are exempt).
  Acceptance: `check_no_background_jobs.sh` prints `handoff: OK` with the watcher running; the
  discrimination control shows the same process flags the moment its row is absent; an agent
  may propose a row but only the director's ruling lands one.
  Design (recorded before code, `2026-09-27`): the census header refutes list-matching as
  DETECTION ("a census built from a list of things you thought of cannot see the thing you did
  not") — so the exemption is shaped as a RULING, not a vocabulary: `doctrine/sanctioned_processes.tsv`
  carries executable-substring / ruling / date; the check excludes matching command lines from
  both arms (a sanctioned watcher holds repo handles AND names repo paths by design); the
  header records why a sanctioned list is principled where a detection list is not (auditable,
  reversible, director-owned). Tracked-content gates are unaffected — the exemption covers the
  handoff census only.
  Verification: `2026-09-27` — the real check prints `handoff: OK` with PID 36462 alive; the
  control probe (row absent) flags the same process again. Both directions in the log below.
  Commit: `SEMILITH-AC-0051`
  `promotion: declined (the propose-vs-dispose discipline is stated in the registry header).`

- ID: `ARTIFACT-CLEANUP.3` — **the 2026-10-08 recurring cleanup**
  Status: `done` (`2026-10-08`, `SEMULITH-AC-0060`)
  Goal: remove only untracked cargo incremental `.bin` outputs; retain dependency fixtures
  and diagnostic/reference evidence logs. The 2026-10-06 record is more than 24 hours old.
  Acceptance: a before/after count and byte census, no tracked-file deletion, updated latest
  record, green doctrine gate, committed handoff before resuming `P4-SYSTEM.12`.
  Pre-delete census: Python `Path.rglob` over `target` and `.app-data`, excluding symlinks,
  checked against `git ls-files -z`: 84 files / 295,197,153 B in
  `target/debug/incremental`; 18 / 68,850,571 B in the wasm32 incremental directory;
  no incremental bins under `.app-data`. No stray bins/logs in `target/release` or
  `target/debug/deps`. Retain 126 diagnostic logs (1,130,473 B), 62 reference logs
  (2,096,498 B), and seven dependency-source fixtures (1,056 B).

- ID: `ARTIFACT-CLEANUP.4` — **the 2026-10-09 recurring cleanup**
  Status: `done` (`2026-10-09`, `SEMULITH-AC-0061`)
  Goal: census and remove only untracked cargo incremental `.bin` outputs after the
  dated 2026-10-08 run; preserve reference/diagnostic logs and dependency inputs.
  Acceptance: enumerate counts/bytes and tracked/symlink exclusions before deletion;
  remove exactly the reviewed candidates, prove residue zero, overwrite the latest
  record, pass the doctrine gate and commit before returning to `P4-SYSTEM.12`.

- ID: `ARTIFACT-CLEANUP.5` — **the 2026-10-10 recurring cleanup**
  Status: `done` (`2026-10-10`, `SEMULITH-AC-0062`)
  Goal: the prior run is2026-10-09 17:21:23UTC; perform this recurring run at
  approximately24hours, on clean214a524 with brief0/actual census rc=0. Read
  standing safe-scope/exclusions, current artifact record and book task-tree
  workflow before changes. Census target/.app-data with no symlink traversal
  or nested repository inspection; select only project-local untracked cargo
  incremental .bin outputs. Preserve diagnostic/reference logs, crate-source
  fixtures, all dependency inputs and tracked files. Save path/count/byte/hash
  identities before deletion, revalidate all candidates, delete exactly them,
  then prove selected residue0 and retained inputs/evidence hashes exact.
  Acceptance: before/after evidence, overwrite-only latest record, task/index/
  live/book synchronization, focused doc gates/six books and committed clean
  handoff before P4-SYSTEM.14 a7. No running build during deletion.
  Evidence: target/artifact-cleanup-0062; all scratch on repository volume.

Result: completed2026-10-10T17:22:34.381524+00:00; exact saved204paths/978509475B
revalidated by size/device/inode/mtime/SHA and all-candidate safety preflight,
then unlinked. Twelve cargo incremental roots (84debug/18wasm and102scratch);
repeat census and every saved path show residue0. Release/deps stray bins/logs0.
Retain6192diagnostic logs/7913221B,62reference logs/2097132B and7dependency
source fixtures/1056B:6261files/10011409B, all SHA/bytes exact. Both target and
.app-data are real directories on the repository device; skip symlinks and
three nested repositories, no writes across any Git/volume boundary. Actual
pre-delete process census rc=0/handoff: OK; no active build. Latest record
has one entry. Focused9/six books/verify rc=0; all code/profile/catalog/frozen/
registry/history/LIVE exact. P4 13/18/CPU incomplete7axes unchanged.
promotion: declined (standing safe-scope procedure and measured exclusions remain in this recurring tree).
Next P4-SYSTEM.14 a7/0198, canonical reference rows and their generated consequences.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| — | — | — | all five leaves done; next cleanup time-triggered (~24 h) |

## Decisions

- `2026-09-26`: scope is the directive's enumerated cargo scope and nothing else without
  per-class evidence. The `.app-data/cargo-home/**/tests/data/*.bin` files are crate **source**
  fixtures (inputs), not artifacts — deleting them would be damage wearing a cleanup's clothes.

## Open Questions

- Do `target/refs/*.log` (spike build logs, smoke guest outputs) join the deletion scope? They
  are regenerable but are evidence trails of the last reference run; at 1.3 MB they cost nothing.
  Deferred until their size or staleness makes them a question again.

## Blockers

- None.

## Acceptance Checklist (leaf ARTIFACT-CLEANUP.1)

- [x] **ROOT CAUSE (WHY + WHERE)** — the record file §8 names did not exist; the directive's own
  trigger ("file does not exist → run a cleanup during this session") fired. WHERE the artifacts
  were, from the pre-delete census:

  ```
  $ find target .app-data -path '*incremental*' -name '*.bin' | wc -l               -> 40
  $ find target .app-data -path '*incremental*' -name '*.bin' -exec du -ch {} +     -> 341M total
    (22 files under target/…/incremental, 18 under .app-data/target/debug/incremental)
  $ find .app-data \( -name '*.bin' -o -name '*.log' \) | grep -v incremental        -> 7 files,
    all .app-data/cargo-home/registry/src/**/tests/data/*.bin  (digest, sha2 — crate source
    fixtures, i.e. INPUTS; deleting inputs is damage, not cleanup — kept)
  ```

- [x] **ADDRESSED (verified)** — before → after, measured:

  ```
  BEFORE: 40 incremental .bin / 341M; .app-data 1.4G
  $ find target .app-data -path '*incremental*' -name '*.bin' -delete
  AFTER:  find … '*.bin' | wc -l -> 0;  .app-data 1.1G;  target unchanged (its .bin were the
          linkedspec consumer caches; the superproject target/ still holds its build outputs)
  $ git status --porcelain   -> only the intended tracked files (tree, index, record, registry, changelog)
  ```

- [x] **NO REGRESSION** — nothing executable changed; the enforcer re-run after staging:

  ```
  $ bash scripts/check_doctrines.sh   -> === all doctrines green ===
  ```

  The deleted caches are cargo outputs; the next `make check` / consumer build regenerates them
  (a cold incremental cache is slower, never wrong).

- [x] **FIX** — deleted the 40 enumerated-scope caches; created `docs/ARTIFACT_CLEANUP.md`
  (overwrite-only record); registered it in `doctrine/readme_routes.tsv` in the same commit.

- [x] **LOCKSTEP** — `docs/TASK_TREE.md` row added; CHANGELOG entry; registry derivation comment;
  LIVE_STATUS unchanged (no project-area row describes housekeeping); MEMORY.md unchanged (the
  frontier did not move).

## Acceptance Checklist (leaf ARTIFACT-CLEANUP.4)

- [x] **REPRODUCE / ROOT CAUSE** — the latest record names 2026-10-08; this dated
  run is 2026-10-09. Python Path.rglob census of target/.app-data, excluding symlinks
  and git ls-files entries, enumerates 249 incremental bins / 861,367,249 B. Breakdown:
  debug 165 / 526,348,156 B; Miri AArch64 9 / 53,876,225 B; Miri powerpc64 6 /
  32,141,295 B; wasm 33 / 109,923,020 B; C guest-image probe 24 / 55,985,016 B;
  C engine probe 12 / 83,093,537 B. No stray bins/logs in release/deps roots.
- [x] **FIX / ADDRESSED** — validate each target-local candidate is a regular .bin
  under incremental, untracked, unchanged in size and free of symlink ancestors;
  unlink exactly the saved census. Python repeat census: 249 / 861,367,249 B -> 0.
  Latest record overwritten. Diagnostic outputs 443 / 2,818,921 B, reference logs
  62 / 2,096,498 B and dependency-source fixtures 7 / 1,056 B retained.
- [x] **NO REGRESSION** — actual unsandboxed bash scripts/check_no_background_jobs.sh
  prints handoff: OK before deletion. No active build uses caches; no tracked file or
  dependency input removed. Commit doctrine gate must pass; caches regenerate normally.
- [x] **LOCKSTEP** — tree/index and latest record, MEMORY, CHANGELOG/DEV_NOTES updated.
  LIVE_STATUS reviewed: unchanged, P4 11/18 and CPU-SYSTEM incomplete. No user-visible
  behavior changes, so no product/book rewrite. promotion: declined (recurring procedure
  and measured exclusions remain in this tree). Return to P4-SYSTEM.12 e1d after commit.

## Acceptance Checklist (leaf ARTIFACT-CLEANUP.5)

- [x] **ROOT CAUSE** — cleanup.py --plan rc=0: prior2026-10-09 record,
  approximately24h recurrence;204 safe incremental paths/978509475B from twelve
  roots, stray release/deps0; tracked/symlink/nested-Git/volume exclusions checked.
- [x] **ADDRESSED** — cleanup.py --delete/verify.py rc=0:204paths→0,
  exact saved all-candidate identity preflight;6261retained input/evidence hashes
  and bytes exact; latest one-entry record overwritten with2026-10-10 receipt.
- [x] **NO REGRESSION** — actual pre-delete census rc=0/handoff: OK;
  focused9/six books/verify.py rc=0, all code/canonical/frozen/registry/history/
  LIVE unchanged. No active build, tracked-file or dependency-input deletion.
- [x] **LOCKSTEP** — task/index/latest record/MEMORY/DEV/CHANGELOG/book aligned;
  resume P4-SYSTEM.14 a7 after committed clean actual census.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-10-10` | `.5` | exact204path/978509475B identity+safe-scope preflight, actual pre-delete census, delete/re-census | residue0;6261kept/10011409B SHA exact; focused9/six books/verify rc=0, code/canonical/history/LIVE exact |
| `2026-10-09` | `.4` | Python census, tracked/symlink/size exclusions, exact deletion, repeat census; actual process census | 249 bins / 861,367,249 B -> 0; all evidence/input logs retained; handoff OK |
| `2026-10-08` | `.3` | Python `Path.rglob` census, tracked-file exclusion, deletion, re-census; `du -sh target .app-data` | 102 incremental bins / 364,047,724 B → 0; target 4.8 G → 4.5 G; .app-data 1.4 G unchanged; diagnostic/reference logs and dependency fixtures retained |
| `2026-10-06` | `ARTIFACT-CLEANUP` (time-triggered run) | pre-delete census: `find target .app-data -path '*incremental*' -name '*.bin'` + per-dir `uniq -c` | 192 files / 607 M, all in cargo `*/incremental/*` dirs (144 `target/debug`, 36 wasm32, 12 the `.7` scratch probe's own `target/p4-system-7/fsprobe/target/debug`); 0 stray `.bin`/`.log` in `target/release`/`target/debug/deps`; 62 `target/refs/**/*.log` (2.2 M) kept by standing policy; 7 crate-source fixtures kept |
| `2026-10-06` | `ARTIFACT-CLEANUP` (time-triggered run) | post-delete re-census + `du -sh` | 0 incremental `.bin`; `target` 4.8 G → 4.2 G, `.app-data` unchanged at 1.4 G; `git status` clean apart from intended files |
| `2026-10-04` | `ARTIFACT-CLEANUP` (time-triggered run) | pre-delete census: `find target .app-data -path '*incremental*' -name '*.bin'` + per-dir `uniq -c` | 90 files / 245 M, all in cargo `*/incremental/*` dirs (72 `target/debug`, 18 wasm32); 0 stray `.bin`/`.log` in `target/release`/`target/debug/deps`; 62 `target/refs/*.log` (2.2 M) kept by standing policy; 7 crate-source fixtures kept |
| `2026-10-04` | `ARTIFACT-CLEANUP` (time-triggered run) | post-delete re-census + `du -sh` | 0 incremental `.bin`; `target` 4.2 G → 4.0 G, `.app-data` unchanged at 1.4 G; `git status` clean apart from intended files |
| `2026-10-03` | `ARTIFACT-CLEANUP` (time-triggered run) | pre-delete census: `find target .app-data -path '*incremental*' -name '*.bin'` | 0 files / 0 M — none accumulated since the `2026-10-02` run; 0 stray `.bin`/`.log` in `target/release`/`target/debug/deps`; 62 `target/refs/*.log` (2.2 M) kept by standing policy; 7 crate-source fixtures kept |
| `2026-10-03` | `ARTIFACT-CLEANUP` (time-triggered run) | post-delete re-census + `du -sh` | 0 incremental `.bin` (nothing to delete); `target` 3.9 G, `.app-data` unchanged at 1.4 G; `git status` clean apart from intended files |
| `2026-10-02` | `ARTIFACT-CLEANUP` (time-triggered run) | pre-delete census: `find target .app-data -path '*incremental*' -name '*.bin'` + per-dir `uniq -c` | 105 files / 139 M, all in cargo `*/incremental/*` dirs (84 `target/debug`, 21 wasm32); 0 stray `.bin`/`.log` in `target/release`/`target/debug/deps`; 0 `target/refs/*.log` present this run; 7 crate-source fixtures kept |
| `2026-10-02` | `ARTIFACT-CLEANUP` (time-triggered run) | post-delete re-census + `du -sh` | 0 incremental `.bin`; `target` 4.0 G → 3.9 G, `.app-data` unchanged at 1.4 G; `git status` clean apart from intended files |
| `2026-10-01` | `ARTIFACT-CLEANUP` (time-triggered run) | pre-delete census: `find target .app-data -path '*incremental*' -name '*.bin'` + per-dir `uniq -c` | 96 files / 248 M, all in cargo `*/incremental/*` dirs (48 `target/debug`, 18 `target/x86_64-apple-darwin`, 12 wasm32, 9+9 the two miri profiles); 0 stray `.bin`/`.log` in `target/release`/`target/debug/deps`; 0 `target/refs/*.log` present this run; 7 crate-source fixtures kept |
| `2026-10-01` | `ARTIFACT-CLEANUP` (time-triggered run) | post-delete re-census + `du -sh` | 0 incremental `.bin`; `target` 3.7 G → 3.5 G, `.app-data` unchanged at 1.4 G; `git status` clean apart from intended files |
| `2026-09-30` | `ARTIFACT-CLEANUP` (time-triggered run) | pre-delete census: `find target .app-data -path '*incremental*' -name '*.bin'` + per-dir `uniq -c` | 90 files / 185 M, all in cargo `*/incremental/*` dirs (72 `target/debug/incremental`, 18 `target/wasm32-unknown-unknown/debug/incremental`); 0 stray `.bin`/`.log` in `target/release`/`target/debug/deps`; 0 `target/refs/*.log` present this run; 7 crate-source fixtures kept |
| `2026-09-30` | `ARTIFACT-CLEANUP` (time-triggered run) | post-delete re-census + `du -sh` | 0 incremental `.bin`; `target` 3.4 G → 3.2 G, `.app-data` unchanged at 1.4 G; `git status` clean apart from intended files |
| `2026-09-29` | `ARTIFACT-CLEANUP` (time-triggered run) | pre-delete census: `find target .app-data -path '*incremental*' -name '*.bin'` + per-dir `uniq -c` | 169 files / 272 M, all in cargo `*/incremental/*` dirs (139 `target/debug/incremental`, 30 `target/wasm32-unknown-unknown/debug/incremental`); 0 stray `.bin`/`.log` in `target/release`/`target/debug/deps`; `target/refs/*.log` kept by standing policy; 7 crate-source fixtures kept |
| `2026-09-29` | `ARTIFACT-CLEANUP` (time-triggered run) | post-delete re-census + `du -sh` | 0 incremental `.bin`; `target` 3.4 G → 3.2 G, `.app-data` unchanged at 1.4 G; `git status` clean apart from intended files |
| `2026-09-28` | `ARTIFACT-CLEANUP` (time-triggered run) | pre-delete census: `find target .app-data -path '*incremental*' -name '*.bin'` + per-dir `uniq -c` | 132 files / 720 M, all in cargo `*/incremental/*` dirs (`target/` own + wasm32 profiles, `.app-data/target/` vendored-consumer builds); 0 stray `.bin`/`.log` in `target/release`/`target/debug/deps`; 7 crate-source fixtures kept |
| `2026-09-28` | `ARTIFACT-CLEANUP` (time-triggered run) | post-delete re-census + `du -sh` | 0 incremental `.bin`; `.app-data` 2.0 G → 1.4 G, `target` 3.1 G → 3.0 G; `git status` clean apart from intended files; `bash scripts/check_doctrines.sh` green |
| `2026-09-26` | `ARTIFACT-CLEANUP.1` | pre-delete census: `find target .app-data -path '*incremental*' -name '*.bin'` | 40 files / 341 M, all in cargo incremental dirs |
| `2026-09-26` | `ARTIFACT-CLEANUP.1` | kept-items classification: `.bin`/`.log` outside incremental | 7 crate-source fixtures (inputs), 13 `target/refs/*.log` (evidence) — kept |
| `2026-09-26` | `ARTIFACT-CLEANUP.1` | post-delete re-census + `du -sh` | 0 incremental .bin; `.app-data` 1.4 G → 1.1 G |
| `2026-09-26` | `ARTIFACT-CLEANUP.1` | `bash scripts/check_doctrines.sh` | all doctrines green |
| `2026-09-27` | `ARTIFACT-CLEANUP.2` | `bash scripts/check_no_background_jobs.sh` (live) | `handoff: OK` with the watcher (PID 36462) running — exemption fires |
| `2026-09-27` | `ARTIFACT-CLEANUP.2` | control probe (the row absent) | the same process flags again — the exemption, not blindness, is what changed |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `.5` | `SEMULITH-AC-0062 (leaf ARTIFACT-CLEANUP.5): remove recurring incremental caches and retain evidence` | 2026-10-10;204files/978509475B, residue0;6261retained inputs/evidence hashes exact |
| `.4` | `SEMULITH-AC-0061 (leaf ARTIFACT-CLEANUP.4): remove due incremental caches and preserve evidence inputs` | 2026-10-09 cleanup; 249 files / 861,367,249 B |
| `.3` | `SEMULITH-AC-0060 (leaf ARTIFACT-CLEANUP.3): remove the due incremental caches; preserve diagnostic evidence` | 2026-10-08 cleanup, 102 files / 364,047,724 B |
| `ARTIFACT-CLEANUP` (run) | `SEMULITH-AC-0059 (tree ARTIFACT-CLEANUP): …` | the 2026-10-06 cleanup — 192 incremental caches, 607 MB |
| `ARTIFACT-CLEANUP` (run) | `SEMULITH-AC-0058 (tree ARTIFACT-CLEANUP): …` | the 2026-10-04 cleanup — 90 incremental caches, 245 MB |
| `ARTIFACT-CLEANUP` (run) | `SEMULITH-AC-0057 (tree ARTIFACT-CLEANUP): …` | the 2026-10-03 cleanup — 0 incremental caches present to delete; 62 `target/refs/*.log` (2.2 M) kept |
| `ARTIFACT-CLEANUP` (run) | `SEMULITH-AC-0056 (tree ARTIFACT-CLEANUP): …` | the 2026-10-02 cleanup — 105 incremental caches, 139 MB |
| `ARTIFACT-CLEANUP` (run) | `SEMULITH-AC-0055 (tree ARTIFACT-CLEANUP): …` | the 2026-10-01 cleanup — 96 incremental caches, 248 MB |
| `ARTIFACT-CLEANUP` (run) | `SEMULITH-AC-0054 (tree ARTIFACT-CLEANUP): …` | the 2026-09-30 cleanup — 90 incremental caches, 185 MB |
| `ARTIFACT-CLEANUP` (run) | `SEMILITH-AC-0053 (tree ARTIFACT-CLEANUP): …` | the 2026-09-29 cleanup — 169 incremental caches, 272 MB |
| `ARTIFACT-CLEANUP` (run) | `SEMILITH-AC-0052 (tree ARTIFACT-CLEANUP): …` | the 2026-09-28 cleanup — 132 incremental caches, 720 MB |
| `ARTIFACT-CLEANUP.2` | `SEMILITH-AC-0051 (leaf ARTIFACT-CLEANUP.2): …` | the sanctioned-watcher exemption, data-owned; the census stops crying wolf |
| `ARTIFACT-CLEANUP.1` | `SEMULITH-AC-0050 (leaf ARTIFACT-CLEANUP.1): …` | first §8 cleanup; record + registry row in the creating commit |

## Changelog

- `2026-10-10`: `.5` done;204 cargo incremental caches/978509475B removed, residue0;6261retained input/evidence files SHA exact, no tracked deletion. Latest record/index/book aligned, focused9/six books green.

- `2026-10-08`: `.3` done; 102 incremental caches removed (364,047,724 B), residue 0.
  Diagnostic and reference logs, dependency fixtures retained; latest record overwritten.

- `2026-10-06`: Time-triggered §8 run (the `2026-10-04` record was >24 h old): 192 incremental
  `.bin` caches deleted (607 MB; 144 `target/debug`, 36 wasm32, 12 the `.7` scratch probe's own
  cargo build); 0 stray `.bin`/`.log` in the enumerated locations; 62 `target/refs/**/*.log`
  (2.2 M) and the cargo-home fixtures kept by policy. `docs/ARTIFACT_CLEANUP.md` overwritten with
  the one-line record.

- `2026-10-04`: Time-triggered §8 run (the `2026-10-03` record was >24 h old): 90 incremental
  `.bin` caches deleted (245 MB; 72 `target/debug`, 18 wasm32); 0 stray `.bin`/`.log` in the
  enumerated locations; 62 `target/refs/*.log` (2.2 M) and the cargo-home fixtures kept by
  policy. `docs/ARTIFACT_CLEANUP.md` overwritten with the one-line record.

- `2026-10-03`: Time-triggered §8 run (the `2026-10-02` record was >24 h old): 0 incremental
  `.bin` caches present to delete — none accumulated since the previous run; 0 stray
  `.bin`/`.log` in the enumerated locations; 62 `target/refs/*.log` (2.2 M) and the
  cargo-home fixtures kept by policy. `docs/ARTIFACT_CLEANUP.md` overwritten with the
  one-line record.

- `2026-10-02`: Time-triggered §8 run (the `2026-10-01` run was a full day old): 105
  incremental `.bin` caches deleted (139 MB; 84 `target/debug`, 21 wasm32); 0 stray
  `.bin`/`.log` in the enumerated locations; no `target/refs/*.log` present this run; the
  cargo-home fixtures kept by policy. `docs/ARTIFACT_CLEANUP.md` overwritten with the
  one-line record.

- `2026-10-01`: Time-triggered §8 run (the `2026-09-30` run was a full day old): 96 incremental
  `.bin` caches deleted (248 MB; 48 `target/debug`, 18 x86_64, 12 wasm32, 9+9 miri); 0 stray
  `.bin`/`.log` in the enumerated locations; no `target/refs/*.log` present this run; the
  cargo-home fixtures kept by policy. `docs/ARTIFACT_CLEANUP.md` overwritten with the one-line
  record.

- `2026-09-30`: Time-triggered §8 run (the `2026-09-29` run was a full day old): 90 incremental
  `.bin` caches deleted (185 MB; 72 `target/debug`, 18 wasm32); 0 stray `.bin`/`.log` in the
  enumerated locations; no `target/refs/*.log` present this run; the cargo-home fixtures kept
  by policy. `docs/ARTIFACT_CLEANUP.md` overwritten with the one-line record.

- `2026-09-29`: Time-triggered §8 run (the `2026-09-28` run was >24 h old): 169 incremental
  `.bin` caches deleted (272 MB; 139 `target/debug`, 30 wasm32); 0 stray `.bin`/`.log` in the
  enumerated locations; `target/refs/*.log` and the cargo-home fixtures kept by policy.
  `docs/ARTIFACT_CLEANUP.md` overwritten with the one-line record.

- `2026-09-26`: Created. First leaf opened the same day, because the record file §8 names did not
  exist — the trigger condition "file does not exist → run a cleanup during this session" fired.
