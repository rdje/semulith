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
  Status: `done`
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
  Status: `done`
  Goal: define and check the union of two units' records across a composition boundary —
  requirements, obligations, sources — with conflict detection, the way encodings already union.
  Acceptance: two units compose their records or are rejected with the conflicting fact named;
  fired RED on a genuine contradiction; feeds `MODEL-COMPOSE.3`'s assumption/guarantee discharge,
  which can then read one format.
  Result: met, `2026-09-27`. `scripts/merge_records.py` defines the union and checks it: the
  real profile idempotently self-composes (26 + 34 + 3), a one-statement edit in a copied unit
  is refused with the field, both values and both units named, and a scratch extension unit
  whose requirement depends on the base's `REQ-D-XLEN` composes — and is refused by name when
  the base is withheld. `MODEL-COMPOSE.3` reads the merged view through `merge_units(…)`,
  including the direction census (26 cpu-guarantee, 8 environment-assumption).
  Design (recorded before code, `2026-09-27`), the corpus read in full first, the way `.1`–`.4` did:
  - ⭐ **The unit is a directory; the merge reads through the single mapping owners.** A unit
    carries up to three catalogues by name — `requirements.sexp`, `contract-obligations.sexp`,
    `sources.sexp` — read through `records_sexp.py` / `dossier_sexp.py`, the same dicts the
    gates see. A missing catalogue is the empty set (absence is the empty list, the `.3` rule);
    a missing directory is REFUSED (composing nothing is not composing — the empty-fragment
    refusal of `MODEL-COMPOSE.1`). The merge never parses S-expressions itself.
  - **Merge key = `id`; content equality on collision; `profile_ids` is membership, not
    content.** Two records with the same id must agree on every field EXCEPT `profile_ids`,
    which unions by set-union: a record's applicability list is provenance of which units carry
    it, and the composed unit genuinely applies to both. The same `statement`, `risk`,
    `authority`, `source_refs`, `dependencies`, statuses… under one id is a contradiction:
    REFUSED, naming the field, both values, and both units. Same id + different content in one
    composed unit is a catalogue lying about itself.
  - **Sources merge by source `id` with full-pin equality.** The same source id must pin
    identical bytes (`sha256`, `bytes`, `file`, `title`, `http_status`, `chapter_version`,
    `supplies`); a digest difference for the same id means the two units read different texts of
    "the same" specification — REFUSED naming the field. The document envelope (`publication`,
    `revision`, `base_url`, `retrieved`, `work_dir`) is per-unit metadata: it is NOT part of the
    merge verdict, and which envelope a future emitted composed ledger carries is its emitter's
    decision — a named boundary, deferred to the consumer that emits (the engine, or
    `MODEL-COMPOSE.5`).
  - **The union is closed: references resolve across the boundary.** After the union, every
    `dependencies` id (requirements and obligations alike), every requirement `obligation_ids`,
    and every `source_refs.source_id` must resolve in the union. A reference resolving in
    neither unit is REFUSED, naming the referrer, the missing id, and the unit that carried it.
    This is RECORD-SCHEMA rules 2/5/6 lifted from "within one file" to "within the composed
    unit" — the cross-boundary case the format split made impossible to even state.
  - ⭐ **Measured defect found while designing this leaf, fixed in it (§15 ownership):**
    RECORD-SCHEMA never refuses duplicate record ids within one catalogue. Its `by_id` dict
    silently collapses them (last wins), so a catalogue can contradict itself and stay green.
    Probe (`target/doctrine_scratch/dupprobe`, extracted gate body on a scratch root): two
    `REQ-D-A` records differing in `risk` → `rc=0`. Fixed by adding rule 8 (DUPLICATE-ID) to
    `check_requirements.sh`, fired RED there — one owner of catalogue discipline; the merge
    re-checks it as a precondition because it must stay robust for draft units that never
    passed the gate.
  - **The deliverable is the checker, not a merged file** — the shape of
    `check_encoding_disjoint.py`: a verdict (`the units COMPOSE`) or a refusal naming every
    conflicting fact. Emitting a composed dossier is downstream work; this leaf defines the
    union and proves the check. The module is importable (`merge_units(…)`) so
    `MODEL-COMPOSE.3` reads the same merged view. The verdict reports the composed contract's
    direction census (cpu-guarantee vs environment-assumption) — the assumption inventory
    `docs/CPU_ENVIRONMENT.md` §4 asks to export, and the hook `.3` discharges against.
  - Real-corpus proof plan: (1) idempotent self-merge — `rv64i-lab-v0` with itself composes,
    every record colliding equal; (2) a genuine contradiction fired RED on real data — a
    scratch copy of the profile with one statement edited → CONFLICT naming the field and both
    values; (3) the composition-boundary case — a scratch extension unit carrying a new
    requirement that depends on the base's `REQ-D-XLEN` plus a new source → composes, and the
    cross-boundary dependency resolves in the union.

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
| 1 | `SOT-FORMAT.6` | `pending` | the gate can only be green after the last file moved — and `.5` has now moved it |

## Decisions

| Date | Decision | Rationale |
| --- | --- | --- |
| `2026-09-27` | Record merge: key = `id`; collision = content equality on every field except `profile_ids`, which unions — it is membership, not content | two units carrying the same record (a shared base) differ only in which units carry it; the composed unit genuinely applies to both. Same id + different content is a catalogue lying about itself — refused, field and both values named |
| `2026-09-27` | Sources merge by source `id` with full-pin equality; the document envelope is not part of the verdict | the same source id with different digests means two units read different texts of "the same" specification — the exact contradiction a merge exists to catch. The envelope (`publication`/`revision`/…) is per-unit metadata; which envelope an EMITTED composed ledger carries is its emitter's decision (deferred to the engine / `MODEL-COMPOSE.5`) |
| `2026-09-27` | An obligation's `dependencies` resolve against requirements ∪ obligations; a requirement's against requirements | measured on the corpus: every cpu-guarantee depends on its requirement (`OB-XLEN` → `REQ-D-XLEN`), every environment-assumption on the guarantees it discharges (`OB-ENV-RESET` → `OB-ENTRY-STATE`). The namespaces were inferred from data, not assumed |
| `2026-09-27` | The merge checker re-checks intra-unit id uniqueness as a precondition, and RECORD-SCHEMA gains rule 8 (UNIQUE-ID) as the one owner of catalogue discipline | the design probe showed the gate's id → record map silently collapsed duplicates (last wins), so a self-contradicting catalogue stayed green, `rc=0`. The merge must stay robust for draft units that never passed the gate, so both refuse |
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

## Acceptance Checklist (leaf SOT-FORMAT.5)

- [x] **REPRODUCE / ISSUE** — the split the tree exists to end, shown at the composition
  boundary: §1.2 of `docs/ARCHITECTURE.md` promised "merging records and obligations across a
  composition boundary … lands with `SOT-FORMAT.5`", and nothing in the repository could do it.
  Census before this leaf:

  ```
  $ git ls-files scripts | grep -E 'merge|compose' | grep -v encoding_disjoint
  (no output)                                        # union of records: no rule, no tool
  $ grep -n 'by_id = ' scripts/check_requirements.sh
  by_id = {r.get("id"): r for r in recs}             # and, measured below, silently collapsing
  ```

  ⭐ Two defects surfaced while designing the fix, probe-backed (TOOLS-FIRST, both before any
  code was written):
  1. **RECORD-SCHEMA never refused duplicate record ids.** Two records sharing an id collapsed
     in the `by_id` map (last wins), so a catalogue could contradict itself and stay green:

     ```
     $ # scratch catalogue, two REQ-D-A records differing in 'risk', gate body extracted verbatim
     $ python3 target/doctrine_scratch/dupprobe/gate_body.py target/doctrine_scratch/dupprobe
     __CHECKED__ 1                                    # rc=0 — nothing refused the contradiction
     ```

  2. **Obligation `dependencies` were never checked at all** (the gate checks requirements'
     only), and the corpus's environment-assumptions depend on *obligations*
     (`OB-ENV-RESET` → `OB-ENTRY-STATE`), not on requirements — a namespace fact that had to be
     measured, not assumed:

     ```
     $ # the merge's first closure run on the real profile (obligation deps looked up wrong)
     DANGLING DEP obligation 'OB-ENV-RESET' depends on 'OB-ENTRY-STATE', which no unit provides
     # yet OB-ENTRY-STATE IS an obligation record — 34 of 34 exist; the corpus is mixed-kind:
     # cpu-guarantees depend on requirements, environment-assumptions on guarantees
     ```

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHY: a merge is only definable over one format,
  and even with one format it is only *checkable* if ids are unique within each side and
  references resolve across the union. WHERE: measured, not read —

  ```
  $ grep -n 'by_id = ' scripts/check_requirements.sh          # the gate's id → record map
  by_id = {r.get("id"): r for r in recs}     # last wins: a duplicate id silently collapses
  $ python3 target/doctrine_scratch/dupprobe/gate_body.py target/doctrine_scratch/dupprobe
  __CHECKED__ 1                              # rc=0 — a self-contradicting catalogue stays green
  ```

  The gap sat between `scripts/records_sexp.py` (the mapping, which has no opinion about
  duplicates) and that map; and between the gate's rule 5 (requirements-only dependency check)
  and the obligation records' `dependencies`, which no rule owned.

- [x] **FIX** — `scripts/merge_records.py`: the merge rule as data (key = id, content equality
  on collision, `profile_ids` union, sources full-pin equality, closure over the union,
  direction census for `.3`); RECORD-SCHEMA rule 8 (UNIQUE-ID) as the one owner of catalogue
  discipline, with a fired RED arm. The merge reads only through the mapping owners and parses
  nothing itself.

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  ```
  $ python3 scripts/merge_records.py --self-test
  merge_records --self-test: 18 pass / 0 fail        # 10 GREEN unions, 8 RED contradictions
  $ python3 scripts/merge_records.py profiles/rv64i-lab-v0 profiles/rv64i-lab-v0
  composed: 26 requirement(s), 34 obligation(s) (26 cpu-guarantee, 8 environment-assumption),
            3 source(s) from 2 unit(s)              # the units COMPOSE — idempotent self-merge
  $ # genuine contradiction, fired RED on real data (one statement edited in a copied unit):
  CONFLICT requirement 'REQ-D-XLEN' between units 'profiles/rv64i-lab-v0' and
  'target/doctrine_scratch/sf5/edited': field 'statement' differs — 'profiles/rv64i-lab-v0':
  'XLEN = 64. …' vs 'target/doctrine_scratch/sf5/edited': 'XLEN = 32, edited …'   rc=1
  $ # the composition-boundary case — an extension unit needing the base's REQ-D-XLEN:
  $ python3 scripts/merge_records.py profiles/rv64i-lab-v0 target/doctrine_scratch/sf5/ext
  composed: 27 requirement(s), 35 obligation(s) (27 cpu-guarantee, 8 environment-assumption),
            4 source(s) from 2 unit(s)              # the units COMPOSE
  $ python3 scripts/merge_records.py target/doctrine_scratch/sf5/ext        # base withheld:
  DANGLING DEP requirement 'REQ-EXT-DEMO' … depends on 'REQ-D-XLEN', which no unit provides
  ```

  And the RECORD-SCHEMA fix, before → after on the same probe:

  ```
  $ python3 target/doctrine_scratch/dupprobe/gate_body.py target/doctrine_scratch/dupprobe
  DUPLICATE ID p/requirements.sexp: record 'REQ-D-A' appears more than once — …   rc=1
  $ bash scripts/check_requirements.sh --self-test
  RECORD-SCHEMA --self-test: 23 pass / 0 fail        # was 22; +1 DUPLICATE-ID arm
  ```

- [x] **NO REGRESSION** — sexp 18/0; kernel 50/0; merge 18/0; RECORD-SCHEMA 23/0 and its real
  run green (`5 record file(s) validate and agree with their profile` — the real catalogues
  carry no duplicate ids, so rule 8 bites nothing that exists); `check_semantics.py` 52 of 52;
  `check_citations.py` 52 of 52; `materials.py --self-test` 20/0; `run_smoke.py` ok;
  `compare_readers.py` 28 of 28 agree; the regenerated G0 report diffs in nothing;
  `make check` green. Whole gate green after staging.

- `promotion: recorded (the duplicate-id lesson is general — an id-keyed lookup that silently
  collapses duplicates turns a self-contradicting catalogue green; the gate now carries the
  rule, the lesson card is docs/knowledge/a-duplicate-id-is-a-contradiction-not-a-shadowing.md).
  The mixed-namespace dependency fact is declined here — it is measured, owned and enforced by
  merge_records.py's closure, where anyone extending the record families will meet it.`

- [x] **LOCKSTEP** — `docs/ARCHITECTURE.md` §1.2 (the merge is no longer "lands with
  `SOT-FORMAT.5`" — it is checked today, the tool named); `TOOLBOX.md` gains the instrument;
  `MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md`, `LIVE_STATUS.md` (177 arms re-derived),
  `docs/TASK_TREE.md` and this tree — one commit. Maintenance the growth fired, same commit:
  this tree's done-leaf checklists split to `docs/tasks/archive/SOT-FORMAT.md` (per-part
  ceiling obeyed, not raised — the P0-PROFILE precedent) and `CHANGELOG.md`'s oldest entry
  sharded to `docs/changelog/shard-0003.md` (SHARD-FREEZE verified: 5 rows, exact partition).

## Completed-leaf evidence

Archived to [`archive/SOT-FORMAT.md`](archive/SOT-FORMAT.md) — the full, unedited acceptance
checklists for every `done` leaf (`.1`–`.4`, `.7`–`.10`). Split out when this file crossed its
per-part ceiling (79,270 bytes against 65,536); the ceiling was obeyed, not raised. The live
tree keeps the frontier, the decisions, the open questions, the current leaf's checklist and
both logs.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-27` | `SOT-FORMAT.5` | merge `--self-test` | `18 pass / 0 fail` — 10 GREEN union arms, 8 RED contradiction arms, each naming its fact |
| `2026-09-27` | `SOT-FORMAT.5` | real profile idempotent self-merge | 26 req + 34 ob (26 cpu-guarantee, 8 environment-assumption) + 3 src — COMPOSE |
| `2026-09-27` | `SOT-FORMAT.5` | genuine contradiction on real data (one statement edited in a copied unit) | `CONFLICT requirement 'REQ-D-XLEN' … field 'statement' differs`, both units named, `rc=1` |
| `2026-09-27` | `SOT-FORMAT.5` | composition-boundary case (scratch extension unit → `REQ-D-XLEN`; base withheld) | with base: 27/35/4 COMPOSE; without: `DANGLING DEP … 'REQ-D-XLEN', which no unit provides` |
| `2026-09-27` | `SOT-FORMAT.5` | RECORD-SCHEMA duplicate-id probe, before → after rule 8 | `rc=0` → `DUPLICATE ID … appears more than once`, `rc=1`; self-test 22 → 23 arms |
| `2026-09-27` | `SOT-FORMAT.5` | corpus dependency-namespace census | requirements depend on requirements only (10/10); obligations mixed — 26 cpu-guarantees on their `REQ-*`, 8 environment-assumptions on `OB-*` guarantees; zero dangling ids |
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
| `SOT-FORMAT.5` | `SEMILITH-SF-0060 (leaf SOT-FORMAT.5): …` | the record merge is definable and checked; RECORD-SCHEMA gains UNIQUE-ID; two probe-found defects closed |
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
