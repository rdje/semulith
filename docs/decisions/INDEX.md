# Decision & Fact Records — Index (memory layer C)

Durable, cross-cutting facts and decisions live here, one record per file (ADR-style). Every
record must be listed below (the MEMORY-ARCH doctrine check enforces it). New record: copy
`TEMPLATE.md` → `<type>_<short-kebab-slug>.md`, fill it in, and add its row.

| Record | Type | One-line hook |
| --- | --- | --- |
| [Exact token facets](decision_exact-token-facets.md) | `decision` | strict token ends, generic searches;91 field controls |
| [Append-history predecessors](decision_append-history-predecessors.md) | `decision` | exact old bodies/order through sharding; staged and working proofs; failed Git reads refuse |
| [Book record navigation](decision_book-record-navigation.md) | `decision` | included and cross-unit links; fresh catalogue/path/fragment gate; shared viewing root |
| [Sail GPR comparison](decision_sail-gpr-comparison-method.md) | `decision` | Sail GPR: byte/image, input/impact and source-value composition; complete adequacy/collection pending |
| [Matched experiment contract](decision_qualified-matched-experiment-contract.md) | `decision` | matched-GPR syntax, authenticated evaluation and input/impact review; qualification/retention pending |
| [Obligation parts](decision_obligation-catalog-parts.md) | `decision` | explicit root-relative parts share one expansion owner; frozen bytes/order and fixed caps survive partition |
| [`decision_claim-verification-adopted.md`](decision_claim-verification-adopted.md) | `decision` | "checked" means re-derived, falsified and durable; a missing leg is named, never omitted |
| [`decision_delivery-provenance-is-frozen.md`](decision_delivery-provenance-is-frozen.md) | `decision` | a delivered manifest records what arrived; its live rows are declared, not silently drifting |
| [`reference_upstream-spine-defects.md`](reference_upstream-spine-defects.md) | `reference` | four bedrock-template defects found by use, fixed locally through seams, unfixed upstream |
| [`decision_readme-routing-closure.md`](decision_readme-routing-closure.md) | `decision` | the landing page's caps and every destination it routes to are data in a registry, enforced |
| [`decision_public-repository-no-confidential-content.md`](decision_public-repository-no-confidential-content.md) | `project` | the repo is public and carries nothing confidential, so evidence is recorded unredacted |
| [`decision_reference-acquisition-route.md`](decision_reference-acquisition-route.md) | `decision` | three reference models obtained and runnable; having a binary is not having evidence, and none of them is yet independent |
| [`reference_softfloat-shared-ancestry.md`](reference_softfloat-shared-ancestry.md) | `reference` | withdrawn internal census; public input/output scope and unexamined lineage limits (P4-SYSTEM.14 a6) |
| [`decision_fp-backend-qualification.md`](decision_fp-backend-qualification.md) | `decision` | the FP backend is rustc_apfloat 0.2.3+llvm-462a31f5a5ab (qualified by measurement: 63,752 MPFR cases, zero arithmetic-core disagreements, the LLVM-vs-IEEE flag deviations and the RISC-V policy gaps named) — the model layer owns the target policy; softfloat fails §6 on capability; the fallback stays named |
| [`reference_fp-model-layer-acceptance.md`](reference_fp-model-layer-acceptance.md) | `reference` | FP feature qualification: current governed vectors/fixtures and finite instruction checks; dated corpus/reference/performance receipts with corrected lineage limits |
| [`decision_dual-mandate-production-and-teaching.md`](decision_dual-mandate-production-and-teaching.md) | `decision` | every model is production-grade AND a teaching text; the mistakes stay in the record because they are the instructive part |
| [`decision_browser-wasm-target.md`](decision_browser-wasm-target.md) | `decision` | the browser is a first-class target — JS + Wasm from the first crate, not a late port |
| [`decision_one-definition-one-book.md`](decision_one-definition-one-book.md) | `decision` | one canonical definition, one mdBook, one materials bill; kind and layer decide what a unit may own |
| [`decision_canonical-definition-input.md`](decision_canonical-definition-input.md) | `decision` | one canonical definition per unit as a set of format-fit files — **superseded in part** (`2026-09-14`): the per-file format split is replaced by `decision_one-format-every-source-of-truth`; the no-duplicated-fact rule stands |
| [`decision_composition-model.md`](decision_composition-model.md) | `decision` | breadth comes from composing proven models, not from gating them less; union with conflict detection, and assumption/guarantee discharge |
| [`decision_one-format-every-source-of-truth.md`](decision_one-format-every-source-of-truth.md) | `decision` | every engine input is S-expression, constructs are declared in data, and the Rust reader is LinkedSpec's via the vendored submodule — never hand-written, never `pgen` |
| [`reference_what-running-real-rust-actually-requires.md`](reference_what-running-real-rust-actually-requires.md) | `reference` | a trivial Rust function is 24% executable by rv64i-lab-v0 and halts at instruction one; C is on the critical path and there is no riscv64i Rust target |
| [`decision_push-cadence.md`](decision_push-cadence.md) | `decision` | push every 300 commits; below that a push is exceptional and only the director may grant it — the hook refuses rather than warns |
| [`decision_ci-recovery-push-approval.md`](decision_ci-recovery-push-approval.md) | `decision` | fulfilled: all three hosted workflows pass at 76882c8; the scoped push approval has expired and ordinary cadence applies |
| [`reference_miri-reported-time-is-simulated.md`](reference_miri-reported-time-is-simulated.md) | `reference` | interpreted harness durations use Miri's simulated clock; external job timestamps supply wall-time evidence |
| [`decision_interpreter-before-compiler.md`](decision_interpreter-before-compiler.md) | `decision` | the semantics data is the execution authority — P1 interprets it directly; compiled handlers enter only as generated, equivalence-regressed artifacts |
| [`decision_lane-consumption.md`](decision_lane-consumption.md) | `decision` | every cross-cutting lane names the milestone that consumes it; no-consumer lanes are descoped at the next roadmap revision |
| [Task-family growth (2026-09-20)](decision_task-tree-family-bound.md) | `decision` | Why did the tracked-lane contract change the aggregate and count limits? |
| [Task-family growth (2026-09-28)](decision_task-tree-family-bound-rederivation.md) | `decision` | What did the multi-axis pressure review and P1-LAB split establish? |
| [`decision_profiles-family-two-units.md`](decision_profiles-family-two-units.md) | `decision` | the profiles/ bound is re-derived to 2× (240 files / 1,146,880 B) because the second unit's dossier is the family's designed growth; the per-part stays 32 KiB |
| [`decision_profiles-family-three-units.md`](decision_profiles-family-three-units.md) | `decision` | the profiles/ bound is re-derived to 3× (360 files / 1,720,320 B) because the first board dossier is the family's designed growth — the unit count, not content pressure, drives it; the per-part stays 32 KiB |
| [Four-unit bounds (2026-10-02)](decision_profiles-family-four-units.md) | `decision` | Why rederive when the first device arrives? |
| [Five-unit bounds (2026-10-02; composition corrected)](decision_profiles-family-five-units.md) | `decision` | Why the device/per-part changes, and what did LAN add? |
| [Composed bounds (2026-10-02; superseded in part)](decision_profiles-family-composed-units.md) | `decision` | Which measurements survive the interim raise? |
| [Corpus pressure (2026-10-06)](decision_profiles-family-processor-corpus.md) | `decision` | Why govern corpus growth separately? |
| [Derived bounds (2026-10-02)](decision_derived-members-of-bounded-families.md) | `decision` | How are derived exemptions proved? |
| [`reference_temporary-allocation-controls.md`](reference_temporary-allocation-controls.md) | `reference` | on-volume allocation/cleanup controls, child defaults and custom-vocabulary fixture repair |
| [`decision_task-history-seal-review.md`](decision_task-history-seal-review.md) | `decision` | approved12-file P4 history seal: byte-exact retention, immutable descriptor, checked retrieval and preserved paths/anchors |
| [`decision_models-family-five-books.md`](decision_models-family-five-books.md) | `decision` | the docs/models/ bound is re-derived to 5× (100 files / 655,360 B) because registration day (P5-BOARD.11) lands the third through fifth unit books — the one-definition-one-book rule's designed growth; the per-part stays 32 KiB |
| [`decision_decisions-family-aggregate-rederivation.md`](decision_decisions-family-aggregate-rederivation.md) | `decision` | the decisions/ bound is re-derived to 2× (80 files / 262,144 B) because the aggregate fired at ordinary decision velocity and the count axis is the same calendar; the per-part stays 16 KiB |
| [History-family bytes (2026-10-01)](decision_changelog-family-aggregate-rederivation.md) | `decision` | Why did the aggregate change while the partition and per-part bounds stayed? |
| [Changelog family count](decision_changelog-family-count-rederivation.md) | `decision` | count160→320; byte786432/per-part65536 and frozen partition unchanged |
| [Task-family count (2026-10-01; classification corrected)](decision_task-tree-family-count-rederivation.md) | `decision` | Why96, and what does the retained61-file receipt actually count? |
| [Task-tree part growth (2026-10-01)](decision_task-tree-per-part-growth.md) | `decision` | What size growth did the director authorize, and what remained constrained? |
| [`decision_gate-applicability-by-declared-vehicle.md`](decision_gate-applicability-by-declared-vehicle.md) | `decision` | gates derive per-unit applicability from the declared vehicle (route × comparison) plus the unit's documents — never deferral machinery; a declaration contradicting the documents is a finding |
| [Device applicability (2026-10-02)](decision_device-applicability-by-declared-vehicle.md) | `decision` | Which declarations determine applicable gates? |
| [`decision_work-unit-prefix-semulith.md`](decision_work-unit-prefix-semulith.md) | `decision` | the work-unit prefix is SEMULITH, never SEMILITH — pinned in the commit-msg hook, watched behaviourally by COMMIT-PREFIX; history keeps both spellings, immutably |
| [`decision_c-guest-routing-and-toolchain.md`](decision_c-guest-routing-and-toolchain.md) | `decision` | the C guest lands in P2-SCALAR.5 (G0 precedent), built by the clang 21.1.8 + ld.lld 21.1.8 already on the host — measured present, never installed |
| [`decision_encoding-resourcing-probe.md`](decision_encoding-resourcing-probe.md) | `decision` | the RV64I encodings CAN be re-derived from the primary PDF (measured: 52/52 opcodes, zero conflicts, 37/52 fully by the naive parser) — adopt-in-principle; the re-source is a later reviewed leaf, not this one |
| [`decision_release-route-x86-64-leg.md`](decision_release-route-x86-64-leg.md) | `decision` | the x86-64 leg's route: CI two-host matrix permanent (ubuntu-latest + macos-latest, the digest manifest the contract), Rosetta the time-bounded local bridge (phase-out fall 2027) — no narrower host policy |
| [`decision_release-rv64i-lab-v0.md`](decision_release-rv64i-lab-v0.md) | `decision` | rv64i-lab-v0 v0 is an EXPERIMENTAL release of the versioned evidence artifact, NOT an accepted profile — G-CONTRACT/G-OBLIGATIONS measured open (0/72 checks, 28 planned); the green axes and the closing conditions are named |
| [DSP56300 subset v0 (2026-10-01)](decision_dsp56300-lab-v0-subset.md) | `decision` | Which experimental subset, exclusions and vehicle? |
| [Book pacing (2026-10-02)](decision_mdbook-incremental-engaging.md) | `decision` | How are newcomers and experts both served? |
| [Doctrine-row bound (2026-10-02)](decision_doctrine-enforcement-ceiling-rederivation.md) | `decision` | Why did the 31st doctrine change the ceiling? |
| [`decision_document-everything.md`](decision_document-everything.md) | `decision` | document EVERYTHING — requests, rulings, nothing under the radar; every in-session ruling is routed to a durable layer and committed before the turn ends (director, backfilled from layer A) |
| [`decision_memory-next-action-pointer.md`](decision_memory-next-action-pointer.md) | `decision` | MEMORY.md exists solely to point at the next action — overwrite-only per MEMORY_ARCHITECTURE.md §6; everything durable lives in its own layer and is named by reference only |
| [Task-family bytes (2026-10-03)](decision_task-tree-family-aggregate-rederivation.md) | `decision` | Why did the aggregate change while the count and per-part bounds stayed? |
| [`decision_generated-mirror-needs-tracked-input.md`](decision_generated-mirror-needs-tracked-input.md) | `decision` | a tracked generated module needs a tracked canonical input — the rv64gc state module's landing is flip-bound; the scratch proof is the interim evidence (P4-SYSTEM.2 slice c) |
| [Six-activity count](decision_task-family-six-activity-count.md) | `decision` | Why 107, and what stays fixed before its separate application? |
