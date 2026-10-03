# fault-hints.s — the P2-SCALAR.3 suppressed-effect guest: the RV64I HINT table.
#
# D-HINTS: every code point in the RV64I HINT table executes as a no-op that writes
# nothing to x0's architectural value, and a HINT must not trap (RVI-RV64I §3.1.4,
# Table 1). Each form below targets x0, so the write is architecturally discarded; the
# observation is that the run CONTINUES — a HINT that trapped would end the trace —
# and the landing addi proves the whole table retired. The semihosting markers
# (slli/srai x0, x0, …) are deliberately excluded: spike implements semihosting off a
# specific three-instruction sequence, and a lone marker near a trap is a fragile probe.

      addi  x1, x0, 5          # the HINTs' operand, and liveness
      lui   x0, 0x7FFFF        # HINT (rd = x0): nop
      auipc x0, 0x12345        # HINT (rd = x0): nop
      addi  x0, x1, 1          # HINT (rd = x0, rs1 != x0): nop
      addiw x0, x1, 2          # HINT (rd = x0): nop
      addw  x0, x1, x1         # HINT (rd = x0): nop
      sllw  x0, x1, x1         # HINT (rd = x0): nop
      sub   x0, x1, x1         # HINT (rd = x0): nop
      add   x0, x0, x2         # the NTL.P1 code point (rd = rs1 = x0, rs2 = x2): nop
      addi  x3, x0, 3          # landing: the whole table retired
