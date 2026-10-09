//! STCE selects architectural STIP behavior (RVP-MACHINE 2.1.1.9/2.1.1.18).
//! Literal witnesses use the real state and CSR instructions, without an oracle.

use super::*;
use crate::env::{BoundaryError, Environment, Request, Response};
use crate::exec_rv64gc::{step, StepRv64gc};
use crate::state_rv64gc::{ArchitecturalState, CSR_MENVCFG, CSR_MIP, CSR_STIMECMP};

#[test]
fn cold_pending_uses_the_software_fallback() {
    let state = ArchitecturalState::zeroed_at(0x1000);
    assert_eq!(csr_read(&state, 0x30a), Ok(0));
    assert_eq!(csr_read(&state, 0x344), Ok(0), "cold STCE=0, raw STIP=0");
}

#[test]
fn software_stip_is_writable_in_m_and_read_only_through_delegated_sip() {
    let mut state = ArchitecturalState::zeroed_at(0x1000);
    state.write_csr(CSR_STIMECMP, u64::MAX);
    csr_write(&mut state, 0x344, 32).unwrap();
    assert_eq!(csr_read(&state, 0x344), Ok(32), "software STIP set");
    assert_eq!(csr_read(&state, 0x144), Ok(0), "undelegated view");
    csr_write(&mut state, 0x303, 32).unwrap();
    state.set_mode(PrivilegeMode::S);
    assert_eq!(csr_read(&state, 0x144), Ok(32));
    csr_write(&mut state, 0x144, 0).unwrap();
    assert_eq!(csr_read(&state, 0x144), Ok(32), "sip.STIP is read-only");
    state.set_mode(PrivilegeMode::M);
    csr_write(&mut state, 0x344, 0).unwrap();
    assert_eq!(csr_read(&state, 0x344), Ok(0), "software STIP clear");
}

#[test]
fn comparator_view_retains_software_stip_across_stce_transitions() {
    let mut state = ArchitecturalState::zeroed_at(0x1000);
    state.write_csr(CSR_MIP, 32);
    state.write_csr(CSR_STIMECMP, u64::MAX);
    csr_write(&mut state, 0x30a, 1 << 63).unwrap();
    assert_eq!(csr_read(&state, 0x344), Ok(0), "comparator above time");
    csr_write(&mut state, 0x344, 0).unwrap();
    assert_eq!(
        state.read_csr(CSR_MIP),
        32,
        "enabled writes retain raw STIP"
    );
    state.write_csr(CSR_STIMECMP, 0);
    assert_eq!(csr_read(&state, 0x344), Ok(32), "time equals compare");
    csr_write(&mut state, 0x30a, 0).unwrap();
    assert_eq!(csr_read(&state, 0x344), Ok(32), "retained software view");
    csr_write(&mut state, 0x344, 0).unwrap();
    assert_eq!(csr_read(&state, 0x344), Ok(0), "comparison is now disabled");
    csr_write(&mut state, 0x30a, 1 << 63).unwrap();
    assert_eq!(csr_read(&state, 0x344), Ok(32));
    csr_write(&mut state, 0x30a, 0).unwrap();
    assert_eq!(
        csr_read(&state, 0x344),
        Ok(0),
        "raw clear survives comparator view"
    );
}

struct Instruction {
    word: u32,
    requests: Vec<Request>,
}

impl Environment for Instruction {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        self.requests.push(request);
        match request {
            Request::FetchParcel { addr: 0x1000 } => Ok(Response::FetchParcel(self.word as u16)),
            Request::FetchParcel { addr: 0x1002 } => {
                Ok(Response::FetchParcel((self.word >> 16) as u16))
            }
            _ => panic!("unexpected CSR request: {request:?}"),
        }
    }
}

#[test]
fn all_six_csr_forms_select_stip_writability_at_execution() {
    // CSRRW/RS/RC x5,mip,x2, with x2=32; WI/RSI/RCI use zimm=2.
    // Columns: raw result at initial STIP 0/1, each with STCE 0/1.
    let forms = [
        (0x3441_12f3, [0x20, 0, 0x20, 0x20]),
        (0x3441_22f3, [0x222, 0x202, 0x222, 0x222]),
        (0x3441_32f3, [0x202, 0x202, 0x202, 0x222]),
        (0x3441_52f3, [2, 2, 2, 0x22]),
        (0x3441_62f3, [0x202, 0x202, 0x222, 0x222]),
        (0x3441_72f3, [0x200, 0x200, 0x220, 0x220]),
    ];
    // STCE, compare, raw pending, returned old value, result column.
    let cases = [
        (0, 0, 0x202, 0x202, 0),
        (0, u64::MAX, 0x202, 0x202, 0),
        (1 << 63, 0, 0x202, 0x222, 1),
        (1 << 63, u64::MAX, 0x202, 0x202, 1),
        (0, 0, 0x222, 0x222, 2),
        (0, u64::MAX, 0x222, 0x222, 2),
        (1 << 63, 0, 0x222, 0x222, 3),
        (1 << 63, u64::MAX, 0x222, 0x202, 3),
    ];
    for (stce, compare, raw, visible, column) in cases {
        for (word, results) in forms {
            let mut state = ArchitecturalState::zeroed_at(0x1000);
            state.write_csr(CSR_MENVCFG, stce);
            state.write_csr(CSR_STIMECMP, compare);
            state.write_csr(CSR_MIP, raw);
            state.write_x(2, 32);
            state.write_x(5, 0x55);
            let mut env = Instruction {
                word,
                requests: vec![],
            };
            assert_eq!(step(&mut state, &mut env), StepRv64gc::Executed);
            assert_eq!(state.pc(), 0x1004);
            assert_eq!(state.mode(), PrivilegeMode::M);
            assert_eq!(
                state.read_x(5),
                visible,
                "{stce:#x}, {compare:#x}, {raw:#x}, {word:#x}"
            );
            assert_eq!(state.read_x(2), 32);
            assert_eq!(state.read_csr(CSR_MIP), results[column]);
            assert_eq!(
                env.requests,
                [
                    Request::FetchParcel { addr: 0x1000 },
                    Request::FetchParcel { addr: 0x1002 }
                ]
            );
        }
    }
}
