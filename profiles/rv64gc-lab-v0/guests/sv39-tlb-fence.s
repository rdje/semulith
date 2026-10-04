auipc x1, 0
addi x1, x1, 752
csrrw x0, mtvec, x1
auipc x11, 0
addi x11, x11, 2047
addi x11, x11, 2037
lui x10, 131073
addi x10, x10, -2047
sd x10, 0, x11
lui x10, 131073
addi x10, x10, 1
sd x10, 16, x11
auipc x11, 0
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2003
lui x10, 131073
addi x10, x10, -1023
sd x10, 16, x11
auipc x11, 0
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 1973
lui x10, 131074
addi x10, x10, -1841
sd x10, 16, x11
lui x10, 131074
addi x10, x10, -785
sd x10, 24, x11
auipc x11, 0
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 1923
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
addi x11, x11, 1877
lui x10, 131072
addi x10, x10, 207
sd x10, 0, x11
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
addi x12, x12, 1823
lui x10, 271396
addi x10, x10, 578
sw x10, 0, x12
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
addi x12, x12, 2047
addi x12, x12, 2047
addi x12, x12, 1761
lui x10, 472887
addi x10, x10, 883
sw x10, 0, x12
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
addi x12, x12, 2047
addi x12, x12, 2047
addi x12, x12, 2047
addi x12, x12, 2047
addi x12, x12, 1691
lui x10, 349525
addi x10, x10, 1365
sw x10, 0, x12
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
addi x12, x12, 2047
addi x12, x12, 2047
addi x12, x12, 2047
addi x12, x12, 2047
addi x12, x12, 2047
addi x12, x12, 2047
addi x12, x12, 1613
lui x10, 419430
addi x10, x10, 1638
sw x10, 0, x12
lui x2, 128
addi x2, x2, 1
addi x6, x0, 1
slli x6, x6, 44
or x2, x2, x6
addi x5, x0, 8
slli x5, x5, 60
or x2, x2, x5
csrrw x0, satp, x2
lui x13, 0x402
lui x16, 0x403
addi x19, x0, 1
addi x20, x0, 1
csrrw x0, mscratch, x20
addi x3, x0, 1
slli x3, x3, 11
csrrw x0, mstatus, x3
auipc x4, 0
addi x4, x4, 16
csrrw x0, mepc, x4
mret
ld x14, x13, 0
ld x15, x16, 0
ecall
msect:
auipc x11, 0
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 1417
lui x10, 131074
addi x10, x10, 207
sd x10, 16, x11
lui x10, 131074
addi x10, x10, 1263
sd x10, 24, x11
addi x20, x0, 2
csrrw x0, mscratch, x20
addi x3, x0, 1
slli x3, x3, 11
csrrw x0, mstatus, x3
auipc x4, 0
addi x4, x4, 16
csrrw x0, mepc, x4
mret
ld x23, x13, 0
ld x24, x16, 0
sfence.vma x0, x19
ld x25, x13, 0
ld x26, x16, 0
sfence.vma x0, x0
ld x27, x16, 0
csrrs x12, mscratch, x0
addi x22, x0, 1
beq x12, x22, toM
csrrs x7, mcause, x0
csrrs x8, mtval, x0
csrrs x9, mepc, x0
addi x9, x9, 4
csrrw x0, mepc, x9
mret
toM:
addi x3, x0, 3
slli x3, x3, 11
csrrw x0, mstatus, x3
auipc x4, 0
addi x4, x4, -164
csrrw x0, mepc, x4
mret
