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
  Blocker: LinkedSpec is preparing its **integration document for downstream consumers and it is
  not done** (director, `2026-09-14`). Integrating against an unpublished contract means
  integrating against today's internals — which is how a submodule becomes a fork.
  Read `linkedspec/docs/linkedspec-book/` when it unblocks (director, `2026-09-14`).
  Goal: add `../linkedspec` as a **git submodule** pinned to a commit, and read `.sexp` through its
  `specs/Lispish.spec` on the `rust/linkedspec-runtime` backend. No S-expression parser is written
  by hand in this project's Rust crates.
  Acceptance: the submodule is pinned, not tracked-by-branch; the LinkedSpec reader and
  `scripts/sexp.py` agree on every tracked `.sexp` file, compared mechanically — two readers of one
  format that disagree is the defect this tree exists to prevent; the integration follows the
  published document rather than the source.
  ⚠️ Also sequenced after `.1`–`.6`: a parser contract should describe a settled format, and this
  tree is what settles it.


## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `SOT-FORMAT.8` | `pending` | measured drift in the director's only window — the book's canonical-definition chapter describes no part of the canonical definition |
| 2 | `SOT-FORMAT.1` | `pending` | the schema language must exist **before** any record moves, or the migration spends a window with real validation replaced by "it parses" |
| 3 | `SOT-FORMAT.2` | `pending` | the constructs already in `.sexp` are the cheapest proof the schema layer holds, and they carry a verdict (`52 of 52`) that must not move |
| 4 | `SOT-FORMAT.3` | `pending` | records next, because `RECORD-SCHEMA` is the gate with the most to lose |
| 5 | `SOT-FORMAT.4` | `pending` | configuration last of the conversions — 39 arms and two comparators ride on it |
| 6 | `SOT-FORMAT.5` | `pending` | merge is only definable once everything is one format |
| 7 | `SOT-FORMAT.6` | `pending` | the gate can only be green after the last file moves |
| 8 | `SOT-FORMAT.9` | `blocked` | the LinkedSpec reader — waiting on that project's integration document for downstream consumers |

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

- `SOT-FORMAT.9` only: **LinkedSpec's integration document for downstream consumers is not
  finished** (director, `2026-09-14`). Nothing else in this tree depends on it — `.7`, `.8` and
  `.1`–`.6` all run on the Python tooling, which is where the schema layer belongs anyway.

## Acceptance Checklist (current leaf — `SOT-FORMAT.7`)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHERE: `scripts/sexp.py`, the string branch of
  `parse()`. It collected escape pairs raw and handed the assembled string to a codec:

  ```python
  stack[-1].append("".join(buf).encode().decode("unicode_escape"))
  ```

  WHY that fails: `unicode_escape` is **Latin-1**. It reads each byte as one character, so the two
  UTF-8 bytes of `§` come back as two characters. Measured on the repository's own files:

  ```
  $ python3 -c '…read rv64i.sem.sexp through the reader…'
    definitions/riscv/rv64i.sem.sexp   source lines w/ non-ASCII:  56   corrupted strings: 52
  raw bytes in file : b'RVI-RV64I \xc2\xa73.1.2.1 \xe2\x80\x94 D-LUI-AUIP'
  as the reader sees: 'RVI-RV64I Â§3.1.2.1 â\x80\x94 D-LUI-AUIP'
  ```

  **All 52 citations** — every specification locator committed one leaf earlier as *"52 of 52,
  every rule cited"*. The claim was true of the file and false of what any consumer received.
  WHY no gate saw it: the reader had **no self-test** (`scripts/test_sexp.py` did not exist), and
  every downstream check asked about structure or behaviour. `check_semantics.py` asks whether a
  citation is *present*; a corrupted string is still present. Nothing was pointed at **fidelity**.

- [x] **ADDRESSED (verified)** — leg 2. Escapes are decoded from a closed five-entry table written
  here, and an escape outside it is **refused rather than guessed**. Round-trip proven against the
  file's own bytes — every citation the reader returns must be findable verbatim in what it read:

  ```
  citations read : 52
  present in the file byte-for-byte: 52 / 52
  mojibake remaining: 0
  sample: 'RVI-RV64I §3.1.2.1 — D-LUI-AUIPC'
  ```

  The reader now carries a self-test, **fired RED before the fix** — the three arms that name the
  defect failed on the unfixed reader and pass on the fixed one:

  ```
  $ python3 scripts/sexp.py --self-test        # BEFORE
    FAIL  GREEN non-ASCII round-trips byte-for-byte: got 'RVI-RV64I Â§3.1.2.1 â\x80\x94 D-LUI'
    FAIL  GREEN a citation survives the whole pipeline: mojibake: 'Â§ â\x80\x94 Âµ'
    FAIL  RED   an unknown escape is refused, not guessed: accepted '(x (s "a\qb"))'
  sexp --self-test: 15 pass / 3 fail
  $ python3 scripts/sexp.py --self-test        # AFTER
  sexp --self-test: 18 pass / 0 fail
  ```

- [x] **NO REGRESSION** — leg 3. No tracked file's **content** changed: the files were always right.
  Every consumer of the reader re-run:

  ```
  $ python3 scripts/check_semantics.py definitions/riscv/rv64i.sexp definitions/riscv/rv64i.sem.sexp
    52 of 52 declared instruction(s) have checked semantics
  $ python3 scripts/gen_fragments.py && git diff --stat definitions/
                                        # empty — reproduced byte-for-byte
  $ python3 scripts/run_smoke.py | tail -1
    run_smoke: ok — every program matches its specification-derived expectations and reproduces;
               every cross-model comparison that is enabled agrees
  ```

  ⛔ No backslash exists in any tracked `.sexp` file (`grep -c '\\' …` → 0 on all four), so
  refusing unknown escapes cannot break a file that parses today — checked before tightening.

- [x] **LOCKSTEP** — `TOOLBOX.md` gains the self-test row; `DEV_NOTES.md` carries the dated lesson,
  promoted to [`a-parse-without-error-is-not-a-faithful-read`](../knowledge/a-parse-without-error-is-not-a-faithful-read.md);
  the reader's own docstring no longer cites the superseded format split; `MEMORY.md` and
  `docs/TASK_TREE.md` name this tree. ⚠️ The **mdBook is not yet in lockstep** on the format itself
  — measured during this leaf and owned as `SOT-FORMAT.8`, at frontier order 2, not logged and left.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
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
| `SOT-FORMAT.7` | `SEMULITH-SF-0041 (leaf SOT-FORMAT.7): the reader corrupted every citation it read` | 52 of 52 citations restored; 18 arms where there were none |

## Changelog

- `2026-09-14`: Created. Supersedes the format split in `decision_canonical-definition-input`, which
  I had defended on the grounds that records are not trees — a true statement about shape that
  answered the wrong question. The question is whether two of them can be merged by a defined rule.
