# XTASK ordinary history — part 6

Ordinary, directly readable task history: the narrative paragraphs of the closed `XTASK.6` slices 6ab–6av from the
leaf's Task Tree node, retained verbatim from `docs/tasks/XTASK.md` as staged for `SEMULITH-XTASK-0062` on top of commit
`a8d4d526785ba60f6ebf628d82614279ab0e6e7b` (one contiguous span, one anchor). The live tree keeps one pointer line in the node; the open
slices' paragraphs stay live. Relative links inside the retained text are written from `docs/tasks/`, their
original base. No seal, reader or inverse map is involved: moving closed records verbatim into an ordinary
archive part is the task family's standing mechanism (decision_containment-reset, 2026-10-21); XTASK.4 slice 4b,
SEMULITH-XTASK-0062.

| Span | Bytes | SHA256 |
| --- | --- | --- |
| slice paragraphs 6ab–6av | 43129 | `33922c5d73bb46303a3b52d142b151a3ebeb12ea3060776eb8e313d3321f520b` |
<a id="slice-paragraphs-6ab-to-6av"></a>

## slice-paragraphs-6ab-to-6av

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
  Slice 6ar (`2026-10-28`, `SEMULITH-XTASK-0054`; on clean 99b89790, taken out of turn — no feature leaf unblocked): `PROFILE-CONSISTENCY`'s
  driver is Rust — `xtask/src/check_profile_consistency.rs` (8828 lines, assembled from the script by
  `target/xtask/xt0053/gen_module.py` + `assemble.py`: the 51 fixture arms, the prober and the main path by hand, the 445 unrolled
  `score` probes and the 25 mode loops derived) ports the bash driver line for line: the 330-line inline Python judge (over the
  pinned dossier reader and verification modules) runs verbatim through `python3 -` as a string constant extracted from the
  script, NOT ported, its `--csr-cross` mode passed through; the four tools the real run consults first and the forty-odd probe
  suites spawned as the script spawned them; the controls' fixture surgery (`sed -i.bak`, range deletes, `grep -v`, the dossier
  strings composed from `BASE`) as the same literal text manipulation; the XTASK.8 prefetch kept in shape — a recording pass,
  `scripts/doctrine_prefetch.py` in parallel, the scoring pass answered from the record, the `PROFILE_CONSISTENCY_PREFETCH`,
  `…_MISSES` and `…_RECORD_ARGV` knobs honoured; the quiet run's output kept in `target/profile-consistency-selftest.log` with
  the MISS excerpt on a refusal; the 51 bash arms are 51 `tally.arm(` calls and the 494 bash `score` lines 494 `tally.score(`
  calls (the mode loops keep their one GREEN and one RED call each), the arm total unchanged; `scripts/check_profile_consistency.sh`
  a shim of `cargo xtask check-profile-consistency`. Measured in a disposable draft crate: the self-test `1164 pass / 0 fail` with stdout
  and stderr byte-identical to the bash driver's, the real tree's stdout and stderr byte-identical (`PROFILE-CONSISTENCY: ok (5 profile dossier(s) internally consistent)`), and 2 scratch fixture repositories — a clone of the repository, a profile's declared count edited away from its enumeration — 2 identical, 0 differ in stdout,
  stderr and exit status. In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at deny-warnings rc=0 (clean on the first in-tree run). Every pinned-module caller now
  answers through a shim; `check_readme_routes.sh` (PATH-shadowing tool fixtures) stays the one deferred driver. Next: slice `6as` —
  `check_readme_routes.sh` behind a held shim, or the leaf's closing review.
  Slice 6as (`2026-10-28`, `SEMULITH-XTASK-0057`; on clean 69d90094, taken out of turn — no feature leaf unblocked): the leaf's running
  driver count is re-derived, and `DERIVED-COUNTS` now owns it. From slice 6ai on, every slice's docs script stated `N of 42 drivers
  through shims` in `docs/TASK_TREE.md` and `MEMORY.md`, and 6ai's `42` was itself a miscount — the project registry holds 41 drivers
  (`grep -cE '^  "[A-Z]' scripts/check_doctrines.project.sh` = 41) — so the claim drifted through twelve slices unchecked (§15, an own
  defect: a running total, the founding defect class of `DERIVED-COUNTS`). `xtask/src/check_derived_counts.rs`'s claims table gains two
  rows on the live phrase `N of M drivers through shims` — the shim count (registered paths whose text runs `exec cargo xtask`) and the
  registry size — observed RED on the live documents before the correction (four `COUNT DRIFT` findings, `MEMORY.md` and
  `docs/TASK_TREE.md`: 38 against 39, 42 against 41) and GREEN after it. 39 of 41 drivers answer through shims today; `README-ROUTING-CLOSURE`
  and `SEAM-INTEGRITY` are the two in bash. The closed slices' paragraphs and acceptance rows keep the numbers they stated, and the CHANGELOG
  entries are frozen — both are history. In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at deny-warnings rc=0. Next: slice `6at` —
  `check_readme_routes.sh` behind a held shim. Its controls shadow `git`, `wc`, `python3`, `sort` and `grep` on `PATH` and redefine five shell
  functions inside subshells, so the port spawns the same tools where the script did and carries the redefinitions as seams of its own —
  a design settled first, in that slice.
  Slice 6at (`2026-10-28`, `SEMULITH-XTASK-0058`; on clean 8a493254, taken out of turn — no feature leaf unblocked): `README-ROUTING-CLOSURE`'s
  driver is Rust — `xtask/src/check_readme_routes.rs` (1923 lines) ports the bash driver line for line, and the design is this: the three
  Python programs the script ran on `python3 -`'s stdin (the link parser, the family measure, the registry reader) run verbatim, NOT ported;
  `wc` (through the checked scalar-count rules of `scripts/read_text_metrics.bash`: status, stderr and shape), the README guard and the
  hint pipeline (`grep -oE | tr | sort -u` under `pipefail`, through `bash -c`) are spawned as the script spawned them, every child of a
  fixture under that fixture's exported environment — so the controls' `PATH`-shadowed `git`, `wc`, `python3`, `sort` and `grep` meet
  the same calls; the five shell functions the controls redefined in subshells (the family measure, the registry reader, the
  regeneration-set check, the hint producer, the row reader called alone) are a `Seams` value only the self-test sets; output keeps
  the shell's order (stdout and stderr tagged, merged where an arm wrote `2>&1`, stdout alone where the entry flow captured it). The
  ninety-four bash arms are ninety-four `tally.arm(` calls, the arm total unchanged; `scripts/check_readme_routes.sh` a shim of `cargo
  xtask check-readme-routes` that keeps the scratch preamble `probe_temporary_locality.py` reads. Measured in a disposable draft crate:
  the self-test `94 pass / 0 fail` with stdout and stderr byte-identical to the bash driver's (6 s against 12 s), the real tree's stdout
  and stderr byte-identical (`README-ROUTING-CLOSURE: ok (44 governed destination(s))`), and 4 scratch fixture repositories — a
  clone of the repository, an ungoverned link added to the landing page, `LIVE_STATUS.md` grown past its byte ceiling, a malformed
  registry row (refused) — 4 identical, 0 differ in stdout, stderr and exit status. In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at deny-warnings
  rc=0 (clean on the first in-tree run). 40 of 41 drivers through shims now — and the claim row slice 6as added held its first run: the run script checked the counts
  before its docs step, `DERIVED-COUNTS` refused the applied tree (the documents still said 39, the registry already 40), and the slice
  was finished with the docs first and the counts after them. `SEAM-INTEGRITY` waits on the readers of `GAP-CLAIM-CENSUS`, a universal
  spine check. Next:
  slice `6au` — the leaf's closing review.
  Slice 6au (`2026-10-28`, `SEMULITH-XTASK-0059`; on clean 94de1c7b, taken out of turn — no feature leaf unblocked): `SEAM-INTEGRITY`'s driver
  is Rust — `xtask/src/check_seam_integrity.rs` (636 lines) ports the bash driver line for line, and the closing review that 6at named
  moves to slice 6av: its first measurement found the stated hold weaker than the leaf said. `SEAM-INTEGRITY` READS `GAP-CLAIM-CENSUS`'s
  text (its `CENSUS_RE`, for the vocabulary rule R5), and that driver stays bash — so nothing blocked the port; the 6r-era phrase "waits
  on `check_gap_claims.sh`'s readers" had been carried forward unexamined. The port asks the owner for its effective rules as the script
  did (`scripts/check_task_acceptance.sh --print-sig`, `--print-code-re`), extracts the built-in defaults and the census list from the
  scripts' text as its `sed` did, runs the box scoper (`awk`) verbatim per task file and every pattern test through the shell's own
  `grep -E`, and the verdict line's box count through the script's own pipeline; the nineteen bash `score` lines are nineteen
  `tally.score(` calls, the arm total unchanged; `scripts/check_seam_integrity.sh` a shim of `cargo xtask check-seam-integrity` that keeps
  the scratch preamble the locality probe reads. Measured in a disposable draft crate: the self-test `19 pass / 0 fail` with stdout and
  stderr byte-identical to the bash driver's, the real tree's stdout and stderr byte-identical (`SEAM-INTEGRITY: ok (1843 current tracked
  acceptance box(es) …)`), and 4 scratch fixture repositories — a clone of the repository, a seam file emptied (refused: the controls
  no longer discriminate), an acceptance box without evidence, a prose file the classifier over-matches — 4 identical, 0 differ in stdout, stderr and
  exit status. In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at deny-warnings rc=0 (clean on the first in-tree run). 41 of 41 drivers through shims: every driver of
  the project registry. Next: slice `6av` — the leaf's closing review, which weighs the four checks the universal registry runs from
  project-owned scripts (`MEMORY-ARCH`, `README-STABILITY`, `TASK-ACCEPTANCE`, `GAP-CLAIM-CENSUS`): the spine's registry, two of them
  carrying source fixes owed upstream (`scripts/update_scaffold.sh`'s note, `reference_upstream-spine-defects.md`).
  Slice 6av (`2026-10-28`, `SEMULITH-XTASK-0060`; on clean 476146b4, taken out of turn — no feature leaf unblocked): the leaf's closing
  review, documentation only (target/xtask/xt0060/census.sh → census.txt). The project registry holds 41 drivers (`grep -cE '^  "[A-Z]'
  scripts/check_doctrines.project.sh` = 41) and every one of their scripts is a shim (`exec cargo xtask` in 41 of 41), the count
  re-derived by `DERIVED-COUNTS`; every arm total held through its port. The leaf's inventory (target/xtask/xt0004/drivers.md, 55
  rows) reconciles: 41 ported, 7 spine scripts `scripts/update_scaffold.sh` re-syncs (`NEUTRAL`), the registry comment's placeholder
  path, two outside the port — `knowledge-map/scripts/check_knowledge_map.sh` ("a submodule, read-only" as first recorded — wrong:
  ordinary tracked bash, the universal registry's conditional `KNOWLEDGE-MAP` check; corrected in slice 4b) and
  `scripts/check_doctrines.project.sh` (the runner, `XTASK.8`'s) — and four scripts the UNIVERSAL registry runs from copies the project
  owns: `MEMORY-ARCH`, `README-STABILITY`, `TASK-ACCEPTANCE`, `GAP-CLAIM-CENSUS`. Those four stay bash (`decision_universal-registry-checks-stay-bash.md`): none of the
  eleven universal scripts invokes cargo (two `cargo` lines in all eleven, both evidence vocabulary), so the spine runs on bash, git
  and python3 alone in any clone; each of the four is read or run as TEXT outside the crate — the orientation qualifier writes the
  memory check into a crate-less fixture, mutates it and runs it; README-ROUTES copies the README guard into its fixtures;
  SEAM-INTEGRITY asks the acceptance check for its rules and reads the census vocabulary from the gap check; the handoff census holds
  all four across a scaffold sync — and two carry source fixes owed to the bash template upstream. The open questions of 6r, 6u and 6x
  stay in this tree's Open Questions, their doctrine owners' to answer; none blocks the close. Leaf done. Next: the tree's frontier is
  `XTASK.4`.

