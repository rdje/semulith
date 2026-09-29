# bound-ext.s — the P2-SCALAR.2 boundary guest for load/store extension: the sign edge
# at each width (0x7F/0x80, 0x7FFF/0x8000, 0x7FFFFFFF/0x80000000) read through the
# sign/zero PAIR at one address — the pair is the observation (D-LOAD-EXT) — plus the
# all-ones value at each width, the 0x00 byte, and store truncation at values whose
# truncated form differs from both clamping outcomes.
#
# Data lives at base+1024 and beyond, well clear of this code (D-CODE-VISIBILITY);
# every access is naturally aligned, so no step raises D-MISALIGN-DATA. The 0x00
# byte's load is observed through a pre-write of -1, because a 0 written into an
# already-zero register is not a visible change.

      addi x10, x0, 1               # the main-memory base 0x8000_0000, built arithmetically
      slli x10, x10, 31
      addi x1, x0, 0x7F             # ---- the edge values: sign-bit boundaries at each width ----
      addi x2, x0, 0x80
      addi x3, x0, -1
      lui x4, 0x8
      addi x4, x4, -1
      lui x5, 0x8
      addi x6, x0, -1
      srli x6, x6, 33
      addi x7, x0, 1
      slli x7, x7, 31
      addi x8, x0, 0x180
      lui x9, 0xFFFF8

      # ---- commit the edge table: one store per value, all aligned, all in-region ----
      sb x1, 1024, x10
      sb x2, 1025, x10
      sb x3, 1026, x10
      sh x4, 1032, x10
      sh x5, 1034, x10
      sh x3, 1036, x10
      sw x6, 1040, x10
      sw x7, 1044, x10
      sw x3, 1048, x10

      # ---- the sign-edge probes: sign/zero PAIRS at one address — the pair is
      #      the observation (D-LOAD-EXT) ----
      lb x11, x10, 1024
      lb x12, x10, 1025
      lbu x13, x10, 1025
      lb x14, x10, 1026
      lbu x15, x10, 1026
      lh x16, x10, 1032
      lh x17, x10, 1034
      lhu x18, x10, 1034
      lh x19, x10, 1036
      lhu x20, x10, 1036
      lw x21, x10, 1040
      lw x22, x10, 1044
      lwu x23, x10, 1044
      lw x24, x10, 1048
      lwu x25, x10, 1048

      # ---- the 0x00 byte: a zero load observed through a pre-write ----
      sb x0, 1027, x10
      addi x26, x0, -1
      lb x26, x10, 1027

      # ---- store truncation at non-clamping values (D-LOAD-EXT's store half) ----
      sb x8, 1056, x10
      lbu x27, x10, 1056
      sh x9, 1064, x10
      lhu x28, x10, 1064
      sw x9, 1072, x10
      lwu x29, x10, 1072
