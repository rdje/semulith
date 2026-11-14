//! Declared device regions under `OB-GC-ENV-DATA-ACCESS-V4` (`P4-SYSTEM.20` slice e).
//!
//! A device region's reads have side effects. It answers `Load` and `Store` of its declared
//! widths, naturally aligned and wholly inside it, and refuses everything else with an
//! access fault and no side effect: an `AtomicLoad`, a `StorePermission`, a `Fetch` or
//! `FetchParcel`, a `WalkAccess`, and any access of an undeclared width or extent. So no
//! instruction is fetched from it, no page table lives in it, and no atomic touches it — a
//! nonmatching SC's permission check is refused too, since a device can hold no reservation.
//!
//! The laboratory declares no device region. This fixture is the provider a board would be,
//! so the CPU's half of the composition is checked before any board exists: each refusal
//! becomes the architectural access fault of the original access, with no partial effect,
//! and a plain load reads the device exactly once. Its negative is the fixture auditor: with
//! the region map as its witness, it names a device that answers, or takes a side effect
//! for, a request it had to refuse.

use semulith_core::env::{
    AccessWidth, BoundaryError, ContractViolation, Environment, Failure, Request, Response,
};
use semulith_core::exec_rv64gc::{self, StepRv64gc};
use semulith_core::outcome::ModelError;
use semulith_core::privilege::PrivilegedHart;
use semulith_core::state_rv64gc::{
    ArchitecturalState, PrivilegeMode, CSR_MCAUSE, CSR_MEPC, CSR_MTVAL, CSR_SATP,
};

use crate::fixtures::FlatMemory;

const ENTRY: u64 = 0x1000;
/// One page-aligned 4 KiB device region, so a page-table walk can be rooted in it.
const DEVICE: u64 = 0x4000_0000;
const DEVICE_SIZE: u64 = 0x1000;
/// The device's first read value; each successful read returns the next one.
const FIRST: u64 = 0x10;
const SENTINEL: u64 = 0x1234;

/// Hand-encoded words, each with rd = x6 and rs1 = x5 (the device address); x7 is the
/// AMO and SC source.
const LW: u32 = 0x0002_a303;
const LD: u32 = 0x0002_b303;
const LB: u32 = 0x0002_8303;
const SW: u32 = 0x0062_a023;
const LR_W: u32 = 0x1002_a32f;
const AMOADD_W: u32 = 0x0072_a32f;
const SC_W: u32 = 0x1872_a32f;
const ADDI: u32 = 0x0010_0313;

/// A read-side-effecting device register: each successful read returns its count and
/// advances it — a FIFO's shape — so a second read is visible in the value as well as in
/// the count.
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
struct Device {
    reads: u64,
    writes: u64,
    last_write: u64,
}

impl Device {
    fn read(&mut self) -> u64 {
        let value = FIRST + self.reads;
        self.reads += 1;
        value
    }
}

/// How the provider's device region behaves.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum Conformance {
    /// As `OB-GC-ENV-DATA-ACCESS-V4` requires.
    Conforming,
    /// Answers atomic reads and store-permission checks as main memory would: the atomic
    /// read takes the device's side-effecting read.
    AnswersAtomics,
    /// Refuses as required, but only after taking the side-effecting read.
    RefusesAfterReading,
}

/// The bytes a request touches.
fn span(request: Request) -> (u64, u64) {
    match request {
        Request::Fetch { addr } => (addr, 4),
        Request::FetchParcel { addr } => (addr, 2),
        Request::Load { width, addr }
        | Request::AtomicLoad { width, addr }
        | Request::Store { width, addr, .. }
        | Request::StorePermission { width, addr } => (addr, width.bytes()),
        Request::WalkAccess { addr } => (addr, 8),
    }
}

/// Does `[addr, addr + len)` touch the device region? Computed in u128, so nothing wraps.
fn touches_device(request: Request) -> bool {
    let (addr, len) = span(request);
    u128::from(addr) < u128::from(DEVICE) + u128::from(DEVICE_SIZE)
        && u128::from(DEVICE) < u128::from(addr) + u128::from(len)
}

/// Is this a device access the region answers: a `Load` or `Store` of a declared width
/// (W or D), naturally aligned and wholly inside the region?
fn device_answers(request: Request) -> bool {
    let (Request::Load { width, addr } | Request::Store { width, addr, .. }) = request else {
        return false;
    };
    matches!(width, AccessWidth::W | AccessWidth::D)
        && addr % width.bytes() == 0
        && addr >= DEVICE
        && addr - DEVICE <= DEVICE_SIZE - width.bytes()
}

/// Main memory at `ENTRY`, plus one declared device region.
struct DeviceMap {
    memory: FlatMemory,
    device: Device,
    conformance: Conformance,
}

impl DeviceMap {
    fn new(word: u32, conformance: Conformance) -> Self {
        let mut memory = FlatMemory::with_fetch_align(ENTRY, 48, 2);
        memory.load_image(0, &word.to_le_bytes());
        Self {
            memory,
            device: Device::default(),
            conformance,
        }
    }
}

impl Environment for DeviceMap {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        if !touches_device(request) {
            return self.memory.request(request);
        }
        if device_answers(request) {
            return Ok(match request {
                Request::Store { data, width, .. } => {
                    self.device.writes += 1;
                    self.device.last_write = data & (u64::MAX >> (64 - width.bits()));
                    Response::StoreDone
                }
                _ => Response::Load(self.device.read()),
            });
        }
        match (self.conformance, request) {
            (Conformance::AnswersAtomics, Request::AtomicLoad { .. }) => {
                Ok(Response::Load(self.device.read()))
            }
            (Conformance::AnswersAtomics, Request::StorePermission { .. }) => {
                Ok(Response::StorePermitted)
            }
            (Conformance::RefusesAfterReading, _) => {
                self.device.read();
                Err(Failure::AccessFault.into())
            }
            _ => Err(Failure::AccessFault.into()),
        }
    }
}

/// The fixture-only auditor. Its witness is the region map: a request that touches the
/// device and is not one the device answers must be refused, and refused without a side
/// effect. It has no role in ordinary CPU execution.
struct DeviceAuditor {
    map: DeviceMap,
    enabled: bool,
}

impl Environment for DeviceAuditor {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        let must_refuse = touches_device(request) && !device_answers(request);
        let before = self.map.device;
        let answer = self.map.request(request);
        if self.enabled && must_refuse && (answer.is_ok() || self.map.device != before) {
            return Err(ContractViolation::DeviceRefusalBroken { request }.into());
        }
        answer
    }
}

/// A hart at `pc` in M-mode with Bare translation; x5 names the device and x6 holds the
/// sentinel a refused access must leave in place.
fn hart(pc: u64) -> ArchitecturalState {
    let mut hart = ArchitecturalState::zeroed_at(pc);
    hart.write_x(5, DEVICE);
    hart.write_x(6, SENTINEL);
    hart.write_x(7, 0x55);
    hart
}

/// One refusal case: how the hart is placed, and the access fault the refusal becomes.
struct Refusal {
    what: &'static str,
    word: u32,
    hart: fn() -> ArchitecturalState,
    cause: u64,
    tval: u64,
}

fn at_entry() -> ArchitecturalState {
    hart(ENTRY)
}

fn in_device() -> ArchitecturalState {
    hart(DEVICE)
}

/// S-mode under Sv39 with the root page table in the device region: the fetch's own walk
/// reads the device.
fn walk_rooted_in_device() -> ArchitecturalState {
    let mut hart = hart(ENTRY);
    hart.set_mode(PrivilegeMode::S);
    hart.write_csr(CSR_SATP, (8 << 60) | (DEVICE >> 12));
    hart
}

const REFUSALS: [Refusal; 6] = [
    Refusal {
        what: "LR.W: an atomic read",
        word: LR_W,
        hart: at_entry,
        cause: 5,
        tval: DEVICE,
    },
    Refusal {
        what: "AMOADD.W: an atomic read",
        word: AMOADD_W,
        hart: at_entry,
        cause: 7,
        tval: DEVICE,
    },
    Refusal {
        what: "SC.W with no reservation: a store-permission check",
        word: SC_W,
        hart: at_entry,
        cause: 7,
        tval: DEVICE,
    },
    Refusal {
        what: "LB: a width the region does not declare",
        word: LB,
        hart: at_entry,
        cause: 5,
        tval: DEVICE,
    },
    Refusal {
        what: "a fetch from the region",
        word: ADDI,
        hart: in_device,
        cause: 1,
        tval: DEVICE,
    },
    Refusal {
        what: "a page-table walk rooted in the region",
        word: ADDI,
        hart: walk_rooted_in_device,
        cause: 1,
        tval: ENTRY,
    },
];

/// Did the step leave everything but its trap untouched?
fn untouched(hart: &mut ArchitecturalState, device: Device) -> bool {
    hart.read_x(6) == SENTINEL && !hart.reservation().snapshot().2 && device == Device::default()
}

pub(super) fn positive() -> Result<(), String> {
    // A plain load reads the device exactly once per instruction, and the value shows it.
    for (word, width) in [(LW, "W"), (LD, "D")] {
        let mut map = DeviceMap::new(word, Conformance::Conforming);
        map.memory.load_image(4, &word.to_le_bytes());
        let mut hart = at_entry();
        for (n, value) in [(1, FIRST), (2, FIRST + 1)] {
            if exec_rv64gc::step(&mut hart, &mut map) != StepRv64gc::Executed
                || hart.read_x(6) != value
                || hart.read_csr(CSR_MCAUSE) != 0
                || map.device.reads != n
            {
                return Err(format!(
                    "{width} load {n}: x6 {:#x}, {} device read(s), cause {}",
                    hart.read_x(6),
                    map.device.reads,
                    hart.read_csr(CSR_MCAUSE)
                ));
            }
        }
    }
    let mut map = DeviceMap::new(SW, Conformance::Conforming);
    let mut hart = at_entry();
    if exec_rv64gc::step(&mut hart, &mut map) != StepRv64gc::Executed
        || hart.read_csr(CSR_MCAUSE) != 0
        || map.device
            != (Device {
                reads: 0,
                writes: 1,
                last_write: SENTINEL,
            })
    {
        return Err(format!("SW: the device saw {:?}", map.device));
    }
    // Every refused kind becomes the original access's access fault, with no effect.
    for case in &REFUSALS {
        let mut map = DeviceMap::new(case.word, Conformance::Conforming);
        let mut hart = (case.hart)();
        let outcome = exec_rv64gc::step(&mut hart, &mut map);
        if outcome != StepRv64gc::Executed
            || hart.read_csr(CSR_MCAUSE) != case.cause
            || hart.read_csr(CSR_MTVAL) != case.tval
            || !untouched(&mut hart, map.device)
        {
            return Err(format!(
                "{}: {outcome:?}, cause {} tval {:#x} (expected {} {:#x}), x6 {:#x}, device {:?}",
                case.what,
                hart.read_csr(CSR_MCAUSE),
                hart.read_csr(CSR_MTVAL),
                case.cause,
                case.tval,
                hart.read_x(6),
                map.device
            ));
        }
    }
    Ok(())
}

/// Run one access against a non-conforming device under the auditor.
fn audited(
    word: u32,
    conformance: Conformance,
    enabled: bool,
) -> (ArchitecturalState, Device, StepRv64gc) {
    let mut auditor = DeviceAuditor {
        map: DeviceMap::new(word, conformance),
        enabled,
    };
    let mut hart = at_entry();
    let outcome = exec_rv64gc::step(&mut hart, &mut auditor);
    (hart, auditor.map.device, outcome)
}

/// The non-conforming devices the auditor must name, each with the request it names.
const BREACHES: [(u32, Conformance, Request); 4] = [
    (
        LR_W,
        Conformance::AnswersAtomics,
        Request::AtomicLoad {
            width: AccessWidth::W,
            addr: DEVICE,
        },
    ),
    (
        AMOADD_W,
        Conformance::AnswersAtomics,
        Request::AtomicLoad {
            width: AccessWidth::W,
            addr: DEVICE,
        },
    ),
    (
        SC_W,
        Conformance::AnswersAtomics,
        Request::StorePermission {
            width: AccessWidth::W,
            addr: DEVICE,
        },
    ),
    (
        LR_W,
        Conformance::RefusesAfterReading,
        Request::AtomicLoad {
            width: AccessWidth::W,
            addr: DEVICE,
        },
    ),
];

fn device_breaches(enabled: bool) -> Result<(), String> {
    for (word, conformance, request) in BREACHES {
        let (mut hart, _, outcome) = audited(word, conformance, enabled);
        let expected = StepRv64gc::Failed(ModelError::ContractViolation(
            ContractViolation::DeviceRefusalBroken { request },
        ));
        if outcome != expected
            || hart.pc() != ENTRY
            || hart.read_x(6) != SENTINEL
            || hart.read_csr(CSR_MCAUSE) != 0
            || hart.read_csr(CSR_MEPC) != 0
            || hart.reservation().snapshot().2
        {
            return Err(format!(
                "{conformance:?} device, word {word:#010x}: expected {expected:?}, got {outcome:?}"
            ));
        }
    }
    Ok(())
}

pub(super) fn negative() -> Result<(), String> {
    // The auditor passes a conforming device's refusals and answers untouched.
    for case in &REFUSALS[..4] {
        let (hart, device, outcome) = audited(case.word, Conformance::Conforming, true);
        if outcome != StepRv64gc::Executed
            || hart.read_csr(CSR_MCAUSE) != case.cause
            || device != Device::default()
        {
            return Err(format!(
                "the auditor refused a conforming device: {}: {outcome:?}",
                case.what
            ));
        }
    }
    device_breaches(true)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn device_regions_hold_and_breaches_are_named() {
        assert_eq!(positive(), Ok(()));
        assert_eq!(negative(), Ok(()));
    }

    #[test]
    fn disabling_the_device_auditor_is_detected() {
        let error = device_breaches(false).expect_err("the fixture must discriminate");
        assert!(error.contains("got Executed"), "{error}");
    }

    #[test]
    fn a_non_conforming_device_takes_the_side_effect_the_auditor_names() {
        // Without the auditor, the LR completes and the device has been read: the very
        // side effect version 4 exists to prevent.
        let (hart, device, outcome) = audited(LR_W, Conformance::AnswersAtomics, false);
        assert_eq!(outcome, StepRv64gc::Executed);
        assert_eq!(hart.read_x(6), FIRST);
        assert_eq!(device.reads, 1);
    }
}
