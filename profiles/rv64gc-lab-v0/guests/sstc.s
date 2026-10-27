auipc x1, 0                  #: the handler's base: this instruction's own address, {new}. | RVI-RV32I §1.1.4
addi x1, x1, 116              #: the handler sits after the main body, at {new}. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1          #: direct-mode mtvec = the handler; no GPR written. | RVP-MACHINE §2.1.5
addi x5, x0, -1              #: a sentinel the M-mode read must replace. | RVI-RV32I §1.1.4
csrrs x5, stimecmp, x0       #: in M, stimecmp is accessible with STCE and TM both clear; it resets to 0: {new}. | RVP-SSTC §2.1 (stimecmp); the state document's reset
addi x6, x0, 1               #: 1 … | RVI-RV32I §1.1.4
slli x6, x6, 40              #: … at bit 40: a 64-bit compare value, {new}. | RVI-RV64I §3.1.2.1
csrrw x0, stimecmp, x6       #: M writes the supervisor timer compare; no GPR written. | RVP-SSTC §2.1
addi x7, x0, -1              #: a sentinel the read-back must replace. | RVI-RV32I §1.1.4
csrrs x7, stimecmp, x0       #: stimecmp holds all 64 bits written: {new}. | RVP-SSTC §2.1
addi x3, x0, 1               #: 1 … | RVI-RV32I §1.1.4
slli x3, x3, 11              #: … at bit 11: mstatus.MPP = S: {new}. | RVI-RV64I §3.1.2.1
csrrs x0, mstatus, x3        #: MPP <- S. | RVI-ZICSR §5.1.1
auipc x4, 0                  #: the S-mode entry base: {new}. | RVI-RV32I §1.1.4
addi x4, x4, 16              #: the instruction after mret: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4           #: mepc <- the S-mode entry. | RVI-ZICSR §5.1.1
mret                         #: drop to S at mepc. | RVP-INSNS §3.3.2 (mret)
addi x8, x0, -1              #: a sentinel the first refused access must leave untouched. | RVI-RV32I §1.1.4
csrrs x8, stimecmp, x0       #: S access with mcounteren.TM clear: illegal-instruction before any effect; the handler (visit 1) sets TM and returns. | RVP-SSTC §2.1 (mcounteren.TM gates S access to stimecmp)
addi x30, x0, -1             #: a sentinel the handler's second cause read must replace. | RVI-RV32I §1.1.4
addi x9, x0, -1              #: a sentinel the second refused access must leave untouched. | RVI-RV32I §1.1.4
csrrs x9, stimecmp, x0       #: S access with TM set but menvcfg.STCE clear: still illegal-instruction; the handler (visit 2) sets STCE and returns. | RVP-SSTC §2.1 (menvcfg.STCE gates stimecmp outside M)
addi x10, x0, -1             #: a sentinel the now-legal read must replace. | RVI-RV32I §1.1.4
csrrs x10, stimecmp, x0      #: with TM and STCE both set, S reads stimecmp: {new} — the value M wrote. | RVP-SSTC §2.1
addi x11, x0, 1              #: 1 … | RVI-RV32I §1.1.4
slli x11, x11, 41            #: … at bit 41: the kernel's own compare value, {new}. | RVI-RV64I §3.1.2.1
csrrw x0, stimecmp, x11      #: the S-mode kernel programs its own timer — no M-mode round trip. | RVP-SSTC §1 (the extension's purpose)
addi x12, x0, -1             #: a sentinel the read-back must replace. | RVI-RV32I §1.1.4
csrrs x12, stimecmp, x0      #: S reads back what it programmed: {new}. | RVP-SSTC §2.1
csrrs x30, mcause, x0        #: the handler: the cause, {new} (2, illegal-instruction). | RVP-MACHINE §2.1.3.1
addi x27, x0, -1             #: a sentinel the flag read must replace. | RVI-RV32I §1.1.4
csrrs x27, mscratch, x0      #: the visit flag: 0 on the first visit, 1 on the second. | RVP-MACHINE §2.1.1.3
bne x27, x0, second          #: the second visit opens the second gate. | RVI-RV32I §1.1.6
addi x28, x0, 2              #: bit 1: mcounteren.TM, {new}. | RVI-RV32I §1.1.4
csrrs x0, mcounteren, x28    #: visit 1: TM <- 1 (the first gate opens). | RVP-MACHINE §2.1.1.11
addi x27, x0, 1              #: the flag's new value, {new}. | RVI-RV32I §1.1.4
csrrw x0, mscratch, x27      #: remember the visit. | RVP-MACHINE §2.1.1.3
beq x0, x0, resume           #: to the common return. | RVI-RV32I §1.1.6
second:
lui x28, 0x80000             #: bit 63: menvcfg.STCE, {new} (LUI sign-extends to bit 63). | RVI-RV64I §3.1.2.2
csrrs x0, menvcfg, x28       #: visit 2: STCE <- 1 (the second gate opens). | RVP-MACHINE §2.1.1.18; RVP-SSTC §2.1
resume:
csrrs x29, mepc, x0          #: mepc is the refused instruction's own address: {new}. | RVP-MACHINE §2.1.3.1
addi x29, x29, 4             #: step past it: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x29          #: mepc <- the next instruction. | RVI-ZICSR §5.1.1
mret                         #: back to S at mepc. | RVP-INSNS §3.3.2 (mret)
