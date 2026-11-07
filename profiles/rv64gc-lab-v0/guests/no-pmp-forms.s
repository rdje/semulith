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
addi x5, x0, 66                #: what the cell holds: {new}. | RVI-RV32I §1.1.4
sd x5, 0, x1                   #: M stores it. | RVI-RV64I §3.1.3
addi x3, x0, 3                 #: both MPP bits: {new}. | RVI-RV32I §1.1.4
slli x3, x3, 11                #: at bit 11: {new}. | RVI-RV64I §3.1.2.1
addi x2, x0, 1                 #: MPRV's bit: {new}. | RVI-RV32I §1.1.4
slli x2, x2, 17                #: at bit 17: {new}. | RVI-RV64I §3.1.2.1
csrrc x0, mstatus, x3          #: MPP cleared; no GPR written. | RVI-ZICSR §5.1.1
addi x19, x0, 1                #: MPP = S: {new}. | RVI-RV32I §1.1.4
slli x19, x19, 11              #: at bit 11: {new}. | RVI-RV64I §3.1.2.1
csrrs x0, mstatus, x19         #: MPP = S; no GPR written. | RVI-ZICSR §5.1.1
csrrs x0, mstatus, x2          #: MPRV: M's data accesses now take S's privilege; no GPR written. | RVP-MACHINE §2.1.1.6.3
auipc x27, 0                   #: where a refused access would resume: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 24              #: past the two accesses: {new}. | RVI-RV32I §1.1.4
addi x7, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x7, x1, 0                   #: a load at S's privilege, with nothing configured: {new}. | RVI-RV64I §3.1.3; RVP-MACHINE §2.1.7; RVP-MACHINE §2.1.1.6.3 (boundary: S's load, by MPRV)
addi x8, x0, 88                #: a new value: {new}. | RVI-RV32I §1.1.4
sd x8, 0, x1                   #: a store at S's privilege. | RVI-RV64I §3.1.3; RVP-MACHINE §2.1.7; RVP-MACHINE §2.1.1.6.3
csrrc x0, mstatus, x2          #: MPRV cleared; no GPR written. | RVP-MACHINE §2.1.1.6.3
addi x9, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x9, x1, 0                   #: M reads what that store left: {new}. | RVI-RV64I §3.1.3 (boundary: S's store took)
csrrc x0, mstatus, x3          #: MPP cleared; no GPR written. | RVI-ZICSR §5.1.1
csrrs x0, mstatus, x2          #: MPRV: M's data accesses now take U's privilege; no GPR written. | RVP-MACHINE §2.1.1.6.3
auipc x27, 0                   #: where a refused access would resume: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 24              #: past the two accesses: {new}. | RVI-RV32I §1.1.4
addi x7, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x7, x1, 0                   #: a load at U's privilege, with nothing configured: {new}. | RVI-RV64I §3.1.3; RVP-MACHINE §2.1.7; RVP-MACHINE §2.1.1.6.3 (boundary: U's load, by MPRV)
addi x8, x0, 99                #: a new value: {new}. | RVI-RV32I §1.1.4
sd x8, 0, x1                   #: a store at U's privilege. | RVI-RV64I §3.1.3; RVP-MACHINE §2.1.7; RVP-MACHINE §2.1.1.6.3
csrrc x0, mstatus, x2          #: MPRV cleared; no GPR written. | RVP-MACHINE §2.1.1.6.3
addi x9, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x9, x1, 0                   #: M reads what that store left: {new}. | RVI-RV64I §3.1.3 (boundary: U's store took)
c.nop                          #: the end of the program. | RVI-C §27.1.8
