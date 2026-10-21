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
`PROFILE-CONSISTENCY` ("No typed success word substitutes for executed evidence"). An
unsatisfied finite method leaves the legs measured but `blocked`. A high- or
critical-risk requirement stays pending on its second method, because no declaration
vocabulary for one exists yet. An obligation without a declared feature disposition stays
pending; the disposition is never inferred from the mnemonics. A control that diverges
somewhere other than the witness step and register is not the stated reason.

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
the leg table on stdout within 64 KiB. The probe runs 19 tests in both interpreter modes
on synthetic cases where each knob breaks exactly one leg, plus the real tree; each of the
five seam omissions (`credit-pending`, `trust-receipt`, `infer-feature`, `any-control`,
`coverage-optional`) runs its one discriminating test and fails. `PROFILE-CONSISTENCY`
runs the probe in its self-test and the measurement on the real path on every commit.
