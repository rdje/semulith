#|never: x28, x29
# a-lrsc-loop.s — a constrained LR/SC loop terminating on its FIRST SC
# (P4-SYSTEM.4 slice d): under the declared deterministic policy the eventuality
# guarantee's degenerate one-hart form holds — the retry branch is never taken,
# proven by the landing marker and by the step trace's fall-through.

      addi x10, x0, 1              #: raw material for the region base. | RVI-RV32I §1.1.4
      slli x10, x10, 31            #: x10 = 0x8000_0000. | RVI-RV64I §3.1.2.1
      addi x1, x10, 256            #: the counter's address. | RVI-RV32I §1.1.4
      addi x7, x0, 41              #: the initial count. | RVI-RV32I §1.1.4

      sw x7, 0, x1                 #: mem = 41. | RVI-RV64I §3.1.3
retry:
      lr.w x5, (x1)                #: the sequence begins: reserve and load 41. | RVI-A §12.1.3
      addi x5, x5, 1               #: the critical section: 42 — base-I only, same address and size, well under 16 instructions. | RVI-A §12.1.3
      sc.w x6, x5, (x1)            #: the FIRST SC succeeds under the declared never-spurious policy: rd <- 0, mem <- 42. | RVI-A §12.1.3; state.sexp's reservation candidate (decision 3)
      bne x6, x0, retry            #: code 0: the retry branch is NOT taken — the degenerate one-hart eventuality, recorded. | RVI-A §12.1.3
      sw x5, 8, x1                 #: the landing marker: 42 stored beside the counter — proof the flow arrived past the loop. | RVI-RV64I §3.1.3
      lw x8, x1, 0                 #: read-back of the counter: 42. | RVI-RV64I §3.1.3
