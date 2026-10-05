#|never: x28, x29
# fencei-selfmod.s — the acceptance pair's WITH-synchronization member (P4-SYSTEM.6
# slice b, decision 3): a store patches a later instruction's word, and fence.i — the
# architectural synchronization, legal now that the slot is bound — executes BETWEEN
# the store and the fetch. The patched instruction is observed through its effects
# (x2 <- 7). On this always-coherent engine the visibility was already guaranteed by
# construction (D-CODE-VISIBILITY); fence.i retires as the declared nop — the
# synchronization the architecture NAMES, executed and legal.

      lui   x1, 0x00700          #: x1 = 0x00700000. | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
      addi  x1, x1, 0x113        #: x1 = 0x00700113 — the encoding of `addi x2, x0, 7`, assembled from the encoding rule, never read back from any model. | RVI-RV32I §1.1.4; §1.1.2 (the I-format layout)
      auipc x3, 0                #: x3 = this instruction's own address (entry+0x08). | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
      sw    x1, 16, x3           #: [entry+0x18] <- the patch: the word three steps down. | RVI-RV32I §1.1.6
      fence.i                    #: THE ARCHITECTURAL SYNCHRONIZATION, executed and legal (the slot bound at slice b): it orders the store before every later fetch — and on this machine it retires as the declared nop, the coherent-latitude landing (nothing to flush). | RVI-ZIFENCEI §4.1; the .6 brief's decision 2
      addi  x4, x0, 4            #: an ordinary write between the fence.i and the target. | RVI-RV32I §1.1.4
      addi  x2, x0, 2            #: entry+0x18, fetched AFTER the store and the fence.i: executes as `addi x2, x0, 7` — the patched instruction observed through its effects (D-CODE-VISIBILITY — immediate visibility is the laboratory's declared choice, a legal subset of the chapter's may-or-may-not). | RVI-ZIFENCEI §4.1; D-CODE-VISIBILITY
      addi  x5, x0, 5            #: the landing: the patch, the synchronization and the patched fetch all retired. | RVI-RV32I §1.1.4 #|end
