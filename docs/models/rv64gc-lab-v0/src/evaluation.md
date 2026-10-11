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
set covers every relevant dependency. Source/image correspondence,
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

Full CI passed on the clean composition milestone. Complete adequacy, reviewed fresh
collection, retention/case/capture declarations and full policy/status derivation
remain subsequent owned work. No canonical capture or CPU acceptance changes here.

## Bind the parent program identifier

The evaluator now freezes the parent experiment's `program` before artifact reads,
normalizing an accepted mapped string to a plain value. For a supported rule, a value outside 1–65,536
characters refuses before the manifest read. Unknown rules remain `unsupported`
before this method-specific bound applies. Both authenticated expectation
snapshots must name that exact program, even when their two labels agree with
each other. Case, prefixes and whitespace are significant; the checker does not
infer a path from a basename. Unsupported expectation flags do not excuse a
contradictory program identifier.

The public `compare_unit` accepts an optional `program` keyword for this binding.
When supplied, it requires a plain string within the same character bound before
payload parsing, then checks both validated, singly mapped expectations. Omitted
or `None` context preserves the existing pure byte-unit API. The evaluator always
supplies the frozen context. This creates no second expectation loader or artifact
reopen, and does not change the fixed artifact read/snapshot budgets.

Identifier equality is one adequacy obligation. It does not establish that the
pinned source assembles to the pinned image, that the image corresponds to a
source-grounded property, or that the dependency closure and collector are
adequate. Those checks remain mandatory subsequent work. Positive evaluation
still returns `pending`; no canonical capture or CPU acceptance is added.

This example changes both expectation labels, then republishes their exact pins
and receipts. All bytes authenticate, but the parent relationship refuses:

```bash
PYTHONPATH=scripts python3 - <<'PY_PROGRAM'
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from matched_gpr_evaluation import evaluate_retained_unit
from probe_matched_gpr_evaluation import Fixture
from probe_matched_gpr_comparison import encode

parent = Path("target/parent-program-example")
parent.mkdir(parents=True, exist_ok=True)
with TemporaryDirectory(dir=parent) as directory:
    fixture = Fixture(Path(directory))
    def check():
        return evaluate_retained_unit(fixture.root, **fixture.arguments())
    print(check().disposition)
    for role, original in (("expectation", fixture.base),
                           ("mutant-expectation", fixture.control)):
        changed = deepcopy(original)
        changed["program"] = "consistently-wrong.s"
        fixture.write(fixture.inputs[role], encode(changed))
    fixture.publish_receipts()
    result = check()
    print(result.disposition, result.record.disposition,
          result.authentication.disposition, result.comparison)
    print(result.reason)
PY_PROGRAM
python3 scripts/probe_matched_gpr_program.py
python3 -O scripts/probe_matched_gpr_program.py
```

It prints `pending`, then `refused valid matched None`, then
`comparison: expectation program differs from parent`. The final commands run
23 controls in each mode. Seven omissions lose 7/13/5/1/1/1/1 assertions with zero
test errors in both modes: type/bound, program binding, forwarding, pre-read
freeze, early evaluator bound, plain-value normalization and rule selection. Existing 52
comparison and 42 evaluation controls remain green; their APIs and omission
controls remain covered. The earlier a41 synthetic positive was explicitly
pending these adequacy obligations, so the new refusal does not rewrite a
historical qualification or execution claim.

A draft initially applied the parent bound before rule selection. The combined
unknown-rule/oversized-label control reproduced a diagnostic regression from
`unsupported` to `refused`, with no artifact reads or qualification. Move the
bound after supported selection, still before artifact I/O. The exact recovered
draft loses one assertion with no errors normally and optimized; the repaired
23-case suite passes. This ordering preserves method support as a separate finding.

## ELF container alignment

The public `scripts/riscv_asm.py::write_elf64(path, entry, payload, ialign)` writes
one RV64 little-endian executable. IALIGN is explicit profile data: 16 or 32 bits.
It preserves the supplied payload exactly, with one read/write/execute PT_LOAD
at the entry's virtual and physical addresses and equal file/memory lengths.
Null, `.text` and `.shstrtab` headers remain available to public loaders.

The file offset is the first offset after the 120-byte header area congruent to
entry modulo 4096. For entry 0x80000000 it is 4096; for 0x80000002 it is 4098.
Zeros before the payload are outside PT_LOAD and add no guest instructions.
The string table follows the payload; up to seven zero bytes align the section
table to 8. Text alignment is 2 for IALIGN=16 and 4 for IALIGN=32, including legal
halfword entries. These are the [gABI segment](https://gabi.xinuos.com/elf/07-pheader.html),
[section](https://gabi.xinuos.com/elf/03-sheader.html) and
[natural structure alignment](https://gabi.xinuos.com/elf/01-intro.html) constraints.

Ratified RVI-PSABI 1.0 §8.1 requires EF_RISCV_RVC=1 when the binary permits 16-bit
instruction alignment. The writer sets this bit for IALIGN=16. Float-ABI bits
remain 0 (soft-float calling convention); internal FP instructions do not imply
a hardware floating-point calling convention. This freestanding container makes
no compiled LP64D claim. The pinned PDF is catalogued as RVI-PSABI-1.0 and in this
unit's sources; the [published psABI](https://riscv-non-isa.github.io/riscv-elf-psabi-doc/)
explains the same distinction.

Run this complete example from the repository root. It emits ignored artifacts,
reads literal ELF64 field layouts independently, then runs both control modes:

```bash
python3 - <<'PY'
from pathlib import Path
import struct, sys
sys.path.insert(0, 'scripts')
from riscv_asm import write_elf64
out = Path('target/elf-layout-example')
out.mkdir(parents=True, exist_ok=True)
for entry, ialign in ((0x80000000, 32), (0x80000002, 16)):
    path = out / f'ialign{ialign}.elf'
    payload = b'\x13\x00\x00\x00'
    write_elf64(path, entry, payload, ialign)
    data = path.read_bytes()
    h = struct.unpack_from('<16sHHIQQQIHHHHHH', data)
    p = struct.unpack_from('<IIQQQQQQ', data, h[5])
    text = struct.unpack_from('<IIQQQQIIQQ', data, h[6] + 64)
    if data[p[2]:p[2] + p[5]] != payload:
        raise SystemExit('loaded payload differs')
    print(hex(entry), p[2], p[7], h[6] % 8, h[7], text[8])
PY
python3 scripts/probe_elf_writer.py
python3 -O scripts/probe_elf_writer.py
```

The first two lines are `0x80000000 4096 4096 0 0 4` and
`0x80000002 4098 4096 0 1 2`; each probe reports 15 tests/0 failures/0 errors.
Eight independent omissions fail in both modes. The controls cover every legal
page offset, exact headers/payload/string table/padding, upper address bounds,
real path writes and legacy bytearray payloads. Unknown/noninteger IALIGN,
noninteger/out-of-range entry, overflowing load extent and misaligned entry
raise AsmError before touching the output. Empty or odd-sized payloads remain
representable: this container writer does not validate instruction semantics.

D43-ELF-ALIGNMENT reproduced four inherited header defects from the exact old
writer. Its historical Sail/Spike tolerance was insufficient validation; the
Rust parser fixture was also synthetic, despite its old writer-round-trip name.
All 49 RV64I and 167 RV64GC guest payloads remain byte-identical after repair;
only ELF layout/metadata change, so newly generated ELF fingerprints change.
Retained historical artifacts and receipts remain immutable. These finite checks
supply no CPU acceptance, complete dependency adequacy or method qualification.
