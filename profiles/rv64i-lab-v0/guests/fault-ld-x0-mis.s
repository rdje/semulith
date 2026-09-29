# fault-ld-x0-mis.s — the P2-SCALAR.3 fault guest: D-LOAD-X0 on the misaligned path.
#
# "Loads with a destination of x0 must still raise any exceptions" (D-LOAD-X0): the
# discarded value does not suppress the exception. A 4-byte load at 2 mod 4 into x0
# raises cause 0x04 exactly as if rd were an ordinary register — a model that skipped
# the access because the destination is x0 would retire the step instead.

      addi  x10, x0, 1         # build the main-memory base 0x80000000 arithmetically
      slli  x10, x10, 31
      lw    x0, x10, 1026      # 0x80000402 — misaligned; rd = x0 suppresses NOTHING
