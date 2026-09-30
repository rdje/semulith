# dir-memwalk.s — the P2-SCALAR.5 strand-3 guest: a loop that LOADS AND STORES every
# iteration (the census's gap 6: c-scope's loop only stores; the corpus's other memory
# guests are straight-line). Four cells copied forward under a counted loop — the memory
# walk with a carried induction register, ending on the requested trap.
#
# Data: src at entry+0x60 (four cells, store-initialized), dst at entry+0xA0 — both past
# the code (which ends at entry+0x4C). The bne target is a label; the loop body is six
# instructions.

      auipc x1, 0              # x1 = 0x80000000
      addi  x1, x1, 96         # x1 = &src
      addi  x2, x0, 10
      sd    x2, 0, x1          # src[0] <- 10
      addi  x2, x0, 20
      sd    x2, 8, x1          # src[1] <- 20
      addi  x2, x0, 30
      sd    x2, 16, x1         # src[2] <- 30
      addi  x2, x0, 40
      sd    x2, 24, x1         # src[3] <- 40
      addi  x3, x0, 4          # the countdown
      addi  x4, x1, 64         # x4 = &dst
loop: ld    x5, x1, 0          # LOAD …
      sd    x5, 0, x4          # … and STORE in the same iteration
      addi  x1, x1, 8          # the walk advances both pointers
      addi  x4, x4, 8
      addi  x3, x3, -1
      bne   x3, x0, loop
      ebreak                   # the copy completed: requested trap (cause 0x03)
