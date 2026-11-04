auipc x1, 0                  #: the handler's base: this instruction's own address. | RVI-RV32I §1.1.4
addi x1, x1, 516             #: the handler sits right after the main body. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1          #: direct-mode mtvec = the handler; no GPR written. | RVP-MACHINE §2.1.1.7
lui x31, 0x2                 #: bit 13: mstatus.FS = Initial, so the FP CSRs are accessible. | RVP-MACHINE §2.1.1.6.7
csrrs x0, mstatus, x31       #: set FS; no GPR written. | RVI-ZICSR §5.1.1
addi x6, x0, -1              #: a sentinel the read of mhartid must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x6, mhartid, x0        #: mhartid is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-MACHINE §2.1.1.5
addi x7, x0, -1              #: a sentinel the read of misa must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x7, misa, x0           #: misa is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-MACHINE §2.1.1.1
addi x8, x0, -1              #: a sentinel the read of mstatus must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x8, mstatus, x0        #: mstatus is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-MACHINE §2.1.1.6
addi x9, x0, -1              #: a sentinel the read of mtvec must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x9, mtvec, x0          #: mtvec is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-MACHINE §2.1.1.7
addi x10, x0, -1             #: a sentinel the read of medeleg must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x10, medeleg, x0       #: medeleg is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-MACHINE §2.1.1.8
addi x11, x0, -1             #: a sentinel the read of mideleg must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x11, mideleg, x0       #: mideleg is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-MACHINE §2.1.1.8
addi x12, x0, -1             #: a sentinel the read of mie must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x12, mie, x0           #: mie is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-MACHINE §2.1.1.9
csrrs x0, mip, x0            #: mip is implemented: read with rd = x0, so it writes no GPR and raises nothing; its value is compared only through the sip alias below (the reference's CLINT holds mip.MTIP, a device this laboratory does not declare). | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-MACHINE §2.1.1.9
addi x13, x0, 1              #: the marker after mip's read: it ran, so the read did not trap. | RVI-RV32I §1.1.4; RVP-MACHINE §2.1.1.9
addi x14, x0, -1             #: a sentinel the read of mscratch must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x14, mscratch, x0      #: mscratch is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-MACHINE §2.1.1.13
addi x15, x0, -1             #: a sentinel the read of mepc must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x15, mepc, x0          #: mepc is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-MACHINE §2.1.1.14
addi x16, x0, -1             #: a sentinel the read of mcause must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x16, mcause, x0        #: mcause is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-MACHINE §2.1.1.15
addi x17, x0, -1             #: a sentinel the read of mtval must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x17, mtval, x0         #: mtval is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-MACHINE §2.1.1.16
addi x18, x0, -1             #: a sentinel the read of menvcfg must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x18, menvcfg, x0       #: menvcfg is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-MACHINE §2.1.1.18
addi x19, x0, -1             #: a sentinel the read of mcounteren must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x19, mcounteren, x0    #: mcounteren is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-MACHINE §2.1.1.11
addi x20, x0, -1             #: a sentinel the read of mcycle must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x20, mcycle, x0        #: mcycle is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-MACHINE §2.1.1.10
addi x21, x0, -1             #: a sentinel the read of minstret must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x21, minstret, x0      #: minstret is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-MACHINE §2.1.1.10
addi x22, x0, -1             #: a sentinel the read of sstatus must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x22, sstatus, x0       #: sstatus is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-SUPERVISOR §11.1.1.1
addi x23, x0, -1             #: a sentinel the read of stvec must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x23, stvec, x0         #: stvec is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-SUPERVISOR §11.1.1.2
addi x24, x0, -1             #: a sentinel the read of sscratch must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x24, sscratch, x0      #: sscratch is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-SUPERVISOR §11.1.1.6
addi x25, x0, -1             #: a sentinel the read of sepc must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x25, sepc, x0          #: sepc is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-SUPERVISOR §11.1.1.7
addi x26, x0, -1             #: a sentinel the read of scause must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x26, scause, x0        #: scause is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-SUPERVISOR §11.1.1.8
addi x27, x0, -1             #: a sentinel the read of stval must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x27, stval, x0         #: stval is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-SUPERVISOR §11.1.1.9
addi x5, x0, -1              #: a sentinel the read of sie must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x5, sie, x0            #: sie is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-SUPERVISOR §11.1.1.3
addi x6, x0, -1              #: a sentinel the read of sip must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x6, sip, x0            #: sip is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-SUPERVISOR §11.1.1.3
addi x7, x0, -1              #: a sentinel the read of scounteren must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x7, scounteren, x0     #: scounteren is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-SUPERVISOR §11.1.1.5
addi x8, x0, -1              #: a sentinel the read of satp must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x8, satp, x0           #: satp is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-SUPERVISOR §11.1.1.11
addi x9, x0, -1              #: a sentinel the read of stimecmp must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x9, stimecmp, x0       #: stimecmp is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-SSTC §12.1
addi x10, x0, -1             #: a sentinel the read of cycle must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x10, cycle, x0         #: cycle is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVI-ZICNTR §6.1.1
addi x11, x0, -1             #: a sentinel the read of time must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x11, time, x0          #: time is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVI-ZICNTR §6.1.1
addi x12, x0, -1             #: a sentinel the read of instret must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x12, instret, x0       #: instret is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVI-ZICNTR §6.1.1
addi x13, x0, -1             #: a sentinel the read of fflags must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x13, fflags, x0        #: fflags is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVI-F §20.1.2
addi x14, x0, -1             #: a sentinel the read of frm must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x14, frm, x0           #: frm is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVI-F §20.1.2
addi x15, x0, -1             #: a sentinel the read of fcsr must replace (a reset value of 0 is then an observed change). | RVI-RV32I §1.1.4
csrrs x15, fcsr, x0          #: fcsr is implemented: its value replaces the sentinel; rs1 = x0 writes nothing. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVI-F §20.1.2
csrrsi x0, mideleg, 2        #: delegate the supervisor software interrupt so sie's and sip's SSI bits are visible (undelegated bits read as zero). | RVP-MACHINE §2.1.1.8
csrrsi x0, sie, 2            #: write mie.SSIE THROUGH the sie view. | RVP-SUPERVISOR §11.1.1.3
addi x11, x0, -1             #: sentinel. | RVI-RV32I §1.1.4
csrrs x11, mie, x0           #: mie shows the bit written through sie, 2: one register, two names. | RVP-SUPERVISOR §11.1.1.3; RVP-MACHINE §2.1.1.9
csrrsi x0, mip, 2            #: write mip.SSIP through the machine view (no delivery in M: the interrupt is delegated). | RVP-MACHINE §2.1.1.9
addi x12, x0, -1             #: sentinel. | RVI-RV32I §1.1.4
csrrs x12, sip, x0           #: sip shows the bit written through mip, 2: one register, two names. | RVP-SUPERVISOR §11.1.1.3; RVP-MACHINE §2.1.1.9
csrrci x0, sip, 2            #: clear SSIP through the sip view, before S could take it. | RVP-SUPERVISOR §11.1.1.3
addi x12, x0, -1             #: sentinel. | RVI-RV32I §1.1.4
csrrs x12, sip, x0           #: the bit cleared through sip is gone: 0. | RVP-SUPERVISOR §11.1.1.3
csrrsi x0, sstatus, 2        #: write mstatus.SIE THROUGH the sstatus view. | RVP-SUPERVISOR §11.1.1.1
addi x13, x0, -1             #: sentinel. | RVI-RV32I §1.1.4
csrrs x13, mstatus, x0       #: mstatus shows SIE, bit 1, set through sstatus (with FS = Initial). | RVP-SUPERVISOR §11.1.1.1; RVP-MACHINE §2.1.1.6
csrrwi x0, fflags, 31        #: all five accrued flags through the fflags view. | RVI-F §20.1.2
csrrwi x0, frm, 4            #: rounding mode RMM through the frm view. | RVI-F §20.1.2
addi x14, x0, -1             #: sentinel. | RVI-RV32I §1.1.4
csrrs x14, fcsr, x0          #: fcsr composes the two: frm above fflags, (4 << 5) | 31 = 0x9f. | RVI-F §20.1.2
addi x15, x0, -1             #: sentinel. | RVI-RV32I §1.1.4
csrrs x15, mstatus, x0       #: the FP CSR writes made FS Dirty, and SD summarizes it. | RVP-MACHINE §2.1.1.6.7
addi x5, x0, 7               #: the sentinel the refused writes must leave untouched. | RVI-RV32I §1.1.4
addi x6, x0, 9               #: a value to (try to) write. | RVI-RV32I §1.1.4
addi x30, x0, -1             #: a sentinel the handler's cause read must replace. | RVI-RV32I §1.1.4
csrrw x5, mhartid, x6        #: CSRRW always writes, and mhartid is read-only (csr[11:10] = 11): illegal-instruction, rd untouched. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x16, x5, 0              #: x5 still holds its sentinel, 7: the refused CSRRW committed nothing to rd. | RVP-CSR §1.1.1 (boundary: a read-only CSR refuses CSRRW)
addi x30, x0, -1             #: re-arm the cause sentinel. | RVI-RV32I §1.1.4
csrrs x5, mhartid, x6        #: CSRRS with rs1 != x0 is a write attempt too: illegal-instruction, rd untouched. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x16, x5, 1              #: x5 still holds its sentinel: 7 + 1 = 8, so the refused CSRRS committed nothing either. | RVP-CSR §1.1.1 (boundary: a read-only CSR refuses CSRRS with rs1 != x0)
addi x17, x0, -1             #: sentinel. | RVI-RV32I §1.1.4
csrrs x17, mhartid, x0       #: mhartid kept its value, 0, through both attempts, and CSRRS with rs1 = x0 is legal on it. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-MACHINE §2.1.1.5 (boundary: a read-only CSR reads with rs1 = x0)
csrrwi x0, mscratch, 5       #: mscratch <- 5, legal in M: the value S's refused write must not replace. | RVP-MACHINE §2.1.1.13
csrrwi x0, sscratch, 3       #: sscratch <- 3, legal in M (a CSR is accessible at all higher levels): the value U's refused write must not replace. | RVP-CSR §1.1.1; RVP-SUPERVISOR §11.1.1.6
addi x3, x0, 1               #: 1 … | RVI-RV32I §1.1.4
slli x3, x3, 11              #: … at bit 11: mstatus.MPP = S. | RVI-RV64I §3.1.2.1
csrrs x0, mstatus, x3        #: MPP <- S. | RVI-ZICSR §5.1.1
auipc x4, 0                  #: the S-mode entry base. | RVI-RV32I §1.1.4
addi x4, x4, 16              #: the instruction after mret. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4           #: mepc <- the S-mode entry. | RVI-ZICSR §5.1.1
mret                         #: drop to S at mepc. | RVP-MACHINE §2.1.3.2
addi x18, x0, -1             #: sentinel (in S). | RVI-RV32I §1.1.4
csrrs x18, sstatus, x0       #: sstatus is readable in S: mstatus's supervisor view, with SD, FS Dirty and SIE. | RVI-ZICSR §5.1.1; RVP-SUPERVISOR §11.1.1.1
addi x19, x0, -1             #: the sentinel the privilege-refused write must leave untouched. | RVI-RV32I §1.1.4
addi x28, x0, -1             #: a sentinel the handler's read of mscratch must replace. | RVI-RV32I §1.1.4
addi x30, x0, -1             #: re-arm the cause sentinel. | RVI-RV32I §1.1.4
csrrw x19, mscratch, x6      #: a write of 9 to an M-level CSR from S (csr[9:8] = 11): illegal-instruction before any effect. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x20, x19, 0             #: x19 still holds its sentinel, -1: the refused write committed nothing to rd. | RVP-CSR §1.1.1 (boundary: an M-level CSR refuses S)
addi x21, x0, -1             #: sentinel (in S). | RVI-RV32I §1.1.4
csrrs x21, sscratch, x0      #: the supervisor's own scratch reads in S (csr[9:8] = 01): the 3 M wrote. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVP-SUPERVISOR §11.1.1.6 (boundary: an S-level CSR reads in S)
auipc x4, 0                  #: the U-mode entry base. | RVI-RV32I §1.1.4
addi x4, x4, 16              #: the instruction after sret. | RVI-RV32I §1.1.4
csrrw x0, sepc, x4           #: sepc <- the U-mode entry. | RVI-ZICSR §5.1.1
sret                         #: drop to U at sepc (sstatus.SPP is 0: this S was not entered by a trap). | RVP-MACHINE §2.1.3.2
addi x22, x0, -1             #: sentinel (in U). | RVI-RV32I §1.1.4
csrrs x22, fflags, x0        #: an unprivileged CSR reads in U (csr[9:8] = 00): the 31 written through fflags. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1; RVI-F §20.1.2 (boundary: a U-level CSR reads in U)
addi x23, x0, -1             #: the sentinel the privilege-refused write must leave untouched. | RVI-RV32I §1.1.4
addi x27, x0, -1             #: a sentinel the handler's read of sscratch must replace. | RVI-RV32I §1.1.4
addi x30, x0, -1             #: re-arm the cause sentinel. | RVI-RV32I §1.1.4
csrrw x23, sscratch, x6      #: a write of 9 to an S-level CSR from U (csr[9:8] = 01): illegal-instruction before any effect. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1
addi x24, x23, 0             #: x23 still holds its sentinel, -1: the refused write committed nothing to rd. The budget ends here; the handler below runs only on a trap. | RVP-CSR §1.1.1 (boundary: an S-level CSR refuses U)
csrrs x30, mcause, x0        #: the handler, in M: the cause, 2 (illegal-instruction). | RVP-MACHINE §2.1.1.15
csrrs x28, mscratch, x0      #: mscratch read in M after the trap: no refused write reached it. | RVP-CSR §1.1.1; RVP-MACHINE §2.1.1.13
csrrs x27, sscratch, x0      #: sscratch read in M after the trap: no refused write reached it. | RVP-CSR §1.1.1; RVP-SUPERVISOR §11.1.1.6
csrrs x29, mepc, x0          #: mepc is the refused instruction's own address. | RVP-MACHINE §2.1.1.14
addi x29, x29, 4             #: step past it. | RVI-RV32I §1.1.4
csrrw x0, mepc, x29          #: mepc <- the next instruction. | RVI-ZICSR §5.1.1
mret                         #: back to the mode the trap came from, at mepc. | RVP-MACHINE §2.1.3.2
