# fault-selfmod.s — the P2-SCALAR.3 guest: D-CODE-VISIBILITY, pinned three-way.
#
# This laboratory re-reads memory on every instruction fetch, so a store that modifies
# a later-fetched instruction is visible IMMEDIATELY (a legal implementation choice,
# not an architectural guarantee — without Zifencei a caching hart is equally legal).
# Measured before authoring: sail-riscv 0.14 AND spike 1.1.1-dev both re-read too
# (spike's commit log even shows the store landing: mem 0x80000014 <- 0x00700113), so
# the profile's choice is pinned by the three-way comparison rather than asserted.
# The sw below patches step 5's word from `addi x2, x0, 2` into `addi x2, x0, 7`.

      lui   x1, 0x00700        # x1 = 0x00700000
      addi  x1, x1, 0x113      # x1 = 0x00700113 == the encoding of `addi x2, x0, 7`
      auipc x3, 0              # x3 = this instruction's address (0x80000008)
      sw    x1, 12, x3         # [0x80000014] <- 0x00700113: patches the word two steps down
      addi  x4, x0, 4          # an ordinary write between the patch and its target
      addi  x2, x0, 2          # fetched AFTER the store: executes as addi x2, x0, 7
      addi  x5, x0, 5          # landing
