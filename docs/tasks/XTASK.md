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
  Children: `XTASK.1` … `XTASK.7`

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

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `XTASK.6` | `active` | slice `6f`: guard the unchecked scratch allocations of `check_seam_integrity.sh` and `check_contract_freeze.sh`, whose self-tests `cd` into it (read the failure paths first, no blind probe) |
| 2 | `XTASK.4` | `active` | the remaining 13 scripts wait, each constraint recorded; `bootstrap.sh` and `check_portability.sh` are measurable offline |

## Decisions

- `2026-10-23`: the director: "Migration to xtask shall be done with extrem care, and incrementally for not
  breaking anything" (`decision_rust-native-tooling.md`).

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

- [x] slice 6a **REPRODUCE / ISSUE** — before-*.stdout/stderr: `bash scripts/check_wasm_build.sh` → `PORT-WEB: ok (workspace builds for wasm32-unknown-unknown)` rc 0; `--self-test` → `PORT-WEB --self-test: 4 pass / 0 fail`; fake `rustup` → `PORT-WEB: REFUSED — rustup target 'wasm32-unknown-unknown' is not installed, this check cannot judge.` rc 2; wasm-only flags → `PORT-WEB: REFUSED — the check does not discriminate (self-test failed).` rc 2, `--self-test` `1 pass / 3 fail`; a unix import in semulith-core → `PORT-WEB: FAIL — the workspace must build for wasm32-unknown-unknown` rc 1, `grep -c unix` 3; arm_total before = 1670.
- [x] slice 6a **ROOT CAUSE (WHY + WHERE)** — the doctrine lived only in bash (`grep -cE '(^|[; ])arm "' scripts/check_wasm_build.sh` = 4 at 557d2f56), and `arm_total` counted only the bash idioms, so a port would have dropped the claimed total with no arm removed; drivers.md: 54 drivers, 7 spine, 8 calling a pinned script, 39 free.
- [x] slice 6a **FIX** — xtask/src/check_wasm_build.rs (`grep -cE '^[[:space:]]+tally\.arm\(' xtask/src/check_wasm_build.rs` = 4); main.rs `NATIVE`, `PORTED`, dispatch; scripts/check_wasm_build.sh a three-command shim (`shasum -a 256` = 05b911439fab3af5f3234c57e9b2206f8853b27ace2dee463f53f4cfb865d3f8); `arm_total` counts a shim's module, two self-test arms.
- [x] slice 6a **ADDRESSED (verified)** — `cmp` before/after: ok stdout and stderr, native ok stdout, `--self-test` stdout and stderr, missing-target stdout and stderr, broken-self-test stderr, broken `--self-test` stdout → byte-identical, the three `self-test MISS` lines identical; host-only RED rc 1, stderr identical apart from build progress lines; shim run 0.54 s and 0.51 s against the old driver's 0.53 s; `DERIVED-COUNTS --self-test: 12 pass / 0 fail`; blind counter → `MISS: GREEN a shim's xtask arms are counted with the bash arms`, tolerant counter → `MISS: REFUSE a shim whose xtask module is missing yields no total right verdict, wrong reason`, both `11 pass / 1 fail`, restored `scripts/check_derived_counts.sh: OK`; shim RED → `scripts/check_wasm_build.sh must stay a shim of cargo xtask check-wasm-build`, restored `scripts/check_wasm_build.sh: OK`.
- [x] slice 6a **NO REGRESSION** — make-check.log `make check rc=0 in 43 s`, 493 passed, 0 failed (`cargo test -p xtask` `6 passed`); `API-DOCS: ok (5 crate(s) documented; …)`; arm_total after = 1672 and LIVE_STATUS re-derived (`COUNT DRIFT … claims '1670' … has 1672` → fixed); `ls target/doctrine-selftest | wc -l` = 0 (no scratch leaked); `cargo xtask focused` rc 0 before the commit.
- [x] slice 6a **LOCKSTEP** — LIVE_STATUS (1672 arms), docs/doctrines/evidence.md and docs/toolbox/execution.md rows, the tree (XTASK.4 constraints, XTASK.5 blocked with its options, XTASK.6 inventory and slice 6a), docs/TASK_TREE.md, CHANGELOG, MEMORY.
- [x] slice 6b **REPRODUCE / ISSUE** — before-*.stdout/stderr (bash driver): `COMMIT-PREFIX: ok (the hook refuses SEMILITH- naming SEMULITH, accepts SEMULITH-)` rc 0; `COMMIT-PREFIX --self-test: 4 pass / 0 fail`; unpinned hook rc 1 `NOT REFUSED: a SEMILITH- subject passed .githooks/commit-msg — the pin is absent or dead`; over-tight rc 1 `OVER-TIGHT: …`; missing hook rc 2 `COMMIT-PREFIX: REFUSED — .githooks/commit-msg does not exist; …`; unwritable scratch rc 2 `COMMIT-PREFIX: REFUSED — the check does not discriminate (self-test failed).`; `shasum -a 256 .githooks/commit-msg` re-checked `OK` after each swap, mode `-rwxr-xr-x`.
- [x] slice 6b **ROOT CAUSE (WHY + WHERE)** — the doctrine lived only in bash (`grep -cE '(^|[; ])arm "' scripts/check_commit_prefix.sh` = 4 at 253a0256); `grep -n "check_commit_prefix" .githooks/commit-msg` = 18, a comment only, so no hook calls the driver; PORT-WEB's private `scratch` and `combined` were the helpers a second module needs.
- [x] slice 6b **FIX** — xtask/src/check_commit_prefix.rs (`grep -cE '^[[:space:]]+tally\.arm\(' xtask/src/check_commit_prefix.rs` = 4), xtask/src/harness.rs (`scratch`, `combined`), check_wasm_build.rs on the harness, main.rs `NATIVE`/`PORTED`/dispatch; scripts/check_commit_prefix.sh a three-command shim (`shasum -a 256` = 73774026fdec58101662ea7d18b9738457c826ae7bfc2953c887809e16abfbcf); the scratch-cause lines print only under `--self-test`.
- [x] slice 6b **ADDRESSED (verified)** — `cmp` before/after through the shim: ok stdout and stderr, native ok stdout, `--self-test` stdout and stderr, unpinned/empty/over-tight/missing-hook stderr, unwritable-scratch stdout and stderr → byte-identical; PORT-WEB on the harness: ok stdout and stderr, `--self-test`, missing target, broken self-test, unwritable scratch → byte-identical, host-only RED rc 1 `grep -c unix` 3; shim RED → `scripts/check_commit_prefix.sh must stay a shim of cargo xtask check-commit-prefix`, restored `scripts/check_commit_prefix.sh: OK`.
- [x] slice 6b **NO REGRESSION** — make-check.log `make check rc=0 in 69 s`, 493 passed, 0 failed; `API-DOCS: ok (5 crate(s) documented; …)`; `DERIVED-COUNTS: ok (3 derived count claim(s) re-derived)`, arm_total 1672; `ls target/doctrine-selftest | wc -l` = 0 and no `commit-prefix.*` under target/doctrine_scratch; `cargo xtask focused` rc 0 before the commit.
- [x] slice 6b **LOCKSTEP** — docs/doctrines/governance.md row, the tree (slice 6b, frontier 6c), docs/TASK_TREE.md, CHANGELOG, MEMORY.
- [x] slice 6c **REPRODUCE / ISSUE** — before-*.stdout/stderr (bash driver, real package): `DELIVERY-PROVENANCE: ok` + `  docs/provenance/planning-package-v0.2: 20 frozen-in-place, 2 relocated re-derived; 3 live row(s) declared` rc 0; `DELIVERY-PROVENANCE --self-test: 9 pass / 0 fail`; `DRIFTED (frozen-in-place) RULES.md` with `delivered 8e7bf579156cf0d0ed07fb13f2855610fbdcbed6ffca1b7afb350342df154cae` rc 1; UNDECLARED listing `docs/ARCHITECTURE.md`, `README.md`, `ROADMAP.md`, `RULES.md`; ORPHAN listing `_b.txt`, `Alpha.txt`, `zeta.txt`; missing dispositions rc 1; no hasher `DELIVERY-PROVENANCE: REFUSED — no sha256sum or shasum on PATH; this check cannot judge.` rc 2; unwritable scratch rc 2; no package `DELIVERY-PROVENANCE: ok (no packages under docs/provenance/)` rc 0; tree digest 2d90ab8e3893e3cafe889491fdfcd2865e7d34e75dd5c56d6831d5178f4721e2 re-derived after each case.
- [x] slice 6c **ROOT CAUSE (WHY + WHERE)** — the doctrine lived only in bash (`grep -cE '(^|[; ])arm "' scripts/check_delivery_provenance.sh` = 9 at 6b59f3cb); `grep -n "check_delivery_provenance" scripts/probe_temporary_locality.py` = 156 (the preamble is read as text); `grep -n "CENSUS_RE" scripts/check_task_acceptance.sh` = 87 and `grep -n "check_gap_claims" scripts/check_seam_integrity.sh` = 249, 251, 321 (why `check_gap_claims.sh` waits).
- [x] slice 6c **FIX** — xtask/src/check_delivery_provenance.rs (`grep -cE '^[[:space:]]+tally\.arm\(' xtask/src/check_delivery_provenance.rs` = 9); main.rs `NATIVE`/`PORTED`/dispatch and the shim test's second shape; scripts/check_delivery_provenance.sh a shim with the locality preamble (`shasum -a 256` = 912546f7e201a39ed040820ca196f2a3fae3be5bfd9d0e660905e2fc19076f84).
- [x] slice 6c **ADDRESSED (verified)** — `cmp` before/after, stdout and stderr each: ok, `--self-test`, drift, undeclared, orphan, missing, no hasher, unwritable scratch, no package → byte-identical (native ok stdout too); mutant (`got != want && false`) → `DELIVERY-PROVENANCE --self-test: 7 pass / 2 fail`, `MISS: RED frozen row byte changed expected rc=1 got rc=0`, main `REFUSED — the check does not discriminate` rc 2, restored `xtask/src/check_delivery_provenance.rs: OK`; shim RED → `must stay a shim of cargo xtask check-delivery-provenance`, restored `scripts/check_delivery_provenance.sh: OK`.
- [x] slice 6c **NO REGRESSION** — make-check.log `make check rc=0 in 43 s`, 493 passed, 0 failed; `PORT-WEB: ok (workspace builds for wasm32-unknown-unknown)`; locality.log `TMP-LOCALITY: 58/58 shell sites qualified and cleaned`, `2/2 Python self-tests`, `28 unset/foreign child environments constrained`, bare-shell rc 1 (its RED arm); `SEAM-INTEGRITY: ok (1522 …)`; `API-DOCS: ok`; arm_total 1672, `DERIVED-COUNTS: ok`; `cargo xtask focused` rc 0 before the commit.
- [x] slice 6c **LOCKSTEP** — docs/doctrines/governance.md row; docs/toolbox/governance.md deliberately unchanged (`wc -c` 16302 of 16384); the tree (coupling findings, slice 6c, frontier 6d), docs/TASK_TREE.md, CHANGELOG, MEMORY.
- [x] slice 6d **REPRODUCE / ISSUE** — before-*.stdout/stderr (bash driver): `API-DOCS: ok (5 crate(s) documented; … 0 undocumented public item(s), each crate at its recorded count)` rc 0; `API-DOCS --self-test: 15 pass / 0 fail`; broken link → `crates/semulith-core/src/lib.rs:58:11  unresolved link to `nowhere_xt0008`` rc 1; rise → `semulith-verify: 1 undocumented > recorded 0; document the new item(s):` naming `crates/semulith-verify/src/run.rs:105:5`; fall → `lower the record to 0`; malformed → `malformed record row: 'semulith-core 0'` rc 2; unreadable → `unreadable record: [Errno 2] No such file or directory: 'doctrine/undocumented_items.tsv'` rc 2; ghost rows → `aaa: recorded, but not a workspace crate directory`; missing row → `xtask: no recorded count (measured 0)`; unwritable scratch → `REFUSED — the check does not discriminate` rc 2.
- [x] slice 6d **ROOT CAUSE (WHY + WHERE)** — the doctrine lived in bash with an inline Python ratchet (`grep -cE '(^|[; ])arm "' scripts/check_rustdoc.sh` = 15, `grep -n "python3 -c" scripts/check_rustdoc.sh` = 35 at 1a22c3a3); coupling.md: no other tracked script names it.
- [x] slice 6d **FIX** — xtask/src/check_rustdoc.rs (`grep -cE '^[[:space:]]+tally\.arm\(' xtask/src/check_rustdoc.rs` = 15); `locale_sorted` moved into xtask/src/harness.rs; main.rs `NATIVE`/`PORTED`/dispatch; scripts/check_rustdoc.sh a three-command shim (`shasum -a 256` = c43f24aa3dd2328383dce32bc6e6997613a7ae32d20ec09de1ec18223cf1e34e).
- [x] slice 6d **ADDRESSED (verified)** — `cmp` before/after, stdout and stderr each: ok, `--self-test`, link, rise, fall, malformed, unreadable, ghost, missing row, unwritable scratch → byte-identical (native ok stdout too); against the old script: `malformed record row: "it's\tx\ty"` and the duplicate row → byte-identical; mutant (`count > row && false`) → `API-DOCS --self-test: 14 pass / 1 fail`, `MISS: RED a rise is refused`, main `REFUSED` rc 2, restored `xtask/src/check_rustdoc.rs: OK`; shim RED → `must stay a shim of cargo xtask check-rustdoc`, restored `scripts/check_rustdoc.sh: OK`; DELIVERY-PROVENANCE ok stdout and orphan stderr on the moved helper → byte-identical.
- [x] slice 6d **NO REGRESSION** — make-check.log `make check rc=0 in 32 s`, 493 passed, 0 failed; `PORT-WEB: ok`; `API-DOCS: ok (5 crate(s) documented; …)` from the Rust check; arm_total 1672, `DERIVED-COUNTS: ok`; locality.log `TMP-LOCALITY: 57/57 shell sites qualified and cleaned`; `SEAM-INTEGRITY: ok (1528 …)`; every changed file restored (`shasum -a 256 -c` OK); `cargo xtask focused` rc 0 before the commit.
- [x] slice 6d **LOCKSTEP** — docs/doctrines/evidence.md and docs/toolbox/execution.md rows, the tree (coupling census, slice 6d, frontier 6e), docs/TASK_TREE.md, CHANGELOG, MEMORY.
- [x] slice 6e **REPRODUCE / ISSUE** — before-*.stdout/stderr (bash driver): `PUSH-RECORD: ok (the ledger is append-only; 2 entries well-formed)` rc 0; `PUSH-RECORD --self-test: 6 pass / 0 fail`; `MISSING FIELD SEMULITH-PUSH-0001: no 'Reason:'`; `BAD RANGE SEMULITH-PUSH-0001`; `NONSEQUENTIAL SEMULITH-PUSH-0003: the 2(th) entry must be SEMULITH-PUSH-0002`; `1 entry well-formed`; staged rewrite `REWRITTEN push-approvals.md`; staged append `3 entries well-formed`; unwritable scratch → the defect below (killed, `refuse rc=143`).
- [x] slice 6e **ROOT CAUSE (WHY + WHERE)** — the doctrine lived in bash with an inline Python check (`grep -cE '(^|[; ])arm "' scripts/check_push_record.sh` = 6, `grep -n "python3 -" scripts/check_push_record.sh` = 24 at 922a1dbd); the defect: `grep -n 't="$(SELFTEST_TMP)"' scripts/check_push_record.sh` unguarded, then `git -C "$t" init -q` (line 98) — `git -C ""` leaves the directory unchanged.
- [x] slice 6e **FIX** — xtask/src/check_push_record.rs (`grep -cE '^[[:space:]]+tally\.arm\(' xtask/src/check_push_record.rs` = 6; `let Ok(t) = scratch(…) else { … return false; }` before any git command); main.rs `NATIVE`/`PORTED`/dispatch; scripts/check_push_record.sh a three-command shim (`shasum -a 256` = 5b4c913fc3539f2f4af15d9fd6ee6495027862208ff1d8f339976119ad5181f0); the knowledge card and its INDEX row.
- [x] slice 6e **ADDRESSED (verified)** — `cmp` before/after, stdout and stderr each: ok, `--self-test`, missing, badrange, nonseq, single, rewritten, append → byte-identical (native ok stdout too); unwritable scratch → `PUSH-RECORD: REFUSED — the check does not discriminate (self-test failed).` rc 2 with `shasum -a 256 .git/config` 5fa9bf39d1cee284… before and after, `git diff --cached --quiet` clean, HEAD 922a1dbd; restoration after the incident: `git config user.name` → `Richard DJE`, `git config user.email` → `richard.dje@gmail.com` (global; `git config --local --list | grep -c "^user\."` = 0), index clean, `ls .git/index.lock` absent; mutant (`… && false`) → `PUSH-RECORD --self-test: 5 pass / 1 fail`, main `REFUSED` rc 2, restored `xtask/src/check_push_record.rs: OK`; shim RED → `must stay a shim of cargo xtask check-push-record`, restored `scripts/check_push_record.sh: OK`.
- [x] slice 6e **NO REGRESSION** — make-check.log `make check rc=0 in 31 s`, 493 passed, 0 failed; `PORT-WEB: ok`; `API-DOCS: ok`; arm_total 1672, `DERIVED-COUNTS: ok`; locality.log `TMP-LOCALITY: 56/56 shell sites qualified and cleaned`; `docs/push-approvals.md: OK` after every staged case; `cargo xtask focused` rc 0 before the commit.
- [x] slice 6e **LOCKSTEP** — docs/doctrines/governance.md row; docs/toolbox/governance.md unchanged (at its cap); docs/knowledge card and INDEX; the tree (slice 6e, the defect, frontier 6f), docs/TASK_TREE.md, CHANGELOG, MEMORY.

## Acceptance Checklist (leaf XTASK.7)

- [x] **ROOT CAUSE (WHY + WHERE)** — the focused set did not run API-DOCS: `git show eaa63f58:xtask/src/main.rs | sed -n '/^const FOCUSED/,/^];/p' | grep -c check_rustdoc` = 0 against 26 entries (before.stdout `focused: 0 red of 26`); documentation commits ran the check by hand, and XTASK.3's gate refusal (2026-10-23) is what the set would have caught. Resolved by `decision_focused-set-runs-api-docs.md` under the director's delegation of 2026-10-26 (`decision_four-rulings-delegated.md`).
- [x] **FIX** — xtask/src/main.rs: `FOCUSED` gains `&["bash", "scripts/check_rustdoc.sh"]` between `check_requirements.sh` and `make book` (`sed -n '/^const FOCUSED/,/^];/p' xtask/src/main.rs | grep -c check_rustdoc` = 1), the test `assert_eq!(FOCUSED.len(), 27)` (cargo-test.log `test result: ok. 6 passed; 0 failed`); docs/toolbox/execution.md row (`grep -c '27-check' docs/toolbox/execution.md` = 1); criterion 6 (disposable target for altered builds) in this tree.
- [x] **ADDRESSED (verified)** — measure-1.out (the code change, the index row still at 4/6): `focused: 1 red of 27`, `verdict lines: 25 identical, 1 differ` — the one `FRONTIER-SYNC`, `COUNT DRIFT XTASK: the index claims 4/6 leaves complete; the tree has 5/7`, this leaf's own index row, fixed; the new entry `check_rustdoc.sh` → `API-DOCS: ok (5 crate(s) documented; no broken or private intra-doc link, no invalid HTML; 0 undocumented public item(s), each crate at its recorded count)`. RED red.out — `[\`Request\`]` → `[\`Reqest\`]` at crates/semulith-core/src/env.rs:132 with `CARGO_TARGET_DIR=target/xtask/xt0012/red-target`: `focused: 1 red of 27` rc 1 in 163 s, `check_rustdoc.sh rc=1`, `API-DOCS: FAIL — the workspace's rustdoc carries link or HTML defects`, `crates/semulith-core/src/env.rs:132:45  unresolved link to \`Reqest\``; restored `shasum -a 256 crates/semulith-core/src/env.rs` = 851b0a3c15e3ab8aabf4f553b3b6af566e4c2e1dcfe54770c92014bb2a4dd913; the disposable target (182M) removed, `ls target/debug/incremental | wc -l` = 84 before and after. measure-2.out (the finished slice, nothing staged): `focused: 0 red of 27` rc 0, `verdict lines: 25 identical, 1 differ` — `SEAM-INTEGRITY: ok (1543 current tracked acceptance box(es) …)` → `(1548 …)`, the five boxes of this checklist; the one new entry `check_rustdoc.sh`.
- [x] **NO REGRESSION** — make-check.log `make check rc=0 in 49 s`, 490 passed, 0 failed; after-1: every verdict line but the index row's identical to before/, `FRONTIER-SYNC: ok (35 tree(s) mirrored by docs/TASK_TREE.md)`, `TREE-CLAIMS: ok`, `DERIVED-COUNTS: ok` once the row read 5/7; the chain's focused run on the staged tree before the commit.
- [x] **LOCKSTEP** — docs/toolbox/execution.md row (27-check); the tree (XTASK.7 node, Children `XTASK.1` … `XTASK.7`, criterion 6, the open question resolved, the changelog line), docs/TASK_TREE.md (5 of 7), CHANGELOG, MEMORY; the knowledge card's focused-set count.

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
