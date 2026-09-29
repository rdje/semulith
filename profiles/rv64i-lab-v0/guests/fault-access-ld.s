# fault-access-ld.s — the P2-SCALAR.3 fault guest: a load access fault, cross-model.
#
# D-ADDRESS-SPACE: an access outside every declared region raises an access-fault
# exception — cause 0x05, tval = the address. guest-no-device pins the same rule at
# 0x0200_BFF8, but that address is spike's built-in CLINT, so its spike comparison is
# disabled; 0x40000000 is no platform's device (outside sail's region AND spike's
# DRAM), so THIS guest carries the access-fault rule into the three-way comparison.
# x1 is never written.

      lui   x11, 0x40000       # x11 = 0x40000000: outside every region either platform declares
      ld    x1, x11, 0         # trap (0x05, 0x40000000); x1 must never be written
