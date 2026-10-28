# XTASK: cargo xtask becomes the front door, incrementally and with extreme care

## Metadata

- Tree ID: `XTASK`
- Status: `active`
- Roadmap lane: cross-cutting — Rust-native tooling (director, 2026-10-23; `decision_rust-native-tooling.md`)
- Gate: none of its own — every existing doctrine must stay green through every leaf
- Consumed by: the commit workflow — every slice of every tree runs the focused checks and the gate, which
  `XTASK.1`–`XTASK.2` front; consumption point: the first P4-SYSTEM slice after `XTASK.2` (`decision_lane-consumption`)
- Created: `2026-10-23`
- Owner: repo-local workflow

## Goal

`cargo xtask` is the project's automation entry point — check, gate, book, CI, focused checks — reached
through a dependency-free Rust crate, while every existing check keeps its behaviour. Python and shell tooling
moves behind it one shimmed, measured leaf at a time; nothing breaks on the way.

## Non-Goals

- No big-bang rewrite. A leaf ports one thing, keeps the old path as a shim, and proves equality.
- No change to the 35 scripts pinned by the retained M case or to their probes unless a new capture is planned.
- No new crate dependency, no network, no change to the vendored Cargo.lock identity.
- No change to the git hooks until xtask has run green behind them for a reviewed period.

## Acceptance Criteria (every leaf)

1. **Behaviour preserved, measured:** the same exit codes and the same output lines the gate matches, recorded
   before and after on the real tree.
2. **Shim first:** the old script or target stays and delegates (or is delegated to) until every gate arm that
   names it has moved and been fired RED again.
3. **No weakening:** no arm removed, no expected count lowered, no check skipped to make a port pass.
4. **Workspace health:** the wasm build, clippy at deny-warnings, `cargo test`, every doctrine and `make ci` green.
5. One leaf per commit, `COMMIT.md` workflow.
6. **Disposable target for altered builds:** a measurement that builds the workspace under altered sources or
   flags (a RED, a mutation copy, a bogus-flag probe) sets `CARGO_TARGET_DIR` (or `--target-dir`) under the unit's
   evidence directory or `target/tmp/<unit>` and removes it; the acceptance row names it
   (`decision_orphan-incremental-sessions.md`, 2026-10-26).

## Task Tree

- ID: `XTASK`
  Status: `active`
  Goal: cargo xtask as the front door, incrementally.
  Children: `XTASK.1` … `XTASK.7`, `XTASK.8`

- ID: `XTASK.1` — **the front door, delegation only**
  Status: `done` (`2026-10-23`, `SEMULITH-XTASK-0001`; owned on clean 79644a8; evidence target/xtask/xt0001;
  prototyped first in a detached worktree, target/xtask-proto, then removed)
  Goal: a std-only `xtask` crate and the `cargo xtask` alias; subcommands `check`, `gate`, `book`, `ci`,
  `vendor`, `hooks` that run exactly what the Makefile targets run; excluded from (or clean under) the
  workspace wasm32 build; registry and toolbox rows.
  Acceptance: each subcommand's exit code and output equal its Makefile target's on the real tree, including a
  RED case (a deliberately broken copy); `make` targets unchanged.
  Result: `xtask/` (std only, no dependency, `[lints] workspace = true`) forwards every argument to `make` from
  the repository root — `env!("CARGO_MANIFEST_DIR")`'s parent, never `make -C`, whose "Entering directory" lines
  would change the output — with the same streams and exit status (a signal is never success; a missing make is
  127); no argument runs `make help`. So every target keeps one definition, the Makefile, and the subcommand set
  is the Makefile's. `.cargo/config.toml` gains the alias `xtask = "run --quiet --offline --package xtask --"`;
  the workspace gains the member (Cargo.lock +4 lines, no dependency). Measured before landing, in a detached
  worktree sharing the vendored store: fmt, clippy -D warnings, the wasm32 workspace build and API-DOCS green;
  the Makefile's own vendor command for the new lock ran from the local cache with the workspace's three crates
  byte-identical. One effect to know: the lock change makes `make vendor` re-vendor once, which prunes the
  standard library's 31 crates the portability check's Miri leg keeps in the same store (34 → 3); that leg
  re-syncs them with `cargo vendor --sync` on every run, so this is churn, not loss. The API-DOCS ratchet counts
  `xtask/` too (record row `xtask 0`); README (layout, commands, `make book` now names the API reference — a
  RUSTDOC.2 alignment gap closed here), `docs/ARCHITECTURE.md` §4 (one ownership row; the book includes it) and
  the execution toolbox row follow.

- ID: `XTASK.2` — **the focused-check runner is tracked**
  Status: `done` (`2026-10-23`, `SEMULITH-XTASK-0002`; owned on clean 31f64ba; evidence target/xtask/xt0002)
  Goal: `cargo xtask focused` runs the focused check set the commit workflow uses today (26 checks plus
  `make book`), replacing the scratch runner scripts rebuilt per unit under target/.
  Acceptance: the same 26 results as the scratch runner on the same tree; RED when one check is broken.
  Result: `cargo xtask focused [--out DIR]` is native in the xtask crate (still std only); every other
  argument list still goes to make. The set is the `FOCUSED` table — the 26 commands the scratch runners have
  run since 2026-10-22, in their order — and it is now tracked for the first time. Each check runs from the
  root with stdin closed; its combined output goes to `DIR/<script stem>.log`, one line `HH:MM:SS <command>
  rc=<n>: <last line>` is printed, `focused-checks.json` records `[[command], rc]` per check, and the run
  ends `focused: <n> red of 26`, exit 1 on any red, 2 on bad arguments or an unwritable directory. It never
  commits; the commit stays the `COMMIT.md` workflow's. Three unit tests (every listed script exists and the
  set is 26; log names unique; the clock and verdict helpers). The runner is documented in the README and the
  execution toolbox, not in `COMMIT.md` or the task-tree guide: those are spine files the scaffold updater
  overwrites. From this unit on, the commit chain runs `cargo xtask focused` instead of a scratch copy.

- ID: `XTASK.3` — **one source of truth for the targets**
  Status: `done` (`2026-10-23`, `SEMULITH-XTASK-0003`; owned on clean dea2560; evidence target/xtask/xt0003)
  Goal: the Makefile targets delegate to xtask (or the reverse), never two definitions.
  Result: already true by XTASK.1's design, the reverse direction: xtask forwards every non-native argument
  list to make, and its one native command, `focused`, has no Makefile twin (measured: 14 Makefile rules,
  all `.PHONY`; one native). Now guarded: the natives are declared once in `NATIVE`, `main` dispatches
  through it, and a unit test reads the real Makefile, requires its rules and its `.PHONY` list to agree,
  and refuses a native name that is also a rule; a second test pins the rule parse (variables, recipes,
  comments ignored). Fired RED by a temporary `focused:` rule (`focused is defined twice`), the Makefile
  restored byte-identical. Moving a target's logic into Rust stays a later, per-target, shimmed step. The
  same unit sharded CHANGELOG.md (62,075 → 48,125 B; 18 oldest entries to docs/changelog/shard-0414.md,
  completeness `70 entries before == 52 kept + 18 moved`, SHARD-FREEZE 416 rows).
  Two defects owned mid-slice. The first focused run was RED on SEAM-INTEGRITY: the ROOT CAUSE box quoted a
  Python print, not a recognised evidence token; re-evidenced with `wc -l` and the Makefile's digest. Then the
  gate refused (18:56Z → 19:48Z) on API-DOCS: this unit's crate doc linked the private `NATIVE`
  (`rustdoc::private_intra_doc_links`, denied) — and the refusal's listing showed only missing-docs warnings,
  because since RUSTDOC.3 the failing build also warns on 267 undocumented items and the listing printed every
  diagnostic up to a 60-line cut-off, burying the one error. The link is now a code span; the check lists
  only denied errors (`defects()`), with two arms on an 80-warning crate proving the error is named and no
  warning line shown (self-test 15 / 0; arm total 1670). The focused set does not run API-DOCS (it predates
  it), so this cost a gate run; whether to add it is an open question below, not changed here.

- ID: `XTASK.4` — **the small shell glue, one script per leaf**
  Status: `active`
  Goal: the 14 shell scripts that are neither doctrine drivers nor pinned, each ported behind a shim.
  Inventory (measured 2026-10-24 on 90c69268; target/xtask/xt0004/inventory.md): 74 tracked `*.sh` — 55 doctrine
  drivers named by `check_doctrines.sh` or its project slot, 0 named by the retained case's
  `dependencies.sexp` (196 entries, none a shell script), 5 evidence or upstream artifacts (the three probe
  runners under `docs/tasks/artifacts/`, the two LinkedSpec repros) — leaving 14. Three are hook-coupled and
  wait for the hooks (non-goal above): `pre_push.sh` and `approved_push.sh` (the pre-push hook's body) and
  `gen_knowledge_map.sh` (called by the pre-commit hook). The others, smallest first: `build_bench.sh` (11
  lines), `build_c_guest.sh` (18, already one `exec python3`), `install_ci_mdbook.sh` (35, CI), `fetch_act4.sh`
  (37), `update_scaffold.sh` (78), `fetch_sources.sh` (96), `check_push_cadence.sh` (187),
  `check_no_background_jobs.sh` (188), `bootstrap.sh` (200), `check_portability.sh` (250, CI),
  `fetch_references.sh` (330). The thin wrappers gain little from a port; each slice states its gain.
  One script per slice and per commit, not per leaf: the task-source reader knows direct leaves only
  (`TREE.N`; a nested `XTASK.4.1` was refused as `foreign leaf`, measured), as P4-SYSTEM's slices do.
  Slice `4a` — `build_bench.sh` becomes `cargo xtask build-bench`: done (`2026-10-24`, `SEMULITH-XTASK-0004`;
  owned on clean 90c69268; evidence target/xtask/xt0004). The bench's wasm build is a native subcommand,
  `build_bench`, run by `make bench` through the old script, now a shim of three commands (`set -euo pipefail`,
  `cd` to the root, `exec cargo xtask build-bench "$@"`); `PORTED` lists it and a unit test refuses any other
  line in it, so the shim cannot grow a second definition. Measured equal before and after on the real tree:
  stdout byte-identical through the shim, the subcommand and `make bench`; module digest unchanged; the same
  exit status for a wasm-only build failure (101), a copy failure (1) and success (0). Gain: the first script
  out of shell, and the shape later slices follow — a native subcommand, a shim, a test holding the shim.
  Found while measuring (front door, not this slice): when the environment breaks rustc's target probe for the
  host (an invalid `RUSTFLAGS`), `cargo xtask` exits 1 with no message, because quiet `cargo run` prints
  nothing there, where `cargo build` exits 101 and names the flag; a compile error in xtask is still shown
  (101). Owned as an open question below: the fix trades XTASK.1's quiet output against the message.
  The remaining 13, measured on 557d2f56 (target/xtask/xt0004/findings.md), each with what limits its port:
  four are hook-coupled (`pre_push.sh`, `approved_push.sh`, `gen_knowledge_map.sh`, and `check_push_cadence.sh`,
  which `pre_push.sh` calls); three fetch over the network, so their clone or download path cannot be measured
  equal offline (`fetch_act4.sh`, `fetch_sources.sh`, `fetch_references.sh`); `install_ci_mdbook.sh` is read as
  text by `capture_book_dependencies.py`; `update_scaffold.sh` is the template's own updater;
  `build_c_guest.sh` is one `exec python3`, so a port adds a Rust forwarder and removes no shell;
  `check_no_background_jobs.sh` comes from the template and its ancestry exclusion would change under cargo;
  `bootstrap.sh` (a temporary local clone) and `check_portability.sh` are measurable offline. The doctrine
  drivers carry the larger gain, so `XTASK.6` goes first; these wait, each constraint recorded.

- ID: `XTASK.5` — **check-examples leaves the product CLI**
  Status: `done` (`2026-10-26`, `SEMULITH-XTASK-0010`; closed by decision, no code change)
  Goal: the development check `semulith check-examples` (called by RECORD-SCHEMA through `cargo run`) becomes
  `cargo xtask check-examples`; the product CLI keeps product commands only.
  Result: closed without a code change by `decision_check-examples-stays-in-the-cli.md` (the workflow, under the
  director's delegation of 2026-10-26, `decision_four-rulings-delegated.md`). The command validates the frozen
  records bundle and presents its report — the CLI's architectural role (`docs/ARCHITECTURE.md` §4, "user
  commands and report presentation") — so it was never development-only tooling, and the goal's premise
  ("the product CLI keeps product commands only") already holds. Moving it would have turned G1's criterion 3
  false unless the pinned `gate_report.py` changed, a planned capture of the retained M case for no product
  gain. The gate keeps calling it through `cargo run`; a future move travels with a capture that also teaches
  the report its new location. Measured unchanged: `grep -c 'Some("check-examples")' crates/semulith-cli/src/main.rs`
  = 1, `grep -c check-examples scripts/check_requirements.sh` = 2; `python3 scripts/gate_report.py`
  regenerates G1 byte-identical (GATE-REPORT ok).

- ID: `XTASK.6` — **doctrine drivers, one per slice**
  Status: `active`
  Goal: unpinned doctrine drivers ported one at a time, output lines kept identical, arms re-fired RED.
  Inventory (measured 2026-10-24 on 557d2f56; target/xtask/xt0004/drivers.md): 54 drivers registered by
  `check_doctrines.sh` and its project slot — 7 spine (in `update_scaffold.sh`'s `NEUTRAL` list, so a scaffold
  sync would overwrite a port), 8 calling a pinned script directly (`gate_report.py`, `specfp.py`, `sexp.py`,
  `record_catalog.py`, `check_sexp_schema.py`, `records_sexp.py`, `dossier_sexp.py`,
  `retain_div_statement.py`), 39 free (transitive Python imports traced per slice, not yet in bulk). One
  driver per slice and per commit, as in `XTASK.4`. A ported driver's arms move into its xtask module, so the
  `DERIVED-COUNTS` arm total must count them there, or the claimed total would drop with no arm removed.
  Slices 6a–6aa (with 6r-b): [retained verbatim](archive/XTASK-3.md#slice-paragraphs-6a-to-6aa).
  Slice 6ab (`2026-10-27`, `SEMULITH-XTASK-0038`; on clean 4d6a890f, taken out of turn — no feature leaf unblocked): `FRONTIER-SYNC`'s
  driver is Rust — `xtask/src/check_frontier_sync.rs` (668 lines) ports the bash driver line for line: the inline Python judge
  (the task-tree index and the closed-tree register against every tree, through the shared `task_source` reader) runs verbatim
  through `python3 -` as a string constant extracted from the script, NOT ported; the controls write the script's synthetic trees,
  index and register — its `tree`, `index`, `index_for`, `closed` and `archive_fixture` heredocs as the same texts (the dashed
  frontier row's `—` cells included), its `source_edit` as the same single replacement — through forty-one arms (frontier drift,
  status drift, unknown and done leaves, premature completion, the register's counts and stale frontiers, trees in both files or
  neither, missing files and rows, the shared-source qualification, annotated counts, a linked archive directory); the forty-one
  bash arms are forty-one `tally.arm(` calls, the arm total unchanged; `scripts/check_frontier_sync.sh` a shim of `cargo xtask
  check-frontier-sync`. Measured in a disposable draft crate: the self-test `41 pass / 0 fail` with stdout and stderr
  byte-identical to the bash driver's, the real tree's stdout and stderr byte-identical (`FRONTIER-SYNC: ok (35 tree(s) mirrored by
  docs/TASK_TREE.md)`), and 4 scratch fixture repositories (scripts and `docs/` copied in) — the corpus, a status drift, an
  unlisted tree, no index — 4 identical, 0 differ in stdout, stderr and exit status. `docs/tasks/XTASK.md`, at 117906 B against its
  131,072 B per-part ceiling before this slice's text, has the closed slices' narrative paragraphs 6a–6aa (6r-b among them; 55667 B,
  one contiguous span of 452 lines, 27 slices; 6k's paragraph stays beside the open slices') moved verbatim out of the leaf's
  Task Tree node into `docs/tasks/archive/XTASK-3.md` after this slice's text lands (the a43b mechanism, as parts 1 and 2: SHA256 in
  the part's table, one pointer line left in the node; the live leaf 62338 B before this slice's text). In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at
  deny-warnings rc=0 (clean on the first in-tree run). Next: slice `6ac` — `check_task_history.sh` behind a held shim.
  Slice 6ac (`2026-10-27`, `SEMULITH-XTASK-0039`; on clean 2e87f916, taken out of turn — no feature leaf unblocked): `TASK-HISTORY`'s
  driver is Rust — `xtask/src/check_task_history.rs` (263 lines) ports the bash driver line for line: the five Python judges
  (`task_history_archive.py` against HEAD's descriptor taken through `git show`, the three preservation judges, the links judge)
  run as the driver ran them with their output and exit statuses passing straight through, NOT ported; the controls are the
  script's fifty-two probe runs — forty-six cases of `probe_task_history.py` and the three probe suites plain and optimized — the
  arm table taken from the script; the fifty-two bash arms are fifty-two `tally.arm(` calls, the arm total unchanged;
  `scripts/check_task_history.sh` a shim of `cargo xtask check-task-history`. Measured in a disposable draft crate: the self-test
  `52 pass / 0 fail` with stdout and stderr byte-identical to the bash driver's, the real tree's stdout and stderr byte-identical
  (the five judges' lines through `TASK-HISTORY-LINKS: ok (8 historical links, no live narrative includes)`), the unknown-arguments
  refusal identical, and 3 scratch fixture repositories (full clones of the repository) — the clone,
  no HEAD at all (git's own `fatal:` line passing through, as the script let it — the first draft swallowed it, caught by this
  state), the descriptor edited — 3 identical, 0 differ in stdout, stderr and exit status. In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at
  deny-warnings rc=0 (clean on the first in-tree run). Next: slice `6ad` — `check_changelog_shards.sh` behind a held shim.
  Slice 6ad (`2026-10-27`, `SEMULITH-XTASK-0040`; on clean ad9a8294, taken out of turn — no feature leaf unblocked): `SHARD-FREEZE`'s
  driver is Rust — `xtask/src/check_changelog_shards.rs` (631 lines) ports the bash driver line for line: the partition judge
  `scripts/check_history_partition.py` over the committed manifest and archive descriptor taken through `git show` into scratch
  files, then `scripts/history_predecessor.py`, both run as the driver ran them, NOT ported; the controls write the script's
  synthetic shards, heads and manifests (the manifest rows through the harness's hasher in the glob's order, the `prev` rows as
  the script spelled them) and run its eighteen archive-probe and twelve predecessor-probe invocations; the forty-four bash arms
  are forty-four `tally.arm(` calls (the first draft folded thirty into two loops the arm counter cannot see — unrolled before
  measuring), the arm total unchanged; `scripts/check_changelog_shards.sh` a shim of `cargo xtask check-changelog-shards`. Measured
  in a disposable draft crate: the self-test `44 pass / 0 fail` with stdout and stderr byte-identical to the bash driver's, the real
  tree's stdout and stderr byte-identical (the predecessor's line and `SHARD-FREEZE: ok (… shard row(s) frozen, 2 heads + shards
  append-only, exactly partitioned)`), and 3 scratch fixture repositories — a clone of the repository, a shard thawed after the event, no CHANGELOG.md at all — 3 identical, 0 differ in stdout, stderr and
  exit status. In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at deny-warnings rc=0 (clean on the first in-tree run). Next: slice `6ae` — `check_derived_counts.sh`
  behind a held shim (the arm counter itself).
  Slice 6ae (`2026-10-27`, `SEMULITH-XTASK-0041`; on clean 9fed766d, taken out of turn — no feature leaf unblocked): `DERIVED-COUNTS`
  is Rust — `xtask/src/check_derived_counts.rs` (477 lines) ports the bash doctrine line for line, natively this time: the
  claims table verbatim, each enumerator run through `bash -c` from the root as the script's `eval` ran it (whitespace stripped,
  a failure or silence a NO ENUMERATOR), the arm total derived in Rust by the script's own rules — bash `arm "` and `score "`
  lines, a shim's `exec cargo xtask` subcommand resolved to `xtask/src/<name>.rs` and its `tally.arm(`/`tally.score(` lines, a
  missing module yielding no total — the live documents read from the routes registry's `hot_live` rows, and the claim
  extraction left to the shell's own `grep -E`/`grep -oE` so the match is the script's; `--list` kept; the twelve bash arms are
  twelve `tally.arm(` calls, the arm total unchanged; `scripts/check_derived_counts.sh` a shim of `cargo xtask check-derived-counts`.
  Measured in a disposable draft crate: the self-test `12 pass / 0 fail` with stdout and stderr byte-identical to the bash
  driver's, the real tree's stdout and stderr byte-identical (`DERIVED-COUNTS: ok (3 derived count claim(s) re-derived)`), the
  `--list` table byte-identical, and 3 scratch fixture repositories — a clone of the repository, a drifted arm-total claim in LIVE_STATUS.md, no routes registry — 3 identical, 0 differ in stdout, stderr and exit
  status. In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at deny-warnings rc=0 (clean on the first in-tree run). Next: slice `6af` — `check_artifact_cleanup.sh`
  behind a held shim.
  Slice 6af (`2026-10-27`, `SEMULITH-XTASK-0042`; on clean b57535c2, taken out of turn — no feature leaf unblocked): `ARTIFACT-COHORT`'s
  driver is Rust — `xtask/src/check_artifact_cleanup.rs` (343 lines) ports the bash driver line for line: the cleanup
  instrument's seven probe suites and their mutations run as the driver ran them (`python3 -B [-O] scripts/probe_*.py`), plain and
  optimized, NOT ported; the eighteen instruments and controls checked tracked through `git ls-files --error-unmatch`; no real
  cleanup runs; the sixteen bash `score` lines are sixteen `tally.score(` lines (this driver scores, it does not `arm`; the counter
  reads both idioms since 6q), the arm total unchanged; `scripts/check_artifact_cleanup.sh` a shim of `cargo xtask
  check-artifact-cleanup`. Measured in a disposable draft crate: the self-test `150 pass / 0 fail` with stdout and stderr
  byte-identical to the bash driver's, the real tree's stdout and stderr byte-identical (the self-test line, then `ARTIFACT-COHORT:
  bounded planning/checking controls green; no real cleanup`), the unknown-arguments refusal identical, and 2 scratch fixture
  repositories — a clone of the repository, an instrument untracked in the clone — 2 identical, 0 differ in stdout, stderr and exit status. In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at
  deny-warnings rc=0 (clean on the first in-tree run). `check_readme_routes.sh`, the last free driver, is DEFERRED with its reason: its controls shadow the
  PATH tools (`wc`, `python3`, `sort`, `grep` in a fixture `bin/`), so a port must call the same tools to stay measurable by them —
  sized at about 600 lines of Rust, out of proportion for an out-of-turn slice while features wait. Next: slice `6ag` —
  `check_source_format.sh` over `sexp.rs`, the first of the three `sexp`-only callers.
  Slice 6ag (`2026-10-27`, `SEMULITH-XTASK-0043`; on clean afee5b58, taken out of turn — no feature leaf unblocked): `SOURCE-FORMAT`
  is Rust — `xtask/src/check_source_format.rs` (452 lines) ports the driver's inline Python line for line over the harness's own
  reader: every file of the four families (tracked under `git`, everything there under `fs`), a retired-format file an OUTSIDE
  FORMAT, a `.sexp` the reader refuses UNREADABLE with the reader's own text (`sexp.rs` equal to the pinned `scripts/sexp.py`,
  refusal texts included — 6j, 6p), a corpus without a `.sexp` NO SEXP SOURCE, an empty corpus refused; the shared reader's
  refusal probe runs as the script ran it, plain and optimized; the seven bash arms and eighteen `score` lines are seven
  `tally.arm(` calls and eighteen `tally.score(` lines, the arm total unchanged; `scripts/check_source_format.sh` a shim of
  `cargo xtask check-source-format`. Measured in a disposable draft crate: the self-test `25 pass / 0 fail` with stdout and stderr
  byte-identical to the bash driver's, the real tree's stdout and stderr byte-identical (`SOURCE-FORMAT: ok (331 source-of-truth
  file(s) under definitions/ schema/ profiles/ materials/, all in the one format)`), and 3 scratch fixture repositories —
  a clone of the repository, a `.toml` planted and tracked under a unit, an unterminated `.sexp` planted and tracked — 3 identical, 0 differ in stdout, stderr and exit status. In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at deny-warnings
  rc=0 (clean on the first in-tree run). Next: slice `6ah` — `check_semantics_corpus.sh` over `sexp.rs`.
  Slice 6ah (`2026-10-27`, `SEMULITH-XTASK-0044`; on clean 5284f544, taken out of turn — no feature leaf unblocked): `SEMANTICS`'s
  driver is Rust — `xtask/src/check_semantics_corpus.rs` (573 lines) ports the driver's inline Python line for line: the
  semantics documents paired with the fragments beside them and judged by `scripts/check_semantics.py`, spawned as the Python spawned
  it; the encoding documents read through the harness's own reader (`sexp.rs`) — the composed fragments' names, the fragment root —
  and the refinement rule judged by `check_semantics.compose` through `python3 -`, as the Python called it in-process; the citations
  arm's availability probe through `python3 -` with the Python's own exception tuple, `check_citations.py --corpus` spawned when the
  pages are present, the NAMED SKIP otherwise; the eight bash arms are eight `tally.arm(` calls, the arm total unchanged;
  `scripts/check_semantics_corpus.sh` a shim of `cargo xtask check-semantics-corpus`. Two intended differences on paths no corpus
  has: an encoding without `(fragment-root …)` and a form-less encoding are reported UNREADABLE where the inline Python ended with a
  traceback (measured in a fourth clone with the root form removed: the bash driver's traceback, status 1; the port's `UNREADABLE` finding, status 1). Measured in a
  disposable draft crate: the self-test `8 pass / 0 fail` with stdout and stderr byte-identical to the bash driver's, the real
  tree's stdout and stderr byte-identical (`SEMANTICS: ok (14 check(s) — pairs, refinement rule, citations)`), and 3
  scratch fixture repositories — a clone of the repository, a semantics document planted without a fragment beside it, a planted pair whose rule cites nothing — 3 identical, 0 differ in stdout, stderr and exit status. In tree: `cargo test -p xtask` `test result: ok. 17 passed`;
  clippy at deny-warnings rc=0 (clean on the first in-tree run). Next: slice `6ai` — `check_upstream_index.sh` behind a held shim, the last `sexp` caller.
  Slice 6ai (`2026-10-27`, `SEMULITH-XTASK-0045`; on clean b41abdba, taken out of turn — no feature leaf unblocked): `UPSTREAM-INDEX`'s
  driver is Rust — `xtask/src/check_upstream_index.rs` (562 lines) ports the bash driver line for line: the inline Python judge
  (every issue record against its two indices and report, the verified pins, the blocks entries against every tree's leaves, the
  subtree's self-containment) runs verbatim through `python3 -` as a string constant extracted from the script, reading the records
  with the pinned `sexp.py` it copies into the scratch tree, NOT ported; the controls write the script's synthetic tracker (its
  `mk`, `idx`, `reset` and record heredocs as the same texts, its four Python edits as the same replacements) and print one line per
  arm as the script did; the scan runs without a self-test gate, as the script ran it; the twenty-one bash arms are twenty-one
  `tally.arm(` calls, the arm total unchanged; `scripts/check_upstream_index.sh` a shim of `cargo xtask check-upstream-index`. Measured
  in a disposable draft crate: the self-test `21 pass / 0 fail` with stdout and stderr byte-identical to the bash driver's, the real
  tree's stdout and stderr byte-identical (`UPSTREAM-INDEX: ok (3 issue record(s) mirrored by both indices)`), and 4
  scratch fixture repositories — a clone of the repository, the top index carrying a stale state, the vendor index carrying a stale severity, a record without its blocks field — 4 identical, 0 differ in stdout, stderr and exit status. In tree: `cargo test -p xtask` `test result: ok. 17 passed`;
  clippy at deny-warnings rc=0 (clean on the first in-tree run). The `sexp` callers are all ported; of the registry's forty-two drivers, twenty-nine answer
  through shims, one is deferred with its reason, and eleven call `dossier_sexp`, `record_catalog`, `check_sexp_schema`,
  `gate_report`, `specfp` or `retain_div_statement` in their own text. The first precheck was refused by `SEAM-INTEGRITY`: its
  temporary-locality probe pins this entrypoint's `mkdir -p "$ROOT/target/tmp"` and `export TMPDIR` lines, which the shim now keeps
  (the cargo child's scratch stays on the volume, as the script's children's did). Next: slice `6aj` — `check_contract_freeze.sh` behind a held
  shim, its inline judge (over the pinned `record_catalog` and `sexp`) run verbatim — the first of the eleven pinned-module callers.
  Slice 6aj (`2026-10-27`, `SEMULITH-XTASK-0046`; on clean c1b98abf, taken out of turn — no feature leaf unblocked): `CONTRACT-FREEZE`'s
  driver is Rust — `xtask/src/check_contract_freeze.rs` (391 lines) ports the bash driver line for line: the inline Python judge
  (every unit's contract versions against their obligation records — members, pins, extensions, supersessions — over the pinned
  `record_catalog` and `sexp`) runs verbatim through `python3 -` as a string constant extracted from the script, from the scratch
  tree in the controls where the script symlinked `scripts/`, NOT ported; the controls take the real contract and its rendered
  catalogue and apply the script's `sed` edits as the same first-occurrence and range replacements; the ancestry probe runs plain
  and optimized — it extracted the judge from the shell driver's text, so it now rebuilds the same shell function around the Rust
  module's verbatim constant when the driver is a shim (the first in-tree self-test refused with `real shell judge boundary changed`;
  the probe's file missed the slice commit's staging and lands in slice 6aj-b, `SEMULITH-XTASK-0055`); judge first, controls only for a pass; the nine bash arms are nine `tally.arm(` calls, the arm total unchanged;
  `scripts/check_contract_freeze.sh` a shim of `cargo xtask check-contract-freeze`. Measured in a disposable draft crate: the
  self-test `13 pass / 0 fail` with stdout and stderr byte-identical to the bash driver's, the real tree's stdout and stderr
  byte-identical (`CONTRACT-FREEZE: ok (1 versioned unit(s), 3 version(s), 0 finding(s))`), and 3 scratch fixture repositories — a clone of the repository, a frozen version's record edited in its catalogue part, a member dropped from the contract — 3 identical, 0 differ in stdout,
  stderr and exit status. In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at deny-warnings rc=0 (clean on the first in-tree run). Next: slice `6ak` —
  `check_fp_vectors.sh` behind a held shim (its generator and judge spawned as before).
  Slice 6ak (`2026-10-27`, `SEMULITH-XTASK-0047`; on clean 1be4fb4c, taken out of turn — no feature leaf unblocked): `FP-VECTORS`'s
  driver is Rust — `xtask/src/check_fp_vectors.rs` (415 lines) ports the bash driver line for line: the generator
  (`scripts/gen_fp_vectors.py --check`, `--out`, `--fixtures-out`) spawned as the script spawned it; the hardware cross-check — the
  spec-side reference `scripts/specfp.py` against the host's IEEE in RNE, directed ties, 400 seeded cases, the format conversions —
  run verbatim through `python3 -` as a string constant extracted from the script, NOT ported; the controls write the generator's
  table into scratch and apply the script's `sed` edits as first-occurrence replacements, its `printf >>` as an append and its
  `awk` field rewrite as the same seventh-field toggle rebuilt with single spaces; the mutated reference judged from its own
  directory; controls first, then the table's `--check`, then the cross-check, as the script ordered them; the seven bash arms are
  seven `tally.arm(` calls, the arm total unchanged; `scripts/check_fp_vectors.sh` a shim of `cargo xtask check-fp-vectors`.
  Measured in a disposable draft crate: the self-test `7 pass / 0 fail` with stdout and stderr byte-identical to the bash
  driver's, the real tree's stdout and stderr byte-identical (`FP-VECTORS: ok (crates/semulith-core/src/fp/tests/vectors.rs matches the spec-side reference, 230 vectors + 3168 fixtures; reference vs hardware RNE: agree 2131)`), and 3 scratch fixture repositories — a clone of the repository, an expected value edited by hand in the tracked table, a fixture row's expected value edited — 3 identical, 0 differ in stdout,
  stderr and exit status. In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at deny-warnings rc=0 (clean on the first in-tree run). Next: slice `6al` —
  `check_gate_report.sh` behind a held shim (two arms; the report judge spawned as before).
  Slice 6al (`2026-10-27`, `SEMULITH-XTASK-0048`; on clean 2532f41f, taken out of turn — no feature leaf unblocked): `GATE-REPORT`'s
  driver is Rust — `xtask/src/check_gate_report.rs` (358 lines) ports the bash driver line for line: the generator
  (`scripts/gate_report.py [<profile>] --gate <gate> --stdout`, stderr discarded), its own `--self-test` and the runtime-root probe
  (plain and `-O`, the `git-root` mutation) spawned as the script spawned them, NOT ported; the controls run against the REAL
  reports — every `profiles/<id>/G?-REPORT.md` in the glob's order and the repo-level `BREADTH` report — determinism, the
  `**Verdict:` marker edit as the same first-occurrence replacement, the tamper's visibility; a stale report explained as before
  (`diff` spawned on a scratch copy of the generated text, twenty lines indented, the regeneration command); the two bash arms
  are two `tally.arm(` calls inside the same two-mode loop, the arm total unchanged; `scripts/check_gate_report.sh` a shim of
  `cargo xtask check-gate-report`. Measured in a disposable draft crate: the self-test `20 pass / 0 fail` with stdout and stderr
  byte-identical to the bash driver's, the real tree's stdout and stderr byte-identical (`GATE-REPORT: ok (5 generated report(s) in sync with their inputs)`), and 3 scratch fixture repositories — a clone of the repository, a profile report's verdict marker edited by hand, the repo-level report edited — 3 identical, 0 differ in stdout,
  stderr and exit status. In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at deny-warnings rc=0 (clean on the first in-tree run). Next: slice `6am` —
  `check_materials_bill.sh` behind a held shim (eleven arms).
  Slice 6am (`2026-10-27`, `SEMULITH-XTASK-0049`; on clean 629a7f61, taken out of turn — no feature leaf unblocked): `MATERIALS-BILL`'s
  driver is Rust — `xtask/src/check_materials_bill.rs` (538 lines) ports the bash driver line for line: the inline Python judge
  (every registered unit's bill against the pinned dossier — the generated fragments' DRIFT, a `###` section and a does-not-supply
  statement for every material the declared shape enumerates — over the pinned `sexp`, `dossier_sexp` and `gen_model_book`) runs
  verbatim through `python3 -` as a string constant extracted from the script, NOT ported; the generator, its catalogue tests and
  the controls' four inline Python edits spawned as the script spawned them; the controls re-root the REAL dossiers and book (the
  processor's, the UART's, the board's) into scratch as the script did; the eleven bash arms are eleven `tally.arm(` calls, the
  arm total unchanged; `scripts/check_materials_bill.sh` a shim of `cargo xtask check-materials-bill`. Measured in a disposable
  draft crate: the self-test `11 pass / 0 fail` with stdout and stderr byte-identical to the bash driver's, the real tree's stdout and
  stderr byte-identical (the per-unit lines and `MATERIALS-BILL: ok (6 unit(s) — generated tables match the pinned data; every material states what it does not supply)`), and 3 scratch fixture repositories — a clone of the repository, a generated table edited by hand in the tracked book, a material's section removed from the tracked bill — 3 identical, 0 differ in stdout,
  stderr and exit status. CHANGELOG.md, at 65714 B against its 65,536 B ceiling after this slice's entry, is sharded in this
  unit (`scripts/shard_history.py --max-bytes 49152`: `docs/changelog/shard-0419.md` sealed, the head 48532 B; the prechecks had refused the ceiling). In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at deny-warnings rc=0 (clean on the first in-tree run). Next: slice `6an` —
  `check_definition_gen.sh` behind a held shim (forty-two arms).
  Slice 6an (`2026-10-27`, `SEMULITH-XTASK-0050`; on clean 034b14c5, taken out of turn — no feature leaf unblocked): `DEF-GEN`'s driver
  is Rust — `xtask/src/check_definition_gen.rs` (1046 lines) ports the bash driver line for line: the generator
  (`scripts/gen_definition.py --check|--out …`), the C-expansion and C-engine probes (plain and under their three mutations) and the
  controls' four inline Python programs (the fence mutator over the pinned `sexp`/`records_sexp`, the ghost instruction, the fieldless
  operand, the reversed decode rows) spawned as the script spawned them, NOT ported; the controls run over a surgical copy of the real
  unit and over staged rv64gc compositions written as the script's heredocs wrote them (the A, F, F+D, M and C surfaces), the `sed`
  and `grep -v` edits as the same literal replacements and line drops, the needle checks as the same substring tests; the census's
  two pairs judged as before, the encoding's digest through the harness's hasher; the forty-two bash arms are forty-two `tally.arm(`
  calls (the needle loops keep their one call each, as the script's did), the arm total unchanged; `scripts/check_definition_gen.sh`
  a shim of `cargo xtask check-definition-gen`. Measured in a disposable draft crate: the self-test `56 pass / 0 fail` with stdout and
  stderr byte-identical to the bash driver's, the real tree's stdout and stderr byte-identical (`DEF-GEN: ok (crates/semulith-core/src/definition_rv64gc.rs matches the canonical definition, encoding sha256 8b77378df968f968)` and the rv64gc line), and 3 scratch fixture repositories — a clone of the repository, the tracked rv64i module edited by hand, the tracked rv64gc module edited by hand — 3 identical, 0 differ in stdout,
  stderr and exit status. In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at deny-warnings rc=0 (clean on the first in-tree run). Next: slice `6ao` —
  `check_dossier_schema.sh` behind a held shim (forty-seven arms).
  Slice 6ao (`2026-10-27`, `SEMULITH-XTASK-0051`; on clean 25d1351b, taken out of turn — no feature leaf unblocked): `DOSSIER-SCHEMA`'s
  driver is Rust — `xtask/src/check_dossier_schema.rs` (666 lines) ports the bash driver line for line: the inline Python sweep
  (every tracked `profiles/*/*.sexp` against its same-named or suffix-family schema through `scripts/check_sexp_schema.py`, the
  schema-less documents counted BY NAME, over the pinned `dossier_sexp`) runs verbatim through `python3 -` as a string constant
  extracted from the script, NOT ported; the three probes of the controls — the experiment verification cases, the expectation
  mapping (its `--emit` fixtures written as the redirection wrote them) and its mutation, the bounded-artifact suite plain and `-O`
  under its ten omissions — spawned as the script spawned them; the synthetic facet schema and documents written as the heredoc
  and printfs wrote them; the forty-seven bash arms are forty-seven `tally.arm(` calls, unrolled as the script's were, the arm total
  unchanged; `scripts/check_dossier_schema.sh` a shim of `cargo xtask check-dossier-schema`. Measured in a disposable draft crate:
  the self-test `47 pass / 0 fail` with stdout and stderr byte-identical to the bash driver's, the real tree's stdout and stderr
  byte-identical (`DOSSIER-SCHEMA: ok (277 __SKIPPED__ 4 (baseline.sexp, portability.sexp, sail-identity.sexp))`), and 3 scratch fixture repositories — a clone of the repository, a dossier document planted with no same-named schema, a tracked dossier document left unterminated — 3 identical, 0 differ in stdout,
  stderr and exit status. In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at deny-warnings rc=0 (clean on the first in-tree run). Next: slice `6ap` —
  `check_requirements.sh` behind a held shim (seventy-nine arms).
  Slice 6ap (`2026-10-28`, `SEMULITH-XTASK-0052`; on clean 258c10f6, taken out of turn — no feature leaf unblocked): `RECORD-SCHEMA`'s
  driver is Rust — `xtask/src/check_requirements.rs` (1910 lines) ports the bash driver line for line: the 670-line inline Python
  judge (every tracked record file against its schema and the fifteen cross-checks, over the pinned validators and readers) runs
  verbatim through `python3 -` as a string constant extracted from the script, NOT ported — the root passed as `.` as the script
  passed it; the controls' fixture writers are the script's own `python3 -c` programs re-composed around the same JSON records, the
  record mutations piped through the same one-line programs, the versioned-mirror and mirror-derive fixtures and the `--audit` report
  run verbatim, the two probes (plain and `-O`) and the workspace's Rust graph checker (`cargo run -p semulith-cli -- check-examples`)
  spawned as before; the seventy-nine bash arms are seventy-nine `tally.arm(` calls, the arm total unchanged;
  `scripts/check_requirements.sh` a shim of `cargo xtask check-requirements`. Measured in a disposable draft crate: the self-test
  `79 pass / 0 fail` with stdout and stderr byte-identical to the bash driver's, the real tree's stdout and stderr byte-identical
  (`RECORD-SCHEMA: ok (23 record file(s) validate and agree with their profile; the Rust graph checker accepts the examples bundle)`), and 3 scratch fixture repositories — a clone of the repository, a requirement's statement edited away from its decision, a JSONL file planted that no schema governs — 3 identical, 0 differ in stdout,
  stderr and exit status. In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at deny-warnings rc=0 (clean on the first in-tree run). Next: slice `6aq` —
  `check_guest_gen.sh` behind a held shim (332 arms, the largest driver).
  Slice 6aq (`2026-10-28`, `SEMULITH-XTASK-0053`; on clean fd4ed3e9, taken out of turn — no feature leaf unblocked): `GUEST-GEN`'s
  driver is Rust — `xtask/src/check_guest_gen.rs` (4002 lines, generated from the script by `target/xtask/xt0052/gen_module.py`:
  the sixteen fixture arms and the two mode loops written by hand, the 312 probe arms derived from the script's `out=…; arm …`
  pairs) ports the bash driver line for line: the generator (`scripts/gen_guests.py --check|--out …`), the base-mirror governor
  (`scripts/check_gc_mirror.py`), the twenty-odd probe suites (plain and `-O`, each under its mutations) and the controls' three
  inline Python edits spawned as the script spawned them, NOT ported; the surgical guests directory copied as the script copied
  it, the `sed`, `printf >>`, `mv` and `cp` edits as the same literal operations; the quiet run keeps the controls' output in
  `target/guest-gen/self-test.log` and shows its last eighty lines on a refusal, as the script did; the 332 bash arms are 332
  `tally.arm(` calls (the two mode loops keep their one GREEN and one RED call each, as the script's did), the arm total unchanged;
  `scripts/check_guest_gen.sh` a shim of `cargo xtask check-guest-gen`. Measured in a disposable draft crate: the self-test
  `400 pass / 0 fail` with stdout and stderr byte-identical to the bash driver's, the real tree's stdout and stderr byte-identical (the
  three `GUEST-GEN: ok` lines, `GUEST-GEN: ok (the base mirror holds: 46 file(s) byte-identical, 42 independently checked count-only migration(s), 7 recorded re-derivation(s), 3 pinned image-identical source re-derivation(s))`), and 3 scratch fixture repositories — a clone of the repository (the vendored crates and cargo home copied in), the tracked rv64i fixture edited by hand (`FAIL`, by name), the tracked rv64gc fixture edited by hand (the controls judge the LIVE rv64gc pair, so the edit refuses the check — exit 2 — as 6u's and 6x's did; the same open question) — 3 identical, 0 differ in stdout,
  stderr and exit status (§9, recorded in `docs/knowledge/a-clone-of-the-repository-cannot-build-what-the-repository-builds.md`: a bare clone lacks the
  untracked vendored source root `.app-data/vendor`, so the C-image probes refused on both sides until the directory was linked in).
  `docs/tasks/XTASK.md`, over its 131,072 B per-part ceiling with this slice's text (133490 B; the prechecks refused it), had the
  closed rows 6y–6ap (37565 B, one contiguous span of 108 rows) moved verbatim into `docs/tasks/archive/XTASK-4.md` in the same commit
  (the a43b mechanism, as parts 1–3: SHA256 in the part's table, one pointer left in the checklist; the live leaf 96007 B) — recorded here by
  slice 6aq-b (`SEMULITH-XTASK-0056`), the slice commit's text having missed it. In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at deny-warnings rc=0 (clean on the first in-tree run). Next: slice `6ar` —
  `check_profile_consistency.sh` behind a held shim (the last pinned-module caller; 51 arms, 2361 lines).
  Slice 6k (`2026-10-27`, `SEMULITH-XTASK-0019`; on clean 04b650e7, the tooling slice taken while every feature leaf waits on a
  ruling — recorded in the Decisions): `EXERCISE-COVERAGE` is Rust — `xtask/src/check_exercise_coverage.rs` (874 lines; the
  220-line inline Python ported line for line as the first consumer of the Rust reader, with `riscv_asm.resolve_composition`
  ported beside it: one resolver, a missing fragment or an unmet `requires` refused by the pinned words) behind a held shim
  (`scripts/check_exercise_coverage.sh` → `cargo xtask check-exercise-coverage`). Measured before the apply in a disposable
  draft crate: the self-test `23 pass / 0 fail` (23 bash arms out, 23 `tally.arm(` in — the arm total unchanged), the real
  tree's stdout and stderr byte-identical to the bash driver's (`ok (5 profile(s) — every declared form exercised, 19/19 /
  200/200 / 52/52)`), and seven scratch fixture trees — green, unexercised, denominator lie, no composition, unresolved form,
  no guests, device contradiction — identical in stdout, stderr and exit status (`7 identical, 0 differ`; the first pass
  compared only the refusal path: the fixture roots lacked the two fragments the pseudo arms copy, both drivers refused
  alike). In tree: `cargo test -p xtask` `test result: ok. 12 passed`; clippy at deny-warnings rc=0 (clean on the first run; rustfmt reflowed the hand-written module before the chain). Next: slice `6l` — `check_unit_composition.sh`,
  the second consumer of the composition resolver, after the next five feature units.

- ID: `XTASK.7` — **the focused set runs API-DOCS**
  Status: `done` (`2026-10-26`, `SEMULITH-XTASK-0011`; owned on clean eaa63f58; evidence target/xtask/xt0012)
  Goal: `cargo xtask focused` runs the rustdoc check before `make book` (`decision_focused-set-runs-api-docs.md`).
  Result: `FOCUSED` gains `bash scripts/check_rustdoc.sh` (the registered driver path, a shim of
  `cargo xtask check-rustdoc`) between `check_requirements.sh` and `make book`; the set is 27 checks and the
  test says so. Measured on the clean HEAD and on the finished slice: `focused: 0 red of 26` → `0 red of 27`, 25 of
  the 26 earlier verdict lines byte-identical, the one difference `SEAM-INTEGRITY`'s box count (1543 → 1548: this
  leaf's five acceptance rows), one new line `API-DOCS: ok (5 crate(s) documented …)`; RED: a broken intra-doc
  link in `semulith-core` makes the run `1 red of 27` naming the lint and the line, restored byte-identical, the
  altered source built only in a disposable target directory. Documentation commits no longer run the check by
  hand.

- ID: `XTASK.8` — **the commit gate under ten minutes**
  Status: `done` (`2026-10-27`; opened `2026-10-26` on the director's instruction: "50min is not acceptable, that is way too
  long, we need to shorten it by a lot to accelerate feature implementation"; the tooling unit of the 5:1 ratio in
  place of slice 6j — slices a–c `SEMULITH-XTASK-0016`, slice d `SEMULITH-XTASK-0017`: 52–56 min → 6.8 min for a code
  commit, 27 s for a documentation commit)
  Goal: the pre-commit gate well under ten minutes for a code commit and a few minutes for a docs-only commit —
  the same checks, the same verdict lines, the same refusals; only wall time and the order of EXECUTION change,
  the order of REPORTING kept.
  Measured before (ddcee89f): the gate ran the 11 universal checks and the project slot's 41 one after another;
  the lived gates of 2026-10-26 (chain logs): 52–56 min (56, 52, 52 and 55 min); the per-check census (every project check at once on
  12 cores) put PROFILE-CONSISTENCY at 45 of those minutes, and alone, serial, on an idle machine its self-test
  is 2746 s (45.8 min) — 51 fixture arms 2.7 s in total, 1114 probe invocations (each a distinct `python3 [-O]
  scripts/probe_*.py [--mutation m]`) 2730 s of it — the heaviest script probe_matched_gpr_unit_evaluation.py at 11 s × 54, the longest single invocation probe_div_method.py 47 s; the census's serial sum, 3253 s (54 min), agrees with the lived
  gates (census under load: PROFILE-CONSISTENCY 2687 s, GUEST-GEN 201 s, RECORD-SCHEMA 97 s, ARTIFACT-COHORT 48 s, the rest ≤ 40 s).
  Slice a — the censuses (above). Slice b — `scripts/check_doctrines.project.sh` runs its registered checks
  through a bounded pool (`xargs -P`, POSIX, so the hook runs under any bash; `DOCTRINE_JOBS=1` is the old serial
  run, `DOCTRINE_TIMES=<file>` records each check's wall time) and reports them in registry order: a failing
  check's complete output, nothing for a green one — byte-for-byte the serial loop's output, measured on a stub
  registry (two red, three green, two cargo, one missing path) under pools of 1 and 12. Safe because every check
  owns its scratch (mktemp under target/doctrine-selftest, or a path only it uses — census in target/xtask/xt0017),
  no check writes a tracked file (mtime census over two pooled runs), and the cargo-invoking checks run one after
  another in a single LANE beside the pool: cargo re-uplifts a binary by copy to a fresh inode on every
  `cargo run` and releases its lock before the exec, so two concurrent runs of one binary race (the chain's own
  gate refused once with `never executed`; 4 of 36 runs failed at six-way concurrency). The lane is detected from
  each script's text (`grep -q cargo`): 13 checks summing 197 s, never overlapping (red_pool.sh `LANE-SERIAL`).
  Project slot: the pooled gate 406 s, its checks' own walls summing to 1137 s.
  The pool exposed a latent race in `scripts/artifact_cargo.py`: on macOS `killpg` on a group whose only member
  is an exited, unreaped leader returns EPERM (measured: zombie leader → EPERM, reaped → ESRCH, zombie leader
  with a live descendant → OK and the descendant dies); `_stop` tolerated ESRCH alone, so the pipe-overflow
  test's child, finishing first under load, made ARTIFACT-COHORT refuse once in the pooled run. `_stop` now
  tolerates EPERM too (nothing owned can be alive when it is returned); a 24th Cargo test with its omission
  seam `stop-zombie` reproduces the exact failure (ARTIFACT-COHORT self-test 148 → 150 arms).
  Slice c — PROFILE-CONSISTENCY's self-test prefetches its probe invocations in parallel
  (`scripts/doctrine_prefetch.py`, which enumerates them from the script's own text) and answers each
  `out="$(python3 …)"` from the record through a `python3` function that shadows the command inside the
  self-test only (an exact argv match is answered; anything else — a program on stdin included — runs live: a
  missed shape costs time, never a wrong answer; `PROFILE_CONSISTENCY_PREFETCH=0` is the serial control; eight
  unit controls in target/xtask/xt0017/control_shadow.sh). `--self-test` output identical with and without it;
  wall 2746 s (45.8 min) → 447 s (7.5 min: 5 s recording, ~350 s parallel, the rest answering; 0 misses; 24 jobs no faster than 12 — CPU-bound). The full gate after slices b and c, idle machine: 406 s (6.8 min), `=== all doctrines green ===`: PROFILE-CONSISTENCY 403 s, GUEST-GEN 323 s, RECORD-SCHEMA 97 s, ARTIFACT-COHORT 67 s, the rest under 45 s; the eleven universal checks together 3.1 s.
  Slice d (`2026-10-27`, applied on clean fa536bf7; evidence target/xtask/xt0018; `decision_docs-only-gate-path.md`
  first) — the docs-only path, one level up from the arms: a check that DECLARES its input closure (the tracked
  prefixes it reads, `DOCTRINE_CLOSURES` beside the registry, declared only after reading the check and the Python
  it calls for every path they open) is answered from its last GREEN run when the commit stages nothing inside the
  closure and the closure's content key (`git ls-files -s` over it, digested — every blob id as the commit will
  carry it) equals the recorded one (target/doctrine-gate/green/<ID>, per clone). No declaration, no staged set
  (a run outside a commit), a staged path inside, or a differing key: the check runs; a refusal is never recorded;
  `DOCTRINE_DOCS_ONLY=0` is the control and `DOCTRINE_TIMES` records a skip as `skipped`. Six closures declared —
  PROFILE-CONSISTENCY, GUEST-GEN, RECORD-SCHEMA, ARTIFACT-COHORT, DEF-GEN, CONTRACT-FREEZE — every one of them
  reading `scripts/` and none a document, so a documentation commit skips exactly the checks that bound the gate.
  Controls in a scratch repository (red_docs_only.sh): ten scenarios as predicted — no staged set runs everything; the first docs-only run records green (the red stub never); the second skips the closure stub only, serial and pooled alike with identical stderr; `DOCTRINE_DOCS_ONLY=0`, a staged path inside the closure and committed closure content no run has seen each run it; green again after. Measured: 27 s, `=== all doctrines green ===`, the six declared checks answered from the record (the recording run before it, every check running: 508 s); a code commit: every check runs — 406 s alone, 8–9.4 min as the chains lived it.
  Acceptance: the gate's verdict lines and refusals unchanged on the same tree (measured on the stub registry
  and on a real refusal); a code commit's gate well under ten minutes; every check's own scratch untouched by
  the others.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `XTASK.6` | `active` | slice `6ar`: `check_profile_consistency.sh` behind a held shim — the last pinned-module caller; taken out of turn while every feature leaf waits on a ruling |
| 2 | `XTASK.4` | `active` | the remaining 13 scripts wait, each constraint recorded; `bootstrap.sh` and `check_portability.sh` are measurable offline |

## Decisions

- `2026-10-23`: the director: "Migration to xtask shall be done with extrem care, and incrementally for not
  breaking anything" (`decision_rust-native-tooling.md`).
- `2026-10-26`: the director: "Please alternate Rust tooling port and project feature implementation. Do not get
  stuck on Rust's tooling because the project work needs to progress" (`decision_alternate-port-and-features.md`):
  after a slice lands, the next unit is a project feature leaf; a slice drafted ahead waits its turn.

## Open Questions

- (Resolved 2026-10-26 by `decision_focused-set-runs-api-docs.md`, executed by `XTASK.7`.) Whether `cargo xtask
  focused` should also run API-DOCS: the set reproduced the pre-XTASK scratch set, which predates the doctrine,
  and XTASK.3's gate refusal is what it would have caught.
- The front door's silent exit (found in `XTASK.4` slice `4a`, measured with cargo 1.95.0 in a throwaway
  crate): with an invalid host `RUSTFLAGS`, `cargo run --quiet` exits 1 and prints nothing; without `--quiet`
  it prints the cause; `cargo build --quiet` exits 101 with the cause. Options: drop `--quiet` from the alias
  (cargo's "Finished/Running" lines join stderr; stdout unchanged), or leave it, since only a broken
  environment reaches it. Not changed in `4a`; a change to XTASK.1's measured output is its own slice.
- Whether new tooling must be born in Rust once XTASK.1 exists — proposed in the decision record; to be
  confirmed by the director before any check enforces it. Does not block XTASK.1.
- (6r, `2026-10-27`) `CITATION-QUOTES`'s availability probe exits 1 for "pages absent" and Python exits 1 for an uncaught exception, so a sources manifest the reader refuses outside the probe's `except` tuple reads as absence — NAMED SKIP, exit 0 (measured in the 6r fixture `manifest-unreadable`; the card: `docs/knowledge/a-crash-that-exits-one-reads-as-an-absence.md`, landed with the family's second re-derivation in 6r-b). The port reproduces it; the doctrine's owner decides whether the probe should refuse (exit 2) on any exception — a one-line change to the script, re-measured through the shim.
- (6u, `2026-10-27`) `BOARD-VERDICT`'s controls copy the LIVE board (`profiles/netboard-lab-v0`) and expect it ACCEPTED, so a corpus whose live board is rejected makes the check refuse as non-discriminating (exit 2) instead of failing by name (exit 1) — measured in the 6u fixtures `no-board` and `rejected`. The port reproduces it; the doctrine's owner decides whether the controls should run over a frozen fixture board instead.
- (6x, `2026-10-27`) `STATE-GEN`'s controls judge the LIVE rv64gc pair (`profiles/rv64gc-lab-v0/state.sexp` against `crates/semulith-core/src/state_rv64gc.rs`) and expect it in sync, so a corpus whose live rv64gc module or census is edited makes the check refuse as non-discriminating (exit 2) instead of failing by name (exit 1) — measured in the 6x fixtures `gc-module-hand-edited` and `gc-census-silent`; the rv64i pair fails by name. The port reproduces it; the doctrine's owner decides, beside 6u's question, whether the controls should run over frozen fixture copies.

## Blockers

- None. (`XTASK.5`'s blocker of 2026-10-24 — the pinned `gate_report.py` reading `check-examples` in the CLI source —
  was resolved by decision on 2026-10-26: the command stays in the CLI; see the leaf.)

## Acceptance Checklist (leaf XTASK.1)

[Evidence requirements](../TASK_TREE_README.md#acceptance-checklist-required-for-any-leaf-that-lands-a-code-change).

- [x] **REPRODUCE / ISSUE** — before.log: `cargo xtask help` → `error: no such command: `xtask``; `ls -d xtask` absent; `grep -n "alias" .cargo/config.toml` empty at 79644a8.
- [x] **ROOT CAUSE (WHY + WHERE)** — the project's automation lives only in `Makefile` (14 .PHONY targets — first written 15, corrected by XTASK.3's measurement) and 288 scripts; `grep -rn "xtask" $(git ls-files)` had no hit; the director's direction (`decision_rust-native-tooling.md`) asks for xtask with extreme care, so the first step must move nothing: delegation.
- [x] **FIX** — `xtask/Cargo.toml`, `xtask/src/main.rs` (`diff -r` against the validated prototype: identical), the workspace member and its comment, the cargo alias, `Cargo.lock` (+4), the ratchet's `xtask` row and directory, README, ARCHITECTURE §4, the toolbox row.
- [x] **ADDRESSED (verified)** — `cmp target/xtask/xt0001/make-help.before target/xtask/xt0001/xtask-help.after` → `help identical to make help`; red.log: `make no-such-target` rc 2 and `cargo xtask no-such-target` rc 2, `unknown-target outputs identical`; SUMMARY.md broken → `make book` rc 2 and `cargo xtask book` rc 2, `broken-book outputs identical apart from timestamps`, restored `4ddfd80e78ce0148abb699ee10c7bd633a659b6472696201524ecd31dcf6ce33` byte-identical, `make book (restored) rc=0`; vendor-and-check.log: `make check rc=0 in 43 s`, `cargo xtask check rc=0 in 24 s`, `check outputs identical as sorted lines (timings and cargo progress lines removed)`, tests `287 passed`, `173 passed`, `17 passed`, 0 failed.
- [x] **NO REGRESSION** — checks.log: `API-DOCS --self-test: 13 pass / 0 fail`, `API-DOCS: ok (5 crate(s) documented; … 267 undocumented public item(s), each crate at its recorded count)`, `PORT-WEB: ok (workspace builds for wasm32-unknown-unknown)`; `make vendor` → `vendor: .app-data/vendor populated from Cargo.lock` (34 → 3 entries; the Miri leg re-syncs the rest); `bash scripts/check_readme_routes.sh` → `README-STABILITY: OK — README.md is 73/85 lines, 4404/4864 bytes`; `bash scripts/check_book_index.sh` → `BOOK-INDEX: ok`; focused checks rc 0 (focused-checks.json); no product crate source changed (`git status --short crates/` empty).
- [x] **LOCKSTEP** — README, ARCHITECTURE §4 (and so the book's architecture chapter), the execution toolbox row, `doctrine/undocumented_items.tsv`, the XTASK tree and docs/TASK_TREE.md, CHANGELOG, MEMORY.

## Acceptance Checklist (leaf XTASK.2)

- [x] **REPRODUCE / ISSUE** — the focused set existed only in untracked runners: `git ls-files | xargs grep -ln "check_memory_architecture.sh.*check_readme_routes"` empty at 31f64ba; target/p4-system-14/a42ax/focused-and-commit.sh, target/rustdoc/rd000[1-3]/focused-and-commit.sh, target/xtask/xt0001/focused-and-commit.sh — one copy per unit; `cargo xtask focused` → make's `No rule to make target` (rc 2).
- [x] **ROOT CAUSE (WHY + WHERE)** — `grep -n "Focused validation passes" docs/TASK_TREE_README.md` = 73: the workflow requires the validation but no tracked file defines the set, so each unit re-derived it from the previous scratch copy (TOOLBOX.md: a diagnostic in a scratch directory is a "trust me").
- [x] **FIX** — `FOCUSED`, `focused()`, `log_name()`, `utc_clock()`, `last_line()` and three tests in `xtask/src/main.rs`; README and toolbox rows.
- [x] **ADDRESSED (verified)** — the same tree, both runners: `scratch rc=0 in 163 s`, `xtask focused rc=0 in 156 s`, both `focused: 0 red of 26`, `26 verdict lines identical (command, rc, last line)`, `JSON records identical`; `1668 self-test arms` → `1667` in LIVE_STATUS: `scratch (broken) rc=1`, `xtask focused (broken) rc=1`, `bash scripts/check_derived_counts.sh rc=1` the single red line, `focused: 1 red of 26`, `broken-tree verdicts identical`, restored `86871d03ddec3b467ea4b8968f91d2213163962bdf2a636b00ce1cea7edd11e1` byte-identical; `cargo xtask focused --bogus` → rc 2 `usage: cargo xtask focused [--out DIR]`.
- [x] **NO REGRESSION** — no-regression.log: `cargo xtask help` vs `make help` → `help identical to make help (XTASK.1 delegation unchanged)`; `PORT-WEB: ok (workspace builds for wasm32-unknown-unknown)`; `make check rc=0 in 33 s` with `287 passed`, `173 passed`, `17 passed`, `3 passed` (xtask), 0 failed; `cargo fmt --all -- --check` rc 0; `API-DOCS: ok (5 crate(s) documented; … 267 undocumented public item(s), each crate at its recorded count)`; `cargo xtask focused` rc 0 before the commit (commit-focused/focused-checks.json).
- [x] **LOCKSTEP** — README (one command row), the execution toolbox row, the XTASK tree and docs/TASK_TREE.md, CHANGELOG, MEMORY.

## Acceptance Checklist (leaf XTASK.3)

- [x] **REPRODUCE / ISSUE** — nothing prevented a second definition: `grep -n '"focused"' xtask/src/main.rs` matched only the dispatch literal at dea2560, and no test read the Makefile; a `focused:` rule added to the Makefile would have been silently shadowed for `cargo xtask` users.
- [x] **ROOT CAUSE (WHY + WHERE)** — `grep -E '^[a-z][a-z-]*:' Makefile | wc -l` = 14 rules (`shasum -a 256 Makefile` = 8c36efd6d2271f30f4e9fdefdde36a1e9c0ced5e06a50ee2250274a90f881970; after.log lists them: help vendor gate check fmt clippy test book ci bench smoke-bench hooks bootstrap update-scaffold); xtask's natives: `focused` only — one source today by construction, but held by nothing.
- [x] **FIX** — `NATIVE` and the dispatch through it, `makefile_rules()` and two tests in `xtask/src/main.rs`; `python3 scripts/shard_history.py --max-bytes 49152` (shard.log).
- [x] **ADDRESSED (verified)** — red.log: with a temporary `.PHONY: focused …` and `focused:` rule, `cargo test -p xtask` → `focused is defined twice`, `test result: FAILED. 4 passed; 1 failed`; restored `8c36efd6d2271f30f4e9fdefdde36a1e9c0ced5e06a50ee2250274a90f881970` byte-identical → `test result: ok. 5 passed; 0 failed`.
- [x] **NO REGRESSION** — after.log: `help identical to make help`, `unknown target identical (rc 2)`; `cargo fmt --all -- --check` and `cargo clippy -p xtask --all-targets -- -D warnings` clean; shard.log: `completeness: 70 entries before == 52 kept + 18 moved, order and bytes exact`, `head: 62075 -> 48125 bytes`, `bash scripts/check_changelog_shards.sh` → `SHARD-FREEZE: ok (416 shard row(s) frozen, 2 heads + shards append-only, exactly partitioned)`; `cargo xtask focused` rc 0 before the commit (commit-focused/focused-checks.json).
- [x] **LOCKSTEP** — the XTASK tree (XTASK.1's target count corrected), docs/TASK_TREE.md, CHANGELOG and its shard, MEMORY.
- [x] **ROOT CAUSE** (defects owned mid-slice) — commit-focused-red-1/check_seam_integrity.log: `REGRESSED docs/tasks/XTASK.md: a current tracked acceptance box lacks a declared evidence signature`; commit.log: `API-DOCS: FAIL …` followed only by `missing documentation for a variant` lines and `awk: i/o error occurred while closing /dev/stdout`; api-docs-repro.log: `cargo doc rc=101`, `error: public documentation for `xtask` links to private item `NATIVE`` at `xtask/src/main.rs:14:88`, at line 1613 of the build's output — past the listing's `head -60`.
- [x] **ADDRESSED** (defects owned mid-slice) — `bash scripts/check_seam_integrity.sh` → `SEAM-INTEGRITY: ok (1478 current tracked acceptance box(es) match declared signatures; classification properties hold)`; api-docs-fix.log: `API-DOCS --self-test: 15 pass / 0 fail`; with the private link restored temporarily → `API-DOCS: FAIL …` listing exactly `xtask/src/main.rs:14:88  public documentation for `xtask` links to private item `NATIVE``; after the fix `API-DOCS: ok (5 crate(s) documented; … 267 undocumented public item(s), each crate at its recorded count)` rc 0; `bash scripts/check_derived_counts.sh` → `DERIVED-COUNTS: ok` after 1668 → 1670 arms.

## Acceptance Checklist (leaf XTASK.4)

- [x] slice 4a **REPRODUCE / ISSUE** — before.stdout: `bench: bench/semulith_verify.wasm (138930 bytes)` and the serve line, rc 0; `shasum -a 256 bench/semulith_verify.wasm` = 9afa2775c5c6c5406da879936f626316643f4cb40c0bea45be0e501dc4d3013e; `shasum -a 256 scripts/build_bench.sh` at 90c69268 = d7ad190b47e9f9a4…; `grep -c "build_bench" scripts/check_*.sh` empty — no gate arm names the script; `make bench rc=0`; `node scripts/smoke_bench.js` → `smoke_bench: ok (53 arms — clean 49, 3 trace-level mutants, the census arm)`.
- [x] slice 4a **ROOT CAUSE (WHY + WHERE)** — the bench build lived only in shell (`wc -l scripts/build_bench.sh` = 11): `cargo build --release -p semulith-verify --target wasm32-unknown-unknown`, a `cp` to `bench/`, two `echo` lines; inventory.md: 74 tracked scripts, 55 drivers, 0 pinned, 5 artifacts, 14 to port, 3 hook-coupled.
- [x] slice 4a **FIX** — xtask/src/main.rs: `build_bench` (cargo's status passed through, a failed copy 1, the same two lines), `NATIVE` gains `build-bench`, `PORTED` and the test `a_ported_script_is_a_shim_that_only_runs_its_subcommand`; scripts/build_bench.sh a three-command shim (`shasum -a 256` = e7dab7cc6d7a83bfe160caa5cd1599e8fcca89b810a4978eba2d29548e78bda6).
- [x] slice 4a **ADDRESSED (verified)** — `cmp before.stdout after-shim.stdout`, `… after-native.stdout`, `before-make.stdout after-make.stdout` → byte-identical, each rc 0, module 9afa2775c5c6c5406da879936f626316643f4cb40c0bea45be0e501dc4d3013e and mode `-rwxr-xr-x` unchanged; wasm-only RED (`CARGO_TARGET_WASM32_UNKNOWN_UNKNOWN_RUSTFLAGS="-C xt0004-bogus"`): old script, shim and subcommand rc 101, stdout 0 B, `grep -c "unknown codegen option"` 1 each, `make bench` rc 2; copy RED (module mode 444): old script rc 1 (`cp: … Permission denied`), shim rc 1 (`xtask build-bench: cannot copy the module to bench/semulith_verify.wasm: Permission denied (os error 13)`); shim RED: one appended line → `test result: FAILED. 5 passed; 1 failed` naming `scripts/build_bench.sh must stay a shim of cargo xtask build-bench`, restored `scripts/build_bench.sh: OK` (shasum -c).
- [x] slice 4a **NO REGRESSION** — `cargo test -p xtask` → `test result: ok. 6 passed; 0 failed`; `cargo fmt --all -- --check` clean; `cargo clippy -p xtask --all-targets -- -D warnings` clean; after-smoke.log `smoke_bench: ok (53 arms …)`; `cargo xtask focused` rc 0 before the commit; the pre-commit gate (wasm build, API-DOCS) on commit.
- [x] slice 4a **LOCKSTEP** — README (the xtask row no longer says nothing moved; a `build-bench` row; `README-STABILITY: OK — README.md is 75/85 lines, 4592/4864 bytes`), docs/toolbox/execution.md, docs/ARCHITECTURE.md (the book includes it), the tree (XTASK.4 inventory, slice 4a, the open question), docs/TASK_TREE.md, CHANGELOG, MEMORY.

## Acceptance Checklist (leaf XTASK.6)

Rows 6a–6o: [retained verbatim](archive/XTASK-1.md#acceptance-rows-6a-to-6o).
Rows 6p–6x (with 6r-b): [retained verbatim](archive/XTASK-2.md#acceptance-rows-6p-to-6x).
Rows 6y–6ap: [retained verbatim](archive/XTASK-4.md#acceptance-rows-6y-to-6ap).
- [x] slice 6aq **REPRODUCE / ISSUE** — before/ (bash driver at fd4ed3e9; target/xtask/xt0052/before/): the three `GUEST-GEN: ok` lines (`GUEST-GEN: ok (the base mirror holds: 46 file(s) byte-identical, 42 independently checked count-only migration(s), 7 recorded re-derivation(s), 3 pinned image-identical source re-derivation(s))`) rc 0, stderr empty; `GUEST-GEN --self-test: 400 pass / 0 fail`; `grep -c 'arm "' scripts/check_guest_gen.sh` = 332 (two inside mode loops, run four times each).
- [x] slice 6aq **ROOT CAUSE (WHY + WHERE)** — the driver lived in bash around `scripts/gen_guests.py`, `scripts/check_gc_mirror.py`, twenty-odd probe suites (`grep -c 'scripts/probe_' scripts/check_guest_gen.sh` = 290) and three inline Python edits; all of them stay as they are, spawned as the script spawned them.
- [x] slice 6aq **FIX** — xtask/src/check_guest_gen.rs (`shasum -a 256` = 8848ea5694b14acbd3f2e4d2bccb1fb9f1eea8d200eca3bf085f756b463f7483; `wc -l` = 4002; `grep -cE '^[[:space:]]+tally\.arm\('` = 332); main.rs doc bullet, `mod`, `NATIVE`, `PORTED`, dispatch; scripts/check_guest_gen.sh a shim (`exec cargo xtask check-guest-gen "$@"`); docs/tasks/XTASK.md's closed rows 6y–6ap moved verbatim into docs/tasks/archive/XTASK-4.md (37565 B, 108 rows, SHA256 in the part's table; `wc -c docs/tasks/XTASK.md` 133490 → 96007; recorded by 6aq-b).
- [x] slice 6aq **ADDRESSED (verified)** — the draft binary against before/: `cmp after/selftest.out before/selftest.out` rc=0, `cmp after/real.out before/real.out` rc=0, stderr identical both; 3 fixture repositories (target/xtask/xt0052/red/summary.txt): `RED/GREEN paths: 3 identical, 0 differ` — stdout, stderr and rc each.
- [x] slice 6aq **NO REGRESSION** — `cargo test -p xtask` → `test result: ok. 17 passed` (the shim test holds the new shim to one command); `cargo clippy -p xtask --all-targets -- -D warnings` rc=0 (clean on the first in-tree run); `cargo fmt -p xtask -- --check` rc=0; `bash scripts/check_guest_gen.sh` through the shim → the same three `ok` lines; `bash scripts/check_derived_counts.sh` → ok (332 bash arms out, 332 `tally.arm(` in; 1692 holds).
- [x] slice 6aq **LOCKSTEP** — docs/toolbox rows unchanged (the command still answers through the shim); the tree (slice 6aq, frontier 6ar, the Decisions bullet), the knowledge card and its INDEX row, the archive part 4 and its pointer (named by 6aq-b), docs/TASK_TREE.md, CHANGELOG, MEMORY.

## Acceptance Checklist (leaf XTASK.7)

- [x] **ROOT CAUSE (WHY + WHERE)** — the focused set did not run API-DOCS: `git show eaa63f58:xtask/src/main.rs | sed -n '/^const FOCUSED/,/^];/p' | grep -c check_rustdoc` = 0 against 26 entries (before.stdout `focused: 0 red of 26`); documentation commits ran the check by hand, and XTASK.3's gate refusal (2026-10-23) is what the set would have caught. Resolved by `decision_focused-set-runs-api-docs.md` under the director's delegation of 2026-10-26 (`decision_four-rulings-delegated.md`).
- [x] **FIX** — xtask/src/main.rs: `FOCUSED` gains `&["bash", "scripts/check_rustdoc.sh"]` between `check_requirements.sh` and `make book` (`sed -n '/^const FOCUSED/,/^];/p' xtask/src/main.rs | grep -c check_rustdoc` = 1), the test `assert_eq!(FOCUSED.len(), 27)` (cargo-test.log `test result: ok. 6 passed; 0 failed`); docs/toolbox/execution.md row (`grep -c '27-check' docs/toolbox/execution.md` = 1); criterion 6 (disposable target for altered builds) in this tree.
- [x] **ADDRESSED (verified)** — measure-1.out (the code change, the index row still at 4/6): `focused: 1 red of 27`, `verdict lines: 25 identical, 1 differ` — the one `FRONTIER-SYNC`, `COUNT DRIFT XTASK: the index claims 4/6 leaves complete; the tree has 5/7`, this leaf's own index row, fixed; the new entry `check_rustdoc.sh` → `API-DOCS: ok (5 crate(s) documented; no broken or private intra-doc link, no invalid HTML; 0 undocumented public item(s), each crate at its recorded count)`. RED red.out — `[\`Request\`]` → `[\`Reqest\`]` at crates/semulith-core/src/env.rs:132 with `CARGO_TARGET_DIR=target/xtask/xt0012/red-target`: `focused: 1 red of 27` rc 1 in 163 s, `check_rustdoc.sh rc=1`, `API-DOCS: FAIL — the workspace's rustdoc carries link or HTML defects`, `crates/semulith-core/src/env.rs:132:45  unresolved link to \`Reqest\``; restored `shasum -a 256 crates/semulith-core/src/env.rs` = 851b0a3c15e3ab8aabf4f553b3b6af566e4c2e1dcfe54770c92014bb2a4dd913; the disposable target (182M) removed, `ls target/debug/incremental | wc -l` = 84 before and after. measure-2.out (the finished slice, nothing staged): `focused: 0 red of 27` rc 0, `verdict lines: 25 identical, 1 differ` — `SEAM-INTEGRITY: ok (1543 current tracked acceptance box(es) …)` → `(1548 …)`, the five boxes of this checklist; the one new entry `check_rustdoc.sh`.
- [x] **NO REGRESSION** — make-check.log `make check rc=0 in 49 s`, 490 passed, 0 failed; after-1: every verdict line but the index row's identical to before/, `FRONTIER-SYNC: ok (35 tree(s) mirrored by docs/TASK_TREE.md)`, `TREE-CLAIMS: ok`, `DERIVED-COUNTS: ok` once the row read 5/7; the chain's focused run on the staged tree before the commit.
- [x] **LOCKSTEP** — docs/toolbox/execution.md row (27-check); the tree (XTASK.7 node, Children `XTASK.1` … `XTASK.7`, criterion 6, the open question resolved, the changelog line), docs/TASK_TREE.md (5 of 7), CHANGELOG, MEMORY; the knowledge card's focused-set count.

## Acceptance Checklist (leaf XTASK.8, slices a–c)

- [x] **ROOT CAUSE (WHY + WHERE)** — the gate ran its checks one after another: `grep -c '^  "' scripts/check_doctrines.project.sh` = 41 registered project checks behind a `for entry in "${PROJECT_DOCTRINES[@]}"` loop at ddcee89f, and PROFILE-CONSISTENCY's self-test made its probe invocations one after another — `wc -l < target/xtask/xt0017/rest/argv` = 1114, their serial sum 2730 s of a 2746 s self-test (pc-serial-times.tsv). The pooled run's one refusal: `killpg` returns EPERM for an exited, unreaped leader (measured: zombie leader → EPERM, reaped → ESRCH, zombie leader with a live descendant → OK and the descendant dies) and `_stop` in scripts/artifact_cargo.py tolerated `ProcessLookupError` alone. The chain's gate refusal: `cargo xtask check-push-record` → `could not execute process … (never executed)` — cargo copies the uplifted binary to a fresh inode on every run (`/usr/bin/stat -f %i target/debug/xtask` differs across two back-to-back runs) and releases its lock before the exec; six workers × six `cargo xtask check-registry-mirror` → 4 of 36 failed.
- [x] **FIX** — scripts/check_doctrines.project.sh: an `xargs -P` pool, reported in registry order (`DOCTRINE_JOBS`, `DOCTRINE_TIMES`); scripts/check_profile_consistency.sh `self_test`: a recording pass, `scripts/doctrine_prefetch.py` in parallel, an answering `python3` shadow (`PROFILE_CONSISTENCY_PREFETCH=0` the control); scripts/artifact_cargo.py `_stop` tolerates `PermissionError`, a 24th Cargo test with the seam `stop-zombie`; scripts/check_doctrines.project.sh: the checks whose script names cargo (`grep -q cargo`) run in one serial lane beside the pool.
- [x] **ADDRESSED (verified)** — red_pool.sh: `cmp` of stderr and rc identical for a pool of 1, a pool of 12 and the serial loop at HEAD on a stub registry (red, green, slow, missing); measure_pc.sh: `SELFTEST-STDOUT-IDENTICAL`, `SELFTEST-STDERR-IDENTICAL (0 B)`, `shadow misses: 0`, 2746 s → 447 s; control_shadow.sh 12 GREEN / 0 RED; gate-lane.log: `=== all doctrines green ===` in 406 s where the lived gates took 52–56 min; red_pool.sh `LANE-SERIAL` at jobs 1 and 12 (the two cargo stubs never overlap).
- [x] **NO REGRESSION** — `PROFILE-CONSISTENCY --self-test: 1164 pass / 0 fail` with and without the prefetch; `ARTIFACT-COHORT --self-test: 150 pass / 0 fail` (was 148) and `python3 -B scripts/probe_artifact_cargo.py --mutation stop-zombie` → `artifact Cargo: 1 tests / 1 failures / 0 errors`; every project check rc 0 in the pooled run (`awk -F'\t' '$2!=0' target/xtask/xt0017/gate/times.pool.tsv | wc -l` = 0); no scratch left behind (`ls target/doctrine-selftest | wc -l` = 0).
- [x] **LOCKSTEP** — the tree (XTASK.8 node, Children, frontier rows, changelog line), docs/TASK_TREE.md, CHANGELOG.md entry, MEMORY.md next_action, the knowledge card and its INDEX row.

## Changelog

- `2026-10-23`: Created task tree from the director's direction and the measured assessment
  (target/rustdoc-xtask-assessment/).
- `2026-10-23`: XTASK.1 done — `cargo xtask` delegates to the Makefile, measured equal; XTASK.2 next.
- `2026-10-23`: XTASK.2 done — `cargo xtask focused` is the tracked focused set, measured equal to the scratch runner; XTASK.3 next.
- `2026-10-23`: XTASK.3 done — one definition per target, guarded by a test that reads the Makefile; XTASK.4 next.
- `2026-10-24`: XTASK.4 opened with its measured inventory (14 scripts, 3 hook-coupled); slice 4a done — `build_bench.sh` is `cargo xtask build-bench` behind a held shim, measured equal.
- `2026-10-24`: XTASK.5 blocked (pinned `gate_report.py` reads `check-examples` in the CLI); XTASK.6 slice 6a done — `PORT-WEB` is Rust behind a held shim, measured byte-identical; the arm total counts a shim's module (1672).
- `2026-10-24`: XTASK.6 slice 6b done — `COMMIT-PREFIX` is Rust behind a held shim, measured byte-identical with the real hook swapped and restored; the doctrine modules share `harness.rs`.
- `2026-10-24`: XTASK.6 slice 6c done — `DELIVERY-PROVENANCE` is Rust behind a held shim keeping the locality preamble, measured byte-identical on nine paths of the real package.
- `2026-10-24`: XTASK.6 slice 6d done — `API-DOCS` is Rust (`cargo xtask check-rustdoc`), its Python ratchet ported with it, measured byte-identical on twelve paths.
- `2026-10-24`: XTASK.6 slice 6e done — `PUSH-RECORD` is Rust behind a held shim, byte-identical on nine paths; the bash self-test's unguarded scratch acted on the real repository during a failure-injection run (stopped, restored, verified; owned, card written); slice 6f guards the two drivers with the same form.
- `2026-10-26`: XTASK.5 closed by decision — `check-examples` stays a product command; no code change, no capture spent.
- `2026-10-26`: XTASK.7 done — `cargo xtask focused` runs API-DOCS before `make book`, 27 checks; the leaf-wide criteria gain the disposable-target rule for altered builds.
- `2026-10-26`: XTASK.6 slice 6f done — all 32 bash self-tests check their scratch allocation and stop before any command (both allocation forms, one census); ok and `--self-test` byte-identical, the guarded failure path leaves `.git/config`, HEAD and the index unchanged; slice 6g is `FIXTURE-FINGERPRINT`.
- `2026-10-26`: XTASK.6 slice 6g done — `FIXTURE-FINGERPRINT` is Rust behind a held shim (a JSON reader with Python's messages, the hasher shared through the harness), byte-identical on eight paths and a fifteen-finding scratch tree; CHANGELOG.md sharded; slice 6h is `FACT-OWNERSHIP`.
- `2026-10-26`: XTASK.6 slice 6h done — `FACT-OWNERSHIP` is Rust behind a held shim (a `glob` reader with Python's rules, the string helpers shared through the harness), byte-identical on eleven paths; the arm total re-derived 1675 → 1677 (the bash idiom had missed two `armp` arms); slice 6i is `REGISTRY-MIRROR`.
- `2026-10-26`: XTASK.6 slice 6i done — `REGISTRY-MIRROR` is Rust behind a held shim (three regular expressions by hand, the family union written as before), byte-identical on twelve paths; the six uncoupled drivers left all need a Rust S-expression reader first — slice 6j is that design.
- `2026-10-26`: XTASK.8 opened on the director's instruction and its slices a–c done — the pooled project slot and PROFILE-CONSISTENCY's parallel prefetch take the commit gate from 52–56 min to 6.8 min, every verdict line unchanged.
- `2026-10-27`: XTASK.8 slice d done — the docs-only path (`decision_docs-only-gate-path.md`): six declared closures, a documentation commit's gate 27 s, `=== all doctrines green ===`, the six declared checks answered from the record (the recording run before it, every check running: 508 s); the leaf is done.
- `2026-10-27`: XTASK.6 slice 6j done — the Rust S-expression reader `xtask/src/sexp.rs` is in the harness, equal to the pinned `scripts/sexp.py` by a unit test over every tracked `.sexp` file and 389 of 390 command-line cases (the 41-digit-integer fixture is the documented limit); nothing ported, the pinned reader untouched; slice 6k ports the first consumer.
- `2026-10-27`: XTASK.6 slice 6k done — `EXERCISE-COVERAGE` is Rust behind a held shim (the inline Python and `resolve_composition` ported line for line onto the 6j reader), byte-identical on the real tree and on seven fixture states, 23 arms; taken out of turn because no feature leaf was unblocked (the `.14` declarations and ZICNTR wait on the pinned-tooling ruling, LAB-BENCH.2 on a user-feedback round, P5-BOARD.5 on the CPU's acceptance) — the alternation resumes with features the day a ruling lands; slice 6l ports `check_unit_composition.sh`.
- `2026-10-27`: XTASK.6 slice 6l done — the schema validator `xtask/src/schema.rs` is in the harness, equal to the pinned `scripts/check_sexp_schema.py` by its 51 arms (byte-identical output) and by a unit test over every (file, schema) pair the project validates (315); regex facets are an enumerated anchored subset refusing unknown shapes by name; nothing ported, the pinned validator untouched; taken out of turn — no feature leaf is unblocked until the pinned-tooling ruling lands; slice 6m ports the disjointness judge.
- `2026-10-27`: XTASK.6 slice 6m done — the encoding-disjointness judge is Rust (`xtask/src/disjoint.rs`, with the one composition resolver moved to `composition.rs` and shared with the exercise-coverage census): 17 arms byte-identical to the pinned judge's self-test, 23 tracked documents identical in stdout, stderr and exit status; nothing ported, no shim, the pinned judge untouched; taken out of turn — no feature leaf is unblocked until the pinned-tooling ruling lands; slice 6n ports `check_unit_composition.sh` behind a held shim.
- `2026-10-27`: XTASK.6 slice 6n done — `UNIT-COMPOSITION` is Rust behind a held shim over the Rust judge, validator and resolver, byte-identical on the real tree and nine fixture states, nine arms; the three-unit port that began with the schema validator closes; four uncoupled drivers remain, all reading through `records_sexp.py` — slice 6o measures that reader's port the way 6j measured `sexp.py`; taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6o done — the record mapping is Rust (`xtask/src/records.rs`), equal to the pinned `records_sexp.py` on all 16 tracked catalogues and held there by two unit tests; nothing ported, nothing shimmed (`decision_rust-records-mapping.md`); of the four uncoupled drivers two read records as dictionaries (6n's "three" corrected); slice 6p ports `check_scope_coverage.sh`; taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6p done — `SCOPE-COVERAGE` is Rust behind a held shim over the Rust record mapping, byte-identical on the real tree and 11 fixture repositories, ten arms; the first driver ported over the mapping; three uncoupled drivers remain (`check_extraction.sh` next, slice 6q); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6q done — `EXTRACTION`'s driver is Rust behind a held shim (the pinned Python judge spawned as before, not ported; the fixtures written through the Rust record mapping), byte-identical on the real tree and 8 fixture repositories, eleven arms; the closed slices' acceptance rows 6a–6o moved verbatim to `docs/tasks/archive/XTASK-1.md` (this leaf 125,454 → 81406 B); two uncoupled drivers remain (`check_citation_quotes.sh` next, slice 6r); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6r done — `CITATION-QUOTES`'s driver is Rust behind a held shim (the pinned Python tool and its two inline controls spawned verbatim), byte-identical on the real tree and 5 fixture repositories, twenty-two arms; CHANGELOG.md sharded (`docs/changelog/shard-0417.md`); one uncoupled driver remains (`check_m_vectors.sh`, slice 6s); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6s done — `M-VECTORS`'s driver is Rust behind a held shim (the inline Python judge run verbatim), byte-identical on the real tree and 5 fixture repositories, six arms; the uncoupled drivers are all ported (6k–6s); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6t done — `BOOK-INDEX`'s driver is Rust behind a held shim (the generator spawned as before), byte-identical on the real tree and 5 fixture repositories, ten arms; next `check_board_verdict.sh` (slice 6u); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6u done — `BOARD-VERDICT`'s driver is Rust behind a held shim (the judge spawned as before), byte-identical on the real tree and 5 fixture repositories, six arms; §9: the controls copy the live board, so a rejected live board refuses the check instead of failing by name (an open question); next `check_board_gen.sh` (slice 6v); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6r-b done — the knowledge family's second re-derivation (`decision_knowledge-family-second-rederivation.md`: ceiling 56 files / 180,224 B, health 48 / 157,696) and the deferred 6r card landed; §15: the health line had fired four slices earlier and was read as noise — the slice runners now print it.
- `2026-10-27`: XTASK.6 slice 6v done — `BOARD-GEN`'s driver is Rust behind a held shim (the generator spawned as before), byte-identical on the real tree and 5 fixture repositories, nine arms; next `check_platform_gen.sh` (slice 6w); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6w done — `PLATFORM-GEN`'s driver is Rust behind a held shim (the generator spawned as before), byte-identical on the real tree and 5 fixture repositories, eleven arms; next `check_state_gen.sh` (slice 6x); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6x done — `STATE-GEN`'s driver is Rust behind a held shim (the generator spawned as before; the script's rv64gc template embedded verbatim), byte-identical on the real tree and 5 fixture repositories, twenty-nine arms; CHANGELOG.md sharded (`docs/changelog/shard-0418.md`); next `check_interaction_matrix.sh` (slice 6y); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6y done — `INTERACTION-MATRIX`'s driver is Rust behind a held shim (the judge spawned as before), byte-identical on the real tree and 4 fixture repositories, fifteen arms; XTASK.md's closed rows 6p–6x archived (part 2); next `check_unit_books.sh` (slice 6z); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6z done — `UNIT-BOOKS`'s driver is Rust behind a held shim (the judge spawned as before over a fresh mdbook bundle), byte-identical on the real tree and 4 fixture repositories, eighteen arms; next `check_tree_claims.sh` (slice 6aa); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6aa done — `TREE-CLAIMS`'s driver is Rust behind a held shim (the inline Python judge run verbatim), byte-identical on the real tree and 4 fixture repositories, thirty-eight arms; next `check_frontier_sync.sh` (slice 6ab); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6ab done — `FRONTIER-SYNC`'s driver is Rust behind a held shim (the inline Python judge run verbatim), byte-identical on the real tree and 4 fixture repositories, forty-one arms; XTASK.md's closed-slice paragraphs 6a–6aa archived (part 3); next `check_task_history.sh` (slice 6ac); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6ac done — `TASK-HISTORY`'s driver is Rust behind a held shim (the five Python judges run as before), byte-identical on the real tree and 3 fixture repositories, fifty-two arms; next `check_changelog_shards.sh` (slice 6ad); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6ad done — `SHARD-FREEZE`'s driver is Rust behind a held shim (the partition and predecessor judges run as before), byte-identical on the real tree and 3 fixture repositories, forty-four arms; next `check_derived_counts.sh` (slice 6ae); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6ae done — `DERIVED-COUNTS` is Rust behind a held shim (a native port: the claims, the enumerators through `bash -c`, the arm total by the script's rules), byte-identical on the real tree and 3 fixture repositories, twelve arms; next `check_artifact_cleanup.sh` (slice 6af); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6af done — `ARTIFACT-COHORT`'s driver is Rust behind a held shim (the probe suites run as before), byte-identical on the real tree and 2 fixture repositories, sixteen scorings; `check_readme_routes.sh` deferred with its reason (PATH-shadowing controls, ~600 lines); next `check_source_format.sh` over `sexp.rs` (slice 6ag); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6ag done — `SOURCE-FORMAT` is Rust behind a held shim over the harness's reader (the first `sexp`-only caller ported; the refusal probe run as before), byte-identical on the real tree and 3 fixture repositories, seven arms and eighteen scorings; next `check_semantics_corpus.sh` (slice 6ah); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6ah done — `SEMANTICS`'s driver is Rust behind a held shim (the encoding documents over the harness's reader, the judges spawned as before), byte-identical on the real tree and 3 fixture repositories, eight arms; next `check_upstream_index.sh` (slice 6ai); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6ai done — `UPSTREAM-INDEX`'s driver is Rust behind a held shim (the inline Python judge run verbatim), byte-identical on the real tree and 4 fixture repositories, twenty-one arms; the `sexp` callers are all ported — 29 of 42 drivers answer through shims, one deferred, eleven call other pinned modules; next `check_contract_freeze.sh` (slice 6aj); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6aj done — `CONTRACT-FREEZE`'s driver is Rust behind a held shim (the inline Python judge run verbatim), byte-identical on the real tree and 3 fixture repositories, nine arms; the first of the eleven pinned-module callers; next `check_fp_vectors.sh` (slice 6ak); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6ak done — `FP-VECTORS`'s driver is Rust behind a held shim (the generator spawned and the hardware cross-check run verbatim), byte-identical on the real tree and 3 fixture repositories, seven arms; next `check_gate_report.sh` (slice 6al); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6al done — `GATE-REPORT`'s driver is Rust behind a held shim (the generator and its probe spawned as before), byte-identical on the real tree and 3 fixture repositories, two arms; next `check_materials_bill.sh` (slice 6am); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6am done — `MATERIALS-BILL`'s driver is Rust behind a held shim (the inline Python judge run verbatim, the generator spawned as before), byte-identical on the real tree and 3 fixture repositories, eleven arms; CHANGELOG.md sharded (`docs/changelog/shard-0419.md`); next `check_definition_gen.sh` (slice 6an); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6an done — `DEF-GEN`'s driver is Rust behind a held shim (the generator, the probes and the controls' inline programs spawned as before), byte-identical on the real tree and 3 fixture repositories, forty-two arms; next `check_dossier_schema.sh` (slice 6ao); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-27`: XTASK.6 slice 6ao done — `DOSSIER-SCHEMA`'s driver is Rust behind a held shim (the inline sweep run verbatim, the probes spawned as before), byte-identical on the real tree and 3 fixture repositories, forty-seven arms; next `check_requirements.sh` (slice 6ap); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-28`: XTASK.6 slice 6ap done — `RECORD-SCHEMA`'s driver is Rust behind a held shim (the inline judge run verbatim, the writers, probes and the Rust graph checker spawned as before), byte-identical on the real tree and 3 fixture repositories, seventy-nine arms; next `check_guest_gen.sh` (slice 6aq); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-28`: XTASK.6 slice 6aq done — `GUEST-GEN`'s driver is Rust behind a held shim (generator, governor, probes and inline edits spawned as before; the module generated from the script), byte-identical on the real tree and 3 fixture repositories, 332 arms; XTASK.md's closed rows 6y–6ap archived (part 4, named by 6aq-b); next `check_profile_consistency.sh` (slice 6ar, the last pinned-module caller); taken out of turn while every feature leaf waits on the pinned-tooling ruling.
