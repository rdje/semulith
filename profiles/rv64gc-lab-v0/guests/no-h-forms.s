auipc x1, 0                    #: the base for the handler: {new}. | RVI-RV64I §3.1.2.1
addi x1, x1, 16                #: the handler, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1            #: mtvec = the handler; no GPR written. | RVP-MACHINE §2.1.1.7
jal x0, 20                     #: past the handler; x0 discards the link. | RVI-RV32I §1.1.5.1
csrrs x30, mcause, x0          #: the handler reads mcause: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.15
csrrs x29, mtval, x0           #: and mtval: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.16
csrrs x28, mepc, x0            #: and mepc, the instruction's own address: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.14
jalr x0, x27, 0                #: on, to where x27 says, still in M. | RVI-RV32I §1.1.5.1
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x5, misa, x0             #: misa's letters: H, bit 7, is not among them: {new}. | RVP-MACHINE §2.1.1.1; RVP-INTRO Introduction (boundary: misa names no H)
addi x6, x0, 3                 #: mstatus.GVA and MPV, the bits H would add: {new}. | RVI-RV32I §1.1.4
slli x6, x6, 38                #: mstatus.GVA and MPV, the bits H would add: {new}. | RVI-RV64I §3.1.2.1
csrrs x0, mstatus, x6          #: M tries to set both; no GPR written. | RVP-MACHINE §2.1.1.6
addi x7, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x7, mstatus, x0          #: they do not hold: {new}. | RVP-MACHINE §2.1.1.6 (boundary: mstatus holds no H state)
addi x8, x0, 1092              #: the virtual-supervisor interrupt bits: {new}. | RVI-RV32I §1.1.4
csrrs x0, mideleg, x8          #: M tries to delegate them; no GPR written. | RVP-MACHINE §2.1.1.8
addi x9, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x9, mideleg, x0          #: none holds: {new}. | RVP-MACHINE §2.1.1.8
csrrs x0, mie, x8              #: M tries to enable them; no GPR written. | RVP-MACHINE §2.1.1.9
addi x10, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x10, mie, x0             #: none holds: {new}. | RVP-MACHINE §2.1.1.9
addi x11, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x11, mhartid, x0         #: the one hart: {new}. | RVP-MACHINE §2.1.1.5 (boundary: one hart)
c.nop                          #: the end of the program. | RVI-C §27.1.8
