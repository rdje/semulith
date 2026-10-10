//! FENCE.I's coherent-memory choice and forward-compatible ignored fields.
//!
//! RVI-ZIFENCEI 4.1 supplies the instruction contract. Immediate visibility
//! without a fence is the stronger, explicitly selected laboratory provider.

use semulith_core::definition_rv64gc::{InsnDef, INSNS};
use semulith_core::env::{AccessWidth, BoundaryError, Environment, Request, Response};
use semulith_core::exec_rv64gc::{self, StepRv64gc};
use semulith_core::privilege::PrivilegedHart;
use semulith_core::reservation::Reservation;
use semulith_core::state_rv64gc::{
    ArchitecturalState, PrivilegeMode, CSR_COUNT, CSR_FFLAGS, CSR_FRM, CSR_MCAUSE, CSR_MCYCLE,
    CSR_MEPC, CSR_MINSTRET, CSR_MSCRATCH, CSR_MSTATUS, CSR_MTVAL, CSR_MTVEC, CSR_SSCRATCH,
};
use semulith_core::translation::{Tlb, TlbEntry};
use semulith_core::wait::HartState;

use crate::fixtures::FlatMemory;

const ENTRY: u64 = 0x1000;
const DATA: u64 = 0x1080;
const FENCE_I: u32 = 0x0000_100f;
const NONZERO: u32 = 0xffff_9f8f;
const NOP: u32 = 0x0000_0013;
const MODES: [PrivilegeMode; 3] = [PrivilegeMode::M, PrivilegeMode::S, PrivilegeMode::U];
const REGISTERS: [(u32, u32); 5] = [(0, 0), (0, 31), (31, 0), (31, 31), (7, 13)];

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
    reservation: Reservation,
    tlb: Tlb,
    wait: HartState,
    pc: u64,
    mode: PrivilegeMode,
    memory: Vec<u8>,
    requests: Vec<Request>,
    parcels: u64,
    executed: bool,
}

impl Observation {
    fn capture(hart: &mut ArchitecturalState, observer: &Observer, executed: bool) -> Self {
        Self {
            x: std::array::from_fn(|r| hart.read_x(r as u8)),
            f: std::array::from_fn(|r| hart.read_f(r as u8)),
            csrs: std::array::from_fn(|i| hart.read_csr(i)),
            reservation: *hart.reservation(),
            tlb: hart.tlb().clone(),
            wait: *hart.hart_state(),
            pc: hart.pc(),
            mode: hart.mode(),
            memory: observer.memory.bytes().to_vec(),
            requests: observer.requests.clone(),
            parcels: observer.memory.fetch_count(),
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
    if actual.reservation != expected.reservation {
        return Err("reservation differs".into());
    }
    if actual.tlb != expected.tlb {
        return Err("TLB/cursor differs".into());
    }
    if actual.wait != expected.wait {
        return Err("wait state differs".into());
    }
    if actual.pc != expected.pc || actual.mode != expected.mode {
        return Err("PC/mode differs".into());
    }
    if actual.parcels != expected.parcels || actual.executed != expected.executed {
        return Err("boundary outcome/parcels differ".into());
    }
    Ok(())
}

struct Fixture {
    hart: ArchitecturalState,
    observer: Observer,
    expected: Observation,
}

impl Fixture {
    fn new(image: &[u8], mode: PrivilegeMode, entry: u64, target: u64, patch: u64) -> Self {
        let mut memory = FlatMemory::with_fetch_align(ENTRY, 0x200, 2);
        memory.load_image((entry - ENTRY) as usize, image);
        memory.load_image(0x80, &0x1122_3344_5566_7788_u64.to_le_bytes());
        let mut hart = ArchitecturalState::zeroed_at(entry);
        hart.set_mode(mode);
        hart.write_csr(CSR_MSTATUS, 0xa_0000_6000); // FS Dirty, no enabled interrupts.
        hart.write_csr(CSR_MTVEC, 0x1100);
        hart.write_csr(CSR_MSCRATCH, 0x1234_5678_9abc_def0);
        hart.write_csr(CSR_SSCRATCH, 0xfedc_ba98_7654_3210);
        hart.write_csr(CSR_MCAUSE, 0x55);
        hart.write_csr(CSR_MEPC, 0x1200);
        hart.write_csr(CSR_MTVAL, 0x0123_4567_89ab_cdef);
        hart.write_csr(CSR_FFLAGS, 0x15);
        hart.write_csr(CSR_FRM, 3);
        hart.write_csr(CSR_MCYCLE, 41);
        hart.write_csr(CSR_MINSTRET, 17);
        for r in 1..32 {
            hart.write_x(r, 0x1111_2222_0000_0000 + u64::from(r));
        }
        hart.write_x(6, target);
        hart.write_x(9, patch);
        for r in 0..32 {
            hart.write_f(r, 0x7ff8_0000_0000_1000 + u64::from(r));
        }
        hart.reservation().establish(DATA, 8);
        // Bare translation does not consult these entries. Five installations
        // seed a nonzero FIFO cursor as well as valid local/global mappings.
        for i in 0..5 {
            hart.tlb().install(TlbEntry {
                valid: true,
                global: i % 2 == 0,
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
        let observer = Observer {
            memory,
            requests: Vec::new(),
        };
        let expected = Observation::capture(&mut hart, &observer, true);
        Self {
            hart,
            observer,
            expected,
        }
    }

    fn word(word: u32, mode: PrivilegeMode) -> Self {
        Self::new(
            &word.to_le_bytes(),
            mode,
            ENTRY,
            DATA,
            0x8877_6655_4433_2211,
        )
    }

    fn fetch(&mut self, length: u64) {
        for offset in (0..length).step_by(2) {
            self.expected.requests.push(Request::FetchParcel {
                addr: self.expected.pc + offset,
            });
        }
        self.expected.parcels += length / 2;
    }

    fn retire(&mut self, length: u64) {
        self.expected.pc += length;
        self.expected.csrs[CSR_MCYCLE] += 1;
        self.expected.csrs[CSR_MINSTRET] += 1;
    }

    fn observe(&mut self, table: &[InsnDef]) -> Observation {
        let outcome = exec_rv64gc::step_over(&mut self.hart, &mut self.observer, table);
        Observation::capture(
            &mut self.hart,
            &self.observer,
            outcome == StepRv64gc::Executed,
        )
    }

    fn check(&mut self, table: &[InsnDef]) -> Result<(), String> {
        judge(&self.observe(table), &self.expected)
    }
}

fn word(imm12: u32, rs1: u32, rd: u32) -> u32 {
    (imm12 << 20) | (rs1 << 15) | (rd << 7) | FENCE_I
}

fn check_word(table: &[InsnDef], word: u32, mode: PrivilegeMode) -> Result<(), String> {
    let mut fixture = Fixture::word(word, mode);
    fixture.fetch(4);
    fixture.retire(4);
    fixture
        .check(table)
        .map_err(|error| format!("FENCE.I {word:#010x} {mode:?}: {error}"))
}

fn self_modify(
    table: &[InsnDef],
    fence: u32,
    compressed: bool,
    offset: u64,
    mode: PrivilegeMode,
) -> Result<(), String> {
    let entry = ENTRY + offset;
    let target = entry + 16;
    let (old, patch, patch_offset, length) = if compressed {
        (0x4409_u32, 0x441d_u64, 0, 2) // C.LI x8,2 -> C.LI x8,7.
    } else {
        (0x0020_0413_u32, 0x70_u64, 2, 4) // ADDI x8,0,2 -> ADDI x8,0,7.
    };
    // SH patches only the required halfword, including at a 2-mod-4 word PC.
    // LHU reads it back before the changed instruction is fetched and executed.
    let words = [
        (9 << 20) | (6 << 15) | (1 << 12) | (patch_offset << 7) | 0x23,
        fence,
        (patch_offset << 20) | (6 << 15) | (5 << 12) | (10 << 7) | 3,
        0x0010_0393,
    ];
    let mut image: Vec<_> = words.into_iter().flat_map(u32::to_le_bytes).collect();
    image.extend_from_slice(&old.to_le_bytes()[..length as usize]);
    let mut fixture = Fixture::new(&image, mode, entry, target, patch);
    for boundary in 0..5 {
        let size = if boundary == 4 { length } else { 4 };
        fixture.fetch(size);
        match boundary {
            0 => {
                let address = target + u64::from(patch_offset);
                fixture.expected.requests.push(Request::Store {
                    width: AccessWidth::H,
                    addr: address,
                    data: patch,
                });
                let start = (address - ENTRY) as usize;
                fixture.expected.memory[start..start + 2]
                    .copy_from_slice(&(patch as u16).to_le_bytes());
            }
            2 => {
                fixture.expected.requests.push(Request::Load {
                    width: AccessWidth::H,
                    addr: target + u64::from(patch_offset),
                });
                fixture.expected.x[10] = patch;
            }
            3 => fixture.expected.x[7] = 1,
            4 => fixture.expected.x[8] = 7,
            _ => {}
        }
        fixture.retire(size);
        fixture.check(table).map_err(|error| {
            format!("patched {compressed:?} offset{offset} {mode:?} fence{fence:#x} boundary{boundary}: {error}")
        })?;
    }
    Ok(())
}

fn patches(fence: u32) -> Result<(), String> {
    for compressed in [false, true] {
        for offset in [0, 2] {
            for mode in MODES {
                self_modify(INSNS, fence, compressed, offset, mode)?;
            }
        }
    }
    Ok(())
}

pub(super) fn positive() -> Result<(), String> {
    for mode in MODES {
        check_word(INSNS, FENCE_I, mode)?;
    }
    patches(FENCE_I)?;
    patches(NOP)
}

pub(super) fn negative() -> Result<(), String> {
    for imm12 in 0..4096 {
        for (rs1, rd) in REGISTERS {
            if imm12 == 0 && rs1 == 0 && rd == 0 {
                continue;
            }
            for mode in MODES {
                check_word(INSNS, word(imm12, rs1, rd), mode)?;
            }
        }
    }
    patches(NONZERO)
}

#[cfg(test)]
mod tests {
    use super::*;
    use semulith_core::definition_rv64gc::Sem;

    fn changed_table(mask: u32, effect: &'static Sem) -> Vec<InsnDef> {
        assert_eq!(INSNS.iter().filter(|row| row.name == "fence.i").count(), 1);
        INSNS
            .iter()
            .map(|row| InsnDef {
                name: row.name,
                mask: if row.name == "fence.i" {
                    row.mask | mask
                } else {
                    row.mask
                },
                value: row.value,
                operands: row.operands,
                from: row.from,
                source: row.source,
                effect: if row.name == "fence.i" {
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
    fn all_fields_and_patched_parcels_preserve_the_declared_state() {
        assert_eq!(positive(), Ok(()));
        assert_eq!(negative(), Ok(()));
    }

    #[test]
    fn eleven_wrong_instruction_tables_fail_named_observations() {
        let cases: [(u32, &Sem, &str); 11] = [
            (0xfff0_0000, &Sem::Nop, "CSR owners differ"),
            (0x000f_8f80, &Sem::Nop, "CSR owners differ"),
            (
                0,
                &Sem::Set(&Sem::Reg("rd"), &Sem::Lit(0x0bad_c0de)),
                "integer registers differ",
            ),
            (
                0,
                &Sem::Set(&Sem::FReg("rd"), &Sem::Lit(0x0bad_c0de)),
                "floating registers differ",
            ),
            (
                0,
                &Sem::CsrWrite(&Sem::Lit(0x340), &Sem::Lit(0)),
                "CSR owners differ",
            ),
            (
                0,
                &Sem::Load(&Sem::Lit(64), &Sem::Lit(0), &Sem::Lit(DATA)),
                "requests differ",
            ),
            (
                0,
                &Sem::Store(&Sem::Lit(64), &Sem::Lit(DATA), &Sem::Lit(0)),
                "requests differ",
            ),
            (
                0,
                &Sem::TrapDeliver(&Sem::Lit(2), &Sem::Inst),
                "CSR owners differ",
            ),
            (
                0,
                &Sem::SetPc(&Sem::Add(&Sem::Pc, &Sem::Lit(8))),
                "PC/mode differs",
            ),
            (
                0,
                &Sem::StoreConditional(&Sem::Lit(64), &Sem::Lit(DATA + 8), &Sem::Lit(0)),
                "reservation differs",
            ),
            (
                0,
                &Sem::TlbInvalidate(&Sem::Lit(0), &Sem::Lit(0), &Sem::Lit(1), &Sem::Lit(1)),
                "TLB/cursor differs",
            ),
        ];
        for (mask, effect, reason) in cases {
            let table = changed_table(mask, effect);
            let error = check_word(&table, NONZERO, PrivilegeMode::M).expect_err(reason);
            assert!(error.contains(reason), "{reason}: {error}");
        }
    }

    #[test]
    fn sixteen_corrupted_captures_fail_the_complete_auditor() {
        let mut fixture = Fixture::word(NONZERO, PrivilegeMode::M);
        fixture.fetch(4);
        fixture.retire(4);
        let observed = fixture.observe(INSNS);
        assert_eq!(judge(&observed, &fixture.expected), Ok(()));
        let check = |bad: Observation, reason| {
            assert_eq!(judge(&bad, &fixture.expected).unwrap_err(), reason);
        };
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
            let mut bad = observed.clone();
            bad.requests.push(request);
            check(bad, "requests differ");
        }
        let mut bad = observed.clone();
        bad.memory[0x80] ^= 1;
        check(bad, "memory differs");
        let mut bad = observed.clone();
        bad.x[5] ^= 1;
        check(bad, "integer registers differ");
        let mut bad = observed.clone();
        bad.f[5] ^= 1;
        check(bad, "floating registers differ");
        let mut bad = observed.clone();
        bad.csrs[CSR_MSCRATCH] ^= 1;
        check(bad, "CSR owners differ");
        let mut bad = observed.clone();
        bad.reservation.clear();
        check(bad, "reservation differs");
        let mut bad = observed.clone();
        bad.reservation.establish(DATA + 8, 4);
        check(bad, "reservation differs");
        let mut bad = observed.clone();
        bad.tlb.invalidate(None, None);
        check(bad, "TLB/cursor differs");
        let mut bad = observed.clone();
        let entry = bad.tlb.lookup(0x41, 0x12).expect("the seeded cursor slot");
        bad.tlb.install(entry); // Same entries, different replacement cursor.
        for vpn in 0x41..=0x44 {
            assert_eq!(bad.tlb.lookup(vpn, 0x12), observed.tlb.lookup(vpn, 0x12));
        }
        check(bad, "TLB/cursor differs");
        let mut bad = observed.clone();
        bad.wait.enter();
        check(bad, "wait state differs");
        let mut bad = observed.clone();
        bad.pc += 2;
        check(bad, "PC/mode differs");
        let mut bad = observed.clone();
        bad.mode = PrivilegeMode::U;
        check(bad, "PC/mode differs");
        let mut bad = observed.clone();
        bad.parcels += 1;
        check(bad, "boundary outcome/parcels differ");
        let mut bad = observed;
        bad.executed = false;
        check(bad, "boundary outcome/parcels differ");
    }
}
