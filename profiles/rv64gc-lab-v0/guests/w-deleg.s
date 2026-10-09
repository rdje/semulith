# P4-SYSTEM.13 c13a1: fresh spec-side parcel derivation, 28 boundaries.
# A timer delegated to S wakes the M hart without trapping. Revoking delegation then delivers the pending STI.
# Enable menvcfg.STCE in M. RV64 LUI sign extension sets bit 63; other bits are WPRI.
lui x31, 0x80000
csrrs x0, menvcfg, x31
#|never: x28, x29
      auipc x1, 0
      addi x1, x1, 64
      csrrw x0, mtvec, x1
      addi x15, x0, 1
      slli x15, x15, 5
      csrrs x0, mideleg, x15
      csrrs x0, mie, x15
      addi x8, x0, 15
      csrrw x0, stimecmp, x8
      addi x6, x0, 8
      csrrs x0, mstatus, x6
      wfi
      rdtime x7
      csrrc x0, mideleg, x15
      addi x7, x0, 0
      addi x9, x0, 42 #|end
handler:
      csrrs x11, mcause, x0
      csrrs x12, mepc, x0
      addi x16, x0, 1
      slli x16, x16, 16
      csrrw x0, stimecmp, x16
      csrrs x13, mepc, x0
      addi x13, x13, 4
      csrrw x0, mepc, x13
      mret
