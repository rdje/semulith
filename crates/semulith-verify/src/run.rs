//! The observation runner and the first-divergence comparator — `P1-LAB.8`, task card T006.
//!
//! A **step observation** is the normalized observation vocabulary this project compares
//! models in (`scripts/compare_traces.py` reduces the reference models to exactly this
//! shape): `(pc, encoded word, register writes, trap)`. Register writes are what the
//! architectural state diff shows (so a write to x0 never appears — the state discards it,
//! which is the architecture's own rule); a trap is the `(cause code, tval)` pair both
//! reference models report. The vocabulary deliberately says nothing about fetch widths,
//! memory-write granularity or trace spellings — those are harness differences, enumerated
//! in `references.sexp`, not observations.
//!
//! [`run`] drives `semulith-core::exec` over any [`Environment`] and records one observation
//! per step, stopping on a trap (the laboratory's harness contract: REQ-D-ECALL-EBREAK and
//! contained exceptions report and stop unless the harness says otherwise), on a model
//! error, on an undefined case, or when the step budget is spent.
//!
//! [`compare`] walks two observation streams and reports the FIRST divergence — the first
//! step where the pc, the instruction word, a register write, or the trap cause/tval
//! differs — or a length mismatch, which is a non-agreement until explained. A shorter
//! trace is never a pass: a model that stopped early agreed on nothing past the stop. This
//! is the `EVD-02` minimized-discrepancy form; every later difference may be a consequence
//! of the first, so only the first is reported.

use semulith_core::definition::InsnDef;
use semulith_core::env::{BoundaryError, Environment, Request, Response};
use semulith_core::exec;
use semulith_core::outcome::{
    ExceptionCause, ModelError, RequestedTrapKind, StepOutcome, TargetEvent, UndefinedCase,
};
use semulith_core::state::ArchitecturalState;

/// One step of normalized observation: what executed, what it wrote, what it raised.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Step {
    /// Address of the executed (or trapping) instruction.
    pub pc: u64,
    /// The encoded 32-bit word at that address. `None` marks the fetch-fault step
    /// (D-FETCH-FAULT-REPORT): the fetch at `pc` failed, so no word exists — and
    /// inventing one would put a fiction in the comparison vocabulary. Every other
    /// step carries the word its fetch returned.
    pub word: Option<u32>,
    /// Architectural register writes `(index, value)`, ascending by index. A write the
    /// architecture discards (x0) never appears.
    pub writes: Vec<(u8, u64)>,
    /// The trap this step raised, as `(cause code, tval)` — the unprivileged cause
    /// vocabulary's codes for exceptions, 11/3 for ECALL/EBREAK.
    pub trap: Option<(u8, u64)>,
}

impl Step {
    fn same_observation(&self, other: &Step) -> bool {
        self.pc == other.pc
            && self.word == other.word
            && self.writes == other.writes
            && self.trap == other.trap
    }
}

/// The synchronous-exception cause codes of the unprivileged vocabulary — the mcause values
/// the pinned causes table assigns (`scripts/compare_traces.py`'s `TRAP_NAMES` maps both
/// reference models' spellings onto these same codes).
#[must_use]
pub const fn cause_code(cause: ExceptionCause) -> u8 {
    match cause {
        ExceptionCause::InstructionAddressMisaligned => 0x00,
        ExceptionCause::InstructionAccessFault => 0x01,
        ExceptionCause::IllegalInstruction => 0x02,
        ExceptionCause::LoadAddressMisaligned => 0x04,
        ExceptionCause::LoadAccessFault => 0x05,
        ExceptionCause::StoreAddressMisaligned => 0x06,
        ExceptionCause::StoreAccessFault => 0x07,
    }
}

/// Why a [`run`] stopped.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Stop {
    /// The step budget was spent without the program stopping on its own.
    Budget,
    /// A trap was reported (a synchronous exception or a requested trap); the trapping
    /// step is the last observation.
    Trap,
    /// The instruction fetch itself faulted (`InstructionAccessFault`). The final step
    /// observation carries `word: None` — a fetch that failed supplied no word, and
    /// inventing one would put a fiction in the comparison vocabulary. Both reference
    /// models report the fault the same way (spike: epc at the target, no commit; sail:
    /// the trap with the target as tval), so the step is comparable.
    FetchFault {
        /// The pc whose fetch faulted.
        at: u64,
    },
    /// The model or the harness is wrong; the failed step is NOT an observation (nothing
    /// about it is trustworthy).
    Failed(ModelError),
    /// A source-classified unspecified/reserved case (D-RESERVED-DECODE); carried, not
    /// converted.
    Undefined(UndefinedCase),
}

/// The trace a run produced: one observation per executed step, plus why it stopped.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Trace {
    pub steps: Vec<Step>,
    pub stop: Stop,
}

/// One boundary crossing, recorded as it happened: the request and the answer.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Crossing {
    pub request: Request,
    /// `None` marks a target-facing failure answer (access fault / misaligned); the
    /// distinction from a contract violation is the answer's own type, preserved here.
    pub response: Result<Response, BoundaryError>,
}

/// Drives `exec::step` over `env`, recording observations until the program stops or the
/// budget is spent. Every boundary crossing is recorded in order (the second return value),
/// so a test can assert the fetch count (OB-ENV-FETCH-SUPPLY's no-extraneous-fetch clause)
/// or that a misaligned access never crossed the boundary.
///
/// This is [`run_over`] over the generated definition — the one observation path.
#[must_use]
pub fn run(env: &mut impl Environment, entry: u64, budget: usize) -> (Trace, Vec<Crossing>) {
    run_over(env, entry, budget, semulith_core::definition::INSNS)
}

/// Drives `exec::step_over` over a caller-supplied instruction table — the P1-LAB.9 mutation
/// suite's seam (`semulith-verify::mutate`). Production [`run`] passes the generated
/// `definition::INSNS`; the suite passes a table with one row mutated, so a known-wrong model
/// produces the observations the differential must catch.
#[must_use]
pub fn run_over(
    env: &mut impl Environment,
    entry: u64,
    budget: usize,
    insns: &[InsnDef],
) -> (Trace, Vec<Crossing>) {
    let (trace, crossings, _) =
        run_state_over(env, ArchitecturalState::zeroed_at(entry), budget, insns);
    (trace, crossings)
}

/// [`run_state_over`] over the generated definition — the snapshot resume's path
/// (`P2-SCALAR.7`): the run continues from a caller-supplied state instead of cold reset.
#[must_use]
pub fn run_from(
    env: &mut impl Environment,
    state: ArchitecturalState,
    budget: usize,
) -> (Trace, Vec<Crossing>) {
    let (trace, crossings, _) =
        run_state_over(env, state, budget, semulith_core::definition::INSNS);
    (trace, crossings)
}

/// The state-returning form (`P2-SCALAR.7`): the trace, the crossings, and the
/// architectural state the run ended in — what a snapshot captures mid-run.
#[must_use]
pub fn run_state(
    env: &mut impl Environment,
    state: ArchitecturalState,
    budget: usize,
) -> (Trace, Vec<Crossing>, ArchitecturalState) {
    run_state_over(env, state, budget, semulith_core::definition::INSNS)
}

/// Drives `exec::step_over` from a caller-supplied initial state. The loop is
/// [`run_over`]'s, unchanged — only the starting state differs: cold reset zeroes the
/// register file at the entry; a resume trusts the recorded state (the snapshot's own
/// identity and digest checks are what make that trust earned).
#[must_use]
pub fn run_state_over(
    env: &mut impl Environment,
    state: ArchitecturalState,
    budget: usize,
    insns: &[InsnDef],
) -> (Trace, Vec<Crossing>, ArchitecturalState) {
    let mut state = state;
    let mut crossings = Vec::new();
    let mut steps = Vec::new();
    loop {
        if steps.len() >= budget {
            return (
                Trace {
                    steps,
                    stop: Stop::Budget,
                },
                crossings,
                state,
            );
        }
        let crossing_env = &mut *env;
        let mut recorded = Recording {
            inner: crossing_env,
            log: &mut crossings,
        };
        let before = snapshot(&state);
        let pc = state.pc();
        let outcome = exec::step_over(&mut state, &mut recorded, insns);
        if let StepOutcome::Event(
            event @ TargetEvent::Exception {
                cause: ExceptionCause::InstructionAccessFault,
                ..
            },
        ) = outcome
        {
            // The fetch failed: the observation is the word-less step — the pc whose
            // fetch faulted, the trap the rule reports, and no invented word
            // (D-FETCH-FAULT-REPORT: on the jump's TARGET, not on the jump).
            steps.push(Step {
                pc,
                word: None,
                writes: Vec::new(),
                trap: Some(trap_pair(&event)),
            });
            return (
                Trace {
                    steps,
                    stop: Stop::FetchFault { at: pc },
                },
                crossings,
                state,
            );
        }
        let word = recorded_word(&recorded, pc);
        let writes = diff(before, &state);
        match outcome {
            StepOutcome::Advanced(_) => steps.push(Step {
                pc,
                word: Some(word),
                writes,
                trap: None,
            }),
            StepOutcome::Event(event) => {
                let trap = trap_pair(&event);
                steps.push(Step {
                    pc,
                    word: Some(word),
                    writes,
                    trap: Some(trap),
                });
                return (
                    Trace {
                        steps,
                        stop: Stop::Trap,
                    },
                    crossings,
                    state,
                );
            }
            StepOutcome::Undefined(case) => {
                // D-RESERVED-DECODE: the laboratory's diagnostic policy, made explicit
                // HERE in the harness — never in the interpreter. The interpreter
                // reported the source-classified unspecified case; the laboratory's
                // declared policy converts it to an illegal-instruction trap whose
                // tval is the reserved word itself (measured: both reference models
                // report exactly this). The stop reason stays `Undefined` — the
                // conversion does not launder the case's classification (SEM-07).
                let UndefinedCase::ReservedDecode { .. } = case;
                steps.push(Step {
                    pc,
                    word: Some(word),
                    writes: Vec::new(),
                    trap: Some((
                        cause_code(ExceptionCause::IllegalInstruction),
                        u64::from(word),
                    )),
                });
                return (
                    Trace {
                        steps,
                        stop: Stop::Undefined(case),
                    },
                    crossings,
                    state,
                );
            }
            StepOutcome::Failed(error) => {
                return (
                    Trace {
                        steps,
                        stop: Stop::Failed(error),
                    },
                    crossings,
                    state,
                );
            }
        }
    }
}

/// The recorded word for the step that just ran: the fetch response of the fetch this step
/// made at its pc. The contract supplies exactly one fetch per step; a recording that shows
/// otherwise is a harness bug and must not be silently read past.
fn recorded_word<E: Environment>(env: &Recording<'_, E>, pc: u64) -> u32 {
    for crossing in env.log.iter().rev() {
        match crossing {
            Crossing {
                request: Request::Fetch { addr },
                response: Ok(Response::Fetch(word)),
            } if *addr == pc => return *word,
            _ => {}
        }
    }
    panic!("run: no recorded fetch at pc {pc:#x} for the step just executed");
}

/// `pub(crate)` for `bench` (`P1-LAB.11`): the instrumented mode builds its Step stream
/// with exactly the runner's snapshot/diff, so a measured mode can never drift from the
/// observation construction it measures.
pub(crate) fn snapshot(state: &ArchitecturalState) -> [u64; 32] {
    let mut regs = [0u64; 32];
    for (i, reg) in regs.iter_mut().enumerate() {
        *reg = state.read_x(i as u8);
    }
    regs
}

pub(crate) fn diff(before: [u64; 32], after: &ArchitecturalState) -> Vec<(u8, u64)> {
    let mut writes = Vec::new();
    for (i, was) in before.iter().enumerate() {
        let now = after.read_x(i as u8);
        if now != *was {
            writes.push((i as u8, now));
        }
    }
    writes
}

/// `pub(crate)` for `bench` (`P1-LAB.11`): the diagnostic mode's crossing log is this same
/// wrapper, so the measured diagnostic overhead is the production recording's overhead.
pub(crate) struct Recording<'a, E: Environment> {
    pub(crate) inner: &'a mut E,
    pub(crate) log: &'a mut Vec<Crossing>,
}

impl<E: Environment> Environment for Recording<'_, E> {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        let response = self.inner.request(request);
        self.log.push(Crossing { request, response });
        response
    }
}

/// The observation-vocabulary trap pair for a target event: `(cause code, tval)`.
/// `pub(crate)` for `bench` (`P1-LAB.11`): the benchmark's instrumented and diagnostic modes
/// build the same Step stream through this one mapping, so a measured mode cannot drift
/// from the runner's trap spelling.
pub(crate) fn trap_pair(event: &TargetEvent) -> (u8, u64) {
    match event {
        TargetEvent::Exception { cause, at } => (cause_code(*cause), *at),
        TargetEvent::RequestedTrap { kind, at } => (
            match kind {
                RequestedTrapKind::EnvironmentCall => 0x0b,
                RequestedTrapKind::Breakpoint => 0x03,
            },
            *at,
        ),
    }
}

/// A comparison that could not run: an empty observation stream is never a match — a model
/// that produced nothing agreed to nothing.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct CompareError(pub String);

/// The outcome of walking two observation streams together.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Verdict {
    /// Both streams are identical for their whole length.
    Agree { steps: usize },
    /// The first step at which the observations differ, named precisely.
    Divergence(Divergence),
    /// One stream ended before the other; the agreeing prefix is not a pass.
    LengthMismatch {
        agreed: usize,
        /// The name of the stream that continued.
        longer: String,
    },
}

/// The first differing observation: which step, which field, both models' values.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Divergence {
    pub at: usize,
    pub what: String,
}

/// Walk two observation streams and report the first divergence, a length mismatch, or
/// agreement. `names` label the two streams in reports.
pub fn compare(a: &[Step], b: &[Step], names: (&str, &str)) -> Result<Verdict, CompareError> {
    if a.is_empty() || b.is_empty() {
        return Err(CompareError(format!(
            "{} has {} step(s), {} has {} — an empty trace is not a match",
            names.0,
            a.len(),
            names.1,
            b.len()
        )));
    }
    let n = a.len().min(b.len());
    for i in 0..n {
        if a[i].same_observation(&b[i]) {
            continue;
        }
        let what = if a[i].pc != b[i].pc {
            format!(
                "pc: {} observes {:#018x}, {} observes {:#018x}",
                names.0, a[i].pc, names.1, b[i].pc
            )
        } else if a[i].word != b[i].word {
            let word = |s: &Step| match s.word {
                Some(word) => format!("{word:#010x}"),
                None => "no word (a fetch fault)".to_string(),
            };
            format!(
                "the instruction word at {:#018x}: {} observes {}, {} observes {}",
                a[i].pc,
                names.0,
                word(&a[i]),
                names.1,
                word(&b[i])
            )
        } else if a[i].writes != b[i].writes {
            let detail = write_diff(&a[i].writes, &b[i].writes, names);
            format!("a register write at {:#018x}: {detail}", a[i].pc)
        } else {
            match (&a[i].trap, &b[i].trap) {
                (Some((ca, _)), Some((cb, _))) if ca != cb => format!(
                    "the trap cause at {:#018x}: {} observes {:#04x}, {} observes {:#04x}",
                    a[i].pc, names.0, ca, names.1, cb
                ),
                (Some((_, ta)), Some((_, tb))) if ta != tb => format!(
                    "the trap tval at {:#018x}: {} observes {:#018x}, {} observes {:#018x}",
                    a[i].pc, names.0, ta, names.1, tb
                ),
                (Some(_), None) => format!(
                    "{} observes a trap at {:#018x} that {} does not",
                    names.0, a[i].pc, names.1
                ),
                (None, Some(_)) => format!(
                    "{} observes a trap at {:#018x} that {} does not",
                    names.1, a[i].pc, names.0
                ),
                _ => unreachable!("keys differ but no field differs"),
            }
        };
        return Ok(Verdict::Divergence(Divergence { at: i, what }));
    }
    if a.len() != b.len() {
        let longer = if a.len() > b.len() { names.0 } else { names.1 };
        return Ok(Verdict::LengthMismatch {
            agreed: n,
            longer: longer.to_string(),
        });
    }
    Ok(Verdict::Agree { steps: n })
}

fn write_diff(a: &[(u8, u64)], b: &[(u8, u64)], names: (&str, &str)) -> String {
    let mut seen = std::collections::BTreeSet::new();
    for (reg, _) in a.iter().chain(b.iter()) {
        if !seen.insert(*reg) {
            continue;
        }
        let av = a.iter().find(|(r, _)| r == reg).map(|(_, v)| *v);
        let bv = b.iter().find(|(r, _)| r == reg).map(|(_, v)| *v);
        match (av, bv) {
            (Some(x), Some(y)) if x != y => {
                return format!(
                    "{} observes x{reg} = {x:#018x}, {} observes x{reg} = {y:#018x}",
                    names.0, names.1
                );
            }
            (Some(x), None) => {
                return format!(
                    "{} observes x{reg} = {x:#018x}, {} observes no write",
                    names.0, names.1
                );
            }
            (None, Some(y)) => {
                return format!(
                    "{} observes x{reg} = {y:#018x}, {} observes no write",
                    names.1, names.0
                );
            }
            _ => {}
        }
    }
    "register write sets differ".to_string()
}

/// Render a verdict the way the evidence report prints it: the first divergence named, or
/// agreement, or the length-mismatch refusal.
#[must_use]
pub fn render(verdict: &Verdict, a_len: usize, b_len: usize, names: (&str, &str)) -> String {
    match verdict {
        Verdict::Agree { steps } => format!(
            "AGREE over {steps} aligned step(s) ({}: {a_len} parsed, {}: {b_len} parsed)",
            names.0, names.1
        ),
        Verdict::Divergence(d) => format!("FIRST DIVERGENCE at aligned step {}\n  {}", d.at, d.what),
        Verdict::LengthMismatch { agreed, longer } => format!(
            "LENGTH MISMATCH after {agreed} agreeing step(s): {} produced {a_len}, {} produced {b_len}\n  \
             {longer} continues past the shorter trace. The agreeing prefix is NOT a pass — \
             explain why one model stopped before recording this as evidence.",
            names.0, names.1
        ),
    }
}

#[cfg(test)]
mod tests;
