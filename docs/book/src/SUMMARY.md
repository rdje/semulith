# Summary

[Introduction](introduction.md)

# The project

- [What is claimed, and what is not](claim-scope.md)
- [Current status](status.md)

# The models

- [One definition, one book](models.md)
- [The information a unit demands — CPU, DSP, board](models/the-information-a-unit-demands.md)

# The plan

- [Milestones and their dependencies](plan/overview.md)
    - [P0 — profile and evidence access](plan/p0.md)
    - [P1 — the processor laboratory](plan/p1.md)
    - [P2 — the first validated profile](plan/p2.md)
    - [P3 — breadth, and the DSP pressure](plan/p3.md)
    - [P4 — the Linux CPU profile](plan/p4.md)
        - [P4.2 — Privilege and mode transitions](plan/p4/privilege.md)
        - [P4.3 — Sv39 translation and protection](plan/p4/sv39.md)
        - [P4.4 — Atomics and reservations](plan/p4/atomics.md)
        - [P4.5 — Interrupts, counters and wait](plan/p4/interrupts.md)
        - [P4.6 — Instruction visibility and fence semantics](plan/p4/fence-i.md)
        - [P4.7 — Floating point](plan/p4/floating-point.md)
    - [P5–P7 — board, Linux, computer](plan/p5-p7.md)
    - [Multicore and optimization](plan/multicore.md)

# The contracts

- [The method](contracts/method.md)
- [Engineering rules](contracts/rules.md)
- [Architecture and canonical definitions](contracts/architecture.md)
- [The CPU/environment contract](contracts/cpu-environment.md)
- [Evidence, traceability and gates](contracts/evidence-and-gates.md)
- [archogen and eADL](contracts/archogen.md)
- [The information catalog](contracts/information-catalog.md)
- [Risks and decisions due](contracts/risks.md)
- [Sources and naming](contracts/sources.md)
- [Disposition of the v0.1 review](contracts/review-disposition.md)

# The data contracts

- [Schemas and fixtures](data/overview.md)
- [A worked example](data/worked-example.md)

# Working in this repository

- [Task-trees](working/task-trees.md)
- [What "checked" means](working/claim-verification.md)
- [The doctrine gates](working/doctrines.md)
- [Provenance and frozen records](working/provenance.md)

# Annexes

- [How the tracked assembler works](annex/assembler.md)
- [Building the first CPU model, step by step](annex/building-first-model.md)

[Glossary](glossary.md)

[Index](index.md)
