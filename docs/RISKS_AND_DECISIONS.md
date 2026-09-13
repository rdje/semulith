# Risks and decision deadlines — v0.2

## 1. Risk register

| ID / priority | Failure mode | Detection signal | Required response |
|---|---|---|---|
| RK01 / high | No usable reference for selected target | P0 cannot reproduce matched arithmetic plus event/fault experiment | Change evidence path or keep target explicitly experimental; do not promise differential validation |
| RK02 / high | References share the same mistake source | Shared numeric library, generator, or expected-result engine found | Record correlation and obtain independent evidence for affected obligations |
| RK03 / high | CPU harness assumptions disagree with target/board | Unmapped config field, inconsistent units or event rule, integration-only failure | Correct contract ownership, reduce case, invalidate affected evidence, rerun CPU/composition gates |
| RK04 / high | Graph misses impact of a shared change | Unmapped modified code/configuration or escaped regression | Broaden selection, repair dependencies, retain escaped case and checker regression |
| RK05 / high | Canonical definition drifts from generated code | Regeneration changes tracked outputs or owner map has duplicates | Reject acceptance until one owner and reproducible generation are restored |
| RK06 / high | Comparator hides semantic error | Known mutation passes, new broad mask, expected values change without source reason | Fail validator gate and review affected past evidence |
| RK07 / high | FP backend implements wrong target policy | NaN/boxing/rounding/flag mismatch or ambiguous specialization | Reject that capability until backend/configuration is qualified |
| RK08 / medium | Scalar abstractions cannot express DSP behavior | Real-spec cases require hidden shared assumptions or unrepresentable progress | Revise internal boundary before stable general API; keep real DSP claims bounded |
| RK09 / medium | Per-instruction overhead blocks useful debug loop | Allocation-heavy common path or repeated benchmark regression | Measure cause; specialize representations/observers; preserve semantic evidence |
| RK10 / medium | Evidence bureaucracy outgrows implementation | Repeated manual status edits and inconsistent reports | Automate derivation/checks; simplify records without dropping obligations |
| RK11 / medium | Delayed effects or waits disappear with tracing off | Observations differ across observer modes or idle cannot wake | Separate semantic state from diagnostics; add equivalence/wake fixtures |
| RK12 / medium | User goal expands through incidental features | Board/desktop work begins before CPU gate or capability list grows without tasks | Restore staged priorities; define the new increment explicitly |
| RK13 / medium | Artifact use/redistribution assumptions are wrong | Selected source/tool terms or redistribution status unresolved | Resolve actual artifact terms; keep restricted material out of distributable package; select another path if needed |
| RK14 / medium | Host checks remain unavailable | Mandatory release job cannot run | Report incomplete gate or explicitly adopt a narrower stated host policy; never silently pass |

These are engineering risks, not a claim that every listed failure has occurred. Review risks at milestone boundaries and after escaped failures.

## 2. Decisions due before work depends on them

| Decision | Owner/procedure | Due | Current state |
|---|---|---|---|
| Exact RV64I profile and laboratory policies | Source-grounded profile task | G0 | Selected family, parameters to resolve |
| Actual oracle and effective configurations | Reference smoke-test task | G0 | Candidates identified; not yet acquired/tested for this project |
| Requirement/contract schema and symbol extraction convention | Core/verification design task | G1 | Starter schemas supplied; executable extractor/checker pending |
| Semantics source ownership and generation manifests | Canonical-definition task | G1 | Rust handlers plus structured metadata chosen |
| Trace observer/typed effect boundary | Execution slice and mutation tasks | G1 | Architectural requirements specified; exact API pending |
| Benchmark host, sample sizes and thresholds | Repeated baseline measurements | G1 | No invented performance threshold |
| First real DSP and achievable evidence | DSP selection experiment | Before real DSP compatibility work | TI manual is a candidate only |
| Named FP backend and specialization | Numeric qualification task | Before FP capability implementation/acceptance | Rust production requirement chosen; dependency not yet qualified |
| Exact Linux CPU and firmware needs | P4 profile task | Before CPU-SYSTEM gate | Provisional RV64GC/system features, not a complete profile |
| Mandatory host/endian CI implementation | Release infrastructure task | CPU-LAB | Policy fixed, infrastructure not claimed available |
| First board/device versions | Board-definition task | Before P5 implementation | Deferred by CPU-first sequencing |
| Naming/namespace | Project naming check | Before publication/reservation | Semulith proposed; no reservation |
| Desktop and broader weak-memory objectives | Product increment definition | Before their implementation | Later increments, not part of first headless release |

## 3. Artifact-use posture

The default distribution contains our Rust code, descriptions and tests we may distribute, generated outputs whose inputs permit that use, and source provenance. External tools may remain local development dependencies. Record actual terms per artifact and distinguish using a reference, deriving test observations, copying source, and redistributing vendor files. Do not assume a generic simulator prohibition or permission without the applicable source.

This draft acquires no paid tool, hardware, or restricted vendor asset. Selection and access are explicit P0/target-selection work; any real unresolved legal interpretation is attached to that artifact rather than generalized into an automatic approval process.
