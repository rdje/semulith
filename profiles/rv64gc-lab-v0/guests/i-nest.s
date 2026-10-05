#|never: x28, x29
# i-nest.s — an interrupt taken inside a handler, and the xRET stack's restoration
# (P4-SYSTEM.5 slice b): the first delivery pushes MIE into MPIE; software re-enables
# inside the handler and a second, higher-priority interrupt nests; the nested mret
# pops back into the first handler with MIE restored, and the outer mret returns to
# the interrupted flow (RVP-MACHINE §2.1.1.6.1, §2.1.3.2).

      auipc x1, 0                  #: x1 = this instruction's own address. | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
      addi x1, x1, 45              #: mtvec's BASE rides 44 bytes in; MODE adds 1. | RVI-RV32I §1.1.4
      ori x1, x1, 1                #: MODE = Vectored (the two handlers get their own slots). | RVI-RV32I §1.1.4
      csrrw x0, mtvec, x1          #: mtvec = BASE | 1. | RVI-ZICSR §5.1.1
      addi x2, x0, 2               #: the SSIP bit. | RVI-RV32I §1.1.4
      csrrs x0, mip, x2            #: SSIP <- 1. | RVP-MACHINE §2.1.1.9
      csrrs x0, mie, x2            #: SSIE <- 1. | RVP-MACHINE §2.1.1.9
      addi x6, x0, 8               #: the MIE bit. | RVI-RV32I §1.1.4
      csrrs x0, mstatus, x6        #: MIE <- 1. | RVP-MACHINE §2.1.1.6.1
      addi x7, x0, 0               #: — delivery 1: SSI, vectored to BASE+4. | RVP-MACHINE §2.1.1.7
      addi x9, x0, 42              #: the landing marker: the outer mret returns here. | RVI-RV32I §1.1.4 #|end

      jal x0, ssi_handler          #: BASE slot (unused on this flow — SSI rides BASE+4). | RVP-MACHINE §2.1.1.7
      jal x0, ssi_handler          #: BASE+4 slot: the vectored SSI delivery's landing. | RVP-MACHINE §2.1.1.7
      addi x0, x0, 0               #: (never executed — vector spacing)
      addi x0, x0, 0               #: (never executed — vector spacing)
      addi x0, x0, 0               #: (never executed — vector spacing)
      addi x0, x0, 0               #: (never executed — vector spacing)
      addi x0, x0, 0               #: (never executed — vector spacing)
      addi x0, x0, 0               #: (never executed — vector spacing)
      addi x0, x0, 0               #: (never executed — vector spacing)
      jal x0, sei_handler          #: BASE+36 slot: the vectored SEI delivery's landing. | RVP-MACHINE §2.1.1.7

ssi_handler:
      csrrs x11, mcause, x0        #: handler A observes the Interrupt bit with cause 1. | RVP-MACHINE §2.1.1.9
      csrrs x12, mstatus, x0       #: the push: MPIE <- 1, MIE <- 0 (the handler is quiet). | RVP-MACHINE §2.1.1.6.1
      csrrc x0, mip, x2            #: clear SSIP FIRST — otherwise the resume head after the nested return re-fires it. | RVP-MACHINE §2.1.1.9
      csrrs x14, mepc, x0          #: save the outer resume address in a REGISTER before re-enabling — the nested delivery clobbers mepc. | RVP-MACHINE §2.1.1.14
      addi x14, x14, 4             #: step it past the delivery placeholder. | RVI-RV32I §1.1.4
      addi x8, x0, 1               #: raw material for SEIP's bit. | RVI-RV32I §1.1.4
      slli x8, x8, 9               #: x8 = 1 << 9. | RVI-RV64I §3.1.2.1
      csrrs x0, mip, x8            #: SEIP <- 1: a second cause is posted from inside the handler. | RVP-MACHINE §2.1.1.9
      csrrs x0, mie, x8            #: SEIE <- 1. | RVP-MACHINE §2.1.1.9
      csrrs x0, mstatus, x6        #: MIE <- 1 again: the next boundary takes SEI NESTED inside A. | RVP-MACHINE §2.1.1.6.1
      csrrw x0, mepc, x14          #: the nested mret lands here: restore the stepped outer mepc. | RVI-ZICSR §5.1.1
      mret                         #: the OUTER mret: the stack pops per MPP and pc <- the restored mepc — the landing marker. | RVP-MACHINE §2.1.3.2

sei_handler:
      csrrs x21, mcause, x0        #: handler B (nested) observes the Interrupt bit with cause 9. | RVP-MACHINE §2.1.1.9
      csrrs x22, mstatus, x0       #: the second push: MPIE <- the MIE software set inside A. | RVP-MACHINE §2.1.1.6.1
      csrrc x0, mip, x8            #: clear SEIP before returning. | RVP-MACHINE §2.1.1.9
      csrrs x23, mepc, x0          #: B's mepc is the instruction A was about to run. | RVP-MACHINE §2.1.1.14
      mret                         #: the NESTED mret: pops back into A with MIE <- MPIE restored. | RVP-MACHINE §2.1.3.2
