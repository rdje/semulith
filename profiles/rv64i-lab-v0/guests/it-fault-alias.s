# it-fault-alias.s — the P2-SCALAR.4 interaction guest (fault × alias): a misaligned load
# over its OWN base register.
#
# rd == rs1 on a load that faults: the address is sampled from the base BEFORE any write
# commits, and a trapping instruction retires no write at all — so the base register is
# PRESERVED through the fault. Measured three-way by probe `alias-fault` BEFORE this guest
# was authored: all three raise misaligned-load (0x04) with tval = the computed address and
# x5 keeps the value the lui gave it (the trap step writes nothing).

      lui   x5, 0x80000      # x5 = 0xFFFFFFFF80000000 (the U-immediate sign-extends)
      lw    x5, x5, 1        # 0xFFFFFFFF80000001 — misaligned; rd == rs1: the base survives
