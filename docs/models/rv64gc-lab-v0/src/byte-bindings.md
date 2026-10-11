# Binding authenticated Sail snapshots

## Binding authenticated bytes to context frozen before reads

The [retained method readers](retained-method.md) authenticate one file and bind its contents. The declared
file-set reader already retains the exact identity and three receipt snapshots.
Calling the legacy readers again would reopen those paths and compare different
bytes. Use these public APIs instead:

| Before artifact I/O | After successful declared-file authentication |
| --- | --- |
| `bind_reference_identity(current_candidate)` → `ReferenceIdentity` | `check_reference_identity_bytes(payload, path=..., context=...)` → `IdentityCheck` |
| `bind_receipt_context(run=..., inputs=..., observations=..., current_candidate=...)` → `ReceiptContext` | `check_receipt_bytes(payload, context=...)` → `ReceiptCheck` |

Freeze **all** selected contexts before reading the manifest or other artifacts.
Run exit status and ordered argv are receipt context even though the execution
plan does not retain exit status. Optional candidate fields belong to identity
context even when absent. The selected context comes from the already raw-schema/
scoped-graph validated parent. Binders raise `IdentityError` or `BindingError`
without artifact or schema I/O. They validate only their used fields and existing
selected-context bounds; a receipt context can have fewer than eight inputs and
does not prove principal-role coverage or the fixed method invocation.

Contexts are frozen records containing immutable tuples and scalar values. Identity
binding normalizes accepted string subclasses to plain strings; optional presence
and value remain distinct. Receipt binding freezes run ID/kind, ordered argv,
exit, candidate/binary identity, collector ID, input ID/digest inventory, all three
non-receipt output identities/sizes/digests, and the receipt record/path. Create
contexts with the binders; manually forged receipt contexts are outside that API
contract. Later changes to caller dictionaries cannot update a bound context.
If a new context should apply, explicitly bind it and evaluate again.

Both byte consumers require 1–65536 immutable bytes, inclusive, before decoding or
schema work. Identity context counts/types and canonical diagnostic path precede
parsing. They reuse the existing raw schema, sole dossier mapper and binding owners;
project schema loading remains permitted tool I/O. They never open an artifact,
read a binary cache or execute a process. Pass the **same `FileFact.data` bytes**
from a successful file-set check; do not read a path to obtain another copy.

Every byte result has `pin=None`. Identity mismatch is `stale`; malformed identity
or unavailable identity schema refuses under the legacy identity contract. Receipt
contradiction/malformed bytes refuse; receipt schema-tool I/O is `unavailable`.
A matched receipt returns immutable facts, including coherent nonzero/signal exit
as failed-process data. A byte match does not authenticate itself. Combine it with
the separate file-set pin facts before making any authenticated-content claim.
Neither context nor byte binding supplies source correctness, complete dependency
coverage, image/program correspondence, execution attestation, observed comparison,
lasting currentness or qualification. Complete method composition remains pending.

This example uses only synthetic in-memory declarations and payloads. Its one
collector input and short argv intentionally satisfy selected receipt context,
not the complete method. Dummy digests authenticate nothing. It writes no files
and executes no reference process:

```bash
PYTHONPATH=scripts python3 - <<'PY_BYTES'
import dossier_sexp as D
import records_sexp as S
from matched_gpr_artifacts import encode_capture
from matched_gpr_identity import bind_reference_identity, check_reference_identity_bytes
from matched_gpr_receipt import bind_receipt_context, check_receipt_bytes

candidate = dict(id="sail-riscv", role="reference", status="illustrative",
                 origin="https://example.invalid/sail", kind="executable",
                 binary="reference/bin/sail", binary_sha256="a" * 64, version="v1",
                 lineage="unknown; synthetic example")
inputs = [dict(id="collector", role="collector", path="example/collector.py", sha256="b" * 64)]
outputs = [dict(id=name, role=role, path="example/base." + name,
                byte_size=0, sha256="c" * 64)
           for name, role in (("trace", "raw-gpr"), ("stdout", "process-stdout"),
                              ("stderr", "process-stderr"))]
receipt = dict(id="receipt", role="process-receipt", path="example/base.receipt.sexp",
               byte_size=0, sha256="d" * 64)
args = dict(run=dict(id="base", kind="baseline", argv=[candidate["binary"]],
                     process_exit=1, verdict="REFUSED", input_ids=["collector"],
                     observation_ids=[item["id"] for item in outputs] + ["receipt"]),
            inputs=inputs, observations=outputs + [receipt], current_candidate=candidate)
identity_context = bind_reference_identity(candidate)
receipt_context = bind_receipt_context(**args)
descriptor = dict(profile="example", retrieved="2026-10-11", work_dir="reference",
                  host=dict(os="example", kernel="example", arch="example", cxx="example"),
                  candidate=[candidate])
identity_bytes = S.render_forms([D.references_to_form(descriptor)]).encode()
capture = dict(format_version="sail-gpr-capture-v1", run_id="base", run_kind="baseline",
               argv=list(args["run"]["argv"]), process_exit=1,
               reference_candidate_id="sail-riscv", reference_binary_sha256="a" * 64,
               collector_input_id="collector", input=[dict(id="collector", sha256="b" * 64)],
               observation=outputs, host=dict(os="example", kernel="example", arch="example"),
               tool=[dict(id="collector", version="illustrative")])
receipt_bytes = encode_capture(capture, path=receipt["path"])
candidate["version"] = "v2"
args["run"]["process_exit"] = 0
identity = check_reference_identity_bytes(identity_bytes, path="example/identity.sexp",
                                           context=identity_context)
checked = check_receipt_bytes(receipt_bytes, context=receipt_context)
print(identity.disposition, checked.disposition, checked.facts.process_exit, identity.pin, checked.pin)
print(check_reference_identity_bytes(identity_bytes, path="example/identity.sexp",
                                      context=bind_reference_identity(candidate)).disposition,
      check_receipt_bytes(receipt_bytes, context=bind_receipt_context(**args)).disposition)
exact = identity_bytes + b" " * (65536 - len(identity_bytes))
print(check_reference_identity_bytes(exact, path="example/identity.sexp", context=identity_context).disposition,
      check_reference_identity_bytes(exact + b" ", path="example/identity.sexp", context=identity_context).disposition,
      check_receipt_bytes(memoryview(receipt_bytes), context=receipt_context).disposition)
PY_BYTES
python3 scripts/probe_matched_gpr_bytes.py
python3 -O scripts/probe_matched_gpr_bytes.py
```

It prints `matched matched 1 None None`, `stale refused`, then
`matched refused refused`. Frozen context still binds the original failed-process
bytes; rebinding detects the changed candidate version and exit. The inclusive
64 KiB identity succeeds; its extra byte and byte-view receipt refuse.
All 22 controls and fourteen independent omissions run in normal/optimized Python
under PROFILE-CONSISTENCY, alongside unchanged legacy identity40/receipt43 controls.
The suite also authenticates a real synthetic declared file set, changes its paths
and caller context afterward, and binds all three retained receipt snapshots with
artifact/process calls forbidden. This proves snapshot consumption, not adequacy
of those synthetic source/program/image payloads or complete qualification.
