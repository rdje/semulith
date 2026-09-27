//! Target arithmetic primitives for `rv64i-lab-v0`, written to SEM-03: every operation
//! states its widths, signedness, intermediate precision, truncation, and exceptional
//! behavior in its own contract, independently of host defaults.
//!
//! Source linkage: each function's contract names the requirement record in
//! `profiles/rv64i-lab-v0/requirements.sexp` and the pinned locator the requirement's
//! statement was derived from. These primitives are the executable half of those
//! requirements; the instruction layer that composes them (state read/write, immediate
//! extraction) lands with the interpreter slice (`P1-LAB.8`).
//!
//! Target values are held in `u64` regardless of the operation's signedness: signedness is
//! a per-operation contract, not a type (SEM-03). A signed view is taken inside the one
//! operation that needs it and documented there.

/// XLEN for `rv64i-lab-v0`: the integer registers and the supported user address space
/// are 64 bits. — REQ-D-XLEN (RVI-RV64I §3.1.1).
pub const XLEN: u32 = 64;

/// The register/immediate shift-amount width at XLEN = 64: 6 bits index 0..=63.
/// — REQ-D-SHAMT (RVI-RV64I §3.1.2.1, §3.1.2.2).
pub const SHAMT_BITS: u32 = 6;

/// The shift-amount width for the `*W` shifts: 5 bits index 0..=31.
/// — REQ-D-SHAMT (RVI-RV64I §3.1.2.1, §3.1.2.2).
pub const SHAMT_W_BITS: u32 = 5;

// ── Integer register/immediate arithmetic ────────────────────────────────────────────────
// REQ-D-ALU-REG / REQ-D-ALU-IMM (RVI-RV32I §1.1.4). Width: XLEN. Intermediate precision:
// full XLEN, single truncation modulo 2^XLEN. Flags: none. Exceptional behavior: none —
// overflow is ignored, the result wraps.

/// `ADD` / `ADDI`: addition modulo 2^XLEN.
#[must_use]
pub fn add(x: u64, y: u64) -> u64 {
    x.wrapping_add(y)
}

/// `SUB`: subtraction modulo 2^XLEN.
#[must_use]
pub fn sub(x: u64, y: u64) -> u64 {
    x.wrapping_sub(y)
}

/// `SLT` / `SLTI`: signed less-than. Width: XLEN, interpreted as two's-complement.
/// Result: 1 or 0. No truncation (the 1-bit result is zero-extended into XLEN).
#[must_use]
pub fn slt(x: u64, y: u64) -> u64 {
    u64::from((x as i64) < (y as i64))
}

/// `SLTU` / `SLTIU`: unsigned less-than. Result: 1 or 0.
/// (The `SLTIU` immediate is sign-extended *before* this comparison — that composition is
/// an instruction-layer rule, REQ-D-ALU-IMM, not part of this primitive.)
#[must_use]
pub fn sltu(x: u64, y: u64) -> u64 {
    u64::from(x < y)
}

/// `AND` / `ANDI`: bitwise and. Width: XLEN, no signedness.
#[must_use]
pub fn and(x: u64, y: u64) -> u64 {
    x & y
}

/// `OR` / `ORI`: bitwise or. Width: XLEN, no signedness.
#[must_use]
pub fn or(x: u64, y: u64) -> u64 {
    x | y
}

/// `XOR` / `XORI`: bitwise xor. Width: XLEN, no signedness.
#[must_use]
pub fn xor(x: u64, y: u64) -> u64 {
    x ^ y
}

// ── Field extraction and extension ───────────────────────────────────────────────────────

/// Extract bits `hi..=lo` (inclusive, 0-indexed) of `value`, zero-extended into XLEN.
/// Contract: `lo <= hi < XLEN`. Used for immediate fields and the shift-amount masks.
/// No signedness; the result is exactly `hi - lo + 1` bits wide.
#[must_use]
pub fn bits(value: u64, hi: u32, lo: u32) -> u64 {
    debug_assert!(lo <= hi && hi < XLEN, "bits: need lo <= hi < {XLEN}");
    (value >> lo) & (u64::MAX >> (XLEN - 1 - (hi - lo)))
}

/// Sign-extend the low `from_bits` of `value` into XLEN: bit `from_bits - 1` is replicated
/// into every bit position above it. Contract: `1 <= from_bits <= XLEN`.
/// — REQ-D-ALU-IMM (12-bit I-immediate), REQ-D-LOAD-EXT (load widths), REQ-D-LUI-AUIPC
/// (32-bit U-immediate), all via the same width-parametric rule.
#[must_use]
pub fn sext(value: u64, from_bits: u32) -> u64 {
    debug_assert!(
        (1..=XLEN).contains(&from_bits),
        "sext: need 1 <= from_bits <= {XLEN}"
    );
    ((value << (XLEN - from_bits)) as i64 >> (XLEN - from_bits)) as u64
}

// ── Shifts ───────────────────────────────────────────────────────────────────────────────
// REQ-D-SHAMT (RVI-RV64I §3.1.2.1, §3.1.2.2): the shift amount is 6 bits (register/immediate)
// or 5 bits (`*W`), fixed by decode — the caller passes an already-masked amount, and the
// contract below states what this primitive requires. An unmasked amount reaching these
// functions is a model error (SEM-01), not target behavior: it panics rather than silently
// wrapping the amount, because a silently wrapped amount would turn a decoder bug into a
// plausible-looking wrong result.

/// The shift amount for `SLL`/`SRL`/`SRA` and the immediate forms: the low 6 bits of rs2.
/// — REQ-D-SHAMT.
#[must_use]
pub fn shamt64(rs2: u64) -> u64 {
    bits(rs2, SHAMT_BITS - 1, 0)
}

/// The shift amount for `SLLW`/`SRLW`/`SRAW`: the low 5 bits of rs2.
/// — REQ-D-SHAMT.
#[must_use]
pub fn shamt32(rs2: u64) -> u64 {
    bits(rs2, SHAMT_W_BITS - 1, 0)
}

/// `SLL`/`SLLI`: logical left shift, zeros shifted in. Width: XLEN.
/// Contract: `shamt < XLEN` (decode enforces REQ-D-SHAMT via [`shamt64`]).
#[must_use]
pub fn shl(x: u64, shamt: u64) -> u64 {
    debug_assert!(
        shamt < u64::from(XLEN),
        "shl: unmasked shift amount — a decoder bug"
    );
    x << shamt
}

/// `SRL`/`SRLI`: logical right shift, zeros shifted in. Width: XLEN.
/// Contract: `shamt < XLEN`.
#[must_use]
pub fn shr(x: u64, shamt: u64) -> u64 {
    debug_assert!(
        shamt < u64::from(XLEN),
        "shr: unmasked shift amount — a decoder bug"
    );
    x >> shamt
}

/// `SRA`/`SRAI`: arithmetic right shift, the sign bit is replicated. Width: XLEN,
/// interpreted as two's-complement. Contract: `shamt < XLEN`.
#[must_use]
pub fn sar(x: u64, shamt: u64) -> u64 {
    debug_assert!(
        shamt < u64::from(XLEN),
        "sar: unmasked shift amount — a decoder bug"
    );
    ((x as i64) >> shamt) as u64
}

// ── Word operations ──────────────────────────────────────────────────────────────────────
// REQ-D-WSUFFIX (RVI-RV64I §3.1.2, §3.1.2.1, §3.1.2.2): the `*W` instructions ignore the
// upper 32 bits of their inputs, produce a 32-bit signed result, and sign-extend it to
// XLEN — bits XLEN-1 through 31 of the result are equal. Intermediate precision: 32 bits,
// then one truncation (modulo 2^32) and one extension to 64. Overflow within the 32-bit
// operation is ignored.

/// `ADDW`/`ADDIW`: 32-bit wrapping addition, result sign-extended to XLEN.
#[must_use]
pub fn addw(x: u64, y: u64) -> u64 {
    sext(u64::from((x as u32).wrapping_add(y as u32)), 32)
}

/// `SUBW`: 32-bit wrapping subtraction, result sign-extended to XLEN.
#[must_use]
pub fn subw(x: u64, y: u64) -> u64 {
    sext(u64::from((x as u32).wrapping_sub(y as u32)), 32)
}

/// `SLLW`/`SLLIW`: shift the low 32 bits left, zeros shifted in, result sign-extended.
/// Contract: `shamt < 32` (decode enforces REQ-D-SHAMT via [`shamt32`]).
#[must_use]
pub fn shlw(x: u64, shamt: u64) -> u64 {
    debug_assert!(shamt < 32, "shlw: unmasked shift amount — a decoder bug");
    sext(u64::from((x as u32) << shamt), 32)
}

/// `SRLW`/`SRLIW`: logical right shift of the low 32 bits, zeros shifted in,
/// result sign-extended (the extension replicates bit 31 of the *shifted* 32-bit value).
/// Contract: `shamt < 32`.
#[must_use]
pub fn shrw(x: u64, shamt: u64) -> u64 {
    debug_assert!(shamt < 32, "shrw: unmasked shift amount — a decoder bug");
    sext(u64::from((x as u32) >> shamt), 32)
}

/// `SRAW`/`SRAIW`: arithmetic right shift of the low 32 bits as two's-complement,
/// result sign-extended. Contract: `shamt < 32`.
#[must_use]
pub fn sarw(x: u64, shamt: u64) -> u64 {
    debug_assert!(shamt < 32, "sarw: unmasked shift amount — a decoder bug");
    sext(u64::from(((x as u32 as i32) >> shamt) as u32), 32)
}

/// `LUI`/`AUIPC` offset formation: the 32-bit U-immediate placed with the low 12 bits
/// zeroed, sign-extended to XLEN. Width: 32, sign-extended. — REQ-D-LUI-AUIPC
/// (RVI-RV64I §3.1.2.1). (`AUIPC` adds the address of the instruction itself; that
/// composition is instruction-layer.)
#[must_use]
pub fn lui_auipc_offset(imm20: u64) -> u64 {
    sext(imm20 << 12, 32)
}

#[cfg(test)]
mod tests;
