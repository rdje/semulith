lui x5, 0x12345              #: garbage for the HIGH word of the first operand … | RVI-RV32I §1.1.4
addi x5, x5, 0x678           #: … 0x12345678 … | RVI-RV32I §1.1.4
slli x5, x5, 32              #: … moved to bits 63..32. | RVI-RV64I §3.1.2.1
addi x7, x0, -7              #: the low word to carry: -7 … | RVI-RV32I §1.1.4
slli x7, x7, 32              #: … its low 32 bits isolated: up … | RVI-RV64I §3.1.2.1
srli x7, x7, 32              #: … and back down, zero-filled: 0xfffffff9. | RVI-RV64I §3.1.2.1
or x5, x5, x7                #: x5 = 0x12345678_fffffff9: as a WORD it is -7. | RVI-RV32I §1.1.4
lui x6, 0x2bcdf              #: garbage for the high word of the second operand … | RVI-RV32I §1.1.4
addi x6, x6, -255            #: … 0x2bcdef01 … | RVI-RV32I §1.1.4
slli x6, x6, 32              #: … in bits 63..32 … | RVI-RV64I §3.1.2.1
addi x6, x6, 2               #: … and the low word 2: x6 = 0x2bcdef01_00000002. | RVI-RV32I §1.1.4
mulw x8, x5, x6              #: the low 32 bits only: -7 x 2 = -14, sign-extended: {new}. | RVI-M §11.1.1
divw x9, x5, x6              #: -7 / 2 as 32-bit signed words, towards zero, sign-extended: {new}. | RVI-M §11.1.2
remw x10, x5, x6             #: … the 32-bit remainder, sign-extended: {new}. | RVI-M §11.1.2
divuw x11, x5, x6            #: 0xfffffff9 / 2 as UNSIGNED words: {new} (bit 31 clear). | RVI-M §11.1.2
remuw x12, x5, x6            #: … the unsigned word remainder {new}. | RVI-M §11.1.2
addi x13, x0, 1              #: a divisor whose LOW WORD is zero: 1 … | RVI-RV32I §1.1.4
slli x13, x13, 32            #: … << 32 = 2^32 - nonzero as XLEN, zero as a word. | RVI-RV64I §3.1.2.1
divw x14, x5, x13            #: a WORD division by zero: Table 1 at L = 32 - all bits set, sign-extended: {new}. | RVI-M §11.1.2 (Table 1)
divuw x15, x5, x13           #: unsigned: 2^32 - 1, sign-extended: {new}. | RVI-M §11.1.2 (Table 1)
remw x16, x5, x13            #: the remainder is the dividend's word, sign-extended - including on a divide by zero: {new}. | RVI-M §11.1.2 (Table 1)
remuw x17, x5, x13           #: … REMUW sign-extends it too: {new}. | RVI-M §11.1.2
lui x18, 0x80000             #: the most-negative WORD, -2^31, sign-extended. | RVI-RV32I §1.1.4
addi x19, x0, -1             #: the divisor -1. | RVI-RV32I §1.1.4
divw x20, x18, x19           #: WORD overflow, -2^31 / -1: the quotient equals the dividend, {new}. | RVI-M §11.1.2 (Table 1)
addi x21, x0, 21             #: a sentinel the overflow remainder must replace. | RVI-RV32I §1.1.4
remw x21, x18, x19           #: … the remainder zero: {new}. | RVI-M §11.1.2 (Table 1)
addi x22, x0, 1              #: the divisor 1. | RVI-RV32I §1.1.4
divuw x23, x19, x22          #: 0xffffffff / 1 unsigned: the 32-bit quotient has bit 31 set, so it SIGN-extends: {new}. | RVI-M §11.1.2
lui x24, 0x40000             #: 2^30. | RVI-RV32I §1.1.4
addi x25, x0, 2              #: 2. | RVI-RV32I §1.1.4
mulw x26, x24, x25           #: 2^30 x 2 = 2^31 wraps to the most-negative word, sign-extended: {new}. | RVI-M §11.1.1
