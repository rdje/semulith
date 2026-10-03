# bound-shiftw.s — the P2-SCALAR.2 boundary guest for the *W shift forms: the 5-bit
# shift-amount domain exercised EXHAUSTIVELY (one sraiw sweep over all 32 amounts),
# every shamt bit pinned on slliw and srliw, and the 5-bit vs 6-bit register-amount
# discriminator rs2 = 96 as an srl/srlw pair on identical operands (D-SHAMT, D-WSUFFIX).
#
# The operand's low 32 bits are 0x80000001: bit 31 drives both the arithmetic fill
# within the word and the *W sign extension of the result; bit 0 walks the left
# shifts. The srlw identity under rs2 = 96 is pre-written with 1 so it lands as a
# visible change.

      lui x8, 0x80000               # build X: 0xFFFFFFFF80000000 …
      addi x8, x8, 1                # … X = 0xFFFFFFFF80000001; low32 = 0x80000001

      # ---- the 5-bit shamt domain, EXHAUSTED: sraiw by every amount 0..31 ----
      # Sign fill inside 32 bits, then the *W sign extension; 32 distinct results.
      sraiw x9, x8, 0               # shamt 0: the identity — and the *W sign extension is STILL applied
      sraiw x9, x8, 1
      sraiw x9, x8, 2
      sraiw x9, x8, 3
      sraiw x9, x8, 4
      sraiw x9, x8, 5
      sraiw x9, x8, 6
      sraiw x9, x8, 7
      sraiw x9, x8, 8
      sraiw x9, x8, 9
      sraiw x9, x8, 10
      sraiw x9, x8, 11
      sraiw x9, x8, 12
      sraiw x9, x8, 13
      sraiw x9, x8, 14
      sraiw x9, x8, 15
      sraiw x9, x8, 16
      sraiw x9, x8, 17
      sraiw x9, x8, 18
      sraiw x9, x8, 19
      sraiw x9, x8, 20
      sraiw x9, x8, 21
      sraiw x9, x8, 22
      sraiw x9, x8, 23
      sraiw x9, x8, 24
      sraiw x9, x8, 25
      sraiw x9, x8, 26
      sraiw x9, x8, 27
      sraiw x9, x8, 28
      sraiw x9, x8, 29
      sraiw x9, x8, 30
      sraiw x9, x8, 31              # shamt 31: all sign, 0xFFFFFFFFFFFFFFFF

      # ---- srliw / slliw: the bit-pinning set {0,1,2,4,8,16,31} ----
      srliw x20, x8, 0
      srliw x20, x8, 1
      srliw x20, x8, 2
      srliw x20, x8, 4
      srliw x20, x8, 8
      srliw x20, x8, 16
      srliw x20, x8, 31
      slliw x21, x8, 0
      slliw x21, x8, 1
      slliw x21, x8, 2
      slliw x21, x8, 4
      slliw x21, x8, 8
      slliw x21, x8, 16
      slliw x21, x8, 31

      # ---- register-amount corners: the 5-bit vs 6-bit read, pinned as a PAIR ----
      addi x10, x0, 96              # 96 = 64 + 32: low6 = 32, low5 = 0
      srl x12, x8, x10              # the 64-bit form reads rs2[5:0] = 32
      addi x11, x0, 1               # pre-write: the srlw identity must be a VISIBLE change
      srlw x11, x8, x10             # rs2[4:0] = 0: the identity, sign-extended — the pair's other half
      addi x13, x0, -1              # -1: every low-5 read sees 31
      sllw x14, x8, x13             # rs2[4:0] = 31: bit 0 reaches bit 31
      sraw x15, x8, x13             # rs2[4:0] = 31: all sign
