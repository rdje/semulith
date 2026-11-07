# `REQ-D-ABI`, `REQ-D-FP-DEFER`, `REQ-D-ROUTE-FLIP` and `REQ-D-SCOPE-CENSUS` are credited `implemented`, each on a selection's record, and `G-OBLIGATIONS` closes

- **Type:** `decision`
- **Date:** `2026-11-07`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a51-14, `SEMULITH-P4-0392`; the workflow under [`decision_four-rulings-delegated.md`](decision_four-rulings-delegated.md) and [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md), carrying out track 4 of [`decision_the-seventeen-called.md`](decision_the-seventeen-called.md) through [`decision_a-credit-with-no-case.md`](decision_a-credit-with-no-case.md).
answers: Who signs these four credits, what does each claim and leave out, and what does closing the axis mean?

## The fact / decision

1. **Authority.** Each record in `profiles/rv64gc-lab-v0/credits.sexp` carries `authority review`.
2. **Sufficiency.** One retained record per requirement, every fact equal to its declaration, every required check served by a run that exited 0 and repeated, and a statement trace leaving no clause unread. That is sufficient for `implemented` and for nothing more.
3. **What each claims, and what it leaves out:**

   | Credit | Requirement, risk | What it reads | Controls | Not claimed |
   | --- | --- | --- | --- | --- |
   | `CR-D-ABI-1` | `REQ-D-ABI`, medium | one function built under three ABIs, flags and instructions; the workload's flags; the toolchain pin | 5 violating copies; `lp64` and `lp64f` objects | the assembler's guests and the ACT suites, which make no calls across the ABI and are tagged otherwise on purpose; the whole of the psABI |
   | `CR-D-FP-DEFER-1` | `REQ-D-FP-DEFER`, high | the pin, the lock's checksum, every user of the backend, the records | 5 violating copies; a second producer, `cargo tree`; `FP-VECTORS` | numeric and instruction behaviour, `REQ-GC-F`'s and `REQ-GC-D`'s own |
   | `CR-D-ROUTE-FLIP-1` | `REQ-D-ROUTE-FLIP`, low | the vehicle, the composition, each mirror's header and gate | 4 violating copies, a stale mirror among them | instruction behaviour; a read runs no generator, their drift gates do, in every commit |
   | `CR-D-SCOPE-CENSUS-1` | `REQ-D-SCOPE-CENSUS`, low | the 52-form base against `rv64i-lab-v0`, the total, the composition | 2 violating copies; `DENOMINATOR LIE` | that each form is executed or behaves, which are `EXERCISE-COVERAGE`'s and each extension's |

4. **`G-OBLIGATIONS` closes.** All 48: 46 `implemented`, 2 `not-applicable`, and none `planned` or `partial`. Each of the 46 on a current credit that authenticates on every read. The route's two `L` requirements, `REQ-GC-PARTIAL-PROGRESS` and `REQ-GC-PRIV-INSNS`, closed with what is not compared named as a limit, on the same rule as the seven: `wfi`'s stall and the fetches it withholds, and faults injected at a chosen suboperation, are past the reference and stay uncredited. That is the call [`decision_the-seventeen-called.md`](decision_the-seventeen-called.md) made, and a reader who holds those clauses must be witnessed would read both as `partial` and this axis as open.
5. **What this does not mean.** `CPU-SYSTEM` still reads `incomplete`: `G-RELEASE` is open, and a closed axis grants no release. Each credit is finite evidence on named inputs, not proof, and agreement with the pinned reference is what it says and no more.

## How to apply

- Any fact moving lapses that credit by name, and the gate fails. To change a selection on purpose, delete its record and credit together and take a new one.
- The credits with cases stay as [`decision_the-four-with-no-switch-credited-implemented.md`](decision_the-four-with-no-switch-credited-implemented.md) and its predecessors state them.
