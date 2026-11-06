# Batch I's nine requirements are credited `implemented`, each on its own case, signed by review under delegation

- **Type:** `decision`
- **Date:** `2026-11-06`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a46-4, `SEMULITH-P4-0362`; the workflow under
  [`decision_four-rulings-delegated.md`](decision_four-rulings-delegated.md), carrying out the first batch of
  [`decision_obligations-route.md`](decision_obligations-route.md); the act and its rulings are
  [`decision_req-gc-m-credited-implemented.md`](decision_req-gc-m-credited-implemented.md)'s.
answers: Who signs Batch I's nine credits, what does one finite case per requirement claim, and what does each leave out?

## The fact / decision

1. **Authority.** Each record in `profiles/rv64gc-lab-v0/credits.sexp` carries `authority review`, as the five before it.
2. **Sufficiency.** One finite case per requirement: its predeclared witnesses, a baseline, a byte-identical repeat, one control diverging at the predeclared witness. Each measures `DIV-POLICY: satisfied — 10 of 10 legs satisfied`, and that is sufficient for `implemented` and for nothing more: the M rulings' reading of the derivation.
3. **What each claims, and what it leaves out** (each record's `limitations`):

   | Credit | Requirement, risk | Witnesses | Control | Not claimed |
   | --- | --- | --- | --- | --- |
   | `CR-D-ALU-IMM-1` | `REQ-D-ALU-IMM`, low | 13 | an immediate not sign-extended | |
   | `CR-D-ALU-REG-1` | `REQ-D-ALU-REG`, low | 10 | SLTU read as signed | |
   | `CR-D-LUI-AUIPC-1` | `REQ-D-LUI-AUIPC`, medium | 9 | an AUIPC offset not sign-extended | AUIPC at addresses other than this program's |
   | `CR-D-JALR-LSB-1` | `REQ-D-JALR-LSB`, medium | 10 | a target that keeps its low bit | a halfword target (`REQ-D-IALIGN-16`, `REQ-GC-C`); a misaligned target's fault |
   | `CR-D-NO-DELAY-SLOTS-1` | `REQ-D-NO-DELAY-SLOTS`, low | 11 | a delay slot that ran | anything but the landing's read of what the skipped instruction would have written |
   | `CR-D-SHAMT-1` | `REQ-D-SHAMT`, high | 15 | an amount not masked to 6 bits | a reserved shift encoding |
   | `CR-D-WSUFFIX-1` | `REQ-D-WSUFFIX`, high | 12 | a word not sign-extended | |
   | `CR-D-LOAD-EXT-1` | `REQ-D-LOAD-EXT`, high | 12 | LW not sign-extended | alignment, faults, translation, atomic access; memory is observed only through the read-back; byte offsets assume `REQ-D-ENDIAN`, still `planned` |
   | `CR-D-LOAD-X0-1` | `REQ-D-LOAD-X0`, high | 16 | a discarded load that skipped its fault | a load's other side effects; the fault's selection (`REQ-D-FAULT-PRIORITY`), the CSR reads (`REQ-GC-CSR-ACCESS`), the return (`REQ-GC-PRIV-INSNS`) |

4. **A form that writes no GPR.** The form-coverage leg counted a form as predeclared only at a witness of its own step. A branch, a store or a load to `x0` writes no GPR, so three of the nine could never satisfy it, and 17 forms between them. The review now also counts such a form when a property's cell names it and that witness comes after a step of the form: the read that observes it, which the property states. A form with any GPR write gets no such route. Each condition has its own test and its own seam, and the leg says which forms it counted this way.
5. **The dependencies stay planned, by the plan's order.** `REQ-D-XLEN` is implemented; `REQ-D-ENDIAN` is not. The derivation reads obligations, not dependencies, and Batch II carries it.
6. **No dossier copy**, by the director's ruling. `G-TRACE` lists all fourteen credited cases, reading each from `evidence/`.

## Why

- The route is [`decision_obligations-route.md`](decision_obligations-route.md)'s: one requirement, one case, one control, on tools that needed one change, and that change is in a review no case pins.
- Weakening the leg would have been wrong in the other direction. "A form is covered if the program runs it" would credit a store nothing read back. The rule asks for the read, named in advance.

## How to apply

- Any pin movement lapses a credit: the three pins and every input of the case's manifest. A window would now cost fourteen re-captures, not five.
- Batch II and on use the same rule: `FENCE`, `ECALL`, `EBREAK`, `FENCE.I` and the rest of the silent forms are predeclared by the read that follows them.
