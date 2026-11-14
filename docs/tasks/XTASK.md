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
  Children: `XTASK.1` … `XTASK.7`, `XTASK.8`, `XTASK.9`, `XTASK.10`, `XTASK.11`, `XTASK.12`, `XTASK.13`, `XTASK.14`, `XTASK.15`, `XTASK.16`, `XTASK.17`, `XTASK.18`

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
  Status: `done` (`2026-10-29`, `SEMULITH-XTASK-0072`: one script of fourteen ported, 13 stay shell by ruling 2, `decision_xtask-closes-with-shell-remainder.md`)
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
  Slices 11a–11e: [retained verbatim](archive/XTASK-7.md#slice-paragraphs-11a-to-11e).

- ID: `XTASK.12` — **a quiet refusal names the arm that missed**
  Status: `done` (`2026-10-29`, slices a–c; hosted CI green on cefb0d84: doctrines 40782096575 `=== all doctrines green ===`, rust 40782096560 success; opened by the hosted doctrines run 40746652030 on 45f970c0)
  Goal: when a doctrine's quiet self-test (the one its real run makes before judging) misses, the refusal names every missed arm
  and its output, so a hosted refusal can be diagnosed from its log.
  Slices 12a–12c: [retained verbatim](archive/XTASK-7.md#slice-paragraphs-12a-to-12c).

- ID: `XTASK.13` — **the eleven fragile doctrines judge frozen copies (ruling 5's rule)**
  Status: `active` (slice a done `2026-10-29`; opened `2026-10-29`; open question (e) answered by the workflow under the director's delegation of 2026-10-28:
  "I do not think you need my input to take your decision on what to do next … schedule what you need to schedule")
  Goal: each doctrine `XTASK.11` slice e classified FRAGILE (target/xtask/xt0068/classification.md) judges frozen copies in its
  self-test, and a deleted or damaged live source fails by name instead of refusing; one slice per doctrine, each fired RED with
  the binary before and after on the doctrine's own corpus states. Order: DEF-GEN and GUEST-GEN (their live in-sync arm repeats
  the real check — dropped, a frozen pair kept), BOOK-INDEX, BOARD-GEN, PLATFORM-GEN, MATERIALS-BILL, EXERCISE-COVERAGE,
  CONTRACT-FREEZE, the RECORD-SCHEMA and UNIT-BOOKS probes, then PROFILE-CONSISTENCY's 14 probes case by case (a real-tree arm
  that is a deliberate prediction stays, named); DOSSIER-SCHEMA's legacy arm is checked on the way. Scheduled between the
  feature units (5:1).
  Slices 13a–13b3: [retained verbatim](archive/XTASK-7.md#slice-paragraphs-13a-to-13b3).
  Slices 13b4–13c: [retained verbatim](archive/XTASK-8.md#slice-paragraphs-13b4-to-13c).
  Slice k (`2026-11-14`, `SEMULITH-XTASK-0092`; on clean 1fa19741; evidence target/xtask/xt0092): the first of PROFILE-CONSISTENCY's probes, `probe_experiment_graph.py`, judges a frozen subset. The 5:1 turn, after `P4-SYSTEM.20` a to c. **What measuring found.** Of the 14 probes the classification named (target/xtask/xt0068/classification.md), two hold deliberate real-tree predictions and stay, named: `probe_requirement_status.py` and `probe_dossier_qualification.py` (both re-predicted at `P4-SYSTEM.20` slice a). This one ran three scope arms over the live rv64gc dossier through `load_scope`, which also reads the contract's registry under `crates/`. **The change.** Those arms read `scripts/fixtures/profile-consistency/experiment-graph/`: `REQ-D-FP-DEFER` and `REQ-D-ABI`, its one dependency, the three FP obligations and their four-version supersession chain, copied from 1fa19741 (8,407 B). Same arms, same counts. **The chain's focused set caught the first draft:** RECORD-SCHEMA validates every `requirements.sexp` in the tree, and `REQ-D-FP-DEFER` alone named a dependency the file did not hold (`DANGLING DEP … 'REQ-D-ABI'`); the fixture carries the dependency closure, and RECORD-SCHEMA reads 42 record files.
  Slice l (`2026-11-14`, `SEMULITH-XTASK-0093`; on clean 96b97664; evidence target/xtask/xt0093): `probe_retained_sail_identity.py` judges a frozen copy. The 5:1 turn, after `P4-SYSTEM.20` d, e, f1, f2 and f3. **The change.** Its eleven tests read the dossier's `references.sexp`, the published descriptor `retained/sail-identity.sexp` and `schema/references.sexp` live, and the identity owner read its schema from its own root. They now read `scripts/fixtures/profile-consistency/retained-sail-identity/`, the three files frozen from 96b97664 in their own layout (30,058 B), with the owner's root patched to it for the class. Same tests, same counts, plain and `-O`. **Measured in clones:** a deleted `references.sexp`, a garbled descriptor or a deleted schema failed the probe before (11 errors, 14 failures, 11 errors); after, 11 tests / 0 failures in every state. **Who holds the live files now.** I first wrote that the credit derivation authenticates the descriptor through each case's planned pin, and measured before committing: with the descriptor garbled, all 46 credits still read current. What does hold it is the method review: it refuses with `capture input pin refuses: profiles/rv64gc-lab-v0/retained/sail-identity.sexp`, and PROFILE-CONSISTENCY's real judgement runs the policy review over every retained case and fails, all 42 lines `FINDING finite method not satisfied (refused)` (target/xtask/xt0093/real-check-policy.txt). **Found, owned as slice m, before the next probe:** that policy line drops the method's reason, so naming the file takes a second command; the doctrine's aim is a failure by name.

  | Damaged live state | Before | After |
  | --- | --- | --- |
  | none | `rc=0`, `74 pass / 0 fail` | `rc=0`, `74 pass / 0 fail` |
  | `contract.sexp` deleted | `rc=1`, `73 pass / 1 fail` | `rc=0`, `74 pass / 0 fail` |
  | `references.sexp` deleted | `rc=1`, `FileNotFoundError` | `rc=0`, `74 pass / 0 fail` |
  | `requirements.sexp` garbled | `rc=1`, `SexpError` | `rc=0`, `74 pass / 0 fail` |

  The three mutations still fail (70/4, 73/1, 71/3), as the driver expects. No path a case pins moved. Next at the 5:1 turn: the next of the ten, `probe_retained_sail_identity.py` (two live reads), then `probe_div_capture_retention.py` (one).
  Slice j (`2026-11-07`, `SEMULITH-XTASK-0088`; on clean ee6829b7; evidence target/xtask/xt0088): `UNIT-BOOKS`' probes judge a fixture of their own. The 5:1 turn, after a51-14. **What measuring found.** The doctrine's arms and `probe_unit_books.py` already read synthetic trees. The real reads were in `probe_book_navigation.py`'s command-line tests, which ran the real tool, so its root was the real tree: `lan9118-lab-v0` and `netboard-lab-v0`, the real registry and the real `docs/tasks/P4-SYSTEM.md`. **The change.** Those tests run a copy of the tool inside the fixture, so its root is where it stands, and nothing it reads is the real tree's. The tool gains no knob for this.

  | Damaged state | Before | After |
  | --- | --- | --- |
  | none | `rc=0` | `rc=0` |
  | a unit's row removed from `materials/units.sexp` | `rc=2`, navigation probe failed | `rc=1`, `MODEL-CATALOGUE unregistered lan9118-lab-v0` |
  | the registry unreadable | `rc=2`, navigation probe failed | `rc=2`, `REFUSED — cannot read materials/units.sexp` |
  | `docs/tasks/P4-SYSTEM.md` moved | `rc=2`, navigation probe failed | `rc=1`, `BOOK DOES NOT BUILD project` |
  | the tool's renderer check removed | not measured | `rc=2`, navigation probe failed: the controls still discriminate |

  Self-test unchanged, and 27 probe tests. No path a case pins moved. Next at the 5:1 turn: PROFILE-CONSISTENCY's probes, case by case.
  Slice i (`2026-11-07`, `SEMULITH-XTASK-0087`; on clean 815c7afb; evidence target/xtask/xt0087): `RECORD-SCHEMA`'s controls judge a frozen copy, so a damaged real schema fails by its own name. The 5:1 turn, after a51-9. **The change.** `scripts/fixtures/record-schema/`, 21 files, 61,774 B: the 15 grammars the controls read, `schema-tokens.sexp` with one facet per token language, and five documents shrunk to what their schemas require. The names are flat because the judge finds catalogues by basename anywhere in the tree: the first layout kept a `schema/` directory in the fixture, and the first real run judged those grammars as records. The self-test's fixture root held a link to the real `schema/` and copied the real JSON schemas, so a damaged grammar missed arms about something else. It now copies the frozen grammars into scratch, so no arm can reach a real directory. A new real step runs before the judge, `probe_schema_token_facets.py --live`: every real facet, the inventory and the five complete documents, each finding by name. **A defect measuring found:** a JSON schema that is not JSON crashed the judge, and the report was a traceback, then "a record file contradicts its schema" with an empty body. It now refuses, naming the file, with an arm of its own. **Stated counts.** A new anchored facet now moves one number, `LIVE_FACETS` in the probe. It used to restate three, 143 in the probe and 148 and 864 in the driver.

  | Damaged state | Before | After |
  | --- | --- | --- |
  | none | `rc=0`, `ok` | `rc=0`, `ok` |
  | an unreviewed token language in a real schema | `rc=2`, self-test miss | `rc=1`, names the facet: `no reviewed token example` |
  | a real facet's end anchor lost | `rc=2`, self-test miss | `rc=1`, names the facet: `no reviewed token boundary` |
  | a real facet's `\Z` loosened to `$` | `rc=2`, self-test miss | `rc=1`, names the facet: `admits` |
  | a real facet's pattern removed | `rc=2`, self-test miss | `rc=1`, `142 anchored facet(s), the inventory states 143` |
  | `schema/contract-obligations.sexp` unreadable | `rc=2`, self-test miss | `rc=1`, names the file: `cannot load` |
  | `schema/contract.sexp` unreadable | `rc=2`, self-test miss, on an arm about something else | `rc=1`, names the file: `cannot load` |
  | a JSON schema that is not JSON | `rc=2`, self-test miss | `rc=2`, refuses, naming the file: `not valid JSON` |
  | a real document's token damaged | `rc=2`, self-test miss | `rc=1`, names the document and field |
  | the frozen copy's `schema-tokens.sexp` deleted | no such copy | `rc=2`, self-test miss naming it |

  Self-test: 89 arms, 1 of them new. No path a case pins moved. Next at the 5:1 turn: UNIT-BOOKS' probes.
  Slice h (`2026-11-07`, `SEMULITH-XTASK-0086`; on clean daadeb52; evidence target/xtask/xt0086): `CONTRACT-FREEZE`'s controls judge a frozen unit, and a lost contract is named. The 5:1 turn, after a51-4. **What measuring found.** Today's self-test was the only thing catching a deleted contract: the judge itself reads `ok (0 versioned unit(s), 0 version(s), 0 finding(s))`. Freezing the controls alone would have turned that refusal into a quiet pass. So the judge gains two findings, `CONTRACT MISSING` and `NO VERSIONED UNIT`, each with an arm. **The change.** `scripts/fixtures/contract-freeze/profiles/u/` holds four versions, six records and one supersession, verbatim from `rv64gc-lab-v0`, their pins still matching, and `probe_contract_ancestry.py` reads it too. A missing frozen file is named before any arm runs. Each state judged by the binary before and after on throwaway clones:

  | Damaged state | Before | After |
  | --- | --- | --- |
  | none | `rc=0` | `rc=0` |
  | `contract.sexp` deleted | `rc=2`, self-test miss | `rc=1`, `CONTRACT MISSING rv64gc-lab-v0` |
  | a version's catalogue part deleted | `rc=1`, `UNREADABLE CATALOG` | the same |
  | a frozen record edited | `rc=1`, `FROZEN RECORD EDITED` | the same |
  | a member removed | `rc=1`, `UNVERSIONED RECORD` | the same |
  | the frozen copy deleted | no such copy | `rc=2`, naming it |

  Self-test: 15 arms, 2 of them new. No path a case pins moved. Next at the 5:1 turn: RECORD-SCHEMA's probes.
  Slices 13d–13g: [retained verbatim](archive/XTASK-9.md#slice-paragraphs-13d-to-13g).

- ID: `XTASK.14` — **a killed gate cannot block a cleanup: printable prefetch keys**
  Status: `done` (`2026-11-06`, `SEMULITH-XTASK-0083`; on clean f73cbf53; evidence target/xtask/xt0083)
  Goal: the defect `ARTIFACT-CLEANUP.37` found. `XTASK.8`'s prefetch names its record files with U+001F and U+001E. A gate that dies leaves them under `target/doctrine-selftest/`, and the artifact census rightly refuses a control character, so one killed gate blocks every later cleanup until someone removes them by hand. **This is the second time:** AC0085 hit it on 2026-10-27, and `docs/knowledge/a-name-one-tool-writes-is-a-path-another-tool-refuses.md` named the fix without scheduling it.
  Result: a record key is now each argument percent-encoded, joined by commas, on both sides (`record_key`, `doctrine_prefetch.key`); a new arm holds the two equal through `doctrine_prefetch.py --key`, because a difference would not fail anything: every arm would quietly run live. Not counted in the 5:1, being a defect's fix. **Measured** (red-before.txt, red-after.txt, misses.txt): before, `census refuses: unsafe relative path`; after, the census accepts it; `PROFILE_CONSISTENCY_PREFETCH_MISSES` over a whole self-test wrote nothing: 0 misses, `PROFILE-CONSISTENCY: ok`. Left alone: a dead process's scratch directory stays until a cleanup's hand reaches it, which the census can now read and the recurring record can name.

- ID: `XTASK.15` — **the commit chain and its scratch sweep are tracked**
  Status: `done` (`2026-11-10`, `SEMULITH-XTASK-0089`; found by `ARTIFACT-CLEANUP.40`, AC0096; on clean 8f8caa23; evidence target/xtask/xt0089)
  Goal: `target/xtask/xt0002/commit-chain.sh` and `target/xtask/sweep_unit_scratch.sh` run for every unit, yet both are untracked files under `target/`. A fix to either is not versioned, and removing `target/` removes them. AC0096 found the cost: the sweep had left 21 scratch clones of 13 landed units (524,516 KiB), because it looked only inside `red-*`. It is fixed in place, with a control, on this disk only. Move both behind `cargo xtask`, the chain's refusal of an empty message and the sweep's control as tests: a repository one and two levels down removed; a broken `.git`, a symlink and every file kept. One slice, at the next XTASK turn, ahead of `XTASK.13`'s next: it is small, and every unit's commit runs through it.
  Result: `cargo xtask commit-unit <evidence-dir>` is the chain and `cargo xtask sweep-scratch <evidence-dir>` the sweep, in `xtask/src/commit_unit.rs`. The 5:1 turn, after `P4-SYSTEM.18` slice c1. **Kept:** the refusal of an empty or misshapen message before any check runs, the focused set into `<dir>/commit-focused`, `git commit -F` under the hooks with its output in `<dir>/commit.log`, the message emptied only when the commit lands, then the sweep. **Measured equal:** on two identical layouts the shell sweep and this one remove the same four directories and leave the same 16 paths (equivalence.txt). **Two hazards closed, each measured.** (1) A hook's `GIT_DIR` and `GIT_INDEX_FILE` would send a scratch repository's git into the committing one. Every git here drops those variables: pointed at a decoy repository, the tests pass and the decoy is untouched, and with the scrub omitted seven of eight fail and the decoy's config is written (decoy.txt). (2) Under `cargo run` the gate would inherit 16 variables that describe the `xtask` package (env-xtask.txt), so `git commit` starts without them. **Controls:** 10 tests on scratch repositories; each of 17 guards, weakened alone, fails one (mutations.tsv). **Corrected at `XTASK.16`:** this record and its commit message said `cargo test` ran them at every commit. Nothing did then. The focused set does since `XTASK.16`. The shell files stay under `target/` as one-line callers. This unit lands through `cargo xtask commit-unit`.

- ID: `XTASK.16` — **a check runs when its driver changes: the gate's skip is turned round, and the chain runs the tests**
  Status: `done` (`2026-11-10`, `SEMULITH-XTASK-0090`; found landing `XTASK.15`; on clean 276ce805; evidence target/xtask/xt0090)
  Goal: `XTASK.15`'s gate took 2.5 minutes where the two before it took 21. The gate may answer six heavy checks from their last green run when a commit stages nothing inside the inputs each declares (`XTASK.8` slice d). No declaration named `xtask/`, where all six drivers have lived since 2026-10-27, so a commit changing only a driver skipped that driver's own check.
  Result: not counted in the 5:1, being a defect's fix. **Measured.** (1) Of 189 commits since 2026-10-27, 11 change `xtask/` and stage nothing inside any of the six declarations, and `447ad5f9` changed three of the six drivers that way. (2) Nothing wrong landed: all 42 doctrines pass with nothing skipped, and `cargo test --all` passes 529 tests. (3) The declarations were incomplete for documents too. With every documentation file absent, five of the six pass. `PROFILE-CONSISTENCY` passes only with four present: three decision records the dossier's selections name, and one unit-book page a probe opens. **The fix.** The declaration is turned round. `scripts/doctrine_skip.sh` keeps a short ledger of documentation that records the work. A check skips only when every staged path is ledger and every tracked byte outside the ledger is as it was at the check's last green run. A ledger document that tracked data names is derived at each commit and counts as an input. So code never skips, and nothing has to list it. The gate runs the rule's 37 controls before it may skip, and refuses in one second when they fail. `scripts/probe_ledger_independence.sh` repeats the measurement. **The tests.** Nothing ran `cargo test` at a commit, though `XTASK.15`'s record said so. The focused set now runs `cargo test --all` third: 30 checks, and 40 s more. **Room.** `XTASK.13`'s slices d to g moved verbatim to archive part 9, and six count clauses left the toolbox. `decision_docs-only-gate-path.md` carries the addendum.

- ID: `XTASK.17` — **the ledger's independence is re-measured at the push boundary**
  Status: `pending` (opened `2026-11-10` by `XTASK.16`)
  Goal: the gate's own controls hold the skip rule to its logic, and the documents data names are derived. One thing they cannot see is a script that starts reading a ledger document. `scripts/probe_ledger_independence.sh` measures exactly that in about 20 minutes, and today it runs by hand. Run it where the push suite runs, on a scratch copy of the tree if the suite's other legs must not see documents vanish, and refuse the push when a skipping check reads the ledger.

- ID: `XTASK.18` — **the chain's message check says what it wants, and accepts what the hook accepts**
  Status: `done` (`2026-11-10`, `SEMULITH-XTASK-0091`; found landing `SEMULITH-LC-0056`; the XTASK turn after five features; evidence target/xtask/xt0091)
  Goal: `cargo xtask commit-unit` refused the subject `SEMULITH-LC-0056: …` in one second with `EMPTY-OR-MALFORMED git_message_brief.txt: not starting the gate`. The commit-msg hook accepts that shape, and the four push records carry it. The check wants a space after the number, as the shell chain's did, and its refusal does not say so. Accept a colon there too, and print the shape it wants. Small: a one-second refusal, and the unit landed with the usual `(leaf …)` subject.
  Result: the XTASK turn after five feature units (`.18` c2a, c2b, `.19` a, `P5-BOARD.13`'s brief, `.20`'s brief). `subject_shaped` in `xtask/src/commit_unit.rs` accepts a space or a colon after the number, and the refusal prints the shape it wants and the first line it got, cut at 80 characters. Before: `SEMULITH-LC-0056: …` refused with no reason. After: the same subject passes the check (a unit test), and `SEMULITH-P4-0396; another mark` is refused with both halves printed. The hook stays the judge of the subject; this only keeps the gate from running on a message that cannot pass it.

- ID: `XTASK.19` — **the toolchain floats: hosted CI installs today's stable, so a Rust release turns it red with no code change**
  Status: `active` (found `2026-11-14` by the approved push `SEMULITH-PUSH-0007`: hosted run `43633628211`, `rust`, failed on `aa93d858` while `make ci` was green twice locally; slices a and a2 done `2026-11-14`, `SEMULITH-XTASK-0096` and `-0097`; slice b `2026-11-15`, `SEMULITH-XTASK-0098`; open until the hosted runs are green)
  Defect: `rust-toolchain.toml` names `channel = "stable"`, and all three workflows install and select `stable` (`RUSTUP_TOOLCHAIN=stable`), so each hosted run takes that day's release while this host's `stable` is 1.95.0. Rust 1.100.0 came out on 2026-11-09, after the last hosted run (2026-11-07), and its clippy flags `needless_range_loop` at four sites in `crates/semulith-dsp56300`: `dump.rs` lines 42, 45 and 48, and a test at `exec.rs` line 882. `cargo clippy --all-targets --all-features -- -D warnings` fails on them. **Reproduce:** `RUSTUP_HOME=.app-data/rustup-ci rustup toolchain install 1.100.0 --profile minimal --component clippy,rustfmt`, then that clippy command under `RUSTUP_TOOLCHAIN=1.100.0` and an on-volume `CARGO_TARGET_DIR`: the same four errors (target/ci-recovery/toolchain-drift/clippy-1.100.log). Crates that depend on `semulith-dsp56300` were not reached, so more may follow. **Impact:** the hosted `rust` workflow is red; any later push can fail the same way on a release nobody chose.
  Plan: (a) the four loops iterate their arrays, and clippy 1.100 runs again until the workspace is clean; (b) the toolchain is pinned to one exact version that `rust-toolchain.toml` names and every workflow installs, so local and hosted builds judge with the same clippy, and a version bump becomes a unit of its own, with a decision record (after `LIVE-CONTAINMENT.6`: the decisions index has 23 B left); (c) the push that turns hosted CI green is the director's to approve. **Approved, 2026-11-14, the director's words:** "Granted \"Your call, later: turning hosted CI green needs one more push after XTASK.19 lands. I'll ask then.\"." With a caution, also theirs: "Look push shall be exceptional so please do not use exceptionality to push without honoring the push cadence. So I hope these pushes of yours are really exceptional." So: exactly one push, for this purpose only, after this leaf lands and `make ci` is green on the pinned toolchain, through `scripts/approved_push.sh` with those words; nothing else rides on it, and every later push waits for the 300-commit cadence.
  Second symptom (found `2026-11-14` reading hosted run `43633628199`, `portability`): the native leg `host (ubuntu-latest, rv64i-lab-v0)` failed and the matrix cancelled the other three. Rust 1.100.0's cargo puts integration-test executables under `target/debug/build/<package>/<hash>/out/`, and five test files in `crates/semulith-cli/tests` found the `semulith` binary two directories above their own executable: ten tests panicked on `NotFound` (the uploaded `native.log`). **Reproduced** on 1.100.0 here: `cargo test --all --no-fail-fast` 529 passed, 10 failed, every failure that spawn (target/xtask/xt0097/test-1.100-before.log). The same root cause: a release nobody chose.
  Acceptance: `cargo clippy --all-targets --all-features -- -D warnings` and `cargo test --all` pass on the pinned toolchain locally and in the hosted `rust` and `portability` workflows; the pin is held by a check, so a workflow that floats again refuses.
  Order: next, before `P4-SYSTEM.20` g: a red hosted CI is a defect owned now. Maintenance, not a feature unit.
  Slice a (`SEMULITH-XTASK-0096`, evidence target/xtask/xt0096): the three register loops in `dump.rs` iterate `m.r`, `m.n` and `m.m` with `enumerate()`, and the test at `exec.rs` zips the addresses with the slice `m.x[0x200..=0x20D]`. Clippy 1.100.0 now passes over the whole workspace (`clippy-1.100.log`, every crate checked, `rc=0`); on the same target directory HEAD's files fail with exactly the four errors (`red-head.log`, `rc=101`). On this host's 1.95.0, fmt, clippy and the crate's 17 tests pass, and the runner's dump is byte-identical to HEAD's on all six DSP guests with `--dump-mem --dump-stack` (`dump/cmp.log`). Slice b, the pin and the check that holds it, follows `LIVE-CONTAINMENT.6`, so its decision record has room.
  Slice a2 (`SEMULITH-XTASK-0097`, evidence target/xtask/xt0097): the `cli` helper in the five test files runs `env!("CARGO_BIN_EXE_semulith")`, the path Cargo sets for a package's integration tests, instead of climbing from its own executable. On 1.100.0 `cargo test --all --no-fail-fast` now passes 539 of 539 (`test-1.100-after.log`), and clippy 1.100.0 stays clean; on 1.95.0, fmt, clippy and the crate's 14 tests pass. The tests' `root()` helpers still climb to the repository root from their executable, which holds while `target/` lives inside the repository, as it must on this volume; they were left. The closed acceptance checklists of `XTASK.7` to `XTASK.12`, `XTASK.15`, `XTASK.16` and `XTASK.18` moved verbatim to `archive/XTASK-11.md` (`move.log`: two spans, 22,377 B, each found once with its digest), so this file has room for slice b: 129,456 → 107,392 B before this record.
  Slice b (`SEMULITH-XTASK-0098`, evidence target/xtask/xt0098): `rust-toolchain.toml` names `channel = "1.95.0"`, and the three workflows set `RUSTUP_TOOLCHAIN=1.95.0` and run `rustup toolchain install 1.95.0`. 1.95.0, not the newest release, because it is the exact build (`59807616e`) behind every local gate, the version-0 release and the recorded portability rows: pinning it changes nothing this host measures, and moving to 1.100.0 is a later unit of its own, which slices a and a2 already prepared. The new doctrine `TOOLCHAIN-PIN` (`xtask/src/check_toolchain_pin.rs`, shim `scripts/check_toolchain_pin.sh`, registered after `ARTIFACT-COHORT`) refuses a channel or a partial version in the toolchain file, and a workflow step that selects a channel, another release, or a variable not assigned from the Miri leg's printer; its self-test judges ten frozen fixtures. Born in Rust behind a shim, like the 42 ported drivers. The local toolchain stays the same build: `rustup show active-toolchain` names `1.95.0-aarch64-apple-darwin`, `rustc 1.95.0 (59807616e 2026-04-14)`. Its targets match what local checks need (`wasm32-unknown-unknown`); the Rosetta leg's `x86_64-apple-darwin` is not installed in it, and since that leg runs only by hand, the target is added when a unit next records it (`.20` g), as the leg's hint says. Recorded in `decision_the-toolchain-is-pinned.md`.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `XTASK.19` | `active` | hosted CI is red on `aa93d858`; slices a and a2 fixed what Rust 1.100.0 broke, slice b pinned 1.95.0 under `TOOLCHAIN-PIN`; next `make ci`, the director's one push, and the hosted runs read green; before `P4-SYSTEM.20` g |
| 2 | `XTASK.13` | `active` | ruling 5's rule for the eleven fragile doctrines, one slice each, between feature units: slices a (DEF-GEN), b1 (GUEST-GEN's census and surgical arms), b2 (its mirror and parcel-count arms) b3 (its parcel author probe), b4 (the author probes' owned corpus, and the real-run step) and b5 (their other corpus reads), b6 (the rest of its self-test: GUEST-GEN whole), c (BOOK-INDEX), d (BOARD-GEN), e (PLATFORM-GEN), f (MATERIALS-BILL), g (EXERCISE-COVERAGE), h (CONTRACT-FREEZE), i (RECORD-SCHEMA) and j (UNIT-BOOKS) done; PROFILE-CONSISTENCY's probes: k (`probe_experiment_graph.py`) and l (`probe_retained_sail_identity.py`) done 2026-11-14; m next, the policy review's finding naming the method's reason, then the next probe, case by case, after five feature units |
| 3 | `XTASK.17` | `pending` | the ledger probe runs by hand; at the push boundary it would run every time |

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
- (Answered 2026-10-29 by the workflow under the director's delegation of scheduling: yes — `XTASK.13`.) (e, `2026-10-28`) Whether ruling 5's rule (a self-test judges frozen copies; a deleted source fails by name) extends to the 11
  doctrines `XTASK.11` slice e classified FRAGILE (target/xtask/xt0068/classification.md). Recommended: yes, one slice per
  doctrine in this order — DEF-GEN and GUEST-GEN (their live in-sync arm repeats the real check: drop it, keep a frozen pair),
  BOOK-INDEX (freeze a small book), then BOARD-GEN, PLATFORM-GEN, MATERIALS-BILL, EXERCISE-COVERAGE, CONTRACT-FREEZE, the
  RECORD-SCHEMA and UNIT-BOOKS probes, and PROFILE-CONSISTENCY's 14 probes last, case by case (some real-tree arms are deliberate
  predictions and stay, named). The director's.

## Blockers

- None. (`XTASK.5`'s blocker of 2026-10-24 — the pinned `gate_report.py` reading `check-examples` in the CLI source —
  was resolved by decision on 2026-10-26: the command stays in the CLI; see the leaf.)

## Acceptance Checklists (leaves XTASK.1 to XTASK.4)

[Retained verbatim](archive/XTASK-10.md#acceptance-checklists-xtask-1-to-xtask-4).

## Acceptance Checklist (leaf XTASK.6)

Rows 6a–6o: [retained verbatim](archive/XTASK-1.md#acceptance-rows-6a-to-6o).
Rows 6p–6x (with 6r-b): [retained verbatim](archive/XTASK-2.md#acceptance-rows-6p-to-6x).
Rows 6y–6ap: [retained verbatim](archive/XTASK-4.md#acceptance-rows-6y-to-6ap).
Rows 6aq–6av: [retained verbatim](archive/XTASK-5.md#acceptance-rows-6aq-to-6av).

## Acceptance Checklists (leaves XTASK.7 to XTASK.9)

[Retained verbatim](archive/XTASK-11.md#acceptance-checklists-xtask-7-to-xtask-9).

## Acceptance Checklist (leaf XTASK.13)

- [x] slice l **ROOT CAUSE** — `git show 96b97664:scripts/probe_retained_sail_identity.py | grep -c 'selected_parent(ROOT)\|bounded_bytes(ROOT / IDENTITY)'` = 2: the live dossier and descriptor; damaged in a clone, `grep -c 'before	rc=1' target/xtask/xt0093/red.txt` = 3.
- [x] slice l **ADDRESSED** — `grep -c 'after	rc=0	RETAINED-SAIL-IDENTITY: 11 tests / 0 failures / 0 errors' target/xtask/xt0093/red.txt` = 4: undamaged and in each damaged state.
- [x] slice l **NO REGRESSION** — `python3 -B scripts/probe_retained_sail_identity.py` → `RETAINED-SAIL-IDENTITY: 11 tests / 0 failures / 0 errors`, plain and `-O`, the string `grep -n 'RETAINED-SAIL-IDENTITY' xtask/src/check_profile_consistency.rs` expects; a garbled live descriptor still fails the real judgement: `grep -c 'FINDING finite method not satisfied (refused)' target/xtask/xt0093/real-check-policy.txt` = 42.
- [x] slice k **ROOT CAUSE** — `git show 1fa19741:scripts/probe_experiment_graph.py | grep -n 'profiles/rv64gc-lab-v0'` → line 199, the scope arms' directory: the live dossier; damaged in a copy, `grep -c 'before	rc=1' target/xtask/xt0092/red.txt` = 3.
- [x] slice k **ADDRESSED** — `grep -c 'after	rc=0	EXPERIMENT-GRAPH: 74 pass / 0 fail' target/xtask/xt0092/red.txt` = 4: undamaged and in each damaged state.
- [x] slice k **NO REGRESSION** — `bash scripts/check_requirements.sh` → `RECORD-SCHEMA: ok (42 record file(s) …)`; `python3 -B scripts/probe_experiment_graph.py` → `EXPERIMENT-GRAPH: 74 pass / 0 fail`, plain and `-O`; `--mutation ignore-witness-budget` → `70 pass / 4 fail`, `ignore-witness-kind` → `73 pass / 1 fail`, `ignore-control-baseline` → `71 pass / 3 fail`, the four strings `grep -n 'EXPERIMENT-GRAPH' xtask/src/check_profile_consistency.rs` expects.
- [x] slice j **ROOT CAUSE** — the navigation probe's command line ran the real tool over the real tree: `grep -c 'unit-row-removed before rc=2' target/xtask/xt0088/red-states.txt` = 1, and `git show ee6829b7:scripts/probe_book_navigation.py | grep -c "N.ROOT / 'docs/models/lan9118-lab-v0'"` = 1.
- [x] slice j **ADDRESSED** — `grep -c 'unit-row-removed after rc=1' target/xtask/xt0088/red-states.txt` = 1, naming it: `grep -c 'MODEL-CATALOGUE unregistered lan9118-lab-v0' target/xtask/xt0088/red-unit-row-removed-after.txt` = 1; `grep -c 'task-file-moved after rc=1' target/xtask/xt0088/red-states.txt` = 1; the controls still discriminate: `grep -c 'tool-damaged after rc=2' target/xtask/xt0088/red-states.txt` = 1.
- [x] slice j **NO REGRESSION** — `grep -c 'green-control after rc=0' target/xtask/xt0088/red-states.txt` = 1; `git diff --cached --name-only | grep -c evidence/` = 0; `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `46 credit(s), 46 current, 0 lapsed`.
- [x] slice i **ROOT CAUSE** — the controls read the real grammars, so damage read as a check that cannot discriminate: `grep -c 'unreviewed-language before rc=2' target/xtask/xt0087/red-states.txt` = 1, `grep -c 'lost-facet before rc=2' target/xtask/xt0087/red-states.txt` = 1, and the unnamed crash: `grep -c 'Traceback' target/xtask/xt0087/red-json-schema-damaged-before.txt` = 4.
- [x] slice i **ADDRESSED** — `cargo xtask check-requirements --self-test` `rc=0`, `89 pass / 0 fail`; `grep -c 'unreviewed-language after rc=1' target/xtask/xt0087/red-states.txt` = 1, `grep -c 'schema-unreadable after rc=1' target/xtask/xt0087/red-states.txt` = 2, `grep -c 'json-schema-damaged after rc=2' target/xtask/xt0087/red-states.txt` = 1, `grep -c 'frozen-deleted after rc=2' target/xtask/xt0087/red-states.txt` = 1; `python3 -B scripts/probe_schema_token_facets.py --live` `rc=0`; each mutation still fails its control: `python3 -B scripts/probe_schema_token_facets.py --mutation loose-end` → `FAILED (failures=43)`.
- [x] slice i **NO REGRESSION** — `grep -c 'green-control after rc=0' target/xtask/xt0087/red-states.txt` = 1; `git diff --cached --name-only | grep -c evidence/` = 0; `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `38 credit(s), 38 current, 0 lapsed`.
- [x] slice h **ROOT CAUSE** — the self-test read the live contract, and was the only catch for a lost one: `grep -c 'contract-deleted before rc=2' target/xtask/xt0086/red-states.txt` = 1, and `grep -c '0 versioned unit(s), 0 version(s), 0 finding(s)' target/xtask/xt0086/red-contract-deleted-before.txt` = 1.
- [x] slice h **ADDRESSED** — `cargo xtask check-contract-freeze --self-test` `rc=0`, `15 pass / 0 fail`; `grep -c 'contract-deleted after rc=1' target/xtask/xt0086/red-states.txt` = 1, naming it: `grep -c 'CONTRACT MISSING rv64gc-lab-v0' target/xtask/xt0086/red-contract-deleted-after.txt` = 2; `grep -c 'frozen-deleted after rc=2' target/xtask/xt0086/red-states.txt` = 1; `CONTRACT-ANCESTRY: 4 tests / 0 failures / 0 errors`.
- [x] slice h **NO REGRESSION** — `grep -c 'green-control after rc=0' target/xtask/xt0086/red-states.txt` = 1; `git diff --cached --name-only | grep -c evidence/` = 0; `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `36 credit(s), 36 current, 0 lapsed`.
- [x] slice g **ROOT CAUSE** — the self-test read the live fragments: `grep -c 'base-deleted before rc=2' target/xtask/xt0085/red-states.txt` = 1, the verdict `EXERCISE-COVERAGE: REFUSED — the check does not discriminate (self-test failed).`, on a self-test miss whose detail points into the self-test's own scratch copy, never at the real fragment.
- [x] slice g **ADDRESSED** — `cargo xtask check-exercise-coverage --self-test` `rc=0`, `23 pass / 0 fail`; `grep -c 'deleted after rc=1' target/xtask/xt0085/red-states.txt` = 3 and `grep -c 'after rc=1' target/xtask/xt0085/red-states.txt` = 5, each naming its fragment (`grep -c 'UNMET DEPENDENCY' target/xtask/xt0085/red-base-deleted-after.txt` = 2, one per dossier composing it); `grep -c 'frozen-deleted after rc=2' target/xtask/xt0085/red-states.txt` = 1.
- [x] slice g **NO REGRESSION** — `grep -c 'green-control after rc=0' target/xtask/xt0085/red-states.txt` = 1; `git diff --cached --name-only | grep -c evidence/` = 0; `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `30 credit(s), 30 current, 0 lapsed`.
- [x] slice f **ROOT CAUSE** — the self-test read the live dossiers: `grep -c 'dossier-deleted before rc=2' target/xtask/xt0084/red-states.txt` = 1, `MATERIALS-BILL: REFUSED — the check does not discriminate (self-test failed).`, naming nothing.
- [x] slice f **ADDRESSED** — `cargo xtask check-materials-bill --self-test` `rc=0`, `12 pass / 0 fail`; `grep -c 'after rc=1' target/xtask/xt0084/red-states.txt` = 5, each naming its unit (`grep -c 'CANNOT JUDGE' target/xtask/xt0084/red-board-deleted-after.txt` = 1).
- [x] slice f **NO REGRESSION** — `grep -c 'green-control after rc=0' target/xtask/xt0084/red-states.txt` = 1; `git diff --cached --name-only | grep -c evidence/` = 0; every fragment `gen_model_book: ok`.
- [x] slice e **ROOT CAUSE** — `scripts/check_platform_gen.sh` self-test read the live board and the live dossier: with `profiles/netboard-lab-v0/board.sexp` deleted the before binary reads `rc=2`, `PLATFORM-GEN self-test MISS: GREEN the generator emits the manifest from the real inputs`, a scratch path, and the same for the obligations, the profile and a deleted `platform.sexp` (target/xtask/xt0082/red-states.txt). Two arms ran `--check` from another directory, so `grep -c 'board-dir", &p("d1")' ` on the old source = 1 shows the path alone made them DRIFT.
- [x] slice e **ADDRESSED** — `cargo xtask check-platform-gen --self-test` `rc=0`, `13 pass / 0 fail`; each deleted source `rc=1` naming its file, with the controls unaffected; the hand-edited manifest `rc=1` DRIFT; a damaged frozen profile `rc=2`.
- [x] slice e **NO REGRESSION** — every state restored (`git diff --quiet`); `PLATFORM-GEN: ok (1 board(s)…)` on the clean tree, `rc=0`, its verdict line unchanged; `BOARD-GEN --self-test: 11 pass / 0 fail`; `bash scripts/check_requirements.sh` `rc=0`; `DERIVED-COUNTS: ok`; `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0`, `19 current, 0 lapsed`; no path a case pins moved.

- [x] slice d **ROOT CAUSE** — `scripts/check_board_gen.sh` self-test read the live board and its live part units: with `profiles/netboard-lab-v0/board.sexp` deleted the before binary reads `rc=2`, `BOARD-GEN self-test MISS: GREEN the generator emits the artifacts from the real definition`, a scratch path, and the same for a part's deleted `requirements.sexp` (target/xtask/xt0081/red-states.txt).
- [x] slice d **ADDRESSED** — `cargo xtask check-board-gen --self-test` `rc=0`, `11 pass / 0 fail`; the deleted definition `rc=1` naming `profiles/netboard-lab-v0/board.sexp: missing`, with the controls unaffected; the deleted part catalogue `rc=1` naming its unit in each `DANGLING DEP`; the hand-edited artifact and moved definition `rc=1` DRIFT; a damaged frozen part `rc=2`.
- [x] slice d **NO REGRESSION** — every state restored (`git diff --quiet`); `BOARD-GEN: ok (1 board(s)…)` on the clean tree, `rc=0`; `DERIVED-COUNTS: ok`, 1744 arms; `bash scripts/check_readme_routes.sh` `rc=0`; `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0`, `5 current, 0 lapsed`; no path a case pins moved.

- [x] slice c **ROOT CAUSE** — `scripts/check_book_index.sh` self-test copied the live book: with `docs/book/src/claim-scope.md` deleted the before binary reads `rc=2`, `BOOK-INDEX self-test MISS: GREEN the generator emits an index from the real book` over a scratch path (target/xtask/xt0080/red-states.txt); `grep -n 'SUMMARY.md").is_file' xtask/src/check_book_index.rs` at 18a09566: the real run's only guard read a deleted `SUMMARY.md` as no book.
- [x] slice c **ADDRESSED** — `cargo xtask check-book-index --self-test` `rc=0`, `14 pass / 0 fail`; the three deleted sources `rc=2` naming each file (`no SUMMARY.md under docs/book/src`), with the controls unaffected; the hand-edited index `rc=1` DRIFT; the fixture damaged `rc=2`; clean `rc=0`, `BOOK-INDEX: ok (… 40 table rows)`.
- [x] slice c **NO REGRESSION** — every state restored (`git diff --quiet`, `cmp`); `DERIVED-COUNTS: ok`; `bash scripts/check_readme_routes.sh` `rc=0`; the focused stage and the commit gate (target/xtask/xt0080 chain log). No path a case pins moved: `git diff --cached --name-only` ∩ target/p4-system-14/a43e-4/frozen-paths.txt = ∅.

- [x] slice b6 **ROOT CAUSE** — target/xtask/xt0078/red/fragment.err: `zifencei.sexp` deleted, `rc=2`, `GUEST-GEN --self-test: 246 pass / 154 fail`: `python3 -B scripts/live_reads.py` names 23 live composition files in each of seven probes, and `stage_gc_c_corpus.py` read them too, so one damaged live source refused the self-test instead of failing by name.
- [x] slice b6 **ADDRESSED** — target/xtask/xt0079/red-states.txt: six states, each `rc=1` naming the file (`composes 'riscv/zifencei', but definitions/riscv/zifencei.sexp does not exist`; `sexp.SexpError: definitions/riscv/zifencei.sem.sexp: 3 unterminated list(s)`), `GUEST-GEN --self-test: 400 pass / 0 fail` in every one.
- [x] slice b6 **NO REGRESSION** — `GUEST-GEN: ok` on the clean tree, `rc=0`, `400 pass / 0 fail`; every state restored (`cmp` silent, `git diff --stat -- definitions` empty); `GC-SNAPSHOT-AUTHOR: 21 tests / 0 failures`, its `canonical-context` omission still `1 failures`; `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` → `4 credit(s), 4 current, 0 lapsed`; staged ∩ the four manifests = ∅ (`grep -c` 0 each, staged.txt).
- [x] slice b5 **ROOT CAUSE** — target/xtask/xt0078/red-before.txt: `mm-sret` edited with its fixture regenerated, `corpus-record-edited before rc=2`, `GUEST-GEN --self-test: 399 pass / 1 fail`, the one miss `GREEN fixed misa and privileged author legality`: the probe read the live record; the census (`scripts/live_reads.py`) names 33, 57, 29, 25 and 23 live files in the five probes it touches.
- [x] slice b5 **ADDRESSED** — target/xtask/xt0078/red-after.txt: the same state `rc=1`, `MIRROR DRIFT — mm-sret.s`, `GUEST-GEN --self-test: 400 pass / 0 fail`; target/xtask/xt0078/final-census.txt: `live-nonschema 0` in all nine author probes; governor-census.txt: `not named by the governor: 0` over the 26, so no new step was added.
- [x] slice b5 **NO REGRESSION** — `GUEST-GEN: ok` on the clean tree, `rc=0`; `cmp` silent between the live and frozen 52 files; each state restored (`cmp`); `git diff --cached --name-only` holds no path of the case manifests; `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` → `4 credit(s), 4 current, 0 lapsed`; each probe's printed totals unchanged (`5 corpus repairs / 140 steps`, `17 corpus gaps / 476 steps`).
- [x] slice b4 **ROOT CAUSE** — target/xtask/xt0077/red-before.txt: `inj-walk-l0` edited with its fixture regenerated, `owned-record-edited before rc=2`, `GUEST-GEN --self-test: 391 pass / 9 fail`: eight author probes read the live owned corpus, so the self-test refused before any check could name the record, and no real-run step re-derived it.
- [x] slice b4 **ADDRESSED** — target/xtask/xt0077/red-after.txt: the same state `rc=1`, `MIRROR DRIFT — inj-walk-l0.s`, `GUEST-GEN --self-test: 400 pass / 0 fail`; target/xtask/xt0077/red-step.txt: one line of prose, `prose before rc=0`, `prose after rc=1`, `DRIFT — inj-walk-l0`; `python3 -B scripts/probe_gc_provenance.py --mutation parcel-history` still `AssertionError: generic output inherited FP provenance`.
- [x] slice b4 **NO REGRESSION** — `GUEST-GEN: ok` on the clean tree, `rc=0`; each state restored (`cmp`); `git diff --cached --name-only` holds no path of the three manifests (`grep -c` 0 each, target/xtask/xt0077/staged.txt); `python3 -B scripts/requirement_status.py --profile rv64gc-lab-v0` → `3 of 3 credit record(s) current; 0 drift`; the deriver unchanged (`git diff --cached --name-only` holds no `scripts/derive_rv64gc_expectations.py`).
- [x] slice b3 **ROOT CAUSE** — target/xtask/xt0076/red-before.txt: `gc-guest-missing` `rc=2` through the self-test, the miss `GREEN parcel author controls use only tracked inputs`; `legacy-guest-missing` `rc=2` with two arms missed, the first `GREEN byte guest budgets, visibility and head boundaries`; `grep -n 'profiles/rv64gc-lab-v0' scripts/probe_gc_parcel_guest.py` at b95a8f66 read the live encoding, guests and unit files, and `--cold` listed `definitions` and `profiles`.
- [x] slice b3 **ADDRESSED** — target/xtask/xt0076/red-after.txt: `gc-guest-missing` and `legacy-guest-missing` `rc=2` on the generator's refusal naming the file, `GUEST-GEN --self-test: 400 pass / 0 fail` in every state; `python3 -B scripts/probe_gc_parcel_guest.py --cold` `rc=0` → `tracked-only inputs and no reference cache passed`; each of the eight `--mutation` arms `rc=1` with its reason (m.*.out); the owned state: `derive_rv64gc_expectations: DRIFT — inj-walk-l0`, the check `391 pass / 9 fail` (red-owned.txt), naming slice b4's scope.
- [x] slice b3 **NO REGRESSION** — `in-sync` `rc=0` before and after, `GUEST-GEN: ok`; `git diff --cached --name-only` holds no path of `evidence/rv64gc-m-forms-v5/dependencies.sexp` or the xlen-v2 manifest (`grep -c` 0); `python3 -B scripts/requirement_status.py` → `46 planned, 2 implemented … 0 drift`; the staged prechecks and the commit gate (chain log).
- [x] slice a **ROOT CAUSE (WHY + WHERE)** — `self_test` copied the live fragments and pairs and judged the live rv64gc pair (`grep -c 'repo.join(ENCODING_GC)\|repo.join(OUT_GC)\|repo.join("definitions/riscv")'` = 3 in target/xtask/xt0073/check_definition_gen.rs.before); `run` returned ok when the rv64i encoding was absent; red.txt: four corpus states `before rc=2 REFUSED — the check does not discriminate (self-test failed)`.
- [x] slice a **FIX** — scripts/fixtures/def-gen/ (25 frozen files; `python3 -B scripts/gen_definition.py --check` over the frozen pair rc=0); xtask/src/check_definition_gen.rs: the controls read `FIXTURE`, `run` fails an orphaned module by name; scripts/probe_c_engine.py `--data-root`; clippy `-D warnings` rc=0.
- [x] slice a **ADDRESSED (verified)** — red.txt: `gc-module-hand-edited after rc=1 … out of sync`, `fragment-edited after rc=1 … out of sync`, `encoding-missing after rc=1 … is generated, but its encoding … is absent`, `fragment-missing after rc=2` naming the missing semantics document; `in-sync` rc=0 both; `tree restored: 0 paths changed`.
- [x] slice a **NO REGRESSION** — `DEF-GEN --self-test: 56 pass / 0 fail`; `bash scripts/check_definition_gen.sh` rc=0 (both pairs `ok … matches …`); `cargo test -p xtask` `test result: ok. 17 passed`; `python3 -B scripts/probe_c_engine.py` (default root) passes; the commit gate green (chain log).
- [x] slice b1 **ROOT CAUSE (WHY + WHERE)** — `self_test` copied the live rv64i guests and judged the live rv64gc pair (`grep -c 'repo.join(GUESTS_DIR)\|OUT_GC,' target/xtask/xt0074/check_guest_gen.rs.before` = 3); red.txt: `gc-fixture-hand-edited before rc=2 … self-test`.
- [x] slice b1 **FIX** — scripts/fixtures/guest-gen/ (two mini corpora; `gen_guests.py --check` over the frozen rv64gc pair rc=0); xtask/src/check_guest_gen.rs: the surgical and census arms read `FIXTURE_*`; clippy `-D warnings` rc=0.
- [x] slice b1 **ADDRESSED (verified)** — red.txt: `gc-fixture-hand-edited after rc=1 … out of sync`; `in-sync` rc=0 both; the two states still refused name their live arms (`GREEN the base mirror holds on the real tree`, `GREEN full historical parcel count census`) — b2; `tree restored: 0 paths changed`.
- [x] slice b1 **NO REGRESSION** — `GUEST-GEN --self-test: 400 pass / 0 fail` (before and after); the commit gate green (chain log).
- [x] slice b2 **ROOT CAUSE (WHY + WHERE)** — the base-mirror arms judged the live pair and the parcel-count arms counted the live corpus: in target/xtask/xt0075/check_guest_gen.rs.before `grep -c 'judge_mirror(repo, Path::new(GUESTS_DIR)'` = 3 and `grep -c '"scripts/derive_gc_parcel_counts.py",'` = 4, none passing an encoding or guest directory; target/xtask/xt0074/red/gc-guest-missing.after.err names the eight live arms; red-before.txt: `gc-mirror-drift` and `rv64i-guest-unassemblable` before refused through the self-test (396/4, 395/5).
- [x] slice b2 **FIX** — scripts/fixtures/guest-gen/base-mirror/ (16 files; `python3 -B scripts/check_gc_mirror.py --owner … --mirror … --encoding scripts/fixtures/def-gen/profiles/rv64gc-lab-v0/encoding.sexp` rc=0, `7 recorded re-derivation(s), 3 pinned …`); `check_gc_mirror.py --self-test --encoding`; `derive_gc_parcel_counts.py --encoding --guests`; xtask/src/check_guest_gen.rs: the 14 arms read the frozen pair and encoding; clippy `-D warnings` rc=0.
- [x] slice b2 **ADDRESSED (verified)** — red-invalid-before/*.after.*: `gc-mirror-drift after rc=1 … out of sync` (0 misses), `rv64i-guest-unassemblable after rc=2` the generator naming `smoke-arith.s` (0 misses), `gc-guest-missing after` `399 pass / 1 fail` (the cold probe, b3), `in-sync after rc=0`; `git status --short profiles` restored 0 paths.
- [x] slice b2 **NO REGRESSION** — `GUEST-GEN --self-test: 400 pass / 0 fail` (guest-gen-selftest.log); `cargo test -p xtask` `test result: ok. 17 passed`; `python3 -B scripts/derive_gc_parcel_counts.py` live `171 exact architectural traces`, its manifest equal to HEAD's but the tool's own digest; `python3 -B scripts/check_gc_mirror.py` live `46 file(s) byte-identical, 42 … count-only`; freeze-check.txt empty; the commit gate (chain log).

## Acceptance Checklists (leaves XTASK.10 to XTASK.12, XTASK.15, XTASK.16 and XTASK.18)

[Retained verbatim](archive/XTASK-11.md#acceptance-checklists-xtask-10-to-xtask-18).

## Acceptance Checklist (leaf XTASK.19)

- [x] **REPRODUCE / ISSUE** — hosted run `43633628211` (`rust`, `aa93d858`): `Clippy (deny warnings)` exits 101 on four `needless_range_loop` errors (`gh run view 43633628211 --log-failed`); reproduced on HEAD's files with 1.100.0 from `.app-data/rustup-ci` (target/xtask/xt0096/red-head.log: the four errors, `rc=101`).
- [x] **ROOT CAUSE (WHY + WHERE)** — `RUSTUP_TOOLCHAIN=stable` in all three workflows and `channel = "stable"` in `rust-toolchain.toml`: each hosted run takes that day's release (`clippy 0.1.100 (0ef1bc3860 2026-11-09)`), which flags index loops this host's 1.95.0 accepts.
- [x] **FIX (slice a)** — `crates/semulith-dsp56300/src/dump.rs`: the `r`, `n` and `m` loops iterate the arrays; `src/exec.rs`: the REP test zips the addresses with the slice.
- [x] **ADDRESSED (slice a, verified)** — 1.100.0: `cargo clippy --all-targets --all-features -- -D warnings` `rc=0`, all five workspace crates checked (target/xtask/xt0096/clippy-1.100.log).
- [x] **NO REGRESSION (slice a)** — 1.95.0: fmt `rc=0`, clippy `rc=0`, `cargo test -p semulith-dsp56300` 17 passed; the runner's dump on the six guests is byte-identical to HEAD's (`cmp`, dump/cmp.log); the chain's focused set runs `cargo test --all`.
- [x] **REPRODUCE / ISSUE (slice a2)** — hosted run `43633628199`, job `host (ubuntu-latest, rv64i-lab-v0)`: `gc_demo_detects_named_faults_and_refuses_unsupported_json` panicked at `crates/semulith-cli/tests/model_rv64gc.rs:11:46` on `NotFound`, the test executable under `target/debug/build/semulith-cli/<hash>/out/`; on 1.100.0 here, 529 passed, 10 failed (target/xtask/xt0097/test-1.100-before.log).
- [x] **ROOT CAUSE (slice a2)** — `cli()` in five test files joined `semulith` to `current_exe().parent().parent()`. Cargo 1.95.0 runs test executables from `target/debug/deps`, so that is `target/debug`; Cargo 1.100.0 runs them from `target/debug/build/<package>/<hash>/out/` (`grep -o 'Running tests/model_rv64gc.rs ([^)]*)' target/xtask/xt0097/test-1.100-before.log` → `…/target-1.100/debug/build/semulith-cli/da77ad3ad818cdb1/out/model_rv64gc-da77ad3ad818cdb1`), so it is `target/debug/build/semulith-cli`, while the binary stays at `target/debug/semulith`.
- [x] **FIX (slice a2)** — `cli()` runs `env!("CARGO_BIN_EXE_semulith")` in `model_rv64gc.rs`, `option_spellings.rs`, `reduce_rv64gc.rs`, `replay_rv64gc.rs`, `snapshot_rv64gc.rs` (`fix_bin_lookup.py`, which refuses unless each file holds the old helper exactly once).
- [x] **ADDRESSED (slice a2, verified)** — 1.100.0: `cargo test --all --no-fail-fast` `rc=0`, 539 passed, 0 failed (test-1.100-after.log); `cargo clippy --all-targets --all-features -- -D warnings` `rc=0`.
- [x] **NO REGRESSION (slice a2)** — 1.95.0: fmt `rc=0`, clippy `rc=0`, `cargo test -p semulith-cli` 14 passed; the chain's focused set runs `cargo test --all`; the archive move verified by `move.log`.
- [x] **FIX (slice b)** — `rust-toolchain.toml` `channel = "1.95.0"`; `.github/workflows/{rust,doctrines,portability}.yml` `RUSTUP_TOOLCHAIN=1.95.0` and `rustup toolchain install 1.95.0`; `TOOLCHAIN-PIN` (`xtask/src/check_toolchain_pin.rs`, `scripts/check_toolchain_pin.sh`, the registry, `DOCTRINE_ENFORCEMENT.md`, `docs/doctrines/governance.md`, the book).
- [x] **VERIFIED (slice b)** — `bash scripts/check_toolchain_pin.sh --self-test` → `TOOLCHAIN-PIN --self-test: 10 pass / 0 fail`; `bash scripts/check_toolchain_pin.sh` `rc=0`, `6 workflow step(s) in 3 workflow(s) name it, 2 take the Miri nightly`; the same module on HEAD's toolchain file and workflows `rc=1` with 7 floating sites (target/xtask/xt0098/head-tree.out); `cargo test -q -p xtask` 31 passed; `scripts/check_registry_mirror.sh` `REGISTRY-MIRROR: ok`.
- [ ] **ADDRESSED (slice b)** — the hosted `rust` workflow green on the pinned toolchain.
- [x] **LOCKSTEP (slices a to b)** — the tree, docs/TASK_TREE.md, the book's `working/doctrines.md`, MEMORY, CHANGELOG; `decision_the-toolchain-is-pinned.md` and its row in `docs/decisions/index/part-2.md`.

## Changelog

- `2026-11-15`: XTASK.19 slice b done — 1.95.0 pinned in `rust-toolchain.toml` and every workflow; `TOOLCHAIN-PIN` holds it; the director's push and the hosted runs remain.
- `2026-11-14`: XTASK.19 slice a2 done — the CLI's tests run the binary Cargo names for them, so Rust 1.100.0's new test layout passes all 539 tests; closed checklists to archive part 11.
- `2026-11-14`: XTASK.19 slice a done — the four loops Rust 1.100.0's clippy flags iterate their arrays; clippy 1.100.0 is clean over the workspace, and the DSP runner's dump is unchanged.
- `2026-11-10`: XTASK.18 done — the chain accepts a colon after the work-unit number, as the hook does, and its refusal says what it wants and what it got.
- `2026-11-10`: XTASK.16 done — a check skips only on a ledger-only commit, so a driver's change runs its check; the gate holds the rule to 37 controls; the focused set runs the tests. XTASK.17 opened.
- `2026-11-10`: XTASK.15 done — the commit chain and its sweep are `cargo xtask commit-unit` and `sweep-scratch`; every git drops a hook's repository variables, and the gate starts without the `xtask` package's.
- `2026-11-05`: XTASK.13 slice b6 done — the rest of GUEST-GEN's self-test judges frozen copies; six damaged states each fail by name at 400 of 400; DEF-GEN's frozen tree gains `profile.sexp`; taken at 4 of 5 features, recorded why.
- `2026-11-05`: XTASK.13 slice b5 done — the author probes' other corpus reads judge 26 frozen records; the mirror governor already names a damaged live one, so the drafted step was dropped; `scripts/live_reads.py` measures what a probe reads; seven probes' composition reads are b6.
- `2026-11-04`: XTASK.13 slice b4 done — the author probes judge a frozen owned corpus; GUEST-GEN's real check re-derives the live one; the probes' other corpus reads are b5.
- `2026-11-03`: XTASK.13 slice b3 done — the parcel author probe judges frozen copies; the author probes' owned-corpus arms and the real-run step are b4.
- `2026-11-02`: XTASK.13 slice b2 done — GUEST-GEN's base-mirror and parcel-count arms judge a frozen owner→mirror pair; the parcel author's cold and legacy arms are b3.
- `2026-10-29`: XTASK.13 slice b1 done — GUEST-GEN's census and surgical arms judge frozen mini corpora; the mirror and count arms are b2.
- `2026-10-29`: XTASK.13 slice a done — DEF-GEN's controls judge a frozen copy (scripts/fixtures/def-gen); an orphaned module fails by name.
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
- `2026-10-28`: XTASK.12 slice a — UNIT-BOOKS' quiet refusal names its missed arms (the hosted refusal on 45f970c0 said only "self-test failed"); 28 drivers next.
- `2026-10-28`: XTASK.12 slice b — every driver's quiet refusal names its missed arms (28 more drivers; 29 of 29).
- `2026-10-28`: XTASK.12 slice c — the include probe asserts the refusal's reason, not pathlib's call count (3 on Python 3.12, 1 on 3.14); the doctrines suite green under 3.12.
- `2026-10-29`: XTASK.12 done — hosted doctrines green on cefb0d84; XTASK.4 done by ruling 2 (13 scripts stay shell); open question (e) answered: XTASK.13 extends ruling 5 to the eleven fragile doctrines.
