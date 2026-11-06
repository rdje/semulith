auipc x1, 0                    #: the base for the handler: {new}. | RVI-RV64I §3.1.2.1
addi x1, x1, 16                #: the handler, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1            #: mtvec = the handler; no GPR written. | RVP-MACHINE §2.1.1.7
jal x0, 20                     #: past the handler; x0 discards the link. | RVI-RV32I §1.1.5.1
csrrs x30, mcause, x0          #: the handler reads mcause: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.15
csrrs x29, mtval, x0           #: and mtval: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.16
csrrs x28, mepc, x0            #: and mepc, the instruction's own address: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.14
jalr x0, x27, 0                #: on, to where x27 says, still in M. | RVI-RV32I §1.1.5.1
addi x10, x0, 1                #: raw material for the region base. | RVI-RV32I §1.1.4
slli x10, x10, 31              #: 0x80000000: {new}. | RVI-RV64I §3.1.2.1
lui x1, 7                      #: 0x7000: {new}. | RVI-RV64I §3.1.2.1
add x1, x1, x10                #: the data cell, on a page of its own, past this program: {new}. | RVI-RV32I §1.1.4
addi x9, x0, 41                #: a sentinel a refused move must leave: {new}. | RVI-RV32I §1.1.4
addi x30, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
fmv.x.d x9, f1                 #: FS is Off: FMV.X.D is illegal-instruction, and writes nothing. | RVP-MACHINE §2.1.1.6.7
addi x26, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
addi x26, x9, 0                #: copied: {new}, nothing committed. | RVI-RV32I §1.1.4
addi x31, x0, 1                #: 1, for the FS field: {new}. | RVI-RV32I §1.1.4
slli x31, x31, 13              #: at bit 13: {new}. | RVI-RV64I §3.1.2.1
csrrs x0, mstatus, x31         #: FS = Initial: the floating-point state is enabled; no GPR written. | RVP-MACHINE §2.1.1.6.7
addi x5, x0, 1023              #: 1.0: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 52                #: 1.0: {new}. | RVI-RV64I §3.1.2.1
fmv.d.x f1, x5                 #: 1.0, into f1; no GPR written. | RVI-D §21.1.5
addi x5, x0, 1                 #: 3.0: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 12                #: 3.0: {new}. | RVI-RV64I §3.1.2.1
addi x5, x5, -2047             #: 3.0: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 51                #: 3.0: {new}. | RVI-RV64I §3.1.2.1
fmv.d.x f2, x5                 #: 3.0, into f2; no GPR written. | RVI-D §21.1.5
csrrs x19, mstatus, x0         #: mstatus: {new}. | RVP-MACHINE §2.1.1.6.7
srli x19, x19, 13              #: FS, at the bottom: {new}. | RVI-RV64I §3.1.2.1
andi x19, x19, 3               #: FS alone: {new}. | RVI-RV32I §1.1.4
addi x5, x0, 1                 #: 9.0: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 13                #: 9.0: {new}. | RVI-RV64I §3.1.2.1
addi x5, x5, 17                #: 9.0: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 49                #: 9.0: {new}. | RVI-RV64I §3.1.2.1
fmv.d.x f3, x5                 #: 9.0, into f3; no GPR written. | RVI-D §21.1.5
addi x5, x0, -1025             #: -1.0: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 52                #: -1.0: {new}. | RVI-RV64I §3.1.2.1
fmv.d.x f4, x5                 #: -1.0, into f4; no GPR written. | RVI-D §21.1.5
addi x5, x0, 2047              #: 1.5: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 51                #: 1.5: {new}. | RVI-RV64I §3.1.2.1
fmv.d.x f5, x5                 #: 1.5, into f5; no GPR written. | RVI-D §21.1.5
addi x7, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x7, f4                 #: FMV.X.D moves -1.0's bits, all 64: {new}. | RVI-D §21.1.5 (boundary: a sign bit reaches the GPR)
fsd f3, 0, x1                  #: FSD stores 9.0. | RVI-D §21.1.3
fld f6, x1, 0                  #: FLD loads what FSD stored; written to f6. | RVI-D §21.1.3
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f6                 #: read back through a GPR: {new}. | RVI-D §21.1.3
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
ld x6, x1, 0                   #: the store itself, as an integer: {new}. | RVI-RV64I §3.1.3
addi x5, x0, 2047              #: a signaling NaN with a payload: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 39                #: a signaling NaN with a payload: {new}. | RVI-RV64I §3.1.2.1
addi x5, x5, 9                 #: a signaling NaN with a payload: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 13                #: a signaling NaN with a payload: {new}. | RVI-RV64I §3.1.2.1
addi x5, x5, 837               #: a signaling NaN with a payload: {new}. | RVI-RV32I §1.1.4
fmv.d.x f10, x5                #: a signaling NaN with a payload, into f10; no GPR written. | RVI-D §21.1.5
fsd f10, 0, x1                 #: FSD stores the NaN. | RVI-D §21.1.3
fld f11, x1, 0                 #: FLD loads it back. | RVI-D §21.1.3
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f11                #: read back through a GPR: {new}. | RVI-D §21.1.3
fadd.d f8, f1, f2, 0           #: FADD: 1.0 + 3.0 is exact; written to f8. | RVI-D §21.1.4
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.4
fsub.d f8, f1, f2, 0           #: FSUB: 1.0 - 3.0 is exact; written to f8. | RVI-D §21.1.4
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.4
fmul.d f8, f2, f2, 0           #: FMUL: 3.0 * 3.0 is exact; written to f8. | RVI-D §21.1.4
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.4
addi x20, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
csrrs x20, fflags, x0          #: An exact result raises no flag: {new}. | RVI-F §20.1.2
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
fsqrt.d f8, f3, 0              #: FSQRT of 9.0 is exact; written to f8. | RVI-D §21.1.4
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.4
fmadd.d f8, f2, f2, f1, 0      #: FMADD: 3.0 * 3.0 + 1.0; written to f8. | RVI-D §21.1.4
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.4
fmsub.d f8, f2, f2, f1, 0      #: FMSUB: 3.0 * 3.0 - 1.0; written to f8. | RVI-D §21.1.4
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.4
fnmsub.d f8, f2, f2, f1, 0     #: FNMSUB: -(3.0 * 3.0) + 1.0; written to f8. | RVI-D §21.1.4
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.4
fnmadd.d f8, f2, f2, f1, 0     #: FNMADD: -(3.0 * 3.0) - 1.0; written to f8. | RVI-D §21.1.4
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.4
fsgnj.d f8, f1, f4             #: FSGNJ takes rs2's sign; written to f8. | RVI-D §21.1.5
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.5
fsgnjn.d f8, f4, f4            #: FSGNJN takes the opposite of rs2's sign; written to f8. | RVI-D §21.1.5
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.5
fsgnjx.d f8, f4, f4            #: FSGNJX takes the XOR of the signs; written to f8. | RVI-D §21.1.5
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.5
fsgnj.d f8, f10, f10           #: Sign injection does not canonicalize a NaN; written to f8. | RVI-D §21.1.5
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.5
addi x20, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
csrrs x20, fflags, x0          #: And a signaling NaN sets no flag there: {new}. | RVI-F §20.1.2
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
addi x5, x0, 0                 #: 0.0: {new}. | RVI-RV32I §1.1.4
fmv.d.x f9, x5                 #: 0.0, into f9; no GPR written. | RVI-D §21.1.5
addi x5, x0, -1                #: -0.0: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 63                #: -0.0: {new}. | RVI-RV64I §3.1.2.1
fmv.d.x f12, x5                #: -0.0, into f12; no GPR written. | RVI-D §21.1.5
fmin.d f8, f9, f12             #: FMIN of 0.0 and -0.0, -0.0 counting as the smaller; written to f8. | RVI-D §21.1.4
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.4
fmax.d f8, f1, f2              #: FMAX of 1.0 and 3.0; written to f8. | RVI-D §21.1.4
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.4
fdiv.d f8, f1, f2, 0           #: FDIV: 1.0 / 3.0, to nearest, ties to even; written to f8. | RVI-D §21.1.4
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.4 (boundary: FDIV rounds to nearest)
addi x20, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
csrrs x20, fflags, x0          #: NX: an inexact result sets it: {new}. | RVI-F §20.1.2
fdiv.d f8, f1, f9, 0           #: 1.0 / 0.0 is infinity; written to f8. | RVI-D §21.1.4
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.4
addi x20, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
csrrs x20, fflags, x0          #: DZ joins NX, which stays set: the flags are sticky: {new}. | RVI-F §20.1.2
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
fdiv.d f8, f1, f2, 3           #: The same quotient under a static RUP; written to f8. | RVI-D §21.1.4; RVI-F §20.1.2
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.4; RVI-F §20.1.2 (boundary: a static RUP)
csrrwi x0, frm, 3              #: frm <- RUP; no GPR written. | RVI-F §20.1.2
fdiv.d f8, f1, f2, 7           #: The same quotient under DYN, reading frm's RUP; written to f8. | RVI-D §21.1.4; RVI-F §20.1.2
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.4; RVI-F §20.1.2 (boundary: DYN reads frm)
csrrwi x0, frm, 0              #: frm <- RNE; no GPR written. | RVI-F §20.1.2
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
fsqrt.d f8, f4, 0              #: The square root of -1.0 is the canonical NaN; written to f8. | RVI-D §21.1.4; RVI-F §20.1.3
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.4; RVI-F §20.1.3 (boundary: the canonical NaN)
addi x20, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
csrrs x20, fflags, x0          #: NV: an invalid operation sets it: {new}. | RVI-F §20.1.2
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
fmin.d f8, f1, f8              #: With one NaN input FMIN returns the other, 1.0; written to f8. | RVI-D §21.1.4
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.4
addi x5, x0, 2047              #: the largest finite value: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 52                #: the largest finite value: {new}. | RVI-RV64I §3.1.2.1
addi x5, x5, -1                #: the largest finite value: {new}. | RVI-RV32I §1.1.4
fmv.d.x f13, x5                #: the largest finite value, into f13; no GPR written. | RVI-D §21.1.5
fmul.d f8, f13, f13, 0         #: that value squared overflows. | RVI-D §21.1.4
addi x20, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
csrrs x20, fflags, x0          #: OF and NX: an overflow sets both: {new}. | RVI-F §20.1.2
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
addi x5, x0, 1                 #: the least subnormal: {new}. | RVI-RV32I §1.1.4
fmv.d.x f14, x5                #: the least subnormal, into f14; no GPR written. | RVI-D §21.1.5
addi x5, x0, 511               #: 0.5: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 53                #: 0.5: {new}. | RVI-RV64I §3.1.2.1
fmv.d.x f15, x5                #: 0.5, into f15; no GPR written. | RVI-D §21.1.5
fmul.d f8, f14, f15, 0         #: half of it is tiny and inexact. | RVI-D §21.1.4; RVI-F §20.1.4
addi x20, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
csrrs x20, fflags, x0          #: UF and NX: a tiny, inexact result sets both: {new}. | RVI-F §20.1.2
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
addi x5, x0, 1023              #: 1.0 and one unit in the last place: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 52                #: 1.0 and one unit in the last place: {new}. | RVI-RV64I §3.1.2.1
addi x5, x5, 1                 #: 1.0 and one unit in the last place: {new}. | RVI-RV32I §1.1.4
fmv.d.x f16, x5                #: 1.0 and one unit in the last place, into f16; no GPR written. | RVI-D §21.1.5
addi x5, x0, 1                 #: the largest subnormal: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 52                #: the largest subnormal: {new}. | RVI-RV64I §3.1.2.1
addi x5, x5, -1                #: the largest subnormal: {new}. | RVI-RV32I §1.1.4
fmv.d.x f17, x5                #: the largest subnormal, into f17; no GPR written. | RVI-D §21.1.5
fmul.d f8, f16, f17, 0         #: Their product is below the least normal, and rounds up to it; written to f8. | RVI-D §21.1.4; RVI-F §20.1.4
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.4; RVI-F §20.1.4
addi x20, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
csrrs x20, fflags, x0          #: NX alone: tininess is detected after rounding, and this result is normal then: {new}. | RVI-F §20.1.2
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
addi x5, x0, 1                 #: the canonical NaN: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 12                #: the canonical NaN: {new}. | RVI-RV64I §3.1.2.1
addi x5, x5, -1                #: the canonical NaN: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 51                #: the canonical NaN: {new}. | RVI-RV64I §3.1.2.1
fmv.d.x f18, x5                #: the canonical NaN, into f18; no GPR written. | RVI-D §21.1.5
addi x5, x0, 2047              #: a signaling NaN: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 52                #: a signaling NaN: {new}. | RVI-RV64I §3.1.2.1
addi x5, x5, 1                 #: a signaling NaN: {new}. | RVI-RV32I §1.1.4
fmv.d.x f19, x5                #: a signaling NaN, into f19; no GPR written. | RVI-D §21.1.5
addi x11, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
feq.d x11, f1, f1              #: FEQ of equal values: {new}. | RVI-D §21.1.6
addi x12, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
flt.d x12, f1, f2              #: FLT of 1.0 and 3.0: {new}. | RVI-D §21.1.6
addi x13, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fle.d x13, f2, f1              #: FLE of 3.0 and 1.0: {new}. | RVI-D §21.1.6
addi x11, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
feq.d x11, f18, f1             #: FEQ is quiet on a quiet NaN: 0, and no flag: {new}. | RVI-D §21.1.6
addi x20, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
csrrs x20, fflags, x0          #: FEQ on a quiet NaN sets no flag: {new}. | RVI-F §20.1.2
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
addi x21, x0, 3                #: both FS bits: {new}. | RVI-RV32I §1.1.4
slli x21, x21, 13              #: at bit 13: {new}. | RVI-RV64I §3.1.2.1
csrrc x0, mstatus, x21         #: FS cleared; no GPR written. | RVI-ZICSR §5.1.1
addi x21, x0, 1                #: 1: {new}. | RVI-RV32I §1.1.4
slli x21, x21, 14              #: bit 14, FS = Clean: {new}. | RVI-RV64I §3.1.2.1
csrrs x0, mstatus, x21         #: FS = Clean; no GPR written. | RVI-ZICSR §5.1.1
fmv.x.d x7, f1                 #: a move out only reads the state. | RVI-D §21.1.5
csrrs x19, mstatus, x0         #: mstatus: {new}. | RVP-MACHINE §2.1.1.6.7
srli x19, x19, 13              #: FS, at the bottom: {new}. | RVI-RV64I §3.1.2.1
andi x19, x19, 3               #: FS alone: {new}. | RVI-RV32I §1.1.4
addi x12, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
flt.d x12, f18, f1             #: FLT signals on any NaN: 0: {new}. | RVI-D §21.1.6
csrrs x19, mstatus, x0         #: mstatus: {new}. | RVP-MACHINE §2.1.1.6.7
srli x19, x19, 13              #: FS, at the bottom: {new}. | RVI-RV64I §3.1.2.1
andi x19, x19, 3               #: FS alone: {new}. | RVI-RV32I §1.1.4
addi x20, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
csrrs x20, fflags, x0          #: FLT on a quiet NaN sets NV: {new}. | RVI-F §20.1.2
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
addi x14, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fclass.d x14, f1               #: FCLASS of 1.0 sets bit 6, a positive normal: {new}. | RVI-D §21.1.7
addi x14, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fclass.d x14, f19              #: FCLASS of a signaling NaN sets bit 8: {new}. | RVI-D §21.1.7
addi x14, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fclass.d x14, f18              #: FCLASS of a quiet NaN sets bit 9: {new}. | RVI-D §21.1.7
addi x15, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fcvt.w.d x15, f5, 0            #: FCVT.W of 1.5 rounds to nearest, ties to even: {new}. | RVI-D §21.1.5 (boundary: FCVT.W rounds)
addi x15, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fcvt.w.d x15, f5, 1            #: the same value under a static RTZ: {new}. | RVI-D §21.1.5
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
addi x16, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fcvt.wu.d x16, f4, 0           #: FCVT.WU of -1.0 cannot be represented, and clips to: {new}. | RVI-D §21.1.5 (boundary: FCVT.WU clips)
addi x20, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
csrrs x20, fflags, x0          #: NV: an unrepresentable conversion sets it: {new}. | RVI-F §20.1.2
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
addi x15, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fcvt.w.d x15, f18, 0           #: FCVT.W of a NaN is the largest word: {new}. | RVI-D §21.1.5
addi x16, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fcvt.wu.d x16, f18, 0          #: FCVT.WU of a NaN is the largest word, sign-extended: {new}. | RVI-D §21.1.5
addi x17, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fcvt.l.d x17, f4, 0            #: FCVT.L of -1.0: {new}. | RVI-D §21.1.5
addi x17, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fcvt.l.d x17, f18, 0           #: FCVT.L of a NaN is the largest doubleword: {new}. | RVI-D §21.1.5
addi x18, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fcvt.lu.d x18, f2, 0           #: FCVT.LU of 3.0: {new}. | RVI-D §21.1.5
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
addi x19, x0, -1               #: -1: a signed integer, or a huge unsigned one: {new}. | RVI-RV32I §1.1.4
fcvt.d.w f8, x19, 0            #: From the word -1; written to f8. | RVI-D §21.1.5
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.5
fcvt.d.wu f8, x19, 0           #: From the unsigned word 2^32 - 1; written to f8. | RVI-D §21.1.5
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.5
fcvt.d.l f8, x19, 0            #: From the doubleword -1; written to f8. | RVI-D §21.1.5
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.5
fcvt.d.lu f8, x19, 0           #: From the unsigned doubleword 2^64 - 1; written to f8. | RVI-D §21.1.5
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.5
addi x22, x0, -769             #: a single 1.5, NaN-boxed: {new}. | RVI-RV32I §1.1.4
slli x22, x22, 22              #: a single 1.5, NaN-boxed: {new}. | RVI-RV64I §3.1.2.1
fmv.d.x f11, x22               #: f11 holds it; no GPR written. | RVI-D §21.1.5
addi x14, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fclass.d x14, f11              #: seen as a double, the box is a quiet NaN: {new}. | RVI-D §21.1.7
fcvt.d.s f8, f11, 0            #: FCVT.D.S of a boxed single 1.5 widens exactly; written to f8. | RVI-D §21.1.5
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.5 (boundary: FCVT.D.S widens)
fcvt.d.s f8, f1, 0             #: FCVT.D.S reads 1.0, not boxed as a single, as the canonical NaN; written to f8. | RVI-D §21.1.5; RVI-D §21.1.2
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.5; RVI-D §21.1.2 (boundary: FCVT.D.S reads through the box)
addi x5, x0, 1                 #: a third: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 14                #: a third: {new}. | RVI-RV64I §3.1.2.1
addi x5, x5, -43               #: a third: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 12                #: a third: {new}. | RVI-RV64I §3.1.2.1
addi x5, x5, 1365              #: a third: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 12                #: a third: {new}. | RVI-RV64I §3.1.2.1
addi x5, x5, 1365              #: a third: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 12                #: a third: {new}. | RVI-RV64I §3.1.2.1
addi x5, x5, 1365              #: a third: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 12                #: a third: {new}. | RVI-RV64I §3.1.2.1
addi x5, x5, 1365              #: a third: {new}. | RVI-RV32I §1.1.4
fmv.d.x f20, x5                #: a third, into f20; no GPR written. | RVI-D §21.1.5
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
fcvt.s.d f8, f20, 3            #: FCVT.S.D of a third, under a static RUP, rounds and writes its single boxed; written to f8. | RVI-D §21.1.5; RVI-D §21.1.2
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.5; RVI-D §21.1.2 (boundary: FCVT.S.D rounds and boxes)
fcvt.s.d f8, f20, 2            #: The same value under a static RDN; written to f8. | RVI-D §21.1.5; RVI-F §20.1.2
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.5; RVI-F §20.1.2 (boundary: FCVT.S.D under RDN)
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
fcvt.s.d f8, f19, 0            #: a signaling NaN narrowed: an invalid operation. | RVI-D §21.1.5
addi x20, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
csrrs x20, fflags, x0          #: NV: a signaling input to a conversion sets it: {new}. | RVI-F §20.1.2
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: the last result, the single canonical NaN, boxed: {new}. | RVI-D §21.1.5
addi x30, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
fcvt.d.w f8, x19, 5            #: A reserved rounding mode is illegal even on FCVT.D.W, which cannot round | RVI-F §20.1.2
addi x30, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
fcvt.d.s f8, f11, 6            #: And on FCVT.D.S, which never rounds | RVI-F §20.1.2
csrrwi x0, frm, 5              #: frm <- 5, a reserved mode; no GPR written. | RVI-F §20.1.2
addi x30, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
fadd.d f8, f1, f2, 7           #: DYN with frm holding 5 is reserved, so illegal-instruction | RVI-F §20.1.2
addi x6, x0, 77                #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x6, f8                 #: f8 still holds the last result: {new}. | RVI-F §20.1.2
csrrwi x0, frm, 0              #: frm <- RNE; no GPR written. | RVI-F §20.1.2
