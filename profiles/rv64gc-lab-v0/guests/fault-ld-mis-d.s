# fault-ld-mis-d.s — the P2-SCALAR.3 fault guest: a misaligned DOUBLEWORD load.
#
# The 8-byte case at a 4-aligned-but-not-8 address: the alignment rule is per access
# width (D-MISALIGN-DATA), so 0x80000404 passes a 4-byte test and fails the 8-byte one.
# cause 0x04, tval = the effective address; x1 is never written.

      addi  x10, x0, 1         # build the main-memory base 0x80000000 arithmetically
      slli  x10, x10, 31
      ld    x1, x10, 1028      # 0x80000404 — 4-aligned, NOT 8-aligned: the width is the rule
