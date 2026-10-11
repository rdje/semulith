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
evaluator now composes that retention, this context and correspondence
[below](#compose-authenticated-source-and-elf-snapshots).
Complete closure, conservative impact, source-grounded properties, collection
provenance and full method/policy adequacy remain pending; no qualification or
CPU acceptance follows from this context.

## Compose authenticated source and ELF snapshots

`evaluate_retained_unit` now requests the shared reader's source/image retention
and combines the entry context above with complete byte correspondence. Its
function signature stays the same. The frozen `EvaluationCheck` appends an
optional `source_image` finding after all existing positional fields. The
[record, authentication and observed comparison fields](evaluation.md#independent-results-and-limits)
keep their separate meanings. A source/image mismatch can coexist with matched
authentication and a satisfied three-run comparison.

Before artifact I/O, the evaluator selects immutable source/image bindings from
the already frozen execution plan, alongside the selected program and budget.
The shared ledger authenticates each declared file once, including the earlier
manifest seed, and retains seventeen payloads. It uses the existing 1 MiB source
and 64 KiB image role caps and reserves another 64 KiB for the rebuilt ELF inside
the fixed 16 MiB snapshot ceiling. The cumulative artifact-read ceiling remains
128 MiB. The public reader's omitted/false flag still retains fifteen payloads;
only this evaluator now explicitly requests the opt-in.

The evaluator first checks the authenticated identity, receipts, complete byte
comparison and recorded verdicts as before. **Failed and unsupported comparisons
return before entry extraction or reconstruction**, with `source_image=None`.
An invalid entry or unavailable image tool must not hide those diagnostic
outcomes. A satisfied comparison reaches the public entry-context API using the
exact authenticated baseline expectation and selected parent program/budget.
The comparison's sole-value control already requires every other expectation
field to match; no second control-equality rule is introduced.

An entry-context `UnitError` yields a separate `refused` reason beginning
`image context:`. The satisfied comparison and authentication summary remain
available, and `source_image` is absent because reconstruction was not reached.
A missing entry is no longer enough for a positive composed evaluation, although
the generic expectation grammar and standalone comparison APIs still permit it.
Odd addresses remain valid context metadata; the builder loads its canonical
GC context, then owns alignment and load-extent refusals.

The evaluator forwards exact retained source/image bytes and validated
program/entry to `check_source_image` once. Its returned `SourceImageCheck` is
retained directly, with `matched`, `refused` or `unavailable` and metadata-only
facts. A complete-byte mismatch preserves both image fingerprints. Unavailable
canonical construction stays distinct from invalid source/image content;
unexpected programming failures propagate. Nothing is rebuilt from a reopened
artifact path. Later path changes cannot replace the supplied snapshots, and a
later check must authenticate again.

### Run the composed outcomes

Run from the repository root. `Fixture` is a test-data author using the public
encoders and builder. It writes a real GC source/ELF pair and explicit entry,
plus the synthetic 22-file record described in the
[evaluation example](evaluation.md#run-the-synthetic-evidence-cases). The source
and synthetic trace both describe `addi x1, x0, 1`; no reference process runs.
The builder used to author the image is also the reconstruction owner, so this
fixture is a composition control, not an independent encoding oracle or captured
experiment. The independent builder/correspondence controls remain separate.

```bash
PYTHONPATH=scripts python3 - <<'PY_IMAGE_EVALUATION'
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock
import matched_gpr_evaluation as E
from probe_matched_gpr_evaluation import Fixture, PC

base = Path('target/p4-system-14/a42d3b/book-fixtures')
base.mkdir(parents=True, exist_ok=True)
with TemporaryDirectory(dir=base) as directory:
    fixture = Fixture(Path(directory))
    def evaluate():
        return E.evaluate_retained_unit(fixture.root, **fixture.arguments())
    def show(checked):
        print(checked.disposition, checked.record.disposition,
              checked.authentication.disposition, checked.comparison.disposition,
              checked.source_image.disposition if checked.source_image else None)

    checked = evaluate()
    show(checked)
    print(hex(checked.source_image.facts.entry), checked.source_image.facts.encoding_path,
          all(fact.data is None for fact in checked.authentication.files))

    # Change unloaded ELF padding and re-pin the file/receipts: authentication
    # can match while complete source/image correspondence refuses.
    changed = bytearray(fixture.image)
    changed[200] ^= 1
    fixture.write(fixture.inputs['guest-image'], bytes(changed))
    fixture.publish_receipts()
    checked = evaluate()
    show(checked)
    facts = checked.source_image.facts
    print(facts.image_sha256 != facts.rebuilt_image_sha256,
          checked.authentication.disposition == 'matched')
    fixture.write(fixture.inputs['guest-image'], fixture.image)
    fixture.publish_receipts()

    with mock.patch.object(E.F.G, 'build_guest_image',
                           side_effect=E.F.G.ImageUnavailable('synthetic unavailable tool')):
        show(evaluate())

    fixture.runs['baseline'].update(process_exit=1, verdict='REFUSED')
    fixture.publish_receipts()
    with mock.patch.object(E.C, 'expectation_image_context', side_effect=AssertionError('entry reached')), \
         mock.patch.object(E.F, 'check_source_image', side_effect=AssertionError('build reached')):
        show(evaluate())

    fixture.runs['baseline'].update(process_exit=0, verdict='AGREE')
    for role, document in (('expectation', fixture.base), ('mutant-expectation', fixture.control)):
        document.pop('entry')
        fixture.write(fixture.inputs[role], PC.encode(document))
    fixture.publish_receipts()
    show(evaluate())
PY_IMAGE_EVALUATION
python3 scripts/probe_matched_gpr_image_evaluation.py
python3 -O scripts/probe_matched_gpr_image_evaluation.py
```

The five evaluations print `pending valid matched satisfied matched`,
`refused valid matched satisfied refused`,
`unavailable valid matched satisfied unavailable`,
`failed valid matched failed None`, and `refused valid matched satisfied None`.
The positive facts name entry `0x80000000` and canonical route
`profiles/rv64gc-lab-v0/encoding.sexp`, with all returned file payloads absent.
The two mismatch Booleans are `True True`. The unavailable tool is deliberately
simulated; it does not report that the current canonical tool is missing.

Both probe commands report 26 tests, zero failures and zero errors. Fourteen
independent omissions of retention, context validation/forwarding, exact byte
selection, no-reopen behavior, result propagation or comparison ordering must
fail in normal and optimized Python, without harness errors. The existing
42 evaluation controls/29 omissions and 23 parent-program controls/seven
omissions are re-run against the composed evaluator; prior receipts remain
immutable. Tests also cover source/image inclusive caps and one-byte overflow,
full ELF header/padding/payload/section changes, byte-equivalent comments,
nondefault entry and two-boundary budget, bundle release and programming errors.

### Remaining limits

Positive evaluation still returns `pending`, with no qualification field or CPU
acceptance. Correspondence establishes complete reconstructed ELF bytes, not a
source-grounded expected property, complete dependency closure, conservative
impact result, actual collector execution/provenance or full method/policy
adequacy. Caller-selected current parent, scoped authority, provenance and
complete current tool adequacy remain obligations. Other declared dependencies
in this fixture are opaque and cannot establish those facts.

The reader performs the reservation; the evaluator performs the reconstruction.
`snapshot_bytes` reports only payloads returned by the reader, excluding unused
rebuild room, the earlier manifest peak and process RAM. The extra 64 KiB bounds
one final rebuilt ELF payload. Source decoding, parsing objects/tokens, assembled
intermediate buffers, chunks, immutable copies and project-tool I/O are outside
that artifact-snapshot accounting. These are bounded supplied-artifact and final
image sizes, not an exact RAM or execution-time guarantee. No reference binary
or process is accessed; returned findings retain no supplied or rebuilt bytes.
