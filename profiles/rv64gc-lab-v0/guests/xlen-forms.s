addi x5, x0, 1               #: 1, the bit to place at the top of a 64-bit register. | RVI-RV32I §1.1.4
slli x5, x5, 63              #: bit 63 exists: 1 << 63 = -2^63, {new} — a 64-bit register, not a 32-bit one. | RVI-RV64I §3.1.2.1
srli x6, x5, 63              #: the logical shift back by 63 yields 1: {new} — the top bit was bit 63. | RVI-RV64I §3.1.2.1
srai x7, x5, 63              #: the arithmetic shift copies bit 63 into all 64 bits: {new}. | RVI-RV64I §3.1.2.1
addi x8, x0, -1              #: -1: all 64 bits set, {new}. | RVI-RV32I §1.1.4
slli x9, x8, 32              #: bits 32..63 are real: -1 << 32 = {new}. | RVI-RV64I §3.1.2.1
slli x10, x8, 40             #: a 6-bit shift amount (40 > 31 is legal in RV64I): {new}. | RVI-RV64I §3.1.2.1
srli x11, x8, 1              #: the largest positive XLEN value 2^63 - 1: {new}. | RVI-RV64I §3.1.2.1
addi x12, x11, 1             #: 2^63 - 1 + 1 wraps modulo 2^64 to -2^63: {new} — no overflow trap. | RVI-RV32I §1.1.4
add x13, x8, x8              #: -1 + -1 = -2 modulo 2^64: {new} — the carry out of bit 63 is discarded. | RVI-RV32I §1.1.4
lui x14, 0x80000             #: LUI 0x80000: the 32-bit immediate sign-extended to 64 bits: {new}. | RVI-RV64I §3.1.2.2
addiw x15, x14, 1            #: ADDIW: the low word 0x80000001, sign-extended: {new}. | RVI-RV64I §3.1.2
srliw x16, x14, 1            #: SRLIW: the low word 0x80000000 >> 1 = 0x40000000, sign-extended with bit 31 clear: {new}. | RVI-RV64I §3.1.2.1
sraiw x17, x14, 1            #: SRAIW: the low word's sign at bit 31 is copied: 0xC0000000 sign-extended: {new}. | RVI-RV64I §3.1.2.1
addw x18, x8, x5             #: ADDW ignores bits 32..63 of its inputs: -1 + 0 (the low word of -2^63) = -1 as a word, sign-extended: {new}. | RVI-RV64I §3.1.2
subw x19, x0, x11            #: SUBW: 0 - 0xFFFFFFFF (the low word of 2^63 - 1) = 1 as a word, sign-extended: {new}. | RVI-RV64I §3.1.2
sllw x20, x6, x11            #: SLLW takes the low 5 bits of the shift amount: 1 << 31 = 0x80000000, sign-extended: {new}. | RVI-RV64I §3.1.2.1
auipc x1, 0                  #: the handler's base: this instruction's own 64-bit address, {new}. | RVI-RV32I §1.1.4
addi x1, x1, 24              #: the handler sits six instructions on, at {new}. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1          #: direct-mode mtvec = the handler; no GPR written. | RVP-MACHINE §2.1.5
addi x21, x0, 1              #: 1, the bit to place at 2^40. | RVI-RV32I §1.1.4
slli x21, x21, 40            #: the address 2^40 = {new}: a 64-bit address, outside every declared region. | RVI-RV64I §3.1.2.1
ld x22, x21, 0               #: a load at 2^40 raises a load access fault (cause 5, tval = the address); x22 is never written. | RVP-MACHINE §2.1.6 (D-ADDRESS-SPACE)
csrrs x30, mcause, x0        #: the handler reads mcause: {new} = 5, a load access fault. | RVP-MACHINE §2.1.6
csrrs x31, mtval, x0         #: the handler reads mtval: {new} — the faulting address, all 64 bits of it. | RVP-MACHINE §2.1.7
