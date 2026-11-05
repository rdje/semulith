# bound-shift.s — the P2-SCALAR.2 boundary guest for the 64-bit shift forms: the
# 6-bit shift-amount domain exercised EXHAUSTIVELY (one srli sweep over all 64 amounts
# of one operand), every shamt bit pinned on slli and srai, and the register-amount
# corners rs2 = 64 and rs2 = -1 (D-SHAMT).
#
# The operand X = 0x8000000000000001 is built only from already-covered forms. Bit 63
# makes the srai sign fill and the srli zero fill visible; bit 0 walks up through every
# slli and out at shamt 63. The srli sweep's 64 results are pairwise distinct, and the
# srl-by-64 identity is pre-written with -1, because the laboratory's observation
# vocabulary is the VISIBLE register change.

      lui x8, 0x80000               # build X: 0xFFFFFFFF80000000 …
      slli x8, x8, 32               # … shifted left 32: 0x8000000000000000 …
      addi x8, x8, 1                # … X = 0x8000000000000001: bit 63 AND bit 0 set

      # ---- the 6-bit shamt domain, EXHAUSTED: srli by every amount 0..63 ----
      # The 64 results are pairwise distinct, so every step is a visible change.
      srli x9, x8, 0                # shamt 0: the identity
      srli x9, x8, 1
      srli x9, x8, 2
      srli x9, x8, 3
      srli x9, x8, 4
      srli x9, x8, 5
      srli x9, x8, 6
      srli x9, x8, 7
      srli x9, x8, 8
      srli x9, x8, 9
      srli x9, x8, 10
      srli x9, x8, 11
      srli x9, x8, 12
      srli x9, x8, 13
      srli x9, x8, 14
      srli x9, x8, 15
      srli x9, x8, 16
      srli x9, x8, 17
      srli x9, x8, 18
      srli x9, x8, 19
      srli x9, x8, 20
      srli x9, x8, 21
      srli x9, x8, 22
      srli x9, x8, 23
      srli x9, x8, 24
      srli x9, x8, 25
      srli x9, x8, 26
      srli x9, x8, 27
      srli x9, x8, 28
      srli x9, x8, 29
      srli x9, x8, 30
      srli x9, x8, 31
      srli x9, x8, 32
      srli x9, x8, 33
      srli x9, x8, 34
      srli x9, x8, 35
      srli x9, x8, 36
      srli x9, x8, 37
      srli x9, x8, 38
      srli x9, x8, 39
      srli x9, x8, 40
      srli x9, x8, 41
      srli x9, x8, 42
      srli x9, x8, 43
      srli x9, x8, 44
      srli x9, x8, 45
      srli x9, x8, 46
      srli x9, x8, 47
      srli x9, x8, 48
      srli x9, x8, 49
      srli x9, x8, 50
      srli x9, x8, 51
      srli x9, x8, 52
      srli x9, x8, 53
      srli x9, x8, 54
      srli x9, x8, 55
      srli x9, x8, 56
      srli x9, x8, 57
      srli x9, x8, 58
      srli x9, x8, 59
      srli x9, x8, 60
      srli x9, x8, 61
      srli x9, x8, 62
      srli x9, x8, 63               # shamt 63: only bit 63 survives

      # ---- srai / slli: the bit-pinning set {0,1,2,4,8,16,32,63} — every shamt
      #      bit pinned on every form; the sign fill (srai) and the discard (slli).
      srai x20, x8, 0
      srai x20, x8, 1
      srai x20, x8, 2
      srai x20, x8, 4
      srai x20, x8, 8
      srai x20, x8, 16
      srai x20, x8, 32
      srai x20, x8, 63
      slli x21, x8, 0
      slli x21, x8, 1
      slli x21, x8, 2
      slli x21, x8, 4
      slli x21, x8, 8
      slli x21, x8, 16
      slli x21, x8, 32
      slli x21, x8, 63

      # ---- register-amount corners: the amount is rs2's LOW 6 BITS ----
      addi x10, x0, 64              # 64: a 6-bit read sees 0
      addi x11, x0, -1              # pre-write: the identity result below must be a VISIBLE change
      srl x11, x8, x10              # rs2[5:0] = 0: the identity, observed as -1 -> X
      addi x12, x0, -1              # -1: every low-6 read sees 63
      sll x13, x8, x12              # rs2[5:0] = 63: bit 0 walks to bit 63
      sra x14, x8, x12              # rs2[5:0] = 63: all sign
