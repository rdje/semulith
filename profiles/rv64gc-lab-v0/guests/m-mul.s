addi x5, x0, 7               #: a small positive operand, 7. | RVI-RV32I §1.1.4
addi x6, x0, -3              #: a small negative operand, -3. | RVI-RV32I §1.1.4
mul x7, x5, x6               #: 7 x -3, mixed signs: the low 64 bits are -21 = {new}. | RVI-M §11.1.1
mulh x8, x5, x6              #: the high half of the signed product -21: {new}. | RVI-M §11.1.1
mulhsu x9, x5, x6            #: 7 (signed) x -3 read UNSIGNED (2^64 - 3): the high half {new}. | RVI-M §11.1.1
mulhu x10, x5, x6            #: both unsigned, the same magnitudes: the high half {new}. | RVI-M §11.1.1
mulhsu x11, x6, x5           #: -3 (signed) x 7 (unsigned): a negative product, high half {new}. | RVI-M §11.1.1
addi x12, x0, 1              #: build the most-negative value: 1 … | RVI-RV32I §1.1.4
slli x12, x12, 63            #: … shifted to bit 63 = -2^63. | RVI-RV64I §3.1.2.1
addi x13, x0, 13             #: a sentinel the zero half must REPLACE. | RVI-RV32I §1.1.4
mul x13, x12, x12            #: (-2^63)^2 = 2^126: the low half {new}. | RVI-M §11.1.1
mulh x14, x12, x12           #: … signed x signed, the high half {new} (2^62). | RVI-M §11.1.1
mulhu x15, x12, x12          #: 2^63 x 2^63 unsigned = 2^126: the high half {new}. | RVI-M §11.1.1
mulhsu x16, x12, x12         #: -2^63 (signed) x 2^63 (unsigned) = -2^126: the high half {new}. | RVI-M §11.1.1
addi x17, x0, -1             #: -1: all bits set. | RVI-RV32I §1.1.4
mul x18, x17, x17            #: (-1) x (-1): the low half {new}. | RVI-M §11.1.1
addi x19, x0, 19             #: a sentinel the zero half must REPLACE. | RVI-RV32I §1.1.4
mulh x19, x17, x17           #: … signed, the product is +1: the high half {new}. | RVI-M §11.1.1
mulhu x20, x17, x17          #: (2^64 - 1)^2 unsigned: the high half {new} (2^64 - 2). | RVI-M §11.1.1
mulhsu x21, x17, x17         #: -1 (signed) x (2^64 - 1) (unsigned): the high half {new}. | RVI-M §11.1.1
mul x22, x12, x17            #: -2^63 x -1 = 2^63, which wraps at 64 bits: the low half {new}. | RVI-M §11.1.1
addi x23, x0, 23             #: a sentinel the zero half must REPLACE. | RVI-RV32I §1.1.4
mulh x23, x12, x17           #: … and the high half of the exact 2^63: {new}. | RVI-M §11.1.1
srli x24, x17, 1             #: the most-positive value, 2^63 - 1. | RVI-RV64I §3.1.2.1
mulhu x25, x24, x24          #: (2^63 - 1)^2 unsigned: the high half {new}. | RVI-M §11.1.1
mulh x26, x24, x12           #: (2^63 - 1) x -2^63, signed: the high half {new}. | RVI-M §11.1.1
