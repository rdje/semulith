//! Tests for the target arithmetic primitives.
//!
//! Two layers, per the `P1-LAB.2` acceptance:
//!
//! 1. **Boundary cases at full XLEN** — wrap points, sign boundaries, shift corners.
//! 2. **Exhaustive checks at a tractably reduced width (8 bits)** — every `(x, y)` pair of
//!    the binary operations, every `(x, shamt)` of the shifts, every `x` of the extensions
//!    and comparisons, compared against a reference formulated on a *different host width*
//!    (16/128-bit arithmetic, multiplication-as-shift, De Morgan formulations). Each
//!    reference is an independent machine path from the `u64` primitive; agreement across
//!    the two precisions is the host-mode-consistency evidence — nothing is assumed about
//!    what a host operation does, each assumption is fired at every input in the reduced
//!    space. The low byte of the `u64` result is compared, so the reduced-width reference
//!    judges the same function the target executes.

use super::*;

// ── Width-8 references: deliberately NOT the u64 formulation ─────────────────────────────

fn add8_ref(x: u8, y: u8) -> u8 {
    ((u16::from(x) + u16::from(y)) & 0xff) as u8
}

fn sub8_ref(x: u8, y: u8) -> u8 {
    ((u16::from(x) + 0x100 - u16::from(y)) & 0xff) as u8
}

fn shl8_ref(x: u8, shamt: u8) -> u8 {
    // multiplication by 2^shamt is a different machine path from `<<`
    (u16::from(x).wrapping_mul(1u16 << shamt)) as u8
}

fn shr8_ref(x: u8, shamt: u8) -> u8 {
    ((u16::from(x)) >> shamt) as u8
}

fn sar8_ref(x: u8, shamt: u8) -> u8 {
    ((x as i8) >> shamt) as u8
}

fn sext8_ref(x: u8, from_bits: u8) -> u8 {
    ((x << (8 - from_bits)) as i8 >> (8 - from_bits)) as u8
}

fn and8_ref(x: u8, y: u8) -> u8 {
    // De Morgan: a different formulation of the same truth table
    !(!x | !y)
}

fn bits8_ref(x: u8, hi: u8, lo: u8) -> u8 {
    let mut out = 0u8;
    for b in lo..=hi {
        out |= ((x >> b) & 1) << b;
    }
    out >> lo
}

/// A small deterministic generator (splitmix64) for the 32-bit sweeps — no dependencies.
struct Splitmix(u64);
impl Splitmix {
    fn next(&mut self) -> u64 {
        self.0 = self.0.wrapping_add(0x9e37_79b9_7f4a_7c15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xbf58_476d_1ce4_e5b9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94d0_49bb_1331_11eb);
        z ^ (z >> 31)
    }
}

// ── Exhaustive reduced-width (8-bit) layer ───────────────────────────────────────────────

#[test]
fn exhaustive_add_sub_wrap_at_width_8() {
    for x in 0..=u8::MAX {
        for y in 0..=u8::MAX {
            assert_eq!(add(u64::from(x), u64::from(y)) as u8, add8_ref(x, y));
            assert_eq!(sub(u64::from(x), u64::from(y)) as u8, sub8_ref(x, y));
        }
    }
}

#[test]
fn exhaustive_logic_and_compare_at_width_8() {
    for x in 0..=u8::MAX {
        for y in 0..=u8::MAX {
            assert_eq!(and(u64::from(x), u64::from(y)) as u8, and8_ref(x, y));
            assert_eq!(or(u64::from(x), u64::from(y)) as u8, x | y);
            assert_eq!(xor(u64::from(x), u64::from(y)) as u8, x ^ y);
            assert_eq!(sltu(u64::from(x), u64::from(y)), u64::from(x < y));
            // signed comparison is width-sensitive: the 8-bit signed view must be embedded
            // at XLEN (sign-extended) before the u64 primitive is asked about it
            let xs = (x as i8 as i64) as u64;
            let ys = (y as i8 as i64) as u64;
            assert_eq!(slt(xs, ys), u64::from((x as i8) < (y as i8)));
        }
    }
}

#[test]
fn exhaustive_shifts_at_width_8() {
    for x in 0..=u8::MAX {
        for shamt in 0..8 {
            // logical shifts are width-transparent on the low byte (zeros shift in)
            assert_eq!(
                shl(u64::from(x), u64::from(shamt)) as u8,
                shl8_ref(x, shamt)
            );
            assert_eq!(
                shr(u64::from(x), u64::from(shamt)) as u8,
                shr8_ref(x, shamt)
            );
            // arithmetic shift replicates the SIGN: embed the 8-bit signed view at XLEN,
            // then the whole result equals the sign-extended 8-bit reference
            let xs = (x as i8 as i64) as u64;
            let expected = i64::from(sar8_ref(x, shamt) as i8) as u64;
            assert_eq!(sar(xs, u64::from(shamt)), expected);
        }
    }
}

#[test]
fn exhaustive_sext_and_bits_at_width_8() {
    for x in 0..=u8::MAX {
        for from_bits in 1..=8 {
            assert_eq!(
                sext(u64::from(x), u32::from(from_bits)) as u8,
                sext8_ref(x, from_bits)
            );
        }
        for lo in 0..8 {
            for hi in lo..8 {
                assert_eq!(
                    bits(u64::from(x), u32::from(hi), u32::from(lo)) as u8,
                    bits8_ref(x, hi, lo)
                );
            }
        }
    }
}

// ── Shift-amount masking — REQ-D-SHAMT ───────────────────────────────────────────────────

#[test]
fn shamt_masks_drop_the_bits_the_spec_drops() {
    // 6-bit mask: bit 6 and above of rs2 must not contribute
    assert_eq!(shamt64(0x3f), 0x3f);
    assert_eq!(shamt64(0x40), 0); // 64 mod 64 would be 0 if wrapped — the mask forbids it silently
    assert_eq!(shamt64(0xff), 0x3f);
    assert_eq!(shamt64(u64::MAX), 0x3f);
    assert_eq!(shamt64(0x1234_5678_9abc_def0), 0x30);
    // 5-bit mask for the *W shifts
    assert_eq!(shamt32(0x1f), 0x1f);
    assert_eq!(shamt32(0x20), 0);
    assert_eq!(shamt32(0xffff_ffff_ffff_ffff), 0x1f);
}

#[test]
#[should_panic(expected = "unmasked shift amount")]
fn unmasked_shift_amount_panics_instead_of_wrapping() {
    // a decoder that forgot REQ-D-SHAMT must fail loudly, never compute `x << 0` for shamt 64
    let _ = shl(1, 64);
}

// ── Boundary cases at full XLEN ──────────────────────────────────────────────────────────

#[test]
fn full_width_wrap_and_sign_boundaries() {
    assert_eq!(add(u64::MAX, 1), 0); // REQ-D-ALU-REG: wraps modulo 2^64
    assert_eq!(sub(0, 1), u64::MAX);
    assert_eq!(add(u64::MAX, u64::MAX), u64::MAX - 1);

    // signed view: all-ones is -1, so it is less than every non-negative value
    assert_eq!(slt(u64::MAX, 0), 1);
    assert_eq!(slt(0, u64::MAX), 0);
    assert_eq!(slt(0x8000_0000_0000_0000, 0x7fff_ffff_ffff_ffff), 1); // INT_MIN < INT_MAX
    assert_eq!(sltu(u64::MAX, 0), 0); // unsigned: all-ones is the greatest value
}

#[test]
fn full_width_shift_corners() {
    assert_eq!(shl(1, 0), 1);
    assert_eq!(shl(1, 63), 0x8000_0000_0000_0000);
    assert_eq!(shr(0x8000_0000_0000_0000, 63), 1);
    assert_eq!(sar(0x8000_0000_0000_0000, 63), u64::MAX); // sign replicated
    assert_eq!(sar(0x4000_0000_0000_0000, 62), 1); // positive stays positive
    assert_eq!(sar(u64::MAX, 1), u64::MAX); // -1 >> 1 == -1
}

#[test]
fn sext_widths_used_by_the_isa() {
    // REQ-D-ALU-IMM: 12-bit I-immediate, range -2048..=2047
    assert_eq!(sext(0x7ff, 12), 0x7ff);
    assert_eq!(sext(0x800, 12), 0xffff_ffff_ffff_f800);
    assert_eq!(sext(0xfff, 12), u64::MAX);
    // REQ-D-LUI-AUIPC / REQ-D-WSUFFIX: 32-bit views
    assert_eq!(sext(0x7fff_ffff, 32), 0x7fff_ffff);
    assert_eq!(sext(0x8000_0000, 32), 0xffff_ffff_8000_0000);
    // full width is the identity
    assert_eq!(sext(0xdead_beef_cafe_babe, 64), 0xdead_beef_cafe_babe);
    // single bit: from_bits = 1 replicates bit 0
    assert_eq!(sext(1, 1), u64::MAX);
}

#[test]
fn lui_auipc_offset_formation() {
    assert_eq!(lui_auipc_offset(0), 0);
    assert_eq!(lui_auipc_offset(1), 4096);
    // imm[19] set: the 32-bit value is negative, so it sign-extends
    assert_eq!(lui_auipc_offset(0x8_0000), 0xffff_ffff_8000_0000);
    assert_eq!(lui_auipc_offset(0xf_ffff), 0xffff_ffff_ffff_f000);
}

// ── Word operations — REQ-D-WSUFFIX ──────────────────────────────────────────────────────

#[test]
fn word_ops_ignore_upper_inputs_and_sign_extend_results() {
    // upper 32 bits of the inputs are ignored
    assert_eq!(addw(0xdead_beef_0000_0001, 0), 1);
    // 32-bit wrap, then sign extension of the 32-bit result
    assert_eq!(addw(0xffff_ffff, 1), 0);
    assert_eq!(addw(0x7fff_ffff, 1), 0xffff_ffff_8000_0000); // INT32_MAX + 1 wraps to INT32_MIN
    assert_eq!(subw(0, 1), 0xffff_ffff_ffff_ffff); // 0 - 1 = 0xffffffff, sign-extended

    assert_eq!(shlw(1, 31), 0xffff_ffff_8000_0000);
    assert_eq!(shrw(0xffff_ffff_ffff_ffff, 31), 1); // low 32 bits shifted, then extended
    assert_eq!(sarw(0x0000_0000_8000_0000, 31), 0xffff_ffff_ffff_ffff);
    // upper junk must not leak into the arithmetic view of the low word
    assert_eq!(sarw(0x7fff_ffff_8000_0000, 4), 0xffff_ffff_f800_0000);
}

#[test]
fn word_ops_agree_with_a_u64_width_reference_over_a_sweep() {
    // reference computed in u64 (a different machine width from the u32 arithmetic inside
    // the primitives), on boundary-heavy generated inputs
    let mut rng = Splitmix(0x5eed_u64);
    for _ in 0..100_000 {
        let raw = rng.next();
        let x = match raw & 7 {
            0 => 0,
            1 => u64::MAX,
            2 => 0x7fff_ffff,
            3 => 0x8000_0000,
            4 => 0xffff_ffff,
            _ => raw,
        };
        let y = rng.next();
        let s = rng.next() % 32;

        let add_ref = sext(((x & 0xffff_ffff) + (y & 0xffff_ffff)) & 0xffff_ffff, 32);
        assert_eq!(addw(x, y), add_ref, "addw({x:#x}, {y:#x})");
        let sub_ref = sext(
            ((x & 0xffff_ffff) + 0x1_0000_0000 - (y & 0xffff_ffff)) & 0xffff_ffff,
            32,
        );
        assert_eq!(subw(x, y), sub_ref, "subw({x:#x}, {y:#x})");
        let shl_ref = sext(((x & 0xffff_ffff) << s) & 0xffff_ffff, 32);
        assert_eq!(shlw(x, s), shl_ref, "shlw({x:#x}, {s})");
        let shr_ref = sext((x & 0xffff_ffff) >> s, 32);
        assert_eq!(shrw(x, s), shr_ref, "shrw({x:#x}, {s})");
        let sar_ref = sext((((x as u32 as i32) >> s) as u32) as u64, 32);
        assert_eq!(sarw(x, s), sar_ref, "sarw({x:#x}, {s})");
    }
}
