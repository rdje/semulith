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
    (revision "3dc4e62")
    (env-var "SEMULITH_CHIPDOC_ROOT")
    (derivation "Re-derived 2026-09-14 by a PATH SWEEP, not a sample:
                 find . -name '*.pdf' | grep -iE '/(isa|cpu|architecture|processors|m68k|z80|65c02|dsp|mcu)/'
                 ⭐ The first pass guessed vendor directory names instead and missed eight
                 documents, among them the ENTIRE M68000 architecture — which lives under
                 nxp/m68k/, not a motorola/ directory that does not exist. A catalogue assembled by
                 guessing where things are records the surveyor's expectations, not the corpus.")
    (note "Curated, in its own words, to expose enough behaviour to reconstruct implementable
           intent AND to build software emulators that run real C/C++/Rust software — which is
           this project's north star stated by someone else, independently. 5434 files, 302
           PDFs at the 3dc4e62 re-pin `2026-10-02` (working-tree census, .git excluded; 5415
           tracked at HEAD — the 5696 figure at c4ad8a2 included the untracked .git/.runtime
           payload; the PDF axis is directly comparable: 293 → 302, the MCU batch among them;
           5383/285 at d2437ff, 5313/257 at 92a73b6, 5309/255 at 73711d6, 3684/196 at the
           3c45e81 baseline). Terms are recorded per document family in that repository's own
           README files, so a material's licence below is read from the DOCUMENT, not assumed
           from the corpus."))

  ;; ------------------------------------------------------------------------------------
  ;; Materials.
  ;; ------------------------------------------------------------------------------------
  (gap
    (id "GAP-RISCV-JAN-2026-PDF")
    (looked-for "the January 2026 riscv-isa-manual release PDFs (2026-01-17 / 2026-01-21), the
                 closest official release to this profile's pinned docs.riscv.org revision")
    (probe "not in this corpus; offered by an external investigation as an interim substitute")
    (result "DECLINED as a substitute, deliberately. Swapping them in would replace the artifact
             every one of the 52 citations resolves against with one that numbers its chapters
             differently, turning 52 resolving citations into 52 unresolvable ones — a strictly
             worse position reached by acquiring more material.")
    (consequence "they may be catalogued LATER as additional reference materials, under their own
                  ids, never as `RVI-RV32I` or `RVI-RV64I`. Acquiring a document and repointing a
                  pin are two different decisions and only the first is cheap.")
    (status resolved)
    (resolved-on "2026-09-14")
    (resolved-by "DECISION, recorded at filing (MODEL-METHOD.12): DECLINED as a substitute — the
                  result field above is the disposition, not an open question. Chipdoc's poller
                  read this record as open on 2026-09-30 because it carried no status; chipdoc
                  mirrored it resolved (declined as a pin substitute) under the same reasoning,
                  and this status makes the catalogue say so itself."))

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
    (corpus-path "risc-v/isa/reference/github-riscv-isa-manual/2026-09-11/riscv-isa-manual_2026-09-11_RISC-V_Unprivileged_and_Privileged_ISA.pdf")
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
           SETTLED 2026-09-14, after an external investigation challenged the pin: the two are
           DIFFERENT PUBLICATIONS of the same specification, not a right one and a wrong one.
           github.com/riscv/riscv-isa-manual numbers `Introduction` as Chapter 1, so RV32I is §2
           and RV64I §4; docs.riscv.org (the Ratified Specifications Library, which this profile
           pins) renders `Introduction` as unnumbered front matter, so RV32I is §1.1 and RV64I
           §3.1. The pinned URLs return HTTP 200 with bytes identical to the recorded digests and
           `scripts/check_citations.py` resolves 52 of 52. See
           docs/knowledge/a-version-string-is-not-an-identity.md.
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
  ;;
  ;; ⛔ A RESOLVED GAP IS KEPT, NEVER DELETED. It carries (status resolved) and the evidence
  ;; that closed it. Deleting it would erase the fact that the question was ever asked, and the
  ;; next surveyor would have to rediscover both the absence and the fix. Two of the three below
  ;; were closed by the corpus itself, three commits after this project measured and reported them.
  ;; ------------------------------------------------------------------------------------
  (gap
    (id "GAP-AMD64-APM")
    (looked-for "AMD64 Architecture Programmer's Manual (the AMD ISA)")
    (probe "find . -iname '*APM*' -o -iname '*AMD64*' -o -iname '*24592*'")
    (result "no match; the corpus's amd/ directory holds one document, an IO Virtualization
             (IOMMU) specification, which is system IP and not an instruction set")
    (consequence "there is no AMD instruction-set manual in this corpus. An x86-64 unit derived
                  from it would rest on Intel's description of the architecture only.")
    (status resolved)
    (resolved-on "2026-09-14")
    (resolved-by "the corpus imported all 5 AMD64 APM volumes at commit e401a56 — Vol 1
                  Application Programming (24592 Rev 3.23, 392 pp), Vol 2 System Programming
                  (24593 Rev 3.41, 833 pp), Vol 3 General-Purpose and System Instructions
                  (24594 Rev 3.36, 696 pp), Vol 4 128/256-bit Media (26568 Rev 3.25, 1049 pp),
                  Vol 5 64-bit Media and x87 (26569 Rev 3.16, 368 pp). Verified here by digest;
                  all five are catalogued below.")
    (residual "the corpus records that AMD's current doc hub is not scriptable, so a newer APM
               revision could exist and not be captured. A gap CLOSED is not a gap that cannot
               reopen."))

  (gap
    (id "GAP-INTEL-SDM-VOL1")
    (looked-for "Intel 64 and IA-32 SDM Volume 1: Basic Architecture (document 253665)")
    (probe "find . -iname '*253665*' -o -iname '*Vol1*'")
    (result "no match; Volumes 2, 3 and 4 are present")
    (consequence "Volume 1 carries the basic execution environment, the data types and the
                  register overview — the architectural STATE a model declares first. An x86 unit
                  could not state its state from this corpus alone.")
    (status resolved)
    (resolved-on "2026-09-14")
    (resolved-by "X86-SDM-VOL1-253665 catalogued through the corpus seam (MODEL-METHOD.13) —
                  the material's own note records the closure. Chipdoc's poller read this record
                  as open on 2026-09-30 because it carried no status; chipdoc mirrored it resolved
                  (the volume is held), and this status makes the catalogue say so itself."))

  (gap
    (id "GAP-RISCV-V20260120-UNPRIV-PDF")
    (looked-for "the pinned publication's OWN PDF for the pinned version segment:
                 docs.riscv.org/reference/isa/v20260120/_attachments/riscv-unprivileged.pdf —
                 4,580,174 B, sha256
                 06bb3c23074f72060a0ec061a80933af948cae7ceafdcd9d1fe177b05fd150bc, 696 pages,
                 self-identifying `Version 20260120: Official Release`")
    (probe "corpus-wide at 73711d6 (2026-09-29): find -iname '*20260120*' -o -iname
            '*unprivileged*' → exactly one hit, the 20260911 intermediate; the pinned snapshot
            risc-v/isa/pinned/v20260120 holds unpriv/ priv/ biblio/ + SHA256SUMS — no PDF")
    (result "ABSENT from the corpus at the f33d330-predecessor 73711d6 (2026-09-29): exactly
             one `*20260120*`/`*unprivileged*` hit, the 20260911 intermediate; the pinned
             snapshot held 72 HTML pages and no PDF. Acquired directly by semulith
             (digest-pinned copy), then mirrored by chipdoc the same day.")
    (consequence "the digest-pinned local copy was the MODEL-METHOD.14 probe's input for a few
                  hours; the corpus seam now owns the bytes (RVI-UNPRIV-PDF-V20260120 and
                  RVI-PRIV-PDF-V20260120, both reference-only with the numbering trap
                  documented). ⛔ THE POLLED CHANNEL COULD NOT SEE THIS RECORD when it was
                  filed: chipdoc's poller then read only top-level (gap …) forms and this
                  catalogue nests its gaps inside the (materials …) form — measured 2026-09-29
                  (poll_semulith_gaps.py --semulith-root . --json → semulith_gaps_open: 0).
                  The request travelled operator-relayed; the deafness was surfaced for a
                  chipdoc-side fix. FIXED chipdoc-side 2026-09-30 (corpus `6bfabf2`): the
                  poller descends into the wrapper and reads the nested records — re-measured
                  here at the 92a73b6 re-pin (same probe → semulith_gaps_open: 2, the two
                  then-status-less records, unmirrored: []). The channel is now TWO-WAY: a
                  gap filed in this catalogue surfaces there without an operator relay.")
    (status resolved)
    (resolved-on "2026-09-29")
    (resolved-by "chipdoc mirrored both v20260120 PDFs at
                  risc-v/isa/reference/docs.riscv.org-v20260120/ (REQ-008, fulfilled same-day,
                  with the numbering-trap correction); byte-equality with the independent
                  docs.riscv.org fetch verified here — sha256
                  06bb3c23074f72060a0ec061a80933af948cae7ceafdcd9d1fe177b05fd150bc, two
                  acquisitions, one set of bytes; adopted through the corpus seam under
                  MODEL-METHOD.16"))

  (material
    (id "NXP-DSP56300-FAMILY-MANUAL")
    (title "DSP56300 16-Bit Digital Signal Processor Family Manual")
    (revision "2000")
    (release-kind final)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "nxp/dsp/dsp56300/current/DSP56300_Family_Manual.pdf")
    (cache-path "nxp/dsp56300-family-manual.pdf")
    (sha256 "b2e8e346fe55b05d20ad0e6bc03d45fd1e080d46d9a9cd9540271c0c37f5a31e")
    (bytes 24396254)
    (supplies "the DSP56300 family architecture: 24-bit data words, 56-bit accumulators WITH 8
               guard bits — the measured counterpoint to the TI C6000 family's absence of both
               (DSP-REVIEW.1/.2)")
    (status wanted)
    (note "Answers GAP-DSP56K-FAMILY-MANUAL the same day it was filed (`2026-09-30`, the channel's
           2026-09-30 DSP batch; corpus SHA256SUMS verified). Recovered from a Wayback snapshot by
           chipdoc (the vendor's downloads are blocked) — the provenance rides in the corpus's
           family README."))
  (material
    (id "ADI-SHARC-PRM-2.4")
    (title "SHARC Processor Programming Reference, Rev 2.4")
    (revision "2.4")
    (release-kind final)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "adi/dsp/sharc/current/SHARC_Processor_Programming_Reference_Rev2.4.pdf")
    (cache-path "adi/sharc-programming-reference-2.4.pdf")
    (sha256 "0b40637d05c7f33bc8e39235ee8a9d2c734b12c0372aff1eeac56a7554895869")
    (bytes 5516505)
    (supplies "the SHARC programming model: SIMD compute blocks, the DAGs' circular AND
               bit-reversed addressing — bit-reversed addressing is measured ABSENT from all
               three TI C6000 manuals (DSP-REVIEW.3)")
    (status wanted)
    (note "Answers GAP-ADI-SHARC-PRM the same day it was filed (`2026-09-30`; corpus SHA256SUMS
           verified). The full SHARC family dir also landed (2106x/21160/2126x/2136x/2137x/214xx
           hardware references + TigerSHARC + Blackfin + ADSP-219x in the same batch) — catalogued
           on demand, not preemptively."))
(gap
    (id "GAP-DSP56K-FAMILY-MANUAL")
    (looked-for "the Motorola DSP56300 Family Manual (the DSP56362/56366 pin-compatible
                 family's architecture document): the 24-bit-word, 56-bit-accumulator
                 WITH-guard-bits counterpoint to the TI C6000 family's measured absence of
                 both (DSP-REVIEW.1/.2)")
    (probe "corpus-wide at 92a73b6 (2026-09-30): no motorola/ or freescale/ DSP directory
            exists (the m68k line lives at nxp/m68k and is NOT a DSP); the TI set is
            complete for C6000; adi/dsp/sharc/ exists and is EMPTY")
    (result "ABSENT from the corpus at 92a73b6 — filed for the channel; the review does not
             block on it (the TI evidence stands on its own locators), but the .7 findings
             report wants the cross-vendor contrast before classifying 'no accumulator' as
             anything but a TI fact")
    (status resolved)
    (resolved-on "2026-09-30")
    (resolved-by "the channel, same day: chipdoc's 2026-09-30 DSP batch landed
                  nxp/dsp/dsp56300/current/ with its SHA256SUMS verified here; adopted as
                  NXP-DSP56300-FAMILY-MANUAL. Measured end-to-end: gap filed 2026-09-30,
                  the watcher's 19:42:33 fire (the CHANNEL.md §7 incident's fix held), the
                  batch committed chipdoc-side the same day."))
  (gap
    (id "GAP-ADI-SHARC-PRM")
    (looked-for "an Analog Devices SHARC programming reference (ADSP-2106x or ADSP-214xx):
                 the DAG-based addressing with circular AND bit-reversed modes —
                 bit-reversed addressing is measured ABSENT from all three TI C6000 manuals
                 (BITR is a data operation, not an addressing mode; DSP-REVIEW.3)")
    (probe "corpus-wide at 92a73b6 (2026-09-30): adi/dsp/sharc/ exists and is EMPTY (a
            placeholder); no other ADI content")
    (result "ABSENT from the corpus at 92a73b6 — filed for the channel; the empty directory
             says the want was contemplated there already")
    (status resolved)
    (resolved-on "2026-09-30")
    (resolved-by "the channel, same day: adi/dsp/sharc/current/ landed with 7 verified
                  documents incl. the Programming Reference (SHA256SUMS checked here);
                  adopted as ADI-SHARC-PRM-2.4."))

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

  ;; ------------------------------------------------------------------------------------
  ;; A material that is not one file. ⛔ Its identity is its MANIFEST's digest: a snapshot
  ;; identified by the digest of one of its pages is not identified at all.
  ;; ------------------------------------------------------------------------------------
  (material
    (id "RVI-PINNED-V20260120")
    (title "RISC-V Ratified Specifications Library, version segment v20260120 — full HTML snapshot")
    (revision "v20260120")
    (release-kind ratified)
    (kind snapshot)
    (manifest "SHA256SUMS")
    (pages 72)
    (licence "unrecorded")
    (licence-evidence "the served pages carry only \"Copyright © RISC-V International®\" and no
                       CC-BY statement, unlike the GitHub PDF — read, not assumed. OQ-4 stays open
                       for this rendering, which is why the snapshot is cached and not tracked.")
    (corpus "chipdoc")
    (corpus-path "risc-v/isa/pinned/v20260120")
    (cache-path "riscv/pinned-v20260120")
    (sha256 "f77463370c2fe52513a9803917c30b717f6169f2164d0c848b85c2fcd817530b")
    (bytes 6229)
    (supplies "⭐ THE ARTIFACT THIS PROJECT ACTUALLY CITES — 46 unprivileged + 24 privileged pages,
               an index and a bibliography. All 52 semantic citations in rv64i.sem.sexp resolve
               against it, and against no other publication of this specification.")
    (status authoritative)
    (note "This ends a real fragility. The citation evidence lived only in target/sources/, an
           UNTRACKED working area that needs the network to rebuild, which is why
           scripts/check_citations.py could never be a commit gate. Cached here it is
           reproducible offline from a manifest that verifies all 72 pages.
           ⭐ INDEPENDENT CORROBORATION, and it is worth more than it looks: chipdoc acquired this
           snapshot by its own route and its digests for intro, rv32 and rv64 EQUAL the ones
           committed in profiles/rv64i-lab-v0/sources.toml. Two acquisitions, two parties, one set
           of bytes — which is the one thing the external challenge to this pin could not have
           produced by agreement.")) 

  (material
    (id "AMD64-APM-VOL1")
    (title "AMD64 Architecture Programmer's Manual, Volume 1: Application Programming (24592)")
    (revision "Rev 3.23 2020-10")
    (release-kind final)
    (pages 392)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "amd/isa/apm/current/24592_Rev3.23_2020-10_AMD64_APM_Vol1_Application_Programming.pdf")
    (cache-path "amd/amd64-apm-vol1-24592.pdf")
    (sha256 "bc34c4426baaa4c0aa3fbca8205f29e555c9a9b7e6d93bcd33625a8bfae75537")
    (bytes 2496645)
    (supplies "the AMD64 application programming model: registers, data types, addressing")
    (status reference-only)
    (note "⭐ Closes GAP-AMD64-APM. AMD64 is the architecture x86-64 actually IS — Intel implements AMD's
           64-bit extension — so for an x86-64 unit this is not a second opinion about the same
           document, it is the other author of the same architecture. That makes Intel-vs-AMD a
           genuine independence axis for x86, in the EVD-04 sense, which the RISC-V unit does not
           have available to it."))

  (material
    (id "AMD64-APM-VOL2")
    (title "AMD64 Architecture Programmer's Manual, Volume 2: System Programming (24593)")
    (revision "Rev 3.41 2023-06")
    (release-kind final)
    (pages 833)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "amd/isa/apm/current/24593_Rev3.41_2023-06_AMD64_APM_Vol2_System_Programming.pdf")
    (cache-path "amd/amd64-apm-vol2-24593.pdf")
    (sha256 "6a330e406ffe39893b09f56925969cf16ac35cbbebd961f9ed9a630189a917ff")
    (bytes 20303609)
    (supplies "paging, protection, interrupts, system registers and SVM virtualization")
    (status reference-only)
    (note "Closes GAP-AMD64-APM, with Vols 1 and 3-5."))

  (material
    (id "AMD64-APM-VOL3")
    (title "AMD64 Architecture Programmer's Manual, Volume 3: General-Purpose and System Instructions (24594)")
    (revision "Rev 3.36 2024-03")
    (release-kind final)
    (pages 696)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "amd/isa/apm/current/24594_Rev3.36_2024-03_AMD64_APM_Vol3_General-Purpose_and_System_Instructions.pdf")
    (cache-path "amd/amd64-apm-vol3-24594.pdf")
    (sha256 "4d8eff047a237895dfa4433111511088a80b40dde9e2012f9b652113ee58a00e")
    (bytes 16745121)
    (supplies "every general-purpose and system instruction: encoding, operation, exceptions")
    (status reference-only)
    (note "The volume that pairs with Intel SDM Vol 2 — two independent descriptions of one
           instruction set, which is exactly the kind of pair a differential argument needs."))

  (material
    (id "AMD64-APM-VOL4")
    (title "AMD64 Architecture Programmer's Manual, Volume 4: 128-Bit and 256-Bit Media Instructions (26568)")
    (revision "Rev 3.25 2021-11")
    (release-kind final)
    (pages 1049)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "amd/isa/apm/current/26568_Rev3.25_2021-11_AMD64_APM_Vol4_128-Bit_and_256-Bit_Media_Instructions.pdf")
    (cache-path "amd/amd64-apm-vol4-26568.pdf")
    (sha256 "6fc81538046b83ca3cacb8afc209c3d3f1aa0e0ca1e15161b04fdf3e0348912e")
    (bytes 3570599)
    (supplies "SSE and AVX media instructions")
    (status reference-only)
    (note "Closes GAP-AMD64-APM."))

  (material
    (id "AMD64-APM-VOL5")
    (title "AMD64 Architecture Programmer's Manual, Volume 5: 64-Bit Media and x87 Floating-Point Instructions (26569)")
    (revision "Rev 3.16 2021-11")
    (release-kind final)
    (pages 368)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "amd/isa/apm/current/26569_Rev3.16_2021-11_AMD64_APM_Vol5_64-Bit_Media_and_x87_FP_Instructions.pdf")
    (cache-path "amd/amd64-apm-vol5-26569.pdf")
    (sha256 "8c8c63c5e285c50faac2e7d474cf5046f5fcccb54673f464f57a8cb171ef0767")
    (bytes 1129228)
    (supplies "MMX and x87 floating-point")
    (status reference-only)
    (note "Closes GAP-AMD64-APM."))

  (material
    (id "X86-SDM-VOL1-253665")
    (title "Intel 64 and IA-32 Architectures Software Developer's Manual, Volume 1: Basic Architecture")
    (revision "253665 rev 092 2026-06")
    (release-kind final)
    (pages 600)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "intel/isa/sdm/current/253665_2026-06_Intel_64_IA-32_SDM_Vol1_Basic_Architecture.pdf")
    (cache-path "x86/intel-sdm-vol1-253665.pdf")
    (sha256 "9d862bd7592d9fdd9f747c91d5e85be23ae3103f77185d1dcf7c5eb7277e5bdb")
    (bytes 3645716)
    (supplies "the basic execution environment, data types and register overview")
    (status reference-only)
    (note "⭐ Closes GAP-INTEL-SDM-VOL1, three commits after this project measured and reported the
           absence. This is the volume an x86 unit STARTS from: architectural state is declared
           before anything else, and Volumes 2-4 assume it rather than define it."))

  (material
    (id "M68000-PRM")
    (title "M68000 Family Programmer's Reference Manual (M68000PRM)")
    (revision "1992")
    (release-kind final)
    (pages 646)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "nxp/m68k/current/M68000PRM_1992_M68000_Programmers_Reference_Manual.pdf")
    (cache-path "motorola/m68000-prm.pdf")
    (sha256 "06e4864b78da0e815054cead9326b7ec9914661f240fd39a455f2061ff47c4e8")
    (bytes 4725896)
    (supplies "the complete 68000-family programmer's model, instruction set and addressing modes")
    (status candidate)
    (note "⛔ MISSED BY THE FIRST SURVEY, and the reason is instructive: it is filed under nxp/m68k/,
           because NXP inherited Motorola's semiconductor business through Freescale. A sweep by
           vendor name would have to know a thirty-year corporate history to find it; a sweep by
           PATH finds it immediately. A strong `start small` candidate in its own right — a CISC
           architecture with variable-length encoding, which is a genuinely different decoding
           problem from every fixed-width RISC in this catalogue."))

  (material
    (id "ARM-CORTEX-A76-TRM")
    (title "Arm Cortex-A76 Core Technical Reference Manual (100798)")
    (revision "r4p1 2020-07-31")
    (release-kind final)
    (pages 620)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "arm/processors/cortex-a/cortex-a76/current/100798_0401_00_2020-07-31_Cortex_A76_Technical_Reference_Manual.pdf")
    (cache-path "arm/cortex-a76-trm-100798.pdf")
    (sha256 "ea16a7af56045572125e0be1f6be8877eaef1e37d67133d8fb5dbcb96f7f9e57")
    (bytes 2527677)
    (supplies "one IMPLEMENTATION of the A-profile architecture: its IMPLEMENTATION DEFINED choices, caches, errata")
    (status reference-only)
    (note "The architecture manual says what is architecturally required; this says what one part
           actually does where the architecture leaves it open. `IMPLEMENTATION DEFINED` is exactly
           where a model must declare a choice rather than inherit one, so an architecture manual
           alone is not sufficient to model a PART."))

  (material
    (id "ESP32-TRM")
    (title "ESP32 Technical Reference Manual")
    (revision "v5.8 2025-07")
    (release-kind final)
    (pages 784)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "espressif/mcu/esp32/current/esp32_trm_v5.8_2025-07_ESP32_Technical_Reference_Manual.pdf")
    (cache-path "espressif/esp32-trm.pdf")
    (sha256 "4ba58e9fa0405ec2bf80b912a29b483f6edc8c4b2b1058201913a2fe37e582f0")
    (bytes 10173126)
    (supplies "a complete SoC: Xtensa LX6 cores, memory map, and every on-chip peripheral")
    (status candidate)
    (note "`P5-BOARD` material. A whole SoC in one document — the layer boundary this project draws
           between processor and board runs straight through it."))

  (material
    (id "ESP32-S3-TRM")
    (title "ESP32-S3 Technical Reference Manual")
    (revision "v1.8 2026-03")
    (release-kind final)
    (pages 1531)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "espressif/mcu/esp32-s3/current/esp32-s3_trm_v1.8_2026-03_ESP32-S3_Technical_Reference_Manual.pdf")
    (cache-path "espressif/esp32-s3-trm.pdf")
    (sha256 "4484bf8a69035ec42a731c58c64ada6fbd1f1618c5559409f134d9ea083f444f")
    (bytes 15215232)
    (supplies "the ESP32-S3 SoC: dual Xtensa LX7, vector extensions, peripherals")
    (status candidate)
    (note "`P5-BOARD` material."))

  (material
    (id "ESP32-C3-TRM")
    (title "ESP32-C3 Technical Reference Manual")
    (revision "v1.4 2026-03")
    (release-kind final)
    (pages 903)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "espressif/mcu/esp32-c3/current/esp32-c3_trm_v1.4_2026-03_ESP32-C3_Technical_Reference_Manual.pdf")
    (cache-path "espressif/esp32-c3-trm.pdf")
    (sha256 "90ef825653e7a2657dc1bb294041aace9f9b69da87d775c2f1b5bd11eb317423")
    (bytes 9623028)
    (supplies "a shipping RISC-V SoC: RV32IMC core, memory map, peripherals, interrupt matrix")
    (status wanted)
    (note "⭐ THE MOST DIRECTLY USEFUL BOARD DOCUMENT IN THE CATALOGUE for this project's current path.
           Its core is RISC-V, so it is the first real unit where this project's own RV work becomes
           the processor half of a board — and the UART and interrupt controller the director set
           aside as `board, not processor` are specified here, in the document where they belong."))

  (material
    (id "RP2040-DS")
    (title "RP2040 Datasheet")
    (revision "RP-008371-DS-1 2025-02-20")
    (release-kind final)
    (pages 642)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "raspberry-pi/mcu/rp2040/current/RP-008371-DS-1_2025-02-20_RP2040_Datasheet.pdf")
    (cache-path "raspberry-pi/rp2040-ds.pdf")
    (sha256 "be56fbb75ba0ae9e26558a73c93ac3e75c2ad4e6878d3b6703de2a76d886ea8c")
    (bytes 5301205)
    (supplies "dual Cortex-M0+ (Armv6-M), the memory map, PIO and every peripheral")
    (status candidate)
    (note "`P5-BOARD` material, and it pairs exactly with ARM-M-DDI0419E: the architecture manual gives
           the 374-page instruction set, this gives the part built around it. Processor and board,
           two documents, one system — the cleanest test of the layer boundary in the catalogue."))

  (material
    (id "RP2350-DS")
    (title "RP2350 Datasheet")
    (revision "2025-07-29")
    (release-kind final)
    (pages 1380)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "raspberry-pi/mcu/rp2350/current/RP2350_2025-07-29_RP2350_Datasheet.pdf")
    (cache-path "raspberry-pi/rp2350-ds.pdf")
    (sha256 "2877d0f270fb6d6a57943bee58aaad536aa027bea1e5b1c4ce2541a3230d4be8")
    (bytes 7968417)
    (supplies "Cortex-M33 AND Hazard3 RISC-V cores selectable on one die, plus peripherals")
    (status candidate)
    (note "⭐ A part that ships BOTH an Arm and a RISC-V core on one die, software-selectable. If a
           composition model is real, the same board description should compose with either
           processor — which makes this the sharpest available test of `MODEL-COMPOSE`'s slots."))

  ;; ------------------------------------------------------------------------------------
  ;; Adopted from the chipdoc feed (catalog/semulith-proposals.sexp) under MODEL-METHOD.15,
  ;; 2026-09-29 — the director's 2026-09-27 flagged set (psABI, SBI, BRS, U-Boot, DT, FU540,
  ;; virtio, ACT); psABI was already catalogued above. The records are the feed's own, in this
  ;; file's syntax, and every digest was re-verified at fetch, not trusted from the feed.
  ;; ------------------------------------------------------------------------------------

  (material
    (id "RISCV-ARCH-TEST-ACT4")
    (title "RISC-V Architectural Test Suite (riscv-arch-test / ACT) — documentation and test plans")
    (revision "branch act4 e2216915 2026-09")
    (release-kind intermediate)
    (kind snapshot)
    (manifest "SHA256SUMS")
    (licence "Apache-2.0 AND CC-BY-4.0")
    (licence-evidence "upstream COPYING.APACHE and COPYING.CC in the repository root")
    (corpus "chipdoc")
    (corpus-path "risc-v/compliance/riscv-arch-test/current")
    (cache-path "riscv/riscv-arch-test-act4")
    (sha256 "ec4b9eb6f86a9caa4780d3dea0d78fddd247ba8c3d5138e18f57447b8c8bb5c8")
    (bytes 12229)
    (supplies "the operational definition of architectural compliance: docs/ (developer guide,
               coverage, memory map, SBI changes) and testplans/ (per-extension coverage CSVs and the
               privileged test plans)")
    (status wanted)
    (note "⛔ PARTIAL BY DESIGN: the full tree is ~672 MB uncompressed, almost entirely generated
           .S tests (635 MB) and .svh coverpoints (31 MB); only the documentation and test-plan
           metadata (136 files, ~1 MB) are committed. The full suite is identified by commit
           e2216915d9a17acc142610831d88de8b65683866 and must be fetched from upstream.
           This is the `P2-SCALAR.5` blocker-(a) material: the campaign's planning half is now
           catalogued and cached; the generated tests arrived `2026-09-30` with `.5` strand 2 —
           a blobless sparse clone at the same pin, `target/refs/riscv-arch-test/` (untracked;
           `tests/env` + `tests/rv64i/I` + `config`, 45 MB — the RV64I campaign needs nothing
           else of the ~672 MB tree)."))

  (material
    (id "RISCV-SBI-2.0")
    (title "RISC-V Supervisor Binary Interface Specification, version 2.0")
    (revision "2.0")
    (release-kind ratified)
    (pages 74)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "risc-v/system-ip/sbi/current/riscv-sbi-2.0.pdf")
    (cache-path "riscv/riscv-sbi-2.0.pdf")
    (sha256 "63084f54f382715efb340f46695d0e5cebd98965292d034d1b184b1abd3a682b")
    (bytes 485497)
    (supplies "the SBI call ABI between supervisor software and M-mode firmware: timer, IPI, console,
               system reset, hart state, and the HSM extension a Linux boot depends on")
    (status wanted)
    (note "The boot-chain contract on the software side; OPENSBI-v1.9 is its reference
           implementation (feed record, not yet adopted)."))

  (material
    (id "RISCV-BRS-1.0")
    (title "RISC-V Boot and Runtime Services Specification (BRS), version 1.0")
    (revision "1.0 2025-08-29")
    (release-kind ratified)
    (pages 31)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document — recorded as unrecorded rather than guessed")
    (corpus "chipdoc")
    (corpus-path "risc-v/firmware/brs/current/riscv-brs-spec_v1.0_2025-08-29.pdf")
    (cache-path "riscv/riscv-brs-1.0.pdf")
    (sha256 "a04583ee136f51ace99ab78aab75834dfe4874009ff52ff97d02e37610f3c4fe")
    (bytes 210075)
    (supplies "the server-class RISC-V boot contract: hart and SBI requirements, UEFI/ACPI/SMBIOS
               expectations, device-property conventions for UARTs, and firmware-update/security
               guidance")
    (status wanted)
    (note "Sits above the SBI implementation: OpenSBI implements the SBI, BRS states what a
           platform must present to the OS."))

  (material
    (id "DT-SPEC-0.4")
    (title "Devicetree Specification, version 0.4")
    (revision "v0.4 2023-06-28")
    (release-kind final)
    (pages 64)
    (licence "Apache-2.0")
    (licence-evidence "the document's own License Information section: \"Licensed under the Apache
                       License, Version 2.0 … You may obtain a copy of the License at
                       http://www.apache.org/licenses/LICENSE-2.0\" — read from the PDF, not assumed")
    (corpus "chipdoc")
    (corpus-path "devicetree/spec/current/devicetree-specification-v0.4.pdf")
    (cache-path "devicetree/devicetree-specification-v0.4.pdf")
    (sha256 "c141dd78af0971fffed19433f84af5beab6aa058cfff2e33076805cef9f92e02")
    (bytes 422295)
    (supplies "the node/property model, standard nodes (/memory, /cpus, /chosen, interrupt mapping),
               compatible matching, and the DTS/DTB format contract — the machine-readable board
               description a Linux boot consumes. The strongest datasheet class in the corpus because
               its correctness is checked by a real OS, not by a reader.")
    (status wanted)
    (note "Bindings for individual devices are NOT in this document — they live in the Linux kernel
           tree (Documentation/devicetree/bindings/) and must be cited at a pinned commit. The v1.0
           rework is in development and not yet a stable tag."))

  (material
    (id "UBOOT-2026.07")
    (title "U-Boot v2026.07 documentation subtree (doc/, Licenses/, README)")
    (revision "v2026.07 2026-07")
    (release-kind final)
    (kind snapshot)
    (manifest "SHA256SUMS")
    (licence "GPL-2.0-or-later")
    (licence-evidence "upstream Licenses/ and per-file SPDX headers; the project licence is GPL-2.0+")
    (corpus "chipdoc")
    (corpus-path "uboot/current")
    (cache-path "uboot/v2026.07")
    (sha256 "2b6e485d220cf8fa5cf976134ca3ea37fa1d49af35ed0f4e2e5963b1406858ad")
    (bytes 124423)
    (supplies "the bootloader contract between OpenSBI and Linux: boot flow, environment, FIT images,
               driver model, EFI loader, device-tree bindings, and per-board bring-up notes")
    (status wanted)
    (note "Snapshot identity is the digest of the SHA256SUMS manifest (1219 files), as for
           RVI-PINNED-V20260120. U-Boot publishes documentation as reStructuredText, not PDF, so the
           tracked artifact is the doc/ subtree; the 46 MB source tarball is referenced by tag, not
           committed."))

  (material
    (id "SIFIVE-FU540-C000")
    (title "SiFive FU540-C000 Manual v1p5")
    (revision "v1p5")
    (release-kind final)
    (pages 159)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document")
    (corpus "chipdoc")
    (corpus-path "sifive/fu540/current/FU540-C000_v1p5_manual.pdf")
    (cache-path "sifive/fu540-c000-v1p5.pdf")
    (sha256 "5fa68a677ca4bc9fc81456840834eb4fa72874a2bd72a76c33f6709f3ecab79c")
    (bytes 2361460)
    (supplies "a complete Linux-capable RISC-V board: memory map plus register descriptions for
               CLINT, PLIC, the SiFive UART (§13 — txdata/rxdata/txctrl/rxctrl/ie/ip/div; NOT a
               16550, corrected 2026-10-02 after a zero-hit pdftotext census of this artifact),
               SPI, I2C, PWM, GPIO, DMA, Ethernet (GEM), QSPI and DDR, and the boot flow")
    (status candidate)
    (note "v1p5 is now the current issue; v1p0 is retained at sifive/fu540/legacy/ in the corpus for
           citation compatibility. Composes with RVI-PINNED-V20260120 (the processor)."))

  (material
    (id "VIRTIO-1.2")
    (title "Virtual I/O Device (VIRTIO) Version 1.2 (OASIS CS01)")
    (revision "1.2 cs01 2022-07-01")
    (release-kind final)
    (pages 282)
    (licence "OASIS IPR Non-Assertion Mode")
    (licence-evidence "the document's own Status section: \"provided under the Non-Assertion Mode of
                       the OASIS IPR Policy\"")
    (corpus "chipdoc")
    (corpus-path "virtio/spec/current/virtio-v1.2-cs01_2022-07-01.pdf")
    (cache-path "virtio/virtio-1.2.pdf")
    (sha256 "42c7d2b9da95b4763e5416e18eab08d9a5d715dd98390cb5fb727205c15f5e45")
    (bytes 1213207)
    (supplies "split and packed virtqueue formats, feature negotiation, device configuration space,
               and per-device contracts (net, block, console, entropy) — the devices QEMU virt
               exposes to a guest")
    (status wanted)
    (note "The cheapest route to a Linux userspace on QEMU virt: model virtio devices instead of real
           hardware."))

  (material
    (id "RVI-UNPRIV-PDF-V20260120")
    (title "The RISC-V Instruction Set Manual, Volume I Unprivileged — docs.riscv.org PDF attachment, v20260120")
    (revision "v20260120")
    (release-kind ratified)
    (pages 696)
    (licence "unrecorded")
    (licence-evidence "the docs.riscv.org rendering carries only \"Copyright © RISC-V
                       International®\" and no CC-BY statement — the same OQ-4 position as the
                       pinned HTML snapshot")
    (corpus "chipdoc")
    (corpus-path "risc-v/isa/reference/docs.riscv.org-v20260120/riscv-unprivileged.pdf")
    (cache-path "riscv/riscv-unprivileged-v20260120.pdf")
    (sha256 "06bb3c23074f72060a0ec061a80933af948cae7ceafdcd9d1fe177b05fd150bc")
    (bytes 4580174)
    (supplies "the pinned publication's OWN PDF for the pinned version segment — and its
               instruction-format tables are SELECTABLE TEXT (pdftotext census by MODEL-BOOKS.2:
               232 [01]{7} lines vs 0 on all six pinned HTML/TXT artifacts), which is what the
               MODEL-METHOD.14 encoding-extraction probe needs")
    (status reference-only)
    (note "⛔ NOT A CITATION SOURCE, measured three ways and all three agree: this PDF numbers
           RV32I Chapter 2 and RV64I Chapter 4 (Introduction = Chapter 1); the pinned HTML
           numbers them §1.1 and §3.1, which is what all 52 semantic citations use. The trap is
           documented in the corpus mirror's README and re-measured here from the extracted
           text layer (\"Chapter 2. RV32I Base Integer Instruction Set, Version 2.1\").
           ⭐ TWO INDEPENDENT ACQUISITIONS, ONE SET OF BYTES: fetched from docs.riscv.org by
           MODEL-BOOKS.2 (HTTP 200, this digest) and mirrored by chipdoc (REQ-008, fulfilled
           2026-09-29) — the digests are equal. The HTML snapshot stays the citation authority;
           this answers only the \"are the tables text?\" question."))

  (material
    (id "RVI-PRIV-PDF-V20260120")
    (title "The RISC-V Instruction Set Manual, Volume II Privileged Architecture — docs.riscv.org PDF attachment, v20260120")
    (revision "v20260120")
    (release-kind ratified)
    (pages 214)
    (licence "unrecorded")
    (licence-evidence "as RVI-UNPRIV-PDF-V20260120 — the rendering carries no licence statement")
    (corpus "chipdoc")
    (corpus-path "risc-v/isa/reference/docs.riscv.org-v20260120/riscv-privileged.pdf")
    (cache-path "riscv/riscv-privileged-v20260120.pdf")
    (sha256 "2556d93a23cf8e1a476acc5208c505423866bb11753e850e0e1851935eeb3354")
    (bytes 1578278)
    (supplies "the privileged architecture for the pinned version segment — P4's M/S/U modes,
               Sv39 translation, CSR and interrupt evidence base, in the same publication family
               as the pin")
    (status reference-only)
    (note "Same numbering trap as the unprivileged volume (measured in its README): cite the
           pinned HTML snapshot, never this PDF, by section number. Mirrored by chipdoc under
           REQ-008 alongside the unprivileged volume the probe needed; catalogued here while
           the mirror is fresh rather than re-discovered at P4."))

  ;; ------------------------------------------------------------------------------------
  ;; Adopted from the chipdoc ANSWERS feed (catalog/responses.sexp, records in
  ;; catalog/semulith-proposals.sexp) under P5-BOARD.9, 2026-10-01 — the five FULFILLED
  ;; answers to the ten network-connected-board requests (P5-BOARD.8); the five BLOCKED
  ;; answers are measured negatives, recorded in materials/requests.sexp. Every digest
  ;; re-verified at fetch, never trusted from the feed.
  ;; ------------------------------------------------------------------------------------
  (material
    (id "MICROCHIP-LAN9118")
    (title "LAN9118 High Performance Single-Chip 10/100 Non-PCI Ethernet Controller datasheet")
    (revision "DS00002266B 2018-11-30")
    (release-kind final)
    (pages 109)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document")
    (corpus "chipdoc")
    (corpus-path "network/ethernet-lan9118/current/LAN9118_datasheet.pdf")
    (cache-path "network/lan9118.pdf")
    (sha256 "72fe68f241b5bc91a861cff98a877ae907339d396e64394b0f5daa2c391bf6ee")
    (bytes 836922)
    (supplies "a complete register-level 10/100 Ethernet MAC+PHY contract on a 16-bit non-PCI
               host bus: CSR set, FIFO packet memory, MII/PHY management, address filtering,
               interrupts and power management")
    (status wanted)
    (note "The wired-NIC candidate with a simple public register contract; QEMU's lan9118 model
           is a potential second implementation for differential checking. LAN9220 is the same
           family. Fulfilled from the official Microchip source."))
  (material
    (id "UBLOX-SARA-R4-AT")
    (title "u-blox SARA-R4 series AT commands manual")
    (revision "UBX-17003787 2021-07-08")
    (release-kind final)
    (pages 510)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document")
    (corpus "chipdoc")
    (corpus-path "network/modem-sara-r4/current/SARA-R4_ATCommands_UBX-17003787.pdf")
    (cache-path "network/sara-r4-at.pdf")
    (sha256 "ce73aa65261c052d48700846a58eb5144822f067703ffbd9ed1313fd13a634b6")
    (bytes 4955316)
    (supplies "the AT-command surface of an LTE Cat M1/NB-IoT module: general, SIM, network,
               packet-switched/socket data, SMS, GNSS and power-saving commands")
    (status wanted)
    (note "Recovered from a Wayback capture (20220121075106) of the official u-blox URL; the live
           u-blox site has rehomed content and the direct path now 404s."))
  (material
    (id "ESPRESSIF-ESP-AT")
    (title "ESP-AT User Guide (Espressif AT firmware for ESP32)")
    (revision "latest, docs.espressif.com build 2026-09-29")
    (release-kind final)
    (pages 533)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document")
    (corpus "chipdoc")
    (corpus-path "network/wifi-esp-at/current/esp-at-en-latest-esp32.pdf")
    (cache-path "network/esp-at.pdf")
    (sha256 "eb1f0c574fc3e532c92376f18417c24dc46a2a5cd82ec7d3429874f35e7b52e3")
    (bytes 9468246)
    (supplies "the documented AT command set for ESP32 WiFi modules (STA/AP, TCP/UDP sockets,
               MQTT, HTTP, mDNS) — the command layer above the ESP32/C3/S3 register maps held
               in the corpus (SVD-ESPRESSIF there; the ESP32 TRMs catalogued above)")
    (status wanted)
    (note "The WiFi-via-module route: a documented command surface over UART/USB; the corpus
           already holds the underlying ESP32 register maps, so this is the missing
           command-layer document."))
  (material
    (id "NORDIC-NRF52840-PS")
    (title "nRF52840 Product Specification")
    (revision "v1.7 2021-11-22")
    (release-kind final)
    (pages 631)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document")
    (corpus "chipdoc")
    (corpus-path "network/rfic-nrf52840/current/nRF52840_PS_v1.7.pdf")
    (cache-path "network/nrf52840-ps.pdf")
    (sha256 "f43354b2be1d5558e9e409787a940b16322d2d560da87b33f6206361bbc1469a")
    (bytes 12677464)
    (supplies "register-level documentation of a BLE/802.15.4/Thread radio SoC: RADIO,
               FICR/UICR, timers, PPI, GPIO, serial, ADC, AES/CCM and the memory map")
    (status wanted)
    (note "Recovered from a Wayback capture (20240829095752) of the official infocenter URL,
           which now returns HTTP 403; v1.9/v1.10 exist but have no archived snapshot."))
  (material
    (id "MICROCHIP-AT86RF233")
    (title "AT86RF233 Datasheet (2.4 GHz 802.15.4 radio transceiver)")
    (revision "Atmel-8351 2014-07")
    (release-kind final)
    (pages 225)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document")
    (corpus "chipdoc")
    (corpus-path "network/rfic-at86rf233/current/AT86RF233_datasheet.pdf")
    (cache-path "network/at86rf233.pdf")
    (sha256 "838d074fc1265d3dd50da0b407d1f987f09ebdb5a00a906c3b8c786fee52c543")
    (bytes 4588559)
    (supplies "the register-level 802.15.4 PHY/MAC contract: SPI register map, frame buffer,
               AES/CRC/address-match accelerators, RX/TX state machine and energy detect/RSSI")
    (status wanted)
    (note "A second register-documented radio so the RFIC leg's evidence does not rest on one
           vendor. Fulfilled from the official Microchip source (Atmel-8351)."))

  ;; ------------------------------------------------------------------------------------
  ;; Adopted from the chipdoc ANSWERS feed (catalog/responses.sexp) under MCU-DOCS.2,
  ;; 2026-10-02 — the twelve FULFILLED answers to the twelve MCU-documentation requests
  ;; (MCU-DOCS.1; the director's 2026-10-02 steer), PM0214 included as the STM32 answer's
  ;; named second document. Every digest re-verified at fetch, never trusted from the feed.
  ;; Measured at adoption: the three M-profile ARMs were ALREADY HELD corpus-side before
  ;; the requests (adoption was still the act — the corpus is not the tracked catalog),
  ;; and the RP2040 datasheet was held TWICE over — corpus-side AND in this catalog as
  ;; RP2040-DS since 2026-09-14 (same sha256, cached). The .1 survey measured the
  ;; semulith-facing proposals feed only: not the corpus's full tree, and not this
  ;; catalog. Recorded in the tree; the survey card
  ;; (docs/knowledge/a-survey-that-found-things-can-still-have-missed-things.md) gained
  ;; the recurrence.
  ;; ------------------------------------------------------------------------------------
  (material
    (id "ARM-ARMV6M-DDI0419E")
    (title "Armv6-M Architecture Reference Manual")
    (revision "DDI0419E 2018-07")
    (release-kind final)
    (pages 374)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document")
    (corpus "chipdoc")
    (corpus-path "arm/architecture/m-profile/armv6-m/current/DDI0419E_2018-07_Armv6-M_Architecture_Reference_Manual.pdf")
    (cache-path "mcu/armv6-m-arm.pdf")
    (sha256 "7a61a708b40748219991145090ad7dd8ee41474ff89f4e45219a32f5ea93632f")
    (bytes 2265970)
    (supplies "the minimal M-profile architecture contract (Cortex-M0/M0+/M1): the Thumb subset, the exception model, NVIC, SysTick, and the system-control register blocks")
    (status wanted)
    (note "The smallest honest MCU processor profile's architecture. Already held corpus-side before the request (the .1 survey measured the proposals feed, not the full catalog)."))
  (material
    (id "ARM-ARMV7M-DDI0403E")
    (title "Armv7-M Architecture Reference Manual")
    (revision "DDI0403E.e")
    (release-kind final)
    (pages 858)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document")
    (corpus "chipdoc")
    (corpus-path "arm/processors/cortex-m/armv7-m/current/DDI0403_E.e_ARMv7-M_Architecture_Reference_Manual.pdf")
    (cache-path "mcu/armv7-m-arm.pdf")
    (sha256 "76500176d20f897eaf05eeadb5a6202cef641e332073b107905c8898e0ee0747")
    (bytes 5957561)
    (supplies "the v7-M architecture contract: Thumb-2, the exception/interrupt model, NVIC, SysTick, the optional MPU, the debug architecture — what every Cortex-M3/M4-class MCU model is written against")
    (status wanted)
    (note "Already held corpus-side before the request (same survey-boundary note as ARM-ARMV6M-DDI0419E)."))
  (material
    (id "ARM-ARMV8M-DDI0553B")
    (title "Armv8-M Architecture Reference Manual")
    (revision "DDI0553B.z 2026-02")
    (release-kind final)
    (pages 2149)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document")
    (corpus "chipdoc")
    (corpus-path "arm/architecture/m-profile/armv8-m/current/DDI0553B.z_2026-02_Armv8-M_Architecture_Reference_Manual.pdf")
    (cache-path "mcu/armv8-m-arm.pdf")
    (sha256 "468594b22cf5a4bae1261f2cd39d5aa51040fbb566be18cc358c169918fd7a72")
    (bytes 16439994)
    (supplies "the current M-profile generation (Cortex-M23/M33/M55 class): mainline and baseline profiles, TrustZone-M, the revised exception and security model")
    (status wanted)
    (note "Already held corpus-side before the request (same survey-boundary note)."))
  (material
    (id "ARM-CORTEX-M0P-DDI0484C")
    (title "Cortex-M0+ Technical Reference Manual")
    (revision "DDI0484C r0p1 2013-01")
    (release-kind final)
    (pages 51)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document")
    (corpus "chipdoc")
    (corpus-path "arm/processors/cortex-m/cortex-m0plus/current/DDI0484C_2013-01_Cortex-M0plus_Technical_Reference_Manual.pdf")
    (cache-path "mcu/cortex-m0plus-trm.pdf")
    (sha256 "fe0ca5812590905e0628888871591704b09f3b4702317133938fc6fe1497a718")
    (bytes 427153)
    (supplies "the canonical v6-M core's implementation contract: pipeline, bus interface (AHB-lite), interrupt latency, the core register and system block integration — the RP2040's core")
    (status wanted)
    (note "Fulfilled 2026-10-02 from the Arm documentation-service API. Pairs with RPI-RP2040-DS as the complete MCU documentation pair (core TRM + SoC datasheet)."))
  (material
    (id "ARM-CORTEX-M3-DDI0337H")
    (title "Cortex-M3 Technical Reference Manual")
    (revision "DDI0337H r2p0 2010-03")
    (release-kind final)
    (pages 133)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document")
    (corpus "chipdoc")
    (corpus-path "arm/processors/cortex-m/cortex-m3/current/DDI0337H_2010-03_Cortex-M3_Technical_Reference_Manual.pdf")
    (cache-path "mcu/cortex-m3-trm.pdf")
    (sha256 "27d591dbee0ca98a6fe84ddb6a07145269beb24576b874d4edef83c5ec520045")
    (bytes 1058368)
    (supplies "the canonical v7-M MCU core's implementation contract — the most-documented MCU core in history; QEMU's lm3s/mps2 models are potential second implementations for differential checking")
    (status wanted)
    (note "Fulfilled 2026-10-02 from the Arm documentation-service API."))
  (material
    (id "ARM-CORTEX-M4-DDI0439B")
    (title "Cortex-M4 Technical Reference Manual")
    (revision "DDI0439B r0p0 2010-03")
    (release-kind final)
    (pages 117)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document")
    (corpus "chipdoc")
    (corpus-path "arm/processors/cortex-m/cortex-m4/current/DDI0439B_2010-03_Cortex-M4_Technical_Reference_Manual.pdf")
    (cache-path "mcu/cortex-m4-trm.pdf")
    (sha256 "f3f4b039116a0f9ea77c2788d6dfe657db45abc2b93ea1e3f3faaa4d511726d0")
    (bytes 895629)
    (supplies "the v7E-M core class (DSP extension, optional FPU) — the most-deployed MCU core class (STM32F4, nRF52840, i.MX RT)")
    (status wanted)
    (note "Fulfilled 2026-10-02 from the Arm documentation-service API."))
  (material
    (id "SIFIVE-FE310-G002")
    (title "SiFive FE310-G002 Manual")
    (revision "v1p7")
    (release-kind final)
    (pages 122)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document")
    (corpus "chipdoc")
    (corpus-path "sifive/fe310/current/FE310-G002_manual_v1p7.pdf")
    (cache-path "mcu/fe310-g002-manual.pdf")
    (sha256 "8e415163edfee3d14365e360a6ba313bdfb6f30b388ae9b17a6b037e27c7eca9")
    (bytes 1778902)
    (supplies "the RISC-V MCU contract: the E31 core, CLINT/PLIC (the timer and interrupt-controller contracts netboard-lab-v0 deliberately excludes), the peripheral set (GPIO, UART, SPI, I2C, PWM, WDT)")
    (status wanted)
    (note "Fulfilled 2026-10-02 from the SiFive CDN. The corpus also holds the G003 manual and both datasheets — the G002/G003 deltas are covered by holding both."))
  (material
    (id "NXP-IMXRT1050RM")
    (title "i.MX RT1050 Processor Reference Manual")
    (revision "Rev 0 2018-11")
    (release-kind final)
    (pages 3355)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document")
    (corpus "chipdoc")
    (corpus-path "nxp/imxrt/rt1050/current/IMXRT1050RM_2018-11_i.MX_RT1050_Processor_Reference_Manual.pdf")
    (cache-path "mcu/imxrt1050-rm.pdf")
    (sha256 "8ebe1a8843021e4279b4dd32e4a61c0c34e1c68538e9902959b09e7a1cf4798c")
    (bytes 19720404)
    (supplies "the crossover MCU class (Cortex-M7 at 600 MHz): full peripheral register contracts, clock tree, boot ROM interface — where MCU and application-processor documentation styles meet")
    (status wanted)
    (note "Fulfilled 2026-10-02 from a Wayback capture of the official NXP URL (the live URL 404s; the secured CDN 403s automated clients) — a measured route, recorded in the channel's evidence."))
  (material
    (id "TI-MSP430FR59XX-UG")
    (title "MSP430FR58xx/FR59xx/FR6xx Family User's Guide")
    (revision "SLAU367P Rev P 2020-04")
    (release-kind final)
    (pages 1024)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document")
    (corpus "chipdoc")
    (corpus-path "ti/mcu/msp430/fr59xx/current/SLAU367P_2020-04_MSP430FR58xx_FR59xx_FR6xx_Family_Users_Guide.pdf")
    (cache-path "mcu/msp430fr59xx-ug.pdf")
    (sha256 "82b04e7ad8219b6929f46fe59bbd0acf421f4faf36bd7a3eb0fbb6191d47c5d1")
    (bytes 6747929)
    (supplies "the ultra-low-power MCU classic — a non-Arm 16-bit architecture with full public documentation: the FRAM memory model, the power-management module, and the peripheral register contracts")
    (status wanted)
    (note "Fulfilled 2026-10-02 directly from ti.com/lit. The deliberate non-Arm contrast that keeps the MCU direction honest about what is Arm-shaped and what is not."))
  (material
    (id "MICROCHIP-SAMD21-DS40001882")
    (title "SAM D21 Family Data Sheet")
    (revision "DS40001882")
    (release-kind final)
    (pages 1160)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document")
    (corpus "chipdoc")
    (corpus-path "microchip/samd21/current/SAM-D21-DA1-Family-Data-Sheet-DS40001882.pdf")
    (cache-path "mcu/samd21-datasheet.pdf")
    (sha256 "dd583ced025b1c1c6221dcecd223b554ca54f7b05079ff9c3ff54944717f2183")
    (bytes 11828168)
    (supplies "the classic Cortex-M0+ vendor MCU datasheet: the peripheral register contracts (SERCOM, TC/TCC, ADC, DAC), the clock system (GCLK), power management and the event system")
    (status wanted)
    (note "Fulfilled 2026-10-02 from a Wayback capture of ww1.microchip.com (the live URL 403s automated clients) — the LAN9118 channel precedent measured Microchip as a good source family."))
  (material
    (id "ST-STM32L4-RM0394")
    (title "STM32L41xxx/L46xxx Reference Manual")
    (revision "RM0394 2018-10")
    (release-kind final)
    (pages 1600)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document")
    (corpus "chipdoc")
    (corpus-path "st/mcu/stm32/l4/current/RM0394_2018-10_STM32L41xxx-L46xxx_Reference_Manual.pdf")
    (cache-path "mcu/stm32l4-rm0394.pdf")
    (sha256 "44b528d82190627d8c08955f8422d2a57717f2bfce03f202826a79b2f7d86722")
    (bytes 29515460)
    (supplies "the dominant MCU vendor line's reference-manual class: the full peripheral register contracts for an STM32L4+ (GPIO, timers, USART, SPI, I2C, ADC, DMA, RCC)")
    (status wanted)
    (note "Fulfilled 2026-10-02 from Wayback captures of the official st.com URLs (st.com resets automated clients) — a measured route."))
  (material
    (id "ST-STM32-CM4-PM0214")
    (title "STM32 Cortex-M4 MCUs and MPUs Programming Manual")
    (revision "PM0214 Rev 10 2020-03")
    (release-kind final)
    (pages 262)
    (licence "unrecorded")
    (licence-evidence "not yet read from the document")
    (corpus "chipdoc")
    (corpus-path "st/mcu/stm32/l4/current/PM0214_2020-03_STM32_Cortex-M4_Programming_Manual.pdf")
    (cache-path "mcu/stm32-cm4-pm0214.pdf")
    (sha256 "fb54012a46c674a26dee56bc8cdfa281315f78634f18998001144980b08d1b03")
    (bytes 2732268)
    (supplies "the vendor's view of the Cortex-M4 core: the programming model, the instruction set summary, the core peripheral registers (NVIC, SCB, SysTick, FPU) as ST documents them")
    (status wanted)
    (note "The STM32 answer's named second document (REQ-MCU-STM32-RM asked for the RM + programming manual pair). Fulfilled 2026-10-02 from the same measured Wayback route."))
)
