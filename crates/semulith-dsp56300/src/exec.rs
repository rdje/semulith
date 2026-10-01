//! Semantics for subset v0 — the definitional interpreter. Each rule cites its manual
//! source; the condition-code rules are FM Table 5-1 (reset/default scaling mode, which
//! subset v0 never leaves: S1 = S0 = 0), cross-checked against the reference's observed
//! end-state (`sr c00310` after the demo guest pins U = NOT(bit47 XOR bit46) — the manual
//! text's "U = (Bit 47 xor Bit 46)" is a known PDF-extraction inversion of its own prose
//! "set if the two MSBs are identical", and the differential harness is the arbiter).
//!
//! Measured against the pinned reference (slice 4, the alu/shift/jsr guests):
//! - MOVE of A1/B1 to memory is a RAW MSP read — the shifter/limiter sits on the
//!   whole-accumulator (A/B) read path, not the A1/B1 path (alu guest: `move a1,x:` with
//!   A2=0, A1=$FE00FF stores $FE00FF and L stays clear). A2/B2 read as the sign-extended
//!   extension byte (FM §3.4.1.2, hardware-verified upstream).
//! - MOVE #xx,A/B sign-extends the 8-bit signed fraction through the extension byte
//!   (shift guest: `move #$80,a` leaves A2=$FF) — the FM's "the remaining bits are zeroed"
//!   (13-113) does NOT hold for A2.
//! - RTS restores PC only (FM 13-168: "SSH → PC; SP − 1 → SP") — SR is NOT pulled (that is
//!   RTI's shape, 13-167); the jsr guest pins it (U survives both returns).

use crate::decode::{Acc, AluOp, AluSrc, EaMode, Insn, MulPair, Reg, Space};
use crate::machine::{s24, s56};
use crate::machine::{Machine, ModelStop, MASK24, MASK56, P_WORDS};

// CCR bit positions in SR (FM Table 5-1 / Figure 12-6: S L E U N Z V C in bits 7-0). S has
// no writer in subset v0 (it sets on whole-accumulator bus reads, which v0 does not decode)
// and names no constant here.
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
///
/// S is deliberately NOT computed here: the standard definition (Table 5-1) sets S when an
/// accumulator is READ to the XDB/YDB bus, and subset v0 decodes no whole-accumulator bus
/// read (the A1/A2/B1/B2 move paths do not carry it — measured on the pinned reference,
/// which updates S only in its accumulator-read helper). An ALU result in the "data growth"
/// range does NOT set S (the shift guest pins this: `asr` of a negative accumulator).
fn ccr_standard(m: &mut Machine, res: u64, logical: bool) {
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

/// The 24-bit-operation CCR update (AND/OR/EOR 13-11/13-68/13-150, LSR 13-95): N = result
/// bit 47, Z = bits 47-24 all zero, V always cleared. E, U, S, L and C are UNCHANGED — the
/// per-instruction CCR figures exempt them from the standard definition.
fn ccr_logic24(m: &mut Machine, res_msp: u32) {
    m.sr = if res_msp & 0x80_0000 != 0 {
        m.sr | CCR_N
    } else {
        m.sr & !CCR_N
    };
    m.sr = if res_msp == 0 {
        m.sr | CCR_Z
    } else {
        m.sr & !CCR_Z
    };
    m.sr &= !CCR_V;
}

fn acc_mut(m: &mut Machine, acc: Acc) -> &mut u64 {
    match acc {
        Acc::A => &mut m.a,
        Acc::B => &mut m.b,
    }
}

/// The 56-bit shape of a data-ALU source operand: a 24-bit word is sign-extended into the
/// extension byte and zero-filled below the MSP (CMP's description, 13-44); a 48-bit long
/// word sign-extends from bit 47; an accumulator is taken whole.
fn alu_source(m: &Machine, src: AluSrc, dest: Acc) -> u64 {
    let word = |v: u32| ((s24(v) as i64) << 24) as u64 & MASK56;
    let long = |hi: u32, lo: u32| {
        let v = ((hi as u64) << 24) | u64::from(lo);
        if v & (1 << 47) != 0 {
            v | (0xFFu64 << 48)
        } else {
            v
        }
    };
    match src {
        AluSrc::X0 => word(m.x0),
        AluSrc::X1 => word(m.x1),
        AluSrc::Y0 => word(m.y0),
        AluSrc::Y1 => word(m.y1),
        AluSrc::LongX => long(m.x1, m.x0),
        AluSrc::LongY => long(m.y1, m.y0),
        AluSrc::OtherAcc => match dest {
            Acc::A => m.b,
            Acc::B => m.a,
        },
    }
}

/// ADD/SUB/CMP (13-7/13-172/13-44): 56-bit two's-complement arithmetic. V is the signed
/// overflow of the 56-bit result; C is the carry out of bit 55 for ADD, the borrow for
/// SUB/CMP (Table 5-1). CMP updates the CCR without storing the result.
fn alu_arith(m: &mut Machine, op: AluOp, s: u64, dest: Acc) {
    let d = *acc_mut(m, dest);
    let (wrapped, v, c) = if op == AluOp::Add {
        let sum = d as u128 + s as u128;
        let w = sum as u64 & MASK56;
        let signed = s56(d) as i128 + s56(s) as i128;
        (w, signed != i128::from(s56(w)), (sum >> 56) != 0)
    } else {
        let diff = s56(d) as i128 - s56(s) as i128;
        let w = diff as u64 & MASK56;
        (w, diff != i128::from(s56(w)), d < s)
    };
    if op != AluOp::Cmp {
        *acc_mut(m, dest) = wrapped;
    }
    ccr_standard(m, wrapped, false);
    set_v(m, v);
    set_c(m, c);
}

/// AND/OR/EOR (13-11/13-150/13-68): 24-bit logical operations on bits 47-24 of the
/// destination; the extension byte and the LSP are NOT affected.
fn alu_logic(m: &mut Machine, op: AluOp, s: u64, dest: Acc) {
    let s_msp = ((s >> 24) as u32) & MASK24;
    let acc = acc_mut(m, dest);
    let msp = ((*acc >> 24) as u32) & MASK24;
    let r = match op {
        AluOp::And => msp & s_msp,
        AluOp::Or => msp | s_msp,
        AluOp::Eor => msp ^ s_msp,
        _ => unreachable!("alu_logic is AND/OR/EOR only"),
    };
    // Replace bits 47-24 only: keep the extension byte (55-48) and the LSP (23-0) —
    // AND/OR/EOR write the MSP alone (measured: the reference's logical ops store only
    // A1/B1; the FM's "the remaining bits are not affected" holds for A2 AND A0 here).
    *acc = (*acc & 0x00FF_0000_00FF_FFFF) | (u64::from(r) << 24);
    ccr_logic24(m, r);
}

/// Dispatch one data-ALU core operation on a 56-bit source operand.
fn alu_op(m: &mut Machine, op: AluOp, s: u64, dest: Acc) {
    match op {
        AluOp::Add | AluOp::Sub | AluOp::Cmp => alu_arith(m, op, s, dest),
        _ => alu_logic(m, op, s, dest),
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

/// The extension-byte readout: the 8 LSBs of the bus carry A2/B2, with bits 8-23 the sign
/// extension of its bit 7 (FM §3.4.1.2; no limiting on this path).
fn ext_read(acc: u64) -> u32 {
    let ext = ((acc >> 48) & 0xFF) as u32;
    if ext & 0x80 != 0 {
        ext | 0xFF_FF00
    } else {
        ext
    }
}

/// Read a register onto the data bus for a move. Measured readout rules (the module
/// header's list): A1/B1 read the MSP RAW (the shifter/limiter lives on the
/// whole-accumulator path, which subset v0 does not decode); A2/B2 sign-extend the
/// extension byte.
fn bus_read(m: &mut Machine, reg: Reg) -> u32 {
    match reg {
        Reg::X0 => m.x0,
        Reg::X1 => m.x1,
        Reg::Y0 => m.y0,
        Reg::Y1 => m.y1,
        Reg::A1 => ((m.a >> 24) as u32) & MASK24,
        Reg::B1 => ((m.b >> 24) as u32) & MASK24,
        Reg::A2 => ext_read(m.a),
        Reg::B2 => ext_read(m.b),
        Reg::AccA | Reg::AccB | Reg::R(_) | Reg::N(_) => {
            unreachable!("decode names only data registers on the move bus")
        }
    }
}

/// A 24-bit MSP value as a full accumulator: sign extension into the extension byte,
/// zeroed LSP (the accumulator-destination rule of the immediate/absolute moves).
fn acc_from_msp(v: u32) -> u64 {
    ((s24(v) as i64) << 24) as u64 & MASK56
}

fn bus_write(m: &mut Machine, reg: Reg, value: u32) {
    let value = value & MASK24;
    match reg {
        Reg::X0 => m.x0 = value,
        Reg::X1 => m.x1 = value,
        Reg::Y0 => m.y0 = value,
        Reg::Y1 => m.y1 = value,
        Reg::AccA => m.a = acc_from_msp(value),
        Reg::AccB => m.b = acc_from_msp(value),
        Reg::R(i) => m.r[i] = value,
        Reg::N(i) => m.n[i] = value,
        // Accumulator parts as move DESTINATIONS are not in subset v0 (the
        // accumulator-write readout rules land with the guest that needs them); decode
        // refuses them.
        Reg::A1 | Reg::A2 | Reg::B1 | Reg::B2 => {
            unreachable!("decode refuses accumulator-part move destinations")
        }
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

/// The linear effective address and the address-register update (Effective Addressing Mode
/// Encoding 1, Table 12-13). Subset v0 models linear addressing only: a mode register other
/// than `$FFFFFF` selects modulo/reverse-carry arithmetic, which is outside the subset — a
/// named stop, never a guessed wrap.
fn effective_addr(m: &mut Machine, mode: EaMode, rn: usize) -> Result<u32, ModelStop> {
    if m.m[rn] != MASK24 {
        return Err(ModelStop::Input(format!(
            "M{rn} = {:06X} selects modulo/reverse-carry addressing — outside subset v0",
            m.m[rn]
        )));
    }
    let base = m.r[rn];
    let n = m.n[rn];
    let (ea, update) = match mode {
        EaMode::NoUpdate => (base, None),
        EaMode::PostInc => (base, Some(base.wrapping_add(1))),
        EaMode::PostDec => (base, Some(base.wrapping_sub(1))),
        EaMode::PostAddN => (base, Some(base.wrapping_add(n))),
        EaMode::PostSubN => (base, Some(base.wrapping_sub(n))),
        EaMode::DispAddN => (base.wrapping_add(n), None),
        EaMode::PreDec => {
            let a = base.wrapping_sub(1);
            (a, Some(a))
        }
    };
    if let Some(a) = update {
        m.r[rn] = a & MASK24;
    }
    Ok(ea & MASK24)
}

/// The loop-exit unwind (FM §13 DO "End of Loop" / ENDDO 13-67): LF restored from SSL's
/// bit 15 and the PC/SR level purged, then LA and LC restored from the next level.
fn loop_unwind(m: &mut Machine) {
    let stacked_lf = m.ssl() & (1 << 15);
    m.sr = (m.sr & !(1 << 15)) | stacked_lf;
    m.pop();
    let (old_la, old_lc) = m.pop();
    m.la = old_la;
    m.lc = old_lc;
}

/// REP #xxx / REP S (13-160): LC → TEMP; the count → LC; the following single-word,
/// non-control instruction executes count times (a zero count repeats 65,536 times — the
/// REP page's own rule), LC decrementing after each execution; TEMP → LC. The FM's
/// restriction list (A.3.8) forbids repeating two-word or program-flow instructions, and
/// REP at or next to LA is restricted — a guest that tries either is a typed input stop,
/// never a guessed behaviour.
fn rep(m: &mut Machine, rep_addr: u32, count: u32) -> Result<(), ModelStop> {
    let sub_addr = rep_addr + 1;
    let w0 = *m.p.get(sub_addr as usize).ok_or(ModelStop::OutOfWindow {
        space: 'P',
        addr: sub_addr,
    })?;
    let w1 = m.p.get(sub_addr as usize + 1).copied().unwrap_or(0);
    let (sub, words) = crate::decode::decode(w0, w1, sub_addr)?;
    if words != 1
        || matches!(
            sub,
            Insn::JmpAbs { .. }
                | Insn::JsrAbs { .. }
                | Insn::Rts
                | Insn::DoImm { .. }
                | Insn::Enddo
                | Insn::RepImm { .. }
                | Insn::RepReg { .. }
        )
    {
        return Err(ModelStop::Input(
            "REP may repeat only a single-word, non-control instruction (FM A.3.8)".into(),
        ));
    }
    if m.lf() && (rep_addr == m.la || sub_addr == m.la) {
        return Err(ModelStop::Input(
            "REP at or next to the loop-end address LA is restricted (FM §13 REP)".into(),
        ));
    }
    let n = if count == 0 { 65_536 } else { count };
    let temp = m.lc;
    m.lc = n;
    for _ in 0..n {
        // The repeated instruction never redirects control flow (restricted above), so its
        // next-pc is discarded; each repetition counts as a step, like a DO-loop pass.
        execute(m, sub, sub_addr, sub_addr + 1)?;
        m.lc -= 1;
        m.steps += 1;
    }
    m.lc = temp;
    Ok(())
}

/// Execute one decoded instruction. Returns the address of the next instruction to fetch
/// before the hardware loop's end-of-pass rule runs (that rule lives in `step`).
fn execute(m: &mut Machine, insn: Insn, fetch_addr: u32, next_pc: u32) -> Result<u32, ModelStop> {
    let mut next_pc = next_pc;
    match insn {
        Insn::Nop => {}
        Insn::MoveImmShort { dest, imm } => {
            // FM §3.4.1.3 / 13-113: the 8-bit short immediate's placement is
            // destination-class semantics — a signed fraction into the 8 MSBs for
            // X0/X1/Y0/Y1 (bits 23-16) and the whole accumulators (bits 47-40,
            // sign-extended through the extension byte — measured, the module header);
            // an unsigned integer into the 8 LSBs for the AGU R/N registers.
            match dest {
                Reg::AccA => m.a = acc_from_msp(u32::from(imm) << 16),
                Reg::AccB => m.b = acc_from_msp(u32::from(imm) << 16),
                Reg::R(i) => m.r[i] = u32::from(imm),
                Reg::N(i) => m.n[i] = u32::from(imm),
                _ => bus_write(m, dest, u32::from(imm) << 16),
            }
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
        Insn::MoveRegInd {
            space,
            reg,
            write,
            mode,
            rn,
        } => {
            let ea = effective_addr(m, mode, rn)?;
            if write {
                let value = bus_read(m, reg);
                mem_write(m, space, ea, value)?;
            } else {
                let value = mem_word(m, space, ea)?;
                bus_write(m, reg, value);
            }
        }
        Insn::AluReg { op, src, dest } => {
            let s = alu_source(m, src, dest);
            alu_op(m, op, s, dest);
        }
        Insn::AluImmShort { op, imm, dest } => {
            // The 6-bit immediate is an unsigned integer, right-aligned and zero-filled
            // to a 24-bit source word (ADD's description, 13-7) — as a fraction, the
            // 56-bit operand is imm << 24.
            alu_op(m, op, u64::from(imm) << 24, dest);
        }
        Insn::AluImmLong { op, imm, dest } => {
            let s = acc_from_msp(imm);
            alu_op(m, op, s, dest);
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
        Insn::Asr { dest } => {
            // ASR D (13-16): the full 56-bit accumulator arithmetically right by one; the
            // MSB is held, bit 0 → C; V is always cleared; S/E/U/N/Z per the standard
            // definition.
            let before = *acc_mut(m, dest);
            let result = ((s56(before) >> 1) as u64) & MASK56;
            *acc_mut(m, dest) = result;
            ccr_standard(m, result, false);
            set_v(m, false);
            set_c(m, before & 1 != 0);
        }
        Insn::Lsr { dest } => {
            // LSR D (13-95): a 24-bit operation — bits 47-24 shift right by one, bit 24 →
            // C, a 0 into bit 47; the extension byte and the LSP are unaffected.
            let acc = acc_mut(m, dest);
            let msp = ((*acc >> 24) as u32) & MASK24;
            let c = msp & 1 != 0;
            let r = msp >> 1;
            *acc = (*acc & 0x00FF_0000_00FF_FFFF) | (u64::from(r) << 24);
            ccr_logic24(m, r);
            set_c(m, c);
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
        Insn::JsrAbs { target } => {
            // FM 13-89: SP+1 → SP; PC → SSH; SR → SSL; then the jump.
            m.push(next_pc, m.sr)?;
            next_pc = target;
        }
        Insn::Rts => {
            // FM 13-168: SSH → PC; SP-1 → SP. SR is NOT pulled (that is RTI's shape).
            let (pc, _sr) = m.pop();
            next_pc = pc;
        }
        Insn::Enddo => loop_unwind(m),
        Insn::RepImm { count } => {
            rep(m, fetch_addr, u32::from(count))?;
            next_pc = fetch_addr + 2;
        }
        Insn::RepReg { src } => {
            let count = match src {
                Reg::X0 => m.x0,
                Reg::X1 => m.x1,
                Reg::Y0 => m.y0,
                Reg::Y1 => m.y1,
                _ => unreachable!("decode restricts REP S to X0/X1/Y0/Y1"),
            };
            rep(m, fetch_addr, count)?;
            next_pc = fetch_addr + 2;
        }
    }
    Ok(next_pc)
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
    let mut next_pc = execute(m, insn, fetch_addr, fetch_addr + u32::from(words))?;

    // The hardware loop's end-of-pass rule (FM §13 DO): when the instruction just fetched
    // was at LA and LF is set, either loop back (LC ≠ 1: LC-1 → LC, SSH → PC) or exit
    // (LC = 1: SSL's LF alone into SR, LA and LC restored from the stack, SP − 2).
    if m.lf() && fetch_addr == m.la {
        if m.lc != 1 {
            m.lc -= 1;
            next_pc = m.ssh();
        } else {
            loop_unwind(m);
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

    /// The alu guest's end-state, hand-derived from the FM (P3-BREADTH.4 slice 4): the
    /// arithmetic chain (add/sub/cmp leave A at $010000-MSP, C pinned by the cmp borrow),
    /// the 24-bit logical ops (MSP only, A2/A0 untouched, N/Z/V only), the
    /// other-accumulator and 48-bit long-word sources. The words are the pinned
    /// assembler's output for `profiles/dsp56300-lab-v0/guests/alu.a56`.
    #[test]
    fn the_alu_guest_reaches_its_manual_derived_end_state() {
        let m = run(
            &[
                (0x100, 0x2E0100), // move #$010000,a (short form)
                (0x101, 0x44F400),
                (0x102, 0x7FFFFF), // move #$7fffff,x0
                (0x103, 0x200040), // add x0,a
                (0x104, 0x200044), // sub x0,a
                (0x105, 0x200045), // cmp x0,a — borrow: C=1, N=1
                (0x106, 0x0140C6),
                (0x107, 0xFF00FF), // and #$ff00ff,a
                (0x108, 0x0140C2),
                (0x109, 0x00FF00), // or #$00ff00,a
                (0x10A, 0x0140C3),
                (0x10B, 0xFFFFFF), // eor #$ffffff,a → A1 = FE00FF, N=1
                (0x10C, 0x547000),
                (0x10D, 0x000210), // move a1,x:$210 — RAW read (no limiting)
                (0x10E, 0x527000),
                (0x10F, 0x000211), // move a2,x:$211
                (0x110, 0x57F400),
                (0x111, 0x123456), // move #$123456,b
                (0x112, 0x017F8C), // sub #$3f,b → B1 = 123417
                (0x113, 0x0140CD),
                (0x114, 0x123417), // cmp #$123417,b → Z=1
                (0x115, 0x200010), // add b,a — the other-accumulator source
                (0x116, 0x45F400),
                (0x117, 0x000100), // move #$100,x1
                (0x118, 0x44F400),
                (0x119, 0x000200), // move #$200,x0 — X = x1:x0
                (0x11A, 0x200020), // add x,a — the 48-bit long-word source
                (0x11B, 0x547000),
                (0x11C, 0x000212), // move a1,x:$212
                (0x11D, 0x527000),
                (0x11E, 0x000213), // move a2,x:$213
                (0x11F, 0x557000),
                (0x120, 0x000214), // move b1,x:$214
                (0x121, 0x0AF080),
                (0x122, 0x000123), // jmp done
            ],
            21,
        );
        assert_eq!(m.pc, 0x123);
        assert_eq!(m.sr, 0xC0_0330, "E|U from the final add; C cleared by it");
        // A = 00FE00FF000000 + (B1 << 24) + X1:X0 = 01:103616:000200.
        assert_eq!(m.a, 0x01_1036_1600_0200);
        assert_eq!(m.b, 0x00_1234_1700_0000);
        assert_eq!(m.x0, 0x000200);
        assert_eq!(m.x1, 0x000100);
        assert_eq!(
            m.x[0x210], 0xFE00FF,
            "A1 stored raw — no limiter on this path"
        );
        assert_eq!(
            m.x[0x211], 0,
            "A2 readout of $00 (written, equals the seed)"
        );
        assert_eq!(m.x[0x212], 0x103616);
        assert_eq!(m.x[0x213], 0x000001, "A2 = $01 zero-extended");
        assert_eq!(m.x[0x214], 0x123417);
    }

    /// The shift guest's end-state, hand-derived: ASR is the 56-bit arithmetic shift (MSB
    /// held, bit 0 → C, V cleared); LSR is a 24-bit shift of bits 47-24 ONLY — B2 = $FF
    /// survives both LSRs (the discriminator against a 56-bit reading). The negative
    /// short-immediate move sign-extends into A2 (measured; the FM prose says "zeroed").
    #[test]
    fn the_shift_guest_reaches_its_manual_derived_end_state() {
        let m = run(
            &[
                (0x100, 0x2E0300), // move #$3,a → A = 03:0000 at bits 47-40
                (0x101, 0x200022), // asr a
                (0x102, 0x200022), // asr a
                (0x103, 0x2E8000), // move #$80,a → A = FF:800000:000000 (sign-extended)
                (0x104, 0x200022), // asr a → A = FF:C00000:000000, N=1
                (0x105, 0x57F400),
                (0x106, 0x800003), // move #$800003,b → B = FF:800003:000000
                (0x107, 0x20002B), // lsr b → B1 = 400001, C=1, B2 stays FF
                (0x108, 0x20002B), // lsr b → B1 = 200000, C=1
                (0x109, 0x20003A), // asl b → B = FE:400000:000000, C=1
                (0x10A, 0x547000),
                (0x10B, 0x000210), // move a1,x:$210
                (0x10C, 0x527000),
                (0x10D, 0x000211), // move a2,x:$211 → FFFFFF (sign-extended byte)
                (0x10E, 0x557000),
                (0x10F, 0x000212), // move b1,x:$212
                (0x110, 0x537000),
                (0x111, 0x000213), // move b2,x:$213 → FFFFFE
                (0x112, 0x0AF080),
                (0x113, 0x000114), // jmp done
            ],
            14,
        );
        assert_eq!(m.pc, 0x114);
        assert_eq!(
            m.sr, 0xC0_0329,
            "E|N|C from the final asl; S never set (no acc bus read)"
        );
        assert_eq!(m.a, 0xFF_C000_0000_0000);
        assert_eq!(m.b, 0xFE_4000_0000_0000);
        assert_eq!(m.x[0x210], 0xC00000);
        assert_eq!(m.x[0x211], 0xFFFFFF);
        assert_eq!(m.x[0x212], 0x400000);
        assert_eq!(m.x[0x213], 0xFFFFFE);
    }

    /// The rn guest's end-state, hand-derived: every linear (Rn) mode's address and update
    /// arithmetic (Encoding 1, Table 12-13), both move directions, both spaces.
    #[test]
    fn the_rn_guest_reaches_its_manual_derived_end_state() {
        let m = run(
            &[
                (0x100, 0x60F400),
                (0x101, 0x000200), // move #$200,r0
                (0x102, 0x244100), // move #$41,x0 → 410000
                (0x103, 0x445800), // move x0,x:(r0)+  → x:$200, r0=201
                (0x104, 0x244200),
                (0x105, 0x445800), // move x0,x:(r0)+  → x:$201 = 420000, r0=202
                (0x106, 0x244300),
                (0x107, 0x445800), // → x:$202 = 430000, r0=203
                (0x108, 0x244400),
                (0x109, 0x446000), // move x0,x:(r0)   → x:$203 = 440000
                (0x10A, 0x380200), // move #$2,n0
                (0x10B, 0x46C000), // move x:(r0)-n0,y0 → y0 = x:$203, r0=201
                (0x10C, 0x47E800), // move x:(r0+n0),y1 → y1 = x:$203, r0=201
                (0x10D, 0x44F800), // move x:-(r0),x0 → r0=200, x0 = x:$200
                (0x10E, 0x45D800), // move x:(r0)+,x1 → x1 = x:$200, r0=201
                (0x10F, 0x61F400),
                (0x110, 0x000300), // move #$300,r1
                (0x111, 0x390800), // move #$8,n1
                (0x112, 0x4E4900), // move y0,y:(r1)+n1 → y:$300, r1=308
                (0x113, 0x4E4100), // move y0,y:(r1)-n1 → y:$308, r1=300
                (0x114, 0x4CE100), // move y:(r1),x0 → x0 = 440000
                (0x115, 0x0AF080),
                (0x116, 0x000117), // jmp done
            ],
            20,
        );
        assert_eq!(m.pc, 0x117);
        assert_eq!(m.sr, 0xC0_0300, "moves touch no CCR bit");
        assert_eq!(m.x[0x200], 0x410000);
        assert_eq!(m.x[0x201], 0x420000);
        assert_eq!(m.x[0x202], 0x430000);
        assert_eq!(m.x[0x203], 0x440000);
        assert_eq!(m.y[0x300], 0x440000);
        assert_eq!(m.y[0x308], 0x440000);
        assert_eq!((m.r[0], m.r[1]), (0x201, 0x300));
        assert_eq!((m.n[0], m.n[1]), (2, 8));
        assert_eq!((m.x0, m.x1), (0x440000, 0x410000));
        assert_eq!((m.y0, m.y1), (0x440000, 0x440000));
    }

    /// The rep guest's end-state, hand-derived: REP #xxx and REP S repeat their single-word
    /// shadow (LC saved/restored around the count), REP nests inside DO away from LA, and
    /// ENDDO unwinds the DO #10 loop on its first pass (LF cleared, LA/LC restored, SP − 2).
    #[test]
    fn the_rep_guest_reaches_its_manual_derived_end_state() {
        let m = run(
            &[
                (0x100, 0x60F400),
                (0x101, 0x000200), // move #$200,r0
                (0x102, 0x245500), // move #$55,x0 → 550000
                (0x103, 0x0604A0), // rep #4
                (0x104, 0x445800), //   move x0,x:(r0)+ ×4 → x:$200-$203
                (0x105, 0x45F400),
                (0x106, 0x000002), // move #>$2,x1 → x1 = 2 (long form forced)
                (0x107, 0x06C520), // rep x1
                (0x108, 0x445800), //   move x0,x:(r0)+ ×2 → x:$204-$205
                (0x109, 0x060280),
                (0x10A, 0x00010D), // do #2,outerl (LA = 0x10D)
                (0x10B, 0x0603A0), // rep #3
                (0x10C, 0x445800), //   move x0,x:(r0)+ ×3 per pass → $206-$208, $209-$20B
                (0x10D, 0x000000), // outerl: nop (LA)
                (0x10E, 0x000000), // nop
                (0x10F, 0x060A80),
                (0x110, 0x000112), // do #10,early (LA = 0x112, the enddo)
                (0x111, 0x445800), //   move x0,x:(r0)+ → x:$20C
                (0x112, 0x00008C), //   enddo — unwinds the loop on pass 1
                (0x113, 0x445800), // early: move x0,x:(r0)+ → x:$20D (LF clear)
                (0x114, 0x0AF080),
                (0x115, 0x000116), // jmp done
            ],
            16,
        );
        assert_eq!(m.pc, 0x116);
        assert_eq!(m.sr, 0xC0_0300, "moves and loop machinery touch no CCR bit");
        assert_eq!(m.r[0], 0x20E, "14 stores from $200");
        for addr in 0x200..=0x20D {
            assert_eq!(m.x[addr], 0x550000, "x:{addr:03X}");
        }
        assert_eq!(m.la, MASK24, "LA restored");
        assert_eq!(
            m.lc, 0,
            "LC restored (REP's TEMP round-trip and ENDDO's unwind)"
        );
        assert_eq!(m.sp, 0);
        assert!(!m.lf());
        let slots = m.stack_slots();
        assert_eq!(slots[1], [MASK24, 0]);
        assert_eq!(
            slots[2],
            [0x000111, 0xC0_0300],
            "the DO #10 loop's PC/SR level"
        );
    }

    /// The jsr guest's end-state, hand-derived: JSR pushes PC/SR; RTS pulls PC ONLY (FM
    /// 13-168 — SR stays; the U bit set inside the nested call survives both returns).
    #[test]
    fn the_jsr_guest_reaches_its_manual_derived_end_state() {
        let m = run(
            &[
                (0x100, 0x241000), // move #$10,x0 → 100000
                (0x101, 0x0BF080),
                (0x102, 0x00010A), // jsr sub
                (0x103, 0x252000), // move #$20,x1 → 200000 (after the return)
                (0x104, 0x447000),
                (0x105, 0x000230), // move x0,x:$230
                (0x106, 0x457000),
                (0x107, 0x000231), // move x1,x:$231
                (0x108, 0x0AF080),
                (0x109, 0x000113), // jmp done
                (0x10A, 0x56F400),
                (0x10B, 0x000777), // sub: move #$000777,a
                (0x10C, 0x0BF080),
                (0x10D, 0x000111), // jsr inner
                (0x10E, 0x547000),
                (0x10F, 0x000232), // move a1,x:$232
                (0x110, 0x00000C), // rts
                (0x111, 0x014180), // inner: add #$1,a → A1 = 000778, U=1
                (0x112, 0x00000C), // rts
            ],
            12,
        );
        assert_eq!(m.pc, 0x113);
        assert_eq!(
            m.sr, 0xC0_0310,
            "U set by the inner add survives both RTSes"
        );
        assert_eq!(m.a, 0x00_0007_7800_0000);
        assert_eq!(m.sp, 0);
        let slots = m.stack_slots();
        assert_eq!(
            slots[1],
            [0x000103, 0xC0_0300],
            "jsr sub's return PC and SR"
        );
        assert_eq!(
            slots[2],
            [0x00010E, 0xC0_0300],
            "jsr inner's return PC and SR"
        );
        assert_eq!(m.x[0x230], 0x100000);
        assert_eq!(m.x[0x231], 0x200000);
        assert_eq!(m.x[0x232], 0x000778);
    }
}
