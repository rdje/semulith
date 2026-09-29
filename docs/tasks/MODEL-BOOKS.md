# MODEL-BOOKS: one reviewable book per modelled unit — its materials, and its methodology

## Metadata

- Tree ID: `MODEL-BOOKS`
- Status: `active`
- Roadmap lane: cross-cutting deliverable class; applies to every model from `P0` onward
- Gate: none of its own — it is the surface every other gate's result is read through
- Depends on: `P0-PROFILE` (the first model must exist before it can be documented)
- Unlocks: a reviewer who can judge a model without reading TOML
- Created: `2026-09-14`
- Owner: repo-local workflow

## Goal

Give **every modelled unit its own mdBook** — CPU, MCU, DSP, device, board, SoC — describing how it
went **from PDFs, specifications and descriptions to a fully functional model**. One canonical
definition, one book (`decision_one-definition-one-book`). Each does two things the project cannot
currently do for a reader:

1. **States the complete, detailed list of materials** used to specify that model's functionality
   — every specification document, encoding table, reference model and internal contract — each
   pinned by exact identity, with what it supplies **and what it does not**.
2. **Explains the methodology**: how the project got from those initial documents to the model.
   Document → decision → requirement → obligation → check, in prose a reviewer can follow.

Explanation stays **essentially prose**. Code and data snippets appear only where they make a
point faster than a paragraph would; tables are used for the materials list, where a list is the
honest form.

⭐ **And the book carries a second mandate: it is a teaching text.**
`decision_dual-mandate-production-and-teaching` makes every model both signoff production work and
material a student can learn to build production models from — including models capable of running
real compiled code. Concretely, for this tree: the reasoning is recoverable and not just the
result; **the mistakes stay in**, because a matched profile that matched only an instruction set
and a comparator that called a truncated trace agreement are the most instructive pages available;
the *order* of the work is justified rather than listed; and each chapter is written so a reader
could **build** from it rather than only agree with it.

## Why this is a gap, stated as a measurement

Everything a reviewer needs about `rv64i-lab-v0` already exists — and exists as **13 files of
TOML, JSONL and reference prose** inside `profiles/rv64i-lab-v0/`. The project-wide book
(`docs/book/`) narrates the *plan* and the *working practices*; it has no chapter that answers
*"what documents define this processor, and how did you get from them to a model?"*

A materials list that lives only in `sources.toml` is a list the reviewer will not read, and a
methodology that lives only in nine task-tree leaves is a methodology nobody can follow end to end.

## Non-Goals

- **Not a second owner of any fact.** The book renders what `profiles/<id>/` already holds; where
  it states a pinned digest, a count or a verdict, that content is **generated or gated**, never
  retyped. `docs/book/` learned this lesson already — the contracts are included verbatim there so
  the book cannot drift from them.
- **Not a replacement for the project book.** `docs/book/` keeps the plan, the milestones and the
  working practices. A model book is about **one model**.
- **Not documentation of an implementation.** No CPU code exists. A model book documents the
  *specification of the model* and the *route from documents to it* — and must say plainly where
  the route stops.

## Acceptance Criteria

1. Every **registered modelled unit** has a book, and a gate says so — a unit without one is a
   unit whose materials are unreviewable. Today exactly one unit exists (`rv64i-lab-v0`, kind
   `cpu`); the requirement is structural so the second is cheap rather than a redesign.
2. The materials list is **complete**: every document that contributed to the model appears, with
   its exact identity (locator, revision, digest, size, retrieval date), what it supplies, what it
   does **not** supply, and its terms. Generated from the pinned data and gated against it.
3. The methodology chapter follows at least one rule **end to end** — from the sentence in the
   source document to the check that will test it — so the pipeline is demonstrated, not asserted.
4. `make book` builds every book, and the project book routes to each model book.
5. Prose dominates. A chapter that is mostly listing is a chapter that has not been written yet.
6. ⭐ Each chapter passes the teaching test: **could a reader build something from this, or only
   agree with it?** Where the project got something wrong, the book says what the wrong instrument
   reported and why it was believed — removing that to look competent removes the lesson.
7. The model's ability to run real compiled code is stated with its **limits**, derived from the
   extension set rather than asserted: no `M` means runtime multiply calls, no `A` means no
   atomics, no `F`/`D` means a soft-float ABI.

## Task Tree

- ID: `MODEL-BOOKS.1` — **the book structure, and the complete materials bill**
  Status: `done` (`2026-09-29`)
  Goal: establish `docs/models/<unit-id>/` as the per-unit book — repeatable for every future unit
  of **any kind**, since a board's book and a CPU's book differ in content and not in shape — and
  write the materials chapter: every specification artifact, encoding table, reference
  model and internal contract, generated from `sources.toml` / `references.toml` so a digest cannot
  rot, with prose around each explaining its role.
  Acceptance: the generated material tables agree with the pinned data and a gate fails if not;
  every material states what it does NOT supply; `mdbook build` renders it.
  Design (recorded before code, `2026-09-29`):
  - ⛔ The Goal's `sources.toml` / `references.toml` are STALE references — the one-format
    migration (`SOT-FORMAT.4`, `decision_one-format-every-source-of-truth`) retired them;
    the real pinned data is `profiles/rv64i-lab-v0/sources.sexp` (3 specification
    artifacts) and `profiles/rv64i-lab-v0/references.sexp` (4 reference candidates, the
    RISCV-OPCODES encoding source with 6 pinned files). The generator reads exactly those,
    through `dossier_sexp.py` (the single mapping owner).
  - **The structure** (repeatable — a board's book differs in content, not shape):
    `docs/models/<unit-id>/` is one mdBook — `book.toml`, `src/SUMMARY.md`,
    `src/introduction.md` (what the book is, the unit's kind/layer, and the SHAPE
    CONTRACT: the five-part arc of `decision_one-definition-one-book` — materials, gaps,
    method, model, evidence/gate — each part naming its owning leaf), `src/materials.md`
    (the authored bill — prose dominates, the teaching mandate) and
    `src/materials/*.md` (GENERATED fragments, included by the chapter, never edited:
    `pinned-specifications.md`, `encoding-tables.md`, `reference-models.md`,
    `internal-contracts.md`).
  - **The generator** is `scripts/gen_model_book.py` (the `gen_guests.py`/`gate_report.py`
    pattern): reads the pinned dossier, emits the four fragments with OWN-03 manifests
    (input + generator fingerprints), `--check` reports drift instead of writing, refuses
    by name what it cannot emit. Digests, byte counts, versions, invocations and the
    dossier's record counts are all DERIVED — nothing retyped.
  - **"What it does NOT supply"** is authored prose, mechanized by contract: the bill
    carries one `### \`ID\`` section per material, and each section must contain a
    "does not supply" statement. The gate re-derives the material ids from the pinned
    data and refuses a missing section or a section without the statement.
  - **The gate** is `MATERIALS-BILL` (`scripts/check_materials_bill.sh`, #26), the
    GUEST-GEN pattern: (a) DRIFT — regenerate in memory, byte-compare every fragment;
    (b) COMPLETENESS — every pinned material id has its section with the
    does-not-supply statement. Fired RED against the real corpus before registration;
    self-test RED arms; refuses (exit 2) when it cannot judge; mirrored per the registry
    rules. The "every unit has a book" requirement is `.6`'s wiring, NOT this gate.
  - **Registry repairs:** `materials/units.sexp`'s `book` field points at
    `docs/book/src/profiles/rv64i-lab-v0.md`, a page that was never created — corrected
    to `docs/models/rv64i-lab-v0/` (the one registration place,
    `decision_one-definition-one-book`). `doctrine/fact_ownership.tsv` gains the
    owner→mirror rows (sources/references/dossier → the fragments, governed by
    MATERIALS-BILL). `doctrine/readme_routes.tsv` gains the `docs/models/` family row,
    sized from what lands; per-part 32,768 stays.
  - **The mistakes stay in** (teaching mandate): the bill states plainly that the pinned
    specification artifacts contain NO instruction encodings (measured: the format
    diagrams are images), that the encoding source shares an ancestor with SPIKE and not
    SAIL (so sail decoding our bytes is the independent confirmation, spike's is not),
    and that the PDF question is `.2`'s investigation.
  Result: met, `2026-09-29`. **The per-unit book exists and its materials bill is
  generated, complete and gated.** `docs/models/rv64i-lab-v0/` is one mdBook —
  `book.toml`, `src/SUMMARY.md`, `src/introduction.md` (the shape contract: the
  five-part arc of `decision_one-definition-one-book`, each part naming its owning leaf),
  and `src/materials.md` — the bill, prose-first per the teaching mandate, one `###`
  section per material (15 in all: 3 pinned specification artifacts, the encoding source,
  4 reference candidates, 7 internal contracts), every section stating what the material
  does NOT supply. The four identity tables are GENERATED by `scripts/gen_model_book.py`
  from `sources.sexp` / `references.sexp` / the tracked contracts (OWN-03 manifests:
  input + generator fingerprints; digests, byte counts, versions, invocations and record
  counts all derived — nothing retyped). The 26th doctrine `MATERIALS-BILL`
  (`scripts/check_materials_bill.sh`) holds the two halves: DRIFT (regenerate in memory,
  byte-compare) and COMPLETENESS (every pinned material id has its section, every section
  its does-not-supply statement) — fired RED against the real corpus before registration
  (first `NO BOOK rv64i-lab-v0` on the stale units.sexp `book` path, then a DRIFT row
  when the generator's own edit invalidated its fingerprints), self-test 7/0, mirrored
  per the registry rules. Registry repairs landed as designed: `materials/units.sexp`'s
  `book` field corrected to `docs/models/rv64i-lab-v0/` (the old value named a
  project-book page that was never created); `fact_ownership.tsv` gained the four
  owner→mirror rows; `readme_routes.tsv` gained the `docs/models/` family (8 files /
  27,600 B at adoption; health 16 / 64 KiB; ceiling 40 / 256 KiB; per-part 32 KiB
  untouched). `mdbook build docs/models/rv64i-lab-v0` renders. Two in-flight REDs, both
  the author's: the gate's first unit enumeration read the registry's top-level `(unit …)`
  forms as children of a container that does not exist (self-test caught it: "registry
  empty" on a non-empty registry); and the self-test's own fixture copy nested on re-run
  (`cp -R` into an existing directory), which made one arm fail for the WRONG reason —
  both fixed before registration. No defect in any pre-existing instrument or document.
  Lessons: `promotion: declined (the fixtures caught the author's own wiring mistakes —
  each enforcement IS the lesson; a knowledge card would restate what the gates enforce)`.

- ID: `MODEL-BOOKS.2` — **what the materials do not contain**
  Status: `done` (`2026-09-29`)
  Goal: the chapter a specification bill usually omits. This project measured that its pinned
  artifacts contain **no instruction encodings** (the format diagrams are images), which forced a
  second provenance whose ancestry is shared with one comparator and not the other.
  ⭐ Includes a real investigation: the official specification is also published as **PDF**, and
  whether *that* rendering carries the instruction-format tables as selectable text is unknown. If
  it does, encodings can be re-sourced from the primary document and the shared-ancestry problem
  shrinks. If it does not, the finding is stronger and is recorded as such.
  Acceptance: the PDF is fetched and examined with a tool, not assumed; the outcome is recorded
  either way with the command that established it.
  Result: met, `2026-09-29`. **The gaps chapter landed, and the PDF investigation answers
  YES — measured with `pdftotext`, not assumed.** The pinned publication *does* publish a
  PDF rendering at the same version segment (the pinned `rv64i` page links
  `../_attachments/riscv-unprivileged.pdf`); fetched from
  `docs.riscv.org/reference/isa/v20260120/_attachments/riscv-unprivileged.pdf` (HTTP 200,
  4,580,174 B, sha256 `06bb3c23…`, 696 pages, self-identifying `Version 20260120: Official
  Release`) into the untracked on-volume cache `target/materials/`. The same census pattern
  that measures the pinned HTML's gap (`grep -cE '[01]{7}'` → **0** on all six pinned
  artifacts) matches **232** lines in the PDF's text layer; the base-formats figure and
  the RV32I opcode map (Table 13) extract with their bit strings and field names. So the
  pinned specification's own PDF rendering DOES carry the instruction-format tables as
  selectable text, and encodings CAN be re-sourced from the primary document — the
  second provenance's shared-ancestry exposure is no longer forced. Two qualifications
  recorded with the finding: (1) the PDF numbers chapters differently from the pinned
  HTML (Introduction IS Chapter 1 there — RV32I is Chapter 2, RV64I Chapter 4, against
  the HTML's §1.1/§3.1), so locators need a mapping; (2) the extraction is
  layout-fragmented (one field per line), so re-sourcing is engineering with its own
  verification, not a copy-paste. ⛔ The re-sourcing itself is NOT this leaf — the finding
  and its evidence are recorded; changing where encodings come from is future reviewed
  work. Corroboration: the cached GitHub-release PDF (`RVI-ISA-PDF-20260911`, a different
  publication AND revision) extracts too (269 bit-pattern lines) — the finding depends on
  no one PDF. The PDF is deliberately NOT catalogued in `materials/catalog.sexp` (the
  corpus model is corpus-root-based, no network-origin corpus kind; that is a
  `MODEL-METHOD` decision) — its identity is recorded in the chapter and the verification
  log, its cache untracked. The chapter (`docs/models/rv64i-lab-v0/src/gaps.md`) covers,
  prose-first per the teaching mandate: the no-encodings gap and what it forced (the
  second provenance, the parse-and-refuse assembler discipline), the PDF investigation
  with every command and output, the gaps the specification is SUPPOSED to leave (the
  EEI policy choices; a platform), and the gap the references leave (agreement is not
  proof). The gate was NOT extended — the chapter is authored prose with no generated
  content, so MATERIALS-BILL's surface is unchanged (26 doctrines); `materials.md`'s
  open-question sentence now points at the answered finding.
  Lessons: `promotion: declined (the chapter restates what the investigation measured;
  the measurements ARE the content)`.

- ID: `MODEL-BOOKS.3` — **the methodology: from document to model**
  Status: `done` (`2026-09-29`)
  Goal: the prose chapter that explains the pipeline — how a sentence of specification becomes a
  decision with an *authority*, how a decision becomes a requirement record with a *semantic
  class*, how a requirement becomes an obligation with positive **and negative** checks, and how an
  expected value is *derived* rather than copied.
  Acceptance: one rule is followed end to end, by name, from its sentence to its check; the
  chapter explains the judgement calls (authority vs semantic class) that are not mechanical.
  Result: met, `2026-09-29`. **The methodology chapter landed
  (`docs/models/rv64i-lab-v0/src/methodology.md`), following the reserved-FENCE rule end to
  end, by name, through six inspectable hops** — chosen because its chain is complete in
  tracked files AND because it carries DEFECT-A: the pinned sentence (RVI-RV32I §1.1.7,
  quoted verbatim from the pinned artifact) → `D-FENCE` (authority
  `execution-environment`, the correction note intact) → `REQ-D-FENCE` (class
  `implementation-defined`, statement verbatim under RECORD-SCHEMA's rule 4) → `OB-FENCE`
  (`cpu-guarantee`, CHK-FENCE-POS AND CHK-FENCE-NEG, the MIRROR pair) → `fault-fence`
  (EVD-05 expectations derived before any run, measured on both references first) → the
  differentials that keep it true (the offline suite
  `fault_fence_retires_every_reserved_configuration_as_a_fence`; the live three-way
  smoke). The honest gap is in the chapter, not hidden: the obligation's check ids are
  declared and G0 measures 72 declared / 0 implemented — the named-check layer is the
  release gate's skeleton, and the guest corpus is what tests the rule today. The two
  judgement calls get their own sections: semantic class (what kind of freedom the source
  grants — 28 requirements over four classes) and authority (who may decide — with
  RECORD-SCHEMA's AUTHORITY check as the mechanical edge: laboratory policy cannot
  override an architectural rule). The mistakes stay in, per the teaching mandate:
  DEFECT-A (the dossier condemned the mandated nop; the probe discipline inverted it —
  what the wrong reading reported and why it was believed), DEFECT-B (the misaligned-jump
  link write, fixed in semantics DATA, pinned by `never_written x5`), and the two
  authoring REDs (the hand-assembled overlap constant, the systematic trailing paren) —
  the gates catching the author, not only the model. Every id the chapter names was
  grep-verified against the tracked corpus as it was written (the sweep is the
  checklist's evidence); the quoted decision fragments are verbatim substrings of
  `D-FENCE`'s statement (checked programmatically). No gate extended — the chapter is
  authored prose, no generated content (26 doctrines, unchanged).
  Lessons: `promotion: declined (the chapter restates the pipeline the gates already
  enforce; that is its purpose)`.

- ID: `MODEL-BOOKS.4` — **the references, their configuration, and what agreement is worth**
  Status: `pending`
  Goal: how each reference model was obtained, how it was configured to match the profile, what
  the matched-profile control demonstrated, and the independence inventory — in prose, including
  why three models is not three opinions.
  Acceptance: the configuration story is told through the control that changed the observation,
  not through a configuration file listing.

- ID: `MODEL-BOOKS.5` — **the evidence, the gate, and the traceability walk**
  Status: `pending`
  Goal: what has actually been demonstrated, the gate verdict and why it is `incomplete`, and a
  walk a reviewer can repeat: pick a rule, follow it to its requirement, its obligation, its
  declared checks and the experiment that touches it.
  Acceptance: the walk names real ids at every hop and ends at something re-runnable.

- ID: `MODEL-BOOKS.6` — **wiring: every model has a book, and every book builds**
  Status: `pending`
  Goal: `make book` builds the project book and every model book; the project book and `README.md`
  route to each; `doctrine/readme_routes.tsv` governs the new family; a gate requires a book per
  profile directory.
  Acceptance: adding a profile without a book fails the gate; `make book` builds all books.

- ID: `MODEL-BOOKS.7` — **annex: how the tracked assembler works**
  Status: `done` (`2026-09-29`, director request)
  Goal: a teaching chapter in the PROJECT book (`docs/book/`) that explains
  `scripts/riscv_asm.py` end to end — why it exists, where the encodings come from, how one
  instruction is encoded, and why it refuses — written so a reader could build one, not just
  agree with it (the tree's teaching mandate, applied to the one piece of machinery that turns
  the pinned tables into guest bytes).
  Acceptance: `make book` renders it; every mechanism it states is the mechanism the code
  carries; prose dominates.
  Placement decision: the annex lives in the project book (`annex/assembler.md`), not the
  per-unit book, because the per-unit book structure is `.1` (unbuilt) and the assembler is
  shared project machinery, not one unit's data. When `.1` lands, the model book REFERENCES
  the annex; it does not copy it (this tree's first decision: never a second owner of a fact).
  Result: met, `2026-09-29`. The chapter follows the module's own spine: why it exists
  (EVD-05), the table pipeline (pinned `riscv-opcodes` → fragments → composition → bytes),
  the three operand classes (fixed bits, contiguous fields, the derived B/J scramble with its
  accounted-bits self-check), the two-pass label front-end, the ELF writer (including the
  measured Spike refusal that put a section table in), and the refusal discipline
  (`AsmError` — never a guess). Book chapters 28 → 29 (the count is re-derived by
  `DERIVED-COUNTS`; `LIVE_STATUS.md` restates it).
  Lessons: `promotion: declined (no new lesson — the chapter restates mechanisms the code and the gates already carry; that is its purpose)`.

- ID: `MODEL-BOOKS.8` — **annex: building the first CPU model, step by step**
  Status: `done` (`2026-09-29`, director request, out of order like `.7`)
  Goal: a teaching chapter in the PROJECT book (`docs/book/`) that walks the reader through
  creating `rv64i-lab-v0` end to end — from choosing the target to the honest gate
  verdict — every step cleanly explained: what you do, why that order, what actually went
  wrong, and the command that shows it. The dual mandate
  (`decision_dual-mandate-production-and-teaching`) applied to the WHOLE pipeline, where
  `.7` applied it to one tool: written so a reader could build their own model from it,
  not just agree with the result.
  Acceptance: `make book` renders it; every step names the real artifacts and a re-runnable
  command; the mistakes stay in (the matched profile that matched only an instruction set,
  the truncated trace that read as agreement, the dossier defect the spec inverted);
  prose dominates; numbers are re-derived or gated, never retyped where a gate can count.
  Placement decision: the project book's annex, beside `.7`'s — the per-unit book
  structure is `.1` (unbuilt); when it lands, the model book REFERENCES this chapter.
  Result: met, `2026-09-29`. Fourteen steps in the order the work actually happened —
  target, materials, dossier, requirements, state census, definition, generation,
  interpreter, guests, laboratory, references, comparison, detector, campaigns, gate —
  each with what you do, why that order, what went wrong for real, and a re-runnable
  command. The mistakes stay in (the advancing-`mtime` matched profile, the
  truncated-trace agreement, the inverted FENCE dossier defect, the gate-caught authoring
  constants). Every printed command was executed against the real repository before the
  chapter shipped: the scope census counts 52, the `zext-addi` demo catches the mutant
  (rc=1); two draft commands were caught wrong in review (a grep pattern matching
  nothing in `encoding.sexp`; a mutant name that does not exist) and corrected against
  the code. Book chapters 29 → 30 (re-derived by `DERIVED-COUNTS`; `LIVE_STATUS.md`
  restates it).
  Lessons: `promotion: declined (the chapter restates what the gates and the trees already carry; that is its purpose)`.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `MODEL-BOOKS.4` | `pending` | the references, their configuration, and what agreement is worth — the materials, gaps and method chapters are landed (`.1`–`.3`), and `.4`'s story is told through the matched-profile control |

(Leaves `.7` — the assembler annex — and `.8` — the step-by-step build walk — land out of
order on director requests; the per-unit book sequence above is unchanged.)

## Decisions

- `2026-09-14`: a unit's book lives at **`docs/models/<unit-id>/`**, beside the project book
  rather than inside `profiles/`. The path is keyed on the **unit**, not on `profiles/`, because a
  board or a device is a modelled unit and is not a processor profile — `profiles/` stays the home
  of processor profiles specifically. `profiles/<id>/` stays machine-readable data that gates consume;
  `docs/models/<id>/` is the narrative a human reads. Putting the book inside the profile directory
  would have mixed the two and pushed a prose tree under bounds calibrated for data files.
- `2026-09-14`: the book **generates or gates** every fact it restates from the profile. This tree
  exists because `MIRROR-DRIFT` had to be written four times over; a new prose surface that retypes
  digests and counts would be a fifth mirror, created deliberately after learning why not to.

## Open Questions

- ~~Does the specification's **PDF** rendering contain the instruction-format tables as
  text?~~ **ANSWERED `2026-09-29` (leaf `.2`): YES** — the pinned publication's own PDF at
  the same version segment carries the tables as selectable text (232 census-pattern lines
  vs 0 in the pinned HTML; `pdftotext` 4.06; the fetch and examination commands are in the
  leaf's checklist). Encodings CAN be re-sourced from the primary document; the two
  qualifications (the PDF's different chapter numbering; the layout-fragmented extraction)
  are recorded in the gaps chapter. The re-sourcing itself is future reviewed work, not
  done. What remains open from the original question is the *decision* whether to re-source
  (owner: `MODEL-METHOD.3`'s reconciliation lane, when scheduled).
- Should a DSP model book differ in structure? Deferred until `P3-BREADTH` selects a real DSP
  target; the structure here is built to be repeated, and a second model is what will test that.

## Blockers

- ✅ **Unblocked.** `P0-PROFILE.10` landed: the platform is now matched, four refuted claims are
  corrected at source, and the two irreducible reference differences are enumerated. The materials
  bill is now worth writing, and it has one more thing to say — that a "matched profile" is
  matched on its platform as well as its instruction set.

## Acceptance Checklist (leaf `MODEL-BOOKS.1`)

- [x] **REPRODUCE / ISSUE** — the gap the tree was created against: a materials list that
  lives only in the dossier is a list a reviewer will not read. Measured at landing:
  no `docs/models/` existed, and the unit registry's `book` field named a page that was
  never created:

  ```
  $ git ls-files docs/models | wc -l          # before this leaf
  0
  $ ls docs/book/src/profiles/                # the units.sexp book target
  ls: docs/book/src/profiles/: No such file or directory
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — WHY: the per-unit book had no structure (the leaf
  that owns it was unstarted) and the registry's `book` pointer was aspirational prose.
  WHERE: `materials/units.sexp`'s `book` field, and the absent `docs/models/` family.
  The pre-registration RED proved the gate reads the real corpus: fired before the data
  was repaired, it named exactly the stale registry row:

  ```
  $ bash scripts/check_materials_bill.sh        # before the units.sexp repair
  MATERIALS-BILL: a unit's materials bill does not hold.
    NO BOOK rv64i-lab-v0: docs/book/src/profiles/rv64i-lab-v0.md lacks book.toml/src/SUMMARY.md …
  ```

- [x] **FIX** — `docs/models/rv64i-lab-v0/` (the mdBook: skeleton, introduction with the
  five-part shape contract, the materials bill with 15 per-material sections, each with
  its does-not-supply statement); `scripts/gen_model_book.py` (the generator: four
  fragments from the pinned dossier, OWN-03 manifests, `--check` drift mode, refusals by
  name); `scripts/check_materials_bill.sh` (MATERIALS-BILL, doctrine #26 — DRIFT +
  COMPLETENESS, self-test 7/0, fired RED before registration); the registry repairs
  (`units.sexp`'s `book` corrected; `fact_ownership.tsv` +4 mirror rows;
  `readme_routes.tsv` +1 family row, `docs/models/` measured 8 files / 27,600 B); the
  stale `sources.toml`/`references.toml` in the leaf's Goal corrected to the `.sexp`
  reality with the note recorded in the design.

- [x] **ADDRESSED (verified)** —

  ```
  $ python3 scripts/gen_model_book.py
  gen_model_book: wrote 4 fragments under docs/models/rv64i-lab-v0/src/materials
  $ mdbook build docs/models/rv64i-lab-v0
  INFO HTML book written to `docs/models/rv64i-lab-v0/book`
  $ bash scripts/check_materials_bill.sh [--self-test]
  rv64i-lab-v0: 15 materials, every fragment matches the pinned data, every section
  carries its does-not-supply
  MATERIALS-BILL: ok (1 unit(s) — …)
  MATERIALS-BILL --self-test: 7 pass / 0 fail
  ```

- [x] **NO REGRESSION** — the guard set re-run, green; the two mirror caps re-based last
  leaf held (TOOLBOX.md 17,278 / 20,480; DOCTRINE_ENFORCEMENT.md 25,909 / 28,672); no
  Rust changed:

  ```
  $ make gate
  === all doctrines green ===          (26 project doctrines; DERIVED-COUNTS re-derives
                                        26 and 280 arms; README-ROUTING-CLOSURE: 32 destinations)
  $ make book
  INFO HTML book written to `docs/book/book`     (the project book still renders)
  ```

- [x] **LOCKSTEP** — same commit: `MEMORY.md` (overwritten; 3/8), `LIVE_STATUS.md`
  (MODEL-BOOKS 3/8; 26 doctrines / 280 arms; 32 destinations), `CHANGELOG.md`,
  `DEV_NOTES.md`, `docs/TASK_TREE.md` (frontier `.2`), this tree, the three doctrine
  mirrors, `doctrine/readme_routes.tsv`, `doctrine/fact_ownership.tsv`,
  `materials/units.sexp`.

## Acceptance Checklist (leaf `MODEL-BOOKS.2`)

- [x] **REPRODUCE / ISSUE** — the open question the tree carried: does the official
  specification's PDF rendering carry the instruction-format tables as selectable text?
  If yes, encodings can be re-sourced from the primary document and the encoding
  provenance's shared-ancestry exposure shrinks. Until measured, the materials bill could
  only name it as an open investigation.

- [x] **ROOT CAUSE (WHY + WHERE)** — WHY the question was open: the pinned artifacts are
  the HTML renderings, whose format diagrams are images — the encoding content was never
  in the pinned bytes, so nobody had read the PDF's text layer. WHERE the investigation
  had to start: which PDF. The pinned publication (docs.riscv.org, `v20260120`) publishes
  its PDF at the same version segment, linked from the pinned page itself:

  ```
  $ curl -s https://docs.riscv.org/reference/isa/v20260120/unpriv/rv64.html | grep -ioE 'href="[^"]*\.pdf[^"]*"'
  href="../_attachments/riscv-unprivileged.pdf"
  ```

- [x] **FIX** — the chapter `docs/models/rv64i-lab-v0/src/gaps.md` (in the book's
  SUMMARY.md; the bill's open-question sentence in `materials.md` now points at the
  answered finding); the investigation run and recorded with its commands (below). The
  PDF is cached untracked at `target/materials/` (on-volume, gitignored — the
  `target/sources/`/`target/refs/` standing) and deliberately NOT catalogued
  (`catalog.sexp`'s corpus model has no network-origin kind — a MODEL-METHOD decision,
  recorded in the chapter).

- [x] **ADDRESSED (verified)** — fetched and examined with a tool; the answer is YES:

  ```
  $ curl -sS -o target/materials/riscv-unprivileged-v20260120.pdf -w '%{http_code} %{size_download}\n' \
      https://docs.riscv.org/reference/isa/v20260120/_attachments/riscv-unprivileged.pdf
  200 4580174
  $ shasum -a 256 target/materials/riscv-unprivileged-v20260120.pdf
  06bb3c23074f72060a0ec061a80933af948cae7ceafdcd9d1fe177b05fd150bc
  $ file target/materials/riscv-unprivileged-v20260120.pdf
  PDF document, version 1.4, 696 pages
  $ grep -m1 'Official Release' target/materials/riscv-unprivileged-v20260120.txt
  Version 20260120: Official Release
  $ grep -cE '[01]{7}' target/sources/riscv-v20260120/{intro,rv32,rv64}.{html,txt}   # the pinned renderings
  …:0  (all six)
  $ pdftotext target/materials/riscv-unprivileged-v20260120.pdf target/materials/riscv-unprivileged-v20260120.txt
  $ grep -cE '[01]{7}' target/materials/riscv-unprivileged-v20260120.txt              # its PDF rendering
  232
  $ grep -cE '[01]{7}' <(pdftotext .materials/riscv/riscv-isa-manual-20260911.pdf -)  # corroboration
  269
  ```

- [x] **NO REGRESSION** — no gate surface changed (the chapter is authored prose; no
  generated content, so MATERIALS-BILL was not extended and the doctrine count stays 26):

  ```
  $ bash scripts/check_materials_bill.sh [--self-test]
  MATERIALS-BILL: ok (1 unit(s) — …) ; self-test 7 pass / 0 fail
  $ mdbook build docs/models/rv64i-lab-v0 && make book    # both render
  $ make gate
  === all doctrines green ===
  ```

- [x] **LOCKSTEP** — same commit: `MEMORY.md` (overwritten; 4/8), `LIVE_STATUS.md`
  (MODEL-BOOKS 4/8), `CHANGELOG.md`, `DEV_NOTES.md`, `docs/TASK_TREE.md` (frontier `.3`),
  this tree (the open question marked answered).

## Acceptance Checklist (leaf `MODEL-BOOKS.3`)

- [x] **REPRODUCE / ISSUE** — the tree's own gap statement: a methodology that lives only
  in the task-tree leaves is a methodology nobody can follow end to end. The chapter had
  to follow ONE rule from its sentence to its check with every hop inspectable.

- [x] **ROOT CAUSE (WHY + WHERE)** — the rule chosen is the reserved-FENCE rule: its
  chain is complete in tracked files (the sentence is in the pinned artifact; the
  decision, requirement, obligation, guest and suites are all tracked), and it carries
  DEFECT-A — the instructive correction. Every hop was verified to resolve BEFORE the
  chapter was written:

  ```
  $ grep -c '(id "D-FENCE")' profiles/rv64i-lab-v0/profile.sexp                      -> 1
  $ grep -c '"REQ-D-FENCE"' profiles/rv64i-lab-v0/requirements.sexp                  -> 1
  $ grep -c '"OB-FENCE"' profiles/rv64i-lab-v0/contract-obligations.sexp             -> 2
  $ grep -o 'CHK-FENCE-POS\|CHK-FENCE-NEG' …/contract-obligations.sexp               -> both
  $ ls …/guests/fault-fence.s …/guests/fault-fence.expected.sexp                     -> both exist
  $ grep -c fault_fence_retires_every_reserved_configuration_as_a_fence \
      crates/semulith-verify/src/run/tests.rs                                        -> 1
  $ grep -c '"fault-fence"' scripts/run_semulith_smoke.py                            -> 1
  $ grep -c 'never_written "x5"' …/fault-jal-mis.expected.sexp …/fault-jalr-mis…     -> 1, 1
  $ python3 scripts/check_citations.py   ->  52 of 52 instruction citations resolve
  ```

- [x] **FIX** — `docs/models/rv64i-lab-v0/src/methodology.md` (in the book's SUMMARY.md):
  the pipeline as six gated hops; the FENCE walk with real ids; the two judgement calls
  (semantic class, authority — each with its mechanical edge named); the mistakes
  (DEFECT-A, DEFECT-B, the two authoring REDs); the build-it-yourself checklist. The
  quoted decision fragments were checked programmatically as verbatim substrings of
  `D-FENCE`'s statement, and the chapter's census claim (28 requirements, four classes)
  was derived, not remembered.

- [x] **ADDRESSED (verified)** — both books render; the gates stay green:

  ```
  $ mdbook build docs/models/rv64i-lab-v0
  INFO HTML book written to `docs/models/rv64i-lab-v0/book`
  $ make book          # the project book renders
  $ bash scripts/check_materials_bill.sh [--self-test]   # ok; self-test 7/0
  $ make gate
  === all doctrines green ===          (26 — the gate surface unchanged)
  ```

- [x] **NO REGRESSION** — no generated content landed, so MATERIALS-BILL's surface is
  unchanged and no gate was extended; measured on the committed tree:

  ```
  $ git status --short -- scripts/ crates/ | wc -l     # no instrument or crate touched
  0
  $ bash scripts/check_materials_bill.sh
  MATERIALS-BILL: ok (1 unit(s) — generated tables match the pinned data; …)
  ```

  The only surfaces touched are the new chapter, the book's SUMMARY, the bill's one
  answered-question sentence, and the lockstep docs.

- [x] **LOCKSTEP** — same commit: `MEMORY.md` (overwritten; 5/8), `LIVE_STATUS.md`
  (MODEL-BOOKS 5/8), `CHANGELOG.md`, `DEV_NOTES.md`, `docs/TASK_TREE.md` (frontier `.4`),
  this tree.

## Acceptance Checklist (leaf `MODEL-BOOKS.8`)

- [x] **REPRODUCE / ISSUE** — the project book narrates the plan and the working practices;
  no chapter walks the actual creation of the first model end to end. The gap was measured
  when this tree was created ("a methodology that lives only in nine task-tree leaves is a
  methodology nobody can follow end to end"), and the director named it again today.
- [x] **ROOT CAUSE (WHY + WHERE)** — WHY: the build story exists, but scattered across
  thirteen task-tree leaves, the dossier, and the gates — each true, none readable as a
  route. WHERE, measured: the project book had no such chapter before this leaf, and has
  it now:

  ```
  $ git show HEAD:docs/book/src/SUMMARY.md | grep -c building-first-model || true
  0
  $ grep -c building-first-model docs/book/src/SUMMARY.md
  1
  ```
- [x] **FIX** — `docs/book/src/annex/building-first-model.md`: fourteen steps in the
  order the work happened, each what/why/wrong/command; placement beside `.7`'s annex per
  that leaf's placement precedent.
- [x] **ADDRESSED (verified)** — every command the chapter prints was run against the real
  repository:

  ```
  $ grep -oE '\((base|rv64)_[a-z_0-9]+ "[A-Z]+"\)' profiles/rv64i-lab-v0/profile.sexp | wc -l
  52
  $ cargo run -p semulith-cli -- demo --guest=smoke-arith --mutate=zext-addi
  verdict: EXPECTATIONS BROKEN — the detector's answer:
    FIRST DIVERGENCE at aligned step 2: … clean observes x3 = 0xffffffffffffffff, … (rc=1)
  $ make book   # renders, 30 chapters
  ```

  Two draft commands were caught wrong by this same discipline (a grep pattern matching
  nothing in `encoding.sexp`; a mutant name that does not exist) and corrected before
  commit.
- [x] **NO REGRESSION** — the guard set re-run, green:

  ```
  $ make gate
  === all doctrines green ===          (DERIVED-COUNTS re-derives the chapter count)
  $ make book
  INFO HTML book written to docs/book/book
  ```
- [x] **LOCKSTEP** — same commit: `MEMORY.md` (2/8), `LIVE_STATUS.md` (30 chapters;
  MODEL-BOOKS 2/8), `CHANGELOG.md`, `DEV_NOTES.md`, `docs/book/src/SUMMARY.md`, this
  tree.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-14` | `MODEL-BOOKS.1` | `pending` | `pending` |
| `2026-09-29` | `MODEL-BOOKS.7` | `make book`; `make gate` | renders; all doctrines green |
| `2026-09-29` | `MODEL-BOOKS.8` | the chapter's printed commands executed; `make book`; `make gate` | every command behaves as written (52-form census; the zext-addi mutant caught, rc=1); renders; all doctrines green |
| `2026-09-29` | `MODEL-BOOKS.1` | `scripts/check_materials_bill.sh` (pre-registration RED) | rc=1 — `NO BOOK rv64i-lab-v0` naming the stale `units.sexp` book path against the real corpus; then a DRIFT row when the generator's own edit invalidated its fingerprints; GREEN after the registry repair and regeneration |
| `2026-09-29` | `MODEL-BOOKS.1` | authoring RED moments (self-test) | the gate's first unit enumeration read top-level `(unit …)` forms as children of a nonexistent container ("registry empty" on a non-empty registry); the fixture's `cp -R` nested on re-run, making one arm fail for the wrong reason — both fixed, self-test 7/0 |
| `2026-09-29` | `MODEL-BOOKS.1` | `mdbook build docs/models/rv64i-lab-v0`; `make book`; `make gate` | the model book renders (15 materials, every section with its does-not-supply); the project book renders; 26 doctrines green (DERIVED-COUNTS re-derives 26 / 280 arms; README-ROUTING-CLOSURE 32 destinations) |
| `2026-09-29` | `MODEL-BOOKS.2` | the PDF investigation (fetch + `pdftotext`, exact commands in the leaf's checklist) | the pinned publication's PDF at the same version segment (`_attachments/riscv-unprivileged.pdf`, HTTP 200, 4,580,174 B, sha256 `06bb3c23…`, 696 pages, `Version 20260120: Official Release`) carries the format tables as selectable text — 232 `[01]{7}` census lines vs 0 on all six pinned HTML/TXT artifacts; the GitHub-release PDF corroborates (269). Answer recorded: YES, encodings can be re-sourced from the primary document (qualifications: different chapter numbering; layout-fragmented extraction); the re-sourcing itself is future reviewed work |
| `2026-09-29` | `MODEL-BOOKS.2` | `mdbook build docs/models/rv64i-lab-v0`; `make book`; `make gate`; `check_materials_bill.sh [--self-test]` | both books render; all doctrines green (26 — the gate surface unchanged); MATERIALS-BILL ok, self-test 7/0 |
| `2026-09-29` | `MODEL-BOOKS.3` | the id-resolution sweep (every id the chapter names grep-verified against the tracked corpus; the quoted decision fragments programmatically verified as verbatim; the requirement census derived) | every hop resolves: `D-FENCE` / `REQ-D-FENCE` / `OB-FENCE` / CHK-FENCE-POS+NEG / `fault-fence` + expectations / the offline suite / the smoke tuple / the DEFECT-B `never_written` pins; 28 requirements over four semantic classes; citations 52/52 |
| `2026-09-29` | `MODEL-BOOKS.3` | `mdbook build docs/models/rv64i-lab-v0`; `make book`; `make gate`; `check_materials_bill.sh [--self-test]` | both books render; all doctrines green (26); MATERIALS-BILL ok, self-test 7/0 |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `MODEL-BOOKS.1` | `SEMILITH-MB-0003 (leaf MODEL-BOOKS.1): …` | the per-unit book structure (`docs/models/<unit-id>/`) and the materials bill: 15 materials, tables generated from the pinned dossier by `gen_model_book.py`, every material's does-not-supply stated; MATERIALS-BILL the 26th doctrine (fired RED before registration); registry repairs (units.sexp's stale book path, fact_ownership +4, readme_routes +1 family) |
| `MODEL-BOOKS.2` | `SEMILITH-MB-0004 (leaf MODEL-BOOKS.2): …` | the gaps chapter, and the PDF investigation ANSWERED YES with a tool: the pinned publication's own PDF (same version segment, 20260120 Official Release) carries the format tables as selectable text (232 census lines vs 0 in the pinned HTML) — encodings can be re-sourced from the primary document; qualifications recorded (chapter numbering differs; extraction is layout-fragmented); re-sourcing is future reviewed work |
| `MODEL-BOOKS.3` | `SEMILITH-MB-0005 (leaf MODEL-BOOKS.3): …` | the methodology chapter: the reserved-FENCE rule followed end to end by name (sentence → D-FENCE → REQ-D-FENCE → OB-FENCE → fault-fence → the differentials), the authority/semantic-class judgement calls explained, the mistakes in (DEFECT-A inverted, DEFECT-B fixed in data, the two authoring REDs); every id grep-verified as written |
| `MODEL-BOOKS.7` | `SEMILITH-MB-0001 (leaf MODEL-BOOKS.7): …` | the assembler annex in the project book — director request, out of order; the per-unit sequence is unchanged |
| `MODEL-BOOKS.8` | `SEMILITH-MB-0002 (leaf MODEL-BOOKS.8): …` | the step-by-step build walk — director request, out of order like `.7`; chapters 29 → 30 |

## Changelog

- `2026-09-14`: Created. A model's materials and the methodology that turned them into a model had
  no reviewable home: the facts existed as 13 files of TOML/JSONL under `profiles/rv64i-lab-v0/`,
  and the single project book narrates the plan rather than any one model.
- `2026-09-29`: Leaf `.1` done: `docs/models/<unit-id>/` established as the per-unit mdBook
  (the shape contract: five parts, each owned by its leaf) and the complete materials bill
  landed — 15 materials, identity tables generated from the pinned dossier
  (`scripts/gen_model_book.py`), every material stating what it does NOT supply, gated by the
  26th doctrine `MATERIALS-BILL`. Registry repairs: `units.sexp`'s `book` field had named a
  project-book page that was never created — it now names `docs/models/rv64i-lab-v0/`.
- `2026-09-29`: Leaf `.2` done: the gaps chapter (`src/gaps.md`) — what the materials do not
  contain and what each gap forced — and the PDF investigation answered YES by measurement:
  the pinned publication's PDF rendering (same `v20260120` segment) carries the
  instruction-format tables as selectable text, so encodings can be re-sourced from the
  primary document. The qualifications (the PDF's different chapter numbering; the
  layout-fragmented extraction) and the reason the PDF is not catalogued yet are recorded
  in the chapter; the re-sourcing itself is future reviewed work.
- `2026-09-29`: Leaf `.3` done: the methodology chapter (`src/methodology.md`) — the
  reserved-FENCE rule followed end to end, by name, from the pinned sentence to the two
  differentials (six hops, all grep-verified); the authority vs semantic-class judgement
  calls explained with their mechanical edges; DEFECT-A (inverted), DEFECT-B (fixed in
  semantics data) and the two authoring REDs kept in as the teaching material.
- `2026-09-29`: Leaf `.7` done out of order (director request): the project book gains
  `annex/assembler.md` — how `scripts/riscv_asm.py` turns the pinned encoding tables into guest
  bytes, written to the tree's teaching mandate. Chapters 28 → 29.
- `2026-09-29`: Leaf `.8` done out of order (director request): the project book gains
  `annex/building-first-model.md` — the whole pipeline that built `rv64i-lab-v0`, fourteen
  steps, the mistakes kept in, every command executed before shipping. Chapters 29 → 30.
