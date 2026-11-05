# scope-mem.s — the P2-SCALAR.1 scope-completion guest: the RV64I load/store forms no
# tracked guest exercised yet (LB, LBU, LH, LHU, LWU, SB, SH, SW), with LW/LD/SD as the
# already-covered support forms.
#
# The pattern P = 0x80FFF7F080FFF7F0 is chosen so every probe has its top bit set at the
# width being read: each sign-extending load must produce all-ones above the value and
# each zero-extending load must not (D-LOAD-EXT). P is built only from already-covered
# forms, because LUI alone cannot place a positive 0x80… word at both halves.
#
# Data lives at base+1024 and beyond, well clear of this code (D-CODE-VISIBILITY), and
# every access is naturally aligned, so no step raises the D-MISALIGN-DATA exception —
# the smoke-trap guest owns that case.

      addi  x10, x0, 1
      slli  x10, x10, 31         # the main-memory base 0x8000_0000, built arithmetically

      lui   x1, 0x80FFF          # build P's high half: 0xFFFFFFFF80FFF000 …
      addi  x2, x0, 0x7F0
      or    x1, x1, x2           # … 0xFFFFFFFF80FFF7F0 …
      slli  x1, x1, 32           # … 0x80FFF7F000000000
      lui   x3, 0x80FFF          # the same word for the low half …
      or    x3, x3, x2
      slli  x3, x3, 32           # … shifted out and back to zero the upper bits …
      srli  x3, x3, 32           # … 0x0000000080FFF7F0
      or    x7, x1, x3           # P = 0x80FFF7F080FFF7F0

      sd    x7, 1024, x10        # commit P to main memory (already-covered form)

      lb    x11, x10, 1024       # D-LOAD-EXT: byte 0xF0 SIGN-extends
      lbu   x12, x10, 1025       # byte 0xF7 ZERO-extends — the same kind of byte, extended
      lh    x13, x10, 1026       # halfword 0x80FF sign-extends
      lhu   x14, x10, 1026       # the SAME halfword zero-extends — the pair is the point
      lw    x15, x10, 1024       # word 0x80FFF7F0 sign-extends
      lwu   x16, x10, 1028       # the same word (upper half) ZERO-extends — RV64 only
      ld    x17, x10, 1024       # a full XLEN load needs no extension
      lw    x0, x10, 1024        # D-LOAD-X0: the load happens, the value is discarded

      addi  x4, x0, -1           # a store value whose truncation is visible at each width
      sb    x4, 1040, x10        # D-LOAD-EXT's store half: SB writes the low 8 bits
      ld    x18, x10, 1040       # observe: 0x00000000000000FF
      sh    x4, 1048, x10        # SH writes the low 16 bits
      ld    x19, x10, 1048       # observe: 0x000000000000FFFF
      sw    x4, 1056, x10        # SW writes the low 32 bits
      ld    x20, x10, 1056       # observe: 0x00000000FFFFFFFF
      sw    x7, 1064, x10        # SW of P keeps only its low half
      ld    x21, x10, 1064       # observe: 0x0000000080FFF7F0
