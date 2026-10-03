auipc x1, 0
addi x1, x1, 152
csrrw x0, stvec, x1
auipc x1, 0
addi x1, x1, 180
csrrw x0, mtvec, x1
addi x2, x0, 512
addi x2, x2, 256
csrrw x0, medeleg, x2
csrrw x0, mstatus, x0
auipc x4, 0
addi x4, x4, 32
csrrw x0, mepc, x4
mret
.word 0
.word 0
.word 0
.word 0
ecall
ebreak
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
ecall
ebreak
.word 0
.word 0
csrrs x8, scause, x0
csrrs x9, sepc, x0
addi x9, x9, 4
csrrw x0, sepc, x9
sret
.word 0
.word 0
.word 0
.word 0
.word 0
csrrs x12, mscratch, x0
beq x12, x0, dropS
addi x13, x0, 1
beq x12, x13, doecall
csrrs x10, mcause, x0
csrrs x11, mepc, x0
addi x11, x11, 4
csrrw x0, mepc, x11
mret
dropS:
addi x12, x0, 1
csrrw x0, mscratch, x12
csrrs x10, mcause, x0
addi x3, x0, 1
slli x3, x3, 11
csrrw x0, mstatus, x3
auipc x4, 0
addi x4, x4, -116
csrrw x0, mepc, x4
mret
doecall:
addi x12, x0, 2
csrrw x0, mscratch, x12
ecall
.word 0
.word 0
