rdcycle x5
rdtime x6
rdinstret x7
auipc x1, 0
addi x1, x1, 168
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
rdcycle x8
rdcycle x8
ecall
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
rdcycle x13
rdcycle x13
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
csrrs x12, mscratch, x0
beq x12, x0, stage1
addi x13, x0, 1
beq x12, x13, stage2
addi x10, x0, 1
csrrs x0, scounteren, x10
csrrs x15, mcause, x0
csrrs x11, mepc, x0
addi x11, x11, 4
csrrw x0, mepc, x11
mret
stage1:
addi x12, x0, 1
csrrw x0, mscratch, x12
csrrs x9, mcause, x0
addi x10, x0, 1
csrrs x0, mcounteren, x10
csrrs x11, mepc, x0
addi x11, x11, 4
csrrw x0, mepc, x11
mret
stage2:
addi x12, x0, 2
csrrw x0, mscratch, x12
csrrs x14, mcause, x0
csrrw x0, mstatus, x0
auipc x4, 0
addi x4, x4, -144
csrrw x0, mepc, x4
mret
