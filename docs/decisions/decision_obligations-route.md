# G-OBLIGATIONS' other 42 requirements go in batches on the tools as they are, and 14 of them need a ruling first

- **Type:** `decision`
- **Date:** `2026-11-06`
- **Status:** `active` (the route is picked and being carried out from a46-1 on; 17 end at a ruling, called by the engineer when their turn comes under [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md): see "What Batch II found")
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

**B's unit**, three commits since Batch I joined the first two: (1) the batch's programs, cases, statements and declarations, committed before capture; (2) each captured once, with any effect; (3) the reviews and credits. So 15 units and about 6 hours of gate. Each batch is rehearsed end to end on a throwaway clone before (1): a capture is never retried, so a fault found after it spends a case id.

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

- Batch I stands captured (a46-3). A later capture's guard is `target/p4-system-14/a43e-4/capture-now.sh`, not the three-minute wait.
- A batch's declarations and captures are each one commit, so a moved child between them refuses every case in the batch, not one: freeze the union.
- One requirement, one case, one control. A witness that would serve two requirements is written twice.
- A difference is a finding, never a reason to drop a witness quietly: observed and justified under the `implementation-defined` row, or left uncredited and named.

## Batch I, as measured so far (a46-2, 2026-11-06)

Nine programs and nine cases, 108 witnesses. **All three producers agree on every program:** the spec-side author, the lab engine (`every_guest_matches_its_expectations`, 182 guests) and the pinned Sail. **The rehearsal** (`target/p4-system-14/a46-2/rehearse.sh`) ran the route end to end on a throwaway clone: every control diverged where declared, and it found what no table check had.

| Found by rehearsing | What it would have cost after a real capture |
| --- | --- |
| `REQ-D-NO-DELAY-SLOTS` had no witness at a `JAL` or `JALR` step, though both write a link | A case id: the case is pinned at its declaration |
| The new rule read an empty `(writes)` form as a write, so no silent form counted | A failed review, fixable, since the review is not pinned |

**The rule the review needed, landed with the credits (a46-4):** the form-coverage leg counts a form as predeclared only at a witness of its own step, and a branch, a store or a load to `x0` writes no GPR. So it may also be predeclared when a property's cell names it and that witness comes after a step of the form. All nine then read 10 of 10 on the clone.

**Captured (a46-3, 2026-11-06).** Each once, 1.2 s to 1.4 s, every control where declared, and every compared file byte-identical to the rehearsal's. The guard's second run: it held for four and a half minutes at load 13.74 down to 8.21, then ran beside seven to nine sibling processes at load 7.3 to 7.8.

**Credited (a46-4, 2026-11-06).** Nine credits, 10 of 10 legs each ([`decision_batch-i-credited-implemented.md`](decision_batch-i-credited-implemented.md)): 14 `implemented`, 33 `planned`. **The tripwire, read:** the pre-commit gate took 19.3 minutes at 13 cases and 5 credits (a43e-5), 20.1 at Batch I's declarations, 21.3 for the next commit, and 22.3 at the captures, under loads of 8 to 24: about 20 seconds per captured case, against the limit of a minute. The credits' own cost is measured at the next batch. **The route holds.** Batch I took three commits and a preparing one, and needed one rule.

## What Batch II found (a47-1, 2026-11-06)

Reading the next requirements before writing their programs found two walls that the first table did not show, and one false finding.

**1. Ten of the 28 are `implementation-defined`.** Batch I was all `defined`. This category's row asks for a "pinned matching reference configuration with a behavior-changing control", and `_config_effect` measures it as the case's own configuration against the profile override. For these ten the override already is the selection, so there is nothing to compare. They are `PRIV-MODES`, `FAULT-PRIORITY`, `ENDIAN`, `FENCE`, `SV39`, `SVADE`, `WALK-IMPLICIT`, `RESERVATION`, `SC-DETERMINISTIC` and `ATOMIC-MISALIGN`. Measured against the pinned binary's `--print-default-config`:

| Requirement | A real switch? |
| --- | --- |
| `PRIV-MODES` | `extensions.S`, `extensions.U` |
| `SV39` | `extensions.Sv39` |
| `SVADE` | `extensions.Svade`, `extensions.Svadu` |
| `FAULT-PRIORITY` | `memory.misaligned` |
| `ATOMIC-MISALIGN` | `memory.misaligned.exceptions` |
| `RESERVATION`, `SC-DETERMINISTIC` | `memory.reservation` (to be measured against each witness) |
| `ENDIAN`, `FENCE`, `WALK-IMPLICIT` | none found |

So the row can be met honestly for most of them: the same guest under a configuration that selects otherwise, the difference retained, which is what the policy asks (measured since against each switch, with this table's corrections, in [`decision_declared-alternative-configuration.md`](decision_declared-alternative-configuration.md)). It needs the tool to read a case's declared alternative, not only the override. `measure_config_effect.py` and the review are not pinned, so no credit lapses. **It lands with the batch that first needs it.** The three with no switch join what is raised for a ruling, so that group is **17** today, not 14: the 12 selection statements, the 2 past the reference, and these 3.

**2. A `configuration` requirement naming no form could never satisfy the coverage leg**, which allowed that only for `state`. `REQ-D-IALIGN-16` is the first. The reasoning is the same as for state, and an `instruction` or `event` requirement naming no form stays pending. It lands with this batch's credits.

**3. A false finding, fixed here.** A declared case guessed its profile from whichever catalogue names its requirement, and `REQ-D-ECALL-EBREAK` is in both `rv64i` and `rv64gc` with different obligations, so `rv64i` claimed the case and reported it outside its contract. A case's own `case.sexp` names its profile, and that is now what decides. It cost nothing until a mirrored requirement's obligations differed.

**Since a50-2** the seven are declared: `decision_seven-with-a-switch.md` carries each case, and what writing them found, including a setting the override lacks. **The order, restated.** Batch II-a, the five `defined`: `ECALL-EBREAK`, `CSR-ACCESS`, `COUNTERS`, `IALIGN-16`, `FENCEI`. Then the `defined` remainder: `ATOMICS`, `C`, `F`, `D`. Then the tool for a declared alternative, and the seven with a switch. Then the ruling.

**Batch II-a captured (a47-2, 2026-11-06).** Each once, 1.1 s to 1.3 s, every control where declared, every compared file byte-identical to the rehearsal's. The guard's first attempt held for ten minutes at a load above 8 and refused, capturing nothing. Re-armed, it waited 19 minutes more and ran at load 6.6 to 7.0. That cost a wait and no case id, which is the trade the guard was set up to make.

**Batch II-a credited (a47-3, 2026-11-06).** Five credits, 10 of 10 legs each ([`decision_batch-ii-a-credited-implemented.md`](decision_batch-ii-a-credited-implemented.md)): 19 `implemented`, 28 `planned`. **The tripwire, read again:** the pre-commit gate took 20.6 minutes at a47-1 and 21.3 at a47-2, with 27 cases, against 19.3 at 13 cases (a43e-5): about 9 seconds per added case, under loads that moved by more than that. The limit of a minute a case is not close.

## What the `defined` remainder found (a48-1, 2026-11-06)

Batch II-b is `ATOMICS`, `C`, `F` and `D`, one case each: 239 witnesses, all three producers agreeing, rehearsed on a throwaway clone, each 10 of 10 legs there. Writing them found three things.

**1. A case cannot carry a fetch fault.** `REQ-GC-C` says a second-parcel translation fault reports that parcel's address in `xtval` and the instruction's start in `xepc`, before any effect. `matched_gpr_case.read_document` takes a step that fetches a word of a length, or a delivery boundary that fetches and writes nothing. A fetch fault reads a parcel and retires nothing, so it is neither, and that file is one of the 67 pinned children: to teach it lapses every credit. The first draft of `c-forms` carried the fault, and the spec-side derivation and the pinned Sail agreed on it, a measurement with nothing retained.

| Option | Cost | Taken |
| --- | --- | --- |
| A. Open a window for this now | Lapses every current credit, 19 today and 23 once this batch is credited, each re-captured as a new case | No: one sentence of one requirement |
| B. Witness what the format can carry, name the rest | `REQ-GC-C`'s limitation says so; the corpus guest `c-page-straddle` holds the fault against the backend | **Yes** |
| C. Add the boundary at the next window, whatever opens it | A small format change, carried with the next pinned movement | **Yes, with B** |

So the case witnessed the fetch width positively: C.JR in a page's very last parcel, before an invalid page, runs and lands.

**Reversed the same day (a49-0).** The table's "one sentence of one requirement" was a claim, not a measurement: three planned requirements state a fetch fault. Option A is taken, at its lowest price, with what else only a window can move: [`decision_the-window-that-carries-fetch-faults.md`](decision_the-window-that-carries-fetch-faults.md).

**2. The forms are not the requirement.** The first drafts covered every form, and agreed with Sail on every step. Read against the requirements' statements they missed the ordering bits, one store-rules translation, the HINTs, the reserved encodings, the FS gate, sticky flags, most of the reserved rounding modes and most of the NaN rules. **Read the statement before the form list.** Forms are one leg of ten, and the review would not have caught these.

**3. Two bounds, met.** `d-forms.expected.sexp` first came to 78,908 B against a prepared input's 65,536 B. Loading each constant in the fewest rows its bits allow brought it to 59,439 B, and the program from 427 steps to 326, with no witness lost. And a case holds 64 properties: `F` and `D` are at that bound, and `ATOMICS` too, so each drops what it can, and `D`'s limitation names what is witnessed only at format 32.

Holding the declared values to the derivation refused 13 at first, each mine: seven read-backs of negative singles not sign-extended, which the chapter's own `FMV.X.W` statement says they are, and six from one wrong patch address and one sentinel equal to its value. That is the procedure working: values written first, from the statement, then held.

**Batch II-b credited (a49-3, 2026-11-06).** Four credits on the window's tools, 11 of 11 legs each ([`decision_batch-ii-b-credited-implemented.md`](decision_batch-ii-b-credited-implemented.md)): with the 19 re-issued, 23 `implemented`, 24 `planned`. **The tripwire, read again:** the pre-commit gate took 25.3 minutes at a48-1, 26.1 at a49-1 and 27.3 at a49-2, with 48 cases in the tree, the window's peak. That is about 2 minutes for 17 more cases, against the limit of 1 minute per case. Next, the tool for a declared alternative.

**The seven credited (a50-4, 2026-11-06).** [`decision_seven-credited-implemented.md`](decision_seven-credited-implemented.md): 30 `implemented`, 17 `planned`, and all 17 end at a ruling. **The tripwire, read again:** the pre-commit gate took 21.9 minutes at a50-3 with 32 cases in the tree, so nothing needs retiring yet.

**The 17 called (a51-0, 2026-11-07).** [`decision_the-seventeen-called.md`](decision_the-seventeen-called.md): measuring the binary's own switches overturned this record's "no behaviour a reference could be compared on" for most of the 12. Its "What this route cannot close" stands as the record of what was believed at a46-0.
