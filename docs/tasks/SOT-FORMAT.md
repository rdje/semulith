# SOT-FORMAT: one format for every source of truth, extensible without touching the reader

## Metadata

- Tree ID: `SOT-FORMAT`
- Status: `active`
- Roadmap lane: cross-cutting; the input side of the model generator engine
- Gate: contributes `SOURCE-FORMAT` — a source of truth outside the format is refused
- Depends on: `scripts/sexp.py` (the reader, already fired), `MODEL-COMPOSE.2` (fragments)
- Unlocks: record composition (`MODEL-COMPOSE.3`), every construct a future unit kind needs —
  register files, memory maps, pipelines, peripherals — without a parser change
- Created: `2026-09-14`
- Owner: repo-local workflow

## Goal

Make every source of truth the generator engine reads **one format**, S-expression, and make that
format **extensible by data**: a new construct is a new schema file, never an edit to the reader.

Director instruction, `2026-09-14`: *"Sources of truth shall be composables and extensibles to
support new constructs using the same format. for me S-expression or lisp-like is the simplest
format we can chose."*

⭐ This **supersedes** [`decision_canonical-definition-input`](../decisions/decision_canonical-definition-input.md),
which chose "the format its content actually wants" and kept records in JSON Lines and TOML. That
decision defended the split on the grounds that records are not trees. True, and irrelevant — the
question was never what shape the content is. **Composition is a merge, and three formats are three
merge semantics.** `encoding.sexp` composes today; `profile.toml` composes with nothing. The first
board that composes two processors must merge their requirements, obligations and pinned sources
too, and under the split there is no rule by which it could.

## Non-Goals

- **Not a Lisp.** The format is data: no `eval`, no macros, no quoting, no lambda. A reader that can
  execute its input is a reader that cannot be trusted to describe a CPU.
- **Not a new reader, and not a hand-written one.** `scripts/sexp.py` exists and is fired; this
  tree adds a *schema layer* above it and removes hard-coded construct lists from the tools. The
  **Rust** reader the engine will ship comes from **LinkedSpec** (`specs/Lispish.spec`, Rust
  backend), added as a **git submodule** — director instruction, `2026-09-14` — so no S-expression
  parser is written by hand in this project (`decision_one-format-every-source-of-truth`).
- **Not prose conversion.** Markdown documents are not engine inputs and stay Markdown.
- **Not JSON elimination as tidiness.** A file no engine reads — a fetched upstream artifact, a
  third-party log — is out of scope. The scope is exactly: *files the model generator engine
  extracts from*.
- Not a schema for schemas' sake: a construct is declared because a real file uses it.

## Acceptance Criteria

1. **One reader.** Every source of truth in scope parses with `scripts/sexp.py` and nothing else.
2. **The reader enumerates no construct**, and adding a **domain** construct — a register file, a
   memory map, a peripheral — requires a schema file and **zero lines of Python**. Proven by doing
   it. ⚠️ Stated precisely rather than over-claimed: extending the **schema language itself** with a
   new *kind* of declaration does change the validator. That boundary is the same one a database
   draws between adding a table and adding a column type, and it is named here so nobody later
   discovers it as a surprise.
3. **Undeclared is an error.** An unknown construct, an unknown field, a wrong arity or a wrong
   value type is refused **by name**, never ignored. `(sourcs "…")` is a well-formed S-expression
   and must be rejected as loudly as a syntax error.
4. **No gate loses discriminating power.** Every arm of `RECORD-SCHEMA` (15) and
   `PROFILE-CONSISTENCY` (39) that fires RED today still fires RED after the migration, against the
   converted files.
5. **Conversion is lossless and mechanically proven** — a round-trip comparison, not a review.
6. The schema language is **described in itself**, and its own description validates under it.

## Task Tree

- ID: `SOT-FORMAT.1` — **the schema language, written in itself**
  Status: `pending`
  Goal: declare what a construct is — its head, its fields, their arity and value types, whether
  they repeat — as S-expressions in `schema/`. Write the schema language's own schema in the schema
  language and validate it with itself: the fixpoint is what *proves* extensibility rather than
  asserting it.
  Acceptance: `scripts/check_sexp_schema.py` validates a file against a schema and names the
  offending construct/field on failure; `schema/schema.sexp` validates under itself; ≥ 6 arms fired
  RED (undeclared construct, undeclared field, missing required field, wrong arity, wrong value
  type, duplicated single-valued field); `schema/` registered in `doctrine/readme_routes.tsv` **in
  the same commit that creates it**.

- ID: `SOT-FORMAT.2` — **the constructs already in use, declared as data**
  Status: `pending`
  Goal: `encoding`, `fragment` and `semantics` get schema files. `scripts/check_semantics.py`'s
  hard-coded 32-form language moves out of Python and into `schema/`, so a new semantic form is a
  data change.
  Acceptance: the 32 forms are data; `52 of 52 declared instruction(s) have checked semantics` is
  reproduced **byte-identically**; the four controls of `MODEL-METHOD.9` still fire RED; adding a
  33rd form requires no Python edit (demonstrated, then reverted).

- ID: `SOT-FORMAT.3` — **the records: requirements and obligations**
  Status: `pending`
  Goal: convert `requirements.jsonl` (26) and `contract-obligations.jsonl` (34) to the format.
  Acceptance: round-trip proves losslessness field-by-field; `RECORD-SCHEMA`'s 15 arms are re-fired
  RED against the converted form; `scripts/validate_records.py` either reads the new format or is
  retired with its power transferred, and the transfer is demonstrated, not claimed.

- ID: `SOT-FORMAT.4` — **configuration, state and provenance**
  Status: `pending`
  Goal: convert `profile.toml` (26 decisions), `state.json`, `sources.toml`, `references.toml`, the
  reference override JSON and the guest expectation TOMLs.
  Acceptance: `PROFILE-CONSISTENCY`'s 39 arms re-fired RED, including rule 5b; `run_smoke.py` and
  `compare_platforms.py` produce identical verdicts; comments in the TOML sources survive as
  first-class form, since a comment-rich human-authored file was the original argument for TOML and
  losing it would be a real regression.

- ID: `SOT-FORMAT.5` — **record merge: the thing the split made impossible**
  Status: `pending`
  Goal: define and check the union of two units' records across a composition boundary —
  requirements, obligations, sources — with conflict detection, the way encodings already union.
  Acceptance: two units compose their records or are rejected with the conflicting fact named;
  fired RED on a genuine contradiction; feeds `MODEL-COMPOSE.3`'s assumption/guarantee discharge,
  which can then read one format.

- ID: `SOT-FORMAT.6` — **the `SOURCE-FORMAT` gate, and the superseding record**
  Status: `pending`
  Goal: a doctrine gate that refuses a source of truth outside the format, so the split cannot
  return by accident. Supersede `decision_canonical-definition-input` in place; update the mdBook.
  Acceptance: gate registered in `scripts/check_doctrines.project.sh` with a `--self-test` fired RED
  before registration; the superseded decision carries its replacement and its reason; mdBook and
  `DOCTRINE_ENFORCEMENT.md` mirror the registry (checked by `REGISTRY-MIRROR`, not by eye).

- ID: `SOT-FORMAT.7` — **the reader corrupts every non-ASCII string, and has no self-test**
  Status: `done`
  Goal: fix `scripts/sexp.py`'s string decoding and give the reader the self-test it never had.
  Found while designing `.1`, by reading the reader before building on it.
  Acceptance: the 52 citations in `rv64i.sem.sexp` round-trip byte-identically; unknown escapes are
  refused rather than guessed; `sexp.py --self-test` exists with ≥ 10 arms, fired RED before the
  fix; no tracked file's content changes, because the files were always right.
  Verification: `18 pass / 0 fail` (was `15 pass / 3 fail`); 52 of 52 citations verbatim; no
  consumer's verdict moved.
  Commit: `SEMULITH-SF-0041`

- ID: `SOT-FORMAT.8` — **the book does not describe the format it calls a contract**
  Status: `pending`
  Goal: the mdBook chapter *"Architecture and canonical definitions"* includes `docs/ARCHITECTURE.md`,
  which names no format, no `definitions/` directory and no composition — four commits introduced
  all three. The director's only window shows none of it. Close the drift at the source document,
  not in the chapter preface.
  Acceptance: `docs/ARCHITECTURE.md` describes the format, the fragment, the composition operator
  and the schema layer in prose; the book builds; `grep -c 'S-expression' docs/ARCHITECTURE.md` is
  non-zero where it is currently 0.

- ID: `SOT-FORMAT.9` — **the Rust reader comes from LinkedSpec, as a submodule**
  Status: `blocked`
  ⛔ Blocker, `2026-09-20`: **the two readers do not agree, and the cause is upstream.** Four of
  five tracked files agree node-for-node; `materials/catalog.sexp` does not, because a
  double-quoted string containing LF is not read as one string by `specs/Lispish.spec`. Root cause
  located (lines 69/71, `.` without DOTALL), one-line fix written and validated — 8 of 8
  reproduction cases and all five files agree under it — and reported to LinkedSpec at
  `docs/upstream/linkedspec/LS-001-multiline-string/`. It is **their change to make**: patching the pinned
  submodule is how a pin becomes a fork, which is the thing this leaf exists to avoid.
  ⚠️ Everything else in this leaf is delivered and committed. The leaf is not `done` because its
  acceptance says the readers agree on EVERY tracked file, and they do not. Moving that line to
  fit the result would be the only real failure available here.
  Unblocked `2026-09-20`: LinkedSpec published its integration document for downstream consumers
  at commit `ad290bdb4`. The blocker recorded on `2026-09-14` — that integrating against an
  unpublished contract means integrating against today's internals, which is how a submodule
  becomes a fork — is discharged, not waived.
  Goal: `vendor/linkedspec` as a **git submodule pinned to a commit** (director, `2026-09-20`), and
  read `.sexp` through `specs/Lispish.spec` on the `rust/linkedspec-runtime` backend, following the
  published guide — `docs/linkedspec-book/src/public-api/integration-rust.md`, *"Parse Lispish
  files in your application"* from line 198 — and the runnable example
  `examples/integration/rust/src/bin/lispish_file.rs`. No S-expression parser is written by hand in
  this project's Rust crates.
  Acceptance: the submodule is pinned to a commit and not tracked-by-branch; `vendor/` is
  registered in `doctrine/readme_routes.tsv` in the commit that creates it; the integration follows
  the **published document**, and where it departs from it the departure is named; the LinkedSpec
  reader and `scripts/sexp.py` agree on **every tracked `.sexp` file**, compared mechanically —
  two readers of one format that disagree is the defect this tree exists to prevent.
  Delivered: submodule pinned at `ad290bdb4`; the documented PGEN bootstrap run; the consumer
  built per the guide; `scripts/compare_readers.py` (11 arms) comparing both readers over every
  tracked `.sexp`; upstream feedback with a self-contained reproduction script.
  Progress commit: `SEMULITH-SF-0047` — a commit on a blocked leaf, stated as such rather than
  dressed as a completion.
  ⛔ Re-sequenced ahead of `.1`–`.6` on the director's instruction, `2026-09-20`. My own ordering
  put it last, reasoning that a parser contract should describe a settled format. Recorded rather
  than silently dropped, because the consequence is real and now carried knowingly: the grammar
  will meet a format that `.1`–`.6` are still changing, so the agreement check is what protects us
  and it must run against every file, every time, not once.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `SOT-FORMAT.8` | `pending` | measured drift in the director's only window — and `.9` cannot advance until LinkedSpec acts on the reported defect |
| 2 | `SOT-FORMAT.1` | `pending` | the schema language must exist **before** any record moves, or the migration spends a window with real validation replaced by "it parses" |
| 3 | `SOT-FORMAT.2` | `pending` | the constructs already in `.sexp` are the cheapest proof the schema layer holds, and they carry a verdict (`52 of 52`) that must not move |
| 4 | `SOT-FORMAT.3` | `pending` | records next, because `RECORD-SCHEMA` is the gate with the most to lose |
| 5 | `SOT-FORMAT.4` | `pending` | configuration last of the conversions — 39 arms and two comparators ride on it |
| 6 | `SOT-FORMAT.5` | `pending` | merge is only definable once everything is one format |
| 7 | `SOT-FORMAT.6` | `pending` | the gate can only be green after the last file moves |

## Decisions

| Date | Decision | Rationale |
| --- | --- | --- |
| `2026-09-14` | S-expression is the single format for every engine input | director instruction; composition is a merge and three formats are three merge semantics |
| `2026-09-14` | the Rust reader is **LinkedSpec's**, via a git submodule, never hand-written | director instruction; `specs/Lispish.spec` on the Rust backend already exists. ⛔ I first inferred `pgen` from a capability description and was corrected — a description matches several repositories, only a named artifact identifies one |
| `2026-09-14` | Schema language first, migration second | `RECORD-SCHEMA` has 15 fired arms; converting first would trade proven validation for parse-success |
| `2026-09-14` | An undeclared construct is a hard error, never an ignore | S-expressions accept anything syntactically; without this rule "extensible" degrades to "typo-tolerant" |
| `2026-09-14` | Schemas are written in the format they describe | the only way "adding a construct needs no reader change" is provable rather than asserted |

## Open Questions

- Does the schema language need value types beyond symbol, string, integer and list? Deferred until
  a real construct needs one — an unused type is an untested type.
- Do comments belong to the form that follows them, or to the file? `.4` forces the answer, because
  `profile.toml`'s comments carry provenance for 26 decisions.
- ⚠️ **`CHANGELOG.md` is 64,210 B against a 65,536 B ceiling — 1,326 B of headroom, and its 49,152 B
  health target is already crossed.** It has not fired, so this commit does not shard it, but the
  next entry of ordinary size will block a commit mid-work. The registered procedure is to shard
  into `docs/changelog/` (per-part 64 KiB, already in `doctrine/readme_routes.tsv`). Whoever opens
  the next leaf should do that first rather than discover it at `git commit`.

## Blockers

- `SOT-FORMAT.9` only: **an upstream defect in `specs/Lispish.spec`.** A double-quoted string
  containing LF is not read as one string, so `materials/catalog.sexp` reads as 6 top-level forms
  instead of 43 — silently, exit 0. Root cause, minimal reproduction and a validated one-line fix
  are reported at [`docs/upstream/linkedspec/LS-001-multiline-string/`](../feedback/linkedspec-rust-lispish.md).
  Nothing else in this tree depends on it; `.8` and `.1`–`.6` run on the Python tooling.
- ⚠️ The earlier blocker — LinkedSpec's integration document — was **discharged** on `2026-09-20`
  by its publication at `ad290bdb4`. This is a different one, found by doing the work.

## Acceptance Checklist (current leaf — `SOT-FORMAT.9`, progress; acceptance NOT met)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHERE: `vendor/linkedspec/specs/Lispish.spec:69`.

  ```
  $ python3 scripts/compare_readers.py
    DIFFER  materials/catalog.sexp  <root>: A has 43 element(s), B has 6
    compare_readers: 4 of 5 file(s) agree
  $ grep -n 'dquotes:\|others:' vendor/linkedspec/specs/Lispish.spec
    69:dquotes: /"(.*?)(?<!\\)"/     I.return(...)      # `.` does not match LF without DOTALL
    84:others:  /[^\s"{}()\[\];]+/   I.return(...)      # what the text falls through to
  ```

  WHY it is severe rather than cosmetic: the string does not merely lose its newline, it **stops
  being a string**, and its remaining text is re-lexed as syntax. A `)` in the continuation closes
  a form that was never open, so siblings are absorbed into the wrong parent — and it exits 0.

  ```
  (r (a "x\n   y") (b "z"))   ->  ["r",["a","x","y) (b z"]]        want ["r",["a","x\n   y"],["b","z"]]
  materials/catalog.sexp       ->  6 top-level forms, 37 of them nested inside the fifth (want 43)
  ```

  ⛔ Located by refutation, not by guessing: I first hypothesised `;` inside a string, then
  parentheses inside a string. **Both were wrong** — the reader handles them correctly — and the
  controls that pass (spaces, parens, TAB, CR, all on one line) are what localise it to LF.

- [x] **ADDRESSED (verified)** — leg 2, for everything this leaf owns except the agreement itself.
  Submodule pinned to the exact commit named: `ad290bdb427bc19a5af81de0f0b07e119c8999ff`, with
  RGX `8763a0e6bea9` and PGEN `db6f8c6836fe` — the revisions the guide's own evidence section
  names. The documented PGEN bootstrap produced all four `generated/` products; the consumer built
  in 32.15s. `scripts/compare_readers.py`, 11 arms:

  ```
  agree   definitions/riscv/m.sexp             438 nodes identical
  agree   definitions/riscv/rv64i.sem.sexp    1550 nodes identical
  agree   definitions/riscv/rv64i.sexp        1716 nodes identical
  agree   profiles/rv64i-lab-v0/encoding.sexp   18 nodes identical
  DIFFER  materials/catalog.sexp  <root>: A has 43 element(s), B has 6
  compare_readers: 4 of 5 file(s) agree
  ```

  The fix was **validated before being reported**, on a copy of the spec so the submodule stays
  pinned and clean: with `(?s)` on lines 69 and 71, the reproduction goes `4 matched / 4 differed`
  → `8 matched / 0 differed`, and all five files agree.

- [ ] **NOT MET — the readers do not agree on every tracked file.** 4 of 5. The remaining
  disagreement is an upstream defect, reported with a reproduction; it is LinkedSpec's change to
  make, because patching a pinned submodule is how a pin becomes a fork. ⚠️ This box stays unticked
  and the leaf stays `blocked`. Rewriting the criterion to match the result is the only real
  failure available here.

- [x] **NO REGRESSION** — leg 3. The submodule is additive; `vendor` is excluded from the Cargo
  workspace so neither side's build changes, and `.app-data/` is gitignored.

  ```
  $ python3 scripts/sexp.py --self-test          -> 18 pass / 0 fail
  $ python3 scripts/check_citations.py | tail -1 -> 52 of 52 … resolve
  $ python3 scripts/materials.py --self-test     -> 20 pass / 0 fail
  $ python3 scripts/run_smoke.py | tail -1       -> run_smoke: ok …
  $ bash scripts/check_doctrines.sh              -> all doctrines green
  ```

- [x] **LOCKSTEP** — `docs/feedback/` registered in `doctrine/readme_routes.tsv` in the commit that
  creates it; `TOOLBOX.md` gains the comparator; `Cargo.toml` and `.gitignore` carry the reason for
  each addition beside it.

## DEPARTURES FROM THE PUBLISHED GUIDE

The acceptance says the integration follows the published document and that departures are named.
Three, all mine, all corrected:

1. **Jumped to line 198** as directed and skipped *Initial PGEN preparation* 100 lines earlier.
   Build failed on `generated/return_annotation_parser.rs`. The guide is explicit — *"Checkout does
   not generate PGEN's parser inputs"* — and I had not read it.
2. **Used `git submodule update --init --recursive`** where the guide prescribes two targeted
   inits. Cost: 1.7 GB and 30 nested submodules instead of the needed closure.
3. **Used bare `cargo` and my own target directory** instead of `tools/run_cargo_local.sh` and the
   prescribed `.app-data/` layout. Corrected; the guide's layout is also the one Policy 13 wants.

All three are reported upstream as first-consumer papercuts, since we are the first consumer and
each cost a failed attempt.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-20` | `SOT-FORMAT.9` | submodule pin vs the commit the director named | `ad290bdb4…` exact; RGX/PGEN match the guide's evidence |
| `2026-09-20` | `SOT-FORMAT.9` | documented PGEN bootstrap | all 4 `generated/` products, exit 0 |
| `2026-09-20` | `SOT-FORMAT.9` | consumer build per the guide | ok, 32.15s |
| `2026-09-20` | `SOT-FORMAT.9` | `compare_readers.py --self-test` | `11 pass / 0 fail` |
| `2026-09-20` | `SOT-FORMAT.9` | both readers over every tracked `.sexp` | **4 of 5 agree** — acceptance NOT met |
| `2026-09-20` | `SOT-FORMAT.9` | refuted hypothesis: `;` inside a string | handled correctly — not the cause |
| `2026-09-20` | `SOT-FORMAT.9` | refuted hypothesis: parens inside a string | handled correctly — not the cause |
| `2026-09-20` | `SOT-FORMAT.9` | isolation: LF vs CR vs TAB inside a string | only **LF** breaks it |
| `2026-09-20` | `SOT-FORMAT.9` | candidate fix `(?s)` on lines 69/71, on a copy | 8 of 8 cases, 5 of 5 files agree |
| `2026-09-20` | `SOT-FORMAT.9` | regression: sexp, citations, materials, smoke, doctrines | 18/0, 52 of 52, 20/0, ok, green |
| `2026-09-14` | `SOT-FORMAT.7` | read every string in the 4 tracked `.sexp` files through the reader | 52 of 52 citations corrupted; 0 elsewhere |
| `2026-09-14` | `SOT-FORMAT.7` | `sexp.py --self-test` on the unfixed reader | `15 pass / 3 fail` — the 3 name the defect |
| `2026-09-14` | `SOT-FORMAT.7` | `sexp.py --self-test` after the fix | `18 pass / 0 fail` |
| `2026-09-14` | `SOT-FORMAT.7` | round-trip: each citation verbatim in the file's bytes | `52 / 52`, mojibake 0 |
| `2026-09-14` | `SOT-FORMAT.7` | backslash census before tightening escapes | 0 in all 4 tracked `.sexp` files |
| `2026-09-14` | `SOT-FORMAT.7` | `check_semantics.py` | `52 of 52` — unchanged |
| `2026-09-14` | `SOT-FORMAT.7` | `gen_fragments.py` reproduction | `git diff --stat definitions/` empty |
| `2026-09-14` | `SOT-FORMAT.7` | `run_smoke.py` (4 guests, 2 models) | ok — expectations, never-written, reproduction |
| `2026-09-14` | `SOT-FORMAT.7` | drift probe: does the book describe the format? | `grep -c 'S-expression' docs/ARCHITECTURE.md` → 0 — owned as `.8` |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `SOT-FORMAT.9` | `SEMULITH-SF-0047 (leaf SOT-FORMAT.9): two readers, one format, and a defect worth reporting` | **progress on a blocked leaf**, not a completion: 4 of 5 files agree |
| `SOT-FORMAT.7` | `SEMULITH-SF-0041 (leaf SOT-FORMAT.7): the reader corrupted every citation it read` | 52 of 52 citations restored; 18 arms where there were none |

## Changelog

- `2026-09-14`: Created. Supersedes the format split in `decision_canonical-definition-input`, which
  I had defended on the grounds that records are not trees — a true statement about shape that
  answered the wrong question. The question is whether two of them can be merged by a defined rule.
