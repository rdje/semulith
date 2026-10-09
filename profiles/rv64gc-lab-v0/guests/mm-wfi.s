# P4-SYSTEM.13 c13a1: fresh spec-side parcel derivation, 63 boundaries.
# Legal M/S WFI waits for arranged timer wakes. S with TW=1 and U with S present trap before effects.
# Enable menvcfg.STCE in M. RV64 LUI sign extension sets bit 63; other bits are WPRI.
lui x31, 0x80000
csrrs x0, menvcfg, x31
#|never: x28, x29
      auipc x1, 0
      addi x1, x1, 96
      csrrw x0, mtvec, x1
      addi x15, x0, 1
      slli x15, x15, 5
      csrrs x0, mie, x15
      addi x8, x0, 13
      csrrw x0, stimecmp, x8
      wfi
      rdtime x7
      csrrs x0, mideleg, x15
      addi x8, x0, 27
      csrrw x0, stimecmp, x8
      addi x3, x0, 1
      slli x3, x3, 11
      csrrw x0, mstatus, x3
      auipc x4, 0
      addi x4, x4, 16
      csrrw x0, mepc, x4
      mret
      wfi
      ecall
      wfi
      wfi
handler:
      csrrs x12, mscratch, x0
      beq x12, x0, stage1
      addi x13, x0, 1
      beq x12, x13, stage2
      csrrs x15, mcause, x0
      csrrs x8, mepc, x0 #|end
      addi x8, x8, 4
      csrrw x0, mepc, x8
      mret
stage1:
      addi x12, x0, 1
      csrrw x0, mscratch, x12
      csrrs x7, mcause, x0
      addi x2, x0, 1
      slli x2, x2, 21
      csrrs x0, mstatus, x2
      csrrs x10, mepc, x0
      addi x10, x10, 4
      csrrw x0, mepc, x10
      mret
stage2:
      addi x12, x0, 2
      csrrw x0, mscratch, x12
      csrrs x7, mcause, x0
      addi x13, x0, 1
      slli x13, x13, 16
      csrrw x0, stimecmp, x13
      csrrw x0, mstatus, x0
      auipc x4, 0
      addi x4, x4, -108
      csrrw x0, mepc, x4
      mret
