# Qualified matched-experiment contract

- **Type:** `decision`
- **Date:** `2026-10-10`
- **Status:** `active` — grammar/mapping, declared edges and file pins implemented; comparison/qualification and retention pending
- **Owner / source:** `P4-SYSTEM.14` a12–a17, `SEMULITH-P4-0203`–`0208`; existing GC verification policy and evidence-graph requirements
answers: Which matched-GPR syntax, edge, pin, bounded snapshot and trace-budget checks exist, and why does qualification remain closed?

## The fact / decision

<!-- ANCHOR: contract -->
Extend the existing `references.sexp` experiment with an optional, versioned
`verification` block for `matched-gpr-v1`. Keep legacy experiment fields and
records intact. The block carries typed identities and relationships for
inputs, producers, observations, runs and controls; its presence will not mean
that its evidence is adequate or current.

**Current implementation:** a13 implements the optional block in the existing
reference schema and single dossier mapper. a14 adds raw-form schema validation,
scoped identities and declared-edge checks; a15 authenticates declared file pins
through anchored same-volume traversal. a16 repairs Sail comparison to refuse
rows/witnessed deliveries beyond the declared step budget, before value comparison.
a17 adds immutable snapshots from the same authenticated read, with an explicit
caller byte bound and no data on failure. DOSSIER-SCHEMA checks its shape;
PROFILE-CONSISTENCY refuses every block as `UNQUALIFIED EXPERIMENT VERIFICATION`
while comparison/qualification evaluation is pending. Legacy flat metadata and
experiment/model/pair checks remain intact. No GC record is qualified. This contract applies
prospectively, before the forthcoming fresh qualification runs, without backdating
the historical experiments or weakening `profiles/rv64gc-lab-v0/EVIDENCE_POLICY.md`.

## Why

The current metadata can name a program, verdict, reproduction and control in
strings. P4.14 additionally needs exact input and observation identities, executed
repeats, discriminating controls, property scope and producer relationships that
a checker can follow. EVD-01–09 and `docs/EVIDENCE_AND_GATES.md` require those facts;
the GC policy already requires fresh repeated runs and forbids independence credit
from unexamined ancestry. Use the existing canonical S-expression document and
single dossier mapping owner rather than introducing a second source format.

## How to apply

The first implementation is limited to the public adapter's declared GPR-change
and witnessed-delivery observations. Its method version is `matched-gpr-v1`.
It cannot establish unrecorded FP registers, memory, CSRs, request counts or full
architectural equivalence. Other observation methods need their own explicit
versioned contract before they receive credit.

The block has the following required information. Syntax is implemented; matching
relationships and authenticated execution evidence remain separate requirements.

| Information | Required content and relationship |
| --- | --- |
| Version and property scope | Exact method version; requirement and effective-obligation IDs; the particular observations supported for each property. Existence of an ID does not establish coverage. |
| Inputs | Unique input ID, role, canonical repository-relative path and SHA256 for each definition, source, policy, configuration, guest, expectation, adapter, runner and reference-build dependency used. Explicitly record shared inputs. |
| Producers | Unique producer ID and role, with input IDs identifying its implementation/configuration. Reference producers resolve to the existing candidate inventory; expected-result producers have their own declared identity rather than being invented external models. |
| Comparison rule | Exact rule/adapter identity, permitted differences and the complete observed vocabulary; normalization and masks are inputs, never unexplained exceptions. |
| Observations | Unique artifact ID, role, repository-relative path, byte size and SHA256. Bind raw observations and process stdout/stderr where relevant, with the successful process status captured separately. |
| Runs | Unique run ID, kind (`baseline`, `repeat`, `control`), exact invocation/configuration, process exit status, comparison verdict and the observation IDs it produced. |
| Controls | Unique control ID, the run and mutated-input IDs, the expected refusal/divergence and the actual observed reason. State which requirement/property the control can discriminate. |
| Producer assessments | The actual producer pair, subsystem, known shared input IDs, assessment, evidence and consequence. Unknown ancestry remains explicit and earns no independence credit. |
| Limits | Nonempty limitations, unavailable counterparts and observations outside scope. A named difference needs its source/profile justification and exact observations. |

The schema and mapping must reject unknown constructs/fields, wrong arity/types,
duplicate single fields and empty required collections. The evaluator must reject
conflicting IDs, unresolved or cross-profile references, missing required roles,
unsafe/noncanonical paths and mismatched pins. It must preserve repeated child
records through an exact mapping roundtrip. Identical common inputs do not become
multiple independent expected-result producers.

For successful comparison credit, a baseline and a fresh repeat must each have a
successful reference process, a complete valid trace and the required observations.
The repeat relation is declared before execution; this adapter currently requires
byte-identical raw repeat traces. At least one separate control run must discriminate
the claimed property. A comparison divergence produced by a successful reference
process is distinct from a process failure, missing/truncated trace or parser refusal.
Those failures cannot stand in for the intended wrong-value control.

For example, a future M capture may contain `m-baseline`, `m-repeat` and
`m-wrong-quotient`, with the last run using a separately pinned changed expectation.
The first two must agree over their complete declared observations; the control
must diverge at its intended quotient observation. Merely writing these three names
or the word `DIVERGE` into a record provides no execution evidence. This example
is a prospective protocol, not a recorded run.

Every required producer relationship must be assessed. A local source-derived
expectation and a reference binary remain distinct producer identities even when
they share instruction encoding or other inputs; shared inputs and unknown ancestry
must be visible. A `not-examined` assessment records uncertainty. Qualification
must not reinterpret it as independent implementation or independent numeric evidence.

A capture's statements and fingerprints are historical data. Currentness and
adequacy are computed results: relevant changed/deleted inputs invalidate affected
evidence through the old and new dependency edges. Missing artifacts yield an
explicit unavailable/unverified disposition, with no success credit. Requirement
status remains derived from the full policy and evidence graph, not from a record's
verdict string. Legacy records without this block remain historical/unqualified
under this method until explicitly requalified.

### Implementation and retention sequence

1. Implemented at a13: extend `schema/references.sexp` and the single mapping owner
   `scripts/dossier_sexp.py`; prove all existing dossier dictionaries and generated
   consumers remain exact, and exercise the new nested fields with positive and
   malformed/lost-child controls.
2. Declared identity/edge checks implemented at a14 and file pins at a15;
   comparison/qualification evaluation remains pending. Implement remaining checks with
   controls for wrong results, missing/extra observations, stale inputs, failed
   processes, truncated traces, duplicate/conflicting IDs and broken producer edges.
   Demonstrate each control's intended reason; deleting a predicate must expose it.
3. Before the first fresh canonical capture, declare its finite case set, inputs,
   expected producer, comparison rule, repeats, controls and limitations. Measure
   the destination family's file/byte budget and declare bounded artifact retention.
   Existing profile-family headroom is not a license to raise its ceiling or route
   raw logs into a different unbounded family. No old input is removed in this declaration.
4. Use only published reference interfaces, build instructions and artifacts.
   Keep project outputs and scratch on the repository volume. Validate retained
   observations without Git/extraction assumptions if a packed representation is chosen.
   An unavailable retained artifact stays uncredited; a fresh clone must not silently
   inherit successful qualification from an absent local cache.
5. Record and validate the first finite capture, then the remaining declared GC
   experiments. Advance traceability or requirement status only when their full
   gate/policy criteria are actually met. Preserve old records and explicit successor
   edges; do not rewrite a historical capture to appear freshly executed.

Comparison/qualification evaluation and retention layout are the next owned slices. This decision
does not create an artifact store, change a cap, retire a source, run a reference,
change a requirement status or close a CPU-SYSTEM axis.

### Implemented syntax and review commands

The optional block is a direct child of `experiment`. Its scalar fields are
`format_version`, `comparison_rule` and repeated nonempty `limitations`. Its
repeated children are `property`, `input`, `producer`, `observation`, `run`,
`control_run` and `producer_pair`. Each record has an `id`. At least two producers
and three observations/runs are required structurally; every other collection
must be nonempty. Those counts do not prove baseline/repeat/control coverage.

| Child | Other fields; brackets mean optional |
| --- | --- |
| `property` | `requirement_id`, repeated `obligation_ids`, repeated `observation_kinds` (`gpr-change`, `witnessed-delivery`), `statement` |
| `input` | `role`, `path`, `sha256` |
| `producer` | `role` (`reference`, `expected`), `version`, [`candidate_id`], repeated `input_ids`, [repeated `shared_input_ids`] |
| `observation` | `role`, `path`, integer `byte_size`, `sha256` |
| `run` | `kind`, repeated ordered `argv`, repeated `input_ids`, repeated `producer_ids`, [`repeat_of`], integer `process_exit`, `verdict`, repeated `observation_ids` |
| `control_run` | `run_id`, repeated `mutation_input_ids`, repeated `property_ids`, `expected_verdict`, `observed_verdict`, `reason` |
| `producer_pair` | `left`, `right`, `subsystem`, `assessment`, [repeated `shared_input_ids`], `evidence`, `consequence` |

Identity lists must be nonempty and unique when required. `argv` preserves order,
repeated arguments and empty arguments. An optional absent list stays absent in
the mapped dictionary. Digests are 64 lowercase hexadecimal characters. Verdicts
are `AGREE`, `DIVERGE`, `REFUSED`; an expected control verdict is `DIVERGE` or
`REFUSED`. Assessments use the existing four values: `shared`, `not-shared`,
`no-evidence-of-sharing`, `not-examined`. A failed control may honestly record
`observed_verdict "AGREE"`; syntax cannot turn that into adequate evidence.

This complete illustrative experiment passes the **shape** contract. Its dummy
pins and paths are not artifacts or a qualified capture. Adding it to an otherwise
consistent dossier causes the pending-evaluator refusal described above.

```lisp
(experiment (id "example-v1") (program "example.s") (instructions 1)
  (models "sail-riscv") (verdict "AGREE") (reproduced "illustration only")
  (control "illustration only")
  (verification (format_version "matched-gpr-v1")
    (comparison_rule "example-rule") (limitations "synthetic; no execution evidence")
    (property (id "quotient") (requirement_id "REQ-example")
      (obligation_ids "OBL-example") (observation_kinds "gpr-change")
      (statement "quotient at the declared boundary"))
    (input (id "guest") (role "guest") (path "target/example/guest.elf")
      (sha256 "0000000000000000000000000000000000000000000000000000000000000000"))
    (input (id "wrong") (role "mutated-expectation") (path "target/example/wrong.sexp")
      (sha256 "1111111111111111111111111111111111111111111111111111111111111111"))
    (producer (id "reference") (role "reference") (version "example")
      (candidate_id "sail-riscv") (input_ids "guest"))
    (producer (id "expected") (role "expected") (version "example") (input_ids "guest"))
    (observation (id "base-trace") (role "raw-gpr") (path "target/example/base.trace")
      (byte_size 1) (sha256 "2222222222222222222222222222222222222222222222222222222222222222"))
    (observation (id "repeat-trace") (role "raw-gpr") (path "target/example/repeat.trace")
      (byte_size 1) (sha256 "2222222222222222222222222222222222222222222222222222222222222222"))
    (observation (id "control-trace") (role "raw-gpr") (path "target/example/control.trace")
      (byte_size 1) (sha256 "2222222222222222222222222222222222222222222222222222222222222222"))
    (run (id "base") (kind "baseline") (argv "example-runner") (input_ids "guest")
      (producer_ids "reference") (producer_ids "expected")
      (process_exit 0) (verdict "AGREE") (observation_ids "base-trace"))
    (run (id "repeat") (kind "repeat") (repeat_of "base") (argv "example-runner")
      (input_ids "guest") (producer_ids "reference") (producer_ids "expected")
      (process_exit 0) (verdict "AGREE") (observation_ids "repeat-trace"))
    (run (id "control") (kind "control") (argv "example-runner")
      (input_ids "guest") (input_ids "wrong")
      (producer_ids "reference") (producer_ids "expected")
      (process_exit 0) (verdict "DIVERGE") (observation_ids "control-trace"))
    (control_run (id "wrong-quotient") (run_id "control")
      (mutation_input_ids "wrong") (property_ids "quotient")
      (expected_verdict "DIVERGE") (observed_verdict "DIVERGE")
      (reason "illustrative wrong quotient; no run executed"))
    (producer_pair (id "numeric-pair") (left "reference") (right "expected")
      (subsystem "quotient") (assessment "not-examined")
      (shared_input_ids "guest") (evidence "ancestry unknown")
      (consequence "no independence credit"))))
```

From the repository root, inspect a synthetic complete record and run the controls:

```bash
python3 scripts/probe_experiment_verification.py --emit-experiment
python3 scripts/probe_experiment_verification.py --case roundtrip
bash scripts/check_dossier_schema.sh --self-test
bash scripts/check_profile_consistency.sh --self-test
```

The first command prints to stdout and creates no capture. The controls exercise
unknown fields at every nested depth, wrong types/arity, duplicated singular
fields, missing fields/collections, malformed pins, unsupported versions/vocabularies
and repeated identity-list entries. The mapping proof retains multiple records
of every child family and ordered repeated/empty arguments. They establish shape
and losslessness. a14 additionally checks scoped identities, declared edges,
nonnegative observation sizes and lexical relative-path form, as documented in
the GC book. a15 checks physical paths, same-volume regular files, hashes and
observation sizes, with explicit matched/mismatch/unavailable/refused results.
Execution, comparison/invocation equivalence, full dependency currentness and
policy adequacy remain pending; matching pins establish only bytes at check time.
No stored flag can assert qualification on its own.
<!-- ANCHOR_END: contract -->
