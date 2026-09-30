# Decision & Fact Records — Index (memory layer C)

Durable, cross-cutting facts and decisions live here, one record per file (ADR-style). Every
record must be listed below (the MEMORY-ARCH doctrine check enforces it). New record: copy
`TEMPLATE.md` → `<type>_<short-kebab-slug>.md`, fill it in, and add its row.

| Record | Type | One-line hook |
| --- | --- | --- |
| [`decision_claim-verification-adopted.md`](decision_claim-verification-adopted.md) | `decision` | "checked" means re-derived, falsified and durable; a missing leg is named, never omitted |
| [`decision_delivery-provenance-is-frozen.md`](decision_delivery-provenance-is-frozen.md) | `decision` | a delivered manifest records what arrived; its live rows are declared, not silently drifting |
| [`reference_upstream-spine-defects.md`](reference_upstream-spine-defects.md) | `reference` | four bedrock-template defects found by use, fixed locally through seams, unfixed upstream |
| [`decision_readme-routing-closure.md`](decision_readme-routing-closure.md) | `decision` | the landing page's caps and every destination it routes to are data in a registry, enforced |
| [`decision_public-repository-no-confidential-content.md`](decision_public-repository-no-confidential-content.md) | `project` | the repo is public and carries nothing confidential, so evidence is recorded unredacted |
| [`decision_reference-acquisition-route.md`](decision_reference-acquisition-route.md) | `decision` | three reference models obtained and runnable; having a binary is not having evidence, and none of them is yet independent |
| [`reference_softfloat-shared-ancestry.md`](reference_softfloat-shared-ancestry.md) | `reference` | Sail and Spike run the same floating-point source — 184 of 199 shared files byte-identical, so FP differential testing between them is one opinion |
| [`decision_dual-mandate-production-and-teaching.md`](decision_dual-mandate-production-and-teaching.md) | `decision` | every model is production-grade AND a teaching text; the mistakes stay in the record because they are the instructive part |
| [`decision_browser-wasm-target.md`](decision_browser-wasm-target.md) | `decision` | the browser is a first-class target — JS + Wasm from the first crate, not a late port |
| [`decision_one-definition-one-book.md`](decision_one-definition-one-book.md) | `decision` | one canonical definition, one mdBook, one materials bill; kind and layer decide what a unit may own |
| [`decision_canonical-definition-input.md`](decision_canonical-definition-input.md) | `decision` | one canonical definition per unit as a set of format-fit files — **superseded in part** (`2026-09-14`): the per-file format split is replaced by `decision_one-format-every-source-of-truth`; the no-duplicated-fact rule stands |
| [`decision_composition-model.md`](decision_composition-model.md) | `decision` | breadth comes from composing proven models, not from gating them less; union with conflict detection, and assumption/guarantee discharge |
| [`decision_one-format-every-source-of-truth.md`](decision_one-format-every-source-of-truth.md) | `decision` | every engine input is S-expression, constructs are declared in data, and the Rust reader is LinkedSpec's via the vendored submodule — never hand-written, never `pgen` |
| [`reference_what-running-real-rust-actually-requires.md`](reference_what-running-real-rust-actually-requires.md) | `reference` | a trivial Rust function is 24% executable by rv64i-lab-v0 and halts at instruction one; C is on the critical path and there is no riscv64i Rust target |
| [`decision_push-cadence.md`](decision_push-cadence.md) | `decision` | push every 300 commits; below that a push is exceptional and only the director may grant it — the hook refuses rather than warns |
| [`decision_interpreter-before-compiler.md`](decision_interpreter-before-compiler.md) | `decision` | the semantics data is the execution authority — P1 interprets it directly; compiled handlers enter only as generated, equivalence-regressed artifacts |
| [`decision_lane-consumption.md`](decision_lane-consumption.md) | `decision` | every cross-cutting lane names the milestone that consumes it; no-consumer lanes are descoped at the next roadmap revision |
| [`decision_task-tree-family-bound.md`](decision_task-tree-family-bound.md) | `decision` | the docs/tasks/ aggregate bound is raised because the project tracks 25 lanes where it tracked 17; the per-part bound that actually bites is untouched |
| [`decision_task-tree-family-bound-rederivation.md`](decision_task-tree-family-bound-rederivation.md) | `decision` | the aggregate is re-derived to 1 MiB because the family tracks 32 files where it tracked 25 and the evidence archives are the designed growth; the per-part stays 64 KiB and bit correctly — it forced the P1-LAB split |
| [`decision_work-unit-prefix-semulith.md`](decision_work-unit-prefix-semulith.md) | `decision` | the work-unit prefix is SEMULITH, never SEMILITH — pinned in the commit-msg hook, watched behaviourally by COMMIT-PREFIX; history keeps both spellings, immutably |
| [`decision_c-guest-routing-and-toolchain.md`](decision_c-guest-routing-and-toolchain.md) | `decision` | the C guest lands in P2-SCALAR.5 (G0 precedent), built by the clang 21.1.8 + ld.lld 21.1.8 already on the host — measured present, never installed |
| [`decision_encoding-resourcing-probe.md`](decision_encoding-resourcing-probe.md) | `decision` | the RV64I encodings CAN be re-derived from the primary PDF (measured: 52/52 opcodes, zero conflicts, 37/52 fully by the naive parser) — adopt-in-principle; the re-source is a later reviewed leaf, not this one |
