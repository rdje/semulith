# Sources and naming — v0.2

## Design inputs

This package responds to the CPU/DSP roadmap v0.1, the supplied `Review_of_CPU_DSP_Modeling_Roadmap_v0_1.md`, and the user's CPU-first, Rust, AI-assisted, canonical-definition, and archogen integration requirements.

The supplied `os-generation-roadmap-revised-v2.md`, revision 2.0 dated 2026-09-13, supplies the archogen boundary and milestones used in `ARCHOGEN_INTEGRATION.md`. In particular: eADL describes HW/OS functionality without implementation; the engine owns executable implementations and simulator composition; the hosted playground, independent QEMU execution, and physical-target gates are retained. These are project design inputs, not claims of implemented tools. Neither uploaded roadmap/review is modified by this package.

## Primary research sources

Reviewed during roadmap preparation on 2026-09-13. These links are discovery/reference inputs, not dependency lockfiles or proof that a tool has been acquired, built, or qualified for our selected profile. P0 records exact applicable revisions, commits, configurations, artifacts, and terms.

| Source | Reason to consult; boundary |
|---|---|
| [RISC-V RV64I specification, 20260120 snapshot](https://docs.riscv.org/reference/isa/v20260120/unpriv/rv64.html) | Base 64-bit instruction semantics for the provisional first profile; selected environment and system behavior need additional specification |
| [RISC-V RV32I base chapter](https://docs.riscv.org/reference/isa/v20260120/unpriv/rv32.html) | Base definitions inherited and modified by RV64I; read the relevant dependency closure |
| [RISC-V memory model](https://docs.riscv.org/reference/isa/v20260120/unpriv/rvwmo.html) | Ordering constraints; conformance and breadth of explored executions are separate claims |
| [RISC-V vector specification](https://docs.riscv.org/reference/isa/v20260120/unpriv/v-st-ext.html) | Later vector state, element progress, masking, and restart requirements |
| [Sail language and tools](https://github.com/rems-project/sail) | Study executable ISA semantics and tool generation; adoption is a separate architecture choice |
| [Sail RISC-V model](https://github.com/riscv/sail-riscv) | Candidate external semantics, generated C++ simulator, and effective JSON configuration; actual matched-profile access is a P0 gate |
| [RISC-V architectural tests](https://github.com/riscv/riscv-arch-test) | Current ACT4 flow uses configured Sail for expected results; valuable external tests, not an independent second Sail semantics |
| [Spike](https://github.com/riscv-software-src/riscv-isa-sim) | Candidate functional reference; its documented SC execution illustrates that allowed execution and exhaustive weak-memory exploration differ |
| [Berkeley SoftFloat](https://www.jhauser.us/arithmetic/SoftFloat.html) | Numerical reference candidate; does not determine every target-specific FP rule |
| [SoftFloat source and specialization documentation](https://www.jhauser.us/arithmetic/SoftFloat-3/doc/SoftFloat-source.html) | Pin target-dependent numerical policies and build choices |
| [Berkeley TestFloat](https://www.jhauser.us/arithmetic/TestFloat.html) | Numerical test generation/comparison; its usual SoftFloat expected-result path creates shared ancestry |
| [TI C64x/C64x+ CPU and instruction reference, SPRU732J](https://www.ti.com/lit/ug/spru732j/spru732j.pdf) | Real DSP documentation candidate for packets, addressing, and exposed sequencing; no runnable oracle access has been established |
| [Intel software developer manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html) | Architecture and system-behavior source family for later Intel profiles; manuals do not alone reproduce every implementation's timing or errata |
| [QEMU system emulation](https://www.qemu.org/docs/master/system/introduction.html) | Existing whole-system execution reference and architectural context |
| [QEMU RISC-V virt](https://www.qemu.org/docs/master/system/riscv/virt.html) | A virtual platform and independent execution route already selected in archogen's roadmap; pin the actual configuration |
| [QEMU instruction counting](https://www.qemu.org/docs/master/devel/tcg-icount.html) | Instruction-driven virtual time is not cycle-accurate physical timing |
| [Linux RISC-V boot requirements](https://docs.kernel.org/arch/riscv/boot.html) | Kernel entry and system integration constraints beyond scalar ISA behavior |
| [RISC-V SBI specification](https://github.com/riscv-non-isa/riscv-sbi-doc) | Firmware service contracts for the selected Linux route |
| [Miri](https://github.com/rust-lang/miri) | Scoped host Rust correctness checks, including cross-target/endian capabilities and limitations; not guest ISA proof |

No Arm reference model, production Rust floating-point library, DSP oracle, or physical target is selected or qualified by this source list. Resolve each when its target/profile enters scope. Source accessibility does not establish permission to redistribute every source, binary, or derived artifact; record actual applicable terms at acquisition.

## Working name

**Semulith** is the recommendation. It is a coined name suggesting semantics and emulation, broad enough for processor models, boards, and complete systems. It also pairs clearly with archogen: archogen generates specialized OSes; Semulith models machines that execute them.

Proposed command and initial crates: `semulith`, `semulith-core`, `semulith-verify`, `semulith-cli`. These names are proposals, not created packages.

A preliminary indexed exact-name search found no obvious software-project collision. A direct registry lookup did not establish availability. No crate, repository, domain, or trademark has been reserved or cleared. Recheck the exact intended namespaces when publishing; no engineering choice depends on a final public name.
