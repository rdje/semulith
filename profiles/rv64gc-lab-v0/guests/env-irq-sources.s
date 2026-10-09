# P4-SYSTEM.13 c13a1: fresh spec-side parcel derivation, 13 boundaries.
# With STCE enabled, M-source bits stay zero, SSIP/SEIP are software writable, and STIP follows the comparator.
# Enable menvcfg.STCE in M. RV64 LUI sign extension sets bit 63; other bits are WPRI.
lui x31, 0x80000
csrrs x0, menvcfg, x31
#|never: x28, x29
addi x6, x0, 1
addi x8, x0, 1
addi x5, x0, -1
csrrw x0, stimecmp, x5
csrrs x6, mip, x0
csrrs x0, mip, x5
csrrs x7, mip, x0
csrrc x0, mip, x5
csrrs x8, mip, x0
csrrw x0, stimecmp, x0
csrrs x9, mip, x0 #|end
