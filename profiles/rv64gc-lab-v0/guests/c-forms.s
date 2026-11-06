auipc x1, 0                    #: the base for the handler: {new}. | RVI-RV64I §3.1.2.1
addi x1, x1, 16                #: the handler, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1            #: mtvec = the handler; no GPR written. | RVP-MACHINE §2.1.1.7
jal x0, 20                     #: past the handler; x0 discards the link. | RVI-RV32I §1.1.5.1
csrrs x30, mcause, x0          #: the handler reads mcause: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.15
csrrs x29, mtval, x0           #: and mtval: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.16
csrrs x28, mepc, x0            #: and mepc, the instruction's own address: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.14
jalr x0, x27, 0                #: on, to where x27 says, still in M. | RVI-RV32I §1.1.5.1
addi x30, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 10              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
c.fld f8, x8, 0                #: FS is Off: C.FLD obeys the D extension's gate, and is illegal. | RVI-C §27.1.3.2; RVP-MACHINE §2.1.1.6.7
addi x30, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 10              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
c.fsdsp f9, 8                  #: and C.FSDSP likewise. | RVI-C §27.1.3.1; RVP-MACHINE §2.1.1.6.7
addi x31, x0, 1                #: 1, for the FS field: {new}. | RVI-RV32I §1.1.4
slli x31, x31, 13              #: at bit 13: {new}. | RVI-RV64I §3.1.2.1
csrrs x0, mstatus, x31         #: FS = Initial: the floating-point state is enabled; no GPR written. | RVP-MACHINE §2.1.1.6.7
addi x22, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
fmv.x.d x22, f8                #: f8 is untouched by the refused C.FLD: {new}. | RVI-D §21.1.5
c.li x8, -1                    #: C.LI sign-extends its immediate: {new}. | RVI-C §27.1.5.1
c.addi x8, 2                   #: C.ADDI adds its immediate: {new}. | RVI-C §27.1.5.2
c.mv x9, x8                    #: C.MV copies rs2: {new}. | RVI-C §27.1.5.3
c.add x9, x8                   #: C.ADD adds rs2: {new}. | RVI-C §27.1.5.3
c.lui x4, -32                  #: C.LUI sign-extends bit 17 up: {new}. | RVI-C §27.1.5.1
c.slli x9, 3                   #: C.SLLI shifts left: {new}. | RVI-C §27.1.5.2
c.srli x9, 1                   #: C.SRLI shifts in zeros: {new}. | RVI-C §27.1.5.2
c.li x10, -8                   #: -8: {new}. | RVI-C §27.1.5.1
c.srai x10, 1                  #: C.SRAI copies the sign: {new}. | RVI-C §27.1.5.2
c.andi x10, 7                  #: C.ANDI: -4 & 7 is {new}. | RVI-C §27.1.5.2
c.li x11, 6                    #: 6: {new}. | RVI-C §27.1.5.1
c.mv x12, x11                  #: 6: {new}. | RVI-C §27.1.5.3
c.sub x12, x10                 #: C.SUB: 6 - 4 is {new}. | RVI-C §27.1.5.3
c.mv x13, x11                  #: 6: {new}. | RVI-C §27.1.5.3
c.xor x13, x10                 #: C.XOR: 6 ^ 4 is {new}. | RVI-C §27.1.5.3
c.li x14, 3                    #: 3: {new}. | RVI-C §27.1.5.1
c.or x14, x10                  #: C.OR: 3 | 4 is {new}. | RVI-C §27.1.5.3
c.mv x15, x11                  #: 6: {new}. | RVI-C §27.1.5.3
c.and x15, x10                 #: C.AND: 6 & 4 is {new}. | RVI-C §27.1.5.3
lui x8, 0x80000                #: bit 31 set, and sign-extended: {new}. | RVI-RV64I §3.1.2.1
c.addiw x8, -1                 #: C.ADDIW adds in the word, and sign-extends: {new}. | RVI-C §27.1.5.2
c.li x9, 1                     #: 1: {new}. | RVI-C §27.1.5.1
c.addw x8, x9                  #: C.ADDW wraps at the word, and sign-extends: {new}. | RVI-C §27.1.5.3
c.subw x8, x9                  #: C.SUBW wraps back: {new}. | RVI-C §27.1.5.3
addi x2, x0, 1                 #: raw material for the stack pointer: {new}. | RVI-RV32I §1.1.4
slli x2, x2, 31                #: 0x80000000: {new}. | RVI-RV64I §3.1.2.1
lui x3, 7                      #: 0x7000: {new}. | RVI-RV64I §3.1.2.1
add x2, x2, x3                 #: the stack pointer, on a page of its own: {new}. | RVI-RV32I §1.1.4
c.addi16sp 64                  #: C.ADDI16SP adds a multiple of sixteen: {new}. | RVI-C §27.1.5.2
c.addi16sp -32                 #: and its immediate is signed: {new}. | RVI-C §27.1.5.2 (boundary: a signed, scaled immediate)
c.addi4spn x8, 8               #: C.ADDI4SPN writes sp + 8 to rd': {new}. | RVI-C §27.1.5.2
c.li x9, -3                    #: -3, to store: {new}. | RVI-C §27.1.5.1
c.sw x8, x9, 4                 #: C.SW stores the word at x8 + 4. | RVI-C §27.1.3.2
c.lw x10, x8, 4                #: C.LW reads it, sign-extended: {new}. | RVI-C §27.1.3.2
c.sd x8, x9, 8                 #: C.SD stores the doubleword at x8 + 8. | RVI-C §27.1.3.2
c.ld x11, x8, 8                #: C.LD reads it: {new}. | RVI-C §27.1.3.2
c.swsp x9, 16                  #: C.SWSP stores the word at sp + 16. | RVI-C §27.1.3.1
c.lwsp x12, 16                 #: C.LWSP reads it, sign-extended: {new}. | RVI-C §27.1.3.1
c.sdsp x9, 24                  #: C.SDSP stores the doubleword at sp + 24. | RVI-C §27.1.3.1
c.ldsp x13, 24                 #: C.LDSP reads it: {new}. | RVI-C §27.1.3.1
addi x5, x0, 3                 #: 3, for a doubleword pattern's top bits: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 61                #: a doubleword pattern: {new}. | RVI-RV64I §3.1.2.1
fmv.d.x f9, x5                 #: f9 holds it; no GPR written. | RVI-D §21.1.5
c.fsd x8, f9, 16               #: C.FSD stores f9 at x8 + 16. | RVI-C §27.1.3.2
c.fld f8, x8, 16               #: C.FLD loads it into f8. | RVI-C §27.1.3.2
fmv.x.d x14, f8                #: read back through a GPR: {new}. | RVI-D §21.1.5
ld x15, x8, 16                 #: and the store itself, as an integer: {new}. | RVI-RV64I §3.1.3
c.fsdsp f9, 32                 #: C.FSDSP stores f9 at sp + 32. | RVI-C §27.1.3.1
c.fldsp f1, 32                 #: C.FLDSP loads it into f1. | RVI-C §27.1.3.1
fmv.x.d x16, f1                #: read back through a GPR: {new}. | RVI-D §21.1.5
ld x17, x2, 32                 #: and the store itself, as an integer: {new}. | RVI-RV64I §3.1.3
c.nop                          #: C.NOP changes nothing but the pc. | RVI-C §27.1.5.5
auipc x18, 0                   #: two bytes on, and nothing else: {new}. | RVI-RV64I §3.1.2.1
c.li x0, 31                    #: a HINT: C.LI with rd = x0. | RVI-C §27.1.5.1
c.lui x0, 1                    #: a HINT: C.LUI with rd = x0. | RVI-C §27.1.5.1
c.addi x8, 0                   #: a HINT: C.ADDI with no immediate. | RVI-C §27.1.5.2
c.slli x8, 0                   #: a HINT: C.SLLI with no shift. | RVI-C §27.1.5.2
c.srli x8, 0                   #: a HINT: C.SRLI with no shift. | RVI-C §27.1.5.2
c.srai x8, 0                   #: a HINT: C.SRAI with no shift. | RVI-C §27.1.5.2
c.mv x0, x8                    #: a HINT: C.MV with rd = x0. | RVI-C §27.1.5.3
c.add x0, x8                   #: a HINT: C.ADD with rd = x0. | RVI-C §27.1.5.3
c.nop 1                        #: a HINT: C.NOP with an immediate. | RVI-C §27.1.5.5
auipc x19, 0                   #: nine parcels on, eighteen bytes: {new}. | RVI-RV64I §3.1.2.1 (boundary: nine HINTs retire)
addi x20, x8, 0                #: x8 is what it was before them: {new}. | RVI-RV32I §1.1.4
c.li x8, 0                     #: 0, for C.BEQZ: {new}. | RVI-C §27.1.5.1
c.beqz x8, 4                   #: C.BEQZ is taken: over one parcel. | RVI-C §27.1.4
c.li x20, 1                    #: skipped. | RVI-C §27.1.4
c.li x9, 9                     #: landed: {new}. | RVI-C §27.1.4
c.bnez x8, 2                   #: C.BNEZ is not taken on zero: the next parcel runs. | RVI-C §27.1.4
c.li x10, 10                   #: the next parcel: {new}. | RVI-C §27.1.4
c.bnez x10, 4                  #: C.BNEZ is taken on a nonzero value: over one parcel. | RVI-C §27.1.4
c.li x20, 1                    #: skipped. | RVI-C §27.1.4
c.li x11, 11                   #: landed: {new}. | RVI-C §27.1.4
c.j 4                          #: C.J jumps over one parcel. | RVI-C §27.1.4
c.li x20, 1                    #: skipped. | RVI-C §27.1.4
c.li x12, 12                   #: landed: {new}. | RVI-C §27.1.4
auipc x1, 0                    #: the base for C.JR: {new}. | RVI-RV64I §3.1.2.1
addi x1, x1, 12                #: past C.JR's skipped parcel: {new}. | RVI-RV32I §1.1.4
c.jr x1                        #: C.JR jumps to x1. | RVI-C §27.1.4
c.li x20, 1                    #: skipped. | RVI-C §27.1.4
c.li x13, 13                   #: landed: {new}. | RVI-C §27.1.4
auipc x1, 0                    #: the base for C.JALR: {new}. | RVI-RV64I §3.1.2.1
addi x1, x1, 12                #: past C.JALR's skipped parcel: {new}. | RVI-RV32I §1.1.4
c.jalr x1                      #: C.JALR with rd = rs1: it jumps to the old x1 and links pc + 2 in x1: {new}. | RVI-C §27.1.4 (boundary: C.JALR links the next parcel)
c.li x20, 1                    #: skipped. | RVI-C §27.1.4
c.li x14, 14                   #: landed at the old x1: {new}. | RVI-C §27.1.4 (boundary: C.JALR takes the old source)
c.mv x8, x2                    #: the stack pointer again: {new}. | RVI-C §27.1.5.3
c.li x9, 5                     #: 5: {new}. | RVI-C §27.1.5.1
c.sd x8, x9, 0                 #: the cell holds 5. | RVI-C §27.1.3.2
addi x10, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
lr.d x10, (x8)                 #: the reservation: {new}. | RVI-A §12.1.2
c.addi x10, 1                  #: a C form between: {new}. | RVI-C §27.1.6
addi x11, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
sc.d x11, x10, (x8)            #: the C form kept the reservation: {new}. | RVI-C §27.1.6; RVI-A §12.1.2
addi x30, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 10              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
c.ebreak                       #: C.EBREAK raises a breakpoint. | RVI-C §27.1.5.6; RVP-MACHINE §2.1.1.15
addi x30, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 10              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
.half 0x4002                   #: C.LWSP with rd = x0 is reserved. | RVI-C §27.1.3.1; RVP-MACHINE §2.1.1.16
addi x30, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 10              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
.half 0x8002                   #: C.JR with rs1 = x0 is reserved. | RVI-C §27.1.4; RVP-MACHINE §2.1.1.16
addi x30, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 10              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
.half 0x0000                   #: all sixteen bits zero: permanently reserved. | RVI-C §27.1.5.4; RVP-MACHINE §2.1.1.16
addi x30, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read is a change. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
.word 0xffffffff               #: the all-ones instruction: no wider instruction is selected, and ILEN is 32. | RVP-MACHINE §2.1.1.16
addi x10, x0, 1                #: raw material for the region base: {new}. | RVI-RV32I §1.1.4
slli x10, x10, 31              #: 0x80000000: {new}. | RVI-RV64I §3.1.2.1
lui x11, 3                     #: 0x3000: {new}. | RVI-RV64I §3.1.2.1
add x11, x11, x10              #: the root table: {new}. | RVI-RV32I §1.1.4
lui x12, 0x20001               #: the pointer's upper bits: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 1               #: root[0] points at base+0x4000: {new}. | RVP-SUPERVISOR §11.1.4.1
sd x12, 0, x11                 #: root[0] written. | RVI-RV64I §3.1.3
lui x12, 0x20000               #: the leaf's upper bits: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 207             #: root[2] is a 1 GiB leaf, VA = PA, R, W, X, A and D: {new}. | RVP-SUPERVISOR §11.1.4.1
sd x12, 16, x11                #: root[2] written. | RVI-RV64I §3.1.3
lui x11, 4                     #: 0x4000: {new}. | RVI-RV64I §3.1.2.1
add x11, x11, x10              #: the level-1 table: {new}. | RVI-RV32I §1.1.4
lui x12, 0x20001               #: the pointer's upper bits: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 1025            #: level-1[2] points at base+0x5000: {new}. | RVP-SUPERVISOR §11.1.4.1
sd x12, 16, x11                #: level-1[2] written. | RVI-RV64I §3.1.3
lui x11, 5                     #: 0x5000: {new}. | RVI-RV64I §3.1.2.1
add x11, x11, x10              #: the level-0 table: {new}. | RVI-RV32I §1.1.4
addi x12, x0, 1                #: level-0[0] maps VA 0x400000 to base+0x6000, readable and executable; level-0[1] stays invalid: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 16              #: level-0[0] maps VA 0x400000 to base+0x6000, readable and executable; level-0[1] stays invalid: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 1               #: level-0[0] maps VA 0x400000 to base+0x6000, readable and executable; level-0[1] stays invalid: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 13              #: level-0[0] maps VA 0x400000 to base+0x6000, readable and executable; level-0[1] stays invalid: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, -1973           #: level-0[0] maps VA 0x400000 to base+0x6000, readable and executable; level-0[1] stays invalid: {new}. | RVI-RV32I §1.1.4
sd x12, 0, x11                 #: level-0[0] written. | RVI-RV64I §3.1.3
addi x5, x0, 8                 #: raw material for satp.MODE: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 60                #: MODE = Sv39: {new}. | RVI-RV64I §3.1.2.1
lui x2, 128                    #: the root's page number: {new}. | RVI-RV64I §3.1.2.1
addi x2, x2, 3                 #: 0x80003, the root: {new}. | RVI-RV32I §1.1.4
or x2, x2, x5                  #: satp's value: {new}. | RVI-RV32I §1.1.4
csrrw x0, satp, x2             #: translation armed for S; M is not translated. | RVI-ZICSR §5.1.1
addi x3, x0, 3                 #: both MPP bits: {new}. | RVI-RV32I §1.1.4
slli x3, x3, 11                #: at bit 11: {new}. | RVI-RV64I §3.1.2.1
csrrc x0, mstatus, x3          #: MPP cleared; no GPR written. | RVI-ZICSR §5.1.1
addi x3, x0, 1                 #: MPP = S: {new}. | RVI-RV32I §1.1.4
slli x3, x3, 11                #: at bit 11: {new}. | RVI-RV64I §3.1.2.1
csrrs x0, mstatus, x3          #: MPP = S; no GPR written. | RVI-ZICSR §5.1.1
lui x6, 6                      #: 0x6000: {new}. | RVI-RV64I §3.1.2.1
add x6, x6, x10                #: the page S will run: {new}. | RVI-RV32I §1.1.4
addi x6, x6, 2047              #: towards its end: {new}. | RVI-RV32I §1.1.4
addi x6, x6, 2045              #: its last word, at 0xffc: {new}. | RVI-RV32I §1.1.4
addi x7, x0, 71                #: C.LI x21, 13, then C.JR x27: {new}. | RVI-RV32I §1.1.4
slli x7, x7, 13                #: C.LI x21, 13, then C.JR x27: {new}. | RVI-RV64I §3.1.2.1
addi x7, x7, -2011             #: C.LI x21, 13, then C.JR x27: {new}. | RVI-RV32I §1.1.4
slli x7, x7, 12                #: C.LI x21, 13, then C.JR x27: {new}. | RVI-RV64I §3.1.2.1
addi x7, x7, -1355             #: C.LI x21, 13, then C.JR x27: {new}. | RVI-RV32I §1.1.4
sw x7, 0, x6                   #: written to the page's last word. | RVI-RV64I §3.1.3
fence.i                        #: the patched parcels are visible to a later fetch. | RVI-ZIFENCEI §4.1
lui x4, 0x401                  #: VA 0x401000, the invalid page: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, -4                #: the mapped page's last word: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4             #: mepc = there; no GPR written. | RVI-ZICSR §5.1.1
auipc x27, 0                   #: C.JR's target, relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: past MRET: {new}. | RVI-RV32I §1.1.4
mret                           #: to S, at the page's last word. | RVP-MACHINE §2.1.3.2
c.li x23, 15                   #: C.JR ran from the page's very last parcel, and landed: {new}. | RVI-C §27.1.4 (boundary: a page's very last parcel)
