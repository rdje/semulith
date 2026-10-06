;; references.sexp — the reference candidate dossier for `rv64gc-lab-v0` (P4-SYSTEM.2,
;; slice a: the encoding-source re-pin). One document form; validate with
;;   python3 scripts/check_sexp_schema.py profiles/rv64gc-lab-v0/references.sexp schema/references.sexp
;; Re-derive with `scripts/fetch_references.sh [--verify-only] rv64gc-lab-v0` — it needs the
;; network, so it is deliberately NOT a commit gate (the same reasoning as fetch_sources.sh).

(comment "profiles/rv64gc-lab-v0/references.sexp — the reference candidate dossier for"
         "`rv64gc-lab-v0`. This unit is at the profile-resolution stage: the dossier exists"
         "today because the definition fragments of P4-SYSTEM.2 slice (a) derive from encoding"
         "tables that must be pinned before they are derived from — a fragment generated from"
         "an unpinned source would be a model built on something nobody can re-derive (the"
         "rv64i dossier's own rule). The matched-profile EXPERIMENT records arrive with the"
         "privilege leaf's evidence slices; nothing here claims a reference is usable"
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
    (matched_scope "The matched configuration IS recorded (reference/sail-rv64gc-lab-v0.override.sexp, materialized to JSON at use): privileged 1.13, the declared selection, no devices, WFI a nop except in U, Svade selected (Svadu not), medeleg 0xB3FF (the laboratory's WARL-any causes restricted to what release 0.14 accepts — it names 10 and 14 reserved and rejects 17-20 wholesale, measured by bisection at P4-SYSTEM.3 slice (e) part 2). Five experiments measured against it: the atomics corpus (P4-SYSTEM.4 slice (f) — 11 AGREE + 1 NAMED DIVERGENCE of 12 on the corpus's change-observation rule; the one divergence: the laboratory's declared width-equal SC policy fails a .D SC after a .W LR while sail's platform reservation matches on the physical ADDRESS alone — both legal under §12.1.2's latitude; the same experiment caught and fixed at root the bind-day misaligned policy: LR takes the LOAD access-fault cause 5, the exception table's kind mapping, never 7), the mode-matrix corpus (P4-SYSTEM.2 slice h part 2 — 11/12 AGREE, mm-wfi's TW cell a named sail-side gap routed to .5, mm-counters not matchable — the CLINT time-source wall) and the sv39 corpus (P4-SYSTEM.3 slice (e) part 2 — 13 AGREE + 1 AGREE-RECORDED of 14 on three explicit dimensions: the architecture, the page-table walks read-for-read, and the TLB add/flush counts; the one convention recorded: sail judges A/D after the walk, the laboratory at step 9, the delivered trap identical). the interrupt and wake corpus (P4-SYSTEM.5 slice (d) — 6 AGREE + 6 NAMED of 12 on the same rule: the software-posted-bit acceptance/delegation/priority cells match exactly (218 steps across i-accept/i-deleg/i-enable/i-nest/i-vector/w-sw, with sail numbering the interrupt-delivery step and printing no row — the same convention the laboratory declares); the six named are all platform-shaped, never semantic: sail's timer block gates on plat_have_clint so STIP never sets without a CLINT (i-prio step 24, i-timer step 3), sail's wfi is a nop under the matched platform so the laboratory's real halt has no counterpart (the four `<halted>`-step guests), and mm-wfi's TW cell is the named gap freshly measured — probe-tw DIVERGES under the matched config (sail never judges TW: the judgment lives only in the wait-exit path the nop config never reaches) and AGREEs 30/30 under the wfi-wait variant with the delivered trap identical (cause 2, mepc = the wfi's pc, xtval = the wfi's word). the fence.i surface (P4-SYSTEM.6 slice (c) — 6 AGREE of 6 on the same rule: the fencei guests and the standing rewrite fixtures (it-fencei 3, min-fencei 1, fencei-reserved 2, fencei-selfmod 8, fault-selfmod 7, dir-selfmod-fence 8 — 29 steps' change-observations exact): sail's FENCEI is 'a nop for the memory model' with its fields decoded-not-fixed (the shall-ignore sentence quoted in zifencei_insts.sail's own comment), so the designed AGREE measured true on every cell, the patched fetch reads the new value on both sides, and the file stays difference-free. Verdict-neutrality: the .4 corpus re-run under the freshly materialized override reproduces 11 AGREE + 1 NAMED of 12 exactly). An ISA string establishes the instruction set and nothing else (the rv64i dossier's DIFF-PLATFORM-DEFAULT lesson).")
    (terms "BSD-2-Clause (the sail-riscv model). Read and executed locally; no copy is committed and nothing is redistributed.")
    (lineage "The Sail RISC-V model is the RISC-V International reference formal model, written in the Sail ISA description language. Any tool that DERIVES expected results from it shares an ancestor with it. It vendors Berkeley SoftFloat — for this profile's F/D scope a Sail-versus-Spike floating-point comparison is one implementation twice (the shared-ancestry measurement in the rv64i dossier, routed to P4-SYSTEM.7)."))
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
    (lineage "An independently written C++ interpreter, historically the RISC-V golden model and older than the Sail model. Independence from Sail is PLAUSIBLE and NOT established; it also vendors Berkeley SoftFloat (the shared-ancestry measurement routed to P4-SYSTEM.7)."))
  (comment "──────────────────────────────────────────── the ENCODING source re-pin (P4-SYSTEM.2 slice a)"
           "The rv64i dossier pins the RV64I+M tables. This profile's definition fragments add"
           "Zicsr, Zicntr and the privileged system instructions, so the tables carrying them"
           "are pinned here, from the same upstream and through the same fetch route."
           "⚠️ SHARED ANCESTRY, stated (unchanged in kind): this source is upstream of SPIKE and"
           "NOT of SAIL, so Sail decoding our bytes as intended is an independent confirmation"
           "of the encoding and Spike doing so is not."
           "Measured at the re-pin (2026-10-03): upstream moved the instruction tables from the"
           "repository root to extensions/ — the moved rv_i/rv64_i/rv_m/rv64_m hash"
           "byte-identical to the rv64i dossier's pins, so the fetch route now maps table names"
           "under extensions/ and every existing pin still verifies. Zicntr's counter reads"
           "(rdcycle/rdtime/rdinstret) exist upstream ONLY as $pseudo_op rows of csrrs — they"
           "add nothing to the encoding space — and the pinned arg_lut.csv already carries the"
           "csr (31..20) and zimm5 (19..15) operand fields, so arg_lut.csv needs no re-pin; it"
           "is listed here because this profile's fragments derive those field positions from"
           "it (same bytes, same digest as the rv64i pin). csrs.csv supplies the CSR"
           "name-to-address map the assembler resolves csr operands through. encoding.h"
           "(added at P4-SYSTEM.2 slice b) supplies the CSR FIELD masks — mstatus.TSR/TW/TVM/"
           "MPRV and the xIE/xPIE/xPP stack positions — which the pinned specification, again,"
           "renders only as figure images; causes.csv (in the cache since the rv64i era but"
           "never pinned — measured byte-identical to upstream at this re-pin) supplies the"
           "trap cause codes the trap-delivery semantics name. rv_a/rv64_a (added at"
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
           " reuses F's rs3/rm and owns no field.")
  (encoding_source
    (id "RISCV-OPCODES")
    (origin "https://github.com/riscv/riscv-opcodes")
    (license "BSD-3-Clause (RISC-V International, 2022)")
    (retrieved "2026-10-03")
    (work_dir "target/refs/riscv-opcodes")
    (supplies "instruction fixed bits and operand lists for Zicsr (rv_zicsr: csrrw/csrrs/csrrc and their immediate forms), the Zicntr counter reads (rv_zicntr: rdcycle/rdtime/rdinstret as pinned pseudo-op rows of csrrs), the privileged system instructions (rv_system: mret, wfi; rv_s: sret, sfence.vma — RVP-INSNS 18.1), the A extension (rv_a: lr.w/sc.w and the nine amo*.w; rv64_a: the eleven .D forms), Zifencei (rv_zifencei: fence.i), the F extension (rv_f: the 26 RV32F forms; rv64_f: the four 64-bit integer conversions) and the D extension (rv_d: the 26 RV32D forms; rv64_d: the four 64-bit integer conversions and the two 64-bit bit moves); the csr and zimm5 operand field positions plus the aq/rl ordering-field positions and F's rs3/rm positions (arg_lut.csv); the CSR name-to-address map (csrs.csv); the CSR field masks (encoding.h — mstatus.TSR/TW/TVM/MPRV, the xIE/xPIE/xPP positions); and the trap cause codes (causes.csv).")
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
    (file (name "csrs.csv") (sha256 "caf7f732356167cbc5a93eeb6b37ddbaf5c8483229b50ee7cb7a56bb6d29d493") (bytes 6101))
    (file (name "encoding.h") (sha256 "6ce1b7caafd51379ad1f775cbb59f978eda8cdae35bc19ffd0ee00482543d944") (bytes 22687))
    (file (name "causes.csv") (sha256 "237491f164e0818afcacb8853f665a97dedb585e21c64d784433b80ae870ee69") (bytes 554))
    (file (name "arg_lut.csv") (sha256 "cdc61339ffe379c0cd24ad2dc20e57deda95e1da663f94fccb5969d191a8e136") (bytes 1971))))
