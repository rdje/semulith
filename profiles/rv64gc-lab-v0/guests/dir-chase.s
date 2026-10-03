# dir-chase.s — the P2-SCALAR.5 strand-3 guest: a loaded value used as an ADDRESS — the
# pointer chase and the jump table (the census's gap 2: every jalr base in the corpus was
# materialized, never loaded; the idiom existed nowhere, including the compiled guest).
#
# Three data cells live past the code (entry+0x60/0x68/0x70), store-initialized; then a
# load's result is used as the next load's address (the chase), and a load's result is
# used as a JALR target (the jump through memory). Addresses are auipc-materialized with
# the arithmetic shown per line — the assembler's word positions are the derivation.

      auipc x1, 0              # x1 = 0x80000000 (this instruction's pc)
      addi  x1, x1, 96         # x1 = 0x80000060 — &cell0
      addi  x7, x0, 42         # x7 = 42 — the chase's payload
      sd    x7, 16, x1         # cell2 (0x80000070) <- 42
      auipc x2, 0              # x2 = 0x80000010
      addi  x2, x2, 96         # x2 = 0x80000070 — &cell2
      sd    x2, 0, x1          # cell0 (0x80000060) <- &cell2 — the chase pointer
      auipc x3, 0              # x3 = 0x8000001c
      addi  x3, x3, 28         # x3 = 0x80000038 — the stub's address
      sd    x3, 8, x1          # cell1 (0x80000068) <- the stub — the jump-table entry
      ld    x4, x1, 0          # x4 = &cell2 — a LOADED value becomes an address
      ld    x5, x4, 0          # x5 = 42 — the chase lands
      ld    x6, x1, 8          # x6 = the stub's address — the table read
      jalr  x0, x6, 0          # the jump through memory; the link targets x0 (discarded)
      addi  x8, x0, 7          # the stub (entry+0x38): reached ONLY through the table
      addi  x9, x0, 9
      ebreak                   # the run ends on the requested trap (cause 0x03)
