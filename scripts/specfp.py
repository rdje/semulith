#!/usr/bin/env python3
"""specfp.py — a SPEC-SIDE IEEE 754-2008 binary32/binary64 reference in exact rational
arithmetic (P4-SYSTEM.7 slice c4): the authoring model for the model layer's unit vectors
(scripts/gen_fp_vectors.py → crates/semulith-core/src/fp/tests/vectors.rs, gated by
FP-VECTORS) and, from slice c5, the F corpus's expected values (EVD-05).

Measured before it was trusted: 0 disagreements with the host's hardware IEEE (RNE) on 3,000
random binary64 add/mul/div/sqrt cases, and 0 with the model layer across the 63,480-case
slice-(a) corpus (P4-SYSTEM.7 slice c4) — while its OF/UF rules are §7.4/§7.5's as quoted,
which the slice-(a) MPFR oracle's were not (the leaf's record).

Lineage: Python's fractions.Fraction (exact rationals) and decimal (libmpdec, for √ only) —
neither SoftFloat, nor LLVM APFloat, nor MPFR. Every rule below is written from the pinned
chapters and IEEE 754-2008, never from an engine run:
  - rounding: the five RISC-V modes (RVI-F §20.1.2, Table 2) applied to the EXACT value;
  - overflow: §7.4 — the unbounded-exponent rounded result exceeds the largest finite;
  - underflow: tininess AFTER rounding (RVI-F §20.1.4) and inexact (§7.5's default);
  - NaN results: the canonical NaN (RVI-F §20.1.3); NV on signaling inputs and the genuine
    invalids; the FMA ∞×0 rule (RVI-F §20.1.6); min/max/compare/class per §20.1.6–§20.1.9;
    float→int clipping per Table 5 (NV alone; NX otherwise when inexact).
"""
from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction

NV, DZ, OF, UF, NX = 0x10, 0x08, 0x04, 0x02, 0x01
RNE, RTZ, RDN, RUP, RMM = range(5)

FMT = {32: (24, 8), 64: (53, 11)}  # (precision p, exponent bits)


def params(n):
    p, eb = FMT[n]
    bias = (1 << (eb - 1)) - 1
    emin = 1 - bias
    emax = bias
    return p, eb, bias, emin, emax


def canonical(n):
    return 0x7FC00000 if n == 32 else 0x7FF8000000000000


class Val:
    """A decoded operand: kind in {'zero','finite','inf','qnan','snan'}, sign, exact q."""

    def __init__(self, n, bits):
        p, eb, bias, emin, emax = params(n)
        bits &= (1 << n) - 1
        self.sign = bits >> (n - 1)
        e = (bits >> (p - 1)) & ((1 << eb) - 1)
        f = bits & ((1 << (p - 1)) - 1)
        if e == (1 << eb) - 1:
            if f == 0:
                self.kind = "inf"
            else:
                self.kind = "qnan" if f >> (p - 2) & 1 else "snan"
            self.q = None
        elif e == 0 and f == 0:
            self.kind, self.q = "zero", Fraction(0)
        else:
            self.kind = "finite"
            m = f if e == 0 else f | (1 << (p - 1))
            ex = (emin if e == 0 else e - bias) - (p - 1)
            self.q = Fraction(m) * (Fraction(2) ** ex)
            if self.sign:
                self.q = -self.q

    @property
    def nan(self):
        return self.kind in ("qnan", "snan")


def round_int(x: Fraction, mode, negative):
    """Round a non-negative rational to an integer magnitude under `mode` for a value whose
    sign is `negative` (directed modes depend on the sign)."""
    fl = x.numerator // x.denominator
    frac = x - fl
    if frac == 0:
        return fl
    half = Fraction(1, 2)
    if mode == RNE:
        return fl + 1 if frac > half or (frac == half and fl % 2 == 1) else fl
    if mode == RMM:
        return fl + 1 if frac >= half else fl
    if mode == RTZ:
        return fl
    if mode == RDN:
        return fl + 1 if negative else fl
    if mode == RUP:
        return fl if negative else fl + 1
    raise ValueError(mode)


def encode(n, sign, e_biased, frac):
    p, eb, *_ = params(n)
    return (sign << (n - 1)) | (e_biased << (p - 1)) | frac


def largest(n, sign):
    p, eb, *_ = params(n)
    return encode(n, sign, (1 << eb) - 2, (1 << (p - 1)) - 1)


def inf(n, sign):
    p, eb, *_ = params(n)
    return encode(n, sign, (1 << eb) - 1, 0)


def round_rational(n, q: Fraction, mode, zero_sign=0):
    """The IEEE rounding of the exact value q into format n: (bits, flags)."""
    p, eb, bias, emin, emax = params(n)
    if q == 0:
        return encode(n, zero_sign, 0, 0), 0
    sign = 1 if q < 0 else 0
    a = -q if sign else q
    # E: 2^E <= a < 2^(E+1)
    E = a.numerator.bit_length() - a.denominator.bit_length()
    if Fraction(2) ** E > a:
        E -= 1
    while Fraction(2) ** (E + 1) <= a:
        E += 1
    # the unbounded-exponent rounding (for overflow and tininess-after-rounding)
    r = round_int(a / Fraction(2) ** (E - (p - 1)), mode, sign)
    Eu = E
    if r == 1 << p:
        r, Eu = 1 << (p - 1), E + 1
    U = Fraction(r) * Fraction(2) ** (Eu - (p - 1))
    max_finite = Fraction((1 << p) - 1) * Fraction(2) ** (emax - (p - 1))
    if U > max_finite:
        overflow_to_inf = {RNE: True, RMM: True, RTZ: False,
                           RDN: sign == 1, RUP: sign == 0}[mode]
        return (inf(n, sign) if overflow_to_inf else largest(n, sign)), OF | NX
    tiny = U < Fraction(2) ** emin
    # the bounded rounding: the subnormal quantum below emin
    if E < emin:
        quantum = Fraction(2) ** (emin - (p - 1))
        r2 = round_int(a / quantum, mode, sign)
        value = Fraction(r2) * quantum
        inexact = value != a
        if r2 >= 1 << (p - 1):   # rounded up into the smallest normal
            bits = encode(n, sign, 1, r2 - (1 << (p - 1)))
        else:
            bits = encode(n, sign, 0, r2)
        flags = (NX if inexact else 0) | (UF if (tiny and inexact) else 0)
        return bits, flags
    value = U
    inexact = value != a
    bits = encode(n, sign, Eu + bias, r - (1 << (p - 1)))
    return bits, (NX if inexact else 0)


def nan_result(n, *vals):
    flags = NV if any(v.kind == "snan" for v in vals) else 0
    return canonical(n), flags


def zero_sum_sign(mode, sa, sb):
    """IEEE §6.3: an exact zero sum of opposite-signed operands is +0, except RDN → −0; a
    sum of like-signed zeros keeps the sign."""
    if sa == sb:
        return sa
    return 1 if mode == RDN else 0


def add(n, mode, a, b, negate_b=False):
    x, y = Val(n, a), Val(n, b)
    if negate_b and not y.nan:
        y.sign ^= 1
        if y.q is not None:
            y.q = -y.q
    if x.nan or y.nan:
        return nan_result(n, x, y)
    if x.kind == "inf" or y.kind == "inf":
        if x.kind == "inf" and y.kind == "inf" and x.sign != y.sign:
            return canonical(n), NV
        s = x.sign if x.kind == "inf" else y.sign
        return inf(n, s), 0
    q = x.q + y.q
    if q == 0:
        if x.kind == "zero" and y.kind == "zero":
            return round_rational(n, q, mode, zero_sum_sign(mode, x.sign, y.sign))
        return round_rational(n, q, mode, 1 if mode == RDN else 0)
    return round_rational(n, q, mode)


def sub(n, mode, a, b):
    return add(n, mode, a, b, negate_b=True)


def mul(n, mode, a, b):
    x, y = Val(n, a), Val(n, b)
    if x.nan or y.nan:
        return nan_result(n, x, y)
    s = x.sign ^ y.sign
    if x.kind == "inf" or y.kind == "inf":
        if x.kind == "zero" or y.kind == "zero":
            return canonical(n), NV
        return inf(n, s), 0
    return round_rational(n, x.q * y.q, mode, s)


def div(n, mode, a, b):
    x, y = Val(n, a), Val(n, b)
    if x.nan or y.nan:
        return nan_result(n, x, y)
    s = x.sign ^ y.sign
    if x.kind == "inf":
        if y.kind == "inf":
            return canonical(n), NV
        return inf(n, s), 0
    if y.kind == "inf":
        return round_rational(n, Fraction(0), mode, s)
    if y.kind == "zero":
        if x.kind == "zero":
            return canonical(n), NV
        return inf(n, s), DZ
    return round_rational(n, x.q / y.q, mode, s)


def fma(n, mode, a, b, c, negate_product=False, negate_addend=False):
    """(±(a×b)) + (±c) with ONE rounding — the four fused forms as the chapter states them
    (RVI-F §20.1.6): FMADD (rs1×rs2)+rs3; FMSUB (rs1×rs2)−rs3; FNMSUB −(rs1×rs2)+rs3;
    FNMADD −(rs1×rs2)−rs3 — computed from the exact signed terms, never by flipping a
    register's sign bit (the model's method; this reference is the spec's)."""
    x, y, z = Val(n, a), Val(n, b), Val(n, c)
    # RVI-F §20.1.6: ∞×0 is invalid even with a quiet-NaN addend
    if (x.kind == "inf" and y.kind == "zero") or (x.kind == "zero" and y.kind == "inf"):
        return canonical(n), NV
    if x.nan or y.nan or z.nan:
        return nan_result(n, x, y, z)
    ps = x.sign ^ y.sign ^ int(negate_product)
    zs = z.sign ^ int(negate_addend)
    if x.kind == "inf" or y.kind == "inf":
        if z.kind == "inf" and zs != ps:
            return canonical(n), NV
        return inf(n, ps), 0
    if z.kind == "inf":
        return inf(n, zs), 0
    prod = -(x.q * y.q) if negate_product else x.q * y.q
    add_q = -z.q if negate_addend else z.q
    q = prod + add_q
    if q == 0:
        product_zero = x.kind == "zero" or y.kind == "zero"
        if product_zero and z.kind == "zero":
            return round_rational(n, q, mode, zero_sum_sign(mode, ps, zs))
        return round_rational(n, q, mode, 1 if mode == RDN else 0)
    return round_rational(n, q, mode)


def sqrt(n, mode, a):
    x = Val(n, a)
    if x.nan:
        return nan_result(n, x)
    if x.kind == "zero":
        return a & ((1 << n) - 1), 0
    if x.sign:
        return canonical(n), NV
    if x.kind == "inf":
        return a & ((1 << n) - 1), 0
    q = x.q
    num, den = q.numerator, q.denominator
    # exact when q is a perfect square of a rational
    import math
    rn, rd = math.isqrt(num), math.isqrt(den)
    if rn * rn == num and rd * rd == den:
        return round_rational(n, Fraction(rn, rd), mode)
    getcontext().prec = 400
    root = (Decimal(num) / Decimal(den)).sqrt()
    return round_rational(n, Fraction(root), mode)


def min_max(n, a, b, want_max):
    x, y = Val(n, a), Val(n, b)
    flags = NV if (x.kind == "snan" or y.kind == "snan") else 0
    mask = (1 << n) - 1
    if x.nan and y.nan:
        return canonical(n), flags
    if x.nan:
        return b & mask, flags
    if y.nan:
        return a & mask, flags
    def key(v):  # −0 < +0 for these instructions only
        if v.kind == "inf":
            return (Fraction(-1) if v.sign else Fraction(1)) * 10**4000, 0
        return v.q, (-1 if v.sign else 1) if v.kind == "zero" else 0
    kx, ky = key(x), key(y)
    pick_a = (kx >= ky) if want_max else (kx <= ky)
    return (a if pick_a else b) & mask, flags


def compare(n, kind, a, b):
    x, y = Val(n, a), Val(n, b)
    if x.nan or y.nan:
        signaling = x.kind == "snan" or y.kind == "snan"
        nv = signaling if kind == "eq" else True
        return 0, NV if nv else 0
    def num(v):
        if v.kind == "inf":
            return Fraction(-1 if v.sign else 1) * 10**4000
        return v.q
    qx, qy = num(x), num(y)
    holds = {"eq": qx == qy, "lt": qx < qy, "le": qx <= qy}[kind]
    return int(holds), 0


def classify(n, a):
    x = Val(n, a)
    if x.kind == "inf":
        return 1 << (0 if x.sign else 7)
    if x.kind == "snan":
        return 1 << 8
    if x.kind == "qnan":
        return 1 << 9
    if x.kind == "zero":
        return 1 << (3 if x.sign else 4)
    p, eb, bias, emin, emax = params(n)
    subnormal = abs(x.q) < Fraction(2) ** emin
    if x.sign:
        return 1 << (2 if subnormal else 1)
    return 1 << (5 if subnormal else 6)


def to_int(n, iw, signed, mode, a):
    x = Val(n, a)
    lo, hi = (-(1 << (iw - 1)), (1 << (iw - 1)) - 1) if signed else (0, (1 << iw) - 1)
    mask = (1 << iw) - 1
    if x.nan:
        return hi & mask, NV
    if x.kind == "inf":
        return (lo if x.sign else hi) & mask, NV
    q = x.q
    neg = q < 0
    r = round_int(-q if neg else q, mode, neg)
    v = -r if neg else r
    if v < lo or v > hi:
        return (lo if neg else hi) & mask, NV
    return v & mask, (NX if Fraction(v) != q else 0)


def from_int(n, iw, signed, mode, v):
    v &= (1 << iw) - 1
    if signed and v >> (iw - 1):
        v -= 1 << iw
    return round_rational(n, Fraction(v), mode)


def convert(m, n, mode, a):
    """FCVT.S.D / FCVT.D.S (RVI-D §21.1.5): the n-bit float a as an m-bit float. A NaN →
    the canonical NaN, NV iff signaling; ±∞ and ±0 keep their sign; a finite value is the
    exact rational re-rounded in format m (narrowing rounds by mode with IEEE's OF/UF;
    widening is exact — every single is a double)."""
    x = Val(n, a)
    if x.nan:
        return nan_result(m, x)
    if x.kind == "inf":
        return inf(m, x.sign), 0
    if x.kind == "zero":
        return round_rational(m, Fraction(0), mode, x.sign)
    return round_rational(m, x.q, mode)

def fbits(x):
    import struct
    return struct.unpack("<I", struct.pack("<f", x))[0]


def dbits(x):
    import struct
    return struct.unpack("<Q", struct.pack("<d", x))[0]
