//! The rv64gc corpus runner — `P4-SYSTEM.2` slice h (the route flip): the verify-side
//! driver that executes the unit's tracked guests through the TRACKED engine
//! (`semulith_core::exec_rv64gc`), where every slice before this one proved the corpus on
//! the scratch harness (`decision_generated-mirror-needs-tracked-input` — the generated
//! modules are tracked now, so the engine that consumes them is too).
//!
//! The composition DELIVERS every target-visible fault (the zicsr refinement), so unlike
//! [`crate::run`] there is no trap stop: a run executes exactly the expectations' declared
//! step count — continuation past a delivered trap into an unprogrammed vector is out of
//! the corpus's vocabulary by convention, and the declared count is what makes the run's
//! end observable. One fetch per step, one effect per step, register writes observed as
//! CHANGES (a register written its own value is no observation — the same comparison rule
//! as the base profile's offline differential).
//!
//! The diagnostic policy's one act lives here, one layer up from the evaluator
//! (`D-RESERVED-DECODE`): a reserved-decode report converts to the delivered
//! illegal-instruction cause with tval the word — the same rule as rv64i's, delivered
//! rather than reported on this composition.

use semulith_core::env::{BoundaryError, Environment, Request, Response};
use semulith_core::exec_rv64gc::{self, StepRv64gc};
use semulith_core::privilege;
use semulith_core::state_rv64gc::ArchitecturalState;

use crate::fixtures::FlatMemory;
use crate::guests_rv64gc::{Guest, GUESTS};

/// The fetch-request witness: forwards every crossing and counts fetch REQUESTS
/// (successful or faulted — a delivered fetch-fault step's request crossed the boundary
/// and was refused, which is still exactly one fetch for that step).
struct CountFetches<'a> {
    inner: &'a mut FlatMemory,
    fetches: u64,
}

impl Environment for CountFetches<'_> {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        if matches!(request, Request::Fetch { .. }) {
            self.fetches += 1;
        }
        self.inner.request(request)
    }
}

/// One executed step: the pc the instruction was fetched at, the mode the hart was in,
/// and the register CHANGES its effect produced (name, new value), in register order.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Step {
    /// The fetched pc.
    pub pc: u64,
    /// The privilege mode the step executed in (the delivery composition's own
    /// observation — a mode change is visible as control flow, never as a register write).
    pub mode: semulith_core::privilege::PrivilegeMode,
    /// The step's register writes.
    pub writes: Vec<(u8, u64)>,
}

/// A guest's full run: exactly the declared step count, or the model error that ended it
/// early (SEM-02 — a test failure, never a target observation), and the fetch-request
/// count (the no-extraneous-fetch witness).
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Trace {
    /// The executed steps.
    pub steps: Vec<Step>,
    /// The model error, when the run ended on one.
    pub failed: Option<String>,
    /// How many fetch requests the run made (faulted requests included).
    pub fetches: u64,
}

/// Run one tracked guest through the tracked engine: the image at the declared entry,
/// the region the base corpus's fixtures use (64 KiB at the entry — every observation
/// the corpus makes is identical under any size from there to the platform's 2 GiB, the
/// base fixture's own argument), the fetch alignment the profile declares (2 bytes,
/// IALIGN=16 with C), exactly `executed_steps` steps.
#[must_use]
pub fn run_guest(guest: &Guest) -> (Trace, FlatMemory) {
    let mut env = FlatMemory::with_fetch_align(guest.entry, 0x10000, 2);
    let mut image = Vec::with_capacity(guest.words.len() * 4);
    for word in guest.words {
        image.extend_from_slice(&word.to_le_bytes());
    }
    env.load_image(0, &image);
    let mut state = ArchitecturalState::zeroed_at(guest.entry);
    let mut steps = Vec::new();
    let mut failed = None;
    let mut fetches = 0;
    for _ in 0..guest.executed_steps {
        let pc = state.pc();
        let before: Vec<u64> = (0..32).map(|i| state.read_x(i)).collect();
        let mut counting = CountFetches {
            inner: &mut env,
            fetches: 0,
        };
        let outcome = exec_rv64gc::step(&mut state, &mut counting);
        fetches += counting.fetches;
        match outcome {
            StepRv64gc::Executed => {}
            StepRv64gc::ReservedDecode { at, word } => {
                // D-RESERVED-DECODE: the diagnostic policy's conversion, one layer up —
                // the delivered illegal-instruction cause, tval the offending word.
                let handler = privilege::trap_deliver(&mut state, 2, u64::from(word), at);
                state.set_pc(handler);
            }
            StepRv64gc::Failed(error) => {
                failed = Some(format!("{error:?}"));
                break;
            }
        }
        let mut writes = Vec::new();
        for i in 0..32u8 {
            let now = state.read_x(i);
            if now != before[i as usize] {
                writes.push((i, now));
            }
        }
        steps.push(Step {
            pc,
            mode: state.mode(),
            writes,
        });
    }
    (
        Trace {
            steps,
            failed,
            fetches,
        },
        env,
    )
}

/// Find a tracked guest by name — the same lookup the base runner's tests use.
#[must_use]
pub fn guest(name: &str) -> &'static Guest {
    GUESTS
        .iter()
        .find(|g| g.name == name)
        .unwrap_or_else(|| panic!("guest {name} is in the generated fixture"))
}

#[cfg(test)]
mod tests;
