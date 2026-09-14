; materials/catalog.sexp — the primary-source catalogue.
;
; A MATERIAL is a document a model is derived FROM: an ISA manual, an ABI specification, a
; datasheet. This file records which ones this project relies on, what they are, and where a
; copy of each can be found — and it does all of that WITHOUT NAMING A SINGLE ABSOLUTE PATH.
;
; ⛔ WHY THAT MATTERS ENOUGH TO SHAPE THE WHOLE FILE (Policy 12). The repository can be moved
; to another directory, another machine, another filesystem, and nothing about it may break.
; A tracked file holding `/Volumes/SSD/…` is a landmine that goes off on the first move, and it
; goes off silently: the path simply stops existing and a tool reports "not found" about a
; document that is sitting right there. So every path here is relative to something the file
; names:
;
;   cache-path   relative to (cache-root …), which is relative to the REPOSITORY ROOT
;   corpus-path  relative to a CORPUS ROOT, which this file DELIBERATELY DOES NOT KNOW —
;                it is supplied at run time through the named environment variable
;
; The absolute path therefore lives in the operator's environment, which is where machine-shaped
; facts belong, and never in git.
;
; ⛔ A CACHE IS NOT A SOURCE OF TRUTH. `.materials/` is gitignored: these are large third-party
; documents and the repository does not redistribute them. What IS tracked is this file — the
; identity, the revision, the digest and the licence — so a missing cache is a REFUSAL WITH
; INSTRUCTIONS rather than a wrong answer. Run `scripts/materials.py --fetch` to populate it.

(materials
  (schema-version 1)
  (cache-root ".materials")

  ;; ------------------------------------------------------------------------------------
  ;; Corpora: where copies come from. A corpus root is never written down here.
  ;; ------------------------------------------------------------------------------------
  (corpus
    (id "chipdoc")
    (title "chipdoc — curated documentation for digital components, chips, interfaces and protocols")
    (kind git-repository)
    (revision "4201f50")
    (env-var "SEMULITH_CHIPDOC_ROOT")
    (note "Curated, in its own words, to expose enough behaviour to reconstruct implementable
           intent AND to build software emulators that run real C/C++/Rust software — which is
           this project's north star stated by someone else, independently. 3684 files, 196 PDFs.
           Terms are recorded per document family in that repository's own README files, so a
           material's licence below is read from the DOCUMENT, not assumed from the corpus."))

  ;; ------------------------------------------------------------------------------------
  ;; Materials.
  ;; ------------------------------------------------------------------------------------
  (material
    (id "RVI-ISA-PDF-20260911")
    (title "The RISC-V Instruction Set Manual — Volume I Unprivileged and Volume II Privileged")
    (revision "20260911")
    (release-kind intermediate)
    (pages 906)
    (licence "CC-BY-4.0")
    (licence-evidence "the document's own preamble: \"The previous version of this document was
                       released under a Creative Commons Attribution 4.0 International License by
                       the original authors, and this and future versions of this document will be
                       released under the same license.\"")
    (corpus "chipdoc")
    (corpus-path "risc-v/isa/current/riscv-isa-manual_2026-09-11_RISC-V_Unprivileged_and_Privileged_ISA.pdf")
    (cache-path "riscv/riscv-isa-manual-20260911.pdf")
    (sha256 "70cb3c0b1de50d4f932a0ae6a5406891766aa741f6e2399f279e3e3af22a6fd4")
    (bytes 5529517)
    (supplies "the complete unprivileged and privileged architecture in one artifact, including
               every ratified extension — the breadth the pinned HTML chapters do not carry")
    (status reference-only)
    (note "⛔ THIS IS NOT THE ARTIFACT `rv64i-lab-v0` PINS, and it must not be substituted for it.
           Two independent differences, both measured:
           (1) REVISION. This is `20260911: Intermediate Release`; the profile pins `v20260120`
               from docs.riscv.org. An intermediate release is not a ratified one.
           (2) SECTION NUMBERING. This manual numbers RV32I §2.1 and RV64I §2.2. The pinned HTML
               numbers them §1.1 and §3.1, which is what all 52 semantic citations use. A reader
               holding this PDF cannot follow a single one of our locators.
           So it is catalogued as a reference the project may READ — for breadth, for the
           privileged architecture, for extensions the HTML set does not cover — and never as the
           authority a requirement cites. Reconciling the two is owned by `MODEL-METHOD.3`."))

  (material
    (id "RVI-PSABI-1.0")
    (title "RISC-V ELF psABI Specification, version 1.0")
    (revision "1.0")
    (release-kind ratified)
    (pages 56)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "risc-v/psabi/current/riscv-abi_v1.0_RISC-V_ELF_psABI.pdf")
    (cache-path "riscv/riscv-elf-psabi-1.0.pdf")
    (sha256 "a8d06bdcaa82a6a4567a1904dc27ef1ca1043ebaa1f523558c927a9d72bc23d9")
    (bytes 273939)
    (supplies "calling convention, register usage, ELF layout and relocations — the contract a
               model must honour to run code produced by a real C or Rust toolchain")
    (status wanted)
    (note "The north star is a model that runs real C and Rust. A compiler's output obeys this
           document, so it is a source of truth for the ENVIRONMENT the model presents, not for
           instruction semantics. Nothing cites it yet; it is catalogued because the requirement
           it will serve is already stated."))

  (material
    (id "Z80-UM0080")
    (title "Z80 CPU User Manual (UM0080)")
    (revision "2016-08")
    (release-kind final)
    (pages 332)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document")
    (corpus "chipdoc")
    (corpus-path "zilog/z80/current/UM0080_2016-08_Z80_CPU_User_Manual.pdf")
    (cache-path "zilog/z80-um0080.pdf")
    (sha256 "e3c83da5a5d8e372364c20fa53665e6fbb165ec6ac38c8c1eebc359603447b5e")
    (bytes 1587333)
    (supplies "a complete 8-bit CPU in one document: registers, every instruction with its
               encoding and timing, interrupt modes, bus behaviour")
    (status candidate)
    (note "A `start small and grow` candidate. One vendor document describes the WHOLE processor,
           so the materials census for it would be complete rather than mostly-deferred — which
           makes it a strong second unit and an unusually honest teaching text: a student can hold
           the entire source of truth in one hand. No leaf owns it yet."))

  (material
    (id "W65C02S-DS")
    (title "W65C02S 8-bit Microprocessor Datasheet")
    (revision "2022-04")
    (release-kind final)
    (pages 32)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document")
    (corpus "chipdoc")
    (corpus-path "wdc/65c02/current/W65C02S_2022-04_W65C02S_8-bit_Microprocessor_Datasheet.pdf")
    (cache-path "wdc/w65c02s.pdf")
    (sha256 "a6af3ca9da45c8a03504c94c7399cb6b08f15ce14185dd3e1e880433cdaa8cf5")
    (bytes 2655196)
    (supplies "the 6502-family programmer's model, addressing modes and the full opcode matrix")
    (status candidate)
    (note "The smallest complete CPU in the corpus — 32 pages. A second `start small` candidate,
           and a useful CONTRAST to the Z80: same era, same width, different enough that a
           composition vocabulary built for one should not silently assume the other."))

  ;; ------------------------------------------------------------------------------------
  ;; Gaps: what was LOOKED FOR and is not here. A census that records only what it found
  ;; cannot be distinguished from one that did not look.
  ;; ------------------------------------------------------------------------------------
  (gap
    (id "GAP-AMD64-APM")
    (looked-for "AMD64 Architecture Programmer's Manual (the AMD ISA)")
    (probe "find . -iname '*APM*' -o -iname '*AMD64*' -o -iname '*24592*'")
    (result "no match; the corpus's amd/ directory holds one document, an IO Virtualization
             (IOMMU) specification, which is system IP and not an instruction set")
    (consequence "there is no AMD instruction-set manual in this corpus. An x86-64 unit derived
                  from it would rest on Intel's description of the architecture only."))

  (gap
    (id "GAP-INTEL-SDM-VOL1")
    (looked-for "Intel 64 and IA-32 SDM Volume 1: Basic Architecture (document 253665)")
    (probe "find . -iname '*253665*' -o -iname '*Vol1*'")
    (result "no match; Volumes 2, 3 and 4 are present")
    (consequence "Volume 1 carries the basic execution environment, the data types and the
                  register overview — the architectural STATE a model declares first. An x86 unit
                  could not state its state from this corpus alone."))

  (material
    (id "ARM-A-DDI0487M.c")
    (title "Arm Architecture Reference Manual for A-profile architecture (DDI0487M.c)")
    (revision "M.c 2026-06")
    (release-kind final)
    (pages 17145)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "arm/architecture/a-profile/current/DDI0487M.c_2026-06_Arm_A-profile_Architecture_Reference_Manual.pdf")
    (cache-path "arm/arm-a-profile-ddi0487mc.pdf")
    (sha256 "b5f9daa7ec0446777c8f848aa6431c99e5ab6554e5aa171b28b9016771494f8c")
    (bytes 125757212)
    (supplies "AArch64 and AArch32: the complete application, system and exception model for application-class Arm")
    (status reference-only)
    (note "17,145 pages and 126 MB — EIGHTEEN TIMES the RISC-V manual, in one document. That number is
           not trivia; it is the argument for `start small and grow` stated in page counts. A
           materials census for this unit would be honest only if it admitted that no small team
           reads it end to end, which is exactly why the census records what a DECLARED SCOPE
           needs rather than what a document contains."))

  (material
    (id "ARM-M-DDI0553B.z")
    (title "Armv8-M Architecture Reference Manual (DDI0553B.z)")
    (revision "B.z 2026-02")
    (release-kind final)
    (pages 2149)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "arm/architecture/m-profile/armv8-m/current/DDI0553B.z_2026-02_Armv8-M_Architecture_Reference_Manual.pdf")
    (cache-path "arm/armv8-m-ddi0553bz.pdf")
    (sha256 "468594b22cf5a4bae1261f2cd39d5aa51040fbb566be18cc358c169918fd7a72")
    (bytes 16439994)
    (supplies "the Armv8-M microcontroller profile: Thumb instruction set, exception model, MPU, TrustZone-M")
    (status candidate)
    (note "The strongest `grow from there` step after RV64I: a modern, in-production ISA that runs real C
           and Rust, at 2,149 pages rather than 17,145 — and with an exception model small enough to
           model completely rather than partially."))

  (material
    (id "ARM-M-DDI0403E.e")
    (title "ARMv7-M Architecture Reference Manual (DDI0403E.e)")
    (revision "E.e")
    (release-kind final)
    (pages 858)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "arm/processors/cortex-m/armv7-m/current/DDI0403_E.e_ARMv7-M_Architecture_Reference_Manual.pdf")
    (cache-path "arm/armv7-m-ddi0403ee.pdf")
    (sha256 "76500176d20f897eaf05eeadb5a6202cef641e332073b107905c8898e0ee0747")
    (bytes 5957561)
    (supplies "the Armv7-M profile: Thumb-2, the Cortex-M3/M4/M7 programmer's model, NVIC and SysTick")
    (status candidate)
    (note "858 pages — comparable in size to the RISC-V manual, and the ISA behind the most widely
           deployed 32-bit microcontrollers. A realistic second unit."))

  (material
    (id "ARM-M-DDI0419E")
    (title "Armv6-M Architecture Reference Manual (DDI0419E)")
    (revision "E 2018-07")
    (release-kind final)
    (pages 374)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "arm/architecture/m-profile/armv6-m/current/DDI0419E_2018-07_Armv6-M_Architecture_Reference_Manual.pdf")
    (cache-path "arm/armv6-m-ddi0419e.pdf")
    (sha256 "7a61a708b40748219991145090ad7dd8ee41474ff89f4e45219a32f5ea93632f")
    (bytes 2265970)
    (supplies "the Armv6-M profile: the Cortex-M0/M0+ subset — the smallest complete modern Arm")
    (status candidate)
    (note "374 pages for a COMPLETE, currently-shipping 32-bit architecture that compilers target. If
           `start small` must also mean `runs real C and Rust`, this is the smallest document in
           the corpus that satisfies both."))

  (material
    (id "ARM-AR-DDI0406C.d")
    (title "ARM Architecture Reference Manual, ARMv7-A and ARMv7-R (DDI0406C.d)")
    (revision "C.d 2018-04")
    (release-kind final)
    (pages 2720)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "arm/architecture/a-r-profile/armv7-a-r/current/DDI0406C.d_2018-04_ARM_Architecture_Reference_Manual_Armv7-A_and_Armv7-R.pdf")
    (cache-path "arm/armv7-a-r-ddi0406cd.pdf")
    (sha256 "294668ae6480133b32d85e9567cc77c5eb0e1232decdf42cac7ab480e884f6e0")
    (bytes 18635697)
    (supplies "the 32-bit A and R profiles: A32/T32, the classic MMU and PL0/PL1 model")
    (status reference-only)
    (note "Kept for the 32-bit A-profile lineage the A-profile manual no longer centres on."))

  (material
    (id "X86-SDM-VOL2-325383")
    (title "Intel 64 and IA-32 Architectures Software Developer's Manual, Volume 2 (2A-2D): Instruction Set Reference")
    (revision "325383 2026-06")
    (release-kind final)
    (pages 2573)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "intel/isa/sdm/current/325383_2026-06_Intel_64_IA-32_SDM_Vol2_2A-2D_Instruction_Set_Reference.pdf")
    (cache-path "x86/intel-sdm-vol2-325383.pdf")
    (sha256 "db01e5918a710c16487e27a9e71a19af201f39b3311c55550559baaf0805160b")
    (bytes 11258123)
    (supplies "every x86 instruction: encoding, operation pseudocode, flags and exceptions")
    (status reference-only)
    (note "⛔ THE SDM SET IN THIS CORPUS IS INCOMPLETE, and the missing part is the one a model starts
           from. Volumes 2, 3 and 4 are present; VOLUME 1 (Basic Architecture, document 253665) IS
           NOT — probed and absent. Volume 1 carries the basic execution environment, the data
           types and the register overview, so an x86 unit could not state its architectural state
           from this corpus alone. Recorded as a census gap, not worked around."))

  (material
    (id "X86-SDM-VOL3-325384")
    (title "Intel 64 and IA-32 Architectures Software Developer's Manual, Volume 3 (3A-3D): System Programming Guide")
    (revision "325384 2026-06")
    (release-kind final)
    (pages 1602)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "intel/isa/sdm/current/325384_2026-06_Intel_64_IA-32_SDM_Vol3_3A-3D_System_Programming_Guide.pdf")
    (cache-path "x86/intel-sdm-vol3-325384.pdf")
    (sha256 "5b77208f34f7220b489db1642a681153e19dea5251a32973c01cb9e760bd0cce")
    (bytes 9592181)
    (supplies "protection, paging, interrupts and exceptions, system registers, virtualization")
    (status reference-only)
    (note "See the Volume 1 gap recorded on `X86-SDM-VOL2-325383`."))

  (material
    (id "X86-SDM-VOL4-335592")
    (title "Intel 64 and IA-32 Architectures Software Developer's Manual, Volume 4: Model-Specific Registers")
    (revision "335592 2026-06")
    (release-kind final)
    (pages 596)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "intel/isa/sdm/current/335592_2026-06_Intel_64_IA-32_SDM_Vol4_Model-Specific_Registers.pdf")
    (cache-path "x86/intel-sdm-vol4-335592.pdf")
    (sha256 "31d5a364c155a9a8855feb46eb8c3fa8777d768bf04272c0f90757c9e3a644d4")
    (bytes 3004271)
    (supplies "the model-specific registers, per microarchitecture")
    (status reference-only)
    (note "MSRs are per-implementation, so this is the document that makes an x86 model a model of a
           PART rather than of an architecture."))

  (material
    (id "POWER-ISA-3.1C")
    (title "Power ISA Version 3.1C (OpenPOWER)")
    (revision "3.1C 2024-05-26")
    (release-kind final)
    (pages 1495)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "openpower/isa/current/PowerISA_3.1C_2024-05-26_OpenPOWER_ISA_Specification.pdf")
    (cache-path "openpower/power-isa-3.1c.pdf")
    (sha256 "56372d23ece7e9e2c1b381a639443982a3e16e38109df1c141d655b779b61fdb")
    (bytes 6425593)
    (supplies "the complete Power ISA: books I-III, from user instructions to the hypervisor model")
    (status reference-only)
    (note "An openly licensed 64-bit architecture with a full privileged model — a useful CONTRAST to
           RISC-V for testing whether the composition vocabulary generalises beyond one ISA family."))

  (material
    (id "OPENRISC-1000-1.4")
    (title "OpenRISC 1000 Architecture Manual, version 1.4")
    (revision "1.4 2022-02")
    (release-kind final)
    (pages 379)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "openrisc/isa/current/OpenRISC-1000_1.4_2022-02_OpenRISC_1000_Architecture_Manual.pdf")
    (cache-path "openrisc/openrisc-1000-1.4.pdf")
    (sha256 "97027ef5967cdf8e8336db64619da089d3c4130da35c48d446242f5e9099ede7")
    (bytes 2242796)
    (supplies "a complete 32/64-bit RISC architecture including its supervisor model, in 379 pages")
    (status candidate)
    (note "Small, complete, openly specified, and supported by GCC and Linux — another unit where the
           materials census could realistically reach 100% rather than mostly-deferred."))

  (material
    (id "SPARC-2015")
    (title "SPARC Architecture 2015 (V8 and V9)")
    (revision "2015 2016-01")
    (release-kind final)
    (pages 564)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "sparc/isa/current/SPARC-2015_2016-01_SPARC_Architecture_2015_V8_and_V9.pdf")
    (cache-path "sparc/sparc-2015.pdf")
    (sha256 "7503a54267704c23b05ee6c983dd4eafe939901da8bde6419d6f545763d59d3b")
    (bytes 2380376)
    (supplies "SPARC V8 and V9 in one document: register windows, traps, the memory models")
    (status reference-only)
    (note "Register windows are a structure nothing else in this corpus has, which makes it a good
           stress test for whether the state model is general or quietly RISC-V-shaped."))

  (material
    (id "TI-C66X-SPRUGH7")
    (title "TMS320C66x DSP CPU and Instruction Set Reference Guide (SPRUGH7)")
    (revision "2010-11")
    (release-kind final)
    (pages 1013)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "ti/dsp/c66x/cpu/current/SPRUGH7_2010-11_C66x_CPU_and_Instruction_Set_Reference_Guide.pdf")
    (cache-path "ti/c66x-sprugh7.pdf")
    (sha256 "9e4a4d3dfc3bf570c3d7cccd9240c6050893d1f4ad1dade71c5821c75448aca2")
    (bytes 8843031)
    (supplies "the C66x VLIW DSP: 8 functional units, instruction packets, SIMD and fixed/floating-point")
    (status wanted)
    (note "`DSP-REVIEW` material. A VLIW DSP breaks the one-instruction-at-a-time assumption that an
           RV64I model can quietly make, which is precisely why the director put DSPs beside CPUs
           from the start rather than after."))

  (material
    (id "TI-C674X-SPRUFE8B")
    (title "TMS320C674x DSP CPU and Instruction Set User's Guide (SPRUFE8B)")
    (revision "B 2010-07")
    (release-kind final)
    (pages 770)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "ti/dsp/c674x/cpu/current/SPRUFE8B_2010-07_TMS320C674x_DSP_CPU_and_Instruction_Set_Users_Guide.pdf")
    (cache-path "ti/c674x-sprufe8b.pdf")
    (sha256 "34bc36312d37b092be9741986e70088f0fcefa00d8401a078f2b2981bb7b1d37")
    (bytes 3065047)
    (supplies "the C674x unified fixed- and floating-point DSP core")
    (status wanted)
    (note "`DSP-REVIEW` material."))

  (material
    (id "TI-C64X-SPRU732J")
    (title "TMS320C64x/C64x+ DSP CPU and Instruction Set Reference Guide (SPRU732J)")
    (revision "J 2010-07")
    (release-kind final)
    (pages 686)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "ti/dsp/c64x/cpu/current/SPRU732J_2010-07_TMS320C64x_C64x_DSP_CPU_and_Instruction_Set_Reference_Guide.pdf")
    (cache-path "ti/c64x-spru732j.pdf")
    (sha256 "5c1a240b1d3450e4023aba3a23750daf0c4470c198aa6d138cb13b69bc8a4f4f")
    (bytes 2847108)
    (supplies "the C64x fixed-point VLIW DSP")
    (status wanted)
    (note "`DSP-REVIEW` material."))

  (material
    (id "TI-C67X-SPRU733A")
    (title "TMS320C67x/C67x+ DSP CPU and Instruction Set Reference Guide (SPRU733A)")
    (revision "A 2006-11")
    (release-kind final)
    (pages 465)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "ti/dsp/c67x/cpu/current/SPRU733A_2006-11_TMS320C67x_C67x_DSP_CPU_and_Instruction_Set_Reference_Guide.pdf")
    (cache-path "ti/c67x-spru733a.pdf")
    (sha256 "dba7f65ff4c4b8676251d357b3b1cf28d554ab01cdf32917f6b9787bd74a17f9")
    (bytes 1717615)
    (supplies "the C67x floating-point VLIW DSP")
    (status wanted)
    (note "`DSP-REVIEW` material."))

  (material
    (id "TI-C55X-SPRU371F")
    (title "TMS320C55x DSP CPU Reference Guide (SPRU371F)")
    (revision "F 2004-02")
    (release-kind final)
    (pages 263)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "ti/dsp/c55x/cpu/current/SPRU371F_2004-02_TMS320C55x_DSP_CPU_Reference_Guide.pdf")
    (cache-path "ti/c55x-spru371f.pdf")
    (sha256 "43a9461ba20be87cb4ce212e633fb78b892ff2f02131820581777e198d88f40a")
    (bytes 1122365)
    (supplies "the C55x accumulator DSP: dual MACs, saturation and rounding modes, circular addressing")
    (status wanted)
    (note "`DSP-REVIEW` material, and at 263 pages the smallest DSP in the corpus. Accumulator width
           and saturation semantics are `DSP-REVIEW.1`'s subject exactly."))

  (material
    (id "TI-C28X-SPRU430F")
    (title "TMS320C28x CPU and Instruction Set Reference Guide (SPRU430F)")
    (revision "F 2016-05")
    (release-kind final)
    (pages 551)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "ti/dsp/c28x/cpu/current/SPRU430F_2016-05_TMS320C28x_CPU_and_Instruction_Set_Reference_Guide.pdf")
    (cache-path "ti/c28x-spru430f.pdf")
    (sha256 "f705551b1c4630a0476b58d0ba7509e254c5bf1378956c41ade1e2ac16115a72")
    (bytes 2344453)
    (supplies "the C28x fixed-point DSP/MCU hybrid used in real-time control")
    (status wanted)
    (note "`DSP-REVIEW` material."))

  (material
    (id "TI-MSP430-SLAU144K")
    (title "MSP430x2xx Family User's Guide (SLAU144K)")
    (revision "K 2022-08")
    (release-kind final)
    (pages 703)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "ti/mcu/msp430/x2xx/current/SLAU144K_2022-08_MSP430x2xx_Family_Users_Guide.pdf")
    (cache-path "ti/msp430x2xx-slau144k.pdf")
    (sha256 "841493836042c4dc2979ebe9a7b42f4e6f373a01edc34ee6d26445ae38a2f7b2")
    (bytes 9952227)
    (supplies "a complete 16-bit MCU: CPU, memory map and every on-chip peripheral")
    (status candidate)
    (note "An MCU document, so it crosses the layer boundary on purpose: CPU in one half, PERIPHERALS
           in the other. It is the natural first test of whether `processor` and `board` really are
           separable, because here one vendor document describes both."))
)
