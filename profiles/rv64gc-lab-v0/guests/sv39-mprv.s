auipc x1, 0
addi x1, x1, 256
csrrw x0, mtvec, x1
auipc x11, 0
addi x11, x11, 2047
addi x11, x11, 2037
lui x10, 131073
addi x10, x10, -2047
sd x10, 0, x11
auipc x11, 0
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2015
lui x10, 131073
addi x10, x10, -1023
sd x10, 16, x11
auipc x11, 0
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 1985
lui x10, 131074
addi x10, x10, -1841
sd x10, 16, x11
auipc x12, 0
addi x12, x12, 2047
addi x12, x12, 2047
addi x12, x12, 2047
addi x12, x12, 2047
addi x12, x12, 2047
addi x12, x12, 2047
addi x12, x12, 2047
addi x12, x12, 2047
addi x12, x12, 2047
addi x12, x12, 2047
addi x12, x12, 2047
addi x12, x12, 1951
lui x10, 0x42424
addi x10, x10, 0x242
sw x10, 0, x12
lui x2, 128
addi x2, x2, 1
addi x5, x0, 8
slli x5, x5, 60
or x2, x2, x5
csrrw x0, satp, x2
lui x13, 0x402
lui x3, 0x21
addi x3, x3, -2048
csrrw x0, mstatus, x3
ld x14, x13, 0
lui x15, 0x42424
addi x15, x15, 0x243
sd x15, 0, x13
ld x17, x13, 0
lui x3, 0x20
csrrw x0, mstatus, x3
ld x18, x13, 0
csrrw x0, mstatus, x0
ld x16, x13, 0
addi x21, x0, 1
csrrs x7, mcause, x0
csrrs x8, mtval, x0
csrrs x9, mepc, x0
addi x9, x9, 4
csrrw x0, mepc, x9
mret
