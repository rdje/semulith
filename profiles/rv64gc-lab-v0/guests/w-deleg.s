#|never: x28, x29
# w-deleg.s — the locally-enabled-regardless-of-DELEGATION cell (P4-SYSTEM.5 slice c):
# "the hart must resume if a locally enabled interrupt becomes pending, even if it has
# been delegated to a less-privileged mode" (RVP-MACHINE §2.1.3.3 — measured verbatim
# before authoring). STI is delegated to S; the hart halts in M with MIE set; the
# timer's arrival wakes it ANYWAY; the taken-rule then masks the delegated cause at M,
# so NO trap fires and execution resumes at pc + 4. Un-delegating makes the SAME
# still-pending cause take the trap at the next boundary.

      auipc x1, 0                  #: x1 = this instruction's own address. | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
      addi x1, x1, 64              #: the handler rides 64 bytes in. | RVI-RV32I §1.1.4
      csrrw x0, mtvec, x1          #: mtvec programmed. | RVI-ZICSR §5.1.1
      addi x15, x0, 1              #: raw material for STI's bit. | RVI-RV32I §1.1.4
      slli x15, x15, 5             #: x15 = 1 << 5. | RVI-RV64I §3.1.2.1
      csrrs x0, mideleg, x15       #: mideleg[5] <- 1 FIRST: the cause is delegated before it can pend (the delegation is what the cell is ABOUT). | RVP-MACHINE §2.1.1.8
      csrrs x0, mie, x15           #: STIE <- 1 — the local enable the wake honors. | RVP-MACHINE §2.1.1.9
      addi x8, x0, 13              #: stimecmp's target: 13 — two ticks past the wfi's head (time 11 there). | RVI-RV32I §1.1.4
      csrrw x0, stimecmp, x8       #: stimecmp <- 13 (time 8 < 13: STIP computes 0, the wfi's head is quiet). | RVP-SSTC 12.1
      addi x6, x0, 8               #: the MIE bit. | RVI-RV32I §1.1.4
      csrrs x0, mstatus, x6        #: MIE <- 1 — and yet no trap will fire while the cause is delegated. | RVP-MACHINE §2.1.1.8
      wfi                          #: the halt: ONE halted step (time 12 < 13), then STIP arrives and the hart MUST resume — delegation notwithstanding. | RVP-MACHINE §2.1.3.3
      rdtime x7                    #: time is 13: the hart WOKE at the timer's arrival — and the delivery did NOT fire (the taken-rule masks a delegated cause at the delegator): the resume is the pc + 4 continuation. | RVP-MACHINE §2.1.3.3, §2.1.1.8
      csrrc x0, mideleg, x15       #: un-delegate: the SAME still-pending STI now follows M's rule. | RVP-MACHINE §2.1.1.8
      addi x7, x0, 0               #: — the delivery step: STI taken in M at this boundary (STIP & STIE & MIE, mideleg clear) — mepc is THIS instruction's address. | RVP-MACHINE §2.1.1.9
      addi x9, x0, 42              #: the landing marker: wake-regardless-of-delegation, then the trap once un-delegated. | RVI-RV32I §1.1.4 #|end

handler:
      csrrs x11, mcause, x0        #: the handler observes the Interrupt bit with cause 5. | RVP-MACHINE §2.1.1.9
      csrrs x12, mepc, x0          #: mepc is the un-fetched pc (0x80000038 — the delivery placeholder). | RVP-MACHINE §2.1.1.14
      addi x16, x0, 1              #: raw material for the high stimecmp. | RVI-RV32I §1.1.4
      slli x16, x16, 16            #: x16 = 0x10000. | RVI-RV64I §3.1.2.1
      csrrw x0, stimecmp, x16      #: disarm the timer for good. | RVP-SSTC 12.1
      csrrs x13, mepc, x0          #: step the resume address. | RVP-MACHINE §2.1.1.14
      addi x13, x13, 4             #: mepc + 4. | RVI-RV32I §1.1.4
      csrrw x0, mepc, x13          #: write it back. | RVI-ZICSR §5.1.1
      mret                         #: the stack pops per MPP and pc <- mepc — the landing marker. | RVP-MACHINE §2.1.3.2
