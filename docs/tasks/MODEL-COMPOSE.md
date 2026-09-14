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
  Status: `pending`
  Goal: a fragment is a complete, independently checkable description of one thing; a unit names
  the fragments it unions. Give both a form in the canonical definition.
  Acceptance: `rv64i-lab-v0` re-expressed as base + (empty) extension list without changing a
  single observable; a fragment with a hidden dependency is refused.

- ID: `MODEL-COMPOSE.3` — **assumption / guarantee discharge**
  Status: `pending`
  Goal: the inter-unit operator, and the mechanical form of `docs/CPU_ENVIRONMENT.md` §5. Every
  sub-unit `environment-assumption` is matched by a named guarantee or the composition is rejected.
  Acceptance: fired RED by removing one guarantee; the 8 assumptions `rv64i-lab-v0` already carries
  are the first real input.

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
| 1 | `MODEL-COMPOSE.2` | `pending` | the fragment form, now that one composition has actually been performed and the `M` fragment used to do it is still unpinned |
| 2 | `MODEL-COMPOSE.3` | `pending` | the inter-unit operator, whose first input already exists — 8 assumptions `rv64i-lab-v0` carries |
| 3 | `MODEL-COMPOSE.4` | `pending` | slots, which is what makes top-down composition checkable before its parts exist |

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

## Acceptance Checklist (current leaf — `MODEL-COMPOSE.1`)

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

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-14` | `MODEL-COMPOSE.1` | grounding: do the references compose from fragments? | riscv-opcodes 111 files; sail-riscv 34 dirs / 59 encoding files |
| `2026-09-14` | `MODEL-COMPOSE.1` | compose owned RV64I + `M` fragments | 52 + 8 + 5 = 65, no collision, no duplicate name |
| `2026-09-14` | `MODEL-COMPOSE.1` | control: compose with a fragment already contained | 37 collisions named with masks, `rc=1`, REJECTED |
| `2026-09-14` | `MODEL-COMPOSE.1` | unplanned refusal: an empty fragment | `REFUSED … an empty fragment is not a valid one` |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `MODEL-COMPOSE.1` | `SEMULITH-MC-0038 (leaf MODEL-COMPOSE.1): encoding composition is a verdict, not a hope` | 65 compose; 37 collisions rejected in the control |

## Changelog

- `2026-09-14`: Created, replacing a rejected proposal of mine to tier models into gated and
  ungated. Breadth comes from composing proven models, not from gating them less.
