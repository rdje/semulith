# fault-jalr-mis.s — historical basename; GC JALR retains target bit 1.
#
# D-JALR-LSB adds the immediate, then clears only bit 0: 3 becomes 2. Under
# this profile's IALIGN=16 that target is aligned, so JALR writes x5=0x80000008.
# The two-boundary/four-parcel budget ends on the jump without fetching address 2.
# Its register/fetch observations alone cannot distinguish a wrong target of 0;
# direct target-state witnesses are required before OB-JALR-LSB receives credit.

      addi  x1, x0, 3          # target material: both low bits set
      jalr  x5, x1, 0          # legal target 2; preserve bit 1 and write the link
