# dir-runoff.s — the P2-SCALAR.5 strand-3 guest: execution runs OFF THE END of the
# program (the census's gap 1: no guest had ever made semulith fetch past its last word —
# every straight-line guest's budget equals its expectation count, so the fall-through
# fetch never happened).
#
# Measured by probe BEFORE authoring (run_probes_p25s3.py): the zero word at entry+8 —
# never-written in-region memory — raises illegal-instruction (cause 0x02, tval 0) on ALL
# THREE models: sail 0.14 spells the step `c.illegal`, spike `c.unimp`, and semulith
# decodes 0x00000000 against no row of the generated table (a RESERVED encoding), the
# laboratory's declared D-RESERVED-DECODE policy converting it to the same observation.

      addi  x1, x0, 1          # the ordinary prefix
      addi  x2, x0, 2
      # …and no third word: the next fetch reads zeros and the run ends on the trap.
