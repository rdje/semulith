# it-prio-load.s — the P2-SCALAR.4 interaction guest (fault × fault): trap priority on a load.
#
# D-MISALIGN-DATA vs D-ADDRESS-SPACE: a data access that is BOTH misaligned AND unmapped
# raises load-address-misaligned (cause 0x04), tval = the address — the misalignment is
# judged BEFORE the boundary is crossed, so no crossing exists and the unmapped-ness of the
# address never gets to answer. Measured three-way by probe `prio-load` BEFORE this guest
# was authored: all three raise 0x04 with tval 0x40000001, and x2 is never written.

      lui   x1, 0x40000      # x1 = 0x40000000 — outside every region either platform declares
      addi  x1, x1, 1        # x1 = 0x40000001 — 1 mod 4, so a 4-byte load there is misaligned
      lw    x2, x1, 0        # misaligned AND unmapped: the misaligned-load cause wins
