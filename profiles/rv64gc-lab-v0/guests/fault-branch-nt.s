# fault-branch-nt.s — the P2-SCALAR.3 suppressed-effect guest (SEM-06).
#
# D-MISALIGN-REPORT: "No instruction-address-misaligned exception is generated for a
# conditional branch that is not taken." Every branch below points at a MISALIGNED
# target (+6 or +10, both 2 mod 4) and every one is NOT taken — so nothing is raised
# and the fall-through writes happen. One taken branch to an ALIGNED target closes the
# guest, proving the branches themselves were live (its skipped addi is never written).

      addi  x1, x0, 1          # x1 = 1: the operand that makes every condition false below
      beq   x0, x1, 6          # not taken (0 != 1); target 0x8000000A is misaligned — nothing raised
      addi  x2, x0, 2          # fall-through proves continuation
      bne   x0, x0, 6          # not taken (0 == 0); target misaligned
      addi  x3, x0, 3
      blt   x1, x0, 6          # not taken (1 >= 0 signed); target misaligned
      addi  x4, x0, 4
      bge   x0, x1, 6          # not taken (0 < 1 signed); target misaligned
      addi  x5, x0, 5
      bltu  x1, x0, 10         # not taken (1 >= 0 unsigned); target 0x8000002A misaligned
      addi  x6, x0, 6
      bgeu  x0, x1, 10         # not taken (0 < 1 unsigned); target misaligned
      addi  x7, x0, 7
      beq   x0, x0, 8          # TAKEN to an aligned target — the branches are live
      addi  x8, x0, 8          # skipped: x8 must never be written
      addi  x9, x0, 9          # landing
