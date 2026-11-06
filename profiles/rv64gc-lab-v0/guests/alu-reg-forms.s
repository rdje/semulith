addi x5, x0, 5               #: 5, the operand the first forms read. | RVI-RV32I §1.1.4
addi x6, x0, -7              #: -7: negative when signed, huge when unsigned. | RVI-RV32I §1.1.4
add x7, x5, x6               #: ADD: 5 + -7 = {new}. | RVI-RV32I §1.1.4
sub x8, x5, x6               #: SUB subtracts rs2 from rs1: 5 - -7 = {new}. | RVI-RV32I §1.1.4 (boundary: SUB's operand order)
sub x9, x6, x5               #: the other order: -7 - 5 = {new}. | RVI-RV32I §1.1.4
addi x10, x0, -1             #: all 64 bits set: {new}. | RVI-RV32I §1.1.4
srli x11, x10, 1             #: 2^63 - 1, the largest positive value: {new}. | RVI-RV64I §3.1.2.1
add x12, x11, x5             #: overflow is ignored: 2^63 - 1 + 5 keeps the low 64 bits, {new}. | RVI-RV32I §1.1.4 (boundary: ADD overflow ignored)
sub x13, x12, x5             #: and back through the same wrap: {new}. | RVI-RV32I §1.1.4 (boundary: SUB overflow ignored)
slt x14, x6, x5              #: SLT, signed: -7 < 5, so {new}. | RVI-RV32I §1.1.4 (boundary: SLT reads rs1 as negative)
addi x15, x0, 77             #: a sentinel, so the 0 that follows is a change. | RVI-RV32I §1.1.4
sltu x15, x6, x5             #: SLTU, unsigned: rs1 reads 2^64 - 7, not below 5, so {new}. | RVI-RV32I §1.1.4 (boundary: SLTU reads the same rs1 as huge)
sltu x16, x5, x6             #: SLTU, unsigned: 5 < 2^64 - 7, so {new}. | RVI-RV32I §1.1.4
addi x17, x0, 77             #: a sentinel, so the 0 that follows is a change. | RVI-RV32I §1.1.4
slt x17, x5, x5              #: equal is not less: {new}. | RVI-RV32I §1.1.4 (boundary: SLT on equal operands)
xor x18, x5, x6              #: XOR: {new}. | RVI-RV32I §1.1.4
or x19, x5, x6               #: OR: {new}. | RVI-RV32I §1.1.4
and x20, x5, x6              #: AND: {new}. | RVI-RV32I §1.1.4
