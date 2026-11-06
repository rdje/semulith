addi x10, x0, 1              #: raw material for the region base. | RVI-RV32I §1.1.4
slli x10, x10, 31            #: 0x80000000, the region's base: {new}. | RVI-RV64I §3.1.2.1
addi x1, x10, 512            #: the first data cell, past this program: {new}. | RVI-RV32I §1.1.4
addi x2, x1, 16              #: the second cell: {new}. | RVI-RV32I §1.1.4
addi x3, x1, 32              #: the third cell: {new}. | RVI-RV32I §1.1.4
addi x4, x1, 48              #: the fourth cell: {new}. | RVI-RV32I §1.1.4
lui x5, 0x44332              #: the low half of the pattern: {new}. | RVI-RV64I §3.1.2.1
addi x5, x5, 0x211           #: 0x44332211: {new}. | RVI-RV32I §1.1.4
lui x6, 0x88776              #: the high half of the pattern: {new}. | RVI-RV64I §3.1.2.1
addi x6, x6, 0x655           #: 0x88776655, its sign bit set: {new}. | RVI-RV32I §1.1.4
slli x6, x6, 32              #: moved to the upper word: {new}. | RVI-RV64I §3.1.2.1
add x7, x6, x5               #: the pattern 0x8877665544332211: {new}. | RVI-RV32I §1.1.4
addi x9, x0, -1              #: all ones, to show what a narrow store leaves alone: {new}. | RVI-RV32I §1.1.4
sd x7, 0, x1                 #: SD stores all 64 bits of rs2. | RVI-RV64I §3.1.3
ld x11, x1, 0                #: LD loads all 64 bits, the store's value back: {new}. | RVI-RV64I §3.1.3 (boundary: LD reads what SD stored)
ld x22, x1, 0                #: read again: the first load moved nothing, {new}. | RVI-RV64I §3.1.3
lw x12, x1, 4                #: LW sign-extends: the upper word 0x88776655 has its sign bit set: {new}. | RVI-RV64I §3.1.3 (boundary: LW sign-extends)
lwu x13, x1, 4               #: LWU zero-extends the same word: {new}. | RVI-RV64I §3.1.3 (boundary: LWU zero-extends)
lw x14, x1, 0                #: LW of a word with its sign bit clear: {new}. | RVI-RV64I §3.1.3 (boundary: LW of a positive word)
lh x15, x1, 6                #: LH sign-extends the halfword 0x8877: {new}. | RVI-RV64I §3.1.3 (boundary: LH sign-extends)
lhu x16, x1, 6               #: LHU zero-extends the same halfword: {new}. | RVI-RV64I §3.1.3 (boundary: LHU zero-extends)
lb x17, x1, 7                #: LB sign-extends the byte 0x88: {new}. | RVI-RV64I §3.1.3 (boundary: LB sign-extends)
lbu x18, x1, 7               #: LBU zero-extends the same byte: {new}. | RVI-RV64I §3.1.3 (boundary: LBU zero-extends)
sd x9, 0, x2                 #: the second cell, all ones. | RVI-RV64I §3.1.3
sb x7, 0, x2                 #: SB stores only the low 8 bits of rs2. | RVI-RV64I §3.1.3
ld x19, x2, 0                #: read back: only the low byte moved, {new}. | RVI-RV64I §3.1.3 (boundary: SB stores 8 bits)
sd x9, 0, x3                 #: the third cell, all ones. | RVI-RV64I §3.1.3
sh x7, 0, x3                 #: SH stores only the low 16 bits of rs2. | RVI-RV64I §3.1.3
ld x20, x3, 0                #: read back: only the low halfword moved, {new}. | RVI-RV64I §3.1.3 (boundary: SH stores 16 bits)
sd x9, 0, x4                 #: the fourth cell, all ones. | RVI-RV64I §3.1.3
sw x7, 0, x4                 #: SW stores only the low 32 bits of rs2. | RVI-RV64I §3.1.3
ld x21, x4, 0                #: read back: only the low word moved, {new}. | RVI-RV64I §3.1.3 (boundary: SW stores 32 bits)
