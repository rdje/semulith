//! The floating-point model layer (`P4-SYSTEM.7` slice (c4)) — the RISC-V target policy over
//! the qualified backend.
//!
//! `rustc_apfloat` (pinned `=0.2.3+llvm-462a31f5a5ab`) was qualified at slice (a) as
//! arithmetic MACHINERY: its add/sub/mul/div/fma values are MPFR-exact in all five rounding
//! modes at both widths (`docs/decisions/decision_fp-backend-qualification.md`). It is not the
//! policy. This module is the one place the RISC-V F/D semantics meet it, so an evaluator arm
//! never calls the backend directly, and every rule below is the pinned specification's:
//!
//! - **The canonical NaN** on every NaN result — "if the result of a floating-point operation
//!   is NaN, it is the canonical NaN" (RVI-F §20.1.3): `0x7fc00000` / `0x7ff8000000000000`.
//!   The backend propagates payloads (LLVM's convention); this layer discards them.
//! - **NaN-boxing** — `fbox`/`funbox` (RVI-D §21.1.2; the tree applies them, this layer
//!   defines them).
//! - **The exception flags**, fflags' NV DZ OF UF NX, with the backend's two measured
//!   LLVM-vs-IEEE deviations patched here: OVERFLOW is IEEE 754-2008 §7.4's magnitude rule —
//!   "the destination format's largest finite number is exceeded in magnitude by what would
//!   have been the rounded floating-point result were the exponent range unbounded" — where
//!   the backend reports only INEXACT for a directed-mode clamp to the largest finite value
//!   (290 measured cases). The unbounded rounding is computed EXACTLY, not estimated: the
//!   same operation in a backend format with the SAME precision and a 15-bit exponent
//!   ([`WideSingleS`], [`WideDoubleS`]) — rounding there is rounding with an unbounded
//!   exponent for every operation on these operands. UNDERFLOW is computed from the same
//!   value: tininess AFTER rounding (RVI-F §20.1.4) is IEEE 754-2008 §7.5's "a non-zero
//!   result computed as though the exponent range were unbounded would lie strictly between
//!   ±b^emin", and the flag is tiny AND inexact. The backend instead judges the DELIVERED
//!   result, so a value that is tiny unbounded but rounds up to the smallest normal raises
//!   no UF there — the second deviation, measured at slice (c4) (2^-126·(1−2^-24) in RNE), which
//!   slice (a)'s MPFR-side rule shared and so could not see; Berkeley SoftFloat's RISC-V
//!   specialization tests tininess the IEEE way (`init_detectTininess` = after rounding).
//!   (The record's other named deviation — no NV for a signaling NaN through a format
//!   conversion — was the MPFR oracle's, not the backend's: measured at slice (d3), the
//!   backend raises it; see [`convert`].)
//! - **The policy surfaces the backend does not own**: a NaN converted to an integer yields
//!   the target's maximum with NV (Table 5 — the backend returns 0); min/max are RVI-F
//!   §20.1.6's minimumNumber/maximumNumber (−0 < +0, both-NaN canonical, one NaN → the other
//!   operand, NV on a signaling input); the compares' quiet/signaling NV split (§20.1.8); the
//!   class mask (§20.1.9); and the FMA ∞×0 rule ("must set the invalid operation exception
//!   flag when the multiplicands are ∞ and zero, even when the addend is a quiet NaN",
//!   §20.1.6) — all computed here, in bits, never trusted to the backend's conventions.
//! - **The square root**, which the backend does not carry (the qualification record's one
//!   named gap): computed here by exact integer square root with a sticky remainder, so the
//!   result is the correctly rounded value in every mode — falsified against MPFR (slice c4's
//!   scratch re-qualification) and spec-derived unit vectors.
//!
//! Subnormals are IEEE (no flush — RVI-F §20.1.4); tininess is detected after rounding,
//! which is the backend's behaviour (measured clean at slice (a)).
//!
//! Formats are passed as their width in bits (`32`, `64`) — the semantics language carries the
//! format as a literal (`schema/semantics.sexp`'s floating-point block); any other width is a
//! description defect and panics, like the evaluator's other vocabulary guards.

use core::cmp::Ordering;
use rustc_apfloat::ieee::{Double, IeeeFloat, Semantics, Single};
use rustc_apfloat::{Float, FloatConvert, Round, Status, StatusAnd};

/// The accrued-exception flags, fflags bits 4..0 (RVI-F §20.1.2, Table 3).
pub const NV: u64 = 0x10;
/// Divide by zero.
pub const DZ: u64 = 0x08;
/// Overflow.
pub const OF: u64 = 0x04;
/// Underflow.
pub const UF: u64 = 0x02;
/// Inexact.
pub const NX: u64 = 0x01;

/// A floating-point result: the value (an n-bit encoding, or an integer for the
/// conversions and compares, zero-extended into 64 bits) and the exception flags it raised.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Flagged {
    /// The result bits.
    pub bits: u64,
    /// The flags to accrue into fflags (`NV | DZ | OF | UF | NX`).
    pub flags: u64,
}

/// An effective rounding mode (RVI-F §20.1.2, Table 2) — never DYN, never reserved: the
/// `(rounding …)` operator resolves those before any arithmetic runs.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Rm {
    /// 000 — round to nearest, ties to even.
    Rne,
    /// 001 — round towards zero.
    Rtz,
    /// 010 — round down (towards −∞).
    Rdn,
    /// 011 — round up (towards +∞).
    Rup,
    /// 100 — round to nearest, ties to max magnitude.
    Rmm,
}

impl Rm {
    /// The effective mode an encoding's 3-bit value names (0..4), or `None` — 101/110 are
    /// reserved and 111 is DYN, never an effective mode.
    #[must_use]
    pub fn from_bits(rm: u64) -> Option<Rm> {
        match rm {
            0 => Some(Rm::Rne),
            1 => Some(Rm::Rtz),
            2 => Some(Rm::Rdn),
            3 => Some(Rm::Rup),
            4 => Some(Rm::Rmm),
            _ => None,
        }
    }

    /// The mode's 3-bit encoding (Table 2) — the inverse of [`Rm::from_bits`]; the value a
    /// `(rounding …)` node yields to the arithmetic that consumes it.
    #[must_use]
    pub fn bits(self) -> u64 {
        match self {
            Rm::Rne => 0,
            Rm::Rtz => 1,
            Rm::Rdn => 2,
            Rm::Rup => 3,
            Rm::Rmm => 4,
        }
    }

    fn round(self) -> Round {
        match self {
            Rm::Rne => Round::NearestTiesToEven,
            Rm::Rtz => Round::TowardZero,
            Rm::Rdn => Round::TowardNegative,
            Rm::Rup => Round::TowardPositive,
            Rm::Rmm => Round::NearestTiesToAway,
        }
    }
}

/// The `(rounding rm)` resolution: the effective mode for an instruction's rm field, with
/// DYN (111) reading `frm`; `None` is a RESERVED rounding mode — static 101/110 or DYN with
/// frm holding 101–111 — which the laboratory takes as illegal-instruction (the pinned
/// revision's "reserved" behavior; its ratified mandate "still valid"; Sail 0.14's
/// `Fcsr_RM_Illegal` — `P4-SYSTEM.7` slice (c1)).
#[must_use]
pub fn resolve_rm(rm_field: u64, frm: u64) -> Option<Rm> {
    match rm_field {
        7 => Rm::from_bits(frm & 0b111),
        other => Rm::from_bits(other),
    }
}

// ---- formats ---------------------------------------------------------------------------------

fn mask(n: u32) -> u64 {
    if n >= 64 {
        u64::MAX
    } else {
        (1u64 << n) - 1
    }
}

fn check_format(n: u32) {
    assert!(
        n == 32 || n == 64,
        "a floating-point format of {n} bits — the semantics language carries 32 or 64 \
         (check_semantics.check_fp); this is a description defect"
    );
}

/// The canonical NaN of the n-bit format (RVI-F §20.1.3; RVI-D's double form).
#[must_use]
pub fn canonical_nan(n: u32) -> u64 {
    check_format(n);
    if n == 32 {
        0x7fc0_0000
    } else {
        0x7ff8_0000_0000_0000
    }
}

/// `(fbox n v)`: v's low n bits NaN-boxed into FLEN = 64 — all 1s above (RVI-D §21.1.2).
#[must_use]
pub fn fbox(n: u32, v: u64) -> u64 {
    check_format(n);
    (v & mask(n)) | !mask(n)
}

/// `(funbox n v)`: the n-bit operand an FLEN value carries — its low n bits when the upper
/// FLEN-n bits are all 1s, else the n-bit canonical NaN (RVI-D §21.1.2).
#[must_use]
pub fn funbox(n: u32, v: u64) -> u64 {
    check_format(n);
    if n == 64 || v | mask(n) == u64::MAX {
        v & mask(n)
    } else {
        canonical_nan(n)
    }
}

/// Single's precision (24 bits) over a 15-bit exponent. No operation on singles can leave
/// its range, so rounding in it IS IEEE 754-2008 §7.4's "rounded … were the exponent range
/// unbounded" — the exact reference for the overflow flag.
pub struct WideSingleS;
impl Semantics for WideSingleS {
    const BITS: usize = 1 + 15 + 23;
    const EXP_BITS: usize = 15;
}
/// Double's precision (53 bits) over a 15-bit exponent — [`WideSingleS`]'s double twin.
pub struct WideDoubleS;
impl Semantics for WideDoubleS {
    const BITS: usize = 1 + 15 + 52;
    const EXP_BITS: usize = 15;
}
type WideSingle = IeeeFloat<WideSingleS>;
type WideDouble = IeeeFloat<WideDoubleS>;

/// Widen exactly: the same precision over a wider exponent loses nothing.
fn widen<F: Float + FloatConvert<W>, W: Float>(x: F) -> W {
    let mut loses = false;
    x.convert_r(Round::NearestTiesToEven, &mut loses).value
}

/// The backend's status as fflags bits — NV, DZ and NX only: OVERFLOW and UNDERFLOW are
/// this layer's (IEEE 754-2008 §7.4/§7.5 over the exactly-unbounded result).
fn status_flags(status: Status) -> u64 {
    let mut flags = 0;
    if status.contains(Status::INVALID_OP) {
        flags |= NV;
    }
    if status.contains(Status::DIV_BY_ZERO) {
        flags |= DZ;
    }
    if status.contains(Status::INEXACT) {
        flags |= NX;
    }
    flags
}

/// The common tail of a rounded arithmetic result: the canonical NaN, the flags, and
/// OVERFLOW and UNDERFLOW by IEEE's rules over the exactly-unbounded result `wide` (absent
/// when an operand was infinite or NaN — a result from infinities or NaNs is exact or NaN,
/// never an overflow or an underflow).
fn finish<F, W>(n: u32, r: StatusAnd<F>, wide: Option<W>) -> Flagged
where
    F: Float + FloatConvert<W>,
    W: Float,
{
    let mut flags = status_flags(r.status);
    if let Some(w) = wide.filter(|w| w.is_finite() && !w.is_zero()) {
        let magnitude = w.abs();
        if magnitude.partial_cmp(&widen::<F, W>(F::largest())) == Some(Ordering::Greater) {
            // IEEE 754-2008 §7.4: overflow; the clamped or infinite result is inexact
            flags |= OF | NX;
        } else if magnitude.partial_cmp(&widen::<F, W>(F::smallest_normalized()))
            == Some(Ordering::Less)
            && flags & NX != 0
        {
            // §7.5 with tininess after rounding (RVI-F §20.1.4): tiny unbounded, and the
            // delivered result inexact — even where it rounds up to the smallest normal
            flags |= UF;
        }
    }
    let bits = if r.value.is_nan() {
        canonical_nan(n)
    } else {
        r.value.to_bits() as u64
    };
    Flagged { bits, flags }
}

macro_rules! by_format {
    ($n:expr, $f:ident($($arg:expr),*)) => {
        match $n {
            32 => $f::<Single, WideSingle>($n, $($arg),*),
            64 => $f::<Double, WideDouble>($n, $($arg),*),
            other => { check_format(other); unreachable!() }
        }
    };
}

#[derive(Clone, Copy)]
enum Binary {
    Add,
    Sub,
    Mul,
    Div,
}

fn binary_op<T: Float>(op: Binary, x: T, y: T, r: Round) -> StatusAnd<T> {
    match op {
        Binary::Add => x.add_r(y, r),
        Binary::Sub => x.sub_r(y, r),
        Binary::Mul => x.mul_r(y, r),
        Binary::Div => x.div_r(y, r),
    }
}

fn binary<F, W>(n: u32, op: Binary, rm: Rm, a: u64, b: u64) -> Flagged
where
    F: Float + FloatConvert<W>,
    W: Float,
{
    let (x, y) = (F::from_bits(u128::from(a)), F::from_bits(u128::from(b)));
    let r = binary_op(op, x, y, rm.round());
    let wide = (x.is_finite() && y.is_finite())
        .then(|| binary_op(op, widen::<F, W>(x), widen::<F, W>(y), rm.round()).value);
    finish(n, r, wide)
}

/// `(fadd n rm a b)` — a+b (RVI-F §20.1.6).
#[must_use]
pub fn add(n: u32, rm: Rm, a: u64, b: u64) -> Flagged {
    by_format!(n, binary(Binary::Add, rm, a, b))
}

/// `(fsub n rm a b)` — a−b.
#[must_use]
pub fn sub(n: u32, rm: Rm, a: u64, b: u64) -> Flagged {
    by_format!(n, binary(Binary::Sub, rm, a, b))
}

/// `(fmul n rm a b)` — a×b.
#[must_use]
pub fn mul(n: u32, rm: Rm, a: u64, b: u64) -> Flagged {
    by_format!(n, binary(Binary::Mul, rm, a, b))
}

/// `(fdiv n rm a b)` — a÷b.
#[must_use]
pub fn div(n: u32, rm: Rm, a: u64, b: u64) -> Flagged {
    by_format!(n, binary(Binary::Div, rm, a, b))
}

fn fused<F, W>(n: u32, rm: Rm, a: u64, b: u64, c: u64) -> Flagged
where
    F: Float + FloatConvert<W>,
    W: Float,
{
    let (x, y, z) = (
        F::from_bits(u128::from(a)),
        F::from_bits(u128::from(b)),
        F::from_bits(u128::from(c)),
    );
    // RVI-F §20.1.6: ∞×0 is invalid "even when the addend is a quiet NaN" — the rule the
    // IEEE standard leaves to the implementation, decided here, never by the backend.
    if (x.is_infinite() && y.is_zero()) || (x.is_zero() && y.is_infinite()) {
        return Flagged {
            bits: canonical_nan(n),
            flags: NV,
        };
    }
    let r = x.mul_add_r(y, z, rm.round());
    let wide = (x.is_finite() && y.is_finite() && z.is_finite()).then(|| {
        widen::<F, W>(x)
            .mul_add_r(widen::<F, W>(y), widen::<F, W>(z), rm.round())
            .value
    });
    finish(n, r, wide)
}

/// `(fmadd n rm a b c)` — (a×b)+c with one rounding (RVI-F §20.1.6).
#[must_use]
pub fn fma(n: u32, rm: Rm, a: u64, b: u64, c: u64) -> Flagged {
    by_format!(n, fused(rm, a, b, c))
}

// ---- the square root (computed here: the backend carries none) -------------------------------

/// Integer square root with remainder: (⌊√v⌋, v − ⌊√v⌋²), the classic digit-by-digit method —
/// exact, no floating point anywhere.
fn isqrt(v: u128) -> (u128, u128) {
    let mut rem = v;
    let mut root = 0u128;
    let mut bit = 1u128 << 126;
    while bit > v {
        bit >>= 2;
    }
    while bit != 0 {
        if rem >= root + bit {
            rem -= root + bit;
            root = (root >> 1) + bit;
        } else {
            root >>= 1;
        }
        bit >>= 2;
    }
    (root, rem)
}

/// `(fsqrt n rm a)` — √a, correctly rounded in every mode (RVI-F §20.1.6; IEEE 754-2008
/// §5.4.1). √−0 = −0; √+∞ = +∞; a negative non-zero operand (−∞ included) is invalid: NV and
/// the canonical NaN; a signaling NaN raises NV; any NaN yields the canonical NaN. A finite
/// positive operand never overflows or underflows (√ of the smallest subnormal is normal), so
/// the only flag is NX.
#[must_use]
pub fn sqrt(n: u32, rm: Rm, a: u64) -> Flagged {
    check_format(n);
    let (p, ebits) = if n == 32 { (24u32, 8u32) } else { (53, 11) };
    let bias = (1i32 << (ebits - 1)) - 1;
    let a = a & mask(n);
    let sign = a >> (n - 1) != 0;
    let exp = ((a >> (p - 1)) & mask(ebits)) as i32;
    let frac = a & mask(p - 1);
    let emax = mask(ebits) as i32;
    if exp == emax {
        return if frac != 0 {
            // a NaN: NV only when signaling (the quiet bit clear)
            let quiet = frac >> (p - 2) & 1 != 0;
            Flagged {
                bits: canonical_nan(n),
                flags: if quiet { 0 } else { NV },
            }
        } else if sign {
            Flagged {
                bits: canonical_nan(n),
                flags: NV,
            }
        } else {
            Flagged { bits: a, flags: 0 }
        };
    }
    if exp == 0 && frac == 0 {
        return Flagged { bits: a, flags: 0 }; // ±0: √−0 = −0
    }
    if sign {
        return Flagged {
            bits: canonical_nan(n),
            flags: NV,
        };
    }
    // a = m × 2^e, m an integer (the hidden bit made explicit; a subnormal's exponent is the
    // minimum normal one)
    let (mut m, mut e) = if exp == 0 {
        (u128::from(frac), 1 - bias - (p as i32 - 1))
    } else {
        (u128::from(frac | 1 << (p - 1)), exp - bias - (p as i32 - 1))
    };
    // Scale m to 2(p+2) bits — or one fewer, so the remaining exponent is EVEN and √(2^e) a
    // power of two — so ⌊√m⌋ carries exactly p+2 bits: p significand bits, a guard bit and a
    // round bit; the remainder is the sticky bit. m has at most p bits, so the shift is
    // always a left shift of at least p+3, and m never exceeds 2p+4 ≤ 110 bits.
    let bits = 128 - m.leading_zeros();
    let mut shift = 2 * (p + 2) - bits;
    if (e - shift as i32) & 1 != 0 {
        shift -= 1;
    }
    m <<= shift;
    e -= shift as i32;
    let (root, rem) = isqrt(m);
    let sticky = rem != 0;
    // root has p+2 bits: [p significand bits][guard][round]
    let mut keep = root >> 2;
    let low = (root & 0b11) as u8;
    let inexact = low != 0 || sticky;
    // the discarded part against half a unit in the last place
    let above_half = low > 2 || (low == 2 && sticky);
    let at_half = low == 2 && !sticky;
    let up = match rm {
        Rm::Rne => above_half || (at_half && keep & 1 == 1),
        Rm::Rmm => low >= 2,
        Rm::Rtz | Rm::Rdn => false, // a positive result: towards zero and down agree
        Rm::Rup => inexact,
    };
    let mut res_e = e / 2 + 2 + (p as i32 - 1);
    if up {
        keep += 1;
        if keep == 1u128 << p {
            keep >>= 1;
            res_e += 1;
        }
    }
    debug_assert_eq!(128 - keep.leading_zeros(), p, "a normalized significand");
    let biased = (res_e + bias) as u64;
    Flagged {
        bits: biased << (p - 1) | (keep as u64 & mask(p - 1)),
        flags: if inexact { NX } else { 0 },
    }
}

// ---- min / max, compares, classify (policy: computed in bits) --------------------------------

fn decode<F: Float>(v: u64) -> F {
    F::from_bits(u128::from(v))
}

fn min_max<F: Float>(n: u32, a: u64, b: u64, want_max: bool) -> Flagged {
    let (x, y): (F, F) = (decode(a), decode(b));
    let flags = if x.is_signaling() || y.is_signaling() {
        NV
    } else {
        0
    };
    let bits = match (x.is_nan(), y.is_nan()) {
        (true, true) => canonical_nan(n),
        (true, false) => b,
        (false, true) => a,
        (false, false) if x.is_zero() && y.is_zero() => {
            // −0.0 < +0.0 "for the purposes of these instructions only" (RVI-F §20.1.6)
            match (want_max, x.is_negative()) {
                (false, true) | (true, false) => a,
                (false, false) | (true, true) => b,
            }
        }
        (false, false) => match (x.partial_cmp(&y), want_max) {
            (Some(Ordering::Less), false) | (Some(Ordering::Greater), true) => a,
            (Some(Ordering::Equal), _) => a,
            _ => b,
        },
    };
    Flagged { bits, flags }
}

/// `(fmin n a b)` — minimumNumber as RVI-F §20.1.6 amends it.
#[must_use]
pub fn min(n: u32, a: u64, b: u64) -> Flagged {
    check_format(n);
    if n == 32 {
        min_max::<Single>(n, a, b, false)
    } else {
        min_max::<Double>(n, a, b, false)
    }
}

/// `(fmax n a b)` — maximumNumber as RVI-F §20.1.6 amends it.
#[must_use]
pub fn max(n: u32, a: u64, b: u64) -> Flagged {
    check_format(n);
    if n == 32 {
        min_max::<Single>(n, a, b, true)
    } else {
        min_max::<Double>(n, a, b, true)
    }
}

/// The three compares of RVI-F §20.1.8.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Compare {
    /// FEQ — quiet: NV only for a signaling NaN.
    Eq,
    /// FLT — signaling: NV for any NaN.
    Lt,
    /// FLE — signaling: NV for any NaN.
    Le,
}

fn compare_in<F: Float>(kind: Compare, a: u64, b: u64) -> Flagged {
    let (x, y): (F, F) = (decode(a), decode(b));
    if x.is_nan() || y.is_nan() {
        let nv = match kind {
            Compare::Eq => x.is_signaling() || y.is_signaling(),
            Compare::Lt | Compare::Le => true,
        };
        return Flagged {
            bits: 0, // "the result is 0 if either operand is NaN"
            flags: if nv { NV } else { 0 },
        };
    }
    let ord = x.partial_cmp(&y).expect("non-NaN operands are ordered");
    let holds = match kind {
        Compare::Eq => ord == Ordering::Equal,
        Compare::Lt => ord == Ordering::Less,
        Compare::Le => ord != Ordering::Greater,
    };
    Flagged {
        bits: u64::from(holds),
        flags: 0,
    }
}

/// `(feq n a b)` / `(flt n a b)` / `(fle n a b)` — 1 if the relation holds, else 0.
#[must_use]
pub fn compare(n: u32, kind: Compare, a: u64, b: u64) -> Flagged {
    check_format(n);
    if n == 32 {
        compare_in::<Single>(kind, a, b)
    } else {
        compare_in::<Double>(kind, a, b)
    }
}

/// `(fclass n a)` — the 10-bit class mask, exactly one bit set (RVI-F §20.1.9, Table 6);
/// computed from the bits, raising no flag.
#[must_use]
pub fn classify(n: u32, a: u64) -> u64 {
    check_format(n);
    let (p, ebits) = if n == 32 { (24u32, 8u32) } else { (53, 11) };
    let a = a & mask(n);
    let negative = a >> (n - 1) != 0;
    let exp = (a >> (p - 1)) & mask(ebits);
    let frac = a & mask(p - 1);
    let bit = if exp == mask(ebits) {
        match (frac == 0, negative) {
            (true, true) => 0,                           // −∞
            (true, false) => 7,                          // +∞
            (false, _) if frac >> (p - 2) & 1 == 0 => 8, // signaling NaN
            (false, _) => 9,                             // quiet NaN
        }
    } else if exp == 0 {
        match (frac == 0, negative) {
            (true, true) => 3,   // −0
            (true, false) => 4,  // +0
            (false, true) => 2,  // negative subnormal
            (false, false) => 5, // positive subnormal
        }
    } else if negative {
        1 // negative normal
    } else {
        6 // positive normal
    };
    1 << bit
}

// ---- conversions ---------------------------------------------------------------------------------

fn to_int_in<F: Float>(iw: u32, signed: bool, rm: Rm, a: u64) -> Flagged {
    let x: F = decode(a);
    let (min, max) = if signed {
        (1u64 << (iw - 1), mask(iw - 1)) // −2^(iw−1) as iw-bit two's complement; 2^(iw−1)−1
    } else {
        (0, mask(iw))
    };
    if x.is_nan() {
        // Table 5: a NaN converts to the maximum, with NV (the backend returns 0)
        return Flagged {
            bits: max,
            flags: NV,
        };
    }
    let mut exact = false;
    let (value, status) = if signed {
        let r = x.to_i128_r(iw as usize, rm.round(), &mut exact);
        (r.value as u64 & mask(iw), r.status)
    } else {
        let r = x.to_u128_r(iw as usize, rm.round(), &mut exact);
        (r.value as u64 & mask(iw), r.status)
    };
    if status.contains(Status::INVALID_OP) {
        // out of range (or ±∞): clipped to the nearest representable value, NV alone —
        // computed here from the sign rather than trusted to the backend's saturation
        return Flagged {
            bits: if x.is_negative() { min } else { max },
            flags: NV,
        };
    }
    Flagged {
        bits: value,
        flags: if status.contains(Status::INEXACT) {
            NX
        } else {
            0
        },
    }
}

/// `(f2i n iw signed rm a)` — the n-bit float a converted to an iw-bit integer (RVI-F
/// §20.1.7, Table 5). The result is the iw-bit two's-complement pattern, zero-extended; the
/// W forms' sign extension to XLEN is the rule's own.
#[must_use]
pub fn to_int(n: u32, iw: u32, signed: bool, rm: Rm, a: u64) -> Flagged {
    check_format(n);
    assert!(
        iw == 32 || iw == 64,
        "an integer width of {iw} bits — 32 or 64"
    );
    if n == 32 {
        to_int_in::<Single>(iw, signed, rm, a)
    } else {
        to_int_in::<Double>(iw, signed, rm, a)
    }
}

fn from_int_in<F: Float>(iw: u32, signed: bool, rm: Rm, v: u64) -> Flagged {
    let v = v & mask(iw);
    let r: StatusAnd<F> = if signed {
        let shift = 128 - iw;
        F::from_i128_r((i128::from(v as i64) << shift) >> shift, rm.round())
    } else {
        F::from_u128_r(u128::from(v), rm.round())
    };
    Flagged {
        bits: r.value.to_bits() as u64,
        flags: if r.status.contains(Status::INEXACT) {
            NX
        } else {
            0
        },
    }
}

/// `(i2f n iw signed rm v)` — v's low iw bits as an integer converted to an n-bit float,
/// rounded (RVI-F §20.1.7). No integer exceeds either format's range, so the only flag is NX.
#[must_use]
pub fn from_int(n: u32, iw: u32, signed: bool, rm: Rm, v: u64) -> Flagged {
    check_format(n);
    assert!(
        iw == 32 || iw == 64,
        "an integer width of {iw} bits — 32 or 64"
    );
    if n == 32 {
        from_int_in::<Single>(iw, signed, rm, v)
    } else {
        from_int_in::<Double>(iw, signed, rm, v)
    }
}

/// `(f2f m n rm a)` — the n-bit float `a` converted to an m-bit float: FCVT.S.D and FCVT.D.S
/// (RVI-D §21.1.5 — "FCVT.S.D rounds according to the RM field; FCVT.D.S will never round").
/// Narrowing rounds through the backend with OVERFLOW and UNDERFLOW judged on the
/// exactly-unbounded result (the same value rounded at the target's precision over a 15-bit
/// exponent), as for every rounded operation; widening is exact. A NaN input yields the
/// canonical NaN ([`finish`]), and a SIGNALING NaN raises NV — the backend's own
/// `INVALID_OP`, measured at slice (d3) in both directions. (The qualification record had
/// named this a backend deviation; its 24 cases were the MPFR oracle's silence — MPFR has no
/// signaling NaN — and the record carries the correction.)
#[must_use]
pub fn convert(m: u32, n: u32, rm: Rm, a: u64) -> Flagged {
    check_format(m);
    check_format(n);
    assert!(
        m != n,
        "a conversion from format {n} to itself is no conversion"
    );
    let mut loses = false;
    if n == 64 {
        let x = Double::from_bits(u128::from(a));
        let r: StatusAnd<Single> = x.convert_r(rm.round(), &mut loses);
        let wide = x
            .is_finite()
            .then(|| FloatConvert::<WideSingle>::convert_r(x, rm.round(), &mut loses).value);
        finish(m, r, wide)
    } else {
        let x = Single::from_bits(u128::from(a & mask(32)));
        let r: StatusAnd<Double> = x.convert_r(rm.round(), &mut loses);
        finish(m, r, None::<WideDouble>)
    }
}

#[cfg(test)]
mod tests;
