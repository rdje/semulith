auipc x1, 0                  #: the handler's base: this instruction's own address, {new}. | RVI-RV64I §3.1.2.1
addi x1, x1, 36              #: the handler sits nine instructions on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1          #: direct-mode mtvec = the handler; no GPR written. | RVP-MACHINE §2.1.5
addi x21, x0, 1              #: 1, the bit to place at 2^40. | RVI-RV32I §1.1.4
slli x21, x21, 40            #: the address 2^40, outside every declared region: {new}. | RVI-RV64I §3.1.1, §3.1.2.1
addi x2, x0, 1               #: raw material for the region base. | RVI-RV32I §1.1.4
slli x2, x2, 31              #: 0x80000000, readable memory: {new}. | RVI-RV64I §3.1.2.1
jal x0, 36                   #: past the handler; x0 discards the link. | RVI-RV32I §1.1.5.1
addi x20, x0, 99             #: never runs: the transfer above has no delay slot. | RVI-RV32I §1.1.5
csrrs x30, mcause, x0        #: the handler reads mcause: {new} = 5, the load's access fault, raised though rd is x0. | RVI-RV32I §1.1.6; RVP-MACHINE §2.1.6 (boundary: the load to x0 still faults)
csrrs x31, mtval, x0         #: the handler reads mtval: {new}, the address the discarded load named. | RVI-RV32I §1.1.6; RVP-MACHINE §2.1.6 (boundary: the fault reports the load's address)
csrrs x29, mepc, x0          #: the handler reads mepc, the load's own address: {new}. | RVP-MACHINE §2.1.6
addi x29, x29, 4             #: the instruction after the load: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x29          #: resume there; no GPR written. | RVP-MACHINE §2.1.6
mret                         #: back to the instruction after the load. | RVP-MACHINE §2.1.6
addi x20, x0, 99             #: never runs: MRET transfers control. | RVP-MACHINE §2.1.6
addi x30, x0, 77             #: a sentinel: the handler's read of mcause is a change only if the fault is raised. | RVI-RV32I §1.1.4
lb x0, x21, 0                #: LB with rd = x0, at 2^40 + 0: the value would be discarded, but the access fault is still raised. | RVI-RV32I §1.1.6
addi x30, x0, 77             #: a sentinel: the handler's read of mcause is a change only if the fault is raised. | RVI-RV32I §1.1.4
lh x0, x21, 2                #: LH with rd = x0, at 2^40 + 2: the value would be discarded, but the access fault is still raised. | RVI-RV32I §1.1.6
addi x30, x0, 77             #: a sentinel: the handler's read of mcause is a change only if the fault is raised. | RVI-RV32I §1.1.4
lw x0, x21, 4                #: LW with rd = x0, at 2^40 + 4: the value would be discarded, but the access fault is still raised. | RVI-RV32I §1.1.6
addi x30, x0, 77             #: a sentinel: the handler's read of mcause is a change only if the fault is raised. | RVI-RV32I §1.1.4
lbu x0, x21, 1               #: LBU with rd = x0, at 2^40 + 1: the value would be discarded, but the access fault is still raised. | RVI-RV32I §1.1.6
addi x30, x0, 77             #: a sentinel: the handler's read of mcause is a change only if the fault is raised. | RVI-RV32I §1.1.4
lhu x0, x21, 6               #: LHU with rd = x0, at 2^40 + 6: the value would be discarded, but the access fault is still raised. | RVI-RV32I §1.1.6
addi x30, x0, 77             #: a sentinel: the handler's read of mcause is a change only if the fault is raised. | RVI-RV32I §1.1.4
lwu x0, x21, 8               #: LWU with rd = x0, at 2^40 + 8: the value would be discarded, but the access fault is still raised. | RVI-RV32I §1.1.6
addi x30, x0, 77             #: a sentinel: the handler's read of mcause is a change only if the fault is raised. | RVI-RV32I §1.1.4
ld x0, x21, 16               #: LD with rd = x0, at 2^40 + 16: the value would be discarded, but the access fault is still raised. | RVI-RV32I §1.1.6
lw x0, x2, 0                 #: LW with rd = x0 from readable memory: no fault, the value discarded. | RVI-RV32I §1.1.6
addi x22, x0, 5              #: the instruction after it, in sequence, with no handler between: {new}. | RVI-RV32I §1.1.6 (boundary: a load to x0 that does not fault)
addi x24, x0, 5              #: 5, to add to x0. | RVI-RV32I §1.1.4
add x25, x24, x0             #: 5 + x0: x0 still reads zero, so the discarded value went nowhere: {new}. | RVI-RV32I §1.1.6 (boundary: x0 still reads zero)
