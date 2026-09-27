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

- ID: `SOT-FORMAT.10` — **the document grammar joins the agreement sweep**
  Status: `active`
  ⭐ Director instruction, `2026-09-26`: adopt SExprDocumentV1 now — the durable answer to
  both CLASS families — as the judgment call on the recorded candidate.
  Goal: extend `scripts/compare_readers.py` with a third reader — LinkedSpec's
  `SExprDocumentV1.spec` document grammar and its `sexpr_file` consumer — comparing every
  tracked `.sexp` file form-by-form against `sexp.py`, keeping the Lispish comparison as the
  historical layer it is (the LS-001/LS-002 regression guard, CLASS notes and all). The
  document grammar returns tagged tokens (`symbol`/`number`/`string`) with raw lexemes: the
  quoted-numeric family dies because a quoted number arrives tagged `string` — the quote-kind
  LS-002 discards is preserved by construction; the escape-retention family dies because the
  lexeme is decoded on OUR side with sexp.py's own escape table — interpretation moves to the
  canonical reader, anchored, not guessed. It also reads every form in a file, not the first.
  Design decisions, recorded before code: additive, never a replacement (two layers, two
  questions — the extraction contract vs the canonical read path); the C-side normalisation
  may only use sexp.py's own tables (`_ESCAPES`, `_atom`), so it cannot invent agreement; the
  falsifiable acceptance is that the document layer shows 5 of 5 with ZERO class notes on the
  real corpus — the families classified, not counted, today must simply not arise there.
  ⭐ Result exceeded the acceptance: **6 of 6**, because `schema/schema.sexp` itself joined the
  tracked corpus this session — and it passes both layers, so the schema language's fixpoint now
  also verifies through the document grammar.
  Acceptance: `compare_readers.py` gains the document layer over every tracked file (all
  forms per file), ≥ 4 new self-test arms (lexeme decoding anchored to sexp.py's table; kind
  tags prevent quoted-numeric; differing lexemes still refuse; the Lispish layer's verdict and
  class notes are unchanged); corpus run shows the document layer at 5 of 5 with no class
  notes; `make check`-equivalent Python self-tests green; enforcer green.
  Verification: `2026-09-26` — 28 pass / 0 fail (21 → 28 arms); corpus sweep below.
  Commit: `SEMULITH-SF-0056`

- ID: `SOT-FORMAT.1` — **the schema language, written in itself**
  Status: `done`
  Goal: declare what a construct is — its head, its fields, their arity and value types, whether
  they repeat — as S-expressions in `schema/`. Write the schema language's own schema in the schema
  language and validate it with itself: the fixpoint is what *proves* extensibility rather than
  asserting it.
  Design (recorded before code, `2026-09-26`): a schema file is one `(schema (id STRING))` of
  metadata plus one `(construct (name SYMBOL) (field …)…)` per construct. A field instance is a
  child list headed by its field's name; atom fields take exactly one value `(name value)` or the
  bare marker `(name)` when declared `(empty yes)` — the corpus writes `(requires)` that way; form
  fields take the nested form, whole-list when the field name is one of the allowed heads
  (`(source (file …) …)`), single-value otherwise (`(effect (set …))`); `(values SYM)` restricts a
  symbol's spelling; `(repeat yes)` means sibling child lists, 0-or-more; `(optional yes)` is the
  0-or-1 single-field variant. `scripts/check_sexp_schema.py <file> <schema>` validates and names
  the offending construct/field. The validator's fixed kernel is the *interpreter* of
  construct/field declarations — the named boundary from the acceptance criteria: new constructs
  are data; a new KIND of declaration changes the kernel. The fixpoint runs the kernel with
  `schema/schema.sexp` as both schema and target.
  ⭐ The first design assumed a tidy uniform `(name value)` pair grammar; reading the real corpus
  before building (rv64i.sexp's `(source (file …) (file …) (origin …))`, rv64i.sem.sexp's
  `(effect (set …))`, `(requires)` markers) refused it. The language in schema.sexp is the corpus's
  grammar, not an invented one — `.2` will exercise it against encoding/fragment/semantics.
  Acceptance: `scripts/check_sexp_schema.py` validates a file against a schema and names the
  offending construct/field on failure; `schema/schema.sexp` validates under itself; ≥ 6 arms fired
  RED (undeclared construct, undeclared field, missing required field, wrong arity, wrong value
  type, duplicated single-valued field); `schema/` registered in `doctrine/readme_routes.tsv` **in
  the same commit that creates it**.
  Verification: `2026-09-26` — 16 pass / 0 fail (13 RED, 3 GREEN incl. the fixpoint); the
  standalone fixpoint run `schema.sexp` against itself conforms.
  Commit: `SEMULITH-SF-0054`

- ID: `SOT-FORMAT.2` — **the constructs already in use, declared as data**
  Status: `done`
  Goal: `encoding`, `fragment` and `semantics` get schema files. `scripts/check_semantics.py`'s
  hard-coded 32-form language moves out of Python and into `schema/`, so a new semantic form is a
  data change.
  Acceptance: the 32 forms are data; `52 of 52 declared instruction(s) have checked semantics` is
  reproduced **byte-identically**; the four controls of `MODEL-METHOD.9` still fire RED; adding a
  33rd form requires no Python edit (demonstrated, then reverted).
  Result: met, `2026-09-27`. The schema language gained exactly one new declaration kind —
  `(operator …)`, the named boundary of criterion 2's ⚠️ — and `schema/encoding.sexp`,
  `schema/fragment.sexp`, `schema/semantics.sexp` declare every construct in the three corpus
  families, including the three positional mini-languages (`fixed` triples, `operands` lists,
  `pieces` pairs) and the 32-form semantics expression language. `check_semantics.py` loads its
  form table from `schema/semantics.sexp` through the kernel's loader; its walk, messages and exit
  codes are unchanged (one refusal message now names the schema instead of the FORMS table it
  pointed at, which no longer exists). Gate registration of the schema layer stays deferred to
  `.6` — the tree's own sequencing; this leaf proves the layer by recorded corpus verification
  and 15 new self-test arms.
  Design (recorded before code, `2026-09-27`): the corpus was read before building, the way `.1`
  did — and the record grammar of `schema.sexp` does NOT fit three positional mini-languages the
  real files use: fragment `(fixed (31 25 0x0) …)` triples, `(operands rd rs1 rs2)` symbol lists,
  `(pieces (12 12) …)` integer pairs; and the semantics effect bodies are a 32-head expression
  language with per-head arity, not `(name value)` field lists at all. Declaring only the record
  layer would have forced either refusing the real corpus or ignoring shapes — both dishonest.
  Named boundary (the ⚠️ of acceptance criterion 2): the schema language gains exactly ONE new
  declaration kind, `(operator (name SYM) (fixed N) | (variadic) [(min N)] [(arg SPEC)])`, parsed
  by the same kernel meta-level that already parses `(construct …)`/`(field …)`. `SPEC` is
  `symbol|integer|string|expr` or a fixed-length list of those (`(arg (integer integer integer))`
  for `fixed` triples); `expr` — the default — is an atom or an operator form, which is precisely
  the recursion `check_semantics.py` already implements, so operand scoping (a cross-file fact:
  the encoding provides the operands) stays in the checker while structure and arity become data.
  Consequences, stated: a new construct OR a new operator is a schema file edit, zero Python; a
  FIFTH declaration kind would change the kernel again — the same boundary a database draws
  between adding a table and adding a column type. `check_semantics.py` loads the operator table
  from `schema/semantics.sexp` through the kernel's loader and keeps its walk, messages and exit
  codes unchanged. Gate registration of the schema layer is deliberately deferred to `.6` (the
  tree's own sequencing — `.6` IS the `SOURCE-FORMAT` gate); this leaf proves the layer by
  recorded corpus verification and new self-test arms instead.

- ID: `SOT-FORMAT.3` — **the records: requirements and obligations**
  Status: `done`
  Goal: convert `requirements.jsonl` (26) and `contract-obligations.jsonl` (34) to the format.
  Design (recorded before code, `2026-09-27`):
  - ⭐ The JSON contract carries discriminating power the record grammar cannot state: regex
    patterns on ids, `minItems`/`uniqueItems` on lists, `minLength` on prose. Rather than let that
    power evaporate into consumers, the `(field …)` kind grows four optional FACETS —
    `(pattern "…")` and `(min-length N)` on string fields, `(min N)` and `(unique yes)` on
    repeated fields — parsed by the same kernel meta-level. This is the `.2` boundary one level
    down: a new KIND would change the kernel; optional facets on the existing kind are the
    language saying honestly what the corpus's contracts already said. `schema/schema.sexp` gains
    the facet fields so the fixpoint keeps describing the whole language.
  - One form per record, house style (`materials/catalog.sexp`): `(requirement …)` /
    `(obligation …)`; JSON keys are the field names verbatim, so the mapping has no translation
    table to drift. Enums become symbols under `(values …)` (typos refused by name); prose and
    identifiers stay strings; empty lists are absence (repeat fields), as the grammar already
    says. Measured latent defect fixed by the move: the JSON validator never descended into
    `parameters.additionalProperties`, so the schema's own `type: [string, number, boolean,
    null]` silently excluded the arrays three obligations actually write (`legal_access_widths_bits`
    and kin). The S-expression schema states values honestly: `(value (int …)|(str …)|(true)|
    (false)|(null)|(ints …)|(strs …))` — typed wrappers, no unchecked bag. Floats have no
    S-expression atom and appear nowhere in the corpus; a float parameter is refused, and the day
    one is needed is a schema decision, not a silent guess.
  - The mapping lives in one tracked owner, `scripts/records_sexp.py` (JSON-shaped dicts ↔
    forms); `scripts/convert_records.py` drives it for the migration and proves losslessness:
    `jsonl → sexp → jsonl` re-derived and compared field-by-field, and the re-dumped JSONL
    byte-identical to the source file. `RECORD-SCHEMA` re-fires its arms against the converted
    fixtures; `validate_records.py` keeps the JSONL that stays JSONL (`examples/`, frozen
    delivery artifacts) and its requirement/obligation power transfers to the schema layer —
    the transfer demonstrated by the 15 arms, not claimed.
  - Open question carried forward: `profiles/` per-part ceiling (32 KiB) vs the converted
     file sizes — measured at conversion time; if the compact form exceeds it, the re-derivation
     follows the `docs/tasks/` precedent with grounds recorded here.
  Acceptance: round-trip proves losslessness field-by-field; `RECORD-SCHEMA`'s 15 arms are re-fired
  RED against the converted form; `scripts/validate_records.py` either reads the new format or is
  retired with its power transferred, and the transfer is demonstrated, not claimed.
  Verification: `2026-09-27` — see the checklist below; converter 9/0; kernel 31 → 43 arms;
    round-trip byte-identical both catalogues; `RECORD-SCHEMA` 15 → 22 arms, every RED scenario
    re-fired on the converted form; `compare_readers` 13 of 13; full enforcer green.
  Commit: `SEMULITH-SF-0058`
  DEV_NOTES lesson (`2026-09-27`): promotion: declined (both shapes recorded in this leaf; a card is due if a second consumer trips them).

- ID: `SOT-FORMAT.4` — **configuration, state and provenance**
  Status: `done`
  Goal: convert `profile.toml` (26 decisions), `state.json`, `sources.toml`, `references.toml`, the
  reference override JSON and the guest expectation TOMLs.
  Acceptance: `PROFILE-CONSISTENCY`'s 39 arms re-fired RED, including rule 5b; `run_smoke.py` and
  `compare_platforms.py` produce identical verdicts; comments in the TOML sources survive as
  first-class form, since a comment-rich human-authored file was the original argument for TOML and
  losing it would be a real regression.
  Result: met, `2026-09-27`. All nine documents converted and verified; the kernel carries one
  reserved `comment` head; six schemas joined the layer; every consumer reads through the new
  mapping owner. (The DOSSIER's stale "no gate has been run" line was found and corrected in
  passing — `G0` has run; its verdict reads `incomplete`.)
  ⚠ Built-shape correction to the design below, recorded, not silently diverging:
  booleans shipped as the SYMBOL values `true`/`false` (`(cacheable true)`), not `(true)`/
  `(false)` wrappers — `(values …)` already types them; wrappers would add constructs for
  nothing.
  Design (recorded before code, `2026-09-27`), the corpus read in full first, the way `.1`–`.3` did:
  - ⭐ **Comments become first-class forms — the kernel gains ONE reserved head.** `(comment
    "line" …)` is inert data allowed at ANY position (top level, inside constructs, in schema
    files): validation skips it, the mapping owners skip it, and no schema may declare or forbid
    it. This answers the tree's open question: a comment belongs to the FILE as an ordered
    annotation stream, conventionally placed before the form it annotates (after, when it trailed
    a value inline). It is part of the format's surface, not a new declaration kind — criterion
    2's boundary is unchanged, and `commment` is still refused by name.
  - **One root form per file**, named for the document: `(profile …)`, `(state …)`, `(sources …)`,
    `(references …)`, `(override …)`, `(expectations …)`. TOML tables and `[[array]]` blocks
    nest and repeat as forms; JSON objects nest the same way.
  - **The mapping lives in one new owner, `scripts/dossier_sexp.py`** (parallel to
    `records_sexp.py`): keys verbatim as field names (no translation table); strings VERBATIM
    (a hex address stays a string, so the round-trip is exact); floats refused; booleans → the
    symbols `true`/`false` (see the correction above); scalar arrays → repeated atom fields,
    empty arrays → absence (the `.3` rules); arrays of objects → repeated form fields;
    dynamic-keyed maps (guest `writes`, override `extensions`) → entry forms — a schema cannot
    declare a hundred extension names, and a wildcard would gut "undeclared is refused by name".
    `authority` (the one closed project enum) is a symbol under `(values …)`; vocabularies the
    dossier merely RECORDS stay strings — PROFILE-CONSISTENCY keeps owning them.
  - **Consumers change at the seam, not in their logic**: every gate/tool keeps receiving the
    exact dicts `tomllib`/`json` produced, so "identical verdicts" is a data equality. The Sail
    override's JSON is a foreign-tool input, derived from the tracked `.sexp` into `target/refs/`
    on every run — the `.sexp` stays the single source of truth.
  - **Losslessness is proven like `.3`, shaped like this corpus**: `convert_dossier.py verify`
    re-derives TOML/JSON → data → forms → data field-for-field, plus a comment census (every
    TOML comment line appears as a comment-form string, in order) and schema validation. TOML
    re-dump byte-identity is NOT claimed — the files are hand-formatted; data identity + comment
    survival is the honest claim.
  - **Six new schema files** (`schema/{profile,state,sources,references,override,expectations}.sexp`)
    type-check the dossier; completeness stays with PROFILE-CONSISTENCY's 39 arms (`.6` owns the
    permanent `SOURCE-FORMAT` gate); the registry's `schema/` ceiling was re-derived with grounds.

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
  Status: `done`
  Goal: the mdBook chapter *"Architecture and canonical definitions"* includes `docs/ARCHITECTURE.md`,
  which names no format, no `definitions/` directory and no composition — four commits introduced
  all three. The director's only window shows none of it. Close the drift at the source document,
  not in the chapter preface.
  Acceptance: `docs/ARCHITECTURE.md` describes the format, the fragment, the composition operator
  and the schema layer in prose; the book builds; `grep -c 'S-expression' docs/ARCHITECTURE.md` is
  non-zero where it is currently 0.
  Verification: `2026-09-26` — see the log; built-state claims in the new §1.1–§1.3 name their
  instruments, pending layers are labeled specified-not-built, and the one mutable count was
  rephrased to "agreement file by file" rather than a numeral that drifts.
  Commit: `SEMULITH-SF-0053`

- ID: `SOT-FORMAT.9` — **the Rust reader comes from LinkedSpec, as a submodule**
  Status: `done`
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
  **Director instruction, `2026-09-26`: upstream has fixed and pushed the reported bugs — update
  the submodule pin.** The fix is confirmed present at `origin/main` tip `a8d34c845` (the
  `(?s)` DOTALL form on `dquotes`/`squotes` this project validated and reported, shipped as
  upstream commit `8259719f8`); RGX stays pinned at `8763a0e6` on both sides, so the bootstrap
  products remain valid. The update flow follows the guide's own "update deliberately" paragraph:
  fetch, check out the reviewed revision, re-verify, then commit the changed pointer.
  Acceptance met `2026-09-26`: 5 of 5 tracked files agree; the LS-001
  reproduction re-runs 8/0 at the new pin; the residue is two documented CLASS families the
  comparator now enumerates (see the checklist below).
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
| 1 | `SOT-FORMAT.5` | `pending` | merge is only definable now that everything is one format |
| 2 | `SOT-FORMAT.6` | `pending` | the gate can only be green after the last file moved |

## Decisions

| Date | Decision | Rationale |
| --- | --- | --- |
| `2026-09-27` | The kernel reserves ONE head — `(comment "…")`, inert at any position; schemas may not declare or forbid it | comments are the format's surface, like whitespace; declaring them per-schema would duplicate the exemption and re-introduce the loss the leaf exists to prevent |
| `2026-09-27` | Booleans are the symbol values `true`/`false`, not wrapper forms | `(values …)` already types and restricts them; wrappers would add two nullary constructs per schema for zero discriminating power — the built-shape correction to `.4`'s design, recorded in the leaf |
| `2026-09-27` | Field FACETS — `(pattern …)`, `(min-length N)`, `(min N)`, `(unique yes)` — extend `(field …)`; they are not a fifth declaration kind | the JSON record contracts carried discriminating power (id regexes, minItems, uniqueItems, minLength) that the record grammar could not state; evaporating it into consumers would make the schema layer weaker than the contract it replaces. The same boundary as `.2`, one level down: a new KIND changes the kernel, facets on the existing kind are the language |
| `2026-09-27` | `parameters` values are typed wrappers — `(int …)/(str …)/(true)/(false)/(null)/(ints …)/(strs …)` — not an open map | the JSON schema's `additionalProperties` silently excluded the arrays three obligations actually write, and the validator never descended into it; the honest format states what the corpus holds and REFUSES a float, a mixed list or a nested value by name — the day one is needed is a schema decision, not a guessed translation |
| `2026-09-27` | Catalogue discovery excludes the `schema/` directory | the schemas share their basenames with the catalogues (`schema/requirements.sexp` IS named `requirements.sexp`); a gate that judged a schema as its own target would report its own grammar as a records violation — measured by the reworked gate's first self-test run |
| `2026-09-27` | Operators are the one new declaration kind `.2` adds; a fifth kind changes the kernel again | the corpus writes three positional mini-languages no record grammar can state; bending the generated files to fit would have forked the generator and every consumer — the boundary from criterion 2's ⚠️, crossed once, on purpose |
| `2026-09-27` | The schema layer never reads a second file | operand scoping (a cross-file fact: the encoding provides the operands) stayed in `check_semantics.py` — the moment a check needs two sources of truth it belongs to a consumer, not the schema |
| `2026-09-26` | The pin advances on the director's word only after OUR re-run earns it | the tracker separates `fixed-upstream` from `verified` for exactly this; the update flow is fetch → checkout → rebuild → verify → commit pointer |
| `2026-09-26` | CLASS differences are enumerated by the comparator, never counted as agreement | the residue after LS-001 (quote-numeric, escape-retention) is documented upstream behaviour; each family is anchored to exact byte meaning so it cannot mask a real difference — and upstream's document grammar is the durable answer when the engine adopts the reader |
| `2026-09-14` | S-expression is the single format for every engine input | director instruction; composition is a merge and three formats are three merge semantics |
| `2026-09-14` | the Rust reader is **LinkedSpec's**, via a git submodule, never hand-written | director instruction; `specs/Lispish.spec` on the Rust backend already exists. ⛔ I first inferred `pgen` from a capability description and was corrected — a description matches several repositories, only a named artifact identifies one |
| `2026-09-14` | Schema language first, migration second | `RECORD-SCHEMA` has 15 fired arms; converting first would trade proven validation for parse-success |
| `2026-09-14` | An undeclared construct is a hard error, never an ignore | S-expressions accept anything syntactically; without this rule "extensible" degrades to "typo-tolerant" |
| `2026-09-14` | Schemas are written in the format they describe | the only way "adding a construct needs no reader change" is provable rather than asserted |

## Open Questions

- Does the schema language need value types beyond symbol, string, integer and list? Deferred until
  a real construct needs one — an unused type is an untested type.
- ➡️ ANSWERED by `.4` (`2026-09-27`): a comment belongs to the FILE as an ordered annotation
  stream — a first-class `(comment "…")` form, positioned before the form it annotates by house
  convention (after, when it trailed a value inline). The kernel reserves the head; the question
  kept its promise: `profile.toml`'s 27 comment lines all survived as data.
- ⚠️ `CHANGELOG.md`'s shard headroom is deliberately not typed here: a byte count in prose is stale
  the next commit (precedent `SEMULITH-PD-0049`). The instrument owns it:
  `scripts/check_readme_routes.sh` reports the health target and enforces the 64 KiB ceiling, so
  the shard fires at the gate, not mid-review. Whoever next adds an entry needs no special step.
- 💡 The durable answer to both CLASS families in `compare_readers.py` is upstream's
  `SExprDocumentV1` document grammar — tagged token kinds, lexemes, no number conversion or escape
  decoding — which its guide steers document consumers to. Adopting it for the engine's reader
  (and probably retiring the Lispish adapter from the harness) is a candidate leaf for after
  `.2`; it would eliminate the quote-numeric and escape-retention enumeration at the source
  rather than classifying it forever.

## Blockers

- None. `2026-09-26`: the LS-001 blocker is discharged by upstream commit `8259719f8` (DOTALL
  quote readers), shipped at `origin/main` tip `a8d34c845`, on the director's instruction to
  update the pin. The earlier blocker — LinkedSpec's integration document — was **discharged** on
  `2026-09-20` by its publication at `ad290bdb4`.

## Acceptance Checklist (leaf SOT-FORMAT.2)

- [x] **REPRODUCE / ISSUE** — the problem, shown (not asserted):

  ```
  $ sed -n '26,43p' scripts/check_semantics.py          # before the fix
    FORMS: dict[str, int | None] = { "reg": 1, "pc": 0, … "trap": 2 }     # the language, as a Python literal
  $ ls schema/
    schema.sexp                                          # a schema for the schema language only —
                                                         # encoding/fragment/semantics had no schema at all
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHY: the record grammar of `schema.sexp` cannot state
  the positional mini-languages the corpus actually writes, and the semantics checker enumerated
  the language itself — "extensible by data" was true only for record-shaped constructs. WHERE:
  the gap sat between `schema/schema.sexp` and `definitions/riscv/{rv64i,m}.sexp` +
  `rv64i.sem.sexp` (three shapes: `(fixed (31 25 0x0) …)` triples, `(operands rd rs1 rs2)`
  symbol lists, 32-head effect expressions), and at the FORMS dict in `scripts/check_semantics.py`.

- [x] **FIX** — leg 2. One new declaration kind, `(operator (name SYM) (fixed N) | (variadic)
  [(min N)] [(arg SPEC)])`, kernel-parsed next to `(construct …)`/`(field …)`; three schema files
  (`encoding`, `fragment`, `semantics`); `check_semantics.py` loads the form table from
  `schema/semantics.sexp` through the kernel's loader. New constructs and new operators are data;
  a fifth kind would change the kernel — the named boundary.

- [x] **ADDRESSED (verified)** — leg 3, the acceptance criteria, each re-derived:

  ```
  $ grep -c '^(operator' schema/semantics.sexp
    32                                                   # the 32 forms are data
  $ python3 scripts/check_semantics.py definitions/riscv/rv64i.sexp definitions/riscv/rv64i.sem.sexp
    …  52 of 52 declared instruction(s) have checked semantics          (diff vs baseline: identical)
  $ # four MODEL-METHOD.9 controls: missing / unknown-form / bad-operand / no-source
    → each rc 1, refused by name (three byte-identical; unknown-form's message now names the schema)
  $ # 33rd form: append one (operator …) line, no Python touched
    unknown form 'rot' rc 1 → 1 of 1 declared instruction(s) have checked semantics rc 0 → reverted
  ```

- [x] **NO REGRESSION** — leg 4. `sexp --self-test` `18/0`; `check_sexp_schema --self-test`
  `31/0`; `materials --self-test` `20/0`; `check_citations.py` `52 of 52`; `run_smoke.py` `ok`;
  `gen_fragments.py` regeneration byte-identical (`git diff --stat -- definitions/` empty);
  `check_encoding_disjoint.py` `the fragments COMPOSE`; `bash scripts/check_doctrines.sh`
  `=== all doctrines green ===`.

- [x] **LOCKSTEP** — `TOOLBOX.md` row updated; `docs/ARCHITECTURE.md` §1.3 brought current (it
  still described the schema layer as "specified as `SOT-FORMAT.1`, not yet built" — stale since
  `SEMULITH-SF-0054`); `MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md` (+ its lesson promoted to
  `docs/knowledge/the-corpus-writes-shapes-my-grammar-cannot-state.md`), `docs/TASK_TREE.md`
  and this tree in the same commit. Gate registration of the schema layer is deferred to `.6`
  per the tree's frontier — stated here so the deferral is a decision, not a gap.

## Acceptance Checklist (leaf SOT-FORMAT.9 — acceptance MET 2026-09-26)

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

- [x] **ADDRESSED (verified)** — leg 2. Director instruction `2026-09-26`: upstream fixed and
  pushed; the pin advances to `a8d34c84595d46c24cd1820d5fc0414261706412` (`origin/main` tip), which
  ships the fix as upstream commit `8259719f8` — the `(?s)` DOTALL form on `dquotes`/`squotes` that
  this project validated and reported:

  ```
  $ git -C vendor/linkedspec show a8d34c845:specs/Lispish.spec | grep -n 'dquotes:\|squotes:'
    69:dquotes: /(?s)"(.*?)(?<!\\)"/     I.return(...)
    71:squotes: /(?s)'(.*?)(?<!\\)'/     I.return(...)
  ```

  The documented update flow was followed: fetch → check out the reviewed revision → RGX
  bootstrap (no-op, "already generated"; RGX unchanged at `8763a0e6` on both pins) → rebuild the
  consumer (20.39 s, fresh binary at `.app-data/target/debug/lispish_file`) → verify → only then
  commit the pointer. The LS-001 reproduction re-ran against the new pin:

  ```
  $ bash docs/upstream/linkedspec/LS-001-multiline-string/repro.sh \
      .app-data/target/debug/lispish_file vendor/linkedspec/specs/Lispish.spec
    LS-001: 8 matched / 0 differed        (was 4 matched / 4 differed)
  ```

- [x] **NOT MET → MET — the readers agree on every tracked file, and the residue is classified,
  not hidden.** The fix moved the disagreement one layer down, and this layer is documented
  upstream behaviour, enumerated by the comparator rather than counted as agreement-in-spite-of:

  ```
  $ python3 scripts/compare_readers.py
    agree   definitions/riscv/m.sexp                        438 nodes identical
    agree   definitions/riscv/rv64i.sem.sexp               1550 nodes identical
    agree   definitions/riscv/rv64i.sexp                   1716 nodes identical
    agree   materials/catalog.sexp                         1792 nodes identical
    class   materials/catalog.sexp [5][3][1]:  A='20260911' B=20260911  — quoted-numeric (LS-002)
    class   materials/catalog.sexp [5][7][1]:  …\"… vs "…  — escape-retention
    class   materials/catalog.sexp [29][9][1]: …\"… vs "…  — escape-retention
    class   materials/catalog.sexp [36][3][1]: A='1992' B=1992 — quoted-numeric (LS-002)
    agree   profiles/rv64i-lab-v0/encoding.sexp              18 nodes identical
    compare_readers: 5 of 5 file(s) agree
  ```

  Both `class` families follow from Lispish's PUBLISHED extraction contract (its guide documents
  both the quote-kind discard and escape retention), so they are CLASS, not defects. The
  classifier cannot mask a real difference: `quoted-numeric` requires `sexp._atom(A) == B`
  exactly, `escape-retention` requires decoding B with sexp.py's own escape table to reproduce A
  exactly. Proof it still discriminates, fired both ways after the change:

  ```
  $ python3 scripts/compare_readers.py --self-test          -> 21 pass / 0 fail
    (9 new arms: GREEN ×4 classification, RED ×5 masking — different int, non-numeric,
     undecodable retention, trailing backslash, unequal strings)
  $ LISPISH_GRAMMAR=<old pre-fix spec> compare_readers.py materials/catalog.sexp
    DIFFER <root>: A has 43 element(s), B has 6          rc=1   — the defect still fires RED
  ```

- [x] **NO REGRESSION** — leg 3. The submodule's content is untouched by us (clean checkout of
  upstream's commit); the gate set and the consumers of the reader:

  ```
  $ python3 scripts/sexp.py --self-test          -> 18 pass / 0 fail
  $ python3 scripts/check_citations.py | tail -1 -> 52 of 52 … resolve
  $ python3 scripts/materials.py --self-test     -> 20 pass / 0 fail
  $ python3 scripts/run_smoke.py | tail -1       -> run_smoke: ok …
  $ bash scripts/check_doctrines.sh              -> all doctrines green
  ```

- [x] **LOCKSTEP** — `vendor/` gitlink committed with: LS-001 record moved `draft` → `verified`
  (with the `verified-against` pin the UPSTREAM-INDEX gate requires), both index mirrors, the
  vendor README, LS-001's REPORT.md, `MEMORY.md`, `CHANGELOG.md`, and this tree — one commit.

## DEPARTURES FROM THE PUBLISHED GUIDE

The acceptance says the integration follows the published document and that departures are named.
Three from `2026-09-20`, all mine, all corrected upstream since (the guide now teaches each):

1. **Jumped to line 198** as directed and skipped *Initial PGEN preparation* 100 lines earlier.
   Build failed on `generated/return_annotation_parser.rs`. The guide is explicit — *"Checkout does
   not generate PGEN's parser inputs"* — and I had not read it.
2. **Used `git submodule update --init --recursive`** where the guide prescribes two targeted
   inits. Cost: 1.7 GB and 30 nested submodules instead of the needed closure.
3. **Used bare `cargo` and my own target directory** instead of `tools/run_cargo_local.sh` and the
   prescribed `.app-data/` layout. Corrected; the guide's layout is also the one Policy 13 wants.

One new, named rather than corrected: the guide's Lispish section now prescribes **copying the
consumer source into the application's own crate**; this project builds the vendored example
workspace in place (binary lands at the same `.app-data/target/debug/lispish_file` the harness
reads), because the semulith root manifest is a virtual workspace with no package to own a
`src/bin/`. The guide itself documents the example as runnable; the previous pin's verified build
did the same. Revisit when the engine crate adopts the reader.

## Acceptance Checklist (leaf SOT-FORMAT.1)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHERE: "it parses" was the only gate an S-expression
  file faced — the reader accepts a mistyped head silently, exit 0:

  ```
  $ printf '(sourcs (id "u") (width 32))' > target/doctrine_scratch/sourcs.sexp
  $ python3 scripts/sexp.py target/doctrine_scratch/sourcs.sexp
  ok: 1 top-level form(s); heads: sourcs          (rc=0 — nothing refused the typo)
  ```

- [x] **ADDRESSED (verified)** — leg 2. `schema/schema.sexp` is the language in itself;
  `scripts/check_sexp_schema.py` validates any file against any schema and refuses by name:

  ```
  $ python3 scripts/check_sexp_schema.py schema/schema.sexp schema/schema.sexp
  check_sexp_schema: ok — schema/schema.sexp conforms to schema.sexp
  $ python3 scripts/check_sexp_schema.py --self-test
  check_sexp_schema --self-test: 16 pass / 0 fail
  ```

  The 13 RED arms name their reason: undeclared construct, undeclared field, missing required
  field, three wrong-arity shapes, two wrong-value-type shapes, duplicated single-valued field,
  values restriction, wrong form head, recursive-nesting violation, two meta-level schema abuses.

- [x] **NO REGRESSION** — leg 3. The schema layer is additive; no consumer changed. The enforcer
  after staging: `bash scripts/check_doctrines.sh → === all doctrines green ===`.

- [x] **LOCKSTEP** — `schema/` registered in `doctrine/readme_routes.tsv` in the creating commit
  (partitioned, same shape as `definitions/`); `TOOLBOX.md` gains the row; this tree updated in
  the same commit.

## Acceptance Checklist (leaf SOT-FORMAT.10)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHERE: `scripts/compare_readers.py` compared two
  readers while the format carried three contracts; the Lispish route's extraction semantics
  made the two CLASS families unavoidable, so the sweep carried a classification layer instead
  of the fix — measured, four classified atoms on the catalogue alone:

  ```
  $ python3 scripts/compare_readers.py 2>/dev/null | grep -c '^  class'
  4
  ```

- [x] **ADDRESSED (verified)** — leg 2. Reader C (`sexpr_file` over `SExprDocumentV1.spec`)
  joined the sweep additively; its normalisation uses ONLY sexp.py's own tables (`_ESCAPES`,
  `_atom`):

  ```
  $ python3 scripts/compare_readers.py --self-test
  compare_readers --self-test: 28 pass / 0 fail        (21 -> 28; 7 document-layer arms)
  $ python3 scripts/compare_readers.py
    agree   definitions/riscv/m.sexp             438 nodes identical [lispish]; 439 nodes, 1 form(s) [document]
    agree   definitions/riscv/rv64i.sem.sexp    1550 nodes identical [lispish]; 1551 nodes, 1 form(s) [document]
    agree   definitions/riscv/rv64i.sexp        1716 nodes identical [lispish]; 1717 nodes, 1 form(s) [document]
    agree   materials/catalog.sexp              1792 nodes identical [lispish]; 1793 nodes, 1 form(s) [document]
    agree   profiles/rv64i-lab-v0/encoding.sexp   18 nodes identical [lispish];   19 nodes, 1 form(s) [document]
    agree   schema/schema.sexp                     5 nodes identical [lispish];  158 nodes, 4 form(s) [document]
    compare_readers: 6 of 6 file(s) agree
  ```

  The document layer shows ZERO class notes — the four atoms the Lispish layer classifies
  (quoted-numeric, escape-retention) simply agree there, by construction; every form in every
  file is compared (43 forms in the catalogue, 4 in the new schema.sexp — the fixpoint file now
  verifies through the document grammar too); and the sweep grew to 6 files because schema.sexp
  itself joined the tracked corpus this session. The +1 node counts are the document layer
  counting the root form itself — cosmetic, consistent, and not a difference.

- [x] **NO REGRESSION** — leg 3. The Lispish layer is untouched — same four CLASS notes, same
  verdicts, and the surrounding guards unmoved:

  ```
  $ python3 scripts/compare_readers.py 2>/dev/null | grep -c '^  class'
  4
  $ python3 scripts/sexp.py --self-test | tail -1
  sexp --self-test: 18 pass / 0 fail
  ```

- [x] **LOCKSTEP** — `TOOLBOX.md`'s row updated to the three-reader sweep; this tree and
  `MEMORY.md` in the same commit.

## Acceptance Checklist (leaf SOT-FORMAT.3)

- [x] **REPRODUCE / ISSUE** — the split the tree exists to end, shown at the records:

  ```
  $ ls profiles/rv64i-lab-v0/*.jsonl
    requirements.jsonl  contract-obligations.jsonl          # 26 + 34 records, JSON Lines
  $ ls schema/ | grep -c 'requirements\|obligations'
    0                                                       # the schema layer declares nothing for them
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — tool-backed. WHY: the record grammar of `schema.sexp` could
  state structure but not the contracts' discriminating detail — id shapes, non-empty prose,
  at-least-one citations, uniqueness — so a straight conversion would have been strictly weaker
  than the JSON Schema it replaced, and `parameters` was worse: the JSON schema's own
  `additionalProperties: {type: [string, number, boolean, null]}` excluded the arrays three
  obligations write, and the tracked validator never descended into it, so the lie was unmeasured.
  WHERE: the gap sat between `schema/schema.sexp`'s `(field …)` kind and
  `schemas/{requirement,contract-obligation}.schema.json`'s pattern/minItems/uniqueItems/
  minLength/additionalProperties keywords.

  ```
  $ python3 - <<'PY'
  > import json
  > ob = json.loads(open("profiles/rv64i-lab-v0/contract-obligations.jsonl").readline())
  > print("legal_access_widths_bits" in ob["parameters"], type(ob["parameters"]["legal_access_widths_bits"]).__name__)
  False list        # hmm — first record is OB-XLEN; the arrays live in OB-ENV-ACCESS-WIDTHS
  $ grep -o 'legal_access_widths_bits[^]]*]' profiles/rv64i-lab-v0/contract-obligations.jsonl | head -1
  legal_access_widths_bits": [8, 16, 32, 64]     # an array, under a schema whose additionalProperties bans arrays
  ```

- [x] **FIX** — four optional field FACETS in the kernel (`(pattern …)`, `(min-length N)`,
  `(min N)`, `(unique yes)`), declared in `schema/schema.sexp` so the fixpoint keeps describing
  the whole language; two record schemas with JSON keys verbatim as field names and enums under
  `(values …)`; `parameters` as typed wrappers; the mapping owned solely by
  `scripts/records_sexp.py`; the migration and its proof in `scripts/convert_records.py`.

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  ```
  $ python3 scripts/convert_records.py verify profiles/rv64i-lab-v0/requirements.jsonl \
      profiles/rv64i-lab-v0/requirements.sexp
    round-trip ok: 26 requirements record(s), field-by-field equal and byte-identical on re-dump
  $ python3 scripts/convert_records.py verify .../contract-obligations.jsonl .../contract-obligations.sexp
    round-trip ok: 34 contract-obligations record(s), field-by-field equal and byte-identical
  $ python3 scripts/check_sexp_schema.py profiles/rv64i-lab-v0/requirements.sexp schema/requirements.sexp
    check_sexp_schema: ok — requirements.sexp conforms to requirements.sexp
  $ python3 scripts/check_sexp_schema.py profiles/rv64i-lab-v0/contract-obligations.sexp \
      schema/contract-obligations.sexp
    check_sexp_schema: ok — contract-obligations.sexp conforms to contract-obligations.sexp
  $ bash scripts/check_requirements.sh --self-test
    RECORD-SCHEMA --self-test: 22 pass / 0 fail        # the 15 old scenarios re-fired on the
                                                       # converted form + 4 facet arms + 1 standalone
  $ bash scripts/check_requirements.sh
    RECORD-SCHEMA: ok (5 record file(s) validate and agree with their profile)
  $ scripts/gate_report.py rv64i-lab-v0 && git diff --stat -- profiles/rv64i-lab-v0/G0-REPORT.md
    # diff: input names only; 26 requirements, 34 obligations, 68 checks, verdict unchanged
  ```

- [x] **NO REGRESSION** — `sexp --self-test` 18/0; kernel 43/0 (31 → 43; fixpoint green);
  `convert_records --self-test` 9/0; `check_semantics.py` 52 of 52 byte-identical verdict;
  `run_smoke.py` ok (4 guests, both models, reproduce); `compare_readers.py` **13 of 13 agree**
  (the two catalogues and two schemas joined the sweep; zero class notes); `check_citations.py`
  52 of 52; `materials.py --self-test` 20/0; profile dossier sizes 19,545 + 28,449 B — under the
  `profiles/` 32 KiB per-part ceiling, so no re-derivation was needed.

- [x] **LOCKSTEP** — `docs/ARCHITECTURE.md` §1.1/§1.3 current; `LIVE_STATUS.md` (catalogue rows,
  and the stale 33-obligation/66-check row re-derived to 34/68 — a drift found while migrating,
  fixed in passing); `profiles/rv64i-lab-v0/{DOSSIER,ENVIRONMENT,G0-REPORT}.md`; both doctrine
  mirrors' `RECORD-SCHEMA` rows; `TOOLBOX.md` (two rows); `MEMORY.md`; `DEV_NOTES.md` (dated
  entry; promotion declined in this leaf); `CHANGELOG.md`; `docs/TASK_TREE.md` — one commit.

## Acceptance Checklist (leaf SOT-FORMAT.4)

- [x] **REPRODUCE / ISSUE** — the split the tree exists to end, shown at the dossier:
  `ls profiles/rv64i-lab-v0/*.toml *.json` listed `profile.toml  references.toml  sources.toml
  state.json` beside the S-expression corpus; `grep -c '^#' references.toml` -> `65` — a fifth
  of that file was commentary `tomllib` discarded on every read.

- [x] **ROOT CAUSE (WHY + WHERE)** — tool-backed. WHY: a comment-rich human-authored document
  cannot lose its commentary, and a merge cannot read three formats. WHERE: `grep -lE 'tomllib|
  json\.loads' scripts/*.py scripts/*.sh` -> eight files: both record gates, `gate_report.py`,
  `run_smoke.py`, `compare_platforms.py`, both fetch scripts, `check_citations.py` — every one
  parsing a source of truth outside the format.

- [x] **FIX** — one reserved `comment` head in the kernel (annotations skipped, never declared);
  `scripts/dossier_sexp.py` the single mapping owner; `scripts/convert_dossier.py` the migration
  and its proof; six schema files; consumers changed at the seam (same dicts, new loader); the
  Sail override's JSON derived from the tracked `.sexp` on every run.

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:
  `convert_dossier.py verify` on all nine documents -> each `round-trip ok`, field-for-field
  equal, comment census exact, schema-conformant; `check_profile_consistency.sh --self-test`
  -> `39 pass / 0 fail` (rule 5b included); `run_smoke.py` -> `ok` and `compare_platforms.py`
  -> `4 of 4` — identical verdicts.

- [x] **NO REGRESSION** — kernel 50/0; dossier 11/0; converter 12/0; RECORD-SCHEMA 22/0;
  `sexp --self-test` 18/0; `check_semantics.py` and `check_citations.py` 52 of 52 each;
  `fetch_references.sh --verify-only` ok (incl. the 52 == 52 scope cross-check through
  `profile.sexp`); the regenerated G0 report diffs in input names only, every count byte-stable;
  `compare_readers.py` sweeps 28 of 28 files across all three readers.

- [x] **LOCKSTEP** — `docs/ARCHITECTURE.md` §1.1/§1.3; the profile's `DOSSIER.md` /
  `ENVIRONMENT.md` / `G0-REPORT.md`; both doctrine mirrors' `RECORD-SCHEMA` row; `TOOLBOX.md`
  (two rows); `doctrine/readme_routes.tsv` (`schema/` re-derived, grounds recorded);
  `MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md` (lesson promoted to
  `docs/knowledge/portable-shell-fixtures-keep-mutations-whole-line.md`), `docs/TASK_TREE.md`
  and this tree — one commit.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-27` | `SOT-FORMAT.4` | `convert_dossier.py verify`, all nine documents | each `round-trip ok` — field-for-field equal, comment census exact (27 + 35 + 65 + 12 + 12 + 5 + 12 lines), schema-conformant |
| `2026-09-27` | `SOT-FORMAT.4` | self-tests: kernel · dossier · converter · PROFILE-CONSISTENCY · RECORD-SCHEMA | `50/0` (7 comment arms) · `11/0` · `12/0` · `39/0` (rule 5b re-fired) · `22/0` — all on the converted form |
| `2026-09-27` | `SOT-FORMAT.4` | `run_smoke.py` / `compare_platforms.py` / materialized Sail JSON | `ok` and `4 of 4` — identical verdicts; the derived JSON byte-identical to the tracked original |
| `2026-09-27` | `SOT-FORMAT.4` | ceilings + sweep | `references.sexp` 30,012 B < 32,768 (no `profiles/` re-derivation needed); `schema/` re-derived 12 → 24; `compare_readers` 28 of 28 agree (3 documented LS-002 class notes in `sources.sexp` comment strings) |
| `2026-09-27` | `SOT-FORMAT.3` | round-trip, both catalogues | byte-identical on re-dump; 26 + 34 records field-by-field equal |
| `2026-09-27` | `SOT-FORMAT.3` | kernel self-test | `43 pass / 0 fail` (31 → 43; 12 facet arms, each RED arm naming its reason) |
| `2026-09-27` | `SOT-FORMAT.3` | RECORD-SCHEMA self-test | `22 pass / 0 fail` — the 15 old scenarios on the converted form + facet refusals + standalone-obligation arm |
| `2026-09-27` | `SOT-FORMAT.3` | RECORD-SCHEMA real run | ok, 5 record file(s): 3 frozen-example JSONL + 2 converted catalogues |
| `2026-09-27` | `SOT-FORMAT.3` | `compare_readers.py` corpus sweep | **13 of 13 agree**, zero class notes (catalogues + record schemas joined) |
| `2026-09-27` | `SOT-FORMAT.3` | regression: semantics / smoke / citations / materials | 52 of 52 · ok · 52 of 52 · 20/0 |
| `2026-09-27` | `SOT-FORMAT.3` | per-part ceiling probe | 19,545 B + 28,449 B vs 32,768 — no registry re-derivation needed |
| `2026-09-27` | `SOT-FORMAT.2` | the 32 forms are data — `grep -c '^(operator' schema/semantics.sexp` | `32` |
| `2026-09-27` | `SOT-FORMAT.2` | `52 of 52` before→after diff of `check_semantics.py rv64i.sexp rv64i.sem.sexp` | **byte-identical**, rc 0 both (baselines in `target/doctrine_scratch/sf2/`) |
| `2026-09-27` | `SOT-FORMAT.2` | MODEL-METHOD.9 controls missing / operand / no-source, before→after | **byte-identical**, rc 1, each refused by name |
| `2026-09-27` | `SOT-FORMAT.2` | MODEL-METHOD.9 control unknown-form, before→after | rc 1, names `'widget'`; the message now points at `schema/semantics.sexp` instead of the FORMS table it named (the only output change; the table no longer exists) |
| `2026-09-27` | `SOT-FORMAT.2` | 33rd form, zero Python: append `(operator (name rot) (fixed 2))` to `schema/semantics.sexp`, run a one-instruction fragment using `(rot …)` | `unknown form 'rot'` rc 1 → `1 of 1 declared instruction(s) have checked semantics` rc 0; structurally conformant too; **reverted** — schema back to 32 operators, `rot` refused again |
| `2026-09-27` | `SOT-FORMAT.2` | corpus validation: encoding/fragment(+m)/semantics against the new schemas | all `check_sexp_schema: ok — … conforms` |
| `2026-09-27` | `SOT-FORMAT.2` | `check_sexp_schema.py --self-test` | `31 pass / 0 fail` (16 → 31; 15 new operator arms, every RED arm asserting its reason) |
| `2026-09-27` | `SOT-FORMAT.2` | regression: sexp, materials, citations, smoke, gen_fragments regeneration, encoding-disjoint | `18/0`, `20/0`, `52 of 52`, `ok`, `git diff --stat -- definitions/` empty, `the fragments COMPOSE` |
| `2026-09-27` | `SOT-FORMAT.2` | `bash scripts/check_doctrines.sh` | `=== all doctrines green ===` (after staging; the three new schema files join `compare_readers`' sweep at tracking — it enumerates `git ls-files '*.sexp'`, and re-run post-stage shows **9 of 9 agree**, document layer zero class notes) |
| `2026-09-26` | `SOT-FORMAT.10` | consumer probe of the document grammar on a synthetic file | tagged kinds + raw lexemes confirmed (`"20260911"` → kind string; escapes verbatim; `0x10` → number) |
| `2026-09-26` | `SOT-FORMAT.10` | `--self-test` | `28 pass / 0 fail` |
| `2026-09-26` | `SOT-FORMAT.10` | corpus sweep, both layers | **6 of 6 agree**; document layer zero class notes; Lispish layer unchanged (same four CLASS notes); schema.sexp itself passes both layers |
| `2026-09-26` | `SOT-FORMAT.1` | corpus grammar read before design (m.sexp, rv64i.sexp, rv64i.sem.sexp, encoding.sexp) | two form shapes + markers; first uniform-pair design refuted by the real files and redesigned before it shipped |
| `2026-09-26` | `SOT-FORMAT.1` | `--self-test` | `16 pass / 0 fail` (13 RED, 3 GREEN) |
| `2026-09-26` | `SOT-FORMAT.1` | the fixpoint standalone | `schema/schema.sexp conforms to schema.sexp` |
| `2026-09-26` | `SOT-FORMAT.8` | drift probe: `grep -c 'S-expression' docs/ARCHITECTURE.md` | `0` — the chapter named no format, no `definitions/`, no composition |
| `2026-09-26` | `SOT-FORMAT.8` | after the §1.1–§1.3 addition, same probe | `4` — format, fragment, composition operator, schema layer all present in prose |
| `2026-09-26` | `SOT-FORMAT.8` | `make book` | built; the chapter includes the source verbatim, so the preface needed no edit |
| `2026-09-26` | `SOT-FORMAT.8` | claim audit of the new prose against instruments | every built-state claim names its tool (sexp self-test, compare_readers, check_semantics 52/52, check_encoding_disjoint); the schema layer is labeled specified-not-built; the mutable count rephrased to "agreement file by file" |
| `2026-09-26` | `SOT-FORMAT.9` | fix present at new pin: `show a8d34c845:specs/Lispish.spec` | `dquotes`/`squotes` carry `(?s)` — the reported DOTALL form, shipped upstream as `8259719f8` |
| `2026-09-26` | `SOT-FORMAT.9` | RGX pin at old vs new commit | `8763a0e6bea9` both sides — bootstrap products valid; bootstrap re-run said "already generated" |
| `2026-09-26` | `SOT-FORMAT.9` | consumer rebuild at new pin via `run_cargo_local.sh` | ok, 20.39 s, fresh `.app-data/target/debug/lispish_file` |
| `2026-09-26` | `SOT-FORMAT.9` | LS-001 repro against new pin (`.sexp` cases + real grammar) | **8 matched / 0 differed** (was 4/4) — state earns `verified` |
| `2026-09-26` | `SOT-FORMAT.9` | census probe over every tracked `.sexp`, all positions | 2 quote-numeric + 2 escape-retention in `materials/catalog.sexp`, nothing else anywhere |
| `2026-09-26` | `SOT-FORMAT.9` | `compare_readers.py --self-test` after classifier | `21 pass / 0 fail` (9 new arms: 4 classification, 5 masking) |
| `2026-09-26` | `SOT-FORMAT.9` | RED proof: comparator vs pre-fix grammar on catalog.sexp | `DIFFER <root>: A has 43, B has 6`, rc=1 — discrimination intact |
| `2026-09-26` | `SOT-FORMAT.9` | both readers over every tracked `.sexp` at the new pin | **5 of 5 agree** — acceptance met |
| `2026-09-26` | `SOT-FORMAT.9` | regression: sexp, citations, materials, smoke, doctrines | 18/0, 52 of 52, 20/0, ok, green |
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
| `SOT-FORMAT.4` | `SEMILITH-SF-0059 (leaf SOT-FORMAT.4): …` | the dossier behind the schema layer; the reserved comment head; six schemas; 39 arms re-fired; byte-identical override derivation |
| `SOT-FORMAT.3` | `SEMILITH-SF-0058 (leaf SOT-FORMAT.3): …` | the records behind the schema layer; field facets; typed parameters; byte-identical round-trip; 22 record arms |
| `SOT-FORMAT.2` | `SEMILITH-SF-0057 (leaf SOT-FORMAT.2): …` | the operator kind; three domain schemas; the 32 forms are data; 52/52 byte-identical; 31 schema arms |
| `SOT-FORMAT.1` | `SEMULITH-SF-0054 (leaf SOT-FORMAT.1): …` | the schema language in itself; 16 arms; fixpoint green; schema/ registered in the creating commit |
| `SOT-FORMAT.8` | `SEMULITH-SF-0053 (leaf SOT-FORMAT.8): …` | ARCHITECTURE.md gains §1.1–§1.3; the director's window shows the format now |
| `SOT-FORMAT.9` | `SEMULITH-SF-0051 (leaf SOT-FORMAT.9): …` | pin advanced to `a8d34c845`; 5 of 5 agree; comparator enumerates 2 documented CLASS families; LS-001 verified |
| `SOT-FORMAT.9` | `SEMULITH-SF-0047 (leaf SOT-FORMAT.9): two readers, one format, and a defect worth reporting` | **progress on a blocked leaf**, not a completion: 4 of 5 files agree |
| `SOT-FORMAT.7` | `SEMULITH-SF-0041 (leaf SOT-FORMAT.7): the reader corrupted every citation it read` | 52 of 52 citations restored; 18 arms where there were none |

## Changelog

- `2026-09-14`: Created. Supersedes the format split in `decision_canonical-definition-input`, which
  I had defended on the grounds that records are not trees — a true statement about shape that
  answered the wrong question. The question is whether two of them can be merged by a defined rule.
