;; references.sexp — the reference candidate dossier for `rv64gc-lab-v0` (P4-SYSTEM.2,
;; slice a: the encoding-source re-pin). One document form; validate with
;;   python3 scripts/check_sexp_schema.py profiles/rv64gc-lab-v0/references.sexp schema/references.sexp
;; Re-derive with `scripts/fetch_references.sh [--verify-only] rv64gc-lab-v0` — it needs the
;; network, so it is deliberately NOT a commit gate (the same reasoning as fetch_sources.sh).

(comment "profiles/rv64gc-lab-v0/references.sexp — the reference candidate dossier for"
         "`rv64gc-lab-v0`. The dossier began at profile resolution; the unit now executes"
         "the complete composition. P4-SYSTEM.2 slice (a) derives its fragments from encoding"
         "tables that must be pinned before they are derived from — a fragment generated from"
         "an unpinned source would be a model built on something nobody can re-derive (the"
         "rv64i dossier's own rule). Matched results below are finite public-interface evidence;"
         "structured experiment/control/independence records are owned by P4-SYSTEM.14"
         "(docs/EVIDENCE_AND_GATES.md §5). Every field is an observed fact (SRC-03): the two"
         "binary digests below were re-derived on this host the day this file was written.")

(references
  (profile "rv64gc-lab-v0")
  (retrieved "2026-10-03")
  (work_dir "target/refs")
  (host (os "macOS 27.0 (build 26A428)") (kernel "Darwin 27.0.0") (arch "arm64")
        (cxx "Apple clang (/usr/bin/clang)")
        (note "The repository volume holds every artifact this project owns under `target/refs/`; nothing is installed into a shared prefix (policy: project data locality)."))
  (comment "───────────────────────────────────────────────────────────── candidate 1: Sail RISC-V")
  (candidate
    (id "sail-riscv")
    (role "primary oracle candidate")
    (status "obtained")
    (kind "prebuilt release binary")
    (origin "https://github.com/riscv/sail-riscv")
    (release "0.14")
    (binary "target/refs/sail-riscv-Mac-arm64/bin/sail_riscv_sim")
    (binary_sha256 "16de42a86e4ea7a300385092632cd95d153cb3f6c119d31eaa9384953990b7bf")
    (invocation "sail_riscv_sim --config-override <override.json> [--trace...] <elf>")
    (trace_granularity "per instruction, and per effect within it: --trace-instr, --trace-gpr, --trace-csr, --trace-mem, --trace-exception, --trace-interrupt, --trace-pma, --trace-pmp, --trace-step; the implicit-access dimensions are their OWN flags (never in any umbrella): --trace-ptw (each page-table-walk read, by level) and --trace-tlb (adds and flushes). Output to --trace-output <file>.")
    (injection "--gdb-server-port <n> (GDB remote) and --rvfi-dii <port> (RVFI Direct Instruction Injection). --inst-limit bounds a run.")
    (matched_scope "The matched configuration is recorded in reference/sail-rv64gc-lab-v0.override.sexp and materialized to JSON at use: privileged 1.13, declared instruction selection, no devices/CLINT, Zicntr disabled, WFI a nop except in U, Svade selected, and medeleg 0xB3FF (the public validator's accepted subset measured at P4-SYSTEM.3). Nine finite experiments use the corpus's GPR change-observation rule. Historical results: privilege (.2 h part 2), 11/12 AGREE in the mode matrix; mm-wfi's TW cell differs under the matched nop policy and agrees over 30 steps under the public wait variant; mm-counters has no matched time source. Sv39 (.3 e part 2), 13 AGREE plus one recorded A/D-observation convention among 14, with identical delivered traps and the measured walk/TLB trace dimensions. Atomics (.4 f), 11 AGREE plus one named width-equal-SC policy difference among 12; the LR misalignment cause was repaired to load access-fault 5 before closure. Interrupt/wake (.5 d), six AGREE and six named platform differences among 12: the six software-posted-bit guests agree over 218 steps; timer and actual halted boundaries lack a counterpart in the matched configuration. Fence.i (.6 c), six AGREE over 29 steps, including changed instruction bytes after the guest's store. Floating point (.7 e1), 24 AGREE over 927 steps: encoding/state evidence and an additional numeric opinion, not independent numeric evidence (finite agreement does not authenticate implementation ancestry). Faults (.8 e), three AGREE (51+41+128 steps), seven named: the cycle read with Zicntr disabled and six injected-access guests whose refusal regions are absent from this public configuration. M (.11 c2), four AGREE over 99 steps; a deliberately wrong overflow quotient DIVERGEs. C (.12 e2d, 2026-10-09), 27 AGREE over 412 declared boundaries, all 37 compressed spellings present in actual Sail rows, each complete trace repeated byte-identically; includes reserved/FS-Off diagnostics, old-source pc+2 links and the required-second-parcel page fault. One named timer-platform difference: c-irq executes C.ADDI at boundary 9 where the laboratory delivers STI. scripts/probe_gc_sail_timer.py reproduces the public cause: stimecmp reads zero but mip.STIP reads zero twice, versus the laboratory's virtual-time-derived one; both fresh traces identical. Public validate-config rejects enabling Zicntr without a time source, and enabling CLINT in the existing memory map because no CLINT region is defined. No device is added to force agreement. A wrong C.LI expectation DIVERGEs at step 0 through a fresh public run. The tracked adapter compares complete declared GPR changes and witnessed delivery gaps, not unrecorded PCs, words, FP registers, memory, CSRs or request counts. All dependency integration relies on public contracts and outputs, never submodule implementation assumptions. An ISA string establishes instructions, not platform equivalence. P4.13 c28b corrects the scalar misaligned-atomicity granule exponent from 4 to 0: a contained AMO previously completed despite amo=AccessFault, while the old boundary-crossing witness still trapped. Public validation and 242 bare-M aligned/contained/crossing cases at W/D, with fresh repeated PC/word/GPR/CSR/data read-backs, qualify the corrected configuration; restoring exponent4 is a must-diverge control. The original twelve A guests retain eleven AGREE and the named width-SC difference. Before/after public traces are byte-identical over 164 successful old guests; three unchanged counter/timer process refusals earn no successful-comparison credit. P4.13 c28c repairs post-budget run-off refusals by requesting exactly the declared boundary count, retaining the strict whole-trace parser, and recognizing the historical word-less fetch spelling only with a real fetch-class event. The public runner now agrees over 149 enabled guests/4566 declared boundaries with fresh repeated traces; fourteen prior platform/policy differences and three process failures remain, and the disabled cross-model guest still refuses. These are finite GPR-change/delivery observations, not complete architectural equivalence. These corrective runs remain prose/live qualification, not the structured experiment records P4.14 must supply.")
    (terms "BSD-2-Clause (the sail-riscv model). Read and executed locally; no copy is committed and nothing is redistributed.")
    (lineage "Public configuration and trace observations identify this comparator's behavior for named inputs. Its implementation ancestry relative to other comparators is unexamined here. In this project's ACT campaign, signatures produced by the configured Sail run are the expected-result source; they add no second derivation against that producer."))
  (comment "───────────────────────────────────────────────────────────── candidate 2: Spike")
  (candidate
    (id "spike")
    (role "second implementation")
    (status "obtained")
    (kind "source build")
    (origin "https://github.com/riscv-software-src/riscv-isa-sim")
    (binary "target/refs/spike-build/spike")
    (binary_sha256 "8fdf43ac80ccafb96ab076c91967adf6df119b05c5b926ed49a033efe57836a3")
    (invocation "spike --isa=<isa> --priv=<modes> --log-commits --instructions=<n> <elf>")
    (trace_granularity "commit level: --log-commits prints the committed instruction with its register and memory writes; -l/--log gives an execution log; spike-dasm decodes it.")
    (injection "built-in interactive debug mode (-d) with register/memory read-write and single step; OpenOCD/GDB via --rbb-port.")
    (matched_scope "PLATFORM-CONFLICTED for this profile, recorded rather than worked around. Spike bundles a small board with its CPU — a core-local interruptor, a platform interrupt controller, a UART, an Sv57 MMU and 16 PMP regions — and offers no command-line route to remove them (the rv64i dossier's DIFF-PLATFORM-SPIKE, measured). This profile declares Sv39, no CLINT and no PMP (D-SV39, D-NO-PMP), so the conflict is worse than for rv64i, and no platform match is claimed.")
    (terms "BSD-3-Clause (Regents of the University of California). Built and executed locally; no copy is committed.")
    (lineage "Implementation ancestry relative to Sail and other comparators is unexamined here. The recorded public configuration, trace and decoder observations support only their named finite inputs and comparison rules; availability or agreement adds no independence credit."))
  (comment
  "──────────────────────────────────────────── the ENCODING source re-pin (P4-SYSTEM.2 slice a)"
  "The rv64i dossier pins the RV64I+M tables. This profile's definition fragments add"
  "Zicsr, Zicntr and the privileged system instructions, so the tables carrying them"
  "are pinned here, from the same upstream and through the same fetch route."
  "The pinned tables identify public encoding inputs; Sail/Spike implementation ancestry"
  "is unexamined. Finite decoding agreement supplies no independent encoding-lineage credit."
  "Measured at the re-pin (2026-10-03): upstream moved the instruction tables from the"
  "repository root to extensions/ — the moved rv_i/rv64_i/rv_m/rv64_m hash"
  "byte-identical to the rv64i dossier's pins, so the fetch route now maps table names"
  "under extensions/ and every existing pin still verifies. Zicntr's counter reads"
  "(rdcycle/rdtime/rdinstret) exist upstream ONLY as $pseudo_op rows of csrrs — they"
  "add nothing to the encoding space — and the pinned arg_lut.csv already carries the"
  "csr (31..20) and zimm5 (19..15) operand fields, so arg_lut.csv needs no re-pin; it"
  "is listed here because this profile's fragments derive those field positions from"
  "it (same bytes, same digest as the rv64i pin). csrs.csv supplies a public CSR"
  "name-to-address artifact; the normal assembler uses canonical state metadata."
  "encoding.h retains the historical field-mask artifact. Current mstatus positions"
  "follow published Machine Figure 7, with menvcfg.STCE in Figure 24; causes.csv supplies"
  "trap cause codes used by canonical semantics. rv_a/rv64_a (added at"
  " P4-SYSTEM.4 slice a, 2026-10-04, through the same extensions/ fetch route)"
  " carry the A extension's 22 forms — Zaamo's nine AMOs and Zalrsc's"
  " load-reserved/store-conditional pair, each .W and .D; the pinned RVWMO"
  " chapter's Tables 6/7 enumerate exactly this set, so the pin corroborates"
  " rather than surprises. The pinned arg_lut.csv already carries the aq"
  " (26..26) and rl (25..25) operand fields and the combined aqrl (26..25),"
  " so it needs no re-pin; the rows use no amoop operand token (the funct5"
  " is literal fixed bits in every row — measured). rv_zifencei (added at"
  " P4-SYSTEM.6 slice a, 2026-10-05, through the same extensions/ fetch route)"
  " carries Zifencei's single form — fence.i, the instruction-fetch"
  " synchronization instruction: one row, 73 bytes, funct3=1 against fence's 0"
  " inside the MISC-MEM opcode (the pinned Zifencei chapter, Version 2.0, is"
  " its own contract; the row's imm12/rs1/rd operand fields are the base's —"
  " decoded and ignored per the chapter's shall-ignore rule, never owned"
  " here). rv_f/rv64_f (added at P4-SYSTEM.7 slice c2, 2026-10-06, through"
  " the same extensions/ fetch route) carry the F extension's 30 forms —"
  " 26 rows in rv_f (the loads/stores, the four fused multiply-adds, the"
  " arithmetic, sign-injection, min/max, compares, fclass, the 32-bit"
  " conversions and the bit moves) and 4 in rv64_f (the 64-bit integer"
  " conversions) — plus 13 $pseudo_op rows (the two old fmv names, the"
  " fmv.s/fabs.s/fneg.s sign-injection spellings, the eight FP-CSR access"
  " aliases of Zicsr), which the fragment does NOT carry: they are"
  " spellings of real forms (the rv64i write-it-out policy), not forms the"
  " profile selects. The pinned arg_lut.csv already carries rs3 (31..27)"
  " and rm (14..12), so it needs no re-pin. rv_d/rv64_d (added at P4-SYSTEM.7"
  " slice d1, 2026-10-06, through the same route) carry the D extension's"
  " 32 forms — 26 rows in rv_d (FLD/FSD, the four fused multiply-adds, the"
  " arithmetic, sign injection, min/max, the two format conversions"
  " fcvt.s.d/fcvt.d.s, the compares, fclass and the 32-bit integer"
  " conversions) and 6 in rv64_d (the 64-bit integer conversions and the"
  " fmv.x.d/fmv.d.x bit moves) — plus 3 $pseudo_op rows (fmv.d/fabs.d/fneg.d,"
  " spellings of the sign-injection forms) the fragment does NOT carry; D"
  " reuses F's rs3/rm and owns no field."
)
  (encoding_source
    (id "RISCV-OPCODES")
    (origin "https://github.com/riscv/riscv-opcodes")
    (license "BSD-3-Clause (RISC-V International, 2022)")
    (retrieved "2026-10-03")
    (work_dir "target/refs/riscv-opcodes")
    (supplies "instruction fixed bits and operand lists for Zicsr (rv_zicsr: csrrw/csrrs/csrrc and their immediate forms), the Zicntr counter reads (rv_zicntr: rdcycle/rdtime/rdinstret as pinned pseudo-op rows of csrrs), the privileged system instructions (rv_system: mret, wfi; rv_s: sret, sfence.vma — RVP-INSNS 18.1), the A extension (rv_a: lr.w/sc.w and the nine amo*.w; rv64_a: the eleven .D forms), Zifencei (rv_zifencei: fence.i), the F extension (rv_f: the 26 RV32F forms; rv64_f: the four 64-bit integer conversions) and the D extension (rv_d: the 26 RV32D forms; rv64_d: the four 64-bit integer conversions and the two 64-bit bit moves); the csr and zimm5 operand field positions plus the aq/rl ordering-field positions and F's rs3/rm positions (arg_lut.csv); the CSR name-to-address map (csrs.csv); the CSR field masks (encoding.h — mstatus.TSR/TW/TVM/MPRV, the xIE/xPIE/xPP positions); and the trap cause codes (causes.csv).; the M multiply/divide forms (rv_m/rv64_m: the 13 instructions, re-pinned at P4-SYSTEM.11 slice b — the same bytes definitions/riscv/m.sexp names); the compressed forms at RV64 with D (rv_c 23 + rv64_c 10 = Zca, rv_c_d 4 = Zcd — the RV32-only rv32_c/rv32_c_f deliberately not pinned), re-pinned at P4-SYSTEM.12 slice a, fetched from upstream master and pinned by content: the bytes definitions/riscv/c.sexp names")
    (note "The hypervisor, Sm* and other pinned-but-unselected tables (D-NO-H, D-NO-PMP) are deliberately NOT in this pin: the fragment must carry only the profile's selection, and pinning a table nothing derives from would invite a reader to believe it is used. The selected tables carry no unselected instruction — measured row by row at the re-pin.")
    (file (name "rv_zicsr") (sha256 "dd8cc0e2c32fb5658d4aa719cef6ab1b714e2145ba071c9aeb382d9963e4901f") (bytes 940))
    (file (name "rv_zicntr") (sha256 "34ed6bb1cf98448c7c40abbd6f67cbccee0788bd42429a2b1a9538952f6cca8c") (bytes 298))
    (file (name "rv_system") (sha256 "4a58b5f0c908d7b748abbeb9df8335dbc53650ea284b738e4351afd49755e646") (bytes 141))
    (file (name "rv_s") (sha256 "e9d509a3a46de9024547fa75f76bf3c2839910ebc9af81d106cc46bc0ac6eb78") (bytes 132))
    (file (name "rv_a") (sha256 "d9eaa988c4779ca352d9da9eabacf6c71771d0b81e04b234302627f69e0863d9") (bytes 858))
    (file (name "rv64_a") (sha256 "819e0487131bc97cfc0b6f3de62390f2f9936b43e80aef7c6cec14fbe7c7a1b6") (bytes 885))
    (file (name "rv_zifencei") (sha256 "be2d8f7286e06fadafffbde14656e6adb3f923ce704ea0829229d3a3b5f35758") (bytes 73))
    (file (name "rv_f") (sha256 "227e09504c0d758add114d5a77ac06d7e2ffab9c6a9509633c4f531db58b3e3e") (bytes 3050))
    (file (name "rv64_f") (sha256 "5c01c243ccd8a1c0e24a48a1ffcf62eecb10aa36fd6bdcedf7392e670cd46cf9") (bytes 320))
    (file (name "rv_d") (sha256 "24bc7c6384f9a009dbafb3f177ec68b0d4f8fb1c2c2b7b07767320fdd7d4acbc") (bytes 2091))
    (file (name "rv64_d") (sha256 "883e668be4c536d0dfdb8c02bd1f3eb959801eb953f1fb7a4b4e5e623cbf19a9") (bytes 465))
    (file (name "rv_m") (sha256 "1a53ea03820b7044de4f0f04d207c1e4fc0ced46deb2c6ed4a3ca268fa37ddbe") (bytes 432))
    (file (name "rv64_m") (sha256 "112bf223a31b7cc51761ce1572a8a35c2502ab2c5a6e318db80c0601b587480e") (bytes 297))
    (file (name "rv_c") (sha256 "f97db59ffe15873bf4af8ab53694f703a90d582c2602ee876d8578824b1feda8") (bytes 1499))
    (file (name "rv64_c") (sha256 "1c51536f890d0ab1dec9b75980ef1e71ce03194eeb99f294c86d1b337807f284") (bytes 673))
    (file (name "rv_c_d") (sha256 "c52a9107d44ba9edb39d8fda880779f46cf648351cb9a666008ddbe8c1e0ca7a") (bytes 249))
    (file (name "csrs.csv") (sha256 "caf7f732356167cbc5a93eeb6b37ddbaf5c8483229b50ee7cb7a56bb6d29d493") (bytes 6101))
    (file (name "encoding.h") (sha256 "6ce1b7caafd51379ad1f775cbb59f978eda8cdae35bc19ffd0ee00482543d944") (bytes 22687))
    (file (name "causes.csv") (sha256 "237491f164e0818afcacb8853f665a97dedb585e21c64d784433b80ae870ee69") (bytes 554))
    (file (name "arg_lut.csv") (sha256 "cdc61339ffe379c0cd24ad2dc20e57deda95e1da663f94fccb5969d191a8e136") (bytes 1971))))
