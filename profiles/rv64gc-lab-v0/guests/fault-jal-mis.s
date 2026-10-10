# fault-jal-mis.s — historical basename; GC halfword-aligned JAL target.
#
# This mirror uses IALIGN=16. Target 0x80000006 is legal and JAL writes its
# pc+4 link (0x80000008) to x5. The two-boundary/four-parcel budget ends after
# the jump; it does not fetch the target. The base IALIGN=32 fault/no-link
# observation does not transfer to this profile.

      addi  x1, x0, 1          # ordinary first write
      jal   x5, 2              # legal halfword target 0x80000006; link is written
