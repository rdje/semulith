#|never: x28, x29
# w-timer.s — THE acceptance cell (P4-SYSTEM.5 slice c): a TIMER wake occurs without
# CPU retirement. A legal WFI halts the hart; the declared domain ticks through the
# halt (slice a's rule); STIP arrives when time reaches stimecmp (no MMIO, Sstc); the
# wake fires and the taken-rule delivers the trap with mepc = the WFI's pc + 4
# (RVP-MACHINE §2.1.3.3's own rule). The handler's rdtime counts the ticks the halt
# spanned; its rdinstret proves NOTHING retired across it.

      auipc x1, 0                  #: x1 = this instruction's own address. | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
      addi x1, x1, 48              #: the handler rides 48 bytes in. | RVI-RV32I §1.1.4
      csrrw x0, mtvec, x1          #: mtvec programmed. | RVI-ZICSR §5.1.1
      addi x8, x0, 13              #: stimecmp's target: 13 — three ticks past the wfi's head (time 10 there, by the declared domain). | RVI-RV32I §1.1.4
      csrrw x0, stimecmp, x8       #: stimecmp <- 13: STIP computes 0 for now (time 4 < 13), so the wfi's own head is quiet. | RVP-SSTC 12.1
      addi x15, x0, 1              #: raw material for STIE's bit. | RVI-RV32I §1.1.4
      slli x15, x15, 5             #: x15 = 1 << 5. | RVI-RV64I §3.1.2.1
      csrrs x0, mie, x15           #: STIE <- 1. | RVP-MACHINE §2.1.1.9
      addi x6, x0, 8               #: the MIE bit. | RVI-RV32I §1.1.4
      csrrs x0, mstatus, x6        #: MIE <- 1: when the timer arrives, the taken-rule will hold. | RVP-MACHINE §2.1.1.9
      wfi                          #: the M cell: legal, so the hart ENTERS the wait (the nop latitude recorded-not-taken) — TWO halted steps follow (time 11, 12 < 13), then the arrival wakes it and the trap is taken — mepc is the NEXT instruction. | RVP-MACHINE §2.1.3.3; the .5 brief's decision 4
      addi x9, x0, 42              #: the landing marker: the handler's mret returns here (mepc was already the continuation — no +4 step). | RVI-RV32I §1.1.4 #|end

handler:
      rdinstret x14                #: instret is 11 at the handler's FIRST step — the ten setup instructions and the wfi, and NOTHING across the halt or the delivery: the timer wake occurred WITHOUT CPU RETIREMENT (the leaf's acceptance, observed). | RVP-MACHINE §2.1.1.9; the .5 brief's decision 1
      rdtime x13                   #: time is 15: the wfi retired at 10 and five boundaries passed (two halted steps, the delivery, the handler's own) — the halt spanned REAL ticks. | RVP-SSTC 12.1; the .5 brief's decision 1
      csrrs x11, mcause, x0        #: the handler observes the Interrupt bit with cause 5 — the timer, delivered. | RVP-MACHINE §2.1.1.9
      csrrs x12, mepc, x0          #: mepc is the wfi's pc + 4 (0x80000044) — §2.1.3.3's WFI-specific rule, which the generic between-instructions delivery computes for free. | RVP-MACHINE §2.1.3.3
      addi x16, x0, 1              #: raw material for the high stimecmp. | RVI-RV32I §1.1.4
      slli x16, x16, 16            #: x16 = 0x10000, far above this guest's clock. | RVI-RV64I §3.1.2.1
      csrrw x0, stimecmp, x16      #: disarm the timer for good (STIP <- 0 by computation). | RVP-SSTC 12.1
      mret                         #: the stack pops per MPP and pc <- mepc — the landing marker. | RVP-MACHINE §2.1.3.2
