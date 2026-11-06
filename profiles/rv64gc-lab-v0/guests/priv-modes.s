auipc x1, 0                    #: the base for the handler: {new}. | RVI-RV64I §3.1.2.1
addi x1, x1, 16                #: the handler, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1            #: mtvec = the handler; no GPR written. | RVP-MACHINE §2.1.1.7
jal x0, 20                     #: past the handler; x0 discards the link. | RVI-RV32I §1.1.5.1
csrrs x30, mcause, x0          #: the handler reads mcause: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.15
csrrs x29, mtval, x0           #: and mtval: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.16
csrrs x28, mepc, x0            #: and mepc, the instruction's own address: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.14
jalr x0, x27, 0                #: on, to where x27 says, still in M. | RVI-RV32I §1.1.5.1
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x5, misa, x0             #: misa names what the hart implements: {new}. | RVP-MACHINE §2.1.1.1; RVP-INTRO Introduction (boundary: the modes misa names)
addi x6, x0, 1                 #: the bit that names S in misa: {new}. | RVI-RV32I §1.1.4
slli x6, x6, 18                #: at bit 18: {new}. | RVI-RV64I §3.1.2.1
and x7, x5, x6                 #: S: {new}. | RVI-RV32I §1.1.4
addi x6, x0, 1                 #: the bit that names U: {new}. | RVI-RV32I §1.1.4
slli x6, x6, 20                #: at bit 20: {new}. | RVI-RV64I §3.1.2.1
and x7, x5, x6                 #: U: {new}. | RVI-RV32I §1.1.4
addi x7, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
andi x7, x5, 128               #: H: {new}. | RVI-RV32I §1.1.4
addi x6, x0, 3                 #: mstatus's GVA and MPV bits: {new}. | RVI-RV32I §1.1.4
slli x6, x6, 38                #: mstatus's GVA and MPV bits: {new}. | RVI-RV64I §3.1.2.1
addi x7, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x7, mstatus, x0          #: mstatus: {new}. | RVP-MACHINE §2.1.1.6.1
and x7, x7, x6                 #: GVA and MPV alone: {new}. | RVI-RV32I §1.1.4 (boundary: no hypervisor state)
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
ecall                          #: an environment call from M: cause 11. | RVP-MACHINE §2.1.1.15
addi x3, x0, 1                 #: both MPP bits: {new}. | RVI-RV32I §1.1.4
slli x3, x3, 13                #: both MPP bits: {new}. | RVI-RV64I §3.1.2.1
addi x3, x3, -2048             #: both MPP bits: {new}. | RVI-RV32I §1.1.4
csrrc x0, mstatus, x3          #: MPP cleared to U; no GPR written. | RVP-MACHINE §2.1.1.6.1
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x8, mstatus, x0          #: mstatus, MPP reading U: {new}. | RVP-MACHINE §2.1.1.6.1
and x8, x8, x3                 #: MPP alone: {new}. | RVI-RV32I §1.1.4
addi x4, x0, 1                 #: MPP = S: {new}. | RVI-RV32I §1.1.4
slli x4, x4, 12                #: MPP = S: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, -2048             #: MPP = S: {new}. | RVI-RV32I §1.1.4
csrrs x0, mstatus, x4          #: MPP = S; no GPR written. | RVP-MACHINE §2.1.1.6.1
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x8, mstatus, x0          #: mstatus: {new}. | RVP-MACHINE §2.1.1.6.1
and x8, x8, x3                 #: MPP alone: {new}. | RVI-RV32I §1.1.4
auipc x4, 0                    #: the base for S's entry: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16                #: S's entry: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4             #: mepc = S's entry; no GPR written. | RVI-ZICSR §5.1.1
mret                           #: to S. | RVP-MACHINE §2.1.3.2
addi x9, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x9, sscratch, x0         #: S reads its own scratch register: nothing refused, and the sentinel gone: {new}. | RVP-SUPERVISOR §11.1.1.1 (boundary: S has its own CSRs)
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
csrrs x10, mscratch, x0        #: M's register, from S: illegal. | RVP-MACHINE §2.1.6.1; RVI-ZICSR §5.1.1
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x8, mstatus, x0          #: M again: the trap recorded where it came from: {new}. | RVP-MACHINE §2.1.1.6.1
and x8, x8, x3                 #: MPP alone: {new}. | RVI-RV32I §1.1.4
auipc x4, 0                    #: the base for S again: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16                #: the ecall in S: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4             #: mepc = there; no GPR written. | RVI-ZICSR §5.1.1
mret                           #: to S again: MPP still holds S. | RVP-MACHINE §2.1.3.2
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
ecall                          #: an environment call from S: cause 9. | RVP-MACHINE §2.1.1.15
csrrc x0, mstatus, x3          #: MPP cleared to U; no GPR written. | RVP-MACHINE §2.1.1.6.1
auipc x4, 0                    #: the base for U's entry: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16                #: U's entry: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4             #: mepc = U's entry; no GPR written. | RVI-ZICSR §5.1.1
mret                           #: to U. | RVP-MACHINE §2.1.3.2
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
csrrs x10, sscratch, x0        #: S's register, from U: illegal. | RVI-ZICSR §5.1.1
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x8, mstatus, x0          #: M again: {new}. | RVP-MACHINE §2.1.1.6.1
and x8, x8, x3                 #: MPP alone: {new}. | RVI-RV32I §1.1.4
auipc x4, 0                    #: the base for U again: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16                #: the ecall in U: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4             #: mepc = there; no GPR written. | RVI-ZICSR §5.1.1
mret                           #: to U again. | RVP-MACHINE §2.1.3.2
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
ecall                          #: an environment call from U: cause 8. | RVP-MACHINE §2.1.1.15
c.nop                          #: the end of the program. | RVI-C §27.1.8
