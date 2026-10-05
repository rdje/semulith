#|never: x28, x29
# i-timer.s — the STIP-at-reset quirk faced by name, then set/clear across the
# ticking domain (P4-SYSTEM.5 slice b): at reset STIP reads 1 (time >= stimecmp
# 0); writing stimecmp above the current time clears it; the domain's ticks reach
# it again; and an enabled STI is taken as cause 5 with the Interrupt bit
# (RVP-SSTC 12.1, RVP-SUPERVISOR §11.1.1.12).

      auipc x1, 0                  #: x1 = this instruction's own address. | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
      addi x1, x1, 68              #: the handler rides 68 bytes in. | RVI-RV32I §1.1.4
      csrrw x0, mtvec, x1          #: mtvec programmed. | RVI-ZICSR §5.1.1
      csrrs x7, mip, x0            #: THE RESET QUIRK, observed: STIP reads 1 — time 3 >= stimecmp 0 (the bit is computed, not stored; it has read 1 since reset). | RVP-SSTC 12.1; the .5 brief's pre-condition 1
      addi x8, x0, 8               #: stimecmp's target: 8 — three boundaries past this write. | RVI-RV32I §1.1.4
      csrrw x0, stimecmp, x8       #: stimecmp <- 8 (time is 5 at this step's own head). | RVP-SSTC 12.1
      csrrs x7, mip, x0            #: STIP <- 0 by computation (time 6 < 8): writing stimecmp ABOVE time disarms it. | RVP-SUPERVISOR §11.1.1.12
      addi x5, x0, 1               #: one more boundary ticks by (time 7 at the next head). | RVI-RV32I §1.1.4
      csrrs x7, mip, x0            #: STIP <- 1 again (time 8 >= 8): the timer's arrival is time's, no MMIO. | RVP-SSTC 12.1
      addi x15, x0, 1              #: raw material for STIE's bit. | RVI-RV32I §1.1.4
      slli x15, x15, 5             #: x15 = 1 << 5. | RVI-RV64I §3.1.2.1
      csrrs x0, mie, x15           #: STIE <- 1 (MIE still clear: the boundaries pass STI by). | RVP-MACHINE §2.1.1.9
      addi x6, x0, 8               #: the MIE bit. | RVI-RV32I §1.1.4
      csrrs x0, mstatus, x6        #: MIE <- 1: the next boundary takes STI. | RVP-MACHINE §2.1.1.9
      addi x7, x0, 0               #: — the delivery step: cause 5 with the Interrupt bit — mepc is THIS address. | RVP-MACHINE §2.1.1.9
      csrrs x7, mip, x0            #: resumed and disarmed (the handler wrote stimecmp high): STIP stays 0. | RVP-SUPERVISOR §11.1.1.12
      addi x9, x0, 42              #: the landing marker. | RVI-RV32I §1.1.4 #|end

handler:
      csrrs x11, mcause, x0        #: the handler observes the Interrupt bit with cause 5 (0x8000000000000005). | RVP-MACHINE §2.1.1.9
      csrrs x12, mepc, x0          #: mepc is the un-fetched pc. | RVP-MACHINE §2.1.1.14
      addi x13, x0, 1              #: raw material for the high stimecmp value. | RVI-RV32I §1.1.4
      slli x13, x13, 16            #: x13 = 0x10000, far above this guest's clock. | RVI-RV64I §3.1.2.1
      csrrw x0, stimecmp, x13      #: disarm the timer for good. | RVP-SSTC 12.1
      csrrs x14, mepc, x0          #: step the resume address. | RVP-MACHINE §2.1.1.14
      addi x14, x14, 4             #: mepc + 4. | RVI-RV32I §1.1.4
      csrrw x0, mepc, x14          #: write it back. | RVI-ZICSR §5.1.1
      mret                         #: the stack pops per MPP and pc <- mepc. | RVP-MACHINE §2.1.3.2
