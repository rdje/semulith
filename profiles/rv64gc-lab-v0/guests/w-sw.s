#|never: x28, x29
# w-sw.s — the software-posted sources with the globals off (P4-SYSTEM.5 slice c):
# SSIP and SEIP's software-writable B parts wake the hart with MIE CLEAR — "WFI is
# required to resume execution for locally enabled interrupts pending at any privilege
# level, regardless of the global interrupt enable at each privilege level"
# (RVP-MACHINE §2.1.3.3). The wake is IMMEDIATE here (the source is already pending
# when the wfi retires, so the very next head resumes — zero halted steps, by
# declaration); the cell's falsification power is against the WRONG wake rule — a
# wake that required the global enable would stall this guest forever, and its
# expectations (which continue past each wfi) could never derive.

      addi x13, x0, 1              #: raw material for the high stimecmp. | RVI-RV32I §1.1.4
      slli x13, x13, 16            #: x13 = 0x10000. | RVI-RV64I §3.1.2.1
      csrrw x0, stimecmp, x13      #: disarm the reset-quirk STIP first (STIE is never set, but the mip reads below want single-bit values). | RVP-SSTC 12.1
      addi x2, x0, 2               #: the SSIP bit. | RVI-RV32I §1.1.4
      csrrs x0, mip, x2            #: SSIP <- 1 (MIE is clear: the taken-rule passes it by, so the wfi's own head is quiet). | RVP-MACHINE §2.1.1.9
      csrrs x0, mie, x2            #: SSIE <- 1 — the local enable is all the wake needs. | RVP-MACHINE §2.1.1.9
      wfi                          #: the first halt: the wake fires at the VERY NEXT head (a software-posted source is already pending) — M with MIE clear takes nothing, so execution resumes at pc + 4. | RVP-MACHINE §2.1.3.3
      csrrs x7, mip, x0            #: x7 = SSIP alone (0x2 — the timer disarmed): the pending that woke it, interrogated per the spec's own guidance ('the mip or sip registers can be interrogated'). | RVP-MACHINE §2.1.3.3, §2.1.1.9
      csrrc x0, mip, x2            #: clear SSIP. | RVP-MACHINE §2.1.1.9
      addi x8, x0, 1               #: raw material for SEIP's bit. | RVI-RV32I §1.1.4
      slli x8, x8, 9               #: x8 = 1 << 9. | RVI-RV64I §3.1.2.1
      csrrs x0, mip, x8            #: SEIP <- 1 (the software-writable B part). | RVP-MACHINE §2.1.1.9
      csrrs x0, mie, x8            #: SEIE <- 1. | RVP-MACHINE §2.1.1.9
      wfi                          #: the second halt: SEI wakes it the same way — globals still clear. | RVP-MACHINE §2.1.3.3
      csrrs x7, mip, x0            #: x7 = SEIP alone (0x200). | RVP-MACHINE §2.1.1.9
      csrrc x0, mip, x8            #: clear SEIP. | RVP-MACHINE §2.1.1.9
      addi x9, x0, 42              #: the landing marker: both software sources woke the hart with the globals off. | RVI-RV32I §1.1.4 #|end
