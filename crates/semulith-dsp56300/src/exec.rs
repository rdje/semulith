//! Semantics for subset v0 — the definitional interpreter. Each rule cites its manual
//! source; the condition-code rules are FM Table 5-1 (reset/default scaling mode, which
//! subset v0 never leaves: S1 = S0 = 0), cross-checked against the reference's observed
//! end-state (`sr c00310` after the demo guest pins U = NOT(bit47 XOR bit46) — the manual
//! text's "U = (Bit 47 xor Bit 46)" is a known PDF-extraction inversion of its own prose
//! "set if the two MSBs are identical", and the differential harness is the arbiter).

use crate::decode::{Acc, Insn, MulPair, Reg, Space};
use crate::machine::{Machine, ModelStop, MASK24, MASK56, P_WORDS};

// CCR bit positions in SR (FM Table 5-1 / Figure 12-6: S L E U N Z V C in bits 7-0).
const CCR_S: u32 = 1 << 7;
const CCR_L: u32 = 1 << 6;
const CCR_E: u32 = 1 << 5;
const CCR_U: u32 = 1 << 4;
const CCR_N: u32 = 1 << 3;
const CCR_Z: u32 = 1 << 2;
const CCR_V: u32 = 1 << 1;
const CCR_C: u32 = 1 << 0;

fn bit(res: u64, n: u32) -> bool {
    res & (1u64 << n) != 0
}

/// The standard-definition CCR update (FM Table 5-1, no-scaling column) for a Data ALU
/// result: S (sticky), L (sticky, also set when V sets), E, U, N, Z. V and C are per
/// instruction and handled by the caller. `logical` selects the N bit's position (bit 47
/// for logical results, bit 55 for arithmetic).
fn ccr_standard(m: &mut Machine, res: u64, logical: bool) {
    // S — sticky: set when 0.25 ≤ |result| < 0.75 with the accumulator read as a fraction
    // (binary point left of bit 47); cleared only by a hardware reset.
    let mag = if bit(res, 55) {
        (!res).wrapping_add(1) & MASK56
    } else {
        res
    };
    if (1u64 << 45..3u64 << 45).contains(&mag) {
        m.sr |= CCR_S;
    }
    // E — set unless the signed integer portion (bits 55-47, no scaling) is all one value.
    let int_portion_all_same = {
        let v = (res >> 47) & 0x1FF;
        v == 0 || v == 0x1FF
    };
    m.sr = if int_portion_all_same {
        m.sr & !CCR_E
    } else {
        m.sr | CCR_E
    };
    // U — set when the two MSBs of the MSP are identical: NOT(bit47 XOR bit46).
    m.sr = if bit(res, 47) == bit(res, 46) {
        m.sr | CCR_U
    } else {
        m.sr & !CCR_U
    };
    // N — the MS bit of the result (bit 55 arithmetic, bit 47 logical).
    let n = if logical { bit(res, 47) } else { bit(res, 55) };
    m.sr = if n { m.sr | CCR_N } else { m.sr & !CCR_N };
    // Z — the whole 56-bit result is zero.
    m.sr = if res & MASK56 == 0 {
        m.sr | CCR_Z
    } else {
        m.sr & !CCR_Z
    };
}

/// Set V, and with it the sticky L (FM Table 5-1: L is set if the Overflow bit is set).
fn set_v(m: &mut Machine, overflow: bool) {
    if overflow {
        m.sr |= CCR_V | CCR_L;
    } else {
        m.sr &= !CCR_V;
    }
}

fn set_c(m: &mut Machine, carry: bool) {
    m.sr = if carry { m.sr | CCR_C } else { m.sr & !CCR_C };
}

fn acc_mut(m: &mut Machine, acc: Acc) -> &mut u64 {
    match acc {
        Acc::A => &mut m.a,
        Acc::B => &mut m.b,
    }
}

/// The two multiply operands of a pair, as signed 24-bit values (Table 12-16 names them
/// S1*S2; signed MPY/MAC are symmetric, so the pair's order is documentation only).
fn mul_operands(m: &Machine, pair: MulPair) -> (i64, i64) {
    let (a, b) = match pair {
        MulPair::X0X0 => (m.x0, m.x0),
        MulPair::Y0Y0 => (m.y0, m.y0),
        MulPair::X1X0 => (m.x1, m.x0),
        MulPair::Y1Y0 => (m.y1, m.y0),
        MulPair::X0Y1 => (m.x0, m.y1),
        MulPair::Y0X0 => (m.y0, m.x0),
        MulPair::X1Y0 => (m.x1, m.y0),
        MulPair::Y1X1 => (m.y1, m.x1),
    };
    (crate::machine::s24(a) as i64, crate::machine::s24(b) as i64)
}

/// The 56-bit signed product, pre-shifted: signed 24×24 then the fractional ×2 the MAC
/// unit applies (FM §3.3/§13 MPY description), negated first for the "-" sign option.
fn product(m: &Machine, pair: MulPair, negate: bool) -> i64 {
    let (s1, s2) = mul_operands(m, pair);
    let p = if negate { -(s1 * s2) } else { s1 * s2 };
    p << 1
}

/// Read a register onto the data bus for a move, applying the FM's readout rules:
/// - A1 — through the shifter/limiter (13-118: if the accumulator's signed integer
///   portion is in use, the bus carries the 24-bit saturation constant `$7FFFFF`/`$800000`
///   and L is set);
/// - A2 — the extension byte on the bus's 8 LSBs with bits 8-23 the sign extension of its
///   bit 7 (FM §3.4.1.2; no limiting on this path).
fn bus_read(m: &mut Machine, reg: Reg) -> u32 {
    match reg {
        Reg::X0 => m.x0,
        Reg::X1 => m.x1,
        Reg::Y0 => m.y0,
        Reg::Y1 => m.y1,
        Reg::A1 => {
            let a = m.a;
            let int_all_same = {
                let v = (a >> 47) & 0x1FF;
                v == 0 || v == 0x1FF
            };
            if int_all_same {
                ((a >> 24) as u32) & MASK24
            } else {
                m.sr |= CCR_L;
                if bit(a, 55) {
                    0x80_0000
                } else {
                    0x7F_FFFF
                }
            }
        }
        Reg::A2 => {
            let ext = ((m.a >> 48) & 0xFF) as u32;
            if ext & 0x80 != 0 {
                ext | 0xFF_FF00
            } else {
                ext
            }
        }
    }
}

fn bus_write(m: &mut Machine, reg: Reg, value: u32) {
    let value = value & MASK24;
    match reg {
        Reg::X0 => m.x0 = value,
        Reg::X1 => m.x1 = value,
        Reg::Y0 => m.y0 = value,
        Reg::Y1 => m.y1 = value,
        // A1/A2 as move DESTINATIONS are not in subset v0 (the accumulator-write readout
        // rules land with the guest that needs them); decode refuses them.
        Reg::A1 | Reg::A2 => unreachable!("decode refuses A1/A2 move destinations"),
    }
}

fn mem_word(m: &Machine, space: Space, addr: u32) -> Result<u32, ModelStop> {
    let mem = match space {
        Space::X => &m.x,
        Space::Y => &m.y,
    };
    mem.get(addr as usize)
        .copied()
        .ok_or(ModelStop::OutOfWindow {
            space: match space {
                Space::X => 'X',
                Space::Y => 'Y',
            },
            addr,
        })
}

fn mem_write(m: &mut Machine, space: Space, addr: u32, value: u32) -> Result<(), ModelStop> {
    let mem = match space {
        Space::X => &mut m.x,
        Space::Y => &mut m.y,
    };
    let cell = mem.get_mut(addr as usize).ok_or(ModelStop::OutOfWindow {
        space: match space {
            Space::X => 'X',
            Space::Y => 'Y',
        },
        addr,
    })?;
    *cell = value & MASK24;
    Ok(())
}

/// Execute one instruction. Returns the address of the next instruction to fetch; the
/// hardware-loop machinery (FM §13 DO, "End of Loop") may redirect it.
pub fn step(m: &mut Machine) -> Result<(), ModelStop> {
    let fetch_addr = m.pc;
    let w0 = *m.p.get(fetch_addr as usize).ok_or(ModelStop::OutOfWindow {
        space: 'P',
        addr: fetch_addr,
    })?;
    let w1 = m.p.get(fetch_addr as usize + 1).copied().unwrap_or(0);
    let (insn, words) = crate::decode::decode(w0, w1, fetch_addr)?;
    if words == 2 && fetch_addr as usize + 1 >= P_WORDS {
        return Err(ModelStop::OutOfWindow {
            space: 'P',
            addr: fetch_addr + 1,
        });
    }
    let mut next_pc = fetch_addr + u32::from(words);

    match insn {
        Insn::Nop => {}
        Insn::MoveImmShort { dest, imm } => {
            // FM §3.4.1.3: to X0/X1/Y0/Y1 the 8-bit short immediate is a signed fraction
            // stored in bits 23-16, the rest of the register zeroed.
            bus_write(m, dest, u32::from(imm) << 16);
        }
        Insn::MoveImmLong { dest, imm } => bus_write(m, dest, imm),
        Insn::MoveAbsLong {
            space,
            reg,
            write,
            addr,
        } => {
            if write {
                let value = bus_read(m, reg);
                mem_write(m, space, addr, value)?;
            } else {
                let value = mem_word(m, space, addr)?;
                bus_write(m, reg, value);
            }
        }
        Insn::Mpy { pair, dest, negate } => {
            let result = (product(m, pair, negate) as u64) & MASK56;
            *acc_mut(m, dest) = result;
            ccr_standard(m, result, false);
            // V: a signed 24×24 product shifted once fits 49 bits — the 56-bit result
            // cannot overflow (FM Table 5-1's V definition applied to MPY).
            set_v(m, false);
            // C is unchanged by MPY (FM 13-137's condition-code figure: "--" under C).
        }
        Insn::Mac { pair, dest, negate } => {
            let sum = crate::machine::s56(*acc_mut(m, dest)) as i128
                + i128::from(product(m, pair, negate));
            let wrapped = (sum as u64) & MASK56;
            *acc_mut(m, dest) = wrapped;
            ccr_standard(m, wrapped, false);
            // V: set when the true sum is not representable in 56 bits (FM Table 5-1).
            set_v(m, sum != i128::from(crate::machine::s56(wrapped)));
            // C is unchanged by MAC (FM 13-100's condition-code figure).
        }
        Insn::Asl { dest } => {
            let before = *acc_mut(m, dest);
            let result = (before << 1) & MASK56;
            *acc_mut(m, dest) = result;
            ccr_standard(m, result, false);
            // ASL's special definitions (FM 13-15): V is set if bit 55 changed during the
            // shift; C is the last bit shifted out.
            set_v(m, bit(before, 55) != bit(result, 55));
            set_c(m, bit(before, 55));
        }
        Insn::DoImm { count, target } => {
            if count == 0 {
                return Err(ModelStop::Input(
                    "DO with count 0 — the annulled-loop path is not in subset v0 yet".into(),
                ));
            }
            // FM §13 DO: push LA/LC, push PC(first loop instruction)/SR, load LC and LA
            // (the assembler's extension word is expr-1, the last instruction's address),
            // set LF.
            let la = m.la;
            let lc = m.lc;
            m.push(la, lc)?;
            let sr = m.sr;
            m.push(next_pc, sr)?;
            m.lc = u32::from(count);
            m.la = target;
            m.set_lf(true);
        }
        Insn::JmpAbs { target } => next_pc = target,
    }

    // The hardware loop's end-of-pass rule (FM §13 DO): when the instruction just fetched
    // was at LA and LF is set, either loop back (LC ≠ 1: LC-1 → LC, SSH → PC) or exit
    // (LC = 1: SSL's LF alone into SR, LA and LC restored from the stack, SP − 2).
    if m.lf() && fetch_addr == m.la {
        if m.lc != 1 {
            m.lc -= 1;
            next_pc = m.ssh();
        } else {
            let stacked_lf = m.ssl() & (1 << 15);
            m.sr = (m.sr & !(1 << 15)) | stacked_lf;
            m.pop();
            let (old_la, old_lc) = m.pop();
            m.la = old_la;
            m.lc = old_lc;
        }
    }
    m.pc = next_pc & MASK24;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn run(words: &[(u32, u32)], steps: usize) -> Machine {
        let mut m = Machine::new();
        for (addr, word) in words {
            m.p[*addr as usize] = *word;
        }
        m.pc = words.first().map(|(a, _)| *a).unwrap_or(0);
        for _ in 0..steps {
            step(&mut m).expect("guest stays inside subset v0");
        }
        m
    }

    /// MPY/MAC arithmetic, derived by hand from FM §13 (signed 24×24, fractional ×2):
    /// 0x123456 × 0x0ABCDE = 0x0BC24E_29C644? No — the demo record's independent Python
    /// leg: 2*(0x123456*0x0ABCDE + 0x050000*0x0ABCDE) << 4 = 0x001F253D515280. This test
    /// re-derives the two unsifted steps: after MPY then MAC, A must be
    /// 2*(0x123456*0x0ABCDE) + 2*(0x050000*0x0ABCDE) = 0x0001F253D51528.
    #[test]
    fn mpy_then_mac_matches_the_manual_derived_value() {
        let m = run(
            &[
                (0x100, 0x44F400),
                (0x101, 0x123456),
                (0x102, 0x46F400),
                (0x103, 0x0ABCDE),
                (0x104, 0x2000D0), // mpy x0,y0,a
                (0x105, 0x250500), // move #$5,x1
                (0x106, 0x2000E2), // mac x1,y0,a
            ],
            5,
        );
        assert_eq!(m.a, (0x01F253u64 << 24) | 0xD51528);
        assert_eq!(
            m.x1, 0x050000,
            "FM §3.4.1.3: the short immediate is bits 23-16"
        );
        // U set (top two MSP bits identical), E/N/Z/V/C clear — pins the extraction
        // inversion noted in the module header.
        assert_eq!(m.sr & 0xFF, CCR_U);
    }

    /// The full demo guest end-state — the manual-derived ground truth of
    /// `docs/tasks/artifacts/p3-breadth/2026-10-01-evidence-path-demo.md` (derived there
    /// three independent ways BEFORE this model existed: EVD-05).
    #[test]
    fn the_demo_guest_reaches_its_manual_derived_end_state() {
        let m = run(
            &[
                (0x100, 0x44F400),
                (0x101, 0x123456),
                (0x102, 0x46F400),
                (0x103, 0x0ABCDE),
                (0x104, 0x2000D0),
                (0x105, 0x250500),
                (0x106, 0x2000E2),
                (0x107, 0x547000),
                (0x108, 0x000200),
                (0x109, 0x527000),
                (0x10A, 0x000201),
                (0x10B, 0x5C7000),
                (0x10C, 0x000300),
                (0x10D, 0x060480),
                (0x10E, 0x00010F),
                (0x10F, 0x200032),
                (0x110, 0x000000),
                (0x111, 0x547000),
                (0x112, 0x000202),
                (0x113, 0x0AF080),
                (0x114, 0x000115),
            ],
            16,
        );
        assert_eq!(m.pc, 0x115);
        assert_eq!(m.sr, 0xC0_0310);
        assert_eq!(m.a, (0x1F253Du64 << 24) | 0x515280);
        assert_eq!(m.x0, 0x123456);
        assert_eq!(m.x1, 0x050000);
        assert_eq!(m.y0, 0x0ABCDE);
        assert_eq!(m.x[0x200], 0x01F253, "A1 pre-loop into X space");
        assert_eq!(m.x[0x202], 0x1F253D, "A1 post-loop into X space");
        assert_eq!(m.y[0x300], 0x01F253, "A1 pre-loop into Y space");
        assert_eq!(m.la, MASK24, "LA restored from the stack at loop end");
        assert_eq!(m.lc, 0);
        assert_eq!(m.sp, 0);
        assert!(!m.lf());
        let slots = m.stack_slots();
        assert_eq!(slots[1], [MASK24, 0], "the DO pushed the reset LA/LC");
        assert_eq!(
            slots[2],
            [0x00010F, 0xC0_0310],
            "then the first-loop-PC and SR"
        );
    }
}
