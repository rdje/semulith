# dir-chain.s — the P2-SCALAR.5 strand-3 guest: a 14-link serial dependency chain through
# VARIED producers (the census's gap 7: the deepest pinned chains were 7–8 links of a
# single producer). Every link consumes the previous link's result: immediate, register,
# shift, a store→load boundary crossing mid-chain, a *W form, and a closing compare.

      auipc x1, 0              # x1 = 0x80000000
      addi  x1, x1, 96         # x1 = &cell (entry+0x60, past the code)
      addi  x6, x0, 2          # the register operand
      addi  x7, x0, 100        # the closing compare's bound
      addi  x5, x0, 1          # link 1:  1
      slli  x5, x5, 4          # link 2:  1 << 4 = 16
      addi  x5, x5, 3          # link 3:  19
      sll   x5, x5, x6         # link 4:  19 << 2 = 76 (register amount)
      sd    x5, 0, x1          # link 5:  the chain crosses the boundary …
      ld    x5, x1, 0          # link 6:  … and comes back: 76
      srai  x5, x5, 1          # link 7:  38 (arithmetic — the sign bit is clear)
      addw  x5, x5, x6         # link 8:  40 (the *W form: 32-bit wrap + sign-extend)
      xori  x5, x5, 0xFF       # link 9:  40 ^ 255 = 215
      srli  x5, x5, 2          # link 10: 53
      addiw x5, x5, 7          # link 11: 60 (the *W immediate form)
      andi  x5, x5, 62         # link 12: 60 & 62 = 60
      subw  x5, x5, x6         # link 13: 58
      sltu  x5, x5, x7         # link 14: 58 < 100 unsigned → 1
      addi  x8, x0, 8          # landing: the whole chain retired
