#|never: x28, x29
# a-amo-arith-d.s — the five arithmetic AMOs at doubleword width (P4-SYSTEM.4 slice d).
# old = -5, rs2 = 7: the XOR/OR/AND cells exercise negative operands, and rd is the
# old doubleword (no extension at XLEN).

      addi x10, x0, 1              #: raw material for the region base. | RVI-RV32I §1.1.4
      slli x10, x10, 31            #: x10 = 0x8000_0000. | RVI-RV64I §3.1.2.1
      addi x1, x10, 256            #: the cell's data address. | RVI-RV32I §1.1.4
      addi x7, x0, -5              #: x7 = -5 = 0xFFFFFFFFFFFFFFFB: a negative initial value. | RVI-RV32I §1.1.4
      addi x6, x0, 7               #: x6 = 7. | RVI-RV32I §1.1.4

      sd x7, 0, x1                 #: mem = -5 (the add cell). | RVI-RV64I §3.1.3
      amoadd.d x5, x6, (x1)        #: rd <- the old doubleword -5; mem <- -5 + 7 = 2. | RVI-A §12.1.4
      ld x8, x1, 0                 #: read-back: 2. | RVI-RV64I §3.1.3

      sd x7, 0, x1                 #: mem = -5 (the swap cell). | RVI-RV64I §3.1.3
      amoswap.d x5, x6, (x1)       #: rd <- -5; mem <- 7. | RVI-A §12.1.4
      ld x8, x1, 0                 #: read-back: 7. | RVI-RV64I §3.1.3

      sd x7, 0, x1                 #: mem = -5 (the xor cell). | RVI-RV64I §3.1.3
      amoxor.d x5, x6, (x1)        #: rd <- -5; mem <- -5 XOR 7 = 0xFFFFFFFFFFFFFFFC (-4). | RVI-A §12.1.4
      ld x8, x1, 0                 #: read-back: -4. | RVI-RV64I §3.1.3

      sd x7, 0, x1                 #: mem = -5 (the and cell). | RVI-RV64I §3.1.3
      amoand.d x5, x6, (x1)        #: rd <- -5; mem <- -5 AND 7 = 3. | RVI-A §12.1.4
      ld x8, x1, 0                 #: read-back: 3. | RVI-RV64I §3.1.3

      sd x7, 0, x1                 #: mem = -5 (the or cell). | RVI-RV64I §3.1.3
      amoor.d x5, x6, (x1)         #: rd <- -5; mem <- -5 OR 7 = 0xFFFFFFFFFFFFFFFF (-1). | RVI-A §12.1.4
      ld x8, x1, 0                 #: read-back: -1. | RVI-RV64I §3.1.3
