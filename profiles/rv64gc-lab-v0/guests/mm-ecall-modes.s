auipc x1, 0
addi x1, x1, 152
csrrw x0, mtvec, x1
addi x5, x0, 1
ecall
addi x6, x0, 2
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
addi x5, x5, 1
ecall
addi x6, x6, 1
ecall
.word 0
.word 0
.word 0
.word 0
.word 0
addi x5, x5, 1
ecall
addi x6, x6, 1
.word 0
.word 0
.word 0
.word 0
.word 0
.word 0
.word 0
.word 0
.word 0
csrrs x12, mscratch, x0
addi x13, x0, 2
beq x12, x13, dropU
csrrs x7, mcause, x0
csrrs x8, mepc, x0
addi x8, x8, 4
csrrw x0, mepc, x8
addi x12, x12, 1
csrrw x0, mscratch, x12
mret
dropU:
csrrs x7, mcause, x0
addi x12, x0, 3
csrrw x0, mscratch, x12
csrrw x0, mstatus, x0
auipc x4, 0
addi x4, x4, -104
csrrw x0, mepc, x4
mret
