# Combining fresh collection and retained evaluation

`matched_gpr_unit_collector.capture_and_evaluate` composes the existing three-run
collector and retained evaluator. It freezes the planned record and caller
metadata, collects fresh baseline/repeat/control outputs, binds their measured
metadata into the record, and evaluates with the remaining artifact-read allowance.
A positive result is **pending complete method/policy adequacy**. The selected
[reference descriptor](selected-identity.md) and [prepared retention family](prepared-inputs.md)
are declared. The final entrypoint, manifest and authorities must be committed
before canonical execution; capture publication and full policy remain pending.

## Supply a planned record and explicit authorities

Call from the trusted repository root:

```python
result = capture_and_evaluate(
    root, planned_experiment=planned_bytes, scope=scope,
    current_candidate=candidate, author_review=author_review,
    property_authority=authority, max_read_bytes=134217728)
```

`planned_experiment` is1..65536 immutable UTF-8 bytes containing exactly one raw
`experiment` form, with optional structured `(comment ...)` annotations. It uses
the existing references grammar and scoped-record checks, then the sole dossier
mapper. The planned graph supplies the nine principal inputs, three runs and
twelve fresh output targets. Its output hashes/sizes and process exits are
replaced by collection findings. Declared comparison/control verdicts remain
caller claims and must agree with the evaluator's computed findings.

A plain `experiment_verification.Scope` supplies immutable scoped ID sets, each
with at most4096 plain-string IDs. The current candidate is selected from the
separately validated parent. Bind its execution identity and the public execution/
relation plan before artifact I/O. Create the three-run request through the
existing public unit binder; its fresh-name, same-volume, symlink/Git-boundary,
process-group and exclusive-output rules still apply.

Optional `reviewed_inputs`, `author_review`, `property_authority` and
`impact_review` use the same public owners as the [retained evaluator](evaluation.md).
Copy those authorities before collection. An author review supplies its inventory
when no explicit input review is given; two supplied inventories must agree.
Property authority requires author review. Impact requires an input inventory;
its old/new graphs, changed paths and uncertainty are frozen before collection.
These are caller-selected authorities, with their existing adequacy limits.

Preparation failures perform no artifact read or reference launch. Supported
schema-tool I/O can still occur. Unsupported comparison rules return
`unsupported` before collection. Invalid raw grammar/identities/context refuse;
unavailable schema tools report `unavailable`. Invalid read limits refuse even
before parsing or schema work.

## Keep one allowance across both stages

`max_read_bytes` is a plain integer from zero to134217728, inclusive; Boolean,
subclass, negative, oversized and non-integer values refuse. The default is the
unchanged128 MiB ceiling. The evaluator retains its fixed16 MiB snapshot-payload
ceiling and per-role bounds.

1. Reserve the whole delegated allowance for `capture_unit`. A successful recorded
   finding must contain three distinct observed PIDs, zero exits, twelve matching
   output metadata records and consistent bounded charges. Validate that metadata
   before returning unused allowance.
2. Bind actual sizes, digests and measured zero exits into a private parsed copy
   of the planned record. Keep every other field and structured comment form.
   Canonical rendering may change whitespace; the caller's planned bytes are
   unchanged. Bound the resulting immutable record to65536 bytes before evaluation.
3. Reserve the remaining allowance for `evaluate_retained_unit`. It includes its
   initial manifest seed exactly once. Refund only a valid `pending` finding with
   matching seed identity, plain-integer accounting, seed-inclusive authenticated
   and charged bytes, and bounded snapshot metadata.

A failed or invalid delegated finding retains its entire stage reservation and
stops. No retry resets that allowance. In particular, the evaluator can read a
manifest and refuse before its file ledger starts, returning charge zero. This
combined API keeps the evaluation reservation charged for that result, as required
by the [preledger accounting contract](read-allowance.md#carry-collection-charges-forward).
An absent or inconsistent pending counter also refuses without a refund.

`charged_read_bytes` is a conservative reservation-based bound, not always actual
consumption. A fresh-name refusal may charge the entire delegated stage despite
reading no payload. Preparation failures charge zero; record-growth refusal after
successful collection retains that validated collection charge because evaluation
has not started. Unexpected programming exceptions propagate; callers must keep
their active reservation when no valid finding returns.

Artifact payload reads through the collection/evaluation owners are counted.
Schema/runtime I/O, the reference process's own execution, caller-owned parent/
authority allocation, parser objects and copies are separate from these bounds.
No total process-RAM guarantee follows from either byte ceiling.

## Read the independent result fields

The frozen `UnitEvaluation` contains:

| Field | Meaning |
| --- | --- |
| `disposition`, `reason` | Overall `pending`, `failed`, `stale`, `unavailable`, `refused` or `unsupported` finding. Pending grants no qualification. |
| `collection` | Optional validated `UnitCapture`, including historical reached process/receipt metadata. A failed process stops before evaluation. Invalid helper findings are not attached as typed components. |
| `evaluation` | Optional retained `EvaluationCheck`; its independent pin, comparison, source/author/property and impact findings keep their original meanings. |
| `experiment` | Optional bounded immutable measured record. It appears after complete successful collection and record construction, including when later evaluation fails. It is unqualified historical data, and is not written to disk by this API. |
| `charged_read_bytes` | Combined conservative artifact-read charge within the delegated allowance. |

A failed process can leave its real receipt and partial observations. Unexecuted
runs have no success inventory. Existing captures are preserved: reuse of their
output names refuses. A complete measured record can remain contradictory to
its declared verdicts; the evaluator refuses that contradiction. Successful
collection, byte authentication, finite property binding and full policy adequacy
are separate findings. This helper supplies no canonical publication or CPU credit.

## Run a complete synthetic example

This fixture uses the actual tracked DIV guest, expectations and retained excerpt,
plus a synthetic executable that writes a supplied trace. Its observation source
is correlated test data, not Sail or independent execution evidence. The fixture
also supplies synthetic collector/author identities and reviewed metadata. It
owns and removes all files below a disposable directory on the repository volume.
Production collection/evaluation does not import any probe.

```bash
PYTHONPATH=scripts python3 - <<'PY_UNIT_EVALUATION'
from pathlib import Path
from tempfile import TemporaryDirectory
import matched_gpr_unit_collector as U
from probe_matched_gpr_unit_evaluation import Fixture

base = Path("target/unit-evaluation-example")
base.mkdir(parents=True, exist_ok=True)
with TemporaryDirectory(dir=base) as directory:
    fixture = Fixture(Path(directory))
    args = fixture.combined_arguments()
    result = U.capture_and_evaluate(fixture.root, **args)
    print(result.disposition, result.collection.disposition,
          result.evaluation.disposition, result.evaluation.source_property.disposition)
    print(len({run.process.pid for run in result.collection.runs}),
          isinstance(result.experiment, bytes), len(result.experiment) <= 65536)
    print(result.charged_read_bytes == result.collection.charged_read_bytes
          + result.evaluation.authentication.charged_read_bytes,
          result.charged_read_bytes <= 134217728)
    paths = [fixture.root / item["path"] for item in fixture.graph["observation"]]
    before = [path.read_bytes() for path in paths]
    again = U.capture_and_evaluate(fixture.root, **args)
    print(again.disposition, len(again.collection.runs),
          [path.read_bytes() for path in paths] == before)
PY_UNIT_EVALUATION
python3 scripts/probe_matched_gpr_unit_evaluation.py
python3 -O scripts/probe_matched_gpr_unit_evaluation.py
```

The example prints `pending recorded pending matched`, `3 True True`, `True True`,
then `refused 0 True`. Three fresh synthetic processes and authenticated finite
findings remain pending full adequacy. The second call launches no new process
and preserves every prior output byte.

The controls observe actual parent artifact `os.read` payloads. They cover exact
and one-byte-short combined allowances, zero/invalid limits, frozen authorities,
raw-schema-before-mapping, invalid helper/accounting metadata, preledger zero
charges, failed processes, stale inputs, record ceilings, preserved comments,
existing outputs and unexpected programming exceptions. The legacy unit
collector's controls retain their original collection-only contracts.
