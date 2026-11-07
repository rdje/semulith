auipc x1, 0                    #: the base for the handler: {new}. | RVI-RV64I §3.1.2.1
addi x1, x1, 16                #: the handler, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1            #: mtvec = the handler; no GPR written. | RVP-MACHINE §2.1.1.7
jal x0, 20                     #: past the handler; x0 discards the link. | RVI-RV32I §1.1.5.1
csrrs x30, mcause, x0          #: the handler reads mcause: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.15
csrrs x29, mtval, x0           #: and mtval: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.16
csrrs x28, mepc, x0            #: and mepc, the instruction's own address: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.14
jalr x0, x27, 0                #: on, to where x27 says, still in M. | RVI-RV32I §1.1.5.1
addi x10, x0, 1                #: raw material for the region base. | RVI-RV32I §1.1.4
slli x10, x10, 31              #: 0x80000000: {new}. | RVI-RV64I §3.1.2.1
lui x1, 7                      #: 0x7000: {new}. | RVI-RV64I §3.1.2.1
add x1, x1, x10                #: the data cell, on a page of its own, past this program: {new}. | RVI-RV32I §1.1.4
addi x5, x0, 33                #: a value: {new}. | RVI-RV32I §1.1.4
sd x5, 0, x1                   #: stored. | RVI-RV64I §3.1.3
addi x7, x0, 11                #: x7 holds 11, for a fence naming it as rd: {new}. | RVI-RV32I §1.1.4
addi x8, x0, 22                #: x8 holds 22, for one naming it as rs1: {new}. | RVI-RV32I §1.1.4
fence 0, 3, 3, x0, x0          #: FENCE RW, RW: it decodes, and it does not trap. | RVI-RV32I §1.1.7
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x6, x1, 0                   #: the next row ran, and memory is as it was: {new}. | RVI-RV32I §1.1.7, Table 3 Fence mode encoding; RVI-RV64I §3.1.3 (boundary: FENCE RW, RW)
fence 0, 15, 15, x0, x0        #: FENCE IORW, IORW: it decodes, and it does not trap. | RVI-RV32I §1.1.7
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x6, x1, 0                   #: the next row ran, and memory is as it was: {new}. | RVI-RV32I §1.1.7, Table 3 Fence mode encoding; RVI-RV64I §3.1.3 (boundary: FENCE IORW, IORW)
fence 8, 3, 3, x0, x0          #: FENCE.TSO, fm = 1000: it decodes, and it does not trap. | RVI-RV32I §1.1.7
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x6, x1, 0                   #: the next row ran, and memory is as it was: {new}. | RVI-RV32I §1.1.7, Table 3 Fence mode encoding; RVI-RV64I §3.1.3 (boundary: FENCE.TSO, fm = 1000)
fence 0, 0, 0, x0, x0          #: pred and succ empty, reserved: it decodes, and it does not trap. | RVI-RV32I §1.1.7
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x6, x1, 0                   #: the next row ran, and memory is as it was: {new}. | RVI-RV32I §1.1.7, Table 3 Fence mode encoding; RVI-RV64I §3.1.3 (boundary: pred and succ empty, reserved)
fence 8, 15, 15, x0, x0        #: fm = 1000 with other sets, reserved: it decodes, and it does not trap. | RVI-RV32I §1.1.7
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x6, x1, 0                   #: the next row ran, and memory is as it was: {new}. | RVI-RV32I §1.1.7, Table 3 Fence mode encoding; RVI-RV64I §3.1.3 (boundary: fm = 1000 with other sets, reserved)
fence 1, 3, 3, x0, x0          #: a reserved fm: it decodes, and it does not trap. | RVI-RV32I §1.1.7
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x6, x1, 0                   #: the next row ran, and memory is as it was: {new}. | RVI-RV32I §1.1.7, Table 3 Fence mode encoding; RVI-RV64I §3.1.3 (boundary: a reserved fm)
fence 15, 3, 3, x0, x0         #: the top reserved fm: it decodes, and it does not trap. | RVI-RV32I §1.1.7
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x6, x1, 0                   #: the next row ran, and memory is as it was: {new}. | RVI-RV32I §1.1.7, Table 3 Fence mode encoding; RVI-RV64I §3.1.3 (boundary: the top reserved fm)
fence 0, 3, 3, x8, x7          #: rs1 and rd named, and ignored: it decodes, and it does not trap. | RVI-RV32I §1.1.7
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x6, x1, 0                   #: the next row ran, and memory is as it was: {new}. | RVI-RV32I §1.1.7, Table 3 Fence mode encoding; RVI-RV64I §3.1.3 (boundary: rs1 and rd named, and ignored)
addi x9, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
add x9, x7, x0                 #: x7 was named as rd, and kept its value: {new}. | RVI-RV32I §1.1.7; RVI-RV32I §1.1.4
addi x10, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
add x10, x8, x0                #: and x8 too: {new}. | RVI-RV32I §1.1.7; RVI-RV32I §1.1.4
c.nop                          #: the end of the program. | RVI-C §27.1.8
