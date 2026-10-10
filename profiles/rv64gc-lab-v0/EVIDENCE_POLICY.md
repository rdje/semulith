# Verification policy — `rv64gc-lab-v0`

<!-- ANCHOR: policy -->
## Declaration and scope

Declared by `P4-SYSTEM.14`, `SEMULITH-P4-0199`, on 2026-10-10, **after the existing
implementation and historical experiments**, and before the forthcoming evidence
requalification. This does not retroactively make those experiments predeclared.
It instantiates `RULES.md` EVD-01–09 and `docs/EVIDENCE_AND_GATES.md`; it does not
relax their processor-release gate. Future changes to these rules require a new
tracked declaration before the affected qualification runs.

Every included requirement and its effective obligations need a verification
disposition. The source-semantic category, risk and feature requirements below
are cumulative. A new category or unmapped obligation remains incomplete until
its disposition is declared. A policy document's presence is neither evidence
adequacy nor approval of a CPU release.

Existing reports are historical inputs to requalification, with their original
artifacts and limits. To credit them as current, first declare the obligation,
producer, exact observations, expected results, permitted comparison rules and
controls; then execute and record the required fresh, repeated checks under this
policy. Do not choose a weaker disposition because a convenient run already passes.

## Source-semantic dispositions

| Category | Required evidence | Insufficient by itself |
| --- | --- | --- |
| `defined` | Source-located expected observations; directed boundary fixtures; a matched public-reference comparison on the applicable observations. | Model output used as its own expectation; mere reference availability. |
| `implementation-defined` | Source latitude and the selected profile choice; fixtures for that choice; pinned matching reference configuration with a behavior-changing control, or an explicitly observed and justified profile difference. | A configuration file without an observed effect; calling a permitted difference a defect. |
| `unspecified` | Source locator, explicit classification/reportability and tests of the selected laboratory outcome and its limits. | Agreement on one permitted outcome as a universal architectural rule. |
| `reserved` | Revision-specific classification, selected laboratory behavior and separately recorded behavior or explicit unavailable disposition for each proposed reference. | One comparator silently becoming the authority. |
| `undefined` / `unpredictable` | Source-defined limits and reportability; tests of every constraint the source still imposes and of the selected laboratory policy. | Assuming every bit is unconstrained or suppressing the complete observation. |
| `source-specific` | A disposition declared for that precise source category and constraints before its qualification run. | Treating an unfamiliar category as `defined` or as an exclusion. |
| `not-applicable` | A checked source/scope or supersession argument, with the affected requirement and successor identified. | Missing fixtures or a passing subset used to remove an obligation. |

A genuine reference limitation leaves the affected comparison uncredited. Any
alternative disposition needs an explicit source-grounded argument and its own
controls before execution; it cannot be manufactured by relabeling an unrelated
passing result. Finite equality supports only the named inputs and observations.

## Risk and feature obligations

Low- and medium-risk requirements need the category evidence, boundary cases,
repeated execution and at least one discriminating negative control of their
checker or comparison rule. A control may cover multiple requirements only when
the graph states why its failure would be detected for each one.

High- and critical-risk requirements additionally need a second method addressing
the same property, with the producers and common inputs recorded, plus an
adversarial case for the feature's failure mode. Methods can include an independently
derived exact arithmetic expectation, a bounded exhaustive check with stated
bounds, a source-grounded invariant check or qualified hardware observations.
Two wrappers around one producer do not satisfy this requirement. Unexamined
comparator ancestry earns no independence credit; the disposition must identify
what is independently derived, rather than claim independent implementations.

The following feature rules apply regardless of the risk field:

- Privilege, CSR, trap and return checks cover legal/refused modes, aliases and
  preserved state. A forbidden write must not commit its destination or another
  architectural side effect.
- Translation and protection checks observe the relevant walk/request sequence,
  permission and fault priority, fault address and permitted side effects. A
  successful final load alone cannot establish the absence of an extra access.
- Atomics check width, address/physical aliases, destination/source aliases,
  reservation history, completion versus faults and refused stores. Single-hart
  tests earn no multicore or weak-memory-exploration claim.
- Floating-point checks need pinned numeric expected-result producers distinct
  from the backend under test, with bits, rounding, flags, boxing and exceptional
  cases in scope. Public reference agreement adds only its declared observations;
  it does not authenticate SoftFloat or other implementation ancestry.
- Counters, interrupts, wait and progress checks record scheduled time/events,
  delivery boundaries and suppression cases. Host timing is not guest time.
- Fetch, compressed instructions and instruction visibility check parcel/width
  boundaries, original instruction diagnostics, old-source aliases and the
  applicable no-effect/refusal cases.
- CPU/environment assumptions and guarantees need positive and negative checks
  at the typed boundary, independently of the instruction handler where required
  by `docs/CPU_ENVIRONMENT.md`. Distinguish a contract violation from a target trap.

## Records, controls and currentness

Each credited disposition links the requirement, effective obligation,
implementation/configuration owner, tracked runner and structured evidence record.
Record exact definition/source/build/configuration/input identities, command,
expected-result producer, observed artifacts, verdict, repeat result, controls,
comparison rules and limitations. Unknown ancestry remains explicit by subsystem;
shared expected-result producers are counted once. This project's ACT pipeline
uses Sail-produced signatures, so it adds external inputs rather than a second
expected-result derivation against Sail.

Controls must fail for the stated reason: wrong defined bit/result, missing or
extra state/request, shifted boundary, wrong trap or stale configuration as
applicable. Process failure, missing/truncated trace or a refusal is not equality.
A narrower observation vocabulary must be named; GPR-change agreement does not
observe unrecorded FP registers, memory, CSRs or environment requests.

Relevant source, definition, primitive, adapter, expectation, mask, configuration
or build changes invalidate dependent evidence. Check both old and new graph
edges; uncertain influence broadens to the affected profile. Regenerate derived
artifacts through their documented producers and repeat the required runs.

## Status and supersession

Requirement status must be derived and drift-checked from the graph and this
policy. No status is advanced by adding this document. Until that checker and its
records exist, the present catalogue retains its recorded statuses; the generated
GS report's policy-document measurement checks presence only.

The subsequent derivation must distinguish no credited implementation/evidence
(`planned`), incomplete implementation or verification (`partial`), complete
current required evidence (`implemented`), and a validated explicit inapplicability
argument (`not-applicable`). Unresolved source questions cannot close an included
requirement. No typed success word substitutes for executed evidence.

Historical mirrored decisions remain historical. Validate declared replacement
authority and effective contract scope before crediting a successor; preserve the
old record and graph edge. Superseding an obligation does not silently discharge
all requirements that named it, and no untested included requirement disappears.
The scalar profile's evidence cannot automatically credit this profile.

For example, a matching Sail GPR trace can support the declared register changes
of an atomic guest. It cannot by itself close the no-store-on-failed-SC obligation:
that disposition also needs request/reservation observations and a wrong-store
control. Likewise a numeric fixture needs the expected bits and flags from its
named numeric producer, not a copy of the backend's answer.

## Release boundary

CPU-SYSTEM stays incomplete while any required axis is open. This policy grants
no board, Linux, portability, universal-refinement or release acceptance. The
remaining regression, replay, portability and release leaves retain their full
requirements. Full CI is required before a push and at significant milestones;
focused ordinary checks do not replace profile qualification.
<!-- ANCHOR_END: policy -->
