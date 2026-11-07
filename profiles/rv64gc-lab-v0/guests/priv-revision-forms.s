auipc x1, 0                    #: the base for the handler: {new}. | RVI-RV64I §3.1.2.1
addi x1, x1, 16                #: the handler, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1            #: mtvec = the handler; no GPR written. | RVP-MACHINE §2.1.1.7
jal x0, 20                     #: past the handler; x0 discards the link. | RVI-RV32I §1.1.5.1
csrrs x30, mcause, x0          #: the handler reads mcause: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.15
csrrs x29, mtval, x0           #: and mtval: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.16
csrrs x28, mepc, x0            #: and mepc, the instruction's own address: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.14
jalr x0, x27, 0                #: on, to where x27 says, still in M. | RVI-RV32I §1.1.5.1
auipc x1, 0                    #: the base for S's handler: {new}. | RVI-RV64I §3.1.2.1
addi x1, x1, 16                #: S's handler, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, stvec, x1            #: stvec = S's handler; no GPR written. | RVP-SUPERVISOR §11.1.1.3
jal x0, 20                     #: past S's handler; x0 discards the link. | RVI-RV32I §1.1.5.1
csrrs x22, scause, x0          #: S's handler reads scause: {new}. | RVI-ZICSR §5.1.1; RVP-SUPERVISOR §11.1.1.8
csrrs x23, stval, x0           #: and stval: {new}. | RVI-ZICSR §5.1.1; RVP-SUPERVISOR §11.1.1.9
csrrw x0, sepc, x27            #: sepc = where x27 says; no GPR written. | RVI-ZICSR §5.1.1; RVP-SUPERVISOR §11.1.1.7
sret                           #: on, there, still in S. | RVP-MACHINE §2.1.3.2
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x5, mstatus, x0          #: mstatus at reset: {new}. | RVP-MACHINE §2.1.1.6; RVP-MACHINE §2.1 (boundary: the machine level)
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x6, menvcfg, x0          #: menvcfg exists, and reads 0 at reset: {new}. | RVP-MACHINE §2.1.1.18; RVP-MACHINE §2.1
addi x7, x0, -1                #: menvcfg.STCE: {new}. | RVI-RV32I §1.1.4
slli x7, x7, 63                #: menvcfg.STCE: {new}. | RVI-RV64I §3.1.2.1
csrrs x0, menvcfg, x7          #: M sets STCE; no GPR written. | RVP-MACHINE §2.1.1.18
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x8, menvcfg, x0          #: and it holds: {new}. | RVP-MACHINE §2.1.1.18; RVP-MACHINE §2.1 (boundary: menvcfg holds STCE)
addi x9, x0, 2                 #: TM's bit: {new}. | RVI-RV32I §1.1.4
csrrs x0, mcounteren, x9       #: M lets S read time; no GPR written. | RVP-MACHINE §2.1.1.11
addi x3, x0, 3                 #: both MPP bits: {new}. | RVI-RV32I §1.1.4
slli x3, x3, 11                #: at bit 11: {new}. | RVI-RV64I §3.1.2.1
csrrc x0, mstatus, x3          #: MPP cleared; no GPR written. | RVI-ZICSR §5.1.1
addi x3, x0, 1                 #: MPP = S: {new}. | RVI-RV32I §1.1.4
slli x3, x3, 11                #: at bit 11: {new}. | RVI-RV64I §3.1.2.1
csrrs x0, mstatus, x3          #: MPP = S; no GPR written. | RVI-ZICSR §5.1.1
auipc x4, 0                    #: the base for S's entry: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16                #: S's entry, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4             #: mepc = S's entry; no GPR written. | RVI-ZICSR §5.1.1
mret                           #: to S, with translation on. | RVP-MACHINE §2.1.3.2
addi x10, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x10, sstatus, x0         #: S reads its view: UXL, and the rest of this revision's fields: {new}. | RVP-SUPERVISOR §11.1.1.1; RVP-SUPERVISOR §11.1 (boundary: the supervisor level)
addi x11, x0, 9                #: a compare: {new}. | RVI-RV32I §1.1.4
csrrw x0, stimecmp, x11        #: S programs stimecmp, with STCE set and TM clear of its way; no GPR written. | RVP-SUPERVISOR §11.1.1.12
addi x12, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x12, stimecmp, x0        #: and reads it back: {new}. | RVP-SUPERVISOR §11.1.1.12
c.nop                          #: the end of the program. | RVI-C §27.1.8
