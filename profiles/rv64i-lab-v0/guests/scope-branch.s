# scope-branch.s — the P2-SCALAR.1 scope-completion guest: the five conditional branches
# no tracked guest exercised yet (BEQ, BLT, BGE, BLTU, BGEU), each taken AND not taken.
#
# A branch writes no register either way, so the observations are the surrounding ones:
# a TAKEN branch skips an instruction that would have written a register (the negative
# observation — x20..x24 must never be written), and a NOT-taken branch falls through to
# a write that must happen. The operands x1 = x2 = 5 and x3 = -1 make signedness visible:
# -1 is the smallest signed value and the largest unsigned one, so BLT/BGE and
# BLTU/BGEU answer oppositely on the same register pair.

        addi  x1, x0, 5
        addi  x2, x0, 5
        addi  x3, x0, -1

        beq   x1, x2, l_blt    # taken: equal operands
        addi  x20, x0, 1       # NEVER EXECUTED — the first negative observation
l_blt:  beq   x1, x3, l_blt2   # NOT taken: 5 != -1
        addi  x4, x0, 1        # the fall-through write that must happen

l_blt2: blt   x3, x1, l_bge    # taken: -1 < 5 signed
        addi  x21, x0, 1       # NEVER EXECUTED
l_bge:  blt   x1, x3, l_bge2   # NOT taken: 5 < -1 is false signed
        addi  x5, x0, 1

l_bge2: bge   x1, x3, l_bltu   # taken: 5 >= -1 signed
        addi  x22, x0, 1       # NEVER EXECUTED
l_bltu: bge   x3, x1, l_bltu2  # NOT taken: -1 >= 5 is false signed
        addi  x6, x0, 1

l_bltu2: bltu x1, x3, l_bgeu   # taken: 5 < 0xFFFF…FF unsigned
        addi  x23, x0, 1       # NEVER EXECUTED
l_bgeu: bltu  x3, x1, l_bgeu2  # NOT taken: the largest unsigned value is not below 5
        addi  x7, x0, 1

l_bgeu2: bgeu x3, x1, l_end    # taken: 0xFFFF…FF >= 5 unsigned — BGE's opposite answer
        addi  x24, x0, 1       # NEVER EXECUTED
l_end:  bgeu  x1, x3, l_done   # NOT taken: 5 >= 0xFFFF…FF is false unsigned
        addi  x8, x0, 1

l_done: addi  x9, x0, 1        # the end marker: control reached here
