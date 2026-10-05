#|never: x28, x29
# w-notrap.s — wake-WITHOUT-trap and the idle-loop idiom (P4-SYSTEM.5 slice c): with
# the global enable clear the timer's arrival still wakes the hart (§2.1.3.3's must),
# no trap is taken (the taken-rule fails in M with MIE=0), and execution resumes at
# pc + 4 — "software must determine what action to take, including looping back to
# repeat the WFI" (the section's own sentence): this guest halts TWICE.

      addi x8, x0, 8               #: the first stimecmp: 8 — three ticks past the first wfi's head (time 5 there). | RVI-RV32I §1.1.4
      csrrw x0, stimecmp, x8       #: stimecmp <- 8 (time 1 < 8: STIP computes 0, the wfi's head is quiet). | RVP-SSTC 12.1
      addi x15, x0, 1              #: raw material for STIE's bit. | RVI-RV32I §1.1.4
      slli x15, x15, 5             #: x15 = 1 << 5. | RVI-RV64I §3.1.2.1
      csrrs x0, mie, x15           #: STIE <- 1 (MIE stays CLEAR the whole guest — no trap can be taken). | RVP-MACHINE §2.1.1.9
      wfi                          #: the first halt: TWO halted steps (time 6, 7 < 8), then STIP's arrival wakes the hart — M with MIE clear takes nothing, so execution resumes at pc + 4. | RVP-MACHINE §2.1.3.3
      rdtime x7                    #: time is 8 — the wake's own tick, observed: the hart WOKE though nothing traps. | RVP-SSTC 12.1; RVP-MACHINE §2.1.3.3
      csrrs x11, mip, x0           #: STIP reads 1 (time 9 >= 8): the locally-enabled pending that woke it. | RVP-MACHINE §2.1.1.9
      addi x8, x0, 14              #: the second stimecmp: 14 — two ticks past the second wfi's head (time 12 there). | RVI-RV32I §1.1.4
      csrrw x0, stimecmp, x8       #: stimecmp <- 14: STIP <- 0 by computation (time 11 < 14) — the loop's re-arm. | RVP-SSTC 12.1
      wfi                          #: the loop-back: the second halt — ONE halted step (time 13 < 14), then the arrival wakes it again. | RVP-MACHINE §2.1.3.3
      csrrs x7, mip, x0            #: STIP reads 1 again (time 14 >= 14) — the second wake's cause. | RVP-MACHINE §2.1.1.9
      addi x13, x0, 1              #: raw material for the high stimecmp. | RVI-RV32I §1.1.4
      slli x13, x13, 16            #: x13 = 0x10000. | RVI-RV64I §3.1.2.1
      csrrw x0, stimecmp, x13      #: disarm the timer for good. | RVP-SSTC 12.1
      addi x9, x0, 42              #: the landing marker: both halts woke, no trap ever fired. | RVI-RV32I §1.1.4 #|end
