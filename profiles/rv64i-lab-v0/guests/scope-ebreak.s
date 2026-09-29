# scope-ebreak.s — the P2-SCALAR.1 scope-completion guest: EBREAK.
#
# EBREAK is ECALL's sibling: a precise REQUESTED trap to the execution environment
# (D-ECALL-EBREAK), used by debuggers as a breakpoint. It is reported to the harness and
# execution STOPS, so it is the last instruction — one guest per requested trap, because
# a run can end only once.

      addi  x1, x0, 9          # an ordinary write first, so the trap is not the only step
      ebreak                   # the requested trap — the breakpoint itself
