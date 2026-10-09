# P4-SYSTEM.12 e1d2: spec-side C corpus, budget declared by the producer.
auipc x1, 0
addi x1, x1, 40
csrrw x0, mtvec, x1
addi x2, x0, 32
csrrw x0, mie, x2
addi x3, x0, 9
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
