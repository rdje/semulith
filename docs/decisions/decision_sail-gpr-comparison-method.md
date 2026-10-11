# First Sail GPR comparison method

- **Type:** `decision`
- **Date:** `2026-10-11`
- **Status:** `active` — bounded comparison/identity exist; complete authentication/collector/captures pending
- **Owner / source:** `P4-SYSTEM.14` a19–a30, `SEMULITH-P4-0210`–`0221`; GC policy/public Sail adapter
answers: Which Sail GPR checks exist, what remains for authentication/evaluation, and which claims remain unqualified?

## The fact / decision

<!-- ANCHOR: method -->
Declare comparison rule `sail-gpr-change-v1` within the existing
`matched-gpr-v1` verification envelope. Its first supported unit is one property,
one explicit GPR witness, one baseline, one repeat and one wrong-expectation
control. Implement this contract before recording a canonical capture. The
optional witness/baseline grammar and generic witness-kind/budget/baseline-edge
checks exist; they do not execute the method. A26 adds bounded receipt/manifest
syntax. A28 exposes immutable first differences after full-budget validation;
a29 adds bounded byte comparison/decimal-index refusals; a30 authenticates retained
reference identity. Complete authentication/orchestration and collection remain
pending. Production qualification stays closed.

The rule establishes a finite comparison and its declared capture protocol. It
cannot, alone, satisfy the GC policy for every source category, risk or feature.
No current requirement status, processor axis or reference ancestry changes here.

## Scope and trust boundary

Use only candidate `sail-riscv` and the tracked public adapter's GPR-change rule.
The baseline and repeat must agree; the control must diverge at its declared
GPR witness. Witnessed interrupt/fetch gaps may establish trace completeness, but
this first rule credits **GPR-change properties only**. PC/word, direct FP/CSR
state, memory, requests, timing, reservations and delivery properties remain
uncredited except where observed through the declared GPR change. No masks or
source-permitted differences are introduced. A known profile difference needs
another declared disposition; it is not converted into this rule's agreement.

Pin authentication establishes bytes during the check. A retained process receipt
records execution provenance; matching its digest is not execution attestation.
Offline evaluation trusts the reviewed tracked collector and the committed capture
procedure that produced it. A fully forged, self-consistent receipt cannot be
detected from hashes alone. Do not label the result independently authenticated
execution, independent implementations or universal proof. Source grounding and
full verification-policy adequacy remain separately reviewed/checked obligations.

## Typed witness and run relationships

The optional singular `gpr_witness` child on a generic property is required by
this rule. It has exactly `step_n` (integer) and `register` (string). The step is
in the complete declared budget; the register is canonical `x1` through `x31`.
The baseline expectation must declare a change for that register at that step.
An x0 invariant or an unchanged register needs another observation method.
Exactly one property with observation kind `gpr-change` is supported per unit.
Multiple obligation IDs may still express a many-to-many claim, but the witness
cannot discharge an unrelated obligation merely because its ID was named.

The optional `baseline_id` on a generic control record is required by this rule.
It names this unit's sole baseline. `repeat_of` already names that baseline for
the sole repeat. The control's `property_ids` contains exactly the sole property;
its `mutation_input_ids` contains exactly its changed expectation input. This
rule requires expected and observed control verdict `DIVERGE`, never `REFUSED`.
Other honestly recorded outcomes remain valid historical data without this
method's success credit.

The schema and single mapper accept the following typed syntax. These placeholder
IDs are illustrative; no capture has been executed or qualified. Generic validation
does not yet enforce this method's mandatory fields or exact value discrimination:

```lisp
(property (id "quotient") (requirement_id "REQ-example")
  (obligation_ids "OBL-example") (observation_kinds "gpr-change")
  (statement "the quotient change at the named boundary")
  (gpr_witness (step_n 8) (register "x11")))
(control_run (id "wrong-quotient") (run_id "control") (baseline_id "base")
  (mutation_input_ids "wrong-expected") (property_ids "quotient")
  (expected_verdict "DIVERGE") (observed_verdict "DIVERGE")
  (reason "deliberately changed expected quotient; illustrative, not executed"))
```

Runs use one reference producer, with candidate `sail-riscv`, and one expected
producer each. Baseline/repeat use the same expected producer and inputs. The
control uses a distinct expected-producer record for the changed expectation,
with its relationship to the baseline explicit. It is a mutant of the same
expected-result derivation, **not** a second independent method. Assess the actual
producer pairs and retain common inputs/unknown ancestry; producer counts confer
no independence credit.

## Inputs, roles and dependency closure

All recheckable project files use the existing canonical relative paths and
SHA256 pins. Principal roles are `guest-source`, `guest-image`, `reference-config`,
`reference-identity`, `expectation`, `collector`, `adapter` and
`dependency-manifest`. Require one of each principal per run; the
baseline and repeat select the same expectation, and only the control selects
the separately pinned mutant expectation. No input can silently stand for two
principal roles. Validate the complete existing identity/edge graph first.

A finite dependency manifest is a pinned S-expression input with version
`matched-gpr-dependencies-v1` and nonempty `input` children carrying `id`, `role`,
`path`, `sha256`. It contains at most 64 distinct project-file records; paths and
IDs are unique, and nested/self-referencing manifests are forbidden. Reuse the anchored pin reader
for every child. Include relevant definitions, encodings, implementation/expected
producer, assembler, source ledgers, policy, collector/comparison/reader/mapping
helpers and schema dependencies. A manifest is indirection for a finite closure,
not an exception to checking its leaves. Missing, changed or unsafe children earn
no current credit. Conservative impact analysis must traverse old and new closure
edges; uncertainty broadens to the affected profile.

External reference execution identity is distinct from a retained project file.
Retain a candidate-identity document using the existing `references` shape, with
exactly one candidate and no experiments. Match its immutable execution identity
against the current parent candidate: ID, origin, kind, binary path and SHA256,
and release, version, source_commit, asset and asset_sha256 when present. The reference producer's version is
`sha256:<binary_sha256>`. The collector checks the actual executable against that
pin before and after execution. The receipt records that executable identity.
This does not inspect submodule implementation or authenticate unknown ancestry.

The identity document avoids hashing the complete parent `references.sexp` into
its own future experiment, which would create a fingerprint cycle. Historical
`matched_scope` prose is not executable identity. Relevant changes to public
configuration, producer assessments or source/policy dependencies still require
impact/adequacy review; selecting immutable identity fields cannot suppress those
edges.

An offline comparison does not require a reference executable cache: it checks
retained observations, input files, the captured executable identity and current
candidate pins. It does **not** re-execute the reference. Fresh collection/replay
requires the published acquisition/build route and the actual pinned executable;
its availability is reported separately. A descriptor never excuses a missing
file that was declared as a project-file input. Missing retained trace, expectation,
receipt, manifest or required project dependency remains unavailable/uncredited.
Declare this distinction in the first capture's retention record; do not ship an
unbounded binary/cache store or imply replay succeeded in a fresh checkout.

## Invocation and process receipt

Execute from the repository root with persisted relative argv, without a shell.
The reference invocation is the public adapter's finite command: the pinned binary,
`--config-override`, the selected JSON configuration, `--inst-limit`, the declared
instruction count, `--trace-instr`, `--trace-gpr`, `--trace-exception`,
`--trace-output`, that run's trace path, and the pinned guest ELF. Their order is
fixed. Baseline/repeat/control argv may differ **only** in the trace-output value;
all other arguments and reference input identities remain equal. The expectation
mutation changes comparison input, not the executed guest/configuration.

Each run owns exactly one `raw-gpr`, `process-stdout`, `process-stderr` and
`process-receipt` observation. Keep empty stdout/stderr as real separately named
files. Before execution remove only that run's owned output paths, so old output
cannot stand in for a new run. Use a fresh child process for each run. Every process
must exit zero; missing output, signal/nonzero exit or parse refusal cannot satisfy
the wrong-value control. Keep project temporary work on the repository volume.

The receipt is a versioned S-expression observation (`sail-gpr-capture-v1`), not a
second editable source of experiment truth. Its schema and single dossier mapping
are implemented at a26; the collector remains pending. Required content: run ID/kind, ordered
exact argv, process exit, reference candidate/binary SHA256, collector input ID,
input-ID/digest inventory, trace/stdout/stderr identity/size/digests and observed
host/tool versions. Cross-check all of it against the canonical run and its pins.
Do not put the receipt's own hash inside itself. Timestamps or run ordinals can aid
provenance, but do not prove freshness; fresh process/output handling does.

## Bounded evaluation and exact control

Use the authenticated snapshot API, never a pin check followed by reopening.
Limits are for this rule, not a retention-family ceiling: exactly three runs,
1–4,096 declared boundaries, one property/witness, nine principal inputs (eight
plus the mutant expectation), three producers, twelve observations and one control
record. Keep exactly the two producer-pair assessments used by these runs; at most
64 manifest children. Bound raw traces to 4 MiB each, expectations to 1 MiB each,
and receipts, manifests, candidate identities and stdout/stderr to 64 KiB each.
Bound aggregate retained snapshot payload to 16 MiB per experiment. Other principal
files need pin-only authentication; do not load them without an explicit bound.
Project dependency pins may stream without retaining payload; bound one dependency
read to 8 MiB and the aggregate authenticated project-file reads to 128 MiB.
`read_bounded_pin` now enforces an explicit total read cap without retaining payload;
`read_snapshot` shares the bound, including growth probes. Legacy `read_pinned` has
no total byte cap. The future evaluator still owns the aggregate method budgets.
Counts/bytes are checked before allocating/reading beyond a bound. Parsed objects,
chunks and immutable copies add memory: these payload bounds are not exact process
RAM ceilings. Overflow refuses, never truncates to fit.

Parse exactly one expectation document after schema validation, using the single
mapper and its duplicate-write refusal. Require a positive complete instruction
budget equal to the parent experiment; honor `cross_model false` as unsupported.
This rule does not accept `expect_divergence` or fault-injection expectations.
GPR names/values must be valid for RV64 change observations, without widening masks.
Require complete strict trace parsing and the public adapter's successful-process
comparison on all declared boundaries, including the surplus-tail refusal.

Baseline/repeat compare `AGREE`; their complete raw trace bytes are identical.
The changed control expectation differs semantically from the baseline **only**
in the value at its named step/register; all other mapped expectation data is
identical. The two expected values differ as RV64 integers, not just spellings.
The control's successful fresh reference trace is byte-identical to the baseline
trace because its executed inputs are unchanged. Its comparison must `DIVERGE`
at that witness, with precisely the intended value difference and no changed
non-target observation. Check structured rows/changes and the expectation diff;
a verdict/reason substring is not a substitute. A wrong earlier value, changed
program, extra write, missing row or failed process does not satisfy this control.

answers: Why does a Sail difference still require validating every later boundary?
answers: Why can decimal trace indices refuse conversion despite valid syntax?

## Results, gates and implementation order

Compute separate record validity, observed-comparison and method dispositions.
Never store an authoritative `qualified` Boolean. Invalid shape/edges/unsafe paths
are refusals; coherent failed controls remain recorded failures. Missing required
artifacts are unavailable; changed dependency pins are stale. Neither yields
current success. A satisfied method remains only finite evidence for its witness;
full source/risk/feature policy and requirement status derivation follow separately.

The present blanket PROFILE-CONSISTENCY refusal remains until the evaluator and
its controls exist. Then integrate valid failed/stale/unavailable captures without
misreporting them as successful or making honest historical records syntactically
invalid. G-TRACE/G-OBLIGATIONS must consume computed dispositions rather than just
an experiment ID/verdict. Keep tracked review reports reproducible from retained
tracked inputs; transient reference-cache availability must not silently alter a
committed success report. Report replay availability explicitly.

Implement in finite committed slices: typed witness/baseline grammar and artifact
mappings; bounded read-only evaluator with genuine positive and wrong-target/
process/truncation/staleness/producer/limit controls; reviewed collector with fresh
output/process controls; measured bounded retention and predeclared finite case
set; first canonical capture; then full policy/status/mirror derivation. Preserve
all legacy records. Before any canonical capture, resolve the actual retained
file set and registered family budget; this declaration creates no store or cap.
<!-- ANCHOR_END: method -->

## Implemented artifact boundary (a26)

answers: Which artifact-byte checks exist and why do they confer no Sail execution or method credit?

`schema/matched-gpr-dependencies.sexp` and `schema/sail-gpr-capture.sexp` declare
roots `dependencies` and `capture`. Pure mappings live only in dossier_sexp;
`scripts/matched_gpr_artifacts.py` validates supplied immutable bytes (1–65536)
before mapping, with exactly one document, closed fields/types/version/digest
facets and identity checks. Canonical relative location is required: manifests
refuse duplicate IDs/paths, self references, declared nested manifests and >64
leaves; receipts require unique input/output/tool IDs, unique output paths,
collector inventory membership, the exact three output roles and nonnegative
sizes. Hidden nested content still requires authenticated closure evaluation.
Receipt host fields are os/kernel/arch, tools are repeated id/version children;
input inventory is id/sha256, outputs use the existing observation field names.
Unknown writer keys and lossy mappings refuse. Failed exits/empty files remain
representable, with no success credit. The parser performs no artifact I/O or
execution; evaluation must supply authenticated snapshots. No legacy loader
dispatch is added. DOSSIER-SCHEMA controls these APIs, without
claiming a future capture-store sweep. The GC book's References chapter gives
examples/fields. No canonical v1, store, cap or qualification changes.

## Related records

- `docs/decisions/decision_qualified-matched-experiment-contract.md`
- `profiles/rv64gc-lab-v0/EVIDENCE_POLICY.md`
- `docs/EVIDENCE_AND_GATES.md`
