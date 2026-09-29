# MODEL-METHOD: the method for modelling a unit, and the materials that method requires

## Metadata

- Tree ID: `MODEL-METHOD`
- Status: `active` (reopened `2026-09-29` for `.14` — the `MODEL-BOOKS.2` finding: the
  pinned specification's own PDF carries the instruction-format tables as selectable text,
  so the encodings' second provenance may be replaceable by the primary document; the
  evaluation is director-scheduled)
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
  Status: `done`
  Goal: fill the catalogue for the first model honestly. Expected outcome is that a **minority**
  of categories are covered — the profile excludes privilege, translation, floating point, vectors
  and atomics — and the value is in the `missing` rows, not the `covered` ones. ⛔ Device and
  interconnect categories are **`deferred-to-board`**, not missing: they are `P5-BOARD`'s to own,
  and the CPU records an assumption in their place.
  Acceptance: no category absent; each `missing` row names what would close it.


  Result: met, `2026-09-27`. The census swept the cached snapshot rather than trusting the
  first pass, and the evidence revised it: all 8 covered categories' subject matter verified
  present in the pinned pages, and — the measured surprise — the excluded subsystems' chapters
  (f/d/q/v/a-st-ext, rvwmo, counters, zicsr, zifencei) are IN the same snapshot. `missing`
  therefore means the profile excludes the subsystem (the facts are not part of this unit's
  model), not "material absent" — every one of the 6 missing rows now names its closer (a
  profile revision against snapshot chapters for C07/C08/C16; the separate Privileged
  Architecture manual for C12/C14/C15; the Debug specification for C18). Device and
  interconnect categories (C19/C20/C21) moved from `out-of-scope` to the new
  `deferred-to-board` disposition — P5-BOARD owns them and the CPU records an environment
  assumption in their place — and the census now reads: 10 covered, 4 partial, 6 missing (all
  closers named), 3 deferred-to-board, 1 out-of-scope (C17, contract-owned). RECORD-SCHEMA
  rule 12 (UNRESOLVED MATERIAL) keeps every named material honest against catalog.sexp; 33
  arms.

- ID: `MODEL-METHOD.4` — **acquire what the census says is missing and reachable**
  Status: `done`
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
  Result: met, `2026-09-27`. The run-real-code set is acquired, digest-pinned, cached on-volume at
  `.materials/run-real-code/` (gitignored, per the no-redistribution doctrine), and re-derivable
  from the curl commands below. The PDF question is answered YES with the extraction evidence.
  Design (recorded before code, `2026-09-27`), the fetch and provenance machinery read first:
  - ⭐ **Why the bytes are not gate-mechanized, stated rather than silently routed around.** The
    natural homes each refuse these documents for a measured reason: the profile's `sources.sexp`
    composes `base_url/file` — ONE origin per document, and this set is four origins; the
    materials catalogue's fetch seam copies from a `$ENV`-rooted corpus checkout — no URL kind;
    `docs/provenance/` manifests list TRACKED bytes — and third-party documents are not
    redistributed (the materials doctrine, for the same reason `.materials/` is gitignored). So
    the tracked record is THIS LEAF's digest table plus the cache README, and mechanizing a URL
    kind in `materials.py` is the named candidate if a second web-sourced set ever arrives.
  - **The acquisitions, each pinned (sha256 · bytes · cache path · re-derivation):**
    - `riscv-psabi.html` — the RISC-V psABI canonical render, `https://riscv-non-isa.github.io/riscv-elf-psabi-doc/` — `599f10a4b86090c18ded77c813ac89bc5e363e69e545653d46f3090f3f8c9b75` · 547,617 B. The calling convention: registers, stack, TLS. Re-derive: `curl -sSL -o .materials/run-real-code/riscv-psabi.html https://riscv-non-isa.github.io/riscv-elf-psabi-doc/`
    - `elf-gabi.pdf` — the System V / gABI ELF specification, `https://refspecs.linuxfoundation.org/elf/elf.pdf` — `422b6c64e91410fa83008aa2565532c9b523dfa33da8f56b4e2556a576b3ef18` · 345,215 B. Re-derive: `curl -sSL -o .materials/run-real-code/elf-gabi.pdf https://refspecs.linuxfoundation.org/elf/elf.pdf`
    - `linux-asm-generic-unistd.h` — the generic syscall numbers (exit = `__NR_exit`), `https://raw.githubusercontent.com/torvalds/linux/master/include/uapi/asm-generic/unistd.h` — `2e6a1b646c5111ad76db86c0508684223d9956384e1d23e86733eca09505d02d` · 32,020 B. The exit convention a hosted program expects; the laboratory's own harness contract (ECALL/EBREAK as typed environment traps) is the freestanding form, and this header is the hosted form's anchor. Re-derive: `curl -sSL -o .materials/run-real-code/linux-asm-generic-unistd.h https://raw.githubusercontent.com/torvalds/linux/master/include/uapi/asm-generic/unistd.h` ⛔ `master`-pinned: digest protects against silent change; a locator-stable pin is P1-LAB's refinement.
    - `compiler-rt-builtins-readme.txt` — LLVM compiler-rt's builtins inventory, `https://raw.githubusercontent.com/llvm/llvm-project/main/compiler-rt/lib/builtins/README.txt` — `3f89383ae3699e369853e9d6b1140f5372da356b76e86e1c13252810c2b83a97` · 15,334 B. Contains `__muldi3 (di_int a, di_int b); // a * b` — the soft-multiply intrinsic a no-`M` target calls. Re-derive: `curl -sSL -o .materials/run-real-code/compiler-rt-builtins-readme.txt https://raw.githubusercontent.com/llvm/llvm-project/main/compiler-rt/lib/builtins/README.txt`
  - **The PDF question, answered:** YES — the specification's PDF rendering carries the
    instruction-format tables as selectable text. Evidence: `riscv-spec.pdf` (release asset
    `riscv-isa-release-f443409-2026-09-26`) extracts 1.96 MB of text via `pdftotext`, and the
    RV32I format-table region yields clean cells — `funct7 / rs2 / rs1 / funct3 / rd / opcode`.
    Encodings CAN be re-sourced from the primary document; the shared-ancestry position
    improves the day a leaf chooses to. Cached at
    `.materials/run-real-code/riscv-spec-release-f443409.pdf` (`3f470aa95299fcbb…` · 5,522,367 B).
  - **SRC-02 records — the acquisitions that failed, each with its attempt:**
    - the **pinned revision's** release PDF: searched three pages of
      `riscv/riscv-isa-manual` releases for a `20260120`-tagged asset; none found (recent tags
      are per-commit `riscv-isa-release-<sha>-<date>`). The PDF answer above stands on the
      current release asset; matching it to the pinned `v20260120` revision is a follow-up
      attempt when the tag is located. Bounded claim: the answer is about the rendering FORM,
      which the asset demonstrates.
    - the **chipdoc corpus route**: `$SEMULITH_CHIPDOC_ROOT` is unset in this environment, so
      the feed the director flagged (psABI, SBI, BRS, U-Boot, DT, FU540, virtio, ACT) could not
      be read; the psABI was acquired from its canonical public render instead. When the
      variable is set, prefer the corpus copy and cross-check the digest.
    - the **startup/runtime contract**: not a document to acquire — the laboratory's harness
      contract already owns entry state and the ECALL/EBREAK exit convention (`D-ENTRY-STATE`,
      `OB-ENV-EVENT-DELIVERY`); the hosted-form anchors are the two acquisitions above.


  Result: met, `2026-09-27`. The unit registry gained `(requires …)` — the categories a
  unit's scope declares — and `SCOPE-COVERAGE` (19th doctrine, `scripts/check_scope_coverage.sh`,
  7 arms) refuses the day a required category is `missing` or has no census row, fired RED
  before registration on a scratch unit whose required category was absent. `rv64i-lab-v0`
  declares its 14 in-scope categories; the verdict reads `1 unit(s) may code — every required
  category covered` — **P1-LAB's precondition is now a gate's verdict, not a judgement call**,
  composed with EXTRACTION (coverage says the facts are OWNED; extraction says they are
  EXTRACTABLE; both must pass). The tree closes at 13/13.

- ID: `MODEL-METHOD.5` — **the method, in prose, written to be learned from**
  Status: `done`
  Goal: document → decision → requirement → obligation → check, with the judgement calls named:
  authority versus semantic class, what makes an expected value *derived* rather than copied, and
  when a disagreement is a profile difference rather than a defect. ⭐ Written so a student could
  apply it to a processor this project has never modelled — which means the **order** of the steps
  is justified, not merely listed, and the rejected alternatives are kept.
  Acceptance: one rule followed end to end by name; the non-mechanical steps identified as such;
  a reader could carry the method to a different ISA without this project's documents.

  Result: met, `2026-09-27`. `docs/METHOD.md` — one self-contained document, 9.3 KB, written to
  be carried off this repository — walks document → decision → requirement → obligation →
  check with the order justified at each step and the rejected alternatives kept. One rule
  (the shift-amount rule) is followed end to end by name, and its two non-mechanical steps are
  flagged inside the walk. A closing section names the four steps no gate can take (choosing
  the publication, classing the fact, judging the authority, classifying the disagreement) —
  everything else is declared mechanical, which is the method's discipline stated as a rule.
  The mdBook carries it verbatim under The contracts, the way the book handles every source
  document. The carryability probe: outside the worked example, the body references no tool,
  path, or id this project owns.
  Design (recorded before code, `2026-09-27`): the deliverable is one self-contained document,
  `docs/METHOD.md` — the method must be carryable OFF this repository, so it cannot live only in
  the mdBook's narrative or scattered across leaf checklists. The document is written against the
  method this session actually exercised (eleven leaves of it), with the rejected alternatives
  kept, and it names the non-mechanical steps honestly: pinning a source, judging an authority,
  choosing a profile over a reference's default — the steps no gate can take for you.

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
  Status: `done`
  Goal: a gate that refuses model implementation for a profile while a category its declared scope
  requires is `missing`. The rule is the director's; this makes it enforceable rather than
  remembered.
  Acceptance: fired RED against a deliberately uncovered category; `P1-LAB`'s precondition is the
  gate's verdict rather than a judgement call. Composes with `.10`: a category may be covered while
  the definition is still insufficient, and both must pass.

- ID: `MODEL-METHOD.14` — **evaluate re-sourcing the encodings from the primary-document PDF**
  Status: `proposed` (director-scheduled — surfaced `2026-09-29`; no work until scheduled)
  Origin (measured, `MODEL-BOOKS.2`, `2026-09-29`): the pinned unprivileged specification's
  own PDF rendering (`docs.riscv.org` `v20260120`, `_attachments/riscv-unprivileged.pdf`,
  4,580,174 B, sha256 `06bb3c23…d150bc`, 696 pages) carries the instruction-format tables as
  SELECTABLE TEXT — `pdftotext` census `[01]{7}` → 232 lines, vs 0 across all six pinned HTML
  artifacts (`grep -cE '[01]{7}' target/sources/riscv-v20260120/{intro,rv32,rv64}.{html,txt}`).
  The base-formats figure (`imm[31:12]`/`rd`/`opcode`/`U-Type`) and the RV32I opcode map
  (Table 13) extract with bit strings and field names. Today the encodings come from
  RISCV-OPCODES — a second provenance whose ancestry is shared with spike, not sail
  (`docs/models/rv64i-lab-v0/src/gaps.md`, `references.md`); re-sourcing from the primary
  document shrinks that exposure.
  Goal: decide, by measurement, whether `encoding.sexp` (owned by `.8`) can be re-derived from
  the primary document's PDF text layer. Probe one form end to end (extract → parse → compare
  against the current riscv-opcodes-derived entry), estimate the full sweep's cost and
  verifiability, then record adopt/decline as a decision. Two measured qualifications the probe
  must handle: the PDF numbers chapters differently from the pinned HTML (a recorded locator
  mapping is required), and extraction is layout-fragmented (one field per line — parsing is
  engineering with its own verification, not a copy-paste).
  Acceptance: the probe's commands and outputs are recorded either way; if adopt, the re-source
  is its own reviewed leaf with the encoding provenance restated in the dossier and the
  materials bill; if decline, the reason is measured, not assumed.
  Not this leaf: changing any encoding data. This leaf is the evaluation only.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `MODEL-METHOD.14` | `proposed` | the `.2` PDF finding made the encodings' second provenance potentially replaceable by the primary document; the evaluation is real work with its own verification and starts only when the director schedules it |
| — | — | — | leaves `.1`–`.13` done `2026-09-27`: the method, the census, the acquisitions, and the coding gate all land |

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

## Completed-leaf evidence

Archived to [`archive/MODEL-METHOD.md`](archive/MODEL-METHOD.md) — the full, unedited
acceptance checklists and routing evidence for every `done` leaf (`.2`–`.4`, `.7`, `.10`,
`.13`). Split out when this file crossed its per-part ceiling; the ceiling was obeyed,
not raised. The live tree keeps the frontier, the decisions, the open questions and both
logs.

## Acceptance Checklist (leaf MODEL-METHOD.5)

- [x] **REPRODUCE / ISSUE** — the method as it stood: exercised eleven times this session but
  written nowhere a reader could carry it:

  ```
  $ ls docs/METHOD.md 2>&1
  ls: docs/METHOD.md: No such file or directory
  $ grep -rl 'the method' docs/*.md 2>/dev/null | wc -l
  0                                             # no method document anywhere in docs/
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHY: a method that exists only as the history of
  its exercise cannot be learned from — the rejected alternatives die with the session that
  rejected them, and the judgement calls look like mechanics. WHERE: measured, not read —

  ```
  $ git ls-files 'docs/*.md' | xargs grep -l 'no gate can take\|document → decision' 2>/dev/null | wc -l
  0                                             # the spine lived only in leaf checklists
  ```

  Nothing in `docs/` carried the method a reader could take away.

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  ```
  $ grep -c 'shift-amount rule' docs/METHOD.md
  1                                             # one rule followed end to end, by name
  $ grep -A8 'no gate can take' docs/METHOD.md | grep -c '^[0-9]\.\|^[0-9]\.'
  4                                             # the non-mechanical steps, identified as such
  $ make book 2>&1 | tail -1
  INFO HTML book written ...                      # the book carries it verbatim
  $ grep -nE 'scripts/|schema/|\.sexp|rv64i-lab-v0|RECORD-SCHEMA' docs/METHOD.md \
      | grep -vE 'SHAMT' | wc -l
  0                                             # no project-only dependency outside the example
  ```

- [x] **NO REGRESSION** — `make book` builds; sexp 18/0; kernel 50/0; RECORD-SCHEMA 33/0;
  whole gate green after staging.

- `promotion: declined (the framing is the document's own closing section).`

- [x] **LOCKSTEP** — `docs/book/` chapter + SUMMARY row; `MEMORY.md`, `CHANGELOG.md`,
  `DEV_NOTES.md`, `docs/TASK_TREE.md` and this tree — one commit.

## Acceptance Checklist (leaf MODEL-METHOD.6)

- [x] **REPRODUCE / ISSUE** — the director's rule as it stood: prose in the roadmap, nothing
  enforcing it. Census, pre-code:

  ```
  $ git ls-files scripts | grep -c 'scope_coverage'
  0                                             # nothing refused uncovered-scope coding
  $ grep -c 'requires' materials/units.sexp schema/units.sexp
  0                                             # and no unit declared what its scope requires
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHY: "no coding without the source of truth" is
  only as real as the thing that refuses — an intention a gate doesn't carry decays the first
  busy week. WHERE: measured, not read —

  ```
  $ grep -c 'requires' materials/units.sexp schema/units.sexp
  0                                             # no unit could even DECLARE its scope
  $ grep -rl 'scope' scripts/check_doctrines.project.sh | wc -l
  0                                             # and no gate keyed the census to a coding decision
  ```

  The census dispositions existed; the vocabulary to act on them did not.

- [x] **FIX** — the registry gains `(requires …)` (data, zero kernel lines); SCOPE-COVERAGE
  checks required × census: missing or absent refuses by name; a unit with an undeclared
  scope refuses too (code may not start against a scope never declared).

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  ```
  $ bash scripts/check_scope_coverage.sh --self-test
  SCOPE-COVERAGE --self-test: 7 pass / 0 fail
  $ bash scripts/check_scope_coverage.sh
  SCOPE-COVERAGE: ok (1 unit(s) may code — every required category covered)
  $ # fired RED before registration, on a scratch unit whose required category is missing:
  MISSING REQUIRED units.sexp [ghost requires C02]: the census disposition is 'missing' …
  ```

- [x] **NO REGRESSION** — `bash scripts/check_requirements.sh --self-test` 33 pass / 0
  fail + real run green with the registry's new field; `bash scripts/check_extraction.sh
  --self-test` 3 pass / 0 fail + real run green; whole gate green after staging (19
  doctrines, 227 arms).

- `promotion: declined (the "coverage says OWNED, extraction says EXTRACTABLE" composition
  rule is stated in the gate's header and this leaf).`

- [x] **LOCKSTEP** — `scripts/check_doctrines.project.sh` + both mirrors in the registering
  commit; `LIVE_STATUS.md` re-derived; `TOOLBOX.md`; `MEMORY.md`, `CHANGELOG.md`,
  `DEV_NOTES.md`, `docs/TASK_TREE.md` and this tree — one commit.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-27` | `MODEL-METHOD.6` | `--self-test` | `7 pass / 0 fail` — MISSING REQUIRED, UNCOVERED REQUIRED, UNDECLARED SCOPE, NO CENSUS, both GREEN arms, empty-corpus refusal |
| `2026-09-27` | `MODEL-METHOD.6` | RED before registration (scratch unit, required category missing) | `MISSING REQUIRED [ghost requires C02]` |
| `2026-09-27` | `MODEL-METHOD.6` | real run | `ok (1 unit(s) may code)` — rv64i-lab-v0 declares 14 required categories, all covered |
| `2026-09-27` | `MODEL-METHOD.5` | census, pre-code | no method document anywhere in `docs/` |
| `2026-09-27` | `MODEL-METHOD.5` | the acceptance probes | the SHAMT walk present; 4 non-mechanical steps named; book builds; no project-only dependency outside the worked example |
| `2026-09-27` | `MODEL-METHOD.4` | network probes | psABI gh-pages: no PDF (HTML canonical render); ELF gABI: HTTP 200; isa-manual releases carry `riscv-spec.pdf` assets |
| `2026-09-27` | `MODEL-METHOD.4` | the four acquisitions fetched, digested, cached | digests and byte counts in the leaf table; re-hash of the cached copies matches |
| `2026-09-27` | `MODEL-METHOD.4` | content sanity | psABI mentions RISC-V 85×; `__NR_exit` present in the syscall header; `__muldi3 (di_int a, di_int b); // a * b` in the builtins inventory; `%PDF-1.1` magic on the ELF spec |
| `2026-09-27` | `MODEL-METHOD.4` | the PDF question | **YES** — `pdftotext` extracts 1.96 MB of text; the RV32I format-table region yields `funct7 / rs2 / rs1 / funct3` as clean cells |
| `2026-09-27` | `MODEL-METHOD.4` | SRC-02 records | pinned-revision release PDF not located (3 release pages searched); chipdoc route unavailable (`$SEMULITH_CHIPDOC_ROOT` unset); startup contract owned by the harness contract already |
| `2026-09-27` | `MODEL-METHOD.3` | census sweep against the cached snapshot | all 8 covered categories' subjects found in the pinned pages; the excluded chapters (a/d/f/q/v-st-ext, rvwmo, counters, zicsr, zifencei) present in the same snapshot |
| `2026-09-27` | `MODEL-METHOD.3` | revised census | 24 rows: 10 covered, 4 partial, 6 missing (each naming its closer), 3 deferred-to-board, 1 out-of-scope |
| `2026-09-27` | `MODEL-METHOD.3` | RECORD-SCHEMA rule 12 + arm | `33 pass / 0 fail` (was 32); UNRESOLVED MATERIAL fired RED pre-registration |
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
| `MODEL-METHOD.6` | `SEMILITH-MM-0050 (leaf MODEL-METHOD.6): …` | no coding without the source of truth, mechanized; the tree closes 13/13 |
| `MODEL-METHOD.5` | `SEMILITH-MM-0049 (leaf MODEL-METHOD.5): …` | the method, in prose, written to be learned from |
| `MODEL-METHOD.4` | `SEMILITH-MM-0048 (leaf MODEL-METHOD.4): …` | the run-real-code set acquired and digest-pinned; the PDF question answered YES |
| `MODEL-METHOD.3` | `SEMILITH-MM-0047 (leaf MODEL-METHOD.3): …` | the census swept the snapshot; missing now means excluded, with closers named |
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
