#!/usr/bin/env python3
"""gen_fp_vectors.py — emit the model layer's unit-vector table from the spec-side reference
(scripts/specfp.py; P4-SYSTEM.7 slice c4). Each row is a directed case named for the rule it
pins; its expected bits and flags are specfp's — derived from the pinned chapters and IEEE
754-2008, never from an engine. The output is TRACKED and gated (FP-VECTORS): a hand edit of
an expected value is refused as DRIFT.

THE FIXTURES AT SCALE (P4-SYSTEM.7 slice e2): a second, generated table — fp/tests/fixtures.txt,
seeded operands biased toward the classes the rules distinguish (zeros, subnormals, the
exponent edges, infinities, quiet and signaling NaNs, near-cancelling pairs, the integer
conversion edges), across every model-layer operation × format × rounding mode, expected
values from the same reference. The directed vectors are the RULES; the fixtures are the
BREADTH. Plain text, loaded by include_str!, so the table costs rustc nothing.

usage: gen_fp_vectors.py            write vectors.rs AND fixtures.txt
       gen_fp_vectors.py --check    exit 0 iff both tracked tables are the generator's output
       gen_fp_vectors.py --out P    write (or with --check, compare) the vectors at P only
       … --fixtures-out F           also write (or compare) the fixtures at F
"""
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import specfp as S  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "crates/semulith-core/src/fp/tests/vectors.rs"

RM = ["Rm::Rne", "Rm::Rtz", "Rm::Rdn", "Rm::Rup", "Rm::Rmm"]
F_MAX, F_MIN_SUB, F_MIN_NORM = 0x7F7FFFFF, 0x00000001, 0x00800000
ONE, TWO, HALF = 0x3F800000, 0x40000000, 0x3F000000
INF, NINF, QNAN, SNAN, PZ, NZ = 0x7F800000, 0xFF800000, 0x7FC00001, 0x7FA00000, 0, 0x80000000
D_ONE, D_MAX = 0x3FF0000000000000, 0x7FEFFFFFFFFFFFFF

rows = []


def row(op, n, rm, a, b, c, note, fn):
    bits, flags = fn()
    rows.append((op, n, rm, a, b, c, bits, flags, note))


for rm in range(5):
    row("add", 32, rm, ONE, 0x33800000, 0, "1 + 2^-24: the tie (RNE/RMM split), inexact",
        lambda: S.add(32, rm, ONE, 0x33800000))
    row("add", 32, rm, F_MAX, F_MAX, 0, "MAX+MAX: overflow — directed modes clamp WITH OF (the backend's deviation)",
        lambda: S.add(32, rm, F_MAX, F_MAX))
    row("add", 32, rm, 0xFF7FFFFF, 0xFF7FFFFF, 0, "-MAX-MAX: negative overflow per mode",
        lambda: S.add(32, rm, 0xFF7FFFFF, 0xFF7FFFFF))
    row("sub", 32, rm, ONE, ONE, 0, "1-1: the exact-zero sign (−0 only in RDN)",
        lambda: S.sub(32, rm, ONE, ONE))
    row("mul", 32, rm, F_MIN_SUB, HALF, 0, "min-subnormal × 0.5: tiny and inexact — underflow",
        lambda: S.mul(32, rm, F_MIN_SUB, HALF))
    row("mul", 32, rm, F_MIN_NORM, 0x3F7FFFFF, 0, "2^-126·(1−2^-24): tiny after rounding (unbounded), inexact — UF even where it rounds up to the smallest normal",
        lambda: S.mul(32, rm, F_MIN_NORM, 0x3F7FFFFF))
    row("mul", 32, rm, F_MIN_NORM, 0x3F7FFFFE, 0, "2^-126·(1−2^-23): tiny but exact — no UF",
        lambda: S.mul(32, rm, F_MIN_NORM, 0x3F7FFFFE))
    row("div", 32, rm, ONE, 0x40400000, 0, "1/3: inexact per mode",
        lambda: S.div(32, rm, ONE, 0x40400000))
    row("sqrt", 32, rm, TWO, 0, 0, "√2 per mode", lambda: S.sqrt(32, rm, TWO))
    row("sqrt", 32, rm, F_MIN_SUB, 0, 0, "√(min subnormal) = 2^-74.5: a subnormal operand",
        lambda: S.sqrt(32, rm, F_MIN_SUB))
    row("sqrt", 64, rm, 0x4000000000000000, 0, 0, "√2 (double) per mode",
        lambda: S.sqrt(64, rm, 0x4000000000000000))
    row("sqrt", 64, rm, 0x0000000000000003, 0, 0, "√(3 × 2^-1074): an odd subnormal significand",
        lambda: S.sqrt(64, rm, 0x0000000000000003))
    row("fma", 32, rm, 0x3F800001, 0x3F7FFFFE, 0xBF800000, "(1+2^-23)(1-2^-23)-1 = -2^-46: one rounding",
        lambda: S.fma(32, rm, 0x3F800001, 0x3F7FFFFE, 0xBF800000))
    row("fma", 64, rm, D_MAX, 0x4000000000000000, 0xFFEFFFFFFFFFFFFF, "MAX×2-MAX = MAX exactly: no false overflow",
        lambda: S.fma(64, rm, D_MAX, 0x4000000000000000, 0xFFEFFFFFFFFFFFFF))
    row("fma", 64, rm, D_MAX, 0x4000000000000000, 0, "MAX×2+0: overflow per mode (the backend's deviation, fused)",
        lambda: S.fma(64, rm, D_MAX, 0x4000000000000000, 0))

for rm in (0, 1):
    row("add", 32, rm, QNAN, ONE, 0, "a quiet NaN operand: canonical, no flag", lambda: S.add(32, rm, QNAN, ONE))
    row("add", 32, rm, SNAN, ONE, 0, "a signaling NaN operand: canonical, NV", lambda: S.add(32, rm, SNAN, ONE))
    row("add", 32, rm, INF, NINF, 0, "∞-∞: invalid", lambda: S.add(32, rm, INF, NINF))
    row("div", 32, rm, ONE, PZ, 0, "1/+0: +∞, DZ", lambda: S.div(32, rm, ONE, PZ))
    row("div", 32, rm, NZ, PZ, 0, "-0/+0: invalid", lambda: S.div(32, rm, NZ, PZ))
    row("fma", 32, rm, INF, PZ, QNAN, "∞×0+qNaN: NV even with a quiet addend (RVI-F §20.1.6)",
        lambda: S.fma(32, rm, INF, PZ, QNAN))
    row("sqrt", 32, rm, 0xBF800000, 0, 0, "√-1: invalid", lambda: S.sqrt(32, rm, 0xBF800000))
    row("sqrt", 32, rm, NZ, 0, 0, "√-0 = -0", lambda: S.sqrt(32, rm, NZ))
    row("sqrt", 32, rm, 0x40800000, 0, 0, "√4 = 2 exactly", lambda: S.sqrt(32, rm, 0x40800000))
    row("sqrt", 32, rm, SNAN, 0, 0, "√sNaN: canonical, NV", lambda: S.sqrt(32, rm, SNAN))
    row("sqrt", 32, rm, INF, 0, 0, "√+∞ = +∞", lambda: S.sqrt(32, rm, INF))

for a, b, note in ((PZ, NZ, "+0 vs -0"), (NZ, PZ, "-0 vs +0"), (QNAN, ONE, "one quiet NaN"),
                   (ONE, SNAN, "a signaling NaN: NV, the other operand"), (QNAN, SNAN, "two NaNs: canonical"),
                   (ONE, TWO, "ordered")):
    row("min", 32, 0, a, b, 0, f"fmin {note}", lambda: S.min_max(32, a, b, False))
    row("max", 32, 0, a, b, 0, f"fmax {note}", lambda: S.min_max(32, a, b, True))
for a, b, note in ((ONE, ONE, "equal"), (PZ, NZ, "+0 = -0"), (ONE, TWO, "less"),
                   (QNAN, ONE, "quiet NaN"), (SNAN, ONE, "signaling NaN")):
    for k in ("eq", "lt", "le"):
        row(f"f{k}", 32, 0, a, b, 0, f"{k} {note}", lambda: S.compare(32, k, a, b))
for v in (NINF, 0xBF800000, 0x80000001, NZ, PZ, 0x00000001, ONE, INF, SNAN, QNAN):
    row("class", 32, 0, v, 0, 0, "fclass", lambda: (S.classify(32, v), 0))

for rm in range(5):
    row("f2i32", 32, rm, 0x40200000, 0, 0, "2.5 → int per mode", lambda: S.to_int(32, 32, True, rm, 0x40200000))
    row("f2i32", 32, rm, 0xC0200000, 0, 0, "-2.5 → int per mode", lambda: S.to_int(32, 32, True, rm, 0xC0200000))
    row("f2u32", 32, rm, 0xBF000000, 0, 0, "-0.5 → unsigned: 0 or clipped per mode",
        lambda: S.to_int(32, 32, False, rm, 0xBF000000))
    row("i2f32", 32, rm, 0x01000001, 0, 0, "2^24+1 → single per mode", lambda: S.from_int(32, 32, True, rm, 0x01000001))
    row("i2f64", 32, rm, 0xFFFFFFFFFFFFFFFF, 0, 0, "-1 (64-bit) → single", lambda: S.from_int(32, 64, True, rm, 0xFFFFFFFFFFFFFFFF))
    row("u2f64", 32, rm, 0xFFFFFFFFFFFFFFFF, 0, 0, "2^64-1 unsigned → single per mode",
        lambda: S.from_int(32, 64, False, rm, 0xFFFFFFFFFFFFFFFF))
for a, note in ((QNAN, "NaN → the maximum, NV (Table 5)"), (INF, "+∞ → the maximum"), (NINF, "-∞ → the minimum"),
                (0x4F000000, "2^31 → clipped"), (0xCF000000, "-2^31 fits exactly"), (0xCF000001, "below -2^31 → clipped")):
    row("f2i32", 32, 0, a, 0, 0, note, lambda: S.to_int(32, 32, True, 0, a))
    row("f2u64", 32, 0, a, 0, 0, note, lambda: S.to_int(32, 64, False, 0, a))

# P4-SYSTEM.7 slice (d3): the format conversions (row n = the TARGET format; the source is the
# other one). Narrowing rounds with IEEE's OF/UF on the unbounded value; widening is exact; a
# signaling NaN raises NV — the backend's deviation (ii), which fp.rs patches.
D_THIRD, D_TINY_UP, D_TIE_EVEN, D_TIE_UP = 0x3FD5555555555555, 0x380FFFFFE0000000, 0x3FF0000010000000, 0x3FF0000030000000
D_SNAN, D_QNAN = 0x7FF4000000000000, 0x7FF8000000000001
for rm in range(5):
    row("f2f", 32, rm, D_THIRD, 0, 0, "1/3 double → single per mode, inexact",
        lambda: S.convert(32, 64, rm, D_THIRD))
    row("f2f", 32, rm, D_MAX, 0, 0, "double MAX → single: overflow per mode (directed modes clamp WITH OF)",
        lambda: S.convert(32, 64, rm, D_MAX))
    row("f2f", 32, rm, 0xFFEFFFFFFFFFFFFF, 0, 0, "double -MAX → single: negative overflow per mode",
        lambda: S.convert(32, 64, rm, 0xFFEFFFFFFFFFFFFF))
    row("f2f", 32, rm, D_TINY_UP, 0, 0, "2^-126·(1−2^-24) → single: tiny unbounded, inexact — UF even where it rounds up to the smallest normal",
        lambda: S.convert(32, 64, rm, D_TINY_UP))
    row("f2f", 32, rm, 0x1, 0, 0, "double min subnormal → single: underflow to 0 or the min subnormal per mode",
        lambda: S.convert(32, 64, rm, 0x1))
    row("f2f", 32, rm, D_TIE_EVEN, 0, 0, "1 + 2^-24 → single: a tie (RNE to even 1.0, RMM away)",
        lambda: S.convert(32, 64, rm, D_TIE_EVEN))
    row("f2f", 32, rm, D_TIE_UP, 0, 0, "1 + 3·2^-24 → single: a tie whose even neighbour is above",
        lambda: S.convert(32, 64, rm, D_TIE_UP))
for a, note in ((D_SNAN, "double sNaN → single: canonical, NV (the backend's deviation (ii))"),
                (D_QNAN, "double qNaN with a payload → single: canonical, no flag"),
                (0x8000000000000000, "double -0 → single -0"), (0xFFF0000000000000, "double -∞ → single -∞"),
                (D_ONE, "double 1.0 → single 1.0 exactly")):
    row("f2f", 32, 0, a, 0, 0, note, lambda: S.convert(32, 64, 0, a))
for a, note in ((SNAN, "single sNaN → double: canonical, NV (the backend's deviation (ii))"),
                (QNAN, "single qNaN → double: canonical, no flag"),
                (F_MIN_SUB, "single min subnormal → double: exact (a normal double)"),
                (F_MAX, "single MAX → double: exact"), (NZ, "single -0 → double -0"),
                (NINF, "single -∞ → double -∞"), (0x3EAAAAAB, "single ≈1/3 → double: exact, no NX")):
    for rm in (0, 1):
        row("f2f", 64, rm, a, 0, 0, note, lambda: S.convert(64, 32, rm, a))

FIX_OUT = OUT.parent / "fixtures.txt"
FIX_SEED = 20261006
FIX_PER_ROUNDED = 16      # cases per (operation, format, rounding mode)
FIX_PER_UNROUNDED = 64    # cases per (operation, format) for the mode-free operations


def fx_float(rnd, n):
    """One operand: a quarter uniform bit patterns; the rest a random sign, an exponent from
    the edges (0 — zeros and subnormals —, 1, the bias neighbourhood, max-1, max — infinities
    and NaNs, quiet and signaling) or uniform, and an edge or random significand."""
    p, eb, bias, emin, emax = S.params(n)
    if rnd.random() < 0.25:
        return rnd.getrandbits(n)
    sign = rnd.getrandbits(1)
    e_max = (1 << eb) - 1
    e = rnd.choice([0, 0, 1, 2, bias - 1, bias, bias + 1, e_max - 1, e_max, e_max,
                    rnd.randrange(1, e_max)])
    m_bits = p - 1
    m = rnd.choice([0, 1, (1 << m_bits) - 1, 1 << (m_bits - 1), (1 << (m_bits - 1)) | 1,
                    rnd.getrandbits(m_bits), rnd.getrandbits(m_bits)])
    return (sign << (n - 1)) | (e << m_bits) | m


def fx_int(rnd):
    """A 64-bit integer operand, biased to the conversion edges (0, ±1, 2^31, 2^32, 2^53,
    2^63, 2^64 and their neighbours) or uniform."""
    if rnd.random() < 0.4:
        return rnd.getrandbits(64)
    base = rnd.choice([0, 1 << 31, 1 << 32, 1 << 53, 1 << 63, (1 << 64) - 1, 1 << 24])
    return (base + rnd.choice([-2, -1, 0, 1, 2])) & ((1 << 64) - 1)


fixtures = []


def fixture_rows():
    rnd = __import__("random").Random(FIX_SEED)
    for n in (32, 64):
        for rm in range(5):
            for op in ("add", "sub", "mul", "div"):
                for _ in range(FIX_PER_ROUNDED):
                    a, b = fx_float(rnd, n), fx_float(rnd, n)
                    if op == "sub" and rnd.random() < 0.3:
                        b = a ^ rnd.getrandbits(3)          # near-cancellation
                    fixtures.append((op, n, rm, a, b, 0, *getattr(S, op)(n, rm, a, b)))
            for _ in range(FIX_PER_ROUNDED):
                a, b, c = (fx_float(rnd, n) for _ in range(3))
                fixtures.append(("fma", n, rm, a, b, c, *S.fma(n, rm, a, b, c)))
                a = fx_float(rnd, n)
                fixtures.append(("sqrt", n, rm, a, 0, 0, *S.sqrt(n, rm, a)))
            for name, iw, signed in (("f2i32", 32, True), ("f2u32", 32, False),
                                     ("f2i64", 64, True), ("f2u64", 64, False)):
                for _ in range(FIX_PER_ROUNDED):
                    a = fx_float(rnd, n)
                    fixtures.append((name, n, rm, a, 0, 0, *S.to_int(n, iw, signed, rm, a)))
            for name, iw, signed in (("i2f32", 32, True), ("u2f32", 32, False),
                                     ("i2f64", 64, True), ("u2f64", 64, False)):
                for _ in range(FIX_PER_ROUNDED):
                    v = fx_int(rnd)
                    fixtures.append((name, n, rm, v, 0, 0, *S.from_int(n, iw, signed, rm, v)))
            for _ in range(FIX_PER_ROUNDED):
                a = fx_float(rnd, 96 - n)
                fixtures.append(("f2f", n, rm, a, 0, 0, *S.convert(n, 96 - n, rm, a)))
        for _ in range(FIX_PER_UNROUNDED):
            a, b = fx_float(rnd, n), fx_float(rnd, n)
            fixtures.append(("min", n, 0, a, b, 0, *S.min_max(n, a, b, False)))
            fixtures.append(("max", n, 0, a, b, 0, *S.min_max(n, a, b, True)))
            for k in ("eq", "lt", "le"):
                fixtures.append((f"f{k}", n, 0, a, b, 0, *S.compare(n, k, a, b)))
            fixtures.append(("class", n, 0, a, 0, 0, S.classify(n, a), 0))


def emit_fixtures() -> str:
    """The fixtures, as the bytes the tracked file must hold: one case per line,
    `op n rm a b c bits flags` (hex without 0x; rm 0..4 — RNE RTZ RDN RUP RMM)."""
    if not fixtures:
        fixture_rows()
    lines = ["# GENERATED by scripts/gen_fp_vectors.py (the fixtures at scale, P4-SYSTEM.7 slice e2)",
             "# from the spec-side exact-rational reference scripts/specfp.py — neither SoftFloat,",
             "# APFloat nor MPFR. Do not edit; regenerate. Gated by FP-VECTORS.",
             f"# seed {FIX_SEED}; {len(fixtures)} cases; op n rm a b c bits flags"]
    for op, n, rm, a, b, c, bits, flags in fixtures:
        lines.append(f"{op} {n} {rm} {a:x} {b:x} {c:x} {bits & ((1 << 64) - 1):x} {flags:x}")
    return "\n".join(lines) + "\n"

def emit() -> str:
    """The table, as the bytes the tracked file must hold."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        print("// GENERATED by scripts/gen_fp_vectors.py from the spec-side exact-rational reference")
        print("// (scripts/specfp.py — fractions/decimal; neither SoftFloat, APFloat nor MPFR). Do not edit;")
        print("// regenerate. Gated by FP-VECTORS (scripts/check_fp_vectors.sh).")
        print("use crate::fp::Rm;\n")
        print("/// One spec-side vector: the operation, the format, the rounding mode, the operands,")
        print("/// the expected result bits and flags, and the rule the row pins.")
        print("pub(super) struct Vector {")
        for f, ty in (("op", "&'static str"), ("n", "u32"), ("rm", "Rm"), ("a", "u64"),
                      ("b", "u64"), ("c", "u64"), ("bits", "u64"), ("flags", "u64"),
                      ("note", "&'static str")):
            print(f"    pub(super) {f}: {ty},")
        print("}\n")
        print("#[rustfmt::skip]")
        print("pub(super) const VECTORS: &[Vector] = &[")
        for op, n, rm, a, b, c, bits, flags, note in rows:
            print(f'    Vector {{ op: "{op}", n: {n}, rm: {RM[rm]}, a: {a:#x}, b: {b:#x}, '
                  f'c: {c:#x}, bits: {bits:#x}, flags: {flags:#x}, note: "{note}" }},')
        print("];")
    return buf.getvalue()


def main(argv: list[str]) -> int:
    out = OUT
    fix_out = FIX_OUT
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1])
        fix_out = None      # a redirected vector table never touches the tracked fixtures
    if "--fixtures-out" in argv:
        fix_out = Path(argv[argv.index("--fixtures-out") + 1])
    pairs = [(out, emit())]
    if fix_out is not None:
        pairs.append((fix_out, emit_fixtures()))
    if "--check" in argv:
        bad = 0
        for path, text in pairs:
            have = path.read_text() if path.exists() else ""
            if have != text:
                print(f"gen_fp_vectors: DRIFT — {path} is not the generator's output; regenerate, "
                      f"never edit: python3 scripts/gen_fp_vectors.py", file=sys.stderr)
                bad = 1
        return bad
    for path, text in pairs:
        path.write_text(text)
    print(f"gen_fp_vectors: wrote {out} ({len(rows)} vectors)"
          + (f" and {fix_out} ({len(fixtures)} fixtures)" if fix_out is not None else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
