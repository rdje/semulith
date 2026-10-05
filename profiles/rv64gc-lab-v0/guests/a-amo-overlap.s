#|never: x28, x29
# a-amo-overlap.s — register aliasing on the A forms (P4-SYSTEM.4 slice d): rd=rs1=rs2,
# rd=rs2, rd=rs1. Register reads see the PRE-INSTRUCTION register file (the language's
# READS-AND-WRITES contract), so the address and the operand are the old contents and
# rd still lands its own value.

      addi x10, x0, 1              #: raw material for the region base. | RVI-RV32I §1.1.4
      slli x10, x10, 31            #: x10 = 0x8000_0000. | RVI-RV64I §3.1.2.1
      addi x1, x10, 256            #: the cell's data address. | RVI-RV32I §1.1.4
      addi x7, x0, 16              #: the initial word 0x10. | RVI-RV32I §1.1.4

      sw x7, 0, x1                 #: mem = 0x10 (the rd=rs1=rs2 cell). | RVI-RV64I §3.1.3
      amoadd.w x1, x1, (x1)        #: rs1's PRE-value is the address AND the added value: mem <- 0x10 + low32(0x80000100) = 0x80000110; rd <- the old word 0x10. | RVI-A §12.1.4; the READS-AND-WRITES contract (schema/semantics.sexp)
      addi x1, x10, 256            #: re-establish the address (x1 was consumed above). | RVI-RV32I §1.1.4
      lw x8, x1, 0                 #: read-back: 0x80000110. | RVI-RV64I §3.1.3

      addi x6, x0, 5               #: rs2 = 5 (the rd=rs2 cell). | RVI-RV32I §1.1.4
      amoadd.w x6, x6, (x1)        #: rs2's PRE-value (5) is added: mem <- 0x80000110 + 5 = 0x80000115; rd <- the old word 0x80000110, sign-extended (0xFFFFFFFF80000110). | RVI-A §12.1.4; the READS-AND-WRITES contract
      lw x8, x1, 0                 #: read-back: 0x80000115. | RVI-RV64I §3.1.3

      lr.w x1, (x1)                #: rd=rs1 on LR: the address is x1's PRE-value; rd <- the old word 0x80000115 sign-extended, and the reservation registers. | RVI-A §12.1.2; the READS-AND-WRITES contract
      addi x1, x10, 256            #: re-establish the address. | RVI-RV32I §1.1.4
      addi x6, x0, 7               #: rs2 = 7 (the rd=rs2 SC cell). | RVI-RV32I §1.1.4
      sc.w x6, x6, (x1)            #: the reservation pairs: mem <- rs2's PRE-value 7; rd <- the success code 0. | RVI-A §12.1.2; the READS-AND-WRITES contract
      lw x8, x1, 0                 #: read-back: 7. | RVI-RV64I §3.1.3
