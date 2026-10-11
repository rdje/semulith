# Dependency manifest and leaf inspection

## Authenticating and binding the dependency manifest

`matched_gpr_manifest.read_dependency_manifest(root, experiment=…,
current_candidate=…)` authenticates one selected manifest and binds its declared
file identities. The caller first validates the raw parent schema and scoped
graph and supplies the trusted runtime project root. The helper reuses the
relation binder, freezes the nine principal bindings and twelve output paths,
then reads exactly one authenticated manifest snapshot bounded to 64 KiB.

The existing codec validates raw syntax before its single mapping, permits 1–64
children and rejects duplicate child IDs/paths, unsafe paths, lexical self and
nested-manifest roles. Child IDs retain the published nonempty-string grammar.
The new binder allows an exact principal ID/role/path/SHA overlap once. A
conflicting identity, a path assigned another ID or a child aliasing a run output
refuses. The frozen union has at most 73 file bindings; child order is immaterial.
An exact overlap binds a declaration without authenticating that principal file.

A `matched` result authenticates only the manifest. Its pin finding remains
separate from binding: changed bytes are `stale`, missing data is `unavailable`,
unsafe/oversized/syntactically invalid/contradictory data is `refused`; legacy or
other comparison rules remain `unsupported`. Schema-tool I/O is `unavailable`
while retaining the already-matched pin. No manifest path is reopened after
checking its hash. A caller's later dictionary changes cannot alter frozen facts.

This standalone example uses the same fully shown synthetic parent fixture as
the invocation example. It creates only a temporary manifest under `target/` and
removes it afterward. All other-file pins are dummy declarations and their files
are absent. The example creates no Sail process or canonical capture:

```bash
PYTHONPATH=scripts python3 - <<'PY_MANIFEST'
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
import dossier_sexp as D
import experiment_verification as V
import sexp as S
from matched_gpr_artifacts import encode_dependencies
from matched_gpr_manifest import read_dependency_manifest
from probe_matched_gpr_execution import fixture, raw_experiment

root = Path.cwd()
output = root / "target/manifest-binding-example"
output.mkdir(parents=True, exist_ok=True)
with TemporaryDirectory(dir=output) as directory:
    prefix = Path(directory).relative_to(root).as_posix()
    experiment, candidate = fixture()
    manifest = next(item for item in experiment["verification"]["input"]
                    if item["role"] == "dependency-manifest")
    manifest["path"] = prefix + "/manifest.sexp"
    path = root / manifest["path"]
    doc = dict(format_version="matched-gpr-dependencies-v1",
               input=[dict(id="code dependency", role="implementation",
                           path=prefix + "/missing-code.py", sha256="c" * 64)])
    def publish(record):
        payload = encode_dependencies(doc, path=record["path"])
        path.write_bytes(payload)
        record["sha256"] = hashlib.sha256(payload).hexdigest()
    publish(manifest)
    raw = raw_experiment(experiment, candidate)
    scope = V.Scope("synthetic", frozenset({"sail-riscv"}), frozenset({"REQ-synthetic"}),
                    frozenset({"OBL-synthetic"}))
    issues = V.check_experiment(raw, scope)
    if issues:
        raise ValueError(issues)
    canonical = D.references_to_doc([S.Symbol("references"), raw])["experiment"][0]
    manifest = next(item for item in canonical["verification"]["input"]
                    if item["role"] == "dependency-manifest")
    def check():
        return read_dependency_manifest(root, experiment=canonical, current_candidate=candidate)
    checked = check()
    print(checked.disposition, len(checked.plan.inputs))
    canonical["verification"]["run"][2].update(process_exit=127, verdict="REFUSED")
    canonical["verification"]["control_run"][0]["observed_verdict"] = "REFUSED"
    failed = check()
    print(failed.disposition, failed.plan.relations.control_observed_verdict)
    doc["input"] = [deepcopy(canonical["verification"]["input"][0])]
    publish(manifest)
    overlap = check()
    print(overlap.disposition, len(overlap.plan.inputs))
    doc["input"][0]["path"] = canonical["verification"]["observation"][0]["path"]
    publish(manifest)
    bad = check()
    print(bad.disposition, bad.pin.disposition)
    path.write_bytes(b"changed after pin declaration")
    changed = check()
    print(changed.disposition, changed.pin.disposition)
PY_MANIFEST
python3 scripts/probe_matched_gpr_manifest.py
python3 -O scripts/probe_matched_gpr_manifest.py
```

It prints `matched 10`, `matched REFUSED`, `matched 9`, `refused matched`, then
`stale mismatch`. A valid failed-control record remains data. The exact overlap
is counted once; an output alias refuses despite a matched manifest pin; changed
bytes yield no parse or plan. The 33-test suite passes normal/optimized; eight
independent omissions lose 4/2/16/4/1/1/1/1 assertions with no harness errors.
PROFILE-CONSISTENCY runs both modes. Tests cover actual owned files, raw schema
before mapping, all overlap/alias constraints, 64/65 children, inclusive byte
limits, pre-read oversized refusal, snapshots, immutable context/results and
schema-tool unavailability. Temporary fixtures are cleaned after each test.

The helper does not read any child, input, trace, output or executable beyond
the manifest itself. A child disguised as another manifest remains unchecked.
Actual leaf authentication, complete dependency/source/program/image relationships,
old/new impact and aggregate authenticated/snapshot budgets remain mandatory.
A manifest plan grants no current closure, comparison, qualification or CPU credit.

## Inspecting one selected dependency leaf

`matched_gpr_leaf.inspect_dependency_leaf(root, manifest=plan, input_id=…,
max_bytes=…)` authenticates and classifies one child declared by that manifest
plan. Obtain the plan through the public manifest binder after raw parent-schema
and scoped-graph validation. The helper checks the child/union count envelope
before lookup, requires exactly one selected edge and binding, and copies that
binding before reading. A child cannot select the manifest itself or declare the
`dependency-manifest` role. Arbitrary nonempty child IDs remain supported.

The byte limit must be an integer in 0–8 MiB, inclusive. Zero permits an empty
file. One anchored authenticated snapshot supplies both the hash finding and
the content; there is no path reopen between authentication and interpretation.
Oversized files refuse before their payload is read. Failed authentication
prevents interpretation: mismatched bytes are `stale`, absent files are
`unavailable`, and unsafe paths or limits are `refused`. A successful result
retains frozen pin metadata and classification, without retaining the payload.

The classification asks whether those bytes are a document in the **published
bounded dependency format**. `matched_gpr_artifacts.is_dependencies_document`
reuses the existing raw schema and sole canonical mapper. Exactly one valid
`dependencies` document, with optional canonical comments, is a manifest.
Semantic defects in its edges, such as self-reference or a nested-manifest role,
do not hide its document identity. Such content is refused as nested, even when
stored under an implementation filename with a freshly matching hash.

The document format permits at most 64 KiB. Empty or larger payloads, invalid
UTF-8, malformed syntax, unknown fields/version, multiple roots and ordinary
source or binary data are `non-manifest` under that format. This classification
does not validate their source language or establish that they implement the
claimed program. In particular, valid Python `("dependencies", 1)` is ordinary
non-manifest content: a root-name resemblance alone is insufficient. The 8 MiB
leaf read limit and 64 KiB document-format limit serve different contracts.

Schema loading is project-tool I/O, separate from the selected artifact read.
For a nonempty payload within the document bound, unavailable or invalid schema
tools produce `unavailable` with the already-matched pin; they cannot turn a
document into ordinary content. Empty or over-format-bound bytes need no schema
load because they cannot be documents in this bounded format. The public format
classifier raises `ArtifactToolError` for tool failures and `ArtifactError` for
invalid caller arguments; the leaf helper reports these separately.

This standalone example creates only an outer manifest and its selected child
in a temporary directory on the repository volume. All other declared inputs,
outputs and the executable remain absent. Every published outer manifest is
validated through the raw scoped parent before binding. No producer is run and
no canonical capture is written:

```bash
PYTHONPATH=scripts python3 - <<'PY_LEAF'
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
import dossier_sexp as D
import experiment_verification as V
import sexp as S
from matched_gpr_artifacts import encode_dependencies
from matched_gpr_manifest import read_dependency_manifest
from matched_gpr_leaf import inspect_dependency_leaf
from probe_matched_gpr_execution import fixture, raw_experiment

root = Path.cwd()
output = root / "target/dependency-leaf-example"
output.mkdir(parents=True, exist_ok=True)
with TemporaryDirectory(dir=output) as directory:
    prefix = Path(directory).relative_to(root).as_posix()
    child_path = prefix + "/implementation.py"
    outer_path = prefix + "/manifest.sexp"
    child_file = root / child_path
    scope = V.Scope("synthetic", frozenset({"sail-riscv"}),
                    frozenset({"REQ-synthetic"}), frozenset({"OBL-synthetic"}))
    def publish(payload):
        child_file.write_bytes(payload)
        child = dict(id="code dependency", role="implementation", path=child_path,
                     sha256=hashlib.sha256(payload).hexdigest())
        outer = dict(format_version="matched-gpr-dependencies-v1", input=[child])
        encoded = encode_dependencies(outer, path=outer_path)
        (root / outer_path).write_bytes(encoded)
        experiment, candidate = fixture()
        declared = next(item for item in experiment["verification"]["input"]
                        if item["role"] == "dependency-manifest")
        declared.update(path=outer_path, sha256=hashlib.sha256(encoded).hexdigest())
        raw = raw_experiment(experiment, candidate)
        issues = V.check_experiment(raw, scope)
        if issues:
            raise ValueError(issues)
        canonical = D.references_to_doc([S.Symbol("references"), raw])["experiment"][0]
        checked = read_dependency_manifest(root, experiment=canonical,
                                           current_candidate=candidate)
        if checked.disposition != "matched":
            raise ValueError(checked.reason)
        return checked.plan
    def inspect(plan, **kwargs):
        return inspect_dependency_leaf(root, manifest=plan,
                                       input_id="code dependency", **kwargs)
    plan = publish(b'("dependencies", 1)\n')
    first = inspect(plan)
    print(first.disposition, first.classification)
    child_file.write_bytes(b"changed after declaration\n")
    changed = inspect(plan)
    print(changed.disposition, changed.pin.disposition)
    nested = dict(format_version="matched-gpr-dependencies-v1",
                  input=[dict(id="hidden", role="implementation",
                              path=prefix + "/absent.py", sha256="c" * 64)])
    plan = publish(encode_dependencies(nested, path=child_path))
    refused = inspect(plan)
    print(refused.disposition, refused.classification, refused.pin.disposition)
    plan = publish(b"")
    empty = inspect(plan, max_bytes=0)
    print(empty.disposition, empty.classification, empty.pin.byte_size)
PY_LEAF
python3 scripts/probe_matched_gpr_leaf.py
python3 -O scripts/probe_matched_gpr_leaf.py
```

It prints `matched non-manifest`, `stale mismatch`, `refused manifest matched`,
then `matched non-manifest 0`. Changing the selected path later does not change
the earlier frozen finding; it requires another read and authentication.

The 50-test suite passes normally and with optimization. Fifteen independent
omissions lose 4/2/2/2/7/4/8/4/11/7/6/1/3/8/2 assertions, with no harness
errors; PROFILE-CONSISTENCY registers both modes. Controls include actual
empty/binary/text/nested documents, the valid-Python regression, raw schema
before mapping, exactly one canonical mapping, inclusive 64 KiB and 8 MiB
boundaries, zero/custom/invalid limits, pre-read oversize refusal, consumed-byte
accounting, missing/unsafe/stale files, schema failures, immutable metadata and
snapshot-versus-later-path changes. Fixtures are cleaned after every test.

One matched leaf does not authenticate the remaining union. The following declared-file reader
owns shared read/snapshot budgets;
temporary parse objects and copies are additional RAM, not an exact memory cap.
Complete source/program/image relationships, impact, retained identities and
receipts, byte comparison and full method evaluation remain mandatory. This
helper grants no current experiment, complete closure, qualification or CPU
credit. The complete method evaluator must still compose those obligations explicitly.

## Authenticating the declared file set within shared budgets

`matched_gpr_files.read_declared_files(root, manifest=checked,
observations=records, max_read_bytes=…, max_snapshot_bytes=…)` consumes the
public manifest check and the twelve observation records from the same validated
parent. Raw parent/schema/scoped validation remains the caller's responsibility.
The helper authenticates the declared set; completeness of the dependency list,
source/program/image relationships, impact and full method evaluation remain
separate obligations.

Before any new artifact I/O it checks and freezes the used context: 1–64 distinct
children, 9–73 unique union inputs, nine consistent principal bindings and twelve
observations selected by the frozen three-run/four-role plan. IDs and paths are
unique in their respective families, observation paths cannot alias inputs, and
the union must equal the principals plus the declared child IDs. Exact principal
overlaps stay one file. It matches the earlier manifest pin's kind, ID, path,
SHA256 and size to the selected manifest and reuses that pin without reopening
the manifest.

The default aggregate limits are 128 MiB of authenticated project-file reads and
16 MiB of live snapshot payload. Custom limits must be exact integers in
0–128 MiB and 0–16 MiB, respectively. **Both must cover the known manifest
seed.** Its bytes have already been read and its earlier snapshot already
existed. Once released, those bytes leave room for later snapshots, while their
read charge remains cumulative. A zero aggregate limit cannot match this method:
its mandatory manifest is nonempty. An empty selected leaf still supports the
single-file zero limit described above.

This earlier-peak check matters even when all later snapshot files are empty.
The first draft admitted a zero snapshot limit after an actual 217-byte manifest
snapshot. The corrected helper refuses before any new read. The exact previous
draft loses three assertions against the new regression controls, normally and
with optimization. Passing the original controls did not establish that missing
boundary.

Each remaining distinct file receives one anchored authenticated read:

| Selected file | Per-file limit | Payload handling |
| --- | --- | --- |
| Earlier manifest | 64 KiB | Reuse its matched pin; charge its read and check its earlier peak |
| Reference identity | 64 KiB | Retain the authenticated bytes |
| Baseline and mutant expectations | 1 MiB each | Retain the authenticated bytes |
| Three raw GPR traces | 4 MiB each | Retain the authenticated bytes |
| Receipts, stdout and stderr | 64 KiB each | Retain the authenticated bytes, including empty files |
| Other principals | Explicit 8 MiB | Pin-only authentication unless also declared children |
| Other declared children | 8 MiB each | Inspect one transient snapshot, then release it |

A principal also listed as a child is inspected through the same read. Identity
and expectation overlaps retain their stricter principal bounds and their bytes;
other overlaps need a transient snapshot rather than a second pin-only read.
Every child uses the published format classifier from the previous section.
Disguised nested documents refuse, and unavailable schema tools remain separate
from content. Project schema-tool loading is separate from authenticated artifact
I/O and does not turn this ledger into a counter for every process read.

Transient child snapshots come first and are released before the next read.
Pin-only principals follow, then the retained inputs and observations. At each
read, the admitted cap is the smallest of its per-file bound and the remaining
aggregate read budget. Any snapshot, including a transient one, is additionally
bounded by the remaining live-payload room. Oversized files refuse before payload
reading; clipping a cap never truncates an artifact into accepted evidence.

The result exposes three distinct counters:

| Counter | Meaning |
| --- | --- |
| `authenticated_bytes` | Sum of known matched file sizes, including the manifest seed |
| `charged_read_bytes` | Actual matched sizes; after a failed reader call, its entire admitted cap is charged conservatively |
| `retained_bytes` | Payload bytes returned to the caller; zero on any failure |

The shared reader can fail after partially consuming a file without reporting
that partial byte count. Charging its whole admitted cap gives a safe upper bound.
The first failure ends the batch; no subsequent reads or internal retries can
reset that budget. Partial immutable pin/classification facts remain available,
while all earlier retained payloads are dropped. A content failure after a
matched read has a known byte charge. Changed pins are `stale`, absent data is
`unavailable`, and unsafe paths, exhausted limits or contradictions are `refused`.
Earlier failed/unsupported manifest findings pass through without new I/O.

The returned check, file facts, pins, plan and payload bytes are immutable. A
matched result retains fifteen payloads: the reference identity, two expectations
and twelve observations. Their maximum declared bounds sum to 14.625 MiB.
Transient payloads and the earlier manifest peak are checked separately against
the same live-payload ceiling. Parser objects, stream chunks and immutable copies
add memory; this is not an exact process-RAM bound. File facts describe their
individual reads, not an atomic snapshot of all paths or lasting currentness.

The following standalone example makes a synthetic runtime root under repository
`target/`. Every declared path is relative to that root; all temporary data stays
on the repository volume and is removed afterward. The public fixture supplies
the complete parent graph. Its opaque file payloads intentionally provide only
authentication examples: they are unsuitable for method comparison. The external
binary stays absent and no process or canonical capture is produced.

```bash
PYTHONPATH=scripts python3 - <<'PY_FILES'
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
import dossier_sexp as D
import experiment_verification as V
import sexp as S
from matched_gpr_artifacts import encode_dependencies
from matched_gpr_manifest import read_dependency_manifest
from matched_gpr_files import read_declared_files
from probe_matched_gpr_execution import fixture, raw_experiment

output = Path.cwd() / "target/declared-file-example"
output.mkdir(parents=True, exist_ok=True)
with TemporaryDirectory(dir=output) as directory:
    root = Path(directory)
    experiment, candidate = fixture()
    graph = experiment["verification"]
    manifest = next(item for item in graph["input"]
                    if item["role"] == "dependency-manifest")
    def write(record, payload):
        path = root / record["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
        record["sha256"] = hashlib.sha256(payload).hexdigest()
        if "byte_size" in record:
            record["byte_size"] = len(payload)
    for item in graph["input"]:
        if item is not manifest:
            write(item, ("synthetic " + item["id"]).encode())
    for item in graph["observation"]:
        write(item, b"x")
    child = dict(id="code dependency", role="implementation",
                 path="source/code.py", sha256="c" * 64)
    write(child, b'("dependencies", 1)\n')
    document = dict(format_version="matched-gpr-dependencies-v1", input=[child])
    scope = V.Scope("synthetic", frozenset({"sail-riscv"}),
                    frozenset({"REQ-synthetic"}), frozenset({"OBL-synthetic"}))
    def bind():
        write(manifest, encode_dependencies(document, path=manifest["path"]))
        raw = raw_experiment(experiment, candidate)
        issues = V.check_experiment(raw, scope)
        if issues:
            raise ValueError(issues)
        canonical = D.references_to_doc([S.Symbol("references"), raw])["experiment"][0]
        checked = read_dependency_manifest(root, experiment=canonical,
                                           current_candidate=candidate)
        if checked.disposition != "matched":
            raise ValueError(checked.reason)
        return checked, canonical["verification"]["observation"]
    checked, observations = bind()
    def read(**kwargs):
        return read_declared_files(root, manifest=checked,
                                   observations=observations, **kwargs)
    complete = read()
    total = sum(path.stat().st_size for path in root.rglob("*") if path.is_file())
    if (complete.authenticated_bytes, complete.charged_read_bytes) != (total, total):
        raise ValueError("file accounting differs from independent disk census")
    print(complete.disposition, len(complete.files),
          sum(item.data is not None for item in complete.files))
    exhausted = read(max_read_bytes=total - 1)
    print(exhausted.disposition, exhausted.retained_bytes)
    zero = read(max_snapshot_bytes=0)
    print(zero.disposition, zero.retained_bytes)
    (root / child["path"]).write_bytes(b"changed after declaration")
    stale = read()
    print(stale.disposition, stale.retained_bytes)
    nested = dict(format_version="matched-gpr-dependencies-v1",
                  input=[dict(id="hidden", role="implementation",
                              path="never/read.py", sha256="c" * 64)])
    write(child, encode_dependencies(nested, path=child["path"]))
    checked, observations = bind()
    refused = read()
    print(refused.disposition, refused.files[-1].classification,
          refused.files[-1].pin.disposition)
PY_FILES
python3 scripts/probe_matched_gpr_files.py
python3 -O scripts/probe_matched_gpr_files.py
```

It prints `matched 22 15`, `refused 0`, `refused 0`, `stale 0`, then
`refused manifest matched`. Authentication succeeds for the opaque initial
payloads without interpreting them as valid traces, expectations or identities.
The exhausted and stale results return no retained payload; the nested document
has a matched pin and a refused content finding.

The 49-test suite passes normally and with optimization. Thirty-one independent
guard omissions fail with no harness errors; PROFILE-CONSISTENCY runs both modes.
Controls cover actual files, 64 children/73 union inputs/85 total files, exact
principal overlaps, all per-role reader caps, independent consumed-byte totals,
inclusive/exhausted read and live-payload budgets, the known manifest peak, partial
I/O and descriptor-close failures, no reads after failure, payload release,
frozen context and metadata, nested documents/schema failures and later path
changes. Coherent failed-process records remain data. Every fixture is cleaned.

Successful file authentication grants no source correctness, complete dependency
coverage, observed comparison, execution provenance or qualification. The next
method evaluator must consume these exact snapshots, check identities/receipts
and program relationships, compare the complete runs and derive separate
dispositions. It must keep the existing qualification gate closed until all
remaining method and policy obligations are satisfied.
