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
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
fmv.x.w x9, f1                 #: FS is Off: FMV.X.W is illegal-instruction, and writes nothing. | RVP-MACHINE §2.1.1.6.7
addi x26, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x26, x9, 0                #: copied: {new}, nothing committed. | RVI-RV32I §1.1.4
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
flw f8, x1, 0                  #: FS is Off: FLW is illegal-instruction, before any memory access. | RVP-MACHINE §2.1.1.6.7
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
fadd.s f8, f1, f2, 0           #: FS is Off: FADD is illegal-instruction. | RVP-MACHINE §2.1.1.6.7
addi x31, x0, 1                #: 1, for the FS field: {new}. | RVI-RV32I §1.1.4
slli x31, x31, 13              #: at bit 13: {new}. | RVI-RV64I §3.1.2.1
csrrs x0, mstatus, x31         #: FS = Initial: the floating-point state is enabled; no GPR written. | RVP-MACHINE §2.1.1.6.7
addi x5, x0, 127               #: 1.0: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 23                #: 1.0: {new}. | RVI-RV64I §3.1.2.1
fmv.w.x f1, x5                 #: 1.0, into f1; no GPR written. | RVI-F §20.1.7
addi x5, x0, 257               #: 3.0: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 22                #: 3.0: {new}. | RVI-RV64I §3.1.2.1
fmv.w.x f2, x5                 #: 3.0, into f2; no GPR written. | RVI-F §20.1.7
csrrs x19, mstatus, x0         #: mstatus: {new}. | RVP-MACHINE §2.1.1.6.7
srli x19, x19, 13              #: FS, at the bottom: {new}. | RVI-RV64I §3.1.2.1
andi x19, x19, 3               #: FS alone: {new}. | RVI-RV32I §1.1.4
addi x5, x0, 1041              #: 9.0: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 20                #: 9.0: {new}. | RVI-RV64I §3.1.2.1
fmv.w.x f3, x5                 #: 9.0, into f3; no GPR written. | RVI-F §20.1.7
addi x5, x0, 383               #: -1.0: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 23                #: -1.0: {new}. | RVI-RV64I §3.1.2.1
fmv.w.x f4, x5                 #: -1.0, into f4; no GPR written. | RVI-F §20.1.7
addi x5, x0, 255               #: 1.5: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 22                #: 1.5: {new}. | RVI-RV64I §3.1.2.1
fmv.w.x f5, x5                 #: 1.5, into f5; no GPR written. | RVI-F §20.1.7
addi x7, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
fmv.x.w x7, f4                 #: FMV.X.W moves -1.0's bits, the sign filling the upper word: {new}. | RVI-F §20.1.7 (boundary: a sign bit reaches the GPR)
fsw f3, 0, x1                  #: FSW stores 9.0. | RVI-F §20.1.5
flw f6, x1, 0                  #: FLW loads what FSW stored; written to f6. | RVI-F §20.1.5
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
fmv.x.w x6, f6                 #: read back through a GPR: {new}. | RVI-F §20.1.5
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
lw x6, x1, 0                   #: the store itself, as an integer: {new}. | RVI-RV64I §3.1.3
addi x5, x0, 1                 #: a signaling NaN with a payload: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 18                #: a signaling NaN with a payload: {new}. | RVI-RV64I §3.1.2.1
addi x5, x5, -1015             #: a signaling NaN with a payload: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 13                #: a signaling NaN with a payload: {new}. | RVI-RV64I §3.1.2.1
addi x5, x5, 837               #: a signaling NaN with a payload: {new}. | RVI-RV32I §1.1.4
fmv.w.x f10, x5                #: a signaling NaN with a payload, into f10; no GPR written. | RVI-F §20.1.7
fsw f10, 0, x1                 #: FSW stores the NaN. | RVI-F §20.1.5
flw f11, x1, 0                 #: FLW loads it back. | RVI-F §20.1.5
fmv.x.w x6, f11                #: read back through a GPR: {new}. | RVI-F §20.1.5
fadd.s f8, f1, f2, 0           #: FADD: 1.0 + 3.0 is exact; written to f8. | RVI-F §20.1.6
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.6
fsub.s f8, f1, f2, 0           #: FSUB: 1.0 - 3.0 is exact; written to f8. | RVI-F §20.1.6
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.6
fmul.s f8, f2, f2, 0           #: FMUL: 3.0 * 3.0 is exact; written to f8. | RVI-F §20.1.6
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.6
addi x20, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x20, fflags, x0          #: An exact result raises no flag: {new}. | RVI-F §20.1.2
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
fsqrt.s f8, f3, 0              #: FSQRT of 9.0 is exact; written to f8. | RVI-F §20.1.6
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.6
fmadd.s f8, f2, f2, f1, 0      #: FMADD: 3.0 * 3.0 + 1.0; written to f8. | RVI-F §20.1.6
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.6
fmsub.s f8, f2, f2, f1, 0      #: FMSUB: 3.0 * 3.0 - 1.0; written to f8. | RVI-F §20.1.6
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.6
fnmsub.s f8, f2, f2, f1, 0     #: FNMSUB: -(3.0 * 3.0) + 1.0; written to f8. | RVI-F §20.1.6
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.6
fnmadd.s f8, f2, f2, f1, 0     #: FNMADD: -(3.0 * 3.0) - 1.0; written to f8. | RVI-F §20.1.6
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.6
fsgnj.s f8, f1, f4             #: FSGNJ takes rs2's sign; written to f8. | RVI-F §20.1.7
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.7
fsgnjn.s f8, f4, f4            #: FSGNJN takes the opposite of rs2's sign; written to f8. | RVI-F §20.1.7
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.7
fsgnjx.s f8, f4, f4            #: FSGNJX takes the XOR of the signs; written to f8. | RVI-F §20.1.7
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.7
fsgnj.s f8, f10, f10           #: Sign injection does not canonicalize a NaN; written to f8. | RVI-F §20.1.7
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.7
addi x20, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x20, fflags, x0          #: And a signaling NaN sets no flag there: {new}. | RVI-F §20.1.2
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
addi x5, x0, 0                 #: 0.0: {new}. | RVI-RV32I §1.1.4
fmv.w.x f9, x5                 #: 0.0, into f9; no GPR written. | RVI-F §20.1.7
addi x5, x0, 1                 #: -0.0: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 31                #: -0.0: {new}. | RVI-RV64I §3.1.2.1
fmv.w.x f12, x5                #: -0.0, into f12; no GPR written. | RVI-F §20.1.7
fmin.s f8, f9, f12             #: FMIN of 0.0 and -0.0, -0.0 counting as the smaller; written to f8. | RVI-F §20.1.6
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.6
fmax.s f8, f1, f2              #: FMAX of 1.0 and 3.0; written to f8. | RVI-F §20.1.6
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.6
fdiv.s f8, f1, f2, 0           #: FDIV: 1.0 / 3.0, to nearest, ties to even; written to f8. | RVI-F §20.1.6
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.6 (boundary: FDIV rounds to nearest)
csrrs x20, fflags, x0          #: NX: an inexact result sets it: {new}. | RVI-F §20.1.2
fdiv.s f8, f1, f9, 0           #: 1.0 / 0.0 is infinity; written to f8. | RVI-F §20.1.6
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.6
csrrs x20, fflags, x0          #: DZ joins NX, which stays set: the flags are sticky: {new}. | RVI-F §20.1.2
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
fdiv.s f8, f1, f2, 2           #: The same quotient under a static RDN; written to f8. | RVI-F §20.1.6; RVI-F §20.1.2
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.6; RVI-F §20.1.2 (boundary: a static RDN)
csrrwi x0, frm, 2              #: frm <- RDN; no GPR written. | RVI-F §20.1.2
fdiv.s f8, f1, f2, 7           #: The same quotient under DYN, reading frm's RDN; written to f8. | RVI-F §20.1.6; RVI-F §20.1.2
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.6; RVI-F §20.1.2 (boundary: DYN reads frm)
csrrwi x0, frm, 0              #: frm <- RNE; no GPR written. | RVI-F §20.1.2
fdiv.s f8, f4, f2, 1           #: -1.0 / 3.0 under a static RTZ, towards zero; written to f8. | RVI-F §20.1.6; RVI-F §20.1.2
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.6; RVI-F §20.1.2
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
fsqrt.s f8, f4, 0              #: The square root of -1.0 is the canonical NaN; written to f8. | RVI-F §20.1.6; RVI-F §20.1.3
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.6; RVI-F §20.1.3 (boundary: the canonical NaN)
csrrs x20, fflags, x0          #: NV: an invalid operation sets it: {new}. | RVI-F §20.1.2
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
fmin.s f8, f1, f8              #: With one NaN input FMIN returns the other, 1.0; written to f8. | RVI-F §20.1.6
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.6
addi x5, x0, 255               #: the largest finite value: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 23                #: the largest finite value: {new}. | RVI-RV64I §3.1.2.1
addi x5, x5, -1                #: the largest finite value: {new}. | RVI-RV32I §1.1.4
fmv.w.x f13, x5                #: the largest finite value, into f13; no GPR written. | RVI-F §20.1.7
fmul.s f8, f13, f13, 0         #: that value squared overflows. | RVI-F §20.1.6
csrrs x20, fflags, x0          #: OF and NX: an overflow sets both: {new}. | RVI-F §20.1.2
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
addi x5, x0, 1                 #: the least subnormal: {new}. | RVI-RV32I §1.1.4
fmv.w.x f14, x5                #: the least subnormal, into f14; no GPR written. | RVI-F §20.1.7
addi x5, x0, 63                #: 0.5: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 24                #: 0.5: {new}. | RVI-RV64I §3.1.2.1
fmv.w.x f15, x5                #: 0.5, into f15; no GPR written. | RVI-F §20.1.7
fmul.s f8, f14, f15, 0         #: half of it is tiny and inexact. | RVI-F §20.1.6; RVI-F §20.1.4
csrrs x20, fflags, x0          #: UF and NX: a tiny, inexact result sets both: {new}. | RVI-F §20.1.2
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
addi x5, x0, 127               #: 1.0 and one unit in the last place: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 23                #: 1.0 and one unit in the last place: {new}. | RVI-RV64I §3.1.2.1
addi x5, x5, 1                 #: 1.0 and one unit in the last place: {new}. | RVI-RV32I §1.1.4
fmv.w.x f16, x5                #: 1.0 and one unit in the last place, into f16; no GPR written. | RVI-F §20.1.7
addi x5, x0, 1                 #: the largest subnormal: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 23                #: the largest subnormal: {new}. | RVI-RV64I §3.1.2.1
addi x5, x5, -1                #: the largest subnormal: {new}. | RVI-RV32I §1.1.4
fmv.w.x f17, x5                #: the largest subnormal, into f17; no GPR written. | RVI-F §20.1.7
fmul.s f8, f16, f17, 0         #: Their product is below the least normal, and rounds up to it; written to f8. | RVI-F §20.1.6; RVI-F §20.1.4
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.6; RVI-F §20.1.4
csrrs x20, fflags, x0          #: NX alone: tininess is detected after rounding, and this result is normal then: {new}. | RVI-F §20.1.2
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
addi x5, x0, 511               #: the canonical NaN: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 22                #: the canonical NaN: {new}. | RVI-RV64I §3.1.2.1
fmv.w.x f18, x5                #: the canonical NaN, into f18; no GPR written. | RVI-F §20.1.7
addi x5, x0, 255               #: a signaling NaN: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 23                #: a signaling NaN: {new}. | RVI-RV64I §3.1.2.1
addi x5, x5, 1                 #: a signaling NaN: {new}. | RVI-RV32I §1.1.4
fmv.w.x f19, x5                #: a signaling NaN, into f19; no GPR written. | RVI-F §20.1.7
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
fmin.s f8, f18, f18            #: With both inputs NaN, FMIN returns the canonical NaN; written to f8. | RVI-F §20.1.6
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.6
fmin.s f8, f19, f1             #: With one input a signaling NaN, FMIN still returns the other, 1.0; written to f8. | RVI-F §20.1.6
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.6
csrrs x20, fflags, x0          #: NV: a signaling input sets it, even with a result that is not NaN: {new}. | RVI-F §20.1.2
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
addi x5, x0, 255               #: infinity: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 23                #: infinity: {new}. | RVI-RV64I §3.1.2.1
fmv.w.x f21, x5                #: infinity, into f21; no GPR written. | RVI-F §20.1.7
addi x5, x0, 511               #: negative infinity: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 23                #: negative infinity: {new}. | RVI-RV64I §3.1.2.1
fmv.w.x f22, x5                #: negative infinity, into f22; no GPR written. | RVI-F §20.1.7
addi x5, x0, 1                 #: a negative subnormal: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 31                #: a negative subnormal: {new}. | RVI-RV64I §3.1.2.1
addi x5, x5, 1                 #: a negative subnormal: {new}. | RVI-RV32I §1.1.4
fmv.w.x f23, x5                #: a negative subnormal, into f23; no GPR written. | RVI-F §20.1.7
addi x5, x0, 513               #: 2.5: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 21                #: 2.5: {new}. | RVI-RV64I §3.1.2.1
fmv.w.x f24, x5                #: 2.5, into f24; no GPR written. | RVI-F §20.1.7
fmadd.s f8, f21, f9, f18, 0    #: Infinity times zero, plus a quiet NaN, is the canonical NaN; written to f8. | RVI-F §20.1.6; RVI-F §20.1.3
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.6; RVI-F §20.1.3
addi x20, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x20, fflags, x0          #: NV: infinity times zero sets it, even when the addend is a quiet NaN: {new}. | RVI-F §20.1.2
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
addi x11, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
feq.s x11, f1, f1              #: FEQ of equal values: {new}. | RVI-F §20.1.8
addi x12, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
flt.s x12, f1, f2              #: FLT of 1.0 and 3.0: {new}. | RVI-F §20.1.8
addi x13, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
fle.s x13, f2, f1              #: FLE of 3.0 and 1.0: {new}. | RVI-F §20.1.8
feq.s x11, f18, f1             #: FEQ is quiet on a quiet NaN: 0, and no flag: {new}. | RVI-F §20.1.8
csrrs x20, fflags, x0          #: FEQ on a quiet NaN sets no flag: {new}. | RVI-F §20.1.2
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
addi x21, x0, 3                #: both FS bits: {new}. | RVI-RV32I §1.1.4
slli x21, x21, 13              #: at bit 13: {new}. | RVI-RV64I §3.1.2.1
csrrc x0, mstatus, x21         #: FS cleared; no GPR written. | RVI-ZICSR §5.1.1
addi x21, x0, 1                #: 1: {new}. | RVI-RV32I §1.1.4
slli x21, x21, 14              #: bit 14, FS = Clean: {new}. | RVI-RV64I §3.1.2.1
csrrs x0, mstatus, x21         #: FS = Clean; no GPR written. | RVI-ZICSR §5.1.1
fmv.x.w x7, f1                 #: a move out only reads the state. | RVI-F §20.1.7
csrrs x19, mstatus, x0         #: mstatus: {new}. | RVP-MACHINE §2.1.1.6.7
srli x19, x19, 13              #: FS, at the bottom: {new}. | RVI-RV64I §3.1.2.1
andi x19, x19, 3               #: FS alone: {new}. | RVI-RV32I §1.1.4
flt.s x12, f18, f1             #: FLT signals on any NaN: 0: {new}. | RVI-F §20.1.8
csrrs x19, mstatus, x0         #: mstatus: {new}. | RVP-MACHINE §2.1.1.6.7
srli x19, x19, 13              #: FS, at the bottom: {new}. | RVI-RV64I §3.1.2.1
andi x19, x19, 3               #: FS alone: {new}. | RVI-RV32I §1.1.4
csrrs x20, fflags, x0          #: FLT on a quiet NaN sets NV: {new}. | RVI-F §20.1.2
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
csrrs x19, mstatus, x0         #: mstatus: {new}. | RVP-MACHINE §2.1.1.6.7
srli x19, x19, 63              #: SD, at the bottom: {new}. | RVI-RV64I §3.1.2.1
addi x14, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
fclass.s x14, f1               #: FCLASS of 1.0 sets bit 6, a positive normal: {new}. | RVI-F §20.1.9
fclass.s x14, f22              #: FCLASS: negative infinity sets bit 0: {new}. | RVI-F §20.1.9
fclass.s x14, f4               #: FCLASS: a negative normal sets bit 1: {new}. | RVI-F §20.1.9
fclass.s x14, f23              #: FCLASS: a negative subnormal sets bit 2: {new}. | RVI-F §20.1.9
fclass.s x14, f12              #: FCLASS: -0.0 sets bit 3: {new}. | RVI-F §20.1.9
fclass.s x14, f9               #: FCLASS: 0.0 sets bit 4: {new}. | RVI-F §20.1.9
fclass.s x14, f14              #: FCLASS: a positive subnormal sets bit 5: {new}. | RVI-F §20.1.9
fclass.s x14, f21              #: FCLASS: infinity sets bit 7: {new}. | RVI-F §20.1.9
fclass.s x14, f19              #: FCLASS of a signaling NaN sets bit 8: {new}. | RVI-F §20.1.9
fclass.s x14, f18              #: FCLASS of a quiet NaN sets bit 9: {new}. | RVI-F §20.1.9
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
fcvt.w.s x15, f5, 0            #: FCVT.W of 1.5 rounds to nearest, ties to even: {new}. | RVI-F §20.1.7 (boundary: FCVT.W rounds)
fcvt.w.s x15, f5, 1            #: the same value under a static RTZ: {new}. | RVI-F §20.1.7 (boundary: a static RTZ)
fcvt.w.s x15, f24, 2           #: 2.5 under a static RDN: {new}. | RVI-F §20.1.7; RVI-F §20.1.2
fcvt.w.s x15, f24, 3           #: 2.5 under a static RUP: {new}. | RVI-F §20.1.7; RVI-F §20.1.2
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
fcvt.w.s x15, f24, 4           #: 2.5 under a static RMM, ties away from zero: {new}. | RVI-F §20.1.7; RVI-F §20.1.2
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
addi x16, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
fcvt.wu.s x16, f4, 0           #: FCVT.WU of -1.0 cannot be represented, and clips to: {new}. | RVI-F §20.1.7 (boundary: FCVT.WU clips)
addi x20, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x20, fflags, x0          #: NV: an unrepresentable conversion sets it: {new}. | RVI-F §20.1.2
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
fcvt.w.s x15, f18, 0           #: FCVT.W of a NaN is the largest word: {new}. | RVI-F §20.1.7
fcvt.wu.s x16, f18, 0          #: FCVT.WU of a NaN is the largest word, sign-extended: {new}. | RVI-F §20.1.7
addi x17, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
fcvt.l.s x17, f4, 0            #: FCVT.L of -1.0: {new}. | RVI-F §20.1.7
fcvt.l.s x17, f18, 0           #: FCVT.L of a NaN is the largest doubleword: {new}. | RVI-F §20.1.7
addi x18, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
fcvt.lu.s x18, f2, 0           #: FCVT.LU of 3.0: {new}. | RVI-F §20.1.7
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
fcvt.w.s x15, f13, 0           #: a value too large for a word clips to the largest: {new}. | RVI-F §20.1.7
fcvt.w.s x15, f22, 0           #: negative infinity clips to the smallest word: {new}. | RVI-F §20.1.7
addi x17, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
fcvt.l.s x17, f13, 0           #: a value too large for a doubleword clips to the largest: {new}. | RVI-F §20.1.7
fcvt.lu.s x18, f4, 0           #: -1.0 clips to zero as an unsigned doubleword: {new}. | RVI-F §20.1.7
csrrw x0, fflags, x0           #: flags cleared; no GPR written. | RVI-F §20.1.2
addi x19, x0, -1               #: -1: a signed integer, or a huge unsigned one: {new}. | RVI-RV32I §1.1.4
fcvt.s.w f8, x19, 0            #: From the word -1; written to f8. | RVI-F §20.1.7
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.7
fcvt.s.wu f8, x19, 0           #: From the unsigned word 2^32 - 1; written to f8. | RVI-F §20.1.7
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.7
fcvt.s.l f8, x19, 0            #: From the doubleword -1; written to f8. | RVI-F §20.1.7
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.7
fcvt.s.lu f8, x19, 0           #: From the unsigned doubleword 2^64 - 1; written to f8. | RVI-F §20.1.7
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-F §20.1.7
addi x22, x0, 1                #: 1, for a doubleword whose upper bits are not all ones: {new}. | RVI-RV32I §1.1.4
fmv.d.x f20, x22               #: f20 holds an improperly boxed value; no GPR written. | RVI-D §21.1.2
fadd.s f8, f20, f1, 0          #: An improperly boxed input reads as the canonical NaN, so the sum is; written to f8. | RVI-D §21.1.2
fmv.x.w x6, f8                 #: read back through a GPR: {new}. | RVI-D §21.1.2
fmv.w.x f21, x22               #: FMV.W.X moves the low word, and boxes it; no GPR written. | RVI-F §20.1.7
addi x21, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
fmv.x.d x21, f21               #: the upper 32 bits are all ones: {new}. | RVI-D §21.1.2 (boundary: a 32-bit value is NaN-boxed)
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
fadd.s f8, f1, f2, 5           #: A static rounding mode of 5 is reserved, so illegal-instruction | RVI-F §20.1.2
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
fadd.s f8, f1, f2, 6           #: A static rounding mode of 6 is reserved, so illegal-instruction | RVI-F §20.1.2
csrrwi x0, frm, 5              #: frm <- 5, a reserved mode; no GPR written. | RVI-F §20.1.2
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
fadd.s f8, f1, f2, 7           #: DYN with frm holding 5 is reserved, so illegal-instruction | RVI-F §20.1.2
csrrwi x0, frm, 6              #: frm <- 6, a reserved mode; no GPR written. | RVI-F §20.1.2
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
fadd.s f8, f1, f2, 7           #: DYN with frm holding 6 is reserved too | RVI-F §20.1.2
csrrwi x0, frm, 7              #: frm <- 7, a reserved mode; no GPR written. | RVI-F §20.1.2
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
fadd.s f8, f1, f2, 7           #: And with frm holding 7 | RVI-F §20.1.2
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
fmv.x.w x6, f8                 #: f8 still holds the last sum, the canonical NaN: {new}. | RVI-F §20.1.2
csrrwi x0, frm, 0              #: frm <- RNE; no GPR written. | RVI-F §20.1.2
