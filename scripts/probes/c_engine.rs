//! Spec-side instruction words and boundary schedules for P4-SYSTEM.12 c2.
//! RVI-C §27.1.3–§27.1.7, instruction-length encoding, RVP-MACHINE §2.1.1.16.
//! The expectations do not read the expansion declarations or evaluate a second copy.
use std::collections::BTreeMap;

use crate::env::{AccessWidth, BoundaryError, Environment, Failure, Request, Response};
use crate::exec_rv64gc::{step, StepRv64gc};
use crate::privilege::{self, PrivilegeMode};
use crate::state_rv64gc::{ArchitecturalState, CSR_MSTATUS, CSR_SATP};

const PC: u64 = 0x1000;

#[derive(Default)]
struct Memory {
    bytes: BTreeMap<u64, u8>,
    requests: Vec<Request>,
}
impl Memory {
    fn put(&mut self, addr: u64, data: u64, len: u64) {
        for i in 0..len {
            self.bytes.insert(addr + i, (data >> (8 * i)) as u8);
        }
    }
    fn read(&self, addr: u64, len: u64) -> Result<u64, BoundaryError> {
        let mut result = 0;
        for i in 0..len {
            result |= u64::from(
                *self
                    .bytes
                    .get(&addr.wrapping_add(i))
                    .ok_or(Failure::AccessFault)?,
            ) << (8 * i);
        }
        Ok(result)
    }
}
impl Environment for Memory {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        self.requests.push(request);
        match request {
            Request::FetchParcel { addr } => {
                if addr % 2 != 0 {
                    return Err(Failure::Misaligned.into());
                }
                Ok(Response::FetchParcel(self.read(addr, 2)? as u16))
            }
            Request::Fetch { addr } => Ok(Response::Fetch(self.read(addr, 4)? as u32)),
            Request::Load { width, addr } => Ok(Response::Load(self.read(addr, width.bytes())?)),
            Request::Store { width, addr, data } => {
                // Refuse before changing memory if any requested byte is outside it.
                self.read(addr, width.bytes())?;
                self.put(addr, data, width.bytes());
                Ok(Response::StoreDone)
            }
            Request::WalkAccess { addr } => Ok(Response::WalkAccess(self.read(addr, 8)?)),
        }
    }
}
fn state(pc: u64) -> ArchitecturalState {
    ArchitecturalState::zeroed_at(pc)
}
fn exec(
    word: u16,
    setup: impl FnOnce(&mut ArchitecturalState, &mut Memory),
) -> (ArchitecturalState, Memory) {
    let mut s = state(PC);
    let mut m = Memory::default();
    // A neighbor with every bit set distinguishes a 16-bit inst from the fetched word.
    m.put(PC, u64::from(word) | 0xffff_0000, 4);
    setup(&mut s, &mut m);
    assert_eq!(step(&mut s, &mut m), StepRv64gc::Executed);
    (s, m)
}
fn csr(s: &ArchitecturalState, name: &str) -> u64 {
    privilege::csr_state(s, name)
}

#[test]
fn mixed_lengths_at_two_mod_four_and_exact_region_end() {
    let mut s = state(PC);
    let mut m = Memory::default();
    m.put(PC, 0x0085, 2); // c.addi x1, 1
    m.put(PC + 2, 0x0010_0113, 4); // addi x2, x0, 1 at 2 mod 4
    s.write_x(1, 7);
    assert_eq!(step(&mut s, &mut m), StepRv64gc::Executed);
    assert_eq!((s.pc(), s.read_x(1)), (PC + 2, 8));
    assert_eq!(step(&mut s, &mut m), StepRv64gc::Executed);
    assert_eq!((s.pc(), s.read_x(2)), (PC + 6, 1));
    assert_eq!(
        m.requests,
        vec![
            Request::FetchParcel { addr: PC },
            Request::FetchParcel { addr: PC + 2 },
            Request::FetchParcel { addr: PC + 4 }
        ]
    );
    assert_eq!(csr(&s, "minstret"), 2);
}

#[test]
fn signed_immediates_keep_their_mapped_widths() {
    for (word, expected) in [(0x1081, 7u64.wrapping_sub(32)), (0x00fd, 38), (0x10fd, 6)] {
        let (s, _) = exec(word, |s, _| s.write_x(1, 7)); // c.addi x1, -32 / 31 / -1
        assert_eq!(s.read_x(1), expected, "word {word:x}");
        assert_eq!(s.pc(), PC + 2);
    }
    let (s, _) = exec(0x7181, |_, _| {}); // c.lui x3, -32 => -32 << 12
    assert_eq!(s.read_x(3), (-131072i64) as u64);
}

#[test]
fn compact_load_uses_unsigned_offset_and_signed_word_result() {
    // c.lw x8, 124(x8): bits 12:10 and 6:5 all one; rd'/rs1' both zero.
    let (s, m) = exec(0x5c60, |s, m| {
        s.write_x(8, 0x4000);
        m.put(0x407c, 0x8000_0001, 4);
    });
    assert_eq!(s.read_x(8), 0xffff_ffff_8000_0001);
    assert!(m.requests.contains(&Request::Load {
        width: AccessWidth::W,
        addr: 0x407c
    }));
}

#[test]
fn compact_store_snapshots_overlapping_register_operands() {
    let (s, m) = exec(0xc000, |s, m| {
        s.write_x(8, 0x4000);
        m.put(0x4000, 0, 4);
    }); // c.sw x8, 0(x8)
    assert_eq!(m.read(0x4000, 4).unwrap(), 0x4000);
    assert_eq!(s.pc(), PC + 2);
}

#[test]
fn compressed_jumps_link_by_two_and_use_the_old_source() {
    let (s, _) = exec(0x9082, |s, _| s.write_x(1, PC + 7)); // c.jalr x1 (rd=rs1)
    assert_eq!((s.pc(), s.read_x(1)), (PC + 6, PC + 2));
    // c.j -2 and c.j at both signed extremes, hand-encoded from CJ's bit layout.
    for (word, offset) in [(0xbffd, -2i64), (0xb001, -2048), (0xaffd, 2046)] {
        let (s, _) = exec(word, |_, _| {});
        assert_eq!(s.pc(), PC.wrapping_add(offset as u64));
        assert_eq!(s.read_x(1), 0);
    }
}

#[test]
fn compressed_branch_keeps_its_signed_offset_and_fallthrough_length() {
    let (s, _) = exec(0xd001, |_, _| {}); // c.beqz x8, -256
    assert_eq!(s.pc(), PC - 256);
    let (s, _) = exec(0xd001, |s, _| s.write_x(8, 1));
    assert_eq!(s.pc(), PC + 2);
    let (s, _) = exec(0xf001, |s, _| s.write_x(8, 1)); // c.bnez x8, -256
    assert_eq!(s.pc(), PC - 256);
}

#[test]
fn parcel_addresses_and_fallthrough_wrap_at_xlen() {
    let pc = u64::MAX - 1;
    let mut s = state(pc);
    let mut m = Memory::default();
    m.put(pc, 0x0113, 2); // addi x2, x0, 1, split over the address wrap
    m.put(0, 0x0010, 2);
    assert_eq!(step(&mut s, &mut m), StepRv64gc::Executed);
    assert_eq!((s.pc(), s.read_x(2)), (2, 1));
    assert_eq!(
        m.requests,
        vec![
            Request::FetchParcel { addr: pc },
            Request::FetchParcel { addr: 0 }
        ]
    );
}

#[test]
fn malformed_environment_answers_stay_model_failures() {
    struct WrongAnswer;
    impl Environment for WrongAnswer {
        fn request(&mut self, _: Request) -> Result<Response, BoundaryError> {
            Ok(Response::Fetch(1))
        }
    }
    let mut s = state(PC);
    assert!(matches!(
        step(&mut s, &mut WrongAnswer),
        StepRv64gc::Failed(_)
    ));
    assert_eq!((s.pc(), csr(&s, "minstret"), csr(&s, "mtval")), (PC, 0, 0));
}

#[test]
fn reserved_parcels_trap_without_a_link_or_retirement() {
    for word in [0x0000, 0x6101, 0x6181, 0x2001, 0x4002, 0x6002, 0x8002] {
        let (s, m) = exec(word, |s, _| s.write_x(1, 0x55));
        assert_eq!(
            (csr(&s, "mcause"), csr(&s, "mtval"), csr(&s, "mepc")),
            (2, u64::from(word), PC),
            "word {word:x}"
        );
        assert_eq!(s.read_x(1), 0x55);
        assert_eq!(csr(&s, "minstret"), 0);
        assert_eq!(m.requests, vec![Request::FetchParcel { addr: PC }]);
    }
}

#[test]
fn hints_execute_without_trapping_or_register_changes() {
    for word in [0x0081, 0x4005, 0x0082, 0x8006, 0x9006, 0x0005] {
        let (s, _) = exec(word, |s, _| s.write_x(1, 7));
        assert_eq!(s.pc(), PC + 2, "HINT {word:x}");
        assert_eq!(s.read_x(1), 7);
        assert_eq!(csr(&s, "minstret"), 1);
    }
}

#[test]
fn breakpoint_specialization_and_fp_gate_use_only_sixteen_bits() {
    let (s, _) = exec(0x9002, |s, _| s.write_x(1, 7)); // c.ebreak wins over c.jalr/c.add
    assert_eq!((csr(&s, "mcause"), csr(&s, "mepc")), (3, PC));
    let (s, m) = exec(0x2000, |s, _| s.write_x(8, 0x4000)); // c.fld f8, 0(x8), FS=Off
    assert_eq!((csr(&s, "mcause"), csr(&s, "mtval")), (2, 0x2000));
    assert_eq!(m.requests, vec![Request::FetchParcel { addr: PC }]);
}

#[test]
fn fp_load_expands_to_the_f_file_and_marks_dirty() {
    let bits = 0x4009_21fb_5444_2d18;
    let (s, _) = exec(0x2000, |s, m| {
        s.write_csr(CSR_MSTATUS, 1 << 13); // FS=Initial
        s.write_x(8, 0x4000);
        m.put(0x4000, bits, 8);
    });
    assert_eq!(s.read_f(8), bits);
    assert_eq!(privilege::fs(&s), 3);
}

#[test]
fn second_parcel_access_fault_names_the_second_address() {
    let mut s = state(0x1ffe);
    let mut m = Memory::default();
    m.put(0x1ffe, 0x0093, 2);
    assert_eq!(step(&mut s, &mut m), StepRv64gc::Executed);
    assert_eq!(
        (csr(&s, "mcause"), csr(&s, "mtval"), csr(&s, "mepc")),
        (1, 0x2000, 0x1ffe)
    );
    assert_eq!(csr(&s, "minstret"), 0);
    assert_eq!(
        m.requests,
        vec![
            Request::FetchParcel { addr: 0x1ffe },
            Request::FetchParcel { addr: 0x2000 }
        ]
    );
}

fn translated(word: u16) -> (ArchitecturalState, Memory) {
    let mut s = state(0x4ffe);
    let mut m = Memory::default();
    s.write_csr(CSR_SATP, (8 << 60) | 8); // Sv39 root at 0x8000
    s.set_mode(PrivilegeMode::S);
    m.put(0x8000, (9 << 10) | 1, 8);
    m.put(0x9000, (10 << 10) | 1, 8);
    m.put(0xa000 + 4 * 8, (11 << 10) | 0x4b, 8); // V/R/X/A, S leaf
    m.put(0xa000 + 5 * 8, 0, 8); // the next virtual page is unmapped
    m.put(0xbffe, u64::from(word), 2);
    (s, m)
}
#[test]
fn compressed_last_parcel_never_walks_the_unmapped_next_page() {
    let (mut s, mut m) = translated(0x0085);
    assert_eq!(step(&mut s, &mut m), StepRv64gc::Executed);
    assert_eq!((s.pc(), s.read_x(1)), (0x5000, 1));
    assert!(!m.requests.contains(&Request::WalkAccess { addr: 0xa028 }));
    assert_eq!(csr(&s, "minstret"), 1);
}
#[test]
fn straddling_word_page_fault_preserves_instruction_start() {
    let (mut s, mut m) = translated(0x0093);
    assert_eq!(step(&mut s, &mut m), StepRv64gc::Executed);
    assert_eq!(
        (csr(&s, "mcause"), csr(&s, "mtval"), csr(&s, "mepc")),
        (12, 0x5000, 0x4ffe)
    );
    assert_eq!(csr(&s, "minstret"), 0);
    assert!(m.requests.contains(&Request::FetchParcel { addr: 0xbffe }));
    assert!(!m
        .requests
        .iter()
        .any(|r| matches!(r, Request::FetchParcel { addr: 0xc000 })));
}
