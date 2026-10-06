addi x8, x0, 1               #: the FS=Initial pattern starts as a 1. | RVI-RV32I §1.1.4
slli x8, x8, 13              #: 1 << 13 is the FS field's low bit (mstatus[14:13]). | RVP-CSR (the mstatus field table)
csrrs x0, mstatus, x8        #: the corpus enables FP before any FP-CSR access (FS := Initial); rd=x0 discards the old mstatus. | RVP-MACHINE §2.1.1.6.7; the .7 brief's decision 5
addi x5, x0, 31              #: 0x1F — all five accrued flags. | RVI-RV32I §1.1.4
csrrw x0, fflags, x5         #: fflags <- 0x1F; an FP-CSR write also marks FS=Dirty (Sail 0.14's write_fcsr → dirty_fd_context). | RVI-F §20.1.1
addi x6, x0, 3               #: RDN is 3 in the rm/frm vocabulary. | RVI-F §20.1.1 (the rounding-mode table)
csrrw x0, frm, x6            #: frm <- 3 (legal: one-of 0..4). | RVI-F §20.1.1
csrrs x7, fcsr, x0           #: x7 = 0x7F — the composed read: fflags[4:0] with frm[2:0] at bits 7:5. | RVI-F §20.1.1 (the fcsr figure)
addi x9, x0, 64              #: 0x40 — the split-write pattern (frm slice 2, flags slice 0). | RVI-RV32I §1.1.4
csrrw x0, fcsr, x9           #: the two-owner write splits: fflags <- 0, frm <- 2. | RVI-F §20.1.1
addi x10, x0, 5              #: preload x10 so the cleared flags read is an observable change. | RVI-RV32I §1.1.4
csrrs x10, fflags, x0        #: x10 = 0 — the fflags slice of the fcsr write landed (and cleared). | RVI-F §20.1.1
csrrs x11, frm, x0           #: x11 = 2 — the frm slice landed. | RVI-F §20.1.1
addi x9, x0, 0xE5            #: 0xE5: frm slice 7 (illegal), flags slice 0x05. | RVI-RV32I §1.1.4
csrrw x0, fcsr, x9           #: the frm slice 7 is outside one-of 0..4 — frm RETAINS 2; the flags slice lands. | RVI-F §20.1.1; RVP-CSR §1.1.3.1 (the WARL retain rule)
csrrs x12, fcsr, x0          #: x12 = 0x45 — the retention observed through the composed view. | RVI-F §20.1.1
addi x13, x0, 6              #: 6 is illegal for frm. | RVI-RV32I §1.1.4
csrrw x0, frm, x13           #: frm retains 2 at its own address too. | RVI-F §20.1.1
csrrs x14, frm, x0           #: x14 = 2. | RVI-F §20.1.1
csrrs x15, mstatus, x0       #: x15 observes FS=Dirty with SD=1 — the FP-CSR writes dirtied the context. | RVP-MACHINE §2.1.1.6.7
