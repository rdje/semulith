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
  Children: `XTASK.1` … `XTASK.7`, `XTASK.8`, `XTASK.9`, `XTASK.10`, `XTASK.11`

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
  Slice `4b` — the closing review (`2026-10-28`, `SEMULITH-XTASK-0062`; on clean a8d4d526, taken while every feature leaf waits on
  a ruling; evidence target/xtask/xt0062, census.sh → census.txt), documentation only. Every remaining script re-measured against
  what limits its port. Four are hook-family: `pre_push.sh` (called by `.githooks/pre-push`), `approved_push.sh` and
  `check_push_cadence.sh` (called from it), and `knowledge-map/scripts/gen_knowledge_map.sh` (called by `.githooks/pre-commit`;
  ordinary tracked bash) — the hooks change only after a reviewed period (Non-Goals). Three fetch over the network
  (`fetch_act4.sh`, `fetch_sources.sh`, `fetch_references.sh`: 2, 2 and 5 network lines), so their download paths cannot be
  measured equal offline, and the pinned `gate_report.py` prints `fetch_references.sh --verify-only` and names
  `build_c_guest.sh` in its report. `install_ci_mdbook.sh` is run by `doctrines.yml` and read as text by
  `capture_book_dependencies.py`; `update_scaffold.sh` is the bedrock template's own updater; `build_c_guest.sh` is one
  `exec python3` (18 lines: a port adds a forwarder and removes no shell); `check_no_background_jobs.sh` is the handoff rule's
  census, which the cleanup's delete act also runs as its fresh census, and its process-ancestry exclusion would change under
  cargo; `bootstrap.sh` is a fresh clone's first command and runs cargo only `if command -v cargo` — a shim would make the
  bootstrap need the toolchain it may come before (`decision_universal-registry-checks-stay-bash.md`'s first reason);
  `check_portability.sh`'s cold controls put stub `git`, `cargo`, `rustup`, `uname`, `arch` and `xcrun` first on PATH, so a
  shim's `exec cargo xtask` would be answered by the stub and the controls could not reach the instrument, and its equality
  needs the nightly Miri legs (about 100 min) and the Rosetta leg. Proposed: all 13 stay shell, the leaf closing with one
  script of fourteen ported (`build_bench.sh`, 4a) and the tree with it (9 of 9) — a change to the lane the director set, so
  the close waits on the director's word (Open Questions). Correction (§15, own defect): slice 6av recorded
  `knowledge-map/scripts/check_knowledge_map.sh` as "a submodule, read-only"; `git ls-files -s knowledge-map` lists ordinary
  tracked files (mode 100755) and `.gitmodules` names `vendor/linkedspec` alone. It is the universal registry's conditional
  `KNOWLEDGE-MAP` check, held local against a scaffold sync since `LIVE-CONTAINMENT.4` and run as text in crate-less fixtures
  by the orientation qualifier, so it stays bash by that decision's own reasons; the record gains the correction and the 6av
  paragraph is marked. Containment: XTASK.6's closed rows 6aq–6av (13,683 B) moved verbatim to `archive/XTASK-5.md` and its
  slice paragraphs 6ab–6av (43,129 B) to `archive/XTASK-6.md` (the a43b mechanism; the live file 125,750 B before
  this slice's text, ceiling 131,072 B); CHANGELOG.md sharded (14 oldest entries to `docs/changelog/shard-0420.md`, the head 64,688 → 48,558 B).

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
  Status: `done` (`2026-10-28`, `SEMULITH-XTASK-0060`; slices 6a–6av: the project registry's 41 drivers in Rust behind held shims;
  the four universal-registry checks the project owns stay bash — `decision_universal-registry-checks-stay-bash.md`)
  Goal: unpinned doctrine drivers ported one at a time, output lines kept identical, arms re-fired RED.
  Inventory (measured 2026-10-24 on 557d2f56; target/xtask/xt0004/drivers.md): 54 drivers registered by
  `check_doctrines.sh` and its project slot — 7 spine (in `update_scaffold.sh`'s `NEUTRAL` list, so a scaffold
  sync would overwrite a port), 8 calling a pinned script directly (`gate_report.py`, `specfp.py`, `sexp.py`,
  `record_catalog.py`, `check_sexp_schema.py`, `records_sexp.py`, `dossier_sexp.py`,
  `retain_div_statement.py`), 39 free (transitive Python imports traced per slice, not yet in bulk). One
  driver per slice and per commit, as in `XTASK.4`. A ported driver's arms move into its xtask module, so the
  `DERIVED-COUNTS` arm total must count them there, or the claimed total would drop with no arm removed.
  Slices 6a–6aa (with 6r-b): [retained verbatim](archive/XTASK-3.md#slice-paragraphs-6a-to-6aa).
  Slices 6ab–6av: [retained verbatim](archive/XTASK-6.md#slice-paragraphs-6ab-to-6av).
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

- ID: `XTASK.9` — **the units' own scratch removed**
  Status: `done` (`2026-10-28`, `SEMULITH-XTASK-0061`; opened by `ARTIFACT-CLEANUP.30`'s census, AC0086; on clean d860ac3f;
  evidence target/xtask/xt0061)
  Goal: every disposable build directory and scratch clone repository the XTASK units left under `target/xtask/` removed —
  rule 1 of `decision_orphan-incremental-sessions.md`, this tree's Acceptance Criterion 6 — every output, log and summary
  kept, and the removal made mechanical.
  Result: the cleanup's census attributed 450 of its 784 unrecorded files (2,295,034,299 B) to 40 draft-crate target
  directories (`target/xtask/xt0013` … `xt0059`, each a cargo target with `CACHEDIR.TAG`); a wider census found 228 scratch
  clone repositories in the `red-<epoch>` fixture directories beside them. Why they stayed: a draft target was rebuilt across
  a slice's iterations and nothing removed it at the unit's close, and `red_clone.sh` wrote each fixture's compared outputs
  (`*.bash.out`, `*.rs.out`, `tally`, the `summary.txt` the acceptance rows cite through the `red` link) into the directory
  that held its clones — a whole-directory removal would have destroyed cited evidence, and nothing removed the clones inside.
  `remove_scratch.py` validated every path by shape and content (a target: `CACHEDIR.TAG` and only cargo's entries; a clone:
  `.git`) and removed exactly 268 directories (11,125,043,200 B by `du -sk`): `target/xtask` 11,258,164 KB → 393,888 KB, the
  1,408 output files beside the clones all present after; of the AC0086 unrecorded population 450 gone and 334 left
  (1,399,591,247 B, the shared target's own orphan sessions, the `.29` ruling's), none under `target/xtask/`. Mechanical from
  now on, in the local helpers (untracked): `target/xtask/sweep_unit_scratch.sh <evidence-dir>` removes only a directory of
  the evidence dir carrying `CACHEDIR.TAG` and a directory inside a `red-*` carrying `.git`, refuses a path outside
  `target/`, and runs after every successful commit of the chain; `red_clone.sh` removes a clone once its outputs compare
  equal (a DIFFER keeps it for inspection). The sweep's control on a scratch layout removed exactly the target and the clone
  and kept the outputs, a plain directory and a link. Outside this leaf, listed for the director beside the `.29` ruling:
  18 nested cargo target roots of other trees' units (`target/p4-system-7`, `-11`, `-12`, `-13`, `target/refs`,
  `target/linkedspec`, `target/miri`, `target/miri.stale-*`), 24,135,434,240 B, all but `target/miri` older than the rule
  [corrected by `ARTIFACT-CLEANUP.33`: three of them are live — two cargo producer roots, 22.6 GB, and the dsp56300 build;
  the 15 stale ones, 968 MB, were removed].
  Card: `docs/knowledge/scratch-kept-beside-its-outputs-is-never-removed.md`.

- ID: `XTASK.10` — **the focused set runs rustfmt and clippy**
  Status: `done` (`2026-10-28`, `SEMULITH-XTASK-0063`; routed from `P4-SYSTEM.15` slice e-b with its evidence; on clean b917d1ba;
  evidence target/xtask/xt0063)
  Goal: a crate's formatting or lint drift is caught at the commit that makes it, not at the push boundary hundreds of commits
  later — the granted push of 2026-10-28 was refused by `make ci`'s `check` leg over two files formatted wrong since 2026-10-27.
  Result: `FOCUSED` (`xtask/src/main.rs`) begins with the first two steps of `make check`, `cargo fmt --all -- --check` and
  `cargo clippy --all-targets --all-features -- -D warnings`; a cargo step's log is named by its subcommand (`cargo-fmt.log`,
  `cargo-clippy.log`), and the tests hold the set at 29 and the two names. Measured on the clean HEAD and on the change:
  `focused: 0 red of 27` (192 s) → `0 red of 29` (198 s), the 27 earlier verdict lines identical; RED — one appended line both
  misformatted and a clippy error (`clone` on a `Copy` value) makes the run `2 red of 29`, exactly the two new checks
  (`cargo fmt` rc=1, `cargo clippy` rc=101), built in the disposable target/tmp/xt0063-red and removed, the file restored
  byte-identical. The change's own first draft was misformatted and the new check's command caught it before the commit.

- ID: `XTASK.11` — **the doctrine controls refuse and freeze (ruling 5)**
  Status: `done` (`2026-10-28`, slices a–e, `SEMULITH-XTASK-0064` … `0068`; the director's ruling 5, `decision_doctrine-controls-refuse-and-freeze.md`)
  Goal: the three doctrine-owner questions answered as ruled — `CITATION-QUOTES`' availability probe refuses on any
  unexpected exception (6r); `BOARD-VERDICT`'s and `STATE-GEN`'s controls judge frozen fixture copies, so a wrong live board or
  a hand-edited live rv64gc pair fails by name (6u, 6x). One doctrine per slice, each change fired RED. Widened by slice c:
  the ruling's rule is general (a self-test judges frozen copies, never live data), and a deleted source must fail by name, not
  read as "nothing declared yet" — so slice d censuses every doctrine whose controls read live data (BOARD-GEN measured so,
  GUEST-GEN noted at 6aq) and one slice follows per doctrine found.
  Slice a (`2026-10-28`, `SEMULITH-XTASK-0064`; on clean aafcbdfd; evidence target/xtask/xt0064): `CITATION-QUOTES`'
  availability probe (`xtask/src/check_citation_quotes.rs` `AVAILABILITY`) now exits 2 with the exception's type and message
  on any exception outside its named refusals, and exits 0 or 1 only after the call returns — a truncated manifest's
  `DossierError` (the 6r finding) refuses instead of reading as "the pinned pages are absent". Two arms hold it: the probe's
  own text with its call patched to raise a foreign `ValueError` must exit 2 naming it, and patched to return `False` must exit
  1 (the named skip). Measured: `CITATION-QUOTES --self-test: 24 pass / 0 fail` (22 + the two); the real tree's verdict
  unchanged (`115 attributed quote(s) judged … 0 finding(s)`); RED — the same crash program over the slice's predecessor text
  exits 1 (the crash read as absent), so the arm discriminates. Next: slice b — `BOARD-VERDICT`'s frozen fixture board.
  Slice b (`2026-10-28`, `SEMULITH-XTASK-0065`; on clean 37debc11; evidence target/xtask/xt0065): `BOARD-VERDICT`'s controls
  judge frozen copies — `scripts/fixtures/board-verdict/` holds the four documents the controls copied from the live board
  (`board.sexp`, `requirements.sexp`, `contract-obligations.sexp`, `sources.sexp`, taken from `profiles/netboard-lab-v0` today),
  and `xtask/src/check_board_verdict.rs` copies them instead of the live ones; the verdict reads only a board's own documents and
  the board schema, so the controls no longer depend on the corpus they judge. Measured with the binary before and after on the
  6u corpus states, each applied to the tree and restored byte-identical (red.sh): a rejected live board `rc=2 REFUSED — the check
  does not discriminate` → `rc=1 FAIL — the composition does not hold`; no board `rc=2 REFUSED` → `rc=0 ok (no board declares itself
  yet)` [corrected in slice c: that is a silent pass on a deletion, not the ruled outcome — the gate still refuses the state
  through BOARD-GEN, whose controls read the live board too; a board unit holding gen_board's artifacts without `board.sexp`
  must fail by name — slice d's census owns it]; one good board and one of two rejected unchanged (0 and 1). `BOARD-VERDICT --self-test: 6 pass / 0 fail`, the real verdict
  unchanged. Next: slice c — `STATE-GEN`'s frozen rv64gc pair.
  Slice c (`2026-10-28`, `SEMULITH-XTASK-0066`; on clean 45f970c0, after the approved push; evidence target/xtask/xt0066):
  `STATE-GEN`'s controls judge frozen copies — `scripts/fixtures/state-gen/` holds the rv64i descriptor, the arithmetic module and
  an rv64gc pair (`rv64i/state.sexp`, `arith.rs`, `rv64gc/state.sexp` and `rv64gc/state_rv64gc.rs`, the module generated from the
  frozen descriptor at its own path, since a module records its source path and digest; its body equals the live module's). The
  first draft copied the live module and named the descriptor `rv64gc-state.sexp`: the generator refuses a descriptor not named
  `state.sexp` and the copied header named the live path — 2 of 29 arms refused, caught before any commit. The real run now judges
  each pair on its own: a generated module whose descriptor is absent fails by name (before, an absent rv64i descriptor returned
  "ok (no state descriptor yet)" without judging rv64gc at all); only when no pair has either half is there no state yet.
  Measured with the binary before and after on the 6x corpus states, each applied to the tree and restored byte-identical
  (red.sh): the rv64gc module hand-edited 2 REFUSED → 1 FAIL by name; the rv64gc census silenced 2 → 1; the rv64i descriptor
  removed 2 → 1 (`… is generated, but its descriptor … is absent`); the rv64i module hand-edited and the in-sync tree unchanged
  (1, 0). `STATE-GEN --self-test: 29 pass / 0 fail`; the real verdict unchanged. Next: slice d — the census of every doctrine
  whose controls read live data.
  Slice d (`2026-10-28`, `SEMULITH-XTASK-0067`; on clean 8c622c02; evidence target/xtask/xt0067): the missing-board case
  the 6u finding named, finished — `BOARD-VERDICT`'s real run fails by name a `profiles/*` unit holding `composition.sexp` (the
  board generator's manifest, derived from `board.sexp`) without its `board.sexp`; a corpus with no board unit at all is still
  "no board declares itself yet". Measured before and after (red.sh, each state applied to the tree and restored): `board.sexp`
  deleted `rc=0 ok (no board declares itself yet)` → `rc=1 FAIL — profiles/netboard-lab-v0/composition.sexp is generated from a
  board definition, but … board.sexp is absent`; no board unit at all 0 → 0; rejected, one of two rejected and one good board
  unchanged. `BOARD-VERDICT --self-test: 6 pass / 0 fail`. The census (census.py → census.txt): 21 of 41 drivers' self-tests
  reference live tracked data directly and `PROFILE-CONSISTENCY`'s runs 44 probes — some are false positives (route rows that
  merely contain `docs/`), many are deliberate real-tree arms (`a-real-tree-probe-arm-is-a-prediction-the-act-re-states.md`),
  and `BOARD-GEN` is a measured case (it refuses when the live `board.sexp` is absent). Next: slice e — classify the census
  (which GREEN controls require a correct live corpus) and raise the remedies to the director: beyond ruling 5's named three.
  Slice e (`2026-10-28`, `SEMULITH-XTASK-0068`; on clean 59f14afa; evidence target/xtask/xt0068/classification.md): the census
  classified by reading each driver's self-test (two claims re-checked by hand: BOOK-INDEX copies the live `docs/book`; DEF-GEN's
  GREEN in-sync arm runs `--check` on the live rv64gc encoding, state and module — the real check's own test). 11 drivers are
  FRAGILE — a GREEN arm expects a verdict on the unmodified live corpus: BOARD-GEN, BOOK-INDEX, CONTRACT-FREEZE (partly mitigated:
  it judges before its self-test), DEF-GEN, EXERCISE-COVERAGE, GUEST-GEN, MATERIALS-BILL, PLATFORM-GEN, RECORD-SCHEMA and
  UNIT-BOOKS through one probe each, and PROFILE-CONSISTENCY through 14 probes; 10 are false positives (scratch paths, TSV row
  literals); ARTIFACT-COHORT reads only its owned fixtures; DOSSIER-SCHEMA, outside the census, is likely fragile too. The most
  consequential by commits since 2026-09-28: BOOK-INDEX (`docs/book`, 364), PROFILE-CONSISTENCY (`profiles/rv64gc-lab-v0`, 139;
  it refused this way on 2026-10-26), DEF-GEN and GUEST-GEN (their live in-sync arms duplicate the real check). Ruling 5 named
  three doctrines and its record states the rule generally; extending it to the other eleven is a programme of its own (some
  PROFILE-CONSISTENCY real-tree arms are deliberate: `a-real-tree-probe-arm-is-a-prediction-the-act-re-states.md`), so it is
  raised to the director as an Open Question with a recommended order. The leaf is done: its ruled scope is executed.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `XTASK.4` | `active` | ruling 2 (2026-10-28): the leaf closes with its 13 scripts in shell, and the tree with it, once the live-data controls question (e) is answered |

## Decisions

- `2026-10-23`: the director: "Migration to xtask shall be done with extrem care, and incrementally for not
  breaking anything" (`decision_rust-native-tooling.md`).
- `2026-10-26`: the director: "Please alternate Rust tooling port and project feature implementation. Do not get
  stuck on Rust's tooling because the project work needs to progress" (`decision_alternate-port-and-features.md`):
  after a slice lands, the next unit is a project feature leaf; a slice drafted ahead waits its turn.
- `2026-10-28`: `XTASK.6` closes on the project registry; the four universal-registry checks the project owns —
  `MEMORY-ARCH`, `README-STABILITY`, `TASK-ACCEPTANCE`, `GAP-CLAIM-CENSUS` — stay bash (`decision_universal-registry-checks-stay-bash.md`, ruled under
  the delegation of 2026-10-26, authority `review`).

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
- (Answered 2026-10-28 by ruling 5; executed by `XTASK.11` slice a.) (6r, `2026-10-27`) `CITATION-QUOTES`'s availability probe exits 1 for "pages absent" and Python exits 1 for an uncaught exception, so a sources manifest the reader refuses outside the probe's `except` tuple reads as absence — NAMED SKIP, exit 0 (measured in the 6r fixture `manifest-unreadable`; the card: `docs/knowledge/a-crash-that-exits-one-reads-as-an-absence.md`, landed with the family's second re-derivation in 6r-b). The port reproduces it; the doctrine's owner decides whether the probe should refuse (exit 2) on any exception — a one-line change to the script, re-measured through the shim.
- (Answered 2026-10-28 by ruling 5; `XTASK.11` slice b.) (6u, `2026-10-27`) `BOARD-VERDICT`'s controls copy the LIVE board (`profiles/netboard-lab-v0`) and expect it ACCEPTED, so a corpus whose live board is rejected makes the check refuse as non-discriminating (exit 2) instead of failing by name (exit 1) — measured in the 6u fixtures `no-board` and `rejected`. The port reproduces it; the doctrine's owner decides whether the controls should run over a frozen fixture board instead.
- (Answered 2026-10-28 by ruling 5; `XTASK.11` slice c.) (6x, `2026-10-27`) `STATE-GEN`'s controls judge the LIVE rv64gc pair (`profiles/rv64gc-lab-v0/state.sexp` against `crates/semulith-core/src/state_rv64gc.rs`) and expect it in sync, so a corpus whose live rv64gc module or census is edited makes the check refuse as non-discriminating (exit 2) instead of failing by name (exit 1) — measured in the 6x fixtures `gc-module-hand-edited` and `gc-census-silent`; the rv64i pair fails by name. The port reproduces it; the doctrine's owner decides, beside 6u's question, whether the controls should run over frozen fixture copies.
- (Answered 2026-10-28 by ruling 2, `decision_xtask-closes-with-shell-remainder.md`: yes, after `XTASK.11`.) (4b, `2026-10-28`) Whether `XTASK.4` — and with it the tree — closes with its 13 remaining scripts in shell, each for the
  constraint slice 4b measured (hooks, network, pinned readers, the template, the controls' stub cargo). The lane is the
  director's (`decision_rust-native-tooling.md`); until the word, the leaf stays active and no port of them is started.
- (e, `2026-10-28`) Whether ruling 5's rule (a self-test judges frozen copies; a deleted source fails by name) extends to the 11
  doctrines `XTASK.11` slice e classified FRAGILE (target/xtask/xt0068/classification.md). Recommended: yes, one slice per
  doctrine in this order — DEF-GEN and GUEST-GEN (their live in-sync arm repeats the real check: drop it, keep a frozen pair),
  BOOK-INDEX (freeze a small book), then BOARD-GEN, PLATFORM-GEN, MATERIALS-BILL, EXERCISE-COVERAGE, CONTRACT-FREEZE, the
  RECORD-SCHEMA and UNIT-BOOKS probes, and PROFILE-CONSISTENCY's 14 probes last, case by case (some real-tree arms are deliberate
  predictions and stay, named). The director's.

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
- [x] slice 4b **REPRODUCE / ISSUE** — the leaf's frontier said "the remaining 13 scripts wait" with constraints measured on 557d2f56; re-measured at a8d4d526 (target/xtask/xt0062/census.sh rc=0 → census.txt): per script `wc -l`, the cargo and network lines (`grep -cE`), and its callers (`git grep -l`).
- [x] slice 4b **ROOT CAUSE (WHY + WHERE)** — each constraint located: `.githooks/pre-push` → pre_push.sh → approved_push.sh, check_push_cadence.sh; `.githooks/pre-commit` → gen_knowledge_map.sh; network lines 2/2/5 in the three fetchers; gate_report.py (pinned: `git grep -c 'scripts/gate_report.py' -- 'evidence/*/dependencies.sexp'` = 1 each in two manifests) prints fetch_references.sh and build_c_guest.sh; bootstrap.sh:83 `command -v cargo`; probe_portability.py stubs git, cargo, rustup, uname, arch, xcrun.
- [x] slice 4b **FIX** — documentation only: the 4b paragraph, the frontier row, an Open Question for the director, the 6av correction (`git ls-files -s knowledge-map` mode 100755; `git config -f .gitmodules --get-regexp path` → vendor/linkedspec alone) in the paragraph and the decision record; containment 13,683 + 43,129 B moved, CHANGELOG sharded (14 oldest entries to `docs/changelog/shard-0420.md`, the head 64,688 → 48,558 B).
- [x] slice 4b **ADDRESSED (verified)** — the movers' facts (target/xtask/xt0062/rows.json, paras.json: SHA256 of each moved block in the part's table, `grep -c` of each block in the part = 1 and in the live file = 0); `bash scripts/check_changelog_shards.sh` rc=0 after the shard.
- [x] slice 4b **NO REGRESSION** — the prechecks on the staged tree (target/xtask/xt0062/prechecks.txt): FRONTIER-SYNC, MEMORY-ARCH, SEAM-INTEGRITY, TASK-ACCEPTANCE, DERIVED-COUNTS, README-ROUTES, TABLE-ARITY, TASK-HISTORY, SHARD-FREEZE rc=0; the commit gate green (chain log).
- [x] slice 4b **LOCKSTEP** — the tree (4b paragraph, frontier, Open Questions, the marked 6av paragraph, changelog line), archive parts 5 and 6, the decision record's correction, docs/TASK_TREE.md, KNOWLEDGE_MAP.md, CHANGELOG.md and its shard, MEMORY.md.

## Acceptance Checklist (leaf XTASK.6)

Rows 6a–6o: [retained verbatim](archive/XTASK-1.md#acceptance-rows-6a-to-6o).
Rows 6p–6x (with 6r-b): [retained verbatim](archive/XTASK-2.md#acceptance-rows-6p-to-6x).
Rows 6y–6ap: [retained verbatim](archive/XTASK-4.md#acceptance-rows-6y-to-6ap).
Rows 6aq–6av: [retained verbatim](archive/XTASK-5.md#acceptance-rows-6aq-to-6av).

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

## Acceptance Checklist (leaf XTASK.9)

- [x] **ROOT CAUSE (WHY + WHERE)** — target/artifact-cleanup/AC0086-census.txt: `unrecorded 784 files 3,694,625,546 B`, `under target/xtask/*/draft-target: 450 files 2,295,034,299 B`; `find target/xtask -name draft-target` 40 directories, each with `CACHEDIR.TAG`; 228 clone roots (`.git`) under 51 `red-<epoch>` directories, `du -sk` 7.01 GB; `git grep -l -E 'red-17[0-9]{8}' | wc -l` = 0 (no tracked doc cites a path inside them); red_clone.sh writes `$R/$NAME.bash.out` into the clones' directory.
- [x] **FIX** — target/xtask/xt0061/remove_scratch.py (`--apply`): `removed 268; still present 0; kept outputs missing 0`, removed.tsv 268 rows (`wc -l`); the helpers: sweep_unit_scratch.sh (`bash -n` rc=0) called by commit-chain.sh after a successful commit, red_clone.sh removing a matched clone.
- [x] **ADDRESSED (verified)** — `du -sk target/xtask`: 11258164 → 393888; unrecorded-after.txt: `still present 334 files 1,399,591,247 B; gone 450`, `still present under target/xtask/: 0`; the sweep control: `sweep: 2 removed`, outputs, a plain directory and a link kept, a path outside target/ refused rc=2.
- [x] **NO REGRESSION** — `git ls-files -- target | wc -l` = 0 and `git status --short` empty after the removal (no tracked byte touched); the 1,408 kept output files present (`kept outputs missing 0`); the commit gate green (chain log).
- [x] **LOCKSTEP** — the tree (XTASK.9 node, Children, changelog line), docs/TASK_TREE.md (8 of 9 leaves done), the knowledge card and its INDEX row, KNOWLEDGE_MAP.md, CHANGELOG.md, MEMORY.md.

## Acceptance Checklist (leaf XTASK.11)

- [x] slice a **ROOT CAUSE (WHY + WHERE)** — `AVAILABILITY` caught four exception types and called `sys.exit` inside the `try`, so any other exception left the interpreter with status 1, the status the driver reads as absence (the 6r card; target/xtask/xt0064/red-old-text.txt: the predecessor text with a foreign `ValueError` → `rc=1`).
- [x] slice a **FIX** — xtask/src/check_citation_quotes.rs: `except Exception` → exit 2 with the type and message, the exit after the call; two arms (`tally.arm(` ×2) over the probe's own text with its call patched.
- [x] slice a **ADDRESSED (verified)** — `CITATION-QUOTES --self-test: 24 pass / 0 fail` (selftest.out); `bash scripts/check_citation_quotes.sh` rc=0 `115 attributed quote(s) judged (R1 1, R2 108, R3 3, R4 3); 0 finding(s)` (real.out).
- [x] slice a **NO REGRESSION** — `cargo clippy -p xtask --all-targets -- -D warnings` rc=0; `cargo fmt --all -- --check` rc=0; DERIVED-COUNTS re-derived (LIVE_STATUS 1,694 → 1,696 arms); the commit gate green (chain log).
- [x] slice b **ROOT CAUSE (WHY + WHERE)** — `self_test` copied `profiles/netboard-lab-v0`'s four documents (`grep -c 'repo.join(BOARD)'` = 1 in the predecessor), so a rejected live board failed the GREEN control and the check refused (red.txt: `rejected before rc=2 REFUSED`).
- [x] slice b **FIX** — scripts/fixtures/board-verdict/ (four frozen documents, `cmp` equal to the live ones at 37debc11); xtask/src/check_board_verdict.rs copies `FIXTURE`; the unused `BOARD` constant removed (clippy `-D warnings` rc=0).
- [x] slice b **ADDRESSED (verified)** — red.txt: `rejected after rc=1 FAIL — the composition does not hold`, `no-board after rc=0 ok (no board declares itself yet)`; `one-board` and `one-of-two-rejected` unchanged; `tree restored: 0 profile paths changed`.
- [x] slice b **NO REGRESSION** — `BOARD-VERDICT --self-test: 6 pass / 0 fail`; `bash scripts/check_board_verdict.sh` rc=0 `ok (1 board(s) …)`; `cargo fmt --all -- --check` rc=0; the commit gate green (chain log).
- [x] slice c **ROOT CAUSE (WHY + WHERE)** — `self_test` copied the live rv64i descriptor and `arith.rs` and judged the live rv64gc pair (`grep -c 'check(repo, STATE_GC, ARITH, OUT_GC)'` = 1 in the predecessor); `run` returned ok when the rv64i descriptor was absent; red.txt: three corpus states `before rc=2 REFUSED`.
- [x] slice c **FIX** — scripts/fixtures/state-gen/ (four frozen files; `python3 -B scripts/gen_state.py --check` over the frozen pair rc=0); xtask/src/check_state_gen.rs: the controls read `FIXTURE_*`, `run` judges each pair and fails an orphaned module by name; clippy `-D warnings` rc=0.
- [x] slice c **ADDRESSED (verified)** — red.txt: `gc-module-hand-edited after rc=1`, `gc-census-silent after rc=1`, `descriptor-missing after rc=1 … is generated, but its descriptor … is absent`; `module-hand-edited` and `in-sync` unchanged; `tree restored: 0 paths changed`.
- [x] slice c **NO REGRESSION** — `STATE-GEN --self-test: 29 pass / 0 fail`; `bash scripts/check_state_gen.sh` rc=0 (both pairs `ok … matches …`); `cargo fmt --all -- --check` rc=0; the commit gate green (chain log).
- [x] slice d **ROOT CAUSE (WHY + WHERE)** — `run` printed "no board declares itself yet" whenever `boards()` (units with `board.sexp`) was empty, so a deleted `board.sexp` beside its generated `composition.sexp` passed (red.txt: `no-board before rc=0`).
- [x] slice d **FIX** — xtask/src/check_board_verdict.rs: `orphaned_units` (`composition.sexp` without `board.sexp`) fails by name before the empty-corpus branch; clippy `-D warnings` rc=0.
- [x] slice d **ADDRESSED (verified)** — red.txt: `no-board after rc=1 FAIL — … composition.sexp is generated from a board definition, but … board.sexp is absent`; `no-board-unit-at-all after rc=0`; the other three states unchanged; `tree restored: 0 profile paths changed`.
- [x] slice d **NO REGRESSION** — `BOARD-VERDICT --self-test: 6 pass / 0 fail`; `bash scripts/check_board_verdict.sh` rc=0 `ok (1 board(s) …)`; `cargo fmt --all -- --check` rc=0; census.py rc=0 (`drivers 41`); the commit gate green (chain log).
- [x] slice e **ROOT CAUSE (WHY + WHERE)** — census.txt flagged 21 of 41 drivers by string (`grep -c '^- check_' target/xtask/xt0067/census.txt`); a mechanical match cannot tell a live read from a scratch path, so each self-test was read (classification.md, file:line per row).
- [x] slice e **ADDRESSED (verified)** — classification.md `wc -l` = 26: 11 FRAGILE, 10 FALSE-POSITIVE, 1 DEFINITION-INPUT; two rows re-checked by hand (`sed -n 134,138p xtask/src/check_book_index.rs`; `sed -n 930,940p xtask/src/check_definition_gen.rs`).
- [x] slice e **NO REGRESSION** — documentation only (`git diff --cached --name-only | grep -cvE '\.md$'` = 0); FRONTIER-SYNC and the prechecks green; the commit gate green (chain log).

## Acceptance Checklist (leaf XTASK.10)

- [x] **ROOT CAUSE (WHY + WHERE)** — `grep -ciE 'fmt|clippy'` over `FOCUSED` (27 entries) and scripts/check_doctrines.project.sh = 0: no commit-time check runs rustfmt or clippy over the workspace; the push boundary's `make ci` refused at `check` (target/push/last-green.log, P4-SYSTEM.15 slice e-b).
- [x] **FIX** — xtask/src/main.rs: two `FOCUSED` entries first, `log_name` names a cargo step `cargo-<subcommand>`, the tests (`FOCUSED.len()` 29, the two names); `cargo fmt -p xtask` applied to the draft.
- [x] **ADDRESSED (verified)** — target/xtask/xt0063: before.stdout `focused: 0 red of 27`, after.stdout `focused: 0 red of 29`, `earlier verdict lines identical: 27 of 27`; red.stdout `focused: 2 red of 29` (`cargo fmt` rc=1, `cargo clippy` rc=101); `cmp` restored rc=0; the disposable target removed.
- [x] **NO REGRESSION** — `cargo test -p xtask` → `test result: ok. 17 passed`; `cargo clippy -p xtask --all-targets -- -D warnings` rc=0; `cargo fmt --all -- --check` rc=0; the commit gate green (chain log).
- [x] **LOCKSTEP** — the tree (XTASK.10 node, Children, changelog line), docs/TASK_TREE.md (9 of 10 leaves done), the knowledge card that counts the set, CHANGELOG.md, MEMORY.md.

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
- `2026-10-28`: XTASK.6 slice 6ar done — `PROFILE-CONSISTENCY`'s driver is Rust behind a held shim (the inline judge run verbatim, tools and probes spawned as before, the XTASK.8 prefetch kept), byte-identical on the real tree and 2 fixture repositories, 51 arms + 494 scores; every pinned-module caller now answers through a shim; next `check_readme_routes.sh` (slice 6as) or the leaf's closing review; taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-28`: XTASK.6 slice 6as done — the leaf's driver count re-derived (39 of 41 through shims, not 38 of 42) and owned by `DERIVED-COUNTS` (two claim rows, RED on the old text, GREEN on the corrected); next `check_readme_routes.sh` (slice 6at), a design first; taken out of turn while every feature leaf waits on the pinned-tooling ruling.
- `2026-10-28`: XTASK.6 slice 6at done — `README-ROUTING-CLOSURE`'s driver is Rust behind a held shim (the three Python readers run verbatim, the tools spawned under each fixture's environment, the five redefined functions as seams), byte-identical on the real tree and 4 fixture repositories, ninety-four arms; 40 of 41 drivers through shims; next the leaf's closing review (slice 6au).
- `2026-10-28`: XTASK.6 slice 6au done — `SEAM-INTEGRITY`'s driver is Rust behind a held shim (the owner's rules asked of it, the box scoper and pattern tests spawned as before), byte-identical on the real tree and 4 fixture repositories, nineteen scores; the recorded hold on it was examined and found empty; 41 of 41 project drivers through shims; next the leaf's closing review (slice 6av).
- `2026-10-28`: XTASK.6 slice 6av done — the leaf's closing review: 41 of 41 project drivers behind held shims; the four universal-registry checks the project owns stay bash (`decision_universal-registry-checks-stay-bash.md`); XTASK.6 `done`, the frontier `XTASK.4`.
- `2026-10-28`: XTASK.9 done — the units' own scratch removed: 40 draft-crate targets and 228 scratch clones (11.1 GB) the units had left under `target/xtask/`, every output kept; a sweep after every landed commit makes it mechanical.
- `2026-10-28`: XTASK.4 slice 4b — the closing review: all 13 remaining scripts stay shell, each for a measured constraint (proposed; the close waits on the director); the 6av "submodule" claim corrected; XTASK.6's closed rows and paragraphs moved to archive parts 5 and 6.
- `2026-10-28`: XTASK.10 done — `cargo xtask focused` runs rustfmt and clippy first (29 checks); routed from P4-SYSTEM.15 slice e-b after the push boundary refused over formatting drift.
- `2026-10-28`: XTASK.11 slice a — CITATION-QUOTES' availability probe refuses an unexpected exception (ruling 5); 24 arms.
- `2026-10-28`: XTASK.11 slice b — BOARD-VERDICT's controls judge a frozen board; a rejected live board fails by name instead of refusing.
- `2026-10-28`: XTASK.11 slice c — STATE-GEN's controls judge a frozen pair; each pair judged on its own, an orphaned module fails by name; slice b's missing-board claim corrected.
- `2026-10-28`: XTASK.11 slice d — a deleted board fails by name; the live-data census measured (21 of 41 drivers; classification next).
- `2026-10-28`: XTASK.11 done — slice e classifies the live-data census (11 fragile doctrines); extending ruling 5 to them is raised to the director.
