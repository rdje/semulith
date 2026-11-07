auipc x1, 0                    #: the base for the handler: {new}. | RVI-RV64I §3.1.2.1
addi x1, x1, 16                #: the handler, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1            #: mtvec = the handler; no GPR written. | RVP-MACHINE §2.1.1.7
jal x0, 20                     #: past the handler; x0 discards the link. | RVI-RV32I §1.1.5.1
csrrs x30, mcause, x0          #: the handler reads mcause: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.15
csrrs x29, mtval, x0           #: and mtval: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.16
csrrs x28, mepc, x0            #: and mepc, the instruction's own address: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.14
jalr x0, x27, 0                #: on, to where x27 says, still in M. | RVI-RV32I §1.1.5.1
lui x2, 6                      #: mstatus.FS's two bits: {new}. | RVI-RV64I §3.1.2.1
csrrs x0, mstatus, x2          #: FS = Dirty, so the floating-point forms may run; no GPR written. | RVP-MACHINE §2.1.1.6.5
addi x5, x0, 1023              #: double-precision 1.0: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 52                #: double-precision 1.0: {new}. | RVI-RV64I §3.1.2.1
fmv.d.x f1, x5                 #: into f1. | RVI-D §21.1
fcvt.s.d f2, f1, 0             #: D reaches F: the same value, narrowed. | RVI-D §21.1
fmv.x.w x6, f2                 #: its single-precision bits: {new}. | RVI-F §20.1 (boundary: D depends on F)
addi x7, x0, 127               #: single-precision 1.0: {new}. | RVI-RV32I §1.1.4
slli x7, x7, 23                #: single-precision 1.0: {new}. | RVI-RV64I §3.1.2.1
fmv.w.x f3, x7                 #: F writes f3, boxed in D's width. | RVI-F §20.1
fmv.x.d x8, f3                 #: the whole register: {new}. | RVI-D §21.1 (boundary: a single, boxed)
fmv.d.x f4, x7                 #: the same bits as a double, so not boxed as a single. | RVI-D §21.1
fadd.s f5, f4, f4, 0           #: F reads an unboxed value as the canonical NaN. | RVI-D §21.1
fmv.x.w x9, f5                 #: the result: {new}. | RVI-F §20.1
addi x10, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x10, fcsr, x0            #: fcsr, through Zicsr: nothing was signalled: {new}. | RVI-F §20.1; RVI-ZICSR §5.1.1 (boundary: F depends on Zicsr)
addi x11, x0, 127              #: 1.0 again: {new}. | RVI-RV32I §1.1.4
slli x11, x11, 23              #: 1.0 again: {new}. | RVI-RV64I §3.1.2.1
fmv.w.x f6, x11                #: into f6. | RVI-F §20.1
addi x12, x0, 1                #: a value too small to survive the sum: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 23              #: a value too small to survive the sum: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 1               #: a value too small to survive the sum: {new}. | RVI-RV32I §1.1.4
fmv.w.x f7, x12                #: into f7. | RVI-F §20.1
fadd.s f8, f6, f7, 0           #: an inexact sum, which sets NX. | RVI-F §20.1
addi x13, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x13, fflags, x0          #: fflags, through Zicsr: {new}. | RVI-F §20.1; RVI-ZICSR §5.1.1
addi x14, x0, 1                #: RTZ's code: {new}. | RVI-RV32I §1.1.4
csrrw x0, frm, x14             #: frm = RTZ, through Zicsr; no GPR written. | RVI-F §20.1; RVI-ZICSR §5.1.1
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x15, frm, x0             #: and it reads back: {new}. | RVI-F §20.1; RVI-ZICSR §5.1.1
addi x16, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x16, fcsr, x0            #: fcsr composes both: {new}. | RVI-F §20.1; RVI-ZICSR §5.1.1
addi x10, x0, 1                #: raw material for the region base. | RVI-RV32I §1.1.4
slli x10, x10, 31              #: 0x80000000: {new}. | RVI-RV64I §3.1.2.1
lui x1, 7                      #: 0x7000: {new}. | RVI-RV64I §3.1.2.1
add x1, x1, x10                #: the data cell, on a page of its own, past this program: {new}. | RVI-RV32I §1.1.4
c.mv x8, x1                    #: x8 = the data cell, a compact register: Zca is here. | RVI-ZC §28.1.2 (boundary: Zca, always)
addi x17, x0, 1097             #: a doubleword whose halves differ: {new}. | RVI-RV32I §1.1.4
slli x17, x17, 12              #: a doubleword whose halves differ: {new}. | RVI-RV64I §3.1.2.1
addi x17, x17, -1843           #: a doubleword whose halves differ: {new}. | RVI-RV32I §1.1.4
slli x17, x17, 14              #: a doubleword whose halves differ: {new}. | RVI-RV64I §3.1.2.1
addi x17, x17, 1109            #: a doubleword whose halves differ: {new}. | RVI-RV32I §1.1.4
slli x17, x17, 12              #: a doubleword whose halves differ: {new}. | RVI-RV64I §3.1.2.1
addi x17, x17, 1639            #: a doubleword whose halves differ: {new}. | RVI-RV32I §1.1.4
slli x17, x17, 12              #: a doubleword whose halves differ: {new}. | RVI-RV64I §3.1.2.1
addi x17, x17, 1928            #: a doubleword whose halves differ: {new}. | RVI-RV32I §1.1.4
sd x17, 8, x8                  #: at x8 + 8. | RVI-RV64I §3.1.3
addi x18, x0, 1                #: double-precision 2.0: {new}. | RVI-RV32I §1.1.4
slli x18, x18, 62              #: double-precision 2.0: {new}. | RVI-RV64I §3.1.2.1
fmv.d.x f9, x18                #: into f9. | RVI-D §21.1
c.fsd x8, f9, 0                #: Zcd is here: C.FSD stores f9 at x8. | RVI-ZC §28.1.2
ld x19, x8, 0                  #: what C.FSD stored: {new}. | RVI-RV64I §3.1.3 (boundary: Zcd, with D)
c.fld f10, x8, 0               #: and C.FLD reads them back. | RVI-ZC §28.1.2
fmv.x.d x20, f10               #: f10's bits: {new}. | RVI-D §21.1
addi x11, x0, 77               #: a sentinel C.LD must replace, were this C.FLW it would not: {new}. | RVI-RV32I §1.1.4
fmv.d.x f11, x0                #: f11 clear, so a load into it would show. | RVI-D §21.1
c.ld x11, x8, 8                #: this encoding is C.FLW only at RV32; at RV64 it is C.LD: {new}. | RVI-ZC §28.1.2; RVI-C §27.1.3.2 (boundary: Zcf exists only at RV32)
addi x21, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
fmv.x.d x21, f11               #: and f11 took nothing: {new}. | RVI-D §21.1
c.nop                          #: the end of the program. | RVI-C §27.1.8
