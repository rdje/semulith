#|never: x28, x29
# a-amo-sv39.s — the translated-AMO cells (P4-SYSTEM.4 slice d, riding .3's sv39
# machinery): M builds the tables, arms satp, delegates cause 15 to S, and drops to S.
# An AMO on an unreadable page faults 15 — NEVER a load page fault (RVP-SUPERVISOR);
# R∧W succeeds; an aliased VA pairs (the reservation is PHYSICAL-keyed); a trapped SC
# leaves its reservation alive to trap again; misalignment judges before translation.

      auipc x1, 0                  #: x1 = this instruction's own address. | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
      addi x1, x1, 300             #: the S handler rides 300 bytes in. | RVI-RV32I §1.1.4
      csrrw x0, stvec, x1          #: stvec programmed (cause 15 delegates to S). | RVI-ZICSR §5.1.1
      auipc x1, 0                  #: x1 = this address. | RVI-RV32I §1.1.4
      addi x1, x1, 312             #: the M handler rides 312 bytes past its auipc. | RVI-RV32I §1.1.4
      csrrw x0, mtvec, x1          #: mtvec programmed (cause 7 stays in M). | RVI-ZICSR §5.1.1
      addi x2, x0, 1               #: raw material for the delegation mask. | RVI-RV32I §1.1.4
      slli x2, x2, 15              #: medeleg bit 15: store/AMO page faults reach S. | RVI-RV64I §3.1.2.1
      csrrw x0, medeleg, x2        #: medeleg = 0x8000. | RVI-ZICSR §5.1.1

      addi x10, x0, 1              #: raw material for the region base. | RVI-RV32I §1.1.4
      slli x10, x10, 31            #: x10 = 0x8000_0000. | RVI-RV64I §3.1.2.1
      addi x11, x0, 1              #: raw material for the root table's offset. | RVI-RV32I §1.1.4
      slli x11, x11, 12            #: 0x1000. | RVI-RV64I §3.1.2.1
      add x11, x10, x11            #: x11 = base+0x1000 = the ROOT table. | RVI-RV32I §1.1.4
      lui x12, 0x20001             #: the root[0] pointer's upper bits. | RVI-RV64I §3.1.2.1
      addi x12, x12, -2047         #: root[0] = pointer to L1T at base+0x2000 (0x20000801). | RVP-SUPERVISOR §11.1.4.1
      sd x12, 0, x11               #: root[0] written. | RVI-RV64I §3.1.3
      lui x12, 0x20000             #: the identity leaf's upper bits. | RVI-RV64I §3.1.2.1
      addi x12, x12, 207           #: root[2] = a 1 GiB leaf, VA=PA the code region, R|W|X|A|D (0x200000CF). | RVP-SUPERVISOR §11.1.4.1
      sd x12, 16, x11              #: root[2] written. | RVI-RV64I §3.1.3
      addi x11, x0, 2              #: raw material for L1T's offset. | RVI-RV32I §1.1.4
      slli x11, x11, 12            #: 0x2000. | RVI-RV64I §3.1.2.1
      add x11, x10, x11            #: x11 = base+0x2000 = L1T. | RVI-RV32I §1.1.4
      lui x12, 0x20001             #: the L1T[2] pointer's upper bits. | RVI-RV64I §3.1.2.1
      addi x12, x12, -1023         #: L1T[2] = pointer to L0T at base+0x3000 (0x20000C01). | RVP-SUPERVISOR §11.1.4.1
      sd x12, 16, x11              #: L1T[2] written. | RVI-RV64I §3.1.3
      addi x11, x0, 3              #: raw material for L0T's offset. | RVI-RV32I §1.1.4
      slli x11, x11, 12            #: 0x3000. | RVI-RV64I §3.1.2.1
      add x11, x10, x11            #: x11 = base+0x3000 = L0T. | RVI-RV32I §1.1.4
      lui x12, 0x20000             #: the data leaf's upper bits. | RVI-RV64I §3.1.2.1
      addi x12, x12, 197           #: L0T[1] = leaf at PA base+0x4000 with R=0 W=1 A=1 D=1 (0x200010C5). | RVP-SUPERVISOR §11.1.4.1
      sd x12, 8, x11               #: L0T[1] written (the unreadable page). | RVI-RV64I §3.1.3
      lui x12, 0x20000             #: the W=0 leaf's upper bits. | RVI-RV64I §3.1.2.1
      addi x12, x12, 203           #: L0T[4] = leaf at PA base+0x4000 with R=1 W=0 A=1 D=1 (0x200010CB). | RVP-SUPERVISOR §11.1.4.1
      sd x12, 32, x11              #: L0T[4] written (the unwritable page). | RVI-RV64I §3.1.3
      lui x12, 0x20000             #: the R∧W leaf's upper bits. | RVI-RV64I §3.1.2.1
      addi x12, x12, 207           #: L0T[6] = leaf at PA base+0x4000 with R=1 W=1 A=1 D=1 (0x200010CF). | RVP-SUPERVISOR §11.1.4.1
      sd x12, 48, x11              #: L0T[6] written. | RVI-RV64I §3.1.3
      lui x12, 0x20000             #: the alias leaf's upper bits. | RVI-RV64I §3.1.2.1
      addi x12, x12, 207           #: L0T[8] = the SAME PA (base+0x4000), same permissions (0x200010CF). | RVP-SUPERVISOR §11.1.4.1
      sd x12, 64, x11              #: L0T[8] written (the alias mapping). | RVI-RV64I §3.1.3
      addi x5, x0, 8               #: raw material for satp.MODE. | RVI-RV32I §1.1.4
      slli x5, x5, 60              #: MODE = 8 (Sv39). | RVI-RV64I §3.1.2.1
      lui x2, 128                  #: the root PPN's upper bits. | RVI-RV64I §3.1.2.1
      addi x2, x2, 1               #: PPN = 0x80001 (the root table at base+0x1000). | RVI-RV32I §1.1.4
      or x2, x2, x5                #: satp = (8 << 60) | 0x80001. | RVI-RV32I §1.1.4
      csrrw x0, satp, x2           #: satp armed. | RVI-ZICSR §5.1.1
      addi x3, x0, 1               #: raw material for MPP. | RVI-RV32I §1.1.4
      slli x3, x3, 11              #: mstatus.MPP = S. | RVI-RV64I §3.1.2.1
      csrrw x0, mstatus, x3        #: mstatus written. | RVI-ZICSR §5.1.1
      auipc x4, 0                  #: x4 = this address. | RVI-RV32I §1.1.4
      addi x4, x4, 16              #: the S entry is the next-but-one instruction. | RVI-RV32I §1.1.4
      csrrw x0, mepc, x4           #: mepc = the S entry. | RVI-ZICSR §5.1.1
      mret                         #: the stack pops per MPP: enter S, pc <- mepc. | RVP-MACHINE §2.1.3.2

      lui x13, 0x403               #: x13 = VA 0x403000 → the R=0 page. | RVI-RV64I §3.1.2.1
      lui x14, 0x404               #: x14 = VA 0x404000 → the W=0 page. | RVI-RV64I §3.1.2.1
      lui x15, 0x406               #: x15 = VA 0x406000 → the R∧W page. | RVI-RV64I §3.1.2.1
      lui x16, 0x408               #: x16 = VA 0x408000 → the alias of x15's page. | RVI-RV64I §3.1.2.1
      addi x7, x0, 17              #: the initial word. | RVI-RV32I §1.1.4
      addi x6, x0, 42              #: the AMO's operand. | RVI-RV32I §1.1.4

      amoadd.w x5, x6, (x13)       #: cell 1: an AMO on an UNREADABLE page — the store/AMO page fault 15, NEVER a load page fault 13 (RVP-SUPERVISOR's own sentence); S's handler takes it. | RVP-SUPERVISOR; RVI-A §12.1.4
      amoadd.w x5, x6, (x14)       #: cell 2: an AMO on an UNWRITABLE page — 15 likewise. | RVP-SUPERVISOR; RVI-A §12.1.4
      sw x7, 0, x15                #: cell 3 setup: the R∧W page holds 17 (an S-mode translated store). | RVP-SUPERVISOR §11.1.3.2
      amoadd.w x5, x6, (x15)       #: cell 3: the translated AMO succeeds — rd <- the old word 17, mem <- 59. | RVI-A §12.1.4
      lw x8, x15, 0                #: read-back: 59. | RVI-RV64I §3.1.3

      lr.w x5, (x15)               #: cell 4: reserve through VA 0x406000 — rd <- 59. | RVI-A §12.1.2
      sc.w x9, x6, (x16)           #: the ALIAS pairs: a different VA, the SAME physical address — the exact-physical-match policy allows the success (rd <- 0, mem <- 42). | RVI-A §12.1.2; state.sexp's reservation candidate (decision 2)
      lw x8, x15, 0                #: read-back through the other VA: 42 — the reservation is PHYSICAL-keyed. | RVI-RV64I §3.1.3

      lr.w x5, (x14)               #: cell 5: LR on the W=0 page — a LOAD, so R=1 suffices: reserve its PA — rd <- 42. | RVI-A §12.1.2; RVP-MACHINE's exception table
      sc.w x9, x6, (x14)           #: the SC matches — but the page is unwritable: page fault 15 (the trap path, reservation SURVIVES). | RVP-SUPERVISOR; RVI-A §12.1.2
      sc.w x9, x6, (x14)           #: proof of survival: the SC matches AGAIN and faults AGAIN — a cleared reservation would have failed silently with code 1 and no trap. | RVI-A §12.1.2; state.sexp's policy (decision 4)

      addi x17, x15, 2             #: x17 = the R∧W page + 2 — misaligned, and the walk would fault too. | RVI-RV32I §1.1.4
      sc.w x9, x6, (x17)           #: cell 6: misaligned judges BEFORE translation — cause 7 (never a page fault), and the reservation survives again. | RVI-A §12.1.2; state.sexp's policy (decisions 4, 6)
      sc.w x9, x6, (x15)           #: the surviving reservation pairs one last time: rd <- 0, mem <- 42. | RVI-A §12.1.2
      lw x8, x15, 0                #: read-back: 42. | RVI-RV64I §3.1.3 #|end

s_handler:
      csrrs x21, scause, x0        #: the S handler observes the delegated cause (15 every visit). | RVI-ZICSR §5.1.1
      csrrs x22, stval, x0         #: stval is the faulting VA. | RVP-SUPERVISOR §11.1.1.9
      csrrs x23, sepc, x0          #: sepc is the trapping instruction's own address. | RVP-SUPERVISOR §11.1.1.7
      addi x23, x23, 4             #: step past it. | RVI-RV32I §1.1.4
      csrrw x0, sepc, x23          #: write back the resume address. | RVI-ZICSR §5.1.1
      sret                         #: the stack pops per SPP and pc <- sepc. | RVP-MACHINE §2.1.3.2

m_handler:
      csrrs x24, mcause, x0        #: the M handler observes cause 7. | RVI-ZICSR §5.1.1
      csrrs x25, mtval, x0         #: mtval is the misaligned VA. | RVP-MACHINE §2.1.1.16
      csrrs x26, mepc, x0          #: mepc is the trapping instruction. | RVP-MACHINE §2.1.1.14
      addi x26, x26, 4             #: step past it. | RVI-RV32I §1.1.4
      csrrw x0, mepc, x26          #: write back the resume address. | RVI-ZICSR §5.1.1
      mret                         #: the stack pops per MPP and pc <- mepc. | RVP-MACHINE §2.1.3.2
