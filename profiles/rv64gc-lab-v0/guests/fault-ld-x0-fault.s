# fault-ld-x0-fault.s — the P2-SCALAR.3 fault guest: D-LOAD-X0 on the access-fault path.
#
# The same rule one failure mode over: a load into x0 from an address outside every
# declared region still raises the access fault (cause 0x05, tval = the address).
# 0x40000000 is outside BOTH reference platforms' maps, so the comparison runs
# cross-model — and the discarded destination changes nothing (D-LOAD-X0).

      lui   x11, 0x40000       # x11 = 0x40000000: outside every region either platform declares
      ld    x0, x11, 0         # access fault; rd = x0 suppresses NOTHING
