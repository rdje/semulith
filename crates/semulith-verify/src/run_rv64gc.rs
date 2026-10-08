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
//! end observable. Fetch counts record actual word/parcel boundary requests. Register
//! writes are observed as CHANGES (a register written its own value is no observation —
//! the same comparison rule as the base profile's offline differential).
//!
//! The diagnostic policy's one act lives here, one layer up from the evaluator
//! (`D-RESERVED-DECODE`): a reserved-decode report converts to the delivered
//! illegal-instruction cause with tval the word — the same rule as rv64i's, delivered
//! rather than reported on this composition.

use semulith_core::env::{BoundaryError, Environment, Failure, Request, Response};
use semulith_core::exec_rv64gc::{self, StepRv64gc};
use semulith_core::privilege;
use semulith_core::state_rv64gc::ArchitecturalState;

use crate::fixtures::FlatMemory;
use crate::guests_rv64gc::{Guest, Refusal, RefusalKind, GUESTS};

/// The fetch-request witness: forwards every crossing and counts fetch REQUESTS
/// (successful or faulted — a refused request still crossed the boundary). A C-enabled
/// table issues one parcel for a compressed instruction and two for a 32-bit instruction,
/// unless a fault or another delivery prevents a request.
struct CountFetches<'a> {
    inner: &'a mut Refusing<'a>,
    fetches: u64,
}

impl Environment for CountFetches<'_> {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        if matches!(request, Request::Fetch { .. } | Request::FetchParcel { .. }) {
            self.fetches += 1;
        }
        self.inner.request(request)
    }
}

/// The experiment's TYPED fault injection (`P4-SYSTEM.8` slice c): every request whose kind
/// a declared refusal names and whose bytes intersect its region is answered with an access
/// fault — the environment refusing, never a hook inside an instruction. Everything else
/// forwards untouched.
struct Refusing<'a> {
    inner: &'a mut FlatMemory,
    refusals: &'static [Refusal],
}

/// The bytes a request touches, and the refusal kind it answers to.
fn request_span(request: &Request) -> (RefusalKind, u64, u64) {
    match *request {
        Request::Fetch { addr } => (RefusalKind::Fetch, addr, 4),
        Request::FetchParcel { addr } => (RefusalKind::Fetch, addr, 2),
        Request::Load { width, addr } => (RefusalKind::Load, addr, width.bytes()),
        Request::Store { width, addr, .. } => (RefusalKind::Store, addr, width.bytes()),
        Request::WalkAccess { addr } => (RefusalKind::Walk, addr, 8),
    }
}

/// Does a refusal region answer this request? Intersection of `[addr, addr + len)` with
/// `[base, base + size)`, computed in u128 so no region wraps.
fn refused(refusals: &[Refusal], request: &Request) -> bool {
    let (kind, addr, len) = request_span(request);
    refusals.iter().any(|r| {
        r.kind == kind
            && u128::from(addr) < u128::from(r.base) + u128::from(r.size)
            && u128::from(r.base) < u128::from(addr) + u128::from(len)
    })
}

impl Environment for Refusing<'_> {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        if refused(self.refusals, &request) {
            return Err(Failure::AccessFault.into());
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
    env.load_image(0, guest.image);
    let mut state = ArchitecturalState::zeroed_at(guest.entry);
    let mut steps = Vec::new();
    let mut failed = None;
    let mut fetches = 0;
    for _ in 0..guest.executed_steps {
        let pc = state.pc();
        let before: Vec<u64> = (0..32).map(|i| state.read_x(i)).collect();
        let mut refusing = Refusing {
            inner: &mut env,
            refusals: guest.refusals,
        };
        let mut counting = CountFetches {
            inner: &mut refusing,
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

/// The corpus's comparison rule for one guest (the specification-derived writes per step,
/// the never-written registers, the fetch count) — shared by the corpus proof and the
/// contract-check registry (`P4-SYSTEM.9` slice b), so both judge by exactly one rule.
#[cfg(test)]
pub(crate) fn assert_guest_observations(name: &str) {
    let g = guest(name);
    let (trace, _env) = run_guest(g);
    assert!(
        trace.failed.is_none(),
        "{name}: the run ended on a model error: {:?}",
        trace.failed
    );
    assert_eq!(
        trace.steps.len(),
        g.executed_steps,
        "{name}: the trace runs exactly the declared step count"
    );
    for (i, expected) in g.expected.iter().enumerate() {
        assert_eq!(
            expected.step, i,
            "{name}: the fixture's expectations are declared in step order"
        );
        assert_eq!(
            trace.steps[i].writes, expected.writes,
            "{name}: step {i} writes match the specification-derived expectations"
        );
    }
    let mut written: Vec<u8> = trace
        .steps
        .iter()
        .flat_map(|s| s.writes.iter().map(|(r, _)| *r))
        .collect();
    written.sort_unstable();
    for reg in g.never_written {
        assert!(
            !written.contains(reg),
            "{name}: x{reg} must never be written, but the trace wrote it"
        );
    }
    assert_eq!(
        trace.fetches as usize, g.expected_fetches,
        "{name}: the actual word/parcel boundary requests match the declared expectation \
         (faulted requests included; walk faults, interrupts and waiting can prevent requests)"
    );
}

#[cfg(test)]
mod tests;
