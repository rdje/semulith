# Evidence, traceability, and repeatable gates — v0.2

## 1. Evidence is a structured claim

An evidence record names the property and profile it addresses, how it was obtained, exact inputs, expected/observed artifacts, results, independence, limitations, and whether it remains current. Evidence methods include source review, directed tests, differential tests, hardware observations, exhaustive bounded checks, and checked proofs.

Do not rank these using one universal letter grade. A differential test over one arithmetic case and a source-reviewed global state invariant address different obligations. Record evidence per capability and declare the required policy before implementation. A source-reviewed experimental DSP subset may be useful but cannot inherit a fully differentially validated claim from another target.

Finite reference equality supports tested agreement. Universal refinement requires an appropriate checked argument over its stated domain and trust assumptions. Progress and allowed nondeterministic choices remain obligations even when tested runs happen to agree.

## 2. Minimal data contracts

`schemas/requirement.schema.json` defines each requirement. JSONL records use that schema individually. Fields include:

| Field | Meaning |
|---|---|
| `id`, `profile_ids`, `kind`, `statement` | Stable identity, applicability scope, obligation class, and precise assertion |
| `source_refs` | Applicable source ID and precise locator; fingerprints live in the source ledger |
| `applicability`, `research_status`, `implementation_status` | Separate relevance, knowledge, and implementation states |
| `source_semantics` | Original architecture's defined/undefined/etc. category and detail |
| `risk`, `obligation_ids` | Risk class and predeclared verification obligations |
| `dependencies`, `implementation_refs`, `evidence_ids` | Graph edges to requirements, code/configuration owners, and actual evidence |

`schemas/evidence.schema.json` defines records including requirement/obligation IDs, method, status, identity of the evidence producer, artifacts and fingerprints for completed work, ancestry/dependencies, and method limitations. Successful proof records also identify the checked proposition, checker, assumptions, and bounds.

`schemas/contract-obligation.schema.json` defines the versioned CPU/environment requirements. The supplied examples are an explicitly self-defined synthetic arithmetic/contract exercise with planned evidence; they are not real CPU results.

The schemas perform shape checks. The P1 checker additionally validates identifier references, profile consistency, graph integrity, artifact existence and hashes, evidence freshness, and gate policy. A syntactically valid JSON file is not an accepted CPU claim.

## 3. Requirement/code/test/evidence graph

Store explicit node types for requirements, semantic symbols/configuration rules, generated artifacts, generator steps, tests, comparators, source artifacts, reference builds, and evidence results. Named edge types include `implements`, `depends_on`, `generated_from`, `exercises`, `expects_from`, and `supports`.

Use source annotations or a generated symbol manifest to associate implementation sites with IDs. A proc macro is optional; structured comments plus a reliable extractor are sufficient initially. Tests declare their intended obligations. Keep runtime coverage separately: it can reveal missed interactions but is not proof that an obligation was adequately tested.

Required invariants:

- Every referenced ID exists and belongs to compatible profile scope.
- Every included requirement has an executable/configuration owner or a justified global-obligation owner.
- Every included requirement has its required verification dispositions; a proof or invariant check may serve where an ordinary runtime test is inapplicable.
- Every passed obligation points to actual successful, current evidence with required independence.
- No untested included requirement is silently reclassified as an exclusion.
- Shared primitives, adapters, reference configs, normalization rules, generators, and environment contracts appear in dependency analysis.
- Removed nodes/edges cannot silently make affected requirements or tests disappear from the report.

This is many-to-many traceability, not a bijection. The graph itself is checked and regression-tested. It does not prove that its handwritten dependency declarations capture every possible influence.

## 4. Conservative change impact

For a change:

1. Compare both old and new manifests, implementation fingerprints, source dependencies, generator inputs, build features, reference configs, and comparator rules.
2. Seed changed and deleted nodes, newly included requirements, and altered configuration/assumption nodes.
3. Traverse reverse dependency edges in the union of old and new graphs to identify affected obligations and their tests/evidence.
4. Mark that evidence stale; do not treat an old passing result as current.
5. If any relevant change is unmapped or its influence is uncertain, broaden to the complete affected profile or entire relevant suite.
6. Run targeted checks for fast feedback, followed by scheduled broad campaigns and the full applicable gate before a profile release.

Shared arithmetic, decode, memory-contract, event-scheduling, compiler/build, reference-adapter, or comparison-mask changes default to broad affected-profile validation unless narrower impact is justified. A documentation-only change still requires checking whether it changes a normative source interpretation or gate obligation.

A profile release report is generated from pinned inputs. It includes current/past evidence, invalidation reasons, selected test sets, and limitations; missing required checks produce `incomplete`, not `passed`.

## 5. Reference access and independence

P0 produces a working experiment, not a list of promising tools. For each candidate record: exact source/build availability, supported features and configuration, invocation, trace granularity, injection capabilities, effective config, artifact hashes, adapter version, restrictions on use/shipping, and a smoke-test result.

The independence inventory is per subsystem. Separate wrappers can share the same numerical library; different test suites can obtain expected values from one semantic model. Record known common ancestry and unknown ancestry without assuming either independence or correlation.

Current reference facts checked during the 2026-09-13 review:

- [Sail RISC-V](https://github.com/riscv/sail-riscv) generates a C++ simulator and supports JSON configurations and a generated schema; pin the effective configuration.
- [RISC-V architectural tests](https://github.com/riscv/riscv-arch-test) use ACT4, replacing deprecated RISCOF, and compute expected results using configured Sail; ACT4 adds tests but is not a wholly independent semantic engine.
- [TestFloat](https://www.jhauser.us/arithmetic/TestFloat.html) ordinarily compares DUT results against SoftFloat; direct SoftFloat comparison is not automatically a second independent numerical oracle.
- [Spike](https://github.com/riscv-software-src/riscv-isa-sim) supplies another implementation path, but independence of its subsystems must be examined rather than inferred from a different project name.

For a reference-less target, permit explicit experimental work with source review, independently derived boundary cases, bounded proofs where feasible, or hardware evidence. Do not manufacture a differential-validation claim. A real accepted profile must meet its declared obligations; revise scope explicitly if it cannot.

## 6. Testing the validator

Maintain small intentional mutations whose observations must be detected: wrong sign extension; suppressed register write; wrong trap cause; illegal-opcode substitution for a model limitation; an extra memory access; shifted event delivery; an overbroad mask hiding a changed defined bit; and a stale reference configuration.

Add replay/reduction checks: the minimized case retains the original divergence, and the input bundle replays the same result. A seed is accompanied by algorithm/version and the actual relevant event choices. Tests generated from the model remain labeled as such.

Normalize only source-permitted differences under compatible profiles. Undefined fields can have relational constraints; masking a whole register because one field is unspecified is invalid. No-fault final checksums cannot replace fault-priority, partial-progress, or event-boundary checks.

## 7. Processor release gate

| Gate ID | Required evidence |
|---|---|
| G-SCOPE | Exact profile, source revisions, observation contract, and complete selected dependency closure |
| G-STATE | State, aliases, arithmetic, effects, reset, and required pending state have reviewed requirements and evidence |
| G-CONTRACT | Enumerable CPU/environment assumptions and guarantees; validated laboratory and adapter mappings |
| G-TRACE | Graph integrity, actual artifacts, matched inputs, current evidence, and justified comparison rules |
| G-OBLIGATIONS | Every included requirement meets its predeclared verification policy, including risk-specific independence |
| G-INTERACTIONS | Declared fault, alias, boundary, event, progress, and restart interaction matrix exercised |
| G-REGRESSION | Full applicable directed, external, generated, workload, and validator-mutation suites pass |
| G-PORTABILITY | Required native x86-64 and AArch64 execution fixtures agree; selected pure-Rust primitive/state/endian tests pass their pinned Miri/cross-endian plan |
| G-REPLAY | Reports and relevant successes/failures reproduce from recorded definitions, tools, inputs, and event choices |
| G-RELEASE | Reproducible gate report, explicit capability limits, named release decision, and versioned accepted artifact |

The initial release policy makes both native host architectures mandatory. If infrastructure is not yet available, the development profile remains experimental until the check is completed or an explicit narrower host-support policy is adopted and labeled. No “when available” clause turns an incomplete gate into a pass.

Miri checks target an appropriate pure-Rust subset; foreign reference processes and unsupported operations remain covered through separate native tests. Host undefined-behavior checks do not establish guest ISA correctness. [Miri documents cross-target and big-endian testing as well as unsupported operations](https://github.com/rust-lang/miri).

Gate status is `passed`, `failed`, or `incomplete`. A release decision is recorded by the designated project maintainer or delegated release procedure after machine-generated results; it is not presumed to be a manual human sign-off on every code change. Outstanding goal/scope decisions are escalated only when material.

## 8. Later gates

Devices reuse the dossier, graph, and claim machinery. The board gate additionally checks that its guarantees satisfy the CPU assumptions. Linux boot checks system composition and workload progress; it does not retroactively prove CPU completeness.

The ARCHOGEN-OS gate additionally binds eADL/engine/plan/guest identities to the selected Semulith platform and tests. It preserves archogen's independent controls and physical-target gates. Shared device models or source facts enter the combined trust inventory; generated OS/model agreement alone is insufficient. Its full scope is in `ARCHOGEN_INTEGRATION.md`.

Multicore has distinct obligations for atomicity, reservation invalidation, coherence/ordering, interrupts, and fairness before SMP integration. A selected stronger execution model can be architecturally legal without exploring all allowed weak behaviors. Weak-memory exploration has its own checker/corpus/configuration and coverage claims.

The source/dialect, generator, backend, environment, comparator, numeric implementation, reference, and build configuration are all potential evidence invalidators. A locked CPU remains amendable through this process.
