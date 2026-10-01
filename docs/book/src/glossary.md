# Glossary

Included verbatim from the project's canonical glossary, so a term means the same thing in the
book, in the contracts, and in an evidence record.

{{#include ../../GLOSSARY.md}}

## The acronyms this book uses

The canonical glossary above defines the project's contract *terms*; this table expands the
*acronyms* a reader meets in the book's own pages (the frequent ones first, measured on the
book's text).

| Acronym | Expansion | Meaning in this book |
| --- | --- | --- |
| CPU | Central Processing Unit | the scalar processor models (the `rv64i-lab-v0` profile's target class) |
| DSP | Digital Signal Processor | the second architecture family (`dsp56300-lab-v0`); its scalar-breaking properties drive P3 |
| ISA | Instruction Set Architecture | the rules a processor family presents to software (see *Architecture / ISA* above) |
| RV64I | the RISC-V 64-bit base integer ISA | the first profile's instruction set; RISC-V = the open reduced-instruction-set architecture |
| OS | Operating System | the archogen consumer and the Linux milestones (P4, P6) |
| API | Application Programming Interface | the crate/library surface whose cross-architecture stability gate `BREADTH` watches |
| ACT | (RISC-V) Architecture Compatibility Tests | the pinned `riscv-arch-test` campaign; its expectations are Sail-derived, so it is not a second opinion on its own |
| ELF | Executable and Linkable Format | the guest-binary container the toolchain produces |
| JSON | JavaScript Object Notation | the data-contract and fixture format of `schemas/` and `examples/` |
| CI | Continuous Integration | the server-side workflow runs of the doctrine gates and tests |
| FM | Family Manual | the vendor's processor manual — DSP56300FM Rev. 5 for the DSP56300 family — the pinned primary source the DSP model's decode and semantics are derived from |
| ALU | Arithmetic Logic Unit | the DSP56300's Data ALU: the accumulator/MAC core the subset's arithmetic runs on |
| MAC | Multiply-ACcumulate | the DSP's atomic operation (signed `mpy`/`mac` in subset v0) |
| PC | Program Counter | the fetch address register |
| SR | Status Register | the DSP56300 register carrying the condition codes (CCR) and loop/system flags |

And the project's own compressed conventions: the **rule IDs** (`EVD-…`, `SRC-…`, `SEM-…`,
`REQ-…`) are the numbered engineering rules of *Engineering rules* (The contracts); the
**gates** (`G0`, `G1`, `BREADTH`, …) are the reproducible acceptance predicates defined in
*Evidence, traceability and gates*; the **milestones** (`P0`–`P7`) are the roadmap's phases
(*Milestones and their dependencies*); and **RED**/**green** name a doctrine gate's failing /
passing verdict — a gate is always fired RED on a known-bad fixture before it is trusted.

## Three distinctions worth re-reading

- **Validated** is an engineering claim about a named evidence policy, a scope, and an artifact
  version. **Proved** is a claim about a checked proposition with recorded assumptions and
  bounds. They are not degrees of the same thing.
- **Model limitation** is behaviour this implementation cannot yet model. A **target trap** is
  behaviour the architecture defines. Reporting the first as the second is how an emulator
  silently lies to its guest.
- **Architecturally unspecified** has a meaning the specification defines. **Not yet
  researched** is a gap in our knowledge. Collapsing them turns a project bookkeeping problem
  into a claimed architectural fact.
