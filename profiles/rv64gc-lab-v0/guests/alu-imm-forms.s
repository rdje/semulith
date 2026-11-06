addi x5, x0, 5               #: 5, the operand the first forms read. | RVI-RV32I §1.1.4
addi x6, x5, -7              #: ADDI adds the sign-extended immediate: 5 + -7 = {new}. | RVI-RV32I §1.1.4 (boundary: a negative immediate)
addi x7, x0, -1              #: the immediate -1 sign-extends to all 64 bits: {new}. | RVI-RV32I §1.1.4
srli x8, x7, 1               #: 2^63 - 1, the largest positive value: {new}. | RVI-RV64I §3.1.2.1
addi x9, x8, 1               #: overflow is ignored: 2^63 - 1 + 1 keeps the low 64 bits, {new}. | RVI-RV32I §1.1.4 (boundary: ADDI overflow ignored)
addi x10, x0, 2047           #: the largest 12-bit immediate: {new}. | RVI-RV32I §1.1.4 (boundary: the largest immediate)
addi x11, x0, -2048          #: the smallest 12-bit immediate, sign-extended: {new}. | RVI-RV32I §1.1.4 (boundary: the smallest immediate)
slti x12, x5, 6              #: SLTI, signed: 5 < 6, so {new}. | RVI-RV32I §1.1.4
addi x13, x0, 77             #: a sentinel, so the 0 that follows is a change. | RVI-RV32I §1.1.4
slti x13, x5, -1             #: SLTI, signed: 5 < -1 is false, so {new}. | RVI-RV32I §1.1.4 (boundary: SLTI against a negative immediate)
slti x14, x7, 0              #: SLTI, signed: -1 < 0, so {new}. | RVI-RV32I §1.1.4 (boundary: SLTI with a negative operand)
lui x15, 1                   #: 4096, which no unextended 12-bit immediate can reach: {new}. | RVI-RV64I §3.1.2.1
sltiu x16, x15, -1           #: SLTIU sign-extends first, then compares unsigned: 4096 < 2^64 - 1, so {new}. | RVI-RV32I §1.1.4 (boundary: SLTIU's immediate is sign-extended first)
addi x17, x0, 77             #: a sentinel, so the 0 that follows is a change. | RVI-RV32I §1.1.4
sltiu x17, x7, 1             #: SLTIU, unsigned: 2^64 - 1 < 1 is false, so {new}. | RVI-RV32I §1.1.4 (boundary: SLTIU with a negative operand)
sltiu x18, x0, 1             #: SLTIU rd, rs1, 1 sets rd when rs1 is zero: {new}. | RVI-RV32I §1.1.4 (boundary: SLTIU below 1)
xori x19, x5, -1             #: XORI with -1 is the bitwise NOT of 5: {new}. | RVI-RV32I §1.1.4 (boundary: XORI's immediate is sign-extended)
ori x20, x5, -16             #: ORI with the sign-extended -16: {new}. | RVI-RV32I §1.1.4 (boundary: ORI's immediate is sign-extended)
andi x21, x7, -16            #: ANDI with the sign-extended -16: {new}. | RVI-RV32I §1.1.4 (boundary: ANDI's immediate is sign-extended)
