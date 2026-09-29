# fault-fence.s — the P2-SCALAR.3 guest: the corrected D-FENCE.
#
# RVI-RV32I §1.1.7 mandates, verbatim: "Base implementations shall treat all such
# reserved configurations as FENCE instructions (with fm = 0000)" — a reserved FENCE
# *configuration* is architecture-SPECIFIED behavior, not the UNSPECIFIED
# reserved-instruction case, so none of the fences below traps and none falls under
# D-RESERVED-DECODE. With one hart, no devices and an in-order model each is a nop.
# Every form below was measured to execute exactly so on both references.

      addi  x1, x0, 1          # an ordinary write, so the nops sit inside a live run
      fence 1, 15, 15, x0, x0  # fm = 1 (reserved): executes as FENCE fm=0000 — a nop
      fence 8, 3, 3, x0, x0    # FENCE.TSO rw,rw: accepted as FENCE RW,RW (D-FENCE) — a nop
      fence 0, 15, 15, x0, x1  # rd != x0: ignored for forward compatibility — a nop
      fence 0, 15, 15, x1, x0  # rs1 != x0: ignored for forward compatibility — a nop
      fence 0, 0, 15, x0, x0   # pred = 0 (a HINT code point): executes as a nop
      fence 0, 15, 0, x0, x0   # succ = 0 (a HINT code point): executes as a nop
      addi  x2, x0, 2          # landing: the run retired every fence
