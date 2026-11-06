# Batch II-b's four requirements are credited `implemented`, each on its own case, signed by review under delegation

- **Type:** `decision`
- **Date:** `2026-11-06`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a49-3, `SEMULITH-P4-0370`; the workflow under [`decision_four-rulings-delegated.md`](decision_four-rulings-delegated.md) and [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md), carrying out the `defined` remainder of [`decision_obligations-route.md`](decision_obligations-route.md) on the tools of [`decision_the-window-that-carries-fetch-faults.md`](decision_the-window-that-carries-fetch-faults.md); the act and its rulings are [`decision_req-gc-m-credited-implemented.md`](decision_req-gc-m-credited-implemented.md)'s.
answers: Who signs Batch II-b's four credits, what does one finite case per requirement claim, and what does each leave out?

## The fact / decision

1. **Authority.** Each record in `profiles/rv64gc-lab-v0/credits.sexp` carries `authority review`.
2. **Sufficiency.** One finite case per requirement, each `DIV-POLICY: satisfied — 11 of 11 legs satisfied`, the eleventh holding every clause of its statement to a witness or a stated limit. That is sufficient for `implemented` and for nothing more: the M rulings' reading of the derivation.
3. **What each claims, and what it leaves out** (each record's `limitations`):

   | Credit | Requirement, risk | Witnesses | Control | Not claimed |
   | --- | --- | --- | --- | --- |
   | `CR-GC-ATOMICS-1` | `REQ-GC-ATOMICS`, high | 64 | a word AMO not sign-extended | a misaligned atomic, physical aliases and width matching, each its own requirement still `planned`; any multicore or weak-memory claim: atomicity is not exercised against another agent |
   | `CR-GC-C-1` | `REQ-GC-C`, medium | 52 | C.JALR linking four bytes on | every reserved code point and immediate range; a constrained loop's eventual success; a HINT's effect on the performance counters; the fetch width by counting the environment's requests, only by what ran |
   | `CR-GC-F-1` | `REQ-GC-F`, high | 90 | a static RDN ignored | numeric exhaustiveness: results stand at these values; FS Off on every form, only a move, a load and an arithmetic form |
   | `CR-GC-D-1` | `REQ-GC-D`, high | 93 | a static RUP ignored | the same; a reserved mode on FCVT.D.WU, only FCVT.D.W and FCVT.D.S |

4. **The numeric producers.** `F` and `D`'s expected values come from `scripts/specfp`, a tracked spec-side producer distinct from the backend under test, and the pinned Sail is a second one, as the policy's floating-point rule asks.
5. **The dependencies stay planned.** `REQ-D-RESERVATION`, `REQ-D-SC-DETERMINISTIC` and `REQ-D-EXT-CLOSURE` are `planned`; the derivation reads obligations, not dependencies.
6. **No dossier copy.** `G-TRACE` lists all 23 credited cases, reading each from `evidence/`.

## Why

- `REQ-GC-C`'s second-parcel fault is witnessed, not named away: that is what the window was opened for.
- Each case was rehearsed end to end on a clone before it was declared, and every compared file of the real capture matched.

## How to apply

- Any pin movement lapses these credits as it does the other 19: the three pins and every input of the case's manifest.
- Reading a clause of these statements as unwitnessed is a defect in `profiles/rv64gc-lab-v0/statement-trace.sexp`: the trace is annotation, not proof of semantics, and can be argued with.
