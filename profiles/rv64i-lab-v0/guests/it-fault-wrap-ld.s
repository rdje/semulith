# it-fault-wrap-ld.s — the P2-SCALAR.4 interaction guest (fault × boundary): the address
# computation wraps modulo 2^64 INTO the fault.
#
# The effective address is (rs1 + sext(imm)) mod 2^64 (D-ADDR-WRAP's rule, on the load path):
# 0xFFFFFFFFFFFFFFFC + 4 wraps to exactly 0, and address 0 belongs to no declared region, so
# the load raises a load-access-fault (cause 0x05) with tval = 0. Measured three-way by
# probe `wrap-ld` BEFORE this guest was authored: all three report cause 0x05, tval 0 —
# and 0 < 2^56, so DIFF-TVAL-PHYS-MASK (sail's 56-bit tval masking) cannot reach it. x2 is
# never written.

      addi  x1, x0, -4       # x1 = 0xFFFFFFFFFFFFFFFC
      ld    x2, x1, 4        # the address wraps to 0 — unmapped: access fault, tval 0
