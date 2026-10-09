//! No platform source is supplied. STCE selects hart software or comparator STIP.
//! Literal CSR words/observations follow RVP-MACHINE 2.1.1.9/2.1.1.18.
//! An ignored architectural write is not a provider contract violation.

use semulith_core::exec_rv64gc::{self, StepRv64gc};
use semulith_core::state_rv64gc::{
    ArchitecturalState, PrivilegeMode, CSR_MENVCFG, CSR_MIDELEG, CSR_MIP, CSR_STIMECMP,
};

use crate::fixtures::FlatMemory;

const ENTRY: u64 = 0x1000;
type Observation = (u32, Option<(usize, u64)>, u64);

fn run(mut hart: ArchitecturalState, rows: &[Observation]) -> Result<(), String> {
    let mode = hart.mode();
    let mut memory = FlatMemory::with_fetch_align(ENTRY, 128, 2);
    for (i, (word, _, _)) in rows.iter().enumerate() {
        memory.load_image(i * 4, &word.to_le_bytes());
    }
    let mut registers = std::array::from_fn::<_, 32, _>(|i| hart.read_x(i as u8));
    for (i, (_, write, raw_pending)) in rows.iter().enumerate() {
        if let Some((reg, value)) = write {
            registers[*reg] = *value;
        }
        if exec_rv64gc::step(&mut hart, &mut memory) != StepRv64gc::Executed
            || hart.mode() != mode
            || hart.pc() != ENTRY + 4 * (i as u64 + 1)
            || hart.read_csr(CSR_MIP) != *raw_pending
            || memory.fetch_count() != 2 * (i as u64 + 1)
            || registers
                .iter()
                .enumerate()
                .any(|(reg, value)| hart.read_x(reg as u8) != *value)
        {
            return Err(format!(
                "interrupt-source instruction {i} differs from its literal witness"
            ));
        }
    }
    Ok(())
}

fn state() -> ArchitecturalState {
    let mut hart = ArchitecturalState::zeroed_at(ENTRY);
    hart.write_csr(CSR_STIMECMP, u64::MAX);
    for reg in 5..=12 {
        hart.write_x(reg, 0x55); // zero-valued reads must visibly replace a sentinel
    }
    hart
}

pub(super) fn positive() -> Result<(), String> {
    let mut hart = state();
    hart.write_x(31, 1 << 63);
    // Set/read/clear software STIP, enable comparator, assert by compare=0,
    // then disable and recover the cleared software value. Finish visibly.
    run(
        hart,
        &[
            (0x0200_0113, Some((2, 32)), 0),
            (0x3441_12f3, Some((5, 0)), 32),
            (0x3440_2373, Some((6, 32)), 32),
            (0x3441_33f3, Some((7, 32)), 0),
            (0x3440_2473, Some((8, 0)), 0),
            (0x30af_9073, None, 0),
            (0x3440_24f3, Some((9, 0)), 0),
            (0x14d0_1073, None, 0),
            (0x3440_2573, Some((10, 32)), 0),
            (0x30a0_25f3, Some((11, 1 << 63)), 0),
            (0x30a0_1073, None, 0),
            (0x3440_2673, Some((12, 0)), 0),
            (0x02a0_0693, Some((13, 42)), 0),
        ],
    )
}

pub(super) fn negative() -> Result<(), String> {
    // All-one M pending write sets only SSIP/STIP/SEIP, never MSIP/MTIP/MEIP.
    let mut hart = state();
    hart.write_x(31, u64::MAX);
    run(
        hart,
        &[
            (0x344f_92f3, Some((5, 0)), 0x222),
            (0x3440_2373, Some((6, 0x222)), 0x222),
        ],
    )?;

    // Enabled comparator pending is read-only; the hidden software bit survives.
    let mut hart = state();
    hart.write_csr(CSR_MENVCFG, 1 << 63);
    hart.write_csr(CSR_MIP, 32);
    run(
        hart,
        &[
            (0x3440_12f3, Some((5, 0)), 32),
            (0x3440_2373, Some((6, 0)), 32),
            (0x30a0_1073, None, 32),
            (0x3440_2473, Some((8, 32)), 32),
        ],
    )?;

    // sip.STIP is read-only in both M and S, with either selected pending source.
    for mode in [PrivilegeMode::M, PrivilegeMode::S] {
        for (stce, visible) in [(0, 32), (1 << 63, 0)] {
            let mut hart = state();
            hart.set_mode(mode);
            hart.write_csr(CSR_MENVCFG, stce);
            hart.write_csr(CSR_MIDELEG, 32);
            hart.write_csr(CSR_MIP, 32);
            run(
                hart,
                &[
                    (0x1440_12f3, Some((5, visible)), 32),
                    (0x1440_2373, Some((6, visible)), 32),
                ],
            )?;
        }
    }
    Ok(())
}
