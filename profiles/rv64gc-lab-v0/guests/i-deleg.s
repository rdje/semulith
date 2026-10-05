#|never: x28, x29
# i-deleg.s — the delegation mask (P4-SYSTEM.5 slice b): a delegated interrupt is
# masked AT THE DELEGATOR — mideleg[1] makes SSI fire in S/U only, never in M;
# clearing it returns the cause to M from any mode (RVP-MACHINE §2.1.1.8–§2.1.1.9).

      auipc x1, 0                  #: x1 = this instruction's own address. | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
      addi x1, x1, 136             #: the M handler rides 136 bytes in. | RVI-RV32I §1.1.4
      csrrw x0, mtvec, x1          #: mtvec programmed (ecall AND the M-taken SSI). | RVI-ZICSR §5.1.1
      auipc x1, 0                  #: x1 = this address. | RVI-RV32I §1.1.4
      addi x1, x1, 96              #: the S handler rides 96 bytes past this auipc (108 from the entry). | RVI-RV32I §1.1.4
      csrrw x0, stvec, x1          #: stvec programmed (the delegated SSI). | RVI-ZICSR §5.1.1
      addi x2, x0, 2               #: the SSIP bit position (bit 1). | RVI-RV32I §1.1.4
      csrrs x0, mip, x2            #: SSIP <- 1. | RVP-MACHINE §2.1.1.9
      csrrs x0, mie, x2            #: SSIE <- 1. | RVP-MACHINE §2.1.1.9
      csrrs x0, mideleg, x2        #: mideleg[1] <- 1: SSI is delegated to S. | RVP-MACHINE §2.1.1.8
      addi x6, x0, 8               #: the MIE bit. | RVI-RV32I §1.1.4
      csrrs x0, mstatus, x6        #: MIE <- 1. | RVP-MACHINE §2.1.1.6.1
      addi x5, x0, 1               #: IN M: the mask holds — a delegated SSI is NEVER taken in M, even fully enabled. | RVP-MACHINE §2.1.1.8
      addi x3, x0, 1               #: raw material for MPP. | RVI-RV32I §1.1.4
      slli x3, x3, 11              #: mstatus.MPP = S. | RVI-RV64I §3.1.2.1
      csrrw x0, mstatus, x3        #: mstatus written. | RVI-ZICSR §5.1.1
      auipc x4, 0                  #: x4 = this address. | RVI-RV32I §1.1.4
      addi x4, x4, 16              #: the S entry is the next-but-one instruction. | RVI-RV32I §1.1.4
      csrrw x0, mepc, x4           #: mepc = the S entry. | RVI-ZICSR §5.1.1
      mret                         #: enter S. | RVP-MACHINE §2.1.3.2
      addi x5, x5, 1               #: IN S with SIE clear: the delegated SSI still passes by. | RVP-SUPERVISOR §11.1.1.3
      addi x6, x0, 2               #: the SIE bit (bit 1). | RVI-RV32I §1.1.4
      csrrs x0, sstatus, x6        #: SIE <- 1 through the S VIEW (mstatus is M-only — from S the access would be illegal). | RVP-MACHINE §2.1.1.6.1
      addi x7, x0, 0               #: — the delivery step: taken IN S through stvec — sepc is THIS address. | RVP-SUPERVISOR §11.1.1.3
      ecall                        #: from S: cause 9 to M — the M handler will un-delegate. | RVP-MACHINE §2.1.3.1
      addi x7, x0, 0               #: — taken IN M at the next boundary (mideleg cleared, and S is a lower mode) — mepc is THIS address. | RVP-MACHINE §2.1.1.9
      addi x9, x0, 42              #: the landing marker: resume after the M-taken SSI. | RVI-RV32I §1.1.4 #|end

s_handler:
      csrrs x21, scause, x0        #: the S handler observes the Interrupt bit with cause 1. | RVP-SUPERVISOR §11.1.1.3
      csrrs x22, sepc, x0          #: sepc is the un-fetched pc. | RVP-SUPERVISOR §11.1.1.7
      csrrc x0, sip, x2            #: clear SSIP through the S VIEW (mip is M-only). | RVP-SUPERVISOR §11.1.1.4
      csrrs x23, sepc, x0          #: step the resume address. | RVP-SUPERVISOR §11.1.1.7
      addi x23, x23, 4             #: sepc + 4. | RVI-RV32I §1.1.4
      csrrw x0, sepc, x23          #: write it back. | RVI-ZICSR §5.1.1
      sret                         #: the stack pops per SPP and pc <- sepc. | RVP-MACHINE §2.1.3.2

m_handler:
      csrrs x24, mcause, x0        #: the M handler reads the cause — ecall-from-S (9) on the first visit, the Interrupt bit with cause 1 on the second. | RVP-MACHINE §2.1.1.15
      csrrs x25, mepc, x0          #: mepc is the trapping or un-fetched pc. | RVP-MACHINE §2.1.1.14
      addi x10, x0, 15             #: the cause-number mask (mcause carries the Interrupt bit). | RVI-RV32I §1.1.4
      and x10, x24, x10            #: the visit key: 9 on the ecall visit, 1 on the interrupt visit. | RVI-RV32I §1.1.4
      addi x13, x0, 1              #: the SSI cause. | RVI-RV32I §1.1.4
      beq x10, x13, m_consume      #: the interrupt visit consumes SSI instead of re-posting it. | RVI-RV32I §1.1.5
      addi x6, x0, 2               #: the delegation bit again. | RVI-RV32I §1.1.4
      csrrc x0, mideleg, x6        #: mideleg[1] <- 0: SSI returns to M's rule. | RVP-MACHINE §2.1.1.8
      csrrs x0, mip, x6            #: SSIP <- 1 again for the M-taken cell. | RVP-MACHINE §2.1.1.9
      beq x0, x0, m_resume         #: to the shared resume. | RVI-RV32I §1.1.5
m_consume:
      addi x13, x0, 2              #: SSIP's bit. | RVI-RV32I §1.1.4
      csrrc x0, mip, x13           #: clear SSIP — the M-taken cause is consumed. | RVP-MACHINE §2.1.1.9
m_resume:
      csrrs x26, mepc, x0          #: step the resume address. | RVP-MACHINE §2.1.1.14
      addi x26, x26, 4             #: mepc + 4. | RVI-RV32I §1.1.4
      csrrw x0, mepc, x26          #: write it back. | RVI-ZICSR §5.1.1
      mret                         #: the stack pops per MPP and pc <- mepc. | RVP-MACHINE §2.1.3.2
