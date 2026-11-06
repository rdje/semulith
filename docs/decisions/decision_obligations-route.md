# G-OBLIGATIONS' other 42 requirements go in batches on the tools as they are, and 14 of them need a ruling first

- **Type:** `decision`
- **Date:** `2026-11-06`
- **Status:** `active` (the route for 28 is picked and being carried out from a46-1 on; the other 14 are raised to the director when their turn comes)
- **Owner / source:** `P4-SYSTEM.14` a46-0, `SEMULITH-P4-0358`; raised early because its cost would otherwise dominate the work, and read against the director's standard ([`decision_sstc-delivery-needs-the-pinned-window.md`](decision_sstc-delivery-needs-the-pinned-window.md) closed the case before it). **The director can overrule any of it.**
answers: What does it take to close the 42 requirements still `planned`, by what route, what would one case at a time cost, and what can that route not close?

## The fact

`CPU-SYSTEM` reads 2 of 10 axes open: `G-OBLIGATIONS` and `G-RELEASE`. `G-OBLIGATIONS` is 42 `planned`, 5 `implemented`, 1 `not-applicable`. **All 42 already have their two declared contract checks realized** (`G-CONTRACT` green): the model's side exists, and what is missing is the matched-reference comparison and a credit.

Measured by `python3 -B scripts/census_reference_config.py --case rv64gc-sstc-v1` (346 Sail runs in 3.9 s; target/p4-system-14/a46-0): **158 of the 173 corpus guests agree with the pinned Sail on at least one of the two configurations.** Crossing each obligation's realized checks with those guests:

| Class | Count | What it means | Requirements |
| --- | --- | --- | --- |
| **G**, guest-evidenced | 15 | Its checks name corpus guests, and Sail agrees with them | `REQ-D-ALU-IMM`, `-ALU-REG`, `-LUI-AUIPC`, `-NO-DELAY-SLOTS`, `-SHAMT`, `-WSUFFIX`, `-LOAD-EXT`, `-ECALL-EBREAK`, `-ENDIAN`, `-IALIGN-16`, `-FAULT-PRIORITY`, `-SV39`, `-SVADE`, `REQ-GC-C`, and `REQ-D-PRIV-MODES` (12 of its 13; `mm-wfi` is the other) |
| **X**, execution-evidenced | 13 | Its checks run a witness in Rust, so a case's program must be authored | `REQ-D-JALR-LSB`, `-LOAD-X0`, `-FENCE`, `-WALK-IMPLICIT`, `-RESERVATION`, `-SC-DETERMINISTIC`, `-ATOMIC-MISALIGN`, `REQ-GC-CSR-ACCESS`, `-COUNTERS`, `-FENCEI`, `-ATOMICS`, `-F`, `-D` |
| **S**, a statement of selection | 12 | Its checks are a scope predicate and its negative copies: no behaviour a reference could be compared on, as things stand | `REQ-D-GC-COMPOSITION`, `-EXT-CLOSURE`, `-PRIV-REVISION`, `-FP-DEFER`, `-ABI`, `-SBI`, `-NO-PMP`, `-NO-H`, `-RVWMO`, `-PRIV-INSNS`, `-ROUTE-FLIP`, `-SCOPE-CENSUS` |
| **L**, reaches past the reference | 2 | Most of its named guests are behaviour Sail does not show | `REQ-GC-PARTIAL-PROGRESS` (2 of 6 agree), `REQ-GC-PRIV-INSNS` (2 of 5) |

The 15 guests that agree on neither configuration fall into five families. This is a reading of each detail line, not a root cause; each gets one when a case needs it:

| Family | Guests | What the comparison says | Reading |
| --- | --- | --- | --- |
| Wait | `mm-wfi`, `w-deleg`, `w-notrap`, `w-timer` | Sail prints an instruction row where the expectation declares a wait, or the row is refused | The laboratory's `wfi` stalls |
| MTIP | `i-prio`, `i-timer`, `env-irq-sources` | `mip` reads bit 7 set | The reference's CLINT holds it; the laboratory declares none (already `CR-D-CSR-SET-2`'s limitation) |
| Injection | `inj-carrier`, `inj-atomics`, `inj-fp`, `inj-walk-l0`, `-l1`, `-l2` | The expected fault or step is absent | The guests rely on the laboratory's injected faults |
| Reservation width | `a-lrsc-mustfail` | `sc.d` succeeds where the laboratory's exact-width rule fails it | A selected policy within the statement's latitude |
| Not compared | `guest-no-device` | Comparison disabled by its own record | By declaration |

## The options, for the 28 in G and X

The numbers: a commit takes 24 minutes through the gate today at 13 cases, under load (focused 5, doctrines 19; a43e-5's chain). ZICNTR took 5 units on its own (a43c-1 … a43c-5). The window's five cases took 3 (a43e-3, a43e-4, a43e-5), which proves a batch needs no new tool.

| | Units | Gate time alone | Evidence | Verdict |
| --- | --- | --- | --- | --- |
| **A. One case at a time** | 28 × 5 = 140 | 56 hours | 28 cases | Works, and spends its cost on the ceremony rather than on the witnesses |
| **B. Batches, one case per requirement** | 5 batches × 4 = 20 | 8 hours | 28 cases | **Picked.** No pinned file moves and no credit lapses. Each commit is larger, which a gate already judges |
| **C. A family case binding several requirements** | Fewer cases, plus a window | Lower, later | About 8 cases | Rejected for now. A case's `requirement_id` is one field of a pinned schema, so it would lapse all five credits; `authenticate` holds a declaration to the credited requirement alone; and the policy allows one control for several requirements "only when the graph states why its failure would be detected for each one", which each review leg would have to learn |

**B's unit:** (1) the batch's programs, cases and statements; (2) its declarations, committed before capture; (3) each captured once, with any effect; (4) the reviews and credits.

| Batch | Requirements | The rule it brings |
| --- | --- | --- |
| I, the RV64I base | `ALU-IMM`, `ALU-REG`, `LUI-AUIPC`, `JALR-LSB`, `NO-DELAY-SLOTS`, `SHAMT`, `WSUFFIX`, `LOAD-EXT`, `LOAD-X0` | `defined`, on the profile override, the M case's route |
| II, system | `ECALL-EBREAK`, `CSR-ACCESS`, `COUNTERS`, `PRIV-MODES`, `FAULT-PRIORITY`, `IALIGN-16`, `ENDIAN`, `FENCE`, `FENCEI` | Privilege, CSR, trap and return; parcel boundaries |
| III, atomics | `ATOMICS`, `RESERVATION`, `SC-DETERMINISTIC`, `ATOMIC-MISALIGN` | The atomics rule; `a-lrsc-mustfail`'s difference, observed and justified or left uncredited |
| IV, translation | `SV39`, `SVADE`, `WALK-IMPLICIT` | The walk rule: "A successful final load alone cannot establish the absence of an extra access", in a vocabulary of GPR changes |
| V, C, F and D | `REQ-GC-C`, `REQ-GC-F`, `REQ-GC-D` | The floating-point rule's numeric producers; FP state observed through GPRs, and named as narrower |

## What this route cannot close

**S, the 12.** A matched comparison means little for "the privileged architecture is the pinned publication's". The policy allows an alternative: it "needs an explicit source-grounded argument and its own controls before execution", and each already has a positive and a negative check. But `authenticate` only reads a case, `EVIDENCE_POLICY.md` is pinned by every credit and every manifest, so editing it lapses them all, and not every member is the same: `GC-COMPOSITION` could be a real case reading `misa`, while `NO-PMP` and `NO-H` meet the deriver's 33-CSR vocabulary, which is pinned. **Raised for the director when Batch V lands**, with a measured proposal, or sooner on request.

**L, the 2.** "A genuine reference limitation leaves the affected comparison uncredited." `wfi`'s stall and injected faults are what Sail does not show, and relabelling a passing subset would not be honest. They may rightly end `partial`, and `partial` keeps `G-OBLIGATIONS` open. **Whether that closes the axis is the director's**: `P4-SYSTEM.18`'s verdict turns on it.

## Walls to move before they stop a batch

| Wall | Measured | When it hits | What moves it |
| --- | --- | --- | --- |
| `evidence/README.md`'s cap | 4,094 of 4,096 B, with a table its text calls the complete membership | The next row: Batch I | **Done at a46-1:** the table left for a generated page, [the retained cases](../models/rv64gc-lab-v0/src/retained-cases.md), read from each `case.sexp` |
| `credits.sexp`'s document bound | 10,049 B for five, against 65,536 B: about 32 records | Batch V | Split by family, or a raised bound, measured then. `MAX_CREDITS` is 64 |
| The family's census | Re-derived by hand per case: registry row, `FAMILY_FILES`, tables, one probe class | Every batch | Derive what can be derived from the cases |

## The tripwire

Several probes read every case on every run, and their arms run in both Python modes (`probe_div_method.py` took 63 s at load 24, `probe_div_capture_inputs.py` 32 s). **Gate time per case is not measured yet**, so the 8 hours assumes it stays flat, and that is the estimate's weakest number. Batch I adds nine cases and measures it. If a case adds more than a minute to the gate, the work stops and the cost is raised before Batch II, with numbers and options.

## How to apply

- The next case is `a46-2`'s. A later capture's guard is `target/p4-system-14/a43e-4/capture-now.sh`, not the three-minute wait.
- A batch's declarations and captures are each one commit, so a moved child between them refuses every case in the batch, not one: freeze the union.
- One requirement, one case, one control. A witness that would serve two requirements is written twice.
- A difference is a finding, never a reason to drop a witness quietly: observed and justified under the `implementation-defined` row, or left uncredited and named.
