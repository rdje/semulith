# Current processor gate

The complete generated report below is included from the canonical dossier.
G-CONTRACT measures effective version membership and realized bindings, rather
than the raw historical catalogue counts in the materials table. Registration
changes the review surface and collection census, without changing requirements,
frozen records or the acceptance decision.

{{#include ../../../../profiles/rv64gc-lab-v0/GS-REPORT.md}}

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

## Qualification contract and structured syntax

The complete declaration below is included from its authoritative decision.
Grammar/mapping, declared-edge checks and file-pin authentication exist;
qualification remains closed.
The current gate report is unchanged.

{{#include ../../../decisions/decision_qualified-matched-experiment-contract.md:contract}}

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
in production pending comparison/qualification evaluation. Relationship checks do not verify
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

The 4 MiB value is an illustrative caller bound, not an approved retention or
method budget. The future comparison method must declare both its per-file and
aggregate working-set bounds. Holding many snapshots can exceed a single file's
bound. Snapshot assembly uses memory proportional to the bound: collected chunks
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
block pending comparison/qualification evaluation; no canonical capture or CPU
acceptance credit follows from this API.
