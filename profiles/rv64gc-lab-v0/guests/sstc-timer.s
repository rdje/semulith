auipc x1, 0                  #: the M handler's base: this instruction's own address. | RVI-RV32I §1.1.4
addi x1, x1, 712       #: the M handler sits after the S handler. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1          #: direct-mode mtvec = the M handler; no GPR written. | RVP-MACHINE §2.1.1.7
auipc x1, 0                  #: the S handler's base. | RVI-RV32I §1.1.4
addi x1, x1, 660       #: the S handler sits after the main body. | RVI-RV32I §1.1.4
csrrw x0, stvec, x1          #: direct-mode stvec = the S handler; no GPR written. | RVP-SUPERVISOR §11.1.1.2
addi x28, x0, 2              #: illegal-instruction's cause, for the M handler's one comparison. | RVI-RV32I §1.1.4
addi x5, x0, -1              #: a sentinel the read of time must replace. | RVI-RV32I §1.1.4
rdtime x5                    #: time, the value stimecmp is compared against, reads in M. | RVI-ZICNTR §6.1.1; RVI-ZICSR §5.1.1
addi x7, x0, -1              #: a sentinel the read must replace. | RVI-RV32I §1.1.4
csrrs x7, stimecmp, x0       #: in M, stimecmp is accessible with TM and STCE both clear; the laboratory's reset is 0. | RVP-SUPERVISOR §11.1.1.12; RVP-MACHINE §2.1.1.18
addi x6, x0, 1               #: 1 ... | RVI-RV32I §1.1.4
slli x6, x6, 40              #: ... at bit 40: a compare value only 64 bits can hold. | RVI-RV64I §3.1.2.1
csrrw x0, stimecmp, x6       #: M writes the compare; no GPR written. | RVP-SUPERVISOR §11.1.1.12
addi x8, x0, -1              #: a sentinel the read-back must replace. | RVI-RV32I §1.1.4
csrrs x8, stimecmp, x0       #: stimecmp holds all 64 bits. | RVP-SUPERVISOR §11.1.1.12
addi x3, x0, 1               #: 1 ... | RVI-RV32I §1.1.4
slli x3, x3, 11              #: ... at bit 11: mstatus.MPP = S. | RVI-RV64I §3.1.2.1
csrrw x0, mstatus, x3        #: MPP <- S; SIE and MIE clear. | RVP-MACHINE §2.1.1.6
auipc x4, 0                  #: the entry base. | RVI-RV32I §1.1.4
addi x4, x4, 16              #: the instruction after mret. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4           #: mepc <- the entry. | RVI-ZICSR §5.1.1
mret                         #: drop to S at mepc. | RVP-MACHINE §2.1.3.2
addi x30, x0, -1             #: re-arm the cause sentinel. | RVI-RV32I §1.1.4
addi x20, x0, 21             #: the sentinel the refused access must leave untouched. | RVI-RV32I §1.1.4
csrrs x20, stimecmp, x0      #: S with mcounteren.TM clear and menvcfg.STCE clear: illegal-instruction, rd untouched. | RVP-MACHINE §2.1.1.11
addi x21, x20, 0             #: x20 still holds 21: the refused access committed nothing. | RVP-MACHINE §2.1.1.11 (boundary: stimecmp refused in S, TM and STCE clear)
ecall                        #: back to M. | RVP-MACHINE §2.1.1.15
csrrsi x0, mcounteren, 2     #: TM <- 1; STCE stays clear. | RVP-MACHINE §2.1.1.11
addi x3, x0, 1               #: 1 ... | RVI-RV32I §1.1.4
slli x3, x3, 11              #: ... at bit 11: mstatus.MPP = S. | RVI-RV64I §3.1.2.1
csrrw x0, mstatus, x3        #: MPP <- S; SIE and MIE clear. | RVP-MACHINE §2.1.1.6
auipc x4, 0                  #: the entry base. | RVI-RV32I §1.1.4
addi x4, x4, 16              #: the instruction after mret. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4           #: mepc <- the entry. | RVI-ZICSR §5.1.1
mret                         #: drop to S at mepc. | RVP-MACHINE §2.1.3.2
addi x30, x0, -1             #: re-arm the cause sentinel. | RVI-RV32I §1.1.4
addi x20, x0, 22             #: the sentinel the refused access must leave untouched. | RVI-RV32I §1.1.4
csrrs x20, stimecmp, x0      #: S with TM set and STCE clear: still illegal-instruction. | RVP-MACHINE §2.1.1.18
addi x21, x20, 0             #: x20 still holds 22: the refused access committed nothing. | RVP-MACHINE §2.1.1.18 (boundary: stimecmp refused in S, STCE clear)
ecall                        #: back to M. | RVP-MACHINE §2.1.1.15
lui x4, 0x80000              #: bit 31, sign-extended up to bit 63: the pattern that sets menvcfg.STCE. | RVI-RV32I §1.1.4
csrrs x0, menvcfg, x4        #: STCE <- 1. | RVP-MACHINE §2.1.1.18
csrrci x0, mcounteren, 2     #: TM <- 0, with STCE now set. | RVP-MACHINE §2.1.1.11
addi x3, x0, 1               #: 1 ... | RVI-RV32I §1.1.4
slli x3, x3, 11              #: ... at bit 11: mstatus.MPP = S. | RVI-RV64I §3.1.2.1
csrrw x0, mstatus, x3        #: MPP <- S; SIE and MIE clear. | RVP-MACHINE §2.1.1.6
auipc x4, 0                  #: the entry base. | RVI-RV32I §1.1.4
addi x4, x4, 16              #: the instruction after mret. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4           #: mepc <- the entry. | RVI-ZICSR §5.1.1
mret                         #: drop to S at mepc. | RVP-MACHINE §2.1.3.2
addi x30, x0, -1             #: re-arm the cause sentinel. | RVI-RV32I §1.1.4
addi x20, x0, 23             #: the sentinel the refused access must leave untouched. | RVI-RV32I §1.1.4
csrrs x20, stimecmp, x0      #: S with STCE set and TM clear: illegal-instruction, so each gate holds alone. | RVP-MACHINE §2.1.1.11
addi x21, x20, 0             #: x20 still holds 23: the refused access committed nothing. | RVP-MACHINE §2.1.1.11 (boundary: stimecmp refused in S, TM clear)
ecall                        #: back to M. | RVP-MACHINE §2.1.1.15
csrrsi x0, mcounteren, 2     #: TM <- 1: both gates open. | RVP-MACHINE §2.1.1.11
addi x3, x0, 1               #: 1 ... | RVI-RV32I §1.1.4
slli x3, x3, 11              #: ... at bit 11: mstatus.MPP = S. | RVI-RV64I §3.1.2.1
csrrw x0, mstatus, x3        #: MPP <- S; SIE and MIE clear. | RVP-MACHINE §2.1.1.6
auipc x4, 0                  #: the entry base. | RVI-RV32I §1.1.4
addi x4, x4, 16              #: the instruction after mret. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4           #: mepc <- the entry. | RVI-ZICSR §5.1.1
mret                         #: drop to S at mepc. | RVP-MACHINE §2.1.3.2
addi x9, x0, -1              #: a sentinel the read must replace. | RVI-RV32I §1.1.4
csrrs x9, stimecmp, x0       #: both gates open: S reads the value M wrote. | RVP-MACHINE §2.1.1.11; RVP-MACHINE §2.1.1.18 (boundary: stimecmp permitted in S)
addi x6, x0, 1               #: 1 ... | RVI-RV32I §1.1.4
slli x6, x6, 41              #: ... at bit 41: the kernel's own compare value. | RVI-RV64I §3.1.2.1
csrrw x0, stimecmp, x6       #: the S-mode kernel programs its own timer, with no M-mode round trip. | RVP-SUPERVISOR §11.1.1.12
addi x10, x0, -1             #: a sentinel the read-back must replace. | RVI-RV32I §1.1.4
csrrs x10, stimecmp, x0      #: S reads back what it programmed. | RVP-SUPERVISOR §11.1.1.12
ecall                        #: back to M. | RVP-MACHINE §2.1.1.15
csrrw x0, mstatus, x0        #: MPP <- U; SIE and MIE clear. | RVP-MACHINE §2.1.1.6
auipc x4, 0                  #: the entry base. | RVI-RV32I §1.1.4
addi x4, x4, 16              #: the instruction after mret. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4           #: mepc <- the entry. | RVI-ZICSR §5.1.1
mret                         #: drop to U at mepc. | RVP-MACHINE §2.1.3.2
addi x30, x0, -1             #: re-arm the cause sentinel. | RVI-RV32I §1.1.4
addi x20, x0, 24             #: the sentinel the refused access must leave untouched. | RVI-RV32I §1.1.4
csrrs x20, stimecmp, x0      #: U is below stimecmp's own privilege: illegal-instruction, whatever the gates say. | RVP-CSR §1.1.1
addi x21, x20, 0             #: x20 still holds 24: the refused access committed nothing. | RVP-CSR §1.1.1 (boundary: stimecmp refused in U)
ecall                        #: back to M. | RVP-MACHINE §2.1.1.15
addi x4, x0, 32              #: bit 5: the supervisor timer interrupt. | RVI-RV32I §1.1.4
csrrw x0, mideleg, x4        #: delegate it, so sip shows it and S takes it. | RVP-MACHINE §2.1.1.8
addi x3, x0, 1               #: 1 ... | RVI-RV32I §1.1.4
slli x3, x3, 11              #: ... at bit 11: mstatus.MPP = S. | RVI-RV64I §3.1.2.1
csrrw x0, mstatus, x3        #: MPP <- S; SIE and MIE clear. | RVP-MACHINE §2.1.1.6
auipc x4, 0                  #: the entry base. | RVI-RV32I §1.1.4
addi x4, x4, 16              #: the instruction after mret. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4           #: mepc <- the entry. | RVI-ZICSR §5.1.1
mret                         #: drop to S at mepc. | RVP-MACHINE §2.1.3.2
addi x6, x0, -1              #: the largest compare value. | RVI-RV32I §1.1.4
csrrw x0, stimecmp, x6       #: time has not reached it. | RVP-SUPERVISOR §11.1.1.12
addi x11, x0, -1             #: a sentinel the read must replace. | RVI-RV32I §1.1.4
csrrs x11, sip, x0           #: time below stimecmp, treated as unsigned: nothing is pending, and -1 is not read as a past time. | RVP-SUPERVISOR §11.1.1.12 (boundary: not pending below the compare)
csrrw x0, stimecmp, x0       #: a compare of 0: time has reached it. | RVP-SUPERVISOR §11.1.1.12
addi x12, x0, -1             #: a sentinel the read must replace. | RVI-RV32I §1.1.4
csrrs x12, sip, x0           #: time at or above stimecmp: STIP reads set, without any M-mode action. | RVP-SUPERVISOR §11.1.1.12 (boundary: pending at the compare)
csrrsi x0, sstatus, 2        #: SIE <- 1, with sie.STIE still clear. | RVP-SUPERVISOR §11.1.1.1
addi x13, x0, 77             #: this retires in sequence: pending and globally enabled, but STIE clear suppresses it. | RVP-SUPERVISOR §11.1.1.3 (boundary: suppressed, STIE clear)
csrrci x0, sstatus, 2        #: SIE <- 0. | RVP-SUPERVISOR §11.1.1.1
addi x4, x0, 32              #: bit 5. | RVI-RV32I §1.1.4
csrrs x0, sie, x4            #: STIE <- 1, with SIE clear. | RVP-SUPERVISOR §11.1.1.3
addi x14, x0, 78             #: this retires in sequence: pending and enabled, but SIE clear suppresses it in S. | RVP-SUPERVISOR §11.1.1.3 (boundary: suppressed, SIE clear in S)
addi x27, x0, -1             #: a sentinel the S handler's cause read must replace. | RVI-RV32I §1.1.4
csrrsi x0, sstatus, 2        #: SIE <- 1: every condition now holds, and an explicit CSR write is where they are evaluated. | RVP-SUPERVISOR §11.1.1.3
addi x15, x0, 79             #: S's handler ran first, and returned here: this is sepc. | RVP-SUPERVISOR §11.1.1.7 (boundary: delivery returns to the next instruction)
addi x27, x0, -1             #: re-arm the cause sentinel. | RVI-RV32I §1.1.4
addi x16, x0, 0              #: the count of instructions retired on the way to the schedule. | RVI-RV32I §1.1.4
rdtime x17                   #: S reads the time: TM is set. | RVI-ZICNTR §6.1.1; RVP-MACHINE §2.1.1.11
addi x17, x17, 8             #: eight ticks from now. | RVI-RV32I §1.1.4
csrrw x0, stimecmp, x17      #: the kernel schedules its own timer interrupt. | RVP-SUPERVISOR §11.1.1.12
addi x16, x16, 1             #: on the way to the schedule (1). | RVI-RV32I §1.1.4
addi x16, x16, 1             #: on the way to the schedule (2). | RVI-RV32I §1.1.4
addi x16, x16, 1             #: on the way to the schedule (3). | RVI-RV32I §1.1.4
addi x16, x16, 1             #: on the way to the schedule (4). | RVI-RV32I §1.1.4
addi x16, x16, 1             #: on the way to the schedule (5). | RVI-RV32I §1.1.4
addi x16, x16, 1             #: on the way to the schedule (6). | RVI-RV32I §1.1.4
addi x16, x16, 1             #: on the way to the schedule (7). | RVI-RV32I §1.1.4
addi x16, x16, 1             #: on the way to the schedule (8). | RVI-RV32I §1.1.4
addi x16, x16, 1             #: on the way to the schedule (9). | RVI-RV32I §1.1.4
addi x16, x16, 1             #: on the way to the schedule (10). | RVI-RV32I §1.1.4
addi x16, x16, 1             #: on the way to the schedule (11). | RVI-RV32I §1.1.4
addi x16, x16, 1             #: on the way to the schedule (12). | RVI-RV32I §1.1.4
ecall                        #: back to M; SIE and STIE stay set. | RVP-MACHINE §2.1.1.15
csrrw x0, stimecmp, x0       #: pending again, from M. | RVP-SUPERVISOR §11.1.1.12
csrrsi x0, mstatus, 8        #: MIE <- 1: M's interrupts are globally enabled. | RVP-MACHINE §2.1.1.6
addi x18, x0, 80             #: this retires in sequence: a delegated interrupt never traps to M. | RVP-MACHINE §2.1.1.8 (boundary: suppressed, delegated and in M)
addi x19, x0, -1             #: a sentinel the read must replace. | RVI-RV32I §1.1.4
csrrs x19, sip, x0           #: it is still pending: the suppression hid nothing. | RVP-SUPERVISOR §11.1.1.12
csrrci x0, mstatus, 8        #: MIE <- 0. | RVP-MACHINE §2.1.1.6
addi x27, x0, -1             #: re-arm the cause sentinel. | RVI-RV32I §1.1.4
csrrw x0, mstatus, x0        #: MPP <- U; SIE and MIE clear. | RVP-MACHINE §2.1.1.6
auipc x4, 0                  #: the entry base. | RVI-RV32I §1.1.4
addi x4, x4, 16              #: the instruction after mret. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4           #: mepc <- the entry. | RVI-ZICSR §5.1.1
mret                         #: drop to U at mepc. | RVP-MACHINE §2.1.3.2
addi x22, x0, 81             #: S's handler ran before this: below S the interrupt is taken whatever sstatus.SIE says. | RVP-SUPERVISOR §11.1.1.3 (boundary: delivered from U, SIE clear)
ecall                        #: back to M. | RVP-MACHINE §2.1.1.15
csrrw x0, mideleg, x0        #: the interrupt is M's again. | RVP-MACHINE §2.1.1.8
addi x30, x0, -1             #: re-arm the M cause sentinel. | RVI-RV32I §1.1.4
addi x3, x0, 1               #: 1 ... | RVI-RV32I §1.1.4
slli x3, x3, 11              #: ... at bit 11: mstatus.MPP = S. | RVI-RV64I §3.1.2.1
csrrw x0, mstatus, x3        #: MPP <- S; SIE and MIE clear. | RVP-MACHINE §2.1.1.6
auipc x4, 0                  #: the entry base. | RVI-RV32I §1.1.4
addi x4, x4, 16              #: the instruction after mret. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4           #: mepc <- the entry. | RVI-ZICSR §5.1.1
mret                         #: drop to S at mepc. | RVP-MACHINE §2.1.3.2
csrrw x0, stimecmp, x0       #: pending; below M, undelegated, and mie.STIE set: M takes it. | RVP-SUPERVISOR §11.1.1.12; RVP-MACHINE §2.1.1.8
addi x23, x0, 82             #: M's handler ran first, and returned here. | RVP-MACHINE §2.1.1.14 (boundary: delivered to M, not delegated)
ecall                        #: back to M. | RVP-MACHINE §2.1.1.15
lui x4, 0x80000              #: bit 31, sign-extended up to bit 63: the pattern that sets menvcfg.STCE. | RVI-RV32I §1.1.4
csrrc x0, menvcfg, x4        #: STCE <- 0. | RVP-MACHINE §2.1.1.18
csrrw x0, stimecmp, x0       #: M may still write the compare, which no longer drives anything. | RVP-MACHINE §2.1.1.18
addi x4, x0, 32              #: bit 5. | RVI-RV32I §1.1.4
csrrw x0, mideleg, x4        #: delegated again. | RVP-MACHINE §2.1.1.8
addi x3, x0, 1               #: 1 ... | RVI-RV32I §1.1.4
slli x3, x3, 11              #: ... at bit 11: mstatus.MPP = S. | RVI-RV64I §3.1.2.1
csrrw x0, mstatus, x3        #: MPP <- S; SIE and MIE clear. | RVP-MACHINE §2.1.1.6
auipc x4, 0                  #: the entry base. | RVI-RV32I §1.1.4
addi x4, x4, 16              #: the instruction after mret. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4           #: mepc <- the entry. | RVI-ZICSR §5.1.1
mret                         #: drop to S at mepc. | RVP-MACHINE §2.1.3.2
csrrsi x0, sstatus, 2        #: SIE <- 1, STIE still set: only the compare is missing. | RVP-SUPERVISOR §11.1.1.1
addi x12, x0, -1             #: a sentinel the read must replace. | RVI-RV32I §1.1.4
csrrs x12, sip, x0           #: STCE clear: STIP reverts to its other definition, and nothing set it. The compare says pending; sip does not. | RVP-MACHINE §2.1.1.18 (boundary: suppressed, STCE clear)
addi x13, x0, 83             #: this retires in sequence: nothing is pending, so nothing is delivered. The budget ends here. | RVP-MACHINE §2.1.1.18
beq x0, x0, 0                #: never reached under the case's configuration; under any other, a run that took a different route stays here rather than falling into a handler. | RVI-RV32I §1.1.5
s_handler:
addi x24, x0, -1             #: a sentinel the read must replace. | RVI-RV32I §1.1.4
csrrs x27, scause, x0        #: the S handler: Interrupt bit, cause 5. | RVP-SUPERVISOR §11.1.1.8
csrrs x26, sepc, x0          #: the next instruction the interrupted code would have run. | RVP-SUPERVISOR §11.1.1.7
csrrs x25, sstatus, x0       #: where it came from. | RVP-SUPERVISOR §11.1.1.1
andi x25, x25, 256           #: SPP: 1 from S, 0 from U. | RVP-SUPERVISOR §11.1.1.1
addi x31, x16, 0             #: the count so far, when a schedule is what fired. | RVI-RV32I §1.1.4
addi x6, x0, -1              #: the largest compare value. | RVI-RV32I §1.1.4
csrrw x0, stimecmp, x6       #: writing a compare above time clears the interrupt: S acknowledges its own timer. | RVP-MACHINE §2.1.1.9
csrrs x24, sip, x0           #: cleared, without any M-mode action. | RVP-SUPERVISOR §11.1.1.12 (boundary: cleared by writing stimecmp)
sret                         #: back to the interrupted code; SIE restored from SPIE. | RVP-MACHINE §2.1.3.2
m_handler:
csrrs x30, mcause, x0        #: the M handler: the cause. | RVP-MACHINE §2.1.1.15
blt x30, x0, m_interrupt     #: an interrupt has the top bit set: it resumes where it was, not past it. | RVP-MACHINE §2.1.1.15
csrrs x29, mepc, x0          #: mepc is the trapping instruction's own address. | RVP-MACHINE §2.1.1.14
addi x29, x29, 4             #: step past it. | RVI-RV32I §1.1.4
csrrw x0, mepc, x29          #: mepc <- the next instruction. | RVI-ZICSR §5.1.1
beq x30, x28, m_return       #: a refused access returns to the mode it came from. | RVI-RV32I §1.1.5
addi x3, x0, 3               #: 3 ... | RVI-RV32I §1.1.4
slli x3, x3, 11              #: ... at bits 12:11: an environment call returns to M. | RVI-RV64I §3.1.2.1
csrrs x0, mstatus, x3        #: MPP <- M. | RVI-ZICSR §5.1.1
m_return:
mret                         #: back, at mepc. | RVP-MACHINE §2.1.3.2
m_interrupt:
csrrs x29, mepc, x0          #: the next instruction the interrupted code would have run. | RVP-MACHINE §2.1.1.14
addi x6, x0, -1              #: the largest compare value. | RVI-RV32I §1.1.4
csrrw x0, stimecmp, x6       #: clear it; M owns it now. | RVP-MACHINE §2.1.1.9
mret                         #: back to S, at mepc. | RVP-MACHINE §2.1.3.2
