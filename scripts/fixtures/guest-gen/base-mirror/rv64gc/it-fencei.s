# it-fencei.s — the P2-SCALAR.4 expected-divergence guest (fault × event): the guest that
# pins DIFF-FENCEI-EXECUTED.
#
# Measured by probe BEFORE this guest was authored (P2-SCALAR.3): the word 0x0000100F
# (fence.i) EXECUTES as a no-op on both references — sail-riscv 0.14 and spike 1.1.1-dev —
# although the matched configurations exclude Zifencei, and execution CONTINUES past it.
# This profile declares Zifencei absent, so semulith reports the word as a reserved
# encoding and the laboratory's declared D-RESERVED-DECODE policy converts that to the
# illegal-instruction observation (cause 0x02, tval = the word), stopping the run
# (Stop::Undefined keeps the source classification, SEM-07). A legitimate UNSPECIFIED
# divergence: the reserved-instruction note leaves the behavior to the platform.
#
# The expectations below describe SEMULITH's run — two steps, the policy trap last. The
# references run three (the marker addi commits). The comparison is not disabled: it is
# declared to diverge at exactly step 1 (expect_divergence in the expectation document),
# and the references stay each other's control — sail vs spike agree over their full length.

      addi  x1, x0, 1        # the agreeing prefix
      .word 0x0000100F       # fence.i — reserved here; executed as a nop by both references
      addi  x2, x0, 7        # the continuation marker — semulith must NEVER write x2
