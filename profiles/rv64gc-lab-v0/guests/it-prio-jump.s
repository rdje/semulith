# it-prio-jump.s — the P2-SCALAR.4 interaction guest (fault × fault): trap priority on a jump.
#
# D-IALIGN + D-MISALIGN-REPORT vs D-ADDRESS-SPACE: a jump target that is BOTH misaligned
# AND unmapped raises instruction-address-misaligned (cause 0x00) ON THE JUMP, tval = the
# target value — the alignment of the target is judged before any fetch is attempted there.
# Measured three-way (sail-riscv 0.14, spike 1.1.1-dev, semulith) by probe `prio-jump`
# BEFORE this guest was authored: all three raise 0x00 with tval 0x40000002, and the link
# write is suppressed (an instruction that raises a synchronous exception retires no
# architectural write — the DEFECT-B rule), so x5 must NEVER be written.

      lui   x1, 0x40000      # x1 = 0x40000000 — outside every region either platform declares
      addi  x1, x1, 3        # x1 = 0x40000003; JALR clears bit 0, so the target is 0x40000002
      jalr  x5, x1, 0        # misaligned AND unmapped: the misaligned-fetch cause wins
