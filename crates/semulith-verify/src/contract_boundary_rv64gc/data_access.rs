//! Hand-selected memory witnesses for OB-GC-ENV-DATA-ACCESS.

use semulith_core::env::{
    request_checked, AccessWidth, BoundaryError, ContractViolation, Environment, Request, Response,
};
use semulith_core::exec_rv64gc::{self, StepRv64gc};
use semulith_core::outcome::ModelError;
use semulith_core::state_rv64gc::{ArchitecturalState, CSR_MCAUSE, CSR_MEPC, CSR_MTVAL};

use crate::fixtures::FlatMemory;

const ENTRY: u64 = 0x1000;
const DATA: u64 = ENTRY + 32;
const BYTES: [u8; 8] = [0x88, 0x77, 0x66, 0x55, 0x44, 0x33, 0x22, 0x11];

// Independent literal encodings: LBU/LHU/LWU/LD x6,0(x5), SB/SH/SW/SD x6,0(x5).
// Values and byte counts are literals, not derived from the boundary's width helpers.
const CASES: [(AccessWidth, usize, u64, u32, u32); 4] = [
    (AccessWidth::B, 1, 0x88, 0x0002_c303, 0x0062_8023),
    (AccessWidth::H, 2, 0x7788, 0x0002_d303, 0x0062_9023),
    (AccessWidth::W, 4, 0x5566_7788, 0x0002_e303, 0x0062_a023),
    (
        AccessWidth::D,
        8,
        0x1122_3344_5566_7788,
        0x0002_b303,
        0x0062_b023,
    ),
];

fn memory(word: u32, size: usize) -> FlatMemory {
    let mut memory = FlatMemory::with_fetch_align(ENTRY, size, 2);
    memory.load_image(0, &word.to_le_bytes());
    memory
}

fn state() -> ArchitecturalState {
    let mut state = ArchitecturalState::zeroed_at(ENTRY);
    state.write_x(5, DATA);
    state
}

pub(super) fn positive() -> Result<(), String> {
    for (width, bytes, raw, load, store) in CASES {
        let mut memory = memory(load, 48);
        memory.load_image(32, &BYTES);
        let before = memory.bytes().to_vec();
        for _ in 0..2 {
            if request_checked(&mut memory, Request::Load { width, addr: DATA })
                != Ok(Response::Load(raw))
            {
                return Err(format!(
                    "{width:?}: raw value differs from the byte witness"
                ));
            }
        }
        // Main memory is also executable; instruction and data reads share bytes.
        if request_checked(&mut memory, Request::FetchParcel { addr: DATA })
            != Ok(Response::FetchParcel(0x7788))
            || memory.bytes() != before
        {
            return Err(format!(
                "{width:?}: reads changed memory or executable attributes"
            ));
        }
        let mut hart = state();
        if exec_rv64gc::step(&mut hart, &mut memory) != StepRv64gc::Executed
            || hart.read_x(6) != raw
            || hart.pc() != ENTRY + 4
            || hart.read_csr(CSR_MCAUSE) != 0
        {
            return Err(format!(
                "{width:?}: hand-encoded load did not consume the exact value"
            ));
        }

        memory.load_image(0, &store.to_le_bytes());
        let store_before = memory.bytes().to_vec();
        let mut expected = store_before.clone();
        // A narrow store writes only its low bytes, in ascending-address byte order.
        let stored = [0x10, 0x32, 0x54, 0x76, 0x98, 0xba, 0xdc, 0xfe];
        expected[32..32 + bytes].copy_from_slice(&stored[..bytes]);
        // Check the provider with high input bits, independently of the CPU's
        // operand narrowing before it issues an SB/SH/SW request.
        if request_checked(
            &mut memory,
            Request::Store {
                width,
                addr: DATA,
                data: 0xfedc_ba98_7654_3210,
            },
        ) != Ok(Response::StoreDone)
            || memory.bytes() != expected
        {
            return Err(format!(
                "{width:?}: direct store did not keep only the low bytes"
            ));
        }
        memory.bytes_mut().copy_from_slice(&store_before);
        let mut hart = state();
        hart.write_x(6, 0xfedc_ba98_7654_3210);
        if exec_rv64gc::step(&mut hart, &mut memory) != StepRv64gc::Executed
            || hart.pc() != ENTRY + 4
            || memory.bytes() != expected
        {
            return Err(format!(
                "{width:?}: store width, byte order or neighboring bytes differ"
            ));
        }

        // Last requested byte lies outside the declared region. All widths fail,
        // including B at the first byte beyond it; wider accesses straddle its end.
        for (word, cause) in [(load, 5), (store, 7)] {
            let mut memory = memory_for_fault(word, bytes);
            let before = memory.bytes().to_vec();
            let mut hart = state();
            hart.write_x(6, 0xfedc_ba98_7654_3210);
            if exec_rv64gc::step(&mut hart, &mut memory) != StepRv64gc::Executed
                || hart.read_csr(CSR_MCAUSE) != cause
                || hart.read_csr(CSR_MEPC) != ENTRY
                || hart.read_csr(CSR_MTVAL) != DATA
                || hart.read_x(6) != 0xfedc_ba98_7654_3210
                || memory.bytes() != before
            {
                return Err(format!(
                    "{width:?}: region failure has a partial effect or wrong trap"
                ));
            }
        }
    }
    let (hart, outcome) = audited_step(Response::Load(0x1122_3344_5566_7788), true);
    if outcome != StepRv64gc::Executed || hart.read_x(6) != 0x1122_3344_5566_7788 {
        return Err(format!(
            "content auditor rejected its valid byte witness: {outcome:?}"
        ));
    }
    Ok(())
}

fn memory_for_fault(word: u32, bytes: usize) -> FlatMemory {
    memory(word, 32 + bytes - 1)
}

/// Override only data success answers; fetches still use the real memory provider.
struct AnswerProvider {
    memory: FlatMemory,
    answer: Response,
}

impl Environment for AnswerProvider {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        match request {
            Request::Load { .. } | Request::Store { .. } => Ok(self.answer),
            _ => self.memory.request(request),
        }
    }
}

fn require_violation(
    word: u32,
    answer: Response,
    violation: ContractViolation,
) -> Result<(), String> {
    let mut provider = AnswerProvider {
        memory: memory(word, 48),
        answer,
    };
    let mut hart = state();
    hart.write_x(6, 0x1234);
    let outcome = exec_rv64gc::step(&mut hart, &mut provider);
    if outcome != StepRv64gc::Failed(ModelError::ContractViolation(violation))
        || hart.pc() != ENTRY
        || hart.read_x(6) != 0x1234
        || hart.read_csr(CSR_MCAUSE) != 0
        || hart.read_csr(CSR_MEPC) != 0
        || hart.read_csr(CSR_MTVAL) != 0
    {
        return Err(format!(
            "data answer {answer:?}: expected {violation:?}, got {outcome:?}"
        ));
    }
    Ok(())
}

pub(super) fn negative() -> Result<(), String> {
    for (width, _, _, load, store) in CASES {
        let request = Request::Load { width, addr: DATA };
        require_violation(
            load,
            Response::StoreDone,
            ContractViolation::WrongResponseKind {
                request,
                response: Response::StoreDone,
            },
        )?;
        require_violation(
            store,
            Response::Load(0),
            ContractViolation::WrongResponseKind {
                request: Request::Store {
                    width,
                    addr: DATA,
                    data: match width {
                        AccessWidth::B => 0x34,
                        AccessWidth::H | AccessWidth::W | AccessWidth::D => 0x1234,
                    },
                },
                response: Response::Load(0),
            },
        )?;
    }
    for (width, value, word) in [
        (AccessWidth::B, 0x100, 0x0002_c303),
        (AccessWidth::H, 0x1_0000, 0x0002_d303),
        (AccessWidth::W, 0x1_0000_0000, 0x0002_e303),
    ] {
        require_violation(
            word,
            Response::Load(value),
            ContractViolation::LoadValueOutOfWidth { width, value },
        )?;
    }
    endian_violation(true)
}

/// The independent witness is needed for valid-width but incorrect content.
/// This fixture-only auditor deliberately has no role in ordinary CPU execution.
struct ValueAuditor {
    provider: AnswerProvider,
    enabled: bool,
}

impl Environment for ValueAuditor {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        let arrived = request_checked(&mut self.provider, request)?;
        if self.enabled
            && request
                == (Request::Load {
                    width: AccessWidth::D,
                    addr: DATA,
                })
        {
            let expected = Response::Load(0x1122_3344_5566_7788);
            return super::response_matches(request, expected, arrived);
        }
        Ok(arrived)
    }
}

fn audited_step(answer: Response, enabled: bool) -> (ArchitecturalState, StepRv64gc) {
    let mut provider = ValueAuditor {
        provider: AnswerProvider {
            memory: memory(0x0002_b303, 48),
            answer,
        },
        enabled,
    };
    provider.provider.memory.load_image(32, &BYTES);
    let mut hart = state();
    let outcome = exec_rv64gc::step(&mut hart, &mut provider);
    (hart, outcome)
}

fn endian_violation(enabled: bool) -> Result<(), String> {
    let (hart, outcome) = audited_step(Response::Load(0x8877_6655_4433_2211), enabled);
    let violation = ContractViolation::ResponseValueMismatch {
        request: Request::Load {
            width: AccessWidth::D,
            addr: DATA,
        },
        expected: Response::Load(0x1122_3344_5566_7788),
        arrived: Response::Load(0x8877_6655_4433_2211),
    };
    if outcome != StepRv64gc::Failed(ModelError::ContractViolation(violation))
        || hart.pc() != ENTRY
        || hart.read_x(6) != 0
        || hart.read_csr(CSR_MCAUSE) != 0
    {
        return Err(format!(
            "reversed bytes escaped the content auditor: {outcome:?}"
        ));
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    #[test]
    fn disabling_the_content_auditor_is_detected() {
        assert_eq!(super::endian_violation(true), Ok(()));
        let error = super::endian_violation(false).expect_err("the fixture must discriminate");
        assert!(error.contains("Executed"), "{error}");
    }
}
