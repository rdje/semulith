# fault-ld-mis-h.s — the P2-SCALAR.3 fault guest: a misaligned HALFWORD load.
#
# D-MISALIGN-DATA: the access raises address-misaligned (cause 0x04), delivered as a
# contained trap reported to the harness; it is NOT handled invisibly. smoke-trap pins
# the 4-byte case; this is the 2-byte case at an odd address. x1 is never written — the
# negative observation a silently-serviced load would fail.

      addi  x10, x0, 1         # build the main-memory base 0x80000000 arithmetically
      slli  x10, x10, 31
      lh    x1, x10, 1025      # 0x80000401 — odd: not 2-byte aligned. The base itself is
                               # provably fine (the slli retired), so the fault is the misalignment
