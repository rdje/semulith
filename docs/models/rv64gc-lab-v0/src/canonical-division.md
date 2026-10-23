# The first retained canonical division capture

On 2026-10-19, `P4-SYSTEM.14` a42am collected the predeclared
`rv64gc-signed-div-truncation-v2` case. Three fresh executions of the selected
public Sail executable exited zero. Baseline and repeat agreed across all 27
boundaries. The wrong-quotient control diverged exactly at boundary 2, x7.
These are retained finite observations; complete method/policy qualification and
CPU acceptance remain pending. They do not validate every M instruction.

## What was committed before execution

Commit `b160c66e183dee267ebf12edf25066412fe96ff6` contains the reviewed entrypoint,
three exact native predeclarations and prepared inputs. The [capture plan](capture-plan.md)
explains their separate execution, source, semantic and review identities.
The preflight checked every selected input against that committed state and
verified the pinned executable through the public anchored reader. Its3,801,664
bytes fit the collector's 8 MiB member bound. No reference implementation source
was inspected.

All twelve output names and both result names were absent before the single
capture invocation. Collection used the existing three-run combined helper,
with one 128 MiB artifact-read allowance, 30 seconds per process and the fixed 16 MiB
evaluator snapshot ceiling. Preparation/schema/runtime I/O remains separately
bounded; these limits make no atomic-view or total process-RAM guarantee.

The observed process IDs were 39909, 39914 and 39918, with zero exits. They identify
these historical executions; they are not current processes or execution
attestation independent of the trusted collector and runtime.

## The finite result

| Run | Computed result | Evidence |
| --- | --- | --- |
| Baseline | AGREE | All 27 declared boundaries and every required GPR change row agree with the source-derived expectations. |
| Repeat | AGREE | Same executed inputs, a fresh process and byte-identical raw trace. |
| Wrong quotient | DIVERGE | Only the boundary 2 x7 expectation differs: actual signed−7/2 is−3; the control expects−4. The raw reference trace remains identical. |

At boundary 2 the instruction is `0x0262c3b3` at `0x80000008`. The observed x7 bits
are `0xfffffffffffffffd`; the control expects `0xfffffffffffffffc`. This is the
reviewed rounding-toward-zero witness, not a complete division or M campaign.
Each raw trace is 2,298 bytes and has SHA256
`64551458d50ec4345b716abd9f2caf4b42053d6f3a8640735ee539d89a968bde`.

The combined conservative artifact-read charge was 24,337,600 bytes. Retained
evaluation authenticated 85 distinct files totaling 1,048,756 bytes and retained
33,759 snapshot bytes before releasing payloads from its returned summary.
The independent reconstruction of the collection charge counts before/after
input pins, the three output-read passes and receipt authentication; it agrees
with the collector counters. A preflight upper projection of 76,590,974 bytes
covered collection plus evaluation within 134,217,728 bytes. These are different
quantities: actual bounded charges, authenticated file bytes, retained payloads
and a conservative projection.

## Retained artifacts and independent findings

All files live under `evidence/rv64gc-signed-div-truncation-v2/`:

| Files | Meaning |
| --- | --- |
| `baseline`, `repeat`, `control`, each with `.trace`, `.stdout`, `.stderr`, `.receipt.sexp` | Twelve actual observations with typed sizes/digests, fresh process metadata and public invocation receipts. |
| `measured-experiment.sexp` | The native predeclared graph with actual observation sizes/hashes and checked zero exits. Every other field and structured comment is preserved. Verdict words remain claims checked against computed comparisons. |
| `verification.json` | A bounded derived receipt: source/declaration commit, measured-record pin, process metadata, comparison details, separate findings and accounting. It explicitly records qualification as false. Pinned `object` fields name repository-root identities; readers map them to the native `path` contract. Re-evaluation uses the native record and bytes rather than trusting this JSON's verdict. |

The family contains all 22 declared files, including its index, four prepared
inputs and three native declarations. Its count/16 MiB aggregate/4 MiB member
ceilings stay fixed. The measured and JSON result documents each fit 64 KiB.
The three original native declarations and all prepared inputs are unchanged.

Record validity, manifest authentication, selected identity, receipt binding,
source/image correspondence, all 27 source values, input inventory, expected
author, input influence projection and the finite source property are separate
findings. They all bind for this capture. The comparison is `satisfied`; the
retained evaluator still returns `pending` complete method/policy adequacy.
Producer-pair ancestry remains unexamined and earns no independence credit.

## Check the retained result without running Sail

This complete example uses the public bounded reader, current authority owners
and retained evaluator. It launches no process and does not require a reference
binary. Run from the repository root:

```bash
PYTHONPATH=scripts python3 - <<'PY_CANONICAL_DIV'
import json
from capture_div import prepare_capture, ROOT, PREFIX, S, Unit
from experiment_artifacts import observe_bounded_file, read_snapshot

path = PREFIX + "/verification.json"
observed = observe_bounded_file(ROOT, path, max_bytes=65536)
if observed.disposition != "observed":
    raise ValueError(observed.reason)
report_bytes = read_snapshot(ROOT, "input", dict(id="verification", path=path,
                             sha256=observed.sha256), max_bytes=65536)
if report_bytes.pin.disposition != "matched":
    raise ValueError(report_bytes.pin.reason)
report = json.loads(report_bytes.data)
retained = report["measured_experiment"]
measured_pin = {**retained, "path": retained["object"]}
measured = read_snapshot(ROOT, "observation", measured_pin, max_bytes=65536)
if measured.pin.disposition != "matched":
    raise ValueError(measured.pin.reason)
raw = next(form for form in S.parse(measured.data.decode()) if form[0] == "experiment")
d = prepare_capture()
checked = Unit.Evaluation.evaluate_retained_unit(
    ROOT, raw_experiment=raw, scope=d.authorities.scope,
    current_candidate=dict(d.authorities.reference.fields),
    reviewed_inputs=d.inventory, author_review=d.author,
    impact_review=d.impact, property_authority=d.authorities.property_authority)
print(checked.disposition, checked.record.disposition, checked.comparison.disposition)
print(*(run.comparison.verdict for run in checked.comparison.runs))
print(checked.input_review.disposition, checked.expected_author.disposition,
      checked.source_property.disposition)
print(report["qualification"])
PY_CANONICAL_DIV
```

It prints `pending valid satisfied`, `AGREE AGREE DIVERGE`,
`matched matched matched`, then `False`. Public raw-schema and scoped checks run
before mapping and authentication in the retained evaluator. The JSON pin can
establish measured-file byte identity, but it cannot by itself establish method
adequacy or actual process provenance.

A 101-file runtime copy gives the same retained findings in normal/optimized
Python with no Git, acquired material directory or executable and with the valid
parent checkout available as cwd. Process launching is denied. Missing traces or
receipts report unavailable; changed trace bytes report stale; duplicate raw
fields refuse before authentication. The command suite's actual-capture check
also runs in both modes through PROFILE-CONSISTENCY:

```bash
python3 scripts/probe_div_command.py
python3 -O scripts/probe_div_command.py
```

Each mode runs 19 tests. The other command controls continue to use explicitly
synthetic processes; these two commands never rerun canonical Sail.

## Preserve history and finish the policy work

Do not rerun `--capture` against these names. Existing observations refuse reuse;
failed or partial data must also remain intact. An affected implementation change
requires separately owned retention/revalidation and a fresh declared capture,
not rewriting old pins or expectations until a comparison passes.

This capture supplies one bounded signed-DIV witness and its negative control.
The full source/risk/feature policy, complete closure and impact adequacy,
qualification/status integration and remaining profile evidence still belong to
`P4-SYSTEM.14`. CPU remains 14/18; this capture does not close `REQ-GC-M`,
`OB-GC-M`, the environment contract or the processor gate.

## The m-forms capture (a42aw)

The second reviewed case, `rv64gc-m-forms-v3`, was captured once on 2026-10-22 by the tracked tool
`scripts/retain_div_capture.py` — the procedure the first capture ran by hand, now with a preflight
(every output and result name absent, the three declarations regenerating byte for byte, the
binary's digest equal to the retained identity, the declaration commit named), one invocation of
`capture_div.capture` with the case named, and the exclusive publication of the two results. The
declaration commit it records is `4af5a68bbec9f1bf0922ec3787f829e029c15f29` (the re-emitted
declarations of a42av); the binary is the pinned Sail 0.14 release, 3,801,664 bytes.

```bash
python3 -B scripts/retain_div_capture.py --case rv64gc-m-forms-v3 \
    --declaration-commit 4af5a68bbec9f1bf0922ec3787f829e029c15f29 --preflight-only
python3 -B scripts/retain_div_capture.py --case rv64gc-m-forms-v3 \
    --declaration-commit 4af5a68bbec9f1bf0922ec3787f829e029c15f29
```

The first command prints `ready` and starts nothing; the second was run exactly once and refuses
ever since (`outputs already exist; a capture is never rerun`). Its receipt and the offline
re-evaluation of the retained bytes agree:

| Run | Computed result | Evidence |
| --- | --- | --- |
| Baseline | AGREE | All 33 declared boundaries and every GPR change row agree with the source-derived expectations; process 33523 exited 0. |
| Repeat | AGREE | Same executed inputs, a fresh process (33562), a byte-identical raw trace. |
| Wrong quotient | DIVERGE | Only boundary 12's x15 differs: `div x15, x5, x6` observed `0xfffffffffffffffd` (−3), the control expects `0xfffffffffffffffc` (−4); process 33599 exited 0, raw trace identical. |

Each raw trace is 2,794 bytes with SHA256
`784645dcd85f2ce0cc8e734cc22c8c50231ba28434958dec7a6f855ae1cb7f05`. The measured record
`measured-experiment.sexp` is 16,942 bytes (SHA256
`fb22d5e5554a0e132c231e5551ed8314ab4be35ff93e7f086fceeacb6235a152`); the receipt
`verification.json` is 7,017 bytes (SHA256
`91a90d9c56487af1a6b4306e9007d771e17246ddf41b358185374680090a5a5d`) with `qualification` false;
like the first receipt it names repository-root identities under `object`, because a JSON object
carrying both `path` and `sha256` is a fixture pin resolved relative to the record's own directory.
Retained evaluation authenticated 85 files totalling 1,076,834 bytes and kept 40,438 snapshot
bytes; the combined conservative artifact-read charge was 24,396,002 bytes of the 134,217,728
allowance. All 25 predeclared properties bind to the source derivation — the 13 forms and the 12
Table 1 cells — with the control's observed value equal to the source finding's.

Check the retained result without running Sail, naming the case:

```bash
PYTHONPATH=scripts python3 - <<'PY_M_FORMS'
import json
from capture_div import prepare_capture, ROOT, S, Unit, prefix
from experiment_artifacts import observe_bounded_file, read_snapshot

case = "rv64gc-m-forms-v3"
path = prefix(case) + "/verification.json"
observed = observe_bounded_file(ROOT, path, max_bytes=65536)
report = json.loads(read_snapshot(ROOT, "input", dict(id="verification", path=path,
                    sha256=observed.sha256), max_bytes=65536).data)
retained = report["measured_experiment"]
measured = read_snapshot(ROOT, "observation", {**retained, "path": retained["object"]}, max_bytes=65536)
raw = next(form for form in S.parse(measured.data.decode()) if form[0] == "experiment")
d = prepare_capture(case)
checked = Unit.Evaluation.evaluate_retained_unit(
    ROOT, raw_experiment=raw, scope=d.authorities.scope,
    current_candidate=dict(d.authorities.reference.fields), reviewed_inputs=d.inventory,
    author_review=d.author, impact_review=d.impact,
    property_authority=d.authorities.property_authority, case_id=case)
print(checked.disposition, checked.record.disposition, checked.comparison.disposition)
print(*(run.comparison.verdict for run in checked.comparison.runs))
print(len(checked.source_property.facts.observed), report["qualification"])
PY_M_FORMS
```

It prints `pending valid satisfied`, `AGREE AGREE DIVERGE`, then `25 False`. Since a42ax
(2026-10-23) the retained reviews read this capture: `scripts/review_div_method.py` names it
(`RETAINED_CASE_ID`, the 16,942-byte measured pin, the declaration and capture commits) and reports
`satisfied` over 85 authenticated files, and `scripts/review_div_policy.py` measures
[all ten legs satisfied](policy-adequacy.md) with `credited` false. The first case is `invalidated`
history, never rerun. Nothing here credits `REQ-GC-M`; `scripts/requirement_status.py` derives it
`planned` with both cases pending, and the crediting act is a separately owned record
(`decision_ten-legs-satisfied-credit-separate.md`).
