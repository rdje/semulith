;; encoding.sexp — the instruction encodings this model OWNS.
;;
;; ⛔ DERIVED, TRACKED, AND GATED. Before this file existed the assembler read its encodings from
;; `target/refs/riscv-opcodes` — untracked and network-acquired — so a fresh clone could not build
;; a model at all, and the project's own rule (a constant that is a function of an external
;; document is derived or gated, never assumed present) was being broken by its own tooling.
;;
;; ⚠️ WHAT THIS FILE IS NOT. Encodings only: which bits name which instruction, and which fields
;; carry its operands. It says nothing about what an instruction MEANS — that is `semantics.sexp`,
;; and the two are separate because a decoder and an interpreter are separate generated artifacts.
;;
;; Regenerate with `scripts/gen_encoding.py <profile>`. Do not edit by hand.

(encoding
  (profile "rv64i-lab-v0")
  (ilen 32)
  (source
    (id "RISCV-OPCODES")
    (origin "https://github.com/riscv/riscv-opcodes")
    (license "BSD-3-Clause")
    (file (name "rv_i") (sha256 "146e297ddbe346f325d993aaf56d7006f1bfde39df584b888b221543def17b97"))
    (file (name "rv64_i") (sha256 "262cbd0884fe1383fcb7c42070cbc73e309d0452ff8d00b38452a4dee7cfa7f5"))
    (file (name "arg_lut.csv") (sha256 "cdc61339ffe379c0cd24ad2dc20e57deda95e1da663f94fccb5969d191a8e136"))
    (file (name "constants.py") (sha256 "101c5b8a4169a47f80ff6175a19339cf332eb09f3b09489df6ccabd40afe629b"))
    (note "Upstream of Spike and NOT of Sail: Spike generates its encoding.h from this table, while the Sail model hand-writes 59 files of encdec mappings and never references it. So Sail decoding bytes built from this file is an independent confirmation of the encoding; Spike doing so is not."))

  ;; ---- operand field positions, inclusive bit ranges ------------------------
  (field (name rd) (hi 11) (lo 7))
  (field (name rs1) (hi 19) (lo 15))
  (field (name rs2) (hi 24) (lo 20))
  (field (name imm12) (hi 31) (lo 20))
  (field (name imm20) (hi 31) (lo 12))
  (field (name shamtd) (hi 25) (lo 20))
  (field (name shamtw) (hi 24) (lo 20))
  (field (name imm12hi) (hi 31) (lo 25))
  (field (name imm12lo) (hi 11) (lo 7))
  (field (name jimm20) (hi 31) (lo 12))
  (field (name bimm12hi) (hi 31) (lo 25))
  (field (name bimm12lo) (hi 11) (lo 7))

  ;; ---- immediates SCATTERED across their field, most-significant piece first -
  ;; Read as: the field's top bits hold imm[hi:lo], then the next piece, and so on.
  ;; The pieces must total the field width, and the reader refuses a layout that
  ;; does not — a silently wrong immediate is a jump to the wrong address.
  (scatter (name bimm12hi) (hi 31) (lo 25) (pieces (12 12) (10 5)))
  (scatter (name bimm12lo) (hi 11) (lo 7) (pieces (4 1) (11 11)))
  (scatter (name jimm20) (hi 31) (lo 12) (pieces (20 20) (10 1) (11 11) (19 12)))

  ;; ---- the declared instruction scope: 52 mnemonics ----------
  (insn (name add) (fixed (31 25 0x0) (14 12 0x0) (6 2 0xc) (1 0 0x3)) (operands rd rs1 rs2) (from "rv_i"))
  (insn (name addi) (fixed (14 12 0x0) (6 2 0x4) (1 0 0x3)) (operands rd rs1 imm12) (from "rv_i"))
  (insn (name addiw) (fixed (14 12 0x0) (6 2 0x6) (1 0 0x3)) (operands rd rs1 imm12) (from "rv64_i"))
  (insn (name addw) (fixed (31 25 0x0) (14 12 0x0) (6 2 0xe) (1 0 0x3)) (operands rd rs1 rs2) (from "rv64_i"))
  (insn (name and) (fixed (31 25 0x0) (14 12 0x7) (6 2 0xc) (1 0 0x3)) (operands rd rs1 rs2) (from "rv_i"))
  (insn (name andi) (fixed (14 12 0x7) (6 2 0x4) (1 0 0x3)) (operands rd rs1 imm12) (from "rv_i"))
  (insn (name auipc) (fixed (6 2 0x5) (1 0 0x3)) (operands rd imm20) (from "rv_i"))
  (insn (name beq) (fixed (14 12 0x0) (6 2 0x18) (1 0 0x3)) (operands bimm12hi rs1 rs2 bimm12lo) (from "rv_i"))
  (insn (name bge) (fixed (14 12 0x5) (6 2 0x18) (1 0 0x3)) (operands bimm12hi rs1 rs2 bimm12lo) (from "rv_i"))
  (insn (name bgeu) (fixed (14 12 0x7) (6 2 0x18) (1 0 0x3)) (operands bimm12hi rs1 rs2 bimm12lo) (from "rv_i"))
  (insn (name blt) (fixed (14 12 0x4) (6 2 0x18) (1 0 0x3)) (operands bimm12hi rs1 rs2 bimm12lo) (from "rv_i"))
  (insn (name bltu) (fixed (14 12 0x6) (6 2 0x18) (1 0 0x3)) (operands bimm12hi rs1 rs2 bimm12lo) (from "rv_i"))
  (insn (name bne) (fixed (14 12 0x1) (6 2 0x18) (1 0 0x3)) (operands bimm12hi rs1 rs2 bimm12lo) (from "rv_i"))
  (insn (name ebreak) (fixed (31 20 0x1) (19 7 0x0) (6 2 0x1c) (1 0 0x3)) (operands ) (from "rv_i"))
  (insn (name ecall) (fixed (31 20 0x0) (19 7 0x0) (6 2 0x1c) (1 0 0x3)) (operands ) (from "rv_i"))
  (insn (name fence) (fixed (14 12 0x0) (6 2 0x3) (1 0 0x3)) (operands fm pred succ rs1 rd) (from "rv_i"))
  (insn (name jal) (fixed (6 2 0x1b) (1 0 0x3)) (operands rd jimm20) (from "rv_i"))
  (insn (name jalr) (fixed (14 12 0x0) (6 2 0x19) (1 0 0x3)) (operands rd rs1 imm12) (from "rv_i"))
  (insn (name lb) (fixed (14 12 0x0) (6 2 0x0) (1 0 0x3)) (operands rd rs1 imm12) (from "rv_i"))
  (insn (name lbu) (fixed (14 12 0x4) (6 2 0x0) (1 0 0x3)) (operands rd rs1 imm12) (from "rv_i"))
  (insn (name ld) (fixed (14 12 0x3) (6 2 0x0) (1 0 0x3)) (operands rd rs1 imm12) (from "rv64_i"))
  (insn (name lh) (fixed (14 12 0x1) (6 2 0x0) (1 0 0x3)) (operands rd rs1 imm12) (from "rv_i"))
  (insn (name lhu) (fixed (14 12 0x5) (6 2 0x0) (1 0 0x3)) (operands rd rs1 imm12) (from "rv_i"))
  (insn (name lui) (fixed (6 2 0xd) (1 0 0x3)) (operands rd imm20) (from "rv_i"))
  (insn (name lw) (fixed (14 12 0x2) (6 2 0x0) (1 0 0x3)) (operands rd rs1 imm12) (from "rv_i"))
  (insn (name lwu) (fixed (14 12 0x6) (6 2 0x0) (1 0 0x3)) (operands rd rs1 imm12) (from "rv64_i"))
  (insn (name or) (fixed (31 25 0x0) (14 12 0x6) (6 2 0xc) (1 0 0x3)) (operands rd rs1 rs2) (from "rv_i"))
  (insn (name ori) (fixed (14 12 0x6) (6 2 0x4) (1 0 0x3)) (operands rd rs1 imm12) (from "rv_i"))
  (insn (name sb) (fixed (14 12 0x0) (6 2 0x8) (1 0 0x3)) (operands imm12hi rs1 rs2 imm12lo) (from "rv_i"))
  (insn (name sd) (fixed (14 12 0x3) (6 2 0x8) (1 0 0x3)) (operands imm12hi rs1 rs2 imm12lo) (from "rv64_i"))
  (insn (name sh) (fixed (14 12 0x1) (6 2 0x8) (1 0 0x3)) (operands imm12hi rs1 rs2 imm12lo) (from "rv_i"))
  (insn (name sll) (fixed (31 25 0x0) (14 12 0x1) (6 2 0xc) (1 0 0x3)) (operands rd rs1 rs2) (from "rv_i"))
  (insn (name slli) (fixed (31 26 0x0) (14 12 0x1) (6 2 0x4) (1 0 0x3)) (operands rd rs1 shamtd) (from "rv64_i"))
  (insn (name slliw) (fixed (31 25 0x0) (14 12 0x1) (6 2 0x6) (1 0 0x3)) (operands rd rs1 shamtw) (from "rv64_i"))
  (insn (name sllw) (fixed (31 25 0x0) (14 12 0x1) (6 2 0xe) (1 0 0x3)) (operands rd rs1 rs2) (from "rv64_i"))
  (insn (name slt) (fixed (31 25 0x0) (14 12 0x2) (6 2 0xc) (1 0 0x3)) (operands rd rs1 rs2) (from "rv_i"))
  (insn (name slti) (fixed (14 12 0x2) (6 2 0x4) (1 0 0x3)) (operands rd rs1 imm12) (from "rv_i"))
  (insn (name sltiu) (fixed (14 12 0x3) (6 2 0x4) (1 0 0x3)) (operands rd rs1 imm12) (from "rv_i"))
  (insn (name sltu) (fixed (31 25 0x0) (14 12 0x3) (6 2 0xc) (1 0 0x3)) (operands rd rs1 rs2) (from "rv_i"))
  (insn (name sra) (fixed (31 25 0x20) (14 12 0x5) (6 2 0xc) (1 0 0x3)) (operands rd rs1 rs2) (from "rv_i"))
  (insn (name srai) (fixed (31 26 0x10) (14 12 0x5) (6 2 0x4) (1 0 0x3)) (operands rd rs1 shamtd) (from "rv64_i"))
  (insn (name sraiw) (fixed (31 25 0x20) (14 12 0x5) (6 2 0x6) (1 0 0x3)) (operands rd rs1 shamtw) (from "rv64_i"))
  (insn (name sraw) (fixed (31 25 0x20) (14 12 0x5) (6 2 0xe) (1 0 0x3)) (operands rd rs1 rs2) (from "rv64_i"))
  (insn (name srl) (fixed (31 25 0x0) (14 12 0x5) (6 2 0xc) (1 0 0x3)) (operands rd rs1 rs2) (from "rv_i"))
  (insn (name srli) (fixed (31 26 0x0) (14 12 0x5) (6 2 0x4) (1 0 0x3)) (operands rd rs1 shamtd) (from "rv64_i"))
  (insn (name srliw) (fixed (31 25 0x0) (14 12 0x5) (6 2 0x6) (1 0 0x3)) (operands rd rs1 shamtw) (from "rv64_i"))
  (insn (name srlw) (fixed (31 25 0x0) (14 12 0x5) (6 2 0xe) (1 0 0x3)) (operands rd rs1 rs2) (from "rv64_i"))
  (insn (name sub) (fixed (31 25 0x20) (14 12 0x0) (6 2 0xc) (1 0 0x3)) (operands rd rs1 rs2) (from "rv_i"))
  (insn (name subw) (fixed (31 25 0x20) (14 12 0x0) (6 2 0xe) (1 0 0x3)) (operands rd rs1 rs2) (from "rv64_i"))
  (insn (name sw) (fixed (14 12 0x2) (6 2 0x8) (1 0 0x3)) (operands imm12hi rs1 rs2 imm12lo) (from "rv_i"))
  (insn (name xor) (fixed (31 25 0x0) (14 12 0x4) (6 2 0xc) (1 0 0x3)) (operands rd rs1 rs2) (from "rv_i"))
  (insn (name xori) (fixed (14 12 0x4) (6 2 0x4) (1 0 0x3)) (operands rd rs1 imm12) (from "rv_i"))
)
