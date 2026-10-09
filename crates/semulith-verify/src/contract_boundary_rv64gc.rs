//! Direct, typed evidence for the GC laboratory's environment assumptions.
//!
//! These fixtures use hand-selected boundary values and the real interpreter.
//! Violating providers must reach the contract-error channel without delivering
//! an architectural exception. The registry names each positive/negative check.

use semulith_core::env::{
    AccessWidth, BoundaryError, ContractViolation, Environment, Failure, Request, Response,
};
use semulith_core::exec_rv64gc::{self, StepRv64gc};
use semulith_core::outcome::ModelError;
use semulith_core::state_rv64gc::{
    ArchitecturalState, PrivilegeMode, CSR_MCAUSE, CSR_MEPC, CSR_MTVAL, CSR_SATP,
};

use crate::fixtures::{FlatMemory, ScriptedEnv};

/// A named direct boundary check, rather than an unrelated passing guest.
#[derive(Clone, Copy, Debug)]
pub enum BoundaryCheck {
    /// Physical byte-address requests and their exact supplied values.
    AddressUnitsPositive,
    /// Wrong units, narrowed addresses and untranslated addresses are violations.
    AddressUnitsNegative,
}

impl BoundaryCheck {
    /// Run the exact fixture bound by the contract registry.
    pub fn run(self) -> Result<(), String> {
        match self {
            Self::AddressUnitsPositive => address_units_positive(),
            Self::AddressUnitsNegative => address_units_negative(),
        }
    }
}

// VA and PA differ, and every physical address has nonzero bits above bit 31.
// VA 0x0040_0000 has VPN[2:0] = [0, 2, 0]; the L1 PTE is at L1 + 16.
const VA: u64 = 0x0040_0000;
const ROOT: u64 = 0x1_0000_1000;
const L1: u64 = 0x1_0000_2000;
const L0: u64 = 0x1_0000_3000;
const PA: u64 = 0x1_0000_4000;

#[derive(Clone, Copy)]
enum Mapping {
    Exact,
    DataWordIndex,
    WalkTruncated32,
    FetchVirtual,
}

/// A provider adapter whose deliberate address distortion is checked by its
/// independent, exact request script. This is a verification fixture only.
struct AddressProvider {
    inner: ScriptedEnv,
    mapping: Mapping,
}

impl Environment for AddressProvider {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        let arrived = match (self.mapping, request) {
            (Mapping::DataWordIndex, Request::Load { width, addr }) => Request::Load {
                width,
                addr: addr / 4,
            },
            (Mapping::WalkTruncated32, Request::WalkAccess { addr }) => Request::WalkAccess {
                addr: u64::from(addr as u32),
            },
            (Mapping::FetchVirtual, Request::FetchParcel { addr }) => Request::FetchParcel {
                addr: VA + (addr - PA),
            },
            _ => request,
        };
        self.inner.request(arrived)
    }
}

fn scripted_step(
    mapping: Mapping,
    access_failure: bool,
) -> (ArchitecturalState, StepRv64gc, usize) {
    let mut state = ArchitecturalState::zeroed_at(VA);
    state.set_mode(PrivilegeMode::S);
    state.write_csr(CSR_SATP, (8 << 60) | (ROOT >> 12));
    state.write_x(5, VA + 11);
    // LB x6, 0(x5) = 0x00028303. Svade leaf: V/R/W/X/A/D set, U/G clear.
    let mut script = vec![
        (
            Request::WalkAccess { addr: ROOT },
            Ok(Response::WalkAccess(((L1 >> 12) << 10) | 1)),
        ),
        (
            Request::WalkAccess { addr: L1 + 16 },
            Ok(Response::WalkAccess(((L0 >> 12) << 10) | 1)),
        ),
        (
            Request::WalkAccess { addr: L0 },
            Ok(Response::WalkAccess(((PA >> 12) << 10) | 0xcf)),
        ),
        (
            Request::FetchParcel { addr: PA },
            Ok(Response::FetchParcel(0x8303)),
        ),
        (
            Request::FetchParcel { addr: PA + 2 },
            Ok(Response::FetchParcel(0x0002)),
        ),
        (
            Request::Load {
                width: AccessWidth::B,
                addr: PA + 11,
            },
            Ok(Response::Load(0xee)),
        ),
    ];
    if access_failure {
        script[0].1 = Err(Failure::AccessFault);
    }
    let mut provider = AddressProvider {
        inner: ScriptedEnv::new(script),
        mapping,
    };
    let outcome = exec_rv64gc::step(&mut state, &mut provider);
    (state, outcome, provider.inner.remaining())
}

fn address_units_positive() -> Result<(), String> {
    let mut memory = FlatMemory::with_fetch_align(PA, 16, 2);
    memory.load_image(
        0,
        &[
            0x03, 0x83, 0x02, 0x00, 0xaa, 0xbb, 0xcc, 0xdd, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66,
            0x77, 0x88,
        ],
    );
    for (request, expected) in [
        (
            Request::FetchParcel { addr: PA + 2 },
            Response::FetchParcel(0x0002),
        ),
        (
            Request::Load {
                width: AccessWidth::B,
                addr: PA + 5,
            },
            Response::Load(0xbb),
        ),
        (
            Request::Load {
                width: AccessWidth::H,
                addr: PA + 6,
            },
            Response::Load(0xddcc),
        ),
        (
            Request::Load {
                width: AccessWidth::D,
                addr: PA + 8,
            },
            Response::Load(0x8877_6655_4433_2211),
        ),
        (
            Request::WalkAccess { addr: PA + 8 },
            Response::WalkAccess(0x8877_6655_4433_2211),
        ),
        (
            Request::Store {
                width: AccessWidth::B,
                addr: PA + 5,
                data: 0x1234,
            },
            Response::StoreDone,
        ),
    ] {
        let actual = memory.request(request);
        if actual != Ok(expected) {
            return Err(format!(
                "byte address {request:?}: expected {expected:?}, got {actual:?}"
            ));
        }
    }
    if memory.bytes()[4..7] != [0xaa, 0x34, 0xcc] {
        return Err("byte store changed the wrong offset or neighboring bytes".into());
    }
    let (state, outcome, remaining) = scripted_step(Mapping::Exact, false);
    if outcome != StepRv64gc::Executed
        || remaining != 0
        || state.pc() != VA + 4
        || state.read_x(6) != 0xffff_ffff_ffff_ffee
    {
        return Err(format!(
            "physical Sv39 LB: {outcome:?}, remaining={remaining}, pc={:#x}, x6={:#x}",
            state.pc(),
            state.read_x(6)
        ));
    }
    Ok(())
}

fn address_units_negative() -> Result<(), String> {
    for (mapping, scripted, arrived) in [
        (
            Mapping::DataWordIndex,
            Request::Load {
                width: AccessWidth::B,
                addr: PA + 11,
            },
            Request::Load {
                width: AccessWidth::B,
                addr: (PA + 11) / 4,
            },
        ),
        (
            Mapping::WalkTruncated32,
            Request::WalkAccess { addr: ROOT },
            Request::WalkAccess { addr: 0x1000 },
        ),
        (
            Mapping::FetchVirtual,
            Request::FetchParcel { addr: PA },
            Request::FetchParcel { addr: VA },
        ),
    ] {
        let (state, outcome, _) = scripted_step(mapping, false);
        let expected = StepRv64gc::Failed(ModelError::ContractViolation(
            ContractViolation::ResponseMismatch { scripted, arrived },
        ));
        if outcome != expected
            || state.pc() != VA
            || state.mode() != PrivilegeMode::S
            || state.read_x(6) != 0
            || state.read_csr(CSR_MCAUSE) != 0
            || state.read_csr(CSR_MEPC) != 0
            || state.read_csr(CSR_MTVAL) != 0
        {
            return Err(format!(
                "address violation: expected {expected:?} without trap/effect, got {outcome:?}"
            ));
        }
    }
    // A legitimate physical access failure still delivers a target exception.
    let (state, outcome, _) = scripted_step(Mapping::Exact, true);
    if outcome != StepRv64gc::Executed
        || state.mode() != PrivilegeMode::M
        || state.read_csr(CSR_MCAUSE) != 1
        || state.read_csr(CSR_MEPC) != VA
        || state.read_csr(CSR_MTVAL) != VA
        || state.read_x(6) != 0
    {
        return Err(format!(
            "legitimate walk access failure lost its target exception: {outcome:?}"
        ));
    }
    Ok(())
}
