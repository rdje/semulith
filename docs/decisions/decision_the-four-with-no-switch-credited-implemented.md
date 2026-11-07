# `REQ-D-ENDIAN`, `REQ-D-FENCE`, `REQ-D-WALK-IMPLICIT` and `REQ-GC-PARTIAL-PROGRESS` are credited `implemented`, each on a declared disposition

- **Type:** `decision`
- **Date:** `2026-11-07`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a51-10, `SEMULITH-P4-0388`; the workflow under [`decision_four-rulings-delegated.md`](decision_four-rulings-delegated.md) and [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md), carrying out track 3 of [`decision_the-seventeen-called.md`](decision_the-seventeen-called.md).
answers: Who signs these four credits, why can a declared disposition stand in for an effect, and what does each case leave out?

## The fact / decision

1. **Authority.** Each record in `profiles/rv64gc-lab-v0/credits.sexp` carries `authority review`.
2. **Sufficiency.** One finite case per requirement, each `DIV-POLICY: satisfied — 11 of 11 legs satisfied`. That is sufficient for `implemented` and for nothing more: the M rulings' reading of the derivation.
3. **Why a disposition can stand in for an effect.** The policy's `implementation-defined` row asks for a reference configuration with a behaviour-changing control, or an observed and justified difference. The pinned binary has no key for any of these, so neither arm can be met. The policy also says an alternative "needs an explicit source-grounded argument and its own controls before execution; it cannot be manufactured by relabeling an unrelated passing result." So each requirement keeps its category. Each has a record in `profiles/rv64gc-lab-v0/dispositions.sexp`, declared before its capture, and the review reads that record, its source and its control on every read.
4. **What each claims, and what it leaves out** (each record's `limitations`):

   | Credit | Requirement, risk | Witnesses | Control, where it diverges | Disposition | Not claimed |
   | --- | --- | --- | --- | --- | --- |
   | `CR-D-ENDIAN-1` | `REQ-D-ENDIAN`, medium | 8 | a big-endian byte 0, step 19 | `DS-ENDIAN` | a comparison with a hart of the other byte order, since the pinned binary offers none |
   | `CR-D-FENCE-1` | `REQ-D-FENCE`, medium | 10 | a reserved fm that trapped, step 29 | `DS-FENCE` | any ordering, since no other hart or device exists here to observe one |
   | `CR-D-WALK-IMPLICIT-1` | `REQ-D-WALK-IMPLICIT`, high | 6 | a walk reaching another page, step 74 | `DS-WALK-IMPLICIT`, with the walk record | the order and number of reads, since TLB replacement is not architectural; the catalogue facts about `rv64i-lab-v0` |
   | `CR-GC-PARTIAL-PROGRESS-1` | `REQ-GC-PARTIAL-PROGRESS`, high | 20 | a faulting load that wrote rd, step 103 | `DS-PARTIAL-PROGRESS` | a fault injected at a chosen suboperation, past the reference; that no suboperation is restartable, a claim over the whole engine |

5. **The walk record is more than the case.** The policy's translation rule says a successful final load cannot establish the absence of an extra access, and a GPR comparison cannot see one. So `REQ-D-WALK-IMPLICIT` also retains what each producer's walks read, and the review re-derives the comparison on every read: the same 6 PTEs with the same values on both producers, 8 bytes each, at most 3 per walk, none written from the first walk on.
6. **No dossier copy.** `G-TRACE` lists all 42 credited cases, reading each from `evidence/`.

## How to apply

- Any pin movement lapses these credits as it does the other 38: the three pins and every input of the case's manifest.
- `dispositions.sexp` is read on every read: removing a record, or naming a property the case does not declare, reads the leg pending, and a current credit over a pending measurement is a finding.
- A pinned window with a key for byte order, fences or preciseness ends the reason for that disposition. The requirement then owes the measured effect.
