# bound-arith.s — the P2-SCALAR.2 boundary guest for wrap/overflow arithmetic: the
# signed-extreme wraps modulo 2^64 (D-ALU-REG, overflow ignored, no trap), the same
# wraps through the immediate path (D-ALU-IMM), the *W 32-bit wraps whose result
# sign-extends from bit 31 while the operand's garbage upper half contributes nothing
# (D-WSUFFIX), the comparisons at the signed extremes, and the U-immediate sign edges
# (D-LUI-AUIPC), including auipc 0x80000 whose sign-extended offset wraps the address
# sum modulo 2^64 (D-ADDR-WRAP).
#
# No memory access — this guest is pure arithmetic. The sltu 0-result is pre-written
# with 1 so it lands as a visible 1->0 transition.

      addi x1, x0, -1               # build INT64_MAX = 0x7FFFFFFFFFFFFFFF …
      srli x1, x1, 1                # … 0x7FFFFFFFFFFFFFFF
      addi x2, x0, 1                # build INT64_MIN = 0x8000000000000000 …
      slli x2, x2, 63               # … 0x8000000000000000
      addi x4, x0, 1
      add x3, x1, x4                # ---- the wrap corners: modulo 2^64, overflow ignored ----
      sub x5, x2, x4
      add x6, x1, x1
      addi x7, x2, -1
      addi x8, x0, -2048            # ---- the immediate extremes ----
      addi x9, x0, 2047

      # ---- the *W wraps: the low 32 bits wrap, bit 31 of the result sign-extends,
      #      and the operand's garbage upper half must be IGNORED ----
      lui x10, 0xDEADB              # garbage upper half: 0xFFFFFFFFDEADB000 …
      addi x10, x10, 0x7EF          # … 0xFFFFFFFFDEADB7EF …
      slli x10, x10, 32             # … 0xDEADB7EF00000000 …
      addi x11, x0, -1              # … all ones …
      srli x11, x11, 33             # … 0x000000007FFFFFFF (low32 = INT32_MAX) …
      or x10, x10, x11              # … X10 = 0xDEADB7EF7FFFFFFF: garbage above, INT32_MAX below
      addiw x12, x10, 1             # low32 INT32_MAX + 1 wraps to INT32_MIN, sign-extended
      addiw x13, x2, -1             # low32 of INT64_MIN is 0; 0 - 1 wraps to all-ones
      addw x14, x10, x4             # the register path of the same wrap
      subw x15, x2, x4              # 0 - 1 in 32 bits
      subw x16, x4, x10             # 1 - INT32_MAX wraps negative in 32 bits

      # ---- comparisons at the signed extremes ----
      slt x17, x2, x1               # INT64_MIN < INT64_MAX, signed: 1
      addi x18, x0, 1               # pre-write: the unsigned answer below is 0
      sltu x18, x2, x1              # the SAME pair, unsigned: 0x8000… > 0x7FFF…, so 0
      sltu x19, x0, x2              # 0 < 0x8000000000000000, unsigned: 1
      slti x20, x2, -2048           # INT64_MIN < -2048, signed: 1
      sltiu x21, x0, -1             # 0 < 0xFFFF…, unsigned against the sign-extended immediate: 1

      # ---- the U-immediate sign edges (D-LUI-AUIPC) ----
      lui x22, 0x7FFFF              # the POSITIVE edge: bit 31 of the 32-bit value is CLEAR
      auipc x23, 0x80000            # pc + sext(0x80000000): wraps modulo 2^64 to exactly 4*n
      auipc x24, 0x7FFFF            # the positive edge: no wrap, plain addition
