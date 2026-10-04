auipc x1, 0
addi x1, x1, 208
csrrw x0, mtvec, x1
auipc x11, 0
addi x11, x11, 2047
addi x11, x11, 2037
lui x10, 131073
addi x10, x10, 1
sd x10, 16, x11
auipc x11, 0
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2019
lui x10, 131073
addi x10, x10, 1025
sd x10, 0, x11
auipc x11, 0
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 1973
lui x10, 131072
addi x10, x10, 207
sd x10, 0, x11
lui x2, 128
addi x2, x2, 1
addi x5, x0, 8
slli x5, x5, 60
or x2, x2, x5
csrrw x0, satp, x2
lui x13, 0x40000
slli x13, x13, 8
addi x3, x0, 1
slli x3, x3, 11
csrrw x0, mstatus, x3
auipc x4, 0
addi x4, x4, 16
csrrw x0, mepc, x4
mret
ld x14, x13, 0
addi x21, x0, 1
csrrs x7, mcause, x0
csrrs x8, mtval, x0
csrrs x9, mepc, x0
addi x9, x9, 4
csrrw x0, mepc, x9
mret
