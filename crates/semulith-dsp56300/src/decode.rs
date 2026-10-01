//! Decode for subset v0 — every mask derived from the pinned family manual's instruction
//! descriptions and encoding tables, cross-checked against the pinned assembler's output.
//!
//! Sources (DSP56300FM Rev. 5):
//! - NOP — §13 (13-149): opcode `$000000`.
//! - MPY (±)S1,S2,D — 13-137/13-138: Data Bus Move Field `|$20|` (no parallel move,
//!   13-112) + `1QQQdk00`; QQQ per Table 12-16.
//! - MAC (±)S1,S2,D — 13-99/13-100: same move field + `1QQQdk10`.
//! - ASL D — 13-15: same move field + `0011d010`.
//! - MOVE #xx,D (immediate short) — 13-113/13-114: `001ddddd iiiiiiii 00000000`.
//! - MOVE #xxxxxx,D (immediate long), MOVE S,X:<abs> / X:<abs>,D — 13-118 (X Memory Data
//!   Move, Instruction Formats and Opcodes 1): `01dd<S>ddd W 1 MMMRRR 00000000` with
//!   MMMRRR = `110100` (immediate, extension word) or `110000` (absolute address,
//!   extension word); bit 19 carries the space (0 = X, 1 = Y — measured on the pinned
//!   assembler's output for `move a1,x:…` `$547000` vs `move a1,y:…` `$5C7000`).
//! - DO #xxx,expr — 13-58: `00000110 iiiiiiii 1000 hhhh` + absolute-address extension word.
//! - JMP <abs> — 13-83: `0000 1010 11 MMMRRR 10000000` with MMMRRR = `110000` + extension.
//!
//! Register codes (Table 12-13, whose PDF table extraction is lossy — the codes below are
//! the cells the pinned assembler emits, each one confirmed against a load-bearing guest
//! word): X0 `$04`, X1 `$05`, Y0 `$06`, Y1 `$07`, A2 `$0A`, A1 `$0C`. A word naming any
//! other code is outside subset v0 and stops the model by name.

use crate::machine::{ModelStop, MASK24};

/// X or Y data space (P is fetch-only in subset v0).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Space {
    X,
    Y,
}

/// A register the subset's moves can name.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Reg {
    X0,
    X1,
    Y0,
    Y1,
    A1,
    A2,
}

/// A multiply source pair, QQQ per FM Table 12-16 (encoding 1).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum MulPair {
    X0X0,
    Y0Y0,
    X1X0,
    Y1Y0,
    X0Y1,
    Y0X0,
    X1Y0,
    Y1X1,
}

/// The destination accumulator of a Data ALU operation (d: 0 = A, 1 = B, Table 12-13).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Acc {
    A,
    B,
}

/// A decoded subset-v0 instruction. Two-word forms carry their extension word's content.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Insn {
    Nop,
    /// MOVE #xx,D — the 8-bit short immediate (its placement is destination-class
    /// semantics, FM §3.4.1.3: a signed fraction into the 8 MSBs for X0/X1/Y0/Y1).
    MoveImmShort {
        dest: Reg,
        imm: u8,
    },
    /// MOVE #xxxxxx,D — the 24-bit immediate in the extension word.
    MoveImmLong {
        dest: Reg,
        imm: u32,
    },
    /// MOVE S,X/Y:<abs> (write = register to memory) or X/Y:<abs>,D (write = false).
    MoveAbsLong {
        space: Space,
        reg: Reg,
        write: bool,
        addr: u32,
    },
    Mpy {
        pair: MulPair,
        dest: Acc,
        negate: bool,
    },
    Mac {
        pair: MulPair,
        dest: Acc,
        negate: bool,
    },
    Asl {
        dest: Acc,
    },
    /// DO #xxx,expr — 12-bit count; `target` is the extension word (LA, the assembled
    /// last-loop-instruction address).
    DoImm {
        count: u16,
        target: u32,
    },
    JmpAbs {
        target: u32,
    },
}

fn reg_of(code: u32) -> Option<Reg> {
    match code {
        0x04 => Some(Reg::X0),
        0x05 => Some(Reg::X1),
        0x06 => Some(Reg::Y0),
        0x07 => Some(Reg::Y1),
        0x0A => Some(Reg::A2),
        0x0C => Some(Reg::A1),
        _ => None,
    }
}

fn mul_pair(qqq: u32) -> MulPair {
    match qqq & 7 {
        0 => MulPair::X0X0,
        1 => MulPair::Y0Y0,
        2 => MulPair::X1X0,
        3 => MulPair::Y1Y0,
        4 => MulPair::X0Y1,
        5 => MulPair::Y0X0,
        6 => MulPair::X1Y0,
        _ => MulPair::Y1X1,
    }
}

/// Decode one instruction from `w0` (and `w1`, the following word, read only by two-word
/// forms). Returns the instruction and its length in words. Anything else is a typed stop
/// with the word named — never a guessed translation.
pub fn decode(w0: u32, w1: u32, addr: u32) -> Result<(Insn, u8), ModelStop> {
    let unsupported = || ModelStop::UnsupportedInsn { addr, word: w0 };

    if w0 == 0 {
        return Ok((Insn::Nop, 1));
    }

    // Data Bus Move Field $20 — no parallel move; the low 16 bits are the opcode (13-112).
    if w0 & 0xFF_0000 == 0x20_0000 {
        let low = w0 & 0xFFFF;
        // MPY/MAC (±)S1,S2,D: 1QQQdk00 / 1QQQdk10 (13-99, 13-138).
        if low & 0xFF80 == 0x0080 {
            let pair = mul_pair((low >> 4) & 7);
            let dest = if low & 0x8 != 0 { Acc::B } else { Acc::A };
            let negate = low & 0x4 != 0;
            return match low & 0x3 {
                0 => Ok((Insn::Mpy { pair, dest, negate }, 1)),
                2 => Ok((Insn::Mac { pair, dest, negate }, 1)),
                _ => Err(unsupported()),
            };
        }
        // ASL D: 0011d010 (13-15).
        if low & 0xFFF7 == 0x0032 {
            let dest = if low & 0x8 != 0 { Acc::B } else { Acc::A };
            return Ok((Insn::Asl { dest }, 1));
        }
        return Err(unsupported());
    }

    // MOVE #xx,D (immediate short): 001ddddd iiiiiiii 00000000 (13-114).
    if w0 & 0xE0_00FF == 0x20_0000 {
        let dest = reg_of((w0 >> 16) & 0x1F).ok_or_else(unsupported)?;
        return Ok((
            Insn::MoveImmShort {
                dest,
                imm: (w0 >> 8) as u8,
            },
            1,
        ));
    }

    // The 01 move class (13-118): 01dd<S>ddd W 1 MMMRRR + optional extension word.
    if w0 & 0xC0_0000 == 0x40_0000 && w0 & 0x4000 != 0 {
        let space = if w0 & 0x8_0000 != 0 {
            Space::Y
        } else {
            Space::X
        };
        let reg = reg_of(((w0 >> 17) & 0x18) | ((w0 >> 16) & 0x07)).ok_or_else(unsupported)?;
        let write = w0 & 0x8000 == 0;
        return match (w0 >> 8) & 0x3F {
            // MMMRRR = 110100: MOVE #xxxxxx,D — the extension word is the immediate.
            0x34 if !write => Ok((
                Insn::MoveImmLong {
                    dest: reg,
                    imm: w1 & MASK24,
                },
                2,
            )),
            // MMMRRR = 110000: X/Y absolute in the extension word, either direction.
            0x30 => Ok((
                Insn::MoveAbsLong {
                    space,
                    reg,
                    write,
                    addr: w1 & MASK24,
                },
                2,
            )),
            _ => Err(unsupported()),
        };
    }

    // DO #xxx,expr: 00000110 iiiiiiii 1000 hhhh + absolute-address extension (13-58).
    if w0 & 0xFF_00F0 == 0x06_0080 {
        let count = (((w0 & 0xF) << 8) | ((w0 >> 8) & 0xFF)) as u16;
        return Ok((
            Insn::DoImm {
                count,
                target: w1 & MASK24,
            },
            2,
        ));
    }

    // JMP <absolute>: 0000 1010 11 MMMRRR 10000000, MMMRRR = 110000 + extension (13-83).
    if w0 & 0xFF_C0FF == 0x0A_C080 && (w0 >> 8) & 0x3F == 0x30 {
        return Ok((
            Insn::JmpAbs {
                target: w1 & MASK24,
            },
            2,
        ));
    }

    Err(unsupported())
}

#[cfg(test)]
mod tests {
    use super::*;

    /// The pinned assembler's words for the `.3` demo guest (docs/tasks/artifacts/
    /// p3-breadth/dsp56300-demo/micro.a56) — every form the first differential case needs,
    /// decoded against the manual-derived masks.
    #[test]
    fn decodes_the_demo_guest_forms() {
        assert_eq!(
            decode(0x44F400, 0x123456, 0x100),
            Ok((
                Insn::MoveImmLong {
                    dest: Reg::X0,
                    imm: 0x123456
                },
                2
            ))
        );
        assert_eq!(
            decode(0x46F400, 0x0ABCDE, 0x102),
            Ok((
                Insn::MoveImmLong {
                    dest: Reg::Y0,
                    imm: 0x0ABCDE
                },
                2
            ))
        );
        assert_eq!(
            decode(0x2000D0, 0, 0x104),
            Ok((
                Insn::Mpy {
                    pair: MulPair::Y0X0,
                    dest: Acc::A,
                    negate: false
                },
                1
            ))
        );
        assert_eq!(
            decode(0x250500, 0, 0x105),
            Ok((
                Insn::MoveImmShort {
                    dest: Reg::X1,
                    imm: 0x05
                },
                1
            ))
        );
        assert_eq!(
            decode(0x2000E2, 0, 0x106),
            Ok((
                Insn::Mac {
                    pair: MulPair::X1Y0,
                    dest: Acc::A,
                    negate: false
                },
                1
            ))
        );
        assert_eq!(
            decode(0x547000, 0x000200, 0x107),
            Ok((
                Insn::MoveAbsLong {
                    space: Space::X,
                    reg: Reg::A1,
                    write: true,
                    addr: 0x200
                },
                2
            ))
        );
        assert_eq!(
            decode(0x527000, 0x000201, 0x109),
            Ok((
                Insn::MoveAbsLong {
                    space: Space::X,
                    reg: Reg::A2,
                    write: true,
                    addr: 0x201
                },
                2
            ))
        );
        assert_eq!(
            decode(0x5C7000, 0x000300, 0x10B),
            Ok((
                Insn::MoveAbsLong {
                    space: Space::Y,
                    reg: Reg::A1,
                    write: true,
                    addr: 0x300
                },
                2
            ))
        );
        assert_eq!(
            decode(0x060480, 0x00010F, 0x10D),
            Ok((
                Insn::DoImm {
                    count: 4,
                    target: 0x10F
                },
                2
            ))
        );
        assert_eq!(
            decode(0x200032, 0, 0x10F),
            Ok((Insn::Asl { dest: Acc::A }, 1))
        );
        assert_eq!(decode(0x000000, 0, 0x110), Ok((Insn::Nop, 1)));
        assert_eq!(
            decode(0x0AF080, 0x000115, 0x113),
            Ok((Insn::JmpAbs { target: 0x115 }, 2))
        );
    }

    /// A word outside the subset stops the model by name — the ARCHITECTURE §2 rule.
    #[test]
    fn refuses_an_out_of_subset_word_by_name() {
        let stop = decode(0xDEADBE, 0, 0x42).unwrap_err();
        assert_eq!(
            stop,
            ModelStop::UnsupportedInsn {
                addr: 0x42,
                word: 0xDEADBE
            }
        );
    }
}
