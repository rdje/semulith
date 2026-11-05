auipc x1, 0
addi x1, x1, 116
csrrw x0, mtvec, x1
csrrwi x0, cycle, 1
csrrwi x0, misa, 1
csrrs x5, misa, x0
addi x6, x0, -1
csrrw x0, mstatus, x6
csrrs x7, mstatus, x0
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
.word 0
.word 0
.word 0
.word 0
csrrs x8, mcause, x0
csrrs x9, mepc, x0
addi x9, x9, 4
csrrw x0, mepc, x9
mret
