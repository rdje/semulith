# Policy legs measured

The evidence policy names, for a requirement's source-semantic category and risk, what a
credited disposition needs. `scripts/review_div_policy.py` reads those requirements as ten
legs and measures each one against the retained bytes of every case the finite method review
holds a reviewed capture for — since a43e-5 (2026-11-05) `rv64gc-m-forms-v6`, `rv64gc-xlen-forms-v3`, `rv64gc-csr-set-v2`,
`rv64gc-zicntr-v2` and `rv64gc-sstc-v1`, since a46-4 (2026-11-06) Batch I's nine and since a47-3 Batch II-a's five, each re-issued at a49-3 with Batch II-b's four and read by eleven legs, and all 42 captured and credited again under new ids in version 1's window (`P4-SYSTEM.20` f1 to f3, 2026-11-14); every earlier case is history below, and most have [left the tree](retired-cases.md) — on top of the finite method review. It opens only
bounded tracked files, launches no process and grants no credit: `credited` reports a separately
owned record in `credits.sexp`, never the measurement. Both cases measured every leg satisfied and were
credited — the M case by `CR-GC-M-2`, the XLEN case by `CR-D-XLEN-1` (a43a-3) — until the planned lapse that
opens CSR-SET (`P4-SYSTEM.14` a43b-2b, 2026-11-02) moved pinned inputs of both captures, which read
`invalidated`, 8 of 10 legs, their credits retired. Re-captured once each as v5 and xlen-v2, traces byte-identical
(a43b-2d), both measure every leg satisfied again and are credited by `CR-GC-M-3` and `CR-D-XLEN-2` (a43b-2e); the
tables below are the measurements of their predecessors, which the re-captures reproduce. **The window that opens SSTC did the same (`P4-SYSTEM.14`
a43e-1 … a43e-5, 2026-11-05):** four captures read `invalidated`, 8 of 10 legs, their credits retired, until each was re-captured once, traces byte-identical, and credited again. Each table below names the case it measured; the re-captures reproduce it.

## The eleventh leg: every clause of the statement (a49-1)

`EVIDENCE_POLICY.md` declares it, "Statement trace". A case can cover every form, agree with the reference on every step, and leave clauses of its requirement's statement unread: first drafts of the A, C, F and D cases did, and reading the 19 credited statements clause by clause found two more the ten legs had passed. So `profiles/rv64gc-lab-v0/statement-trace.sexp` splits each statement into clauses, and `scripts/statement_trace.py` holds it on every read:

| Held | Refused when |
| --- | --- |
| The clauses' words, in order, are exactly the statement's | a clause is skipped, reordered or added to |
| Each clause names declared properties, a limit, or both | a clause names neither |
| A named property is one the case declares | it names a witness that is not there |
| A limit is a literal part of the case's `limitation` | it names a limit the case does not state |
| Every declared property stands for some clause | a witness goes unread |

```text
$ python3 -B scripts/statement_trace.py --profile rv64gc-lab-v0 | tail -1
STATEMENT-TRACE: rv64gc-lab-v0: 46 of 46 requirements with a declared trace; annotation, not proof of semantics
$ python3 -B scripts/statement_trace.py --profile rv64gc-lab-v0 --requirement REQ-D-LOAD-X0
A load with rd = x0 must still raise any exceptions
    witness: lb-x0-faults
    …
and cause any other side effects,
    limit: the other side effects a load may cause are not witnessed
even though the loaded value is discarded.
    witness: x0-reads-zero
```

**What it found.** With the first trace written:

| Requirement | The clause | What the ten legs had passed |
| --- | --- | --- |
| `REQ-GC-CSR-ACCESS` | "a satp access in S with mstatus.TVM=1" | No witness and no limit: now `satp-tvm-cause`, `satp-tvm-rd-kept` |
| `REQ-GC-CSR-ACCESS` | "csrrs/csrrc with rs1=x0 and csrrsi/csrrci with uimm=0" | Half witnessed: now `csrrc-x0-no-write`, `csrrci-zero-no-write` |
| `REQ-GC-FENCEI` | "a fence.i word with nonzero fields executes, never raises" | No witness and no limit: now `fence-i-fields-ignored` |
| `REQ-GC-FENCEI` | "a store to a later-fetched address is visible to the next fetch immediately" | Named only as a limit: now `store-visible-without-fence` |
| `REQ-D-IALIGN-16` | "while ILEN remains 32" | No witness and no limit: now a named limit, `REQ-GC-C`'s all-ones case holding it |

**What it does not do.** A trace is annotation, not proof of semantics (RULES EVD-06): it says which witness a reader should hold a clause to, and that reader can still disagree. What it cannot do is leave a clause out. `scripts/probe_statement_trace.py` runs 15 tests in both interpreter modes and seven seam omissions, and the policy probe holds the leg itself.

## The ten legs and what the bytes say

| Leg | Policy words | Measured on the M case (v4) |
| --- | --- | --- |
| source-located-expectations | source-located expected observations; model output is not its own expectation | satisfied: 33 of 33 steps carry a derivation and a source; the witness step 12 cites `REQ-GC-M`'s source; the expected producer reads only its own inputs |
| boundary-fixtures | directed boundary fixtures | satisfied: 12 Table 1 rows present (steps 20–24, 26–32) and all 12 predeclared as properties |
| matched-reference-comparison | a matched public-reference comparison on the applicable observations | satisfied: method satisfied, baseline AGREE under `sail-gpr-change-v1`, vocabulary `gpr-change` named |
| repeated-execution | repeated execution | satisfied: repeat AGREE |
| discriminating-control | one discriminating negative control that fails for the stated reason | satisfied: control DIVERGE at step 12, register x15, the property the `control_run` names |
| record-linkage | requirement, effective obligation, tracked runner, producer, record, limitations | satisfied: `REQ-GC-M`, `OB-GC-M`, collector, expected producer, three limitations |
| currentness | relevant changes invalidate dependent evidence | satisfied: the policy document is pinned by the manifest and unchanged; the method binding matched |
| risk-method | high and critical risk need a second method | satisfied: medium risk needs none |
| feature-rules | the seven feature families | satisfied by declaration: none applies to `OB-GC-M` |
| form-coverage | every form the requirement names | satisfied: 13 of 13 forms predeclared and 13 exercised (`mul`, `mulh`, `mulhsu`, `mulhu`, `mulw`, `div`, `divu`, `rem`, `remu`, `divw`, `divuw`, `remw`, `remuw`) |

Ten legs satisfied, none pending; the disposition was `satisfied`, and from 2026-10-26 `credited` was true:
the record `CR-GC-M-1` in `credits.sexp` (signed `review` under `decision_four-rulings-delegated.md`, per
`decision_req-gc-m-credited-implemented.md`) credited the case, and `REQ-GC-M` derived `implemented`. Since
2026-10-29 the case is `invalidated`: `P4-SYSTEM.14` a44-2b moved pinned inputs of its capture (the matched
cases' declarations became data) and retired the record (that decision's Retirement), so the consumer reports
`DIV-POLICY: invalidated — 8 of 10 legs satisfied; missing matched-reference-comparison, currentness` and
`REQ-GC-M` derived `planned` until the M case's v4 capture was measured and credited. The same day the M case was
re-captured as `rv64gc-m-forms-v4` under the new manifest (a44-3 declared, a44-4 captured: traces byte-identical to
v3's), and this review now reads v4 (`CASE_ID`): `DIV-POLICY: satisfied — 10 of 10 legs satisfied; credited by
CR-GC-M-2` (a44-5), and `REQ-GC-M` derived `implemented` again — until a43b-2b, since which the line reads
`DIV-POLICY: invalidated — 8 of 10 legs satisfied; missing matched-reference-comparison, currentness; invalidated by
schema/matched-case.sexp: SHA256 differs; no qualification credit` — and since a43e-5 the review reads v6:
`DIV-POLICY: satisfied — 10 of 10 legs satisfied; credited by CR-GC-M-4`. The consumer reads boundary rows and forms from the
expectation file (a step whose source cites a chapter table row, or carries a `(boundary: …)` tag, is a directed
boundary fixture; a step's mnemonic is its form), never from the chapter itself.

## The XLEN case's ten legs (a43a-2f)

`REQ-D-XLEN` (XLEN = 64: the integer registers and the supported user address space are 64 bits) is a `state`
requirement of low risk under `OB-XLEN`; its case predeclares seventeen witnesses and one control
(`decision_reviews-read-every-retained-case.md`). Before a43a-2f the consumer measured it 7 of 10: it knew M's `Table`
rows only, it had no feature disposition for `OB-XLEN`, and it read a requirement naming no instruction as `0 of 0`
forms, pending. Now:

| Leg | Measured on the XLEN case |
| --- | --- |
| source-located-expectations | satisfied: 25 of 25 steps carry a derivation and a source; the witness step 24 cites `REQ-D-XLEN`'s source (`RVI-RV64I §3.1.1`) |
| boundary-fixtures | satisfied: 10 tagged rows (steps 1, 5–10, 13, 16, 24: bit 63, bit 32, a shift amount above 31, 2^63 − 1, the wrap at 2^63, the carry out of bit 63, bit 31 extended, the word's sign bit, `rs2[4:0]`, an address above 2^32), all predeclared |
| matched-reference-comparison | satisfied: method satisfied (88 authenticated files), baseline AGREE under `sail-gpr-change-v1` |
| repeated-execution | satisfied: repeat AGREE |
| discriminating-control | satisfied: control DIVERGE at step 24, register x31 (2^40 observed, 0 in the control's expectation) |
| record-linkage | satisfied: `REQ-D-XLEN`, `OB-XLEN`, collector, expected producer, three limitations |
| currentness | satisfied: the policy pinned and unchanged; the method binding matched |
| risk-method | satisfied: low risk needs no second method |
| feature-rules | satisfied by declaration: none applies to `OB-XLEN` — the access fault at 2^40 and the handler's `CSRRS` of `mtval` observe the address; no trap, CSR or protection behaviour is claimed |
| form-coverage | satisfied vacuously, and said so: a state requirement names no form; its 17 predeclared witnesses stand for it |

Measured at a43a-2f `DIV-POLICY: satisfied — 10 of 10 legs satisfied; no qualification credit`; since a43a-3 the
record `CR-D-XLEN-1` credited it, the line ending `credited by CR-D-XLEN-1` (`decision_req-d-xlen-credited-implemented.md`),
until a43b-2b retired it; its re-capture xlen-v2 measures 10 of 10 and is credited by `CR-D-XLEN-2` (a43b-2e),
two limitations fewer: its receipt names `REQ-D-XLEN` and its record carries its own control.

## The CSR-SET case: the first `implementation-defined` requirement

The policy asks this category for more than a matched comparison: "pinned matching reference configuration with a
behavior-changing control, or an explicitly observed and justified profile difference", and it calls "a configuration file
without an observed effect" insufficient. Until a43b-3g the comparison leg measured `defined`'s row for every case, so a
case on its own configuration would have satisfied it with the configuration alone. The leg now reads the category:

| Category | The comparison leg also needs | Measured text |
| --- | --- | --- |
| `defined` | nothing | unchanged, to the byte, for the M and XLEN cases |
| `implementation-defined` | the selection recorded in the catalogue, and a retained effect | `; category implementation-defined: selection recorded; observed effect under the profile override: step 34 …` |
| any other | pending until a row is written for it | `; category unspecified: no row measured for it here` |

The effect is [the run retained beside the overlay](references.md). The review trusts no verdict in it: it reads seven pins
against the case's own bytes, then re-derives the first difference offline. Each failure leaves the leg pending and names
what failed:

| The record must pin | Against | The leg then reads |
| --- | --- | --- |
| its case | the case id | `the retained effect does not pin its case` |
| the guest | `guest.elf`'s digest | `… does not pin the guest` |
| the case's configuration | `reference-config.json`'s digest | `… does not pin the case's configuration` |
| the binary | the reference producer's version | `… does not pin the reference producer's binary` |
| a different configuration | the alternative's digest is not the case's | `… does not pin a different configuration` |
| the alternative | the one the case declares, rendered by `prepare_div_inputs` ([a50-1](references.md#when-the-override-is-the-selection)), else the profile override as it renders it | `… does not pin its declared alternative`, `… does not pin the profile override` |
| its trace | the raw trace's digest and size | `… does not pin its trace` |
| *(re-derived)* a difference | the trace against the case's baseline expectation | `the retained effect reads AGREE: no observed effect` |
| *(re-derived)* at a witness | a declared property's step | `the retained effect first differs at step N, no declared property's` |

A record without its trace, or a malformed one, refuses (exit 2): that pair cannot be measured honestly. An alternative the tool refuses reads pending, `the case's declared alternative refuses: …`.

| Leg | Measured on `rv64gc-csr-set-v1` |
| --- | --- |
| source-located-expectations | satisfied: 157 of 157 steps carry a derivation and a source; witness step 130 cites `REQ-D-CSR-SET`'s source; the expected producer reads only its own inputs |
| boundary-fixtures | satisfied: seven `(boundary: …)` rows at steps 101, 111, 113, 136, 138, 144 and 156, all predeclared |
| matched-reference-comparison | satisfied: method satisfied (88 authenticated files), baseline AGREE under `sail-gpr-change-v1`, the selection recorded, the effect observed at step 34 |
| repeated-execution | satisfied: repeat AGREE |
| discriminating-control | satisfied: control DIVERGE at step 130, register x28 (5 observed, 9 in the control's expectation) |
| record-linkage | satisfied: `REQ-D-CSR-SET`, `OB-CSR-SET`, collector, expected producer, three limitations |
| currentness | satisfied: the policy pinned and unchanged; the method binding matched |
| risk-method | satisfied: high risk, second method `independent-exact-expectation` by `expected` and `reference` on the guest source and the manifest; ancestry recorded, no independence credit; the seven refused-access properties executed |
| feature-rules | satisfied by declaration: the privilege and CSR rule applies, and the disposition names the properties that cover it; the probe checks that each of its 20 names is one this case declares |
| form-coverage | satisfied vacuously, and said so: a state requirement names no form; its 53 predeclared witnesses stand for it |

```text
$ python3 -B scripts/review_div_policy.py --every-retained
rv64gc-m-forms-v8: DIV-POLICY: satisfied — 11 of 11 legs satisfied; credited by CR-GC-M-6
rv64gc-xlen-forms-v5: DIV-POLICY: satisfied — 11 of 11 legs satisfied; credited by CR-D-XLEN-5
rv64gc-csr-set-v4: DIV-POLICY: satisfied — 11 of 11 legs satisfied; credited by CR-D-CSR-SET-4
rv64gc-zicntr-v4: DIV-POLICY: satisfied — 11 of 11 legs satisfied; credited by CR-D-ZICNTR-4
rv64gc-sstc-v3: DIV-POLICY: satisfied — 11 of 11 legs satisfied; credited by CR-D-SSTC-3
rv64gc-alu-imm-v3: DIV-POLICY: satisfied — 11 of 11 legs satisfied; credited by CR-D-ALU-IMM-3
```

That is six of the 42 lines, one per retained capture; the other 36 read the same, each with its own credit.

Inside this window (a49-1, a49-2) the predecessors' lines read `DIV-POLICY: invalidated — 9 of 11 legs satisfied; missing matched-reference-comparison, currentness`, as version 1's did from slice a to f1, until a49-3 named their successors. Inside the window before it (a43e-1 … a43e-4) the retired cases' lines read `DIV-POLICY: invalidated — 8 of 10 legs satisfied; missing matched-reference-comparison, currentness`. The CSR-SET case was measured at a43b-3g with `no qualification credit`; a record has credited it since a43b-3h
(`decision_req-d-csr-set-credited-implemented.md`).

`rv64gc-zicntr-v1` is the second case through that branch, and the review needed no change for it (a43c-5). Its feature disposition is the
first to name the counter rule, "Counters, interrupts, wait and progress checks record scheduled time/events, delivery boundaries and
suppression cases. Host timing is not guest time.":

| Leg | Measured on `rv64gc-zicntr-v1` |
| --- | --- |
| source-located-expectations | satisfied: 292 of 292 steps carry a derivation and a source; witness step 109 cites `REQ-D-ZICNTR`'s source; the expected producer reads only its own inputs |
| boundary-fixtures | satisfied: 26 `(boundary: …)` rows from step 22 to step 291, all predeclared |
| matched-reference-comparison | satisfied: method satisfied (88 authenticated files), baseline AGREE under `sail-gpr-change-v1`, the selection recorded, the effect observed at step 6 |
| repeated-execution | satisfied: repeat AGREE |
| discriminating-control | satisfied: control DIVERGE at step 109, register x21 (21 observed, 102 in the control's expectation) |
| record-linkage | satisfied: `REQ-D-ZICNTR`, `OB-ZICNTR`, collector, expected producer, three limitations |
| currentness | satisfied: the policy pinned and unchanged; the method binding matched |
| risk-method | satisfied: high risk, second method `independent-exact-expectation` by `expected` and `reference` on the guest source and the manifest; ancestry recorded, no independence credit; the 13 rd-kept properties executed |
| feature-rules | satisfied by declaration: the counter rule and the privilege and CSR rule apply, and the disposition names the properties that cover them; the probe checks that each of its 26 names is one this case declares |
| form-coverage | satisfied vacuously, and said so: a state requirement names no form; its 44 predeclared witnesses stand for it |

The disposition reads the counter rule's three parts honestly. The schedule is the step boundary itself, a guest count and never host time, and each value is
recorded at its declared boundary. The suppression is the trap that retires nothing. Nothing is delivered, because no interrupt or wait is scheduled, so timer
delivery stays with `REQ-D-SSTC` and rates with the environment contract.

`rv64gc-sstc-v1` is the third case through that branch, and the review needed no change for it either (a43e-5). Its disposition is the first to witness all of the counter rule rather than to say why a part does not apply:

| Leg | Measured on `rv64gc-sstc-v1` |
| --- | --- |
| source-located-expectations | satisfied: 315 of 315 steps carry a derivation and a source; witness step 172 cites `REQ-D-SSTC`'s source; the expected producer reads only its own inputs |
| boundary-fixtures | satisfied: 17 `(boundary: …)` rows from step 33 to step 313, all predeclared |
| matched-reference-comparison | satisfied: method satisfied (88 authenticated files), baseline AGREE under `sail-gpr-change-v1`, the selection recorded, the effect observed at step 8 |
| repeated-execution | satisfied: repeat AGREE |
| discriminating-control | satisfied: control DIVERGE at step 172, register x11 (0 observed, 32 in the control's expectation) |
| record-linkage | satisfied: `REQ-D-SSTC`, `OB-SSTC`, collector, expected producer, three limitations |
| currentness | satisfied: the policy pinned and unchanged; the method binding matched |
| risk-method | satisfied: high risk, second method `independent-exact-expectation` by `expected` and `reference` on the guest source and the manifest; ancestry recorded, no independence credit |
| feature-rules | satisfied by declaration: the counter rule and the privilege and CSR rule apply, and the disposition names every one of the 39 properties; the probe holds that set equal to the case's declaration |
| form-coverage | satisfied vacuously, and said so: a state requirement names no form; its 39 predeclared witnesses stand for it |

The counter rule's three parts, each witnessed. Scheduled events are guest counts at declared boundaries, never host time, with pending read below and at the compare. Delivery boundaries are witnessed from S, on a schedule, from U and to M, each a boundary of its own in the case that fetches nothing and writes nothing, which is what the window added. Suppression is witnessed under four conditions: STIE clear, SIE clear in S, delegated while in M, and STCE clear, that last twice. One thing is held back: a scheduled delivery's exact boundary is what both producers do on this configuration, not a latency claim, and the disposition says so. No wait is scheduled, so `wfi`'s wake stays `P4-SYSTEM.5`'s.

**A form that writes no GPR (a46-4).** The form-coverage leg counts a form as predeclared at a witness of its own step. A branch, a store and a load to `x0` write no GPR, so they have no change to witness there, in this vocabulary. Such a form is also predeclared when a property's cell names it and that witness comes after a step of the form: the read that observes it, stated by the property. A form with any GPR write gets no such route, and neither does one never exercised. On `rv64gc-load-ext-v1` the leg reads:

```text
11 of 11 forms predeclared ['lb', 'lbu', 'ld', 'lh', 'lhu', 'lw', 'lwu', 'sb', 'sd', 'sh', 'sw']; 11 exercised [...]; writing no GPR, read after their own step: ['sb', 'sd', 'sh', 'sw']
```

**A declared disposition (a51-7, a51-8).** The policy allows one: "Any alternative disposition needs an explicit source-grounded argument and its own controls before execution; it cannot be manufactured by relabeling an unrelated passing result." The leg reads it from `profiles/<profile>/dispositions.sexp` (`schema/dispositions.sexp`, `scripts/dispositions.py`), one record per requirement. It applies to an `implementation-defined` requirement the pinned reference offers nothing to select otherwise for, and to a `source-specific` one, whose row is exactly this. A record of `kind case` must name this case's own declared control, or the leg reads pending. Such a requirement keeps the category its source gives it, which is why `REQ-D-ENDIAN` still reads `implementation-defined`. RECORD-SCHEMA holds the two together: a record answering a requirement of another category is a finding, and so is a `source-specific` requirement with no record. See [how the last 17 close](requirement-status.md#how-the-last-17-close-p4-system14-a51-0-2026-11-07).

**A `memory` requirement naming no form (a51-1).** `REQ-D-RVWMO` says what one hart sees of the memory model and names no form, so the same reading holds. And `REQ-D-PRIV-INSNS`, an `instruction` requirement that named none, read pending as the rule says, which was a fault in the catalogue: its four instructions are named now.

**A `configuration` requirement naming no form (a47-3).** The leg allowed a requirement to name no form only for kind `state`. `REQ-D-IALIGN-16` says where an instruction may start and names none, so the same reading holds, and the leg says `a configuration requirement names no form: coverage is vacuous, its 6 predeclared witnesses stand for it`. An `instruction` or `event` requirement naming no form stays pending: that would be a fault in the catalogue.

## What a satisfied measurement is, and is not

The measurement says the retained bytes of one case meet every leg the policy names for its
category and risk. It is not a credit: the policy makes a satisfied
measurement the input to a separately owned crediting record, and a retained receipt is never
replaced (`decision_ten-legs-satisfied-credit-separate.md`). Since a42ay (2026-10-23) that
record has a shape and a reader: a `(credit …)` record in `profiles/rv64gc-lab-v0/credits.sexp`
that `scripts/credit_records.py` re-authenticates on every read, and that the
[status derivation](requirement-status.md) alone credits through. This consumer reports
`credited` from that catalogue — the summary ends `credited by <record>` instead of `no
qualification credit` — and makes a record over a measurement that is not `satisfied` a
finding (`decision_credit-is-a-catalogue-record.md`). The catalogue holds no record: writing
the first one is the crediting act, and it is the director's. The normative text such a record
would rest on is retained: the DIV/DIVU statement (`retained/div-statement.html`, a42z) and, since
a42bb, the eleven other M statements and Table 1 (`retained/m-statements.html`, `RVI-M-STATEMENTS`;
`decision_m-statements-retained.md`).

## History: the first case and its two pending legs

Measured on `rv64gc-signed-div-truncation-v2` (a42aq, 2026-10-21), eight legs were satisfied
and two pending: six Table 1 rows were present (steps 10–13, 17, 19) and none predeclared as
a property; `div` alone was predeclared, four forms exercised, thirteen required. They could
not be closed by relabeling — the policy credits only declared observations, and declaring
the rows for retained bytes is a new predeclaration the retained-identity controls refuse
(`decision_policy-legs-measured-two-pending.md`). The m-forms program below predeclared them;
its capture (a42aw) is the retained case now, and the first case is `invalidated` history.

The policy document is one of the reviewed inputs each case pins by SHA256 (64 for the two retained captures;
67 for a case reviewed since a44-2b, which adds its declaration, the declaration's schema and its reader). An edit to
it changes the dependency manifest's expected bytes and refuses the finite method, so the
currentness leg fails until a fresh capture: a policy change is a capture, not a note.

## What the consumer refuses

A receipt whose `qualification` is true while any leg is pending is a finding and fails
`PROFILE-CONSISTENCY` ("No typed success word substitutes for executed evidence"). A refused,
unavailable or unsupported finite method leaves the legs measured but `blocked`. A high- or
critical-risk requirement stays pending until its case declares a second method and an
adversarial case that meet the five conditions below. An obligation without a declared feature disposition stays
pending; the disposition is never inferred from the mnemonics. A control that diverges
somewhere other than the step and register of the property the `control_run` names is not the
stated reason; the leg reads that property, not the first one declared (a42at).

## The second method, first for CSR-SET (a43b-2b)

`REQ-D-CSR-SET` is `(risk high)`: its case can be credited only once it says what its second
method and adversarial case are. Since a43b-2b (2026-11-02) a case declaration may carry two
optional forms (`schema/matched-case.sexp`), as CSR-SET's will:

```lisp
(second_method (kind "independent-exact-expectation")
               (producer_ids "expected") (producer_ids "reference")
               (common_input_ids "guest-source") (common_input_ids "dependency-manifest")
               (independently_derived "The expected values are derived from the pinned privileged chapters by the source author, with no reference output among its inputs."))
(adversarial (property_ids "csr-mhartid-write-refused") (property_ids "csr-mscratch-refused-from-s")
             (failure_mode "A forbidden CSR write or access commits its destination or another architectural side effect."))
```

(The property ids and texts are illustrative; CSR-SET's own unit declares the real ones.) `kind` is one of
the policy's four named methods as a token — `independent-exact-expectation`,
`bounded-exhaustive-check`, `source-grounded-invariant-check`, `qualified-hardware-observation`; the
policy's text stays the authority. The review reads both forms from the case's `case.sexp`, which its
manifest pins (so the method review's currentness authenticates it), and judges them against the
record's own graph — the declaration restates nothing the record holds. A declaration is judged at
any risk, never ignored, by five conditions; the cell names, numbered, every one that fails:

| # | Condition | What it rules out |
| --- | --- | --- |
| 1 | a second method of one of the four kinds and an adversarial case are both declared | a declaration with nothing to judge |
| 2 | its producers are two or more producers of the record, with distinct versions | "two wrappers around one producer" — `expected` and `expected-mutant` share the author's digest |
| 3 | every pair of them is a recorded producer pair, and their shared inputs are exactly the declared common inputs | common inputs restated rather than read from the record |
| 4 | no such pair is recorded `shared`, and what is independently derived is named — reported beside the recorded ancestry, which earns no independence credit | a claim of independent implementations over shared or unexamined ancestry |
| 5 | every adversarial property is a declared property of the capture, and its baseline agrees | an adversarial case named but never executed |

Without a declaration, low and medium risk need no second method and high or critical risk stays
pending, as before. On the probe's CSR-SET-shaped declaration the cell reads

```text
risk high: second method independent-exact-expectation by ['expected', 'reference'] on common inputs
['dependency-manifest', 'guest-source']; independently derived: the expected values derived from the
pinned chapter, no reference output among the inputs; ancestry ['not-examined']: no independence credit;
adversarial ['p0'] (a forbidden CSR write commits its destination) executed, baseline AGREE
```

and with the two producers given one version — two wrappers — `risk high: second method not
satisfied — (2) producers ['expected', 'reference'] are not two or more producers of the record with
distinct versions`. No retained case declares the forms yet; CSR-SET's will be the first (a43b-3).

## What a moved pin does

A `stale` finite method — one of the case's pinned inputs changed since the capture — is not
refused. The measurement reports `invalidated`, names the first moved declaration
(`invalidated by evidence/…/planned-experiment.sexp: SHA256 differs`), leaves the two legs that
depend on the method (`matched-reference-comparison`, `currentness`) unsatisfied and exits 0,
unless the receipt still claims `qualification`. That
is the policy's own currentness rule ("changes invalidate dependent evidence") read as a status
of the evidence rather than a lock on the tree: the invalidated case credits nothing, `REQ-GC-M`
keeps deriving `planned`, and the next capture supersedes it. A case declared before a43b-2b names no
control id or statement, so the producer refuses to prepare it and the regenerated declarations cannot
name the moved one; the method review then reads the capture's own manifest through the measured
record's pin and re-checks the pins of the declaration's route — the case file, then its schema — so
v4 and xlen-v1 read `invalidated by schema/matched-case.sexp: SHA256 differs` from a43b-2b until their
re-captures took their rows (a43b-2e), and a refusal with nothing moved stays a refusal. The finite method's probe keeps
every seam reachable meanwhile by running its deep arms against a synthetic current capture;
its real-tree arm, like the command probe's, asserts the state the dependency manifest predicts
(`decision_stale-method-invalidates-not-locks.md`, the director's ruling of 2026-10-22).

## Run and controls

```bash
python3 -B scripts/review_div_policy.py
python3 -B scripts/review_div_policy.py --json
python3 -B scripts/review_div_policy.py --every-retained
python3 -B scripts/probe_div_policy.py
python3 -B -O scripts/probe_div_policy.py
python3 -B scripts/probe_div_policy.py --mutation trust-receipt
```

The first command measures the default case, v7 since a49-3, and prints `DIV-POLICY: satisfied — 11 of
11 legs satisfied; credited by CR-GC-M-5`; `--json` puts the leg table on stdout within 64 KiB, with the twelve
boundary rows present and predeclared and the thirteen forms required, predeclared and
exercised. `--every-retained` measures every case with a reviewed capture, one line each prefixed by
the case, and exits with the worst code. The probe runs 70 tests in both interpreter modes on synthetic
cases where each knob breaks exactly one leg (a `(boundary: …)` tag marks a row; a state requirement
naming no form is satisfied vacuously, any other kind naming none stays pending), plus the real tree
through one `--every-retained` run (each case's eleven legs while every pin is current; `invalidated`
with the two method legs missing once a pin moves) and three credit-record cases (a current record
over a satisfied measurement reports `credited`; one over a pending measurement and a lapsed one
are findings), six second-method cases — the CSR-SET-shaped declaration satisfied, then one
condition broken at a time, two wrappers judged at high and at low risk alike — and fifteen category
cases, one per row above; each of the 42
seam omissions (among them `credit-pending`, `trust-receipt`, `infer-feature`, `any-control`,
`coverage-optional`, `lock-stale`, `first-property`, `credit-any`, `state-vacuous`, `memory-vacuous`, `boundary-tag`,
one per condition: `both-forms`, `distinct-versions`, `recorded-common`, `shared-pair`,
`adversarial-executed`; and one per judgement of the category row: `category-row`, `selection-recorded`,
`unknown-category`, `effect-case`, `effect-guest`, `effect-config`, `effect-binary`, `effect-differs`,
`effect-override`, `effect-trace`, `effect-diverges`, `effect-at-witness`) runs its one discriminating test and fails.
`PROFILE-CONSISTENCY` runs the probe in its self-test and `--every-retained` on the real path on
every commit.

## The program the m-forms case predeclares

`profiles/rv64gc-lab-v0/guests/m-forms.s` is the corpus program the first case's two pending
legs asked for, authored before any case named it. Thirty-three instructions: seven set up the
operands (−7, 2, −1, −2^63 and a register whose word is −2^31 with a zero high half),
thirteen exercise every M form once with operands that tell each form from its neighbour
(MULW from MUL, DIVW from DIV, REMW from REM, REMUW from REMU, MULHSU from MULH and MULHU),
and twelve are the Table 1 cells — division by zero and signed overflow for DIV, DIVU, REM
and REMU and for their word forms — each citing `RVI-M §11.1.2 (Table 1)` as its source, which
is the marker the boundary-fixtures leg reads. One sentinel precedes the overflow remainder,
whose zero would otherwise replace a zero invisibly, and three late results replace earlier
ones in reused registers, each with a different value.

The expectations were derived on the explicit-budget parcel route the C-composed profile
requires, validated against the schema, and checked byte-identical on re-derivation:

```bash
python3 scripts/derive_rv64gc_expectations.py --check --parcels --steps 33 profiles/rv64gc-lab-v0/guests/m-forms.s
python3 scripts/check_sexp_schema.py profiles/rv64gc-lab-v0/guests/m-forms.expected.sexp schema/expectations.sexp
python3 scripts/run_rv64gc_sail.py m-forms --out-dir target/p4-system-14/a42ar
```

The author's owned-guest list is not touched. `scripts/derive_rv64gc_expectations.py` is one of
the 64 inputs the retained case pins, and a one-line registration there made the finite method
review `stale` on the first commit attempt, which is the currentness leg doing its work: a change to
the expected author invalidates the evidence derived with it. The program is checked with its
explicit budget until the author changes together with a fresh capture.

The last command was a live experiment against the pinned Sail 0.14 binary (a42ar): it agreed
on all 33 declared steps with two byte-identical traces. That agreement was not a capture. The
verify-side differential executes the program on every commit through the regenerated fixture,
and the interaction matrix names it under boundary × boundary. At a42at the property binding
declared the case: `rv64gc-m-forms-v3`, twenty-five predeclared properties — one per form and
one per Table 1 cell — each a reviewed RV64 value the binding holds to the source derivation,
with the reviewed words of all 33 boundaries, and one control (the DIV rounding witness at
boundary 12, −3 → −4) (`decision_many-predeclared-properties-one-control.md`). The declaration
(a42au, re-emitted a42av) and the capture (a42aw, [the m-forms capture](canonical-division.md))
followed; at a42ax the retained reviews read it, and the ten legs above are its measurement.
Nothing is credited.
