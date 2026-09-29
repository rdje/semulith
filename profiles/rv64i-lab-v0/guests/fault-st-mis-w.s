# fault-st-mis-w.s — the P2-SCALAR.3 fault guest: a misaligned WORD store.
#
# The 4-byte store at 2 mod 4: cause 0x06, tval = 0x80000402, no store crossing (the
# alignment check precedes the boundary — the suppressed effect, SEM-06).

      addi  x10, x0, 1         # build the main-memory base 0x80000000 arithmetically
      slli  x10, x10, 31
      addi  x1, x0, 7          # the value that must never reach memory
      sw    x1, 1026, x10      # 0x80000402 — 2 mod 4: trap (0x06, 0x80000402), no store crossing
