#|never: x28, x29
# i-enable.s — pending with the enable clear is never taken; the moment the enable
# lands, the NEXT step boundary takes it (P4-SYSTEM.5 slice b — per-step evaluation
# makes the spec's "bounded amount of time" and the CSR-write immediacy
# construction-shaped, RVP-MACHINE §2.1.1.9).

      auipc x1, 0                  #: x1 = this instruction's own address. | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
      addi x1, x1, 56              #: the handler rides 56 bytes in. | RVI-RV32I §1.1.4
      csrrw x0, mtvec, x1          #: mtvec programmed. | RVI-ZICSR §5.1.1
      addi x2, x0, 2               #: the SSIP bit position (bit 1). | RVI-RV32I §1.1.4
      csrrs x0, mip, x2            #: SSIP <- 1 FIRST: pending before any enable. | RVP-MACHINE §2.1.1.9
      addi x5, x0, 1               #: enable still clear: the evaluation passes it by — marker one. | RVP-MACHINE §2.1.1.9 (the (b) clause)
      addi x5, x5, 1               #: marker two: pending alone never fires. | RVP-MACHINE §2.1.1.9
      addi x6, x0, 8               #: the MIE bit. | RVI-RV32I §1.1.4
      csrrs x0, mstatus, x6        #: MIE <- 1. | RVP-MACHINE §2.1.1.6.1
      addi x5, x5, 1               #: marker three: enable still missing — (b) keeps failing. | RVP-MACHINE §2.1.1.9
      csrrs x0, mie, x2            #: SSIE <- 1 at LAST: the very next boundary takes it. | RVP-MACHINE §2.1.1.9
      addi x7, x0, 0               #: — the delivery step (no register observation) — mepc is THIS instruction's address. | RVP-MACHINE §2.1.1.9
      addi x5, x5, 1               #: resumed: the marker completes at 4 — the write's immediacy is one boundary, by construction. | RVP-MACHINE §2.1.1.9
      addi x9, x0, 42              #: the landing marker. | RVI-RV32I §1.1.4 #|end

handler:
      csrrs x11, mcause, x0        #: the handler observes the Interrupt bit with cause 1. | RVP-MACHINE §2.1.1.9
      csrrs x12, mepc, x0          #: mepc is the un-fetched pc (taken BETWEEN instructions). | RVP-MACHINE §2.1.1.9
      csrrc x0, mip, x2            #: SSIP <- 0 before returning. | RVP-MACHINE §2.1.1.9
      csrrs x14, mepc, x0          #: step the resume address. | RVP-MACHINE §2.1.1.9
      addi x14, x14, 4             #: mepc + 4. | RVI-RV32I §1.1.4
      csrrw x0, mepc, x14          #: write it back. | RVI-ZICSR §5.1.1
      mret                         #: the stack pops per MPP and pc <- mepc. | RVP-MACHINE §2.1.3.2
