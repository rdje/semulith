# fault-st-mis-h.s — the P2-SCALAR.3 fault guest: a misaligned HALFWORD store.
#
# D-MISALIGN-DATA on the store side: cause 0x06, tval = the effective address. ⭐ The
# suppressed effect (SEM-06): the store is judged BEFORE the boundary is crossed, so no
# store request ever reaches the environment — the offline gate's crossing log proves
# the absence, which a final-state check could not distinguish from a serviced store.

      addi  x10, x0, 1         # build the main-memory base 0x80000000 arithmetically
      slli  x10, x10, 31
      addi  x1, x0, 7          # the value that must never reach memory
      sh    x1, 1025, x10      # 0x80000401 — odd: trap (0x06, 0x80000401), no store crossing
