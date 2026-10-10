//! Direct event-location and step-boundary witnesses; no external source is added.

use semulith_core::definition_rv64gc::INSNS;
use semulith_core::env::{
    check_event_delivery, AccessWidth, BoundaryError, ContractViolation, Environment,
    EventDeliveryPoint, Request, Response,
};
use semulith_core::exec_rv64gc::{self, StepRv64gc};
use semulith_core::outcome::ModelError;
use semulith_core::privilege::{PrivilegeMode, PrivilegedHart};
use semulith_core::state_rv64gc::{
    ArchitecturalState, CSR_MCAUSE, CSR_MCYCLE, CSR_MENVCFG, CSR_MEPC, CSR_MIE, CSR_MINSTRET,
    CSR_MSTATUS, CSR_MTVAL, CSR_MTVEC, CSR_SATP, CSR_STIMECMP,
};

use crate::fixtures::FlatMemory;

const ENTRY: u64 = 0x1000;
const DATA: u64 = 0x1020;
const HANDLER: u64 = 0x1100;

fn memory_with_word(word: u32) -> FlatMemory {
    let mut memory = FlatMemory::with_fetch_align(ENTRY, 64, 2);
    memory.load_image(0, &word.to_le_bytes());
    memory
}

fn timer_state(threshold: u64) -> ArchitecturalState {
    let mut hart = ArchitecturalState::zeroed_at(ENTRY);
    hart.write_csr(CSR_MENVCFG, 1 << 63); // fixture selects comparator-driven pending
    hart.write_csr(CSR_STIMECMP, threshold);
    hart.write_csr(CSR_MSTATUS, 8); // MIE
    hart.write_csr(CSR_MIE, 32); // STIE, no external source
    hart.write_csr(CSR_MTVEC, HANDLER);
    hart
}

fn delivered(hart: &ArchitecturalState, cycle: u64) -> bool {
    hart.pc() == HANDLER
        && hart.read_csr(CSR_MCAUSE) == ((1_u64 << 63) | 5)
        && hart.read_csr(CSR_MEPC) == ENTRY + 4
        && hart.read_csr(CSR_MTVAL) == 0
        && hart.read_csr(CSR_MCYCLE) == cycle
        && hart.read_csr(CSR_MINSTRET) == 1
}

pub(super) fn positive() -> Result<(), String> {
    check_event_delivery(EventDeliveryPoint::BetweenInstructions)
        .map_err(|error| format!("legal location refused: {error:?}"))?;
    // ADDI x6,x0,1; ADDI x7,x0,2. The threshold becomes pending only
    // after the first instruction completes; the second is never fetched.
    let mut memory = memory_with_word(0x0010_0313);
    memory.load_image(4, &0x0020_0393_u32.to_le_bytes());
    let mut hart = timer_state(1);
    if exec_rv64gc::step(&mut hart, &mut memory) != StepRv64gc::Executed
        || hart.pc() != ENTRY + 4
        || hart.read_x(6) != 1
        || hart.read_x(7) != 0
        || hart.read_csr(CSR_MCYCLE) != 1
        || hart.read_csr(CSR_MINSTRET) != 1
        || hart.read_csr(CSR_MCAUSE) != 0
        || memory.fetch_count() != 2
    {
        return Err("timer did not wait for the first instruction boundary".into());
    }
    if exec_rv64gc::step(&mut hart, &mut memory) != StepRv64gc::Executed
        || !delivered(&hart, 2)
        || hart.read_x(6) != 1
        || hart.read_x(7) != 0
        || memory.fetch_count() != 2
    {
        return Err("pending delivery did not precede the next parcel request".into());
    }

    // WFI retires once; two idle boundaries reach the threshold without a
    // fetch/retirement; the fourth boundary wakes and delivers before fetch.
    let mut memory = memory_with_word(0x1050_0073);
    let mut hart = timer_state(3);
    for cycle in 1..=3 {
        if exec_rv64gc::step(&mut hart, &mut memory) != StepRv64gc::Executed
            || !hart.hart_state().is_waiting()
            || hart.pc() != ENTRY + 4
            || hart.read_csr(CSR_MCYCLE) != cycle
            || hart.read_csr(CSR_MINSTRET) != 1
            || hart.read_csr(CSR_MCAUSE) != 0
            || memory.fetch_count() != 2
        {
            return Err(format!(
                "waiting boundary {cycle} changed retirement/fetch/schedule"
            ));
        }
    }
    if exec_rv64gc::step(&mut hart, &mut memory) != StepRv64gc::Executed
        || hart.hart_state().is_waiting()
        || !delivered(&hart, 4)
        || memory.fetch_count() != 2
    {
        return Err("idle timer wake did not occur between instructions".into());
    }
    Ok(())
}

struct AttemptDuringRequest {
    memory: FlatMemory,
    at: Request,
    guard: bool,
    attempted: bool,
}

impl Environment for AttemptDuringRequest {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        if request == self.at {
            self.attempted = true;
            if self.guard {
                check_event_delivery(EventDeliveryPoint::DuringRequest(request))?;
            }
        }
        self.memory.request(request)
    }
}

fn forbidden(at: Request, word: u32, guard: bool) -> Result<(), String> {
    let mut provider = AttemptDuringRequest {
        memory: memory_with_word(word),
        at,
        guard,
        attempted: false,
    };
    let mut hart = ArchitecturalState::zeroed_at(ENTRY);
    hart.write_x(5, DATA);
    hart.write_x(6, 0x44);
    if matches!(at, Request::WalkAccess { .. }) {
        hart.set_mode(PrivilegeMode::S);
        hart.write_csr(CSR_SATP, (8 << 60) | 2); // root PA 0x2000
    }
    let original_mode = hart.mode();
    let original_memory = provider.memory.bytes().to_vec();
    let outcome = if matches!(at, Request::Fetch { .. }) {
        // Public legacy table seam, still the real GC evaluator; no C rows means
        // word fetch. The generated ADDI row itself is unchanged.
        let addi = INSNS
            .iter()
            .find(|row| row.name == "addi")
            .expect("ADDI declared");
        exec_rv64gc::step_over(&mut hart, &mut provider, std::slice::from_ref(addi))
    } else {
        exec_rv64gc::step(&mut hart, &mut provider)
    };
    let expected = StepRv64gc::Failed(ModelError::ContractViolation(
        ContractViolation::EventDuringRequest { request: at },
    ));
    if !provider.attempted
        || outcome != expected
        || hart.pc() != ENTRY
        || hart.mode() != original_mode
        || hart.read_x(6) != 0x44
        || hart.read_csr(CSR_MCAUSE) != 0
        || hart.read_csr(CSR_MEPC) != 0
        || hart.read_csr(CSR_MTVAL) != 0
        || hart.read_csr(CSR_MCYCLE) != 0
        || hart.read_csr(CSR_MINSTRET) != 0
        || provider.memory.bytes() != original_memory
    {
        return Err(format!(
            "forbidden delivery at {at:?}: expected {expected:?}, got {outcome:?}"
        ));
    }
    Ok(())
}

const ATTEMPTS: [(Request, u32); 6] = [
    (Request::Fetch { addr: ENTRY }, 0x0010_0313),
    (Request::FetchParcel { addr: ENTRY }, 0x0010_0313),
    (
        Request::Load {
            width: AccessWidth::B,
            addr: DATA,
        },
        0x0002_c303,
    ),
    (
        Request::Store {
            width: AccessWidth::B,
            addr: DATA,
            data: 0x44,
        },
        0x0062_8023,
    ),
    (Request::WalkAccess { addr: 0x2000 }, 0x0010_0313),
    (
        Request::StorePermission {
            width: AccessWidth::W,
            addr: DATA,
        },
        0x1802_a32f,
    ),
];

pub(super) fn negative() -> Result<(), String> {
    for (request, word) in ATTEMPTS {
        forbidden(request, word, true)?;
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    #[test]
    fn disabling_the_location_guard_is_detected_for_every_request_kind() {
        for (request, word) in super::ATTEMPTS {
            let error = super::forbidden(request, word, false)
                .expect_err("disabled guard must lose the negative fixture");
            assert!(error.contains("Executed"), "{error}");
        }
    }
}
