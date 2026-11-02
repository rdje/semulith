# fault-jalr-mis.s — the P2-SCALAR.3 fault guest: a JALR whose target keeps bit 1 set.
#
# D-JALR-LSB clears only bit 0 of the target, so x1 = 3 yields 2 — still not 4-byte
# aligned under IALIGN=32, and the trap is raised ON THE JUMP (D-IALIGN,
# D-MISALIGN-REPORT) with tval = 2. The link write is suppressed exactly as for JAL
# (the DEFECT-B pin, `never_written x5`).

      addi  x1, x0, 3          # target material: 3 & ~1 = 2 — misaligned under IALIGN=32
      jalr  x5, x1, 0          # trap (0x00, 0x2) on the jump; x5 must never be written
