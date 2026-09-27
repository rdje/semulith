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
  Status: `pending`
  Goal: a composition may declare an unbound slot with its requirements, so shape, address space
  and unmet requirements are checkable **before the parts exist**.
  Acceptance: a partial composition passes the checks that apply and is reported partial; a
  composition claiming completeness with an unbound slot is rejected.

- ID: `MODEL-COMPOSE.5` — **nesting: a composition is a unit**
  Status: `pending`
  Goal: `computer → board → soc → {cpu, device}` uses one record shape at every level.
  Acceptance: a two-level composition is checked by the same code as a one-level one.

- ID: `MODEL-COMPOSE.6` — **semantic refinement points**
  Status: `pending`
  Goal: the hard axis. An extension can change base behaviour — adding CSRs changes trap handling;
  adding `C` changes `IALIGN` and therefore which branch targets fault. A fragment must **declare**
  that it modifies a base behaviour; a silent override is a defect.
  Acceptance: a fragment that redefines a base semantic without declaring it is refused.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `MODEL-COMPOSE.4` | `pending` | slots — top-down composition with holes, checkable before the parts exist |
| 2 | `MODEL-COMPOSE.6` | `pending` | semantic refinement points — the hard axis, needs `MODEL-METHOD.9`'s semantics to exist first |

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

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
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
| `MODEL-COMPOSE.3` | `SEMILITH-MC-0040 (leaf MODEL-COMPOSE.3): …` | assumption/guarantee discharge decides over the merged union; 8/8 on the real corpus; fired RED by removing one guarantee |
| `MODEL-COMPOSE.2` | `SEMULITH-MC-0039 (leaf MODEL-COMPOSE.2): fragments get a form and a home` | nothing observable moved; M pinned |
| `MODEL-COMPOSE.1` | `SEMULITH-MC-0038 (leaf MODEL-COMPOSE.1): encoding composition is a verdict, not a hope` | 65 compose; 37 collisions rejected in the control |

## Changelog

- `2026-09-14`: Created, replacing a rejected proposal of mine to tier models into gated and
  ungated. Breadth comes from composing proven models, not from gating them less.
