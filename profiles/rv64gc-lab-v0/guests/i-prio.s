#|never: x28, x29
# i-prio.s — the fixed priorities among simultaneous pending (P4-SYSTEM.5 slice b):
# MEI MSI MTI SEI SSI STI (RVP-MACHINE §2.1.1.9) — with all three software-reachable
# causes pending at once, SEI fires first, then SSI, then STI, each handler clearing
# its own bit before the next boundary re-evaluates.

      auipc x1, 0                  #: x1 = this instruction's own address. | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
      addi x1, x1, 76             #: the handler rides 76 bytes in. | RVI-RV32I §1.1.4
      csrrw x0, mtvec, x1          #: mtvec programmed. | RVI-ZICSR §5.1.1
      addi x2, x0, 2               #: the SSIP bit. | RVI-RV32I §1.1.4
      csrrs x0, mip, x2            #: SSIP <- 1. | RVP-MACHINE §2.1.1.9
      addi x8, x0, 1               #: raw material for SEIP's bit. | RVI-RV32I §1.1.4
      slli x8, x8, 9               #: x8 = 1 << 9 (the SEIP position). | RVI-RV64I §3.1.2.1
      csrrs x0, mip, x8            #: SEIP <- 1 — and STIP is ALREADY 1 (the reset quirk: time 0 >= stimecmp 0). | RVP-MACHINE §2.1.1.9; RVP-SSTC 12.1
      csrrs x0, mie, x2            #: SSIE <- 1. | RVP-MACHINE §2.1.1.9
      csrrs x0, mie, x8            #: SEIE <- 1. | RVP-MACHINE §2.1.1.9
      addi x15, x0, 1              #: raw material for STIE's bit. | RVI-RV32I §1.1.4
      slli x15, x15, 5             #: x15 = 1 << 5. | RVI-RV64I §3.1.2.1
      csrrs x0, mie, x15           #: STIE <- 1: all three causes enabled. | RVP-MACHINE §2.1.1.9
      addi x6, x0, 8               #: the MIE bit. | RVI-RV32I §1.1.4
      csrrs x0, mstatus, x6        #: MIE <- 1: the priority walk starts at the next boundary. | RVP-MACHINE §2.1.1.9
      addi x7, x0, 0               #: — delivery 1: SEI first (cause 9 outranks SSI and STI). | RVP-MACHINE §2.1.1.9
      addi x7, x0, 0               #: — delivery 2: SSI next (SEIP cleared in the handler). | RVP-MACHINE §2.1.1.9
      addi x7, x0, 0               #: — delivery 3: STI last (the timer cause waits its turn). | RVP-MACHINE §2.1.1.9
      addi x9, x0, 42              #: the landing marker: all three drained, in the spec's order. | RVI-RV32I §1.1.4 #|end

handler:
      csrrs x11, mcause, x0        #: the handler reads the cause it was entered for — the Interrupt bit with 9, then 1, then 5 (each visit sees its own). | RVP-MACHINE §2.1.1.9
      csrrs x12, mepc, x0          #: mepc is the un-fetched pc each time. | RVP-MACHINE §2.1.1.14
      addi x10, x0, 15             #: the cause-number mask (mcause carries the Interrupt bit). | RVI-RV32I §1.1.4
      and x10, x11, x10            #: the visit key: 9, then 1, then 5. | RVI-RV32I §1.1.4
      addi x13, x0, 9              #: the SEI cause for the visit key. | RVI-RV32I §1.1.4
      beq x10, x13, clear_sei      #: visit 1 disarms SEI only. | RVI-RV32I §1.1.5
      addi x13, x0, 1              #: the SSI cause — and, on the STI fall-through, raw material for the high stimecmp. | RVI-RV32I §1.1.4
      beq x10, x13, clear_ssi      #: visit 2 disarms SSI only. | RVI-RV32I §1.1.5
      slli x13, x13, 12            #: fall through to the STI visit: x13 = 0x1000, above any time this guest reaches. | RVI-RV64I §3.1.2.1
      csrrw x0, stimecmp, x13      #: STIP <- 0 by computation — the timer cause is disarmed for good. | RVP-SSTC 12.1
      beq x0, x0, resume           #: (the unconditional hop to the shared resume). | RVI-RV32I §1.1.5
clear_sei:
      csrrc x0, mip, x8            #: clear SEIP (x8 still 1 << 9 from the main flow). | RVP-MACHINE §2.1.1.9
      beq x0, x0, resume           #: to the shared resume. | RVI-RV32I §1.1.5
clear_ssi:
      addi x8, x0, 2               #: SSIP's bit. | RVI-RV32I §1.1.4
      csrrc x0, mip, x8            #: clear SSIP. | RVP-MACHINE §2.1.1.9
resume:
      csrrs x13, mip, x0           #: the remaining pending set is visible (SEIP|SSIP|STIP, then SSIP|STIP, then STIP, then 0). | RVP-MACHINE §2.1.1.9
      csrrs x14, mepc, x0          #: step the resume address. | RVP-MACHINE §2.1.1.14
      addi x14, x14, 4             #: mepc + 4. | RVI-RV32I §1.1.4
      csrrw x0, mepc, x14          #: write it back. | RVI-ZICSR §5.1.1
      mret                         #: the stack pops per MPP and pc <- mepc. | RVP-MACHINE §2.1.3.2
