# XTASK ordinary history — part 7

Ordinary, directly readable task history: the narrative paragraphs of the closed slices of `XTASK.11` and `XTASK.12` and of `XTASK.13` slices a to b3, retained verbatim
from `docs/tasks/XTASK.md` as staged for `SEMULITH-XTASK-0080` on top of commit `18a09566408b1d78d24ee2c0eb83b7ef19eed3bc`. The live tree keeps one pointer line per node. Relative links inside the
retained text are written from `docs/tasks/`, their original base. No seal, reader or inverse map is involved: moving closed records verbatim into an ordinary archive part is the
task family's standing mechanism (decision_containment-reset, 2026-10-21).

| Span | Bytes | SHA256 |
| --- | --- | --- |
| slice paragraphs 11a-11e | 6877 | `8b0715e43ae3abc89df770670381f2e1e3736fc8e1973191d02471235cbd7bf7` |
| slice paragraphs 12a-12c | 4160 | `98eb56be6e3d6d0f9639aae6cce9f68a5ee3e2baa70ea44593ffd602acc41716` |
| slice paragraphs 13a-13b3 | 9501 | `376d11fbe3fca43d5173c4b4fc558d981b1e7feed48aba4700d4ba5f18200b2d` |

<a id="slice-paragraphs-11a-to-11e"></a>

## slice-paragraphs-11a-to-11e

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

<a id="slice-paragraphs-12a-to-12c"></a>

## slice-paragraphs-12a-to-12c

  Slice a (`2026-10-28`, `SEMULITH-XTASK-0069`; on clean 474efaa6; evidence target/xtask/xt0069): the granted push's hosted run
  confirmed the ARTIFACT-COHORT fix and refused on `UNIT-BOOKS: REFUSED — the check does not discriminate (self-test failed)` —
  with nothing more, because `check_unit_books.rs` printed a miss only in a verbose run. Its inputs did not change between the
  passing hosted run (b917d1ba) and this one (`git diff --stat` empty over docs/book, materials, docs/models and its scripts), and
  here it passes (`22 pass / 0 fail`): the cause is not yet known. The driver's tally now keeps every miss and a quiet run prints
  them before the refusal line; verbose output is unchanged. RED: the navigation probe made to exit 1 (restored byte-identical) —
  the quiet run prints `UNIT-BOOKS navigation probe failed` and the probe's own line, then the refusal. A census found 28 more
  drivers whose quiet refusal hides its misses (quiet-miss.txt): slice b. Own slip, recorded: this slice's edit, build and RED ran
  while slice e's commit gate was running — the gate passed, and this slice's gate re-validates the tree.
  Slice b (`2026-10-28`, `SEMULITH-XTASK-0070`; on clean 18bfc69c, pushed as SEMULITH-PUSH-0004; evidence target/xtask/xt0070): the
  28 other drivers the census found get the same report path, by one transformation (transform.py; each step had to match once
  per file, every touched file backed up in before/): each `Tally` keeps a `misses` list, every guarded miss print goes through
  `report()` (printed at once when verbose, kept always), and a quiet self-test prints its misses before the caller's refusal;
  two literal-only reports became `.to_owned()` for clippy. Measured: a structural check over all 29 drivers (`misses.push`,
  the quiet loop, no verbose-only miss print left) 29 of 29; every self-test unchanged and green (selftests.txt: 29 of 29 rc=0,
  the same pass counts, from `BOARD-GEN 9` to `README-ROUTING-CLOSURE 94`); RED on the tree, each restored byte-identical
  (red/): the frozen STATE-GEN module, the frozen board and the live rv64gc definition module hand-edited — each quiet run now
  prints `… self-test MISS: GREEN …` before its refusal (1, 2 and 1 lines). The last one is open question (e) in miniature: a
  live module edit refuses DEF-GEN instead of failing it by name. The leaf is done once the hosted run is green.
  Slice c (`2026-10-28`, `SEMULITH-XTASK-0071`; on clean 447ad5f9; evidence target/xtask/xt0071): the hosted run of slice a's push
  (40763391753 on 18bfc69c) named the miss — `probe_book_includes.IncludeTests.test_another_volume_and_changed_input_refuse`,
  line 230, `AssertionError: 3 != 1`. The test patched `Path.stat` and asserted the include target was stat'ed exactly once, and
  a sibling assertion counted `Path.lstat` calls; how many pathlib calls reach those methods is the interpreter's (3.11 and 3.12
  route `is_symlink()`, `exists()` and `stat()` through `Path.stat`: 3; 3.14 only `stat()`: 1). The runner's `python3` is 3.12,
  this host's 3.14. Reproduced exactly here under Python 3.12.15 (installed beside the default) and 3.11: `3 != 1`. The test now
  holds the property — the refusal names `another volume` and the source is never opened (an `os.open` spy), the change test's
  refusal names `changed` — with `calls >= 1` (and `>= 2`) proving the patch was consulted. RED: the volume refusal removed from
  `book_paths.source_path` and `book_includes` (restored byte-identical) fails the test on 3.11 (wrong reason) and 3.14 (no
  refusal). Parity: the whole doctrines suite with `python3` resolving to 3.12 — `=== all doctrines green ===` (13 checks,
  1224 s). `probe_book_navigation.py`'s deep-nesting test fails on 3.11 only (exit 1 against 2), not on the runner's 3.12:
  noted, out of scope. Card: `docs/knowledge/a-count-of-pathlib-calls-tests-the-interpreter.md`.
  Closed (`2026-10-29`): the push of this slice (cefb0d84, SEMULITH-PUSH-0005) turned the hosted doctrines run green —
  40782096575 `=== all doctrines green ===`, rust 40782096560 success — the first green hosted doctrines run since 2026-10-08.

<a id="slice-paragraphs-13a-to-13b3"></a>

## slice-paragraphs-13a-to-13b3

  Slice a (`2026-10-29`, `SEMULITH-XTASK-0073`; on clean 1067faed; evidence target/xtask/xt0073): `DEF-GEN`'s controls judge
  a frozen copy. `scripts/fixtures/def-gen/` mirrors the repository's layout (25 files, 440 KB): both units' `encoding.sexp`
  and `state.sexp`, the twenty `definitions/riscv` fragments and `crates/semulith-core/src/definition_rv64gc.rs` regenerated
  at its fixture path (`gen_definition.py --check` rc=0 over the frozen pair; its body equals the live module's but for the
  input paths its manifest records). Every control reads `FIXTURE` — the surgical rv64i unit, the staged rv64gc compositions,
  the fence mutator (it now takes its source as an argument instead of opening the live `system.sem.sexp`) and the census's
  in-sync and hand-edit arms — and `scripts/probe_c_engine.py` gains `--data-root` (default the repository; the engine it
  compiles is always the tracked one), which the controls point at the copy. The absence branch the freeze exposed: `run`
  printed "ok (no encoding composition yet)" when the rv64i encoding was missing, which a deleted live encoding would now
  reach; a generated module whose encoding or state descriptor is absent is now an orphan, failed by name. Measured on the
  real tree, the binary before and after (red.txt, the tree restored, 0 paths changed): `in-sync` 0 → 0;
  `gc-module-hand-edited`, `fragment-edited` and `encoding-missing` 2 (REFUSED, self-test failed) → 1, each named;
  `fragment-missing` 2 → 2, now the generator's named refusal (`fragment 'riscv/system' has no semantics document`), never
  the self-test's. `DEF-GEN --self-test: 56 pass / 0 fail` before and after. Next: slice b, GUEST-GEN.
  Slice b1 (`2026-10-29`, `SEMULITH-XTASK-0074`; on clean e32cc645; evidence target/xtask/xt0074): `GUEST-GEN`'s census
  and surgical controls judge frozen mini corpora. A whole frozen copy would be 3 MB (the rv64i set 512 KB, the rv64gc
  set 2.5 MB with a 1 MB fixture), so `scripts/fixtures/guest-gen/` holds what the arms use: three rv64i guests
  (smoke-arith, guest-control, smoke-trap — the surgical arms' own) and three rv64gc guests (smoke-arith, bound-arith,
  c-alu) with their byte fixture regenerated at its path, each corpus with its own run-order record, composed over DEF-GEN's
  frozen definitions (one frozen canonical definition, not two); 92 KB. The census's in-sync arm judges the frozen pair
  (`run` judges the live pairs), its hand-edit arm edits a copy of the frozen fixture. `run` has no absence branch to expose
  (it always judges both pairs and the mirror). Measured on the real tree, before → after (red.txt, restored, 0 paths
  changed): `in-sync` 0 → 0; `gc-fixture-hand-edited` 2 (self-test failed) → 1, named; `gc-guest-missing` and
  `rv64i-guest-unassemblable` 2 → 2, still through the self-test — the three base-mirror arms (the live owner/mirror pair)
  and the parcel-count arms (the full live census) still read the live corpus, slice b2's scope, named by the after
  binary's MISS lines. `GUEST-GEN --self-test: 400 pass / 0 fail` before and after. Next: slice b2 (the mirror arms over a
  frozen self-consistent pair — the checker hard-codes seven re-derivations and three pinned source re-derivations — and
  the census arms).
  Slice b2 (`2026-11-02`, `SEMULITH-XTASK-0075`; on clean 7b1a8f44; evidence target/xtask/xt0075): `GUEST-GEN`'s
  base-mirror and parcel-count arms judge frozen copies. `scripts/fixtures/guest-gen/base-mirror/` holds byte copies of
  the eight guests the mirror governor's predicates need, from both units (16 files, 69,445 B): its seven recorded
  re-derivations (three with pinned source re-derivations) and `bound-arith`, a count-only migration; under DEF-GEN's
  frozen rv64gc encoding the governor reads it `5 file(s) byte-identical, 1 … count-only migration(s), 7 recorded
  re-derivation(s), 3 pinned image-identical source re-derivation(s)` — every predicate the live pair exercises — and the
  census counts its 8 guests exactly. The three base-mirror arms judge the pair (`judge_mirror` takes its encoding; `run`
  keeps judging the live pair); the governor's seven self-test arms pass `--encoding` the frozen encoding, and
  `check_gc_mirror.py --self-test` takes its composition from that encoding's own root — the assembler reads the encoding
  and `definitions/` alone (measured over the four combinations of `profile.sexp` and `state.sexp`), so no other unit file
  is copied; the five parcel-count arms run `derive_gc_parcel_counts.py --encoding … --guests` the frozen mirror (its
  self-test's manifest census now over its own hand guests; `manifest()` fingerprints the unit it counts — the live
  manifest differs from HEAD's only in the tool's own digest). Measured, HEAD's checker over HEAD's tree (a worktree, the
  states applied there) against the slice's over the working tree, one live file damaged at a time (red-before.txt,
  red-invalid-before/*.after.*): `in-sync` before `398 pass / 2 fail` — the two `artifact_cleanup.Boundary: ('.app-data',
  'symlink')` misses the worktree's read-only link causes, in every before state — after `rc=0`; `gc-mirror-drift` before
  +2 base-mirror arms → after `rc=1`, `FAIL — …guests_rv64gc.rs is out of sync`, 0 misses; `rv64i-guest-unassemblable`
  before +3 base-mirror arms → after `rc=2`, the generator's own refusal naming `smoke-arith.s` and `zzz9`, 0 misses;
  `gc-guest-missing` before +8 (the 3 base-mirror and 4 parcel-count arms and the cold probe) → after `399 pass / 1 fail`,
  the one miss `GREEN parcel author controls use only tracked inputs`: `probe_gc_parcel_guest.py --cold` copies every
  tracked input and its legacy arm reads five live guests — slice b3. The first before run was invalid and is kept as
  such (red-invalid-before.txt): its binary, built in a worktree since removed, judged that worktree, because `cargo xtask`
  fixes its repository root at build time — knowledge card `an-xtask-binary-judges-the-tree-it-was-built-in.md`. Taken at
  the 5:1 turn between a43b-2c's declarations and a43b-2d's captures: none of the 100 paths frozen for the captures moved
  (`comm -12` of the changed and frozen sets = 0; both declarations still regenerate byte-identically). `GUEST-GEN
  --self-test: 400 pass / 0 fail` (the arm count unchanged; two arms renamed: `the base mirror holds on the frozen pair`,
  `the frozen parcel count census`). The two tool rows of `docs/toolbox/guest-evidence.md` were rewritten within its part bound (16,374 of 16,384 B; README-ROUTING-CLOSURE refused the first draft at 16,666): its next row partitions the family. The chain's focused stage refused once, `BOOK-INDEX` (the book's index derives from its text and the new doctrines-page section was not yet in it); regenerated by `gen_book_index.py`. Next: slice b3 (the parcel author probe's cold and legacy arms).
  Slice b3 (`2026-11-03`, `SEMULITH-XTASK-0076`; on clean b95a8f66; evidence target/xtask/xt0076): `GUEST-GEN`'s parcel author probe judges frozen copies.
  `scripts/fixtures/guest-gen/parcel-legacy/` holds byte copies of the five legacy guests (10 files, 102 KB), and the probe's staged composition reads
  DEF-GEN's frozen rv64gc encoding, state and definitions. `--cold` copies only what the probe reads now: the top-level `scripts/`, those frozen
  directories and `schema/`, not `definitions` and `profiles`; a deleted live guest used to raise "cold probe requires a regular tracked input". The state
  descriptor stays, measured: without it the probe passes only where the local reference cache is present, because CSR names then resolve through
  target/refs/riscv-opcodes/csrs.csv (`--cold` refused `mtvec` naming that path). The eight mutation arms keep their reasons (each `rc=1`, target/xtask/xt0076/m.*.out). Measured
  on the real tree, the binary before and after with the live file restored after each (red-before.txt, red-after.txt): `in-sync` 0 → 0; `gc-guest-missing` and
  `legacy-guest-missing` 2 → 2, from `REFUSED — the check does not discriminate` (1 and 2 arms missed) to the generator's own refusal naming the file (`gen_guests:
  REFUSED — …run-order.txt: lists c-alu — not on disk`), the self-test `400 pass / 0 fail` in every state; `legacy-expectation-edited` 1 → 1. The first after run was invalid
  and is kept as such (red-after-invalid-untracked-fixtures.txt): the new fixtures were untracked, and `--cold` copies tracked files. **Drafted and taken back:** a real-run
  step for `derive_rv64gc_expectations.py --check-owned`, moved out of this probe. Fired on the one state only it could name, an owned record hand-edited with its fixture
  regenerated, the tool itself reads `DRIFT — inj-walk-l0` but the check never reaches the step: `391 pass / 9 fail`, six more probes (`probe_gc_fetch`, `_author`,
  `_privilege_author`, `_integer_author`, `_counter_author`, `_cache_author`, with `_provenance` and `_owned_extent` beside them) still read the live owned corpus (red-owned.txt). A step that
  cannot be observed RED is not known to work (`TOOLBOX.md`), so it waits for those probes: slice b4, next at the 5:1 turn, a frozen owned corpus for them and then the real-run step. The
  corpus lost nothing here: the same six keep asserting `--check-owned` meanwhile. `GUEST-GEN --self-test: 400 pass / 0 fail` (the arm count unchanged). No path a case pins moved, and none
  is frozen at this turn: CSR-SET's declarations come after it. Next: slice b4.
