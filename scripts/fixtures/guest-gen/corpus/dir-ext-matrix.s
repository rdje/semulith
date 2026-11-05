# dir-ext-matrix.s — the P2-SCALAR.5 strand-3 guest: the cross-width SIGN-EXTENDING
# round-trip matrix at the sign edges (the census's gap 3: same-width sign/zero pairs are
# pinned by bound-ext, zero-extending wider reads by scope-mem/bound-alias — but a narrow
# store read back WIDER, and a wide store read at a narrow HIGH lane whose top bit is
# set, were pinned nowhere).
#
# One scratch cell (entry+0x60), explicitly re-zeroed between widths — memory contents
# are not an entry-state promise (D-ENTRY-STATE covers registers). Every value below is
# the little-endian lane composition (D-ENDIAN) under the read width's extension rule
# (D-LOAD-EXT): the READ's width governs, so the interesting edges are the lanes whose
# top bit stands — byte 1 of a stored 0x8000, the high half of 0x80000000, the high word
# of 0x8000000000000000.

      auipc x1, 0              # x1 = 0x80000000
      addi  x1, x1, 160        # x1 = &cell (entry+0xA0 — PAST the code's 0x8C end)
      sd    x0, 0, x1          # cell <- 0 (explicit — no entry-state promise)
# ---- byte edge: store 0x80 as a byte, read back at every width
      addi  x2, x0, 128        # x2 = 0x80
      sb    x2, 0, x1          # cell.b0 <- 0x80 (bytes 80 00 00 …)
      lb    x5, x1, 0          # sign: 0xFF…FF80
      lbu   x6, x1, 0          # zero: 0x80
      lh    x7, x1, 0          # 0x0080 — b1 is zero
      lw    x8, x1, 0          # 0x00000080
      ld    x9, x1, 0          # 0x80
# ---- half edge: store 0x8000 as a halfword, read the HIGH BYTE's sign
      sd    x0, 0, x1          # re-zero
      lui   x2, 8              # x2 = 0x8000
      sh    x2, 0, x1          # cell.h0 <- 0x8000 (bytes 00 80 00 …)
      lb    x5, x1, 0          # b0 = 0x00 → 0
      lb    x6, x1, 1          # b1 = 0x80 → 0xFF…FF80 — the high lane signs
      lhu   x7, x1, 0          # zero: 0x8000
      lh    x8, x1, 0          # sign: 0xFFFF8000
      lw    x9, x1, 0          # 0x00008000
      ld    x10, x1, 0         # 0x8000
# ---- word edge: store 0x80000000, read the high half's sign
      sd    x0, 0, x1          # re-zero
      lui   x2, 0x80000        # x2 = 0xFFFFFFFF80000000 (LUI sign-extends; the store keeps the low 32)
      sw    x2, 0, x1          # cell.w0 <- 0x80000000 (bytes 00 00 00 80)
      lb    x5, x1, 3          # b3 = 0x80 → 0xFF…FF80
      lh    x6, x1, 2          # high half 0x8000 → 0xFFFF8000
      lwu   x7, x1, 0          # zero: 0x80000000 — the RV64-only form
      lw    x8, x1, 0          # sign: 0xFFFFFFFF80000000
      ld    x9, x1, 0          # 0x80000000
# ---- double edge: 0x8000000000000000, read the high word's sign
      lui   x2, 0x80000        # 0xFFFFFFFF80000000
      slli  x2, x2, 32         # 0x8000000000000000
      sd    x2, 0, x1          # the full-width store needs no re-zero
      lb    x5, x1, 7          # b7 = 0x80 → 0xFF…FF80
      lh    x6, x1, 6          # 0x8000 → 0xFFFF8000
      lw    x7, x1, 4          # high word 0x80000000 → 0xFFFFFFFF80000000
      ld    x8, x1, 0          # the value itself
      addi  x11, x0, 1         # landing: the whole matrix retired
