# P4-SYSTEM.13 c13a1: fresh spec-side parcel derivation, 25 boundaries.
# Timer wake occurs without retirement: two idle steps then delivery. Handler reads instret=13, time=17 and mepc=0x80000034.
# Enable menvcfg.STCE in M. RV64 LUI sign extension sets bit 63; other bits are WPRI.
lui x31, 0x80000
csrrs x0, menvcfg, x31
#|never: x28, x29
      auipc x1, 0
      addi x1, x1, 48
      csrrw x0, mtvec, x1
      addi x8, x0, 15
      csrrw x0, stimecmp, x8
      addi x15, x0, 1
      slli x15, x15, 5
      csrrs x0, mie, x15
      addi x6, x0, 8
      csrrs x0, mstatus, x6
      wfi
      addi x9, x0, 42 #|end
handler:
      rdinstret x14
      rdtime x13
      csrrs x11, mcause, x0
      csrrs x12, mepc, x0
      addi x16, x0, 1
      slli x16, x16, 16
      csrrw x0, stimecmp, x16
      mret
