//! Tests for the typed outcome families (`P1-LAB.5`). The acceptance criteria:
//!
//! 1. a target exception can be **delivered and execution continue** — demonstrated with
//!    a stub stepper (test code, not instruction semantics): the harness records the
//!    event and steps on;
//! 2. an **unimplemented instruction cannot be reported as an illegal-instruction
//!    trap** — the families are distinct by construction, and the test proves the match
//!    arms enforce it.

use super::*;
use crate::state::ArchitecturalState;

/// A stub instruction — enough shape to exercise the outcome families without any
/// production semantics (those belong to `.8`).
#[derive(Clone, Copy)]
enum Stub {
    /// Add a value to a register: a completing instruction.
    Add { reg: u8, value: u64 },
    /// An EBREAK: a requested trap.
    Break,
    /// An instruction this model does not have.
    Missing,
}

/// The stub's step: what each kind of instruction produces as a [`StepOutcome`]. An
/// unimplemented instruction reports `ModelError::Unimplemented` — SEM-02's rule, in the
/// one place this test can own it.
fn stub_step(state: &mut ArchitecturalState, stub: Stub) -> StepOutcome {
    match stub {
        Stub::Add { reg, value } => {
            state.write_x(reg, state.read_x(reg) + value);
            StepOutcome::Advanced(Advance::Completed)
        }
        Stub::Break => StepOutcome::Event(TargetEvent::RequestedTrap {
            kind: RequestedTrapKind::Breakpoint,
            at: state.pc(),
        }),
        Stub::Missing => StepOutcome::Failed(ModelError::Unimplemented {
            what: "stub extension instruction",
        }),
    }
}

#[test]
fn a_delivered_exception_lets_execution_continue() {
    // The acceptance, first clause: a target exception is delivered to the harness and
    // execution continues — REQ-D-ECALL-EBREAK: "execution stops unless the harness
    // contract says otherwise." Here the contract says otherwise.
    let mut state = ArchitecturalState::zeroed_at(0x1000);
    let program = [
        Stub::Add { reg: 5, value: 1 },
        Stub::Break,
        Stub::Add { reg: 5, value: 1 },
    ];
    let mut delivered = Vec::new();
    for stub in program {
        match stub_step(&mut state, stub) {
            StepOutcome::Event(event) => {
                delivered.push(event); // delivered to the harness…
                state.set_pc(state.pc() + 4); // …and execution continues
            }
            StepOutcome::Advanced(Advance::Completed) => state.set_pc(state.pc() + 4),
            other => panic!("the stub program produced {other:?}"),
        }
    }
    assert_eq!(
        delivered,
        vec![TargetEvent::RequestedTrap {
            kind: RequestedTrapKind::Breakpoint,
            at: 0x1004,
        }]
    );
    assert_eq!(state.read_x(5), 2, "the instruction after the trap ran");
    assert_eq!(state.pc(), 0x100C, "pc advanced past the whole program");
}

#[test]
fn an_unimplemented_instruction_is_not_an_illegal_instruction_trap() {
    // The acceptance, second clause (SEM-02): the stub stepper's Missing arm is a
    // ModelError, and extracting an IllegalInstruction trap out of it is not a match the
    // type allows — the only Exception constructor is TargetEvent::Exception, which the
    // Missing arm never produces.
    let mut state = ArchitecturalState::zeroed_at(0x1000);
    let outcome = stub_step(&mut state, Stub::Missing);
    assert_eq!(
        outcome,
        StepOutcome::Failed(ModelError::Unimplemented {
            what: "stub extension instruction"
        })
    );
    // Exhaustive match: every way to read a target event out of a StepOutcome goes
    // through the Event arm — Failed carries no ExceptionCause, so "unimplemented, but
    // reported as a trap" has no typed expression.
    let trap_reported = match outcome {
        StepOutcome::Event(TargetEvent::Exception {
            cause: ExceptionCause::IllegalInstruction,
            ..
        }) => true,
        StepOutcome::Event(_) | StepOutcome::Advanced(_) | StepOutcome::Undefined(_) => false,
        StepOutcome::Failed(ModelError::ContractViolation(_)) => false,
        StepOutcome::Failed(_) => false,
    };
    assert!(!trap_reported, "a model gap dressed as a target trap");
}

#[test]
fn the_four_families_are_distinct_values() {
    // SEM-01 as a value-level fact: same step shape, four different families, and no
    // From impl crosses between them.
    let advanced = StepOutcome::Advanced(Advance::Stop {
        reason: StopReason::TrapReported,
    });
    let event = StepOutcome::Event(TargetEvent::Exception {
        cause: ExceptionCause::LoadAddressMisaligned,
        at: 0x2000,
    });
    let undefined = StepOutcome::Undefined(UndefinedCase::ReservedDecode { at: 0x3000 });
    let failed = StepOutcome::Failed(ModelError::InconsistentState { what: "self-test" });
    let all = [advanced, event, undefined, failed];
    assert_eq!(all.len(), 4);
    let mut families = all.to_vec();
    families.dedup();
    assert_eq!(families.len(), 4, "no two families collapse into one value");
}

#[test]
fn env_contract_violations_re_home_into_model_error() {
    // P1-LAB.4's boundary-local ContractViolation joins the ModelError family (SEM-01's
    // harness-contract-violation member).
    let violation = crate::env::ContractViolation::ScriptExhausted;
    let error = ModelError::from(violation);
    assert_eq!(error, ModelError::ContractViolation(violation));
    let StepOutcome::Failed(ModelError::ContractViolation(back)) = StepOutcome::Failed(error)
    else {
        panic!("the re-homed violation survives a StepOutcome round trip");
    };
    assert_eq!(back, violation);
}

#[test]
fn reserved_decode_carries_its_source_classification() {
    // REQ-D-RESERVED-DECODE: the outcome exists so the report need not disguise itself
    // as an exception. Undefined is not Event; the conversion is the policy's act.
    let outcome = StepOutcome::Undefined(UndefinedCase::ReservedDecode { at: 0x4000 });
    assert!(matches!(outcome, StepOutcome::Undefined(_)));
    assert_ne!(
        outcome,
        StepOutcome::Event(TargetEvent::Exception {
            cause: ExceptionCause::IllegalInstruction,
            at: 0x4000,
        }),
        "an unspecified case is not silently an illegal-instruction trap"
    );
}
