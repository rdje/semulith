#|never: x28, x29
# a-lrsc-pair.s — the load-reserved / store-conditional pairs succeeding
# (P4-SYSTEM.4 slice d): rd <- 0 on success, the store observed by read-back — the
# bound-ext pattern — at both widths, at the sign edge for .W.

      addi x10, x0, 1              #: raw material for the region base. | RVI-RV32I §1.1.4
      slli x10, x10, 31            #: x10 = 0x8000_0000. | RVI-RV64I §3.1.2.1
      addi x1, x10, 256            #: the pair's data address. | RVI-RV32I §1.1.4
      lui x7, 0x80000              #: bit 31 to the top. | RVI-RV64I §3.1.2.1
      addi x7, x7, 5               #: x7's low word = 0x8000_0005 (the sign edge). | RVI-RV32I §1.1.4
      addi x6, x0, 42              #: the value the SC stores. | RVI-RV32I §1.1.4

      sw x7, 0, x1                 #: mem = 0x8000_0005 (the .W pair). | RVI-RV64I §3.1.3
      lr.w x5, (x1)                #: LR loads the word SIGN-EXTENDED (0xFFFFFFFF80000005) and registers the reservation. | RVI-A §12.1.2
      sc.w x9, x6, (x1)            #: the reservation matches (valid ∧ PA equal ∧ width equal): the store lands, rd <- 0, the reservation clears. | RVI-A §12.1.2; state.sexp's reservation candidate
      lw x8, x1, 0                 #: read-back: 42 — the conditional store is observed in memory. | RVI-RV64I §3.1.3

      sd x7, 0, x1                 #: mem = the same value as a doubleword (the .D pair). | RVI-RV64I §3.1.3
      lr.d x5, (x1)                #: LR.D loads the full doubleword (0xFFFFFFFF80000005) and reserves. | RVI-A §12.1.2
      sc.d x9, x6, (x1)            #: the .D reservation matches: the store lands, rd <- 0. | RVI-A §12.1.2
      ld x8, x1, 0                 #: read-back: 42. | RVI-RV64I §3.1.3
