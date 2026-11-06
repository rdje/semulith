auipc x1, 0                  #: the base for the handler: {new}. | RVI-RV64I §3.1.2.1
addi x1, x1, 16              #: the handler, at its offset from the start: {new}. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1          #: mtvec = the handler; no GPR written. | RVP-MACHINE §2.1.1.7
jal x0, 36                   #: past the handler; x0 discards the link. | RVI-RV32I §1.1.5.1
csrrs x30, mcause, x0        #: the handler reads mcause: {new}. | RVP-MACHINE §2.1.1.11; RVP-MACHINE §2.1.1.15
addi x31, x0, 2              #: 2, illegal-instruction's cause. | RVI-RV32I §1.1.4
beq x30, x31, 8              #: a refused read resumes after itself. | RVI-RV32I §1.1.5.2
jalr x0, x28, 0              #: an ECALL resumes in M at x28. | RVI-RV32I §1.1.5.1
csrrs x29, mepc, x0          #: the refused instruction's own address: {new}. | RVP-MACHINE §2.1.1.14
addi x29, x29, 4             #: the instruction after it: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x29          #: resume there; no GPR written. | RVP-MACHINE §2.1.1.14
mret                         #: back in the mode it came from. | RVP-MACHINE §2.1.3.2
rdcycle x5                   #: RDCYCLE in M reads the cycle count; no gate applies: {new}. | RVI-ZICNTR §6.1.1 (boundary: RDCYCLE in M)
rdtime x6                    #: RDTIME in M reads time: {new}. | RVI-ZICNTR §6.1.1 (boundary: RDTIME in M)
rdinstret x7                 #: RDINSTRET in M reads instret: {new}. | RVI-ZICNTR §6.1.1 (boundary: RDINSTRET in M)
addi x3, x0, 1               #: 1, for the MPP field. | RVI-RV32I §1.1.4
slli x3, x3, 11              #: at bit 11: mstatus.MPP = S: {new}. | RVI-RV64I §3.1.2.1
csrrw x0, mstatus, x3        #: MPP <- S; no GPR written. | RVP-MACHINE §2.1.1.6
auipc x4, 0                  #: the base for the drop: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16              #: the instruction after mret: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4           #: mepc <- that address; no GPR written. | RVP-MACHINE §2.1.1.14
mret                         #: drop to S. | RVP-MACHINE §2.1.3.2
addi x20, x0, 21             #: a sentinel: a refused read must leave it. | RVI-RV32I §1.1.4
rdcycle x20                  #: mcounteren.CY is clear: refused in S, rd untouched. | RVP-MACHINE §2.1.1.11; RVI-ZICNTR §6.1.1
addi x21, x20, 0             #: copied: {new}, nothing committed. | RVP-MACHINE §2.1.1.11; RVI-ZICNTR §6.1.1 (boundary: S with CY clear keeps rd)
auipc x28, 0                 #: the base for the way back: {new}. | RVI-RV64I §3.1.2.1
addi x28, x28, 12            #: the next phase, in M: {new}. | RVI-RV32I §1.1.4
ecall                        #: ECALL carries S or U back to M, and the handler jumps to x28. | RVP-MACHINE §2.1.3.1
csrrwi x0, mcounteren, 1     #: mcounteren <- CY alone; no GPR written. | RVP-MACHINE §2.1.1.11
addi x3, x0, 1               #: 1, for the MPP field. | RVI-RV32I §1.1.4
slli x3, x3, 11              #: at bit 11: mstatus.MPP = S: {new}. | RVI-RV64I §3.1.2.1
csrrw x0, mstatus, x3        #: MPP <- S; no GPR written. | RVP-MACHINE §2.1.1.6
auipc x4, 0                  #: the base for the drop: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16              #: the instruction after mret: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4           #: mepc <- that address; no GPR written. | RVP-MACHINE §2.1.1.14
mret                         #: drop to S. | RVP-MACHINE §2.1.3.2
addi x8, x0, 21              #: a sentinel, so the read below is a change. | RVI-RV32I §1.1.4
rdcycle x8                   #: CY is set: S reads the cycle count: {new}. | RVP-MACHINE §2.1.1.11; RVI-ZICNTR §6.1.1 (boundary: S with CY set reads)
addi x20, x0, 22             #: a sentinel: a refused read must leave it. | RVI-RV32I §1.1.4
rdtime x20                   #: TM is clear: refused in S. | RVP-MACHINE §2.1.1.11; RVI-ZICNTR §6.1.1
addi x22, x20, 0             #: copied: {new}, nothing committed. | RVP-MACHINE §2.1.1.11; RVI-ZICNTR §6.1.1 (boundary: each gate is its own bit)
auipc x28, 0                 #: the base for the way back: {new}. | RVI-RV64I §3.1.2.1
addi x28, x28, 12            #: the next phase, in M: {new}. | RVI-RV32I §1.1.4
ecall                        #: ECALL carries S or U back to M, and the handler jumps to x28. | RVP-MACHINE §2.1.3.1
csrrwi x0, mcounteren, 7     #: mcounteren <- all three; no GPR written. | RVP-MACHINE §2.1.1.11
addi x3, x0, 1               #: 1, for the MPP field. | RVI-RV32I §1.1.4
slli x3, x3, 11              #: at bit 11: mstatus.MPP = S: {new}. | RVI-RV64I §3.1.2.1
csrrw x0, mstatus, x3        #: MPP <- S; no GPR written. | RVP-MACHINE §2.1.1.6
auipc x4, 0                  #: the base for the drop: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16              #: the instruction after mret: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4           #: mepc <- that address; no GPR written. | RVP-MACHINE §2.1.1.14
mret                         #: drop to S. | RVP-MACHINE §2.1.3.2
csrrwi x0, scounteren, 1     #: scounteren <- CY alone; no GPR written. | RVP-SUPERVISOR §11.1.1.5
addi x3, x0, 256             #: 256, sstatus.SPP. | RVI-RV32I §1.1.4
csrrc x0, sstatus, x3        #: SPP <- U; no GPR written. | RVP-SUPERVISOR §11.1.1.1
auipc x4, 0                  #: the base for the drop: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16              #: the instruction after sret: {new}. | RVI-RV32I §1.1.4
csrrw x0, sepc, x4           #: sepc <- that address; no GPR written. | RVP-SUPERVISOR §11.1.1.7
sret                         #: drop to U. | RVP-MACHINE §2.1.3.2
rdcycle x9                   #: both CY bits are set: U reads the cycle count: {new}. | RVP-SUPERVISOR §11.1.1.5; RVI-ZICNTR §6.1.1 (boundary: U with both bits set reads)
addi x20, x0, 23             #: a sentinel: a refused read must leave it. | RVI-RV32I §1.1.4
rdtime x20                   #: scounteren.TM is clear: refused in U. | RVP-SUPERVISOR §11.1.1.5; RVI-ZICNTR §6.1.1
addi x23, x20, 0             #: copied: {new}, nothing committed. | RVP-SUPERVISOR §11.1.1.5; RVI-ZICNTR §6.1.1 (boundary: U needs scounteren's bit too)
