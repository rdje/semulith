#|never: x28, x29
# a-amo-arith-w.s — the five arithmetic AMOs at word width (P4-SYSTEM.4 slice d).
# Each cell: store the initial word, run the AMO, read the word back. The initial
# 0x8000_0005 has bit 31 SET, so rd's sign extension of the old word is observable
# (D-LOAD-EXT's word edge), and the wrapped 32-bit add shows the width discipline.

      addi x10, x0, 1              #: raw material for the region base. | RVI-RV32I §1.1.4
      slli x10, x10, 31            #: x10 = 0x8000_0000, the declared region's base. | RVI-RV64I §3.1.2.1
      addi x1, x10, 256            #: the cell's data address, clear of the code. | RVI-RV32I §1.1.4
      lui x7, 0x80000              #: bit 31 rides to the top — the low word is 0x8000_0000. | RVI-RV64I §3.1.2.1
      addi x7, x7, 5               #: x7's low word = 0x8000_0005: the sign-edge initial value. | RVI-RV32I §1.1.4
      lui x6, 0x80000              #: rs2's low word starts at 0x8000_0000. | RVI-RV64I §3.1.2.1
      addi x6, x6, 3               #: x6's low word = 0x8000_0003. | RVI-RV32I §1.1.4

      sw x7, 0, x1                 #: mem = 0x8000_0005 (the add cell's initial). | RVI-RV64I §3.1.3
      amoadd.w x5, x6, (x1)        #: rd <- the OLD word 0x8000_0005, SIGN-EXTENDED (0xFFFFFFFF80000005); mem <- old + rs2 = 0x00000008 (32-bit wrap). | RVI-A §12.1.4
      lw x8, x1, 0                 #: read-back: 0x00000008 — the wrapped add landed. | RVI-RV64I §3.1.3

      sw x7, 0, x1                 #: mem = 0x8000_0005 (the swap cell). | RVI-RV64I §3.1.3
      amoswap.w x5, x6, (x1)       #: rd <- the old word sign-extended; mem <- rs2 = 0x8000_0003. | RVI-A §12.1.4
      lw x8, x1, 0                 #: read-back: 0x8000_0003. | RVI-RV64I §3.1.3

      sw x7, 0, x1                 #: mem = 0x8000_0005 (the xor cell). | RVI-RV64I §3.1.3
      amoxor.w x5, x6, (x1)        #: rd <- the old word sign-extended; mem <- 0x8000_0005 XOR 0x8000_0003 = 0x00000006. | RVI-A §12.1.4
      lw x8, x1, 0                 #: read-back: 0x00000006. | RVI-RV64I §3.1.3

      sw x7, 0, x1                 #: mem = 0x8000_0005 (the and cell). | RVI-RV64I §3.1.3
      amoand.w x5, x6, (x1)        #: rd <- the old word sign-extended; mem <- 0x8000_0005 AND 0x8000_0003 = 0x8000_0001. | RVI-A §12.1.4
      lw x8, x1, 0                 #: read-back: 0x8000_0001. | RVI-RV64I §3.1.3

      sw x7, 0, x1                 #: mem = 0x8000_0005 (the or cell). | RVI-RV64I §3.1.3
      amoor.w x5, x6, (x1)         #: rd <- the old word sign-extended; mem <- 0x8000_0005 OR 0x8000_0003 = 0x8000_0007. | RVI-A §12.1.4
      lw x8, x1, 0                 #: read-back: 0x8000_0007. | RVI-RV64I §3.1.3
