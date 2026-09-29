# fault-access-sd.s — the P2-SCALAR.3 fault guest: a store access fault, cross-model.
#
# D-ADDRESS-SPACE on the store side: cause 0x07, tval = the address. The fault is
# answered AT the boundary: the environment refuses the request and no memory changes
# (there is no memory there), and the store's value vanishes with the trap — a failing
# access modifies nothing (SEM-06, catalog C11).

      lui   x11, 0x40000       # x11 = 0x40000000: outside every region either platform declares
      addi  x1, x0, 9          # the value that must never reach memory
      sd    x1, 0, x11         # trap (0x07, 0x40000000); nothing is modified
