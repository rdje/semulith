# Collecting a three-run unit

`matched_gpr_unit_collector` implements the baseline/repeat/control collection
boundary for `sail-gpr-change-v1`. The caller first validates the raw parent
schema/scoped graph and obtains the public execution binder's plan. Collection
records fresh processes and outputs; it does not compare traces, publish a
canonical experiment, establish dependency adequacy or qualify a requirement.

## Freeze and preflight the whole unit

`freeze_unit(plan, outputs=...)` takes exactly twelve `OutputTarget` values and
returns a frozen `UnitRequest` containing three run requests in baseline, repeat,
control order. Freeze all used fields before artifact I/O. Require the common
binary, boundary count and seven principal inputs, the same baseline/repeat
expectation, a distinct control expectation, and globally distinct run/output
IDs and paths. Every input and all twelve output identities participate in the
preflight; an output cannot erase the other run's expectation.

`capture_unit(root, request=..., max_read_bytes=134217728)` requires all twelve
output names to be absent in existing safe same-volume parents. Use a new owned
output set for each capture. It never removes an older capture. Anchor the
parents, refuse symlinks/nested Git boundaries and reserve every output name
exclusively before launching any process. This proves actual namespace
separation, including case/normalization aliases on the current filesystem.
Remove only those owned reservations, preserving any foreign replacement.
Recheck the anchored parents before and after each run. As with the one-process
collector, this is a finite POSIX protocol with owned paths, not a transaction
against concurrent hostile namespace mutation or escaping daemons.

## Share one read allowance

The one-process APIs now accept `max_read_bytes` and report immutable
`charged_read_bytes` counters. Limits are plain integers, inclusive, from zero
to128 MiB; Boolean/negative/oversized values refuse before I/O. `capture_run`
defaults to its existing128 MiB allowance. For compatibility,
`capture_run_with_receipt` defaults to `None`, retaining the original128 MiB
process allowance plus at most8,716,288 publication-read bytes. An explicit
integer instead shares that allowance across collection and publication.
Existing positional result fields remain first; the counter is appended with
a default of zero.

Reserve each bounded read before calling the reader. Refund only after complete
matching metadata validates, using the actual observed byte count. A failed,
malformed or escaping reader keeps its entire reserved allowance charged;
partial consumption is not exposed by every reader failure. Stop that helper
immediately. Empty files may match at a zero-byte allowance without a payload
read. No helper can borrow from a later run or reset the unit allowance.

`capture_unit` passes the remaining allowance to each receipt-producing call and
subtracts its charge before continuing. Invalid findings conservatively consume
the entire delegated allowance and refuse. The unit's counter is therefore a
conservative bound on artifact reads, including executable/input pin checks,
output observations, receipt reads and publication rechecks. Schema/tool/runtime
I/O and process RAM are separate from this artifact-read budget. Collection
retains no trace/expectation payloads; the16 MiB retained-snapshot budget belongs
to subsequent evaluation. A combined pipeline must carry this charge forward
rather than reset its allowance for that evaluation.

## Results and failures

`UnitCapture` contains the disposition/reason, the ordered `PublishedCapture`
results actually reached, and total `charged_read_bytes`. It returns `recorded`
only after three distinct observed PIDs, three zero exits and twelve bounded
output metadata records. This is collection success, never comparison success.
A recorded nonzero/signal exit instead returns `failed` with its failed-process
receipt and stops before the next process. Other failures retain their
`stale`/`unavailable`/`refused` disposition and reached metadata. A failed unit
never returns a success receipt inventory. Completed files remain historical
observations; unexecuted runs have no returned observations. Reservations normally
vanish before execution. If an observed Git boundary revokes cleanup authority,
refuse and leave earlier empty reservations in place.

Tests use actual synthetic children and separately labeled live Sail smoke.
They must discriminate aggregate exhaustion, exact inclusive limits, failed
reader charging, frozen requests, cross-run/path aliases, pre-existing outputs,
exclusive reservations and early termination in both Python modes. Full closure,
source/property review, policy binding, canonical retention and qualification
remain separate work.

## Complete synthetic example

This runs three synthetic reference processes and publishes their receipts. The
five-byte traces test collection, not instruction semantics.

```bash
python3 - <<'PYCODE'
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
sys.path.insert(0, str(Path('scripts').resolve()))
import matched_gpr_collector as C
import matched_gpr_unit_collector as U
from probe_matched_gpr_collector import Fixture

base = Path('target/unit-collector-example')
base.mkdir(parents=True, exist_ok=True)
with TemporaryDirectory(dir=base) as directory:
    f = Fixture(Path(directory))
    # The fixture initially has old synthetic observations. This example owns
    # them and removes them before requesting a fresh unit output set.
    for item in f.graph['observation']:
        (f.root / item['path']).unlink()
    plan = C.E.bind_execution(f.experiment, f.candidate).plan
    outputs = tuple(C.OutputTarget(o['role'], o['id'], o['path'])
                    for o in f.graph['observation'])
    request = U.freeze_unit(plan, outputs=outputs)
    result = U.capture_unit(f.root, request=request)
    print(result.disposition, len(result.runs),
          len({r.process.pid for r in result.runs}),
          all(r.process.process_exit == 0 for r in result.runs))
    print(0 < result.charged_read_bytes <= C.TOTAL_BYTES,
          all(r.receipt is not None for r in result.runs))
    again = U.capture_unit(f.root, request=request)
    print(again.disposition, len(again.runs), again.charged_read_bytes)
PYCODE
```

Output:

```text
recorded 3 3 True
True True
refused 0 0
```

The second request refuses before a process or artifact read because those
outputs now exist. Their bytes remain intact. A new capture needs new output
names; the helper does not replace prior evidence.

The normal CI controls require no external reference cache:

```bash
python3 scripts/probe_matched_gpr_unit_collector.py
python3 -O scripts/probe_matched_gpr_unit_collector.py
```

With the already acquired pinned Sail executable, the optional live unit smoke
reuses the existing public m-div comparison and exact wrong-value witness:

```bash
python3 scripts/probe_matched_gpr_unit_collector.py --real-sail-smoke
```

It calls the unit collector once, reports three fresh zero-exit process receipts
and AGREE/AGREE/DIVERGE, and removes its unique on-volume scratch. The report
includes the unit's read charge/limit. This prospective test envelope still has
synthetic identities and an incomplete dependency list; raw scoped-record and
closure adequacy are unestablished, canonical capture is false and qualification
is closed. It establishes the collection route, not CPU acceptance.
