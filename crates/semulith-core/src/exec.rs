//! The definitional interpreter — `P1-LAB.8`, task card T006: the first execution slice.
//!
//! [`step`] is the evaluator the whole project exists for: it executes ONE instruction of the
//! profile against the architectural state and the environment boundary, and reports what
//! happened in `.5`'s typed outcome families. The semantics it executes are exactly the `Sem`
//! effect trees lowered from `definitions/riscv/rv64i.sem.sexp` into `.6`'s `definition` — the
//! semantics DATA stays the one executable owner of every rule (OWN-01); this module is its
//! evaluator, not a second implementation. There is no handwritten per-instruction behavior
//! anywhere: decode, operand extraction and evaluation all read the generated tables.
//!
//! The reporting rules this module implements, each named by its source rule:
//!
//! - **Fetch** — one 32-bit `Fetch` at the pc (D-FETCH-IMPLICIT). An access-fault answer is
//!   `InstructionAccessFault` reported AT the pc, including when the pc is the target of a
//!   jump (`REQ-D-FETCH-FAULT-REPORT`).
//! - **Decode** — a word no entry matches is the reserved case, reported as
//!   [`UndefinedCase::ReservedDecode`] (`D-RESERVED-DECODE`): the architecture declares the
//!   behavior UNSPECIFIED, so the model records the case as what the source classifies it as
//!   and never auto-converts it into a trap. Conversion is the diagnostic policy's explicit
//!   act, one layer up.
//! - **Targets** — a taken branch/jump whose target is not 4-byte aligned raises
//!   `InstructionAddressMisaligned` ON THE BRANCH OR JUMP, `at` the target value
//!   (`REQ-D-IALIGN`, `REQ-D-MISALIGN-REPORT`). A branch that is not taken raises nothing.
//! - **Data access** — a misaligned load/store raises its address-misaligned exception before
//!   the boundary is crossed (D-MISALIGN-DATA: raised, not handled invisibly; alignment is the
//!   instruction layer's rule, and a request the contract forbids must not be formed). An
//!   access outside every declared region is the boundary's `AccessFault` answer, converted
//!   into the matching load/store access-fault — never substituted for anything else
//!   (D-MAIN-VS-IO).
//! - **Requested traps** — `ECALL`/`EBREAK` are `RequestedTrap` events (REQ-D-ECALL-EBREAK),
//!   carried with the cause vocabulary's codes (11 / 3). A tree naming any other cause is a
//!   description defect (`ModelError::InvalidDescription`), never a silently invented trap.
//! - **Model limitations** — everything the model or harness got wrong is `ModelError`
//!   (SEM-02); none of it is ever emitted as a target exception.
//!
//! Widths are explicit everywhere, per the semantics file's own rule — an implicit width is
//! where two models silently disagree. Expression evaluation therefore carries a width
//! alongside every value, with this algebra (the only one under which all 52 effect trees are
//! simultaneously correct, verified against the pinned specification-derived guest
//! expectations and the reference models):
//!
//! - `Lit`/`Reg`/`Pc`/`Xlen` are XLEN-wide (64); an `Imm` carries its composed field width
//!   (12/13/21/20 for imm12/bimm12/jimm20/imm20; 6 or 5 for `shamt`); `Load` carries its
//!   width argument; `Trunc`/`Bits` carry their declared width.
//! - `Sext`/`Zext` extend **from the operand's own width to N** — which is what makes
//!   `(sext 64 (shl (imm imm20) (lit 12)))` the LUI sign-extension from bit 31, and
//!   `(sext 64 (load (lit 8) …))` the LB extension from 8.
//! - A shift whose amount is a literal widens by that amount (LUI's `shl` assembles the
//!   32-bit constant); a computed amount shifts within the left operand's width, and the tree
//!   states any narrowing itself (`trunc 32` on the *W shifts).
//!
//! Progress: an instruction completes as a unit (OB-ENV-PARTIAL-PROGRESS) and the pc advances
//! by 4 only when the effect did not transfer control and did not stop execution — a trap or
//! fault leaves the pc at the instruction that raised it, which is the address a handler
//! would resume from.

use crate::arith;
use crate::definition::{decode, FieldDef, InsnDef, Sem, FIELDS};
use crate::env::{AccessWidth, BoundaryError, Environment, Failure, Request, Response};
use crate::outcome::{
    Advance, ExceptionCause, ModelError, RequestedTrapKind, StepOutcome, TargetEvent, UndefinedCase,
};
use crate::state::ArchitecturalState;

/// Execute the instruction at the current pc: fetch through the environment, decode, evaluate
/// the semantics-data effect tree. Everything observable about one instruction retires through
/// the returned [`StepOutcome`]; the harness matches on it.
pub fn step(state: &mut ArchitecturalState, env: &mut impl Environment) -> StepOutcome {
    let pc = state.pc();
    let word = match env.request(Request::Fetch { addr: pc }) {
        Ok(Response::Fetch(word)) => word,
        Ok(_) => {
            return StepOutcome::Failed(ModelError::InvalidDescription {
                what: "environment answered a Fetch with a non-fetch response",
            });
        }
        Err(BoundaryError::Target(Failure::AccessFault)) => {
            return StepOutcome::Event(TargetEvent::Exception {
                cause: ExceptionCause::InstructionAccessFault,
                at: pc,
            });
        }
        Err(BoundaryError::Target(Failure::Misaligned)) => {
            // The environment judged the pc misaligned. The model normally holds the
            // IALIGN=32 invariant itself (a misaligned transfer is caught at `SetPc`), but a
            // custom environment may answer this way and the report stays honest.
            return StepOutcome::Event(TargetEvent::Exception {
                cause: ExceptionCause::InstructionAddressMisaligned,
                at: pc,
            });
        }
        Err(BoundaryError::Violation(violation)) => {
            return StepOutcome::Failed(ModelError::ContractViolation(violation));
        }
    };
    let Some(insn) = decode(word) else {
        return StepOutcome::Undefined(UndefinedCase::ReservedDecode { at: pc });
    };
    let operands = match extract_operands(insn, word) {
        Ok(operands) => operands,
        Err(error) => return StepOutcome::Failed(error),
    };
    let mut frame = Frame {
        state,
        env,
        pc,
        operands,
        pc_written: false,
    };
    match frame.run(insn.effect) {
        Ok(_) => {
            let pc_written = frame.pc_written;
            // borrows end here; the default advance is the only pc write the frame did not do
            drop(frame);
            if !pc_written {
                state.set_pc(pc.wrapping_add(4));
            }
            StepOutcome::Advanced(Advance::Completed)
        }
        Err(outcome) => outcome,
    }
}

/// One extracted operand: its name, value and explicit width. Widths ride with values so the
/// evaluator can state `sext`/`zext` without guessing.
type Operand = (&'static str, u64, u32);

/// Extract the operands the encoding declares for this word, applying the binding rule the
/// semantics layer documents (`scripts/check_semantics.py`, re-derived by the generator):
/// a split store immediate reads as one `imm12`, a split branch immediate as one `bimm12`,
/// and either shift field reads as `shamt`. Scattered immediates unscramble per their field's
/// piece table, MSB-first.
fn extract_operands(insn: &InsnDef, word: u32) -> Result<Vec<Operand>, ModelError> {
    let field =
        |name: &str| -> Option<&'static FieldDef> { FIELDS.iter().find(|f| f.name == name) };
    let raw =
        |f: &FieldDef| -> u64 { u64::from(word >> f.lo) & mask_u64(u32::from(f.hi - f.lo + 1)) };

    // The scattered-immediate contribution of one field, placed at its imm-bit offsets.
    let scattered = |f: &FieldDef| -> u64 {
        let mut value = 0u64;
        let mut cursor = u32::from(f.hi - f.lo + 1);
        for &(imm_hi, imm_lo) in f.scatter {
            let width = u32::from(imm_hi - imm_lo + 1);
            cursor -= width;
            let bits = (raw(f) >> cursor) & mask_u64(width);
            value |= bits << imm_lo;
        }
        value
    };

    let mut operands: Vec<Operand> = Vec::with_capacity(insn.operands.len() + 1);
    for &name in insn.operands {
        match name {
            // The hi half of a split immediate owns the composition (the lo half is skipped
            // below); the pair (hi, lo) is adjacent in the operand list by construction.
            "imm12hi" => {
                let hi = field("imm12hi").expect("operand names a declared field");
                let lo = field("imm12lo").expect("operand names a declared field");
                operands.push(("imm12", (raw(hi) << 5) | raw(lo), 12));
            }
            "bimm12hi" => {
                let hi = field("bimm12hi").expect("operand names a declared field");
                let lo = field("bimm12lo").expect("operand names a declared field");
                operands.push(("bimm12", scattered(hi) | scattered(lo), 13));
            }
            "shamtd" => operands.push(("shamt", raw(field("shamtd").expect("declared")), 6)),
            "shamtw" => operands.push(("shamt", raw(field("shamtw").expect("declared")), 5)),
            "imm12lo" | "bimm12lo" => {} // consumed by the hi half
            _ => {
                let Some(f) = field(name) else {
                    // FENCE's fm/pred/succ are declared operands without field ranges — its
                    // rule reads none, so nothing is extracted for them.
                    continue;
                };
                let width = u32::from(f.hi - f.lo + 1);
                let value = if f.scatter.is_empty() {
                    raw(f)
                } else {
                    scattered(f)
                };
                operands.push((name, value, width));
            }
        }
    }
    Ok(operands)
}

fn mask_u64(width: u32) -> u64 {
    if width >= 64 {
        u64::MAX
    } else {
        (1u64 << width) - 1
    }
}

/// The evaluation frame for one step: the state and environment borrows, the executing
/// instruction's address, its extracted operands, and whether a `set-pc` already wrote the pc
/// (the default `pc + 4` advance must not overwrite it).
struct Frame<'a, E: Environment> {
    state: &'a mut ArchitecturalState,
    env: &'a mut E,
    pc: u64,
    operands: Vec<Operand>,
    pc_written: bool,
}

/// Evaluation stopped by something other than a value: a typed target event or a model error,
/// propagated to the step's outcome. This is the only non-local flow; there is no exception
/// mechanism and no family crossing.
type Flow = StepOutcome;

impl<E: Environment> Frame<'_, E> {
    /// Evaluate one tree node. Effects perform their action and return `(0, 64)`; expressions
    /// return `(value, width)`. `Err(flow)` is a target event or model error ending the step.
    fn run(&mut self, sem: &Sem) -> Result<(u64, u32), Flow> {
        match sem {
            Sem::Lit(value) => Ok((*value, 64)),
            Sem::Reg(name) => {
                let index = self.operand(name)?;
                Ok((self.state.read_x(index as u8), 64))
            }
            Sem::Imm(name) => {
                let (_, value, width) = self.operand_full(name)?;
                Ok((value, width))
            }
            Sem::Pc => Ok((self.pc, 64)),
            Sem::Xlen => Ok((64, 64)),
            Sem::Add(a, b) => {
                let (x, wx) = self.run(a)?;
                let (y, wy) = self.run(b)?;
                Ok((arith::add(x, y), wx.max(wy)))
            }
            Sem::Sub(a, b) => {
                let (x, wx) = self.run(a)?;
                let (y, wy) = self.run(b)?;
                Ok((arith::sub(x, y), wx.max(wy)))
            }
            Sem::And(a, b) => {
                let (x, wx) = self.run(a)?;
                let (y, wy) = self.run(b)?;
                Ok((arith::and(x, y), wx.max(wy)))
            }
            Sem::Or(a, b) => {
                let (x, wx) = self.run(a)?;
                let (y, wy) = self.run(b)?;
                Ok((arith::or(x, y), wx.max(wy)))
            }
            Sem::Xor(a, b) => {
                let (x, wx) = self.run(a)?;
                let (y, wy) = self.run(b)?;
                Ok((arith::xor(x, y), wx.max(wy)))
            }
            Sem::Shl(a, b) => {
                let (x, wx) = self.run(a)?;
                let (y, _wy) = self.run(b)?;
                // A literal amount widens by the amount itself (LUI's `shl` assembles a
                // 32-bit constant); a computed amount shifts within the left operand's
                // width, and the tree states any narrowing itself.
                let widened = if let Sem::Lit(_) = b {
                    wx + y as u32
                } else {
                    wx
                };
                Ok((arith::shl(x, y), widened))
            }
            Sem::Shr(a, b) => {
                let (x, wx) = self.run(a)?;
                let (y, _) = self.run(b)?;
                // The shift operates at the left operand's width: the low `wx` bits, zeros
                // brought in above (the tree states any narrowing itself).
                Ok((arith::shr(x & mask_u64(wx), y), wx))
            }
            Sem::Sar(a, b) => {
                let (x, wx) = self.run(a)?;
                let (y, _) = self.run(b)?;
                // Arithmetic: replicate the WIDTH's sign bit (bit wx-1), not bit 63 — after
                // `trunc 32` the u64 carries zeros above bit 31, and an arithmetic shift of
                // the low 32 bits must replicate bit 31. Sign-extending to 64 first makes the
                // ordinary 64-bit sar do exactly that.
                Ok((arith::sar(arith::sext(x, wx), y), wx))
            }
            Sem::Slt(a, b) => {
                let (x, _) = self.run(a)?;
                let (y, _) = self.run(b)?;
                Ok((arith::slt(x, y), 64))
            }
            Sem::Sltu(a, b) => {
                let (x, _) = self.run(a)?;
                let (y, _) = self.run(b)?;
                Ok((arith::sltu(x, y), 64))
            }
            Sem::Eq(a, b) => {
                let (x, _) = self.run(a)?;
                let (y, _) = self.run(b)?;
                Ok((u64::from(x == y), 64))
            }
            Sem::Ne(a, b) => {
                let (x, _) = self.run(a)?;
                let (y, _) = self.run(b)?;
                Ok((u64::from(x != y), 64))
            }
            Sem::Lt(a, b) => {
                let (x, _) = self.run(a)?;
                let (y, _) = self.run(b)?;
                Ok((u64::from((x as i64) < (y as i64)), 64))
            }
            Sem::Ltu(a, b) => {
                let (x, _) = self.run(a)?;
                let (y, _) = self.run(b)?;
                Ok((u64::from(x < y), 64))
            }
            Sem::Ge(a, b) => {
                let (x, _) = self.run(a)?;
                let (y, _) = self.run(b)?;
                Ok((u64::from((x as i64) >= (y as i64)), 64))
            }
            Sem::Geu(a, b) => {
                let (x, _) = self.run(a)?;
                let (y, _) = self.run(b)?;
                Ok((u64::from(x >= y), 64))
            }
            Sem::Trunc(width, v) => {
                let (value, _) = self.run(v)?;
                Ok((value & mask_u64(*width as u32), *width as u32))
            }
            Sem::Sext(width, v) => {
                let (value, from) = self.run(v)?;
                let from = from.min(*width as u32);
                Ok((arith::sext(value, from), *width as u32))
            }
            Sem::Zext(width, v) => {
                let (value, from) = self.run(v)?;
                Ok((value & mask_u64(from.min(*width as u32)), *width as u32))
            }
            Sem::Bits(hi, lo, v) => {
                let (value, _) = self.run(v)?;
                Ok((
                    arith::bits(value, u32::from(*hi), u32::from(*lo)),
                    u32::from(*hi - *lo + 1),
                ))
            }
            Sem::Load(width, _signed, addr) => {
                let (width, _ws) = self.run(width)?;
                let (addr, _) = self.run(addr)?;
                let access = Self::access_width(width)?;
                if !addr.is_multiple_of(access.bytes()) {
                    return Err(StepOutcome::Event(TargetEvent::Exception {
                        cause: ExceptionCause::LoadAddressMisaligned,
                        at: addr,
                    }));
                }
                match self.env.request(Request::Load {
                    width: access,
                    addr,
                }) {
                    Ok(Response::Load(value)) => Ok((value, access.bits())),
                    Ok(_) => Err(StepOutcome::Failed(ModelError::InvalidDescription {
                        what: "environment answered a Load with a non-load response",
                    })),
                    Err(BoundaryError::Target(Failure::AccessFault)) => {
                        Err(StepOutcome::Event(TargetEvent::Exception {
                            cause: ExceptionCause::LoadAccessFault,
                            at: addr,
                        }))
                    }
                    Err(BoundaryError::Target(Failure::Misaligned)) => {
                        Err(StepOutcome::Event(TargetEvent::Exception {
                            cause: ExceptionCause::LoadAddressMisaligned,
                            at: addr,
                        }))
                    }
                    Err(BoundaryError::Violation(violation)) => Err(StepOutcome::Failed(
                        ModelError::ContractViolation(violation),
                    )),
                }
            }
            Sem::Store(width, addr, value) => {
                let (width, _ws) = self.run(width)?;
                let (addr, _) = self.run(addr)?;
                let (value, _) = self.run(value)?;
                let access = Self::access_width(width)?;
                if !addr.is_multiple_of(access.bytes()) {
                    return Err(StepOutcome::Event(TargetEvent::Exception {
                        cause: ExceptionCause::StoreAddressMisaligned,
                        at: addr,
                    }));
                }
                match self.env.request(Request::Store {
                    width: access,
                    addr,
                    data: value,
                }) {
                    Ok(Response::StoreDone) => Ok((0, 64)),
                    Ok(_) => Err(StepOutcome::Failed(ModelError::InvalidDescription {
                        what: "environment answered a Store with a non-store response",
                    })),
                    Err(BoundaryError::Target(Failure::AccessFault)) => {
                        Err(StepOutcome::Event(TargetEvent::Exception {
                            cause: ExceptionCause::StoreAccessFault,
                            at: addr,
                        }))
                    }
                    Err(BoundaryError::Target(Failure::Misaligned)) => {
                        Err(StepOutcome::Event(TargetEvent::Exception {
                            cause: ExceptionCause::StoreAddressMisaligned,
                            at: addr,
                        }))
                    }
                    Err(BoundaryError::Violation(violation)) => Err(StepOutcome::Failed(
                        ModelError::ContractViolation(violation),
                    )),
                }
            }
            Sem::Set(target, value) => {
                let Sem::Reg(name) = target else {
                    return Err(StepOutcome::Failed(ModelError::InvalidDescription {
                        what: "set writes something that is not a register",
                    }));
                };
                let index = self.operand(name)?;
                let (value, _) = self.run(value)?;
                // D-LOAD-X0's general form: writing x0 is architecturally discarded; the
                // state owns that discipline.
                self.state.write_x(index as u8, value);
                Ok((0, 64))
            }
            Sem::SetPc(target) => {
                let (target, _) = self.run(target)?;
                if !target.is_multiple_of(4) {
                    // REQ-D-IALIGN / REQ-D-MISALIGN-REPORT: raised ON the branch or jump, at
                    // the offending target value; the pc stays at the transfer instruction.
                    return Err(StepOutcome::Event(TargetEvent::Exception {
                        cause: ExceptionCause::InstructionAddressMisaligned,
                        at: target,
                    }));
                }
                self.state.set_pc(target);
                self.pc_written = true;
                Ok((0, 64))
            }
            Sem::Seq(steps) => {
                for step in *steps {
                    self.run(step)?;
                }
                Ok((0, 64))
            }
            Sem::Nop => Ok((0, 64)),
            Sem::If(cond, then, else_) => {
                let (cond, _) = self.run(cond)?;
                if cond != 0 {
                    self.run(then)
                } else {
                    self.run(else_)
                }
            }
            Sem::Trap(cause, tval) => {
                let (cause, _) = self.run(cause)?;
                let (tval, _) = self.run(tval)?;
                let kind = match cause {
                    11 => RequestedTrapKind::EnvironmentCall,
                    3 => RequestedTrapKind::Breakpoint,
                    _ => {
                        return Err(StepOutcome::Failed(ModelError::InvalidDescription {
                            what: "trap cause outside the requested-trap vocabulary",
                        }));
                    }
                };
                Err(StepOutcome::Event(TargetEvent::RequestedTrap {
                    kind,
                    at: tval,
                }))
            }
        }
    }

    fn operand(&self, name: &str) -> Result<u64, Flow> {
        Ok(self.operand_full(name)?.1)
    }

    fn operand_full(&self, name: &str) -> Result<Operand, Flow> {
        self.operands
            .iter()
            .copied()
            .find(|(n, _, _)| *n == name)
            .ok_or(StepOutcome::Failed(ModelError::InvalidDescription {
                what: "tree reads an operand the encoding does not provide",
            }))
    }

    /// The tree's width argument must name a width the environment contract offers; anything
    /// else is a description defect, never rounded to a nearby width.
    fn access_width(bits: u64) -> Result<AccessWidth, Flow> {
        match bits {
            8 => Ok(AccessWidth::B),
            16 => Ok(AccessWidth::H),
            32 => Ok(AccessWidth::W),
            64 => Ok(AccessWidth::D),
            _ => Err(StepOutcome::Failed(ModelError::InvalidDescription {
                what: "load/store width outside the contract's width set",
            })),
        }
    }
}

#[cfg(test)]
mod tests;
