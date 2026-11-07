auipc x1, 0                    #: the base for the handler: {new}. | RVI-RV64I §3.1.2.1
addi x1, x1, 16                #: the handler, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1            #: mtvec = the handler; no GPR written. | RVP-MACHINE §2.1.1.7
jal x0, 20                     #: past the handler; x0 discards the link. | RVI-RV32I §1.1.5.1
csrrs x30, mcause, x0          #: the handler reads mcause: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.15; RVP-MACHINE §2.1.3.2
csrrs x29, mtval, x0           #: and mtval: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.16
csrrs x28, mepc, x0            #: and mepc, the instruction's own address: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.14
jalr x0, x27, 0                #: on, to where x27 says, still in M. | RVI-RV32I §1.1.5.1
addi x25, x0, 3                #: both MPP bits: {new}. | RVI-RV32I §1.1.4
slli x25, x25, 11              #: at bit 11, kept in x25: {new}. | RVI-RV64I §3.1.2.1
addi x19, x0, 1                #: MPP = S: {new}. | RVI-RV32I §1.1.4
slli x19, x19, 11              #: at bit 11, kept in x19: {new}. | RVI-RV64I §3.1.2.1
addi x6, x0, 128               #: mstatus.MPIE's bit: {new}. | RVI-RV32I §1.1.4
csrrs x0, mstatus, x6          #: MPIE = 1, with MIE = 0; no GPR written. | RVP-MACHINE §2.1.1.6
csrrc x0, mstatus, x25         #: MPP cleared; no GPR written. | RVI-ZICSR §5.1.1
csrrs x0, mstatus, x25         #: MPP set; no GPR written. | RVI-ZICSR §5.1.1
auipc x4, 0                    #: the base for mret's target: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16                #: the row after mret, in M: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4             #: mepc = there; no GPR written. | RVP-MACHINE §2.1.1.14
mret                           #: mret in M: its own mode, so it executes. | RVP-MACHINE §2.1.3.2; RVP-INSNS §18.1
auipc x7, 0                    #: the row mepc named: {new}. | RVP-MACHINE §2.1.3.2; RVP-INSNS §18.1
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x8, mstatus, x0          #: what mret left: {new}. | RVP-MACHINE §2.1.3.2; RVP-MACHINE §2.1.1.6 (boundary: mret pops the stack)
addi x6, x0, 8                 #: MIE's bit: {new}. | RVI-RV32I §1.1.4
csrrc x0, mstatus, x6          #: MIE cleared again; no GPR written. | RVP-MACHINE §2.1.1.6
addi x6, x0, 1                 #: MPRV: {new}. | RVI-RV32I §1.1.4
slli x6, x6, 17                #: MPRV: {new}. | RVI-RV64I §3.1.2.1
csrrs x0, mstatus, x6          #: set in mstatus; no GPR written. | RVP-MACHINE §2.1.1.6
csrrc x0, mstatus, x25         #: MPP cleared; no GPR written. | RVI-ZICSR §5.1.1
csrrs x0, mstatus, x19         #: MPP set; no GPR written. | RVI-ZICSR §5.1.1
auipc x4, 0                    #: the base for the next mode's entry: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16                #: its entry, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4             #: mepc = there; no GPR written. | RVI-ZICSR §5.1.1
mret                           #: there. | RVP-MACHINE §2.1.3.2
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
ecall                          #: S comes back, so M can read what mret left. | RVP-MACHINE §2.1.3.1
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x8, mstatus, x0          #: MPRV, after a target that was not M: {new}. | RVP-MACHINE §2.1.3.2; RVP-MACHINE §2.1.1.6 (boundary: mret clears MPRV)
csrrc x0, mstatus, x25         #: MPP cleared; no GPR written. | RVI-ZICSR §5.1.1
csrrs x0, mstatus, x19         #: MPP set; no GPR written. | RVI-ZICSR §5.1.1
auipc x4, 0                    #: the base for the next mode's entry: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16                #: its entry, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4             #: mepc = there; no GPR written. | RVI-ZICSR §5.1.1
mret                           #: there. | RVP-MACHINE §2.1.3.2
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
mret                           #: mret in S: below its mode. | RVP-MACHINE §2.1.3.2; RVP-INSNS §18.1
csrrc x0, mstatus, x25         #: MPP cleared; no GPR written. | RVI-ZICSR §5.1.1
auipc x4, 0                    #: the base for the next mode's entry: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16                #: its entry, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4             #: mepc = there; no GPR written. | RVI-ZICSR §5.1.1
mret                           #: there. | RVP-MACHINE §2.1.3.2
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
mret                           #: mret in U: below its mode. | RVP-MACHINE §2.1.3.2; RVP-INSNS §18.1
csrrc x0, mstatus, x25         #: MPP cleared; no GPR written. | RVI-ZICSR §5.1.1
auipc x4, 0                    #: the base for the next mode's entry: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16                #: its entry, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4             #: mepc = there; no GPR written. | RVI-ZICSR §5.1.1
mret                           #: there. | RVP-MACHINE §2.1.3.2
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
sret                           #: sret in U: below its mode. | RVP-MACHINE §2.1.3.2; RVP-INSNS §18.1
addi x6, x0, 288               #: SPIE and SPP: {new}. | RVI-RV32I §1.1.4
csrrs x0, sstatus, x6          #: set in sstatus; no GPR written. | RVP-SUPERVISOR §11.1.1.1
csrrc x0, mstatus, x25         #: MPP cleared; no GPR written. | RVI-ZICSR §5.1.1
csrrs x0, mstatus, x19         #: MPP set; no GPR written. | RVI-ZICSR §5.1.1
auipc x4, 0                    #: the base for the next mode's entry: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16                #: its entry, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4             #: mepc = there; no GPR written. | RVI-ZICSR §5.1.1
mret                           #: there. | RVP-MACHINE §2.1.3.2
auipc x4, 0                    #: the base for sret's target: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16                #: the row after sret: {new}. | RVI-RV32I §1.1.4
csrrw x0, sepc, x4             #: sepc = there; no GPR written. | RVP-SUPERVISOR §11.1.1.7
sret                           #: sret in S, with TSR clear: it executes. | RVP-MACHINE §2.1.3.2; RVP-INSNS §18.1
auipc x7, 0                    #: the row sepc named: {new}. | RVP-MACHINE §2.1.3.2; RVP-INSNS §18.1
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x8, sstatus, x0          #: what sret left: {new}. | RVP-MACHINE §2.1.3.2; RVP-SUPERVISOR §11.1.1.1 (boundary: sret pops the stack)
addi x6, x0, 2                 #: SIE's bit: {new}. | RVI-RV32I §1.1.4
csrrc x0, sstatus, x6          #: SIE cleared again; no GPR written. | RVP-SUPERVISOR §11.1.1.1
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
ecall                          #: back to M. | RVP-MACHINE §2.1.3.1
addi x6, x0, 1                 #: TSR: {new}. | RVI-RV32I §1.1.4
slli x6, x6, 22                #: TSR: {new}. | RVI-RV64I §3.1.2.1
csrrs x0, mstatus, x6          #: set in mstatus; no GPR written. | RVP-MACHINE §2.1.1.6.6
csrrc x0, mstatus, x25         #: MPP cleared; no GPR written. | RVI-ZICSR §5.1.1
csrrs x0, mstatus, x19         #: MPP set; no GPR written. | RVI-ZICSR §5.1.1
auipc x4, 0                    #: the base for the next mode's entry: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16                #: its entry, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4             #: mepc = there; no GPR written. | RVI-ZICSR §5.1.1
mret                           #: there. | RVP-MACHINE §2.1.3.2
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
sret                           #: sret in S with TSR set. | RVP-MACHINE §2.1.3.2; RVP-MACHINE §2.1.1.6.6
auipc x4, 0                    #: the base for sret's target: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16                #: the row after sret: {new}. | RVI-RV32I §1.1.4
csrrw x0, sepc, x4             #: sepc = there; no GPR written. | RVP-SUPERVISOR §11.1.1.7
sret                           #: sret in M, with TSR set: TSR binds S only, so it executes, on to U. | RVP-MACHINE §2.1.3.2; RVP-MACHINE §2.1.1.6.6
auipc x7, 0                    #: the row sepc named, in U: {new}. | RVP-MACHINE §2.1.3.2; RVP-MACHINE §2.1.1.6.6
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
ecall                          #: back to M. | RVP-MACHINE §2.1.3.1
addi x6, x0, 1                 #: TSR: {new}. | RVI-RV32I §1.1.4
slli x6, x6, 22                #: TSR: {new}. | RVI-RV64I §3.1.2.1
csrrc x0, mstatus, x6          #: cleared in mstatus; no GPR written. | RVP-MACHINE §2.1.1.6.6
addi x6, x0, 2                 #: SIE's bit, and SSIP's and SSIE's: {new}. | RVI-RV32I §1.1.4
csrrc x0, sstatus, x6          #: SIE clear; no GPR written. | RVP-SUPERVISOR §11.1.1.1
csrrs x0, mie, x6              #: the software interrupt enabled locally; no GPR written. | RVP-MACHINE §2.1.1.9
csrrs x0, mip, x6              #: and pending, not delegated; no GPR written. | RVP-MACHINE §2.1.1.9
wfi                            #: wfi in M with MIE clear and nothing delegated: pending and locally enabled, so it wakes at once. | RVP-MACHINE §2.1.3.3; RVP-INSNS §18.1
addi x9, x0, 1                 #: the row after it ran: {new}. | RVI-RV32I §1.1.4 (boundary: a wake, at any level)
csrrs x0, mideleg, x6          #: now delegated to S; no GPR written. | RVP-MACHINE §2.1.1.8
wfi                            #: wfi in M again, delegated this time. | RVP-MACHINE §2.1.3.3; RVP-INSNS §18.1
addi x9, x0, 2                 #: the row after it ran: {new}. | RVI-RV32I §1.1.4
csrrc x0, mstatus, x25         #: MPP cleared; no GPR written. | RVI-ZICSR §5.1.1
csrrs x0, mstatus, x19         #: MPP set; no GPR written. | RVI-ZICSR §5.1.1
auipc x4, 0                    #: the base for the next mode's entry: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16                #: its entry, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4             #: mepc = there; no GPR written. | RVI-ZICSR §5.1.1
mret                           #: there. | RVP-MACHINE §2.1.3.2
wfi                            #: wfi in S, TW clear and SIE clear: it wakes at once, and no trap is taken. | RVP-MACHINE §2.1.3.3; RVP-INSNS §18.1
addi x9, x0, 3                 #: the row after it ran: {new}. | RVI-RV32I §1.1.4 (boundary: wfi in S)
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
ecall                          #: back to M. | RVP-MACHINE §2.1.3.1
addi x6, x0, 2                 #: SSIP's bit: {new}. | RVI-RV32I §1.1.4
csrrc x0, mip, x6              #: no longer pending; no GPR written. | RVP-MACHINE §2.1.1.9
csrrc x0, mie, x6              #: nor enabled; no GPR written. | RVP-MACHINE §2.1.1.9
addi x6, x0, 1                 #: TW: {new}. | RVI-RV32I §1.1.4
slli x6, x6, 21                #: TW: {new}. | RVI-RV64I §3.1.2.1
csrrs x0, mstatus, x6          #: set in mstatus; no GPR written. | RVP-MACHINE §2.1.1.6.6
csrrc x0, mstatus, x25         #: MPP cleared; no GPR written. | RVI-ZICSR §5.1.1
csrrs x0, mstatus, x19         #: MPP set; no GPR written. | RVI-ZICSR §5.1.1
auipc x4, 0                    #: the base for the next mode's entry: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16                #: its entry, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4             #: mepc = there; no GPR written. | RVI-ZICSR §5.1.1
mret                           #: there. | RVP-MACHINE §2.1.3.2
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
wfi                            #: wfi in S with TW set, and nothing pending to complete it. | RVP-MACHINE §2.1.3.3; RVP-MACHINE §2.1.1.6.6
addi x6, x0, 1                 #: TW: {new}. | RVI-RV32I §1.1.4
slli x6, x6, 21                #: TW: {new}. | RVI-RV64I §3.1.2.1
csrrc x0, mstatus, x6          #: cleared in mstatus; no GPR written. | RVP-MACHINE §2.1.1.6.6
csrrc x0, mstatus, x25         #: MPP cleared; no GPR written. | RVI-ZICSR §5.1.1
auipc x4, 0                    #: the base for the next mode's entry: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16                #: its entry, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4             #: mepc = there; no GPR written. | RVI-ZICSR §5.1.1
mret                           #: there. | RVP-MACHINE §2.1.3.2
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
wfi                            #: wfi in U, with S present. | RVP-MACHINE §2.1.3.3; RVP-INSNS §18.1
csrrc x0, mstatus, x25         #: MPP cleared; no GPR written. | RVI-ZICSR §5.1.1
auipc x4, 0                    #: the base for the next mode's entry: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16                #: its entry, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4             #: mepc = there; no GPR written. | RVI-ZICSR §5.1.1
mret                           #: there. | RVP-MACHINE §2.1.3.2
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
sfence.vma x0, x0              #: sfence.vma in U. | RVP-SUPERVISOR §11.1.2.1; RVP-INSNS §18.1
addi x6, x0, 1                 #: TVM: {new}. | RVI-RV32I §1.1.4
slli x6, x6, 20                #: TVM: {new}. | RVI-RV64I §3.1.2.1
csrrs x0, mstatus, x6          #: set in mstatus; no GPR written. | RVP-MACHINE §2.1.1.6.6
csrrc x0, mstatus, x25         #: MPP cleared; no GPR written. | RVI-ZICSR §5.1.1
csrrs x0, mstatus, x19         #: MPP set; no GPR written. | RVI-ZICSR §5.1.1
auipc x4, 0                    #: the base for the next mode's entry: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16                #: its entry, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4             #: mepc = there; no GPR written. | RVI-ZICSR §5.1.1
mret                           #: there. | RVP-MACHINE §2.1.3.2
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
sfence.vma x0, x0              #: sfence.vma in S with TVM set. | RVP-SUPERVISOR §11.1.2.1; RVP-MACHINE §2.1.1.6.6
addi x6, x0, 1                 #: TVM: {new}. | RVI-RV32I §1.1.4
slli x6, x6, 20                #: TVM: {new}. | RVI-RV64I §3.1.2.1
csrrc x0, mstatus, x6          #: cleared in mstatus; no GPR written. | RVP-MACHINE §2.1.1.6.6
addi x10, x0, 1                #: raw material for the region base. | RVI-RV32I §1.1.4
slli x10, x10, 31              #: 0x80000000: {new}. | RVI-RV64I §3.1.2.1
lui x1, 7                      #: 0x7000: {new}. | RVI-RV64I §3.1.2.1
add x1, x1, x10                #: the data cell, on a page of its own, past this program: {new}. | RVI-RV32I §1.1.4
addi x7, x0, 66                #: what the first page holds: {new}. | RVI-RV32I §1.1.4
sd x7, 0, x1                   #: the first data page holds 66. | RVI-RV64I §3.1.3
lui x15, 1                     #: one page: {new}. | RVI-RV64I §3.1.2.1
add x15, x15, x1               #: the second data page: {new}. | RVI-RV32I §1.1.4
addi x7, x0, 88                #: what the second holds: {new}. | RVI-RV32I §1.1.4
sd x7, 0, x15                  #: the second data page holds 88. | RVI-RV64I §3.1.3
lui x11, 3                     #: 0x3000: {new}. | RVI-RV64I §3.1.2.1
add x11, x11, x10              #: the root table: {new}. | RVI-RV32I §1.1.4
lui x12, 0x20001               #: the pointer's upper bits: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 1               #: root[0] points at base+0x4000: {new}. | RVP-SUPERVISOR §11.1.4.1
sd x12, 0, x11                 #: root[0] written. | RVI-RV64I §3.1.3
lui x12, 0x20000               #: the leaf's upper bits: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 207             #: root[2] is a 1 GiB leaf, VA = PA, R, W, X, A and D: {new}. | RVP-SUPERVISOR §11.1.4.1
sd x12, 16, x11                #: root[2] written. | RVI-RV64I §3.1.3
lui x11, 4                     #: 0x4000: {new}. | RVI-RV64I §3.1.2.1
add x11, x11, x10              #: the level-1 table: {new}. | RVI-RV32I §1.1.4
lui x12, 0x20001               #: the pointer's upper bits: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 1025            #: level-1[2] points at base+0x5000: {new}. | RVP-SUPERVISOR §11.1.4.1
sd x12, 16, x11                #: level-1[2] written. | RVI-RV64I §3.1.3
lui x11, 5                     #: 0x5000: {new}. | RVI-RV64I §3.1.2.1
add x11, x11, x10              #: the level-0 table: {new}. | RVI-RV32I §1.1.4
addi x12, x0, 1                #: level-0[0] maps VA 0x400000 to the first page: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 16              #: level-0[0] maps VA 0x400000 to the first page: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 1               #: level-0[0] maps VA 0x400000 to the first page: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 13              #: level-0[0] maps VA 0x400000 to the first page: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, -825            #: level-0[0] maps VA 0x400000 to the first page: {new}. | RVI-RV32I §1.1.4
sd x12, 0, x11                 #: level-0[0] written. | RVI-RV64I §3.1.3
addi x5, x0, 8                 #: raw material for satp.MODE: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 60                #: MODE = Sv39: {new}. | RVI-RV64I §3.1.2.1
lui x2, 128                    #: the root's page number: {new}. | RVI-RV64I §3.1.2.1
addi x2, x2, 3                 #: 0x80003, the root: {new}. | RVI-RV32I §1.1.4
or x2, x2, x5                  #: satp's value: {new}. | RVI-RV32I §1.1.4
csrrw x0, satp, x2             #: translation armed for S; M is not translated. | RVI-ZICSR §5.1.1
addi x3, x0, 3                 #: both MPP bits: {new}. | RVI-RV32I §1.1.4
slli x3, x3, 11                #: at bit 11: {new}. | RVI-RV64I §3.1.2.1
csrrc x0, mstatus, x3          #: MPP cleared; no GPR written. | RVI-ZICSR §5.1.1
addi x3, x0, 1                 #: MPP = S: {new}. | RVI-RV32I §1.1.4
slli x3, x3, 11                #: at bit 11: {new}. | RVI-RV64I §3.1.2.1
csrrs x0, mstatus, x3          #: MPP = S; no GPR written. | RVI-ZICSR §5.1.1
addi x26, x11, 0               #: level-0[0]'s address, through the identity leaf: {new}. | RVI-RV32I §1.1.4
auipc x4, 0                    #: the base for S's entry: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16                #: S's entry, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4             #: mepc = S's entry; no GPR written. | RVI-ZICSR §5.1.1
mret                           #: to S, with translation on. | RVP-MACHINE §2.1.3.2
lui x13, 0x400                 #: VA 0x400000: {new}. | RVI-RV64I §3.1.2.1
addi x24, x0, 0                #: a nonzero register holding ASID 0: {new}. | RVI-RV32I §1.1.4
addi x18, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x18, x13, 0                 #: the first page: {new}. | RVP-SUPERVISOR §11.1.2.1
addi x12, x0, 1                #: the other mapping: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 16              #: the other mapping: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 1               #: the other mapping: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 13              #: the other mapping: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 199             #: the other mapping: {new}. | RVI-RV32I §1.1.4
sd x12, 0, x26                 #: the PTE rewritten. | RVP-SUPERVISOR §11.1.4.1
sfence.vma x0, x0              #: rs1 = x0 and rs2 = x0: every entry. | RVP-SUPERVISOR §11.1.2.1
addi x18, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x18, x13, 0                 #: the same VA, after the fence: {new}. | RVP-SUPERVISOR §11.1.2.1 (boundary: sfence.vma x0, x0)
addi x12, x0, 1                #: the other mapping: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 16              #: the other mapping: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 1               #: the other mapping: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 13              #: the other mapping: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, -825            #: the other mapping: {new}. | RVI-RV32I §1.1.4
sd x12, 0, x26                 #: the PTE rewritten. | RVP-SUPERVISOR §11.1.4.1
sfence.vma x13, x0             #: rs1 = the VA and rs2 = x0: that page. | RVP-SUPERVISOR §11.1.2.1
addi x18, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x18, x13, 0                 #: the same VA, after the fence: {new}. | RVP-SUPERVISOR §11.1.2.1 (boundary: sfence.vma x13, x0)
addi x12, x0, 1                #: the other mapping: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 16              #: the other mapping: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 1               #: the other mapping: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 13              #: the other mapping: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 199             #: the other mapping: {new}. | RVI-RV32I §1.1.4
sd x12, 0, x26                 #: the PTE rewritten. | RVP-SUPERVISOR §11.1.4.1
sfence.vma x0, x24             #: rs1 = x0 and rs2 names an ASID: that ASID. | RVP-SUPERVISOR §11.1.2.1
addi x18, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x18, x13, 0                 #: the same VA, after the fence: {new}. | RVP-SUPERVISOR §11.1.2.1 (boundary: sfence.vma x0, x24)
addi x12, x0, 1                #: the other mapping: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 16              #: the other mapping: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 1               #: the other mapping: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 13              #: the other mapping: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, -825            #: the other mapping: {new}. | RVI-RV32I §1.1.4
sd x12, 0, x26                 #: the PTE rewritten. | RVP-SUPERVISOR §11.1.4.1
sfence.vma x13, x24            #: rs1 = the VA and rs2 names an ASID: that page in that ASID. | RVP-SUPERVISOR §11.1.2.1
addi x18, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x18, x13, 0                 #: the same VA, after the fence: {new}. | RVP-SUPERVISOR §11.1.2.1 (boundary: sfence.vma x13, x24)
c.nop                          #: the end of the program. | RVI-C §27.1.8
