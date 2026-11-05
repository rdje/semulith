# A requirement names what the effective contract holds: eight stranded rv64gc requirements rebound, and a rule so none strands again

- **Type:** `decision`
- **Date:** `2026-11-05`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a45-1, `SEMULITH-P4-0350`; the workflow under [`decision_four-rulings-delegated.md`](decision_four-rulings-delegated.md): it makes no new claim, credits nothing and moves no retained case. Its statement rider goes with [`decision_sstc-delivery-needs-the-pinned-window.md`](decision_sstc-delivery-needs-the-pinned-window.md).
answers: Why could eight rv64gc requirements never have reached implemented, what binds them now, and what about their stale statements?

## The fact

The status derivation closes a requirement only when `set(obligation_ids) <= credited`, and it refuses a case naming an obligation outside the effective contract. Measured at 78c8fea2 by comparing each requirement's `obligation_ids` with `contract_measure`: **8 of 48 requirements named only superseded obligations**, so no credit could ever close them, and `G-OBLIGATIONS` could never have gone green. RECORD-SCHEMA said nothing, because its rule asks only that a named obligation exists.

| Requirement | Named | The effective contract holds |
| --- | --- | --- |
| `REQ-D-FAULT-PRIORITY` | `OB-FAULT-PRIORITY` | `OB-GC-FAULT-PRIORITY-V2` |
| `REQ-D-FP-DEFER` | `OB-FP-DEFER` | `OB-GC-FP-QUALIFIED-V2` |
| `REQ-D-ROUTE-FLIP` | `OB-ROUTE-FLIP` | `OB-GC-DEFINITION-V2` |
| `REQ-D-RESOLUTION-ROUTE` | `OB-RESOLUTION-ROUTE` | `OB-GC-DEFINITION-V2`; the stage it states has ended |
| `REQ-D-ECALL-EBREAK` | `OB-ECALL-EBREAK` | `OB-GC-ECALL-EBREAK-V1` |
| `REQ-GC-PRIV-INSNS` | `OB-GC-PRIV-INSNS` | `OB-GC-PRIV-INSNS-V1` |
| `REQ-D-RESERVATION` | `OB-RESERVATION` | `OB-GC-RESERVATION-V2` |
| `REQ-D-SC-DETERMINISTIC` | `OB-SC-DETERMINISTIC` | `OB-GC-SC-DETERMINISTIC-V2` |

## The decision

1. **Seven rebind to the successor the contract already names.** `REQ-D-RESOLUTION-ROUTE` is `excluded`, `not-applicable`, with its argument: a stage, not a behaviour. So the profile reads 43 `planned`, 4 `implemented`, 1 `not-applicable`.
2. **Rule 16, `SUPERSEDED OBLIGATION`:** an included requirement may not name an obligation its contract supersedes. Fired RED on the real tree (`OB-RESERVATION` put back).
3. **Rule 14 frees a mirror whose contract supersedes every obligation the owner's record names.** `REQ-D-ECALL-EBREAK` is mirrored from rv64i, whose record is right for rv64i; this profile's contract already left it behind (`why "the rv64i base mirror says no privileged modes…"`).
4. **The statements wait for the window, and this is why.** Four read stale: `REQ-D-FP-DEFER` ("implements no floating point until…"), `REQ-D-ROUTE-FLIP` (a partial composition), `REQ-D-ECALL-EBREAK` ("no privileged modes", with OQ-5 open), `REQ-GC-PRIV-INSNS` (`wfi` a no-op). Measured by rewriting them and running RECORD-SCHEMA: the first two must equal `profile.sexp`'s decisions, and `profile.sexp` is pinned by every case; all four are mirrored by frozen contract versions whose successors do not name them. So correcting them takes the pinned window and a contract version that gives the successors their requirement mirrors. **None can honestly be credited before that.** It is a rider on the window, not a reason to open one.

## Why

- One owner per fact: the contract owns what holds now, and a requirement that names something else states history as a claim.
- A rule rather than a one-time repair: the next supersession would strand its requirement the same way, silently, with every gate green.

## What this does not settle

- **Ten environment obligations (`OB-GC-ENV-*`) name no requirement.** They are judged through `G-CONTRACT`, where their checks are realized, so nothing is stranded; but `G-OBLIGATIONS`' denominator does not see them, and a reader of that row should know.
- The four credits are unaffected: `4 credit(s), 4 current, 0 lapsed`, since a case pins its own requirement's semantic hash.
