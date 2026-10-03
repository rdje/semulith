# it-progress-loop.s — the P2-SCALAR.4 interaction guest (progress × progress, with the
# x0-link alias): an unbounded counting loop, observed under the budget contract.
#
# OB-ENV-PARTIAL-PROGRESS: every iteration is a visible step — the counter write commits on
# each pass, so "the model is making progress" is observable, never asserted. The jump's
# link register is x0: the transfer happens and the link write is architecturally discarded
# (x0 hardwired zero) — a control transfer whose link is aliased to the register that cannot
# hold it. The program never stops on its own; the run ends exactly when the step budget is
# spent (Stop::Budget), which is the laboratory's contract with a non-terminating guest.

      addi  x1, x0, 1        # the counter starts at 1 (0 -> 1 is the first visible write)
loop: addi  x1, x1, 1        # one visible count per iteration
      jal   x0, -4           # back to `loop`; the link targets x0 and is discarded
