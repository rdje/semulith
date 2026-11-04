# Policy legs measured

The evidence policy names, for a requirement's source-semantic category and risk, what a
credited disposition needs. `scripts/review_div_policy.py` reads those requirements as ten
legs and measures each one against the retained bytes of every case the finite method review
holds a reviewed capture for — since a43b-2e (2026-11-02) the M case's `rv64gc-m-forms-v5` and the XLEN
case's `rv64gc-xlen-forms-v2`, each re-captured with its control declared, and since a43b-3g (2026-11-04) the CSR-SET
case's `rv64gc-csr-set-v1`; the earlier cases (v2, v3, v4 and xlen-v1) are history below — on top of the finite method review. It opens only
bounded tracked files, launches no process and grants no credit: `credited` reports a separately
owned record in `credits.sexp`, never the measurement. Both cases measured every leg satisfied and were
credited — the M case by `CR-GC-M-2`, the XLEN case by `CR-D-XLEN-1` (a43a-3) — until the planned lapse that
opens CSR-SET (`P4-SYSTEM.14` a43b-2b, 2026-11-02) moved pinned inputs of both captures, which read
`invalidated`, 8 of 10 legs, their credits retired. Re-captured once each as v5 and xlen-v2, traces byte-identical
(a43b-2d), both measure every leg satisfied again and are credited by `CR-GC-M-3` and `CR-D-XLEN-2` (a43b-2e); the
tables below are the measurements of their predecessors, which the re-captures reproduce.

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
schema/matched-case.sexp: SHA256 differs; no qualification credit` — and since a43b-2e the review reads v5:
`DIV-POLICY: satisfied — 10 of 10 legs satisfied; credited by CR-GC-M-3`. The consumer reads boundary rows and forms from the
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
| the profile override | the override as `prepare_div_inputs` renders it | `… does not pin the profile override` |
| its trace | the raw trace's digest and size | `… does not pin its trace` |
| *(re-derived)* a difference | the trace against the case's baseline expectation | `the retained effect reads AGREE: no observed effect` |
| *(re-derived)* at a witness | a declared property's step | `the retained effect first differs at step N, no declared property's` |

A record without its trace, or a malformed one, refuses (exit 2): that pair cannot be measured honestly.

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
rv64gc-m-forms-v5: DIV-POLICY: satisfied — 10 of 10 legs satisfied; credited by CR-GC-M-3
rv64gc-xlen-forms-v2: DIV-POLICY: satisfied — 10 of 10 legs satisfied; credited by CR-D-XLEN-2
rv64gc-csr-set-v1: DIV-POLICY: satisfied — 10 of 10 legs satisfied; credited by CR-D-CSR-SET-1
```

Measured at a43b-3g with `no qualification credit`; the record `CR-D-CSR-SET-1` credits it since a43b-3h
(`decision_req-d-csr-set-credited-implemented.md`).

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

The first command measures the default case, v5 since a43b-2e, and prints `DIV-POLICY: satisfied — 10 of
10 legs satisfied; credited by CR-GC-M-3`; `--json` puts the leg table on stdout within 64 KiB, with the twelve
boundary rows present and predeclared and the thirteen forms required, predeclared and
exercised. `--every-retained` measures every case with a reviewed capture, one line each prefixed by
the case, and exits with the worst code. The probe runs 48 tests in both interpreter modes on synthetic
cases where each knob breaks exactly one leg (a `(boundary: …)` tag marks a row; a state requirement
naming no form is satisfied vacuously, any other kind naming none stays pending), plus the real tree
through one `--every-retained` run (each case's ten legs while every pin is current; `invalidated`
with the two method legs missing once a pin moves) and three credit-record cases (a current record
over a satisfied measurement reports `credited`; one over a pending measurement and a lapsed one
are findings), six second-method cases — the CSR-SET-shaped declaration satisfied, then one
condition broken at a time, two wrappers judged at high and at low risk alike — and fifteen category
cases, one per row above; each of the twenty-seven
seam omissions (`credit-pending`, `trust-receipt`, `infer-feature`, `any-control`,
`coverage-optional`, `lock-stale`, `first-property`, `credit-any`, `state-vacuous`, `boundary-tag`,
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
