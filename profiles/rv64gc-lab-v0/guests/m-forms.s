addi x5, x0, -7              #: the signed dividend -7 (also the operand whose word is -7). | RVI-RV32I §1.1.4
addi x6, x0, 2               #: the divisor 2. | RVI-RV32I §1.1.4
addi x7, x0, -1              #: -1: all bits set, the overflow divisor and the unsigned maximum. | RVI-RV32I §1.1.4
addi x8, x0, 1               #: build the most-negative XLEN value: 1 … | RVI-RV32I §1.1.4
slli x8, x8, 63              #: … at bit 63 = -2^63. | RVI-RV64I §3.1.2.1
addi x9, x0, 1               #: build the most-negative WORD with a zero high half: 1 … | RVI-RV32I §1.1.4
slli x9, x9, 31              #: … at bit 31 = 0x80000000, -2^31 as a word, +2^31 as XLEN. | RVI-RV64I §3.1.2.1
mul x10, x5, x6              #: MUL: the low 64 bits of -7 x 2 = -14: {new}. | RVI-M §11.1.1
mulh x11, x5, x6             #: MULH: the high half of the signed product -14: {new}. | RVI-M §11.1.1
mulhsu x12, x5, x7           #: MULHSU: -7 (signed) x 2^64 - 1 (unsigned) = -7 x 2^64 + 7, the high half -7: {new}. | RVI-M §11.1.1
mulhu x13, x7, x6            #: MULHU: (2^64 - 1) x 2 = 2^65 - 2 unsigned, the high half 1: {new}. | RVI-M §11.1.1
mulw x14, x5, x9             #: MULW: the low 32 bits of -7 x 2^31, sign-extended: {new} (MUL would give 0xfffffffc80000000). | RVI-M §11.1.1
div x15, x5, x6              #: DIV: -7 / 2 rounds TOWARDS ZERO: {new} (-3, not -4). | RVI-M §11.1.2
divu x16, x7, x6             #: DIVU: (2^64 - 1) / 2 unsigned: {new}. | RVI-M §11.1.2
rem x17, x5, x6              #: REM: the remainder takes the dividend's sign: {new} (-1). | RVI-M §11.1.2
remu x18, x7, x6             #: REMU: (2^64 - 1) rem 2 unsigned: {new}. | RVI-M §11.1.2
divw x19, x9, x6             #: DIVW: the low words only, -2^31 / 2 = -2^30, sign-extended: {new} (DIV would give 2^30). | RVI-M §11.1.2
divuw x20, x9, x6            #: DIVUW: 0x80000000 / 2 unsigned words, bit 31 clear: {new}. | RVI-M §11.1.2
remw x21, x9, x5             #: REMW: -2^31 rem -7 as words, the dividend's sign: {new} (-2; REM of +2^31 would give +2). | RVI-M §11.1.2
remuw x22, x9, x5            #: REMUW: 0x80000000 rem 0xfffffff9 unsigned words = the dividend, sign-extended: {new}. | RVI-M §11.1.2
div x23, x5, x0              #: DIVISION BY ZERO, signed: Table 1 - the quotient has all bits set, {new}; no trap. | RVI-M §11.1.2 (Table 1)
divu x24, x5, x0             #: by zero, unsigned: 2^64 - 1, all bits set, {new}. | RVI-M §11.1.2 (Table 1)
rem x25, x5, x0              #: the remainder of division by zero equals the dividend: {new}. | RVI-M §11.1.2 (Table 1)
remu x26, x5, x0             #: … unsigned as well: the dividend, {new}. | RVI-M §11.1.2 (Table 1)
div x27, x8, x7              #: SIGNED OVERFLOW, -2^63 / -1: Table 1 - the quotient equals the dividend, {new}; no trap. | RVI-M §11.1.2 (Table 1)
addi x28, x0, 28             #: a sentinel the overflow remainder must REPLACE (a zero over a zero would show nothing). | RVI-RV32I §1.1.4
rem x28, x8, x7              #: … and the remainder is zero: {new}. | RVI-M §11.1.2 (Table 1)
divw x29, x9, x0             #: WORD division by zero: Table 1 at L = 32 - all bits set, sign-extended: {new}. | RVI-M §11.1.2 (Table 1)
divuw x30, x9, x0            #: unsigned word by zero: 2^32 - 1, sign-extended: {new}. | RVI-M §11.1.2 (Table 1)
remw x31, x9, x0             #: the word remainder of division by zero is the dividend's word, sign-extended: {new}. | RVI-M §11.1.2 (Table 1)
remuw x10, x9, x0            #: … REMUW too: the dividend's word, sign-extended, {new} (replacing the MUL result). | RVI-M §11.1.2 (Table 1)
divw x11, x9, x7             #: WORD OVERFLOW, -2^31 / -1: the quotient equals the dividend, sign-extended, {new} (replacing the MULH result). | RVI-M §11.1.2 (Table 1)
remw x12, x9, x7             #: … and the word remainder is zero: {new} (replacing the MULHSU result). | RVI-M §11.1.2 (Table 1)
