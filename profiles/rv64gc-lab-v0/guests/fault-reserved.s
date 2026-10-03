# fault-reserved.s — the P2-SCALAR.3 reserved-encoding guest (SEM-07).
#
# 0xFFFFFFFF matches no row of the generated decode table: a RESERVED instruction.
# The architecture declares the behavior UNSPECIFIED; this laboratory's policy
# (D-RESERVED-DECODE) raises illegal-instruction — and the model reports the case AS
# the unspecified case it is (Stop::Undefined), the conversion to the trap observation
# being the harness policy's explicit act, never the interpreter's. Both references
# raise illegal-instruction with tval = the offending word (measured), so the
# policy-converted observation is three-way comparable.

      addi  x1, x0, 1          # an ordinary write first, so the reserved word is not the only step
      .word 0xFFFFFFFF         # no decode-table row matches: the reserved case itself
