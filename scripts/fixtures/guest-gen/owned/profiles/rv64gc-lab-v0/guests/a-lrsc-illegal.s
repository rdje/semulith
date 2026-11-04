#|never: x28, x29
# a-lrsc-illegal.s — the reserved A encodings are refused, never guessed
# (P4-SYSTEM.4 decision 9, the legality cells): an LR with rs2≠0, a reserved AMO
# funct5, and an A-form funct3 outside .W/.D all decode to NO row — the diagnostic
# policy converts the miss to the delivered illegal-instruction cause 2 with xtval
# the word (D-RESERVED-DECODE), and the handler resumes past each.

      auipc x1, 0                  #: x1 = this instruction's own address. | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
      addi x1, x1, 60              #: the handler rides 60 bytes in. | RVI-RV32I §1.1.4
      csrrw x0, mtvec, x1          #: mtvec is programmed. | RVI-ZICSR §5.1.1
      addi x10, x0, 1              #: raw material for the region base. | RVI-RV32I §1.1.4
      slli x10, x10, 31            #: x10 = 0x8000_0000. | RVI-RV64I §3.1.2.1
      addi x2, x10, 256            #: A, naturally aligned. | RVI-RV32I §1.1.4
      addi x7, x0, 17              #: the initial word. | RVI-RV32I §1.1.4
      addi x6, x0, 42              #: a value no trapped step may store. | RVI-RV32I §1.1.4
      sw x7, 0, x2                 #: A = 17. | RVI-RV64I §3.1.3

      .word 0x103120af             #: an LR.W word with rs2=3 (the lr row's own 24..20=0 rule): NO row matches — delivered illegal-instruction, cause 2, xtval the word. | D-RESERVED-DECODE; RVI-A §12.1.2
      .word 0x2800a32f             #: funct5 0x05 — no Zaamo operation owns it (0x02 would be LR's own!): cause 2, xtval the word. | D-RESERVED-DECODE; RVI-A §12.1.4
      .word 0x000082af             #: the A opcode with funct3=0 (only .W=2/.D=3 exist): cause 2, xtval the word. | D-RESERVED-DECODE; RVI-A §12.1.2

      lr.w x5, (x2)                #: after three refused words the machine is consistent: reserve A — rd <- 17. | RVI-A §12.1.2
      sc.w x9, x6, (x2)            #: the pair succeeds: rd <- 0, A <- 42. | RVI-A §12.1.2
      lw x8, x2, 0                 #: read-back: 42. | RVI-RV64I §3.1.3 #|end

handler:
      csrrs x11, mcause, x0        #: the handler observes cause 2 (every visit). | RVI-ZICSR §5.1.1
      csrrs x12, mtval, x0         #: xtval is the offending WORD (the diagnostic policy's explicit act, one layer up). | D-RESERVED-DECODE; RVP-MACHINE §2.1.1.16
      csrrs x13, mepc, x0          #: xepc is the .word's own address. | RVP-MACHINE §2.1.1.14
      addi x13, x13, 4             #: step past it. | RVI-RV32I §1.1.4
      csrrw x0, mepc, x13          #: write back the resume address. | RVI-ZICSR §5.1.1
      mret                         #: the stack pops per MPP and pc <- mepc. | RVP-MACHINE §2.1.3.2
