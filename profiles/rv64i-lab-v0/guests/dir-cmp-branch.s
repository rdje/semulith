# dir-cmp-branch.s — the P2-SCALAR.5 strand-3 guest: the compare→branch idiom — a branch
# whose condition register is written by the IMMEDIATELY PRECEDING slt/slti/sub (the
# census's gap 5: corpus compares are observed as writes, ACT4's slt is compare-and-store;
# nobody branched on a freshly computed predicate). Taken AND not-taken on both senses.

      addi  x5, x0, 5
      addi  x6, x0, 7
      slt   x7, x5, x6         # 5 < 7 → 1
      bne   x7, x0, l1         # TAKEN on the computed predicate — skips the marker
      addi  x8, x0, 17         # never executes
l1:   slti  x7, x6, 0          # 7 < 0 → 0
      beq   x7, x0, l2         # TAKEN (equal) — skips the marker
      addi  x8, x0, 34         # never executes
l2:   sub   x7, x6, x6         # 0
      bne   x7, x0, l3         # NOT taken — falls through
      addi  x9, x0, 3          # executes
l3:   slt   x7, x5, x6         # 1 (recomputed)
      beq   x7, x0, l4         # NOT taken (1 != 0) — falls through
      addi  x10, x0, 4         # executes
l4:   addi  x11, x0, 11        # landing: two taken, two not-taken, all four senses
