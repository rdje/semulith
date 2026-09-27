//! The typed outcome families — SEM-01's separation, made structural
//! (`docs/ARCHITECTURE.md` §5): model limitation, internal error, malformed input, target
//! exception, undefined-case diagnostic, wait and control stop remain distinct typed
//! outcomes, and no `From` impl ever crosses the families.
//!
//! The four families, and what each one IS:
//!
//! - [`TargetEvent`] — something the *target* did under a named source rule: a synchronous
//!   exception, a requested trap (ECALL/EBREAK). Delivery is a data event, not a stop
//!   command: the harness receives it and decides whether execution continues (OB-ENV-EVENT-
//!   DELIVERY pins the delivery point to the instruction that raised the condition;
//!   REQ-D-ECALL-EBREAK says execution stops *unless the harness contract says otherwise*).
//! - [`Advance`] — execution progress: an instruction completed, or a requested control
//!   stop. There is no waiting in this profile (no `WFI` reaches it without privileged
//!   modes, and nothing could wake one — OB-ENV-VIRTUAL-TIME) and no partial progress
//!   (OB-ENV-PARTIAL-PROGRESS: every instruction completes or faults as a unit).
//! - [`ModelError`] — the model or the harness is wrong: missing behavior, an invalid
//!   description, inconsistent state, or a harness contract violation. SEM-02: none of
//!   these may ever be emitted as a target exception. `env`'s [`ContractViolation`] re-homes
//!   here — the boundary's error family was boundary-local since `.4` and is a model error
//!   by SEM-01's taxonomy.
//! - [`UndefinedCase`] — a case the *source* classifies as unspecified/reserved, carried as
//!   its own outcome under the run's diagnostic policy. REQ-D-RESERVED-DECODE: the model
//!   must be able to report that the case WAS unspecified — so this outcome is never
//!   silently converted into [`TargetEvent::Exception`]; conversion is the policy's explicit
//!   act, and it must stay able to say why.
//!
//! Precise shapes are a P1 design result (ARCHITECTURE §5); these are the families the
//! interpreter slice (`.8`) composes, nothing more invented than a consumer needs.

use crate::env::ContractViolation;

/// Something the target did, under a named source rule. Receiving one is not stopping:
/// the harness decides continuation per its contract.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum TargetEvent {
    /// A synchronous exception, delivered at the instruction that raised it
    /// (OB-ENV-EVENT-DELIVERY). `at` is where the rule reports it — the branch, or the
    /// target, per REQ-D-MISALIGN-REPORT / REQ-D-FETCH-FAULT-REPORT; that positioning is
    /// instruction-layer and arrives with the interpreter (`.8`).
    Exception {
        /// The exception cause — the vocabulary of the unprivileged spec's synchronous
        /// exceptions, report-only here (this profile models no privileged CSR to hold it).
        cause: ExceptionCause,
        /// The address the rule reports the exception at.
        at: u64,
    },
    /// A precise requested trap (REQ-D-ECALL-EBREAK): reported to the harness as a typed
    /// environment-trap outcome; execution stops unless the harness contract says
    /// otherwise — which is the harness's reading of this event, not the event's command.
    RequestedTrap {
        /// Which requested trap.
        kind: RequestedTrapKind,
        /// The address of the trapping instruction.
        at: u64,
    },
}

/// The synchronous-exception cause vocabulary of `rv64i-lab-v0` — the unprivileged spec's
/// causes, each named by the rule that raises it. Carried as data because this profile
/// models no privileged CSR; the causes exist whether or not an instruction can read them.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum ExceptionCause {
    /// Taken branch/jump target not 4-byte aligned (REQ-D-IALIGN, REQ-D-MISALIGN-REPORT).
    InstructionAddressMisaligned,
    /// Instruction fetch outside the declared executable region
    /// (REQ-D-FETCH-FAULT-REPORT, OB-ADDRESS-SPACE).
    InstructionAccessFault,
    /// An encoding that is illegal under the active decode policy. The profile's RESERVED
    /// space is not automatically this — see [`UndefinedCase`].
    IllegalInstruction,
    /// A misaligned load (OB-MISALIGN-DATA — raised, not handled invisibly).
    LoadAddressMisaligned,
    /// A load outside every declared region (OB-ADDRESS-SPACE).
    LoadAccessFault,
    /// A misaligned store (OB-MISALIGN-DATA).
    StoreAddressMisaligned,
    /// A store outside every declared region (OB-ADDRESS-SPACE).
    StoreAccessFault,
}

/// The requested traps of `rv64i-lab-v0` (REQ-D-ECALL-EBREAK) — deliberate, synchronous,
/// and reported to the harness rather than to a guest handler (no privilege modes).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum RequestedTrapKind {
    /// `ECALL` — a request for the execution environment's attention.
    EnvironmentCall,
    /// `EBREAK` — a request for the debugger's attention.
    Breakpoint,
}

/// Execution progress: a step completed, or control stopped by request. There is no
/// `Waited` in this profile (nothing can wake one) and no partial advance
/// (OB-ENV-PARTIAL-PROGRESS) — both absences are platform facts, recorded here so a
/// future extension reopens them in the type, not around it.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Advance {
    /// The instruction at the current pc completed; pc has moved on.
    Completed,
    /// Execution stopped by request — a reported trap with no continuation in the harness
    /// contract, or a harness stop. Stopping is a control outcome, never an error and
    /// never a target event.
    Stop {
        /// Why the stop was requested.
        reason: StopReason,
    },
}

/// Why a control stop was requested.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum StopReason {
    /// A trap was reported and the harness contract provides no continuation
    /// (REQ-D-ECALL-EBREAK's default).
    TrapReported,
    /// The harness asked to stop (a breakpoint in the test driver, a step budget spent).
    HarnessRequest,
}

/// The model or the harness is wrong. SEM-02: none of these may be emitted as a target
/// exception — an unimplemented instruction is a `ModelError`, never an
/// `IllegalInstruction` trap, because the target did nothing wrong.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum ModelError {
    /// Behavior the model does not have yet — an unimplemented instruction, an
    /// unmodeled case. The honest report of a gap; pretending the target trapped is the
    /// substitution SEM-02 forbids.
    Unimplemented {
        /// What is missing — a name stable enough for a divergence report.
        what: &'static str,
    },
    /// A description or configuration is invalid — a malformed descriptor, an
    /// inconsistent fixture setup.
    InvalidDescription {
        /// What is invalid.
        what: &'static str,
    },
    /// Internal state became inconsistent — the model contradicted itself.
    InconsistentState {
        /// What broke.
        what: &'static str,
    },
    /// The harness (environment fixture) violated the request/response contract
    /// (SEM-01's harness-contract-violation member; re-homed from `env`'s boundary-local
    /// family, `P1-LAB.4`).
    ContractViolation(ContractViolation),
}

impl From<ContractViolation> for ModelError {
    fn from(violation: ContractViolation) -> Self {
        Self::ContractViolation(violation)
    }
}

/// A case the source classifies as unspecified or reserved, carried under the run's
/// diagnostic policy. REQ-D-RESERVED-DECODE requires the model to be able to report that
/// the case WAS unspecified — so this family exists precisely so the report does not have
/// to disguise itself as an exception.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum UndefinedCase {
    /// A reserved encoding reached decode (REQ-D-RESERVED-DECODE, REQ-D-SHIFTW-RESERVED).
    /// What happens next is the diagnostic policy's explicit act — trap as
    /// [`TargetEvent::Exception`], halt with the report, explore — and the report keeps
    /// the case's source classification either way.
    ReservedDecode {
        /// The address of the reserved word.
        at: u64,
    },
}

/// Everything one step of execution can produce. The interpreter (`.8`) returns this;
/// the harness matches on it. The families stay separable: a harness that only wants
/// events can match `Event` and leave the rest to a default arm without ever confusing a
/// model error for a target trap.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum StepOutcome {
    /// Execution progressed.
    Advanced(Advance),
    /// The target did something under a named rule.
    Event(TargetEvent),
    /// A source-classified unspecified/reserved case; the policy decides.
    Undefined(UndefinedCase),
    /// The model or harness is wrong (SEM-01, SEM-02).
    Failed(ModelError),
}

#[cfg(test)]
mod tests;
