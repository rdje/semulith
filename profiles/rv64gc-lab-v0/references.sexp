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
    (trace_granularity "per instruction, and per effect within it: --trace-instr, --trace-gpr, --trace-csr, --trace-mem, --trace-exception, --trace-interrupt, --trace-pma, --trace-pmp, --trace-step. Output to --trace-output <file>.")
    (injection "--gdb-server-port <n> (GDB remote) and --rvfi-dii <port> (RVFI Direct Instruction Injection). --inst-limit bounds a run.")
    (matched_scope "No matched configuration is recorded for THIS profile yet. Release 0.14 exposes the full extension/privileged config namespace (the rv64i dossier's matched override is the precedent), and the privileged matched experiment is P4-SYSTEM.2 slice h's ATTEMPT, not a foregone result: if it fails, the affected axes read incomplete, never passed. An ISA string establishes the instruction set and nothing else (the rv64i dossier's DIFF-PLATFORM-DEFAULT lesson).")
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
           "trap cause codes the trap-delivery semantics name.")
  (encoding_source
    (id "RISCV-OPCODES")
    (origin "https://github.com/riscv/riscv-opcodes")
    (license "BSD-3-Clause (RISC-V International, 2022)")
    (retrieved "2026-10-03")
    (work_dir "target/refs/riscv-opcodes")
    (supplies "instruction fixed bits and operand lists for Zicsr (rv_zicsr: csrrw/csrrs/csrrc and their immediate forms), the Zicntr counter reads (rv_zicntr: rdcycle/rdtime/rdinstret as pinned pseudo-op rows of csrrs) and the privileged system instructions (rv_system: mret, wfi; rv_s: sret, sfence.vma — RVP-INSNS 18.1); the csr and zimm5 operand field positions (arg_lut.csv); the CSR name-to-address map (csrs.csv); the CSR field masks (encoding.h — mstatus.TSR/TW/TVM/MPRV, the xIE/xPIE/xPP positions); and the trap cause codes (causes.csv).")
    (note "The hypervisor, Sm* and other pinned-but-unselected tables (D-NO-H, D-NO-PMP) are deliberately NOT in this pin: the fragment must carry only the profile's selection, and pinning a table nothing derives from would invite a reader to believe it is used. The selected tables carry no unselected instruction — measured row by row at the re-pin.")
    (file (name "rv_zicsr") (sha256 "dd8cc0e2c32fb5658d4aa719cef6ab1b714e2145ba071c9aeb382d9963e4901f") (bytes 940))
    (file (name "rv_zicntr") (sha256 "34ed6bb1cf98448c7c40abbd6f67cbccee0788bd42429a2b1a9538952f6cca8c") (bytes 298))
    (file (name "rv_system") (sha256 "4a58b5f0c908d7b748abbeb9df8335dbc53650ea284b738e4351afd49755e646") (bytes 141))
    (file (name "rv_s") (sha256 "e9d509a3a46de9024547fa75f76bf3c2839910ebc9af81d106cc46bc0ac6eb78") (bytes 132))
    (file (name "csrs.csv") (sha256 "caf7f732356167cbc5a93eeb6b37ddbaf5c8483229b50ee7cb7a56bb6d29d493") (bytes 6101))
    (file (name "encoding.h") (sha256 "6ce1b7caafd51379ad1f775cbb59f978eda8cdae35bc19ffd0ee00482543d944") (bytes 22687))
    (file (name "causes.csv") (sha256 "237491f164e0818afcacb8853f665a97dedb585e21c64d784433b80ae870ee69") (bytes 554))
    (file (name "arg_lut.csv") (sha256 "cdc61339ffe379c0cd24ad2dc20e57deda95e1da663f94fccb5969d191a8e136") (bytes 1971))))
