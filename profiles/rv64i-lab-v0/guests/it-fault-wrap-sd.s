# it-fault-wrap-sd.s — the P2-SCALAR.4 interaction guest (fault × boundary): the wrapped
# store. This is the DIFF-TVAL-PHYS-MASK redesign: the probe measured `sd` at the TOP of the
# address space (0xFFFFFFFFFFFFFFF8), where sail-riscv 0.14 masks the access-fault tval to
# its 56-bit physical-address width while spike and semulith report the full address — a
# reference-vs-reference difference, recorded in references.sexp. So the guest wraps the
# address to exactly 0 instead: below 2^56, the tval is exact on all three models.
#
# 0xFFFFFFFFFFFFFFF8 + 8 wraps modulo 2^64 to 0 (D-ADDR-WRAP, on the store path); no region
# covers address 0, so the store raises a store-access-fault (cause 0x07) with tval = 0 and
# modifies NOTHING (SEM-06: the boundary refuses the request; the crossing is recorded and
# answered AccessFault, which the mutation suite's census pins).

      addi  x1, x0, -8       # x1 = 0xFFFFFFFFFFFFFFF8
      addi  x2, x0, 7        # the store data
      sd    x2, 8, x1        # the address wraps to 0 — unmapped: access fault, tval 0
