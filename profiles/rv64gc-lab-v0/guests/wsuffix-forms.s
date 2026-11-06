lui x5, 0x80000              #: a word with its sign bit set: {new}. | RVI-RV64I §3.1.2, §3.1.2.1, §3.1.2.2
addi x6, x0, -1              #: all 64 bits set: {new}. | RVI-RV32I §1.1.4
srli x7, x6, 33              #: 0x7FFFFFFF, the largest positive word: {new}. | RVI-RV64I §3.1.2, §3.1.2.1, §3.1.2.2
addi x8, x0, 1               #: 1. | RVI-RV32I §1.1.4
slli x9, x8, 32              #: bit 32 alone, above every word: {new}. | RVI-RV64I §3.1.2, §3.1.2.1, §3.1.2.2
addiw x10, x7, 1             #: ADDIW: overflow is ignored and the word sign-extends: {new}. | RVI-RV64I §3.1.2, §3.1.2.1, §3.1.2.2 (boundary: ADDIW overflow)
addiw x11, x9, 5             #: ADDIW ignores bit 32 of its input: {new}. | RVI-RV64I §3.1.2, §3.1.2.1, §3.1.2.2 (boundary: ADDIW ignores the upper bits)
slliw x12, x8, 31            #: SLLIW: bit 31 of the word, sign-extended: {new}. | RVI-RV64I §3.1.2, §3.1.2.1, §3.1.2.2 (boundary: SLLIW's result sign-extends)
srliw x13, x5, 0             #: SRLIW by 0 still sign-extends the word: {new}. | RVI-RV64I §3.1.2, §3.1.2.1, §3.1.2.2 (boundary: SRLIW by zero)
srliw x14, x5, 1             #: SRLIW shifts zeros into the word, so bit 31 clears: {new}. | RVI-RV64I §3.1.2, §3.1.2.1, §3.1.2.2 (boundary: SRLIW zero-fills the word)
sraiw x15, x5, 1             #: SRAIW copies bit 31 of the word: {new}. | RVI-RV64I §3.1.2, §3.1.2.1, §3.1.2.2 (boundary: SRAIW copies bit 31)
addw x16, x7, x8             #: ADDW: overflow is ignored and the word sign-extends: {new}. | RVI-RV64I §3.1.2, §3.1.2.1, §3.1.2.2 (boundary: ADDW overflow)
addw x17, x9, x8             #: ADDW ignores bit 32 of its input: {new}. | RVI-RV64I §3.1.2, §3.1.2.1, §3.1.2.2 (boundary: ADDW ignores the upper bits)
subw x18, x5, x8             #: SUBW: the word's underflow is ignored: {new}. | RVI-RV64I §3.1.2, §3.1.2.1, §3.1.2.2 (boundary: SUBW underflow)
sllw x19, x7, x8             #: SLLW: the word shifted, sign-extended: {new}. | RVI-RV64I §3.1.2, §3.1.2.1, §3.1.2.2
srlw x20, x6, x8             #: SRLW reads only the low word of all ones, so bit 31 clears: {new}. | RVI-RV64I §3.1.2, §3.1.2.1, §3.1.2.2 (boundary: SRLW ignores the upper bits)
sraw x21, x5, x8             #: SRAW copies bit 31 of the word: {new}. | RVI-RV64I §3.1.2, §3.1.2.1, §3.1.2.2
