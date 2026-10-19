# Collecting a fresh reference process

This is the implementation contract for P4-SYSTEM.14 a42v/a42w. The first comparison
method needs fresh baseline, repeat and control processes. A retained receipt or
matching trace hash alone cannot establish that they ran. This slice collects
**one process** through the published reference invocation. Complete experiment
orchestration, closure review, bounded canonical retention and
qualification remain separate work. No canonical capture is created here.

## Frozen request

`freeze_request(plan, run_id=..., outputs=...)` takes the public execution binder's
plan and exactly four `OutputTarget(role, observation_id, path)` values. The caller
owns raw schema/scoped graph validation and output-path ownership. Freeze every
used field into plain immutable values before any artifact I/O. Require this
method's fixed eleven reference arguments, 1–4096 boundaries, seven common inputs
and the selected expectation, distinct input/output identities and canonical
repository-relative paths. Refuse malformed/aliased requests before reads or
writes. Public plans are prerequisites, not self-authenticating capabilities.

`capture_run(root, request=...)` returns metadata only. Revalidate/copy the request;
a caller mutation during reads cannot redirect execution or output cleanup.
Authenticate the selected binary and eight input files before and after execution
using the existing shared reader, at most8 MiB/file and128 MiB aggregate. The
current pinned Mac-arm64 Sail binary is3801664B, within that existing bound.
The [unit collector](unit-collector.md) shares an explicit allowance across all
three runs; ordinary single-run calls retain their documented defaults.
A missing, unsafe or changed pin refuses collection; hashes describe check-time
bytes, not loaded-code attestation. Complete dependency adequacy remains caller
review work. The helper cannot discover all dependencies of arbitrary code.

## Owned outputs and fresh execution

Require existing same-volume output parents, refusing symlinks, Git metadata and
nested Git repositories. Check all targets before changing any: existing outputs
must have different device/inode identities from the binary, eight protected
inputs and each other. Lexically different paths can name the same file on a
case-insensitive volume; a later stale pin cannot undo an overwritten input.
Clear only the four declared regular output files, including an old receipt;
refuse special files/directories. Reserve all four names exclusively before
launch, so even previously absent case/normalization aliases refuse. Remove the
trace/receipt reservations and retain separate stdout/stderr files, even empty.
Never clear a whole directory. The reference creates its trace at the cleared
owned path. Temporary/cache environment paths derive from an owned output parent.

Launch a new POSIX session without a shell; stdin is the read-only OS null device. A small fixed Python exec shim sets a
4 MiB per-file hard limit, then replaces itself with the exact reference argv;
the recorded reference arguments exclude this implementation shim. The interpreter
is an external read-only toolchain dependency. A30-second deadline kills the owned
process group and reaps its leader; cleanup also runs on exceptions. Reap/terminate
that owned group before returning, including descendants. This is a finite POSIX
collector, not a portable claim about arbitrary process trees or hostile daemons
that deliberately escape their session.

After execution require a stable regular trace of at most4 MiB and stdout/stderr
of at most64 KiB each. The hard file limit limits overflow on disk; a stream over
its stricter64 KiB method bound still refuses, never truncates. The shared
`observe_bounded_file` API hashes a fresh file with anchored traversal, bounded
streaming and stability checks. Its `ObservedFile` result means **observed**, not
matched against a supplied pin; it retains no payload and exposes no PinResult.
Existing pin/snapshot APIs keep their supplied-digest authentication unchanged.
These limits are not exact total process RAM or filesystem usage ceilings.

## Result and credit

A `recorded` result contains the observed PID, actual exit status and three ordered
output metadata records. Nonzero/signal exits can be recorded as failed historical
data when their files are complete and bounded; they cannot satisfy a control.
Timeout, missing output, oversized observed files, unsafe paths or pin changes
cannot produce `recorded`. A hard-limit write failure may leave a bounded partial
trace and a failed exit; recording those bytes grants no completeness credit. Earlier refusals have no process identity. An old receipt is never
reused or minted by this helper. Neither `recorded` nor exit0 asserts trace
correctness, comparison success, source-property coverage or qualification.

Controls must execute real synthetic child processes, separately identified from
Sail. Discriminate stale output, missing trace, empty streams, failed/signal exits,
wrong/changed pins, unsafe targets, aliasing, overflow, deadline/group cleanup and
frozen context in both normal and optimized Python. Real Sail collection remains
separate from these synthetic controls; the [first canonical capture](canonical-division.md) is retained.

## Complete synthetic example

This example executes the control suite's **synthetic reference**, not Sail. Its
five-byte trace is deliberately not architectural evidence. The public execution
binder supplies the plan; the collector supplies actual process/output metadata.

```bash
python3 - <<'PYCODE'
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
sys.path.insert(0, str(Path('scripts').resolve()))
import matched_gpr_collector as C
from probe_matched_gpr_collector import Fixture

base = Path('target/collector-example')
base.mkdir(parents=True, exist_ok=True)
with TemporaryDirectory(dir=base) as directory:
    f = Fixture(Path(directory))
    plan = C.E.bind_execution(f.experiment, f.candidate).plan
    outputs = tuple(C.OutputTarget(role, f.observation('baseline', role)['id'],
                    f.observation('baseline', role)['path']) for role in C.E.OUTPUT_ROLES)
    request = C.freeze_request(plan, run_id=f.runs['baseline']['id'], outputs=outputs)
    result = C.capture_run(f.root, request=request)
    print(result.disposition, result.process_exit, len(result.outputs))
    f.mode('missing')
    result = C.capture_run(f.root, request=f.request())
    print(result.disposition, result.process_exit, bool(result.outputs))
PYCODE
```

Output:

```text
recorded 0 3
unavailable 0 False
```

The first run creates separate empty stdout/stderr files and observes a trace.
The second process also exits zero, but creates no trace. The collector removed
the old trace first, so this run is unavailable and returns no output facts.
Neither call publishes a receipt or qualifies the experiment.

A separate development smoke used the pinned Mac-arm64 Sail executable: three
fresh PIDs, all exit0, byte-identical27-boundary m-div traces. Public comparisons
were AGREE/AGREE/DIVERGE, with control step2/x7 observed -3 versus expected -4.
That smoke has no canonical capture, retained receipt, complete closure review or
qualification credit. The finite property and complete-method boundaries still
apply; synthetic process controls are not a substitute for that real run.

The optional reproducible live smoke is one command, with no network acquisition:

```bash
python3 scripts/probe_matched_gpr_collector.py --real-sail-smoke
```

It requires the already acquired pinned executable. It prints one JSON metadata
report and the live summary, then removes its unique on-volume scratch directory.
It uses the public override mapper without changing the shared materialized config.
The prospective envelope still uses synthetic IDs; raw scoped-record validation,
receipt publication, full closure and qualification are not established. Missing
or changed reference inputs return2/unavailable or refused, never a green smoke.
No mutation can be combined with this option. The normal CI command runs only
synthetic children and requires no reference cache.

## Publishing the fresh process receipt

`capture_run_with_receipt(root, request=...)` collects one process through
`capture_run`, then publishes its `sail-gpr-capture-v1` receipt. It freezes the
request and observed host OS/kernel/architecture before artifact I/O. Tool rows
identify the selected collector and reference by their SHA256 pins and record
the executing Python version. These observations describe this invocation;
they do not authenticate unknown dependencies or execution ancestry.

A `PublishedCapture` retains the process finding even when publication fails.
Only `recorded` has a fourth `CapturedOutput` for the receipt. The receipt binds
exact ordered argv, actual exit, candidate/binary pin, all eight input pins and
three output sizes/digests through the existing codec and receipt byte checker.
It never includes its own hash. Nonzero and signal exits remain failed-process
receipts. A collection failure publishes nothing and keeps its disposition.

Publication authenticates the three collected outputs again, then opens the
absent receipt name exclusively through anchored same-volume directories. It
refuses existing names, symlinks and nested Git parents; it never truncates or
replaces a receipt. Write at most64 KiB, handle short writes, fsync, authenticate
the resulting file and recheck the three outputs before success. Failure removes
only the receipt inode created by this call, never a replacement at that path.
No partial receipt is returned as recorded. Concurrent hostile namespace changes
are outside this finite POSIX collector's trust model; checks detect observed
replacement rather than claiming a filesystem transaction across all inputs.

The existing collector's per-call128 MiB read budget still applies. Publication
adds at most two reads of each bounded trace/stream and one64 KiB receipt read
(8,716,288 B), with no output payload retention. The serialized receipt is bounded
separately to64 KiB. An explicit read limit shares collection/publication accounting; the
[unit collector](unit-collector.md) carries the remainder across all three runs.
The [first canonical capture](canonical-division.md) is retained. Complete closure/policy adequacy and qualification remain pending.

## Complete receipt example

This executes the same synthetic reference used above and reads the receipt
through the published artifact codec. The streams are real empty files.

```bash
python3 - <<'PYCODE'
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
sys.path.insert(0, str(Path('scripts').resolve()))
from matched_gpr_collector import capture_run_with_receipt
from matched_gpr_artifacts import parse_capture
from probe_matched_gpr_collector import Fixture

base = Path('target/receipt-publication-example')
base.mkdir(parents=True, exist_ok=True)
with TemporaryDirectory(dir=base) as directory:
    f = Fixture(Path(directory))
    result = capture_run_with_receipt(f.root, request=f.request())
    receipt = result.receipt
    doc = parse_capture((f.root / receipt.path).read_bytes(), path=receipt.path)
    print(result.disposition, doc['run_kind'], doc['process_exit'])
    print(len(doc['input']), len(doc['observation']), len(doc['tool']))
    f.mode('failed')
    result = capture_run_with_receipt(f.root, request=f.request())
    print(result.disposition, result.process.process_exit)
PYCODE
```

Output:

```text
recorded baseline 0
8 3 3
recorded 7
```

The last line is a published failed-process receipt. It earns no agreement or
control success. Neither call creates a canonical experiment or qualifies one.

Run the synthetic publication controls in both Python modes:

```bash
python3 scripts/probe_matched_gpr_publication.py
python3 -O scripts/probe_matched_gpr_publication.py
```

The optional live smoke also exercises receipt publication with the already
acquired pinned Sail binary:

```bash
python3 scripts/probe_matched_gpr_publication.py --real-sail-smoke
```

It publishes three transient receipts, checks their exact bytes/argv/exits and
reuses the existing complete comparison/witness smoke. Normal and optimized
runs give AGREE/AGREE/DIVERGE with three distinct PIDs and identical traces.
Unique scratch and receipts are removed. The JSON report explicitly keeps
canonical capture false, closure adequacy unestablished and qualification closed.
