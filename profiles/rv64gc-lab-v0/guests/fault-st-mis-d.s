# fault-st-mis-d.s — the P2-SCALAR.3 fault guest: a misaligned DOUBLEWORD store.
#
# The 8-byte store at 4 mod 8: cause 0x06, tval = 0x80000404, no store crossing. With
# fault-ld-mis-d this pins the width rule on both sides: 4-aligned is not 8-aligned.

      addi  x10, x0, 1         # build the main-memory base 0x80000000 arithmetically
      slli  x10, x10, 31
      addi  x1, x0, 7          # the value that must never reach memory
      sd    x1, 1028, x10      # 0x80000404 — 4-aligned, NOT 8-aligned: trap (0x06, 0x80000404)
