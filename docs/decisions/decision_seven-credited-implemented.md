# The seven with a switch are credited `implemented`, each measured against what selects otherwise

- **Type:** `decision`
- **Date:** `2026-11-06`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a50-4, `SEMULITH-P4-0375`; the workflow under [`decision_four-rulings-delegated.md`](decision_four-rulings-delegated.md) and [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md), carrying out the step of [`decision_obligations-route.md`](decision_obligations-route.md) on the cases of [`decision_seven-with-a-switch.md`](decision_seven-with-a-switch.md).
answers: Who signs the seven's credits, what does one finite case per requirement claim, and what does each leave out?

## The fact / decision

1. **Authority.** Each record in `profiles/rv64gc-lab-v0/credits.sexp` carries `authority review`.
2. **Sufficiency.** One finite case per requirement, each `DIV-POLICY: satisfied — 11 of 11 legs satisfied`, the eleventh holding every clause of its statement to a witness or a stated limit. That is sufficient for `implemented` and for nothing more: the M rulings' reading of the derivation.
3. **What each claims, and what it leaves out** (each record's `limitations`):

   | Credit | Requirement, risk | Witnesses | Control | Compared with, first difference | Not claimed |
   | --- | --- | --- | --- | --- | --- |
   | `CR-D-SVADE-1` | `REQ-D-SVADE`, medium | 15 | a hardware A update | its alternative, Svade off, step 93 | why the profile chose Svade; the other scheme beyond the one retained run |
   | `CR-D-ATOMIC-MISALIGN-1` | `REQ-D-ATOMIC-MISALIGN`, medium | 26 | the misaligned cause | its alternative, the misaligned scheme, step 24 | an AMO judged before translation under the bare profile override: that needs this case's overlay until the next pinned window |
   | `CR-D-FAULT-PRIORITY-1` | `REQ-D-FAULT-PRIORITY`, medium | 37 | misaligned judged low | its alternative, no misaligned check, step 159 | two translation faults competing; a breakpoint, read as Sdtrig's absence from the selection and not from a trigger CSR |
   | `CR-D-PRIV-MODES-1` | `REQ-D-PRIV-MODES`, high | 15 | a hart without S | its alternative, S off, step 5 | that three modes are what Linux needs; every mode-dependent behaviour in each mode; a hypervisor instruction's refusal, so H's absence is read from `misa` and `mstatus` |
   | `CR-D-SV39-1` | `REQ-D-SV39`, high | 11 | Sv48 taken | its alternative, Sv48 on, step 17 | the SoC precedent; the U54's A and D behaviour; translation in any mode but S; ASIDs |
   | `CR-D-RESERVATION-1` | `REQ-D-RESERVATION`, medium | 24 | an eight-byte set | the profile override, step 23 | exact width, which is past the reference: stated, not compared; another hart or device; multicore behaviour |
   | `CR-D-SC-DETERMINISTIC-1` | `REQ-D-SC-DETERMINISTIC`, medium | 21 | an SC past its address | the profile override, step 21 | translation reads and TLB fills; reservation history as a whole and physical aliases, which are `REQ-D-RESERVATION`'s; exact width; multicore progress |

4. **What the effect adds.** Each of these is the profile's choice among options the reference also offers, so each case retains the same guest through the same binary under what selects otherwise, and the review re-derives the first difference from that raw trace. It must fall on a declared witness, or the leg reads pending. So a selection that changed nothing could not have been credited.
5. **The two high-risk cases** carry the second method and an adversarial set, as the policy asks: `rv64gc-priv-modes-v1` on seven properties, `rv64gc-sv39-v1` on five.
6. **The dependencies.** `REQ-D-EXT-CLOSURE`, `REQ-D-GC-COMPOSITION` and `REQ-D-ENDIAN` stay `planned` and are named in older records' limitations. The derivation reads obligations, not dependencies. One older limitation that called these seven's neighbours "still planned", in `CR-GC-ATOMICS-1`, no longer held and now reads "each on its own case".
7. **No dossier copy.** `G-TRACE` lists all 30 credited cases, reading each from `evidence/`.

## Why

- **Each case was held three ways before this:** rehearsed on a clone before declaring, each real capture byte-identical to the rehearsal, and each control diverging only where predeclared.
- **What remains is not more of the same.** With these seven, 30 are `implemented` and 17 are `planned`. All 17 end at a ruling, by [`decision_obligations-route.md`](decision_obligations-route.md): selection statements, two past the reference, and three with no switch to compare. Those calls come next, each measured and recorded.

## How to apply

- Any pin movement lapses these credits as it does the other 23: the three pins and every input of the case's manifest. The next pinned window's list is in [`decision_csr-write-three-producers.md`](decision_csr-write-three-producers.md).
- Reading a clause of these statements as unwitnessed is a defect in `profiles/rv64gc-lab-v0/statement-trace.sexp`: the trace is annotation, not proof of semantics, and can be argued with.
