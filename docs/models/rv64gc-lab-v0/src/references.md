# References and comparison limits

The generated [reference table](materials.md#reference-candidates) identifies each
candidate and its recorded matching scope. `references.sexp` is canonical;
`reference/sail-rv64gc-lab-v0.override.sexp` declares the public configuration.
Adapters and author scripts are tracked project tools. Dependency interaction uses
published configuration, builds, APIs and outputs; source access grants no license
to infer a submodule's internal implementation or ancestry.

## What the earlier comparisons mean

Earlier privilege, Sv39, atomic, interrupt/wake, FENCE.I, FP, fault, M and C runs
are historical finite observations. They name agreement, architectural latitude
and platform differences separately. The live adapter compares declared GPR changes
and witnessed delivery gaps. It does not infer complete PC, instruction-word, FP,
memory, CSR or request equality from the same text output.

For example, the compressed timer guest differs at the boundary where the
laboratory delivers STI and the matched reference proceeds with C.ADDI. Public
configuration and fresh public traces identify an unmatched timer source.
That result is not a compressed arithmetic defect and is not acceptance for
Sstc timing. Likewise disabled reference Zicntr and absent injected physical
refusal regions leave those observations unmatched.

A deliberately wrong C.LI result must diverge through a fresh reference run.
An adapter that accepts a failed producer, stale trace or changed expected value
is itself a defect, even if the reference program normally succeeds. Controls
must exercise the actual execution/comparison path and then prove restoration.

## Independence has a denominator too

No current claim authenticates Sail/Spike implementation ancestry. Agreement is
useful on named inputs, but it does not establish independent numeric derivation.
The spec-side author and engine can share opcode tables or arithmetic producers;
record those common inputs and do not count two wrappers as two methods.

For an FP requirement, a source-derived exact arithmetic fixture can provide a
second method when its producer and scope are explicit. A Sail GPR-only trace
cannot by itself qualify FP result bits/flags. For translation, a separately
specified request-path expectation can expose a walk or fault-order defect that
a final handler register masks. The policy requires methods to address the same
property, with their controls and limitations recorded.

## Artifact syntax you can inspect

Two prospective artifact documents now have schemas and one mapping owner,
`scripts/dossier_sexp.py`. `schema/matched-gpr-dependencies.sexp` describes a
`dependencies` root with version `matched-gpr-dependencies-v1` and 1–64 `input`
children. Each input has `id`, `role`, canonical repository-relative `path` and
lowercase 64-hex `sha256`. IDs and paths are unique. The document cannot name
itself or declare a child with role `dependency-manifest`. Detecting manifest
content hidden behind another role is now covered by [leaf inspection](closure.md#inspecting-one-selected-dependency-leaf)
and the shared reader. Completeness of the relevant closure remains pending.

For example, this is valid **syntax with a dummy pin**, not a verified file:

```lisp
(dependencies (format_version "matched-gpr-dependencies-v1")
  (input (id "mapper") (role "mapping") (path "scripts/dossier_sexp.py")
    (sha256 "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")))
```

`schema/sail-gpr-capture.sexp` describes a `capture` root with version
`sail-gpr-capture-v1`. It records the following data:

| Field/child | Content |
| --- | --- |
| `run_id`, `run_kind` | Run identity and `baseline`, `repeat` or `control` |
| Repeated `argv`, integer `process_exit` | Exact argument order, including repeated/empty arguments; actual process result |
| `reference_candidate_id`, `reference_binary_sha256`, `collector_input_id` | Recorded executable identity and the collector's input identity |
| Repeated `input` | Unique `id` and exact SHA256; collector ID must occur in this inventory |
| Three `observation` children | Unique `id`/`path`, nonnegative `byte_size`, SHA256; exactly one each of `raw-gpr`, `process-stdout`, `process-stderr` |
| `host`, repeated `tool` | Nonempty host `os`/`kernel`/`arch`; unique tool `id` with nonempty `version` |

The receipt never contains its own hash or names itself as an output. Empty output
files and nonzero or signal exits are valid recorded data; they do not meet the
method's success requirements. Versions and provenance are recorded observations,
not attestation that a process executed. The bounded receipt-binding check below
now matches selected run/argv/input/output/candidate fields; complete graph and
method evaluation remain separate obligations.

From the repository root, these commands print complete illustrative documents to
stdout and run the controls. They create no capture and their dummy pins do not
authenticate anything:

```bash
python3 scripts/probe_matched_gpr_artifacts.py --emit dependencies
python3 scripts/probe_matched_gpr_artifacts.py --emit capture
python3 scripts/probe_matched_gpr_artifacts.py
python3 -O scripts/probe_matched_gpr_artifacts.py
bash scripts/check_dossier_schema.sh --self-test
```

The public `parse_dependencies(payload, path=...)` and `parse_capture(payload,
path=...)` in `scripts/matched_gpr_artifacts.py` accept immutable bytes plus the
artifact's canonical relative location. Each refuses more than 64 KiB **before**
decoding/parsing, malformed UTF-8, extra/missing roots, unknown fields, duplicate
singulars and invalid types/facets. They validate raw shape before dictionary
mapping, then check the identities above. They never open an artifact or launch
a process; consumers pass bytes from the anchored authenticated
snapshot reader. Parsing does not authenticate a pin. Schema files themselves
are read as project tools. These are payload limits, not total process RAM caps.
The convenience encoders refuse unknown keys, lossy mappings and oversized
serialized documents; rendering a caller-owned dictionary has no separate RAM
budget guarantee.

DOSSIER-SCHEMA runs these offline controls before its existing tracked dossier
sweep. That sweep covers `profiles/*/*.sexp`; it does not yet sweep a prospective
nested capture store. No such store or canonical v1 capture exists. The future
retention/capture slice must explicitly connect its files to evaluation and gates.

## Retained method checks

The [retained Sail method chapter](retained-method.md) contains the complete
identity, receipt and invocation examples, plus witness/control/derivation/pair
bindings. [Authenticated evaluation](evaluation.md) composes them with bounded
comparison and [source/ELF correspondence](image-binding.md#compose-authenticated-source-and-elf-snapshots).
Complete method/policy adequacy and qualification remain pending.

## What comes next

A27 repairs the terminal-newline defect found at a26: all project exact-token
facets now use strict end anchors. For example a 64-hex SHA256 followed by a newline,
`"AGREE\n"`, `"baseline\n"` or `"x31\n"` refuses schema validation, rather than
becoming a subtly different identity/verdict. Generic `pattern "needle"` still
accepts `"hayneedlehay"`; the schema kernel deliberately implements substring
search, so exactness belongs to the declared token pattern. The repair changes
83 declarations in 13 schemas; all 91 patterned fields have positive and boundary
controls, including five complete canonical-document regressions. Run:

```bash
python3 scripts/probe_schema_token_facets.py
python3 -O scripts/probe_schema_token_facets.py
bash scripts/check_requirements.sh --self-test
```

These offline controls preserve all canonical document bytes. They prove grammar
behavior, not file authenticity, producer execution or evidence qualification.

Historical comparisons remain prose in the canonical dossier. Optional structured
graphs, typed witnesses/baselines, bounded pin/snapshot readers and these artifact
formats and a [bounded byte comparison](evidence.md#bounded-three-run-byte-comparison)
and retained reference-identity authentication, [receipt binding](retained-method.md#authenticating-and-binding-a-process-receipt)
and [execution binding](retained-method.md#binding-the-declared-sail-invocations) exist. The composed evaluator also binds
source/ELF bytes. Complete closure/impact/source-grounded property/provenance and
policy adequacy, reviewed fresh collection, measured capture retention and canonical
captures remain pending. PROFILE-CONSISTENCY continues
to refuse v1 blocks as unqualified. The [policy](policy.md) was declared after
implementation and is prospective; this book does not backdate it. Candidate
availability, a successful book build and syntax checks do not advance requirement
status or close G-TRACE. Full policy/status consumers follow verified captures.

At composition checkpoint `3e5a3ea`, full local CI passed all 443 Rust tests,
doctrines, browser bench, 53 smoke controls and seven book builds. All 1,370
tracked files/modes/submodule pins remained unchanged. This regression checkpoint
provides no experiment qualification or CPU acceptance credit.

## Reviewed input inventory

A42m adds an optional `reviewed_inputs` argument to `evaluate_retained_unit`.
It supplies a separate current `InputReview(profile_id, experiment_id, inputs)`
from `scripts/matched_gpr_input_review.py`. The caller selects and owns that
review, just as it owns the current scope/candidate. Copying the experiment's
own declaration into this argument supplies no independent coverage review.
There is no new serialized format, review producer or canonical capture here.

Before artifact reads, the evaluator validates the selected profile/experiment
and copies every input binding. After authenticating the manifest, it compares
its complete declared inventory with this frozen review before reading the file
set. Equality covers input ID, role, canonical path and SHA256; ordering does not
matter. Missing reviewed IDs, unreviewed declared IDs and changed identities
return separate sorted `missing_ids`, `unreviewed_ids` and `changed_ids` tuples.
A mismatch makes evaluation `refused` with `authentication=None`; the independent
manifest finding remains available.

The appended optional `input_review` finding has `matched`/`refused`, reason,
profile/experiment IDs, both inventory counts and those three tuples. `matched`
means metadata equality, not file authentication or complete source coverage.
It can coexist with later stale files or failed process evidence. Malformed
review context refuses before artifact I/O; a manifest failure leaves this
finding absent. Omitting the argument preserves the existing API and yields
`input_review=None`. Every positive complete evaluation still remains `pending`;
PROFILE-CONSISTENCY continues to refuse qualification.

The boundary accepts plain frozen `InputReview` and `InputBinding` objects with
plain tuples of 9–73 unique IDs/paths: nine principals plus at most 64 distinct
manifest children. Role/ID and selected profile/experiment text is nonempty,
at most 65,536 characters; canonical paths at most 4,096 characters, and digests
are lowercase 64-hex SHA256. Existing child IDs may contain spaces. Bounds apply
before member indexing/copying. Returned facts contain no artifact payloads.
This validates the declared set against caller authority; relevance/completeness
of that review, conservative old/new impact, source-grounded properties,
collector provenance and full policy adequacy remain separate obligations.

This complete **synthetic metadata example** opens no artifact files and runs
no reference process. Its dummy digests confer no authentication or qualification:

```bash
PYTHONPATH=scripts python3 - <<'PY_REVIEW'
from matched_gpr_execution import COMMON_ROLES, InputBinding
from matched_gpr_input_review import InputReview, freeze_review, compare_inputs
roles = (*COMMON_ROLES, "expectation", "expectation", "implementation")
pins = tuple(InputBinding(role, f"pin-{i}", f"inputs/{i}.dat", "a" * 64)
             for i, role in enumerate(roles))
review = freeze_review(InputReview("example", "unit", pins),
                       profile_id="example", experiment_id="unit")
for declared in (tuple(reversed(pins)), pins[:-1],
                 pins + (InputBinding("source", "extra", "inputs/extra", "b" * 64),)):
    result = compare_inputs(review, declared)
    print(result.disposition, result.missing_ids, result.unreviewed_ids)
PY_REVIEW
```

It prints `matched () ()`, `refused ('pin-9',) ()`, then
`refused () ('extra',)`. To use a genuinely reviewed inventory in evaluation:

```python
checked = evaluate_retained_unit(root, raw_experiment=raw_form, scope=scope,
                                current_candidate=candidate, reviewed_inputs=review)
```

The library performs no dependency discovery or review attestation. Tests use
separate synthetic authority and real on-volume artifact files; missing/extra/
changed inventories refuse even when every declared file pin matches. Additional
controls check context copying, bounds/types, coherent failed processes, legacy
behavior and guard omissions in normal/optimized Python. Run them with
`python3 scripts/probe_matched_gpr_input_review.py`; no reference process runs.

## Snapshot expectation author contract (a42o)

P4-0257 implements this API under a contract declared before implementation.
It reuses the existing bounded spec-side author; it introduces no second numerical interpreter or canonical
capture. `derive_snapshot(source, program=..., instructions=...)` in
`scripts/derive_rv64gc_expectations.py` accepts plain immutable UTF-8 bytes
(1–1,048,576), at most 8,192 `splitlines` lines, a plain nonempty program
label (1–65,536 characters) and a plain integer budget (1–4,096). Invalid input
must refuse before canonical tool-data reads. The program is an opaque exact
label; it is never opened as a source path.

Use the current canonical RV64GC assembler with IALIGN16, independent of the
legacy pre-bind `DERIVE_ENCODING` override. Share source preflight/context owners
with image construction. Execute the exact assembled initial bytes, at most
32 KiB, for exactly the budget; branches, modified instruction memory and
compressed parcels use the existing rules. The selected author starts cold at
`0x80000000` in its 64 KiB region and declared laboratory reset/time state. This
API supports that fixed author domain, not arbitrary entry/reset configuration.
Running off, `#|end`, halt or delivery does not silently shorten the budget.

Snapshot observations use the stock numeric rules and their stock derivation/
source notes. `#:` annotations cannot supply evidence or overwrite those notes;
they are ignored on this route. Source-side `#|refuse:` and `#|never:` controls
are unsupported here and must explicitly refuse. This does not alter either
legacy file route's supported annotations, controls or 10,000-boundary limit.
Unknown valid instruction shapes remain unsupported rather than fabricated traps;
reserved behavior retains the author's selected, source-located laboratory rule.

The result is a frozen `SnapshotDerivation`: exact program, author/encoding paths,
route `snapshot-parcels-v1`, entry/region, source size/SHA256, initial payload
size/SHA256, instruction count and an immutable tuple of `SnapshotStep` facts.
Each step has index, starting PC, actual fetched instruction bits/length when
available, fetch count, sorted immutable GPR `(register, value)` changes, stock
derivation and source note. Delivery/halt/fetch-fault steps have no complete
instruction bits/length. GPR changes preserve the existing unchanged-value/x0
elision; they are not a write-count, memory, FP or full-state observation.

Do not return the mutable hart/step records, source bytes or initial image.
The facts make no original-capture chronology claim. Metadata comes from this
producer; its authenticity, correctness, complete dependency/source review and
relationship to a claimed requirement remain separate obligations. A numeric
match alone does not qualify an experiment, establish implementation ancestry or
advance CPU status. Full source-grounded property binding and reviewed fresh
collection still follow.

`SnapshotError` distinguishes malformed metadata/source or assembly refusal,
`SnapshotUnsupported` a control or semantic shape outside this bounded route,
and `SnapshotUnavailable` unavailable/invalid current canonical tools. Diagnostics
must not echo arbitrary source. The API performs no source-path reads/writes or
reference execution; canonical project tool-data reads remain explicit. Bounds
cover supplied source, initial image and step count, not exact process RAM/time.

### Complete snapshot-author example

From the repository root, this derives observations from supplied bytes. It reads
current canonical project tool data, creates no source/output file and executes
no reference or production CPU engine:

```bash
PYTHONPATH=scripts python3 - <<'PY_SNAPSHOT_AUTHOR'
from derive_rv64gc_expectations import derive_snapshot, SnapshotError, SnapshotUnsupported
source = b"addi x1, x0, 5\nc.addi x1, 1\n"
run = derive_snapshot(source, program="example.s", instructions=2)
print(run.route, run.instructions, run.payload_size)
for step in run.steps:
    print(step.n, hex(step.pc), hex(step.instruction_bits),
          step.instruction_length, step.fetches, step.writes)
try:
    derive_snapshot(bytearray(source), program="example.s", instructions=2)
except SnapshotError:
    print("mutable source refused")
try:
    derive_snapshot(b"#|never: x31\n" + source, program="example.s", instructions=2)
except SnapshotUnsupported:
    print("source control unsupported")
PY_SNAPSHOT_AUTHOR
```

It prints:

```text
snapshot-parcels-v1 2 6
0 0x80000000 0x500093 4 2 ((1, 5),)
1 0x80000004 0x85 2 1 ((1, 6),)
mutable source refused
source control unsupported
```

The payload identity describes the initial assembled image. A later store into
instruction memory changes the actual recorded instruction bits, not that initial
fingerprint. Halt/delivery/fetch-fault facts preserve their absence of a complete
instruction. A repeated same-value destination and x0 produce no GPR change.
These are the author's existing rules, not new model semantics or evidence for
unobserved effects.

Normal and optimized controls run with `python3 scripts/probe_gc_snapshot_author.py`
and `python3 -O scripts/probe_gc_snapshot_author.py`. They check immutable input,
preflight before tool reads, fixed canonical context, exact budget, source-path
independence, stock notes, explicit unsupported controls, actual modified bytes,
copying/immutability and named failures. The initial API's leaked assembler
exception is fixed: malformed assembly now gives the declared bounded
`SnapshotError`. Its permanent assertion failed before conversion and passes after.

The old 167 parcel and 41 historical word routes reproduce their prior complete
serialized output byte for byte. The snapshot route matches 133 canonical guests'
4,044 GPR boundaries and explicitly refuses 34 source-control guests. These are
regression/capability checks, not new reference runs, original-capture chronology,
source proof for every claimed property, or CPU acceptance. Existing files are
never regenerated or rewritten by the snapshot API.

Legacy controls also preserve their intended failure reasons for reserved bits,
division rounding, page permissions and explicit budgets past the source end.
The temporary mutant loaders and map target follow the shared author's new shape;
an import/type crash cannot substitute for a discriminating semantic failure.

## Source-derived GPR expectation binding (a42p)

The pure byte API `compare_source_expectation` in
`scripts/matched_gpr_comparison.py` implements this bounded value check:

```python
checked = compare_source_expectation(
    source=source_bytes, baseline_expectation=expectation_bytes,
    instructions=3, program="division.s", witness=GprWitness(2, "x3"))
```

Both payloads must be plain immutable bytes, nonempty and at most 1 MiB.
The program is an exact plain string of 1–65,536 characters; the instruction
budget is an exact integer of 1–4,096. The copied typed witness names an in-budget
step and canonical `x1`–`x31`. Preflight source UTF-8/8,192 lines and all supplied
shapes/bounds before schema or assembler tool reads. There is no artifact path,
source reopen, output or reference process. Tool/schema reads are explicit; payload
bounds are not exact RAM or time limits. The caller owns authentication and the
aggregate read/payload budgets when composing this API.

The existing expectation mapper validates exactly one complete ordered baseline
document and RV64 GPR values; no second loader is introduced. Require the exact
program/budget and an explicit RV64 entry. A valid entry outside the snapshot
author's fixed cold context is unsupported. Cross-model exclusions, declared
profile divergence and fault injection remain unsupported. Declared delivery/wait
labels or derivation markers, and any source boundary without a complete fetched
instruction, need a later typed event binding. This first consumer therefore
credits ordinary fetched GPR changes only, including mixed widths and changed
instruction memory. Source directives cannot override the stock numerical rules.

Derive once through `derive_snapshot`; bind its complete context/step sequence
to the request. Compare every step's complete GPR change set as RV64 integers,
including missing/extra changes, before accepting the named witness. Matching
only the witness is insufficient. The witness must actually change its selected
register; x0 and unchanged-register invariants need another observation method.
Expectation instruction labels and source/derivation prose confer no semantic
authority. Fetch-count and negative-observation metadata earn no additional credit.

The frozen `SourceExpectationCheck` has `disposition`, `reason`, optional `facts`
and optional structured `difference`. `facts` contains the frozen public snapshot
derivation, baseline byte size/SHA256, copied witness and its derived RV64 value
(`None` when the register does not change).
The snapshot includes source/payload identities, actual instruction bits/PCs and
stock source/derivation text. It contains no raw source or expectation bytes.
A difference records the first step and complete derived/expected GPR sets;
matched and failed value checks retain their independent derivation facts.

`matched` means the supplied source derives all these GPR changes and the witness;
`failed` means coherent GPR data differs or the witness is not an actual change.
Malformed inputs or contradictory returned context are `refused`; unavailable
canonical author context is `unavailable`; unsupported source/event/context is
`unsupported`. Existing schema-tool failure classification stays with the shared
expectation decoder. Unexpected programming failures propagate. No result grants
artifact authenticity, original-capture chronology, producer authenticity or
ancestry, source/requirement adequacy, reference PC/encoding equality, full method
qualification or CPU acceptance. The existing three-run and retained-evaluator
APIs keep their contracts; composition is a later owned slice.

Run this complete synthetic example from the repository root. It derives both
boundaries, then detects a changed value in the supplied expectation; no reference
process or capture is involved.

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, 'scripts')
import dossier_sexp as D
import records_sexp as R
from matched_gpr_comparison import GprWitness, compare_source_expectation

source = b'addi x1, x0, 5\nc.addi x1, 1\n'
doc = dict(program='example.s', entry='0x80000000', instructions=2, step=[
    dict(n=n, insn='example', writes={'x1': hex(value)},
         derivation='synthetic example', source='illustration')
    for n, value in enumerate((5, 6))])

def compare():
    return compare_source_expectation(
        source=source, baseline_expectation=R.render_forms([D.expectations_to_form(doc)]).encode(),
        program='example.s', instructions=2, witness=GprWitness(1, 'x1'))

matched = compare()
print(matched.disposition, matched.facts.witness.step_n,
      matched.facts.witness.register, matched.facts.witness_value)
doc['step'][1]['writes']['x1'] = '0x7'
failed = compare()
print(failed.disposition, failed.difference.step_n,
      failed.difference.observed, failed.difference.expected)
doc['entry'] = '0x80000002'
print(compare().disposition)
PY
```

```text
matched 1 x1 6
failed 1 (('x1', 6),) (('x1', 7),)
unsupported
```

`python3 scripts/probe_matched_gpr_derivation.py` and its `python3 -O` variant
each pass 23 tests; 19 omissions each lose assertions with zero errors. Existing
52-test byte-comparison controls and 14 omissions retain identical normal/optimized
results. Canonical capability checks account for all 167 guests: 125 match over
3,794 steps, 41 are explicitly unsupported (17 source-control/semantic, 17 event-boundary,
seven expectation-exclusion cases). `min-fencei.s` has no changing GPR witness and
gets no credit from this method. Those checks neither regenerate the fixtures nor
qualify a capture, requirement or processor.

The original entry-context probes retain 25 tests/16 omissions, and program
context retains 23/7, normally and optimized. Their selectors target the original
public guards explicitly; all 56 omission sites across the four comparator
consumers are singular. An ambiguous selector is a harness refusal and earns no
semantic-control credit.

## Authenticated source-value composition (a42q)

`evaluate_retained_unit` now calls `compare_source_expectation` after its
successful three-run comparison and complete source/ELF correspondence. It uses
the exact retained source/baseline snapshots and the existing frozen parent
program, budget and witness. It neither reopens artifact paths nor runs another
expected-result implementation. Existing identity, receipt, authentication,
comparison, input-review, impact and image findings stay separate.

Append optional `EvaluationCheck.source_values: SourceExpectationCheck | None`
after all existing positional fields. It is absent before this phase, including
failed/unsupported byte comparisons and unsuccessful source/image checks. Once
reached, return the public source-value result with its frozen metadata and no
raw payload. A returned matched/failed derivation must agree with the independent
image finding's program, entry, encoding path, source size/SHA256 and initial
payload size/SHA256. Contradictory contexts refuse. Actual retained ELF equality
remains the image owner's check; this does not duplicate or replace that rule.

Source-value `failed`, `refused` and `unavailable` results make evaluation return
that disposition while retaining all earlier findings. The source API's ordinary
fetched-boundary scope is narrower than the prospective complete method. Its
`unsupported` result therefore leaves evaluation **pending**, with the explicit
unsupported finding and no source-value credit. It does not turn a byte-supported
historical record into a claim that the full method can never support it. Invalid
or unknown source-result shapes refuse; an invalid/misbound source finding is not
retained. Unexpected programming failures propagate.

A source-value match also leaves evaluation **pending complete method/policy
adequacy**. Frozen selection proves which declared witness was checked; it does
not establish the meaning of a requirement, the declared producer's authenticity,
complete dependency/source adequacy, collector provenance, ancestry or capture
freshness. No stored success flag, canonical qualification, requirement status or
CPU acceptance is added. PROFILE-CONSISTENCY's qualification refusal remains.

Shared artifact-read and retained-payload ceilings stay 128 MiB and 16 MiB, with
the existing per-role bounds. The author uses at most 32 KiB of temporary initial
instruction bytes after the image reconstruction has released its at-most-64-KiB
ELF. Reuse the existing reserved temporary payload room; do not add artifact reads
or retain either rebuilt byte image in the result. Parsed objects, hart state,
steps and immutable copies remain outside these payload-only bounds; they are
not exact RAM ceilings. Canonical schema/assembler data reads remain explicit
tool I/O with complete current dependency adequacy still separately required.

This complete synthetic example makes every temporary artifact under the
repository's `target` directory and removes it afterward. The existing fixture
helper builds example pins/receipts; no reference executable is run and no
capture is qualified.

```bash
python3 - <<'PY'
from copy import deepcopy
from pathlib import Path
import sys
import tempfile
sys.path.insert(0, 'scripts')
import matched_gpr_evaluation as E
from probe_matched_gpr_evaluation import Fixture, PC

scratch = Path('target/source-value-example')
scratch.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(dir=scratch) as directory:
    fixture = Fixture(Path(directory))
    matched = E.evaluate_retained_unit(fixture.root, **fixture.arguments())
    print(matched.disposition, matched.source_values.disposition,
          matched.source_values.facts.witness_value)

    fixture.base['step'][0]['writes']['x1'] = '0x9'
    fixture.control = deepcopy(fixture.base)
    fixture.control['step'][0]['writes']['x1'] = '0xa'
    fixture.write(fixture.inputs['expectation'], PC.encode(fixture.base))
    fixture.write(fixture.inputs['mutant-expectation'], PC.encode(fixture.control))
    trace = (b'[0] [M]: 0x0000000080000000 (0x00100093) addi x1, x0, 1\n'
             b'x1 <- 0x0000000000000009\n')
    for kind in fixture.runs:
        fixture.write(fixture.observation(kind, 'raw-gpr'), trace)
    fixture.publish_receipts()
    failed = E.evaluate_retained_unit(fixture.root, **fixture.arguments())
    print(failed.disposition, failed.comparison.disposition,
          failed.source_image.disposition, failed.source_values.difference.observed,
          failed.source_values.difference.expected)
PY
```

```text
pending matched 1
failed satisfied matched (('x1', 1),) (('x1', 9),)
```

The first result earns no complete-method credit. The second retains a satisfied
three-run byte comparison and matching source/ELF bytes while the source-derived
GPR values fail. The trace/expectation pair cannot supply its own source proof.
