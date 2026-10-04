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
//! - **Reserved decode** — a word no row matches is reported as
//!   [`StepRv64gc::ReservedDecode`] (`D-RESERVED-DECODE`): the architecture declares the
//!   behavior UNSPECIFIED, and the conversion to the delivered illegal-instruction cause
//!   is the diagnostic policy's explicit act, one layer up (the verify-side runner's,
//!   the same rule as rv64i's, delivered rather than reported on this composition).

use crate::definition_rv64gc::{FieldDef, InsnDef, Sem, FIELDS, INSNS};
use crate::env::{AccessWidth, BoundaryError, Environment, Failure, Request, Response};
use crate::outcome::ModelError;
use crate::privilege;
use crate::state_rv64gc::{ArchitecturalState, CSR_ELEMENTS};
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

/// Execute one instruction decoded from a caller-supplied instruction table — the same
/// seam `exec::step_over` documents for the base profile: the table is data, and over
/// the generated table this is the production definition.
pub fn step_over(
    state: &mut ArchitecturalState,
    env: &mut impl Environment,
    insns: &[InsnDef],
) -> StepRv64gc {
    let pc = state.pc();
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
                Err(StepRv64gc::Executed)
            }
            Err(BoundaryError::Target(Failure::Misaligned)) => {
                // an odd pc — only a manipulated xepc/xTVEC produces one under IALIGN=16;
                // the fetch-misaligned case, delivered (cause 0, tval = the VA)
                deliver(state, 0, va, pc);
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
        return StepRv64gc::ReservedDecode { at: pc, word };
    };
    let mut frame = Frame {
        state,
        env,
        pc,
        word,
        operands: extract(insn, word),
        pre_regs: [0; 32],
        pc_written: false,
        trapped: false,
        failed: None,
    };
    for i in 0..32 {
        frame.pre_regs[i] = frame.state.read_x(i as u8);
    }
    frame.run(insn.effect);
    if let Some(error) = frame.failed {
        return StepRv64gc::Failed(error);
    }
    if !frame.pc_written {
        frame.state.set_pc(pc.wrapping_add(4));
    }
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
                let Sem::Reg(name) = **target else {
                    panic!("set writes a register")
                };
                let (index, _) = self.operand(name);
                let (v, _) = self.run(value);
                if self.trapped || self.failed.is_some() {
                    return (0, 64);
                }
                self.state.write_x(index as u8, v);
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
        }
    }
}

fn arith2(f: &mut Frame, a: &Sem, b: &Sem, op: impl Fn(u64, u64) -> u64) -> (u64, u32) {
    let (x, wx) = f.run(a);
    let (y, wy) = f.run(b);
    (op(x, y), wx.max(wy))
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
                let width = u32::from(f.hi - f.lo) + 1;
                out.push((
                    name,
                    if f.scatter.is_empty() {
                        raw(f)
                    } else {
                        scattered(f)
                    },
                    width,
                ));
            }
        }
    }
    out
}
