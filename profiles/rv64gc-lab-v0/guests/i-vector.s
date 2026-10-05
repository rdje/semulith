#|never: x28, x29
# i-vector.s — both vector modes delivered as declared (P4-SYSTEM.5 slice b):
# interrupt delivery HONORS mtvec/stvec.MODE (Vectored = BASE + 4×cause), while a
# synchronous trap under the same MODE keeps BASE (RVP-MACHINE §2.1.1.7 — delivering
# MODE=1 as BASE for an interrupt would be a description lie). The M cell rides SEI
# (BASE+36), the S cell rides SSI (SBASE+4): SEIP is read-only in sip, so the S-taken
# cause is the one software can clear through the S view.

      auipc x1, 0                  #: x1 = this instruction's own address. | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
      addi x1, x1, 109             #: mtvec's BASE rides 108 bytes in; MODE adds 1. | RVI-RV32I §1.1.4
      ori x1, x1, 1                #: MODE = Vectored. | RVI-RV32I §1.1.4
      csrrw x0, mtvec, x1          #: mtvec = BASE | 1. | RVI-ZICSR §5.1.1
      auipc x1, 0                  #: x1 = this address. | RVI-RV32I §1.1.4
      addi x1, x1, 129             #: stvec's BASE rides 129 bytes past this auipc (144 from the entry); MODE adds 1. | RVI-RV32I §1.1.4
      ori x1, x1, 1                #: MODE = Vectored for stvec too. | RVI-RV32I §1.1.4
      csrrw x0, stvec, x1          #: stvec = SBASE | 1. | RVI-ZICSR §5.1.1
      addi x8, x0, 1               #: raw material for SEIP's bit. | RVI-RV32I §1.1.4
      slli x8, x8, 9               #: x8 = 1 << 9. | RVI-RV64I §3.1.2.1
      csrrs x0, mip, x8            #: SEIP <- 1. | RVP-MACHINE §2.1.1.9
      csrrs x0, mie, x8            #: SEIE <- 1. | RVP-MACHINE §2.1.1.9
      addi x6, x0, 8               #: the MIE bit. | RVI-RV32I §1.1.4
      csrrs x0, mstatus, x6        #: MIE <- 1. | RVP-MACHINE §2.1.1.6.1
      addi x7, x0, 0               #: — delivery 1: SEI VECTORED to M — pc <- BASE + 4×9 = BASE + 36, never BASE. | RVP-MACHINE §2.1.1.7
      ecall                        #: from M: a SYNCHRONOUS trap under MODE=Vectored still lands at BASE (never BASE + 4×cause). | RVP-MACHINE §2.1.1.7
      addi x2, x0, 2               #: the SSIP bit. | RVI-RV32I §1.1.4
      csrrs x0, mideleg, x2        #: mideleg[1] <- 1 FIRST — SSI is masked at M before it can pend there (MIE is 1 again from the return). | RVP-MACHINE §2.1.1.8
      csrrs x0, mip, x2            #: SSIP <- 1 — delegated, so M's taken-rule never sees it. | RVP-MACHINE §2.1.1.9
      csrrs x0, mie, x2            #: SSIE <- 1. | RVP-MACHINE §2.1.1.9
      addi x3, x0, 1               #: raw material for MPP. | RVI-RV32I §1.1.4
      slli x3, x3, 11              #: mstatus.MPP = S. | RVI-RV64I §3.1.2.1
      csrrw x0, mstatus, x3        #: mstatus written. | RVI-ZICSR §5.1.1
      auipc x4, 0                  #: x4 = this address. | RVI-RV32I §1.1.4
      addi x4, x4, 24              #: the S entry rides 24 bytes past this auipc (116 from the entry), inside the M table's unused slots. | RVI-RV32I §1.1.4
      csrrw x0, mepc, x4           #: mepc = the S entry. | RVI-ZICSR §5.1.1
      mret                         #: enter S. | RVP-MACHINE §2.1.3.2

      jal x0, base_handler         #: BASE slot: the synchronous trap's landing. | RVP-MACHINE §2.1.1.7
      jal x0, base_handler         #: BASE+4 slot (unused on this flow — no SSI is ever taken in M). | RVP-MACHINE §2.1.1.7
      addi x6, x0, 2               #: the S entry (riding the M table's unused slots): the SIE bit. | RVI-RV32I §1.1.4
      csrrs x0, sstatus, x6        #: SIE <- 1 through the S VIEW (mstatus is M-only from S). | RVP-MACHINE §2.1.1.6.1
      addi x7, x0, 0               #: — delivery 2: SSI VECTORED to S — pc <- SBASE + 4×1 = SBASE + 4; sepc is THIS address. | RVP-MACHINE §2.1.1.7; RVP-SUPERVISOR §11.1.1.2
      addi x9, x0, 42              #: the landing marker. | RVI-RV32I §1.1.4 #|end
      addi x0, x0, 0               #: (never executed — unused M-table slot)
      addi x0, x0, 0               #: (never executed — unused M-table slot)
      addi x0, x0, 0               #: (never executed — unused M-table slot)
      jal x0, sei_m_handler        #: BASE+36 slot (which SBASE aliases): the vectored SEI delivery's landing. | RVP-MACHINE §2.1.1.7
      jal x0, ssi_s_handler        #: SBASE+4 slot: the vectored SSI delivery's landing. | RVP-MACHINE §2.1.1.7; RVP-SUPERVISOR §11.1.1.2

base_handler:
      csrrs x11, mcause, x0        #: the BASE slot: ecall's cause 11 — the synchronous trap ignored the vector offset. | RVP-MACHINE §2.1.1.7
      csrrs x12, mepc, x0          #: mepc is the ecall's own address. | RVP-MACHINE §2.1.1.14
      addi x12, x12, 4             #: step past it. | RVI-RV32I §1.1.4
      csrrw x0, mepc, x12          #: write it back. | RVI-ZICSR §5.1.1
      mret                         #: the stack pops per MPP and pc <- mepc. | RVP-MACHINE §2.1.3.2

sei_m_handler:
      csrrs x13, mcause, x0        #: the BASE+36 slot: the Interrupt bit with cause 9 — the vectored delivery computed it. | RVP-MACHINE §2.1.1.7
      csrrs x14, mepc, x0          #: mepc is the un-fetched pc. | RVP-MACHINE §2.1.1.14
      csrrc x0, mip, x8            #: clear SEIP through MIP — it is read-only in sip, so the M-side cause is the M-cleared one. | RVP-MACHINE §2.1.1.9; RVP-SUPERVISOR §11.1.1.4
      csrrs x14, mepc, x0          #: step the resume address. | RVP-MACHINE §2.1.1.14
      addi x14, x14, 4             #: mepc + 4. | RVI-RV32I §1.1.4
      csrrw x0, mepc, x14          #: write it back. | RVI-ZICSR §5.1.1
      mret                         #: the stack pops per MPP and pc <- mepc. | RVP-MACHINE §2.1.3.2

ssi_s_handler:
      csrrs x21, scause, x0        #: the SBASE+4 slot: the Interrupt bit with cause 1. | RVP-MACHINE §2.1.1.7; RVP-SUPERVISOR §11.1.1.2
      csrrs x22, sepc, x0          #: sepc is the un-fetched pc. | RVP-SUPERVISOR §11.1.1.7
      csrrc x0, sip, x2            #: clear SSIP through the S view — SSIP is the pending bit software CAN clear from S. | RVP-SUPERVISOR §11.1.1.4
      csrrs x23, sepc, x0          #: step the resume address. | RVP-SUPERVISOR §11.1.1.7
      addi x23, x23, 4             #: sepc + 4. | RVI-RV32I §1.1.4
      csrrw x0, sepc, x23          #: write it back. | RVI-ZICSR §5.1.1
      sret                         #: the stack pops per SPP and pc <- sepc. | RVP-MACHINE §2.1.3.2
