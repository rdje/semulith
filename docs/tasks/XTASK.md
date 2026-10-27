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
  Slice `6a` — `PORT-WEB` (`check_wasm_build.sh`, pure bash, 4 arms) becomes `cargo xtask check-wasm-build`:
  done (`2026-10-24`, `SEMULITH-XTASK-0005`; owned on clean 557d2f56; evidence target/xtask/xt0005). The
  doctrine is `xtask/src/check_wasm_build.rs`: the same preflight, four arms with the same names and reasons,
  the same verdict lines and exit statuses (0 ok, 1 fail, 2 refused); the registered script is a held shim
  (`PORTED`). Measured byte-identical against the bash driver on every path: ok, `--self-test`, a missing
  target, a self-test broken by wasm-only flags (refused), the self-test's three misses, and a real
  host-only import in `semulith-core` (FAIL naming `unix`); the run takes the same half-second. The arm total
  now counts a shim's module (`xtask/src/<name>.rs`, one `tally.arm(` per arm) and yields nothing when the
  module is missing, with two new `DERIVED-COUNTS` arms, each fired RED (a counter blind to the module; one
  tolerating its absence): 1670 → 1672 = 1670 − 4 bash arms + 4 Rust arms + 2 new. A defect owned mid-slice:
  the first fixture line contained the idiom it wrote (`x=1; arm "one"`), so the real total read 1673; the
  line is now built from pieces, so the source does not match.
  Slice `6b` — `COMMIT-PREFIX` (`check_commit_prefix.sh`, pure bash, 4 arms) becomes
  `cargo xtask check-commit-prefix`: done (`2026-10-24`, `SEMULITH-XTASK-0006`; owned on clean 253a0256;
  evidence target/xtask/xt0006). The behavioural probe of `.githooks/commit-msg` is
  `xtask/src/check_commit_prefix.rs`, with the same two synthetic subjects, four fixture hooks, findings,
  verdict lines and exit statuses (0 ok, 1 the hook does not pin, 2 refused); the registered script is a held
  shim. The scratch-directory and child-process helpers it shares with `PORT-WEB` are one module,
  `xtask/src/harness.rs`. Measured byte-identical against the bash driver with the real hook swapped and
  restored (digest and mode checked): ok, `--self-test`, an unpinned hook (NOT REFUSED), an empty hook, an
  over-tight hook (OVER-TIGHT), a missing hook (refused), an unwritable scratch directory (refused);
  `PORT-WEB` re-measured on the shared helpers, byte-identical again. One intended difference, in a path no
  gate reads: with an unwritable scratch directory, `--self-test` names the cause (`cannot create a scratch
  directory`) where bash ran its arms against missing fixture files and printed a count (`2 pass / 2 fail`,
  `PORT-WEB` `0 pass / 4 fail`); the exit status (1) and the main run's refusal are the same. A defect owned
  mid-slice: both modules printed that cause during the main run's silent self-test, one stderr line more
  than bash; now only `--self-test` prints it. Arm total unchanged at 1672 (4 bash arms became 4 Rust arms).
  Coupling found before `6c` (6b59f3cb): `check_gap_claims.sh` waits — `check_task_acceptance.sh` (line 87)
  and `check_seam_integrity.sh` (`vocabulary_agreement`, lines 249, 251, 321) read its `CENSUS_RE` line as
  text, so a shim would break them until those readers move. `check_delivery_provenance.sh` is named by
  `probe_temporary_locality.py` (line 156), which requires its `# All scratch,` preamble (`mkdir -p` and
  `export TMPDIR` on `target/tmp`); the probe is not pinned, so the shim keeps that preamble instead.
  Slice `6c` — `DELIVERY-PROVENANCE` (`check_delivery_provenance.sh`, pure bash, 9 arms) becomes
  `cargo xtask check-delivery-provenance`: done (`2026-10-24`, `SEMULITH-XTASK-0007`; owned on clean 6b59f3cb;
  evidence target/xtask/xt0007). The doctrine is `xtask/src/check_delivery_provenance.rs`, its nine arms with
  the same names and reasons. Kept from bash on purpose: hashing through `sha256sum` or `shasum -a 256` chosen
  as `command -v` chose (no new crate; the same refusal when neither exists); the locale's collation through
  `sort` (measured: en_US.UTF-8 lists `_b.txt`, `Alpha.txt`, `zeta.txt` and `docs/ARCHITECTURE.md` before
  `README.md`, which byte order would not); `comm -23` as a multiset difference; bash's split of a disposition
  row (the third field keeps the rest, one trailing separator after a single field dropped — probed in bash
  on five row shapes). The shim keeps the `# All scratch,` preamble `probe_temporary_locality.py` reads, and the
  shim test accepts exactly that second shape. Measured byte-identical against the bash driver on the real
  package (20 frozen-in-place, 2 relocated, 3 live; restored by a tree digest after each case): ok,
  `--self-test`, a drifted frozen row, undeclared rows, orphan dispositions, a missing `dispositions.tsv`, no
  hasher on `PATH`, an unwritable scratch directory (refused) and no package at all. A drift-blind mutant of
  the module is caught by its own arms (`7 pass / 2 fail`, main run refused). Found while drafting: a Unix-only
  mode check would have broken the workspace's wasm32 build, which `PORT-WEB` exists to catch; it is
  `cfg(unix)`. `docs/toolbox/governance.md` keeps its row (the command still works through the shim): the file
  is 82 B under its 16,384 B cap, so it is partitioned before the next governance row, not squeezed.
  Coupling census before `6d` (1a22c3a3; target/xtask/xt0007/coupling.md): of the 36 unported free drivers,
  25 are named by another tracked script — some read as bytes (`probe_handoff_census.py`), copied into fixture
  repositories and run there (`qualify_orientation_indexes.py`, the README-routes self-test), or grepped for a
  constant (`CENSUS_RE`), where a shim cannot serve; others only in a generator's hint or a history note — and
  11 are named by none. A fixture-run driver needs a design first (the Rust check run against a fixture's root,
  the binary reached without the fixture's cargo configuration), so the uncoupled 11 go first.
  Slice `6d` — `API-DOCS` (`check_rustdoc.sh`, named by none, 15 arms, an inline Python ratchet) becomes
  `cargo xtask check-rustdoc`: done (`2026-10-24`, `SEMULITH-XTASK-0008`; owned on clean 1a22c3a3; evidence
  target/xtask/xt0008). The rustdoc check in Rust, `xtask/src/check_rustdoc.rs`: the doc build with the three
  denied lints, the awk defect listing (`error:` lines but "could not document", their `-->` location, at most
  60), the Python ratchet with its messages — Python's `repr` of a malformed row (double quotes when the row
  holds an apostrophe), its `OSError` text (`[Errno 2] No such file or directory: '…'`), its list of stray
  locations — and the fifteen arms, the inherited-`RUSTDOCFLAGS` arm now guarding the order in which the
  check sets the variable over an inherited one. The crate directories keep the glob's locale order, through
  `locale_sorted`, now in `harness.rs` (moved from slice 6c's module; `DELIVERY-PROVENANCE` re-measured on it,
  byte-identical). Measured byte-identical against the bash driver on twelve paths: ok, `--self-test`, a
  broken link in `semulith-core`, a rise (a field's doc removed in `semulith-verify`), a fall, a malformed row,
  an apostrophe-and-tab row, a duplicate row, an unreadable record, two ghost rows, a missing row and an
  unwritable scratch directory. A rise-blind mutant is caught (`14 pass / 1 fail`, main run refused).
  Slice `6e` — `PUSH-RECORD` (`check_push_record.sh`, named by none, 6 arms, an inline Python check) becomes
  `cargo xtask check-push-record`: done (`2026-10-24`, `SEMULITH-XTASK-0009`; owned on clean 922a1dbd;
  evidence target/xtask/xt0009). The ledger's shape and append-only property are `xtask/src/check_push_record.rs`;
  the Python's two regular expressions are matched by hand (no new crate; ASCII digits for `\d`), and the
  self-test's scratch repository runs the same git commands in the same order, so its arms see the same
  accumulated fixture (`git checkout -- file` after `git add` restores from the index, as in bash). Measured
  byte-identical against the bash driver on nine paths, the real ledger staged and unstaged for two of them:
  ok, `--self-test`, a missing field, a bad range, a renumbered entry, a single entry ("1 entry"), a staged
  rewrite (REWRITTEN), a staged pure append ("3 entries"); a rewrite-blind mutant is caught (`5 pass / 1 fail`,
  main run refused). **A defect owned mid-slice, found the hard way:** the bash driver's self-test never
  checked its scratch allocation, so with `target/doctrine-selftest` unwritable (a failure-injection run) it
  carried on with `t=""`, and `git -C ""` acts in the caller's directory: it ran `git init`, `git config
  user.email t@t`, `git config user.name t`, `git add -A` and `git commit -m base` on the real repository,
  output discarded by the main run. Stopped about ten minutes in, during the real pre-commit gate: the process
  tree killed, children included; no commit made (HEAD `922a1dbd`), no `index.lock`; the appended `[user]`
  section (last in `.git/config`) removed, the identity again the global one every commit carries; the index
  unstaged to clean; `.git/hooks` untouched. The probe was fired without first reading the path it drives —
  the lesson is the card `docs/knowledge/an-empty-scratch-path-falls-back-to-the-repository.md`. The Rust
  module stops when `scratch` fails, before any git command: with the directory unwritable it refuses (rc 2)
  and `.git/config`, the index and HEAD are unchanged (measured). Two other drivers carry the fallback form
  unguarded: `check_seam_integrity.sh` (`cd "$t" && git init -q . && git add leaf.md`) and
  `check_contract_freeze.sh` (`cd "$t" && judge "$t"`) — owned as slice `6f`, read before any probe.
  Slice `6f` — **every bash self-test checks its scratch allocation**: done (`2026-10-26`,
  `SEMULITH-XTASK-0012`; owned on clean f8f3a549; evidence target/xtask/xt0010). The form was the scaffold's, not
  two drivers': `grep -lF 't="$(SELFTEST_TMP)"' scripts/*.sh | wc -l` = 32 drivers on f8f3a549, every
  allocation inside `self_test()` and none checked — 19 bare, 13 with a same-line `; mkdir -p "$t/…"`
  (`check_requirements.sh:709` among them). The reading 6e asked for, widened to `ln -s`
  (`grep -nE 'git -C "\$t"|cd "\$t"|ln -s'`), found 14 fallback-form lines in 6 drivers: `cd "$t"` ×9
  (`check_contract_freeze.sh` six, `check_seam_integrity.sh` three, one `git init -q . && git add leaf.md`),
  `ln -s` ×5 (the real `scripts/` and `schema/` linked into fixtures, two archive links, one relative); no
  `rm -rf "$t"/*`. Each allocation now reads `t="$(SELFTEST_TMP)" && [ -n "$t" ] && [ -d "$t" ] || { echo
  "<DOCTRINE> self-test: cannot create a scratch directory under target/doctrine-selftest" >&2; return 1; }`
  — the Rust modules' wording (`harness.rs`) — with any same-line tail kept after it, applied by one script over
  the census (`guard_scratch2.py`: both forms, exactly one match per driver asserted, the doctrine name read
  from the driver's own tally line). Measured before and after on the same clean HEAD for 31 drivers
  (`PROFILE-CONSISTENCY`'s main path is the gate's ~50-min self-test; its before and after lines are the two
  chain gates' PROJECT-SPECIFIC logs): ok and `--self-test`, stdout, stderr and rc each — 186 of 186 files
  byte-identical (before2 in 923 s). The failure path, guarded, for all 32: `target/doctrine-selftest`
  mode 500, with `.git/config`'s digest, HEAD, the index content and the `schema/*.sexp` count snapshotted before
  and verified after — every main run `REFUSED — the check does not discriminate (self-test failed).` rc 2 (stdout empty; the 30 that discard the self-test's output say nothing more, `check_guest_gen.sh` and `check_profile_consistency.sh` keep their log and show the cause), every `--self-test` run rc 1 naming it (`mktemp: failed to create directory via template …: Permission denied`, then `<DOCTRINE> self-test: cannot create a scratch directory under target/doctrine-selftest`); `.git/config` 5fa9bf39d1cee284…, HEAD f8f3a549, index content 9bcbf7e2e0659714… and 25 schemas identical before and after, the directory restored to 755, nothing left under it. No arm added or removed, no pinned or spine script touched, no build
  under altered sources (criterion 6 not engaged). Next: slice `6g`, `FIXTURE-FINGERPRINT`
  (`check_fixture_fingerprints.sh`, named by none, 7 arms, inline Python on the standard library only) — the
  smallest of the 9 uncoupled drivers that remain.
  Slice `6g` — `FIXTURE-FINGERPRINT` (`check_fixture_fingerprints.sh`, named by none, 7 arms, an inline Python scan)
  becomes `cargo xtask check-fixture-fingerprints`: done (`2026-10-26`, `SEMULITH-XTASK-0013`; owned on clean dc2d2878;
  evidence target/xtask/xt0013). The rule — every tracked JSON/JSONL object carrying both `path` and `sha256` names
  a file that exists, resolved against the record's directory, whose content hashes to that value — is
  `xtask/src/check_fixture_fingerprints.rs`: the `os.walk` order (records in name order, then subdirectories in
  listing order, `.git` and `target` never entered, a link to a directory never followed), the root-relative
  exclusions, Python `dict` semantics for duplicate keys (the last value at the first key's position), a JSON
  reader written here (no new crate) that reports a malformed record with Python's `json` messages and positions
  — `Expecting ',' delimiter: line 1 column 22 (char 21)`, the BOM, trailing commas, `Invalid \escape`, each of
  22 shapes unit-tested — and hashing through the harness's external hasher (`sha256sum`, else `shasum -a 256`),
  moved from `check_delivery_provenance.rs` into `harness.rs` as `locale_sorted` was in 6d. Measured byte-identical
  against the bash driver on the real tree: ok (`1 pinned fingerprint(s) re-derived`, 0.37 s both), `--self-test`
  (`7 pass / 0 fail`), a drifted pin, a malformed pin, a missing file, an unparseable `.json` and an unparseable
  `.jsonl` line (each a tracked file altered and restored digest-verified), and the unwritable-scratch refusal; and
  on a scratch tree of fifteen findings of every shape (links, excluded subtrees, duplicate keys, a `.jsonl` with
  blank and broken lines) with a relative and an absolute root. Three differences, each by design: the `--self-test`
  refusal names the cause without `mktemp`'s own line; without `sha256sum`/`shasum` on `PATH` the port refuses where
  the script hashed with Python; without `python3` the port judges where the script refused. A drift-blind mutant is
  caught (`5 pass / 2 fail`, main run refused), built only into a disposable target directory (criterion 6).
  `DELIVERY-PROVENANCE` re-measured on the moved hasher: ok, `--self-test` and no-hasher paths byte-identical to
  6c's. The same unit sharded CHANGELOG.md (the 18 oldest entries to docs/changelog/shard-0415.md, 64,497 →
  47,718 B, boundary bytes as ef340a9c left them). Next: slice `6h`, `FACT-OWNERSHIP` (`check_fact_ownership.sh`,
  named by none, 8 arms, Python on `glob` and `re` only) — 8 uncoupled drivers remain.
  Slice `6h` — `FACT-OWNERSHIP` (`check_fact_ownership.sh`, named by none, 10 arms — the bash idiom count saw 8,
  missing the two `armp` arms — an inline Python check) becomes `cargo xtask check-fact-ownership`: done
  (`2026-10-26`, `SEMULITH-XTASK-0014`; owned on clean c163dd96; evidence target/xtask/xt0014). The
  no-duplicated-fact rule (`MODEL-METHOD.7`) is `xtask/src/check_fact_ownership.rs`: the registry's rows and
  their six findings, the `sorted(set)` listing printed as Python's `repr` prints it, the corpus census's ten
  restatement pairs with same-unit pairing for `profiles/*/` patterns and the two checkable directions for
  cross-family ones, and the script's `glob` patterns expanded by a reader written here (no new crate) with
  Python's rules — a `*` never matches a hidden name, a family `dir/` is present when it holds a `.sexp` at
  any depth, a literal segment must exist. Python's `splitlines`/`strip` moved from 6g's module into
  `harness.rs` (`FIXTURE-FINGERPRINT` re-measured byte-identical on them). Measured byte-identical against
  the bash driver on the real tree: ok (`74 fact kind(s): one owner each, every mirror governed`),
  `--self-test` (`10 pass / 0 fail`), an unregistered governor, an ungoverned mirror, a missing owner, an
  unnamed pair, two owners, a malformed row (refused), an empty registry (refused), the registry gone
  (refused), the unwritable-scratch refusal — each altered tracked file restored digest-verified. Two
  differences by design: the `--self-test` refusal names the cause without `mktemp`'s own line; without
  `python3` the port judges where the script's self-test could not run. A governor-blind mutant is caught
  (`9 pass / 1 fail`, main run refused), built only into a disposable target directory. The arm total moves
  1675 → 1677 and LIVE_STATUS is re-derived: the module's ten `tally.arm(` restore the honest count. Next:
  slice `6i`, `REGISTRY-MIRROR` (`check_registry_mirror.sh`, named by none, 13 arms, Python on `re` only) — 7
  uncoupled drivers remain.
  Slice `6i` — `REGISTRY-MIRROR` (`check_registry_mirror.sh`, named by none, 13 arms, an inline Python check)
  becomes `cargo xtask check-registry-mirror`: done (`2026-10-26`, `SEMULITH-XTASK-0015`; owned on clean 39150ac2;
  evidence target/xtask/xt0015). The two registries' quoted triples, the two human mirrors and the
  `docs/doctrines/` family union (written as the script's `cat` wrote it, byte-identical) with their five
  comparisons — coverage, phantom rows, the project section, executable paths, the "<N> checks run today"
  sentence spelled or in digits — are `xtask/src/check_registry_mirror.rs`, the script's three regular
  expressions matched by hand (no new crate) and unit-tested against Python's own matches. Measured
  byte-identical against the bash driver on the real tree: ok (`3 document(s) mirror the registry`),
  `--self-test` (`13 pass / 0 fail`), a registered id without its row, a phantom row, a drifted and an
  unreadable count sentence, a family union missing a project row, a registered check made non-executable, a
  missing mirror, an emptied universal registry (refused), the universal driver absent (`ok (no driver yet)`),
  the unwritable-scratch refusal — each altered tracked file restored digest-verified (the mode change by
  `chmod`). Two differences by design: the `--self-test` refusal names the cause without `mktemp`'s own line;
  without `python3` the port judges where the script refused. A phantom-blind mutant is caught (`12 pass / 1
  fail`, main run refused), built only into a disposable target directory; the arm total is unchanged (13 bash
  arms out, 13 `tally.arm(` in). Found while porting: clippy's arity cap (`too_many_arguments`) refused an
  eight-argument arm helper, so the tally carries the fixture registries. Next: slice `6j`, a design — the six
  uncoupled drivers that remain (`check_m_vectors.sh`, `check_unit_composition.sh`, `check_scope_coverage.sh`,
  `check_citation_quotes.sh`, `check_extraction.sh`, `check_exercise_coverage.sh`) all read the corpus through
  the pinned Python readers (`sexp.py`, `records_sexp.py`) or load a project module, so a port needs a Rust
  S-expression reader measured equal to the pinned one on the corpus first, as its own slice.
  Slice 6j (`2026-10-27`, `SEMULITH-XTASK-0018`; on clean 8ebbf2dc, the one tooling slice after features 6–10): the
  reader is `xtask/src/sexp.rs` (649 lines; `decision_rust-sexp-reader.md`) — the pinned grammar, refusal messages, line
  numbers and Python-shaped I/O errors, the pinned reader's twenty self-test arms re-asserted as a unit test, and the
  equality held permanently by `the_corpus_reads_as_the_pinned_reader_reads_it`: every tracked `.sexp` file (367) dumped
  through both readers in one `python3 -I` process and required byte-identical (an absent comparator fails, never skips).
  `cargo xtask sexp <file>` mirrors `scripts/sexp.py <file>`: 390 cases (the corpus, 21 fixtures, the usage path), 389
  identical; the one difference is the documented limit — a 41-digit integer Python holds and `i128` refuses (rc 0 vs 1),
  absent from the corpus by the test's own word. Nothing ported, no shim, `scripts/sexp.py` untouched (a pinned input of the
  M case's manifest). clippy's `--fix` rewrote one manual range check and rustfmt three expressions before the chain. Next:
  slice `6k` — the first consumer, `check_exercise_coverage.sh` (reads through `children`/`read_file`/`field` directly), after
  the next five feature units.
  Slice 6l (`2026-10-27`, `SEMULITH-XTASK-0020`; on clean bbf9a326, taken out of turn — no feature leaf unblocked, recorded in
  the Decisions): the schema validator is Rust — `xtask/src/schema.rs` (2097 lines; `decision_rust-schema-validator.md`):
  the pinned kernel (constructs, fields, facets, operators), the validation walk and every refusal text byte for byte,
  the 51 self-test arms re-asserted (`cargo xtask check-sexp-schema --self-test` prints the pinned tool's 52 lines
  byte-identically), and the equality held permanently by `the_corpus_validates_as_the_pinned_validator_validates_it`
  over every (file, schema) pair the project validates (315 today, one `python3 -I` comparator process; an absent
  comparator fails). The command line mirrors the pinned tool: 315 pairs identical in stdout, stderr and exit status.
  The one limit: regex facets are an anchored hand-written subset (31 distinct corpus patterns, all inside it); a
  pattern outside it is refused by name at schema load. Nothing ported, no shim, `scripts/check_sexp_schema.py` untouched
  (an M-manifest input). In tree: `cargo test -p xtask` `test result: ok. 15 passed` (3 s); clippy at deny-warnings rc=0 (clean after its `--fix` simplified one boolean expression). Next: slice
  `6m` — the encoding-disjointness judge (`check_encoding_disjoint.py`: 496 lines, validates through this module first).
  Slice 6m (`2026-10-27`, `SEMULITH-XTASK-0021`; on clean eef7f048, taken out of turn — no feature leaf unblocked): the
  encoding-disjointness judge is Rust — `xtask/src/disjoint.rs` (796 lines: the instruction rows' masks and values,
  fragment loading on the `.sexp` and riscv-opcodes routes, schema validation through `schema.rs` before judging, the slot
  rules, exhaustive collisions, declared specializations, the pseudo rules, and the command line's texts) with the one
  composition resolver moved to `xtask/src/composition.rs` (90 lines), shared by the exercise-coverage census and the
  judge. `cargo xtask check-encoding-disjoint <fragment…> | --self-test` mirrors `python3 scripts/check_encoding_disjoint.py`:
  the 17 arms re-asserted in-process with the pinned labels, fixtures and needles (`--self-test` stdout byte-identical), and
  the judge over every tracked encoding and `definitions/riscv` document — 23: 12 compose, 1 rejects (`zicntr.sexp`, a
  pseudo-only fragment judged alone), 10 semantics files refused as not fragments — identical in stdout, stderr and exit
  status (`23 identical, 0 differ`); `EXERCISE-COVERAGE` through the shared resolver stays byte-identical to its 6k baseline.
  Nothing ported, no shim: the pinned judge is a library and CLI no bash driver wraps, and it stays (an M-manifest input).
  In tree: `cargo test -p xtask` `test result: ok. 15 passed`; clippy at deny-warnings rc=0 (clean after its `--fix` of two findings and two type aliases for the judge's tuple types). Next: slice `6n` — `check_unit_composition.sh`
  (49 lines of inline Python over this judge, 6 bash arms) behind a held shim.
  Slice 6n (`2026-10-27`, `SEMULITH-XTASK-0022`; on clean 51615ac1, taken out of turn — no feature leaf unblocked): `UNIT-COMPOSITION`
  is Rust — `xtask/src/check_unit_composition.rs` (338 lines) ports the driver's 49-line inline Python line for line over
  the Rust judge, validator and resolver (6m, 6l, 6k): every tracked `profiles/*/encoding.sexp` REFUSED by name when unreadable,
  REJECTED with its collision, duplicate-name and pseudo-problem counts, or composing (partial when it declares slots); the shell
  wrapper's verdict lines and exit statuses the same; the nine bash arms (the leaf said six — the count was wrong, the
  script has nine) are nine `tally.arm(` calls, the arm total unchanged; `scripts/check_unit_composition.sh` a shim of
  `cargo xtask check-unit-composition`. Measured in a disposable draft crate: the self-test `9 pass / 0 fail` with stdout
  byte-identical to the bash driver's, the real tree's stdout and stderr byte-identical (`UNIT-COMPOSITION: ok (3 unit
  composition(s) decided)`), and nine scratch fixture trees — green, partial, slots claiming completeness, partial with nothing
  unbound, an undeclared compose field, a ghost fragment, a collision, a ghost pseudo, no document — 9 identical, 0 differ in stdout, stderr
  and exit status. In tree: `cargo test -p xtask` `test result: ok. 15 passed`; clippy at deny-warnings rc=0 (clean on the first run). The three-unit port towards
  `UNIT-COMPOSITION` closes; the uncoupled drivers left are `check_m_vectors.sh`, `check_scope_coverage.sh`,
  `check_citation_quotes.sh` and `check_extraction.sh` (the last three read through `records_sexp` as well — its port is
  the next design question). Next: slice `6o` — `records_sexp.py` measured equal, the way 6j measured `sexp.py`.
  Slice 6o (`2026-10-27`, `SEMULITH-XTASK-0023`; on clean 5f55db54, taken out of turn — no feature leaf unblocked): the record
  mapping is Rust — `xtask/src/records.rs` (1076 lines) ports `scripts/records_sexp.py`, the single owner of the JSON key ↔
  field correspondence: the four record shapes (requirement, obligation, unit, category-need) read into ordered JSON-shaped
  records, the typed parameter values (`int`, `str`, `true`, `false`, `null`, `ints`, `strs`), the refusals for values the corpus
  does not write, and the writer (`dict_to_form`, the closed string escapes, one form per line) — together with the catalogue
  reader's include expansion (`record_catalog.text`: cycle, duplicate-part, unreadable-part, include-family, catalogue-root,
  part-form, include-shape, include-path and include-escape refusals), so a composed obligation catalogue reads as the pinned
  tool reads it. Measured in a disposable draft crate over every tracked catalogue the mapping serves (16: the RECORD-SCHEMA
  map's requirements, obligations, units and category-needs files plus the obligation parts): the JSON dumps through both
  readers 16 catalogues, 16 identical, 0 differ; the three catalogues the pinned renderer round-trips byte for byte (`netboard-lab-v0/requirements.sexp`,
  `netboard-lab-v0/contract-obligations.sexp`, `rv64gc-lab-v0/contract-v1.obligations.sexp`) round-trip here too; the other
  thirteen differ from their files through either renderer (comments and layout the compact renderer drops) — the pinned tool's
  own behaviour, measured. Held permanently by two unit tests (`the_catalogues_read_as_the_pinned_mapping_reads_them`, one
  `python3 -I` comparator process; `the_renderer_round_trips_the_rendered_catalogues`); `cargo xtask records <catalogue>
  [--dump]` is the by-hand surface. Nothing ported, nothing shimmed: `scripts/records_sexp.py` is a pinned input of the M case's
  manifest and its callers still run it. In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at deny-warnings rc=0 (clean on the first in-tree run). Of the four
  uncoupled drivers, two read records as dictionaries (`check_scope_coverage.sh`, `check_extraction.sh`); the 6n text above said
  three — `check_citation_quotes.sh` reads through `sexp` only (corrected here, §15). Next: slice `6p` — `check_scope_coverage.sh`
  over the Rust mapping, behind a held shim.
  Slice 6p (`2026-10-27`, `SEMULITH-XTASK-0024`; on clean cc60342a, taken out of turn — no feature leaf unblocked): `SCOPE-COVERAGE`
  is Rust — `xtask/src/check_scope_coverage.rs` (354 lines) ports the driver's 68-line inline Python line for line over the
  Rust record mapping (6o): every tracked `materials/units.sexp` read as records, each unit's declared `requires` against the
  census beside the registry — no census, an unreadable registry or census, an undeclared scope, a required category with no
  row, one `missing`, one with a disposition the gate cannot judge — with the shell wrapper's verdict lines and exit statuses;
  the ten bash arms are ten `tally.arm(` calls, the arm total unchanged; `scripts/check_scope_coverage.sh` a shim of
  `cargo xtask check-scope-coverage`. Measured in a disposable draft crate: the self-test `10 pass / 0 fail` with stdout and
  stderr byte-identical to the bash driver's, the real tree's stdout and stderr byte-identical (`SCOPE-COVERAGE: ok (6 unit(s)
  may code — every required category covered)`), and 11 scratch fixture repositories — green, no registry, no census, a required category missing, one with no census row, an undeclared scope, an unknown disposition, an unreadable registry, an unreadable census, a non-record registry form, a later census row replacing an earlier one — 11 identical, 0 differ in stdout,
  stderr and exit status (the unreadable and non-record states hold the Rust reader's and mapping's refusal texts equal to the
  Python exceptions' as well). In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at deny-warnings rc=0 (clean on the first in-tree run). Three uncoupled
  drivers remain: `check_extraction.sh` (the last to read records as dictionaries), `check_citation_quotes.sh`,
  `check_m_vectors.sh`. Next: slice `6q` — `check_extraction.sh` over the Rust mapping, behind a held shim.
  Slice 6q (`2026-10-27`, `SEMULITH-XTASK-0025`; on clean 8918b099, taken out of turn — no feature leaf unblocked): `EXTRACTION`'s
  driver is Rust — `xtask/src/check_extraction.rs` (499 lines) ports the driver's 33-line inline Python line for line: every
  tracked `profiles/*/profile.sexp`'s unit judged by `scripts/check_extraction.py`, the pinned Python judge (566 lines over
  `check_semantics`, `dossier_sexp`, `records_sexp`, `riscv_asm`), spawned exactly as the driver spawned it and NOT ported — its
  CANNOT JUDGE / INSUFFICIENT / per-unit lines and the shell wrapper's verdicts and exit statuses the same; the eleven bash arms
  are eleven `tally.arm(` calls (the arm total unchanged) and the judge's seventeen controls are scored once beside them, as the
  script scored them; the fixtures' requirement and obligation records are written through the Rust record mapping
  (`records::dump`, 6o) where the script wrote them through `records_sexp.dump` — the mapping's writer in a doctrine for the
  first time; `scripts/check_extraction.sh` a shim of `cargo xtask check-extraction`. Measured in a disposable draft crate:
  the self-test `12 pass / 0 fail` with stdout and stderr byte-identical to the bash driver's, the real tree's stdout and
  stderr byte-identical (`EXTRACTION: ok (5 unit(s) sufficient — P1-LAB may cite this)`), and 8 scratch fixture
  repositories (every pinned script, the schemas and the definitions copied in) — the real corpus, no units, an insufficient
  unit, a unit the judge cannot read, a sibling-crate declaration contradicted by an encoding, the device-model and
  profile-resolution legs green, a device register without a reset, an obligation checked one way — 8 identical, 0 differ in stdout,
  stderr and exit status. In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at deny-warnings rc=0 (clean on the first in-tree run). The first in-tree run was
  refused by `DERIVED-COUNTS` at 1691 arms (§15 — I had read the counter's `tally.arm(` rule and not its bash `score "` rule): the
  bash driver's one `score` is counted, the module's `tally.score(` was not; `scripts/check_derived_counts.sh` now counts a shim
  module's `tally.score(` beside its `tally.arm(`, as it counts the bash idiom (its fixture carries one; `12 pass / 0 fail`), and
  the arm total holds at 1692. Containment, in the same
  unit: this leaf stood at 125,454 B against the 131,072 B per-part ceiling — the acceptance rows of the closed slices 6a–6o
  (44128 B, one contiguous span) moved verbatim into `docs/tasks/archive/XTASK-1.md` (the a43b mechanism: SHA256 in the part's
  table, found once, one pointer left), the live leaf 81406 B after the move. Two uncoupled drivers remain:
  `check_citation_quotes.sh` (slice 6r) and `check_m_vectors.sh`.
  Slice 6r (`2026-10-27`, `SEMULITH-XTASK-0026`; on clean dff02433, taken out of turn — no feature leaf unblocked): `CITATION-QUOTES`'s
  driver is Rust — `xtask/src/check_citation_quotes.rs` (445 lines) ports the bash driver line for line: the pinned Python tool
  `scripts/check_citation_quotes.py` spawned exactly as the driver spawned it and NOT ported, the driver's two inline Python
  controls — the source-availability probe (the NAMED SKIP route) and the altered-bytes identity control — run verbatim through
  `python3 -` as string constants, the NAMED SKIP, FAIL and REFUSED lines and exit statuses the same (the 6q frontier row said
  "over the Rust reader": the driver reads nothing itself — corrected here); the twenty-two bash arms are twenty-two `tally.arm(`
  calls, the arm total unchanged; `scripts/check_citation_quotes.sh` a shim of `cargo xtask check-citation-quotes`. Measured in a
  disposable draft crate: the self-test `22 pass / 0 fail` with stdout and stderr byte-identical to the bash driver's, the real
  tree's stdout and stderr byte-identical (`CITATION-QUOTES: 115 attributed quote(s) judged (R1 1, R2 108, R3 3, R4 3); 0
  finding(s); …`), and 5 scratch fixture repositories (every pinned script copied in) — the pinned pages absent (NAMED
  SKIP), a sources manifest that cannot be read (measured: ALSO the NAMED SKIP — §9 below), a synthetic pinned page with a quote in
  its section (judged green), one with a quote the page never says (FAIL, to stderr as the script's `>&2` sent it — the first
  draft printed it to stdout, caught by this state), a page whose bytes differ from the pin (evidence REFUSED) — 5 identical, 0 differ in
  stdout, stderr and exit status. **§9 finding, the pinned driver's and reproduced faithfully:** the availability probe exits 1 for
  "pages absent" and Python exits 1 for an uncaught exception — a manifest the reader refuses with an exception outside the
  probe's `except` tuple crashes with a traceback on stderr and the driver reads the 1 as absence: NAMED SKIP, exit 0, a green
  gate. Not fixed here (the port is held byte-identical to the script); recorded as an open question for the doctrine's owner.
  The knowledge card for it is drafted (target/xtask/xt0026/card.md) and NOT added: `docs/knowledge/` stands at 130,763 B of its
  131,072 B aggregate ceiling (41 files; README-ROUTES refused the first run at 133,410 B) — the directory's containment is the
  next maintenance unit, and the card lands with it. In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at deny-warnings rc=0 (clean on the first in-tree run). CHANGELOG.md,
  at 63257 B against its 65,536 B ceiling, is sharded in this unit (`scripts/shard_history.py --max-bytes 49152`: `docs/changelog/shard-0417.md`
  sealed, the head 48775 B before this entry). One uncoupled driver remains: `check_m_vectors.sh` — slice `6s`.
  Slice 6s (`2026-10-27`, `SEMULITH-XTASK-0027`; on clean f3b3e612, taken out of turn — no feature leaf unblocked): `M-VECTORS`'s
  driver is Rust — `xtask/src/check_m_vectors.rs` ( lines) ports the bash driver line for line: the inline Python judge
  (the generator loaded as a module, its table and its reference judged on an operand set the table does not use) runs verbatim
  through `python3 -` as a string constant extracted from the script, NOT ported; the controls run over copies of the generator
  and a table each copy generated, the script's four `sed` mutations as the same first-occurrence replacements and the table's
  overflow line replaced once; judge first, controls only for a pass, the same verdict lines and exit statuses; the six bash arms
  are six `tally.arm(` calls, the arm total unchanged; `scripts/check_m_vectors.sh` a shim of `cargo xtask check-m-vectors`.
  Measured in a disposable draft crate: the self-test `6 pass / 0 fail` with stdout and stderr byte-identical to the bash driver's,
  the real tree's stdout and stderr byte-identical (`M-VECTORS: ok (4485 vectors in sync with the generator; the reference judged
  on 151x48 operand pairs at both widths; 0 finding(s))`), and 5 scratch fixture repositories (every pinned script and the
  table copied in) — in sync, a hand-edited table, the table missing, the generator truncated, a reference that floors — 5 identical, 0 differ
  in stdout, stderr and exit status (the first draft passed the live paths absolute and the DRIFT line printed them — the script
  passes them relative; three states caught it, §15). In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at deny-warnings rc=0 (clean on the first in-tree run).
  The uncoupled drivers are all ported (6k–6s). Left in the registry (re-measured by the drivers' own text — the first census matched `.sexp` filenames and over-counted the pinned callers): fourteen free drivers whose judges are separate Python scripts spawned by path or inline Python without pinned imports (`check_book_index.sh`, `check_board_verdict.sh`, `check_board_gen.sh`, `check_platform_gen.sh`, `check_state_gen.sh`, `check_interaction_matrix.sh`, `check_unit_books.sh`, `check_tree_claims.sh`, `check_frontier_sync.sh`, `check_task_history.sh`, `check_changelog_shards.sh`, `check_readme_routes.sh`, `check_derived_counts.sh`, `check_artifact_cleanup.sh`; `check_seam_integrity.sh` waits on `check_gap_claims.sh`'s readers and the spine's `check_doctrines.sh` is held NEUTRAL), and twelve whose own text imports or runs a pinned module — the three on `sexp` alone (`check_semantics_corpus.sh`, `check_source_format.sh`, `check_upstream_index.sh`) portable over `sexp.rs` as 6k was. Next: slice `6t` — `check_book_index.sh` behind a held shim.
  Slice 6t (`2026-10-27`, `SEMULITH-XTASK-0028`; on clean a010ecdb, taken out of turn — no feature leaf unblocked): `BOOK-INDEX`'s
  driver is Rust — `xtask/src/check_book_index.rs` (308 lines) ports the bash driver line for line: the generator
  `scripts/gen_book_index.py` spawned exactly as the driver spawned it (`--check` over the book, the glossary and the committed
  index), NOT ported; the status reading the same — 1 with the generator's named `DRIFT` line is the FAIL, every other failure
  a refusal, launch failures and unknown exits included; the controls over a copy of the real book (an index emitted, a faithful
  regeneration in sync, a hand-edited index, the chapters emptied, a chapter the SUMMARY names removed, the SUMMARY removed) and
  the judge's four status readings; the ten bash arms are ten `tally.arm(` calls (one arm's "no output" form kept), the arm
  total unchanged; `scripts/check_book_index.sh` a shim of `cargo xtask check-book-index`. Measured in a disposable draft crate:
  the self-test `10 pass / 0 fail` with stdout and stderr byte-identical to the bash driver's, the real tree's stdout and stderr
  byte-identical (`BOOK-INDEX: ok (docs/book/src/index.md matches the book, 40 table rows)`), and 5 scratch fixture
  repositories (every pinned script, the book and the glossary copied in) — green, a hand-edited index, a chapter missing, the
  chapters emptied, no SUMMARY — 5 identical, 0 differ in stdout, stderr and exit status. In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at
  deny-warnings rc=0 (clean on the first in-tree run).
  The first chain was refused by `PROFILE-CONSISTENCY`'s self-test: the `group-cleanup` mutation of the matched-GPR collector
  probe survived (`25 tests / 0 failures`) while fixture repositories and draft builds ran beside the gate; alone on the idle
  machine the mutation is caught three runs of three (rc 1, `25 tests / 1 failures`) — a load-sensitive control, recorded for
  the doctrine's owner (§9; no card while `docs/knowledge/` sits at its ceiling, see 6r-b); the chain re-ran on an idle machine.
  Next: slice `6u` — `check_board_verdict.sh` behind a held shim (its judge `board_verdict.py` spawned as before).
  Slice 6u (`2026-10-27`, `SEMULITH-XTASK-0029`; on clean f229ae89, taken out of turn — no feature leaf unblocked): `BOARD-VERDICT`'s
  driver is Rust — `xtask/src/check_board_verdict.rs` (246 lines) ports the bash driver line for line: the judge
  `scripts/board_verdict.py` spawned exactly as the driver spawned it for every tracked `profiles/*/board.sexp` (the glob's locale
  order kept), NOT ported; the controls over scratch copies of the real board with the script's five text mutations (an answer
  removed, an answer to a ghost, an obligation answered twice, a `satisfies` edge to a ghost, a guarantee's line removed), the same
  verdict lines and exit statuses; the six bash arms are six `tally.arm(` calls, the arm total unchanged;
  `scripts/check_board_verdict.sh` a shim of `cargo xtask check-board-verdict`. Measured in a disposable draft crate: the self-test
  `6 pass / 0 fail` with stdout and stderr byte-identical to the bash driver's, the real tree's stdout and stderr byte-identical
  (`BOARD-VERDICT: ok (1 board(s) — every CPU assumption discharged, every satisfies edge resolved, every composition disposition
  bound)`), and 5 scratch fixture repositories (every pinned script, the profiles, schemas, definitions and materials copied
  in — the judge reads the composed dossiers, so a board alone refuses) — one board, no board, two boards, the real board rejected,
  one of two rejected (FAIL by name) — 5 identical, 0 differ in stdout, stderr and exit status. §9, the script's and reproduced faithfully: the
  controls copy the LIVE board, so a corpus whose live board is rejected reads as a check that does not discriminate — REFUSED,
  exit 2, never FAIL by name (the `no board` and `rejected` states); an open question for the doctrine's owner beside 6r's. In
  tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at deny-warnings rc=0 (clean on the first in-tree run). Next: slice `6v` — `check_board_gen.sh` behind a held
  shim (its generator `gen_board.py` spawned as before).
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
| 1 | `XTASK.6` | `active` | slice `6v`: `check_board_gen.sh` behind a held shim — the board's generator spawned as before; taken out of turn while every feature leaf waits on a ruling |
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
- (6r, `2026-10-27`) `CITATION-QUOTES`'s availability probe exits 1 for "pages absent" and Python exits 1 for an uncaught exception, so a sources manifest the reader refuses outside the probe's `except` tuple reads as absence — NAMED SKIP, exit 0 (measured in the 6r fixture `manifest-unreadable`; the card is drafted in target/xtask/xt0026/card.md and waits for `docs/knowledge/`'s containment — the directory is at 130,763 of 131,072 B). The port reproduces it; the doctrine's owner decides whether the probe should refuse (exit 2) on any exception — a one-line change to the script, re-measured through the shim.
- (6u, `2026-10-27`) `BOARD-VERDICT`'s controls copy the LIVE board (`profiles/netboard-lab-v0`) and expect it ACCEPTED, so a corpus whose live board is rejected makes the check refuse as non-discriminating (exit 2) instead of failing by name (exit 1) — measured in the 6u fixtures `no-board` and `rejected`. The port reproduces it; the doctrine's owner decides whether the controls should run over a frozen fixture board instead.

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
- [x] slice 6p **REPRODUCE / ISSUE** — before/ (bash driver at cc60342a; target/xtask/xt0024/before/): `SCOPE-COVERAGE: ok (6 unit(s) may code — every required category covered)` rc 0, stderr empty; `SCOPE-COVERAGE --self-test: 10 pass / 0 fail`; `grep -c 'arm "' scripts/check_scope_coverage.sh` = 10.
- [x] slice 6p **ROOT CAUSE (WHY + WHERE)** — the doctrine lived in bash around a 68-line inline Python block importing `records_sexp` and `sexp` (`grep -c 'import records_sexp' scripts/check_scope_coverage.sh` = 1); until 6o there was no Rust record mapping to port it onto without a second owner of the field correspondence.
- [x] slice 6p **FIX** — xtask/src/check_scope_coverage.rs (`shasum -a 256` = c06112909eb7aaea49aded81738aa3b52c3ad189596a8166e43c8d3ded99b6b4; `wc -l` = 354; `grep -cE '^[[:space:]]+tally\.arm\('` = 10); main.rs doc bullet, `mod`, `NATIVE`, `PORTED`, dispatch; scripts/check_scope_coverage.sh a shim (`exec cargo xtask check-scope-coverage "$@"`).
- [x] slice 6p **ADDRESSED (verified)** — the draft binary against before/: `cmp after/selftest.out before/selftest.out` rc=0, `cmp after/real.out before/real.out` rc=0, stderr identical both; 11 scratch fixture repositories (target/xtask/xt0024/red/summary.txt): `RED/GREEN paths: 11 identical, 0 differ` — stdout, stderr and rc each.
- [x] slice 6p **NO REGRESSION** — `cargo test -p xtask` → `test result: ok. 17 passed` (the shim test holds the new shim to one command); `cargo clippy -p xtask --all-targets -- -D warnings` rc=0 (clean on the first in-tree run); `cargo fmt -p xtask -- --check` rc=0; `bash scripts/check_scope_coverage.sh` through the shim → the same `ok (6 unit(s) may code — every required category covered)` line; `bash scripts/check_derived_counts.sh` → ok (10 bash arms out, 10 `tally.arm(` in).
- [x] slice 6p **LOCKSTEP** — docs/toolbox rows unchanged (the command still answers through the shim); the tree (slice 6p, frontier 6q, the Decisions bullet), docs/TASK_TREE.md, CHANGELOG, MEMORY.
- [x] slice 6q **REPRODUCE / ISSUE** — before/ (bash driver at 8918b099; target/xtask/xt0025/before/): `EXTRACTION: ok (5 unit(s) sufficient — P1-LAB may cite this)` rc 0, stderr empty; `EXTRACTION --self-test: 12 pass / 0 fail`; `grep -c 'arm "' scripts/check_extraction.sh` = 11 (plus one `score` of the judge's `17 pass / 0 fail`); `wc -c docs/tasks/XTASK.md` = 125454 against the 131072 B ceiling.
- [x] slice 6q **ROOT CAUSE (WHY + WHERE)** — the driver lived in bash around a 33-line inline Python block spawning `scripts/check_extraction.py` per unit, its fixtures written through `records_sexp.dump` (`grep -c 'import records_sexp' scripts/check_extraction.sh` = 3); until 6o the fixtures had no Rust writer. The leaf grew by one slice's rows and paragraph per unit with no closed span moved since the tree opened.
- [x] slice 6q **FIX** — xtask/src/check_extraction.rs (`shasum -a 256` = 665b89cd42b889a31564359db5377ce01c476247d3b7ef9e8dde5cb0c7d4e55e; `wc -l` = 499; `grep -cE '^[[:space:]]+tally\.arm\('` = 11); main.rs doc bullet, `mod`, `NATIVE`, `PORTED`, dispatch; scripts/check_extraction.sh a shim (`exec cargo xtask check-extraction "$@"`); scripts/check_derived_counts.sh counts `tally.score(` in a shim's module (`DERIVED-COUNTS --self-test: 12 pass / 0 fail`); docs/tasks/archive/XTASK-1.md (`wc -c` = 45079; one span, SHA256 `473efb2129b4dfcf63ff154e49258093f3e1ee378d5d4986e3687b4b9eae07bc`) with one pointer in this leaf.
- [x] slice 6q **ADDRESSED (verified)** — the draft binary against before/: `cmp after/selftest.out before/selftest.out` rc=0, `cmp after/real.out before/real.out` rc=0, stderr identical both; 8 fixture repositories (target/xtask/xt0025/red/summary.txt): `RED/GREEN paths: 8 identical, 0 differ` — stdout, stderr and rc each; the moved span's SHA256 found once in the part's table (`grep -c` = 1) and its rows absent from the live leaf (`grep -c 'slice 6a \*\*' docs/tasks/XTASK.md` = 0).
- [x] slice 6q **NO REGRESSION** — `cargo test -p xtask` → `test result: ok. 17 passed` (the shim test holds the new shim to one command); `cargo clippy -p xtask --all-targets -- -D warnings` rc=0 (clean on the first in-tree run); `cargo fmt -p xtask -- --check` rc=0; `bash scripts/check_extraction.sh` through the shim → the same `ok (5 unit(s) sufficient — P1-LAB may cite this)` line; `bash scripts/check_derived_counts.sh` → ok (11 bash arms + 1 `score` out, 11 `tally.arm(` + 1 `tally.score(` in; 1692 holds); `wc -c docs/tasks/XTASK.md` after the move = 81406 (49666 B under the ceiling before this slice's own rows).
- [x] slice 6q **LOCKSTEP** — docs/toolbox rows unchanged (the command still answers through the shim); the tree (slice 6q, frontier 6r, the Decisions bullet), the archive part and its pointer, docs/TASK_TREE.md, CHANGELOG, MEMORY.
- [x] slice 6r **REPRODUCE / ISSUE** — before/ (bash driver at dff02433; target/xtask/xt0026/before/): `CITATION-QUOTES: 115 attributed quote(s) judged (R1 1, R2 108, R3 3, R4 3); 0 finding(s); 86 unattributed (counted, never judged); …` rc 0, stderr empty; `CITATION-QUOTES --self-test: 22 pass / 0 fail`; `grep -c 'arm "' scripts/check_citation_quotes.sh` = 22; `wc -c CHANGELOG.md` = 63257 against the 65536 B ceiling.
- [x] slice 6r **ROOT CAUSE (WHY + WHERE)** — the driver lived in bash around the tool's invocations and two inline Python controls (`grep -c 'python3 -' scripts/check_citation_quotes.sh` = 2); the tool itself (`wc -l scripts/check_citation_quotes.py` = 337, over `check_citations`) is the judge and stays pinned Python. CHANGELOG.md grows by one entry per unit; its last shard was cut at AC-0085.
- [x] slice 6r **FIX** — xtask/src/check_citation_quotes.rs (`shasum -a 256` = 3700a19e17e19cd693bb8fe833aea96552270b6799b0ef8726913d11b5386e4d; `wc -l` = 445; `grep -cE '^[[:space:]]+tally\.arm\('` = 22); main.rs doc bullet, `mod`, `NATIVE`, `PORTED`, dispatch; scripts/check_citation_quotes.sh a shim (`exec cargo xtask check-citation-quotes "$@"`); CHANGELOG.md sharded (`docs/changelog/shard-0417.md`; `wc -c CHANGELOG.md` = 48775 after the cut, before this entry).
- [x] slice 6r **ADDRESSED (verified)** — the draft binary against before/: `cmp after/selftest.out before/selftest.out` rc=0, `cmp after/real.out before/real.out` rc=0, stderr identical both; 5 fixture repositories (target/xtask/xt0026/red/summary.txt): `RED/GREEN paths: 5 identical, 0 differ` — stdout, stderr and rc each.
- [x] slice 6r **NO REGRESSION** — `cargo test -p xtask` → `test result: ok. 17 passed` (the shim test holds the new shim to one command); `cargo clippy -p xtask --all-targets -- -D warnings` rc=0 (clean on the first in-tree run); `cargo fmt -p xtask -- --check` rc=0; `bash scripts/check_citation_quotes.sh` through the shim → the same `115 attributed quote(s) judged` line; `bash scripts/check_derived_counts.sh` → ok (22 bash arms out, 22 `tally.arm(` in; 1692 holds); the history check over the new shard → ok.
- [x] slice 6r **LOCKSTEP** — docs/toolbox rows unchanged (the command still answers through the shim); the tree (slice 6r, frontier 6s, the Decisions bullet, the 6q frontier wording corrected, the §9 open question; the knowledge card deferred — `docs/knowledge/` at its aggregate ceiling, its containment the next maintenance unit), docs/TASK_TREE.md, CHANGELOG (sharded, then the entry), MEMORY.
- [x] slice 6s **REPRODUCE / ISSUE** — before/ (bash driver at f3b3e612; target/xtask/xt0027/before/): `M-VECTORS: ok (4485 vectors in sync with the generator; the reference judged on 151x48 operand pairs at both widths; 0 finding(s))` rc 0, stderr empty; `M-VECTORS --self-test: 6 pass / 0 fail`; `grep -c 'arm "' scripts/check_m_vectors.sh` = 6.
- [x] slice 6s **ROOT CAUSE (WHY + WHERE)** — the driver lived in bash around a 47-line inline Python judge (`grep -c 'python3 - ' scripts/check_m_vectors.sh` = 1) loading `scripts/gen_m_vectors.py` as a module — the reference is Python and stays so; the controls were four `sed` mutations of generator copies.
- [x] slice 6s **FIX** — xtask/src/check_m_vectors.rs (`shasum -a 256` = ; `wc -l` = ; `grep -cE '^[[:space:]]+tally\.arm\('` = 6); main.rs doc bullet, `mod`, `NATIVE`, `PORTED`, dispatch; scripts/check_m_vectors.sh a shim (`exec cargo xtask check-m-vectors "$@"`).
- [x] slice 6s **ADDRESSED (verified)** — the draft binary against before/: `cmp after/selftest.out before/selftest.out` rc=0, `cmp after/real.out before/real.out` rc=0, stderr identical both; 5 fixture repositories (target/xtask/xt0027/red/summary.txt): `RED/GREEN paths: 5 identical, 0 differ` — stdout, stderr and rc each (the first draft: 3 differ, the DRIFT line's path — fixed, re-measured).
- [x] slice 6s **NO REGRESSION** — `cargo test -p xtask` → `test result: ok. 17 passed` (the shim test holds the new shim to one command); `cargo clippy -p xtask --all-targets -- -D warnings` rc=0 (clean on the first in-tree run); `cargo fmt -p xtask -- --check` rc=0; `bash scripts/check_m_vectors.sh` through the shim → the same `4485 vectors in sync` line; `bash scripts/check_derived_counts.sh` → ok (6 bash arms out, 6 `tally.arm(` in; 1692 holds).
- [x] slice 6s **LOCKSTEP** — docs/toolbox rows unchanged (the command still answers through the shim); the tree (slice 6s, the frontier, the Decisions bullet), docs/TASK_TREE.md, CHANGELOG, MEMORY.
- [x] slice 6t **REPRODUCE / ISSUE** — before/ (bash driver at a010ecdb; target/xtask/xt0028/before/): `BOOK-INDEX: ok (docs/book/src/index.md matches the book, 40 table rows)` rc 0, stderr empty; `BOOK-INDEX --self-test: 10 pass / 0 fail`; `grep -c 'arm "' scripts/check_book_index.sh` = 10.
- [x] slice 6t **ROOT CAUSE (WHY + WHERE)** — the driver lived in bash around `scripts/gen_book_index.py --check` (`grep -c gen_book_index.py scripts/check_book_index.sh` = 9) and a status-reading function (`grep -c judge_generator` = 6); the generator is the judge and stays pinned Python, spawned as before.
- [x] slice 6t **FIX** — xtask/src/check_book_index.rs (`shasum -a 256` = b89db20eac461d2f78320cb2c04870f4ed1a1f291c728040f8fea36897894b5c; `wc -l` = 308; `grep -cE '^[[:space:]]+tally\.arm\('` = 10); main.rs doc bullet, `mod`, `NATIVE`, `PORTED`, dispatch; scripts/check_book_index.sh a shim (`exec cargo xtask check-book-index "$@"`).
- [x] slice 6t **ADDRESSED (verified)** — the draft binary against before/: `cmp after/selftest.out before/selftest.out` rc=0, `cmp after/real.out before/real.out` rc=0, stderr identical both; 5 fixture repositories (target/xtask/xt0028/red/summary.txt): `RED/GREEN paths: 5 identical, 0 differ` — stdout, stderr and rc each.
- [x] slice 6t **NO REGRESSION** — `cargo test -p xtask` → `test result: ok. 17 passed` (the shim test holds the new shim to one command); `cargo clippy -p xtask --all-targets -- -D warnings` rc=0 (clean on the first in-tree run); `cargo fmt -p xtask -- --check` rc=0; `bash scripts/check_book_index.sh` through the shim → the same `40 table rows` line; `bash scripts/check_derived_counts.sh` → ok (10 bash arms out, 10 `tally.arm(` in; 1692 holds).
- [x] slice 6t **LOCKSTEP** — docs/toolbox rows unchanged (the command still answers through the shim); the tree (slice 6t, frontier 6u, the Decisions bullet), docs/TASK_TREE.md, CHANGELOG, MEMORY.
- [x] slice 6u **REPRODUCE / ISSUE** — before/ (bash driver at f229ae89; target/xtask/xt0029/before/): `BOARD-VERDICT: ok (1 board(s) — every CPU assumption discharged, every satisfies edge resolved, every composition disposition bound)` rc 0, stderr empty; `BOARD-VERDICT --self-test: 6 pass / 0 fail`; `grep -c 'arm "' scripts/check_board_verdict.sh` = 6.
- [x] slice 6u **ROOT CAUSE (WHY + WHERE)** — the driver lived in bash around `scripts/board_verdict.py` (`grep -c board_verdict.py scripts/check_board_verdict.sh` = 8) with five inline Python text mutations of the board copy (`grep -c 'python3 -' scripts/check_board_verdict.sh` = 5); the judge stays pinned Python, spawned as before.
- [x] slice 6u **FIX** — xtask/src/check_board_verdict.rs (`shasum -a 256` = 7ac17a0ecf1a3fbd60f5fd694105ca9f4909b28819a6d28ea1b0553b016f96bc; `wc -l` = 246; `grep -cE '^[[:space:]]+tally\.arm\('` = 6); main.rs doc bullet, `mod`, `NATIVE`, `PORTED`, dispatch; scripts/check_board_verdict.sh a shim (`exec cargo xtask check-board-verdict "$@"`).
- [x] slice 6u **ADDRESSED (verified)** — the draft binary against before/: `cmp after/selftest.out before/selftest.out` rc=0, `cmp after/real.out before/real.out` rc=0, stderr identical both; 5 fixture repositories (target/xtask/xt0029/red/summary.txt): `RED/GREEN paths: 5 identical, 0 differ` — stdout, stderr and rc each (the first fixture set copied the board alone: every state REFUSED on both sides — identical and uninformative; the corpus copied in, the states speak).
- [x] slice 6u **NO REGRESSION** — `cargo test -p xtask` → `test result: ok. 17 passed` (the shim test holds the new shim to one command); `cargo clippy -p xtask --all-targets -- -D warnings` rc=0 (clean on the first in-tree run); `cargo fmt -p xtask -- --check` rc=0; `bash scripts/check_board_verdict.sh` through the shim → the same `1 board(s)` line; `bash scripts/check_derived_counts.sh` → ok (6 bash arms out, 6 `tally.arm(` in; 1692 holds).
- [x] slice 6u **LOCKSTEP** — docs/toolbox rows unchanged (the command still answers through the shim); the tree (slice 6u, frontier 6v, the Decisions bullet, the §9 open question), docs/TASK_TREE.md, CHANGELOG, MEMORY.

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
