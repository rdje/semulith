//! The model layer's unit proof (`P4-SYSTEM.7` slice (c4)): every expected value below is
//! SPEC-SIDE — the generated table (`vectors.rs`) comes from an exact-rational IEEE reference
//! written from the pinned chapters (fractions/decimal: neither SoftFloat, nor the backend,
//! nor MPFR), and the hand rows cite their sentence. The backend's agreement with MPFR is the
//! qualification record's; this proves the POLICY layered over it.

use super::*;

mod vectors;
use vectors::VECTORS;

fn run(op: &str, n: u32, rm: Rm, a: u64, b: u64, c: u64) -> Flagged {
    match op {
        "add" => add(n, rm, a, b),
        "sub" => sub(n, rm, a, b),
        "mul" => mul(n, rm, a, b),
        "div" => div(n, rm, a, b),
        "fma" => fma(n, rm, a, b, c),
        "sqrt" => sqrt(n, rm, a),
        "min" => min(n, a, b),
        "max" => max(n, a, b),
        "feq" => compare(n, Compare::Eq, a, b),
        "flt" => compare(n, Compare::Lt, a, b),
        "fle" => compare(n, Compare::Le, a, b),
        "class" => Flagged {
            bits: classify(n, a),
            flags: 0,
        },
        "f2i32" => to_int(n, 32, true, rm, a),
        "f2u32" => to_int(n, 32, false, rm, a),
        "f2i64" => to_int(n, 64, true, rm, a),
        "f2u64" => to_int(n, 64, false, rm, a),
        "i2f32" => from_int(n, 32, true, rm, a),
        "u2f32" => from_int(n, 32, false, rm, a),
        "i2f64" => from_int(n, 64, true, rm, a),
        "u2f64" => from_int(n, 64, false, rm, a),
        "f2f" => convert(n, if n == 32 { 64 } else { 32 }, rm, a),
        other => panic!("a vector names an operation this test does not drive: {other}"),
    }
}

#[test]
fn every_spec_side_vector_holds() {
    let mut failures = Vec::new();
    for v in VECTORS {
        let (op, n, rm, a, b, c) = (v.op, v.n, v.rm, v.a, v.b, v.c);
        let (bits, flags, note) = (v.bits, v.flags, v.note);
        let got = run(op, n, rm, a, b, c);
        if got != (Flagged { bits, flags }) {
            failures.push(format!(
                "{op} f{n} {rm:?} a={a:#x} b={b:#x} c={c:#x}: got bits {:#x} flags {:#x}, \
                 the specification gives {bits:#x} / {flags:#x} — {note}",
                got.bits, got.flags
            ));
        }
    }
    assert!(
        failures.is_empty(),
        "{} of {} vectors:\n{}",
        failures.len(),
        VECTORS.len(),
        failures.join("\n")
    );
}

/// The fixtures AT SCALE (`P4-SYSTEM.7` slice (e2)): the same reference over seeded operands
/// biased toward the classes the rules distinguish, every operation × format × mode — the
/// directed vectors are the rules, these are the breadth. `op n rm a b c bits flags`, hex.
#[test]
fn every_spec_side_fixture_holds() {
    let text = include_str!("tests/fixtures.txt");
    let hex = |s: &str| u64::from_str_radix(s, 16).expect("a hex field");
    let (mut cases, mut failures) = (0usize, Vec::new());
    for line in text
        .lines()
        .filter(|l| !l.starts_with('#') && !l.is_empty())
    {
        let f: Vec<&str> = line.split(' ').collect();
        assert_eq!(f.len(), 8, "a fixture row has 8 fields: {line}");
        let (op, n) = (f[0], f[1].parse::<u32>().expect("a format"));
        let rm = Rm::from_bits(hex(f[2])).expect("a legal rounding mode");
        let want = Flagged {
            bits: hex(f[6]),
            flags: hex(f[7]),
        };
        let got = run(op, n, rm, hex(f[3]), hex(f[4]), hex(f[5]));
        cases += 1;
        if got != want && failures.len() < 20 {
            failures.push(format!(
                "{line}: got bits {:#x} flags {:#x}",
                got.bits, got.flags
            ));
        }
    }
    assert!(
        cases > 3000,
        "the fixture table holds {cases} cases — truncated?"
    );
    assert!(
        failures.is_empty(),
        "fixtures disagreeing with the reference (first {}):\n{}",
        failures.len(),
        failures.join("\n")
    );
}

#[test]
fn nan_boxing_follows_the_d_chapter() {
    // "The upper bits of a valid NaN-boxed value must be all 1s" (RVI-D §21.1.2)
    assert_eq!(fbox(32, 0x3f80_0000), 0xffff_ffff_3f80_0000);
    assert_eq!(
        fbox(32, 0x1234_5678_3f80_0000),
        0xffff_ffff_3f80_0000,
        "only the low n bits ride"
    );
    assert_eq!(funbox(32, 0xffff_ffff_3f80_0000), 0x3f80_0000);
    // "otherwise the input value is treated as an n-bit canonical NaN"
    assert_eq!(funbox(32, 0x0000_0000_3f80_0000), 0x7fc0_0000);
    assert_eq!(
        funbox(32, 0xfffe_ffff_3f80_0000),
        0x7fc0_0000,
        "one zero bit unboxes to the canonical NaN"
    );
    assert_eq!(
        fbox(64, 0x3ff0_0000_0000_0000),
        0x3ff0_0000_0000_0000,
        "FLEN-wide: identity"
    );
    assert_eq!(funbox(64, 0x0000_0000_3f80_0000), 0x0000_0000_3f80_0000);
}

#[test]
fn the_canonical_nans() {
    // RVI-F §20.1.3: "For single-precision floating-point, this corresponds to the pattern
    // 0x7fc00000"; the double form is RVI-D's
    assert_eq!(canonical_nan(32), 0x7fc0_0000);
    assert_eq!(canonical_nan(64), 0x7ff8_0000_0000_0000);
}

#[test]
fn rounding_mode_resolution() {
    // static modes 000..100 are themselves; 101/110 reserved; 111 is DYN through frm, and a
    // frm holding 101..111 is a reserved DYNAMIC mode (RVI-F §20.1.2, Table 2)
    assert_eq!(resolve_rm(0, 4), Some(Rm::Rne));
    assert_eq!(resolve_rm(4, 0), Some(Rm::Rmm));
    assert_eq!(resolve_rm(5, 0), None);
    assert_eq!(resolve_rm(6, 0), None);
    assert_eq!(resolve_rm(7, 1), Some(Rm::Rtz));
    assert_eq!(resolve_rm(7, 3), Some(Rm::Rup));
    for code in 0..=4 {
        assert_eq!(
            Rm::from_bits(code).map(Rm::bits),
            Some(code),
            "bits() inverts from_bits()"
        );
    }
    for frm in 5..=7 {
        assert_eq!(
            resolve_rm(7, frm),
            None,
            "DYN with frm = {frm:#05b} is reserved"
        );
    }
}

#[test]
fn a_directed_overflow_carries_of_where_the_backend_does_not() {
    // The measured LLVM-vs-IEEE deviation (decision_fp-backend-qualification): MAX+MAX in RTZ
    // clamps to MAX, and IEEE 754-2008 §7.4 still signals overflow — the unbounded rounding
    // (2^129 here) exceeds the largest finite.
    let raw =
        Single::from_bits(0x7f7f_ffff).add_r(Single::from_bits(0x7f7f_ffff), Round::TowardZero);
    assert!(
        !raw.status.contains(Status::OVERFLOW),
        "the backend's own report (the deviation)"
    );
    let r = add(32, Rm::Rtz, 0x7f7f_ffff, 0x7f7f_ffff);
    assert_eq!(
        r,
        Flagged {
            bits: 0x7f7f_ffff,
            flags: OF | NX
        }
    );
}

#[test]
fn no_overflow_from_infinite_operands() {
    // ∞ + 1 is exact: no OF even though the result exceeds the largest finite
    assert_eq!(
        add(32, Rm::Rne, 0x7f80_0000, 0x3f80_0000),
        Flagged {
            bits: 0x7f80_0000,
            flags: 0
        }
    );
    assert_eq!(
        fma(64, Rm::Rtz, 0x7ff0_0000_0000_0000, 0x4000_0000_0000_0000, 0),
        Flagged {
            bits: 0x7ff0_0000_0000_0000,
            flags: 0
        }
    );
}

#[test]
#[should_panic(expected = "a floating-point format of 16 bits")]
fn a_format_outside_the_language_is_a_description_defect() {
    let _ = add(16, Rm::Rne, 0, 0);
}
