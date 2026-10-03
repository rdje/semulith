wfi
auipc x1, 0
addi x1, x1, 188
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
wfi
ecall
wfi
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
wfi
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
csrrs x12, mscratch, x0
beq x12, x0, stage1
addi x13, x0, 1
beq x12, x13, stage2
csrrs x15, mcause, x0
csrrs x8, mepc, x0
addi x8, x8, 4
csrrw x0, mepc, x8
mret
stage1:
addi x12, x0, 1
csrrw x0, mscratch, x12
csrrs x7, mcause, x0
addi x2, x0, 1
slli x2, x2, 21
csrrs x0, mstatus, x2
csrrs x8, mepc, x0
addi x8, x8, 4
csrrw x0, mepc, x8
mret
stage2:
addi x12, x0, 2
csrrw x0, mscratch, x12
csrrs x7, mcause, x0
csrrw x0, mstatus, x0
auipc x4, 0
addi x4, x4, -152
csrrw x0, mepc, x4
mret
