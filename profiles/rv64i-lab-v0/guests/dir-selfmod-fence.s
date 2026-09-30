# dir-selfmod-fence.s — the P2-SCALAR.5 strand-3 guest: a store over a LATER
# instruction's word, then FENCE, then the execution of the patched word (the census's
# gap 4: fault-selfmod pins the distance-2 no-fence shape; the fence between the patch
# and the fetch was unpinned).
#
# D-CODE-VISIBILITY is a laboratory policy, not an architectural guarantee — so the shape
# was MEASURED BY PROBE on all three models before authoring (run_probes_p25s3.py): the
# patch (addi x2, x0, 2 → addi x2, x0, 7) is visible through `fence rw, rw` on sail 0.14,
# spike 1.1.1-dev AND semulith (x2 <- 7 everywhere). fence without Zifencei orders
# nothing fetch-related; the profile makes no memory-ordering claim (D-FENCE) and
# re-reads memory per fetch (D-CODE-VISIBILITY).

      lui   x1, 0x00700        # x1 = 0x00700000
      addi  x1, x1, 0x113      # x1 = 0x00700113 == the encoding of `addi x2, x0, 7`
      auipc x3, 0              # x3 = this instruction's address (entry+8)
      sw    x1, 16, x3         # [entry+0x18] <- the patch: the word three steps down
      fence 0, 3, 3, x0, x0    # FENCE RW,RW between the store and the fetch — a nop here
      addi  x4, x0, 4          # an ordinary write between the fence and the target
      addi  x2, x0, 2          # entry+0x18: fetched AFTER the store and the fence — as 7
      addi  x5, x0, 5          # landing
