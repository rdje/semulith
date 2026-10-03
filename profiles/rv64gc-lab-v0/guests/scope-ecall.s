# scope-ecall.s — the P2-SCALAR.1 scope-completion guest: ECALL.
#
# ECALL causes a precise REQUESTED trap to the execution environment (D-ECALL-EBREAK):
# it is a target observation, not a model failure — which is why ModelError and
# TargetEvent are different types. With no privileged modes in this profile there is no
# guest handler, so the laboratory reports the trap to the harness and execution STOPS.
# The ecall is therefore the last instruction: the run ends on the trap, exactly as
# `smoke-trap` ends on its contained misaligned-load trap.

      addi  x1, x0, 7          # an ordinary write first, so the trap is not the only step
      ecall                    # the requested trap — the environment call itself
