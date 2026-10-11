# Authenticated Sail byte evaluation

`evaluate_retained_unit` in `scripts/matched_gpr_evaluation.py` composes the
existing scoped-record, declared-file, identity, receipt and byte-comparison
checks. It authenticates each declared artifact once, uses its exact snapshot,
and reports the different findings separately. A positive byte composition is
**pending complete method/policy adequacy**. It grants no qualification or CPU
acceptance credit. The existing PROFILE-CONSISTENCY qualification refusal remains.

The caller supplies the trusted runtime root, one raw `experiment` form, a
`experiment_verification.Scope`, and the current selected candidate dictionary:

```python
checked = evaluate_retained_unit(
    root, raw_experiment=raw_form, scope=scope, current_candidate=candidate)
```

The raw form is in-memory data from the current parent, not another artifact
path to reopen. Scope supplies the profile's declared candidate, requirement and
effective obligation IDs; it is caller-selected authority. Candidate selection
comes from the current validated parent. This helper does not authenticate that
whole parent file, attest the caller's authority or make all files an atomic
snapshot. Later relevant changes need another evaluation and conservative impact
analysis.

## What the evaluator computes

1. Reuse the existing raw schema and scoped identity/edge checks. Duplicate or
   unknown fields refuse before dossier mapping. The existing dossier mapper
   alone converts the raw form; no alternate format loader is introduced.
2. Bind execution/relations using their public owners. Generic record validity
   is separate from whether this particular method supports those declarations.
   Freeze the candidate's execution values/presence, all three selected receipt
   contexts, run verdicts and observation records before artifact I/O.
3. Authenticate the bounded manifest, check that its relations equal the frozen
   selection, then authenticate the complete declared set through the shared
   reader. Reuse the manifest seed without reopening it. Apply the fixed 128 MiB
   cumulative artifact-read and 16 MiB live snapshot-payload budgets, with the
   existing per-role bounds and terminal failure behavior.
4. Consume the exact retained identity and receipt bytes through the public
   [frozen byte consumers](byte-bindings.md). Bind each receipt's run/argv/exit,
   candidate/collector and input/output inventories. No legacy one-file reader
   runs again, and no binary cache or reference process is accessed.
5. Pass both retained expectations and all three retained traces, with the bound
   receipt process exits, to the existing
   [byte comparison](evidence.md#bounded-three-run-byte-comparison). Require the
   complete ordered computed run set. Cross-check each recorded run verdict
   against its computed comparison or refusal. Declared verdict strings cannot
   replace observed outcomes.
6. Return immutable findings and metadata. Release raw payloads from the returned
   authentication summary. A coherent failed process/control remains a valid
   record with failed observed evidence; it does not become a schema error.

The shared reader checks the declared flat dependency set, including disguised
nested manifests. This establishes the declared bytes at the check, not that the
set covers every relevant dependency. Parent-program/source/image correspondence,
complete closure adequacy, old/new impact, collector provenance and the full
source/risk/feature policy remain mandatory work. The evaluator deliberately
does not turn a successful comparison into a successful complete method.

All used fields freeze before reads, including the receipt exit status absent
from the execution plan. Changing the caller's dictionaries during a read cannot
change the selected check. Changing a path after authentication cannot replace
the retained bytes used for comparison. These properties do not prove that a path
will stay current after checking, or that a recorded process really ran. The
declared method's reviewed collector/capture trust boundary still applies.

## Independent results and limits

`EvaluationCheck` is a frozen record with these independent fields:

| Field | Meaning |
| --- | --- |
| `disposition`, `reason` | Current evaluation finding; the positive byte case is `pending`, not qualified. |
| `record` | `RecordCheck(disposition, issues)`: raw schema/scoped graph validity only. |
| `manifest` | Optional public manifest check, retaining its independent pin and frozen plan. |
| `authentication` | Optional declared-set summary: disposition/reason, manifest pin, metadata-only file facts and byte accounting. |
| `identity` | Optional identity-byte check; its pin is `None` because authentication is separate. |
| `receipts` | Ordered immutable `ReceiptBinding(run_id, run_kind, declared_verdict, check)` records reached before any terminal refusal. Byte checks have no pins. |
| `comparison` | Optional public `ComparisonUnit` with the computed run comparisons/refusals. |

The record disposition is `valid` after raw schema/scoped graph checks,
`refused` after their findings or a malformed record, and `unchecked` when an
invalid scope or unavailable schema tool prevents judging it. `valid` does not
mean every method requirement holds, every declaration is true or every artifact
exists. Record issues are immutable named findings from the existing validator.

| Evaluation disposition | Meaning |
| --- | --- |
| `pending` | The declared files, identity, receipts and observed byte unit bind; complete method/policy adequacy still lacks credit. |
| `failed` | Supported, coherently recorded byte evidence fails the comparison/control, including nonzero/signal process exits and trace refusal. |
| `stale` | A required pin changed, or retained execution identity differs from the frozen current candidate. |
| `unavailable` | A required safe artifact read or supported required schema-tool I/O cannot complete. |
| `refused` | Invalid raw record, contradictory method context/receipt/verdict, unsafe/oversized artifact or malformed required bytes. |
| `unsupported` | The selected rule or expectation exclusion needs another method. |

A receipt with a nonzero exit can bind successfully while evaluation is `failed`.
A pin can match while its contents refuse. A record can be valid while evidence
is stale, unavailable, unsupported or contradictory. A computed `satisfied`
**comparison** is retained even if a false recorded verdict makes the enclosing
evaluation refuse. No authoritative `qualified` Boolean is stored.

The authentication summary preserves the public reader's `authenticated_bytes`
and conservative `charged_read_bytes`. `snapshot_bytes` is the total payload
returned by that reader before release; it is neither the earlier live peak nor
process RAM. Every returned file fact has `data=None`. The initial manifest check
can fail before declared-set authentication starts, leaving `authentication=None`
and its separate manifest pin available. That seed read is bounded to 64 KiB.
When the set reader runs, its shared ledger includes the seed exactly once.

Schema loading is permitted project-tool I/O. Caller-owned raw parent allocation,
parsing objects, chunks, immutable copies and comparison structures add memory
outside the retained snapshot-payload bound. The evaluator offers no option to
raise the fixed method budgets. Raw payloads are not retained in the result;
needed currentness checks require another complete evaluation.

## Run the synthetic evidence cases

The following example uses the probe's `Fixture` **only to construct test data**.
It creates 22 real files under a disposable directory on the repository volume:
nine principal inputs, one dependency child and twelve observations. The helper
uses the public encoders and declared graph shape; production evaluation has no
dependency on probes. Its data inventory is:

| Synthetic file group | Content and limit of the example |
| --- | --- |
| Reference identity | One raw-schema-valid Sail descriptor with a dummy binary digest; that binary does not exist. |
| Two expectations | One `x1` change to `0x1`, and the sole control value changed to `0x2`. |
| Three traces | Identical complete one-boundary synthetic GPR text observing `x1=1`. |
| Stdout/stderr and receipts | Real empty streams; separately encoded receipts naming the exact selected pins, argv and recorded exit. |
| Other principals and child | Opaque synthetic declarations, explicitly inadequate to prove source/image correspondence or complete dependency coverage. |

No reference process runs. Dummy identity/digests and self-consistent synthetic
receipts are not execution attestation. This is why even the positive example
returns `pending`.

```bash
PYTHONPATH=scripts python3 - <<'PY_EVALUATION'
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
import dossier_sexp as D
import records_sexp as S
from matched_gpr_artifacts import encode_capture
from matched_gpr_evaluation import evaluate_retained_unit
from probe_matched_gpr_evaluation import Fixture

parent = Path("target/evaluation-example")
parent.mkdir(parents=True, exist_ok=True)
with TemporaryDirectory(dir=parent) as directory:
    fixture = Fixture(Path(directory))
    def check():
        return evaluate_retained_unit(fixture.root, **fixture.arguments())
    positive = check()
    print(positive.disposition, positive.record.disposition,
          positive.authentication.disposition, positive.comparison.disposition,
          tuple(run.comparison.verdict for run in positive.comparison.runs))
    total = sum(path.stat().st_size for path in fixture.root.rglob("*") if path.is_file())
    print(len(positive.authentication.files),
          positive.authentication.charged_read_bytes == total,
          all(fact.data is None for fact in positive.authentication.files))

    excluded = deepcopy(fixture.base)
    excluded["cross_model"] = False
    fixture.write(fixture.inputs["expectation"], S.render_forms([D.expectations_to_form(excluded)]).encode())
    fixture.publish_receipts()
    unsupported = check()
    print(unsupported.disposition, unsupported.record.disposition, unsupported.comparison.disposition)
    fixture.write(fixture.inputs["expectation"], S.render_forms([D.expectations_to_form(fixture.base)]).encode())

    fixture.runs["control"].update(process_exit=-9, verdict="REFUSED")
    fixture.graph["control_run"][0]["observed_verdict"] = "REFUSED"
    fixture.publish_receipts()
    failed = check()
    print(failed.disposition, failed.record.disposition,
          failed.receipts[2].check.facts.process_exit,
          failed.comparison.runs[2].comparison is None)

    receipt = fixture.receipt("baseline")
    contradictory = fixture.capture("baseline")
    contradictory["argv"][0] = "wrong/binary"
    fixture.write(receipt, encode_capture(contradictory, path=receipt["path"]))
    refused = check()
    print(refused.disposition, refused.record.disposition,
          refused.authentication.disposition, refused.receipts[-1].run_kind)

    child = fixture.root / fixture.child["path"]
    child.write_bytes(b"changed later")
    stale = check()
    print(stale.disposition, stale.record.disposition, stale.authentication.disposition)
    child.unlink()
    unavailable = check()
    print(unavailable.disposition, unavailable.record.disposition, unavailable.authentication.disposition)
    args = fixture.arguments()
    args["scope"] = replace(args["scope"], requirement_ids=frozenset())
    invalid = evaluate_retained_unit(fixture.root, **args)
    print(invalid.disposition, invalid.record.disposition, invalid.authentication)
PY_EVALUATION
python3 scripts/probe_matched_gpr_evaluation.py
python3 -O scripts/probe_matched_gpr_evaluation.py
```

It prints:

```text
pending valid matched satisfied ('AGREE', 'AGREE', 'DIVERGE')
22 True True
unsupported valid unsupported
failed valid -9 True
refused valid matched baseline
stale valid stale
unavailable valid unavailable
refused refused None
```

The final two commands run all 42 controls normally and optimized. All 29
independent omitted guards fail without test errors in both modes. These cover
raw/scoped validity, tool failures, pre-read context freeze, terminal reads,
manifest/identity/receipt reopens, exact selected bytes, process exits, observed
verdicts, complete comparisons, released payloads and immutable results.
The initial failed-baseline probe incorrectly dereferenced a missing comparison;
the public byte owner correctly returned `comparison=None` plus a process-refusal
reason. The corrected control checks that representation and the separate valid
record/failed evaluation. No implementation success was credited from the error.

Full CI follows the clean composition commit. Complete adequacy, reviewed fresh
collection, retention/case/capture declarations and full policy/status derivation
remain subsequent owned work. No canonical capture or CPU acceptance changes here.
