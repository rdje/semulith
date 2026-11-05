#|never: x28, x29
# a-lrsc-mustfail.s — every store-conditional must-fail that can fire at one hart
# (P4-SYSTEM.4 slice d, the brief's decision 8): rd <- 1 each time, memory proven
# untouched by read-back, and the machine still consistent enough to close on a
# succeeding pair. The other-hart and device must-fails are vacuous at harts=1.

      addi x10, x0, 1              #: raw material for the region base. | RVI-RV32I §1.1.4
      slli x10, x10, 31            #: x10 = 0x8000_0000. | RVI-RV64I §3.1.2.1
      addi x1, x10, 256            #: address A. | RVI-RV32I §1.1.4
      addi x2, x10, 264            #: address B. | RVI-RV32I §1.1.4
      addi x7, x0, 17              #: the initial word. | RVI-RV32I §1.1.4
      addi x6, x0, 42              #: the value every failed SC must NOT store. | RVI-RV32I §1.1.4

      sc.w x9, x6, (x1)            #: SC WITHOUT any LR: no matching reservation — rd <- 1, nothing stored (the reservation is empty anyway). | RVI-A §12.1.2; state.sexp's reservation candidate
      lw x8, x1, 0                 #: read-back: 0 — nothing was written. | RVI-RV64I §3.1.3

      sw x7, 0, x1                 #: A = 17. | RVI-RV64I §3.1.3
      sw x7, 0, x2                 #: B = 17. | RVI-RV64I §3.1.3
      lr.w x5, (x1)                #: reserve A: rd <- 17. | RVI-A §12.1.2
      sc.w x9, x6, (x2)            #: SC to a DIFFERENT address B: address-not-in-reservation-set — rd <- 1, nothing stored, the reservation clears. | RVI-A §12.1.2
      lw x8, x2, 0                 #: read-back: B still 17. | RVI-RV64I §3.1.3

      lr.w x5, (x1)                #: reserve A again. | RVI-A §12.1.2
      sc.w x9, x6, (x2)            #: an INTERVENING SC to any address (this one fails) — it clears the reservation too. | RVI-A §12.1.2
      sc.w x9, x6, (x1)            #: the pair is gone: rd <- 1, nothing stored. | RVI-A §12.1.2
      lw x8, x1, 0                 #: read-back: A still 17. | RVI-RV64I §3.1.3

      lr.w x5, (x1)                #: reserve A. | RVI-A §12.1.2
      lr.w x5, (x2)                #: a later LR REPLACES the reservation with B's. | RVI-A §12.1.2
      sc.w x9, x6, (x1)            #: an SC pairs only with the MOST RECENT LR: A mismatches — rd <- 1, nothing stored. | RVI-A §12.1.2
      lw x8, x1, 0                 #: read-back: A still 17. | RVI-RV64I §3.1.3

      lr.w x5, (x1)                #: reserve A at width .W. | RVI-A §12.1.2
      sc.d x9, x6, (x1)            #: a .D SC covers bytes OUTSIDE the four reserved — width mismatch, rd <- 1. | RVI-A §12.1.2; state.sexp's reservation candidate (the minimal set)
      lw x8, x1, 0                 #: read-back: A still 17. | RVI-RV64I §3.1.3

      lr.d x5, (x1)                #: reserve A at width .D. | RVI-A §12.1.2
      sc.w x9, x6, (x1)            #: the declared policy requires width EQUAL (decision 3, laboratory): rd <- 1. The spec's "within the reservation set" sentence ALONE would not force this cell (4 bytes lie within the 8) — the honest failure leg is the policy, recorded as such. | state.sexp's reservation candidate (decision 3); RVI-A §12.1.2
      lw x8, x1, 0                 #: read-back: A still 17. | RVI-RV64I §3.1.3

      lr.w x5, (x1)                #: reserve A one last time. | RVI-A §12.1.2
      sc.w x9, x6, (x1)            #: recovery: the fresh pair succeeds — rd <- 0, A <- 42, the machine stays consistent. | RVI-A §12.1.2
      lw x8, x1, 0                 #: read-back: 42. | RVI-RV64I §3.1.3
