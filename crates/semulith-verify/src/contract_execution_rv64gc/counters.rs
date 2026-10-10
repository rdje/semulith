//! Zicntr 6.1.1 and the Machine/Supervisor counter-enable rules.
//! Literal read values and trap transitions are derived before execution.

use semulith_core::definition_rv64gc::{InsnDef, INSNS};
use semulith_core::env::{BoundaryError, Environment, Request, Response};
use semulith_core::exec_rv64gc::{self, StepRv64gc};
use semulith_core::privilege::PrivilegedHart;
use semulith_core::reservation::Reservation;
use semulith_core::state_rv64gc::{
    ArchitecturalState, PrivilegeMode, CSR_COUNT, CSR_FFLAGS, CSR_FRM, CSR_MCAUSE, CSR_MCOUNTEREN,
    CSR_MCYCLE, CSR_MEPC, CSR_MINSTRET, CSR_MSCRATCH, CSR_MSTATUS, CSR_MTVAL, CSR_MTVEC,
    CSR_SCOUNTEREN,
};
use semulith_core::translation::{Tlb, TlbEntry};
use semulith_core::wait::HartState;

use crate::fixtures::FlatMemory;

const ENTRY: u64 = 0x1000;
const HANDLER: u64 = 0x1100;
const DATA: u64 = 0x1080;
const MODES: [PrivilegeMode; 3] = [PrivilegeMode::M, PrivilegeMode::S, PrivilegeMode::U];
// Address, enable bit, storage owner. These are the three selected Zicntr views.
const COUNTERS: [(u32, u64, usize); 3] = [
    (0xc00, 1, CSR_MCYCLE),
    (0xc01, 2, CSR_MCYCLE),
    (0xc02, 4, CSR_MINSTRET),
];
const INITIAL: [(u64, u64); 4] = [
    (0, 0),
    (41, 17),
    (u64::MAX, 0x8000_0000_1234_5678),
    (0x8000_0001_0000_0001, u64::MAX),
];

struct Observer {
    memory: FlatMemory,
    requests: Vec<Request>,
}

impl Environment for Observer {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        self.requests.push(request);
        self.memory.request(request)
    }
}

#[derive(Clone)]
struct Observation {
    x: [u64; 32],
    f: [u64; 32],
    csrs: [u64; CSR_COUNT],
    pc: u64,
    mode: PrivilegeMode,
    reservation: Reservation,
    tlb: Tlb,
    wait: HartState,
    memory: Vec<u8>,
    requests: Vec<Request>,
    parcels: u64,
    executed: bool,
}

impl Observation {
    fn capture(h: &mut ArchitecturalState, o: &Observer, executed: bool) -> Self {
        Self {
            x: std::array::from_fn(|i| h.read_x(i as u8)),
            f: std::array::from_fn(|i| h.read_f(i as u8)),
            csrs: std::array::from_fn(|i| h.read_csr(i)),
            pc: h.pc(),
            mode: h.mode(),
            reservation: *h.reservation(),
            tlb: h.tlb().clone(),
            wait: *h.hart_state(),
            memory: o.memory.bytes().to_vec(),
            requests: o.requests.clone(),
            parcels: o.memory.fetch_count(),
            executed,
        }
    }
}

fn judge(actual: &Observation, expected: &Observation) -> Result<(), String> {
    if actual.requests != expected.requests {
        return Err("requests differ".into());
    }
    if actual.memory != expected.memory {
        return Err("memory differs".into());
    }
    if actual.x != expected.x {
        return Err("integer registers differ".into());
    }
    if actual.f != expected.f {
        return Err("floating registers differ".into());
    }
    if actual.csrs != expected.csrs {
        return Err("CSR owners differ".into());
    }
    if actual.pc != expected.pc || actual.mode != expected.mode {
        return Err("PC/mode differs".into());
    }
    if actual.reservation != expected.reservation {
        return Err("reservation differs".into());
    }
    if actual.tlb != expected.tlb {
        return Err("TLB/cursor differs".into());
    }
    if actual.wait != expected.wait {
        return Err("wait state differs".into());
    }
    if actual.parcels != expected.parcels || actual.executed != expected.executed {
        return Err("extent/outcome differs".into());
    }
    Ok(())
}

#[derive(Clone, Copy, Debug)]
struct Cell {
    address: u32,
    bit: u64,
    owner: usize,
    mode: PrivilegeMode,
    m_enable: u64,
    s_enable: u64,
    rd: u32,
    cycle: u64,
    retired: u64,
}

impl Cell {
    fn legal(self) -> bool {
        match self.mode {
            PrivilegeMode::M => true,
            PrivilegeMode::S => self.m_enable & self.bit != 0,
            PrivilegeMode::U => self.m_enable & self.bit != 0 && self.s_enable & self.bit != 0,
        }
    }

    fn word(self) -> u32 {
        // CSRRS rd,counter,x0: source field zero, so there is never a CSR write.
        (self.address << 20) | (self.rd << 7) | 0x2073
    }

    fn fixture(self) -> (ArchitecturalState, Observer, Observation) {
        let mut h = ArchitecturalState::zeroed_at(ENTRY);
        h.set_mode(self.mode);
        h.write_csr(CSR_MSTATUS, 0xa_0000_6000); // Dirty FP context; no interrupt enables.
        h.write_csr(CSR_MCOUNTEREN, self.m_enable);
        h.write_csr(CSR_SCOUNTEREN, self.s_enable);
        h.write_csr(CSR_MCYCLE, self.cycle);
        h.write_csr(CSR_MINSTRET, self.retired);
        h.write_csr(CSR_MTVEC, HANDLER);
        h.write_csr(CSR_MCAUSE, 0x55);
        h.write_csr(CSR_MEPC, 0x1200);
        h.write_csr(CSR_MTVAL, 0x7788);
        h.write_csr(CSR_MSCRATCH, 0x1122_3344_5566_7788);
        h.write_csr(CSR_FFLAGS, 0x15);
        h.write_csr(CSR_FRM, 3);
        for r in 1..32 {
            h.write_x(r, 0x1111_2222_3333_0000 + u64::from(r));
        }
        for r in 0..32 {
            h.write_f(r, 0x7ff8_0000_0000_1000 + u64::from(r));
        }
        h.reservation().establish(DATA, 8);
        // Bare fetches do not consult these entries; preserve both entries and cursor.
        for i in 0_u64..5 {
            h.tlb().install(TlbEntry {
                valid: true,
                global: i.is_multiple_of(2),
                asid: 0x12,
                vpn: 0x40 + i,
                pa_base: 0x9000 + i * 0x1000,
                r: true,
                w: true,
                x: true,
                u: false,
                a: true,
                d: true,
                level: 0,
            });
        }
        let mut memory = FlatMemory::with_fetch_align(ENTRY, 0x200, 2);
        memory.load_image(0, &self.word().to_le_bytes());
        memory.load_image(0x80, &0x8877_6655_4433_2211_u64.to_le_bytes());
        let observer = Observer {
            memory,
            requests: Vec::new(),
        };
        let mut expected = Observation::capture(&mut h, &observer, true);
        expected.requests = vec![
            Request::FetchParcel { addr: ENTRY },
            Request::FetchParcel { addr: ENTRY + 2 },
        ];
        expected.parcels = 2;
        expected.csrs[CSR_MCYCLE] = self.cycle.wrapping_add(1);
        if self.legal() {
            if self.rd != 0 {
                expected.x[self.rd as usize] = if self.owner == CSR_MCYCLE {
                    self.cycle
                } else {
                    self.retired
                };
            }
            expected.csrs[CSR_MINSTRET] = self.retired.wrapping_add(1);
            expected.pc = ENTRY + 4;
        } else {
            expected.csrs[CSR_MCAUSE] = 2;
            expected.csrs[CSR_MEPC] = ENTRY;
            expected.csrs[CSR_MTVAL] = u64::from(self.word());
            // M delivery: MPIE <- MIE(0), MIE <- 0, MPP <- origin mode.
            expected.csrs[CSR_MSTATUS] = (expected.csrs[CSR_MSTATUS]
                & !((3 << 11) | (1 << 7) | (1 << 3)))
                | ((self.mode as u64) << 11);
            expected.pc = HANDLER;
            expected.mode = PrivilegeMode::M;
        }
        (h, observer, expected)
    }

    fn observe(self, table: &[InsnDef]) -> (Observation, Observation) {
        let (mut h, mut o, expected) = self.fixture();
        let outcome = exec_rv64gc::step_over(&mut h, &mut o, table);
        (
            Observation::capture(&mut h, &o, outcome == StepRv64gc::Executed),
            expected,
        )
    }

    fn check(self, table: &[InsnDef]) -> Result<(), String> {
        let (actual, expected) = self.observe(table);
        judge(&actual, &expected).map_err(|e| format!("{self:?}: {e}"))
    }
}

fn matrix(legal: bool) -> Result<usize, String> {
    let mut count = 0;
    for mode in MODES {
        for m_enable in 0..8 {
            for s_enable in 0..8 {
                for (address, bit, owner) in COUNTERS {
                    for rd in [0, 5, 31] {
                        for (cycle, retired) in INITIAL {
                            let cell = Cell {
                                address,
                                bit,
                                owner,
                                mode,
                                m_enable,
                                s_enable,
                                rd,
                                cycle,
                                retired,
                            };
                            if cell.legal() == legal {
                                cell.check(INSNS)?;
                                count += 1;
                            }
                        }
                    }
                }
            }
        }
    }
    Ok(count)
}

pub(super) fn positive() -> Result<(), String> {
    let count = matrix(true)?;
    if count != 4032 {
        return Err(format!("positive matrix extent {count}, expected 4032"));
    }
    Ok(())
}

pub(super) fn negative() -> Result<(), String> {
    let count = matrix(false)?;
    if count != 2880 {
        return Err(format!("negative matrix extent {count}, expected 2880"));
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use semulith_core::definition_rv64gc::Sem;
    use semulith_core::env::AccessWidth;

    fn cell(mode: PrivilegeMode) -> Cell {
        Cell {
            address: 0xc00,
            bit: 1,
            owner: CSR_MCYCLE,
            mode,
            m_enable: 0,
            s_enable: 0,
            rd: 5,
            cycle: 0x8000_0001_2345_6789,
            retired: 17,
        }
    }

    fn wrong_table(effect: &'static Sem) -> Vec<InsnDef> {
        INSNS
            .iter()
            .map(|row| InsnDef {
                from: row.from,
                name: row.name,
                mask: row.mask,
                value: row.value,
                operands: row.operands,
                source: row.source,
                effect: if row.name == "csrrs" {
                    effect
                } else {
                    row.effect
                },
                length: row.length,
                expansion: row.expansion,
            })
            .collect()
    }

    #[test]
    fn counter_reads_and_gated_traps_match_all_literal_cells() {
        assert_eq!(positive(), Ok(()));
        assert_eq!(negative(), Ok(()));
    }

    #[test]
    fn wrong_counter_effects_fail_named_observations() {
        let cases: [(PrivilegeMode, u32, &Sem, &str); 11] = [
            (PrivilegeMode::M, 5, &Sem::Nop, "integer registers differ"),
            (
                PrivilegeMode::M,
                5,
                &Sem::Set(&Sem::Reg("rd"), &Sem::CsrRead(&Sem::Lit(0xc02))),
                "integer registers differ",
            ),
            (
                PrivilegeMode::M,
                5,
                &Sem::Set(
                    &Sem::Reg("rd"),
                    &Sem::Trunc(32, &Sem::CsrRead(&Sem::Field("csr"))),
                ),
                "integer registers differ",
            ),
            (
                PrivilegeMode::S,
                5,
                &Sem::Set(&Sem::Reg("rd"), &Sem::CsrState(&Sem::Field("csr"))),
                "integer registers differ",
            ),
            (
                PrivilegeMode::M,
                0,
                &Sem::TrapDeliver(&Sem::Lit(2), &Sem::Inst),
                "CSR owners differ",
            ),
            (
                PrivilegeMode::M,
                0,
                &Sem::CsrWrite(&Sem::Lit(0xb00), &Sem::Lit(0)),
                "CSR owners differ",
            ),
            (
                PrivilegeMode::M,
                0,
                &Sem::Set(&Sem::FReg("rd"), &Sem::Lit(0)),
                "floating registers differ",
            ),
            (
                PrivilegeMode::M,
                5,
                &Sem::Load(&Sem::Lit(64), &Sem::Lit(0), &Sem::Lit(DATA)),
                "requests differ",
            ),
            (
                PrivilegeMode::M,
                0,
                &Sem::SetPc(&Sem::Add(&Sem::Pc, &Sem::Lit(8))),
                "PC/mode differs",
            ),
            (
                PrivilegeMode::M,
                0,
                &Sem::StoreConditional(&Sem::Lit(64), &Sem::Lit(DATA + 8), &Sem::Lit(0)),
                "reservation differs",
            ),
            (
                PrivilegeMode::M,
                0,
                &Sem::TlbInvalidate(&Sem::Lit(0), &Sem::Lit(0), &Sem::Lit(1), &Sem::Lit(1)),
                "TLB/cursor differs",
            ),
        ];
        for (mode, rd, effect, reason) in cases {
            let table = wrong_table(effect);
            let error = Cell { rd, ..cell(mode) }.check(&table).expect_err(reason);
            assert!(error.contains(reason), "{reason}: {error}");
        }
    }

    #[test]
    fn corrupted_counter_captures_fail_every_auditor_component() {
        let (actual, expected) = cell(PrivilegeMode::M).observe(INSNS);
        assert_eq!(judge(&actual, &expected), Ok(()));
        let check =
            |bad: Observation, reason| assert_eq!(judge(&bad, &expected).unwrap_err(), reason);
        for request in [
            Request::Load {
                width: AccessWidth::D,
                addr: DATA,
            },
            Request::Store {
                width: AccessWidth::D,
                addr: DATA,
                data: 0,
            },
            Request::WalkAccess { addr: DATA },
        ] {
            let mut bad = actual.clone();
            bad.requests.push(request);
            check(bad, "requests differ");
        }
        let mut bad = actual.clone();
        bad.memory[0x80] ^= 1;
        check(bad, "memory differs");
        let mut bad = actual.clone();
        bad.x[0] = 1;
        check(bad, "integer registers differ");
        let mut bad = actual.clone();
        bad.x[5] ^= 1;
        check(bad, "integer registers differ");
        let mut bad = actual.clone();
        bad.f[31] ^= 1;
        check(bad, "floating registers differ");
        let mut bad = actual.clone();
        bad.csrs[CSR_MCYCLE] ^= 1;
        check(bad, "CSR owners differ");
        let mut bad = actual.clone();
        bad.csrs[CSR_MCOUNTEREN] ^= 1;
        check(bad, "CSR owners differ");
        let mut bad = actual.clone();
        bad.pc += 4;
        check(bad, "PC/mode differs");
        let mut bad = actual.clone();
        bad.mode = PrivilegeMode::S;
        check(bad, "PC/mode differs");
        let mut bad = actual.clone();
        bad.reservation.clear();
        check(bad, "reservation differs");
        let mut bad = actual.clone();
        bad.tlb = Tlb::new();
        check(bad, "TLB/cursor differs");
        let mut bad = actual.clone();
        bad.wait.enter();
        check(bad, "wait state differs");
        let mut bad = actual.clone();
        bad.parcels += 1;
        check(bad, "extent/outcome differs");
        let mut bad = actual.clone();
        bad.executed = false;
        check(bad, "extent/outcome differs");
    }
}
