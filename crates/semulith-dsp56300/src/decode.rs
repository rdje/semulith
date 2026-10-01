//! Decode for subset v0 — every mask derived from the pinned family manual's instruction
//! descriptions and encoding tables, cross-checked against the pinned assembler's output.
//!
//! Sources (DSP56300FM Rev. 5; page numbers are the printed page footers — the chapter's
//! own table of contents numbers pages differently, a measured FM-internal discrepancy):
//! - NOP — 13-145: opcode `$000000`.
//! - MPY (±)S1,S2,D — 13-137/13-138: Data Bus Move Field `|$20|` (no parallel move,
//!   13-112) + `1QQQdk00`; QQQ per Table 12-16.
//! - MAC (±)S1,S2,D — 13-99/13-100: same move field + `1QQQdk10`.
//! - ASL D — 13-15: same move field + `0011d010`; ASR D — 13-17: `0010d010`;
//!   LSR D — 13-96: `0010d011`.
//! - ADD/SUB/CMP S,D — 13-8 / 13-173 / 13-46: same move field + `0JJJd000` / `0JJJd100` /
//!   `0JJJd101` (JJJ per Table 12-13, 12-18; CMP has no X/Y long-word source — Table 12-16).
//! - AND/OR/EOR S,D — 13-12 / 13-150 / 13-69: same move field + `01JJd110` / `01JJd010` /
//!   `01JJd011` (JJ: X0=00, Y0=01, X1=10, Y1=11 — Table 12-13's source-operand encoding).
//! - The six ops' immediate forms (e.g. ADD 13-8): #xx is
//!   `00000001 01iiiiii 1000dkkk` (6-bit immediate), #xxxx is `00000001 01000000 1100dkkk`
//!   + immediate extension word; kkk: ADD 000, OR 010, EOR 011, SUB 100, CMP 101, AND 110.
//! - MOVE #xx,D (immediate short) — 13-113/13-114: `001ddddd iiiiiiii 00000000`.
//! - MOVE #xxxxxx,D (immediate long), MOVE S,X:<abs> / X:<abs>,D, and the register-indirect
//!   forms — 13-118 (X Memory Data Move): `01dd<S>ddd W 1 MMMRRR` + extension word for
//!   MMMRRR = `110100` (immediate) or `110000` (absolute); the linear register-indirect
//!   modes per Effective Addressing Mode Encoding 1 (Table 12-13, 12-18): 000/001 (Rn)∓Nn,
//!   010/011 (Rn)∓, 100 (Rn), 101 (Rn+Nn), 111 -(Rn); bit 19 carries the space (0 = X,
//!   1 = Y — measured on the pinned assembler's output for `move a1,x:…` `$547000` vs
//!   `move a1,y:…` `$5C7000`).
//! - DO #xxx,expr — 13-58: `00000110 iiiiiiii 1000 hhhh` + absolute-address extension word.
//! - REP #xxx / REP S — 13-161: `00000110 iiiiiiii 1010 hhhh` /
//!   `00000110 11dddddd 00100000` (dddddd is the six-bit register code, Table 12-13).
//! - ENDDO — 13-67: `$00008C`. RTS — 13-168: `$00000C`.
//! - JMP <abs> — 13-83: `0000 1010 11 MMMRRR 10000000` with MMMRRR = `110000` + extension;
//!   JSR <abs> — 13-89: `0000 1011 11 MMMRRR 10000000`, same extension shape.
//!
//! Register codes (Table 12-13's six-bit encoding / Table 12-14, whose PDF table extraction
//! is lossy — the codes below are the cells the pinned assembler emits, each one confirmed
//! against a load-bearing guest word): X0 `$04`, X1 `$05`, Y0 `$06`, Y1 `$07`, A2 `$0A`,
//! B2 `$0B`, A1 `$0C`, B1 `$0D`, A `$0E`, B `$0F`, R0–R7 `$10`–`$17`, N0–N7 `$18`–`$1F`.
//! A word naming any other code is outside subset v0 and stops the model by name.

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
    B1,
    B2,
    /// The 56-bit accumulator as an immediate-move destination (A `$0E`, B `$0F`).
    AccA,
    AccB,
    /// AGU address register R0–R7 (`$10`–`$17`) — immediate-move destinations only.
    R(usize),
    /// AGU offset register N0–N7 (`$18`–`$1F`) — immediate-move destinations only.
    N(usize),
}

/// The subset's data-ALU core operation (kkk in the immediate forms: ADD 000, OR 010,
/// EOR 011, SUB 100, CMP 101, AND 110 — e.g. FM 13-8).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AluOp {
    Add,
    Sub,
    Cmp,
    And,
    Or,
    Eor,
}

/// A data-ALU register source. JJJ per Table 12-13 (12-18): the other accumulator `001`,
/// the 48-bit long words X `010` / Y `011`, X0 `100`, Y0 `101`, X1 `110`, Y1 `111`. The
/// logical ops' two-bit JJ names only the four word registers (13-12).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AluSrc {
    X0,
    X1,
    Y0,
    Y1,
    /// The 48-bit long word X1:X0.
    LongX,
    /// The 48-bit long word Y1:Y0.
    LongY,
    /// The accumulator that is NOT the destination (JJJ `001`).
    OtherAcc,
}

/// The linear register-indirect addressing modes (MMM, Effective Addressing Mode Encoding
/// 1, Table 12-13). Modulo and reverse-carry arithmetic are outside subset v0: execution
/// stops by name if the mode register Mn is not `$FFFFFF` (linear).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EaMode {
    /// (Rn)-Nn — post-decrement by Nn (MMM 000).
    PostSubN,
    /// (Rn)+Nn — post-increment by Nn (MMM 001).
    PostAddN,
    /// (Rn)- — post-decrement (MMM 010).
    PostDec,
    /// (Rn)+ — post-increment (MMM 011).
    PostInc,
    /// (Rn) — no update (MMM 100).
    NoUpdate,
    /// (Rn+Nn) — displacement, no update (MMM 101).
    DispAddN,
    /// -(Rn) — pre-decrement (MMM 111).
    PreDec,
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
    /// MOVE through a linear register-indirect effective address (Rn) (write = register
    /// to memory). The address register update follows the mode.
    MoveRegInd {
        space: Space,
        reg: Reg,
        write: bool,
        mode: EaMode,
        rn: usize,
    },
    /// ADD/SUB/CMP/AND/OR/EOR S,D — the register-source data-ALU core.
    AluReg {
        op: AluOp,
        src: AluSrc,
        dest: Acc,
    },
    /// The 6-bit immediate data-ALU forms (`00000001 01iiiiii 1000dkkk`).
    AluImmShort {
        op: AluOp,
        imm: u8,
        dest: Acc,
    },
    /// The 24-bit immediate data-ALU forms (`00000001 01000000 1100dkkk` + extension).
    AluImmLong {
        op: AluOp,
        imm: u32,
        dest: Acc,
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
    Asr {
        dest: Acc,
    },
    Lsr {
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
    JsrAbs {
        target: u32,
    },
    Rts,
    Enddo,
    /// REP #xxx — 12-bit count (the FM's REP page: a zero count repeats 65,536 times).
    RepImm {
        count: u16,
    },
    /// REP S — the count from a word register's 24 bits (X0/X1/Y0/Y1 in subset v0).
    RepReg {
        src: Reg,
    },
}

fn reg_of(code: u32) -> Option<Reg> {
    match code {
        0x04 => Some(Reg::X0),
        0x05 => Some(Reg::X1),
        0x06 => Some(Reg::Y0),
        0x07 => Some(Reg::Y1),
        0x0A => Some(Reg::A2),
        0x0B => Some(Reg::B2),
        0x0C => Some(Reg::A1),
        0x0D => Some(Reg::B1),
        0x0E => Some(Reg::AccA),
        0x0F => Some(Reg::AccB),
        0x10..=0x17 => Some(Reg::R((code - 0x10) as usize)),
        0x18..=0x1F => Some(Reg::N((code - 0x18) as usize)),
        _ => None,
    }
}

/// The registers an (Rn)/absolute move can name as its data end — the data-ALU set. AGU
/// registers move to/from X/Y memory through other classes, all outside subset v0.
fn is_data_reg(reg: Reg) -> bool {
    matches!(
        reg,
        Reg::X0 | Reg::X1 | Reg::Y0 | Reg::Y1 | Reg::A1 | Reg::A2 | Reg::B1 | Reg::B2
    )
}

/// The registers an immediate move can target in subset v0: the word registers, the whole
/// accumulators, and the AGU R/N registers. Accumulator PARTS (A0/A1/A2, B0/B1/B2) as move
/// destinations carry the accumulator-write readout rules and stay outside subset v0.
fn is_imm_dest(reg: Reg) -> bool {
    !matches!(reg, Reg::A1 | Reg::A2 | Reg::B1 | Reg::B2)
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
    // RTS — 13-168: `$00000C`. ENDDO — 13-67: `$00008C`.
    if w0 == 0x00000C {
        return Ok((Insn::Rts, 1));
    }
    if w0 == 0x00008C {
        return Ok((Insn::Enddo, 1));
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
        // ASL D: 0011d010 (13-15); ASR D: 0010d010 (13-17); LSR D: 0010d011 (13-96).
        if low & 0xFFF7 == 0x0032 {
            let dest = if low & 0x8 != 0 { Acc::B } else { Acc::A };
            return Ok((Insn::Asl { dest }, 1));
        }
        if low & 0xFFF7 == 0x0022 {
            let dest = if low & 0x8 != 0 { Acc::B } else { Acc::A };
            return Ok((Insn::Asr { dest }, 1));
        }
        if low & 0xFFF7 == 0x0023 {
            let dest = if low & 0x8 != 0 { Acc::B } else { Acc::A };
            return Ok((Insn::Lsr { dest }, 1));
        }
        // The register-source data-ALU core (bit 7 = 0): ADD/SUB/CMP use the 3-bit JJJ
        // (Table 12-13); AND/OR/EOR the 2-bit JJ with bits 7-6 = 01 (13-12).
        if low & 0x80 == 0 {
            let dest = if low & 0x8 != 0 { Acc::B } else { Acc::A };
            let jjj = (low >> 4) & 7;
            let word_src = || match jjj & 3 {
                0 => AluSrc::X0,
                1 => AluSrc::Y0,
                2 => AluSrc::X1,
                _ => AluSrc::Y1,
            };
            let (op, src) = match low & 7 {
                // ADD/SUB: 0JJJd000 / 0JJJd100 — JJJ 000 is reserved (Table 12-13).
                0 | 4 => {
                    let src = match jjj {
                        1 => AluSrc::OtherAcc,
                        2 => AluSrc::LongX,
                        3 => AluSrc::LongY,
                        4..=7 => word_src(),
                        _ => return Err(unsupported()),
                    };
                    let op = if low & 7 == 0 { AluOp::Add } else { AluOp::Sub };
                    (op, src)
                }
                // CMP: 0JJJd101 — no X/Y long-word source (Table 12-16).
                5 => {
                    let src = match jjj {
                        1 => AluSrc::OtherAcc,
                        4..=7 => word_src(),
                        _ => return Err(unsupported()),
                    };
                    (AluOp::Cmp, src)
                }
                // AND/OR/EOR: 01JJd110 / 01JJd010 / 01JJd011.
                6 | 2 | 3 if low & 0xC0 == 0x40 => {
                    let op = match low & 7 {
                        6 => AluOp::And,
                        2 => AluOp::Or,
                        _ => AluOp::Eor,
                    };
                    (op, word_src())
                }
                _ => return Err(unsupported()),
            };
            return Ok((Insn::AluReg { op, src, dest }, 1));
        }
        return Err(unsupported());
    }

    // MOVE #xx,D (immediate short): 001ddddd iiiiiiii 00000000 (13-114).
    if w0 & 0xE0_00FF == 0x20_0000 {
        let dest = reg_of((w0 >> 16) & 0x1F).ok_or_else(unsupported)?;
        if !is_imm_dest(dest) {
            return Err(unsupported());
        }
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
        let mmmrrr = (w0 >> 8) & 0x3F;
        return match mmmrrr {
            // MMMRRR = 110100: MOVE #xxxxxx,D — the extension word is the immediate.
            0x34 if !write && is_imm_dest(reg) => Ok((
                Insn::MoveImmLong {
                    dest: reg,
                    imm: w1 & MASK24,
                },
                2,
            )),
            // MMMRRR = 110000: X/Y absolute in the extension word, either direction.
            0x30 if is_data_reg(reg) => Ok((
                Insn::MoveAbsLong {
                    space,
                    reg,
                    write,
                    addr: w1 & MASK24,
                },
                2,
            )),
            // The linear register-indirect modes (Encoding 1, Table 12-13).
            _ if is_data_reg(reg) => {
                let mode = match mmmrrr >> 3 {
                    0 => EaMode::PostSubN,
                    1 => EaMode::PostAddN,
                    2 => EaMode::PostDec,
                    3 => EaMode::PostInc,
                    4 => EaMode::NoUpdate,
                    5 => EaMode::DispAddN,
                    7 => EaMode::PreDec,
                    // MMM = 110 with RRR ≠ 000/100: no such mode.
                    _ => return Err(unsupported()),
                };
                Ok((
                    Insn::MoveRegInd {
                        space,
                        reg,
                        write,
                        mode,
                        rn: (mmmrrr & 7) as usize,
                    },
                    1,
                ))
            }
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

    // REP #xxx: 00000110 iiiiiiii 1010 hhhh (13-161).
    if w0 & 0xFF_00F0 == 0x06_00A0 {
        let count = (((w0 & 0xF) << 8) | ((w0 >> 8) & 0xFF)) as u16;
        return Ok((Insn::RepImm { count }, 1));
    }
    // REP S: 00000110 11dddddd 00100000 (13-161) — subset v0 counts from X0/X1/Y0/Y1.
    if w0 & 0xFF_C0FF == 0x06_C020 {
        let src = reg_of((w0 >> 8) & 0x3F).ok_or_else(unsupported)?;
        if !matches!(src, Reg::X0 | Reg::X1 | Reg::Y0 | Reg::Y1) {
            return Err(unsupported());
        }
        return Ok((Insn::RepReg { src }, 1));
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

    // JSR <absolute>: 0000 1011 11 MMMRRR 10000000, MMMRRR = 110000 + extension (13-89).
    if w0 & 0xFF_C0FF == 0x0B_C080 && (w0 >> 8) & 0x3F == 0x30 {
        return Ok((
            Insn::JsrAbs {
                target: w1 & MASK24,
            },
            2,
        ));
    }

    // The immediate data-ALU core: #xx is 00000001 01iiiiii 1000dkkk; #xxxx is
    // 00000001 01000000 1100dkkk + extension word (e.g. ADD 13-8). kkk: ADD 000, OR 010,
    // EOR 011, SUB 100, CMP 101, AND 110.
    if w0 & 0xFF_C0F0 == 0x01_4080 || w0 & 0xFF_C0F0 == 0x01_40C0 {
        let long = w0 & 0xF0 == 0xC0;
        let op = match w0 & 7 {
            0 => AluOp::Add,
            2 => AluOp::Or,
            3 => AluOp::Eor,
            4 => AluOp::Sub,
            5 => AluOp::Cmp,
            6 => AluOp::And,
            _ => return Err(unsupported()),
        };
        let dest = if w0 & 0x8 != 0 { Acc::B } else { Acc::A };
        if long {
            return Ok((
                Insn::AluImmLong {
                    op,
                    imm: w1 & MASK24,
                    dest,
                },
                2,
            ));
        }
        return Ok((
            Insn::AluImmShort {
                op,
                imm: ((w0 >> 8) & 0x3F) as u8,
                dest,
            },
            1,
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

    /// The slice-4 forms, pinned against the pinned assembler's words for the probe corpus
    /// (target/dsp56300-probe/probe.a56 + probe2.a56, assembled `2026-10-01`): every mask
    /// derived from the FM figures, every emitted word confirming them.
    #[test]
    fn decodes_the_slice4_probe_forms() {
        // The register-source data-ALU core (move field $20 + 0JJJd_kk / 01JJd_kk).
        let alu = |word, op, src, dest| {
            assert_eq!(
                decode(word, 0, 0x100),
                Ok((Insn::AluReg { op, src, dest }, 1)),
                "word {word:06X}"
            );
        };
        alu(0x200040, AluOp::Add, AluSrc::X0, Acc::A); // add x0,a
        alu(0x200078, AluOp::Add, AluSrc::Y1, Acc::B); // add y1,b
        alu(0x200010, AluOp::Add, AluSrc::OtherAcc, Acc::A); // add b,a
        alu(0x200018, AluOp::Add, AluSrc::OtherAcc, Acc::B); // add a,b
        alu(0x200044, AluOp::Sub, AluSrc::X0, Acc::A); // sub x0,a
        alu(0x200045, AluOp::Cmp, AluSrc::X0, Acc::A); // cmp x0,a
        alu(0x200046, AluOp::And, AluSrc::X0, Acc::A); // and x0,a
        alu(0x200042, AluOp::Or, AluSrc::X0, Acc::A); // or x0,a
        alu(0x200043, AluOp::Eor, AluSrc::X0, Acc::A); // eor x0,a

        // The immediate forms: #xx = $014080|ii<<8|d<<3|kkk, #xxxx = $0140C0|d<<3|kkk.
        let imm = |w0, w1, op, imm: u32, dest, len| {
            assert_eq!(
                decode(w0, w1, 0x100),
                Ok((
                    if len == 1 {
                        Insn::AluImmShort {
                            op,
                            imm: imm as u8,
                            dest,
                        }
                    } else {
                        Insn::AluImmLong { op, imm, dest }
                    },
                    len
                )),
                "word {w0:06X}"
            );
        };
        imm(0x014580, 0, AluOp::Add, 0x05, Acc::A, 1); // add #$5,a
        imm(0x0140C0, 0x123456, AluOp::Add, 0x123456, Acc::A, 2); // add #$123456,a
        imm(0x01478C, 0, AluOp::Sub, 0x07, Acc::B, 1); // sub #$7,b
        imm(0x017F85, 0, AluOp::Cmp, 0x3F, Acc::A, 1); // cmp #$3f,a
        imm(0x016A86, 0, AluOp::And, 0x2A, Acc::A, 1); // and #$2a,a
        imm(0x01518A, 0, AluOp::Or, 0x11, Acc::B, 1); // or #$11,b
        imm(0x017F83, 0, AluOp::Eor, 0x3F, Acc::A, 1); // eor #$3f,a
        imm(0x0140C8, 0x654321, AluOp::Add, 0x654321, Acc::B, 2); // add #$654321,b
        imm(0x0140C5, 0x0ABCDE, AluOp::Cmp, 0x0ABCDE, Acc::A, 2); // cmp #$0abcde,a

        // The single-bit shifts (move field $20).
        assert_eq!(
            decode(0x200022, 0, 0x100),
            Ok((Insn::Asr { dest: Acc::A }, 1))
        );
        assert_eq!(
            decode(0x20002A, 0, 0x100),
            Ok((Insn::Asr { dest: Acc::B }, 1))
        );
        assert_eq!(
            decode(0x200023, 0, 0x100),
            Ok((Insn::Lsr { dest: Acc::A }, 1))
        );
        assert_eq!(
            decode(0x20002B, 0, 0x100),
            Ok((Insn::Lsr { dest: Acc::B }, 1))
        );

        // Control flow and repeat.
        assert_eq!(
            decode(0x0BF080, 0x000134, 0x100),
            Ok((Insn::JsrAbs { target: 0x134 }, 2))
        );
        assert_eq!(decode(0x00000C, 0, 0x100), Ok((Insn::Rts, 1)));
        assert_eq!(decode(0x00008C, 0, 0x100), Ok((Insn::Enddo, 1)));
        assert_eq!(
            decode(0x0604A0, 0, 0x100),
            Ok((Insn::RepImm { count: 4 }, 1))
        );
        assert_eq!(
            decode(0x06C420, 0, 0x100),
            Ok((Insn::RepReg { src: Reg::X0 }, 1))
        );

        // The (Rn) addressing modes (01 move class, Encoding 1 of Table 12-13).
        let mv = |word, space, reg, write, mode, rn| {
            assert_eq!(
                decode(word, 0, 0x100),
                Ok((
                    Insn::MoveRegInd {
                        space,
                        reg,
                        write,
                        mode,
                        rn
                    },
                    1
                )),
                "word {word:06X}"
            );
        };
        mv(0x446000, Space::X, Reg::X0, true, EaMode::NoUpdate, 0); // move x0,x:(r0)
        mv(0x45E000, Space::X, Reg::X1, false, EaMode::NoUpdate, 0); // move x:(r0),x1
        mv(0x445800, Space::X, Reg::X0, true, EaMode::PostInc, 0); // move x0,x:(r0)+
        mv(0x46D000, Space::X, Reg::Y0, false, EaMode::PostDec, 0); // move x:(r0)-,y0
        mv(0x4C4900, Space::Y, Reg::X0, true, EaMode::PostAddN, 1); // move x0,y:(r1)+n1
        mv(0x4CCA00, Space::Y, Reg::X0, false, EaMode::PostAddN, 2); // move y:(r2)+n2,x0
        mv(0x444300, Space::X, Reg::X0, true, EaMode::PostSubN, 3); // move x0,x:(r3)-n3
        mv(0x47EC00, Space::X, Reg::Y1, false, EaMode::DispAddN, 4); // move x:(r4+n4),y1
        mv(0x4E4500, Space::Y, Reg::Y0, true, EaMode::PostSubN, 5); // move y0,y:(r5)-n5
        mv(0x457E00, Space::X, Reg::X1, true, EaMode::PreDec, 6); // move x1,x:-(r6)

        // The B-side readouts and the AGU/accumulator immediate destinations.
        assert_eq!(
            decode(0x537000, 0x000210, 0x100),
            Ok((
                Insn::MoveAbsLong {
                    space: Space::X,
                    reg: Reg::B2,
                    write: true,
                    addr: 0x210
                },
                2
            ))
        );
        assert_eq!(
            decode(0x5D7000, 0x000211, 0x100),
            Ok((
                Insn::MoveAbsLong {
                    space: Space::Y,
                    reg: Reg::B1,
                    write: true,
                    addr: 0x211
                },
                2
            ))
        );
        assert_eq!(
            decode(0x60F400, 0x000200, 0x100),
            Ok((
                Insn::MoveImmLong {
                    dest: Reg::R(0),
                    imm: 0x200
                },
                2
            ))
        );
        assert_eq!(
            decode(0x56F400, 0x123456, 0x100),
            Ok((
                Insn::MoveImmLong {
                    dest: Reg::AccA,
                    imm: 0x123456
                },
                2
            ))
        );
        assert_eq!(
            decode(0x380400, 0, 0x100),
            Ok((
                Insn::MoveImmShort {
                    dest: Reg::N(0),
                    imm: 0x04
                },
                1
            ))
        );
        assert_eq!(
            decode(0x2E0500, 0, 0x100),
            Ok((
                Insn::MoveImmShort {
                    dest: Reg::AccA,
                    imm: 0x05
                },
                1
            ))
        );
        assert_eq!(
            decode(0x351000, 0, 0x100),
            Ok((
                Insn::MoveImmShort {
                    dest: Reg::R(5),
                    imm: 0x10
                },
                1
            ))
        );
        assert_eq!(
            decode(0x3F3F00, 0, 0x100),
            Ok((
                Insn::MoveImmShort {
                    dest: Reg::N(7),
                    imm: 0x3F
                },
                1
            ))
        );
    }

    /// Accumulator-PART move destinations are outside subset v0 — a typed stop at decode,
    /// never a guessed translation (and never the old unreachable arm).
    #[test]
    fn refuses_accumulator_part_move_destinations_by_name() {
        // move #$5,a1 — the pinned assembler's $2C0500.
        assert!(matches!(
            decode(0x2C0500, 0, 0x100),
            Err(ModelStop::UnsupportedInsn { .. })
        ));
        // move #$123456,b2 — $4BF400 would decode as MoveImmLong to B2.
        assert!(matches!(
            decode(0x4BF400, 0x123456, 0x100),
            Err(ModelStop::UnsupportedInsn { .. })
        ));
        // An AGU register as the data end of an (Rn) move: move x:(r0),r2 = $62E000.
        assert!(matches!(
            decode(0x62E000, 0, 0x100),
            Err(ModelStop::UnsupportedInsn { .. })
        ));
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
