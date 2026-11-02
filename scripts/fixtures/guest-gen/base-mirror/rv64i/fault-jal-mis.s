# fault-jal-mis.s — the P2-SCALAR.3 fault guest: a JAL to a misaligned target.
#
# D-IALIGN + D-MISALIGN-REPORT: a taken jump whose target is not 4-byte aligned raises
# instruction-address-misaligned ON THE JUMP, tval = the target value. ⭐ And the link
# write is SUPPRESSED: an instruction that raises a synchronous exception retires no
# architectural write — both references suppress it (measured), and this guest is the
# DEFECT-B pin (the model once wrote x5 before trapping; `never_written x5` is the
# negative observation that catches a regression).

      addi  x1, x0, 1          # an ordinary write first, so the trap is not the only step
      jal   x5, 2              # target = 0x80000006 — not 4-byte aligned: trap on the jump
