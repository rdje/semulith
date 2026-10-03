addi x3, x0, 1
slli x3, x3, 11
auipc x1, 0
addi x1, x1, 104
csrrw x0, mtvec, x1
csrrw x0, mstatus, x3
auipc x4, 0
addi x4, x4, 32
csrrw x0, mepc, x4
mret
.word 0
.word 0
.word 0
.word 0
csrrs x5, sstatus, x0
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
csrrs x12, mscratch, x0
bne x12, x0, stage2
addi x12, x0, 1
csrrw x0, mscratch, x12
csrrs x7, mcause, x0
addi x2, x0, 1
slli x2, x2, 17
csrrs x0, mstatus, x2
auipc x4, 0
addi x4, x4, 48
csrrw x0, mepc, x4
mret
.word 0
.word 0
.word 0
.word 0
.word 0
.word 0
.word 0
.word 0
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
stage2:
addi x12, x0, 2
csrrw x0, mscratch, x12
csrrs x7, mcause, x0
csrrs x14, mstatus, x0
addi x3, x0, 3
slli x3, x3, 11
addi x2, x0, 1
slli x2, x2, 17
or x3, x3, x2
csrrw x0, mstatus, x3
auipc x4, 0
addi x4, x4, 44
csrrw x0, mepc, x4
mret
.word 0
.word 0
.word 0
.word 0
.word 0
.word 0
.word 0
csrrs x8, mstatus, x0
