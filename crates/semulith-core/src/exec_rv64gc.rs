//! The rv64gc definitional interpreter — `P4-SYSTEM.2` (the route flip): the privileged
//! counterpart of [`crate::exec`].
//!
//! [`step`] executes ONE instruction of `rv64gc-lab-v0` against the privileged
//! architectural state and the environment boundary. The semantics it evaluates are the
//! `Sem` effect trees lowered into [`crate::definition_rv64gc`] from the unit's composition
//! (base `riscv/rv64i` + the Zicsr, Zicntr and privileged-system fragments) — the semantics
//! DATA stays the one executable owner of every rule (OWN-01); this module is its
//! evaluator, not a second implementation, and its shared-variant arms are the same
//! algebra `exec` documents (the rv64gc module's own `Sem` type, per
//! `decision_generated-mirror-needs-tracked-input`).
//!
//! What differs from `exec` is the privileged composition's own rules, each named:
//!
//! - **Delivery, not report** — every target-visible fault is DELIVERED by the
//!   architecture on this composition (the zicsr refinement declared in
//!   `zicsr.sem.sexp`): the pinned cause vocabulary, xtval the address or the word, xepc
//!   the instruction's own address, pc ← xtvec, the privilege stack updated — all of it
//!   through [`crate::privilege`], never per-instruction. Execution continues at the
//!   handler; the laboratory's run ends at the declared step count, not at the trap.
//! - **The trap-END discipline** — a delivered trap ends the step: the effect tree's
//!   remaining writes do not land (the scratch corpus runner's measured fix, ridden into
//!   the tracked engine here — `Frame.trapped`, checked at the top of the evaluator and
//!   before every register write).
//! - **Translation hooks** (`P4-SYSTEM.3`): every access address passes through
//!   [`crate::translation`] before it crosses the boundary — fetch in 16-bit
//!   parcels (decision 5, coalescing to exactly one request whenever the parcels'
//!   translated addresses share one physical 32-bit unit; under Bare that is every
//!   case, so the Bare request shape is byte-exact), loads and stores after the
//!   model-side misalignment check (the pinned implementation-defined priority,
//!   decision 7). Bare is the exact identity path; satp.MODE=Sv39 enters the walk
//!   — slice (c)'s — and until then is the named unimplemented case, never a wrong
//!   answer. The effective mode is the one computation (§2.1.1.6.4): fetch uses
//!   the current mode, data accesses use MPP when MPRV=1, and M is never
//!   translated.
//! - **Misaligned data accesses** raise their address-misaligned cause (4/6) before the
//!   boundary is crossed (D-MISALIGN-DATA: a request the contract forbids must not be
//!   formed); an outside-every-region access is the boundary's `AccessFault` answer,
//!   delivered as the matching load/store access-fault cause (5/7).
//! - **Fetch** — one 32-bit `Fetch` per instruction in Bare (the parcels coalesce —
//!   above). IALIGN is 16 with C, so a fetch is
//!   alignment-legal at any even address; the environment judges (it carries the
//!   profile's IALIGN as data) and an `AccessFault`/`Misaligned` answer is delivered as
//!   cause 1/0 with tval the pc. A taken branch or jump to an ODD target raises
//!   cause 0 on the jump (D-IALIGN-16), delivered.
//! - **Requested traps** — `ecall`/`ebreak` are the semantics data's own `trap-deliver`
//!   effects (the composition's declared refinement of the base requested-trap form);
//!   a `Sem::Trap` node reaching this evaluator is a description defect, panicking like
//!   `exec`'s vocabulary guard rather than silently inventing a behavior.
//! - **The floating-point state** (`P4-SYSTEM.7`, schema/semantics.sexp's floating-point
//!   block): an instruction whose rule reads or writes the FP state is ILLEGAL at
//!   mstatus.FS = Off — judged at the head of the step, before ANY effect of the rule
//!   ([`touches_fp_state`]; an FLW raises 2, never its load's fault); `(freg x)` reads the
//!   pre-instruction f-file; a write to an f-register marks FS Dirty; each arithmetic operator
//!   is [`crate::fp`]'s (the model layer over the qualified backend — never the backend
//!   directly) and accrues its flags through [`privilege::accrue_fflags`] (sticky; Dirty iff
//!   fflags changes); a reserved rounding mode is illegal-instruction at `(rounding …)`,
//!   before any flag accrues.
//! - **Reserved decode** — a word no row matches is reported as
//!   [`StepRv64gc::ReservedDecode`] (`D-RESERVED-DECODE`): the architecture declares the
//!   behavior UNSPECIFIED, and the conversion to the delivered illegal-instruction cause
//!   is the diagnostic policy's explicit act, one layer up (the verify-side runner's,
//!   the same rule as rv64i's, delivered rather than reported on this composition).

use crate::definition_rv64gc::{FieldDef, InsnDef, Sem, FIELDS, INSNS};
use crate::env::{AccessWidth, BoundaryError, Environment, Failure, Request, Response};
use crate::fp;
use crate::interrupts;
use crate::muldiv;
use crate::outcome::ModelError;
use crate::privilege;
use crate::privilege::PrivilegedHart;
use crate::state_rv64gc::{ArchitecturalState, CSR_ELEMENTS};
use crate::timekeeping;
use crate::translation;

/// Everything observable about one executed instruction: either the effect ran (any
/// delivered trap included — delivery is execution on this composition), or the decode
/// miss the diagnostic policy converts one layer up, or the model failed (SEM-02 —
/// never emitted as a target outcome).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum StepRv64gc {
    /// The instruction's effect ran to completion (a delivered trap ends the effect
    /// early — the trap-END discipline — and is still `Executed`: delivery is the
    /// architecture's own act, not a stop).
    Executed,
    /// A word no decode row matches (`D-RESERVED-DECODE`): the model records the case;
    /// the policy conversion is not the evaluator's act.
    ReservedDecode {
        /// The pc the word was fetched at.
        at: u64,
        /// The fetched word itself.
        word: u32,
    },
    /// The model or the environment contract failed (SEM-02).
    Failed(ModelError),
}

/// Execute the instruction at the current pc — [`step_over`] over the generated
/// rv64gc definition, the one execution path.
pub fn step(state: &mut ArchitecturalState, env: &mut impl Environment) -> StepRv64gc {
    step_over(state, env, INSNS)
}

/// The WFI instruction word (the pinned `rv_system` table's row — its mask is all-ones,
/// so the word IS the instruction's identity; `P4-SYSTEM.5` decision 4's halt entry
/// keys on it).
const WFI_WORD: u32 = 0x1050_0073;

/// Execute one instruction decoded from a caller-supplied instruction table — the same
/// seam `exec::step_over` documents for the base profile: the table is data, and over
/// the generated table this is the production definition.
pub fn step_over(
    state: &mut ArchitecturalState,
    env: &mut impl Environment,
    insns: &[InsnDef],
) -> StepRv64gc {
    let pc = state.pc();
    // P4-SYSTEM.5 decision 4: the halted step. While WAITING the step head evaluates
    // the wake FIRST (§2.1.3.3 — a locally-enabled pending interrupt at any privilege,
    // regardless of the global enables and mideleg). The step the wake does not fire
    // on retires nothing, issues no fetch and advances the domain one tick (slice (a)'s
    // rule — this is what makes the leaf's acceptance true); the step it fires on is
    // ordinary (decision 6): it falls through to the head evaluation below, so a taken
    // trap's xepc is this pc — the WFI's pc + 4, the section's own rule, which the
    // generic between-instructions delivery computes for free because the WFI retired
    // into the halt with pc advanced — and an untrapped resume continues here.
    if state.hart_state().is_waiting() {
        if !interrupts::wake_pending(state) {
            timekeeping::advance(state, false);
            return StepRv64gc::Executed;
        }
        state.hart_state().wake();
    }
    // P4-SYSTEM.5 decision 3: pending evaluation at the HEAD of every step — "bounded
    // amount of time" per-step by construction. An eligible interrupt is delivered
    // BETWEEN instructions (mepc/sepc the un-fetched pc); the delivery is a step
    // boundary (time ticks) that retires nothing (minstret does not move).
    if let Some(pend) = interrupts::pending(state) {
        let handler = interrupts::deliver(state, pend, pc);
        state.set_pc(handler);
        timekeeping::advance(state, false);
        return StepRv64gc::Executed;
    }
    // The fetch's two 16-bit parcels, translated independently (P4-SYSTEM.3 decision 5).
    // The recorded coalescing choice: when both parcels' TRANSLATED addresses lie in one
    // physical 32-bit unit, the fetch is exactly one request — under Bare that is every
    // case, so the Bare request shape is byte-exact (the corpus's one-fetch-per-step
    // census is the measurement). A page-straddling instruction fetches each parcel's
    // own physical unit and joins the halves — two requests, its own case, never
    // silently coalesced.
    let parcels = translation::fetch_parcels(pc);
    let mut parcel_pas = [0u64; 2];
    for (i, parcel) in parcels.iter().enumerate() {
        match translation::translate(state, env, *parcel, translation::AccessKind::Fetch) {
            translation::Translate::Identity(pa) | translation::Translate::Physical(pa) => {
                parcel_pas[i] = pa;
            }
            translation::Translate::PageFault { cause, tval }
            | translation::Translate::AccessFault { cause, tval } => {
                deliver(state, cause, tval, pc);
                timekeeping::advance(state, false);
                return StepRv64gc::Executed;
            }
            translation::Translate::Failed(error) => return StepRv64gc::Failed(error),
        }
    }
    let coalesced = parcel_pas[1] == parcel_pas[0].wrapping_add(2);
    let mut fetch16 = |addr: u64, va: u64| -> Result<u64, StepRv64gc> {
        // one 32-bit fetch at the parcel's physical address; the caller keeps 16 bits
        match env.request(Request::Fetch { addr }) {
            Ok(Response::Fetch(word)) => Ok(u64::from(word)),
            Ok(_) => Err(StepRv64gc::Failed(ModelError::InvalidDescription {
                what: "environment answered a Fetch with a non-fetch response",
            })),
            Err(BoundaryError::Target(Failure::AccessFault)) => {
                // the boundary's access fault at fetch, delivered (cause 1, tval = the VA)
                deliver(state, 1, va, pc);
                timekeeping::advance(state, false);
                Err(StepRv64gc::Executed)
            }
            Err(BoundaryError::Target(Failure::Misaligned)) => {
                // an odd pc — only a manipulated xepc/xTVEC produces one under IALIGN=16;
                // the fetch-misaligned case, delivered (cause 0, tval = the VA)
                deliver(state, 0, va, pc);
                timekeeping::advance(state, false);
                Err(StepRv64gc::Executed)
            }
            Err(BoundaryError::Violation(violation)) => {
                Err(StepRv64gc::Failed(ModelError::ContractViolation(violation)))
            }
        }
    };
    let word = if coalesced {
        // the parcels' one shared physical unit: exactly one fetch request (the Bare
        // request shape, byte-exact)
        match fetch16(parcel_pas[0], pc) {
            Ok(w) => w as u32,
            Err(outcome) => return outcome,
        }
    } else {
        // the straddle: each parcel's own unit, 16 bits from each
        let lo = match fetch16(parcel_pas[0], parcels[0]) {
            Ok(w) => w & 0xFFFF,
            Err(outcome) => return outcome,
        };
        let hi = match fetch16(parcel_pas[1], parcels[1]) {
            Ok(w) => w & 0xFFFF,
            Err(outcome) => return outcome,
        };
        (lo | (hi << 16)) as u32
    };
    let Some(insn) = insns.iter().find(|i| word & i.mask == i.value) else {
        // a step boundary without an instruction (the diagnostic policy converts one
        // layer up): time ticks, minstret does not (P4-SYSTEM.5 decision 1)
        timekeeping::advance(state, false);
        return StepRv64gc::ReservedDecode { at: pc, word };
    };
    // P4-SYSTEM.7: the FP-state contract's Off gate — "any instruction that attempts to read
    // or write the corresponding state will cause an illegal-instruction exception"
    // (RVP-MACHINE §2.1.1.6.7), judged before ANY effect of the rule (Sail 0.14 judges it at
    // decode, fdext_control.sail:19). A delivery is a step boundary that retires nothing.
    if touches_fp_state(insn.effect) && !privilege::fp_enabled(state) {
        deliver(state, 2, u64::from(word), pc);
        timekeeping::advance(state, false);
        return StepRv64gc::Executed;
    }
    let mut frame = Frame {
        state,
        env,
        pc,
        word,
        operands: extract(insn, word),
        pre_regs: [0; 32],
        pre_fregs: [0; 32],
        pc_written: false,
        trapped: false,
        failed: None,
    };
    for i in 0..32 {
        frame.pre_regs[i] = frame.state.read_x(i as u8);
        frame.pre_fregs[i] = frame.state.read_f(i as u8);
    }
    frame.run(insn.effect);
    if let Some(error) = frame.failed {
        return StepRv64gc::Failed(error);
    }
    // P4-SYSTEM.5 decision 4: a LEGAL wfi enters the wait (the generated effect's legality
    // — illegal in U with S present, illegal in S with TW=1 — stands, corpus-proven; the
    // nop latitude is recorded-not-taken). A trapped wfi waits for nothing.
    if word == WFI_WORD && !frame.trapped {
        frame.state.hart_state().enter();
    }
    if !frame.pc_written {
        frame.state.set_pc(pc.wrapping_add(4));
    }
    // P4-SYSTEM.5 decision 1: the declared virtual-time domain ticks at every step
    // boundary; minstret counts GENUINELY — a trap-delivering instruction's step
    // retires nothing (a completed one, `!frame.trapped`, retires one)
    timekeeping::advance(frame.state, !frame.trapped);
    StepRv64gc::Executed
}

/// Deliver a trap through the privilege machinery (the one path): cause, tval, the
/// faulting instruction's own pc; the hart's pc moves to the handler and the step's
/// remaining effects end (`trapped`).
fn deliver(state: &mut ArchitecturalState, cause: u64, tval: u64, pc: u64) -> bool {
    let handler = privilege::trap_deliver(state, cause, tval, pc);
    state.set_pc(handler);
    true
}

fn mask64(width: u32) -> u64 {
    if width >= 64 {
        u64::MAX
    } else {
        (1u64 << width) - 1
    }
}

fn sext64(value: u64, from: u32) -> u64 {
    let from = from.min(64);
    if from == 0 || from == 64 {
        return value;
    }
    let sign = 1u64 << (from - 1);
    if value & sign != 0 {
        value | !mask64(from)
    } else {
        value & mask64(from)
    }
}

fn access_width(width: u64) -> Result<AccessWidth, ModelError> {
    match width {
        8 => Ok(AccessWidth::B),
        16 => Ok(AccessWidth::H),
        32 => Ok(AccessWidth::W),
        64 => Ok(AccessWidth::D),
        _ => Err(ModelError::InvalidDescription {
            what: "a load/store width outside the access-width vocabulary",
        }),
    }
}

/// The evaluation frame: the READS-AND-WRITES contract (register reads see pre-state),
/// the pc-transfer record, the trap-END flag, and the model-error slot for environment
/// contract failures mid-effect.
struct Frame<'a> {
    state: &'a mut ArchitecturalState,
    env: &'a mut dyn Environment,
    pc: u64,
    word: u32,
    operands: Vec<(&'static str, u64, u32)>,
    pre_regs: [u64; 32],
    /// The pre-instruction f-file — `(freg x)` reads it (the READS-AND-WRITES contract).
    pre_fregs: [u64; 32],
    pc_written: bool,
    trapped: bool,
    failed: Option<ModelError>,
}

impl Frame<'_> {
    fn operand(&self, name: &str) -> (u64, u32) {
        self.operands
            .iter()
            .copied()
            .find(|(n, _, _)| *n == name)
            .map(|(_, v, w)| (v, w))
            .unwrap_or_else(|| {
                panic!("tree reads an operand the encoding does not provide: {name}")
            })
    }

    /// Deliver from inside an effect: the hart's pc moves to the handler, the transfer
    /// is recorded, and the step's remaining effects end.
    fn deliver(&mut self, cause: u64, tval: u64) {
        let pc = self.pc;
        let handler = privilege::trap_deliver(self.state, cause, tval, pc);
        self.state.set_pc(handler);
        self.pc_written = true;
        self.trapped = true;
    }

    fn run(&mut self, sem: &Sem) -> (u64, u32) {
        if self.trapped || self.failed.is_some() {
            return (0, 64); // a delivered trap or a model failure ends the step: no further effect
        }
        match sem {
            Sem::Lit(v) => (*v, 64),
            Sem::Reg(name) => {
                let (index, _) = self.operand(name);
                (self.pre_regs[index as usize], 64)
            }
            Sem::Imm(name) | Sem::Field(name) => self.operand(name),
            Sem::Pc => (self.pc, 64),
            Sem::Inst => (u64::from(self.word), 64),
            Sem::Mode => (self.state.mode().code(), 64),
            Sem::Xlen => (64, 64),
            Sem::Add(a, b) => arith2(self, a, b, u64::wrapping_add),
            Sem::Sub(a, b) => arith2(self, a, b, u64::wrapping_sub),
            Sem::And(a, b) => arith2(self, a, b, |x, y| x & y),
            Sem::Or(a, b) => arith2(self, a, b, |x, y| x | y),
            Sem::Xor(a, b) => arith2(self, a, b, |x, y| x ^ y),
            Sem::Shl(a, b) => {
                let (x, wx) = self.run(a);
                let (y, _) = self.run(b);
                (x.wrapping_shl(y as u32), wx + y as u32)
            }
            Sem::Shr(a, b) => {
                let (x, wx) = self.run(a);
                let (y, _) = self.run(b);
                ((x & mask64(wx)).wrapping_shr(y as u32), wx)
            }
            Sem::Sar(a, b) => {
                let (x, wx) = self.run(a);
                let (y, _) = self.run(b);
                ((sext64(x, wx) as i64).wrapping_shr(y as u32) as u64, wx)
            }
            Sem::Slt(a, b) => cmp2(self, a, b, |x, y| (x as i64) < (y as i64)),
            Sem::Sltu(a, b) => cmp2(self, a, b, |x, y| x < y),
            Sem::Eq(a, b) => cmp2(self, a, b, |x, y| x == y),
            Sem::Ne(a, b) => cmp2(self, a, b, |x, y| x != y),
            Sem::Lt(a, b) => cmp2(self, a, b, |x, y| (x as i64) < (y as i64)),
            Sem::Ltu(a, b) => cmp2(self, a, b, |x, y| x < y),
            Sem::Ge(a, b) => cmp2(self, a, b, |x, y| (x as i64) >= (y as i64)),
            Sem::Geu(a, b) => cmp2(self, a, b, |x, y| x >= y),
            // P4-SYSTEM.11 (b): M — at the operands' width, through the model layer.
            Sem::Mul(a, b) => muldiv2(self, a, b, muldiv::mul),
            Sem::MulH(a, b) => muldiv2(self, a, b, muldiv::mulh),
            Sem::MulHsu(a, b) => muldiv2(self, a, b, muldiv::mulhsu),
            Sem::MulHu(a, b) => muldiv2(self, a, b, muldiv::mulhu),
            Sem::Div(a, b) => div2(self, a, b, "div", muldiv::div),
            Sem::DivU(a, b) => div2(self, a, b, "divu", muldiv::divu),
            Sem::Rem(a, b) => div2(self, a, b, "rem", muldiv::rem),
            Sem::RemU(a, b) => div2(self, a, b, "remu", muldiv::remu),
            Sem::Trunc(w, v) => {
                let (v, _) = self.run(v);
                (v & mask64(*w as u32), *w as u32)
            }
            Sem::Sext(w, v) => {
                let (v, from) = self.run(v);
                (sext64(v, from), *w as u32)
            }
            Sem::Zext(w, v) => {
                let (v, from) = self.run(v);
                (v & mask64(from.min(*w as u32)), *w as u32)
            }
            Sem::Bits(hi, lo, v) => {
                let (v, _) = self.run(v);
                (
                    (v >> lo) & mask64(u32::from(*hi - *lo) + 1),
                    u32::from(*hi - *lo) + 1,
                )
            }
            Sem::Load(width, _signed, addr) => {
                let (w, _) = self.run(width);
                let (a, _) = self.run(addr);
                let Ok(width) = access_width(w) else {
                    self.failed = Some(ModelError::InvalidDescription {
                        what: "a load width outside the access-width vocabulary",
                    });
                    return (0, 64);
                };
                if a % (w / 8) != 0 {
                    // misaligned data access: raised before the boundary is crossed (cause 4)
                    self.deliver(4, a);
                    return (0, 64);
                }
                // the translation hook (P4-SYSTEM.3): misalignment is judged first by
                // the pinned implementation-defined priority (decision 7); the address
                // that crosses the boundary is the translated one
                let pa = match translation::translate(
                    self.state,
                    self.env,
                    a,
                    translation::AccessKind::Load,
                ) {
                    translation::Translate::Identity(pa) | translation::Translate::Physical(pa) => {
                        pa
                    }
                    translation::Translate::PageFault { cause, tval }
                    | translation::Translate::AccessFault { cause, tval } => {
                        self.deliver(cause, tval);
                        return (0, 64);
                    }
                    translation::Translate::Failed(error) => {
                        self.failed = Some(error);
                        return (0, 64);
                    }
                };
                match self.env.request(Request::Load { width, addr: pa }) {
                    Ok(Response::Load(v)) => (v, w as u32),
                    Ok(_) => {
                        self.failed = Some(ModelError::InvalidDescription {
                            what: "environment answered a Load with a non-load response",
                        });
                        (0, 64)
                    }
                    Err(BoundaryError::Target(Failure::AccessFault)) => {
                        self.deliver(5, a);
                        (0, 64)
                    }
                    Err(BoundaryError::Target(Failure::Misaligned)) => {
                        self.deliver(4, a);
                        (0, 64)
                    }
                    Err(BoundaryError::Violation(v)) => {
                        self.failed = Some(ModelError::ContractViolation(v));
                        (0, 64)
                    }
                }
            }
            Sem::Store(width, addr, value) => {
                let (w, _) = self.run(width);
                let (a, _) = self.run(addr);
                let (v, _) = self.run(value);
                let Ok(width) = access_width(w) else {
                    self.failed = Some(ModelError::InvalidDescription {
                        what: "a store width outside the access-width vocabulary",
                    });
                    return (0, 64);
                };
                if a % (w / 8) != 0 {
                    // misaligned data access: raised before the boundary is crossed (cause 6)
                    self.deliver(6, a);
                    return (0, 64);
                }
                // the translation hook (P4-SYSTEM.3): same ordering as the load — the
                // address that crosses the boundary is the translated one
                let pa = match translation::translate(
                    self.state,
                    self.env,
                    a,
                    translation::AccessKind::Store,
                ) {
                    translation::Translate::Identity(pa) | translation::Translate::Physical(pa) => {
                        pa
                    }
                    translation::Translate::PageFault { cause, tval }
                    | translation::Translate::AccessFault { cause, tval } => {
                        self.deliver(cause, tval);
                        return (0, 64);
                    }
                    translation::Translate::Failed(error) => {
                        self.failed = Some(error);
                        return (0, 64);
                    }
                };
                match self.env.request(Request::Store {
                    width,
                    addr: pa,
                    data: v,
                }) {
                    Ok(Response::StoreDone) => (0, 64),
                    Ok(_) => {
                        self.failed = Some(ModelError::InvalidDescription {
                            what: "environment answered a Store with a non-store response",
                        });
                        (0, 64)
                    }
                    Err(BoundaryError::Target(Failure::AccessFault)) => {
                        self.deliver(7, a);
                        (0, 64)
                    }
                    Err(BoundaryError::Target(Failure::Misaligned)) => {
                        self.deliver(6, a);
                        (0, 64)
                    }
                    Err(BoundaryError::Violation(viol)) => {
                        self.failed = Some(ModelError::ContractViolation(viol));
                        (0, 64)
                    }
                }
            }
            Sem::Set(target, value) => {
                let (name, float) = match **target {
                    Sem::Reg(name) => (name, false),
                    Sem::FReg(name) => (name, true),
                    _ => panic!("set writes a register"),
                };
                let (index, _) = self.operand(name);
                let (v, _) = self.run(value);
                if self.trapped || self.failed.is_some() {
                    return (0, 64);
                }
                if float {
                    // an f-register write marks FS Dirty unconditionally (the FP-state
                    // contract; Sail 0.14's wF)
                    self.state.write_f(index as u8, v);
                    privilege::mark_fp_dirty(self.state);
                } else {
                    self.state.write_x(index as u8, v);
                }
                (0, 64)
            }
            Sem::SetPc(target) => {
                let (t, _) = self.run(target);
                if t % 2 != 0 {
                    // the misaligned-target rule (D-IALIGN-16), raised on the jump, delivered
                    self.deliver(0, t);
                    return (0, 64);
                }
                self.state.set_pc(t);
                self.pc_written = true;
                (0, 64)
            }
            Sem::Seq(steps) => {
                for s in *steps {
                    self.run(s);
                }
                (0, 64)
            }
            Sem::Nop => (0, 64),
            Sem::If(c, t, e) => {
                let (c, _) = self.run(c);
                if c != 0 {
                    self.run(t)
                } else {
                    self.run(e)
                }
            }
            Sem::Trap(_, _) => {
                panic!(
                    "rv64gc refines the requested-trap form away — a Sem::Trap node \
                        reaching this evaluator is a description defect"
                )
            }
            Sem::CsrState(a) => {
                let (addr, _) = self.run(a);
                (privilege::csr_state(self.state, csr_name(addr as u16)), 64)
            }
            Sem::CsrRead(a) => {
                let (addr, _) = self.run(a);
                match privilege::csr_read(self.state, addr as u16) {
                    Ok(v) => (v, 64),
                    Err(_) => {
                        // illegal-instruction, delivered by the architecture (tval = the word)
                        let word = u64::from(self.word);
                        self.deliver(2, word);
                        (0, 64)
                    }
                }
            }
            Sem::CsrWrite(a, v) => {
                let (addr, _) = self.run(a);
                let (v, _) = self.run(v);
                if privilege::csr_write(self.state, addr as u16, v).is_err() {
                    let word = u64::from(self.word);
                    self.deliver(2, word);
                }
                (0, 64)
            }
            Sem::CsrRw(a, v) => {
                // the atomic read-write (P4-SYSTEM.8 slice a): the read and the write are both
                // judged before the old value reaches its destination, so a refused write
                // leaves rd untouched — the instruction completes or faults as a unit
                let (addr, _) = self.run(a);
                let (v, _) = self.run(v);
                if self.trapped || self.failed.is_some() {
                    return (0, 64);
                }
                let word = u64::from(self.word);
                let Ok(old) = privilege::csr_read(self.state, addr as u16) else {
                    self.deliver(2, word);
                    return (0, 64);
                };
                if privilege::csr_write(self.state, addr as u16, v).is_err() {
                    self.deliver(2, word);
                    return (0, 64);
                }
                (old, 64)
            }
            Sem::TrapDeliver(cause, tval) => {
                let (c, _) = self.run(cause);
                let (t, _) = self.run(tval);
                self.deliver(c, t);
                (0, 64)
            }
            Sem::Xret(x) => {
                let (code, _) = self.run(x);
                let level = if code == 3 {
                    privilege::PrivilegeMode::M
                } else {
                    privilege::PrivilegeMode::S
                };
                let pc = privilege::xret(self.state, level);
                self.state.set_pc(pc);
                self.pc_written = true;
                (0, 64)
            }
            Sem::TlbInvalidate(va, asid) => {
                // SFENCE.VMA's real effect (P4-SYSTEM.3 decision 2): the four cases
                // over the modelled TLB — rs1's value is the VA, rs2's low 16 bits
                // the ASID; a non-canonical VA is a no-op by the spec's own sentence.
                // No architectural register is written.
                let (va, _) = self.run(va);
                let (asid, _) = self.run(asid);
                translation::fence(self.state, va, (asid & 0xFFFF) as u16);
                (0, 64)
            }
            Sem::LoadReserved(width, _signed, addr) => {
                let (w, _) = self.run(width);
                let (a, _) = self.run(addr);
                let Ok(width) = access_width(w) else {
                    self.failed = Some(ModelError::InvalidDescription {
                        what: "a load-reserved width outside the access-width vocabulary",
                    });
                    return (0, 64);
                };
                if a % (w / 8) != 0 {
                    // misaligned LR: the LOAD access-fault cause 5 — RVP-MACHINE's
                    // exception table maps load-reserved to load exceptions ("load and
                    // load-reserved instructions generate load exceptions"), and the
                    // declared policy (decision 6, reference-matched) takes access-fault
                    // over misaligned; judged before translation (the .3 decision-7
                    // hand-off) — and the trap clears nothing (decision 4)
                    self.deliver(5, a);
                    return (0, 64);
                }
                // LR translates under the LOAD rules (RVP-MACHINE's exception table)
                let pa = match translation::translate(
                    self.state,
                    self.env,
                    a,
                    translation::AccessKind::Load,
                ) {
                    translation::Translate::Identity(pa) | translation::Translate::Physical(pa) => {
                        pa
                    }
                    translation::Translate::PageFault { cause, tval }
                    | translation::Translate::AccessFault { cause, tval } => {
                        self.deliver(cause, tval);
                        return (0, 64);
                    }
                    translation::Translate::Failed(error) => {
                        self.failed = Some(error);
                        return (0, 64);
                    }
                };
                match self.env.request(Request::Load { width, addr: pa }) {
                    Ok(Response::Load(v)) => {
                        // a COMPLETED LR registers the reservation — any LR replaces
                        // (decision 4); the faulting paths above establish nothing
                        self.state.reservation().establish(pa, (w / 8) as u8);
                        (v, w as u32)
                    }
                    Ok(_) => {
                        self.failed = Some(ModelError::InvalidDescription {
                            what: "environment answered a Load with a non-load response",
                        });
                        (0, 64)
                    }
                    Err(BoundaryError::Target(Failure::AccessFault)) => {
                        self.deliver(5, a);
                        (0, 64)
                    }
                    Err(BoundaryError::Target(Failure::Misaligned)) => {
                        // unreachable (misalignment is judged before translation) — but an LR is a LOAD:
                        // the declared policy's cause is 5, never 7 (P4-SYSTEM.8 slice a)
                        self.deliver(5, a);
                        (0, 64)
                    }
                    Err(BoundaryError::Violation(v)) => {
                        self.failed = Some(ModelError::ContractViolation(v));
                        (0, 64)
                    }
                }
            }
            Sem::StoreConditional(width, addr, value) => {
                let (w, _) = self.run(width);
                let (a, _) = self.run(addr);
                let (v, _) = self.run(value);
                let Ok(width) = access_width(w) else {
                    self.failed = Some(ModelError::InvalidDescription {
                        what: "a store-conditional width outside the access-width vocabulary",
                    });
                    return (0, 64);
                };
                if a % (w / 8) != 0 {
                    // misaligned atomic: cause 7, before translation (decision 6)
                    self.deliver(7, a);
                    return (0, 64);
                }
                // SC translates under the STORE/AMO rules (RVP-MACHINE's exception table)
                let pa = match translation::translate(
                    self.state,
                    self.env,
                    a,
                    translation::AccessKind::Store,
                ) {
                    translation::Translate::Identity(pa) | translation::Translate::Physical(pa) => {
                        pa
                    }
                    translation::Translate::PageFault { cause, tval }
                    | translation::Translate::AccessFault { cause, tval } => {
                        self.deliver(cause, tval);
                        return (0, 64);
                    }
                    translation::Translate::Failed(error) => {
                        self.failed = Some(error);
                        return (0, 64);
                    }
                };
                // The deterministic policy (decision 3), judged before ANY memory
                // operation — a failed SC "does not give rise to any memory
                // operations" (RVWMO §17.1.1.1). The reservation clears on the
                // COMPLETED path either way (§12.1.2's own sentence); the trap paths
                // clear nothing (a trap does not invalidate — Sail 0.14 cancels on
                // the completed path only).
                if !self.state.reservation().matches(pa, (w / 8) as u8) {
                    self.state.reservation().clear();
                    return (1, 64);
                }
                match self.env.request(Request::Store {
                    width,
                    addr: pa,
                    data: v,
                }) {
                    Ok(Response::StoreDone) => {
                        self.state.reservation().clear();
                        (0, 64)
                    }
                    Ok(_) => {
                        self.failed = Some(ModelError::InvalidDescription {
                            what: "environment answered a Store with a non-store response",
                        });
                        (0, 64)
                    }
                    Err(BoundaryError::Target(Failure::AccessFault)) => {
                        self.deliver(7, a);
                        (0, 64)
                    }
                    Err(BoundaryError::Target(Failure::Misaligned)) => {
                        self.deliver(7, a);
                        (0, 64)
                    }
                    Err(BoundaryError::Violation(viol)) => {
                        self.failed = Some(ModelError::ContractViolation(viol));
                        (0, 64)
                    }
                }
            }
            Sem::Amo(funct5, width, addr, value) => {
                let (w, _) = self.run(width);
                let (a, _) = self.run(addr);
                let (v, _) = self.run(value);
                let Ok(width) = access_width(w) else {
                    self.failed = Some(ModelError::InvalidDescription {
                        what: "an AMO width outside the access-width vocabulary",
                    });
                    return (0, 64);
                };
                if a % (w / 8) != 0 {
                    // misaligned atomic: cause 7, before translation (decision 6)
                    self.deliver(7, a);
                    return (0, 64);
                }
                // ONE translation under the store/AMO rules (decision 5): R and W
                // judged once, the cause always the store/AMO one — never a load
                // page fault
                let pa = match translation::translate(
                    self.state,
                    self.env,
                    a,
                    translation::AccessKind::Atomic,
                ) {
                    translation::Translate::Identity(pa) | translation::Translate::Physical(pa) => {
                        pa
                    }
                    translation::Translate::PageFault { cause, tval }
                    | translation::Translate::AccessFault { cause, tval } => {
                        self.deliver(cause, tval);
                        return (0, 64);
                    }
                    translation::Translate::Failed(error) => {
                        self.failed = Some(error);
                        return (0, 64);
                    }
                };
                // The boundary pair (decision 5): a load followed by a store to the
                // same address — the nine operations are the model's, never the
                // environment's (a Request::Atomic variant would push them there).
                let old = match self.env.request(Request::Load { width, addr: pa }) {
                    Ok(Response::Load(v)) => v,
                    Ok(_) => {
                        self.failed = Some(ModelError::InvalidDescription {
                            what: "environment answered an AMO's load with a non-load response",
                        });
                        return (0, 64);
                    }
                    Err(BoundaryError::Target(Failure::AccessFault)) => {
                        self.deliver(7, a);
                        return (0, 64);
                    }
                    Err(BoundaryError::Target(Failure::Misaligned)) => {
                        self.deliver(7, a);
                        return (0, 64);
                    }
                    Err(BoundaryError::Violation(v)) => {
                        self.failed = Some(ModelError::ContractViolation(v));
                        return (0, 64);
                    }
                };
                let mask = mask64(w as u32);
                let new = match *funct5 {
                    0x00 => old.wrapping_add(v),
                    0x01 => v,
                    0x04 => old ^ v,
                    0x08 => old | v,
                    0x0c => old & v,
                    0x10 => {
                        if sext64(old, w as u32) as i64 <= sext64(v, w as u32) as i64 {
                            old
                        } else {
                            v
                        }
                    }
                    0x14 => {
                        if sext64(old, w as u32) as i64 >= sext64(v, w as u32) as i64 {
                            old
                        } else {
                            v
                        }
                    }
                    0x18 => {
                        if old & mask <= v & mask {
                            old
                        } else {
                            v
                        }
                    }
                    0x1c => {
                        if old & mask >= v & mask {
                            old
                        } else {
                            v
                        }
                    }
                    _ => {
                        self.failed = Some(ModelError::InvalidDescription {
                            what: "an AMO funct5 outside the closed Zaamo nine",
                        });
                        return (0, 64);
                    }
                } & mask;
                match self.env.request(Request::Store {
                    width,
                    addr: pa,
                    data: new,
                }) {
                    Ok(Response::StoreDone) => (old, w as u32),
                    Ok(_) => {
                        self.failed = Some(ModelError::InvalidDescription {
                            what: "environment answered an AMO's store with a non-store response",
                        });
                        (0, 64)
                    }
                    Err(BoundaryError::Target(Failure::AccessFault)) => {
                        self.deliver(7, a);
                        (0, 64)
                    }
                    Err(BoundaryError::Target(Failure::Misaligned)) => {
                        self.deliver(7, a);
                        (0, 64)
                    }
                    Err(BoundaryError::Violation(viol)) => {
                        self.failed = Some(ModelError::ContractViolation(viol));
                        (0, 64)
                    }
                }
            }
            // ---- floating point (P4-SYSTEM.7; the contracts are schema/semantics.sexp's) ----
            Sem::FReg(name) => {
                let (index, _) = self.operand(name);
                (self.pre_fregs[index as usize], 64)
            }
            Sem::Rounding(rm) => {
                let (field, _) = self.run(rm);
                if self.trapped || self.failed.is_some() {
                    return (0, 64);
                }
                let frm = privilege::csr_state(self.state, "frm");
                match fp::resolve_rm(field, frm) {
                    Some(mode) => (mode.bits(), 3),
                    None => {
                        // a RESERVED rounding mode — static 101/110 or DYN with frm 101..111 —
                        // is illegal-instruction (the laboratory's choice, P4-SYSTEM.7 slice c1)
                        let word = u64::from(self.word);
                        self.deliver(2, word);
                        (0, 64)
                    }
                }
            }
            Sem::FBox(n, v) => {
                let (v, _) = self.run(v);
                (fp::fbox(u32::from(*n), v), 64)
            }
            Sem::FUnbox(n, v) => {
                let (v, _) = self.run(v);
                (fp::funbox(u32::from(*n), v), u32::from(*n))
            }
            Sem::FClass(n, a) => {
                let (a, _) = self.run(a);
                (fp::classify(u32::from(*n), a), 64)
            }
            Sem::FMin(n, a, b) => self.fp_pair(*n, a, b, fp::min),
            Sem::FMax(n, a, b) => self.fp_pair(*n, a, b, fp::max),
            Sem::FEq(n, a, b) => self.fp_compare(*n, fp::Compare::Eq, a, b),
            Sem::FLt(n, a, b) => self.fp_compare(*n, fp::Compare::Lt, a, b),
            Sem::FLe(n, a, b) => self.fp_compare(*n, fp::Compare::Le, a, b),
            Sem::FSqrt(n, rm, a) => {
                let (m, _) = self.run(rm);
                let (a, _) = self.run(a);
                if self.trapped || self.failed.is_some() {
                    return (0, 64);
                }
                let r = fp::sqrt(u32::from(*n), effective(m), a);
                self.accrue(r, u32::from(*n))
            }
            Sem::FAdd(n, rm, a, b) => self.fp_rounded(*n, rm, a, b, fp::add),
            Sem::FSub(n, rm, a, b) => self.fp_rounded(*n, rm, a, b, fp::sub),
            Sem::FMul(n, rm, a, b) => self.fp_rounded(*n, rm, a, b, fp::mul),
            Sem::FDiv(n, rm, a, b) => self.fp_rounded(*n, rm, a, b, fp::div),
            Sem::FMadd(n, rm, a, b, c) => {
                let (m, _) = self.run(rm);
                let (a, _) = self.run(a);
                let (b, _) = self.run(b);
                let (c, _) = self.run(c);
                if self.trapped || self.failed.is_some() {
                    return (0, 64);
                }
                let r = fp::fma(u32::from(*n), effective(m), a, b, c);
                self.accrue(r, u32::from(*n))
            }
            Sem::FToI(n, iw, signed, rm, a) => {
                let (m, _) = self.run(rm);
                let (a, _) = self.run(a);
                if self.trapped || self.failed.is_some() {
                    return (0, 64);
                }
                let r = fp::to_int(u32::from(*n), u32::from(*iw), *signed, effective(m), a);
                self.accrue(r, u32::from(*iw))
            }
            Sem::IToF(n, iw, signed, rm, v) => {
                let (m, _) = self.run(rm);
                let (v, _) = self.run(v);
                if self.trapped || self.failed.is_some() {
                    return (0, 64);
                }
                let r = fp::from_int(u32::from(*n), u32::from(*iw), *signed, effective(m), v);
                self.accrue(r, u32::from(*n))
            }
            Sem::FToF(m, n, rm, a) => {
                let (mode, _) = self.run(rm);
                let (a, _) = self.run(a);
                if self.trapped || self.failed.is_some() {
                    return (0, 64);
                }
                let r = fp::convert(u32::from(*m), u32::from(*n), effective(mode), a);
                self.accrue(r, u32::from(*m))
            }
        }
    }

    /// Accrue a floating-point result's flags (sticky; FS Dirty iff fflags changes — the
    /// FP-state contract) and yield its bits at `width`.
    fn accrue(&mut self, r: fp::Flagged, width: u32) -> (u64, u32) {
        privilege::accrue_fflags(self.state, r.flags);
        (r.bits, width)
    }

    /// A rounded two-operand operation: the rounding mode first (a reserved one ends the
    /// step before any flag), then the operands, then the model layer.
    fn fp_rounded(
        &mut self,
        n: u8,
        rm: &Sem,
        a: &Sem,
        b: &Sem,
        op: fn(u32, fp::Rm, u64, u64) -> fp::Flagged,
    ) -> (u64, u32) {
        let (m, _) = self.run(rm);
        let (a, _) = self.run(a);
        let (b, _) = self.run(b);
        if self.trapped || self.failed.is_some() {
            return (0, 64);
        }
        let r = op(u32::from(n), effective(m), a, b);
        self.accrue(r, u32::from(n))
    }

    /// An unrounded two-operand operation yielding a float (min/max).
    fn fp_pair(
        &mut self,
        n: u8,
        a: &Sem,
        b: &Sem,
        op: fn(u32, u64, u64) -> fp::Flagged,
    ) -> (u64, u32) {
        let (a, _) = self.run(a);
        let (b, _) = self.run(b);
        if self.trapped || self.failed.is_some() {
            return (0, 64);
        }
        let r = op(u32::from(n), a, b);
        self.accrue(r, u32::from(n))
    }

    /// A compare, yielding an XLEN 0/1.
    fn fp_compare(&mut self, n: u8, kind: fp::Compare, a: &Sem, b: &Sem) -> (u64, u32) {
        let (a, _) = self.run(a);
        let (b, _) = self.run(b);
        if self.trapped || self.failed.is_some() {
            return (0, 64);
        }
        let r = fp::compare(u32::from(n), kind, a, b);
        self.accrue(r, 64)
    }
}

/// The effective rounding mode a `(rounding …)` node yielded — a description defect if it
/// is not one (check_semantics.check_fp makes every rounded operator's rm a `(rounding …)`).
fn effective(m: u64) -> fp::Rm {
    fp::Rm::from_bits(m).unwrap_or_else(|| {
        panic!("a rounded operator's mode is {m}, not a (rounding …) result — a description defect")
    })
}

/// Does a rule read or write the floating-point state? — the Off gate's population, per the
/// FP-state contract: any f-register (read or `set` target) and any floating-point operator.
/// Decided from the rule itself, so no rule can forget its gate.
fn touches_fp_state(sem: &Sem) -> bool {
    match sem {
        Sem::FReg(_)
        | Sem::Rounding(_)
        | Sem::FBox(..)
        | Sem::FUnbox(..)
        | Sem::FClass(..)
        | Sem::FMin(..)
        | Sem::FMax(..)
        | Sem::FEq(..)
        | Sem::FLt(..)
        | Sem::FLe(..)
        | Sem::FSqrt(..)
        | Sem::FAdd(..)
        | Sem::FSub(..)
        | Sem::FMul(..)
        | Sem::FDiv(..)
        | Sem::FMadd(..)
        | Sem::FToI(..)
        | Sem::IToF(..)
        | Sem::FToF(..) => true,
        Sem::Lit(_)
        | Sem::Reg(_)
        | Sem::Imm(_)
        | Sem::Pc
        | Sem::Xlen
        | Sem::Field(_)
        | Sem::Inst
        | Sem::Mode
        | Sem::Nop => false,
        Sem::Add(a, b)
        | Sem::Sub(a, b)
        | Sem::And(a, b)
        | Sem::Or(a, b)
        | Sem::Xor(a, b)
        | Sem::Shl(a, b)
        | Sem::Shr(a, b)
        | Sem::Sar(a, b)
        | Sem::Slt(a, b)
        | Sem::Sltu(a, b)
        | Sem::Eq(a, b)
        | Sem::Ne(a, b)
        | Sem::Lt(a, b)
        | Sem::Ltu(a, b)
        | Sem::Ge(a, b)
        | Sem::Geu(a, b)
        | Sem::Mul(a, b)
        | Sem::MulH(a, b)
        | Sem::MulHsu(a, b)
        | Sem::MulHu(a, b)
        | Sem::Div(a, b)
        | Sem::DivU(a, b)
        | Sem::Rem(a, b)
        | Sem::RemU(a, b)
        | Sem::Set(a, b)
        | Sem::Trap(a, b)
        | Sem::CsrWrite(a, b)
        | Sem::CsrRw(a, b)
        | Sem::TrapDeliver(a, b)
        | Sem::TlbInvalidate(a, b) => touches_fp_state(a) || touches_fp_state(b),
        Sem::Trunc(_, v)
        | Sem::Sext(_, v)
        | Sem::Zext(_, v)
        | Sem::Bits(_, _, v)
        | Sem::SetPc(v)
        | Sem::CsrState(v)
        | Sem::CsrRead(v)
        | Sem::Xret(v) => touches_fp_state(v),
        Sem::Load(a, b, c)
        | Sem::Store(a, b, c)
        | Sem::If(a, b, c)
        | Sem::LoadReserved(a, b, c)
        | Sem::StoreConditional(a, b, c) => {
            touches_fp_state(a) || touches_fp_state(b) || touches_fp_state(c)
        }
        Sem::Amo(_, a, b, c) => touches_fp_state(a) || touches_fp_state(b) || touches_fp_state(c),
        Sem::Seq(steps) => steps.iter().any(|s| touches_fp_state(s)),
    }
}

fn arith2(f: &mut Frame, a: &Sem, b: &Sem, op: impl Fn(u64, u64) -> u64) -> (u64, u32) {
    let (x, wx) = f.run(a);
    let (y, wy) = f.run(b);
    (op(x, y), wx.max(wy))
}

/// An M multiply (`P4-SYSTEM.11`): at the operands' width — the wider of the two — through the
/// model layer (`muldiv`), which yields a value of that width.
fn muldiv2(f: &mut Frame, a: &Sem, b: &Sem, op: fn(u64, u64, u32) -> u64) -> (u64, u32) {
    let (x, wx) = f.run(a);
    let (y, wy) = f.run(b);
    let w = wx.max(wy);
    (op(x, y, w), w)
}

/// An M division (`P4-SYSTEM.11`). A zero divisor is outside the operator's domain: the
/// definition guards every division (`check_semantics`' domain rule; the generator re-derives
/// it), so reaching one is a DEFINITION defect, never a guest behaviour — refused loudly, as a
/// tree reading an operand the encoding does not provide is. A step that already trapped or
/// failed evaluates its operands as 0 and divides nothing.
fn div2(
    f: &mut Frame,
    a: &Sem,
    b: &Sem,
    name: &str,
    op: fn(u64, u64, u32) -> Option<u64>,
) -> (u64, u32) {
    let (x, wx) = f.run(a);
    let (y, wy) = f.run(b);
    if f.trapped || f.failed.is_some() {
        return (0, 64);
    }
    let w = wx.max(wy);
    let q = op(x, y, w).unwrap_or_else(|| {
        panic!("({name} …) reached with a zero divisor — the definition must guard it")
    });
    (q, w)
}

fn cmp2(f: &mut Frame, a: &Sem, b: &Sem, op: impl Fn(u64, u64) -> bool) -> (u64, u32) {
    let (x, _) = f.run(a);
    let (y, _) = f.run(b);
    (u64::from(op(x, y)), 64)
}

/// The CSR name for a `csr-state` node — the state document's own census; an address it
/// does not carry is a description defect, named.
fn csr_name(addr: u16) -> &'static str {
    CSR_ELEMENTS
        .iter()
        .find(|e| e.address == addr)
        .map(|e| e.name)
        .unwrap_or_else(|| panic!("csr-state of unimplemented address {addr:#x}"))
}

/// Operand extraction — `exec`'s rule, over the generated FIELDS table: composed
/// immediates assemble from their scattered halves; every other operand reads its field
/// (scattered fields reassemble by their declared chunks).
fn extract(insn: &InsnDef, word: u32) -> Vec<(&'static str, u64, u32)> {
    let field = |name: &str| {
        FIELDS
            .iter()
            .find(|f| f.name == name)
            .expect("declared field")
    };
    let raw = |f: &FieldDef| u64::from(word >> f.lo) & mask64(u32::from(f.hi - f.lo) + 1);
    let scattered = |f: &FieldDef| {
        let mut value = 0u64;
        let mut cursor = u32::from(f.hi - f.lo) + 1;
        for &(hi, lo) in f.scatter {
            let width = u32::from(hi - lo) + 1;
            cursor -= width;
            value |= ((raw(f) >> cursor) & mask64(width)) << lo;
        }
        value
    };
    let mut out = Vec::new();
    for &name in insn.operands {
        match name {
            "imm12hi" => {
                let hi = raw(field("imm12hi"));
                let lo = raw(field("imm12lo"));
                out.push(("imm12", (hi << 5) | lo, 12));
            }
            "imm12lo" => {}
            "bimm12hi" => {
                let hi = scattered(field("bimm12hi"));
                let lo = scattered(field("bimm12lo"));
                out.push(("bimm12", hi | lo, 13));
            }
            "bimm12lo" => {}
            "shamtd" => out.push(("shamt", raw(field("shamtd")), 6)),
            "shamtw" => out.push(("shamt", raw(field("shamtw")), 5)),
            _ => {
                let f = field(name);
                // a scattered field carries the width of the immediate it COMPOSES (its highest
                // piece bit + 1: 21 for jimm20), never the field's own width — extending
                // jimm20 from bit 19 turned a +2^19 jump backward (P4-SYSTEM.12 slice a2)
                let (value, width) = if f.scatter.is_empty() {
                    (raw(f), u32::from(f.hi - f.lo) + 1)
                } else {
                    (
                        scattered(f),
                        f.scatter
                            .iter()
                            .map(|&(hi, _)| u32::from(hi) + 1)
                            .max()
                            .expect("a scattered field has pieces"),
                    )
                };
                out.push((name, value, width));
            }
        }
    }
    out
}
