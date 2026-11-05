auipc x1, 0
addi x1, x1, 116
csrrw x0, mtvec, x1
csrrw x0, mstatus, x0
auipc x4, 0
addi x4, x4, 32
csrrw x0, mepc, x4
mret
.word 0
.word 0
.word 0
.word 0
addi x5, x0, 42
csrrw x0, mscratch, x5
.word 0
.word 0
.word 0
.word 0
.word 0
.word 0
.word 0
.word 0
.word 0
.word 0
.word 0
.word 0
.word 0
.word 0
.word 0
csrrs x7, mcause, x0
csrrs x9, mtval, x0
csrrs x8, mepc, x0
addi x8, x8, 4
csrrw x0, mepc, x8
mret
