//! FENCE field treatment and one-hart no-effect witnesses (RV32I 1.1.7).

use semulith_core::definition_rv64gc::{InsnDef, INSNS};
use semulith_core::env::{AccessWidth, BoundaryError, Environment, Request, Response};
use semulith_core::exec_rv64gc::{self, StepRv64gc};
use semulith_core::state_rv64gc::{
    ArchitecturalState, PrivilegeMode, CSR_COUNT, CSR_FFLAGS, CSR_FRM, CSR_MCAUSE, CSR_MCYCLE,
    CSR_MEPC, CSR_MINSTRET, CSR_MSCRATCH, CSR_MSTATUS, CSR_MTVAL, CSR_MTVEC, CSR_SATP,
    CSR_SSCRATCH,
};

use crate::fixtures::FlatMemory;

const ENTRY: u64 = 0x1000;
const DATA: u64 = 0x1080;
const OLD: u64 = 0x1122_3344_5566_7788;
const NEW: u64 = 0x8877_6655_4433_2211;
const FENCES: [u32; 3] = [0x0ff0_000f, 0x8330_000f, 0xffff_8f8f];
const MODES: [PrivilegeMode; 3] = [PrivilegeMode::M, PrivilegeMode::S, PrivilegeMode::U];

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

struct Expected {
    x: [u64; 32],
    f: [u64; 32],
    csrs: [u64; CSR_COUNT],
    pc: u64,
    mode: PrivilegeMode,
    parcels: u64,
    requests: Vec<Request>,
    memory: Vec<u8>,
}

struct Fixture {
    hart: ArchitecturalState,
    observer: Observer,
    expected: Expected,
}

impl Fixture {
    fn new(memory: FlatMemory, mode: PrivilegeMode) -> Self {
        let mut hart = ArchitecturalState::zeroed_at(ENTRY);
        hart.set_mode(mode);
        hart.write_csr(CSR_MSTATUS, 0xa_0000_6000); // FS Dirty; interrupt enables clear.
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
        let mut x = [0; 32];
        for (r, value) in x.iter_mut().enumerate().skip(1) {
            *value = 0x1111_2222_0000_0000 + r as u64;
        }
        x[6] = DATA;
        x[9] = NEW;
        let f = std::array::from_fn(|r| 0x7ff8_0000_0000_1000 + r as u64);
        for r in 0..32 {
            hart.write_x(r, x[r as usize]);
            hart.write_f(r, f[r as usize]);
        }
        let expected = Expected {
            x,
            f,
            // Preservation is relative to the seeded state before execution.
            csrs: std::array::from_fn(|i| hart.read_csr(i)),
            pc: ENTRY,
            mode,
            parcels: 0,
            requests: Vec::new(),
            memory: memory.bytes().to_vec(),
        };
        Self {
            hart,
            observer: Observer {
                memory,
                requests: Vec::new(),
            },
            expected,
        }
    }

    fn bare(words: &[u32], mode: PrivilegeMode) -> Self {
        let mut memory = FlatMemory::with_fetch_align(ENTRY, 0x200, 2);
        for (i, word) in words.iter().enumerate() {
            memory.load_image(i * 4, &word.to_le_bytes());
        }
        memory.load_image(0x80, &OLD.to_le_bytes());
        Self::new(memory, mode)
    }

    fn fetch(&mut self, physical_pc: u64) {
        self.expected.requests.extend([
            Request::FetchParcel { addr: physical_pc },
            Request::FetchParcel {
                addr: physical_pc + 2,
            },
        ]);
    }

    fn step(&mut self, table: &[InsnDef]) -> Result<(), String> {
        self.expected.pc += 4;
        self.expected.csrs[CSR_MCYCLE] += 1;
        self.expected.csrs[CSR_MINSTRET] += 1;
        self.expected.parcels += 2;
        let outcome = exec_rv64gc::step_over(&mut self.hart, &mut self.observer, table);
        if self.observer.requests != self.expected.requests {
            return Err(format!(
                "requests differ: {:?}, required {:?}",
                self.observer.requests, self.expected.requests
            ));
        }
        if self.observer.memory.bytes() != self.expected.memory {
            return Err("memory differs".into());
        }
        if std::array::from_fn(|r| self.hart.read_x(r as u8)) != self.expected.x {
            return Err("integer registers differ".into());
        }
        if std::array::from_fn(|r| self.hart.read_f(r as u8)) != self.expected.f {
            return Err("floating registers differ".into());
        }
        if std::array::from_fn(|r| self.hart.read_csr(r)) != self.expected.csrs {
            return Err("CSR owners differ".into());
        }
        if outcome != StepRv64gc::Executed
            || self.hart.pc() != self.expected.pc
            || self.hart.mode() != self.expected.mode
            || self.observer.memory.fetch_count() != self.expected.parcels
        {
            return Err(format!("state differs: {outcome:?}"));
        }
        Ok(())
    }
}

fn word(config: u32, rs1: u32, rd: u32) -> u32 {
    (config << 20) | (rs1 << 15) | (rd << 7) | 0x0f
}

fn check_word(table: &[InsnDef], word: u32, mode: PrivilegeMode) -> Result<(), String> {
    let mut fixture = Fixture::bare(&[word], mode);
    fixture.fetch(ENTRY);
    fixture
        .step(table)
        .map_err(|error| format!("FENCE {word:#010x} {mode:?}: {error}"))
}

fn reservation(table: &[InsnDef], fence: u32) -> Result<(), String> {
    // LR.D x7,(x6); FENCE; SC.D x8,x9,(x6); LD x10,0(x6).
    let words = [0x1003_33af, fence, 0x1893_342f, 0x0003_3503];
    let mut fixture = Fixture::bare(&words, PrivilegeMode::M);
    for i in 0..4 {
        fixture.fetch(ENTRY + 4 * i);
        match i {
            0 => {
                fixture.expected.requests.push(Request::Load {
                    width: AccessWidth::D,
                    addr: DATA,
                });
                fixture.expected.x[7] = OLD;
            }
            2 => {
                fixture.expected.requests.push(Request::Store {
                    width: AccessWidth::D,
                    addr: DATA,
                    data: NEW,
                });
                fixture.expected.x[8] = 0;
                fixture.expected.memory[0x80..0x88].copy_from_slice(&NEW.to_le_bytes());
            }
            3 => {
                fixture.expected.requests.push(Request::Load {
                    width: AccessWidth::D,
                    addr: DATA,
                });
                fixture.expected.x[10] = NEW;
            }
            _ => {}
        }
        fixture.step(table).map_err(|error| {
            format!(
                "reservation FENCE {fence:#010x} boundary {}: {error}",
                i + 1
            )
        })?;
    }
    Ok(())
}

fn translation(table: &[InsnDef], fence: u32) -> Result<(), String> {
    // A warm 1 GiB S leaf: ADDI x7,0,1; FENCE; ADDI x8,0,2.
    let mut memory = FlatMemory::with_fetch_align(0x8000_0000, 0x4000, 2);
    for (i, word) in [0x0010_0393_u32, fence, 0x0020_0413].iter().enumerate() {
        memory.load_image(0x1000 + i * 4, &word.to_le_bytes());
    }
    memory.load_image(0x2000, &0x2000_00cf_u64.to_le_bytes());
    let mut fixture = Fixture::new(memory, PrivilegeMode::S);
    fixture.hart.write_csr(CSR_SATP, 0x8000_0000_0008_0002);
    fixture.expected.csrs[CSR_SATP] = 0x8000_0000_0008_0002;
    fixture
        .expected
        .requests
        .push(Request::WalkAccess { addr: 0x8000_2000 });
    for i in 0..3 {
        fixture.fetch(0x8000_1000 + 4 * i);
        if i == 0 {
            fixture.expected.x[7] = 1;
        }
        if i == 2 {
            fixture.expected.x[8] = 2;
        }
        fixture.step(table).map_err(|error| {
            format!(
                "translation FENCE {fence:#010x} boundary {}: {error}",
                i + 1
            )
        })?;
    }
    Ok(())
}

pub(super) fn positive() -> Result<(), String> {
    for config in 0..4096 {
        if config >> 8 == 0 || config == 0x833 {
            for mode in MODES {
                check_word(INSNS, word(config, 0, 0), mode)?;
            }
        }
    }
    reservation(INSNS, FENCES[0])?;
    translation(INSNS, FENCES[0])
}

pub(super) fn negative() -> Result<(), String> {
    for config in 0..4096 {
        for mode in MODES {
            if config >> 8 != 0 && config != 0x833 {
                check_word(INSNS, word(config, 0, 0), mode)?;
            }
            for (rs1, rd) in [(0, 31), (31, 0), (31, 31), (7, 13)] {
                check_word(INSNS, word(config, rs1, rd), mode)?;
            }
        }
    }
    for fence in &FENCES[1..] {
        reservation(INSNS, *fence)?;
        translation(INSNS, *fence)?;
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use semulith_core::definition_rv64gc::Sem;

    fn changed_table(mask: u32, effect: &'static Sem) -> Vec<InsnDef> {
        assert_eq!(INSNS.iter().filter(|row| row.name == "fence").count(), 1);
        INSNS
            .iter()
            .map(|row| InsnDef {
                name: row.name,
                mask: if row.name == "fence" {
                    row.mask | mask
                } else {
                    row.mask
                },
                value: row.value,
                operands: row.operands,
                from: row.from,
                source: row.source,
                effect: if row.name == "fence" {
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
    fn all_mode_and_field_cases_preserve_state_and_integration() {
        assert_eq!(positive(), Ok(()));
        assert_eq!(negative(), Ok(()));
    }

    #[test]
    fn ten_wrong_fence_tables_fail_named_observations() {
        let cases: [(&str, u32, &Sem, &str); 8] = [
            ("reject fm", 0xf000_0000, &Sem::Nop, "CSR owners differ"),
            (
                "reject ignored fields",
                0x000f_8f80,
                &Sem::Nop,
                "CSR owners differ",
            ),
            (
                "write GPR",
                0,
                &Sem::Set(&Sem::Reg("rd"), &Sem::Lit(0x0bad_c0de)),
                "integer registers differ",
            ),
            (
                "write FPR",
                0,
                &Sem::Set(&Sem::FReg("rd"), &Sem::Lit(0x0bad_c0de)),
                "floating registers differ",
            ),
            (
                "write CSR",
                0,
                &Sem::CsrWrite(&Sem::Lit(0x340), &Sem::Lit(0)),
                "CSR owners differ",
            ),
            (
                "store",
                0,
                &Sem::Store(&Sem::Lit(64), &Sem::Lit(DATA), &Sem::Lit(0)),
                "requests differ",
            ),
            (
                "trap",
                0,
                &Sem::TrapDeliver(&Sem::Lit(2), &Sem::Inst),
                "CSR owners differ",
            ),
            (
                "skip PC",
                0,
                &Sem::SetPc(&Sem::Add(&Sem::Pc, &Sem::Lit(8))),
                "state differs",
            ),
        ];
        for (name, mask, effect, reason) in cases {
            let table = changed_table(mask, effect);
            let error = check_word(&table, FENCES[2], PrivilegeMode::M).expect_err(name);
            assert!(error.contains(reason), "{name}: {error}");
        }
        let table = changed_table(
            0,
            &Sem::StoreConditional(&Sem::Lit(64), &Sem::Lit(DATA + 8), &Sem::Lit(0)),
        );
        assert!(reservation(&table, FENCES[2])
            .expect_err("consume reservation")
            .contains("requests differ"));
        let table = changed_table(
            0,
            &Sem::TlbInvalidate(&Sem::Lit(0), &Sem::Lit(0), &Sem::Lit(1), &Sem::Lit(1)),
        );
        assert!(translation(&table, FENCES[2])
            .expect_err("flush translation")
            .contains("requests differ"));
    }
}
