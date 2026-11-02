# min-fencei.s — the P2-SCALAR.6 retained MINIMIZED case for DIFF-FENCEI-EXECUTED.
#
# The discrepancy census (this leaf's design) found exactly one model-vs-references
# behavioral divergence: the references execute fence.i although their matched
# configurations exclude Zifencei; this profile declares the extension absent, so the
# laboratory's D-RESERVED-DECODE policy reports the word as illegal-instruction. One word
# reproduces the whole divergence — semulith's policy trap lands at step 0, and both
# references nop the fence.i and run off the end into the zero word (illegal-instruction
# on each, measured at P2-SCALAR.4 and by the strand-3 probe), staying each other's
# control. it-fencei keeps its prefix/marker shape in the corpus; THIS is the retained
# minimal case the leaf's acceptance asks for.

      .word 0x0000100F       # fence.i — reserved here; executed as a nop by both references
