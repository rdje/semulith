# P4-SYSTEM.13 c13a1: fresh spec-side parcel derivation, 21 boundaries.
# Two timer waits wake without traps while MIE is clear; software rearms the comparator between waits.
# Enable menvcfg.STCE in M. RV64 LUI sign extension sets bit 63; other bits are WPRI.
lui x31, 0x80000
csrrs x0, menvcfg, x31
#|never: x28, x29
      addi x8, x0, 10
      csrrw x0, stimecmp, x8
      addi x15, x0, 1
      slli x15, x15, 5
      csrrs x0, mie, x15
      wfi
      rdtime x7
      csrrs x11, mip, x0
      addi x8, x0, 16
      csrrw x0, stimecmp, x8
      wfi
      csrrs x7, mip, x0
      addi x13, x0, 1
      slli x13, x13, 16
      csrrw x0, stimecmp, x13
      addi x9, x0, 42 #|end
