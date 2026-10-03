# dir-x0-writes.s — the P2-SCALAR.5 strand-3 guest: x0 as the destination from EVERY
# producer kind the corpus had not pinned (the census's gap 8: only lw pinned a load→x0
# success path; only addiw/addw/sllw pinned *W→x0). lb/lbu/lh/lhu/lwu/ld and
# subw/srlw/sraw/slliw/srliw/sraiw target x0 here.
#
# The architectural point (D-LOAD-X0): a load to x0 still PERFORMS the access — the
# crossing census pins the six load crossings, and the landing addi proves every form
# retired. The register-file observation is empty by construction (a write to x0 is
# architecturally discarded; the visible-change vocabulary records nothing).

      auipc x1, 0              # x1 = 0x80000000
      addi  x1, x1, 96         # x1 = &cell
      addi  x2, x0, -1         # x2 = 0xFFFFFFFFFFFFFFFF
      sd    x2, 0, x1          # cell <- all-ones
      lb    x0, x1, 0          # discarded — the access still happens (D-LOAD-X0)
      lbu   x0, x1, 0          # discarded
      lh    x0, x1, 0          # discarded
      lhu   x0, x1, 0          # discarded
      lwu   x0, x1, 0          # discarded
      ld    x0, x1, 0          # discarded
      addi  x3, x0, 5          # the *W forms' operand
      subw  x0, x3, x3         # 0 — discarded
      srlw  x0, x3, x3         # 5 >> 5 = 0 — discarded
      sraw  x0, x3, x3         # 0 — discarded
      slliw x0, x3, 1          # 10 — discarded
      srliw x0, x3, 1          # 2 — discarded
      sraiw x0, x3, 1          # 2 — discarded
      addi  x4, x0, 4          # landing: every producer retired, x0 stood at 0 throughout
