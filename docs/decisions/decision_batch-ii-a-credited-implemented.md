# Batch II-a's five requirements are credited `implemented`, each on its own case, signed by review under delegation

- **Type:** `decision`
- **Date:** `2026-11-06`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a47-3, `SEMULITH-P4-0365`; the workflow under
  [`decision_four-rulings-delegated.md`](decision_four-rulings-delegated.md), carrying out the `defined` half of Batch II of
  [`decision_obligations-route.md`](decision_obligations-route.md); the act and its rulings are
  [`decision_req-gc-m-credited-implemented.md`](decision_req-gc-m-credited-implemented.md)'s.
answers: Who signs Batch II-a's five credits, what does one finite case per requirement claim, and what does each leave out?

## The fact / decision

1. **Authority.** Each record in `profiles/rv64gc-lab-v0/credits.sexp` carries `authority review`.
2. **Sufficiency.** One finite case per requirement, each `DIV-POLICY: satisfied — 10 of 10 legs satisfied`, sufficient for `implemented` and for nothing more: the M rulings' reading of the derivation.
3. **What each claims, and what it leaves out** (each record's `limitations`):

   | Credit | Requirement, risk | Witnesses | Control | Not claimed |
   | --- | --- | --- | --- | --- |
   | `CR-D-ECALL-EBREAK-1` | `REQ-D-ECALL-EBREAK`, high | 25 | a cause that does not name its mode | a delegated ECALL from S (bit 9 stays clear here); nested traps; the laboratory's halting report, which is not a trap |
   | `CR-GC-CSR-ACCESS-1` | `REQ-GC-CSR-ACCESS`, high | 21 | a CSR immediate sign-extended | that CSRRW with rd = x0 does not read, which has no side effect here to observe; the counter gates (`REQ-GC-COUNTERS`) and Sstc's (`REQ-D-SSTC`); atomicity beyond one hart |
   | `CR-GC-COUNTERS-1` | `REQ-GC-COUNTERS`, medium | 8 | a refused read that committed | rates and progress (the environment contract's); a CLINT or any device, this case's source of time |
   | `CR-GC-FENCEI-1` | `REQ-GC-FENCEI`, low | 2 | a stale fetch | that a fetch with no FENCE.I may read either value: this machine re-reads memory on every fetch (D-CODE-VISIBILITY); the reserved encodings |
   | `CR-D-IALIGN-16-1` | `REQ-D-IALIGN-16`, medium | 6 | a target rounded to a word | each compressed form's expansion (`REQ-GC-C`); `REQ-D-GC-COMPOSITION`, its dependency, still `planned` |

4. **A `configuration` requirement naming no form.** The coverage leg allowed a requirement to name no form only for kind `state`. `REQ-D-IALIGN-16` says where an instruction may start and names none, so the same reading holds: its predeclared witnesses are its coverage, and the leg says so. An `instruction` or `event` requirement naming no form stays pending, because that would be a fault in the catalogue. One test and one seam.
5. **`REQ-D-ECALL-EBREAK` is this profile's, not `rv64i`'s.** The two share the id with different obligations, and rv64i's question OQ-5 is not this requirement's (`gaps.md`). Credit here says nothing about `rv64i`, whose status stays its own (`decision_mirror-status-is-per-profile.md`). The gate's statement that it "remains partial on OQ-5" was stale, and is gone.
6. **No dossier copy.** `G-TRACE` lists all nineteen credited cases, reading each from `evidence/`.

## Why

- The route is [`decision_obligations-route.md`](decision_obligations-route.md)'s. Each program was rehearsed end to end on a clone before it was declared, and every compared file of the real capture matched.

## How to apply

- Any pin movement lapses a credit. A window would now cost nineteen re-captures.
- The next `defined` requirements are `REQ-GC-ATOMICS`, `REQ-GC-C`, `REQ-GC-F` and `REQ-GC-D`. Each `implementation-defined` one needs the tool for a declared alternative first.
