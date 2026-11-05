# scope-alu.s — the P2-SCALAR.1 scope-completion guest: the RV64I logical, compare,
# shift and *W forms no tracked guest exercised yet, plus FENCE.
#
# Every instruction lands on a decision `profile.sexp` records (D-ALU-REG, D-ALU-IMM,
# D-SHAMT, D-WSUFFIX, D-FENCE), so a disagreement with a reference model lands on a
# decision rather than on "something differs". Operand values are built only from forms
# the earlier guests already cover (addi, lui, slli), and every result register is
# written exactly once, so the trace reads top to bottom.
#
# The register pairs are chosen to make the semantics visible: x1 is all-ones (-1, and
# the largest unsigned value), x4 has bit 63 and bit 31 set with the low 31 bits clear,
# and x5 = 32 is a shift amount whose low-5 and low-6 readings DIFFER — the D-SHAMT pin.

      addi  x1, x0, -1         # setup: -1 / 0xFFFFFFFFFFFFFFFF
      addi  x2, x0, 0x654      # setup: 0b0110_0101_0100
      addi  x3, x0, 0x470      # setup: 0b0100_0111_0000
      lui   x4, 0x80000        # setup: 0xFFFFFFFF80000000 (bit 63 AND bit 31 set)
      addi  x5, x0, 32         # setup: a 6-bit amount that a 5-bit read sees as 0

      and   x6, x2, x3         # D-ALU-REG: bitwise AND
      or    x7, x2, x3         # D-ALU-REG: bitwise OR
      xor   x8, x2, x3         # D-ALU-REG: bitwise XOR

      andi  x9, x4, -1         # D-ALU-IMM: the immediate sign-extends to all-ones
      ori   x10, x4, 0x7FF     # D-ALU-IMM: OR against the sign-extended immediate
      xori  x11, x4, -1        # D-ALU-IMM: XOR against all-ones inverts every bit

      slt   x12, x1, x2        # D-ALU-REG: -1 < 1620 signed → 1
      addi  x13, x0, 1         # pre-write: the laboratory records VISIBLE register changes,
      sltu  x13, x1, x2        # so the 0 below is only observable as a 1→0 transition —
                               # the same operands as SLT, unsigned: not less
      slti  x14, x4, 1         # D-ALU-IMM: a negative register compares below 1
      addi  x15, x0, 1         # pre-write, for the same reason
      sltiu x15, x4, 1         # the same comparison, unsigned: 0 written over the 1
      sltiu x16, x4, -1        # SLTIU sign-extends the immediate FIRST, then compares
                               # unsigned: a zero-extending reader answers 0 here

      sub   x17, x2, x3        # D-ALU-REG: subtract
      sub   x18, x3, x2        # the same pair reversed — the result wraps modulo 2^64

      sll   x19, x3, x2        # D-SHAMT: the amount is rs2's low 6 bits (0x654 → 20)
      srl   x20, x4, x2        # logical: zeros enter from the top
      sra   x21, x4, x2        # arithmetic: the sign bit replicates — same operands

      addw  x22, x4, x2        # D-WSUFFIX: low 32 added, bit 31 of the sum is set
      subw  x23, x4, x2        # low 32 subtracted, bit 31 of the difference is clear
      sllw  x24, x2, x5        # D-SHAMT: the *W shifts read rs2[4:0] — 32 reads as 0
      srlw  x25, x4, x2        # logical, on the low 32 bits only
      sraw  x26, x4, x2        # arithmetic, replicating bit 31 (not bit 63)

      srliw x27, x4, 31        # D-SHAMT: a 5-bit immediate amount on the low 32 bits
      sraiw x28, x4, 31        # arithmetic: bit 31 fills the word, then sign-extends

      fence 0, 15, 15, x0, x0  # D-FENCE: decoded, must not trap, no observable effect
