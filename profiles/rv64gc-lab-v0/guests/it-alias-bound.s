# it-alias-bound.s — the P2-SCALAR.4 interaction guest (alias × boundary): self-aliased
# operations at boundary values. Every operator below reads AND writes the same register
# (rd = rs1 = rs2 where the form allows), at operand values on a domain edge: the 32-bit
# addw wrap, a 6-bit shift-amount read of 65 (which is 1), the shamt-63 extreme, and the
# -1 signed boundary on slt and sub. The old value is therefore both INPUT and overwritten
# OUTPUT in one step — a model that samples the destination early or late gets a different
# answer, and every result is a VISIBLE change (the .1 lesson: a 0 into an already-zero
# register would leave no observation, so x9 is pre-written with 1).

      addi  x5, x0, -1       # x5 = -1
      addw  x5, x5, x5       # low 32: 0xFFFFFFFF + 0xFFFFFFFF wraps to 0xFFFFFFFE; sext -> -2
      addi  x6, x0, 65       # x6 = 65 — the value AND the shift amount
      srl   x6, x6, x6       # the 6-bit amount read sees 65 & 63 = 1: 65 >> 1 = 32
      addi  x7, x0, 63       # x7 = 63
      sll   x7, x7, x7       # shamt 63: 63 << 63 keeps only bit 0, shifted out to the top
      addi  x8, x0, -1       # x8 = -1 — the signed boundary
      addi  x9, x0, 1        # pre-written so the 0 result below is a visible change
      slt   x9, x8, x8       # rs1 == rs2 == -1: (-1 < -1) is false -> 0 (1 -> 0 is observed)
      sub   x8, x8, x8       # rd = rs1 = rs2 = -1: (-1) - (-1) = 0 (-1 -> 0 is observed)
