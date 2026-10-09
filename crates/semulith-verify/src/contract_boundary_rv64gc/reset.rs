//! Independent full-cold-state witnesses, before the first CPU fetch.
//!
//! Values below come from state.sexp's reset rows and RVP-MACHINE §2.1.4,
//! not the generated constructor. This fixture auditor is not a production
//! snapshot format or a detector for arbitrary host-side reset behavior.

use semulith_core::env::ContractViolation;
use semulith_core::exec_rv64gc::{self, StepRv64gc};
use semulith_core::outcome::ModelError;
use semulith_core::privilege::{self, PrivilegedHart};
use semulith_core::reservation::Reservation;
use semulith_core::state_rv64gc::{
    ArchitecturalState, PrivilegeMode, CSR_COUNT, CSR_ELEMENTS, CSR_MCYCLE, CSR_MINSTRET, FP_COUNT,
    INTEGER_COUNT,
};
use semulith_core::translation::{Tlb, TlbEntry};
use semulith_core::wait::HartState;

use crate::fixtures::FlatMemory;

const ENTRY: u64 = 0x1000;
const SIZE: usize = 32;
// ADDI x6,x0,7; the rest of the region is zero after reconstruction.
const IMAGE: [u8; 4] = [0x13, 0x03, 0x70, 0x00];

// CSR identity is by architectural address, independent of generated storage order.
// mcause=0 is the laboratory's declared power-on cause; misa/mstatus are the
// only nonzero RAW owners. mip.STIP is computed separately below.
const RAW: [(&str, u16, u64); 26] = [
    ("mhartid", 0xf14, 0),
    ("misa", 0x301, 0x8000_0000_0014_112d),
    ("mstatus", 0x300, 0x0000_000a_0000_0000),
    ("mtvec", 0x305, 0),
    ("medeleg", 0x302, 0),
    ("mideleg", 0x303, 0),
    ("mie", 0x304, 0),
    ("mip", 0x344, 0),
    ("mscratch", 0x340, 0),
    ("mepc", 0x341, 0),
    ("mcause", 0x342, 0),
    ("mtval", 0x343, 0),
    ("menvcfg", 0x30a, 0),
    ("mcounteren", 0x306, 0),
    ("mcycle", 0xb00, 0),
    ("minstret", 0xb02, 0),
    ("stvec", 0x105, 0),
    ("sscratch", 0x140, 0),
    ("sepc", 0x141, 0),
    ("scause", 0x142, 0),
    ("stval", 0x143, 0),
    ("scounteren", 0x106, 0),
    ("satp", 0x180, 0),
    ("stimecmp", 0x14d, 0),
    ("fflags", 0x001, 0),
    ("frm", 0x002, 0),
];

fn mismatch(component: &'static str, index: Option<usize>) -> ContractViolation {
    ContractViolation::ResetStateMismatch { component, index }
}

fn require(
    matches: bool,
    component: &'static str,
    index: Option<usize>,
) -> Result<(), ContractViolation> {
    if matches {
        Ok(())
    } else {
        Err(mismatch(component, index))
    }
}

fn expected_byte(index: usize) -> u8 {
    IMAGE.get(index).copied().unwrap_or(0)
}

fn cold_state(
    state: &mut ArchitecturalState,
    memory: &FlatMemory,
) -> Result<(), ContractViolation> {
    require(
        INTEGER_COUNT == 32 && FP_COUNT == 32 && CSR_COUNT == 26 && CSR_ELEMENTS.len() == 33,
        "owner inventory",
        None,
    )?;
    require(state.pc() == ENTRY, "pc", None)?;
    require(state.mode() == PrivilegeMode::M, "mode", None)?;
    for index in 0..32 {
        require(state.read_x(index) == 0, "x", Some(usize::from(index)))?;
        require(state.read_f(index) == 0, "f", Some(usize::from(index)))?;
    }
    for (name, address, expected) in RAW {
        let index =
            ArchitecturalState::csr_index(address).ok_or(mismatch("CSR inventory", None))?;
        require(state.read_csr(index) == expected, name, None)?;
    }
    for (name, address, expected) in [
        ("sstatus", 0x100, 0x0000_0002_0000_0000),
        ("sie", 0x104, 0),
        ("sip", 0x144, 0),
        ("cycle", 0xc00, 0),
        ("time", 0xc01, 0),
        ("instret", 0xc02, 0),
    ] {
        require(
            privilege::csr_read(state, address) == Ok(expected),
            name,
            None,
        )?;
    }
    // fcsr is a composed view, but architectural access is illegal at cold FS=Off.
    require(privilege::csr_state(state, "fcsr") == 0, "fcsr", None)?;
    require(
        privilege::csr_read(state, 0x003).is_err(),
        "fcsr access",
        None,
    )?;
    require(
        privilege::csr_read(state, 0x344) == Ok(0x20),
        "computed mip",
        None,
    )?;
    // Literal core field tests independently anchor these private-owner cold
    // values; equality here includes every entry/cursor and reservation field.
    require(*state.tlb() == Tlb::default(), "TLB", None)?;
    require(
        *state.reservation() == Reservation::new(),
        "reservation",
        None,
    )?;
    require(*state.hart_state() == HartState::Active, "hart state", None)?;
    require(memory.bytes().len() == SIZE, "memory extent", None)?;
    for (index, byte) in memory.bytes().iter().enumerate() {
        require(*byte == expected_byte(index), "memory", Some(index))?;
    }
    Ok(())
}

fn cold_memory() -> FlatMemory {
    let mut memory = FlatMemory::with_fetch_align(ENTRY, SIZE, 2);
    memory.load_image(0, &IMAGE);
    memory
}

fn start(state: &mut ArchitecturalState, memory: &mut FlatMemory, audit: bool) -> StepRv64gc {
    if audit {
        if let Err(violation) = cold_state(state, memory) {
            return StepRv64gc::Failed(ModelError::ContractViolation(violation));
        }
    }
    exec_rv64gc::step(state, memory)
}

fn dirty_tlb() -> Tlb {
    let mut tlb = Tlb::default();
    for index in 0..5 {
        tlb.install(TlbEntry {
            valid: true,
            global: true,
            asid: 7,
            vpn: index,
            pa_base: ENTRY + index * 0x1000,
            r: true,
            w: true,
            x: true,
            u: true,
            a: true,
            d: true,
            level: 0,
        });
    }
    tlb
}

pub(super) fn positive() -> Result<(), String> {
    let mut state = ArchitecturalState::zeroed_at(ENTRY + 8);
    state.set_mode(PrivilegeMode::U);
    for index in 0..32 {
        state.write_x(index, u64::MAX - u64::from(index));
        state.write_f(index, u64::MAX - u64::from(index));
    }
    for index in 0..CSR_COUNT {
        state.write_csr(index, u64::MAX);
    }
    *state.tlb() = dirty_tlb();
    state.reservation().establish(ENTRY + 16, 8);
    state.hart_state().enter();
    let mut memory = FlatMemory::with_fetch_align(ENTRY, SIZE, 2);
    memory.bytes_mut().fill(0x5a);
    if cold_state(&mut state, &memory).is_ok() {
        return Err("dirty state passed the cold witness before reset".into());
    }
    state.reset(ENTRY); // the real generated reset, not a fixture copy
    memory = cold_memory(); // reconstruct every memory byte and load the selected image
    let outcome = start(&mut state, &mut memory, true);
    if outcome != StepRv64gc::Executed
        || state.pc() != ENTRY + 4
        || state.mode() != PrivilegeMode::M
        || state.read_x(6) != 7
        || state.read_csr(CSR_MCYCLE) != 1
        || state.read_csr(CSR_MINSTRET) != 1
        || memory.fetch_count() != 2
        || memory
            .bytes()
            .iter()
            .enumerate()
            .any(|(i, b)| *b != expected_byte(i))
    {
        return Err(format!(
            "full cold reset did not execute the literal ADDI: {outcome:?}"
        ));
    }
    Ok(())
}

#[derive(Clone, Copy, Debug)]
enum BadReset {
    Integer(u8),
    Float(u8),
    Csr(&'static str, u16),
    Pc,
    Mode,
    TlbContent,
    TlbCursor,
    Reservation,
    ClearedReservation,
    Waiting,
    Memory(usize),
}

fn cases() -> Vec<BadReset> {
    (1..32)
        .map(BadReset::Integer)
        .chain((0..32).map(BadReset::Float))
        .chain(
            RAW.into_iter()
                .map(|(name, address, _)| BadReset::Csr(name, address)),
        )
        .chain([
            BadReset::Pc,
            BadReset::Mode,
            BadReset::TlbContent,
            BadReset::TlbCursor,
            BadReset::Reservation,
            BadReset::ClearedReservation,
            BadReset::Waiting,
        ])
        .chain((0..SIZE).map(BadReset::Memory))
        .collect()
}

fn poison(
    case: BadReset,
    state: &mut ArchitecturalState,
    memory: &mut FlatMemory,
) -> ContractViolation {
    match case {
        BadReset::Integer(index) => {
            state.write_x(index, 1);
            mismatch("x", Some(usize::from(index)))
        }
        BadReset::Float(index) => {
            state.write_f(index, 1);
            mismatch("f", Some(usize::from(index)))
        }
        BadReset::Csr(name, address) => {
            let index =
                ArchitecturalState::csr_index(address).expect("literal CSR witness resolves");
            state.write_csr(index, state.read_csr(index) ^ 1);
            mismatch(name, None)
        }
        BadReset::Pc => {
            state.set_pc(ENTRY + 4);
            mismatch("pc", None)
        }
        BadReset::Mode => {
            state.set_mode(PrivilegeMode::U);
            mismatch("mode", None)
        }
        BadReset::TlbContent => {
            *state.tlb() = dirty_tlb();
            mismatch("TLB", None)
        }
        BadReset::TlbCursor => {
            // All entry bits remain Default, but FIFO advances to 1. Merely testing
            // occupied()==0 would miss this independently observable retained owner.
            state.tlb().install(TlbEntry::default());
            assert_eq!(state.tlb().occupied(), 0);
            mismatch("TLB", None)
        }
        BadReset::Reservation | BadReset::ClearedReservation => {
            state.reservation().establish(ENTRY + 16, 8);
            if matches!(case, BadReset::ClearedReservation) {
                state.reservation().clear();
            }
            mismatch("reservation", None)
        }
        BadReset::Waiting => {
            state.hart_state().enter();
            mismatch("hart state", None)
        }
        BadReset::Memory(index) => {
            memory.bytes_mut()[index] ^= 1;
            mismatch("memory", Some(index))
        }
    }
}

#[derive(Debug, PartialEq, Eq)]
struct Snapshot {
    x: [u64; 32],
    f: [u64; 32],
    csrs: [u64; CSR_COUNT],
    pc: u64,
    mode: PrivilegeMode,
    tlb: Tlb,
    reservation: Reservation,
    hart_state: HartState,
}

fn snapshot(state: &mut ArchitecturalState) -> Snapshot {
    Snapshot {
        x: std::array::from_fn(|i| state.read_x(i as u8)),
        f: std::array::from_fn(|i| state.read_f(i as u8)),
        csrs: std::array::from_fn(|i| state.read_csr(i)),
        pc: state.pc(),
        mode: state.mode(),
        tlb: state.tlb().clone(),
        reservation: *state.reservation(),
        hart_state: *state.hart_state(),
    }
}

fn negative_case(case: BadReset, audit: bool) -> Result<(), String> {
    let mut state = ArchitecturalState::zeroed_at(ENTRY);
    let mut memory = cold_memory();
    let violation = poison(case, &mut state, &mut memory);
    let before = snapshot(&mut state);
    let bytes = memory.bytes().to_vec();
    let outcome = start(&mut state, &mut memory, audit);
    if outcome != StepRv64gc::Failed(ModelError::ContractViolation(violation))
        || memory.fetch_count() != 0
        || snapshot(&mut state) != before
        || memory.bytes() != bytes
    {
        return Err(format!(
            "{case:?}: missing exact pre-fetch cold-state violation: {outcome:?}"
        ));
    }
    Ok(())
}

pub(super) fn negative() -> Result<(), String> {
    for case in cases() {
        negative_case(case, true)?;
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn disabling_cold_state_auditing_loses_every_bad_reset_case() {
        positive().unwrap();
        let cases = cases();
        assert_eq!(
            cases.len(),
            128,
            "every register/CSR and retained owner stays represented"
        );
        for case in cases {
            negative_case(case, true).unwrap();
            assert!(
                negative_case(case, false).is_err(),
                "{case:?}: disabled auditor retained credit"
            );
        }
    }
}
