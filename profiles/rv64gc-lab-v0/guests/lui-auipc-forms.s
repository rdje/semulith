lui x5, 0x12345              #: LUI fills the low 12 bits with zeros: {new}. | RVI-RV64I §3.1.2.1
lui x6, 0x80000              #: bit 31 set: the 32-bit result sign-extends to 64 bits, {new}. | RVI-RV64I §3.1.2.1 (boundary: LUI sign-extends from bit 31)
lui x7, 0x7ffff              #: bit 31 clear, the largest positive result: {new}. | RVI-RV64I §3.1.2.1 (boundary: LUI's largest positive result)
lui x8, 0xfffff              #: every U-immediate bit set: {new}. | RVI-RV64I §3.1.2.1 (boundary: LUI with all its immediate bits set)
addi x13, x0, 77             #: a sentinel, so the 0 that follows is a change. | RVI-RV32I §1.1.4
lui x13, 0                   #: a zero immediate clears rd: {new}. | RVI-RV64I §3.1.2.1 (boundary: LUI with a zero immediate)
auipc x9, 0                  #: AUIPC with a zero offset reads this instruction's own address: {new}. | RVI-RV64I §3.1.2.1
auipc x10, 1                 #: AUIPC adds the 0x1000 offset to its own address: {new}. | RVI-RV64I §3.1.2.1
auipc x11, 0x80000           #: the offset sign-extends to -2^31, so the 0x80000000 of the address cancels: {new}. | RVI-RV64I §3.1.2.1 (boundary: AUIPC's offset sign-extends)
auipc x12, 0x7ffff           #: the largest positive offset, 0x7ffff000, added: {new}. | RVI-RV64I §3.1.2.1 (boundary: AUIPC's largest positive offset)
