#|never: x28, x29
# a-amo-minmax-w.s — the min/max AMOs at word width: signed vs unsigned on one cell
# (P4-SYSTEM.4 slice d). old = 0x8000_0005 — NEGATIVE signed, LARGE unsigned — so
# signed and unsigned orderings disagree and every cell's outcome names its rule.

      addi x10, x0, 1              #: raw material for the region base. | RVI-RV32I §1.1.4
      slli x10, x10, 31            #: x10 = 0x8000_0000. | RVI-RV64I §3.1.2.1
      addi x1, x10, 256            #: the cell's data address. | RVI-RV32I §1.1.4
      lui x7, 0x80000              #: bit 31 to the top — the low word is 0x8000_0000. | RVI-RV64I §3.1.2.1
      addi x7, x7, 5               #: x7's low word = 0x8000_0005: negative signed, huge unsigned. | RVI-RV32I §1.1.4
      addi x6, x0, 7               #: x6 = 7: positive either way. | RVI-RV32I §1.1.4

      sw x7, 0, x1                 #: mem = 0x8000_0005 (the signed-min cell). | RVI-RV64I §3.1.3
      amomin.w x5, x6, (x1)        #: SIGNED min(-2147483643, 7) = the old word; rd <- the OLD word sign-extended; mem stays 0x8000_0005. | RVI-A §12.1.4
      lw x8, x1, 0                 #: read-back: 0x8000_0005 — the signed minimum kept the negative old word. | RVI-RV64I §3.1.3

      sw x7, 0, x1                 #: mem = 0x8000_0005 (the signed-max cell). | RVI-RV64I §3.1.3
      amomax.w x5, x6, (x1)        #: SIGNED max(-2147483643, 7) = 7; rd <- the old word sign-extended; mem <- 7. | RVI-A §12.1.4
      lw x8, x1, 0                 #: read-back: 7. | RVI-RV64I §3.1.3

      sw x7, 0, x1                 #: mem = 0x8000_0005 (the unsigned-min cell). | RVI-RV64I §3.1.3
      amominu.w x5, x6, (x1)       #: UNSIGNED min(0x80000005, 7) = 7 — the SAME operands, the other ordering; rd <- the old word sign-extended; mem <- 7. | RVI-A §12.1.4
      lw x8, x1, 0                 #: read-back: 7. | RVI-RV64I §3.1.3

      sw x7, 0, x1                 #: mem = 0x8000_0005 (the unsigned-max cell). | RVI-RV64I §3.1.3
      amomaxu.w x5, x6, (x1)       #: UNSIGNED max(0x80000005, 7) = the old word; rd <- the old word sign-extended; mem stays 0x8000_0005. | RVI-A §12.1.4
      lw x8, x1, 0                 #: read-back: 0x8000_0005 — the unsigned maximum kept the huge old word. | RVI-RV64I §3.1.3
