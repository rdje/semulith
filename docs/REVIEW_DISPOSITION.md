# Disposition of the v0.1 review

Date: 2026-09-13. Findings refer to the user's supplied review. Decisions incorporate the subsequent instruction to use a canonical source of truth.

| Finding | Decision | v0.2 treatment |
|---|---|---|
| M1 Product choice | Reject forced either/or; accept clearer priorities | Validated processors are the first product; boards and useful Linux computers are subsequent products |
| M2 Rules versus rationale | Accept | Short RULES.md plus architecture, evidence, catalog, and implementation documents |
| M3 Repeatable gate | Accept with correction | Many-to-many graph, conservative dependencies, stale-evidence invalidation, full release checks; annotations are not semantic proof |
| M4 Oracle availability | Accept early acquisition; adapt grading | Actual smoke tests; capability-specific evidence obligations and ancestry instead of a universal two-tier ranking |
| M5 DSP pilot | Adapt | Real-spec review plus synthetic stress and a bounded real slice; no automatic deferral of all real DSP work until Linux |
| M6 Environment boundary | Accept and strengthen | Independent versioned assumption/guarantee contract with adapter/harness checks and board composition obligations |
| M7 Early performance | Accept with limits | Common fixed-width paths, no mandatory instruction allocation, diagnostic observer modes and benchmarks; semantic effects cannot be compiled away |
| M8 FP dependency | Accept target pinning; qualify implementation first | Rust production numeric interface and a concrete qualification task before FP; TestFloat/SoftFloat ancestry recorded |
| M9 Weak memory and soundness | Accept separate milestone; correct proof argument | Finite differential equality is not universal proof; conformance and exploration completeness are separate |
| M10 Human role | Adapt | User owns goals/tradeoffs; routine work and reproducible gates can be automated; no blanket manual sign-off on every question |
| M11 Risk register | Accept | Ranked failures, observable triggers, and responses |
| M12 Artifact rights | Accept bounded ownership work | Record actual tool/source terms and shipping decisions; no speculative universal legal claims |
| M13 Device rigor | Accept | Reuse dossiers, evidence graph, and gates for devices and composition |
| M14 Endpoint | Adapt | First bounded system is headless with storage/network increments; interactive desktop remains a separately sized later goal |
| M15 Optional gate clauses | Accept explicit policy | Mandatory two native hosts plus scoped endian/Miri checks; missing required result is incomplete |
| M16 AI workflow placement | Accept | Short startup context, canonical instruction pointer, task contracts tied to gates |
| M17 Crate mapping | Accept | Core/verify/CLI ownership table, test harness explicitly in verification crate |
| M18 Diagrams | Accept | Milestone dependency graph and CPU/environment/verification boundary graph |
| M19 Glossary | Accept | Central definitions including validated, proved, locked and oracle |

Additional corrections retained: ACT4 supersedes deprecated RISCOF in the current architectural-test repository; ACT4's Sail-derived expected results are not a wholly independent semantic oracle; TestFloat's usual DUT comparison depends on SoftFloat; a deterministic reference test campaign cannot discharge a universal theorem; sequentially consistent implementations can produce a legal subset without exploring weak-memory outcomes.

The review's unsourced 10×/70% effort estimates and assumptions about mandatory human review hours are not adopted. Estimates will follow measured target/evidence experiments.

New v0.2 decision: begin directly with a small RV64I profile to reduce unnecessary 32-to-64-bit target churn. This changes a provisional v0.1 recommendation, not a user requirement. Separate new system-feature obligations remain necessary for Linux.

New user clarification: a canonical executable processor definition owns generation, while external specifications and independent evidence retain their roles. No generated self-agreement is promoted to conformance proof.

Subsequent user input: archogen will use Semulith platforms for generated-OS testing. Its supplied revision 2.0 controls that interface: eADL describes HW/OS functionality without implementation; the engine owns realization; Semulith supplies executable hardware models. The new integration document maps the timer, preemption, replay, trust, and physical-target obligations. archogen can use a smaller accepted CPU/board branch before Linux, while its hosted playground and existing QEMU/hardware gates remain in place.
