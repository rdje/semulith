# Delegating the artifact read allowance

`matched_gpr_evaluation.evaluate_retained_unit` accepts the optional keyword
`max_read_bytes`. It delegates an inclusive allowance across the initial manifest
snapshot and subsequent declared-file authentication. The default is the existing
128 MiB (`134217728` bytes); callers may lower it. The fixed 16 MiB live snapshot
payload ceiling, per-role limits, qualification refusal and independent findings
remain unchanged. This API does not collect a reference process.

| API | Accepted allowance | Default | Accounting |
| --- | --- | --- | --- |
| `evaluate_retained_unit(..., max_read_bytes=n)` | Plain integer, `0 <= n <= 134217728` | `134217728` | Manifest seed and all declared files share `n`; the seed counts once. |
| `read_dependency_manifest(..., max_read_bytes=n)` | Plain integer, `0 <= n <= 65536` | `65536` | Only the selected manifest snapshot; no child reads. |

Booleans, integer subclasses, floats, strings, `None`, negative integers and
values above the API ceiling refuse. Evaluation checks this before raw-record
validation/schema I/O, returning `record.disposition == "unchecked"`; the
manifest helper checks before relation binding or artifact I/O. Existing scope
validation still applies. Zero allows no payload bytes. A nonempty manifest
therefore refuses at zero, with no declared-set authentication or property
finding. A file larger than its delegated cap refuses before payload reading.

Evaluation gives its manifest reader `min(n, 65536)`. After successful binding,
it passes the **same `n`** to the shared file ledger. That ledger starts with the
already-read manifest's byte count. Subtracting the seed again at this boundary
would charge it twice. Passing a fresh 128 MiB allowance would discard the
caller's limit. No manifest or other authenticated artifact is reopened.

## Carry collection charges forward

The [three-run collector](unit-collector.md#share-one-read-allowance) reports a
conservative `charged_read_bytes` count. A future combined driver must subtract
that charge from the fixed 128 MiB total and delegate only the remainder to
evaluation. For example, a collection charge of `134200000` leaves `17728`
bytes; evaluation cannot read beyond those 17728 bytes. This subtraction needs
validated, immutable collection metadata, not a caller's guessed byte total.
The public [combined unit helper](unit-evaluation.md) now implements that
reservation and refund protocol. The [composed command](capture-plan.md#the-composed-div-command)
now delegates it. Native declarations and the [canonical capture](canonical-division.md) are retained; full policy remains pending.

Reserve the whole delegated allowance before calling evaluation. Refund only
after validating the returned accounting: a plain integer charge within the
delegated allowance, covering the matched manifest seed and every authenticated
byte. After file-ledger preflight succeeds, `charged_read_bytes` includes the
seed and failed-read reservations. It may exceed successfully
`authenticated_bytes`; failed reads do not necessarily expose their partial
consumption. Never refund using only successful bytes. A failure before that
ledger starts can leave `authentication=None`, even if the manifest read consumed
bytes. A declared-file preflight refusal can also return a summary with charge
zero after that seed read: the ledger has not started. A raw-schema-valid trace
size above its role bound reproduces this case. Absent or inconsistent accounting
must keep the whole delegated allowance reserved. Stop on a
failure; do not retry with a reset budget or borrow from a later stage.

The bound covers artifact payload reads through these owners. It does not count
schema/tool/runtime I/O, process memory, caller-owned parent parsing, comparison
objects or copies. Snapshot payload accounting is separate from cumulative read
accounting; decreasing `max_read_bytes` never raises the 16 MiB snapshot cap.

## Exercise actual bounded reads

This complete example uses the property probe's fixture to create 23 real files
on the repository volume. It authenticates the actual retained DIV excerpt,
guest and expectations, with synthetic traces/receipts and a dummy reference
identity. Its independent path inventory supplies the exact required byte sum.
No Sail process, acquired materials cache or canonical capture is involved.

```bash
PYTHONPATH=scripts python3 - <<'PY_ALLOWANCE'
from pathlib import Path
from tempfile import TemporaryDirectory
from matched_gpr_evaluation import evaluate_retained_unit
from probe_matched_gpr_property_evaluation import Fixture

parent = Path("target/read-allowance-example")
parent.mkdir(parents=True, exist_ok=True)
with TemporaryDirectory(dir=parent) as directory:
    f = Fixture(Path(directory))
    records = [*f.graph["input"], f.child, f.normative,
               *f.graph["observation"]]
    paths = {item["path"] for item in records}
    needed = sum((f.root / path).stat().st_size for path in paths)
    def check(limit):
        return evaluate_retained_unit(f.root, max_read_bytes=limit,
                                      **f.arguments())
    zero = check(0)
    print(zero.disposition, zero.authentication, zero.source_property)
    exact = check(needed)
    print(exact.disposition, exact.source_property.disposition,
          len(exact.authentication.files),
          exact.authentication.charged_read_bytes == needed)
    short = check(needed - 1)
    print(short.disposition, short.source_property,
          short.authentication.charged_read_bytes <= needed - 1)
    invalid = check(True)
    print(invalid.disposition, invalid.record.disposition, invalid.manifest)
PY_ALLOWANCE
python3 scripts/probe_matched_gpr_read_allowance.py
python3 -O scripts/probe_matched_gpr_read_allowance.py
```

The example prints `refused None None`, `pending matched 23 True`,
`refused None True`, then `refused unchecked None`. Exact authentication and a
matched finite property still leave complete method/policy adequacy pending.
The diagnostic observes actual `os.read` payload counts, including unsuccessful
paths. Its controls cover exact/short/zero limits, invalid types/domains,
manifest clamping, the inclusive document ceiling, single seed accounting,
unchanged defaults, preledger refusal and stale/unavailable terminal outcomes. The collection-charge
control models caller arithmetic; it does not attest actual collection.
