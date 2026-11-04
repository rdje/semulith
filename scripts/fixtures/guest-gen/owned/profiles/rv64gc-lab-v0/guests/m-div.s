addi x5, x0, -7              #: the dividend -7. | RVI-RV32I §1.1.4
addi x6, x0, 2               #: the divisor 2. | RVI-RV32I §1.1.4
div x7, x5, x6               #: -7 / 2 rounds TOWARDS ZERO: {new} (-3, not -4). | RVI-M §11.1.2
rem x8, x5, x6               #: … the remainder takes the dividend's sign: {new} (-1). | RVI-M §11.1.2
addi x10, x0, 7              #: the dividend 7. | RVI-RV32I §1.1.4
addi x11, x0, -2             #: the divisor -2. | RVI-RV32I §1.1.4
div x12, x10, x11            #: 7 / -2: {new} (-3). | RVI-M §11.1.2
rem x13, x10, x11            #: … the remainder, the dividend's sign: {new} (+1). | RVI-M §11.1.2
div x14, x5, x11             #: -7 / -2: {new} (+3). | RVI-M §11.1.2
rem x15, x5, x11             #: … the remainder {new} (-1). | RVI-M §11.1.2
div x16, x5, x0              #: DIVISION BY ZERO, signed: Table 1 - the quotient has all bits set, {new}; no trap. | RVI-M §11.1.2 (Table 1)
divu x17, x5, x0             #: by zero, unsigned: 2^64 - 1, all bits set, {new}. | RVI-M §11.1.2 (Table 1)
rem x18, x5, x0              #: the remainder of division by zero equals the dividend: {new}. | RVI-M §11.1.2 (Table 1)
remu x19, x5, x0             #: … unsigned as well: the dividend, {new}. | RVI-M §11.1.2 (Table 1)
addi x20, x0, 1              #: build the most-negative value: 1 … | RVI-RV32I §1.1.4
slli x20, x20, 63            #: … at bit 63 = -2^63. | RVI-RV64I §3.1.2.1
addi x21, x0, -1             #: the divisor -1. | RVI-RV32I §1.1.4
div x22, x20, x21            #: SIGNED OVERFLOW, -2^63 / -1: Table 1 - the quotient equals the dividend, {new}; no trap. | RVI-M §11.1.2 (Table 1)
addi x23, x0, 23             #: a sentinel the overflow remainder must REPLACE (a zero over a zero would show nothing). | RVI-RV32I §1.1.4
rem x23, x20, x21            #: … and the remainder is zero: {new}. | RVI-M §11.1.2 (Table 1)
divu x24, x21, x6            #: (2^64 - 1) / 2 unsigned: {new}. | RVI-M §11.1.2
remu x25, x21, x6            #: … the unsigned remainder {new}. | RVI-M §11.1.2
addi x26, x0, 26             #: a sentinel the zero quotient must replace. | RVI-RV32I §1.1.4
divu x26, x5, x21            #: (2^64 - 7) / (2^64 - 1) unsigned: {new}. | RVI-M §11.1.2
remu x27, x5, x21            #: … the remainder is the whole dividend, {new}. | RVI-M §11.1.2
div x28, x20, x6             #: -2^63 / 2 - an exact signed quotient: {new}. | RVI-M §11.1.2
divu x29, x20, x6            #: … read unsigned, 2^63 / 2: {new}. | RVI-M §11.1.2
