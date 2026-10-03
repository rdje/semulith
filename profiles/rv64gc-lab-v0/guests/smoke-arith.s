# smoke-arith.s — the arithmetic half of the P0-PROFILE.6 matched-profile experiment.
#
# Every instruction here targets a decision `profile.toml` records, so a disagreement with a
# reference model lands on a decision rather than on "something differs". Only R/I/I-shift/S
# formats are used: the B and J immediate layouts live in specification FIGURES this project
# cannot read, and `scripts/riscv_asm.py` refuses to guess them (owner: P0-PROFILE.8).
#
# Registers are written x1 upward and never re-read after being checked, so a trace can be read
# top to bottom. x10 holds the main-memory base and is built arithmetically, because LUI cannot
# produce 0x0000_0000_8000_0000 — see the expected-values file.

lui   x1, 0x80000        # D-LUI-AUIPC   : 32-bit U-imm, low 12 zeroed, SIGN-extended to 64
addiw x2, x1, 1          # D-WSUFFIX     : 32-bit add, overflow ignored, result sign-extended
addi  x3, x0, -1         # I-immediate sign-extension; x0 reads as 0 (D-XLEN, x0 hardwired)
slli  x4, x3, 63         # D-SHAMT       : 6-bit shift amount is legal at 64 bits
srli  x5, x4, 63         # logical right shift brings in zeros
srai  x6, x4, 63         # arithmetic right shift replicates the sign bit
addiw x7, x3, 0          # SEXT.W of 0xFFFFFFFF
slliw x8, x3, 31         # D-SHAMT       : *W shifts use a 5-bit amount on the low 32 bits
add   x9, x1, x2         # 64-bit add, wrapping modulo 2^64 (D-ADDR-WRAP's arithmetic)

addi  x10, x0, 1         # build the main-memory base 0x8000_0000 without LUI (see below)
slli  x10, x10, 31

sd    x9, 1024, x10      # commit one 64-bit result to main memory, well clear of this code
