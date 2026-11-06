addi x5, x0, 1               #: 1, the value shifted. | RVI-RV32I §1.1.4
slli x6, x5, 63              #: SLLI takes a 6-bit amount: 1 << 63 = {new}. | RVI-RV64I §3.1.2.1, §3.1.2.2 (boundary: SLLI's largest amount)
srli x7, x6, 63              #: SRLI takes a 6-bit amount: {new}. | RVI-RV64I §3.1.2.1, §3.1.2.2 (boundary: SRLI's largest amount)
srai x8, x6, 63              #: SRAI takes a 6-bit amount and copies the sign: {new}. | RVI-RV64I §3.1.2.1, §3.1.2.2 (boundary: SRAI's largest amount)
slli x9, x5, 32              #: an amount of 32 uses bit 5 of the immediate: {new}. | RVI-RV64I §3.1.2.1, §3.1.2.2 (boundary: an immediate amount above 31)
addi x10, x0, 65             #: 65, whose low 6 bits are 1. | RVI-RV32I §1.1.4
sll x11, x5, x10             #: SLL uses only the low 6 bits of rs2: 1 << 1 = {new}. | RVI-RV64I §3.1.2.1, §3.1.2.2 (boundary: SLL with rs2 above 63)
srl x12, x6, x10             #: SRL uses only the low 6 bits of rs2: 2^63 >> 1 = {new}. | RVI-RV64I §3.1.2.1, §3.1.2.2 (boundary: SRL with rs2 above 63)
sra x13, x6, x10             #: SRA uses only the low 6 bits of rs2 and copies the sign: {new}. | RVI-RV64I §3.1.2.1, §3.1.2.2 (boundary: SRA with rs2 above 63)
addi x14, x0, 64             #: 64, whose low 6 bits are 0. | RVI-RV32I §1.1.4
sll x15, x5, x14             #: so SLL shifts by nothing: {new}. | RVI-RV64I §3.1.2.1, §3.1.2.2 (boundary: SLL with rs2 at 64)
addi x16, x0, 33             #: 33, whose low 5 bits are 1. | RVI-RV32I §1.1.4
lui x17, 0x80000             #: the word with its sign bit set: {new}. | RVI-RV64I §3.1.2.1, §3.1.2.2
sllw x18, x5, x16            #: SLLW uses rs2[4:0]: 1 << 1 = {new}. | RVI-RV64I §3.1.2.1, §3.1.2.2 (boundary: SLLW with rs2 above 31)
srlw x19, x17, x16           #: SRLW uses rs2[4:0]: 0x80000000 >> 1 = {new}. | RVI-RV64I §3.1.2.1, §3.1.2.2 (boundary: SRLW with rs2 above 31)
sraw x20, x17, x16           #: SRAW uses rs2[4:0] and copies bit 31: {new}. | RVI-RV64I §3.1.2.1, §3.1.2.2 (boundary: SRAW with rs2 above 31)
addi x21, x0, 32             #: 32, whose low 5 bits are 0. | RVI-RV32I §1.1.4
sllw x22, x5, x21            #: so SLLW shifts by nothing: {new}. | RVI-RV64I §3.1.2.1, §3.1.2.2 (boundary: SLLW with rs2 at 32)
slliw x23, x5, 31            #: SLLIW takes 5 bits: 1 << 31 as a word, sign-extended: {new}. | RVI-RV64I §3.1.2.1, §3.1.2.2 (boundary: SLLIW's largest amount)
srliw x24, x17, 31           #: SRLIW takes 5 bits: {new}. | RVI-RV64I §3.1.2.1, §3.1.2.2 (boundary: SRLIW's largest amount)
sraiw x25, x17, 31           #: SRAIW takes 5 bits and copies bit 31: {new}. | RVI-RV64I §3.1.2.1, §3.1.2.2 (boundary: SRAIW's largest amount)
