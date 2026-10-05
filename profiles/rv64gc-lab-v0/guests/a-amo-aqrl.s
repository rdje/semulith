#|never: x28, x29
# a-amo-aqrl.s — every aq/rl combination executes identically at one hart
# (P4-SYSTEM.4 decision 1): all four decode, and every effect is defined "as viewed
# by other RISC-V harts" (RVI-A §12.1.1), so at harts=1 the suffix orders nothing
# observable — the same sequence is run four times and lands the same values.

      addi x10, x0, 1              #: raw material for the region base. | RVI-RV32I §1.1.4
      slli x10, x10, 31            #: x10 = 0x8000_0000. | RVI-RV64I §3.1.2.1
      addi x1, x10, 256            #: the cell's data address. | RVI-RV32I §1.1.4
      addi x7, x0, 41              #: the cell's value. | RVI-RV32I §1.1.4
      addi x6, x0, 1               #: the increment. | RVI-RV32I §1.1.4

      sw x7, 0, x1                 #: mem = 41 (suffix: none). | RVI-RV64I §3.1.3
      amoadd.w x5, x6, (x1)        #: no suffix: rd <- 41, mem <- 42. | RVI-A §12.1.1
      lw x8, x1, 0                 #: read-back: 42. | RVI-RV64I §3.1.3

      sw x7, 0, x1                 #: mem = 41 (suffix: .aq). | RVI-RV64I §3.1.3
      amoadd.w.aq x5, x6, (x1)     #: .aq: rd <- 41, mem <- 42 — identical at one hart. | RVI-A §12.1.1
      lw x8, x1, 0                 #: read-back: 42. | RVI-RV64I §3.1.3

      sw x7, 0, x1                 #: mem = 41 (suffix: .rl). | RVI-RV64I §3.1.3
      amoadd.w.rl x5, x6, (x1)     #: .rl: rd <- 41, mem <- 42 — identical at one hart. | RVI-A §12.1.1
      lw x8, x1, 0                 #: read-back: 42. | RVI-RV64I §3.1.3

      sw x7, 0, x1                 #: mem = 41 (suffix: .aqrl). | RVI-RV64I §3.1.3
      amoadd.w.aqrl x5, x6, (x1)   #: .aqrl: rd <- 41, mem <- 42 — identical at one hart. | RVI-A §12.1.1
      lw x8, x1, 0                 #: read-back: 42. | RVI-RV64I §3.1.3

      sw x7, 0, x1                 #: mem = 41 (the LR/SC suffix pair). | RVI-RV64I §3.1.3
      lr.w.aqrl x5, (x1)           #: LR with BOTH bits set decodes and reserves identically: rd <- 41. | RVI-A §12.1.1–§12.1.2
      sc.w.aq x9, x6, (x1)         #: the .aq SC pairs and succeeds: rd <- 0, mem <- 1. | RVI-A §12.1.1–§12.1.2
      lw x8, x1, 0                 #: read-back: 1. | RVI-RV64I §3.1.3
