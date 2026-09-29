# MODEL-BOOKS: one reviewable book per modelled unit — its materials, and its methodology

## Metadata

- Tree ID: `MODEL-BOOKS`
- Status: `done` (8/8 leaves complete `2026-09-29`; `.6` registered the `UNIT-BOOKS` gate
  and closed the tree)
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
  Status: `done` (`2026-09-29`)
  Goal: how each reference model was obtained, how it was configured to match the profile, what
  the matched-profile control demonstrated, and the independence inventory — in prose, including
  why three models is not three opinions.
  Acceptance: the configuration story is told through the control that changed the observation,
  not through a configuration file listing.
  Result: met, `2026-09-29`. **The references chapter landed
  (`docs/models/rv64i-lab-v0/src/references.md`), and the configuration story is told
  through the controls that CHANGED the observation, each with its recorded output.** The
  three controls, all measured: the ISA-string control (P0-PROFILE.5 — the override drives
  sail from its 96-extension default down to `rv64i_zvl32b`, read back with
  `--print-isa-string`; flipping `M` back on produced `DIFFERS … rv64im_zvl32b` against
  the pinned string — a one-letter drift caught), the platform correction
  (DIFF-PLATFORM-DEFAULT — the ISA string matched while the platform did not: the CLINT
  `mtime` probe at 0x0200_BFF8 advanced (2, then 3) under a plain `ld`; the override now
  disables clint/interrupts and declares the single MainMemory region; `guest-no-device`
  is the permanent negative fixture, its spike comparison disabled and printed), and ⭐
  the decisive control (P0-PROFILE.6 — the misaligned policy flipped back to "handled
  invisibly", same ELF, nothing else changed: `FIRST DIVERGENCE at aligned step 2 …
  sail-riscv writes=[(x1, 0)] … spike writes=[]` — one model loaded, the other trapped;
  "the two models agree BECAUSE the profile is matched" is a measurement, not a hope).
  The harness differences are told as the four recorded DIFFs (including
  DIFF-TRAP-RECORD-SHAPE — the comparator's false pass on a truncated trace, caught by
  running it) with the adapter's refusal discipline (it fired mid-run on
  `misaligned-store/amo`). The two reference-vs-reference differences the project measured
  (DIFF-FENCEI-EXECUTED — pinned as the `it-fencei` expected divergence;
  DIFF-TVAL-PHYS-MASK — sail's 56-bit tval mask, the wrap-sd guest kept below 2^56) teach
  the chapter's point: the references are also just implementations. The independence
  inventory is told per subsystem and pair — encoding not-shared (with the cut running
  the OTHER way than first assumed: our assembler shares riscv-opcodes ancestry with
  SPIKE, not sail), FP shared (184 of 199 files byte-identical), integer semantics
  no-evidence-of-sharing (deliberately not "not-shared"), expected-result derivation
  shared (ACT4 ↔ sail — one semantics answering twice), QEMU not-examined (recorded, not
  omitted) — ending in the per-leg verdict: encodings rest on sail alone, semantics on
  both references, nothing on ACT4 or QEMU. Every id, version and count named in the
  chapter was verified against the dossier and the trees as written (the sweep is the
  checklist's evidence). No gate extended — authored prose, no generated content (26
  doctrines, unchanged).
  Lessons: `promotion: declined (the chapter restates what the dossier records and the
  controls measured; that is its purpose)`.

- ID: `MODEL-BOOKS.5` — **the evidence, the gate, and the traceability walk**
  Status: `done` (`2026-09-29`)
  Goal: what has actually been demonstrated, the gate verdict and why it is `incomplete`, and a
  walk a reviewer can repeat: pick a rule, follow it to its requirement, its obligation, its
  declared checks and the experiment that touches it.
  Acceptance: the walk names real ids at every hop and ends at something re-runnable.
  Result: met, `2026-09-29`. **The evidence chapter landed
  (`docs/models/rv64i-lab-v0/src/evidence.md`), completing the five-part arc.** The
  evidence is reported per axis, each line with its instrument and its re-derivation
  command (SCP-05; "supports RV64I" appears nowhere): semantics 52/52 gated, boundaries
  exhausted, the failure layer three-way, the 21-cell matrix resolved, the live
  differential 40 guests / 492/492 aligned steps + the one declared expected divergence,
  restart as measured determinism, portability gated (wasm + the 44-arm browser bench),
  performance as one named host's recorded baseline with no thresholds, and the mutation
  suite as the detector's proof — all under the EVD-01 label (finite tested evidence,
  never proof). The gate verdicts are told honestly: G0 `incomplete` (72 declared checks,
  0 implemented — the generator has no code path to `passed`); G1 `incomplete` (criteria
  1–5 met; criterion 6, the C-toolchain guest, unmet — owner `P2-SCALAR.5`, and that leaf
  is BLOCKED: the ACT4 material absence and the C-guest routing question awaiting the
  director, both named). The capability limits are stated plainly (M-mode-only laboratory;
  no extensions — what no M/A/F/D means for real code; no devices/board/boot; a
  development profile, none accepted). The traceability walk is the EVIDENCE side, distinct
  from `.3`'s specification-side walk: `D-MISALIGN-DATA` → `REQ-D-MISALIGN-DATA`
  (implementation-defined, verbatim statement) → `OB-MISALIGN-DATA` (CHK-MISALIGN-DATA-POS
  AND -NEG; the authority/class contrast with `OB-MISALIGN-REPORT` made explicit) → the
  recorded experiment (`smoke-trap`: AGREE on the architectural DETAIL — cause 0x04, tval
  0x80000401 on both models — with its decisive control) → and it ENDS AT RE-RUNNABLE
  COMMANDS with their real current output: `cargo test -p semulith-verify --lib
  run::tests::smoke_trap` (1 passed) and `python3 scripts/run_semulith_smoke.py` (the
  smoke-trap PASS lines quoted verbatim from a fresh run, including the reproduce sha).
  Both gate reports regenerate byte-identical before the chapter shipped (no drift).
  Every id and number verified by tool as written. No gate extended — authored prose (26
  doctrines, unchanged).
  Lessons: `promotion: declined (the chapter restates what the reports and gates carry;
  that is its purpose)`.

- ID: `MODEL-BOOKS.6` — **wiring: every model has a book, and every book builds**
  Status: `done` (`2026-09-29`)
  Goal: `make book` builds the project book and every model book; the project book and `README.md`
  route to each; `doctrine/readme_routes.tsv` governs the new family; a gate requires a book per
  profile directory.
  Acceptance: adding a profile without a book fails the gate; `make book` builds all books.
  Result: met, `2026-09-29`. **The wiring landed, and the tree CLOSES.** `make book` now
  builds the project book AND every `docs/models/*/book.toml` (the Makefile's `book`
  target loops the family — two books today, both rendered). Routing: the project book
  gains the "The models" section (`models.md` — one definition, one book, naming the
  family and the gate) and README.md's Layout table gains the governed `docs/models/`
  row (69/85 lines, 3,947/4,864 B — inside both caps; the destination was already a
  governed family since `.1`). The 27th doctrine `UNIT-BOOKS`
  (`scripts/check_unit_books.sh`) enumerates the registered units from
  `materials/units.sexp` — the one registration place, never a second registry — and
  refuses by name: a unit whose book is absent (NO BOOK), a book missing its skeleton or
  failing to build (INCOMPLETE BOOK / BOOK DOES NOT BUILD), and a book under
  `docs/models/` no unit registers (ORPHAN BOOK — the reverse direction, so the family
  cannot accrete unregistered prose). Fired RED against the real corpus before
  registration (the book moved aside → `NO BOOK rv64i-lab-v0`, named; restored → GREEN);
  self-test 7/0; mirrored per the registry rules. One measured-in-flight fact corrected
  in the gate's header comment: mdbook TOLERATES a SUMMARY naming a missing chapter
  (renders a draft with a warning — the first self-test arm written for it did not fail),
  so the build arm's broken fixture is a malformed `book.toml`, which fails hard. With
  this leaf the tree's acceptance criteria all read met: (1) every registered unit has a
  book and UNIT-BOOKS says so (this leaf); (2) the materials list is complete, generated
  and gated (`.1`); (3) the methodology follows one rule end to end (`.3`); (4) `make
  book` builds every book and the project book routes (this leaf); (5) prose dominates
  (every chapter); (6) the teaching test — the chapters build from, with the mistakes in
  (every chapter); (7) the ability to run real compiled code is stated with its limits,
  derived from the extension set (`.5`'s capability limits: no M means runtime multiply
  calls, no A means no atomics, no F/D means a soft-float ABI). The tree closes at 8/8.
  The closure crossed the `docs/tasks/` per-part ceiling (MODEL-BOOKS.md reached 69,095 B
  of 65,536), so the `.1`–`.5` checklists moved VERBATIM to
  [`archive/MODEL-BOOKS.md`](archive/MODEL-BOOKS.md) — the ceiling was obeyed, not raised
  (the `P1-LAB`/`P2-SCALAR` precedent); the closing leaf's checklist stays live.
  Lessons: `promotion: declined (the mdbook draft-chapter tolerance is recorded in the
  gate's own header where it bites; a knowledge card would restate it)`.

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
| — | — | — | the tree is complete (8/8 leaves done): the per-unit book structure (`.1`), the gaps chapter with the PDF investigation (`.2`), the methodology (`.3`), the references (`.4`), the evidence and the walk (`.5`), the wiring and the `UNIT-BOOKS` gate (`.6`), and the two annexes (`.7`/`.8`) |

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

## Acceptance Checklists (leaves `MODEL-BOOKS.1`–`.5`)

Archived to [`archive/MODEL-BOOKS.md`](archive/MODEL-BOOKS.md) (per-part ceiling) —
the closing leaf's checklist (`.6`) stays live, below.

## Acceptance Checklist (leaf `MODEL-BOOKS.6`)

- [x] **REPRODUCE / ISSUE** — the arc's chapters existed (`.1`–`.5`) but the structure was
  a habit, not a rule: `make book` built only the project book, nothing routed a reader
  from the project book or README to the model book, and no gate connected the unit
  registry to the book family. Measured:

  ```
  $ git show HEAD~1:Makefile | grep -A1 '^book:'      # before this leaf
  book:
  	mdbook build docs/book
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — WHY: the one-definition-one-book decision was prose
  until this leaf; WHERE: the Makefile's `book` target, the README Layout table, the
  project book's SUMMARY, and the doctrine registry — measured at the pre-leaf state:

  ```
  $ git show HEAD:Makefile | grep -c "docs/models"              -> 0
  $ git show HEAD:scripts/check_doctrines.project.sh | grep -c "units.sexp"   -> 0
  ```

  (no build wired the family, and no gate enumerated the registry's `book` field).

- [x] **FIX** — the Makefile loop over `docs/models/*/book.toml`; the README Layout row
  for the governed `docs/models/` family (fits both caps: 69/85 lines, 3,947/4,864 B);
  the project book's "The models" section (`docs/book/src/models.md` + SUMMARY); the 27th
  doctrine `UNIT-BOOKS` (`scripts/check_unit_books.sh` — NO BOOK / INCOMPLETE BOOK /
  BOOK DOES NOT BUILD / ORPHAN BOOK, all named; enumerates the one registry). Fired RED
  against the real corpus before registration:

  ```
  $ mv docs/models/rv64i-lab-v0 /tmp/… && bash scripts/check_unit_books.sh   # pre-registration
  UNIT-BOOKS: a registered unit lacks its book, or a book lacks its unit.
    NO BOOK rv64i-lab-v0: the registry names 'docs/models/rv64i-lab-v0', which does not exist — …
  $ (restored) bash scripts/check_unit_books.sh
  UNIT-BOOKS: ok (1 unit(s) — every registered unit has its book, and every book builds)
  ```

  One measured correction in flight: mdbook tolerates a SUMMARY naming a missing chapter
  (renders a draft with a warning — the self-test arm written for it did NOT fail), so the
  build arm's broken fixture is a malformed `book.toml`; the gate's header records this.

- [x] **ADDRESSED (verified)** —

  ```
  $ make book 2>&1 | grep -c "HTML book written"   # both books, one command
  2
  $ bash scripts/check_unit_books.sh [--self-test]
  UNIT-BOOKS: ok (1 unit(s) — …) ; UNIT-BOOKS --self-test: 7 pass / 0 fail
  $ bash scripts/check_materials_bill.sh [--self-test]   # ok; 7/0 (unchanged surface)
  $ make gate
  === all doctrines green ===          (27 doctrines; DERIVED-COUNTS re-derives 27 / 287;
                                        the project book is 31 chapters)
  ```

- [x] **NO REGRESSION** — the guard set re-run, green; both books render; the mirror caps
  hold (TOOLBOX.md / DOCTRINE_ENFORCEMENT.md under 20/28 KiB); the tree's acceptance
  criteria re-read and all seven now met (the mapping is in the leaf's Result). Measured:

  ```
  $ bash scripts/check_unit_books.sh
  UNIT-BOOKS: ok (1 unit(s) — every registered unit has its book, and every book builds)
  $ bash scripts/check_materials_bill.sh
  MATERIALS-BILL: ok (1 unit(s) — …)
  ```

- [x] **LOCKSTEP** — same commit: `MEMORY.md` (overwritten; tree closed, out of the active
  list), `LIVE_STATUS.md` (MODEL-BOOKS done 8/8; 27 doctrines / 287 arms; 31 chapters),
  `CHANGELOG.md`, `DEV_NOTES.md`, `docs/TASK_TREE.md` (the tree's row → done), this tree
  (status done; frontier "—").

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
| `2026-09-29` | `MODEL-BOOKS.4` | the id/version/count sweep (every claim the chapter makes verified against the dossier, the override and the trees — the ROOT CAUSE box carries it) | all resolve: the four candidates and their identities, the override's platform shape, the eight DIFFs, the six independence records, the control quotes (archive + dossier), the adapter spellings, the expected-divergence guest, the negative fixture's disabled comparison |
| `2026-09-29` | `MODEL-BOOKS.4` | `mdbook build docs/models/rv64i-lab-v0`; `make book`; `make gate`; `check_materials_bill.sh [--self-test]` | both books render; all doctrines green (26); MATERIALS-BILL ok, self-test 7/0 |
| `2026-09-29` | `MODEL-BOOKS.5` | both gate reports regenerated before writing | byte-identical — no drift (git status clean after regeneration) |
| `2026-09-29` | `MODEL-BOOKS.5` | the walk's terminal commands run fresh | `cargo test -p semulith-verify --lib run::tests::smoke_trap` → 1 passed / 165 filtered out; `run_semulith_smoke.py` → the smoke-trap PASS lines quoted in the chapter verbatim (reproduce sha c9d7a11ce4b7bffe…) |
| `2026-09-29` | `MODEL-BOOKS.5` | `mdbook build docs/models/rv64i-lab-v0`; `make book`; `make gate`; `check_materials_bill.sh [--self-test]`; the per-axis numbers re-derived from live gates | both books render; all doctrines green (26); MATERIALS-BILL ok, self-test 7/0; 52/52 (EXERCISE-COVERAGE), 21 cells (INTERACTION-MATRIX), 492/492 (G1-REPORT) all confirmed live |
| `2026-09-29` | `MODEL-BOOKS.6` | `scripts/check_unit_books.sh` (pre-registration RED) | rc=1 — `NO BOOK rv64i-lab-v0` named against the real corpus (the book moved aside); GREEN after restore |
| `2026-09-29` | `MODEL-BOOKS.6` | authoring RED moment (self-test) | mdbook tolerates a SUMMARY naming a missing chapter (a draft + a warning) — the first build-failure arm did not fail; the broken fixture became a malformed `book.toml`, which fails hard; recorded in the gate's header |
| `2026-09-29` | `MODEL-BOOKS.6` | `make book` (2 books, one command); `make gate`; `check_unit_books.sh [--self-test]`; `check_materials_bill.sh [--self-test]` | both books build; 27 doctrines green (DERIVED-COUNTS re-derives 27 / 287 / 31 chapters); UNIT-BOOKS ok, self-test 7/0; MATERIALS-BILL ok, self-test 7/0 |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `MODEL-BOOKS.1` | `SEMILITH-MB-0003 (leaf MODEL-BOOKS.1): …` | the per-unit book structure (`docs/models/<unit-id>/`) and the materials bill: 15 materials, tables generated from the pinned dossier by `gen_model_book.py`, every material's does-not-supply stated; MATERIALS-BILL the 26th doctrine (fired RED before registration); registry repairs (units.sexp's stale book path, fact_ownership +4, readme_routes +1 family) |
| `MODEL-BOOKS.2` | `SEMILITH-MB-0004 (leaf MODEL-BOOKS.2): …` | the gaps chapter, and the PDF investigation ANSWERED YES with a tool: the pinned publication's own PDF (same version segment, 20260120 Official Release) carries the format tables as selectable text (232 census lines vs 0 in the pinned HTML) — encodings can be re-sourced from the primary document; qualifications recorded (chapter numbering differs; extraction is layout-fragmented); re-sourcing is future reviewed work |
| `MODEL-BOOKS.3` | `SEMILITH-MB-0005 (leaf MODEL-BOOKS.3): …` | the methodology chapter: the reserved-FENCE rule followed end to end by name (sentence → D-FENCE → REQ-D-FENCE → OB-FENCE → fault-fence → the differentials), the authority/semantic-class judgement calls explained, the mistakes in (DEFECT-A inverted, DEFECT-B fixed in data, the two authoring REDs); every id grep-verified as written |
| `MODEL-BOOKS.4` | `SEMILITH-MB-0006 (leaf MODEL-BOOKS.4): …` | the references chapter: the configuration story told through the controls that changed the observation (the ISA-string read-back, the platform correction after the advancing-mtime probe, the decisive misaligned-policy flip), the harness DIFFs, the two measured reference-vs-reference differences, and the independence inventory ending in the per-leg verdict — why three models is not three opinions |
| `MODEL-BOOKS.5` | `SEMILITH-MB-0007 (leaf MODEL-BOOKS.5): …` | the evidence chapter completes the five-part arc: the per-axis ledger with its instruments, both `incomplete` verdicts with their reasons (G0's 72/0; G1's criterion 6 and P2-SCALAR.5's blockers), the capability limits, and the evidence-side traceability walk (`D-MISALIGN-DATA`) ending at two re-runnable commands with fresh output quoted |
| `MODEL-BOOKS.6` | `SEMILITH-MB-0008 (leaf MODEL-BOOKS.6): …` | the wiring, and the TREE CLOSES (8/8): `make book` builds every book, the project book and README route to the model books, and `UNIT-BOOKS` (27th doctrine) requires every registered unit to have a book that builds — fired RED before registration; all seven tree acceptance criteria met |
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
- `2026-09-29`: Leaf `.4` done: the references chapter (`src/references.md`) — how each
  reference was obtained and matched to the profile, told through the controls that changed
  the observation (the ISA-string read-back, the platform correction after the
  advancing-`mtime` probe, the decisive misaligned-policy flip); the harness differences;
  the two measured reference-vs-reference differences; and the independence inventory —
  encodings rest on sail alone, semantics on both references, nothing on ACT4 or QEMU.
- `2026-09-29`: Leaf `.5` done: the evidence chapter (`src/evidence.md`) completes the
  five-part arc — the per-axis evidence ledger (52/52 gated, 21 cells, 40 guests /
  492/492 steps + the declared divergence, determinism, portability, the baseline, the
  detector), both `incomplete` verdicts with their reasons (G0's 72/0; G1's criterion 6 and
  `P2-SCALAR.5`'s named blockers), the capability limits, and the `D-MISALIGN-DATA`
  traceability walk ending at two re-runnable commands with fresh output quoted.
- `2026-09-29`: Leaf `.6` done, and **the tree closes** (8/8): `make book` builds the
  project book and every model book; the project book ("The models" section) and README's
  Layout table route to `docs/models/`; the 27th doctrine `UNIT-BOOKS` enumerates
  `materials/units.sexp` and refuses a unit without a book, a book that does not build, or
  an unregistered book — fired RED against the real corpus before registration. All seven
  tree acceptance criteria are met (the mapping is in `.6`'s Result).
- `2026-09-29`: Leaf `.7` done out of order (director request): the project book gains
  `annex/assembler.md` — how `scripts/riscv_asm.py` turns the pinned encoding tables into guest
  bytes, written to the tree's teaching mandate. Chapters 28 → 29.
- `2026-09-29`: Leaf `.8` done out of order (director request): the project book gains
  `annex/building-first-model.md` — the whole pipeline that built `rv64i-lab-v0`, fourteen
  steps, the mistakes kept in, every command executed before shipping. Chapters 29 → 30.
