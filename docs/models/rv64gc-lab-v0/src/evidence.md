# Current processor gate

The canonical dossier supplies this report. G-CONTRACT counts effective contract
versions and realized check bindings; the materials table retains historical
catalogue counts. Registration governs the review surface and collection census.
Requirements, frozen records and acceptance have their own authorities.

{{#include ../../../../profiles/rv64gc-lab-v0/GS-REPORT.md}}

{{#include ../../../ARCHITECTURE.md:rv64gc-snapshot}}

## Experiment identities

`PROFILE-CONSISTENCY` checks the existing `references.sexp` experiment grammar:
every experiment ID is unique within its dossier, every model names a declared
candidate, and a model occurs only once in an experiment. An independence row
must name two distinct candidates. These rules also apply to a one-model record;
missing a second comparator does not permit an invented first one.

For example, in a dossier whose only candidate is `sail-riscv`, this otherwise
well-shaped illustrative record is refused as `UNKNOWN EXPERIMENT MODEL`:

```lisp
(experiment (id "example-one") (program "example.s") (instructions 1)
  (models "missing-model") (verdict "AGREE") (reproduced "yes")
  (control "a wrong expected value was observed diverging"))
```

Using one ID for two conflicting experiment records is refused as
`DUPLICATE EXPERIMENT ID`. Repeating a candidate in `models` is refused as
`REPEATED EXPERIMENT MODEL`. This illustrative self-pair is refused as `BAD PAIR`:

```lisp
(independence (subsystem "example")
  (pair "sail-riscv") (pair "sail-riscv") (verdict "not-examined")
  (evidence "ancestry is unknown") (consequence "no independence credit"))
```

Run the positive and negative controls from the repository root:

```bash
bash scripts/check_profile_consistency.sh --self-test
```

A legal `not-examined` row records uncertainty. Metadata validation does not
establish adequate evidence, observed controls, current artifacts or independence.
Structured GC runs and policy-derived requirement status remain P4.14 work; the
generated gate report above remains the acceptance authority.

## Shared-reader refusals

All canonical S-expressions use `scripts/sexp.py`. A malformed integer matching
its numeric grammar raises `SexpError` with source/line, base and token length;
the diagnostic never repeats the whole token. The host decimal conversion limit
stays in force. Valid signed decimal/hex/binary values and symbols keep their
meaning; large power-of-two-base integers remain accepted. This parser has no
artifact byte budget: bounded evidence consumers must enforce their own limits.

The CLI reports expected parse, list-head, file-access and decoding failures as
`REFUSED` on stderr with exit1 and no success report. Wrong usage exits2. Head errors describe types and shapes, never whole values;
even a huge valid hexadecimal integer in head position gets a named refusal.
`read_file` remains a library API: I/O/decode exceptions propagate to its caller.
Empty lists are valid parser data but cannot supply the CLI's list-head summary.

From the repository root, these commands use only synthetic in-memory input and
owned temporary files under `target/`; the probe restores its decimal-limit fixture:

```bash
python3 scripts/sexp.py --self-test
python3 -O scripts/sexp.py --self-test
python3 scripts/probe_sexp_refusals.py
python3 -O scripts/probe_sexp_refusals.py
python3 - <<'PYREADER'
import sys
sys.path.insert(0, 'scripts')
import sexp as S
print(S.parse('(n +12 0x1f -0b10)'))
try:
    S.parse('(n\n 0x_)', 'example.sexp')
except S.SexpError as exc:
    print('REFUSED:', exc)
PYREADER
```

Expect18/0 from each legacy self-test,29/0/0 from each refusal probe, values
`12,31,-2` and a refusal naming `example.sexp:2`. Eight independent omitted guards
fail normally and optimized without test errors. Replacing `12` with `13` must
fail the legacy test in both modes; explicit checks prevent `-O` false credit.

## Qualification contract and structured syntax

The complete declaration below is included from its authoritative decision.
[Authenticated evaluation](evaluation.md) composes declared-file, comparison
and source/ELF checks. Full method/policy adequacy remains pending; qualification
stays closed and the current gate report is unchanged.

{{#include ../../../decisions/decision_qualified-matched-experiment-contract.md:contract}}

## First comparison method — contract and implementation boundary

The canonical contract below defines the typed witness and exact wrong-value
control. Its opening paragraph states the current implementation boundary;
[References](references.md#artifact-syntax-you-can-inspect) describes the artifact
formats. Production qualification stays closed; the declaration gives no new
requirement or CPU acceptance credit.

{{#include ../../../decisions/decision_sail-gpr-comparison-method.md:method}}

## Typed witness and control-baseline checks

A property may now carry one `gpr_witness` with integer `step_n` and a canonical
register `x1` through `x31`. Shape validation rejects missing/duplicated/unknown
witness fields, wrong types/arity and other register spellings. After raw shape
validation, the graph checker requires `0 <= step_n < instructions` in the parent
experiment and `gpr-change` among that property's observation kinds. A control's
optional `baseline_id` must resolve to an actual baseline run, rather than a repeat,
control or missing ID. The single mapper preserves both additions; it refuses
unknown witness fields and repeated whole witness children.

Legacy/generic graphs may omit these optional fields. A generic control may name
any declared baseline; the first-method bindings require their sole baseline
and witness, and byte comparison checks the exact intended value difference. A valid locator
does not prove the property, bind an obligation to an observation or qualify a run.
The a20 grammar step added no receipt/manifest mapping or canonical capture;
the artifact formats are described in [References](references.md#artifact-syntax-you-can-inspect).

Run the offline controls from the repository root:

```bash
python3 scripts/probe_experiment_verification.py --case locators
python3 scripts/probe_experiment_verification.py --case locator-shape
python3 scripts/probe_experiment_verification.py --case locator-mapper
python3 scripts/probe_experiment_graph.py
python3 -O scripts/probe_experiment_graph.py
```

The graph suite checks valid first/last boundaries, absent optional fields and
invalid budget/kind/baseline endpoints. Three in-memory guard omissions must each
fail on their named cases; production code has no bypass option. These synthetic
records exercise readers only and confer no execution or CPU acceptance credit.

## Checking identities and declared relationships

`PROFILE-CONSISTENCY` now passes each new verification experiment's raw form to
the schema checker **before mapping it**. A duplicated singular field is refused
before the dictionary could collapse its two values. Legacy records retain their
existing checks. There are no canonical v1 captures yet.

`scripts/experiment_verification.py` owns these relationship checks. The caller
supplies the parent profile's candidate inventory; requirements are filtered by
profile, and effective obligations reuse the existing contract measurement,
including inheritance and supersession. A superseded or foreign obligation cannot
be credited merely because its historical record is still in the catalogue.
This validates compatible identities, without assuming one requirement corresponds
to exactly one obligation or that naming them establishes coverage.

Every child family needs unique IDs. Producer inputs resolve; reference producers
name actual experiment candidates, one producer per candidate. Expected-result
producers keep their own identities. Shared inputs declared on a producer must be
its own inputs. Runs resolve their inputs, producers and observations, include
reference and expected producers, and include each producer's declared inputs.
Every observation belongs to exactly one run, and all observations are used.

Baseline, repeat and control kinds must all be present. A repeat names a baseline
and preserves its input and producer sets. Other run kinds cannot carry
`repeat_of`. Controls name actual control runs, mutated inputs used by that run
and existing properties. Their observed verdict must agree with the run record.
Every control run needs a control record. An honestly recorded control that
expected `DIVERGE` but observed `AGREE` remains consistent data; it earns no
adequacy credit from this checker.

Every producer pair used by a run needs an assessment. Endpoints resolve and
are distinct; a pair/subsystem cannot carry conflicting repeated assessments.
The recorded shared-input IDs must equal the intersection of the producers'
declared input IDs. This makes common inputs visible. It does not authenticate
implementation ancestry: an ancestry assessment and a common guest/source input
describe different facts, and no assessment string creates independence credit.

Paths must use canonical lexical repository-relative POSIX form. Absolute paths,
parent traversal, repeated separators, dot components, backslashes, drive syntax
and control characters are refused. Inputs and observations cannot alias one
declared path, and observation sizes cannot be negative. Filesystem resolution,
symlinks, volume identity, file existence, hashes and actual sizes belong to the
file-pin reader described below.

For an otherwise complete record, these changes have distinct diagnostics:

| Edit | Refusal |
| --- | --- |
| Repeat names a missing run or another repeat | `VERIFICATION REPEAT EDGE` |
| Repeat changes its input or producer set | `VERIFICATION REPEAT INPUTS` |
| Two runs claim the same observation ID | `VERIFICATION OBSERVATION OWNER` |
| Control's observed verdict differs from its run | `VERIFICATION CONTROL VERDICT` |
| Pair hides or invents a declared shared input | `VERIFICATION PAIR SHARING` |
| Property names an obsolete or foreign obligation | `VERIFICATION OBLIGATION SCOPE` |

Run the offline controls from the repository root:

```bash
python3 scripts/probe_experiment_graph.py
bash scripts/check_profile_consistency.sh --self-test
```

The graph suite exercises 63 positive/negative cases. It checks raw duplicated and
unknown fields, current effective scope, every child identity and the declared
edge classes above. Removing a predicate must expose its intended control even
when another rule also refuses the same record.

An empty issue list from `check_experiment` means these declared relationships
are consistent. The blanket `UNQUALIFIED EXPERIMENT VERIFICATION` refusal remains
in production pending complete method/policy adequacy. These relationship checks do not verify
executed mutations, successful processes, invocation equivalence, complete traces,
byte-identical repeats, correct results or sufficient coverage. No CPU requirement
status, gate axis, artifact budget or retention layout changes.

## Authenticating input and observation files

`scripts/experiment_artifacts.py` checks each declared input and observation pin
after raw shape and graph validation. It receives the trusted repository root at
runtime; persisted file paths stay relative. It reads existing files without Git,
extraction or a cache, and creates no artifact store. The pin checker does not run
the reference or execute any command stored in a record.

| Result | Meaning |
| --- | --- |
| `matched` | A stable regular file beneath the repository root matches its SHA256 and, for an observation, its declared byte size. |
| `mismatch` | The existing file's hash or observation size differs. It supplies no successful pin match. |
| `unavailable` | A required file/parent is absent or an I/O operation cannot complete, including a descriptor-close failure. No successful match is inferred. |
| `refused` | The path or file violates the safe-reader contract, or changes during the check. |

For example, replacing a declared observation with a different value of the same
length gives `mismatch: SHA256 differs`; a shorter observation gives
`mismatch: observation byte size differs`. A missing input gives `unavailable`.
These dispositions differ from a comparison's `DIVERGE` or a target trap. The
production diagnostic begins `VERIFICATION ARTIFACT` and names the profile,
experiment, record kind and record ID.

The reader anchors traversal with directory descriptors and refuses symlinks in
any component. Every opened directory/file must be on the repository root's
volume. Nested Git boundary markers are refused before their files are opened;
Git metadata paths, including case variants, are not capture artifacts. Only
regular files can be hashed. A FIFO is opened nonblocking and rejected by type,
so a missing writer cannot hang verification. Missing safe traversal support
refuses rather than falling back to an unsafe path walk.

Hashing uses at most a 1 MiB read chunk and stops at the file's initial size plus
one byte. The reader compares descriptor identity before/after reading, binds the
filename back to that descriptor, rechecks parent identity and Git boundaries,
and rejects concurrent rewrites, growth, shrinkage or replacement. Every acquired
descriptor receives a close callback; remaining callbacks run after an early
return or an I/O/close error, and a close failure yields no successful pin match.
These checks describe
the file during verification; they cannot prevent a later workspace change.

Run the on-volume controls from the repository root:

```bash
python3 scripts/probe_experiment_artifacts.py
python3 -O scripts/probe_experiment_artifacts.py
bash scripts/check_profile_consistency.sh --self-test
```

The pin suite exercises 39 cases with actual owned files, directories, symlinks,
FIFO and streamed reads. Foreign-device controls change only the observed device
metadata; they never write to another volume. Nested-Git cases use marker-only
fixtures, without initializing or amending another repository. Timed mutations
exercise file/parent replacement and a Git boundary appearing during reading.
A filename is also replaced after the final descriptor check, specifically to
test the separate pathname-binding predicate. Open/close tracking checks for
leaks on every branch; the close-error injection follows an actual successful close
and verifies the remaining callbacks and unavailable result. One temporary-directory
lifetime removes the owned fixture.
The suite also runs under Python optimization.

Matching pins do not authenticate successful processes, exact replay invocations,
complete traces, equivalent repeated runs, executed negative controls or correct
results. A genuinely empty file can match its empty-file pin; it still cannot
stand in for a required complete trace. Full dependency currentness, producer
adequacy and policy-derived coverage remain pending. Even when every declared
file matches, production still reports `UNQUALIFIED EXPERIMENT VERIFICATION`.
No fresh canonical capture or CPU acceptance credit is created by these checks.

## Sail comparison requires the complete declared budget

The public Sail adapter compares finite GPR changes and witnessed interrupt/fetch
deliveries. A one-step expectation permits only boundary0. Appending instruction
row1, even with no register change, or a delivery at boundary1 is refused as
`outside declared budget [0, 1)`. A distant row99 also refuses. All parsed rows and
witnessed deliveries are checked **before** value comparison; an earlier wrong
value cannot hide a surplus tail behind a `DIVERGE` result. Missing required rows
retain their existing refusal, and valid last-boundary rows/deliveries still agree.

P4.14 a16 reproduced three false agreements in the preceding adapter: it parsed
the surplus observations but iterated only the expected steps. The runtime's exact
instruction limit did not validate arbitrary retained traces. The repair applies
to both live runs and the cached `--check-trace` path.

```bash
python3 scripts/probe_gc_sail.py
bash scripts/check_guest_gen.sh --self-test
```

The budget controls exercise five tails and three genuine exact-boundary
agreements. Two separate mutations remove the row and delivery checks; each must
fail for its intended reason. These new checks and refusal-reason assertions
remain active under Python optimization; this makes no blanket optimization
claim for the older probe assertions. The existing live atomic-alignment and
timer diagnostics use the pinned public binary and retain their expected results.

The comparison vocabulary remains limited: PC/word, FP registers, direct CSR
state, memory and requests are uncredited except where read into the declared GPR
changes. Validating a trace budget does not authenticate execution or qualify a
structured experiment. No canonical capture or requirement status changes here.

## Structured differences and full-trace validation

`compare_observations(expected, text, returncode=0)` in
`scripts/run_rv64gc_sail.py` returns immutable `Comparison(verdict, detail,
gpr_difference)`. A GPR difference contains `step_n` and the **complete** observed
and expected change sets as sorted tuples of `(register, integer)` pairs. The
ordering is lexical (`x1`, `x10`, `x2`); values are RV64 integers. The first differing
boundary is retained. Agreement has no difference; a first delivery/wait mismatch
also has no GPR difference. Consumers must inspect these fields rather than parse
human-readable diagnostic text.

The historical `compare_trace` delegates to that same comparison owner and returns
its `(verdict, detail)` pair. Complete valid traces retain their previous outcomes
and diagnostic wording. Parsing, process failures and invalid evidence raise
`SailError`. The API accepts already mapped expectations and trace text; it does
not supply schema validation, byte limits, authentication or method qualification.

A28 fixes an older early-return defect: a wrong GPR value or delivery mismatch
could return `DIVERGE` before discovering a missing later row or nonzero `x0`.
The comparator now checks every declared boundary before returning its first
difference. Nonzero `x0` also refuses in the delivery-mismatch row itself. An
incomplete or invalid trace cannot become a successful negative control just
because an earlier observation differed. Surplus observations still refuse before
comparison. Raw trace completeness remains distinct from execution provenance.

This complete example uses **synthetic diagnostic fixtures**, not Sail execution:

```bash
PYTHONPATH=scripts python3 - <<'PY'
from probe_sail_comparison import expected, trace
from run_rv64gc_sail import compare_observations
result = compare_observations(expected([{'x1': '0x2'}]), trace([{'x1': 1}]))
print(result.verdict, result.gpr_difference)
PY
python3 scripts/probe_sail_comparison.py
python3 -O scripts/probe_sail_comparison.py
```

The example prints `DIVERGE GprDifference(step_n=0, observed=(('x1', 1),),
expected=(('x1', 2),))`. The 34-test suite covers exact first differences,
complete change sets, immutable data, mixed GPR/delivery ordering, complete trace
validation and legacy delegation. Ten independent omissions must fail in both
Python modes; GUEST-GEN runs all controls. These results confer no canonical
capture, execution or CPU acceptance credit. Bounded byte evaluation and
authenticated orchestration are partial; complete adequacy remains pending.

Pure [execution binding](retained-method.md#binding-the-declared-sail-invocations) now checks
principal inputs, the binary-pinned reference and exact three-run argv. It does
not authenticate those declarations or replace the complete method evaluator.
[Witness/control/derivation/pair bindings](retained-method.md#binding-witness-control-derivation-and-actual-pairs)
likewise preserve failed recorded outcomes as data, without method credit.

[Byte evaluation](evaluation.md) composes authentication and observed comparisons;
complete method/policy adequacy and qualification remain uncredited.

## Bounded three-run byte comparison

`compare_unit` in `scripts/matched_gpr_comparison.py` checks supplied immutable
bytes. It never opens an artifact or executes a producer. Its keyword arguments
are `instructions`, `witness`, `baseline_expectation`, `control_expectation`,
`baseline`, `repeat`, `control` and optional `program=None`:

| Value | Contract |
| --- | --- |
| `instructions` | Integer 1–4096, excluding booleans; the complete parent budget |
| `GprWitness(step_n, register)` | An in-budget boundary and canonical `x1`–`x31`; both expectations must declare that change |
| Two expectation payloads | Immutable bytes, 1–1048576 bytes each; UTF-8, exactly one raw-schema-valid document, then the single dossier mapping |
| `RunBytes(trace, process_exit)` for each run | Immutable trace bytes, 0–4194304 bytes each; an explicit integer exit with no default |

Optional `program=None` preserves legacy calls. A supplied plain string of
1–65536 characters binds both expectations; the evaluator always supplies it.
All five payload bounds are checked before any decoding/parsing. These are
payload limits, not exact process RAM ceilings. Complete ordered steps must match
the parent budget. Duplicate writes refuse before dictionary collapse. Change
registers must be canonical `x1`–`x31`; values are hexadecimal RV64 integers.
Upper/lowercase hex and redundant leading zeros are allowed within the payload
bound. A spelling change alone cannot satisfy the negative control.

Baseline and repeat must both agree, with byte-identical raw traces. The control
trace must also be byte-identical: it executes the same inputs, while only the
expected value changes. The control expectation must differ in precisely its
witnessed value; every other mapped field remains identical. Comments/formatting
do not change mapped data. The control must diverge at that boundary with exactly
the complete baseline/control change sets. A verdict or diagnostic substring
cannot stand in for these structured checks.

The immutable `ComparisonUnit` returns `disposition`, `reason` and a tuple of
`RunComparison(run_kind, comparison, refusal)` records:

- `satisfied` means this supplied-byte comparison passed. It grants no method
  qualification, authentication, execution provenance or CPU acceptance credit.
- `failed` retains all three computed comparisons/refusals. Nonzero exits,
  empty/truncated/malformed traces, wrong targets and changed raw bytes fail.
- `unsupported` has no run comparisons: `cross_model false`, declared profile
  differences and fault injection need another method.

`UnitError` refuses malformed method inputs, invalid values/budgets and exceeded
payload limits; it is not a canonical record-validity verdict. Other expectation
metadata remains part of the sole-change check. This GPR method gives no extra
credit for `fetches`, `never_written`, PC/word, memory or direct CSR/FP observations.
Recorded process exits alone do not establish that a process executed.
Decimal step/GPR indices that Python refuses to convert raise `SailError`,
which the byte unit retains as a comparison refusal. Production leaves the
interpreter's configured digit limit unchanged. Native-limit and isolated
conversion-injection controls cover both fields and the legacy tuple API.

Run this complete **synthetic** example from the repository root:

```bash
PYTHONPATH=scripts python3 - <<'PY'
from matched_gpr_comparison import GprWitness, RunBytes, compare_unit
base = b'''(expectations (program "fixture.s") (instructions 1)
  (step (n 0) (insn "addi x1,x0,1")
    (writes (write (reg "x1") (value "0x1")))
    (derivation "synthetic example, not execution evidence") (source "fixture")))'''
changed = base.replace(b'(value "0x1")', b'(value "0x2")')
raw = b'''[0] [M]: 0x0000000080000000 (0x00100093) addi x1,x0,1
x1 <- 0x0000000000000001
'''
run = RunBytes(raw, 0)
result = compare_unit(instructions=1, witness=GprWitness(0, "x1"),
                      baseline_expectation=base, control_expectation=changed,
                      baseline=run, repeat=run, control=run)
print(result.disposition, [run.comparison.verdict for run in result.runs])
PY
python3 scripts/probe_matched_gpr_comparison.py
python3 -O scripts/probe_matched_gpr_comparison.py
```

It prints `satisfied ['AGREE', 'AGREE', 'DIVERGE']`. All 52 tests and fourteen
independent omissions run under GUEST-GEN in normal/optimized Python, including
the inclusive payload and 4096-boundary limits. [Evaluation](evaluation.md) now
composes identity/receipt/comparison and source/ELF checks; the [shared reader](closure.md#authenticating-the-declared-file-set-within-shared-budgets) owns aggregate accounting.
Complete closure/impact/property/provenance, full policy, collection and canonical
captures remain pending. This byte unit grants no qualification.

## Authenticating a pin with a total read bound

`read_bounded_pin` returns the same immutable `PinResult` as `read_pinned`, while
requiring keyword `max_bytes`. The limit is a nonnegative integer, excluding
booleans; invalid limits refuse before opening a path. Oversized files refuse
before payload reading. It uses the same anchored traversal, SHA256, identity,
volume/Git-boundary and cleanup checks, without retaining snapshot payload.

```python
from pathlib import Path
from experiment_artifacts import read_bounded_pin

# record is an already schema/graph-validated project-file input.
pin = read_bounded_pin(Path.cwd(), "input", record, max_bytes=8 * 1024 * 1024)
if pin.disposition != "matched":
    raise ValueError(pin.disposition + ": " + pin.reason)
```

Both bounded APIs now keep every read within the call's budget. If the initial
file fills the limit, there is no room for the usual one-byte growth probe; final
descriptor/path metadata checks still refuse growth or replacement. With room
remaining, the growth probe stays within the limit. A zero-bound empty file needs
no read. Before this change, a snapshot at its payload cap could consume one extra
growth byte, then correctly refuse without returning data. That documented
sentinel did not produce agreement; the prospective method needs stricter bounds.

Legacy `read_pinned` retains its streaming/chunk limit and initial-size-plus-one
probe, with no total byte cap. The new per-call limit does not enforce aggregate
experiment budgets: the [shared reader](closure.md#authenticating-the-declared-file-set-within-shared-budgets) owns that accounting.
None of these APIs authenticates a process or qualifies a comparison.

```bash
python3 scripts/probe_experiment_read_limits.py
python3 -O scripts/probe_experiment_read_limits.py
```

The 53 controls measure actual reads, exact/zero limits, growth with/without room,
short reads, refusals and cleanup. Four separate mutations remove the pin bound,
invalid-limit check, sentinel budget or payload-retention separation; each must
fail on named cases, including under optimization. The prior pin/snapshot suites
and their independent guard-omission controls remain in force.

## Taking bounded snapshots for comparison

A pin-only result describes a file during its check. Reopening that filename later
can read different bytes. `read_snapshot` instead returns `Snapshot(pin, data)`
from the same descriptor-anchored, authenticated read. `pin` has the four
previously documented dispositions. `data` is immutable `bytes` only on success;
it is `None` on mismatch, refusal or unavailable I/O, including a close failure
after bytes have been collected. The result record itself is also immutable.

The caller must provide keyword `max_bytes`, a nonnegative integer; booleans,
negative values and other types refuse without opening a path. Omitting the
argument raises the ordinary Python `TypeError`. A file larger than that bound
refuses before payload reading. An empty file with a matching pin and zero bound
returns `b""`, which is distinct from failure's `None`. It remains inadequate as
a complete required trace.

For example, this helper accepts an already schema/graph-validated observation
record. Run with `scripts` on Python's module path, from the repository root:

```python
from pathlib import Path
from experiment_artifacts import read_snapshot


def bytes_for_comparison(record):
    snapshot = read_snapshot(Path.cwd(), "observation", record,
                             max_bytes=4 * 1024 * 1024)
    if snapshot.data is None:
        raise ValueError(snapshot.pin.disposition + ": " + snapshot.pin.reason)
    return snapshot.data
```

The example selects 4 MiB. The shared reader enforces the first method's
per-role and aggregate budgets; this snapshot API alone does not bound multiple
retained files. Snapshot assembly uses memory proportional to the bound: collected chunks
and their joined immutable bytes can coexist, so the bound is **not** a promise
of exactly that many bytes of process memory. The underlying read chunk remains
at most 1 MiB, and all existing stability, volume, Git-boundary and cleanup rules
apply. The pin-only API still streams without retaining payload bytes.

```bash
python3 scripts/probe_experiment_snapshots.py
python3 -O scripts/probe_experiment_snapshots.py
bash scripts/check_profile_consistency.sh --self-test
```

Twenty-four controls cover exact/zero/oversized/invalid bounds, digest and size
mismatch, missing/unsafe paths, symlinks, partial I/O, close failure, concurrent
rewrite, one traversal without reopening, immutable results and a real multi-chunk
snapshot. Open/close tracking observes descriptor cleanup; the owned on-volume
fixture is removed. Five deliberate mutations exercise the bound, required
argument, no-reopen rule, withheld failure data and immutable result. They also
fail under optimization. All 39 original pin controls remain applicable.

A later filename replacement leaves returned bytes intact; it can make the
workspace cease to match that capture. Snapshots provide check-time bytes, not
process authentication, currentness for an entire dependency graph, execution of
a control, evidence adequacy or retention. Production still refuses every v1
block pending complete method/policy adequacy; no canonical capture or CPU
acceptance credit follows from this API.

## Expectation write keys cannot collapse

Each step's `writes` collection maps register names to expected values. A key
must occur once within that step. This conflicting illustrative document has
valid repeated-form shape, but the mapper and dossier gate refuse it:

```lisp
(expectations (program "illustration.s") (instructions 1)
  (step (n 0) (insn "addi x1, x0, 1")
    (writes
      (write (reg "x1") (value "0x2"))
      (write (reg "x1") (value "0x1")))
    (derivation "illustrative conflicting input, not source-derived evidence")
    (source "fixture")))
```

The refusal names the program, step and key:
`expectations 'illustration.s' step 0: duplicate write register 'x1'`.
Repeating the same value also refuses; choosing either the first or last value
would conceal the repeated identity. The same register can appear in different
steps, and distinct keys can have equal values. Empty writes and device register
labels retain their existing meanings.

P4.14 a18 reproduced the preceding failure: dictionary construction silently
kept the last conflicting value, allowing a trace matching that value to report
`AGREE`. The repair lives in the single `expectations_to_doc` mapping owner, so
the public loader and cached Sail CLI refuse before comparison. DOSSIER-SCHEMA
also invokes that mapper after successful expectation shape validation. The
schema grammar is unchanged: shape checking alone cannot establish key identity.

```bash
python3 scripts/probe_expectation_mapping.py
python3 -O scripts/probe_expectation_mapping.py
bash scripts/check_dossier_schema.sh --self-test
python3 scripts/probe_expectation_mapping.py --emit conflicting
```

The last command prints an intentionally invalid mapping fixture; it executes no
reference and creates no capture. Twelve controls check positive mappings,
conflicting/identical/nonadjacent/late duplicates and actual loader paths. Removing
the duplicate guard must fail six duplicate cases, including under optimization.
The dossier gate separately exercises valid, conflicting and identical-key files
through its actual sweep. A raw census found no repeated keys in the 222 current
canonical expectation documents; all valid mapped dictionaries remain unchanged.

This identity check does not validate source derivations or make expected values
correct. It supplies no execution, producer-independence, policy-adequacy or CPU
acceptance credit. Full method/policy adequacy remains pending.
