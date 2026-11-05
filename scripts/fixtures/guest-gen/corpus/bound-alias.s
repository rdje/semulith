# bound-alias.s — the P2-SCALAR.2 boundary guest for alias, overlap and state
# interactions: the little-endian lane proof (one sd of 0x0807060504030201, then lbu
# at each byte lane — D-ENDIAN), overlapping stores composed and read back with one
# ld, register aliasing (rd = rs1 = rs2, a self-referential shift, a load that
# overwrites its own base register — the address is sampled before the write
# commits), and x0 hardwired in both directions (a discarded write; a zero store).
#
# Data lives at base+1024 and beyond, well clear of this code (D-CODE-VISIBILITY);
# every access is naturally aligned, so no step raises D-MISALIGN-DATA.

      addi x10, x0, 1               # the main-memory base 0x8000_0000
      slli x10, x10, 31
      lui x1, 0x4030                # build X = 0x0807060504030201: each byte lane holds its own index+1
      addi x1, x1, 0x201
      lui x2, 0x8070
      addi x2, x2, 0x605
      slli x2, x2, 32
      or x1, x2, x1

      # ---- the little-endian lane proof (D-ENDIAN): one sd, then lbu at every lane ----
      sd x1, 1024, x10
      lbu x11, x10, 1024
      lbu x12, x10, 1025
      lbu x13, x10, 1026
      lbu x14, x10, 1027
      lbu x15, x10, 1028
      lbu x16, x10, 1029
      lbu x17, x10, 1030
      lbu x18, x10, 1031

      # ---- overlap composition: sd, then sb over byte 3, sh over bytes 6-7, one ld ----
      sd x1, 1032, x10
      addi x3, x0, 0xAA
      sb x3, 1035, x10
      addi x4, x0, 0x4CD
      sh x4, 1038, x10
      ld x19, x10, 1032

      # ---- register aliasing: rd IS a source ----
      addi x20, x0, 5
      add x20, x20, x20
      addi x21, x0, 7
      sub x21, x21, x21
      addi x22, x0, 1
      slt x22, x22, x22
      addi x23, x0, 0x21
      sll x23, x23, x23

      # ---- a load that overwrites its own base register ----
      addi x24, x10, 1024
      lb x24, x24, 0

      # ---- x0: hardwired zero, both directions ----
      addi x0, x0, -1
      sd x1, 1040, x10
      sw x0, 1040, x10
      ld x25, x10, 1040
