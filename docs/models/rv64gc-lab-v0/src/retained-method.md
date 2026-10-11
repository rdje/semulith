# Retained Sail method checks

These partial checks support the declared [comparison method](evidence.md#first-comparison-method--contract-and-implementation-boundary).
Complete authenticated evaluation and collection remain pending.

## Authenticating a retained reference identity

`read_reference_identity(root, record, current_candidate)` in
`scripts/matched_gpr_identity.py` checks one `reference-identity` input against
the current Sail candidate. The caller supplies the trusted runtime repository
root and separately validated parent graph/candidate context. The reader checks
its used request fields before I/O, then takes one authenticated immutable
snapshot of at most 64 KiB through the existing anchored reader. It never checks
a pin and reopens the descriptor. Raw `references` schema validation precedes the
single dossier mapper; exactly one references document, one candidate and no
experiments are allowed. Comments may surround that one document.

Execution identity has five required fields: `id` (exactly `sail-riscv`), `origin`,
`kind`, canonical relative `binary` and lowercase SHA256 `binary_sha256`. Optional
`release`, `version`, `source_commit`, `asset` and `asset_sha256` must match in both
presence and value. An absent version differs from a present empty version.
Missing kind/binary/digest refuses even though the general candidate schema makes
these fields optional. Descriptive status, matching-scope prose, host and retrieval
metadata do not change this execution identity. Relevant configuration, source,
producer-assessment and policy changes still require complete dependency checks.
Hashing the entire parent dossier into its own experiment would create a cycle;
this retained descriptor avoids that cycle without excusing closure evaluation.

The frozen `IdentityCheck` keeps its own disposition separate from the reader's
optional `pin` finding. `execution_identity` is an immutable tuple of field/value
pairs, populated only on a current match:

| Disposition | Meaning at this boundary |
| --- | --- |
| `matched` | The retained file matches its pin, validates, and matches the current execution fields. Qualification remains pending. |
| `stale` | The file pin differs, or an authenticated descriptor differs from current execution fields. The nested pin distinguishes these causes. |
| `unavailable` | A required safe read cannot complete. |
| `refused` | Invalid request, unsafe/oversized artifact, malformed descriptor or unsupported candidate identity. A pin can match while descriptor validation refuses. |

This complete synthetic example writes and removes its fixture under `target/`.
Its dummy executable digest declares an identity; no executable is opened or
verified, and no process or canonical capture is created. From the repository root:

```bash
PYTHONPATH=scripts python3 - <<'PY_IDENTITY'
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
import dossier_sexp as D
import records_sexp as R
from matched_gpr_identity import read_reference_identity

root = Path.cwd()
output = root / "target/reference-identity-example"
output.mkdir(parents=True, exist_ok=True)
candidate = dict(id="sail-riscv", role="reference", status="illustrative",
                 kind="executable", origin="https://example.invalid/sail",
                 lineage="unknown; synthetic example", binary="reference/bin/sail",
                 binary_sha256="a" * 64)
doc = dict(profile="illustration", retrieved="2026-10-11", work_dir="reference",
           host=dict(os="example", kernel="example", arch="example", cxx="example"),
           candidate=[candidate])
payload = R.render_forms([D.references_to_form(doc)]).encode("utf-8")
with TemporaryDirectory(dir=output) as directory:
    path = Path(directory) / "identity.sexp"
    path.write_bytes(payload)
    record = dict(id="identity", role="reference-identity",
                  path=path.relative_to(root).as_posix(),
                  sha256=hashlib.sha256(payload).hexdigest())
    checked = read_reference_identity(root, record, candidate)
    print(checked.disposition, checked.pin.disposition)
    changed = dict(candidate, binary_sha256="b" * 64)
    stale = read_reference_identity(root, record, changed)
    print(stale.disposition, stale.pin.disposition)
PY_IDENTITY
python3 scripts/probe_matched_gpr_identity.py
python3 -O scripts/probe_matched_gpr_identity.py
```

The example prints `matched matched`, then `stale matched`: a correctly pinned
historical descriptor can differ from the current candidate. The 40-test suite
runs normal/optimized controls; eight independent omissions lose 4/2/5/1/1/1/20/17
assertions without harness errors. PROFILE-CONSISTENCY runs both modes. Owned
fixtures stay on the repository volume and are removed after each test. Existing
reader controls cover anchored traversal, races, device boundaries and cleanup.
The new controls also require a single bounded read, schema before mapping,
immutable results and no reopen after a successful snapshot.

This boundary does not authenticate the executable, execution, receipts,
invocations, reference-producer version, other inputs/observations or the complete
dependency closure. Offline retained evidence does not depend on a transient
binary cache; fresh replay separately needs the actual pinned executable through
its public acquisition/build route. Full method and aggregate-budget evaluation,
reviewed collection, retention and policy consumers remain pending. No ancestry,
independence, qualification or CPU acceptance credit follows from a match.

## Authenticating and binding a process receipt

`read_run_receipt(root, run=..., inputs=..., observations=...,
current_candidate=...)` in `scripts/matched_gpr_receipt.py` authenticates one
receipt and binds its contents to selected canonical records. First validate the
complete raw parent schema and graph; select this run's records from that graph.
The current candidate's retained identity has its separate check above. This
helper checks used request fields and freezes their values before artifact I/O,
so later mutation of caller dictionaries cannot change the comparison mid-read.
It does not replace parent validation or the complete method evaluator.

The selected context accepts 1–8 inputs, exactly four observations and 1–11 ordered
argv entries. IDs and paths are unique, input/output paths cannot alias, run edges
must name exactly the selected records, and exactly one input has role `collector`.
The observations have one each of `raw-gpr`, `process-stdout`, `process-stderr` and
`process-receipt`. Used context strings have a separate 65,536-character request
limit; caller dictionary allocation is not covered by a RAM ceiling. These bounds
protect this helper; full method evaluation still requires all eight principal
roles, the fixed public invocation, producer bindings and three-run relationships.
Repeated/empty argv strings are preserved exactly, without execution or rewriting.

The helper selects the receipt observation itself, authenticates one immutable
snapshot of at most 64 KiB, and calls the existing bounded `parse_capture` API.
Raw schema validation still precedes the single dossier mapper. No receipt is
reopened after checking its hash. It then requires:

- Exact run ID, kind, ordered argv and integer process exit.
- Exact current Sail candidate ID/binary SHA256 and selected collector input ID.
- The complete input ID/digest inventory; its order is not significant.
- All three output IDs, roles, paths, sizes and digests; inventory order is not significant.

The frozen `ReceiptCheck` keeps its disposition, reason, optional underlying
`pin` and optional `facts` separate. `ReceiptFacts` contains run ID/kind, immutable
argv, process exit and immutable host/tool provenance. Facts appear only after a
successful binding. Host and tool versions describe the retained receipt; this
helper does not compare them with the checking machine or attest their truth.

| Disposition | Meaning at this boundary |
| --- | --- |
| `matched` | Authenticated receipt bytes bind to the frozen selected context. A nonzero or signal exit remains failed-process data. |
| `stale` | Receipt bytes or size differ from the declared observation pin. |
| `unavailable` | A safe artifact read or required schema-tool I/O cannot complete. The receipt pin may already match when the schema is unavailable. |
| `refused` | Invalid/unsafe/oversized context or receipt, invalid syntax, or a contradiction with the selected canonical fields. |

This synthetic example creates only a receipt fixture under `target/`, then removes
it. Input/output pins are dummy declarations and their files are absent. No binary
or process is accessed, and no canonical capture is created. It deliberately shows
that authenticating a receipt does not authenticate its other declared files or
prove the recorded process ran:

```bash
PYTHONPATH=scripts python3 - <<'PY_RECEIPT'
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
from matched_gpr_artifacts import encode_capture
from matched_gpr_receipt import read_run_receipt

root = Path.cwd()
output = root / "target/receipt-binding-example"
output.mkdir(parents=True, exist_ok=True)
candidate = dict(id="sail-riscv", role="reference", status="illustrative",
                 kind="executable", origin="https://example.invalid/sail",
                 lineage="unknown; synthetic example", binary="reference/bin/sail",
                 binary_sha256="a" * 64)
roles = ("guest-source", "guest-image", "reference-config", "reference-identity",
         "expectation", "collector", "adapter", "dependency-manifest")
inputs = [dict(id=role, role=role, path="illustrative-inputs/" + role,
               sha256="b" * 64) for role in roles]
with TemporaryDirectory(dir=output) as directory:
    prefix = Path(directory).relative_to(root).as_posix()
    outputs = [dict(id=name, role=role, path=prefix + "/base." + name,
                    byte_size=0, sha256="c" * 64)
               for name, role in (("trace", "raw-gpr"),
                                  ("stdout", "process-stdout"),
                                  ("stderr", "process-stderr"))]
    receipt = dict(id="receipt", role="process-receipt",
                   path=prefix + "/base.receipt.sexp", byte_size=0, sha256="0" * 64)
    observations = [dict(item) for item in outputs] + [receipt]
    argv = [candidate["binary"], "--config-override", "illustrative-inputs/reference-config",
            "--inst-limit", "1", "--trace-instr", "--trace-gpr", "--trace-exception",
            "--trace-output", outputs[0]["path"], "illustrative-inputs/guest-image"]
    run = dict(id="base", kind="baseline", argv=list(argv), process_exit=0,
               input_ids=[item["id"] for item in inputs],
               producer_ids=["reference", "expected"], verdict="AGREE",
               observation_ids=[item["id"] for item in observations])
    capture = dict(format_version="sail-gpr-capture-v1", run_id="base", run_kind="baseline",
                   argv=list(argv), process_exit=0, reference_candidate_id="sail-riscv",
                   reference_binary_sha256=candidate["binary_sha256"], collector_input_id="collector",
                   input=[dict(id=item["id"], sha256=item["sha256"]) for item in inputs],
                   observation=[dict(item) for item in outputs],
                   host=dict(os="example", kernel="example", arch="example"),
                   tool=[dict(id="collector", version="illustrative")])
    def publish():
        payload = encode_capture(capture, path=receipt["path"])
        (root / receipt["path"]).write_bytes(payload)
        receipt.update(byte_size=len(payload), sha256=hashlib.sha256(payload).hexdigest())
    def check():
        return read_run_receipt(root, run=run, inputs=inputs,
                                observations=observations, current_candidate=candidate)
    publish()
    checked = check()
    print(checked.disposition, checked.facts.process_exit)
    capture["process_exit"] = run["process_exit"] = 1
    run["verdict"] = "REFUSED"
    publish()
    failed = check()
    print(failed.disposition, failed.facts.process_exit)
    capture["argv"][0] = "wrong/binary"
    publish()
    bad = check()
    print(bad.disposition, bad.pin.disposition)
PY_RECEIPT
python3 scripts/probe_matched_gpr_receipt.py
python3 -O scripts/probe_matched_gpr_receipt.py
```

It prints `matched 0`, `matched 1`, then `refused matched`. A coherent failed
process remains bound data; a correctly pinned receipt with a contradictory argv
refuses. The 43-test suite passes normal/optimized; eleven independent omissions
lose 1/4/2/2/2/6/2/4/5/1/1 assertions without harness errors. PROFILE-CONSISTENCY
runs both modes. Controls cover actual owned files, all bindings and pre-read
limits, schema-before-mapping, missing/stale/unsafe data, schema-tool I/O and
immutable context/results. Every temporary fixture is removed after the check.

This helper does not read the selected inputs or raw/stdout/stderr files. It does
not check the fixed invocation, all principal roles, reference-producer version,
three-run relationships, full dependency closure or aggregate budgets. A
self-consistent fabricated receipt cannot establish execution by hashes alone.
The reviewed collector/capture protocol, authenticated remaining inputs and
computed full method/policy checks remain mandatory. PROFILE-CONSISTENCY still
refuses v1 qualification; binding a receipt cannot advance CPU acceptance.

## Binding the declared Sail invocations

`matched_gpr_execution.bind_execution(experiment, current_candidate)` consumes the
canonical dictionary **after** raw schema and scoped graph checks. It returns a
frozen plan for the first method's execution relationships, without opening any
artifact or launching a process. A `matched` result is partial binding only.

Before constructing each used index it requires 9 inputs, 12 observations,
3 runs and 3 producers. The parent budget is 1–4096 boundaries with sole model
Sail. Each run selects eight principal roles: seven common inputs plus an
expectation. Baseline/repeat use the same selections and expected producer;
control selects the other expectation and expected producer. Each run owns one
raw trace, stdout, stderr and receipt; all twelve outputs have distinct owners.
The reference producer names Sail and `sha256:<current binary SHA256>`.

For each run the derived argv is exactly:

```text
binary --config-override config --inst-limit budget --trace-instr --trace-gpr --trace-exception --trace-output this-run-trace guest-image
```

Order, flags and all values must match; only the trace-output path varies across
runs. Paths are canonical repository-relative identifiers. There is no shell
command or implicit current-directory selection. The repeated run names the
baseline through `repeat_of`; other runs cannot carry that edge.

This complete synthetic graph uses dummy pins and creates no files. It passes the
existing raw-schema/scoped graph checker before mapping and binding. It then shows
that failed-process records remain data and a wrong trace-output argument refuses:

```bash
PYTHONPATH=scripts python3 - <<'PY_EXECUTION'
import dossier_sexp as D
import experiment_verification as V
from matched_gpr_execution import bind_execution

candidate = dict(id="sail-riscv", role="reference", status="illustrative", kind="executable",
                 origin="https://example.invalid/sail", lineage="unknown; synthetic example",
                 binary="reference/bin/sail", binary_sha256="a" * 64)
common = ["guest-source", "guest-image", "reference-config", "reference-identity",
          "collector", "adapter", "dependency-manifest"]
output_roles = ("raw-gpr", "process-stdout", "process-stderr", "process-receipt")
roles = (*common, "expectation")
inputs = [dict(id=role, role=role, path="inputs/" + role, sha256=f"{n + 1:x}" * 64)
          for n, role in enumerate(roles)]
inputs.append(dict(id="mutant-expectation", role="expectation",
                   path="inputs/mutant-expectation", sha256="9" * 64))
producers = [dict(id="reference", role="reference", candidate_id="sail-riscv",
                  version="sha256:" + candidate["binary_sha256"], input_ids=common)]
for pid, expectation in (("expected", "expectation"), ("expected-mutant", "mutant-expectation")):
    producers.append(dict(id=pid, role="expected", version="source-derivation-v1",
                          input_ids=["guest-source", expectation, "adapter", "dependency-manifest"]))
observations, runs = [], []
for kind, rid in (("baseline", "base"), ("repeat", "repeat"), ("control", "control")):
    outputs = [dict(id=rid + "-" + role, role=role, path=f"outputs/{rid}.{role}",
                    sha256="b" * 64, byte_size=0) for role in output_roles]
    observations.extend(outputs)
    run = dict(id=rid, kind=kind, input_ids=common + ["mutant-expectation" if kind == "control" else "expectation"],
               producer_ids=["reference", "expected-mutant" if kind == "control" else "expected"],
               observation_ids=[output["id"] for output in outputs], process_exit=0,
               verdict="DIVERGE" if kind == "control" else "AGREE",
               argv=[candidate["binary"], "--config-override", "inputs/reference-config",
                     "--inst-limit", "1", "--trace-instr", "--trace-gpr", "--trace-exception",
                     "--trace-output", outputs[0]["path"], "inputs/guest-image"])
    if kind == "repeat": run["repeat_of"] = "base"
    runs.append(run)
pairs = [dict(id=pid + "-pair", left="reference", right=pid, subsystem="gpr-change",
              assessment="not-examined", shared_input_ids=["guest-source", "adapter", "dependency-manifest"],
              evidence="unknown; synthetic fixture", consequence="no independence credit")
         for pid in ("expected", "expected-mutant")]
graph = dict(format_version="matched-gpr-v1", comparison_rule="sail-gpr-change-v1",
             limitations=["synthetic; no execution or qualification"], input=inputs,
             producer=producers, observation=observations, run=runs, producer_pair=pairs,
             property=[dict(id="property", statement="synthetic GPR change", requirement_id="REQ-synthetic", obligation_ids=["OBL-synthetic"],
                            observation_kinds=["gpr-change"], gpr_witness=dict(step_n=0, register="x1"))],
             control_run=[dict(id="wrong-expectation", run_id="control", baseline_id="base",
                               property_ids=["property"], mutation_input_ids=["mutant-expectation"],
                               expected_verdict="DIVERGE", observed_verdict="DIVERGE",
                               reason="synthetic wrong-expectation control")])
experiment = dict(id="synthetic", program="synthetic.s", instructions=1, models=["sail-riscv"],
                  verdict="AGREE", reproduced="synthetic fixture", control="synthetic fixture", verification=graph)
document = dict(profile="synthetic", retrieved="2026-10-11", work_dir="reference",
                host=dict(os="example", kernel="example", arch="example", cxx="example"),
                candidate=[candidate], experiment=[experiment])
raw = D.references_to_form(document)
form = next(item for item in raw if isinstance(item, list) and item and item[0] == "experiment")
scope = V.Scope("synthetic", frozenset({"sail-riscv"}), frozenset({"REQ-synthetic"}),
                frozenset({"OBL-synthetic"}))
issues = V.check_experiment(form, scope)
if issues:
    raise ValueError(issues)
canonical = D.references_to_doc(raw)["experiment"][0]
checked = bind_execution(canonical, candidate)
print(checked.disposition, len(checked.plan.runs))
for run in canonical["verification"]["run"]:
    run.update(process_exit=127, verdict="REFUSED")
canonical["verification"]["control_run"][0]["observed_verdict"] = "REFUSED"
print(bind_execution(canonical, candidate).disposition, "REFUSED")
canonical["verification"]["run"][2]["argv"][9] = "outputs/wrong.raw-gpr"
print(bind_execution(canonical, candidate).disposition)
print(bind_execution(dict(id="legacy"), candidate).disposition)
PY_EXECUTION
python3 scripts/probe_matched_gpr_execution.py
python3 -O scripts/probe_matched_gpr_execution.py
```

It prints `matched 3`, `matched REFUSED`, `refused`, then `unsupported`. The
48-test suite passes normal/optimized; twelve independent omissions lose
6/8/3/1/3/2/1/44/2/1/1/1 assertions with no harness errors. PROFILE-CONSISTENCY
runs both modes. Controls cover all argv positions, selected roles/membership,
counts before indexing, binary-version binding, repeat/control relations, output
ownership, immutable detached plans and absence of artifact/process I/O.

This plan does not authenticate any declared file or binary. Property/witness,
control and producer-pair semantics, the expected producers' derivation relation,
source/program/image binding, dependency closure and aggregate budgets remain
separate requirements. Identical expectation hashes can bind here; the byte
comparison must still prove a sole changed witness value. Recorded verdicts do
not establish process or comparison success. Unsupported legacy/other rules need
their own method. Malformed or contradictory selected context returns `refused`.
No execution plan grants qualification or CPU acceptance.

At a33, the execution probe adds forced-assertion fixture-isolation controls.
The twelve production omission totals above are reverified with isolated subcases;
two additional cleanup regressions each fail one assertion without errors. An
assertion failure must restore the temporary change before the next subcase.
Historical receipts remain intact; current executable oracles use 48 tests.

## Binding witness, control, derivation and actual pairs

`matched_gpr_relations.bind_relations(experiment, current_candidate)` reuses the
execution binder, then checks the remaining finite declared relationships. The
caller first validates raw schema and the scoped graph. A frozen `matched` plan
means these declarations bind; it does not mean the method succeeded.

It requires exactly one property, one control and two producer pairs before
constructing their indexes. The property observes only `gpr-change` and carries
one typed witness: a step within the parent's 1–4096 budget and canonical `x1`
through `x31`. The control names the sole baseline, control run, property and
mutant expectation input. Its intended verdict is `DIVERGE`. Recorded observed
`AGREE` or `REFUSED` remains coherent failure data when it matches the run; a
control aimed at process refusal needs another method.

The baseline and mutant expected producers must declare the same nonempty
version, consume their own selected expectation and have identical other input
IDs. The control's typed baseline/mutation links make that declared relation
explicit. It is a mutant of one derivation, never a second independent method.
This checks declared versions and inputs, not the expected producer's actual
implementation or the semantic expectation difference. The byte comparison
must still prove that exactly the named RV64 witness value changed.

Exactly the two actual reference/expected pairs must appear, with distinct
identities/endpoints and exact shared-input intersections. Subsystem, assessment,
evidence and consequence are retained as declarations. Neither a pair's
assessment word nor a producer count proves independent ancestry. Unknown
ancestry retains its limits; the full verification policy remains separate.

This standalone example reuses the tracked synthetic fixture builder whose full
graph appears in the invocation example above. It creates no files and executes
no Sail process. Raw validation precedes canonical mapping and relation binding:

```bash
PYTHONPATH=scripts python3 - <<'PY_RELATIONS'
from copy import deepcopy
import dossier_sexp as D
import experiment_verification as V
import sexp as S
from matched_gpr_relations import bind_relations
from probe_matched_gpr_execution import fixture, raw_experiment

experiment, candidate = fixture()
raw = raw_experiment(experiment, candidate)
scope = V.Scope("synthetic", frozenset({"sail-riscv"}), frozenset({"REQ-synthetic"}),
                frozenset({"OBL-synthetic"}))
issues = V.check_experiment(raw, scope)
if issues:
    raise ValueError(issues)
canonical = D.references_to_doc([S.Symbol("references"), raw])["experiment"][0]
checked = bind_relations(canonical, candidate)
print(checked.disposition, checked.plan.witness.register, len(checked.plan.pairs))
failed = deepcopy(canonical)
failed["verification"]["control_run"][0]["observed_verdict"] = "REFUSED"
failed["verification"]["run"][2].update(verdict="REFUSED", process_exit=127)
print(bind_relations(failed, candidate).disposition, "REFUSED")
wrong_target = deepcopy(canonical)
wrong_target["verification"]["control_run"][0]["mutation_input_ids"] = ["expectation"]
print(bind_relations(wrong_target, candidate).disposition)
wrong_derivation = deepcopy(canonical)
wrong_derivation["verification"]["producer"][2]["version"] = "other-derivation"
print(bind_relations(wrong_derivation, candidate).disposition)
wrong_sharing = deepcopy(canonical)
wrong_sharing["verification"]["producer_pair"][0]["shared_input_ids"] = []
print(bind_relations(wrong_sharing, candidate).disposition)
PY_RELATIONS
python3 scripts/probe_matched_gpr_relations.py
python3 -O scripts/probe_matched_gpr_relations.py
```

It prints `matched x1 2`, `matched REFUSED`, then three `refused` results. The
39-test suite passes normal/optimized. Fifteen relation omissions lose
9/5/6/6/4/4/4/1/2/5/2/2/1/4/4 assertions; two cleanup regressions each lose one,
all without harness errors. PROFILE-CONSISTENCY executes both modes. Forced
assertion failures prove later count/version subcases receive isolated fixtures;
the execution probe also checks isolation of all argv positions.

The plan does not traverse obligation IDs or prove source-grounding/adequacy.
Those remain scoped-graph and policy owners. Used producer input lists cap at
eight and pair sharing at seven; copied text caps at 65,536 characters separately
from byte budgets. Parent allocation and aggregate method reads remain future
orchestrator requirements. Immutable plans retain no caller dictionary/list
aliases. No files are authenticated or opened, and no process runs here.
No relation plan grants comparison, method qualification or CPU acceptance.

For manifest and selected-leaf checks, read [dependency closure](closure.md).
