auipc x1, 0                  #: the handler's base: this instruction's own address. | RVI-RV32I §1.1.4
addi x1, x1, 616             #: the handler sits right after the main body. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1          #: direct-mode mtvec = the handler; no GPR written. | RVP-MACHINE §2.1.1.7
addi x6, x0, 9               #: a value to (try to) write. | RVI-RV32I §1.1.4
addi x28, x0, 2              #: illegal-instruction's cause, for the handler's one comparison. | RVI-RV32I §1.1.4
addi x5, x0, -1              #: a sentinel the read of cycle must replace. | RVI-RV32I §1.1.4
rdcycle x5                   #: cycle reads in M, where no gate applies. | RVI-ZICNTR §6.1.1; RVI-ZICSR §5.1.1
addi x7, x0, -1              #: a sentinel the read of time must replace. | RVI-RV32I §1.1.4
rdtime x7                    #: time reads in M, where no gate applies. | RVI-ZICNTR §6.1.1; RVI-ZICSR §5.1.1
addi x8, x0, -1              #: a sentinel the read of instret must replace. | RVI-RV32I §1.1.4
rdinstret x8                 #: instret reads in M, where no gate applies. | RVI-ZICNTR §6.1.1; RVI-ZICSR §5.1.1
addi x9, x0, -1              #: a sentinel the read of mcycle must replace. | RVI-RV32I §1.1.4
csrrs x9, mcycle, x0         #: mcycle reads in M: the machine view of the same count. | RVP-MACHINE §2.1.1.10; RVI-ZICSR §5.1.1
addi x10, x0, -1             #: a sentinel the read of minstret must replace. | RVI-RV32I §1.1.4
csrrs x10, minstret, x0      #: minstret reads in M: the machine view of the same count. | RVP-MACHINE §2.1.1.10; RVI-ZICSR §5.1.1
rdinstret x11                #: the count before three instructions retire. | RVI-ZICNTR §6.1.1
rdcycle x12                  #: the time count, one boundary later. | RVI-ZICNTR §6.1.1
addi x13, x0, 1              #: one retires. | RVI-RV32I §1.1.4
addi x13, x13, 1             #: two retire. | RVI-RV32I §1.1.4
addi x13, x13, 1             #: three retire. | RVI-RV32I §1.1.4
rdinstret x14                #: the count after them: five boundaries on from x11, every one of them retired. | RVI-ZICNTR §6.1.1
rdcycle x15                  #: the time count: five boundaries on from x12. | RVI-ZICNTR §6.1.1
sub x16, x14, x11            #: instret moved by the five instructions retired between its reads: 5. | RVI-ZICNTR §6.1.1 (boundary: instret counts retired instructions)
sub x17, x15, x12            #: cycle moved by 5, one tick per boundary (the laboratory's rate; the reference at instructions_per_tick 1). | RVI-ZICNTR §6.1.1 (boundary: the counters progress)
addi x30, x0, -1             #: re-arm the cause sentinel. | RVI-RV32I §1.1.4
addi x18, x0, 7              #: the sentinel the refused instruction must leave untouched. | RVI-RV32I §1.1.4
csrrw x18, cycle, x6         #: cycle is read-only (csr[11:10] = 11): CSRRW always writes, so illegal-instruction, rd untouched. | RVI-ZICNTR §6.1
addi x19, x18, 0             #: x18 still holds 7: the refused CSRRW committed nothing to rd. | RVI-ZICNTR §6.1 (boundary: CSRRW on a read-only counter)
addi x30, x0, -1             #: re-arm the cause sentinel. | RVI-RV32I §1.1.4
addi x18, x0, 8              #: the sentinel the refused instruction must leave untouched. | RVI-RV32I §1.1.4
csrrs x18, instret, x6       #: CSRRS with rs1 != x0 is a write attempt on the read-only instret: illegal-instruction, rd untouched. | RVI-ZICNTR §6.1
addi x19, x18, 0             #: x18 still holds 8. | RVI-ZICNTR §6.1 (boundary: CSRRS with rs1 != x0)
addi x30, x0, -1             #: re-arm the cause sentinel. | RVI-RV32I §1.1.4
addi x18, x0, 9              #: the sentinel the refused instruction must leave untouched. | RVI-RV32I §1.1.4
csrrsi x18, instret, 1       #: CSRRSI with a nonzero uimm is a write attempt: illegal-instruction, rd untouched. | RVI-ZICNTR §6.1
addi x19, x18, 0             #: x18 still holds 9. | RVI-ZICNTR §6.1 (boundary: CSRRSI with uimm != 0)
addi x30, x0, -1             #: re-arm the cause sentinel. | RVI-RV32I §1.1.4
addi x18, x0, 10             #: the sentinel the refused instruction must leave untouched. | RVI-RV32I §1.1.4
csrrci x18, time, 2          #: CSRRCI with a nonzero uimm on the read-only time: illegal-instruction, rd untouched. | RVI-ZICNTR §6.1
addi x19, x18, 0             #: x18 still holds 10. | RVI-ZICNTR §6.1 (boundary: CSRRCI with uimm != 0)
addi x30, x0, -1             #: re-arm the cause sentinel. | RVI-RV32I §1.1.4
addi x18, x0, 11             #: the sentinel the refused instruction must leave untouched. | RVI-RV32I §1.1.4
csrrwi x18, time, 3          #: CSRRWI always writes: illegal-instruction on the read-only time, rd untouched. | RVI-ZICNTR §6.1
addi x19, x18, 0             #: x18 still holds 11. | RVI-ZICNTR §6.1 (boundary: CSRRWI always writes)
addi x18, x0, -1             #: a sentinel the legal read must replace. | RVI-RV32I §1.1.4
csrrs x18, cycle, x0         #: rs1 = x0 writes nothing, so reading the read-only cycle is legal. | RVI-ZICSR §5.1.1 (boundary: CSRRS with rs1 = x0 is a read)
addi x19, x0, -1             #: a sentinel the legal read must replace. | RVI-RV32I §1.1.4
csrrsi x19, instret, 0       #: uimm = 0 writes nothing: a legal read of the read-only instret. | RVI-ZICSR §5.1.1 (boundary: CSRRSI with uimm = 0 is a read)
rdinstret x11                #: instret before a refused instruction. | RVI-ZICNTR §6.1.1
rdcycle x12                  #: cycle, one boundary later. | RVI-ZICNTR §6.1.1
addi x30, x0, -1             #: re-arm the cause sentinel. | RVI-RV32I §1.1.4
csrrw x0, cycle, x6          #: rd = x0 skips the read, not the write: still illegal; the handler runs seven boundaries, this one retires nothing. | RVI-ZICNTR §6.1
rdinstret x14                #: instret after the trap: it counts the retired instructions only. | RVI-ZICNTR §6.1.1
rdcycle x15                  #: cycle after the trap: it counts every boundary. | RVI-ZICNTR §6.1.1
sub x16, x15, x14            #: cycle minus instret ... | RVI-RV32I §1.1.4
sub x17, x12, x11            #: ... against the same difference before the trap. | RVI-RV32I §1.1.4
sub x16, x16, x17            #: they differ by the boundaries that retired nothing: the refused instruction's own, 1, which is the trap's alone. | RVI-ZICNTR §6.1.1 (boundary: a trapped instruction does not retire)
addi x3, x0, 1               #: 1 ... | RVI-RV32I §1.1.4
slli x3, x3, 11              #: ... at bit 11: mstatus.MPP = S. | RVI-RV64I §3.1.2.1
csrrw x0, mstatus, x3        #: MPP <- S. | RVP-MACHINE §2.1.1.6
auipc x4, 0                  #: the entry base. | RVI-RV32I §1.1.4
addi x4, x4, 16              #: the instruction after mret. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4           #: mepc <- the entry. | RVI-ZICSR §5.1.1
mret                         #: drop to S at mepc. | RVP-MACHINE §2.1.3.2
addi x30, x0, -1             #: re-arm the cause sentinel. | RVI-RV32I §1.1.4
addi x20, x0, 21             #: the sentinel the refused read must leave untouched. | RVI-RV32I §1.1.4
rdcycle x20                  #: mcounteren.CY is clear: illegal-instruction in S, rd untouched. | RVP-MACHINE §2.1.1.11; RVI-ZICNTR §6.1.1
addi x21, x20, 0             #: x20 still holds 21: the refused read committed nothing. | RVP-MACHINE §2.1.1.11; RVI-ZICNTR §6.1.1 (boundary: rdcycle refused in S)
addi x30, x0, -1             #: re-arm the cause sentinel. | RVI-RV32I §1.1.4
addi x20, x0, 22             #: the sentinel the refused read must leave untouched. | RVI-RV32I §1.1.4
rdtime x20                   #: mcounteren.TM is clear: illegal-instruction in S. | RVP-MACHINE §2.1.1.11
addi x21, x20, 0             #: x20 still holds 22: the refused read committed nothing. | RVP-MACHINE §2.1.1.11 (boundary: rdtime refused in S)
addi x30, x0, -1             #: re-arm the cause sentinel. | RVI-RV32I §1.1.4
addi x20, x0, 23             #: the sentinel the refused read must leave untouched. | RVI-RV32I §1.1.4
rdinstret x20                #: mcounteren.IR is clear: illegal-instruction in S. | RVP-MACHINE §2.1.1.11
addi x21, x20, 0             #: x20 still holds 23: the refused read committed nothing. | RVP-MACHINE §2.1.1.11 (boundary: rdinstret refused in S)
ecall                        #: back to M: the handler returns to M after an environment call. | RVP-MACHINE §2.1.1.15
csrrwi x0, mcounteren, 1     #: mcounteren <- CY alone. | RVP-MACHINE §2.1.1.11
addi x3, x0, 1               #: 1 ... | RVI-RV32I §1.1.4
slli x3, x3, 11              #: ... at bit 11: mstatus.MPP = S. | RVI-RV64I §3.1.2.1
csrrw x0, mstatus, x3        #: MPP <- S. | RVP-MACHINE §2.1.1.6
auipc x4, 0                  #: the entry base. | RVI-RV32I §1.1.4
addi x4, x4, 16              #: the instruction after mret. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4           #: mepc <- the entry. | RVI-ZICSR §5.1.1
mret                         #: drop to S at mepc. | RVP-MACHINE §2.1.3.2
addi x22, x0, -1             #: a sentinel the read must replace. | RVI-RV32I §1.1.4
rdcycle x22                  #: mcounteren.CY is set: cycle reads in S. | RVP-MACHINE §2.1.1.11 (boundary: rdcycle permitted in S)
addi x30, x0, -1             #: re-arm the cause sentinel. | RVI-RV32I §1.1.4
addi x20, x0, 24             #: the sentinel the refused read must leave untouched. | RVI-RV32I §1.1.4
rdtime x20                   #: mcounteren.TM is still clear: each bit gates its own counter. | RVP-MACHINE §2.1.1.11
addi x21, x20, 0             #: x20 still holds 24: the refused read committed nothing. | RVP-MACHINE §2.1.1.11 (boundary: rdtime refused in S)
addi x30, x0, -1             #: re-arm the cause sentinel. | RVI-RV32I §1.1.4
addi x20, x0, 25             #: the sentinel the refused read must leave untouched. | RVI-RV32I §1.1.4
rdinstret x20                #: mcounteren.IR is still clear. | RVP-MACHINE §2.1.1.11
addi x21, x20, 0             #: x20 still holds 25: the refused read committed nothing. | RVP-MACHINE §2.1.1.11 (boundary: rdinstret refused in S)
ecall                        #: back to M. | RVP-MACHINE §2.1.1.15
csrrwi x0, mcounteren, 7     #: mcounteren <- CY, TM and IR. | RVP-MACHINE §2.1.1.11
addi x3, x0, 1               #: 1 ... | RVI-RV32I §1.1.4
slli x3, x3, 11              #: ... at bit 11: mstatus.MPP = S. | RVI-RV64I §3.1.2.1
csrrw x0, mstatus, x3        #: MPP <- S. | RVP-MACHINE §2.1.1.6
auipc x4, 0                  #: the entry base. | RVI-RV32I §1.1.4
addi x4, x4, 16              #: the instruction after mret. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4           #: mepc <- the entry. | RVI-ZICSR §5.1.1
mret                         #: drop to S at mepc. | RVP-MACHINE §2.1.3.2
addi x23, x0, -1             #: a sentinel the read must replace. | RVI-RV32I §1.1.4
rdtime x23                   #: mcounteren.TM is set: time reads in S, the read a Linux kernel needs. | RVP-MACHINE §2.1.1.11 (boundary: rdtime permitted in S)
addi x24, x0, -1             #: a sentinel the read must replace. | RVI-RV32I §1.1.4
rdinstret x24                #: mcounteren.IR is set: instret reads in S. | RVP-MACHINE §2.1.1.11 (boundary: rdinstret permitted in S)
ecall                        #: back to M. | RVP-MACHINE §2.1.1.15
csrrw x0, mstatus, x0        #: MPP <- U. | RVP-MACHINE §2.1.1.6
auipc x4, 0                  #: the entry base. | RVI-RV32I §1.1.4
addi x4, x4, 16              #: the instruction after mret. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4           #: mepc <- the entry. | RVI-ZICSR §5.1.1
mret                         #: drop to U at mepc. | RVP-MACHINE §2.1.3.2
addi x30, x0, -1             #: re-arm the cause sentinel. | RVI-RV32I §1.1.4
addi x20, x0, 26             #: the sentinel the refused read must leave untouched. | RVI-RV32I §1.1.4
rdcycle x20                  #: scounteren is clear: illegal-instruction in U, though mcounteren.CY is set. | RVP-SUPERVISOR §11.1.1.5
addi x21, x20, 0             #: x20 still holds 26: the refused read committed nothing. | RVP-SUPERVISOR §11.1.1.5 (boundary: rdcycle refused in U)
ecall                        #: back to M. | RVP-MACHINE §2.1.1.15
csrrwi x0, scounteren, 4     #: scounteren <- IR alone. | RVP-SUPERVISOR §11.1.1.5
csrrw x0, mstatus, x0        #: MPP <- U. | RVP-MACHINE §2.1.1.6
auipc x4, 0                  #: the entry base. | RVI-RV32I §1.1.4
addi x4, x4, 16              #: the instruction after mret. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4           #: mepc <- the entry. | RVI-ZICSR §5.1.1
mret                         #: drop to U at mepc. | RVP-MACHINE §2.1.3.2
addi x25, x0, -1             #: a sentinel the read must replace. | RVI-RV32I §1.1.4
rdinstret x25                #: both enables' IR are set: instret reads in U. | RVP-SUPERVISOR §11.1.1.5 (boundary: rdinstret permitted in U)
addi x30, x0, -1             #: re-arm the cause sentinel. | RVI-RV32I §1.1.4
addi x20, x0, 27             #: the sentinel the refused read must leave untouched. | RVI-RV32I §1.1.4
rdcycle x20                  #: scounteren.CY is clear: each bit gates its own counter in U too. | RVP-SUPERVISOR §11.1.1.5
addi x21, x20, 0             #: x20 still holds 27: the refused read committed nothing. | RVP-SUPERVISOR §11.1.1.5 (boundary: rdcycle refused in U)
ecall                        #: back to M. | RVP-MACHINE §2.1.1.15
csrrwi x0, mcounteren, 3     #: mcounteren <- CY and TM: IR clear. | RVP-MACHINE §2.1.1.11
csrrwi x0, scounteren, 7     #: scounteren <- CY, TM and IR. | RVP-SUPERVISOR §11.1.1.5
csrrw x0, mstatus, x0        #: MPP <- U. | RVP-MACHINE §2.1.1.6
auipc x4, 0                  #: the entry base. | RVI-RV32I §1.1.4
addi x4, x4, 16              #: the instruction after mret. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4           #: mepc <- the entry. | RVI-ZICSR §5.1.1
mret                         #: drop to U at mepc. | RVP-MACHINE §2.1.3.2
addi x26, x0, -1             #: a sentinel the read must replace. | RVI-RV32I §1.1.4
rdcycle x26                  #: both enables' CY are set: cycle reads in U. | RVP-SUPERVISOR §11.1.1.5 (boundary: rdcycle permitted in U)
addi x16, x0, -1             #: a sentinel the read must replace. | RVI-RV32I §1.1.4
rdtime x16                   #: both enables' TM are set: time reads in U. | RVP-SUPERVISOR §11.1.1.5 (boundary: rdtime permitted in U)
addi x30, x0, -1             #: re-arm the cause sentinel. | RVI-RV32I §1.1.4
addi x20, x0, 28             #: the sentinel the refused read must leave untouched. | RVI-RV32I §1.1.4
rdinstret x20                #: mcounteren.IR is clear: illegal-instruction in U, though scounteren.IR is set. | RVP-MACHINE §2.1.1.11; RVP-SUPERVISOR §11.1.1.5
addi x21, x20, 0             #: x20 still holds 28: the refused read committed nothing. | RVP-MACHINE §2.1.1.11; RVP-SUPERVISOR §11.1.1.5 (boundary: rdinstret refused in U)
ecall                        #: back to M. | RVP-MACHINE §2.1.1.15
csrrs x27, mcycle, x0        #: mcycle, in M. | RVP-MACHINE §2.1.1.10
rdcycle x31                  #: cycle, one boundary later. | RVI-ZICNTR §6.1.1
sub x27, x31, x27            #: cycle minus mcycle = 1: one count under two names, moved by the one boundary between the reads. | RVP-MACHINE §2.1.1.10; RVI-ZICNTR §6.1.1 (boundary: mcycle and cycle are one count)
csrrs x27, minstret, x0      #: minstret, in M. | RVP-MACHINE §2.1.1.10
rdinstret x31                #: instret, one boundary later. | RVI-ZICNTR §6.1.1
sub x27, x31, x27            #: instret minus minstret = 1, the read that retired between them. The budget ends here; the handler below runs only on a trap. | RVP-MACHINE §2.1.1.10; RVI-ZICNTR §6.1.1 (boundary: minstret and instret are one count)
csrrs x30, mcause, x0        #: the handler, in M: the cause. | RVP-MACHINE §2.1.1.15
csrrs x29, mepc, x0          #: mepc is the trapping instruction's own address. | RVP-MACHINE §2.1.1.14
addi x29, x29, 4             #: step past it. | RVI-RV32I §1.1.4
csrrw x0, mepc, x29          #: mepc <- the next instruction. | RVI-ZICSR §5.1.1
beq x30, x28, 16             #: a refused access returns to the mode it came from. | RVI-RV32I §1.1.5
addi x3, x0, 3               #: 3 ... | RVI-RV32I §1.1.4
slli x3, x3, 11              #: ... at bits 12:11: an environment call returns to M. | RVI-RV64I §3.1.2.1
csrrs x0, mstatus, x3        #: MPP <- M. | RVI-ZICSR §5.1.1
mret                         #: back, at mepc. | RVP-MACHINE §2.1.3.2
