# P4-SYSTEM.13 c13a1: fresh spec-side parcel derivation, 19 boundaries.
# A timer interrupts between compressed instructions; resume retains halfword PC alignment.
# Enable menvcfg.STCE in M. RV64 LUI sign extension sets bit 63; other bits are WPRI.
lui x31, 0x80000
csrrs x0, menvcfg, x31
auipc x1, 0
addi x1, x1, 40
csrrw x0, mtvec, x1
addi x2, x0, 32
csrrw x0, mie, x2
addi x3, x0, 11
csrrw x0, stimecmp, x3
csrrsi x0, mstatus, 8
c.li x10, 1
c.addi x10, 1
c.j done
c.nop
csrrs x7, mcause, x0
csrrs x8, mepc, x0
csrrw x0, mie, x0
mret
done: c.nop
