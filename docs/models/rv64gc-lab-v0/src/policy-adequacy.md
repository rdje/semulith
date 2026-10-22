# Policy legs measured

The evidence policy names, for a `defined` requirement of low or medium risk, what a
credited disposition needs. `scripts/review_div_policy.py` reads those requirements as ten
legs and measures each one against the retained bytes of
`rv64gc-signed-div-truncation-v2`, on top of the finite method review. It opens only
bounded tracked files, launches no process and grants no credit: `credited` is always
false. The measurement is the input a later, separately owned crediting record would cite;
today it names what is still missing.

## The ten legs and what the bytes say

| Leg | Policy words | Measured on the retained case |
| --- | --- | --- |
| source-located-expectations | source-located expected observations; model output is not its own expectation | satisfied: 27 of 27 steps carry a derivation and a source; the witness step cites RVI-M 11.1.2; the expected producer reads only the guest and the expectation |
| boundary-fixtures | directed boundary fixtures | **pending**: six Table 1 rows are present (steps 10–13, 17, 19) and none is predeclared as a property |
| matched-reference-comparison | a matched public-reference comparison on the applicable observations | satisfied: method satisfied, baseline AGREE under `sail-gpr-change-v1`, vocabulary `gpr-change` named |
| repeated-execution | repeated execution | satisfied: repeat AGREE |
| discriminating-control | one discriminating negative control that fails for the stated reason | satisfied: control DIVERGE at step 2, register x7, the witness |
| record-linkage | requirement, effective obligation, tracked runner, producer, record, limitations | satisfied: `REQ-GC-M`, `OB-GC-M`, collector, expected producer, three limitations |
| currentness | relevant changes invalidate dependent evidence | satisfied: the policy document is pinned by the manifest and unchanged; the 73 identities matched |
| risk-method | high and critical risk need a second method | satisfied: medium risk needs none |
| feature-rules | the seven feature families | satisfied by declaration: none applies to `OB-GC-M` |
| form-coverage | every form the requirement names | **pending**: `div` predeclared; `div`, `divu`, `rem`, `remu` exercised; thirteen required |

Eight legs satisfied, two pending; the disposition is `pending` and `REQ-GC-M` keeps
deriving `planned`. The consumer reads boundary rows and forms from the expectation file
(a step whose source cites a chapter table row is a directed boundary fixture; a step's
mnemonic is its form), never from the chapter itself.

## Why the pending legs cannot be closed by relabeling

The boundary rows exist in the program and the expectation file, and the baseline agreed
on all 27 steps. The policy still credits only declared observations ("Public reference
agreement adds only its declared observations"), and the predeclaration declares one
property, the −7/2 rounding witness. Declaring the rows now would be a new predeclaration,
which the retained-identity controls refuse for retained bytes; the next capture
predeclares them. Form coverage is wider still: nine forms (`mul`, `mulh`, `mulhsu`,
`mulhu`, `mulw`, `divw`, `divuw`, `remw`, `remuw`) need a program, expectations and
properties of their own before `OB-GC-M` can be credited at all.

The policy document is one of the 64 reviewed inputs the case pins by SHA256. An edit to
it changes the dependency manifest's expected bytes and refuses the finite method, so the
currentness leg fails until a fresh capture: a policy change is a capture, not a note.

## What the consumer refuses

A receipt whose `qualification` is true while any leg is pending is a finding and fails
`PROFILE-CONSISTENCY` ("No typed success word substitutes for executed evidence"). A refused,
unavailable or unsupported finite method leaves the legs measured but `blocked`. A high- or
critical-risk requirement stays pending on its second method, because no declaration
vocabulary for one exists yet. An obligation without a declared feature disposition stays
pending; the disposition is never inferred from the mnemonics. A control that diverges
somewhere other than the step and register of the property the `control_run` names is not the
stated reason; the leg reads that property, not the first one declared (a42at).

## What a moved pin does

A `stale` finite method — one of the case's pinned inputs changed since the capture — is not
refused. The measurement reports `invalidated`, names the first moved declaration
(`invalidated by evidence/…/planned-experiment.sexp: SHA256 differs`), keeps the two legs that
depend on the method pending and exits 0, unless the receipt still claims `qualification`. That
is the policy's own currentness rule ("changes invalidate dependent evidence") read as a status
of the evidence rather than a lock on the tree: the invalidated case credits nothing, `REQ-GC-M`
keeps deriving `planned`, and the next capture supersedes it. The finite method's probe keeps
every seam reachable meanwhile by running its deep arms against a synthetic current capture;
its real-tree arm, like the command probe's, asserts the state the dependency manifest predicts
(`decision_stale-method-invalidates-not-locks.md`, the director's ruling of 2026-10-22).

## Run and controls

```bash
python3 -B scripts/review_div_policy.py
python3 -B scripts/review_div_policy.py --json
python3 -B scripts/probe_div_policy.py
python3 -B -O scripts/probe_div_policy.py
python3 -B scripts/probe_div_policy.py --mutation trust-receipt
```

The first command prints `DIV-POLICY: pending — 8 of 10 legs satisfied; missing
boundary-fixtures, form-coverage; no qualification credit` and exits zero; `--json` puts
the leg table on stdout within 64 KiB. The probe runs 22 tests in both interpreter modes
on synthetic cases where each knob breaks exactly one leg, plus the real tree; each of the
seven seam omissions (`credit-pending`, `trust-receipt`, `infer-feature`, `any-control`,
`coverage-optional`, `lock-stale`, `first-property`) runs its one discriminating test and
fails. `PROFILE-CONSISTENCY`
runs the probe in its self-test and the measurement on the real path on every commit.

## The program the crediting capture will predeclare

`profiles/rv64gc-lab-v0/guests/m-forms.s` is the corpus program the two pending legs ask
for, authored before any case names it. Thirty-three instructions: seven set up the
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

The last command is a live experiment against the pinned Sail 0.14 binary: it agreed on all
33 declared steps with two byte-identical traces. That agreement is not a capture. No case
predeclares the program's properties, no receipt cites it and nothing credits it; the
retained case and its measurement are untouched, so `REQ-GC-M` keeps deriving `planned`. The
verify-side differential executes the program on every commit through the regenerated
fixture, and the interaction matrix names it under boundary × boundary. At a42at the property
binding declares the case: `rv64gc-m-forms-v3`, twenty-five predeclared properties — one per
form and one per Table 1 cell — each a reviewed RV64 value the binding holds to the source
derivation, with the reviewed words of all 33 boundaries, and one control (the DIV rounding
witness at boundary 12, −3 → −4). The declaration record and the capture follow; only then can
the retained runs be the ones the policy's legs would credit. Until that capture the retained
case is `invalidated` — the binding is one of its pinned inputs — and nothing is credited
(`decision_many-predeclared-properties-one-control.md`).
