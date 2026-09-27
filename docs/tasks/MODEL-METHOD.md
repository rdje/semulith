# MODEL-METHOD: the method for modelling a unit, and the materials that method requires

## Metadata

- Tree ID: `MODEL-METHOD`
- Status: `active`
- Roadmap lane: cross-cutting; precedes implementation for **every** modelled unit — CPU, MCU, DSP, device, board, SoC
- Gate: contributes the precondition `P1-LAB` must satisfy before any model code is written
- Depends on: `P0-PROFILE` (the first model), `docs/INFORMATION_CATALOG.md` (the 24 categories)
- Unlocks: `MODEL-BOOKS` (which renders this), and a defensible start to `P1-LAB`
- Created: `2026-09-14`
- Owner: repo-local workflow

## Goal

Make two things explicit that the project has so far done implicitly and therefore unevenly:

1. **The method.** How a pile of specification documents becomes a model — document, decision,
   requirement, obligation, check — with the judgement calls named rather than absorbed.
2. **The materials the method requires.** `docs/INFORMATION_CATALOG.md` already states *what you
   must know* to model a processor, in 24 categories. Nothing states **which document supplies
   each category**, and nothing says which categories are supplied by **nothing at all**. That
   second list is the important one: it is the set of things the project would otherwise invent.

Both are captured **machine-readably**, so coverage is a query rather than a reading, and
implementation cannot begin over an uncovered category without a gate saying so.

## Non-Goals

- Not a rewrite of `docs/INFORMATION_CATALOG.md`. That file is the delivered taxonomy of *what
  must be known*; this tree adds the *material that supplies it* and the *coverage census*.
- Not model code. Explicitly the opposite: this tree exists so that code starts from sources
  rather than from recall.
- Not an acquisition of every conceivable document. A category irrelevant to a declared scope is
  marked `not-applicable` **with its reason**, which is a different statement from `missing`.

## The layer boundary — what a CPU/DSP model is NOT

⛔ **Devices are not CPU material.** A UART, an interrupt controller, an interruptor, a DMA engine
or an interconnect belongs to a **board / SoC / ASIC** model, not to a processor model. This
project pipecleans by modelling **CPUs and DSPs first**, and the processor layer ends at the
CPU/environment boundary: the CPU states what it *assumes* of its environment, and a later board
model states what it *guarantees*.

The project's own contracts already own this line and are cited rather than restated:
`docs/INFORMATION_CATALOG.md` says plainly that *"C19–C21 are not all properties of the CPU
itself"*, and `docs/CPU_ENVIRONMENT.md` §5 defines the board composition gate — *for every CPU
assumption, identify the board/device guarantee satisfying it*. `P5-BOARD` is the tree that owns
the other side.

⭐ **The layer names the OWNER, not merely a deferral.** `C19 Platform, devices and interconnect`
is `deferred-to-board` for a CPU and `covered` for a board — the same category in the same
catalogue, answered by a different unit. That is why the catalogue is keyed on a **unit** rather
than on a processor profile: a board's census and a CPU's census are the same schema answered
differently, which is what makes adding the second unit cheap.

**And it is why the boundary is stated before the schema is written.** A category the processor layer does not own is **not `missing`**. Marking
`C19 Platform, devices and interconnect` as `missing` for a CPU model would manufacture an
acquisition task for material the model must never contain, and would make the census read as a
deficiency when it is a correct scope. The disposition vocabulary therefore carries a **layer**,
and `deferred-to-board` is a first-class answer distinct from both `missing` and `not-applicable`.

⚠️ It also corrects a framing in the previous leaf. "Capable of running real code" needs a console
and a program-exit convention — and **those are board concerns**. What the *processor* layer owes
real code is narrower and entirely within it: the psABI, the ELF contract, the entry/startup state,
and the compiler-runtime intrinsics a no-`M` soft-float target calls. The exit convention is an
assumption the CPU records and a board later satisfies.

## Acceptance Criteria

1. Every catalogue category has, per model, exactly one disposition: `covered` (naming the
   material and its locator), `missing` (naming what would close it), `deferred-to-board` (owned by
   a later board/SoC model, with the assumption the CPU records in its place), or
   `not-applicable` (with the reason). No category may be silently absent.
   ⛔ `deferred-to-board` and `missing` must never be conflated: one is a correct scope, the other
   is an acquisition task, and a census that merges them reports a healthy model as deficient.
2. The catalogue is machine-readable, schema-validated, and gated — a coverage claim is a query,
   not a sentence someone wrote.
3. The method is documented in prose, following at least one real rule end to end.
4. A gate prevents implementation beginning while a category the declared scope *needs* is
   `missing` — the director's rule, mechanized: no coding without the source of truth.
5. ⭐ **The catalogue covers what running REAL COMPILED CODE requires**, not only what executing
   instructions requires. `decision_dual-mandate-production-and-teaching` makes "capable of running
   real code (C, Rust)" a stated target, and that pulls in materials the ISA chapters do not own:
   the psABI, the ELF specification, a startup and runtime contract, the compiler-runtime
   intrinsics a no-`M` soft-float target will call, and a program-exit convention. Catalogue
   category `C20` is where they land, and it is currently supplied by nothing.

   Census behind that last clause, over every population that could refute it — the pinned
   specification artifacts, and any pinned material naming an ABI or ELF source:

   ```
   $ grep -oE '^id = "[^"]+"' profiles/rv64i-lab-v0/sources.toml
   RVI-INTRO   RVI-RV32I   RVI-RV64I          # three unprivileged ISA chapters, nothing else
   $ git grep -clE 'psABI|calling.convention|elf.specification' -- profiles/*/sources.toml profiles/*/references.toml | wc -l
   0
   $ grep -c 'software-convention' profiles/rv64i-lab-v0/state.json
   3                                          # the ISA chapters DISCLAIM the ABI; state.json says so
   ```

   The third number is the interesting one: the profile already records three register roles as
   `software-convention` precisely because the ISA chapter does not own them. Nothing yet pins the
   document that does.
6. Every material record states **what it teaches**, not only what it specifies — the catalogue is
   an input to a teaching text, and a material nobody can learn from is a citation.

## ⚡ The S-expression trigger has FIRED — see `decision_canonical-definition-input`

The trigger written below — *"the first time a material must carry a nested semantic expression
rather than a citation"* — fired on `2026-09-14`, when the canonical definition had to become the
input a generator engine reads. The answer: **a set of format-fit files**, with S-expressions for
`encoding.sexp` and `semantics.sexp` and the record files unchanged. The reasoning below stands
for the *materials catalogue*, which is still records; it is the semantics that needed trees.

## Format decision for the materials catalogue — and why not S-expressions there

**The catalogue is JSON Lines against a JSON Schema.** The call was mine and the reasoning is
recorded so it can be overturned on evidence rather than taste:

- This repository already carries a **tracked, gated, self-refusing** JSON Schema validator
  (`scripts/validate_records.py`) and a doctrine (`RECORD-SCHEMA`) that validates every `.jsonl`
  and cross-checks it against its profile. A materials catalogue in JSONL inherits both on day one.
- The data is **flat and heterogeneous** — a category, a disposition, a locator, a digest. That is
  a record, not a tree. S-expressions buy nothing over JSON for records, and cost a parser, a
  schema mechanism and a fourth tracked format.
- ⭐ **Where S-expressions WOULD earn their place is the canonical executable semantics** — the
  *executable definition* of `docs/ARCHITECTURE.md` §4, where an instruction's meaning is a nested
  expression and pattern-matching over it is the whole job. That is exactly why Sail, ACL2 and the
  ISA-formalism tradition use them, and it is a `P1-LAB` decision, not a `P0` one.
- **Trigger to revisit:** the first time a material must carry a *nested semantic expression*
  rather than a citation, this decision is re-opened in `P1-LAB` with that material as the
  worked example.

## Task Tree

- ID: `MODEL-METHOD.1` — **answer the narrower-instrument sweep, and make the answer an instrument**
  Status: `done`
  Goal: the open question left by `P0-PROFILE.10` — *which other "matched" claims rest on an
  instrument answering a narrower question?* Enumerate every pinned scalar that stands for a
  configuration, check each, and replace the pattern with a principle: a match is claimed against
  the **model's own self-description at the widest granularity it offers**, compared field by
  field. Both references emit a device tree; that is the wide instrument.
  Acceptance: every pinned scalar declares what it does **not** establish; the platform comparison
  is a tracked command, not a paragraph; any further instance found is fixed or enumerated.
  Verification: one further instance found and fixed (Spike's ISA was an input, not a read-back); 4 of 4 platform fields shown to disagree; rule 5b added and fired RED.
  Commit: `SEMULITH-MM-0033`

- ID: `MODEL-METHOD.2` — **the materials requirement: schema and catalogue**
  Status: `done`
  Goal: a record type binding each `docs/INFORMATION_CATALOG.md` category to the material kind
  that supplies it, with a **layer** (`processor` / `board` / `system`) and a disposition per
  **modelled unit**, plus the small registry of units themselves (id, kind, layer, book). The
  DSP-specific questions of §5 are carried as their own categories rather than folded into the CPU
  ones. ⛔ Start small: one unit exists, the registry has one row, and nothing is pre-built for
  kinds that have never been exercised.
  Acceptance: schema added; every category represented with an explicit layer; a `board`-layer
  category may not be dispositioned `missing` for a processor model; validates under
  `RECORD-SCHEMA`.

  Result: met, `2026-09-27`. `schema/units.sexp` + `schema/category-needs.sexp` declare the
  two families (zero kernel lines); `records_sexp.py` owns both mappings; `materials/units.sexp`
  carries the one-row registry (rv64i-lab-v0, processor); `materials/category-needs.sexp`
  carries all 24 INFORMATION_CATALOG categories with explicit layers — C01–C06, C22, C23
  covered; C07/C08/C12/C15/C16/C18 missing WITH reasons (excluded subsystems, owed and
  absent); C09, C13, C14, C24 partial; C17, C19, C20, C21 out-of-scope (board-layer, never
  owed by a processor). RECORD-SCHEMA rules 10–11 enforce the registry-nonempty and the layer
  honesty — the acceptance's `board × missing × processor` shape refuses as LAYER LIE (6 new
  arms, 32 total; 7 record files green). `.3`'s census now revises dispositions against
  evidence instead of inventing the record type.
  Design (recorded before code, `2026-09-27`), the catalog and the records machinery read first:
  - **Two record families on the records track, named so the basenames cannot collide with the
    profile's** — `materials/units.sexp` (the registry: `(unit (id …) (kind processor) (layer …)
    (book …))`, one row today) and `materials/category-needs.sexp` (one `(category-need …)` per
    INFORMATION_CATALOG category: category id, layer, the material kind that supplies it, the
    unit, the disposition, an optional reason). `schema/units.sexp` + `schema/category-needs.sexp`
    declare both; `records_sexp.py` owns both mappings; RECORD-SCHEMA gains both basenames and
    the layer-rule arm. The house path from `.3` (SOT-FORMAT.3), walked again.
  - **The disposition vocabulary is honest about the difference between absent and never-needed**:
    `covered` / `partial` / `missing` / `out-of-scope`. `missing` means the unit requires the
    category and the catalogue lacks the material — the acceptance's rule is the mechanical form:
    a board-layer category dispositioned `missing` for a processor unit is a lie about what was
    required (a processor never owed board-layer information), so the gate refuses it and names
    the category; the honest word is `out-of-scope`. Processor-layer exclusions this profile
    carries (privilege, translation, floating point, vectors, atomics) stay `missing` WITH a
    reason — they were owed and are absent — which is `.3`'s census to deepen with evidence.
  - **Layer assignment, stated**: processor — C01–C09, C10, C11, C13, C14, C15, C22, C23, C24;
    board — C17 (reset/time spans into the environment, per the catalog's own note), C19, C20,
    C21 ("not all properties of the CPU itself", per §3); system — C12 (translation spans into
    the OS), C16 (multicore), C18 (implementation observation). The first honest pass at
    `rv64i-lab-v0`'s 24 rows: covered where the profile genuinely owns the fact (C01–C06, C22,
    C23), missing-with-reason for the excluded processor-layer subsystems (C07 FP, C08 V, C12,
    C15, C16), out-of-scope for board-layer rows (C17, C19–C21), partial where the profile owns
    the shape but not the depth (C13 code visibility, C14 ECALL/EBREAK only, C24 replay policy
    declared not built, C09/C10/C11). `.3` revises every disposition it can evidence better.

- ID: `MODEL-METHOD.3` — **the coverage census for `rv64i-lab-v0`**
  Status: `pending`
  Goal: fill the catalogue for the first model honestly. Expected outcome is that a **minority**
  of categories are covered — the profile excludes privilege, translation, floating point, vectors
  and atomics — and the value is in the `missing` rows, not the `covered` ones. ⛔ Device and
  interconnect categories are **`deferred-to-board`**, not missing: they are `P5-BOARD`'s to own,
  and the CPU records an assumption in their place.
  Acceptance: no category absent; each `missing` row names what would close it.

- ID: `MODEL-METHOD.4` — **acquire what the census says is missing and reachable**
  Status: `pending`
  Goal: obtain and pin the materials the census identifies as needed for the *declared* scope, and
  record as `SRC-02` results those that cannot be obtained. ⭐ Includes the **run-real-code** set,
  which the ISA chapters do not own: the RISC-V psABI, the ELF specification, a startup/runtime
  contract, the compiler-runtime intrinsics a no-`M` soft-float target calls, and a program-exit
  convention. ⚠️ This is what makes `state.json`'s `software-convention` register roles
  load-bearing: once real code runs, the calling convention stops being background reading. ⭐ Includes the outstanding question
  from `MODEL-BOOKS.2`: does the specification's **PDF** rendering carry the instruction-format
  tables as selectable text? If so, encodings can be re-sourced from the primary document and the
  shared-ancestry position improves.
  Acceptance: every acquisition pinned with a digest and re-derivable; every failure recorded with
  its attempt.

- ID: `MODEL-METHOD.5` — **the method, in prose, written to be learned from**
  Status: `pending`
  Goal: document → decision → requirement → obligation → check, with the judgement calls named:
  authority versus semantic class, what makes an expected value *derived* rather than copied, and
  when a disagreement is a profile difference rather than a defect. ⭐ Written so a student could
  apply it to a processor this project has never modelled — which means the **order** of the steps
  is justified, not merely listed, and the rejected alternatives are kept.
  Acceptance: one rule followed end to end by name; the non-mechanical steps identified as such;
  a reader could carry the method to a different ISA without this project's documents.

- ID: `MODEL-METHOD.7` — **the canonical definition: what it is and what each file owns**
  Status: `done`
  Goal: document the definition as a set of format-fit files with a **no-duplicated-fact** rule —
  which file owns configuration, state, encodings, semantics, requirements, obligations and
  provenance — and gate that rule, since "single source of truth" means *one owner per fact*
  rather than *one file*.
  Acceptance: every fact kind has exactly one owning file; a gate refuses a fact stated in two.

  Result: met, `2026-09-27`. `doctrine/fact_ownership.tsv` names the one owning file per fact
  kind (8 kinds), the legal derived mirrors, and the governing doctrine; `FACT-OWNERSHIP`
  (18th doctrine, `scripts/check_fact_ownership.sh`, 8 arms) verifies one owner each, owners
  exist, every mirror names a REGISTERED governor, and the corpus's four restatement pairs are
  all named. The inventory found one mirror with NO governor — 28 obligations restate their
  requirement's statement, all matching today but free to drift — so RECORD-SCHEMA gained rule
  9 (MIRROR: an obligation naming its `requirement_id` must state exactly what that requirement
  states, 3 new arms, 26 total). The acceptance's shape — a fact stated in two, refused — is
  the gate's UNGOVERNED MIRROR and UNREGISTERED MIRROR PAIR arms, both fired.
  Design (recorded before code, `2026-09-27`), the corpus's mirrors inventoried first:
  - ⭐ **The corpus already lives on derived mirrors — the rule must govern them, not pretend
    they don't exist.** Measured inventory: decisions↔requirements state the same fact in two
    files, governed by RECORD-SCHEMA rule 4 (statement identity); state↔profile, governed by
    PROFILE-CONSISTENCY rule 4 (agreement); the encoding composition↔its fragments, governed
    by UNIT-COMPOSITION (resolve + decide). ⛔ And one mirror with NO governor, measured:
    28 obligations carry a `requirement_id` and restate that requirement's statement — all
    matching today, but nothing REFUSES the day one drifts. That is the leaf's concrete fix:
    the governor gets built, then the registry names it.
  - **The ownership registry is data, beside the routes registry it mirrors in shape** —
    `doctrine/fact_ownership.tsv`: fact kind · the ONE owning file · its legal mirrors · the
    doctrine governing each mirror pair. The gate (`FACT-OWNERSHIP`, 18th doctrine) verifies:
    every owner exists; every fact kind has exactly one owner; every mirror names a governor;
    every governor is a REGISTERED doctrine that actually runs; and the corpus's enumerated
    mirror pairs are all named in the registry — a duplication the registry does not know
    about is the refusal. "One owner per fact; every mirror governed; nothing stated in two
    ungoverned."
  - **The new governor arm** (RECORD-SCHEMA): an obligation carrying
    `parameters.requirement_id` must state EXACTLY what that requirement states — refused by
    name with both statements' file and id. The 8 environment-assumptions keep their own
    statements (they assume, they do not mirror); the arm keys on the parameter, not the
    direction.

- ID: `MODEL-METHOD.8` — **own the encodings: `encoding.sexp`**
  Status: `done`
  Goal: close the measured gap that the repository does **not own its encodings** — the assembler
  reads them from `target/refs/riscv-opcodes`, which is untracked, so a fresh clone cannot build a
  model. Derive `encoding.sexp` from the pinned table, track it, and gate that it still agrees.
  Acceptance: `git ls-files` shows the encodings tracked; the assembler reads the tracked file; a
  gate fires RED when the tracked file and the pinned upstream disagree.
  Verification: the full evidence path builds with the upstream directory HIDDEN; re-derivation fired RED on a one-bit edit.
  Commit: `SEMULITH-MM-0037`

- ID: `MODEL-METHOD.9` — **the semantics: `semantics.sexp`**
  Status: `done`
  Goal: what each of the declared instructions *does*, as expressions, each carrying the source
  locator it was derived from so a reviewer can check the expression against the sentence.
  Acceptance: every instruction in the declared scope has semantics; every form cites a locator;
  the file parses under a tracked reader that **refuses** a form it does not implement.
  Verification: 52 of 52 instructions, every rule cited; 4 controls fired RED; the language is 32 forms, each added because an instruction needed it.
  Commit: `SEMULITH-MM-0040`

- ID: `MODEL-METHOD.10` — **the extraction contract: is the definition SUFFICIENT?**
  Status: `done`
  Goal: state what a generator engine must be able to extract, and check it — every declared
  instruction has an encoding **and** semantics **and** a requirement; every state element has a
  reset; every obligation has its checks. ⭐ This turns *"the engine can extract all it needs"*
  from an intention into a verdict, and that verdict is the precondition for writing model code.
  Acceptance: fired RED by removing one instruction's semantics; `P1-LAB` cites this check rather
  than a judgement call.

  Result: met, `2026-09-27`. The contract as stated fired RED on the real corpus — measured:
  the ALU family (13 instructions) had no requirement at all. The leaf extended the catalogue
  (D/REQ/OB-ALU-REG and -IMM, statements grounded in the corpus's own §1.1.4 semantics), added
  the `(insns …)` coverage link to 11 requirements, and `scripts/check_extraction.py` now
  decides the integrative claim — SCOPE == ENCODING == SEMANTICS == REQUIREMENTS, one set four
  ways, plus every state element reset and every obligation checked both ways. The real corpus
  is SUFFICIENT (52 instructions, each with all three; the G0 report re-derived to 28/28/36/72
  in the same commit). The acceptance fired RED on a real-corpus copy with one instruction's
  semantics removed (`scope declares 1 instruction(s) the semantics set does not cover: add`).
  `EXTRACTION` registered as the 17th project doctrine — P1-LAB cites a verdict that runs.
  Design (recorded before code, `2026-09-27`), the contract read against the corpus first:
  - ⭐ **The contract as stated fires RED on the real corpus today — measured, and the point.**
    The scope declares 52 instructions; the encoding union and the semantics cover 52; but the
    requirement leg fails: only 7 instruction-kind requirements exist, and even generous
    family-mapping leaves the whole ALU family (ADD/SUB/SLT/SLTU/XOR/OR/AND + the immediates
    ADDI/SLTI/SLTIU/XORI/ORI/ANDI) with no requirement at all. A contract that passes over that
    is the intention restated. So this leaf extends the catalogue where the contract demands
    it: two new decision/requirement/obligation triples (D-ALU-REG, D-ALU-IMM), and an explicit
    instruction-coverage link on every requirement that names specific instructions.
  - **The link is data, added the way the layer allows**: `schema/requirements.sexp` gains
    `(insns …)` — an optional repeated string field, kind-agnostic (FENCE is a memory-kind
    requirement that names one instruction; ECALL-EBREAK an event-kind naming two). Every
    requirement whose statement commits specific instructions names them; reserved/hint decode
    requirements name none (they cover code points, not instructions).
  - **The contract is one equality across four sets + two smaller legs.**
    `scripts/check_extraction.py <unit-dir>` derives: SCOPE (the profile's declared names),
    ENCODING (the composed union), SEMANTICS (checked semantics coverage), REQUIREMENTS
    (∪ requirement.insns) — and requires all four EQUAL. Plus: every state element in
    `state.sexp` carries a `reset` (the corpus already does — integer_registers and pc); every
    obligation carries a positive AND a negative check. A gap names itself, the instruction,
    and the set that's short.
  - **Consequences, stated before code**: the catalogue grows (2 decisions, 2 requirements,
    2 obligations) and the tracked G0 report regenerates (more requirements → more checks,
    verdict unchanged) — `GATE-REPORT` re-derives the new bytes and is part of this commit.
    The ALU statements are sourced from the pinned chapters (RV32I §1.1.4 computational
    instructions; overflow-wrap and signed-comparison facts the corpus already states for
    kin instructions), with locators a reader can check.

- ID: `MODEL-METHOD.11` — **the primary-source corpus: a local cache that holds no absolute path**
  Status: `done`
  Goal: a curated corpus of vendor ISA/architecture manuals became available (`chipdoc`, 3,684
  files / 1.5 GB, 196 PDFs, explicitly curated *"to build software emulators (ISS) that run real
  C/C++/Rust software"*). It lives **outside this repository**, so naming it directly would put an
  absolute path in a tracked file — the exact thing Policy 12 forbids, because the repository must
  survive being moved to another filesystem. Give materials a home, an identity and a resolver that
  is relative all the way down.
  Acceptance: a tracked S-expression catalogue keyed by material id carrying title, revision,
  `sha256`, licence and a **repo-root-relative** cache path; a gitignored `.materials/` cache; a
  resolver that verifies the digest and, when a material is absent, refuses with the command that
  populates it; the external corpus reached **only** through an environment variable the repository
  never stores; `grep` for the corpus's absolute path across tracked files returns 0.
  ⛔ Sequenced before `.2`–`.4` deliberately: the census cannot record *where a material is* until
  "where" has a form that does not break when the repository moves.
  Verification: 22 materials catalogued and fetched, every digest verified; `0` tracked files name
  the corpus root; 15 self-test arms, 9 of them RED about paths.
  Commit: `SEMULITH-MM-0042`

- ID: `MODEL-METHOD.12` — **a citation that is present is not a citation that resolves**
  Status: `done`
  Goal: an external investigation challenged this profile's pinned source, reporting that no
  public build of `riscv-isa-manual` produces the §1.1 / §3.1 numbering all 52 semantic citations
  use. Re-derived: the challenge is **refuted** — 52 of 52 resolve in the pinned artifact, which is
  live, HTTP 200 and byte-identical to the committed digests. But the challenge was only possible
  because **nothing checked that a citation resolves**: `check_semantics.py` asks whether a
  citation is *present*, and a citation that points nowhere is still present. Close that, and close
  the ambiguity in `sources.toml` that made the wrong publication a reasonable guess.
  Acceptance: a tracked instrument resolves every semantic citation against the pinned artifacts
  and names the offending locator on failure, fired RED on a locator that does not exist; it
  refuses with instructions when the artifacts are not fetched rather than reporting success;
  `sources.toml` names its **publication**, not just a version string.
  ⛔ Not a commit gate: the artifacts are fetched, untracked and need the network, and the
  rendering declares no redistribution licence (`OQ-4`), so a fresh clone cannot run it. A gate
  that silently passes when its evidence is absent is the defect, not the fix.
  Verification: challenge refuted — 52 of 52 resolve, pinned URLs live and byte-identical; 10
  self-test arms; absent-evidence control refuses.
  Commit: `SEMULITH-MM-0043`

- ID: `MODEL-METHOD.13` — **the corpus moved, and my survey had sampled rather than swept**
  Status: `done`
  Goal: the corpus advanced three commits (`4201f50` → `3c45e81`) and both gaps this project
  measured are now closed at the source — 5 AMD64 APM volumes and Intel SDM Volume 1 imported.
  It also **moved** the RISC-V PDF, which breaks `--fetch` for a catalogued material today. And a
  re-survey found that my first pass **sampled by guessing vendor directory names** (`zilog`,
  `wdc`, `openrisc`, …) instead of sweeping by path, so it missed eight processor-class documents
  including an entire architecture, M68000, which sits under `nxp/m68k/` rather than a `motorola/`
  directory that does not exist.
  Acceptance: the catalogue is re-derived from a **path sweep**, not a sample, and says so; the
  corpus revision is re-pinned and drift from it is detected rather than discovered; both gap
  records are closed **with evidence and kept**, never deleted; the pinned `v20260120` HTML
  snapshot (72 pages + a verifying manifest) becomes a first-class material, which makes
  `check_citations.py` runnable from the cache **offline**; `--fetch` succeeds for every material.
  ⭐ The corroboration is worth recording on its own: chipdoc independently acquired the
  `v20260120` snapshot by its own route, and its digests for `intro`, `rv32` and `rv64` equal the
  ones committed in `sources.toml`. Two acquisitions, one set of bytes.
  Verification: 22 → 36 materials, 36 of 36 fetched; both gaps closed with evidence; citations
  resolve 52 of 52 **offline**; 20 self-test arms.
  Commit: `SEMULITH-MM-0044`

- ID: `MODEL-METHOD.6` — **no coding without the source of truth, mechanized**
  Status: `pending`
  Goal: a gate that refuses model implementation for a profile while a category its declared scope
  requires is `missing`. The rule is the director's; this makes it enforceable rather than
  remembered.
  Acceptance: fired RED against a deliberately uncovered category; `P1-LAB`'s precondition is the
  gate's verdict rather than a judgement call. Composes with `.10`: a category may be covered while
  the definition is still insufficient, and both must pass.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `MODEL-METHOD.3` | `pending` | the coverage census for `rv64i-lab-v0` — revise each first-pass disposition against evidence |

## Decisions

- `2026-09-14`: the catalogue is **JSON Lines against a JSON Schema**, not S-expressions — see the
  format section above, including the trigger that would re-open it.
- `2026-09-14`: the canonical definition is a **set of format-fit files**, not one file, and
  "single source of truth" is preserved by a no-duplicated-fact rule. S-expressions for encodings
  and semantics; records stay JSON/TOML because they are records and are already gated. See
  [`decision_canonical-definition-input`](../decisions/decision_canonical-definition-input.md).
- `2026-09-14`: `docs/INFORMATION_CATALOG.md` remains the **single owner** of what must be known.
  This tree adds a *material* and a *disposition* per category; it does not restate the category
  definitions, because a second copy of a taxonomy is a second thing to keep correct.

## Open Questions

- Does the specification PDF carry instruction encodings as text? Owner: `MODEL-METHOD.4`.
- Should DSP categories extend C01–C24 or form a parallel set? Deferred to `P3-BREADTH`, when a
  real DSP target exists to test the answer against. `§5` of the catalogue is carried as its own
  category group in the meantime.

## Blockers

- None.

## Acceptance Checklist (current leaf — `MODEL-METHOD.13`)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. Two causes, one in the corpus and one in me.

  WHERE (1): `materials/catalog.sexp`, `RVI-ISA-PDF-20260911`'s `corpus-path`. The corpus moved the
  file (`git diff --name-status` reports `R100`, a pure rename), so a tracked record became false:

  ```
  $ python3 scripts/materials.py --fetch RVI-ISA-PDF-20260911
    REFUSED RVI-ISA-PDF-20260911: not at $SEMULITH_CHIPDOC_ROOT/risc-v/isa/current/riscv-isa-manual_…pdf
  ```

  WHY: the catalogue pins a corpus revision (`4201f50`) but nothing compared it against the
  checkout, so a moved path could only ever be discovered by a failing fetch.

  WHERE (2): my survey method. I enumerated by **guessing vendor directory names** — `zilog`,
  `wdc`, `openrisc`, `openpower`, `sparc`, `ti`, `arm`, `amd`, `intel` — rather than sweeping by
  path. Every probe returned relevant results, so nothing signalled absence. Re-swept by path:

  ```
  $ find . -name '*.pdf' | grep -iE '/(isa|cpu|architecture|processors|m68k|z80|65c02|dsp|mcu)/'
  ```

  Eight documents missed, including the **entire M68000 architecture** (under `nxp/m68k/` — NXP
  inherited Motorola through Freescale) and **every board-class document in the corpus** (three
  ESP32 SoC manuals, two Raspberry Pi datasheets), which is the whole material base for `P5-BOARD`.
  ⭐ The giveaway I ignored: my own probe named a `motorola/` directory that does not exist.

- [x] **ADDRESSED (verified)** — leg 2. Corpus re-pinned `4201f50` → `3c45e81`; the moved path
  corrected; the catalogue re-derived from the sweep and carrying a `derivation` field that names
  the sweep command, so the method can be judged rather than believed. 22 → **36 materials**:

  ```
  $ python3 scripts/materials.py --fetch     ->  36 of 36 ok, every sha256 verified
  $ python3 scripts/materials.py --self-test ->  20 pass / 0 fail  (was 15)
  ```

  **Both gaps this project measured are closed at the source, three commits after it reported
  them** — and closed **with evidence and kept**, never deleted, because a deleted gap erases the
  fact that the question was asked:

  ```
  GAP-AMD64-APM        (status resolved)  5 AMD64 APM volumes imported at e401a56
                       (residual …)       AMD's doc hub is not scriptable; a newer revision could exist
  GAP-INTEL-SDM-VOL1   (status resolved)  SDM Vol 1 (253665 rev 092, 600 pp) imported at 98de100
  ```

  ⭐ **A material that is not one file.** The pinned `v20260120` HTML snapshot is 72 pages; a
  snapshot identified by the digest of one page is not identified at all. `kind snapshot` names a
  `manifest`, whose digest is the material's identity and whose entries verify every page:

  ```
  ok  RVI-PINNED-V20260120 -> .materials/riscv/pinned-v20260120 (6,229 B, sha256 verified,
                                                                 72 manifest entries verified)
  ```

  ⭐ **And that ends a real fragility.** The citation evidence lived only in an untracked working
  area that needs the network — the reason `check_citations.py` could not be a gate. It now runs
  from the manifest-verified cache, **offline**, and says which route it used:

  ```
  via fetched working area target/sources/riscv-v20260120        -> 52 of 52 resolve
  via materials cache .materials/riscv/pinned-v20260120/unpriv   -> 52 of 52 resolve
      (manifest-verified, offline)
  ```

  ⛔ Corpus drift is now **detected, not discovered**: `--list` and `--verify` compare the
  catalogued revision against `git -C $ROOT rev-parse HEAD` and say so.

  ⭐ **Independent corroboration of the pin.** chipdoc acquired the `v20260120` snapshot by its own
  route; its digests for `intro`, `rv32` and `rv64` **equal** those committed in `sources.toml`,
  and its `SHA256SUMS` verifies 72 of 72. Two acquisitions, two parties, one set of bytes — which
  is the one thing last leaf's external challenge could not have produced by agreement.

- [x] **NO REGRESSION** — leg 3. ⛔ The S-expression reader **refused this leaf's own first draft**
  of the catalogue — the generator had written literal `\uXXXX` escapes — and refused it by name:

  ```
  SexpError: materials/catalog.sexp:41: unknown escape '\u' in string. The reader refuses rather
  than guessing what it was meant to be
  ```

  That is `SOT-FORMAT.7`'s closed escape table doing exactly the job it was built for, one leaf
  later, on content rather than on a fixture. Four escapes replaced with the characters themselves;
  the reader was not touched. Full re-run:

  ```
  $ python3 scripts/sexp.py --self-test          -> 18 pass / 0 fail
  $ python3 scripts/check_citations.py           -> 52 of 52 (both routes)
  $ python3 scripts/check_semantics.py …         -> 52 of 52 declared instruction(s)
  $ python3 scripts/run_smoke.py | tail -1       -> run_smoke: ok …
  $ bash scripts/check_doctrines.sh              -> all doctrines green
  ```

- [x] **LOCKSTEP** — knowledge card
  [`a-survey-that-found-things-can-still-have-missed-things`](../knowledge/a-survey-that-found-things-can-still-have-missed-things.md),
  promoted from the dated `DEV_NOTES.md` lesson; `TOOLBOX.md` already carries the resolver rows;
  `materials/` stays within its registry ceilings (43,462 B against a 131,072 B per-part bound).

## ROUTING EVIDENCE

`MODEL-METHOD.13` — the sweep surfaced **every board-class document in the corpus**, which belongs
to `P5-BOARD` and not to this tree: three ESP32 SoC manuals, the RP2040 and the RP2350 datasheets.
Measured and catalogued rather than routed as prose, with two pairings worth the next reader's
attention. `RP2040-DS` pairs exactly with `ARM-M-DDI0419E` — a 374-page architecture manual and the
part built around it, processor and board in two documents, which is the cleanest available test of
this project's layer boundary. `RP2350-DS` describes a part carrying **both** an Arm Cortex-M33 and
a Hazard3 RISC-V core on one die, software-selectable: if `MODEL-COMPOSE`'s slots are real, one
board description should compose with either processor. Reproduces outside the family: the sweep
was over the whole corpus by path, not over `raspberry-pi/`.

`ESP32-C3-TRM` is the one this project reaches first — a shipping RISC-V SoC whose UART and
interrupt matrix are specified in the document where the director said they belong.


`MODEL-METHOD.12` — the interim substitution offered by the external investigation (pull the
2026-01-17 / 01-21 release PDFs as "the closest official match") is **declined**, and the reason is
recorded where the next person will meet it, in `materials/catalog.sexp` as `GAP-RISCV-JAN-2026-PDF`.
Measured: those PDFs number RV32I §2 and RV64I §4, so adopting them would turn 52 resolving
citations into 52 unresolvable ones — a strictly worse position reached by acquiring *more*
material. They may be catalogued later under their own ids as additional references; acquiring a
document and repointing a pin are two decisions and only the first is cheap.


Two findings measured here are **not** this tree's to fix, and both are recorded in the catalogue
as first-class `(gap …)` records rather than as prose someone must remember:

- `GAP-AMD64-APM` — probed `find . -iname '*APM*' -o -iname '*AMD64*' -o -iname '*24592*'` → no
  match. The corpus's `amd/` directory holds exactly one document, an IOMMU specification. **There
  is no AMD instruction-set manual**, so an x86-64 unit built from this corpus would rest on
  Intel's description of the architecture alone. Reproduces outside the family: the probe is over
  the whole corpus, not over `amd/`.
- `GAP-INTEL-SDM-VOL1` — probed `find . -iname '*253665*' -o -iname '*Vol1*'` → no match, while
  Volumes 2, 3 and 4 are present. Volume 1 carries the basic execution environment, data types and
  register overview — the architectural **state** a model declares first. An x86 unit could not
  state its state from this corpus alone.

Both belong to `MODEL-METHOD.3`, the coverage census, which is where a gap becomes a disposition.
Neither is routed to another tree; neither is worked around here.

## Acceptance Checklist (leaf MODEL-METHOD.10)

- [x] **REPRODUCE / ISSUE** — the contract as stated, run against the corpus before any code:

  ```
  $ python3 - <<'PY'   # the requirement leg, measured
  > reqs = records_sexp.load("profiles/rv64i-lab-v0/requirements.sexp")
  > insns = {i for r in reqs for i in r.get("insns", [])}   # {} — the link did not exist
  > PY
  $ # and with the link curated on the 7 instruction-kind requirements alone:
  $ # the ALU family (add sub slt sltu xor or and + addi slti sltiu xori ori andi) has NO requirement
  ```

  The catalogue itself failed the contract's requirement leg — 13 instructions uncovered. That
  is the leaf's real finding, and fixing the corpus is part of the fix.

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHY: every per-family check (ENCODING, SEMANTICS,
  RECORD-SCHEMA) proved its own leg, and nothing proved they described the SAME instruction
  set — the integrative claim was the gap. WHERE: measured, not read —

  ```
  $ grep -c 'insns' schema/requirements.sexp
  0                                             # no requirement↔instruction link existed
  $ grep -c 'ALU' profiles/rv64i-lab-v0/requirements.sexp
  0                                             # the ALU family: no requirement record at all
  ```

  The catalogue itself failed the contract's requirement leg; fixing the corpus is part of
  the fix, not a waiver of it.

- [x] **FIX** — data first: `(insns …)` on `schema/requirements.sexp` (kind-agnostic;
  FENCE names one instruction, ECALL-EBREAK two); the catalogue extended where the contract
  demands it (D/REQ/OB-ALU-REG, D/REQ/OB-ALU-IMM, statements grounded in the corpus's own
  §1.1.4 semantics — including SLTIU's sign-then-unsigned quirk); `check_extraction.py`
  decides one-set-four-ways plus the reset and checks legs; `EXTRACTION` registered as the
  17th doctrine so P1-LAB cites a verdict that runs.

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  ```
  $ python3 scripts/check_extraction.py --self-test
  check_extraction --self-test: 6 pass / 0 fail
  $ bash scripts/check_extraction.sh --self-test
  EXTRACTION --self-test: 3 pass / 0 fail
  $ python3 scripts/check_extraction.py profiles/rv64i-lab-v0
  the definition is SUFFICIENT for an engine: 52 instructions, each with encoding +
  semantics + requirement; reset everywhere; obligations checked both ways
  $ # the acceptance, on a real-corpus copy with one instruction's semantics removed:
  $ python3 scripts/check_extraction.py <copy>
  REFUSED — scope declares 1 instruction(s) the semantics set does not cover: add   rc=1
  ```

- [x] **NO REGRESSION** — `bash scripts/check_requirements.sh --self-test` 23 pass / 0
  fail + real run green (it caught a wrong obligation id mid-curation — `OB-D-ALU-REG` vs
  `OB-ALU-REG` — fixed before commit); `bash scripts/check_profile_consistency.sh` 39 arms +
  real run green; GATE-REPORT re-derived (28/28/36/72, verdict unchanged); the catalogue diff
  is minimal (11 insns additions, 2+2+2 new records, headers preserved); the round-trip owner
  carries `insns` and untouched records re-serialize byte-identically; whole gate green after
  staging.

- `promotion: declined (the "one set, four ways" pattern is stated in the tool's docstring).`

- [x] **LOCKSTEP** — `scripts/check_doctrines.project.sh` + both mirrors in the registering
  commit; `LIVE_STATUS.md` re-derived (17 doctrines, 202 arms); the count-bearing docs
  (DOSSIER/ENVIRONMENT/LIVE_STATUS rows) to 28/36/72; `TOOLBOX.md`; `MEMORY.md`,
  `CHANGELOG.md`, `DEV_NOTES.md`, `docs/TASK_TREE.md` and this tree — one commit.

## Acceptance Checklist (leaf MODEL-METHOD.7)

- [x] **REPRODUCE / ISSUE** — the rule as it stood: `decision_canonical-definition-input`
  states the no-duplicated-fact rule in prose, nothing mechanizes it. Census, pre-code:

  ```
  $ ls doctrine/fact_ownership.tsv 2>&1
  ls: doctrine/fact_ownership.tsv: No such file or directory
  $ grep -c 'MIRROR' scripts/check_requirements.sh
  0                                             # obligation->requirement restatement: ungoverned
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHY: the corpus legitimately DERIVES facts into
  mirrors (a requirement restates a decision; an obligation restates its requirement), and a
  mirror with no governor is one fact stated in two, free to drift — the exact failure the
  prose rule names. WHERE: measured, not read —

  ```
  $ grep -c 'MIRROR' scripts/check_requirements.sh
  0                                             # obligation->requirement: no governor at all
  $ python3 - <<'PY'
  > obs = records_sexp.load("profiles/rv64i-lab-v0/contract-obligations.sexp")
  > print(sum(1 for o in obs if o["parameters"].get("requirement_id")))   # -> 28
  > PY
  ```

  Three mirror pairs were governed (decision<->requirement by RECORD-SCHEMA rule 4;
  state<->profile by PROFILE-CONSISTENCY; composition<->fragments by UNIT-COMPOSITION); the
  obligation->requirement pair was not — 28 restatements, all matching today, free to drift.

  ```
  $ python3 - <<'PY'   # 28 obligations restate a requirement's statement; nothing enforces it
  > obs = records_sexp.load("profiles/rv64i-lab-v0/contract-obligations.sexp")
  > print(sum(1 for o in obs if o["parameters"].get("requirement_id")))   # -> 28
  > PY
  ```

- [x] **FIX** — the registry as data (`doctrine/fact_ownership.tsv`, beside the routes
  registry in shape); the governor where it belongs (RECORD-SCHEMA rule 9 — the mirror check
  keys on the obligation's own `requirement_id`); the gate verifying the registry holds and is
  complete against the corpus's actual pairs.

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  ```
  $ bash scripts/check_requirements.sh --self-test
  RECORD-SCHEMA --self-test: 26 pass / 0 fail     # was 23; +3 mirror arms
  $ bash scripts/check_fact_ownership.sh --self-test
  FACT-OWNERSHIP --self-test: 8 pass / 0 fail
  $ bash scripts/check_fact_ownership.sh
  FACT-OWNERSHIP: ok (8 fact kind(s): one owner each, every mirror governed)
  $ # the acceptance's shape, fired: an ungoverned mirror in the registry
  UNGOVERNED MIRROR state: '...' restates '...' with no governing doctrine          rc=1
  ```

- [x] **NO REGRESSION** — `bash scripts/check_requirements.sh --self-test` 26 pass / 0
  fail + real run green on the 28 real mirrors; PROFILE-CONSISTENCY 39/0; the whole guard
  set and the enforcer green after staging.

- `promotion: declined (the "govern every mirror or refuse it" rule is stated in the gate's header and this leaf, where anyone adding a fact kind meets it).`

- [x] **LOCKSTEP** — `scripts/check_doctrines.project.sh` + both mirrors in the registering
  commit; `LIVE_STATUS.md` re-derived (18 doctrines, 213 arms); `TOOLBOX.md`; `MEMORY.md`,
  `CHANGELOG.md`, `DEV_NOTES.md`, `docs/TASK_TREE.md` and this tree — one commit.

## Acceptance Checklist (leaf MODEL-METHOD.2)

- [x] **REPRODUCE / ISSUE** — the materials side had documents but no REQUIREMENT type.
  Census, pre-code:

  ```
  $ ls schema/units.sexp schema/category-needs.sexp materials/units.sexp materials/category-needs.sexp 2>&1
  ls: schema/units.sexp: No such file or directory           # the type did not exist
  $ grep -c 'category-need' schema/*.sexp materials/*.sexp 2>/dev/null | grep -v ':0' | wc -l
  0                                             # and nothing bound categories to units
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHY: a catalogue of documents (the who/what/where
  of materials) cannot say which information a unit OWES its model — that needs a record
  binding each INFORMATION_CATALOG category to the material kind that supplies it, per unit.
  WHERE: measured, not read —

  ```
  $ ls schema/units.sexp materials/category-needs.sexp 2>&1 | grep -c 'No such'
  2                                             # no schema for either family
  $ grep -rl 'category-need' schema/ materials/ | wc -l
  0                                             # and no record bound a category to a unit
  ```

  Nothing like the requirement type existed anywhere in the corpus.

- [x] **FIX** — two record families on the house records track (`.3`'s path walked again):
  the unit registry and the category-needs catalogue, schema-declared, mapping-owned,
  gated by RECORD-SCHEMA rules 10–11 (registry never empty; `missing` owes a reason;
  `covered` names its material; board-layer `missing` for a processor refuses as LAYER LIE).

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  ```
  $ bash scripts/check_requirements.sh --self-test
  RECORD-SCHEMA --self-test: 32 pass / 0 fail     # was 26; +6 arms on the new families
  $ bash scripts/check_requirements.sh
  RECORD-SCHEMA: ok (7 record file(s) validate and agree with their profile)
  $ grep -c '^(category-need' materials/category-needs.sexp
  24                                            # every category, explicit layer
  $ # the acceptance's rule, fired on a board-layer 'missing' for the processor unit:
  LAYER LIE category-needs.sexp [C19 for rv64i-lab-v0]: a board-layer category dispositioned
  'missing' for a processor unit — ... the honest disposition is 'out-of-scope'    rc=1
  ```

- [x] **NO REGRESSION** — the untouched catalogues re-serialize byte-identically (the new
  mappings dispatch on `book`/`disposition` BEFORE `kind`, so requirement/obligation
  round-trips are unmoved); the duplicate-id arm now keys category-needs on (category, unit);
  `python3 scripts/sexp.py --self-test` 18 pass / 0 fail; kernel 50 pass / 0 fail;
  `python3 scripts/compare_readers.py` 29 of 29 agree (the four new files swept); whole gate
  green after staging.

- `promotion: declined (the ABSENT-vs-NEVER-NEEDED disposition vocabulary is stated in the schema header and this leaf, where the .3 census meets it).`

- [x] **LOCKSTEP** — `TOOLBOX.md`; `MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md`,
  `docs/TASK_TREE.md` and this tree — one commit. No new doctrine: the families ride the
  records track RECORD-SCHEMA already owns.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-27` | `MODEL-METHOD.2` | `--self-test` | `32 pass / 0 fail` (was 26; NO REGISTRY, LAYER LIE, REASONLESS MISSING, UNEVIDENCED COVERED, EMPTY REGISTRY, GREEN census) |
| `2026-09-27` | `MODEL-METHOD.2` | real run | `ok (7 record file(s))` — the 24-row first honest pass green |
| `2026-09-27` | `MODEL-METHOD.2` | schema validation | both new catalogues `conform` under the two new schemas |
| `2026-09-27` | `MODEL-METHOD.7` | mirror inventory, pre-code | 3 pairs governed (decision<->requirement, state<->profile, composition<->fragments); obligation->requirement UNGOVERNED — 28 restatements, all matching, nothing refusing drift |
| `2026-09-27` | `MODEL-METHOD.7` | RECORD-SCHEMA rule 9 + arms | `26 pass / 0 fail` (was 23); MIRROR DRIFT / MIRROR WITHOUT SOURCE / GREEN mirror |
| `2026-09-27` | `MODEL-METHOD.7` | gate `--self-test` | `8 pass / 0 fail`; real run `ok (8 fact kind(s))` |
| `2026-09-27` | `MODEL-METHOD.7` | the acceptance's shapes fired | UNGOVERNED MIRROR and UNREGISTERED MIRROR PAIR, both rc=1 |
| `2026-09-27` | `MODEL-METHOD.10` | contract as stated, run pre-code | requirement leg FAILS: no `insns` link; ALU family (13 instructions) uncovered |
| `2026-09-27` | `MODEL-METHOD.10` | tool `--self-test` | `6 pass / 0 fail`; gate `--self-test` `3 pass / 0 fail` |
| `2026-09-27` | `MODEL-METHOD.10` | real corpus | `SUFFICIENT for an engine: 52 instructions, each with encoding + semantics + requirement` |
| `2026-09-27` | `MODEL-METHOD.10` | the acceptance's RED (real-corpus copy, one sem rule removed) | `does not cover: add`, rc=1 |
| `2026-09-27` | `MODEL-METHOD.10` | gates on the extended catalogue | RECORD-SCHEMA 23/0 + green (caught a wrong obligation id, fixed); PROFILE-CONSISTENCY 39/0 + green; GATE-REPORT re-derived 28/28/36/72 |
| `2026-09-14` | `MODEL-METHOD.11` | corpus survey: files, PDFs, vendors | 3,684 files / 1.5 GB / 196 PDFs across 23 vendors |
| `2026-09-14` | `MODEL-METHOD.11` | `materials.py --self-test` | `15 pass / 0 fail`; 9 RED arms about paths |
| `2026-09-14` | `MODEL-METHOD.11` | `materials.py --fetch` (22 materials) | 22 of 22, every sha256 verified, 233 MB |
| `2026-09-14` | `MODEL-METHOD.11` | Policy 12: corpus root in any tracked file | `0` files; control confirms the probe can see one |
| `2026-09-14` | `MODEL-METHOD.11` | Policy 13: cache volume vs repo volume | both `/dev/disk7s1` |
| `2026-09-14` | `MODEL-METHOD.11` | is the RISC-V PDF the artifact the profile pins? | NO — `20260911 Intermediate` vs pinned `v20260120` |
| `2026-09-14` | `MODEL-METHOD.11` | do our 52 citations resolve in that PDF? | NO — it numbers RV32I §2.1 / RV64I §2.2; we cite §1.1 / §3.1 |
| `2026-09-14` | `MODEL-METHOD.11` | RISC-V ISA manual licence, read from the document | CC-BY-4.0 — bears on `OQ-4` / rule `SRC-01` |
| `2026-09-14` | `MODEL-METHOD.11` | gap probe: AMD64 ISA manual | absent; `amd/` holds one IOMMU spec |
| `2026-09-14` | `MODEL-METHOD.11` | gap probe: Intel SDM Volume 1 | absent; Vols 2/3/4 present |
| `2026-09-14` | `MODEL-METHOD.11` | regression: sexp, semantics, smoke, doctrines | 18/0, 52 of 52, ok, all green |
| `2026-09-14` | `MODEL-METHOD.12` | pinned artifacts on disk vs committed digests | 3 of 3 MATCH, byte-identical |
| `2026-09-14` | `MODEL-METHOD.12` | pinned URLs re-fetched live | HTTP 200 ×3, identical to the pinned copies |
| `2026-09-14` | `MODEL-METHOD.12` | headings published by the pinned rv64.html | `3.1`, `3.1.1`, `3.1.2`, `3.1.2.1`, `3.1.2.2`, `3.1.3`, `3.1.4` |
| `2026-09-14` | `MODEL-METHOD.12` | `check_citations.py` on the real profile | **52 of 52** resolve — the challenge is refuted |
| `2026-09-14` | `MODEL-METHOD.12` | `check_citations.py --self-test` | `10 pass / 0 fail` |
| `2026-09-14` | `MODEL-METHOD.12` | control: working area removed | REFUSED with the fetch command, `exit=1` — no silent pass |
| `2026-09-14` | `MODEL-METHOD.12` | licence of the docs.riscv.org rendering | only `Copyright © RISC-V International®` — no CC-BY; `OQ-4` stays open |
| `2026-09-14` | `MODEL-METHOD.13` | corpus commits since the catalogued revision | 3 (`4201f50` → `3c45e81`), 88 files, +345,967 lines |
| `2026-09-14` | `MODEL-METHOD.13` | `--fetch` of the moved RISC-V PDF, before the fix | REFUSED — a tracked record was false |
| `2026-09-14` | `MODEL-METHOD.13` | path sweep vs the sampled first survey | 8 documents missed, incl. all of M68000 and every board document |
| `2026-09-14` | `MODEL-METHOD.13` | chipdoc's snapshot digests vs this project's `sources.toml` | `intro`/`rv32`/`rv64` all EQUAL — independent acquisition |
| `2026-09-14` | `MODEL-METHOD.13` | `SHA256SUMS` of the pinned snapshot | 72 OK / 0 FAILED |
| `2026-09-14` | `MODEL-METHOD.13` | `materials.py --self-test` after snapshot support | `20 pass / 0 fail` (was 15) |
| `2026-09-14` | `MODEL-METHOD.13` | `materials.py --fetch` (36 materials) | 36 of 36, digests verified, 72 manifest entries |
| `2026-09-14` | `MODEL-METHOD.13` | `check_citations.py` with the working area removed | 52 of 52 **offline**, via the manifest-verified cache |
| `2026-09-14` | `MODEL-METHOD.13` | the reader on this leaf's own first draft | REFUSED: `unknown escape '\u'` — content fixed, reader untouched |
| `2026-09-14` | `MODEL-METHOD.1` | sweep over every pinned configuration scalar | 1 further instance found: Spike's ISA was an input, not a read-back |
| `2026-09-14` | `MODEL-METHOD.1` | Spike ISA read-back, with its control | `rv64i` → `rv64i`; `rv64im` → `rv64im` |
| `2026-09-14` | `MODEL-METHOD.1` | `compare_platforms.py` on both matched models | 4 of 4 fields disagree; 4 devices only Spike advertises |
| `2026-09-14` | `MODEL-METHOD.1` | rule 5b fired RED on the real dossier | `UNSCOPED SCALAR …/spike` |
| `2026-09-14` | `MODEL-METHOD.1` | `check_profile_consistency.sh --self-test` | `39 pass / 0 fail`; 39 written, 39 run |
| `2026-09-14` | `MODEL-METHOD.8` | census: encodings owned by the repo, semantics present | `0` and `0` — both absent |
| `2026-09-14` | `MODEL-METHOD.8` | the whole evidence path with the upstream MOVED ASIDE | `run_smoke: ok` — 4 guests, 2 models, reproduced |
| `2026-09-14` | `MODEL-METHOD.8` | re-derivation fired RED on a one-bit `funct3` edit | `DIFFERS … no longer matches what the pinned tables generate` |
| `2026-09-14` | `MODEL-METHOD.8` | S-expression reader controls | 7 pass / 0 fail, incl. `;` inside a string and a string spanning lines |
| `2026-09-14` | `MODEL-METHOD.8` | `fetch_references.sh --verify-only` | 12 of 12 `MATCH` |
| `2026-09-14` | `MODEL-METHOD.9` | census: machine-executable semantics before this leaf | `0` files; 26 rules, all prose |
| `2026-09-14` | `MODEL-METHOD.9` | `check_semantics.py` on the real fragment | `52 of 52 declared instruction(s) have checked semantics` |
| `2026-09-14` | `MODEL-METHOD.9` | 4 controls: missing, unknown form, bad operand, no source | each refused by name; all restored |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `MODEL-METHOD.2` | `SEMILITH-MM-0046 (leaf MODEL-METHOD.2): …` | the materials requirement: two record families, the unit registry, the 24-category first pass |
| `MODEL-METHOD.7` | `SEMILITH-MM-0045 (leaf MODEL-METHOD.7): …` | the no-duplicated-fact registry and its gate; the obligation mirror governed |
| `MODEL-METHOD.10` | `SEMILITH-MM-0044 (leaf MODEL-METHOD.10): …` | the extraction contract: one set four ways, and P1's start condition fully met |
| `MODEL-METHOD.13` | `SEMULITH-MM-0044 (leaf MODEL-METHOD.13): the corpus moved, and my survey had sampled` | 36 materials; both gaps closed; citations resolve offline |
| `MODEL-METHOD.12` | `SEMULITH-MM-0043 (leaf MODEL-METHOD.12): a citation that is present is not a citation that resolves` | challenge refuted; 52 of 52 resolve |
| `MODEL-METHOD.11` | `SEMULITH-MM-0042 (leaf MODEL-METHOD.11): materials get an identity, and no path that breaks on a move` | 22 materials, 2 measured gaps, 0 absolute paths |
| `MODEL-METHOD.9` | `SEMULITH-MM-0040 (leaf MODEL-METHOD.9): the semantics, 52 of 52, every rule cited` | well-formed and cited — NOT verified correct |
| `MODEL-METHOD.8` | `SEMULITH-MM-0037 (leaf MODEL-METHOD.8): the repository owns its encodings` | builds with the upstream hidden; re-derivation fired RED |
| `MODEL-METHOD.1` | `SEMULITH-MM-0033 (leaf MODEL-METHOD.1): answer the narrower-instrument sweep with a wider instrument` | 1 further instance found and fixed; the pattern gated |

## Changelog

- `2026-09-14`: Created. The project could state *what must be known* to model a processor (24
  catalogue categories) but not *which document supplies each*, nor which are supplied by nothing.

  Census behind that claim, over every population that could refute it — any tracked file binding a
  catalogue category id to a material, and any tracked schema for such a record:

  ```
  $ grep -cE '^\| C[0-9]{2} \|' docs/INFORMATION_CATALOG.md
  24                                    # C01..C24, one table row each
  $ git grep -lE 'C(0[1-9]|1[0-9]|2[0-4])\b' -- profiles schemas doctrine | wc -l
  0                                     # nothing binds a category to a material
  $ git grep -lE '"category"' -- schemas
  schemas/requirement.schema.json       # a DIFFERENT sense: source_semantics.category
  ```

  The categories are defined in exactly one place, nothing binds one to a material, and the single
  schema hit is a false friend — `source_semantics.category` classifies a requirement's *semantic
  status* (defined / implementation-defined / unspecified), not an information category. That gap
  is what this tree closes.
  ⛔ Two of the three numbers above were **typed before they were run**, and were wrong (`0` for a
  population that is `1`, and `24` from a grep that actually counted 26 lines because the file
  mentions some ids again in prose). They are corrected here from the commands' real output — in
  the same leaf that exists to stop a scalar being trusted without checking what it ranges over,
  which is the joke writing itself.
