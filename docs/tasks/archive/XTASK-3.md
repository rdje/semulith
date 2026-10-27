# XTASK ordinary history — part 3

Ordinary, directly readable task history: the narrative paragraphs of the closed `XTASK.6` slices 6a–6aa (with 6r-b) from the
leaf's Task Tree node, retained verbatim from `docs/tasks/XTASK.md` as staged for `SEMULITH-XTASK-0038` on top of commit
`4d6a890fa1060d134d0a55eb32e81150f81951dc` (one contiguous span, one anchor). The live tree keeps one pointer line in the node; the open
slices' paragraphs stay live. Relative links inside the retained text are written from `docs/tasks/`, their
original base. No seal, reader or inverse map is involved: moving closed records verbatim into an ordinary
archive part is the task family's standing mechanism (decision_containment-reset, 2026-10-21); XTASK.6 slice
6ab, SEMULITH-XTASK-0038.

| Span | Bytes | SHA256 |
| --- | --- | --- |
| slice paragraphs 6a–6aa (with 6r-b) | 55667 | `6c8448db748460e7722336f6f4d035d83d16f18466ff2f27cd4586693b605093` |
<a id="slice-paragraphs-6a-to-6aa"></a>

## slice-paragraphs-6a-to-6aa

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
  Slice 6r-b (`2026-10-27`, `SEMULITH-XTASK-0031`; on clean 01a257bb; registry, record and card only): the knowledge family's
  second re-derivation and the 6r card. `README-ROUTES` refused the card at 133,410 B against `docs/knowledge/`'s 131,072 B
  aggregate ceiling (41 files against 40); the family's health line (34 files / 114,688 B) had fired at the 35th card on 2026-10-23
  and printed on every gate since — four slices added cards above it without the raise the first re-derivation's rule put on the
  leaf whose lesson reaches the line (§15: I read the health line as noise). `docs/decisions/decision_knowledge-family-second-rederivation.md`
  re-derives the bounds with the numbers — ceiling 56 files / 180,224 B, health 48 / 157,696, per-part 16,384 unchanged (0.73× at
  staging, the precedent's headroom) — and `doctrine/readme_routes.tsv`'s row carries them; the card
  `docs/knowledge/a-crash-that-exits-one-reads-as-an-absence.md` (6r's §9: a probe whose "absent" exit code is Python's crash code)
  lands with its INDEX row. Measured after the edit: `bash scripts/check_readme_routes.sh` rc 0 with no `docs/knowledge/` line
  (41 files, 133410 B against 48 / 157,696). The slice runners now print the routes check's `health:` lines for the family in
  their prechecks. Next: slice `6v` — `check_board_gen.sh` behind a held shim (its generator `gen_board.py` spawned as before).
  Slice 6v (`2026-10-27`, `SEMULITH-XTASK-0032`; on clean 47a05592, taken out of turn — no feature leaf unblocked): `BOARD-GEN`'s driver
  is Rust — `xtask/src/check_board_gen.rs` (348 lines) ports the bash driver line for line: the generator `scripts/gen_board.py`
  spawned exactly as the driver spawned it (`--check` over every tracked board; the self-test's derivations over a scratch copy of
  the real definition), NOT ported; the controls the same — the seven artifacts emitted, two derivations byte-identical (the
  script's `diff -r` as a recursive byte comparison), a faithful generation in sync, three hand-edited artifacts and a moved
  definition named as DRIFT, an overlapping region and an undeclared device refused at generation; the nine bash arms are nine
  `tally.arm(` calls (one arm's "no output" form kept; the first draft folded three into a loop, which the arm counter cannot see —
  unrolled before measuring), the arm total unchanged; `scripts/check_board_gen.sh` a shim of `cargo xtask check-board-gen`. Measured in
  a disposable draft crate: the self-test `9 pass / 0 fail` with stdout and stderr byte-identical to the bash driver's, the real
  tree's stdout and stderr byte-identical (`BOARD-GEN: ok (1 board(s) — manifest, composed catalogues, hardware description and map
  all byte-exact functions of the canonical definition)`), and 5 scratch fixture repositories (the whole corpus copied in) —
  one board, no board, two boards, a stale artifact, a moved definition — 5 identical, 0 differ in stdout, stderr and exit status. In tree:
  `cargo test -p xtask` `test result: ok. 17 passed`; clippy at deny-warnings rc=0 (clean on the first in-tree run). Next: slice `6w` — `check_platform_gen.sh` behind a held shim
  (its generator `gen_platform.py` spawned as before).
  Slice 6w (`2026-10-27`, `SEMULITH-XTASK-0033`; on clean 42bd2f11, taken out of turn — no feature leaf unblocked): `PLATFORM-GEN`'s
  driver is Rust — `xtask/src/check_platform_gen.rs` (432 lines) ports the bash driver line for line: the generator
  `scripts/gen_platform.py` spawned exactly as the driver spawned it, NOT ported; the eleven controls over a scratch copy of the real
  board (the manifest emitted, two derivations byte-identical, a faithful generation in sync, a hand-edited manifest and a moved
  definition named as DRIFT, a stale dossier pin, a profile without endianness, a load-region that is not RAM, a console claim the
  wiring contradicts, a missing time obligation and an invented time source refused by name) — the script's `sed` and Python edits
  as the same first-occurrence replacements, the 64-hex pin rewrite as a scan; the eleven bash arms are eleven `tally.arm(` calls,
  the arm total unchanged; `scripts/check_platform_gen.sh` a shim of `cargo xtask check-platform-gen`. Measured in a disposable draft
  crate: the self-test `11 pass / 0 fail` with stdout and stderr byte-identical to the bash driver's, the real tree's stdout and
  stderr byte-identical (`PLATFORM-GEN: ok (1 board(s) — the platform capability manifest is a byte-exact function of its canonical
  inputs, the dossier pin verified live)`), and 5 scratch fixture repositories (the whole corpus copied in) — one board, no
  board, two boards, a stale manifest, a moved definition — 5 identical, 0 differ in stdout, stderr and exit status. In tree: `cargo test -p
  xtask` `test result: ok. 17 passed`; clippy at deny-warnings rc=0 (clean on the first in-tree run). Next: slice `6x` — `check_state_gen.sh` behind a held shim (its generator
  `gen_state.py` spawned as before).
  Slice 6x (`2026-10-27`, `SEMULITH-XTASK-0034`; on clean 909d1925, taken out of turn — no feature leaf unblocked): `STATE-GEN`'s
  driver is Rust — `xtask/src/check_state_gen.rs` (556 lines) ports the bash driver line for line: the generator
  `scripts/gen_state.py` spawned exactly as the driver spawned it for the two descriptor/module pairs, NOT ported; the twenty-nine
  controls over scratch copies of the real descriptor and arithmetic module and the script's own rv64gc descriptor template
  (embedded verbatim, its one `(field …)` argument substituted) — emission, sync, a hand-edited module, an XLEN disagreement, an
  unmapped register, a missing census, the three shapes the RV64 path refuses on both descriptors, a descriptor without xlen, four
  censuses silent on a present candidate, the real rv64gc pair in sync and catching a hand edit, a CSR without its reset, a view
  of nothing, four field-table refusals, a duplicate address, a CSR under rv64i — the script's `sed` and Python edits as the same
  first-occurrence replacements (the census remover as the same paren-depth scan); the twenty-nine bash arms are twenty-nine
  `tally.arm(` calls, the arm total unchanged; `scripts/check_state_gen.sh` a shim of `cargo xtask check-state-gen`. Measured in a
  disposable draft crate: the self-test `29 pass / 0 fail` with stdout and stderr byte-identical to the bash driver's, the real
  tree's stdout and stderr byte-identical (two `STATE-GEN: ok (… matches …, sha256 …)` lines, the digest through the harness's
  hasher), and 5 scratch fixture repositories (scripts, profiles, schemas and the core crate's sources copied in) — in
  sync, a hand-edited module, a hand-edited rv64gc module, the descriptor missing, a census silent on the reservation — 5 identical, 0 differ
  in stdout, stderr and exit status (§9, the script's and reproduced, as 6u's: the controls judge the LIVE rv64gc pair, so a
  hand-edited live `state_rv64gc.rs` or a live census edit refuses the check as non-discriminating — exit 2 — instead of failing
  by name; an open question beside 6u's). CHANGELOG.md, at 57071 B against its 65,536 B ceiling, is sharded in this unit ahead
  of the ceiling (`scripts/shard_history.py --max-bytes 49152`: `docs/changelog/shard-0418.md` sealed, the head 48531 B before this entry). In tree:
  `cargo test -p xtask` `test result: ok. 17 passed`; clippy at deny-warnings rc=0 (clean on the first in-tree run). Next: slice `6y` — `check_interaction_matrix.sh` behind a held shim.
  Slice 6y (`2026-10-27`, `SEMULITH-XTASK-0035`; on clean b80d1103, taken out of turn — no feature leaf unblocked): `INTERACTION-
  MATRIX`'s driver is Rust — `xtask/src/check_interaction_matrix.rs` (379 lines) ports the driver's inline Python line for line:
  every tracked unit judged by `scripts/check_interaction_matrix.py`, the pinned Python judge, spawned exactly as the driver spawned
  it and NOT ported, its report lines prefixed with the unit and its findings kept as the Python kept them; the controls write the
  script's synthetic unit (a profile, two guests, a references document, a matrix — the cell texts taken from the script); the
  fifteen bash arms are fifteen `tally.arm(` calls, the arm total unchanged; `scripts/check_interaction_matrix.sh` a shim of
  `cargo xtask check-interaction-matrix`. Measured in a disposable draft crate: the self-test `15 pass / 0 fail` with stdout and
  stderr byte-identical to the bash driver's, the real tree's stdout and stderr byte-identical (the cell report of every unit and
  `INTERACTION-MATRIX: ok (5 unit(s) — …)`), and 4 scratch fixture repositories (scripts, profiles and schemas copied in) —
  the corpus, a unit with no matrix, an orphan guest, no units — 4 identical, 0 differ in stdout, stderr and exit status. `docs/tasks/XTASK.md`, at
  126735 B against its 131,072 B per-part ceiling, has the closed rows 6p–6x (6r-b among them; 21985 B, one contiguous span of
  60 rows) moved verbatim into `docs/tasks/archive/XTASK-2.md` (the a43b mechanism, as 6q's part 1: SHA256 in the part's table, one
  pointer left in the checklist; the live leaf 104842 B before this slice's text). In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at
  deny-warnings rc=0 (clean on the first in-tree run). Next: slice `6z` — `check_unit_books.sh` behind a held shim.
  Slice 6z (`2026-10-27`, `SEMULITH-XTASK-0036`; on clean f1aa78ef, taken out of turn — no feature leaf unblocked): `UNIT-BOOKS`'s
  driver is Rust — `xtask/src/check_unit_books.rs` (310 lines) ports the bash driver line for line: the judge
  `scripts/unit_books.py` spawned exactly as the driver spawned it over a fresh `mdbook` bundle (the `mdbook` preflight kept), NOT
  ported; the controls write the script's synthetic registry, project book and unit books (eighteen arms — no registry, a unit
  without its book, a building book, an orphan book, a book without its SUMMARY, one that does not build, the catalogue missing
  and wrong, six include defects, two rendered-link defects, an absolute book path, an empty registry) and run the script's four
  probe invocations scored as it scored them (not arms — the counter counts neither side's); the eighteen bash arms are eighteen
  `tally.arm(` calls, the arm total unchanged; `scripts/check_unit_books.sh` a shim of `cargo xtask check-unit-books`. Measured in a
  disposable draft crate: the self-test `22 pass / 0 fail` with stdout and stderr byte-identical to the bash driver's, the real
  tree's stdout and stderr byte-identical (`UNIT-BOOKS: ok (6 units + project book; catalogue and 3720 rendered hyperlinks checked
  in fresh bundle)`), and 4 scratch fixture repositories (scripts, the registry, the books and the navigation probe's
  documents copied in) — the corpus, an orphan book, no registry, a broken rendered link — 4 identical, 0 differ in stdout, stderr and exit
  status. In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at deny-warnings rc=0 (clean on the first in-tree run). Next: slice `6aa` — `check_tree_claims.sh`
  behind a held shim.
  Slice 6aa (`2026-10-27`, `SEMULITH-XTASK-0037`; on clean 4b7a2dae, taken out of turn — no feature leaf unblocked): `TREE-CLAIMS`'s
  driver is Rust — `xtask/src/check_tree_claims.rs` (581 lines) ports the bash driver line for line: the inline Python judge
  (every live document's tree facts re-derived over the shared `task_source` reader, archived ranges and their declarations
  qualified) runs verbatim through `python3 -` as a string constant extracted from the script, NOT ported; the controls write the
  script's synthetic registry, live document and trees — its `tree` heredoc, `archive_fixture` and `source_edit` as the same
  texts and the same single replacement — through thirty-eight arms (counts, frontier pointers, tree status, missing documents
  and registries, bold and conditional statuses, duplicate and invalid sources, archived ranges whole, missing, incomplete,
  mis-populated, overlapping, repeated, unsafe or unsupported, leading ratios, a linked archive directory); the thirty-eight bash
  arms are thirty-eight `tally.arm(` calls, the arm total unchanged; `scripts/check_tree_claims.sh` a shim of `cargo xtask
  check-tree-claims`. Measured in a disposable draft crate: the self-test `38 pass / 0 fail` with stdout and stderr
  byte-identical to the bash driver's, the real tree's stdout and stderr byte-identical (`TREE-CLAIMS: ok (5 live document(s)
  state nothing the trees contradict)`), and 4 scratch fixture repositories (scripts, the routes registry, `docs/` and
  the top-level documents copied in) — the corpus, a drifted leaf count, no routes registry, a tree missing — 4 identical, 0 differ in
  stdout, stderr and exit status. In tree: `cargo test -p xtask` `test result: ok. 17 passed`; clippy at deny-warnings rc=0 (clean on the first in-tree run); the first chain refused by
  `PORT-WEB` — the controls' symlink stood unguarded for wasm32, gated `#[cfg(unix)]`, the digest and line count above re-stated,
  the chain re-run. Next: slice `6ab` —
  `check_frontier_sync.sh` behind a held shim.

