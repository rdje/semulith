#|never: x28, x29
# a-amo-minmax-d.s — the min/max AMOs at doubleword width (P4-SYSTEM.4 slice d).
# old = -5 (huge unsigned), rs2 = 7: again the signed and unsigned orderings disagree.

      addi x10, x0, 1              #: raw material for the region base. | RVI-RV32I §1.1.4
      slli x10, x10, 31            #: x10 = 0x8000_0000. | RVI-RV64I §3.1.2.1
      addi x1, x10, 256            #: the cell's data address. | RVI-RV32I §1.1.4
      addi x7, x0, -5              #: x7 = -5: negative signed, huge unsigned. | RVI-RV32I §1.1.4
      addi x6, x0, 7               #: x6 = 7. | RVI-RV32I §1.1.4

      sd x7, 0, x1                 #: mem = -5 (the signed-min cell). | RVI-RV64I §3.1.3
      amomin.d x5, x6, (x1)        #: SIGNED min(-5, 7) = -5; rd <- the old doubleword; mem stays -5. | RVI-A §12.1.4
      ld x8, x1, 0                 #: read-back: -5. | RVI-RV64I §3.1.3

      sd x7, 0, x1                 #: mem = -5 (the signed-max cell). | RVI-RV64I §3.1.3
      amomax.d x5, x6, (x1)        #: SIGNED max(-5, 7) = 7; rd <- the old doubleword; mem <- 7. | RVI-A §12.1.4
      ld x8, x1, 0                 #: read-back: 7. | RVI-RV64I §3.1.3

      sd x7, 0, x1                 #: mem = -5 (the unsigned-min cell). | RVI-RV64I §3.1.3
      amominu.d x5, x6, (x1)       #: UNSIGNED min(0xFF…FB, 7) = 7; rd <- the old doubleword; mem <- 7. | RVI-A §12.1.4
      ld x8, x1, 0                 #: read-back: 7. | RVI-RV64I §3.1.3

      sd x7, 0, x1                 #: mem = -5 (the unsigned-max cell). | RVI-RV64I §3.1.3
      amomaxu.d x5, x6, (x1)       #: UNSIGNED max(0xFF…FB, 7) = the old doubleword; rd <- the old doubleword; mem stays -5. | RVI-A §12.1.4
      ld x8, x1, 0                 #: read-back: -5. | RVI-RV64I §3.1.3
