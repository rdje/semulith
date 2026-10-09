# P4-SYSTEM.13 c13a1: fresh spec-side parcel derivation, 28 boundaries.
# After enabling STCE, observe pending, disarm above time, then reassert and deliver STI as virtual time progresses.
# Enable menvcfg.STCE in M. RV64 LUI sign extension sets bit 63; other bits are WPRI.
lui x31, 0x80000
csrrs x0, menvcfg, x31
#|never: x28, x29
      auipc x1, 0
      addi x1, x1, 68
      csrrw x0, mtvec, x1
      csrrs x7, mip, x0
      addi x8, x0, 10
      csrrw x0, stimecmp, x8
      csrrs x7, mip, x0
      addi x5, x0, 1
      csrrs x7, mip, x0
      addi x15, x0, 1
      slli x15, x15, 5
      csrrs x0, mie, x15
      addi x6, x0, 8
      csrrs x0, mstatus, x6
      addi x7, x0, 0
      csrrs x7, mip, x0
      addi x9, x0, 42 #|end
handler:
      csrrs x11, mcause, x0
      csrrs x12, mepc, x0
      addi x13, x0, 1
      slli x13, x13, 16
      csrrw x0, stimecmp, x13
      csrrs x14, mepc, x0
      addi x14, x14, 4
      csrrw x0, mepc, x14
      mret
