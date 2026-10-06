#|never: x28, x29
addi x6, x0, 1               #: a sentinel the first mip read must REPLACE. | RVI-RV32I §1.1.4
addi x8, x0, 1               #: another sentinel. | RVI-RV32I §1.1.4
addi x5, x0, -1              #: all ones … | RVI-RV32I §1.1.4
csrrw x0, stimecmp, x5       #: stimecmp <- the maximum: STIP, the hart's own comparison, reads 0 (time is far below). | RVP-SSTC 12.1
csrrs x6, mip, x0            #: mip before: no source has asserted anything — 0. | RVP-MACHINE §2.1.1.9
csrrs x0, mip, x5            #: software writes ONES to every mip bit, the M-level sources' MSIP (3), MTIP (7) and MEIP (11) among them. | RVP-MACHINE §2.1.1.9
csrrs x7, mip, x0            #: only the software-writable SSIP and SEIP took (0x202): MSIP, MTIP and MEIP stay 0 — this environment supplies no source, and a write cannot be one. | RVP-MACHINE §2.1.1.9; the contract v1's interrupt-source assumption
csrrc x0, mip, x5            #: software clears what it can. | RVP-MACHINE §2.1.1.9
csrrs x8, mip, x0            #: back to 0: nothing is pending that software did not set. | RVP-MACHINE §2.1.1.9
csrrw x0, stimecmp, x0       #: stimecmp <- 0: now time >= stimecmp … | RVP-SSTC 12.1
csrrs x9, mip, x0            #: … so STIP (bit 5) reads 1 — the hart's own comparison, the one timer source v1 has. | RVP-SSTC 12.1 #|end
