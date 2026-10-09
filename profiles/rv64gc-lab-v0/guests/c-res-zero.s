# P4-SYSTEM.12 e1d2: spec-side C corpus, budget declared by the producer.
auipc x1, 0
addi x1, x1, 20
csrrw x0, mtvec, x1
.half 0x0000
addi x20, x0, 7
c.j done
csrrs x7, mcause, x0
csrrs x8, mtval, x0
csrrs x9, mepc, x0
addi x9, x9, 2
csrrw x0, mepc, x9
mret
done: c.nop
