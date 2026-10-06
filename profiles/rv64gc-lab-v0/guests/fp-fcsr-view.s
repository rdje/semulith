addi x8, x0, 1               #: the FS=Initial pattern starts as a 1. | RVI-RV32I §1.1.4
slli x8, x8, 13              #: 1 << 13 is the FS field's low bit (mstatus[14:13]). | RVP-CSR (the mstatus field table)
csrrs x0, mstatus, x8        #: the corpus enables FP before any FP-CSR access (FS := Initial); rd=x0 discards the old mstatus. | RVP-MACHINE §2.1.1.6.7; the .7 brief's decision 5
addi x5, x0, 31              #: 0x1F — all five accrued flags. | RVI-RV32I §1.1.4
csrrw x0, fflags, x5         #: fflags <- 0x1F; an FP-CSR write also marks FS=Dirty (Sail 0.14's write_fcsr → dirty_fd_context). | RVI-F §20.1.2
addi x6, x0, 3               #: RDN is 3 in the rm/frm vocabulary. | RVI-F §20.1.2 (the rounding-mode table)
csrrw x0, frm, x6            #: frm <- 3 (the three low bits of rs1 — the FSRM sentence). | RVI-F §20.1.2
csrrs x7, fcsr, x0           #: x7 = 0x7F — the composed read: fflags[4:0] with frm[2:0] at bits 7:5. | RVI-F §20.1.2 (the fcsr figure)
addi x9, x0, 64              #: 0x40 — the split-write pattern (frm slice 2, flags slice 0). | RVI-RV32I §1.1.4
csrrw x0, fcsr, x9           #: the two-owner write splits: fflags <- 0, frm <- 2. | RVI-F §20.1.2
addi x10, x0, 5              #: preload x10 so the cleared flags read is an observable change. | RVI-RV32I §1.1.4
csrrs x10, fflags, x0        #: x10 = 0 — the fflags slice of the fcsr write landed (and cleared). | RVI-F §20.1.2
csrrs x11, frm, x0           #: x11 = 2 — the frm slice landed. | RVI-F §20.1.2
addi x9, x0, 0x1E5           #: 0x1E5: bit 8 (beyond fcsr's two fields), frm slice 7, flags slice 0x05. | RVI-RV32I §1.1.4
csrrw x0, fcsr, x9           #: both slices land: frm <- 7 (any 3-bit value — 111 in frm is a dynamic RESERVED rounding mode, reachable by construction), fflags <- 0x05; bit 8 is ignored ('implementations shall ignore writes to these bits'). | RVI-F §20.1.2
csrrs x12, fcsr, x0          #: x12 = 0xE5 — frm 7 composed above flags 0x05; bit 8 reads zero ('supply a zero value when read'). | RVI-F §20.1.2
addi x13, x0, 14             #: 0b1110: low three bits 6, bit 3 beyond frm's field. | RVI-RV32I §1.1.4
csrrw x0, frm, x13           #: frm <- 6 — 'the three least-significant bits of integer register rs1'; bit 3 drops. | RVI-F §20.1.2
csrrs x14, frm, x0           #: x14 = 6 (FRRM: frm in the low three bits, zero above). | RVI-F §20.1.2
csrrs x15, mstatus, x0       #: x15 observes FS=Dirty with SD=1 — the FP-CSR writes dirtied the context. | RVP-MACHINE §2.1.1.6.7
