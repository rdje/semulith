auipc x1, 0                  #: the handler's base: this instruction's own address, {new}. | RVI-RV32I §1.1.4
addi x1, x1, 372         #: the handler sits after the main body, at {new}. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1          #: direct-mode mtvec = the handler; no GPR written. | RVP-MACHINE §2.1.5
lui x31, 0x2                 #: bit 13: mstatus.FS = Initial, so the FP CSRs are accessible: {new}. | RVP-MACHINE §2.1.1.6.7
csrrs x0, mstatus, x31       #: set FS; no GPR written. | RVI-ZICSR §5.1.1
addi x6, x0, -1              #: a sentinel the read of mhartid must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x6, mhartid, x0        #: mhartid is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x7, x0, -1              #: a sentinel the read of misa must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x7, misa, x0           #: misa is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x8, x0, -1              #: a sentinel the read of mstatus must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x8, mstatus, x0        #: mstatus is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x9, x0, -1              #: a sentinel the read of mtvec must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x9, mtvec, x0          #: mtvec is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x10, x0, -1             #: a sentinel the read of medeleg must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x10, medeleg, x0       #: medeleg is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x11, x0, -1             #: a sentinel the read of mideleg must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x11, mideleg, x0       #: mideleg is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x12, x0, -1             #: a sentinel the read of mie must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x12, mie, x0           #: mie is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x13, x0, -1             #: a sentinel the read of mip must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x13, mip, x0           #: mip is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x14, x0, -1             #: a sentinel the read of mscratch must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x14, mscratch, x0      #: mscratch is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x15, x0, -1             #: a sentinel the read of mepc must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x15, mepc, x0          #: mepc is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x16, x0, -1             #: a sentinel the read of mcause must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x16, mcause, x0        #: mcause is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x17, x0, -1             #: a sentinel the read of mtval must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x17, mtval, x0         #: mtval is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x18, x0, -1             #: a sentinel the read of menvcfg must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x18, menvcfg, x0       #: menvcfg is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x19, x0, -1             #: a sentinel the read of mcounteren must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x19, mcounteren, x0    #: mcounteren is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x20, x0, -1             #: a sentinel the read of sstatus must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x20, sstatus, x0       #: sstatus is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x21, x0, -1             #: a sentinel the read of stvec must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x21, stvec, x0         #: stvec is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x22, x0, -1             #: a sentinel the read of sscratch must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x22, sscratch, x0      #: sscratch is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x23, x0, -1             #: a sentinel the read of sepc must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x23, sepc, x0          #: sepc is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x24, x0, -1             #: a sentinel the read of scause must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x24, scause, x0        #: scause is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x25, x0, -1             #: a sentinel the read of stval must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x25, stval, x0         #: stval is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x26, x0, -1             #: a sentinel the read of sie must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x26, sie, x0           #: sie is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x27, x0, -1             #: a sentinel the read of sip must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x27, sip, x0           #: sip is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x5, x0, -1              #: a sentinel the read of scounteren must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x5, scounteren, x0     #: scounteren is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x6, x0, -1              #: a sentinel the read of satp must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x6, satp, x0           #: satp is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x7, x0, -1              #: a sentinel the read of stimecmp must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x7, stimecmp, x0       #: stimecmp is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x8, x0, -1              #: a sentinel the read of fflags must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x8, fflags, x0         #: fflags is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x9, x0, -1              #: a sentinel the read of frm must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x9, frm, x0            #: frm is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x10, x0, -1             #: a sentinel the read of fcsr must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x10, fcsr, x0          #: fcsr is implemented: its reset value {new} replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
csrrsi x0, mideleg, 2        #: delegate the supervisor software interrupt so sie's SSIE bit is writable (undelegated sie bits read as zero). | RVP-MACHINE §2.1.1.9
csrrsi x0, sie, 2            #: write mie.SSIE THROUGH the sie view. | RVP-SUPERVISOR §1.1.3
addi x11, x0, -1             #: sentinel. | RVI-RV32I §1.1.4
csrrs x11, mie, x0           #: mie shows the bit written through sie: {new} — one register, two names. | RVP-SUPERVISOR §1.1.3
csrrsi x0, sstatus, 2        #: write mstatus.SIE THROUGH the sstatus view. | RVP-SUPERVISOR §1.1.1
addi x12, x0, -1             #: sentinel. | RVI-RV32I §1.1.4
csrrs x12, mstatus, x0       #: mstatus shows SIE set through sstatus (with FS = Initial): {new}. | RVP-SUPERVISOR §1.1.1
csrrwi x0, fflags, 31        #: all five accrued flags through the fflags view. | RVI-F §20.1.2
csrrwi x0, frm, 4            #: rounding mode RMM through the frm view. | RVI-F §20.1.2
addi x13, x0, -1             #: sentinel. | RVI-RV32I §1.1.4
csrrs x13, fcsr, x0          #: fcsr composes the two: frm above fflags, {new}. | RVI-F §20.1.2
addi x14, x0, -1             #: sentinel. | RVI-RV32I §1.1.4
csrrs x14, mstatus, x0       #: the FP CSR writes made FS Dirty and SD summarizes it: {new}. | RVP-MACHINE §2.1.1.6.7
addi x5, x0, 7               #: the sentinel the refused write must leave untouched. | RVI-RV32I §1.1.4
addi x6, x0, 9               #: a value to (try to) write. | RVI-RV32I §1.1.4
csrrw x5, mhartid, x6        #: a write to the read-only mhartid: illegal-instruction, rd untouched; the handler records cause 2. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x15, x0, -1             #: sentinel. | RVI-RV32I §1.1.4
csrrs x15, mhartid, x0       #: mhartid preserved its value through the refused write: {new}. | RVP-MACHINE §2.1.1.4
addi x3, x0, 1               #: 1 … | RVI-RV32I §1.1.4
slli x3, x3, 11              #: … at bit 11: mstatus.MPP = S: {new}. | RVI-RV64I §3.1.2.1
csrrs x0, mstatus, x3        #: MPP <- S. | RVI-ZICSR §5.1.1
auipc x4, 0                  #: the S-mode entry base: {new}. | RVI-RV32I §1.1.4
addi x4, x4, 16              #: the instruction after mret: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4           #: mepc <- the S-mode entry. | RVI-ZICSR §5.1.1
mret                         #: drop to S at mepc. | RVP-INSNS §3.3.2 (mret)
addi x16, x0, -1             #: sentinel (in S). | RVI-RV32I §1.1.4
csrrs x16, sstatus, x0       #: sstatus is readable in S: {new} (SD, FS Dirty, SIE — mstatus's supervisor view). | RVP-SUPERVISOR §1.1.1
addi x17, x0, -1             #: the sentinel the privilege-refused access must leave untouched. | RVI-RV32I §1.1.4
addi x30, x0, -1             #: a sentinel the handler's cause read must replace (the first trap left 2 there). | RVI-RV32I §1.1.4
csrrs x17, mscratch, x0      #: an M-level CSR from S: illegal-instruction before any effect; the handler (in M) records cause 2 and returns to S. | RVP-CSR §1.1.1; RVI-ZICSR §5.1.1
addi x18, x0, -1             #: sentinel (in S). | RVI-RV32I §1.1.4
csrrs x18, sscratch, x0      #: the supervisor's own scratch is readable in S: {new}. | RVP-SUPERVISOR §1.1.4
csrrs x30, mcause, x0        #: the handler: the cause, {new}. | RVP-MACHINE §2.1.3.1
csrrs x29, mepc, x0          #: mepc is the refused instruction's own address: {new}. | RVP-MACHINE §2.1.3.1
addi x29, x29, 4             #: step past it: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x29          #: mepc <- the next instruction. | RVI-ZICSR §5.1.1
mret                         #: back to the mode the trap came from, at mepc. | RVP-INSNS §3.3.2 (mret)
