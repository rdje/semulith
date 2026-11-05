# fault-shiftw-res.s — the P2-SCALAR.3 reserved-encoding guest: the OQ-2 closure.
#
# D-SHIFTW-RESERVED: SLLIW/SRLIW/SRAIW encodings with imm[5] != 0 are RESERVED. The
# word below is `slliw x2, x1, 1` with bit 25 set — the *IW funct7 field is mask-pinned
# in the generated table, so the word decodes to nothing and the laboratory policy
# (D-RESERVED-DECODE) raises illegal-instruction. ⭐ OQ-2, measured (P2-SCALAR.3):
# sail-riscv 0.14 AND spike 1.1.1-dev BOTH raise illegal-instruction with tval = the
# word — the previous spec text's behavior — so all three observations agree while the
# model keeps the case's source classification. x2 is never written.

      addi  x1, x0, 7          # the operand the reserved form would have shifted
      .word 0x0210911B         # slliw x2, x1, 1 with imm[5] = 1 — RESERVED (D-SHIFTW-RESERVED)
