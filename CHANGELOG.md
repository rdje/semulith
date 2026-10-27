# CHANGELOG.md

## SEMULITH-XTASK-0016 (leaf XTASK.8 slices a–c) — the commit gate from 52–56 min to 6.8 min

XTASK.8, opened on the director's instruction that a fifty-minute gate is not acceptable: the same checks, the same verdict lines, the same refusals, only the order of execution changes. The censuses first: PROFILE-CONSISTENCY's self-test is 45 of the gate's minutes — 2746 s (45.8 min) alone and serial on an idle machine, 51 fixture arms 2.7 s in total and 1114 probe invocations, each a distinct argv, 2730 s of it — the heaviest script probe_matched_gpr_unit_evaluation.py at 11 s × 54, the longest single invocation probe_div_method.py 47 s; the census's serial sum 3253 s (54 min) (census under load: PROFILE-CONSISTENCY 2687 s, GUEST-GEN 201 s, RECORD-SCHEMA 97 s, ARTIFACT-COHORT 48 s, the rest ≤ 40 s) agrees with the 52–56 min (56, 52, 52 and 55 min) lived. Then `check_doctrines.project.sh` runs its 41 checks through a bounded pool — the cargo-invoking ones in a single serial lane beside it, because cargo re-uplifts a binary by copy on every run and two concurrent runs of one binary race, as the chain's own gate showed — and reports them in registry order (stderr byte-identical to the serial loop at HEAD on a stub registry of red, green and missing checks; `DOCTRINE_JOBS=1` restores the serial run), and PROFILE-CONSISTENCY's self-test prefetches its probe invocations in parallel through `scripts/doctrine_prefetch.py`, answering each arm from the record through a `python3` shadow inside the self-test (an unrecorded argv or a program on stdin runs live; `PROFILE_CONSISTENCY_PREFETCH=0` is the control; eight unit controls green) — `--self-test` output identical, 2746 s (45.8 min) → 447 s (7.5 min: 5 s recording, ~350 s parallel, the rest answering; 0 misses; 24 jobs no faster than 12 — CPU-bound). The pool exposed a latent race in `scripts/artifact_cargo.py` — on macOS `killpg` on a group whose only member is an exited, unreaped leader returns EPERM, which `_stop` did not tolerate — fixed with a 24th Cargo test and its seam `stop-zombie`. The chain gained a guard against an empty commit message, which had cost one full gate. Slice d, the docs-only path, follows with its decision record.

## SEMULITH-P4-0299 (leaf P4-SYSTEM.15 slice b) — the M, A and C suites join the GC campaign

P4-SYSTEM.15 slice b, feature 3 of 5: the pinned riscv-arch-test commit's M, Zaamo, Zalrsc and Zca suites join the external campaign over the GC model. The sparse clone gained their paths at the unchanged pin and `fetch_act4.sh` counts each suite there; `run_act4_campaign.py` takes `--suites` (default I, so rv64i's command lines and record are unchanged), lists every suite it ran in the record and refuses a partial `--record`; the record schema admits `<Suite>-<mnemonic>-<nn>.S`. The campaign: 118 tests, 39,568 signature slots, `118 pass / 0 fail`, every signature equal to the Sail-derived one, spike agreeing as the control; the 51 I rows equal slice a's. gate.sexp's external evidence statement names the suites run and, with their reasons, the ones that have not: F and D (their own DUT configuration), the Misalign suites (the environment's trap handler the DUT pieces do not instantiate, against a profile that traps misaligned data accesses).

## SEMULITH-P4-0298 (leaf P4-SYSTEM.15 slice a) — the external RV64I suite over the GC model

P4-SYSTEM.15 slice a, feature 2 of 5 under the director's ratio (`decision_alternate-port-and-features.md`, amended to five features per tooling slice): the pinned riscv-arch-test RV64I campaign now runs against any unit — `scripts/run_act4_campaign.py --profile rv64gc-lab-v0` drives the GC model, Sail with the unit's override and spike with the unit's ISA/privilege strings, with the unit's own DUT pieces under `profiles/rv64gc-lab-v0/act4/` — and records `profiles/rv64gc-lab-v0/act4.sexp` (51 tests, 17,017 signature slots, `51 pass / 0 fail`), declared in gate.sexp as the G-REGRESSION `external` evidence; the GS report's regression axis moves to 3 of 5 kinds evidenced (M/A/F/D/C suites, workload and validator-mutation remain, as the open row says). A defect owned mid-slice: `semulith run --profile=rv64gc-lab-v0 --trace-stores` accepted the flag and printed no store — the GC branch returned before the store trace; the GC run now records every successful store at the environment boundary, and the same test on both models gives byte-identical store traces. rv64i's command lines and record are unchanged.

## SEMULITH-P4-0297 (leaf P4-SYSTEM.14 a42bc) — the first qualified experiment record: G-TRACE evidenced

a42bc: the first project feature unit under the director's ruling of 2026-10-26 to alternate the Rust tooling port with project work (`decision_alternate-port-and-features.md`). Qualification of a dossier experiment record is now a computed result in one place, `credit_records.dossier_qualification`: a verification-bearing record is qualified exactly when a CURRENT credit record names its case and the record is the case's measured record, form for form; PROFILE-CONSISTENCY calls it where its unconditional `UNQUALIFIED EXPERIMENT VERIFICATION` refusal stood and prints the reasons otherwise. The credited M case's measured record becomes the rv64gc dossier's one experiment (the owner stays under evidence/; the gate refuses the day the two differ) and gate.sexp declares it as the G-TRACE experiment evidence, the G-TRACE open row retiring. Measured: 0 graph findings and 21 of 21 pins matched before the act; after it the gate's dossier judgement is clean, two RED controls refuse an uncredited id and a drifted record, the GS report moves G-TRACE to green (open axes 6 → 5), and status, policy and the three real-tree probes are unchanged. A new probe with six tests and three seams joins the gate's self-test. The eight earlier Sail experiments stay prose: history until re-run as records.

## SEMULITH-XTASK-0015 (leaf XTASK.6 slice 6i) — REGISTRY-MIRROR is `cargo xtask check-registry-mirror`

XTASK.6 slice 6i: the `REGISTRY-MIRROR` doctrine — `DOCTRINE_ENFORCEMENT.md`, the mdBook doctrines chapter and the `docs/doctrines/` family union list exactly what the two registries register, every registered check present and executable, the "<N> checks run today" sentence true — moved from bash with an inline Python check to `xtask/src/check_registry_mirror.rs`, its three regular expressions matched by hand (no new crate) and the union file written as the script's `cat` wrote it (byte-identical). Measured byte-identical against the bash driver on twelve real-tree paths — ok, `--self-test`, a missing row, a phantom row, a drifted and an unreadable count, a family union missing a row, a non-executable check, a missing mirror, an emptied registry, the universal driver absent, the unwritable-scratch refusal — each altered file restored digest-verified; two differences by design (the self-test refusal without `mktemp`'s line; no `python3` judges where the script refused). A phantom-blind mutant is caught, built only into a disposable target; the arm total is unchanged. The six uncoupled drivers that remain all read the corpus through the pinned Python S-expression readers, so slice 6j is a design: a Rust reader measured equal to `sexp.py` on the corpus.

## SEMULITH-XTASK-0014 (leaf XTASK.6 slice 6h) — FACT-OWNERSHIP is `cargo xtask check-fact-ownership`

XTASK.6 slice 6h: the `FACT-OWNERSHIP` doctrine — one owner per fact kind in `doctrine/fact_ownership.tsv`, every mirror governed by a registered doctrine, every corpus restatement pair named — moved from bash with an inline Python check to `xtask/src/check_fact_ownership.rs`: the six row findings, the same-unit and cross-family census over the ten enumerated pairs, Python's `repr` for the two-owners listing, and the script's `glob` patterns expanded by a reader written in the module (no new crate) with Python's rules; the Python string helpers from 6g moved into `harness.rs` (`FIXTURE-FINGERPRINT` re-measured byte-identical on them). Measured byte-identical against the bash driver on eleven real-tree paths — ok, `--self-test`, an unregistered governor, an ungoverned mirror, a missing owner, an unnamed pair, two owners, a malformed row, an empty registry, the registry gone, the unwritable-scratch refusal — each altered file restored digest-verified; two differences by design (the self-test refusal without `mktemp`'s line; no `python3` judges where the script could not). A governor-blind mutant is caught, built only into a disposable target. The derived arm total moves 1675 → 1677: the bash idiom count had missed the driver's two `armp` arms, and the module's ten `tally.arm(` restore the honest count, LIVE_STATUS re-derived.

## SEMULITH-XTASK-0013 (leaf XTASK.6 slice 6g) — FIXTURE-FINGERPRINT is `cargo xtask check-fixture-fingerprints`; CHANGELOG.md sharded

XTASK.6 slice 6g: the `FIXTURE-FINGERPRINT` doctrine — every tracked JSON/JSONL object carrying both `path` and `sha256` names a file that still hashes to that value — moved from bash with an inline Python scan to `xtask/src/check_fixture_fingerprints.rs`: the same walk order and exclusions, Python `dict` semantics for duplicate keys, a JSON reader written in the module (no new crate) that reports a malformed record with Python's `json` messages and positions (22 shapes unit-tested), and hashing through the external hasher now shared in `harness.rs` (moved out of `DELIVERY-PROVENANCE`, which re-measured byte-identical). Measured byte-identical against the bash driver on the real tree — ok, `--self-test`, a drifted, a malformed and a missing pin, an unparseable `.json` and `.jsonl`, the unwritable-scratch refusal, each altered file restored digest-verified — and on a fifteen-finding scratch tree; three differences by design (the self-test refusal without `mktemp`'s line; no hasher on `PATH` refuses where Python hashed; no `python3` judges where the script refused). A drift-blind mutant is caught, built only into a disposable target. The same unit cut the 18 oldest CHANGELOG entries into `docs/changelog/shard-0415.md` (64,497 → 47,718 B) and records the measured finding on `ARTIFACT-CLEANUP.29` in its tree: the recorded orphan class cannot tell a live crate-hash directory from an orphan one, and the `.bin`-only scope covers 64 % of the bytes; three options wait for the ruling.

## SEMULITH-XTASK-0012 (leaf XTASK.6 slice 6f) — every bash self-test checks its scratch allocation

XTASK.6 slice 6f: the unguarded `t="$(SELFTEST_TMP)"` that let `git -C ""` act on the real repository in 6e was not two drivers' form but the scaffold's — 32 drivers, every allocation unchecked, 19 bare and 13 with a same-line `mkdir -p`; the reading widened to `ln -s` found 14 fallback-form lines (`cd "$t"`, links to the real `scripts/` and `schema/`) in 6 of them. One script guards all 32 with the Rust modules' wording (`cannot create a scratch directory under target/doctrine-selftest`), the self-test returning before any command. Measured on the same clean HEAD: ok and `--self-test` byte-identical for the 31 drivers whose main path is not the gate's own self-test (186 of 186 files); the guarded failure path for all 32 with `.git/config`, HEAD, the index and `schema/` verified unchanged. No arm, pinned or spine file touched; no build under altered sources. Slice 6g is `FIXTURE-FINGERPRINT`.

## SEMULITH-XTASK-0011 (leaf XTASK.7) — `cargo xtask focused` runs API-DOCS; the set is 27 checks

XTASK.7: the focused set gains `bash scripts/check_rustdoc.sh` between `check_requirements.sh` and `make book` (`decision_focused-set-runs-api-docs.md`, under the director's delegation of 2026-10-26); the test holds the set to 27. Measured on the real tree: `0 red of 26` → `0 red of 27`, 25 of the 26 earlier verdict lines identical and the one difference `SEAM-INTEGRITY`'s box count (1543 → 1548, this leaf's own five acceptance rows), one new `API-DOCS: ok (5 crate(s) documented …)`; RED: one broken intra-doc link in `semulith-core` makes the run `1 red of 27` naming the lint and the line, the file restored byte-identical, the altered source built only into a disposable target directory that the slice removed — the new leaf-wide criterion 6, from `decision_orphan-incremental-sessions.md`. Documentation commits no longer run the check by hand.

## SEMULITH-XTASK-0010 (leaf XTASK.5) — `check-examples` stays in the product CLI; XTASK.5 closed by decision

XTASK.5: closed without a code change by `decision_check-examples-stays-in-the-cli.md`, under the director's delegation of 2026-10-26 (`decision_four-rulings-delegated.md`). The command validates the frozen records bundle and presents its report — the CLI's architectural role (`docs/ARCHITECTURE.md` §4) — so it was never development-only tooling and the goal's premise already holds; moving it would have turned the G1 report's criterion 3 unmet unless the pinned `gate_report.py` changed, a planned capture of the retained M case spent for no product gain. The blocker row and the frontier's blocked note are removed; `XTASK` stands at 4 of 6 leaves done, frontier `XTASK.6` slice `6f`. Docs only.

## SEMULITH-P4-0296 (leaf P4-SYSTEM.14 a42az) — the crediting act, under the director's delegation; five decision records

a42az: the director delegated the four open rulings on 2026-10-26 (`decision_four-rulings-delegated.md`, one record per ruling). The first credit record, `CR-GC-M-1`, signed `authority review` under it, credits `REQ-GC-M` on the retained m-forms case (25 witnesses, ten legs satisfied) as `implemented` and nothing more; the recorded status moves with it, the GS report is regenerated and two model-book chapters updated. Rehearsed on a smoke root with two RED controls (status left behind → drift; a moved pin → lapsed), then measured on the real tree: 47 planned, 1 implemented, 1 credit current, 0 drift. Two defects owned: the gate's record-schema loop had no branch for `credits.sexp` and handed it to the pinned reader (now read through `credit_records`, three arms, fired on the real tree); the first arms deleted the tracked `schema/credits.sexp` through the fixture's link to the real schema directory (caught by the facet probe's inventory, isolated, restored from git, the arms corrected, the lesson carded). Decided and recorded for their own leaves: `check-examples` stays in the CLI (`XTASK.5` closes), the focused set runs API-DOCS (`XTASK.7`), orphan incremental sessions get a disposable target directory now and a recorded class (`ARTIFACT-CLEANUP.29`). The gate's self-test then refused: three `PROFILE-CONSISTENCY` arms pin the real tree's state (two pending cases, `credited` false, a `derived-status` mutation count of 2) and were re-predicted from the measured tree (one pending, credited by `CR-GC-M-1`, 36), none loosened; the moved-pin branch, exercised with two restored pin moves, now predicts the lapsed record as the one finding; the next act runs the three probes before its chain (carded).

## SEMULITH-AC-0084 (leaf ARTIFACT-CLEANUP.27) — the fourth recurring cleanup through the supported act

.27: at 70 h, on a clean tree with `handoff: OK`, the four acts ran in target/artifact-cleanup/AC0084 (log inside): 253 candidates planned, 6 captured Cargo incremental outputs (15,766,335 B) strictly selected and removed by the guarded core under a fresh census, residue 0, journal `recorded-complete`/`verified`, `--inspect` confirming; 20,071 retained files kept. The unrecorded population grew from 67 files to 247 (770,724,553 B; 83 incremental sessions, each in a crate-hash directory with no live session) across 18 gated commits, so the .25 open question's deferral ends: the sessions come from workspace builds under altered sources or flags (the gate's mutation copies, the XTASK slices' RED measurements), and three options are recorded for the director. The record is overwritten; `.28` is due after 2026-10-27T08:50Z.

## SEMULITH-XTASK-0009 (leaf XTASK.6 slice 6e) — PUSH-RECORD is `cargo xtask check-push-record`; an unguarded scratch path owned

XTASK.6 slice 6e: the `PUSH-RECORD` doctrine — the push-approval ledger is append-only and every entry well-formed — moved from bash with an inline Python check to `xtask/src/check_push_record.rs`, its regular expressions matched by hand, its scratch repository running the same git commands in the same order. Measured byte-identical against the bash driver on nine paths, the real ledger staged and unstaged for two; a rewrite-blind mutant is caught. A defect owned mid-slice: the bash self-test never checked its scratch allocation, and during a failure-injection run (an unwritable scratch directory) `git -C ""` ran its fixture commands — `config user.*`, `add -A`, `commit` — on the real repository. It was stopped during the pre-commit gate, before any commit; the local `[user]` section it appended was removed and the index unstaged, both verified. The Rust module stops before any git command when the scratch fails. The lesson is a new knowledge card; two other drivers with the same unguarded form are slice 6f.

## SEMULITH-XTASK-0008 (leaf XTASK.6 slice 6d) — the rustdoc check in Rust: API-DOCS is `cargo xtask check-rustdoc`

XTASK.6 slice 6d: the `API-DOCS` doctrine moved from bash with an inline Python ratchet to `xtask/src/check_rustdoc.rs` — the doc build with three denied lints, the defect listing, the missing-docs ratchet against `doctrine/undocumented_items.tsv` with its messages (Python's `repr` of a malformed row, its `OSError` text) and the fifteen arms. Measured byte-identical against the bash driver on twelve paths (ok, self-test, a broken link, a rise, a fall, malformed, apostrophe-and-tab and duplicate rows, an unreadable record, ghost rows, a missing row, an unwritable scratch directory); a rise-blind mutant is caught. The locale sort moved into the shared harness, `DELIVERY-PROVENANCE` re-measured on it. The tree records the coupling census: of 36 unported free drivers, 25 are named by another script (some read as bytes or run in fixture repositories, where a shim cannot serve), 11 by none — those go first.

## SEMULITH-XTASK-0007 (leaf XTASK.6 slice 6c) — DELIVERY-PROVENANCE is `cargo xtask check-delivery-provenance`

XTASK.6 slice 6c: the `DELIVERY-PROVENANCE` doctrine — every row of a delivered `MANIFEST.sha256` carries one disposition, frozen and relocated rows re-hashed — moved from bash to `xtask/src/check_delivery_provenance.rs` with its nine arms. Kept from bash on purpose: hashing through `sha256sum` or `shasum` (no new crate; the same refusal when neither exists), the locale's collation through `sort` (en_US.UTF-8 orders the listings differently from byte order, measured), and bash's split of a disposition row. The shim keeps the scratch preamble `probe_temporary_locality.py` reads, and the shim test accepts exactly that shape. Measured byte-identical against the bash driver on nine paths of the real package, each change restored by a tree digest; a drift-blind mutant is caught by the module's own arms. Found while drafting: a Unix-only mode check would have broken the workspace's wasm32 build; it is platform-gated. `check_gap_claims.sh` waits: two checks read its census pattern as text.

## SEMULITH-XTASK-0006 (leaf XTASK.6 slice 6b) — COMMIT-PREFIX is `cargo xtask check-commit-prefix`; the doctrine modules share a harness

XTASK.6 slice 6b: the `COMMIT-PREFIX` doctrine — the behavioural probe that runs `.githooks/commit-msg` on a `SEMILITH-` and a `SEMULITH-` subject — moved from bash to `xtask/src/check_commit_prefix.rs` with its four fixture hooks, findings, verdict lines and exit statuses; `scripts/check_commit_prefix.sh` is a held shim. The scratch-directory and child-process helpers both doctrine modules use are one module, `xtask/src/harness.rs`. Measured byte-identical against the bash driver with the real hook swapped and restored, digest and mode checked (ok, self-test, unpinned, empty, over-tight and missing hooks, an unwritable scratch directory), and `PORT-WEB` re-measured byte-identical on the shared helpers. One intended difference in a path no gate reads: with an unwritable scratch directory, `--self-test` names the cause where bash printed a count from arms run against missing fixtures. The arm total stays 1672.

## SEMULITH-XTASK-0005 (leaf XTASK.6 slice 6a) — the first doctrine in Rust: PORT-WEB is `cargo xtask check-wasm-build`

XTASK.6 slice 6a: the `PORT-WEB` doctrine moved from bash to `xtask/src/check_wasm_build.rs` — the same preflight, the same four arms with their names and reasons, the same verdict lines and exit statuses — and `scripts/check_wasm_build.sh`, which the doctrine slot registers, is a shim held by a unit test. Measured byte-identical against the bash driver on every path (ok, self-test, a missing target, a broken self-test, a real host-only import), in the same half-second. The `DERIVED-COUNTS` arm total now counts a shim's module, one `tally.arm(` per arm, and yields nothing if the module is missing; two new arms, each fired RED, take the total to 1672. Recorded on the tree: the 54-driver inventory (7 spine, 8 calling a pinned script, 39 free), the remaining shell scripts' constraints, and `XTASK.5` blocked — the pinned `gate_report.py` reads `check-examples` in the CLI source, so moving it needs the director's decision.

## SEMULITH-XTASK-0004 (leaf XTASK.4 slice 4a) — the bench build leaves shell: `cargo xtask build-bench`

XTASK.4 opens with its measured inventory: of 74 tracked shell scripts, 55 are doctrine drivers, none is pinned by the retained case, 5 are evidence or upstream artifacts, and the 14 left are ported one per slice (three are hook-coupled and wait for the hooks). Slice 4a: `scripts/build_bench.sh` is now `cargo xtask build-bench`, and the script a three-command shim that `make bench` still runs; a unit test refuses any other line in it. Measured equal on the real tree: stdout byte-identical through the shim, the subcommand and `make bench`, the module digest unchanged, the same exit status for success (0), a wasm-only build failure (101) and a copy failure (1). Found while measuring and left open: when an invalid host `RUSTFLAGS` breaks rustc's target probe, quiet `cargo run` — and so `cargo xtask` — exits 1 with no message.

## SEMULITH-RDOC-0007 (leaf RUSTDOC.7) — semulith-verify documented; the RUSTDOC tree closes

RUSTDOC.7: `semulith-verify`'s 86 undocumented public items (the reduction, replay, report, run, snapshot and model types' fields and variants) now carry docs, each grounded in the code: the two control mutants, the report's verdicts, replay's image-digest check, the reduction's bounds and error messages. The record's last row fell 86 → 0, so every crate is at 0 undocumented items and API-DOCS refuses the first new one (fired RED on `run.rs:105:5`, restored byte-identical). Coverage is 100.0% in all three library crates (core 614, dsp56300 186, verify 490 items). The RUSTDOC tree is complete (7/7) and moves to the closed register; the API reference chapter's table says so.

## SEMULITH-RDOC-0006 (leaf RUSTDOC.6) — runnable examples for the core API

RUSTDOC.6: `semulith-core` had no doc example; it now has five that `cargo test` runs — the crate root decodes `addi x1, x0, 5` and reads its fields, `arith::bits` and `arith::sext` show field extraction and sign extension, and `muldiv::div`/`rem` show RISC-V division's truncation toward zero, `None` on a zero divisor, overflow wrapping and the remainder's sign. Every value was computed by the real code on the first run; fired RED by expecting −4 for −7 / 2 (the M case's own witness), then restored byte-identical. `make check`, API-DOCS and the wasm build green. With six leaves done the RUSTDOC tree's acceptance criteria hold; `semulith-verify`'s 86 undocumented items become RUSTDOC.7.

## SEMULITH-RDOC-0005 (leaf RUSTDOC.5) — semulith-dsp56300 documented

RUSTDOC.5: the DSP crate's 120 undocumented public items (decoder operands and decoded-instruction fields, the machine's registers and stops, the loader's case) now carry docs, each grounded in what the code already states — the decoder's own code tables, its module docs' opcodes and manual pages, the executor's behaviour (ASL/ASR by one bit, LSR on bits 47–24 only, CMP never writing its destination). The ratchet row fell 120 → 0 (86 undocumented in all, all in `semulith-verify`); coverage 186 items, 100.0%. Fired RED with one doc line removed, then restored byte-identical. Docs only: `make check`, the wasm build, the gate reports and every generation check unchanged. Observed, not changed: the executor cites ASR/LSR at FM 13-16/13-95, the decoder at 13-17/13-96. RUSTDOC.6 next.

## SEMULITH-RDOC-0004 (leaf RUSTDOC.4) — the generators document the generated modules

RUSTDOC.4: every one of `semulith-core`'s 61 undocumented public items sat in its four generated modules and came from a fixed template line in `gen_definition.py` or `gen_state.py`; the generators now emit a doc comment for each (14 template edits) and the modules were regenerated through them (DEF-GEN and STATE-GEN exact). The ratchet refused the fall until the core row was lowered 61 → 0 in this commit (267 → 206 undocumented in all); rustdoc's coverage report now measures `semulith_core` at 614 items, 100.0%, and the API reference chapter says so. Fired RED with one emitted doc line removed: `semulith-core: 1 undocumented > recorded 0`, then restored byte-identical. `make check`, the vector and generation checks and the retained M case unchanged. RUSTDOC.5 next.

## SEMULITH-XTASK-0003 (leaf XTASK.3) — one definition per target, guarded

XTASK.3: a command is either native to xtask or the Makefile's, never both. Already true by XTASK.1's design (14 Makefile rules; one native, `focused`), it is now held: the natives are declared once in `NATIVE`, dispatch goes through it, and a unit test reads the real Makefile, requires its rules and `.PHONY` list to agree and refuses a native name that is also a rule — fired RED with a temporary `focused:` rule, then restored byte-identical. Delegation unchanged (help, unknown target). The same unit sharded CHANGELOG.md: the 18 oldest entries to `docs/changelog/shard-0414.md` (62,075 → 48,125 B, order and bytes exact, SHARD-FREEZE 416 rows). Two defects owned mid-slice: a weak evidence box (SEAM-INTEGRITY, caught by `cargo xtask focused`), and a gate refusal on API-DOCS — the new crate doc linked a private item, and the failure listing buried that error under the 267 missing-docs warnings; the link is fixed and API-DOCS now lists only denied errors (two new arms, 1,670 in all).

## SEMULITH-XTASK-0002 (leaf XTASK.2) — the focused check set is tracked: `cargo xtask focused`

XTASK.2: the 26-check focused set every unit runs before its gated commit lived only in per-unit scratch runners under `target/`; it is now the `FOCUSED` table of the xtask crate, run by `cargo xtask focused [--out DIR]` (logs, one verdict line per check, `focused-checks.json`, exit 1 on any red, never commits; every other argument still goes to make). Measured on the same tree against the scratch runner: 26 identical verdict lines and identical JSON, green; with one count broken, both report the same single red check and exit 1. Help delegation unchanged, the wasm build, `make check` (with three new xtask tests) and API-DOCS green. From this unit on, commits run it.

## SEMULITH-XTASK-0001 (leaf XTASK.1) — the cargo xtask front door, delegation only

XTASK.1: the new workspace member `xtask/` (std only, no dependency) and the alias `cargo xtask` forward every argument to `make` from the repository root with the same streams and exit status, so every target keeps one definition, the Makefile, and nothing moved. Prototyped first in a detached worktree; measured on the real tree: `help` byte-identical, an unknown target and a deliberately broken `book` failing alike (rc 2, identical output), `check` with every test identical as sorted lines. fmt, clippy -D warnings, the wasm32 build and API-DOCS stay green (the ratchet counts `xtask/`, row 0). The lockfile gains 4 lines, so `make vendor` re-vendors once and prunes the standard-library crates the portability Miri leg re-syncs on every run. README, ARCHITECTURE §4 and the toolbox follow; README now says `make book` builds the API reference too.

## SEMULITH-RDOC-0003 (leaf RUSTDOC.3) — the missing-docs ratchet

RUSTDOC.3: the API-DOCS build now also warns on `missing_docs`, and the check counts the undocumented public items per crate directory against the new record `doctrine/undocumented_items.tsv` (cli 0, core 61, dsp56300 120, verify 86 = 267). A rise is refused with the crate's items listed; a fall is refused until the row is lowered, so the ratchet only tightens and the record is always the measured count. Six new self-test arms on a two-crate scratch workspace (13 in all); fired RED on the real tree with one added undocumented constant (`semulith-core: 62 undocumented > recorded 61`), then restored byte-identical. LIVE_STATUS 1,668 arms. RUSTDOC.4 next.

## SEMULITH-RDOC-0002 (leaf RUSTDOC.2) — the API reference is built with the book

RUSTDOC.2: `make book` now runs `cargo doc --workspace --no-deps --offline` and places the reference in the book's untracked output (`docs/book/book/api/`, 20 MB, 4 s); the new chapter "The API reference" links the four crate roots and states the measured coverage. A prototype showed the book checker cannot scan rustdoc's own pages (2,332 findings from JavaScript line-range anchors, percent-encoded ids and a missing root index), so UNIT-BOOKS now builds the reference fresh into its bundle and verifies that every book link INTO it lands on a page, without scanning its pages (rustdoc's links are API-DOCS's): three probe tests and three seams, 55 tests both modes; fired RED on the real tree with one broken link into the reference, then green (3,722 links). The derived book index regenerated; LIVE_STATUS 50 chapters.

## SEMULITH-RDOC-0001 (leaf RUSTDOC.1) — the doc defects and the API-DOCS gate

RUSTDOC.1: the new `API-DOCS` doctrine (`scripts/check_rustdoc.sh`) builds the workspace's rustdoc offline on every commit with broken and private intra-doc links and invalid HTML tags denied, and names each defect's file, line and lint; its self-test documents seven scratch crates (including that an inherited `RUSTDOCFLAGS` never decides the verdict) and removes them. Fired RED on the real tree before any fix: 20 defects. Fixed at the source, comments only: `<abs>` operand notations and bit ranges into code spans, links to private or cfg-gated items made plain, `[Self::new]`, an ambiguous link pinned to `mod@bench`, an editorial quote bracket escaped; the two in the generated definition modules fixed in `gen_definition.py` and both modules regenerated (DEF-GEN ok). `make check` rc 0 (287 + 173 + 17 tests), every generation and vector check green, the retained M case untouched (method satisfied, 10 of 10 legs). LIVE_STATUS: 41 doctrines, 1,662 arms; the tooling row In Progress. RUSTDOC.2 next.

## SEMULITH-LC-0054 (leaf LIVE-CONTAINMENT.4) — the tree's closed rows move to an archive part

.4o: docs/tasks/LIVE-CONTAINMENT.md stood at about 128 KB of the task family's 131,072-byte part ceiling. Its four closed row sections (the LC0027 checklist, the acceptance checklist, the verification log and the commit log; 42,607 B, every row ticked) moved verbatim into docs/tasks/archive/LIVE-CONTAINMENT-rows.md — each span's SHA256 listed in the part and found once, byte-identical — with one pointer under each heading (128,385 → 86,120 B). The family's standing mechanism (`decision_containment-reset.md`); no code changed.

## SEMULITH-TOOL-0001 (trees RUSTDOC, XTASK) — register the Rust-native tooling direction

The director, 2026-10-23: SEMULITH uses rustdoc for its API reference and moves to cargo xtask, "with extrem care, and incrementally for not breaking anything", because both are made for a Rust project. Recorded in `decision_rust-native-tooling.md` with the measured assessment (`cargo doc` builds in about 4 s with 0 errors and 287 warnings, 19 of them defects; documented items core 90.1%, verify 82.4%, dsp56300 35.5%; 35 tooling scripts pinned by retained evidence). Two proposed trees: `RUSTDOC` (six leaves, from the 19 doc defects and a link gate to doc examples) and `XTASK` (six leaves, from a delegation-only front door and a tracked focused-check runner to doctrine drivers one per leaf), each declaring its consumer; index rows and a LIVE_STATUS row. No code changed.

## SEMULITH-AC-0083 (leaf ARTIFACT-CLEANUP.26) — the third recurring cleanup through the supported act

.26: at 26 h, on a clean tree with `handoff: OK`, the four acts ran in target/artifact-cleanup/AC0083 (log inside): 73 candidates planned, 6 captured Cargo incremental outputs (15,766,468 B) strictly selected and removed by the guarded core under a fresh census, residue 0, journal `recorded-complete`/`verified`, `--inspect` confirming; 19,342 retained files kept. The 67 unrecorded mutation-build sessions (281,084,868 B) did not grow across nine gated commits: a stable set, so the .25 open question's deferral stands. The record is overwritten; `.27` is due after 2026-10-24T10:15Z.

## SEMULITH-P4-0295 (leaf P4-SYSTEM.14) — retain the other M statements and Table 1

a42bb: the m-forms case's 25 properties cite §11.1.1, §11.1.2 and Table 1, but only the DIV/DIVU statement was retained. The new `scripts/retain_m_statements.py` retains, unmodified and attributed under the a42z licence evidence, the eleven other normative spans and Table 1 in `profiles/rv64gc-lab-v0/retained/m-statements.html` (`RVI-M-STATEMENTS`, 6,018 B, `bc777ebb…`; `--emit` byte-identical on re-emission, `--verify` offline); only reviewed static markup passes. The source and licence pins stay owned by the pinned `retain_div_statement.py` (imported, not edited) and neither the new file nor `sources.sexp` is a pinned input of the retained case, so nothing is invalidated: method `satisfied`, policy `10 of 10`, 0 credited. Probe 20 tests / ten seams in both modes; the gate verifies the excerpt on every commit (arm total 1655). `decision_m-statements-retained.md`; the scope note in `materials/RVI_M_RETENTION.md`. The crediting act's authority and sufficiency remain the director's. The first gated attempt was refused by the self-test, 1154 / 2; the kept log named the method probe's `artifact-selection` and `typed-findings` seams, whose synthetic capture returned `refused` after 31.7 and 59.1 s and printed no reason — it now prints the capture's reason; twelve reruns passed; cause open.

## SEMULITH-LC-0053 (leaf LIVE-CONTAINMENT.4) — LIVE_STATUS rows back to states

.4n: LIVE_STATUS.md stood at 6,137 of its 6,144-byte ceiling. Applying the registry's declared control ("rows are states, not prose"), 22 Notes cells were cut to their state, tree pointer, leaf count and caveats (6,137 → 4,771 B; 49 lines); every dropped phrase was located in its tree or the history shards first, and the three derived counts and every tree claim stay (TREE-CLAIMS and DERIVED-COUNTS ok). No ceiling moved. The book's status chapter includes the file, so it shows the shorter rows.

## SEMULITH-P4-0294 (leaf P4-SYSTEM.14) — move the closed `.14` records into archive part 21

a42ba: docs/tasks/P4-SYSTEM.md stood at 117,506 B of the task family's 131,072-byte part ceiling. The complete records of the closed units a42aq–a42aw (24,128 B) and the acceptance rows a42ar–a42ax (32,158 B) moved verbatim into docs/tasks/archive/P4-SYSTEM-21.md — eight spans, each SHA256 listed in the part and found once, byte-identical — with one pointer each in the live tree (118,497 → 63,186 B). The family's standing mechanism (`decision_containment-reset.md`): no seal, reader or inverse map. No code changed.

## SEMULITH-P4-0293 (leaf P4-SYSTEM.14) — the crediting record: mechanism, no credit

a42ay: a credited disposition is now a record, never a flag — `(credit …)` in `profiles/<profile>/credits.sexp` (schema `schema/credits.sexp`, validated by RECORD-SCHEMA), naming requirement, obligations and case and pinning the measured record, the receipt and the policy document by path, SHA256 and size. The new unpinned `scripts/credit_records.py` reports each record `current` or `lapsed` (every pin and every input of the case's dependency manifest authenticate; the receipt is a complete capture with `qualification` false; the declaration binds the credited requirement); `requirement_status.py` credits a binding only through a current record, and a receipt's own `qualification` true, a lapsed record or one naming an unknown case is a finding; `review_div_policy.py` reports `credited` from the catalogue (`credited by <record>` in the summary) and makes a record over an unsatisfied measurement a finding. Probes: status 22 tests / seven seams (`qualification-word`, `unknown-case-credit`; the `declared-credits` seam retired — the receipt pin makes a declared case uncreditable by construction), policy 25 / eight (`credit-any`); the token-facet inventory gained the date and decision-record languages (25 schemas / 100 facets; RECORD-SCHEMA 70 of 70). Real tree: no catalogue, `REQ-GC-M` `planned`, `0 of 0 credit record(s) current`, `DIV-POLICY: satisfied — 10 of 10 legs satisfied; no qualification credit`. The act — the first record and the recorded status moving in one commit — is the director's (`decision_credit-is-a-catalogue-record.md`). Two family ceilings fired on the focused run and were re-derived with the numbers (`decision_schema-and-decisions-families-rederivation.md`): `schema/` 24 → 32 files (the credit schema was the 25th), the decisions index's per-part 16 → 32 KiB (one row per record, 16,537 B).

## SEMULITH-P4-0292 (leaf P4-SYSTEM.14) — the retained reviews read the m-forms capture

a42ax: `scripts/review_div_method.py` (`RETAINED_CASE_ID`, the 16,942-byte measured pin `fb22d5e5…`, the declaration commit `4af5a68…` and the capture commit `e775705…`) and `scripts/review_div_policy.py` (`CASE_ID`) now name `rv64gc-m-forms-v3` — consumers only, no pinned module moved, no declaration invalidated (`decision_caller-names-the-case.md`). The real tree measures: finite method `satisfied` (85 files / 1,076,834 B authenticated, 40,438 snapshot bytes, 1,142,222 charged, 39 checker sources) and `DIV-POLICY: satisfied — 10 of 10 legs satisfied; no qualification credit` — the twelve Table 1 rows present and predeclared, 13 of 13 forms, the control at step 12 x15. `credited` stays false, `REQ-GC-M` keeps deriving `planned` with both cases pending: a satisfied measurement is the input to a separately owned crediting act whose authority and mechanism the next unit settles (`decision_ten-legs-satisfied-credit-separate.md`). The method probe's fixture, the shared synthetic reference (`probe_div_command.synthesize_reference(…, case_id=…)`) and both real-tree arms follow the retained case; every seam count is unchanged (method 14, command 7, retention 7, policy 7). The policy-adequacy chapter carries the ten legs with the first case as history; method-adequacy, canonical-division, requirement-status, the evidence index and the toolbox rows follow. The first case stays `invalidated` history, never rerun. Two defects owned mid-slice after the first commit attempt was refused by the gate's own self-test with its MISS line discarded (the second silent refusal; a captured rerun passed 1130 of 1130 arms, cause still open): `scripts/check_profile_consistency.sh` now keeps its self-test output at `target/profile-consistency-selftest.log` and prints the `self-test MISS` lines on REFUSED (fired RED in a worktree before landing), and `scripts/check_citations.py --self-test` removes the 19 fixture directories it had leaked on every run (5,494 directories, 87 MB, removed). Knowledge card `a-gate-that-discards-its-self-tests-output-cannot-be-diagnosed.md`.

## SEMULITH-P4-0291 (leaf P4-SYSTEM.14) — capture the m-forms case

a42aw: `rv64gc-m-forms-v3` captured once on 2026-10-22 by the new tracked `scripts/retain_div_capture.py` (preflight: outputs absent, declarations regenerating byte for byte, the binary's digest equal to the retained identity, the declaration commit `4af5a68…` recorded; one invocation of `capture_div.capture`, never retried; exclusive publication of `measured-experiment.sexp` and `verification.json`, qualification false) — the procedure the first capture ran by a scratch script. Result: three fresh zero-exit processes, baseline/repeat AGREE over all 33 boundaries with byte-identical 2,794-byte traces, the control DIVERGE at boundary 12 x15 alone (−3 observed, −4 expected), all nine findings matched, 25 properties bound, 85 files authenticated; the offline re-evaluation of the retained bytes agrees. Probe `probe_div_capture_retention.py` (11 tests over synthetic processes, seven seams) and gate arms; the evidence family holds all 43 declared files; `requirement_status` counts both cases pending, none credited; `REQ-GC-M` stays `planned`. The retained reviews still read the invalidated first case: a42ax switches their pointers and measures the ten legs.

## SEMULITH-P4-0290 (leaf P4-SYSTEM.14) — the evaluation binds the case it is asked to

a42av: `evaluate_retained_unit`, `capture_and_evaluate` and the adequacy review take the reviewed case explicitly (`case_id`, the retained case by default; an unknown case refuses before any artifact read), `capture_div.capture` passes the case it prepares, and the method review keeps its own `RETAINED_CASE_ID` outside the pinned modules — so capturing a declared case never moves a constant inside a pinned input, and switching the retained pointer after a capture invalidates nothing (`decision_caller-names-the-case.md`). The m-forms declaration was re-emitted once over the three edited pinned modules: only the pins of `capture_div.py`, `matched_gpr_evaluation.py`, `matched_gpr_unit_collector.py` and the manifest itself moved; every property, input, observation and run declaration is byte-identical, and the three files regenerate byte for byte. Probes: property-evaluation 25 / 16 seams (`case-pass-through`), unit-evaluation 30 / 26 (`case-forward`); the real tree is unchanged (method `stale`, policy `invalidated`, 2 cases / 1 declared). No capture, receipt or credit; a42aw captures.

## SEMULITH-P4-0289 (leaf P4-SYSTEM.14) — declare the m-forms case

a42au: `rv64gc-m-forms-v3` is declared under `evidence/rv64gc-m-forms-v3/` — four prepared inputs curated by the new tracked `scripts/prepare_div_inputs.py` (the m-forms ELF, the mapped override, the canonical expectation copy, the boundary 12 x15 −3 → −4 control; the tool reproduces the retained v2 bytes exactly and refuses to overwrite) and three native declarations from `scripts/capture_div.py --declare --case rv64gc-m-forms-v3` (25 properties, the control naming `form-div`, 64 children; regenerated byte for byte). The capture command and the capture review take a `--case` selector; the retained case's constants are unchanged, so the method review and its probes are untouched. The evidence family is re-derived for two declared cases (43 files / 32 MiB, index rewritten; `decision_evidence-family-two-cases.md`), and the knowledge-card family, whose exact ceiling fired on the promoted lesson, for designed growth (40 files / 128 KiB; `decision_knowledge-family-first-rederivation.md`); the toolbox's DIV-evidence rows moved to their own family file at the execution table's per-part ceiling. `scripts/requirement_status.py` reports a declared, uncaptured case as `declared` and credits nothing — and now reads a record's properties under its `verification` graph: until this unit both retained cases loaded with zero bindings, a defect its own flat fixture could not see (lesson promoted to `docs/knowledge/a-fixture-must-have-the-real-records-shape.md`). Probes: inputs 34 tests over both cases, status 19 / six seams, authorities, capture review, command and method unchanged in count. No capture, receipt or credit; `REQ-GC-M` stays `planned`. Next: a42av captures the three runs.

## SEMULITH-P4-0288 (leaf P4-SYSTEM.14) — one case, many predeclared properties

a42at: `scripts/matched_gpr_property.py` owns a case table — the retained `rv64gc-signed-div-truncation-v2` keeps its one property; `rv64gc-m-forms-v3` declares, before its declaration record and capture, 25 properties over `m-forms.s` (the 13 forms once each, the 12 Table 1 cells) with the reviewed words of all 33 boundaries, every word and value re-derived independently by the probe; the relation plan carries every declared property (1..64, distinct witnesses) and the one the control run names, whose witness the byte comparison discriminates; the evaluation and the collector build one claim per declared property from the record's own words, and the binding holds every predeclared value to the source derivation the source-value finding already carries; the policy's control leg reads the property the `control_run` names. Probes: property 34 tests / 35 seams, property-evaluation 24 / 16, relations 42 / 19, policy 22 / 7; gate arms re-measured in both modes. The retained case is `invalidated` by this commit (its pinned binding moved; a42as) and nothing is credited; `REQ-GC-M` stays `planned`. Decision record, chapters, toolbox rows. Next: a42au declares the case, a42av captures it.

## SEMULITH-AC-0082 (leaf ARTIFACT-CLEANUP.25) — the second recurring cleanup through the supported act

Plan, strict selection, `--delete` under a fresh host census and `--inspect` in
target/artifact-cleanup/AC0082: 6 captured Cargo incremental outputs removed
(15,766,472 B), residue 0, journal recorded-complete/verified; 67 unrecorded
candidates (281 MB, the gate's mutation-build sessions — an open question), every
input and log untouched. `docs/ARTIFACT_CLEANUP.md` overwritten. Next cleanup after
2026-10-23T08:12Z; P4-SYSTEM.14 a42at resumes meanwhile.

## SEMULITH-P4-0287 (leaf P4-SYSTEM.14) — a stale finite method invalidates, it does not lock

a42as, the director's ruling of 2026-10-22: `scripts/review_div_policy.py` reports a `stale` finite method as `invalidated` with exit 0 and the moved declaration named, keeping exit 1 for a qualification claim over it and for a refused, unavailable or unsupported method; `scripts/probe_div_method.py` builds a synthetic current retained case once per run (current declarations, three synthetic processes, the measured experiment persisted, the copy's method pinned to it) so its 14 seams stay reachable while the curated capture is invalidated, and its real-tree arm — like the command probe's two — asserts the state the dependency manifest predicts. Measured before the change: one appended comment line on a pinned module made 32 of 1,086 self-test arms miss and the gate refuse; after it, both tree states measure green. Decision record, chapter, toolbox mirror, gate counts. No credit granted or removed; `REQ-GC-M` stays planned.

## SEMULITH-P4-0286 (leaf P4-SYSTEM.14) — author the crediting M corpus program

a42ar: `profiles/rv64gc-lab-v0/guests/m-forms.s` exercises all 13 M forms and the 12 Table 1 cells with spec-side expectations on the parcel route (schema-valid, byte-identical on re-derivation, every value matching an independent arithmetic); registered in the run order and the interaction matrix (the author's owned-guest list is a pinned input of the retained case: a one-line registration staled the finite method on the first commit attempt, so ownership waits for the fresh capture); `guests_rv64gc.rs` regenerated; live Sail 0.14 AGREE on 33 steps with byte-identical traces — an experiment, no case or credit; `REQ-GC-M` stays `planned`. P4 closed rows through a42aq moved verbatim into `docs/tasks/archive/P4-SYSTEM-20.md`. The guest pair crossed the `profiles/` 3 MiB aggregate (3,154,244 B) with no health warning possible; both aggregates re-derived by `decision_profiles-family-corpus-second-rederivation.md` to 4 MiB / 800 files with health below the family, per-part unchanged.

## SEMULITH-LC-0052 (leaf LIVE-CONTAINMENT.4) — containment reset by director ruling

Slice (m): the book and unit books carry no size ceiling, the task family's aggregate and count are ungoverned (per-part 128 KiB kept), the second seal is rejected and a unit is recorded once — `docs/decisions/decision_containment-reset.md`; .4c–.4g moved verbatim into `docs/tasks/archive/LIVE-CONTAINMENT-adoption.md`; routes RED 3,148,764 > 3,145,728 then GREEN; both history heads sharded.

## SEMULITH-P4-0285 (leaf P4-SYSTEM.14) — measure the retained case's policy legs

a42aq: `scripts/review_div_policy.py` reads the evidence policy's requirements for a
`defined` medium-risk requirement as ten legs and measures each against the retained
DIV case's own bytes on top of the finite method review: 8 of 10 satisfied; pending
boundary-fixtures (six Table 1 rows present, none predeclared) and form-coverage (one
of thirteen forms predeclared). `OB-GC-M`'s feature disposition declared (none
applies). Measurement grants no credit; `PROFILE-CONSISTENCY` runs it on every commit
and fails a receipt claiming `qualification` the legs refuse. Probe 19 tests normal/O,
five seams RED. a42ap's whole rows retired into task-claims-2.md with exact inverses.
Chapter, toolbox, doctrine mirrors, decision record. `REQ-GC-M` stays `planned`.

## SEMULITH-P4-0284 (leaf P4-SYSTEM.14) — derive requirement status from the evidence graph

a42ap: `scripts/requirement_status.py` derives each requirement's
`implementation_status` from requirements, effective obligations and every
retained case's predeclaration and receipt, and `PROFILE-CONSISTENCY` drift-checks
it on every commit for each policy-declaring profile: rv64gc 48 `planned` (one
case uncredited at `pending`), rv64i 28 `planned`, 0 drift. Declared in the
model-book chapter, toolbox and doctrine mirrors, not in `EVIDENCE_POLICY.md`: the
policy is a pinned reviewed input of the retained case and an edit refused 30
DIV-COMMAND/DIV-METHOD self-test arms until reverted (GS report byte-identical);
probe 17 tests normal/O, five seams RED. a42ao's whole rows and the a22–a36
changelog retired into task-claims-2.md with exact inverses. No status advanced.

## SEMULITH-LC-0051 (leaf LIVE-CONTAINMENT.4) — re-derive the task-family count for retention continuation

Slice (l): the family had been full (107/107) since 2026-10-12 and three members
were within 200 B of the per-part ceiling, so no tree could record a unit. The
first complete-records continuation `task-claims-2.md` holds the whole `.4j`
record and acceptance (3,281 B, exact inverses); the count is 107 → 116 =
33+1+42+40 under `decision_task-family-count-rederivation-retention.md`, health,
aggregate and per-part unchanged. Evidence target/live-containment/lc0051.
Next: P4-SYSTEM.14 a42ap; the aggregate (3,134,069 of 3,145,728 B) is slice (m)'s seal.

## SEMULITH-LC-0050 (leaf LIVE-CONTAINMENT.4) — re-derive the decisions-family bound a second time

Slice (k), routed in from ARTIFACT-CLEANUP.23: the byte axis fired again with
only an index row added, after 26 records in eleven days and none in eight
while two units withheld records to fit. Reviewed authority
`docs/decisions/decision_decisions-family-second-rederivation.md` lands with
the registry row: 160 files / 524,288 B, health 64 / 278,528, per-part 16,384
unchanged; the index's per-part ceiling is the next bite. Evidence
target/live-containment/lc0050. Next: P4-SYSTEM retention capacity.

## SEMULITH-AC-0081 (leaf ARTIFACT-CLEANUP.24) — the first recurring cleanup through the supported act

Plan, strict selection, `--delete` under a fresh host census and `--inspect` in
target/artifact-cleanup/AC0081: 6 captured Cargo incremental outputs removed
(15,766,463 B), residue 0, journal recorded-complete/verified; 13 unrecorded
candidates, every input and log untouched. `docs/ARTIFACT_CLEANUP.md` overwritten.
Next cleanup after 2026-10-21T22:11Z; P4-SYSTEM.14 resumes meanwhile.

## SEMULITH-AC-0080 (leaf ARTIFACT-CLEANUP.14) — bind the host census into the supported cleanup act

New artifact_cleanup_operator.py is the single deleting command: a bounded
fresh run of the public handoff census must give its green verdict immediately
before the guarded core; running work refuses, failed or absent censuses refuse
as unavailable, and one JSON receipt names disposition, stage, counts, failure
and journal. `--inspect` reports plan, selection and journal. Operator 10
tests/3 omissions normal/O; artifact gate 146 outcomes; literal arms 1643. The
priority1 durable-instrument activity closes; .24 runs the next cleanup
through the act. No real cleanup event in this unit.

## SEMULITH-AC-0079 (leaf ARTIFACT-CLEANUP.16) — unlink only what plan, selection and journal agree on

New artifact_cleanup_guarded.py: preflight re-decides the strict selection,
a version-2 journal binds the selection digest and approved indices, every
file is revalidated through its parent descriptor immediately before unlink
with the intent flushed first and absence required after, and the after-state
must equal the plan minus the approved files. D14: stale verdicts name the
first differing member. Guarded 12 tests/4 omissions, journal 29/11, planner
27 normal/O; artifact gate 138 outcomes; literal arms 1641. CLI dry-run only;
the operator act with the host census is .14. No real cleanup event.

## SEMULITH-AC-0078 (leaf ARTIFACT-CLEANUP.17) — select strictly against the published ledger

New artifact_cleanup_selection.py re-censuses a published plan, intersects its
candidates with captured current authority and exclusively publishes the
approved/unrecorded partition beside the plan; cache-named inputs stay
unrecorded (P1 closed). D12: a failed build retires rows whose files rustc
removed. D13: ctime-only drift no longer rejects unchanged recorded outputs.
Selection 11 tests/5 omissions normal/O; artifact gate 128 outcomes; literal
arms 1639. Actual selection on the real tree recorded. No deletion authority.

## SEMULITH-AC-0077 (leaf ARTIFACT-CLEANUP.23) — retire the completed-checklist suffix into a second ledger generation

The cleanup retention terminal becomes a generational chain: generation 2 retains
the b18971e predecessor and its exact suffix, each retained entry re-derives the
descriptor it superseded, and the publisher accepts one generation per owned
transition. Live narrative 12,947 → 2,198 B. Retention probe 45 tests/20 omissions
normal/O; registry row 6 files / 192,801 B under the leaf's authority; docs/decisions/ ceiling pressure routed to LIVE-CONTAINMENT.4 (k). D12/D13 (stale session
rows, ctime drift) logged for .17. No cleanup authority changed.

## SEMULITH-AC-0076 (leaf ARTIFACT-CLEANUP.21) — capture and atomically publish bound build outputs

Each actual producer build is surrounded by an anchored census of its
incremental caches; new or changed-digest files become v2 records with all
four source pins. Publication is lock-serialized, merged (replace/retire/keep),
written to a unique temporary, synchronized, renamed over the ledger and read
back; every failure keeps the previous ledger exact. Provenance 42 tests/22
omissions and Cargo 23 tests/10 omissions normal/O; artifact gate 116 outcomes,
1637 literal arms unchanged. Real ledger published by both producers. Strict
selection .17, core .16 and host workflow .14 remain; no deletion authority.

## SEMULITH-AC-0075 (leaf ARTIFACT-CLEANUP.22) — version support-source pins without rewriting legacy records

Keep exact v1 serialization and add v2 runner/census pins. Strict matching denies
unbound legacy rows and stale support sources; mixed ledgers retain both row
classes without upgrading old authority. No capture, publication or selection
changes yet. 31 tests normal/O and 16 omissions per mode pass; artifact gate 100
outcomes. Shared book/help/toolbox updated. D11 replaces COMMIT's stale book
count with the project/unit contract. LIVE_STATUS and all old evidence unchanged.

## SEMULITH-AC-0074 (leaf ARTIFACT-CLEANUP.20) — bind public Cargo commands and output roots

Both C producers use explicit unchanged Cargo target/intermediate roots, relative
manifests and isolated on-volume storage. Bounded capture/deadline and owned
process-group termination/join cover completion, interruption and failures;
source/manifest/root/ancestor checks surround each invocation.17 tests normal/O,
eight failing omissions per mode and actual engine18/guest2 pass. Cold Cargo
preserves an unchanged cache-shaped input. ARTIFACT-COHORT94 outcomes;40 doctrines,
1637 literal arms. Capture/publication .21 and strict selection .17 remain; P1
open, no new deletion authority/event, CPU/board/replay unchanged.

## SEMULITH-AC-0073 (leaf ARTIFACT-CLEANUP.19) — retain the completed cleanup ledger in bounded Markdown

Retain the full76937B predecessor and exact38046B completed ledger as directly
readable Markdown in a finite119258B terminal. Keep all19 live nodes and child
relationships, one authenticated history pointer and independently bounded new
narrative. First publication proves the source/prefix and both publishing views;
subsequent checks freeze terminal bytes and preserve completed live history.
Reader uses no Git/network/extraction.40 tests normal/O pass;18 guard omissions
each give1 failure/0 errors. D6 ancestor-census and D7 pure-judge presence/mode
guards fixed before signoff. Book shares usage;44 routes/1635 literal sites,
40 doctrines and CPU/board/replay unchanged. P1 actual-build integration remains
.17, followed by core/host binding. No cleanup event or push.
D9 aligns root-relative object locators with the separate fixture-path contract.
Generic guard unchanged; both originals remain byte-exact.

