# P4-SYSTEM.13 c13a1: fresh spec-side parcel derivation, 19 boundaries.
# Software-posted SSIP and SEIP wake WFI with global enables clear. The enabled comparator is disarmed first.
# Enable menvcfg.STCE in M. RV64 LUI sign extension sets bit 63; other bits are WPRI.
lui x31, 0x80000
csrrs x0, menvcfg, x31
#|never: x28, x29
      addi x13, x0, 1
      slli x13, x13, 16
      csrrw x0, stimecmp, x13
      addi x2, x0, 2
      csrrs x0, mip, x2
      csrrs x0, mie, x2
      wfi
      csrrs x7, mip, x0
      csrrc x0, mip, x2
      addi x8, x0, 1
      slli x8, x8, 9
      csrrs x0, mip, x8
      csrrs x0, mie, x8
      wfi
      csrrs x7, mip, x0
      csrrc x0, mip, x8
      addi x9, x0, 42 #|end
