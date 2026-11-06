auipc x1, 0                  #: the base for M's handler: {new}. | RVI-RV64I §3.1.2.1
addi x1, x1, 36              #: M's handler: {new}. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1          #: mtvec = M's handler; no GPR written. | RVP-MACHINE §2.1.1.7
auipc x1, 0                  #: the base for S's handler: {new}. | RVI-RV64I §3.1.2.1
addi x1, x1, 60              #: S's handler: {new}. | RVI-RV32I §1.1.4
csrrw x0, stvec, x1          #: stvec = S's handler; no GPR written. | RVP-SUPERVISOR §11.1.1.2
addi x2, x0, 264             #: medeleg's bit 3 (breakpoint) and bit 8 (ecall from U): 264. | RVP-MACHINE §2.1.1.8
csrrw x0, medeleg, x2        #: those two causes go to S when taken below M; no GPR written. | RVP-MACHINE §2.1.1.8
jal x0, 64                   #: past the handlers; x0 discards the link. | RVI-RV32I §1.1.5.1
csrrs x10, mcause, x0        #: M's handler reads mcause, replacing a sentinel: {new}. | RVP-MACHINE §2.1.3.1; RVP-MACHINE §2.1.1.15 (boundary: the cause names the mode)
csrrs x11, mtval, x0         #: M's handler reads mtval, replacing a sentinel: {new}. | RVP-MACHINE §2.1.3.1; RVP-MACHINE §2.1.1.16
csrrs x12, mepc, x0          #: M's handler reads mepc, the trapping instruction's own address: {new}. | RVP-MACHINE §2.1.3.1; RVP-MACHINE §2.1.1.14
addi x13, x12, 4             #: the instruction after it: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x13          #: resume there; no GPR written. | RVP-MACHINE §2.1.1.14
addi x9, x0, 2               #: 2, illegal-instruction's cause. | RVI-RV32I §1.1.4
bne x10, x9, 8               #: any other cause returns at once. | RVI-RV32I §1.1.5.2
csrrw x0, medeleg, x0        #: the illegal instruction marks the end of delegation: medeleg <- 0; no GPR written. | RVP-MACHINE §2.1.1.8
mret                         #: back to the instruction after the trap. | RVP-MACHINE §2.1.3.2
csrrs x20, scause, x0        #: S's handler reads scause, replacing a sentinel: {new}. | RVP-MACHINE §2.1.1.8; RVP-SUPERVISOR §11.1.1.8 (boundary: the delegated cause reaches S)
csrrs x21, stval, x0         #: S's handler reads stval, replacing a sentinel: {new}. | RVP-MACHINE §2.1.1.8; RVP-SUPERVISOR §11.1.1.9
csrrs x22, sepc, x0          #: S's handler reads sepc, the trapping instruction's own address: {new}. | RVP-MACHINE §2.1.1.8; RVP-SUPERVISOR §11.1.1.7
addi x23, x22, 4             #: the instruction after it: {new}. | RVI-RV32I §1.1.4
csrrw x0, sepc, x23          #: resume there; no GPR written. | RVP-SUPERVISOR §11.1.1.7
sret                         #: back to the instruction after the trap. | RVP-MACHINE §2.1.3.2
addi x10, x0, 77             #: a sentinel, so the handler's read is a change. | RVI-RV32I §1.1.4
addi x11, x0, 77             #: a sentinel, so the handler's read is a change. | RVI-RV32I §1.1.4
ecall                        #: ECALL in M traps to M, whatever medeleg says about other modes. | RVP-MACHINE §2.1.3.1
addi x10, x0, 77             #: a sentinel, so the handler's read is a change. | RVI-RV32I §1.1.4
addi x11, x0, 77             #: a sentinel, so the handler's read is a change. | RVI-RV32I §1.1.4
ebreak                       #: EBREAK in M: its cause is delegated, but a trap never moves to a lower mode, so M takes it. | RVP-MACHINE §2.1.3.1; RVP-MACHINE §2.1.1.8
addi x3, x0, 1               #: 1, for the MPP field. | RVI-RV32I §1.1.4
slli x3, x3, 11              #: at bit 11: mstatus.MPP = S: {new}. | RVI-RV64I §3.1.2.1
csrrw x0, mstatus, x3        #: MPP <- S; no GPR written. | RVP-MACHINE §2.1.1.6
auipc x4, 0                  #: the base for the drop: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16              #: the instruction after mret: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4           #: mepc <- that address; no GPR written. | RVP-MACHINE §2.1.1.14
mret                         #: drop to S. | RVP-MACHINE §2.1.3.2
addi x20, x0, 77             #: a sentinel, so the handler's read is a change. | RVI-RV32I §1.1.4
addi x21, x0, 77             #: a sentinel, so the handler's read is a change. | RVI-RV32I §1.1.4
ebreak                       #: EBREAK in S, delegated: S takes it. | RVP-MACHINE §2.1.3.1; RVP-MACHINE §2.1.1.8
addi x10, x0, 77             #: a sentinel, so the handler's read is a change. | RVI-RV32I §1.1.4
addi x11, x0, 77             #: a sentinel, so the handler's read is a change. | RVI-RV32I §1.1.4
ecall                        #: ECALL in S: bit 9 of medeleg is clear, so M takes it. | RVP-MACHINE §2.1.3.1; RVP-MACHINE §2.1.1.8
addi x3, x0, 256             #: 256, sstatus.SPP. | RVI-RV32I §1.1.4
csrrc x0, sstatus, x3        #: SPP <- U; no GPR written. | RVP-SUPERVISOR §11.1.1.1
auipc x4, 0                  #: the base for the drop: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16              #: the instruction after sret: {new}. | RVI-RV32I §1.1.4
csrrw x0, sepc, x4           #: sepc <- that address; no GPR written. | RVP-SUPERVISOR §11.1.1.7
sret                         #: drop to U. | RVP-MACHINE §2.1.3.2
addi x20, x0, 77             #: a sentinel, so the handler's read is a change. | RVI-RV32I §1.1.4
addi x21, x0, 77             #: a sentinel, so the handler's read is a change. | RVI-RV32I §1.1.4
ecall                        #: ECALL in U, delegated: S takes it. | RVP-MACHINE §2.1.3.1; RVP-MACHINE §2.1.1.8
addi x20, x0, 77             #: a sentinel, so the handler's read is a change. | RVI-RV32I §1.1.4
addi x21, x0, 77             #: a sentinel, so the handler's read is a change. | RVI-RV32I §1.1.4
ebreak                       #: EBREAK in U, delegated: S takes it. | RVP-MACHINE §2.1.3.1; RVP-MACHINE §2.1.1.8
addi x10, x0, 77             #: a sentinel, so the handler's read is a change. | RVI-RV32I §1.1.4
addi x11, x0, 77             #: a sentinel, so the handler's read is a change. | RVI-RV32I §1.1.4
csrrs x5, mstatus, x0        #: U cannot read mstatus: illegal-instruction, undelegated, so M takes it and clears medeleg. | RVP-CSR §1.1.1
addi x10, x0, 77             #: a sentinel, so the handler's read is a change. | RVI-RV32I §1.1.4
addi x11, x0, 77             #: a sentinel, so the handler's read is a change. | RVI-RV32I §1.1.4
ecall                        #: ECALL in U, with medeleg clear: M takes it. | RVP-MACHINE §2.1.3.1; RVP-MACHINE §2.1.1.8
addi x10, x0, 77             #: a sentinel, so the handler's read is a change. | RVI-RV32I §1.1.4
addi x11, x0, 77             #: a sentinel, so the handler's read is a change. | RVI-RV32I §1.1.4
ebreak                       #: EBREAK in U, with medeleg clear: M takes it. | RVP-MACHINE §2.1.3.1; RVP-MACHINE §2.1.1.8
