//! Integer multiply and divide — the semantics language's eight M operators
//! (`schema/semantics.sexp`'s multiply/divide block, `P4-SYSTEM.11` slice a), written to
//! SEM-03: every function states its widths, signedness, intermediate precision, truncation
//! and exceptional behaviour in its own contract, independently of host defaults.
//!
//! Each operator works at a WIDTH `w` (1..=64, the wider of its operands' widths in the
//! evaluator): operands are read as their low `w` bits — sign-extended from bit `w - 1` where
//! the operator is signed — and every result is a `w`-bit value, its bits above `w` clear.
//! Target values are held in `u64` regardless of signedness (SEM-03).
//!
//! These are ARITHMETIC ONLY. What an ISA makes division by zero yield is the definition's to
//! state (`definitions/riscv/m.sem.sexp` guards every division, RVI-M §11.1.2 Table 1), so the
//! four division operators return `None` on a zero divisor — outside their domain — and the
//! evaluator refuses that as a definition defect. Signed overflow (the most-negative `w`-bit
//! value ÷ −1) WRAPS, as `add` wraps: quotient the dividend, remainder 0.

#[cfg(test)]
mod tests;

/// The low `w` bits set.
fn mask(w: u32) -> u64 {
    debug_assert!((1..=64).contains(&w), "a width outside 1..=64: {w}");
    if w >= 64 {
        u64::MAX
    } else {
        (1u64 << w) - 1
    }
}

/// `v`'s low `w` bits, sign-extended from bit `w - 1` — the signed view of a `w`-bit value.
fn signed(v: u64, w: u32) -> i64 {
    let shift = 64 - w;
    ((v << shift) as i64) >> shift
}

/// `(mul a b)` — the low `w` bits of a×b. Signedness is irrelevant to the low half; the
/// product wraps modulo 2^w (intermediate precision: 64 bits, then truncated).
pub fn mul(a: u64, b: u64, w: u32) -> u64 {
    a.wrapping_mul(b) & mask(w)
}

/// `(mulh a b)` — the high `w` bits of the 2w-bit product, both operands signed. The
/// product is exact in 128 bits (|a×b| ≤ 2^126); the arithmetic shift floors, which is the
/// two's-complement high half.
pub fn mulh(a: u64, b: u64, w: u32) -> u64 {
    (((signed(a, w) as i128) * (signed(b, w) as i128)) >> w) as u64 & mask(w)
}

/// `(mulhsu a b)` — the high `w` bits of the 2w-bit product, `a` signed and `b` unsigned.
/// Exact in 128 bits (|a| ≤ 2^63, b < 2^64).
pub fn mulhsu(a: u64, b: u64, w: u32) -> u64 {
    (((signed(a, w) as i128) * ((b & mask(w)) as i128)) >> w) as u64 & mask(w)
}

/// `(mulhu a b)` — the high `w` bits of the 2w-bit product, both operands unsigned. Exact
/// in 128 bits.
pub fn mulhu(a: u64, b: u64, w: u32) -> u64 {
    ((((a & mask(w)) as u128) * ((b & mask(w)) as u128)) >> w) as u64 & mask(w)
}

/// `(div a b)` — a÷b signed, truncating toward zero; `None` when b is zero (outside the
/// domain). Overflow wraps: the most-negative `w`-bit value ÷ −1 is that value. At `w` < 64
/// the 64-bit quotient of the sign-extended operands is exact, and truncating it to `w` bits
/// is the `w`-bit wrap.
pub fn div(a: u64, b: u64, w: u32) -> Option<u64> {
    let (x, y) = (signed(a, w), signed(b, w));
    (y != 0).then(|| x.wrapping_div(y) as u64 & mask(w))
}

/// `(divu a b)` — a÷b unsigned, truncating; `None` when b is zero. Unsigned division cannot
/// overflow.
pub fn divu(a: u64, b: u64, w: u32) -> Option<u64> {
    (a & mask(w)).checked_div(b & mask(w))
}

/// `(rem a b)` — the signed remainder of `div`, its sign the dividend's (zero or the
/// dividend's sign); `None` when b is zero. Overflow's remainder is 0.
pub fn rem(a: u64, b: u64, w: u32) -> Option<u64> {
    let (x, y) = (signed(a, w), signed(b, w));
    (y != 0).then(|| x.wrapping_rem(y) as u64 & mask(w))
}

/// `(remu a b)` — the unsigned remainder of `divu`; `None` when b is zero.
pub fn remu(a: u64, b: u64, w: u32) -> Option<u64> {
    (a & mask(w)).checked_rem(b & mask(w))
}
