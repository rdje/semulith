#|never: x28, x29
# a-lrsc-fault.s — misaligned atomics take the access-fault cause by kind (5 for the LR,
# a load; 7 for SC/AMO — the .4 slice-(f) root fix), judged before
# translation (P4-SYSTEM.4 decision 6), and a trapped SC invalidates NOTHING
# (decision 4): the handler observes cause/xtval/xepc and resumes, then the
# surviving reservation completes its pair.

      auipc x1, 0                  #: x1 = this instruction's own address. | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
      addi x1, x1, 68             #: the handler rides 68 bytes in. | RVI-RV32I §1.1.4
      csrrw x0, mtvec, x1          #: mtvec is programmed; rd=x0 discards the old value. | RVI-ZICSR §5.1.1
      addi x10, x0, 1              #: raw material for the region base. | RVI-RV32I §1.1.4
      slli x10, x10, 31            #: x10 = 0x8000_0000. | RVI-RV64I §3.1.2.1
      addi x2, x10, 256            #: A, naturally aligned. | RVI-RV32I §1.1.4
      addi x1, x10, 254            #: A−2 — misaligned for a word access. | RVI-RV32I §1.1.4
      addi x7, x0, 17              #: the initial word. | RVI-RV32I §1.1.4
      addi x6, x0, 42              #: the value every trapped step must NOT store. | RVI-RV32I §1.1.4
      sw x7, 0, x2                 #: A = 17. | RVI-RV64I §3.1.3

      lr.w x5, (x1)                #: a misaligned LR: the declared policy takes the LOAD access fault 5 (never the misaligned 4), judged before translation — the trap clears nothing. | RVI-A §12.1.2; state.sexp's policy (decision 6)
      sc.w x9, x6, (x1)            #: a misaligned SC: cause 7 likewise (the reservation was empty; nothing else changes). | RVI-A §12.1.2; state.sexp's policy
      amoadd.w x5, x6, (x1)        #: a misaligned AMO: cause 7 likewise. | RVI-A §12.1.4; state.sexp's policy

      lr.w x5, (x2)                #: the survival cell: reserve A (aligned) — rd <- 17. | RVI-A §12.1.2
      sc.w x9, x6, (x1)            #: the misaligned SC traps BEFORE the policy match: cause 7 — and the reservation SURVIVES (a trap is neither success nor failure). | RVI-A §12.1.2; state.sexp's policy (decision 4)
      sc.w x9, x6, (x2)            #: proof: the surviving reservation still pairs — rd <- 0, A <- 42. | RVI-A §12.1.2
      lw x8, x2, 0                 #: read-back: 42. | RVI-RV64I §3.1.3 #|end

handler:
      csrrs x11, mcause, x0        #: the handler observes the cause (5 for the LR, 7 for the SC/AMO visits). | RVI-ZICSR §5.1.1
      csrrs x12, mtval, x0         #: xtval is the faulting address. | RVP-MACHINE §2.1.1.16
      csrrs x13, mepc, x0          #: xepc is the trapping instruction's own address. | RVP-MACHINE §2.1.1.14
      addi x13, x13, 4             #: step past it. | RVI-RV32I §1.1.4
      csrrw x0, mepc, x13          #: write back the resume address. | RVI-ZICSR §5.1.1
      mret                         #: the stack pops per MPP and pc <- mepc. | RVP-MACHINE §2.1.3.2
