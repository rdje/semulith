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
  Status: `pending`
  Goal: the chapter a specification bill usually omits. This project measured that its pinned
  artifacts contain **no instruction encodings** (the format diagrams are images), which forced a
  second provenance whose ancestry is shared with one comparator and not the other.
  ⭐ Includes a real investigation: the official specification is also published as **PDF**, and
  whether *that* rendering carries the instruction-format tables as selectable text is unknown. If
  it does, encodings can be re-sourced from the primary document and the shared-ancestry problem
  shrinks. If it does not, the finding is stronger and is recorded as such.
  Acceptance: the PDF is fetched and examined with a tool, not assumed; the outcome is recorded
  either way with the command that established it.

- ID: `MODEL-BOOKS.3` — **the methodology: from document to model**
  Status: `pending`
  Goal: the prose chapter that explains the pipeline — how a sentence of specification becomes a
  decision with an *authority*, how a decision becomes a requirement record with a *semantic
  class*, how a requirement becomes an obligation with positive **and negative** checks, and how an
  expected value is *derived* rather than copied.
  Acceptance: one rule is followed end to end, by name, from its sentence to its check; the
  chapter explains the judgement calls (authority vs semantic class) that are not mechanical.

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
| 1 | `MODEL-BOOKS.2` | `pending` | the honest counterpart to the bill, and it carries a real investigation that may change where encodings come from (the structure and the bill landed at `.1` — 15 materials, generated and gated) |
| 2 | `MODEL-BOOKS.3` | `pending` | the methodology, once the materials it operates on are documented |

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

- Does the specification's **PDF** rendering contain the instruction-format tables as text? Owner:
  `MODEL-BOOKS.2`. It decides whether encodings can be re-sourced from the primary document, which
  would materially improve the independence position recorded in `references.toml`.
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

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `MODEL-BOOKS.1` | `SEMILITH-MB-0003 (leaf MODEL-BOOKS.1): …` | the per-unit book structure (`docs/models/<unit-id>/`) and the materials bill: 15 materials, tables generated from the pinned dossier by `gen_model_book.py`, every material's does-not-supply stated; MATERIALS-BILL the 26th doctrine (fired RED before registration); registry repairs (units.sexp's stale book path, fact_ownership +4, readme_routes +1 family) |
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
- `2026-09-29`: Leaf `.7` done out of order (director request): the project book gains
  `annex/assembler.md` — how `scripts/riscv_asm.py` turns the pinned encoding tables into guest
  bytes, written to the tree's teaching mandate. Chapters 28 → 29.
- `2026-09-29`: Leaf `.8` done out of order (director request): the project book gains
  `annex/building-first-model.md` — the whole pipeline that built `rv64i-lab-v0`, fourteen
  steps, the mistakes kept in, every command executed before shipping. Chapters 29 → 30.
