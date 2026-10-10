# Qualified matched-experiment contract

- **Type:** `decision`
- **Date:** `2026-10-10`
- **Status:** `active` — prospective contract; implementation pending
- **Owner / source:** `P4-SYSTEM.14` a12, `SEMULITH-P4-0203`; existing GC verification policy and evidence-graph requirements
- answers: What must a new GC matched experiment carry before it can receive qualification credit?

## The fact / decision

<!-- ANCHOR: contract -->
Extend the existing `references.sexp` experiment with an optional, versioned
`verification` block for `matched-gpr-v1`. Keep legacy experiment fields and
records intact. The block will carry typed identities and relationships for
inputs, producers, observations, runs and controls; its presence will not mean
that its evidence is adequate or current.

**Current implementation:** the existing grammar and checker carry the legacy
flat metadata and enforce experiment/model/pair identities. The block specified
here, its mapping, artifact verifier and qualification evaluator are not yet
implemented. No GC record is qualified by this declaration. This contract applies
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

The future block has the following required information. These are contract
fields for the forthcoming schema, not currently accepted syntax or commands.

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

1. Extend `schema/references.sexp` and the single mapping owner
   `scripts/dossier_sexp.py`; prove all existing dossier dictionaries and generated
   consumers remain exact, and exercise the new nested fields with positive and
   malformed/lost-child controls.
2. Implement relationship, input-pin, artifact and comparison validation, with
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

Retention layout and schema implementation are the next owned slices. This decision
does not create an artifact store, change a cap, retire a source, run a reference,
change a requirement status or close a CPU-SYSTEM axis.
<!-- ANCHOR_END: contract -->
