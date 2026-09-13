# Semulith engineering rules — v0.2

Date: 2026-09-13. Normative project rules for the proposed implementation; no claim that the tools enforcing them already exist.

## Scope and authority

- **SCP-01:** Every support claim identifies a versioned processor/device profile, environment contract, observation contract, and applicable specification revisions.
- **SCP-02:** Resolve the transitive dependencies of every included feature before accepting its profile; unrelated excluded features do not block a smaller profile.
- **SCP-03:** Begin with CPU/DSP implementation and its testing environment; board implementation follows the processor gate for the profile it uses.
- **SCP-04:** A semantic correction invalidates affected evidence and requires a newly evaluated profile version.
- **SCP-05:** Report instruction, system, platform, concurrency, timing, compatibility, and evidence scope separately.

## Canonical definitions and generation

- **OWN-01:** Each semantic rule has one owned executable implementation in the versioned canonical processor or device definition.
- **OWN-02:** External specifications govern intended behavior; the canonical executable definition is a source-linked interpretation subject to validation.
- **OWN-03:** Generated artifacts identify their canonical inputs, generator, configuration, and fingerprints, and are changed by regeneration rather than direct editing.
- **OWN-04:** Independent references and expected-result evidence retain their separate provenance and are not replaced by self-generated agreement.
- **OWN-05:** Board definitions compose exact processor/device versions and generate consistent maps and wiring without duplicating their semantics.
- **OWN-06:** eADL describes HW/OS functionality and constraints without implementation; archogen's engine selects realizations; Semulith owns executable hardware models. Shared facts have one owner and versioned exports, and resolved compositions are checked against their contracts.

## Target semantics

- **SEM-01:** Model limitation, internal implementation error, malformed input, target exception, undefined-case diagnostic, wait, and control stop remain distinct typed outcomes.
- **SEM-02:** A target exception is emitted only under a source-linked target rule, never as a substitute for missing supported behavior.
- **SEM-03:** Every numeric operation defines relevant widths, signedness, intermediate precision, truncation, rounding, saturation, flags, and exceptional behavior independently of host defaults.
- **SEM-04:** Exposed sequencing, operand visibility, partial progress, and restart state follow the target definition rather than universal instruction atomicity.
- **SEM-05:** Addresses identify target spaces, units, widths, packing, and access context; host pointers do not supply guest semantics.
- **SEM-06:** Side-effecting accesses occur only at their prescribed semantic point and are not rolled back by assumption.
- **SEM-07:** Architecturally unspecified, undefined, reserved, implementation-defined, and research-unresolved cases preserve their distinct source meanings and choice constraints.
- **SEM-08:** Required state includes hidden or pending information that can influence future supported observations.

## Environment and execution

- **ENV-01:** Environment assumptions and CPU guarantees are enumerable, versioned, source-linked obligations with conformance tests.
- **ENV-02:** A board integration establishes that its environment satisfies the accepted CPU contract instead of silently changing its assumptions.
- **ENV-03:** Guest time, input events, interrupt delivery, and progress are explicitly scheduled and replayable independently of accidental host timing.
- **ENV-04:** Multicore execution enforces the selected target's memory and progress rules; host concurrency is only an implementation mechanism.

## Evidence and claims

- **EVD-01:** Finite testing, including deterministic differential testing, establishes tested evidence and is never labeled universal proof.
- **EVD-02:** A formal claim identifies its checked property, trusted assumptions, exact artifacts, versions, and bounds.
- **EVD-03:** Each included requirement has an approved verification disposition supported by actual evidence, with risk obligations and independence recorded.
- **EVD-04:** Reference configuration and semantic ancestry are recorded per subsystem so shared dependencies are not counted as independent oracles.
- **EVD-05:** Expected values, exclusions, normalization masks, and comparator changes have source-grounded justifications and explicit coverage effects.
- **EVD-06:** Requirement, code, dependency, test, and evidence links are machine-checked many-to-many relationships, not proof of semantics by annotation alone.
- **EVD-07:** Uncertain change impact triggers broader regression selection; profile releases require the full applicable gate, not only the diff-selected tests.
- **EVD-08:** Reports identify input fingerprints, coverage denominators, commands, actual results, evidence freshness, and known limitations and are reproducible from recorded inputs.
- **EVD-09:** Keep a validator mutation suite that verifies detection of known-wrong behaviors and unjustified comparison suppression.
- **EVD-10:** A hardware observation applies to its measured implementation/configuration and does not silently redefine all architectural implementations.

## Rust implementation and performance

- **RUST-01:** Host production modeling is Rust by default; production foreign-language dependencies require an explicit recorded architecture decision.
- **RUST-02:** Diagnostic tracing can be removed or disabled without removing semantic effects or changing guest observations.
- **RUST-03:** Common scalar execution uses efficient fixed-width storage and avoids mandatory per-instruction allocation; departures require measured justification.
- **RUST-04:** Measure performance on specified workloads and hosts and characterize measurement noise before enforcing regression thresholds.
- **RUST-05:** Accepted release portability obligations identify mandatory hosts and selected endian/undefined-behavior checks; missing required checks leave the gate incomplete.

## AI-assisted workflow

- **AI-01:** All Rust coding is AI-assisted through bounded tasks with source requirements, acceptance checks, and durable completion records.
- **AI-02:** Project context resides in versioned repository documents, with one canonical instruction file and thin assistant-specific pointers where needed.
- **AI-03:** AI review and agreement are criticism and workflow aids, not independent conformance evidence by themselves.
- **AI-04:** Routine resolved implementation work proceeds autonomously; material changes to user goals or unresolved architectural commitments are made explicit.
- **AI-05:** Do not hide a discrepancy by deleting a test, weakening a comparator, changing expected values, or shrinking scope without recording its semantic justification and impact.
- **AI-06:** Assign release evaluation to a defined reproducible procedure and record who or what made the acceptance decision without assuming human approval proves correctness.

## Source and release handling

- **SRC-01:** Record actual source/tool availability, applicable terms, redistribution decisions, and fingerprints before relying on or shipping those artifacts.
- **SRC-02:** A missing reference route prevents its associated evidence claim, not honest experimental work with a clearly limited claim.
- **SRC-03:** Never fabricate source hashes, test results, tool availability, namespace availability, or accepted gate status.
