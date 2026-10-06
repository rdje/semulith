//! The M operators against INDEPENDENT formulations — never the same expression twice: the
//! high halves against a 32-bit-limb schoolbook product, the divisions against the defining
//! identities RVI-M §11.1.2 states, and the word width against the host's own `i32`/`u32`
//! arithmetic. The edge rows of Table 1 that are the operators' (overflow) are pinned; the
//! ones that are the definition's (a zero divisor) are pinned as outside the domain.

use super::*;

const MIN: u64 = 1 << 63;

/// A deterministic operand stream: the edges, then a fixed-seed LCG (no host randomness).
fn operands() -> Vec<u64> {
    let mut v = vec![
        0,
        1,
        2,
        3,
        u64::MAX,
        u64::MAX - 1,
        MIN,
        MIN + 1,
        MIN - 1,
        0x8000_0000,
        0x7fff_ffff,
        0xffff_ffff,
        0x1_0000_0000,
        0xffff_ffff_8000_0000,
        0x0000_0000_ffff_fffe,
        0x5555_5555_5555_5555,
        0xaaaa_aaaa_aaaa_aaaa,
    ];
    let mut s: u64 = 0x2026_1006_0000_0011;
    for _ in 0..240 {
        s = s
            .wrapping_mul(6_364_136_223_846_793_005)
            .wrapping_add(1_442_695_040_888_963_407);
        v.push(s);
    }
    v
}

/// The full 128-bit unsigned product by 32-bit limbs, schoolbook — an independent route to
/// the high half (no 128-bit multiply).
fn wide_mulu(a: u64, b: u64) -> (u64, u64) {
    let (a0, a1, b0, b1) = (a & 0xffff_ffff, a >> 32, b & 0xffff_ffff, b >> 32);
    let p00 = a0 * b0;
    let p01 = a0 * b1;
    let p10 = a1 * b0;
    let p11 = a1 * b1;
    let mid = (p00 >> 32) + (p01 & 0xffff_ffff) + (p10 & 0xffff_ffff);
    let lo = (p00 & 0xffff_ffff) | (mid << 32);
    let hi = p11 + (p01 >> 32) + (p10 >> 32) + (mid >> 32);
    (hi, lo)
}

#[test]
fn the_high_halves_match_a_schoolbook_product() {
    for &a in &operands() {
        for &b in &operands() {
            let (hu, lo) = wide_mulu(a, b);
            assert_eq!(mul(a, b, 64), lo, "mul {a:#x} {b:#x}");
            assert_eq!(mulhu(a, b, 64), hu, "mulhu {a:#x} {b:#x}");
            // the signed corrections of the unsigned high half (Hacker's Delight 8-3):
            // a negative operand subtracts the other operand once from the high half
            let neg = |x: u64| x >> 63 == 1;
            let hsu = hu.wrapping_sub(if neg(a) { b } else { 0 });
            let hss = hsu.wrapping_sub(if neg(b) { a } else { 0 });
            assert_eq!(mulhsu(a, b, 64), hsu, "mulhsu {a:#x} {b:#x}");
            assert_eq!(mulh(a, b, 64), hss, "mulh {a:#x} {b:#x}");
        }
    }
}

#[test]
fn the_divisions_satisfy_the_identities_the_specification_states() {
    for &a in &operands() {
        for &b in &operands() {
            if b == 0 {
                continue;
            }
            let (q, r) = (div(a, b, 64).unwrap(), rem(a, b, 64).unwrap());
            if !(a == MIN && b == u64::MAX) {
                // "dividend = divisor × quotient + remainder", except in the case of overflow
                assert_eq!(
                    b.wrapping_mul(q).wrapping_add(r),
                    a,
                    "div/rem {a:#x} {b:#x}"
                );
                // "rounding towards zero": |remainder| < |divisor|
                assert!((r as i64).unsigned_abs() < (b as i64).unsigned_abs());
                // "the sign of a nonzero result equals the sign of the dividend"
                assert!(
                    r == 0 || (r as i64 >= 0) == (a as i64 >= 0),
                    "rem sign {a:#x} {b:#x}"
                );
            }
            let (qu, ru) = (divu(a, b, 64).unwrap(), remu(a, b, 64).unwrap());
            assert_eq!(
                b.wrapping_mul(qu).wrapping_add(ru),
                a,
                "divu/remu {a:#x} {b:#x}"
            );
            assert!(ru < b, "remu bound {a:#x} {b:#x}");
        }
    }
}

#[test]
fn the_word_width_is_the_hosts_32_bit_arithmetic() {
    for &a in &operands() {
        for &b in &operands() {
            let (x, y) = (a as u32, b as u32);
            assert_eq!(
                mul(a, b, 32),
                u64::from(x.wrapping_mul(y)),
                "mul.w {a:#x} {b:#x}"
            );
            let full = i64::from(x as i32) * i64::from(y as i32);
            assert_eq!(mulh(a, b, 32), (full >> 32) as u64 & 0xffff_ffff, "mulh.w");
            assert_eq!(
                mulhu(a, b, 32),
                (u64::from(x) * u64::from(y)) >> 32,
                "mulhu.w"
            );
            if y == 0 {
                continue;
            }
            assert_eq!(
                div(a, b, 32),
                Some(u64::from((x as i32).wrapping_div(y as i32) as u32))
            );
            assert_eq!(
                rem(a, b, 32),
                Some(u64::from((x as i32).wrapping_rem(y as i32) as u32))
            );
            assert_eq!(divu(a, b, 32), Some(u64::from(x / y)));
            assert_eq!(remu(a, b, 32), Some(u64::from(x % y)));
        }
    }
}

#[test]
fn overflow_wraps_to_table_1s_row_at_both_widths() {
    // RVI-M §11.1.2 Table 1, "Overflow (signed only)": quotient −2^(L−1), remainder 0
    assert_eq!(div(MIN, u64::MAX, 64), Some(MIN));
    assert_eq!(rem(MIN, u64::MAX, 64), Some(0));
    assert_eq!(div(0x8000_0000, 0xffff_ffff, 32), Some(0x8000_0000));
    assert_eq!(rem(0x8000_0000, 0xffff_ffff, 32), Some(0));
    // the high bits of a 32-bit operand are not part of it
    assert_eq!(
        div(0xdead_beef_8000_0000, 0x1234_ffff_ffff, 32),
        Some(0x8000_0000)
    );
}

#[test]
fn a_zero_divisor_is_outside_every_division_operators_domain() {
    for w in [64, 32] {
        for &a in &operands() {
            assert_eq!(div(a, 0, w), None);
            assert_eq!(divu(a, 0, w), None);
            assert_eq!(rem(a, 0, w), None);
            assert_eq!(remu(a, 0, w), None);
        }
    }
    // a divisor whose low 32 bits are zero is zero at width 32
    assert_eq!(div(7, 0x1_0000_0000, 32), None);
    assert_eq!(divu(7, 0x1_0000_0000, 64), Some(0));
}

#[test]
fn every_result_is_a_w_bit_value() {
    for &a in &operands() {
        for &b in &operands() {
            for (r, what) in [
                (mul(a, b, 32), "mul"),
                (mulh(a, b, 32), "mulh"),
                (mulhsu(a, b, 32), "mulhsu"),
                (mulhu(a, b, 32), "mulhu"),
                (div(a, b, 32).unwrap_or(0), "div"),
                (rem(a, b, 32).unwrap_or(0), "rem"),
            ] {
                assert_eq!(r >> 32, 0, "{what} at width 32 leaked high bits: {r:#x}");
            }
        }
    }
}
