addi x31, x0, 1              #: the FS=Initial pattern starts as a 1. | RVI-RV32I §1.1.4
slli x31, x31, 13            #: 1 << 13 — mstatus.FS's low bit. | RVP-CSR (the mstatus field table)
csrrs x0, mstatus, x31       #: FS := Initial: the floating-point state is enabled before any F instruction. | RVP-MACHINE §2.1.1.6.7
lui x5, 0x40200              #: build the pattern 0x40200000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f1, x5
fcvt.w.s x6, f1, 0           #: 2.5 in RNE: 2 (ties to even), NX. | RVI-F §20.1.7
fcvt.w.s x7, f1, 4           #: 2.5 in RMM: 3. | RVI-F §20.1.7
fcvt.l.s x8, f1, 3
csrrs x9, fflags, x0         #: x9 = the accrued flags so far. | RVI-F §20.1.2
csrrw x0, fflags, x0         #: clear the accrued flags (an explicit software write — the only way they clear). | RVI-F §20.1.2
lui x10, 0x4f400             #: build the pattern 0x4f400000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f2, x10
fcvt.wu.s x11, f2, 1         #: 3·2^30 fits a u32 — and FCVT.WU sign-extends its 32-bit result: 0xFFFFFFFFC0000000. | RVI-F §20.1.7
fcvt.w.s x12, f2, 1          #: beyond 2^31-1: clipped to 0x7FFFFFFF, NV alone. | RVI-F §20.1.7 (Table 5)
csrrs x13, fflags, x0        #: x13 = the accrued flags so far. | RVI-F §20.1.2
csrrw x0, fflags, x0         #: clear the accrued flags (an explicit software write — the only way they clear). | RVI-F §20.1.2
lui x14, 0x7fc00             #: build the pattern 0x7fc00000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f3, x14
fcvt.lu.s x15, f3, 0         #: NaN → the maximum (2^64-1), NV. | RVI-F §20.1.7 (Table 5)
lui x16, 0xff800             #: build the pattern 0xff800000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f4, x16
fcvt.l.s x17, f4, 0          #: −∞ → the minimum (−2^63), NV. | RVI-F §20.1.7 (Table 5)
lui x18, 0xbf800             #: build the pattern 0xbf800000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f5, x18
fcvt.wu.s x19, f5, 1         #: −1.0 to unsigned: out of range — clipped to 0, NV. | RVI-F §20.1.7 (Table 5)
csrrs x20, fflags, x0        #: x20 = the accrued flags so far. | RVI-F §20.1.2
csrrw x0, fflags, x0         #: clear the accrued flags (an explicit software write — the only way they clear). | RVI-F §20.1.2
addi x21, x0, -7             #: x21 = −7. | RVI-RV32I §1.1.4
fcvt.s.w f6, x21, 0
fmv.x.w x22, f6
fcvt.s.wu f7, x21, 0         #: x21's low 32 bits as UNSIGNED: 4294967289 → rounds to 2^32 in RNE, NX. | RVI-F §20.1.7
fmv.x.w x23, f7
lui x24, 0x1000              #: x24 = 2^24. | RVI-RV32I §1.1.4
addi x24, x24, 1             #: 2^24 + 1 — not a single. | RVI-RV32I §1.1.4
fcvt.s.l f8, x24, 3          #: RUP: 2^24 + 2, NX. | RVI-F §20.1.7
fmv.x.w x25, f8
fcvt.s.lu f9, x21, 1         #: x21 as a u64 (2^64 − 7) in RTZ. | RVI-F §20.1.7
fmv.x.w x26, f9
csrrs x27, fflags, x0        #: x27 = the accrued flags so far. | RVI-F §20.1.2 #|end
