# Requirement status derived

The catalogue's `implementation_status` is not carried; it is derived from the
evidence graph and drift-checked, as the policy's "Status and supersession"
section requires. `scripts/requirement_status.py` is the one derivation; the
`PROFILE-CONSISTENCY` gate runs it on every commit for every profile whose dossier
carries `EVIDENCE_POLICY.md`, and refuses a status that disagrees with its
derivation. The graph it reads is bounded and tracked: `requirements.sexp`, the
effective `contract-obligations.sexp`, and every retained evidence case's
predeclaration (`planned-experiment.sexp`, which names the requirement and
obligation ids a property addresses) and derived receipt (`verification.json`, a
complete capture that carries no verdict of its own), and — since a42ay (2026-10-23) —
the profile's credit catalogue `credits.sexp`, the one crediting word. This chapter, not
the policy document, names the checker: the policy is one of the reviewed inputs the
retained case pins by SHA256, so editing it is a re-capture, not a note.

| Derived status | Rule |
| --- | --- |
| `not-applicable` | applicability `excluded` and source category `not-applicable` together — the explicit, checked argument; one without the other is a finding |
| `implemented` | research `resolved`, included, every effective obligation the requirement names credited by at least one case |
| `partial` | a credited case or an `implementation_refs` entry exists but closure is incomplete; an unresolved source question caps the requirement here |
| `planned` | no credited implementation or evidence; pending, failed, stale or refused cases are reported as uncredited, never counted |

## How a case is credited

A credited disposition is a `(credit …)` record in `profiles/<profile>/credits.sexp`
(schema `schema/credits.sexp`, validated by RECORD-SCHEMA like the other catalogues). It
names the requirement, the effective obligations and the case, pins the measured record,
the receipt and the policy document by path, SHA256 and size, and names the retained
sources it rests on, its authority, date, decision record and limitations.
`scripts/credit_records.py` reads the catalogue and reports each record `current` or
`lapsed`: current only while every pin and every input of the case's dependency manifest
still describe the tree, the receipt is a complete canonical capture with `qualification`
false, and the declaration binds the credited requirement and obligations. The derivation
credits a binding only through a current record naming its case, requirement and
obligation. A receipt whose `qualification` is true is a finding — a typed success word —
and so is a lapsed record or one naming an unknown case or requirement: a moved pin lapses
the credit, the status falls back, the recorded status drifts and the gate fails. The
policy review reports `credited` from the same catalogue and makes a record over a
measurement that is not `satisfied` a finding (`decision_credit-is-a-catalogue-record.md`).

Since a45-1 an included requirement may not name a superseded obligation (RECORD-SCHEMA's `SUPERSEDED OBLIGATION`): eight once did, and no credit could have closed them. One, `REQ-D-RESOLUTION-ROUTE`, is `not-applicable`, a stage that ended (`decision_requirements-bound-to-the-effective-contract.md`).

A case naming an obligation outside the effective contract, or a requirement the
catalogue does not hold, is a finding: supersession preserves the old record and
edge and credits no successor by name.

**Today 16 requirements derive `planned`, 30 `implemented` and two `not-applicable`, and all four state requirements are among the 30.**
The window that carries fetch faults retired all 19 earlier records on 2026-11-06 (`P4-SYSTEM.14` a49-1; `decision_the-window-that-carries-fetch-faults.md`), and credited them again the same day (a49-3): each case re-captured once, the 17 with unchanged guests byte-identical, under an eleventh leg that reads a requirement's every clause.
The window that opens SSTC retired all four earlier records on 2026-11-05 (`P4-SYSTEM.14` a43e-1; `decision_sstc-delivery-needs-the-pinned-window.md`), and it closed the same day (a43e-5):
each case re-captured once, its traces byte-identical, and credited again, with SSTC on the same tools.

```text
$ python3 -B scripts/credit_records.py --profile rv64gc-lab-v0
CREDIT-RECORDS: rv64gc-lab-v0: 30 credit(s), 30 current, 0 lapsed; records read and authenticated, nothing granted
```

No recorded status drifts. The records:

| Requirement | Record | Case | Category, risk |
| --- | --- | --- | --- |
| `REQ-GC-M` | `CR-GC-M-5` | `rv64gc-m-forms-v7` | `defined`, medium |
| `REQ-D-XLEN`, the first `state` requirement | `CR-D-XLEN-4` | `rv64gc-xlen-forms-v4` | `defined`, low |
| `REQ-D-CSR-SET`, the first `implementation-defined` one | `CR-D-CSR-SET-3` | `rv64gc-csr-set-v3` | `implementation-defined`, high |
| `REQ-D-ZICNTR` | `CR-D-ZICNTR-3` | `rv64gc-zicntr-v3` | `implementation-defined`, high |
| `REQ-D-SSTC`, the first with a delivered interrupt | `CR-D-SSTC-2` | `rv64gc-sstc-v2` | `implementation-defined`, high |
| `REQ-D-ALU-IMM` | `CR-D-ALU-IMM-2` | `rv64gc-alu-imm-v2` | `defined`, low |
| `REQ-D-ALU-REG` | `CR-D-ALU-REG-2` | `rv64gc-alu-reg-v2` | `defined`, low |
| `REQ-D-LUI-AUIPC` | `CR-D-LUI-AUIPC-2` | `rv64gc-lui-auipc-v2` | `defined`, medium |
| `REQ-D-JALR-LSB` | `CR-D-JALR-LSB-2` | `rv64gc-jalr-lsb-v2` | `defined`, medium |
| `REQ-D-NO-DELAY-SLOTS` | `CR-D-NO-DELAY-SLOTS-2` | `rv64gc-no-delay-slots-v2` | `defined`, low |
| `REQ-D-SHAMT` | `CR-D-SHAMT-2` | `rv64gc-shamt-v2` | `defined`, high |
| `REQ-D-WSUFFIX` | `CR-D-WSUFFIX-2` | `rv64gc-wsuffix-v2` | `defined`, high |
| `REQ-D-LOAD-EXT` | `CR-D-LOAD-EXT-2` | `rv64gc-load-ext-v2` | `defined`, high |
| `REQ-D-LOAD-X0` | `CR-D-LOAD-X0-2` | `rv64gc-load-x0-v2` | `defined`, high |
| `REQ-D-ECALL-EBREAK` | `CR-D-ECALL-EBREAK-2` | `rv64gc-ecall-ebreak-v2` | `defined`, high |
| `REQ-GC-CSR-ACCESS` | `CR-GC-CSR-ACCESS-2` | `rv64gc-csr-access-v2` | `defined`, high |
| `REQ-GC-COUNTERS` | `CR-GC-COUNTERS-2` | `rv64gc-counters-v2` | `defined`, medium |
| `REQ-GC-FENCEI` | `CR-GC-FENCEI-2` | `rv64gc-fencei-v2` | `defined`, low |
| `REQ-D-IALIGN-16` | `CR-D-IALIGN-16-2` | `rv64gc-ialign-16-v2` | `defined`, medium |
| `REQ-GC-ATOMICS` | `CR-GC-ATOMICS-1` | `rv64gc-atomics-v1` | `defined`, high |
| `REQ-GC-C`, the first with a fetch fault | `CR-GC-C-1` | `rv64gc-c-forms-v1` | `defined`, medium |
| `REQ-GC-F` | `CR-GC-F-1` | `rv64gc-f-forms-v1` | `defined`, high |
| `REQ-GC-D` | `CR-GC-D-1` | `rv64gc-d-forms-v1` | `defined`, high |
| `REQ-D-SVADE` | `CR-D-SVADE-1` | `rv64gc-svade-v1` | `implementation-defined`, medium |
| `REQ-D-ATOMIC-MISALIGN` | `CR-D-ATOMIC-MISALIGN-1` | `rv64gc-atomic-misalign-v1` | `implementation-defined`, medium |
| `REQ-D-FAULT-PRIORITY` | `CR-D-FAULT-PRIORITY-1` | `rv64gc-fault-priority-v1` | `implementation-defined`, medium |
| `REQ-D-PRIV-MODES` | `CR-D-PRIV-MODES-1` | `rv64gc-priv-modes-v1` | `implementation-defined`, high |
| `REQ-D-SV39` | `CR-D-SV39-1` | `rv64gc-sv39-v1` | `implementation-defined`, high |
| `REQ-D-RESERVATION` | `CR-D-RESERVATION-1` | `rv64gc-reservation-v1` | `implementation-defined`, medium |
| `REQ-D-SC-DETERMINISTIC` | `CR-D-SC-DETERMINISTIC-1` | `rv64gc-sc-deterministic-v1` | `implementation-defined`, medium |

The last four are Batch II-b (`decision_batch-ii-b-credited-implemented.md`), new at a49-3. The five before them are Batch II-a (`decision_batch-ii-a-credited-implemented.md`), and the nine before those Batch I (`decision_batch-i-credited-implemented.md`). The first four re-issue their predecessors on the same rulings and limitations: `CR-GC-M-3`, `CR-D-XLEN-2`, `CR-D-CSR-SET-1` and `CR-D-ZICNTR-1`, whose cases are history since a43e-1. The other eight cases are uncredited, read as history on [the retained cases](retained-cases.md). Below, a record's claims are read against its current id.

An earlier window did the same to the first two (`P4-SYSTEM.14` a43b-2e, 2026-11-02):
the planned lapse that opens CSR-SET (a43b-2b; `decision_producer-debt-paid-before-the-next-case.md`)
moved pinned inputs of the cases `CR-GC-M-2` (v4, a44-5) and `CR-D-XLEN-1` (xlen-v1, a43a-3) named,
so both were removed with the catalogue file and the statuses read `planned` until the cases were
re-captured with their control declared (a43b-2c, a43b-2d) and credited again. The other four cases
were uncredited at `pending`: v2, v3 (`CR-GC-M-1` from 2026-10-26 until a44-2b), v4 and xlen-v1. The probe `scripts/probe_requirement_status.py` runs 23
synthetic-graph tests in both interpreter modes and eight seam omissions that each fail
their discriminating test. Nothing here advances a status: a credit record, with the recorded
status moving in the same commit, is the crediting act (a42az for `CR-GC-M-1`, a44-5 for its
re-issue `CR-GC-M-2`, a43a-3 for `CR-D-XLEN-1`, both retired at a43b-2b, a43b-2e for `CR-GC-M-3` and
`CR-D-XLEN-2`, a43b-3h for `CR-D-CSR-SET-1`, and a43c-5 for `CR-D-ZICNTR-1`, all four retired at a43e-1, a43e-5 for the first five records above, a46-4 for the next nine, a47-3 for the next five, all 19 retired at a49-1, a49-3 for all 23, and a50-4 for the last seven), under the rulings on its authority and on the
sufficiency of one finite case (`decision_req-gc-m-credited-implemented.md`). The normative text each
rests on is retained (`RVI-M-DIV-STATEMENT`, and `RVI-M-STATEMENTS` since a42bb; `RVI-RV64I-STATEMENTS`
since a43a-2a; `RVP-CSR-STATEMENTS` since a43b-3b; `RVI-ZICNTR-STATEMENTS` and `RVP-COUNTEREN-STATEMENTS` since a43c-1; `RVP-SSTC-STATEMENTS`, `RVP-STIMECMP-STATEMENTS` and `RVP-STCE-STATEMENTS` since a43d-2; `RVI-RV32I-STATEMENTS` and `RVI-RV64I-FORMS-STATEMENTS` since a46-1; `RVP-ECALL-STATEMENTS`, `RVI-ZICSR-STATEMENTS`, `RVI-ZIFENCEI-STATEMENTS` and `RVI-C-STATEMENTS` since a47-1).

`CR-D-CSR-SET-2` claims the committed set, and its record says what that leaves out
(`decision_req-d-csr-set-credited-implemented.md`):

| Not claimed | Why | Whose it is |
| --- | --- | --- |
| `mip`'s value directly | the case's CLINT holds `mip.MTIP`; `mip` is read with `rd` = x0 and its bits witnessed through `sip` | this case's configuration |
| a CLINT or any device | it is the reference's source of time for this case; the laboratory declares none | not claimed |
| a non-member address trapping | the spec-side deriver's vocabulary is the 33, and it is a pinned input | not witnessed; the negative side is the refused write and the privilege-refused access |
| field semantics | "Per-CSR field semantics (WPRI/WARL/WLRL) belong to the privilege leaf" | `P4-SYSTEM.2` |
| counter rates, timer delivery, numerics | each is witnessed as a member of the set, not as its behaviour | `REQ-D-ZICNTR`, `REQ-D-SSTC`, the F and D cases |

Its dependency `REQ-D-PRIV-MODES` stayed `planned` until a50-4: the derivation reads obligations, not dependencies.

`CR-D-ZICNTR-2` claims what the case read: the three base counters and the two machine views in M, their
progress, five refused write attempts with `rd` kept, a trap that retires nothing, each gate bit of `mcounteren` and
`scounteren` in S and U, and two alias pairs. Its record says what that leaves out
(`decision_req-d-zicntr-credited-implemented.md`):

| Not claimed | Why | Whose it is |
| --- | --- | --- |
| a write through `mcycle` or `minstret` | the spec-side deriver refuses it, and the laboratory's `time` is a view of `mcycle` where the reference's comes from its CLINT, so a write would separate them | not witnessed |
| Zihpm's absence | the deriver's vocabulary is the 33 | not witnessed; a statement of the selection |
| rate and progress semantics | "the counters' rate and progress semantics are the environment contract's to declare" | `P4-SYSTEM.5`, `P4-SYSTEM.9` |
| a CLINT or any device | it is the reference's source of time for this case; the laboratory declares none | not claimed |
| timer delivery | no interrupt or wait is scheduled | `REQ-D-SSTC` |

Its dependency `REQ-D-PRIV-MODES` stayed `planned` for the same reason as CSR-SET's.

`CR-D-SSTC-1` claims what the case read, and it is the first to witness delivery itself: `stimecmp` in M and all 64 bits, each gate alone with `rd` kept, the kernel programming its own timer, STIP below and at the compare, five suppressions under four conditions, delivery from S, from U and to M, one schedule, and its acknowledgement. Its record says what that leaves out (`decision_req-d-sstc-credited-implemented.md`):

| Not claimed | Why | Whose it is |
| --- | --- | --- |
| a scheduled delivery's latency | the statement guarantees a changed comparison reaches STIP "eventually, but not necessarily immediately"; the exact boundary is what both producers do on this configuration | not claimed |
| `mtimecmp` or any M-mode timer | not in this case | not witnessed |
| `wfi`'s wake | no wait is scheduled | `P4-SYSTEM.5` |
| the rate of `time` | the environment contract's to declare | `P4-SYSTEM.5`, `P4-SYSTEM.9` |
| a CLINT or any device | it is the reference's source of time for this case; the laboratory declares none | not claimed |

Its dependency `REQ-D-PRIV-MODES` stayed `planned` too.

**No measured record is copied into `references.sexp`.** A third copy would have taken the file to 77,669 B against the family's 65,536 B per-part ceiling, and the director ruled on 2026-11-04 (`decision_dossier-copies-retire-at-the-next-window.md`) that the next pinned window retire them all. That window was this one: the copies left at a43e-1, and since a43e-5 `gate_report.py` reads each credited case's record from `evidence/`. `G-TRACE` lists all 23, and each row is evidence only while its credit is current:

```text
$ python3 -B scripts/gate_report.py rv64gc-lab-v0 --gate GS --stdout | grep 'G-TRACE. | .experiment' | tail -1
| `G-TRACE` | `experiment` | experiment `rv64gc-sc-deterministic-v1` | yes |
```

Without `tail` it prints all 30. A credited case with no row keeps the axis open and names the case, so "every credited case" is a check and not a promise. The window also moved `contract_measure` out of `gate_report.py` into `scripts/effective_contract.py`, the one import that made a report generator a pinned input of every experiment. a43e-5 was the proof: it edited `gate_report.py`, and all five credits stayed current.

## The route for the rest (`P4-SYSTEM.14` a46-0, 2026-11-06)

The tool the seven with a switch need landed at a50-1: [a case may declare what selects otherwise](references.md#when-the-override-is-the-selection). The seven's cases were declared at a50-2, captured once each at a50-3 (`decision_seven-with-a-switch.md`) and credited at a50-4 (`decision_seven-credited-implemented.md`). When this route was set, 42 were `planned`; Batches I, II-a and II-b and the seven have since credited twenty-five, which left 17. [How each of those closes](#how-the-last-17-close-p4-system14-a51-0-2026-11-07) was called at a51-0, and `REQ-D-SBI` left the CPU's scope, so 16 remain. `G-OBLIGATIONS` stays open on them, and each already has its two contract checks realized. What is missing is the matched comparison and a credit. Run the corpus against the pinned Sail yourself, with nothing retained:

```text
$ python3 -B scripts/census_reference_config.py --case rv64gc-sstc-v2 --out target/reference-config-census/sstc
204 guests
 175  profile AGREE -> case AGREE
```

When the route was set the corpus held 182 guests, and 167 of them agreed on at least one of the two configurations. Crossed with each obligation's checks (`decision_obligations-route.md`):

| Class | Count | Route |
| --- | --- | --- |
| Guests named, and Sail agrees | 15 | A case each, in batches |
| A witness in Rust, so a program must be authored | 13 | A case each, in batches |
| A statement of selection, checked by a scope predicate | 12 | Raised to the director after the batches |
| Behaviour Sail does not show: `wfi`'s stall, injected faults | 2 | May rightly end `partial`; the engineer's call, recorded and reported |

Batch II found what that table had not: ten of the 28 are `implementation-defined`, a category the review measures against a case's own configuration, and for them the profile's override is the selection. The pinned Sail has a real switch for most of them, so a behaviour-changing control exists; the tool does not read one yet (`decision_obligations-route.md`, "What Batch II found").

The batches run one case per requirement, so no pinned file moves and no credit lapses: five batches of three commits against about 140 commits one case at a time. **Batch I, the RV64I base, is done:** declared at a46-2, captured at a46-3, credited at a46-4. Nine cases, 108 witnesses, each program agreeing with all three producers, each 10 of 10 legs. **So is Batch II-a, the five `defined` requirements of system:** `ECALL-EBREAK`, `CSR-ACCESS`, `COUNTERS`, `IALIGN-16`, `FENCEI`, credited at a47-3. **So is the `defined` remainder:** `ATOMICS`, `C`, `F`, `D`, 299 witnesses, credited at a49-3 on the tools of a window that let a case carry a fetch fault and the review read a requirement's every clause (`decision_the-window-that-carries-fetch-faults.md`). Batch II-a was rehearsed end to end on a throwaway clone first, which found two faults a real capture would have spent a case id on. The estimate's weakest number, how much each case adds to the gate, read about 20 seconds per captured case, against a limit of a minute.

## How the last 17 close (`P4-SYSTEM.14` a51-0, 2026-11-07)

The route left 17 at a ruling, 12 of them as selections with "no behaviour a reference could be compared on". Measuring the binary's own switches, all 198 guests under each, showed otherwise: `H` on moves 45 guests' verdicts, 16 PMP entries move 51, and `--trace-ptw` and `--trace-mem` print the walks the route thought were out of reach.

| Track | Requirements | How it closes |
| --- | --- | --- |
| A real case, `defined` | `REQ-D-GC-COMPOSITION`, `REQ-D-EXT-CLOSURE`, `REQ-D-PRIV-REVISION`, `REQ-D-RVWMO`, `REQ-D-PRIV-INSNS`, `REQ-GC-PRIV-INSNS` | One case each, on today's tools |
| A real case with a switch | `REQ-D-NO-H`, `REQ-D-NO-PMP` | A declared alternative, measured as the seven's were |
| A real case, no switch to move | `REQ-D-ENDIAN`, `REQ-D-FENCE`, `REQ-D-WALK-IMPLICIT`, `REQ-GC-PARTIAL-PROGRESS` | `source-specific`, with a disposition declared first |
| Nothing to run | `REQ-D-ABI`, `REQ-D-FP-DEFER`, `REQ-D-ROUTE-FLIP`, `REQ-D-SCOPE-CENSUS` | `source-specific`, with a record pinning the facts and naming its controls |
| Out of the CPU's scope | `REQ-D-SBI` | `not-applicable`, done; `P6-LINUX.2` is its successor |

The policy's text is unchanged, so no credit lapsed for this. Read `decision_the-seventeen-called.md` for each argument and what each leaves out. If a call fails on its measurement, that record reopens it. The first track's six cases are declared since a51-1, not yet captured or credited, so they still read `planned`.

```text
$ python3 -B scripts/requirement_status.py --profile rv64gc-lab-v0 2>&1 | tail -1
REQUIREMENT-STATUS: ok (rv64gc-lab-v0: 48 requirements derived 16 planned, 30 implemented, 2 not-applicable; 32 case(s), 30 credited, 0 declared, 30 of 30 credit record(s) current; 0 drift, 0 finding(s))
```
