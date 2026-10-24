# CHANGELOG.md

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

## SEMULITH-AC-0072 (leaf ARTIFACT-CLEANUP.18) — bound workflow guidance and align the template

Move complete template evidence/general guidance into a separately bounded setup
guide; the template shrinks1610B. All old history and ceilings are retained. Restore the missing sixth box; document supported direct numeric
IDs. Reader/runtime unchanged. Shared book examples display every placeholder;
the materialized template and normative six-label set agree. Guide4259B/78lines,
ceilings6144B/128lines.43 destinations;40 doctrines/1633 arms and CPU/board/replay
state unchanged. Native3/focused16/books7/source-history checks pass.

## SEMULITH-AC-0071 (leaf ARTIFACT-CLEANUP.15) — bind per-file output-provenance records

Add a closed bounded provenance codec and anchored reader: successful bound host
Cargo command, exact new/changed output observations, source pins and current
supplied file facts. Unknown/unchanged inputs, stale sources, aliases and wrong
root/profile claims cannot gain authority.25 tests normal/O/13 omissions each:
28 outcomes; focused gate76, derived1633 sites. Tracked public Cargo dry-run
probe preserves three owned inputs and shows profile scope is not generation.
D3 root mapping/D5 profile controls repaired; D4 task prefix fully restored
before publication. P1 remains open for actual producer/planner integration .17;
core .16 and host/CLI .14 follow. No cache deletion or historical event change.

Focused16/books7/scope pass;3844B whole0384/0385 retained.

## SEMULITH-AC-0070 (leaf ARTIFACT-CLEANUP.13) — record recoverable cleanup intent

Add bounded exclusive plan/source-bound attempt records and readonly inspection.
Ordered plan/ancestor/frame barriers, Darwin full-sync, identity checks and poisoned
writer refusal protect metadata. Torn prefixes remain uncertain; no cache unlink
or current-state/actor attestation.26 tests normal/O/ten omissions each:22 outcomes;
expanded gate48, derived1631 sites. Actual smoke keeps owned dummy cache intact.
Move complete old teaching into bounded shared fragment; all original examples
preserved, book524076/524288B. Guarded core .15 and host/CLI .14 remain pending.
Focused16/books7/scope pass;4030B whole history retained0382/0383.

## SEMULITH-AC-0069 (leaf ARTIFACT-CLEANUP.12) — retain the historical cleanup helper

Preserve original5815B helper as passive authenticated input. Five tests normal/O
replay debug success and release-D1 failure/no receipt inside fresh owned fixtures;
source-pin omission loses1 assertion/0 errors. Cold three-file CLI passes from a
valid parent cwd without Git. Expand focused gate to26 outcomes/derive1629 literal
sites, add bounded artifact-toolbox family and shared book teaching. No real
cleanup or historical event change. Guarded core/journal .13 and host/CLI .14 follow.
Focused16/books7/scope pass;0380/0381 retain3172B whole.

## SEMULITH-AC-0068 (leaf ARTIFACT-CLEANUP.11) — track bounded cleanup plans

Add a bounded immutable cache planner/checker with exclusive output, fixed root,
public HEAD/index protection and descriptor boundary checks. Release caches are
separate from retained strays; no cache deletion API in this slice.24 fixture
tests normal/O plus ten independently failing omissions per mode:22 outcomes.
Register ARTIFACT-COHORT, toolbox and shared CLI/book usage; derive40 doctrines
and1627 literal arms. Preserve original capture and cleanup event identities;
guarded deletion/partial results remain .12. Focused16/books7/normal-print/
actual read-only plan-check and complete source/history/scope proof pass; whole
0378/0379 retain3504B. No latest-cleanup receipt change.

## SEMULITH-AC-0067 (leaf ARTIFACT-CLEANUP.10) — remove due caches and retain method evidence

Remove18 known untracked Cargo incremental caches/78250724B after six normal/O
preflights and actual host census OK. Immediate selected residue0;18121 retained
input/evidence files/152718645B byte/hash-exact. Four nested Git roots skipped;
all tracked code/data/statuses and fixed capacities preserved. Overwrite the
latest receipt, rendered through the existing book include without source growth.
Focused13/books7/normal-print receipt and whole-source/history proof pass;
CH0377 retains636B exactly. Return to full P4 policy/status after normal COMMIT.

## SEMULITH-P4-0283 (leaf P4-SYSTEM.14) — check retained finite method adequacy

Compose reviewed declaration/input/influence authorities and authenticated retained
findings for the first DIV capture. Bind only measured metadata changes, exact
selected artifacts and curated historical origin; require typed complete findings.
Read-only/no Sail/Git/cache/binary; finite method satisfied, full policy pending,
replay not checked; no requirement/CPU/ancestry credit. Native/evaluation charge
1100198B within128MiB; separate snapshot/preparation/source limits preserved.
Twenty tests x2 and14 independently discriminated omissions x2:30 exact outcomes;
103-file runtime refuses missing/stale/forged data and late checker drift. Register
two literal score sites; derived1625 arms. Original producer/capture bytes exact.
Retain four whole closed records2184B in the existing task-claims artifact; fixed capacities. New model teaching and
canonical include/toolbox sync. Focused17/books7/rendered5/examples3/scope normal/O pass; whole history6009B retained0375/0376; source-owner inverses2/eight damaged refusals.

## SEMULITH-P4-0282 (leaf P4-SYSTEM.14) — synchronize capture and replay teaching

Correct nine current teaching/index owners: canonical decision includes, adjacent
evidence chapters, GC gaps and main P4/architecture replay state. First finite DIV
capture is retained in the matched-gpr-v1 envelope; complete policy/qualification
remains pending. GC snapshot/replay/reduction completed .16, G-REPLAY4/4green.
Preserve dated planning history, exact protocols/examples and all code/evidence.
Retain four whole closed am records2574B; all capacities fixed. Book/focused/scope
verification pass: focused17/books7/rendered9/scope normal/O,46 examples exact;
CH0374 whole1107B/inverses2/eight refusals. CPU/board/status unchanged.

## SEMULITH-P4-0281 (leaf P4-SYSTEM.14) — retain the first canonical DIV capture

One composed capture after committed source/declarations: three fresh zero-exit
Sail processes,12 observations, measured native record and derived verification.
Baseline/repeat agree across27 boundaries; wrong quotient diverges at step2 x7.
All traces identical; independent normal/O retained evaluation agrees without a
process. Charge24337600B;85 files/1048756 authenticated bytes/33759 snapshot bytes.
Add actual offline regression: command19 tests x2/same omission losses; ten101-file
copy outcomes and legacy controls pass. Four whole closed al records2498B retained.
Focused17/books7/examples6/surfaces8/scope pass; whole history5007B retained.
All retention caps fixed. Full policy and
qualification pending; CPU/board/status unchanged. Next complete policy integration.

## SEMULITH-P4-0280 (leaf P4-SYSTEM.14) — retain exact DIV capture predeclarations

Retain the planned record,64-child manifest and73-input/author/impact declaration:
41514B across three native documents, independently regenerated and pin-checked.
Keep the8-file evidence family inside its fixed22-file/16MiB envelope; no Sail
observations, measured results, qualification or CPU/board credit.

Gate actual declaration currentness through18 controls normal/O, preserving the
seven omission losses. Eighteen87-file copy outcomes bind or refuse before an
explicit mocked collector; status/prose changes preserve the non-cyclic identity.
Correct stale adjacent book teaching, preserve old examples and whole closed
records3534B/inverses2/nine refusals; CH0371 whole1303B retained.
Focused17/books7/examples4/surfaces5/scope pass; capacities fixed.
Next fresh canonical processes after this declaration commit; full policy remains.

## SEMULITH-P4-0279 (leaf P4-SYSTEM.14) — compose the finite DIV command

Compose the fixed DIV plan,64-child manifest and separate73-input/author/impact
reviews in capture_div. Read-only --declare emits three bounded native documents;
--capture authenticates exact predeclarations before the existing combined helper.
Keep128MiB/16MiB envelopes and separate preparation/tool I/O. Whole changing view
hashes stay outside execution pins. No automatic result-file publication or credit.

Copied84-file synthetic runtime exercises three fresh processes, all27 source
values, exact repeat, wrong quotient, separate bindings and binary-free retained
evaluation. Existing outputs preserve/refuse; failed process leaves its receipt.
17 controls x2/16 outcomes; focused17/books7/examples3/surfaces5 and scope pass.
Six closed records3566B retained whole; all family/member/head caps fixed.
Next commit exact native declarations before Sail; full policy still pending.

## SEMULITH-LC-0049 (leaf LIVE-CONTAINMENT.4) — seal the second finite history segment

Seal158 closed shards plus manifest from a5bf4579:159 originals782755B/11200LF,
retained in one276917B immutable object. Preserve the earlier object/descriptor;
public Python/tar reproduces every source, relocated normal/O reads both segments,
and corrupt new data/changed old descriptor refuse. Verified copy precedes exact
158-source retirement; residue0. Current receipts stay native and numbering holds.

Standing archive delegation and the separate LC0049-CAPACITY record own exactly
this finite expansion:4-file terminal/581897B ceiling, existing metadata/reader and
all ordinary-history/head/other caps fixed. Retain full LC0041 record5552B with
inverses; synchronize front door/book/recovery/registry. Main book shrinks8B and
keeps prior examples. No runtime, CPU/board/replay or qualification change.
Verification:17 focused/seven books/4 examples/3 surfaces; history44/0,
queries263x2/0 defects, source/owner inverses2/seven damaged refusals and protected
scope pass. Director2026-10-19 explicitly approved LC0049.
Then return to P4-SYSTEM.14 final execution/manifest/authorities/capture/full policy.

## SEMULITH-P4-0278 (leaf P4-SYSTEM.14) — review the current authority-selection route

Extend producer review to37 modules and the public13-view authority loader.
Observe actual reads, reject undeclared paths/write modes/processes, and bind view
facts to snapshots. Keep27 execution data separate,64 children/79 reviewed files,
unchanged limits and separate public I/O contracts.31 controls normal/O; five new
omissions lose1 each, old13 omission losses exact,0 errors. Copied runtime matches
both modes; authority18/three omissions unchanged. Book/recovery docs synced.
No canonical capture or qualification; final execution/manifest/authorities next.

Validation:17 focused checks/seven books/one complete two-mode example/three
rendered surfaces plus adjacent prepared-input page; protected inverses exact. Three whole ai
records1960B/inverses2/seven damaged refusals; CH0366 whole819B. All caps fixed.
Fix stale prepared-input population35/63 to37/64 before commit.
LIVE remains42routes/1621arms,CPU14/18,BOARD10/12,replay4/4green.

## SEMULITH-P4-0277 (leaf P4-SYSTEM.14) — select current DIV capture authorities

Add a read-only current-authority command using existing snapshot/schema/catalogue/
scope/identity/property owners. Freeze13 view identities and selected metadata;
raw validation precedes mapping, and duplicate/unknown/superseded/changed selections
refuse. Keep direct1MiB/member,8MiB/pass/two-pass bounds; public tool I/O separate.
Fix the prototype's undeclared alternate-registry read before delegation. Eighteen
controls pass normal/O; raw/registry/semantic omissions lose3/1/3 assertions,0 errors.
No binary/reference process, authority-file publication, capture or qualification.
Final reviewed entrypoint/exact manifest/inventory/impact/full policy remain next.

Validation:17 focused checks/seven books/two examples/three rendered surfaces;
1569 protected files/1Gitlink/93 old entries and all old production/probes exact
except registration. Six whole records3137B/inverses2/ten damaged refusals;
CH0365 keeps one whole1104B entry. All caps fixed. LIVE derives1621arms only;
42routes,CPU14/18,BOARD10/12,replay4/4green unchanged.

## SEMULITH-P4-0276 (leaf P4-SYSTEM.14) — anchor gate reporting to its runtime tree

Fix reproduced P1 parent-context fallback: copied gate code could credit114/114
realized contract pairs with its local registry absent. Derive ROOT from loaded
source, keeping dependency imports and registry selection local with no import
process. Six controls pass normal/O; restoring Git-root selection loses five
assertions/0 errors. Existing gate24/wrapper20 and legacy ancestry matrix pass.
Promote the copied-runtime isolation lesson to the existing locality card.
Current validated authority entrypoint/exact manifest, capture/full policy remain
pending; no qualification or acceptance credit.

Validation:17 focused checks/seven books/one two-mode example/three rendered
surfaces;1564 protected files/1Gitlink/92 whole entries and all old probes exact.
Three whole task records2311B/inverses2/seven damaged refusals; DEV0364 retains
whole5213B entry. All caps fixed. LIVE derives1619arms only;42routes,CPU14/18,
BOARD10/12,replay4/4green unchanged. Production changes only ROOT/registration.

## SEMULITH-P4-0275 (leaf P4-SYSTEM.14) — terminate cyclic contract ancestry

Fix a reproduced P1 hang in CONTRACT-FREEZE and public effective-contract
measurement: schema-valid cyclic extends now terminates with named refusals.
Preserve valid frozen/inherited/superseded behavior. Four controls pass normal/O;
each of two guard omissions loses three assertions with0 errors. Existing
contract13/0 and gate-report24/0 controls pass; copied74-file runtime/views pass
both modes without binary/materials. Close the a42af monitor-decoding instrument
issue with a synthetic regression. Canonical authority selection/entrypoint,
exact manifest, capture and full policy remain pending; no qualification credit.

Validation:17 focused checks/seven books/one two-mode example/three rendered
surfaces pass.1564 protected files/1Gitlink/91 prior entries and all old probes
exact; production differs only by two guards/registration. Six whole task records
3112B/three inverse stages/eight damaged refusals; DEV0363 retains whole3810B entry.
Teaching fits the bounded capture-plan; all old caps fixed. LIVE derives1617arms
only;42routes,CPU14/18,BOARD10/12,replay4/4green unchanged.

## SEMULITH-P4-0274 (leaf P4-SYSTEM.14) — retain bounded prepared DIV capture inputs

Retain four inputs totaling23315B through public image/schema/author owners: complete ELF,
matched config, baseline and sole wrong quotient. Add16 input controls and full
book reproduction examples, with no reference execution. Declare22-slot/16MiB
retention and exact future output names; final entrypoint/manifest/authorities
remain pending. Existing production code/caps and qualification stay unchanged.

Validation:16 positive controls/two modes and actual-loader omission5 losses/0
errors; copied75-file runtime/data gives22 expected outcomes, no binary/materials.
17 focused checks/seven books/three complete examples/eight rendered surfaces pass.
1551 other files/1Gitlink/93 prior entries and all existing production/probes exact.
Three task records2055B/source-owner inverses2/seven damaged refusals; CH0362 keeps
four whole oldest entries3787B. New family five files25990B fits declared bounds;
all old caps preserved. LIVE derives42 routes/1615arms only; CPU14/18,BOARD10/12,
replay4/4green. No canonical capture/qualification.

## SEMULITH-P4-0273 (leaf P4-SYSTEM.14) — publish the selected canonical Sail descriptor

Retain the711B selected Sail identity with explicit publication metadata and
verify exact bytes/current binding offline. Add11 publication controls and a
complete book example; preserve all old Python/probes and their omission losses.
Final entrypoint/output retention/manifest/policy remain pending. No canonical
capture or qualification.

First hook exposed a stage-sensitive GS digest; regenerate through its owner,
repeat the staged report check and retain the whole oldest DEV entry in0361.

Validation:76 normal/O outcomes/0 errors, old omission losses exact; copied69-file
runtime/data set gives12 expected outcomes, no acquired binary/materials.
16 focused checks/seven books/six complete examples/six rendered surfaces pass.
1549 other files/1Gitlink/92 prior entries exact; four whole records3622B,
source-owner inverses2/eight damaged refusals. Source review35/27/63/66files965026B
unchanged; profiles524files3142395B fits unchanged caps. LIVE derived1613 only;
CPU14/18,BOARD10/12,replay4/4green. No canonical capture/qualification.

