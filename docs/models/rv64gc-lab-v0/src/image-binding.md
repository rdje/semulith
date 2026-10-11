# Explicit image context

A source rebuild needs the selected program identifier and entry address. An
expectation file may declare those facts, but reading arbitrary fields from an
unchecked dictionary would bypass the byte comparison's validation. The public
`matched_gpr_comparison.expectation_image_context` reuses that same expectation
owner and returns only three frozen facts: `program`, `instructions` and `entry`.
This is the context boundary for a later source/image check.

## Select before interpreting bytes

The caller supplies an explicit plain string `program` of 1–65536 characters and
a plain integer `instructions` of 1–4096. Invalid selections refuse before parsing
or schema-tool reads. Program identifiers compare exactly: `demo.s`, `./demo.s`
and `Demo.s` are different labels. The API does not resolve them as paths.

The payload must be nonempty plain `bytes`, at most 1 MiB. After those guards, the
existing decoder validates raw schema before the sole mapper; it requires one
expectations document, the selected instruction count, a complete ordered step
sequence, canonical changed-register names and RV64 write values. This consumer
therefore cannot extract a plausible entry while ignoring an invalid later step.
It calls that decoder once, with the supplied bytes and selected budget.

The validated expectation must name the selected program and explicitly contain
a string `entry`. The existing hexadecimal RV64 owner parses it into an integer
in the inclusive range 0–18446744073709551615. Uppercase hexadecimal prefixes and
leading zeros are numeric aliases. There is no default entry address. A missing,
malformed or out-of-range entry raises `UnitError` and yields no context. Generic
expectations still allow an omitted entry; the extra requirement belongs to this
image consumer. Existing byte comparisons retain their APIs and classifications.

An odd entry such as `0x1` is valid metadata here. Alignment, load extent and image
construction belong to the [bounded builder](evaluation.md#build-an-image-from-source-bytes).
Entry extraction supplies no aligned-image claim.

## Run the context example

Run from the repository root. The document is deliberately synthetic; its
`derivation` and `source` strings provide shape, not specification evidence. The
example demonstrates exact parent binding, hexadecimal aliases and refusals
without reading an artifact path or constructing an image.

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, 'scripts')
from matched_gpr_comparison import expectation_image_context, UnitError

payload = b'''(expectations
  (program "demo.s") (entry "0X000080000002") (instructions 1)
  (step (n 0) (insn "addi x1, x0, 1")
    (derivation "synthetic example, not independent evidence")
    (source "synthetic fixture")
    (writes (write (reg "x1") (value "0x1")))))'''
context = expectation_image_context(payload, instructions=1, program='demo.s')
print(context.program, context.instructions, hex(context.entry))
odd = payload.replace(b'0X000080000002', b'0x1')
print('metadata entry', expectation_image_context(odd, instructions=1, program='demo.s').entry)
for data, program in ((payload, './demo.s'),
                      (payload.replace(b'(entry "0X000080000002")', b''), 'demo.s'),
                      (payload.replace(b'0X000080000002', b'0x10000000000000000'), 'demo.s')):
    try:
        expectation_image_context(data, instructions=1, program=program)
    except UnitError as exc:
        print('refused', str(exc))
PY
python3 scripts/probe_matched_gpr_entry.py
python3 -O scripts/probe_matched_gpr_entry.py
```

The values are `demo.s 1 0x80000002` and `metadata entry 1`. Refusals say
`expectation program differs from parent`,
`image expectation requires an explicit string entry`, and
`image expectation entry: hexadecimal RV64 value required`. Both probe commands
report 25 tests, zero failures and zero errors. Sixteen independent omissions of
selection, bounds, validation, forwarding, entry checks or immutability fail in
both modes, with zero harness errors. The original 52 comparison controls and
14 omissions, and 23 parent-program controls and seven omissions, retain their
outcomes. Explicit production guards remain active under Python optimization.

## What the context establishes

The frozen result retains no expectation bytes, pins, paths, process results or
qualification fields. The API performs no artifact-path reads, image builds,
process launches or writes. Its schema loader reads project tools; those reads
are outside supplied-artifact budgets. The byte bound is not a process RAM or
execution-time bound, and the API supplies no new aggregate-budget accounting.

The caller owns authentication of the supplied snapshot, selection and freezing
of the current parent, and complete current tool adequacy. An expectation's
unsupported flags are metadata here: `cross_model false` does not prevent entry
extraction and supplies no comparison or adequacy credit. A valid context proves
neither instruction semantics nor a source-grounded expected property.

To check correspondence, pass the selected label and numeric entry with source
and complete ELF snapshots to the [source/image consumer](evaluation.md#compare-complete-source-and-image-bytes).
Its authentication and aggregate reservation obligations still apply. The
[shared ledger's opt-in retention](closure.md#retain-source-and-elf-bytes-for-a-later-check)
can retain those snapshots within its existing budgets. The authenticated
evaluator has not yet composed that retention, this context and correspondence.
Complete closure, conservative impact, source-grounded properties, collection
provenance and full method/policy adequacy remain pending; no qualification or
CPU acceptance follows from this context.
