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
  Children: `ARTIFACT-CLEANUP.1`, `ARTIFACT-CLEANUP.2`

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

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| — | — | — | `.1` done; the next cleanup is time-triggered (~24 h), so no pending leaf exists between runs |

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

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
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
| `ARTIFACT-CLEANUP` (run) | `SEMULITH-AC-0057 (tree ARTIFACT-CLEANUP): …` | the 2026-10-03 cleanup — 0 incremental caches present to delete; 62 `target/refs/*.log` (2.2 M) kept |
| `ARTIFACT-CLEANUP` (run) | `SEMULITH-AC-0056 (tree ARTIFACT-CLEANUP): …` | the 2026-10-02 cleanup — 105 incremental caches, 139 MB |
| `ARTIFACT-CLEANUP` (run) | `SEMULITH-AC-0055 (tree ARTIFACT-CLEANUP): …` | the 2026-10-01 cleanup — 96 incremental caches, 248 MB |
| `ARTIFACT-CLEANUP` (run) | `SEMULITH-AC-0054 (tree ARTIFACT-CLEANUP): …` | the 2026-09-30 cleanup — 90 incremental caches, 185 MB |
| `ARTIFACT-CLEANUP` (run) | `SEMILITH-AC-0053 (tree ARTIFACT-CLEANUP): …` | the 2026-09-29 cleanup — 169 incremental caches, 272 MB |
| `ARTIFACT-CLEANUP` (run) | `SEMILITH-AC-0052 (tree ARTIFACT-CLEANUP): …` | the 2026-09-28 cleanup — 132 incremental caches, 720 MB |
| `ARTIFACT-CLEANUP.2` | `SEMILITH-AC-0051 (leaf ARTIFACT-CLEANUP.2): …` | the sanctioned-watcher exemption, data-owned; the census stops crying wolf |
| `ARTIFACT-CLEANUP.1` | `SEMULITH-AC-0050 (leaf ARTIFACT-CLEANUP.1): …` | first §8 cleanup; record + registry row in the creating commit |

## Changelog

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
