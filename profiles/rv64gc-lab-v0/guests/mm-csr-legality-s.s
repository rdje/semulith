auipc x1, 0
addi x1, x1, 120
csrrw x0, mtvec, x1
addi x3, x0, 1
slli x3, x3, 11
csrrw x0, mstatus, x3
auipc x4, 0
addi x4, x4, 32
csrrw x0, mepc, x4
mret
.word 0
.word 0
.word 0
.word 0
csrrs x5, mstatus, x0
csrrs x6, sstatus, x0
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
csrrs x8, mepc, x0
addi x8, x8, 4
csrrw x0, mepc, x8
mret
