# MODEL-COMPOSE: assemble proven small models into large ones

## Metadata

- Tree ID: `MODEL-COMPOSE`
- Status: `active`
- Roadmap lane: cross-cutting; the mechanism by which breadth is reached without lowering the bar
- Gate: contributes the composition verdict a composed unit must pass
- Depends on: `decision_composition-model`, `MODEL-METHOD.8` (the definition must be owned before
  it can be composed)
- Unlocks: every unit above a single processor — MCUs, boards, SoCs, computers
- Created: `2026-09-14`
- Owner: repo-local workflow

## Goal

Make canonical definitions **compose**, so that complexity is reached by assembling small proven
models rather than by writing large unproven ones. Two operators, one port mechanism, four
conditions for a composition to be a functional model — all from
[`decision_composition-model`](../decisions/decision_composition-model.md).

⭐ This is the answer to a tension I originally mis-diagnosed. I proposed tiering models into gated
and ungated to buy breadth; the director corrected it to composition. Breadth by **reuse of
evidence**, never by absence of it.

## Non-Goals

- Not a general component framework. The composition vocabulary earns each operator from a real
  case; an operator with no unit needing it is not added.
- Not semantic composition first. Encoding union is **decidable** and semantic union is not, so the
  decidable half is built first and the hard half is approached with refinement points declared
  explicitly (`.6`).
- Not a relaxation of any gate. A composed unit inherits its parts' evidence **and owes its own**.

## Acceptance Criteria

1. A composition is accepted or **rejected with a specific reason** — never accepted with a warning.
2. Encoding-space disjointness is checked mechanically and fired RED on a real collision.
3. Every sub-unit assumption is discharged by a named guarantee, or the composition is rejected.
4. A composition may be **partial** (unbound slots) and still checkable — that is what makes
   top-down design possible — but partial is declared, never inferred from silence.
5. Compositions nest: a composition is itself a unit with the same record shape.

## Task Tree

- ID: `MODEL-COMPOSE.1` — **encoding-space disjointness, proven on a real pair**
  Status: `done`
  Goal: the decidable check — two fragments may not claim the same encoding bits. Demonstrate by
  composing the `M` extension onto this project's `RV64I` base and proving the union is
  conflict-free, then firing the check RED on a deliberate collision.
  Acceptance: the check decides, not estimates; fired RED on a genuine overlap; the composed
  encoding set is larger than either part and provably disjoint.
  Verification: 52 + 8 + 5 = 65 instructions compose with no collision; 37 real collisions detected and rejected in the control.
  Commit: `SEMULITH-MC-0038`

- ID: `MODEL-COMPOSE.2` — **the fragment: what composes, and what a unit names**
  Status: `done`
  Goal: a fragment is a complete, independently checkable description of one thing; a unit names
  the fragments it unions. Give both a form in the canonical definition.
  Acceptance: `rv64i-lab-v0` re-expressed as base + (empty) extension list without changing a
  single observable; a fragment with a hidden dependency is refused.
  Verification: all four guest ELF digests byte-identical after the refactor; two refusals fired; the M fragment pinned.
  Commit: `SEMULITH-MC-0039`

- ID: `MODEL-COMPOSE.3` — **assumption / guarantee discharge**
  Status: `done`
  Goal: the inter-unit operator, and the mechanical form of `docs/CPU_ENVIRONMENT.md` §5. Every
  sub-unit `environment-assumption` is matched by a named guarantee or the composition is rejected.
  Acceptance: fired RED by removing one guarantee; the 8 assumptions `rv64i-lab-v0` already carries
  are the first real input.
  Result: met, `2026-09-27`. `scripts/discharge_assumptions.py` decides discharge over the
  `merge_units(…)` union: the profile alone discharges 8/8 with every edge printed
  (`OB-ENV-RESET -> 'OB-ENTRY-STATE' (cpu-guarantee)`, and kin); a unit split carrying only
  `OB-ENTRY-STATE` discharges `OB-ENV-RESET` across the boundary; removing the guarantee
  rejects the composition naming it (`DANGLING DEP` + `UNDEFINED OBLIGATION` — both halves of
  the corpus catch it). Discharge-specific refusals proven on synthetic fixtures: a demand
  pointing at a demand (`UNDISCHARGED CHAIN`), an assumption naming no guarantee
  (`UNDISCHARGEABLE`), and the complement — an unclaimed guarantee is not an error.
  Design (recorded before code, `2026-09-27`), read against the contract, the schema and `.5`'s
  measured corpus facts:
  - ⭐ **The discharge edge already exists in the corpus — the operator makes it a verdict, not a
    hope.** `SOT-FORMAT.5`'s census measured it: every `environment-assumption`'s `dependencies`
    point at `cpu-guarantee` obligations (`OB-ENV-RESET` → `OB-ENTRY-STATE`, and kin). The rule,
    mechanical: **an assumption is discharged when every dependency resolves in the union to an
    obligation whose direction is a guarantee** — the rule keys on *not* `environment-assumption`,
    so the day the vocabulary earns a third value (a device's guarantee) it is accepted by
    construction. That vocabulary extension is deliberately NOT this leaf: it is a `(values …)`
    data change the day a real device unit exists, named here so nobody discovers the boundary
    as a surprise.
  - **Refusals, each named.** A dependency that resolves to nothing is already refused by
    `merge_units`' closure (`DANGLING DEP`) — removing one guarantee fires RED there, naming the
    assumption and the missing guarantee; that IS the acceptance's fired-RED, and where it lands
    is recorded honestly rather than re-implemented. The discharge-specific refusals: a dependency
    landing on another `environment-assumption` is an undischarged chain (a demand pointing at a
    demand, not a supply); an assumption carrying NO dependency names no guarantee and is
    undischargeable by construction. Both refused by name.
  - **The deliverable is `scripts/discharge_assumptions.py`** — a checker consuming
    `merge_units(…)` (never re-implementing the union): it prints each discharge edge
    (`OB-ENV-RESET -> OB-ENTRY-STATE (cpu-guarantee)`) and either
    `all N environment-assumption(s) discharged by named guarantee(s) — the composition holds`
    or a refusal. Importable, so the engine and future board composition read the same verdict.
  - Real-corpus proof plan: (1) `rv64i-lab-v0` alone discharges 8/8 — the lab discharges its
    CPU's own assumptions today; (2) cross-unit — a scratch unit split carrying only
    `OB-ENTRY-STATE` discharges the rest's `OB-ENV-RESET` across the boundary; (3) the
    acceptance's RED — one guarantee removed → the composition is rejected naming it; (4) the
    discharge-specific REDs — a chain and a zero-dependency assumption, synthetic.

- ID: `MODEL-COMPOSE.4` — **slots: top-down composition with holes**
  Status: `done`
  Goal: a composition may declare an unbound slot with its requirements, so shape, address space
  and unmet requirements are checkable **before the parts exist**.
  Acceptance: a partial composition passes the checks that apply and is reported partial; a
  composition claiming completeness with an unbound slot is rejected.
  Result: met, `2026-09-27`. The vocabulary is data — `compose` gained `(status complete|partial)`
  and `(slot (id …) (requires …))` in `schema/encoding.sexp`, zero kernel lines. The composition
  checker now consumes the ONE shared resolver (`riscv_asm.resolve_composition`, extracted), and
  `UNIT-COMPOSITION` (15th project doctrine, `scripts/check_unit_composition.sh`) decides every
  tracked unit: the profile composes 52/52 today; a real-shaped partial unit reports
  `PARTIAL — 1 slot(s) unbound: clint requires riscv/timer`; the completeness claim with a hole
  fires RED. The substrate defects that would have made the verdict a claim without legs — the
  unit-level union undecided since `.2`, the checker not schema-validating its input — are closed
  and gated.
  Design (recorded before code, `2026-09-27`), grounded in three measured facts read from the
  code first:
  - ⭐ **Two substrate defects, probe-measured, own this leaf's shape.** (1) Since `MODEL-COMPOSE.2`
    moved the 52 instructions into fragments, `check_encoding_disjoint.py` can no longer consume a
    unit's `encoding.sexp` — probe: `check_encoding_disjoint.py profiles/rv64i-lab-v0/encoding.sexp`
    → `REFUSED … yielded no instructions`, rc=2, and no gate invokes the tool on the unit's
    fragments, so **nothing today decides the unit's composed encoding space**; `.1`'s capability
    silently regressed the day `.2` landed. (2) The tool never schema-validates its input — probe:
    a `compose` with an undeclared `(widget "x")` field passes it silently (the schema layer
    refuses the same file by name). Slots live in the compose form, so both defects are this
    leaf's substrate: a slot verdict on a document nobody validates, over a union nobody decided,
    would be a claim without legs.
  - **The vocabulary is data (zero kernel lines).** `compose` gains an optional
    `(status SYMBOL {complete|partial})` and a repeated `(slot …)` child; `slot` is one
    `(id SYMBOL)` and `(requires STRING…)` — the fragment ids the bound unit must provide.
    `partial` is DECLARED, never inferred from silence: a composition with slots but no
    `(status partial)` is claiming completeness while unbound → refused; `(status partial)` with
    no slots declares a hole that isn't there → refused. A slot's `requires` are NOT
    existence-checked — requiring a part that does not exist yet is the point of a slot.
  - **One resolver, two consumers.** The compose→fragments resolution is extracted from
    `riscv_asm.load_canonical_encoding` into `resolve_composition(…)`; the assembler and
    `check_encoding_disjoint.py` both consume it — a second hand-written resolver is how the
    `.2` regression happened. The checker, given a unit's `encoding.sexp`: schema-validates it
    against `schema/encoding.sexp` (the widget gap, closed), resolves and unions the bound
    parts, decides the encoding verdict as today, then applies the slot rules and prints
    `PARTIAL — N slot(s) unbound: <id> requires …` when declared.
  - **The verdict must run somewhere (§15/§16).** Restored capability that no gate invokes is
    the defect restated, so the leaf registers `UNIT-COMPOSITION` (15th project doctrine,
    `scripts/check_unit_composition.sh`): every tracked unit's composition is schema-conformant,
    its fragments resolve with dependencies met, its union is collision-free, and partial is
    declared, never inferred. Fired RED on all three refusal shapes before registration.
  - **No-regression proof is the `.2` precedent**: the assembler's resolution refactor must not
    move a single observable — all four guest ELF digests byte-identical and `run_smoke` ok.

- ID: `MODEL-COMPOSE.5` — **nesting: a composition is a unit**
  Status: `pending`
  Goal: `computer → board → soc → {cpu, device}` uses one record shape at every level.
  Acceptance: a two-level composition is checked by the same code as a one-level one.

- ID: `MODEL-COMPOSE.6` — **semantic refinement points**
  Status: `done`
  Goal: the hard axis. An extension can change base behaviour — adding CSRs changes trap handling;
  adding `C` changes `IALIGN` and therefore which branch targets fault. A fragment must **declare**
  that it modifies a base behaviour; a silent override is a defect.
  Acceptance: a fragment that redefines a base semantic without declaring it is refused.

  Result: met, `2026-09-27`. The vocabulary is data — `schema/semantics.sexp` gains
  `(refines (insn "name"))`, the house list form, zero kernel lines. `check_semantics.py
  --compose` decides the refinement rule over schema-validated files: the acceptance's RED
  fired on a real-shaped composition (a fake extension redefining `add` with no declaration →
  `SILENT REDEFINITION`, rc=1), a declared refinement is accepted and reported, and both lies
  (declaration without override, refining nothing) are refused by name. The third orphan of the
  family `.4` closed for encodings is wired: `SEMANTICS` (16th project doctrine,
  `scripts/check_semantics_corpus.sh`) now runs the per-fragment checks and the 52/52 citation
  resolution in every gate — the semantics corpus, the roadmap's execution authority, is
  continuously healthy for the first time. The IALIGN-class (global-behaviour) refinement
  stays named-and-deferred: per-instruction is the granularity the corpus writes.
  Design (recorded before code, `2026-09-27`), the corpus and the gate set read first:
  - ⭐ **The third orphan of the family `.4` closed for encodings.** Probe: `check_semantics.py`
    and `check_citations.py` are invoked by NOTHING in the gate set — the semantics corpus, which
    `ROADMAP.md` names the execution authority ("the semantics data executes directly"), is
    well-formed, complete and cited only when someone runs the tools by hand. Like the unit-level
    union, a capability without a re-runner regresses silently. This leaf owns the wiring with
    the refinement rule as the gate's first new discriminating arm.
  - **The vocabulary is data, and it lives on the authored side.** Fragments are GENERATED
    (encoding tables) and semantics deliberately live apart in hand-written `.sem.sexp` files —
    so the refinement declaration belongs to the semantics grammar, not the fragment:
    `schema/semantics.sexp` gains `(refines "insn-name")`, a child of the `(semantics …)` root
    naming each base instruction whose semantics this file redefines. Zero kernel lines.
  - **The rule, mechanical.** In composition order (base first): a name defined in file *j* that
    is also defined in any earlier file is an override, legal **iff** file *j* declares
    `(refines "name")`. Refusals, each named: `SILENT REDEFINITION` (the acceptance's fired RED);
    `REFINES WITHOUT OVERRIDE` (a declaration naming nothing the file defines — a lie);
    `REFINES NOTHING` (a declaration naming nothing any earlier file defines — also a lie);
    duplicate definitions within one file, refused as before. Scope, stated: the rule is
    per-instruction, the granularity the corpus actually writes; the IALIGN-class refinement (a
    new construct changing GLOBAL behaviour rather than one instruction's rule) is a future
    construct the day a real file needs it — the vocabulary earns operators from cases, not
    anticipation.
  - **The deliverables**: `check_semantics.py --compose <base.sem> <ext.sem>…` deciding the
    refinement rule over schema-validated files; and `SEMANTICS` (16th project doctrine,
    `scripts/check_semantics_corpus.sh`) wiring the corpus's health into the gate set:
    schema-conformance, per-fragment coverage/citations, the refinement rule per unit, and
    citation resolution through the manifest-verified offline cache — with a NAMED SKIP (not a
    pass, not a fail) when the cache is absent, because a check that cannot judge must never
    report green over an absence (its own header says which route judged).

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `MODEL-COMPOSE.5` | `pending` | nesting — a composition is itself a unit; one record shape at every level, decided by the same code |

## Decisions

- `2026-09-14`: **encodings before semantics.** Encoding union is decidable; semantic union is not.
  Building the decidable half first buys a real, mechanical composition check immediately, and
  makes the hard half approachable with explicit refinement points rather than hope.
- `2026-09-14`: a rejected composition names **which** rule it failed and **where**. A composition
  checker that answers only yes or no cannot be acted on, and one that warns will be ignored.

## Open Questions

- Does a board need an operator beyond union and discharge — for example address-space assignment
  as its own operator rather than a guarantee? Deferred to `.3`/`.4`, where a real board shape will
  answer it better than speculation. ⛔ The vocabulary earns operators from cases, not from
  anticipation.

## Blockers

- None.

## Acceptance Checklist (current leaf — `MODEL-COMPOSE.2`)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHERE: `profiles/rv64i-lab-v0/encoding.sexp` carried
  all 52 instructions **inside the unit**. WHY that fails the composition model: a base ISA is
  shared by every profile that uses it, so a second RV64 profile would have copied 52 instructions
  that then had to be kept equal — the exact duplication `decision_canonical-definition-input`'s
  no-duplicated-fact rule exists to prevent, in the one place most tempting to copy. Census:

  ```
  $ grep -c '^  (insn ' profiles/rv64i-lab-v0/encoding.sexp
  52                       # owned by ONE unit, reusable by none
  $ git ls-files definitions | wc -l
  0
  ```

- [x] **ADDRESSED (verified)** — fragments have a form and a home. `definitions/riscv/rv64i.sexp`
  (52 instructions, the operand fields and scattered-immediate layouts a base owes its extensions)
  and `definitions/riscv/m.sexp` (13 instructions, `(requires "riscv/rv64i")`). The unit now
  **names** what it composes and carries no instruction of its own:

  ```
  (compose (base "riscv/rv64i") (extensions))
  ```

  Before → after on the census that defined the gap:

  ```
  $ grep -c '^  (insn ' profiles/rv64i-lab-v0/encoding.sexp
  0                                    # was 52 — the unit owns no instruction
  $ grep -ch '^  (insn ' definitions/riscv/*.sexp | paste -sd+ - | bc
  65                                   # 52 base + 13 M, reusable by any unit
  $ git ls-files definitions | wc -l
  2                                    # was 0
  ```

  ⭐ **The acceptance test is that nothing observable moved.** A refactor of the source of truth
  must not perturb the evidence, so all four guest programs were re-assembled and re-run:
  `elf sha256` → `59b0029bcf33fa36`, `e9cd138de6562aca`, `05551a3a22afcbbc`, `aadc2c618c84ad78` —
  **byte-identical to before the split**, across two reference models, all reproducing.
  The `M` fragment used in `.1` is now **pinned** (`rv_m`, `rv64_m` digests in `references.toml`):
  a fragment composed from an unpinned source is a model built on something nobody can re-derive.

- [x] **NO REGRESSION** — leg 2. Two refusals, both fired:
  - composing `riscv/m` **without** its base → `fragment 'riscv/m' requires 'riscv/rv64i', which
    this composition does not provide before it. A fragment with an unmet dependency composes by
    luck, not by construction.`
  - composing a fragment that does not exist → `composes 'riscv/nope', but
    definitions/riscv/nope.sexp does not exist`.

  The fragments are re-derived against the pinned tables by `fetch_references.sh`, fired RED on a
  one-nibble `funct3` edit to `mul`: `DIFFERS definitions/ no longer matches what the pinned tables
  generate`, with the line quoted. Restored to `MATCH`. `fetch_references.sh --verify-only` → all
  `MATCH`; whole gate `=== all doctrines green ===`; `make check` →
  `test result: ok. 1 passed; 0 failed`; `scripts/run_smoke.py` → `ok`.
  ⭐ The tracked generator reproduces the fragments **byte-for-byte** — `git diff --stat
  definitions/` after regeneration is empty — so the generator is the owner and the files are not
  a hand-maintained copy of its output.

- [x] **FIX** — `definitions/` created and **registered in the routes registry in the same commit**
  (a new tracked family that nothing governs is how pressure escapes); `scripts/gen_fragments.py`
  replacing the single-profile generator; `riscv_asm.py` resolving a composition and checking
  declared dependencies; `rv_m`/`rv64_m` pinned.

- `promotion: declined (the rule — a source-of-truth refactor must not move the evidence — is demonstrated by this leaf's own digest row and stated in encoding.sexp's header, which anyone composing a second profile reads first)`

- [x] **LOCKSTEP** — leg 3: fragments are re-derived on demand, compositions are checked before
  adoption, and the unit owns no instruction. `TOOLBOX.md`, `MEMORY.md`, `LIVE_STATUS.md`,
  `CHANGELOG.md`, `DEV_NOTES.md` updated in this commit.
  ⚠️ Note on the rename: three references to the old generator name survive in `CHANGELOG.md` and
  in `MODEL-METHOD.8`'s completed checklist. They are **left alone deliberately** — both are
  historical records, true when written, and rewriting them to match today is exactly what the
  `append_history` lifecycle exists to prevent.

### `MODEL-COMPOSE.1` — encoding-space disjointness

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHERE: nothing in this repository could decide whether
  two definition fragments compose. WHY it mattered enough to build first: the project's route to
  breadth is now *assembling proven small models*, and an assembly step with no verdict is an
  assembly step that fails silently at the worst moment. Census before this leaf:

  ```
  $ git ls-files scripts | grep -c -E 'compos|disjoint'
  0
  $ grep -c '^extensions = ' profiles/rv64i-lab-v0/profile.toml
  1                                    # the seam exists, and is empty
  ```

  ⭐ Grounding, measured rather than assumed: both pinned references already compose their
  definitions from fragments — `riscv-opcodes` ships **111** extension files, `sail-riscv` **34**
  extension directories and **59** files defining instruction encodings. The idea was never the
  missing part; a *check* was.

- [x] **ADDRESSED (verified)** — encoding union is decidable, so the check decides. Two
  instructions collide exactly when `(value_a ^ value_b) & mask_a & mask_b == 0`, and the search is
  exhaustive rather than sampled, because a sampled answer would not be a decision.

  ```
  $ scripts/check_encoding_disjoint.py profiles/rv64i-lab-v0/encoding.sexp \
        target/refs/riscv-opcodes/rv_m target/refs/riscv-opcodes/rv64_m
    fragment encoding.sexp     52 instruction(s)
    fragment rv_m               8 instruction(s)
    fragment rv64_m             5 instruction(s)
    composed set: 65 instruction(s) from 3 fragment(s)
    no collisions, no duplicate names — the fragments COMPOSE.
  ```

  **52 + 8 + 5 = 65, provably disjoint.** The project's own owned RV64I base composed with a
  fragment it had never seen, and the answer is a verdict rather than an impression.

- [x] **NO REGRESSION** — leg 2, and the control is a genuine failure rather than a synthetic one.
  Composing the owned encodings with `rv_i` — a fragment they **already contain** — is a realistic
  mistake, and it is caught with the reason and the overlapping mask:

  ```
    COLLISIONS: 37
      add (encoding.sexp) overlaps add (rv_i)    mask=0xfe00707f
      addi (encoding.sexp) overlaps addi (rv_i)  mask=0x0000707f
      …
    REJECTED — these fragments do not compose. A decoder cannot be generated from a
    set in which one word matches two instructions.
  ```

  `rc=1`, 37 collisions named. ⭐ A second refusal fired without being planned: an attempt to fetch
  a non-existent `rv32_i` produced an empty file, and the checker answered
  `REFUSED: … yielded no instructions — an empty fragment is not a valid one` rather than
  reporting "no collisions" over nothing. That is the same refusal discipline the schema validator
  and the S-expression reader carry, and it mattered on its first day.
  Whole gate `=== all doctrines green ===`; `make check` → `test result: ok. 1 passed; 0 failed`;
  `scripts/run_smoke.py` → `ok`, so the evidence path is undisturbed.

- [x] **FIX** — `scripts/check_encoding_disjoint.py`, reading either an owned `encoding.sexp` or a
  `riscv-opcodes` table, so a fragment can be checked before it is adopted.

- `promotion: declined (the lesson — breadth by composing proven parts rather than gating fewer — IS decision_composition-model, which a reader meets before acting; the decidability argument is stated in check_encoding_disjoint.py's docstring where anyone extending it will meet it)`

- [x] **LOCKSTEP** — leg 3: `TOOLBOX.md` gains the instrument; `MEMORY.md`, `LIVE_STATUS.md`,
  `CHANGELOG.md` and `DEV_NOTES.md` updated in this commit.
  ⛔ **What this leaf does NOT claim, stated because the result invites the stronger reading.**
  There is **no RV64IM profile**. The `M` fragment is not pinned, no semantics were composed, and
  nothing was added to `rv64i-lab-v0`. What was demonstrated is that the *decoder* composes — one
  word never matches two instructions across the union. Whether the *meanings* compose is not
  decidable in general and is `.6`'s problem: an extension can change a base instruction's
  behaviour, and a silent override is a defect rather than a composition.

## Acceptance Checklist (leaf MODEL-COMPOSE.3)

- [x] **REPRODUCE / ISSUE** — §5's gate as it stood: a sentence in a document, nothing deciding
  it. Census before this leaf:

  ```
  $ git ls-files scripts | grep -c 'discharge'
  0                                             # "identify the guarantee or reject": no owner
  $ grep -n 'environment-assumption' profiles/rv64i-lab-v0/contract-obligations.sexp | wc -l
  8                                             # the first real input, checked by nothing
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHY: a conditional composition claim ("the CPU is
  validated under explicit environment assumptions") is only as strong as the demonstration
  that the assumptions hold, and the demonstration lived only in prose. WHERE: measured on the
  corpus, not assumed — the discharge edge already exists as obligation `dependencies`, every
  one of the 8 assumptions' deps pointing at `cpu-guarantee` obligations (`SOT-FORMAT.5`'s
  census), so the operator's job was to make that edge a verdict, not to invent it:

  ```
  $ python3 - <<'PY'
  > obs = records_sexp.load("profiles/rv64i-lab-v0/contract-obligations.sexp")
  > env = [o for o in obs if o["direction"] == "environment-assumption"]
  > print(all(d in {o["id"] for o in obs if o["direction"] == "cpu-guarantee"}
  >           for o in env for d in o["dependencies"]))     # -> True
  ```

- [x] **FIX** — `scripts/discharge_assumptions.py`: an assumption is discharged when every
  dependency resolves in the `merge_units(…)` union to an obligation whose direction is a
  guarantee (the rule keys on "not environment-assumption", so a future device-guarantee value
  is accepted by construction); refusals: `UNDISCHARGED CHAIN` (demand → demand),
  `UNDISCHARGEABLE` (no dependency names a guarantee). The union's own closure owns the
  missing-guarantee case — removing one guarantee fires there, and where the RED lands is
  recorded honestly rather than re-implemented.

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  ```
  $ python3 scripts/discharge_assumptions.py --self-test
  discharge_assumptions --self-test: 6 pass / 0 fail
  $ python3 scripts/discharge_assumptions.py profiles/rv64i-lab-v0
  … 8 edges printed (OB-ENV-RESET -> 'OB-ENTRY-STATE' (cpu-guarantee), and kin) …
  all 8 environment-assumption(s) discharged by named guarantee(s) — the composition holds
  $ # cross-unit: the profile minus OB-ENTRY-STATE + a unit carrying only that guarantee
  $ python3 scripts/discharge_assumptions.py target/doctrine_scratch/mc3/cpu target/doctrine_scratch/mc3/reset-harness
  all 8 environment-assumption(s) discharged … — the composition holds
  $ # the acceptance's RED — the guarantee removed entirely:
  $ python3 scripts/discharge_assumptions.py target/doctrine_scratch/mc3/noreset
  DANGLING DEP obligation 'OB-ENV-RESET' … depends on 'OB-ENTRY-STATE', which no unit provides
  UNDEFINED OBLIGATION requirement 'REQ-D-ENTRY-STATE' … names 'OB-ENTRY-STATE', …   rc=1
  ```

- [x] **NO REGRESSION** — `scripts/merge_records.py --self-test` 18 pass / 0 fail;
  `scripts/discharge_assumptions.py --self-test` 6 pass / 0 fail;
  `scripts/check_source_format.sh --self-test` 7 pass / 0 fail; sexp 18 pass / 0 fail; kernel
  50/0; RECORD-SCHEMA 23/0; semantics 52/52; citations 52/52; materials 20/0; smoke ok;
  readers 28/28; whole gate green after staging.

- `promotion: declined (the rule — discharge keys on "not an assumption", so new guarantee
  directions are accepted by construction — is stated in the tool's docstring and this leaf,
  where anyone extending the direction vocabulary meets it).`

- [x] **LOCKSTEP** — `TOOLBOX.md` gains the instrument; `MEMORY.md`, `CHANGELOG.md`,
  `DEV_NOTES.md`, `docs/TASK_TREE.md` and this tree — one commit.

## Acceptance Checklist (leaf MODEL-COMPOSE.4)

- [x] **REPRODUCE / ISSUE** — the two substrate defects, probe-measured before any code:

  ```
  $ python3 scripts/check_encoding_disjoint.py profiles/rv64i-lab-v0/encoding.sexp
  REFUSED … yielded no instructions — an empty fragment is not a valid one      rc=2
  $ # since MODEL-COMPOSE.2 moved the instructions into fragments, the unit-level union
  $ # has no decider — and nothing invokes the tool on the unit's fragments:
  $ git ls-files scripts .github .githooks | grep check_encoding_disjoint
  scripts/check_encoding_disjoint.py        # referenced by nothing that runs
  $ # and the tool never schema-validates its input:
  $ # a compose with an undeclared (widget "x") passes it silently
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHY: a verdict that runs on documents nobody
  validates, over a union nobody decided, is a claim without legs — and a capability
  (`.1`'s unit-level union) can regress silently when a refactor (`.2`) changes what the
  checker reads while nothing re-runs it. WHERE: `check_encoding_disjoint.py` read
  `insn` forms only; `riscv_asm.py` held the compose→fragments resolution inline, unshared.
  Two more latent bugs of the same family surfaced in the resolver itself while testing —
  `children(…, "extensions")[0]` and `children(…, "requires")[0]` indexed a first child the
  0-or-more grammar does not guarantee (absence is schema-legal; the corpus always writes the
  markers, so both IndexErrors were live but unfired). Fixed in the extraction, arms proving
  the absent-marker paths.

  ```
  $ grep -n 'children(comp\[0\], "extensions")\[0\]\|children(frag, "requires")\[0\]' scripts/riscv_asm.py
  (no output)                                     # both unfired IndexErrors, closed
  ```

- [x] **FIX** — data first: `schema/encoding.sexp` gains `(status …)` and `(slot …)`, zero
  kernel lines. Then one resolver: `riscv_asm.resolve_composition(…)` extracted and consumed by
  the assembler and the checker alike. Then the checker: schema-validates the composition
  document AND each resolved fragment against the schema layer before unioning; applies the
  slot rules (partial is declared, never inferred — both directions); reports
  `PARTIAL — N slot(s) unbound: <id> requires …` with the union verdict standing. Then the
  wiring: `UNIT-COMPOSITION` registered as the 15th project doctrine, fired RED before
  registration (real corpus + one undeclared slot → `claiming completeness while a hole is
  open`).

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  ```
  $ python3 scripts/check_encoding_disjoint.py --self-test
  check_encoding_disjoint --self-test: 8 pass / 0 fail
  $ bash scripts/check_unit_composition.sh --self-test
  UNIT-COMPOSITION --self-test: 8 pass / 0 fail
  $ bash scripts/check_unit_composition.sh
  UNIT-COMPOSITION: ok (1 unit composition(s) decided)
  $ python3 scripts/check_encoding_disjoint.py profiles/rv64i-lab-v0/encoding.sexp
  composed set: 52 instruction(s) … the fragments COMPOSE.              # the union, restored
  $ python3 scripts/check_encoding_disjoint.py target/doctrine_scratch/mc4partial/profiles/board/encoding.sexp
  … the fragments COMPOSE. … PARTIAL — 1 slot(s) unbound:
    clint requires riscv/timer                                            rc=0
  ```

- [x] **NO REGRESSION** — the `.2` precedent as proof: the assembler's resolution is refactored,
  not rewritten — `scripts/run_smoke.py` ok, every guest matches its expectations and reproduces;
  `scripts/merge_records.py --self-test` 18 pass / 0 fail;
  `scripts/discharge_assumptions.py --self-test` 6 pass / 0 fail; sexp 18 pass / 0 fail; kernel
  50 pass / 0 fail; RECORD-SCHEMA 23 pass / 0 fail; semantics 52/52; citations 52/52; materials
  20/0; readers 28/28; whole gate green after staging.

- `promotion: declined (the "capability without a re-runner regresses silently" lesson is
  demonstrated by this leaf's own census and stated in the gate's header, where anyone
  restoring a capability will meet it).`

- [x] **LOCKSTEP** — `scripts/check_doctrines.project.sh` + both mirrors
  (`DOCTRINE_ENFORCEMENT.md`, the mdBook doctrines chapter) in the registering commit;
  `LIVE_STATUS.md` re-derived (15 doctrines, 192 arms); `TOOLBOX.md` rows; `MEMORY.md`,
  `CHANGELOG.md`, `DEV_NOTES.md`, `docs/TASK_TREE.md` and this tree — one commit.

## Acceptance Checklist (leaf MODEL-COMPOSE.6)

- [x] **REPRODUCE / ISSUE** — the hard axis as it stood: §-prose in `docs/CPU_ENVIRONMENT.md`'s
  neighbourhood and per-fragment checks that nothing ran. Census before this leaf:

  ```
  $ grep -rn 'check_semantics.py\|check_citations.py' scripts/check_doctrines.project.sh \
        scripts/check_doctrines.sh .githooks/ .github/ 2>/dev/null
  (no output)                        # the execution authority's corpus: no re-runner
  $ grep -c 'refines' schema/semantics.sexp
  0                                  # the refinement vocabulary: nothing to declare with
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHY: a silent semantic override is the worst
  composition defect available — every fragment alone is well-formed, so the lie surfaces only
  in the union, exactly where nobody was looking. WHERE: measured, not read —

  ```
  $ grep -c 'refines' schema/semantics.sexp
  0                                             # the refinement edge had no vocabulary at all
  $ grep -rln 'check_semantics.py' scripts/check_doctrines.project.sh scripts/run_smoke.py
  (no output)                                   # the corpus's judges: invoked by nothing
  ```

  Both halves had to be true for the defect to live: no vocabulary to declare with, and no
  re-runner to catch the silence.

- [x] **FIX** — data first (`refines` in `schema/semantics.sexp`); then `check_semantics.py
  --compose` (schema-validate each file, then the rule: an override is legal iff declared;
  arity still bites without an encoding); then `SEMANTICS`, the 16th doctrine, wiring the
  corpus's health — pairs, refinement rule per unit, and offline citation resolution with a
  NAMED SKIP when the cache cannot judge (never a green over an absence).

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  ```
  $ python3 scripts/check_semantics.py --self-test
  check_semantics --self-test: 8 pass / 0 fail
  $ bash scripts/check_semantics_corpus.sh --self-test
  SEMANTICS --self-test: 7 pass / 0 fail
  $ bash scripts/check_semantics_corpus.sh
  SEMANTICS: ok (3 check(s) — pairs, refinement rule, citations)      # 52/52 inside the gate
  $ # the acceptance's RED, on a real-shaped composition (fake extension redefines add):
  fake.sem.sexp [add]: SILENT REDEFINITION — 'add' is already defined in rv64i.sem.sexp,
  and this file declares no (refines (insn "add")). …                    rc=1
  ```

- [x] **NO REGRESSION** — per-fragment mode byte-stable on the real corpus (52 of 52, same
  verdict line); `scripts/check_semantics.py --self-test` 8 pass / 0 fail;
  `scripts/check_semantics_corpus.sh --self-test` 7 pass / 0 fail; sexp 18 pass / 0 fail;
  kernel 50 pass / 0 fail; RECORD-SCHEMA 23 pass / 0 fail; UNIT-COMPOSITION 8 pass / 0 fail;
  merge 18 pass / 0 fail; discharge 6 pass / 0 fail; readers 28/28 (the schema edits re-swept);
  whole gate green after staging.

- `promotion: declined (the "orphaned tool" pattern is now demonstrated three times — .4's
  census, this leaf's census, and the gates that closed them; a card is due if a FOURTH
  instance is found, per the .6 DEV_NOTES threshold).`

- [x] **LOCKSTEP** — `scripts/check_doctrines.project.sh` + both mirrors in the registering
  commit; `LIVE_STATUS.md` re-derived (16 doctrines, 199 arms); `TOOLBOX.md` rows;
  `MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md`, `docs/TASK_TREE.md` and this tree — one commit.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-27` | `MODEL-COMPOSE.6` | tool `--self-test` | `8 pass / 0 fail` — declared refinement accepted, silent/double/lie/arity/schema arms each naming their reason |
| `2026-09-27` | `MODEL-COMPOSE.6` | gate `--self-test` | `7 pass / 0 fail` — pair coverage, citation-less rule, silent override across a unit, empty-corpus refusal, named skip |
| `2026-09-27` | `MODEL-COMPOSE.6` | real run | `ok (3 check(s))` — rv64i 52/52, refinement rule trivial on one fragment, citations 52/52 via the offline cache |
| `2026-09-27` | `MODEL-COMPOSE.6` | RED before registration (real corpus + fake extension redefining `add`) | `SILENT REDEFINITION`, rc=1 |
| `2026-09-27` | `MODEL-COMPOSE.6` | per-fragment mode, before→after | byte-stable verdict on the real corpus |
| `2026-09-27` | `MODEL-COMPOSE.4` | tool + gate `--self-test` | `8/0` + `8/0` — slots both directions, widget, missing/unmet fragment, collision through the resolved path |
| `2026-09-27` | `MODEL-COMPOSE.4` | real run | profile 52/52 composes; scratch partial unit `PARTIAL — 1 slot(s) unbound: clint requires riscv/timer` |
| `2026-09-27` | `MODEL-COMPOSE.4` | RED before registration (real corpus + one undeclared slot) | `claiming completeness while a hole is open` |
| `2026-09-27` | `MODEL-COMPOSE.4` | the substrate probes | unit union undecided since `.2` (REFUSED rc=2); widget passed silently; two unfired resolver IndexErrors, all closed |
| `2026-09-27` | `MODEL-COMPOSE.4` | no-regression | `run_smoke` ok after the resolver extraction — nothing observable moved |
| `2026-09-27` | `MODEL-COMPOSE.3` | `--self-test` | `6 pass / 0 fail` — incl. the acceptance control (guarantee removed → `DANGLING DEP` + `UNDEFINED OBLIGATION`) |
| `2026-09-27` | `MODEL-COMPOSE.3` | real corpus, profile alone | 8/8 discharged, every edge printed (`OB-ENV-RESET -> 'OB-ENTRY-STATE' (cpu-guarantee)`, and kin) |
| `2026-09-27` | `MODEL-COMPOSE.3` | cross-unit (cpu minus `OB-ENTRY-STATE` + a unit carrying only it) | all 8 discharged across the boundary |
| `2026-09-27` | `MODEL-COMPOSE.3` | the acceptance's RED — guarantee removed entirely | rejected naming `OB-ENV-RESET` and `OB-ENTRY-STATE`, rc=1 |
| `2026-09-27` | `MODEL-COMPOSE.3` | corpus census | every one of the 8 assumptions' deps lands on a `cpu-guarantee` — the edge the operator makes a verdict |
| `2026-09-14` | `MODEL-COMPOSE.1` | grounding: do the references compose from fragments? | riscv-opcodes 111 files; sail-riscv 34 dirs / 59 encoding files |
| `2026-09-14` | `MODEL-COMPOSE.1` | compose owned RV64I + `M` fragments | 52 + 8 + 5 = 65, no collision, no duplicate name |
| `2026-09-14` | `MODEL-COMPOSE.1` | control: compose with a fragment already contained | 37 collisions named with masks, `rc=1`, REJECTED |
| `2026-09-14` | `MODEL-COMPOSE.1` | unplanned refusal: an empty fragment | `REFUSED … an empty fragment is not a valid one` |
| `2026-09-14` | `MODEL-COMPOSE.2` | all four guest ELF digests after the refactor | byte-identical to before; 2 models still agree |
| `2026-09-14` | `MODEL-COMPOSE.2` | compose an extension without its required base | `REFUSED … requires 'riscv/rv64i'` |
| `2026-09-14` | `MODEL-COMPOSE.2` | compose a fragment that does not exist | `REFUSED … does not exist` |
| `2026-09-14` | `MODEL-COMPOSE.2` | fragment re-derivation fired RED on a `funct3` edit | `DIFFERS definitions/ …` — restored |
| `2026-09-14` | `MODEL-COMPOSE.2` | generator reproduces the fragments | `git diff --stat definitions/` empty |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `MODEL-COMPOSE.6` | `SEMILITH-MC-0042 (leaf MODEL-COMPOSE.6): …` | refinement points declared, the semantics corpus gated; 16th doctrine |
| `MODEL-COMPOSE.4` | `SEMILITH-MC-0041 (leaf MODEL-COMPOSE.4): …` | slots declared, the unit union decided and gated; 15th doctrine |
| `MODEL-COMPOSE.3` | `SEMILITH-MC-0040 (leaf MODEL-COMPOSE.3): …` | assumption/guarantee discharge decides over the merged union; 8/8 on the real corpus; fired RED by removing one guarantee |
| `MODEL-COMPOSE.2` | `SEMULITH-MC-0039 (leaf MODEL-COMPOSE.2): fragments get a form and a home` | nothing observable moved; M pinned |
| `MODEL-COMPOSE.1` | `SEMULITH-MC-0038 (leaf MODEL-COMPOSE.1): encoding composition is a verdict, not a hope` | 65 compose; 37 collisions rejected in the control |

## Changelog

- `2026-09-14`: Created, replacing a rejected proposal of mine to tier models into gated and
  ungated. Breadth comes from composing proven models, not from gating them less.
