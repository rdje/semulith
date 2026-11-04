# it-prio-jump.s — historical base fault-priority name; GC target fetch fault.
#
# IALIGN=16 makes target 0x40000002 aligned. JALR first completes and writes
# x5=0x8000000c. The NEXT boundary attempts a parcel fetch at that unmapped
# target and delivers instruction-access-fault (cause 1, EPC/tval 0x40000002).
# Four boundaries/seven parcel requests include this refused target fetch.
# The base profile's IALIGN=32 misaligned-jump/no-link observation does not apply.

      lui   x1, 0x40000        # outside the laboratory memory region
      addi  x1, x1, 3          # odd sum becomes aligned target 0x40000002
      jalr  x5, x1, 0          # completes; the declared next boundary faults on fetch
