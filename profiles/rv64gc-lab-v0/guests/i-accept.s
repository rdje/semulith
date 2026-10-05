#|never: x28, x29
# i-accept.s — the (a)(b)(c) taken-rule at the step head (P4-SYSTEM.5 slice b):
# pending with the enable clear is not taken; M with MIE clear passes it by; M with
# MIE set takes it; and a lower mode takes it regardless of the global enables
# (RVP-MACHINE §2.1.1.9's own rule). SSIP/SSIE drive the software-writable bit.

      auipc x1, 0                  #: x1 = this instruction's own address. | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
      addi x1, x1, 80              #: the handler rides 80 bytes in. | RVI-RV32I §1.1.4
      csrrw x0, mtvec, x1          #: mtvec programmed; rd=x0 discards. | RVI-ZICSR §5.1.1
      addi x2, x0, 2               #: the SSIP bit position (bit 1, cause 1). | RVI-RV32I §1.1.4
      csrrs x0, mip, x2            #: SSIP <- 1: a software pending bit is posted. | RVP-MACHINE §2.1.1.9
      csrrs x0, mie, x2            #: SSIE <- 1: the cause is enabled. | RVP-MACHINE §2.1.1.9
      addi x5, x0, 1               #: M with MIE CLEAR (reset): the evaluation passes the pending interrupt by — the marker executes. | RVP-MACHINE §2.1.1.9 (the (a) clause)
      addi x5, x5, 1               #: and a second boundary, still untaken. | RVP-MACHINE §2.1.1.9
      addi x6, x0, 8               #: the MIE bit position (bit 3). | RVI-RV32I §1.1.4
      csrrs x0, mstatus, x6        #: MIE <- 1: (a)(b)(c) now all hold at the next boundary. | RVP-MACHINE §2.1.1.9
      addi x7, x0, 0               #: — the pending evaluation takes SSI here (the delivery step; no register observation) — mepc is THIS instruction's address. | RVP-MACHINE §2.1.1.9
      addi x5, x5, 1               #: resumed after the handler: the marker completes at 3. | RVI-RV32I §1.1.4
      csrrw x0, mstatus, x0        #: mstatus <- 0: MPP = U (and MIE clears — the boundary before the mret passes the pending by). | RVI-ZICSR §5.1.1
      auipc x4, 0                  #: x4 = this address. | RVI-RV32I §1.1.4
      addi x4, x4, 20              #: the U entry rides 20 bytes past this auipc (72 from the entry). | RVI-RV32I §1.1.4
      csrrw x0, mepc, x4           #: mepc = the U entry. | RVI-ZICSR §5.1.1
      csrrs x0, mip, x2            #: SSIP <- 1 again — posted FROM M (mip is M-only; a U-mode write would be illegal): M with MIE clear passes it by. | RVP-MACHINE §2.1.1.9
      mret                         #: the stack pops per MPP: enter U, pc <- mepc. | RVP-MACHINE §2.1.3.2
      addi x7, x0, 0               #: — taken in U regardless of the global enables (mode U < M), delivered to M — mepc is THIS instruction's address. | RVP-MACHINE §2.1.1.9
      addi x9, x0, 42              #: the landing marker: the flow arrives past the U cell. | RVI-RV32I §1.1.4 #|end

handler:
      csrrs x11, mcause, x0        #: the handler observes the Interrupt bit with cause 1 (0x8000000000000001). | RVP-MACHINE §2.1.1.9
      csrrs x12, mepc, x0          #: mepc is the un-fetched pc (interrupts are taken BETWEEN instructions). | RVP-MACHINE §2.1.1.9
      csrrs x13, mstatus, x0       #: the stack: MPIE <- 1, MIE <- 0, MPP <- the originating mode. | RVP-MACHINE §2.1.1.6.1
      csrrc x0, mip, x2            #: SSIP <- 0: the pending bit is cleared before returning (else the next boundary re-fires). | RVP-MACHINE §2.1.1.9
      csrrs x14, mepc, x0          #: step the resume address past the interrupted instruction. | RVP-MACHINE §2.1.1.9
      addi x14, x14, 4             #: mepc + 4. | RVI-RV32I §1.1.4
      csrrw x0, mepc, x14          #: write it back. | RVI-ZICSR §5.1.1
      mret                         #: the stack pops per MPP and pc <- mepc. | RVP-MACHINE §2.1.3.2
