auipc x1, 0                    #: the base for the handler: {new}. | RVI-RV64I §3.1.2.1
addi x1, x1, 16                #: the handler, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1            #: mtvec = the handler; no GPR written. | RVP-MACHINE §2.1.1.7
jal x0, 20                     #: past the handler; x0 discards the link. | RVI-RV32I §1.1.5.1
csrrs x30, mcause, x0          #: the handler reads mcause: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.15
csrrs x29, mtval, x0           #: and mtval: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.16
csrrs x28, mepc, x0            #: and mepc, the instruction's own address: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.14
jalr x0, x27, 0                #: on, to where x27 says, still in M. | RVI-RV32I §1.1.5.1
addi x25, x0, 3                #: both MPP bits: {new}. | RVI-RV32I §1.1.4
slli x25, x25, 11              #: at bit 11, kept in x25: {new}. | RVI-RV64I §3.1.2.1
addi x19, x0, 1                #: MPP = S: {new}. | RVI-RV32I §1.1.4
slli x19, x19, 11              #: at bit 11, kept in x19: {new}. | RVI-RV64I §3.1.2.1
addi x5, x0, 2                 #: the supervisor software interrupt's bit: {new}. | RVI-RV32I §1.1.4
csrrs x0, mideleg, x5          #: delegated to S; no GPR written. | RVP-MACHINE §2.1.1.8
csrrs x0, mie, x5              #: enabled locally; no GPR written. | RVP-MACHINE §2.1.1.9
csrrs x0, mip, x5              #: and pending; no GPR written. | RVP-MACHINE §2.1.1.9
wfi                            #: wfi in M, with an interrupt pending and enabled: nothing to wait for. | RVP-MACHINE §2.1.3.3; RVP-INSNS §18.1
addi x6, x0, 1                 #: the row after it ran: {new}. | RVI-RV32I §1.1.4; RVP-MACHINE §2.1.3.3 (boundary: wfi retires)
sfence.vma x0, x0              #: sfence.vma in M: it retires. | RVP-SUPERVISOR §11.1.2.1; RVP-INSNS §18.1
addi x7, x0, 2                 #: the row after it ran: {new}. | RVI-RV32I §1.1.4 (boundary: sfence.vma retires)
csrrc x0, mip, x5              #: no longer pending; no GPR written. | RVP-MACHINE §2.1.1.9
csrrc x0, mstatus, x25         #: MPP cleared; no GPR written. | RVI-ZICSR §5.1.1
csrrs x0, mstatus, x19         #: MPP set; no GPR written. | RVI-ZICSR §5.1.1
auipc x4, 0                    #: the base for the next mode's entry: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16                #: its entry, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4             #: mepc = there; no GPR written. | RVI-ZICSR §5.1.1
mret                           #: there. | RVP-MACHINE §2.1.3.2
auipc x8, 0                    #: S reached by mret: {new}. | RVP-MACHINE §2.1.3.2; RVP-INSNS §18.1
auipc x9, 0                    #: the base for sret's target: {new}. | RVI-RV64I §3.1.2.1
addi x9, x9, 16                #: the row after sret: {new}. | RVI-RV32I §1.1.4
csrrw x0, sepc, x9             #: sepc = there; no GPR written. | RVP-MACHINE §2.1.3.2
sret                           #: sret, with SPP = U: on to U. | RVP-MACHINE §2.1.3.2; RVP-INSNS §18.1
auipc x11, 0                   #: U reached by sret: {new}. | RVP-MACHINE §2.1.3.2; RVP-INSNS §18.1
c.nop                          #: the end of the program. | RVI-C §27.1.8
