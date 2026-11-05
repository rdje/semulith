csrrs x5, stimecmp, x0
auipc x1, 0
addi x1, x1, 116
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
csrrs x6, stimecmp, x0
csrrs x7, stimecmp, x0
csrrs x15, stimecmp, x0
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
csrrs x8, mcause, x0
csrrs x12, mscratch, x0
bne x12, x0, second
addi x9, x0, 2
csrrs x0, mcounteren, x9
addi x12, x0, 1
csrrw x0, mscratch, x12
beq x0, x0, resume
second:
lui x9, 0x80000
csrrs x0, menvcfg, x9
resume:
csrrs x10, mepc, x0
addi x10, x10, 4
csrrw x0, mepc, x10
mret
