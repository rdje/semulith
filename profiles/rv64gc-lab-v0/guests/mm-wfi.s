#|never: x28, x29
# mm-wfi.s — WFI's legality matrix over the REAL halt (P4-SYSTEM.5 slice c re-derivation,
# decision 10's named consequence): the legal-WFI cells (M, and S with TW=0) no longer
# nop — they ENTER the wait, so each arranges a timer wake and observes the halt span
# (rdtime after the wake; the S cell's source is DELEGATED to S, which must still wake
# it, RVP-MACHINE §2.1.3.3). The trap cells stand measured-unchanged: S with TW=1 is
# illegal, U with S present is illegal (the .2 TW resolutions, corpus-proven).

      auipc x1, 0                  #: x1 = this instruction's own address. | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
      addi x1, x1, 96              #: the handler rides 96 bytes in. | RVI-RV32I §1.1.4
      csrrw x0, mtvec, x1          #: mtvec programmed. | RVI-ZICSR §5.1.1
      addi x15, x0, 1              #: raw material for STI's bit. | RVI-RV32I §1.1.4
      slli x15, x15, 5             #: x15 = 1 << 5. | RVI-RV64I §3.1.2.1
      csrrs x0, mie, x15           #: STIE <- 1 (MIE stays clear: the legal cells wake WITHOUT a trap). | RVP-MACHINE §2.1.1.9
      addi x8, x0, 11              #: the M cell's stimecmp: 11 — three ticks past the wfi's head (time 8 there). | RVI-RV32I §1.1.4
      csrrw x0, stimecmp, x8       #: stimecmp <- 11 (time 7 < 11: STIP computes 0, the wfi's head is quiet). | RVP-SSTC 12.1
      wfi                          #: the M cell: legal — the hart ENTERS the wait (the nop latitude recorded-not-taken); TWO halted steps follow (time 9, 10 < 11). | RVP-MACHINE §2.1.3.3; the .5 brief's decision 4
      rdtime x7                    #: time is 11: the M cell's span, observed — the arrival woke the hart, M with MIE clear took nothing, execution resumed at pc + 4. | RVP-MACHINE §2.1.3.3; RVP-SSTC 12.1
      csrrs x0, mideleg, x15       #: mideleg[5] <- 1: the S cell's source is DELEGATED — and must still wake the hart ('even if it has been delegated to a less-privileged mode'). | RVP-MACHINE §2.1.3.3, §2.1.1.8
      addi x8, x0, 25              #: the S cell's stimecmp: 25 — three ticks past its wfi's head (time 22 there). | RVI-RV32I §1.1.4
      csrrw x0, stimecmp, x8       #: stimecmp <- 25: STIP <- 0 by computation (time 15 at the next head < 25). | RVP-SSTC 12.1
      addi x3, x0, 1               #: the MPP=S pattern starts as a 1. | RVI-RV32I §1.1.4
      slli x3, x3, 11              #: 1 << 11 is the MPP field's S encoding. | RVI-RV64I §3.1.2.1
      csrrw x0, mstatus, x3        #: mstatus <- 0x800: MPP=S. | RVI-ZICSR §5.1.1
      auipc x4, 0                  #: x4 = this address. | RVI-RV32I §1.1.4
      addi x4, x4, 16              #: the S cell rides 16 bytes past this auipc (entry+0x50). | RVI-RV32I §1.1.4
      csrrw x0, mepc, x4           #: mepc = the S cell. | RVI-ZICSR §5.1.1
      mret                         #: drop to S at the WFI cell (SIE lands clear from SPIE). | RVP-MACHINE §2.1.3.2
      wfi                          #: the S cell: TW=0, legal — the hart ENTERS the wait; TWO halted steps follow (time 23, 24 < 25). | RVP-MACHINE §2.1.3.3
      ecall                        #: the wake resumed at pc + 4 (the delegated arrival woke it, SIE clear took nothing): ecall from S, cause 9, entering the handler at stage 0. | RVP-MACHINE §2.1.3.1
      wfi                          #: the TW=1 cell: WFI in S with TW=1 traps illegal-instruction (the .2 resolution, standing). | RVP-MACHINE §2.1.3.3, §2.1.1.6.6
      wfi                          #: the U cell: WFI in U-mode traps illegal-instruction on this composition (the laboratory's WFI-in-U policy, standing). | RVP-MACHINE §2.1.3.3

handler:
      csrrs x12, mscratch, x0      #: the stage counter (0, then 1, then 2 — the latter two visits read back their own value, no change observed). | RVI-ZICSR §5.1.1
      beq x12, x0, stage1          #: stage 0: branch to the TW-enable stage. | RVI-RV32I §1.1.5
      addi x13, x0, 1              #: the comparison constant 1 (the third visit rewrites its own value, no change observed). | RVI-RV32I §1.1.4
      beq x12, x13, stage2         #: stage 1: branch to the drop-to-U stage. | RVI-RV32I §1.1.5
      csrrs x15, mcause, x0        #: the handler's third visit observes cause 2 (the U-mode WFI). | RVP-MACHINE §2.1.3.1
      csrrs x8, mepc, x0           #: mepc is the trapped U-mode wfi's own address (entry+0x5C). | RVP-MACHINE §2.1.3.1 #|end
      addi x8, x8, 4               #: (never executed within the declared steps — the count-driven termination's own convention)
      csrrw x0, mepc, x8           #: (never executed within the declared steps)
      mret                         #: (never executed within the declared steps)

stage1:
      addi x12, x0, 1              #: the stage counter becomes 1. | RVI-RV32I §1.1.4
      csrrw x0, mscratch, x12      #: mscratch <- 1. | RVI-ZICSR §5.1.1
      csrrs x7, mcause, x0         #: the handler observes cause 9 (the ecall). | RVP-MACHINE §2.1.3.1
      addi x2, x0, 1               #: the TW pattern starts as a 1. | RVI-RV32I §1.1.4
      slli x2, x2, 21              #: 1 << 21 is TW. | RVI-RV64I §3.1.2.1
      csrrs x0, mstatus, x2        #: set mstatus.TW. | RVI-ZICSR §5.1.1
      csrrs x10, mepc, x0          #: mepc is the ecall's address (entry+0x54). | RVP-MACHINE §2.1.3.1
      addi x10, x10, 4             #: step mepc past it. | RVI-RV32I §1.1.4
      csrrw x0, mepc, x10          #: mepc <- entry+0x58 — the TW=1 cell. | RVI-ZICSR §5.1.1
      mret                         #: back to S at the TW=1 WFI cell. | RVP-MACHINE §2.1.3.2

stage2:
      addi x12, x0, 2              #: the stage counter becomes 2. | RVI-RV32I §1.1.4
      csrrw x0, mscratch, x12      #: mscratch <- 2. | RVI-ZICSR §5.1.1
      csrrs x7, mcause, x0         #: the handler's second visit observes cause 2 (the TW=1 WFI). | RVP-MACHINE §2.1.3.1
      addi x13, x0, 1              #: raw material for the high stimecmp. | RVI-RV32I §1.1.4
      slli x13, x13, 16            #: x13 = 0x10000. | RVI-RV64I §3.1.2.1
      csrrw x0, stimecmp, x13      #: disarm the timer FIRST: the delegated STI is still pending, and in U it would be taken in S — the drop must find nothing pending. | RVP-SSTC 12.1; RVP-MACHINE §2.1.1.8
      csrrw x0, mstatus, x0        #: mstatus <- 0 clears MPP to U (and TW back to 0). | RVI-ZICSR §5.1.1
      auipc x4, 0                  #: x4 = this address. | RVI-RV32I §1.1.4
      addi x4, x4, -108            #: the U-mode WFI cell rides 108 bytes back (entry+0x5C). | RVI-RV32I §1.1.4
      csrrw x0, mepc, x4           #: mepc = the U cell. | RVI-ZICSR §5.1.1
      mret                         #: drop to U at the WFI cell. | RVP-MACHINE §2.1.3.2
