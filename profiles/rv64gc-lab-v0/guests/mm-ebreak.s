auipc x1, 0
addi x1, x1, 128
csrrw x0, mtvec, x1
ebreak
addi x5, x0, 1
csrrw x0, mstatus, x0
auipc x4, 0
addi x4, x4, 32
csrrw x0, mepc, x4
mret
.word 0
.word 0
.word 0
.word 0
ebreak
addi x6, x0, 2
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
.word 0
csrrs x7, mcause, x0
csrrs x9, mtval, x0
csrrs x8, mepc, x0
addi x8, x8, 4
csrrw x0, mepc, x8
mret
