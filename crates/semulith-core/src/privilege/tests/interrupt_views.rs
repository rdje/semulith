//! RVP-MACHINE §2.1.1.9: undelegated sip/sie bits are read-only zero.
//! Literal masks and instruction words exercise the real generated state, not
//! the miniature privilege fixture's selected field subset.

use super::*;
use crate::env::{BoundaryError, Environment, Request, Response};
use crate::exec_rv64gc::{step, StepRv64gc};
use crate::state_rv64gc::{
    ArchitecturalState, CSR_MENVCFG, CSR_MIDELEG, CSR_MIE, CSR_MIP, CSR_STIMECMP,
};

const MASKS: [u64; 8] = [0, 0x2, 0x20, 0x22, 0x200, 0x202, 0x220, 0x222];

fn pending_state(mode: PrivilegeMode, delegated: u64) -> ArchitecturalState {
    let mut state = ArchitecturalState::zeroed_at(0x1000);
    state.write_csr(CSR_MENVCFG, 1 << 63); // select the comparator view tested here
    state.set_mode(mode);
    state.write_csr(CSR_MIDELEG, delegated);
    state.write_csr(CSR_MIE, 0x222);
    state.write_csr(CSR_MIP, 0x202); // software/external pending; timer is computed
    state
}

#[test]
fn supervisor_interrupt_views_filter_reads_and_preserve_hidden_owner_bits() {
    for mode in [PrivilegeMode::M, PrivilegeMode::S] {
        for delegated in MASKS {
            let mut state = pending_state(mode, delegated);
            assert_eq!(csr_read(&state, 0x104), Ok(delegated));
            assert_eq!(csr_read(&state, 0x144), Ok(delegated));

            csr_write(&mut state, 0x104, 0).unwrap();
            csr_write(&mut state, 0x144, 0).unwrap();
            assert_eq!(state.read_csr(CSR_MIE), 0x222 & !delegated);
            assert_eq!(state.read_csr(CSR_MIP), 0x202 & !(delegated & 0x2));
            assert_eq!(csr_read(&state, 0x104), Ok(0));
            assert_eq!(csr_read(&state, 0x144), Ok(delegated & 0x220));

            csr_write(&mut state, 0x104, u64::MAX).unwrap();
            csr_write(&mut state, 0x144, u64::MAX).unwrap();
            assert_eq!(state.read_csr(CSR_MIE), 0x222);
            assert_eq!(state.read_csr(CSR_MIP), 0x202);
            assert_eq!(csr_read(&state, 0x104), Ok(delegated));
            assert_eq!(csr_read(&state, 0x144), Ok(delegated));
        }
    }
}

#[test]
fn delegation_changes_visibility_without_changing_pending_or_enabled_state() {
    let mut state = pending_state(PrivilegeMode::M, 0x222);
    // Use architectural delegation writes: revocation takes effect immediately.
    csr_write(&mut state, 0x303, 0).unwrap();
    assert_eq!(csr_read(&state, 0x104), Ok(0));
    assert_eq!(csr_read(&state, 0x144), Ok(0));
    csr_write(&mut state, 0x104, 0).unwrap();
    csr_write(&mut state, 0x144, 0).unwrap();
    assert_eq!(csr_read(&state, 0x304), Ok(0x222));
    assert_eq!(csr_read(&state, 0x344), Ok(0x222));

    csr_write(&mut state, 0x303, 0x222).unwrap();
    assert_eq!(csr_read(&state, 0x104), Ok(0x222));
    assert_eq!(csr_read(&state, 0x144), Ok(0x222));
    state.write_csr(CSR_STIMECMP, 1); // disarm the computed timer at time 0
    assert_eq!(csr_read(&state, 0x144), Ok(0x202));
    csr_write(&mut state, 0x144, 0).unwrap();
    assert_eq!(csr_read(&state, 0x144), Ok(0x200)); // SEIP remains read-only

    state.reset(0x1000);
    assert_eq!(csr_read(&state, 0x104), Ok(0));
    assert_eq!(csr_read(&state, 0x144), Ok(0));
    assert_eq!(csr_read(&state, 0x344), Ok(0)); // cold STCE selects zero software pending
}

struct Instruction {
    word: u32,
    seen: Vec<Request>,
}

impl Environment for Instruction {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        self.seen.push(request);
        match request {
            Request::FetchParcel { addr: 0x1000 } => Ok(Response::FetchParcel(self.word as u16)),
            Request::FetchParcel { addr: 0x1002 } => {
                Ok(Response::FetchParcel((self.word >> 16) as u16))
            }
            _ => panic!("CSR instruction made an unexpected request: {request:?}"),
        }
    }
}

#[test]
fn all_six_csr_forms_obey_delegation_through_actual_cpu_steps() {
    // CSRRW/RS/RC x5,view,x2 (x2=0), then CSRRWI/RSI/RCI x5,view,2.
    // Last columns are the owner values after a fully delegated write.
    let forms = [
        (0x1041_12f3, 0x1441_12f3, 0, 0x200),
        (0x1041_22f3, 0x1441_22f3, 0x222, 0x202),
        (0x1041_32f3, 0x1441_32f3, 0x222, 0x202),
        (0x1041_52f3, 0x1441_52f3, 0x2, 0x202),
        (0x1041_62f3, 0x1441_62f3, 0x222, 0x202),
        (0x1041_72f3, 0x1441_72f3, 0x220, 0x200),
    ];
    for mode in [PrivilegeMode::M, PrivilegeMode::S] {
        for delegated in MASKS {
            for (sie_word, sip_word, mie_after, mip_after) in forms {
                for (word, index, before, after, writable) in [
                    (sie_word, CSR_MIE, 0x222, mie_after, delegated),
                    (sip_word, CSR_MIP, 0x202, mip_after, delegated & 0x2),
                ] {
                    let mut state = pending_state(mode, delegated);
                    // A nondelegated, enabled pending source would correctly
                    // preempt S before fetch, regardless of mstatus.MIE.
                    if index == CSR_MIE {
                        state.write_csr(CSR_MIP, 0);
                        state.write_csr(CSR_STIMECMP, u64::MAX);
                    } else {
                        state.write_csr(CSR_MIE, 0);
                    }
                    state.write_x(5, 0x55);
                    let mut env = Instruction { word, seen: vec![] };
                    assert_eq!(step(&mut state, &mut env), StepRv64gc::Executed);
                    assert_eq!(state.pc(), 0x1004, "{mode:?}, {delegated:#x}, {word:#x}");
                    assert_eq!(state.mode(), mode);
                    assert_eq!(
                        state.read_x(5),
                        delegated,
                        "CSR returns the masked old value"
                    );
                    assert_eq!(
                        state.read_csr(index),
                        (before & !writable) | (after & writable)
                    );
                    assert_eq!(
                        env.seen,
                        [
                            Request::FetchParcel { addr: 0x1000 },
                            Request::FetchParcel { addr: 0x1002 }
                        ]
                    );
                }
            }
        }
    }
}
