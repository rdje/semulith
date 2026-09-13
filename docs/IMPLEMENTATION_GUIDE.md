# AI-assisted implementation guide — v0.2

## 1. Roles and session context

The user owns goals and material scope tradeoffs. The coding assistant executes resolved tasks, obtains evidence, investigates discrepancies, and maintains records. A named release procedure evaluates gates and records acceptance. Human judgment can resolve goals and ambiguous commitments; neither a human signature nor AI agreement substitutes for behavioral evidence.

No requirement assumes the user will manually read every line or approve every question. Routine resolved work proceeds autonomously. A change that conflicts with the user's north star, materially narrows scope, or commits to unavailable evidence is surfaced explicitly with its consequences.

When implementation begins, maintain one canonical repository `AGENTS.md` that points to `RULES.md`, the active profile/contract, current task, source ledger, and actual build/test commands. Other assistant-specific instruction files are thin pointers. This planning package does not install a skill or prescribe multiple agents.

The bounded initial read is: repository instructions, current task, relevant rules/profile/contract, required sources, and the last applicable gate/evidence state. Detailed architecture/catalog files are read when the task touches their subject.

## 2. Task record and completion loop

A task names its objective, profile and requirement/obligation IDs, source inputs, dependencies, expected module changes, acceptance checks, evidence output, unresolved questions, and factual completion status.

Work loop: read sources; establish discriminating expected cases; implement one coherent change; run relevant checks; reduce mismatches; update evidence/coverage/task status; leave a reproducible change. Use the conservative impact policy when updating existing semantics.

Record commands actually run and results actually observed. Do not transform planned validation into successful evidence. When expected behavior is ambiguous, investigate the source and reference configuration, preserve the conflict, and continue independent resolved tasks; seek a user decision only when it changes the contract or goal materially.

## 3. First task cards

| Task | Inputs and work | Acceptance result |
|---|---|---|
| T000 Profile dossier | RV64I specification, selected execution-environment rules; inventory state, instruction scope, access/misalignment and trap policies | Exact development profile, resolved foundational questions, source-linked obligation list |
| T001 Reference smoke test | Selected Sail/Spike builds and compatible configs; independently encoded arithmetic and access/trap experiments | Actual reproducible traces, hashes/configs, documented mismatches and missing injection capabilities |
| T002 Environment contract | Profile and reference mapping | Enumerable assumptions/guarantees, units/event boundaries, independent positive/negative fixture definitions |
| T003 Canonical model skeleton | Owned encodings/state/semantics plus deterministic generation manifest | No duplicate executable owner; regenerated metadata/dispatch passes consistency checks |
| T004 Graph and report checker | Supplied schemas, profile obligations, symbol/test manifests | Reject orphan IDs, stale hashes, unsupported passed claims, missing evidence and deleted dependency links |
| T005 Primitive layer | Source-linked widths and operations | Boundary cases, exhaustive tractable reduced-width checks, host-mode consistency |
| T006 First execution slice | Independent program bytes, controlled environment, canonical handlers | Correct state/access/exception observations and first-divergence report |
| T007 Validator mutations | Arithmetic, access, outcome and masking mutations | Every designated wrong behavior is detected; replay/reduction preserves mismatch |
| T008 Scalar profile completion | Remaining selected RV64I forms and interaction matrix | Full declared profile coverage and current evidence, not just executed mnemonics |
| T009 CPU-LAB release | Complete inputs, native host matrix, selected endian checks | Reproducible passed CPU gate and an explicitly versioned claim |
| T010 DSP architectural stress | Cases grounded in real manuals, plus synthetic executable stress fixture | Documented interface changes and clear split between synthetic and real compatibility evidence |
| T011 Floating-point qualification | Named Rust candidate, exact target policy, ancestry inventory and external numeric fixtures | Decision record with measured correctness/performance evidence before FP support is accepted |

T001 may reveal that T000 needs refinement; that feedback occurs before accepted profile implementation. T010 can study sources early but does not freeze shared APIs before actual processor behavior is exercised. These are engineering dependencies, not fixed week estimates.

During T000, compare the provisional width/features with archogen's selected target when available. Preserve a future adapter to its checked realization plan, using the boundary in `ARCHOGEN_INTEGRATION.md`. Implementing that adapter or an eADL parser is not a prerequisite for the first CPU slice. archogen's hosted S0 remains independent of Semulith readiness.

## 4. First real artifacts

Produce a profile, source lock, requirement catalog, environment contract, canonical model manifest, test list, reference mapping, evidence graph, gate report, and current task index. The user-facing CLI initially supports profile inspection, running laboratory programs, comparison, replay, and reporting; command spellings are chosen with the implementation.

Generated files are regenerated from their owned inputs. Pinned external specifications and separately sourced fixtures retain provenance. Update neither a golden value nor a comparator mask merely to make a discrepancy disappear.

## 5. Budget and progress

Use small per-change checks, bounded generated campaigns, scheduled broader regression, and full release validation. Stop extra testing once the current task's actual obligations are satisfied; additional campaigns need an identified risk or release requirement.

Measure progress in accepted semantic obligations and demonstrated capabilities. Estimate remaining work after observing source interpretation, oracle integration, numeric corner cases, and failure-reduction effort. Do not assume a fixed AI speed multiplier.
