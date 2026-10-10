//! Direct architectural execution witnesses, separate from provider assumptions.
//!
//! Literal CSR words and values follow RVP-SSTC 12.1, RVP-SUPERVISOR
//! 11.1.1.12 and RVP-MACHINE 2.1.1.11/2.1.1.18. No processor semantics live here.

mod load_x0;

use semulith_core::exec_rv64gc::{self, StepRv64gc};
use semulith_core::state_rv64gc::{
    ArchitecturalState, PrivilegeMode, CSR_MCAUSE, CSR_MCOUNTEREN, CSR_MCYCLE, CSR_MENVCFG,
    CSR_MEPC, CSR_MIDELEG, CSR_MINSTRET, CSR_MTVAL, CSR_MTVEC, CSR_STIMECMP,
};

use crate::fixtures::FlatMemory;

const ENTRY: u64 = 0x1000;
const HANDLER: u64 = ENTRY + 0x100;
const STCE: u64 = 1 << 63;

/// The direct witness a registry entry names.
#[derive(Clone, Copy, Debug)]
pub enum ExecutionCheck {
    /// All seven x0 loads still issue exactly one data request.
    LoadX0Positive,
    /// Discarded destinations retain access, alignment and page faults.
    LoadX0Negative,
    /// S programs and reads its timer without an M-mode round trip.
    SstcPositive,
    /// Closed TM/STCE gates and U privilege refuse before destination/compare effects.
    SstcNegative,
}

impl ExecutionCheck {
    /// Companion guests use the registry's existing corpus comparison rule.
    #[must_use]
    pub const fn guests(self) -> &'static [&'static str] {
        match self {
            Self::LoadX0Positive => &["scope-mem", "dir-x0-writes"],
            Self::LoadX0Negative => &["fault-ld-x0-fault", "fault-ld-x0-mis"],
            Self::SstcPositive => &["i-timer", "w-timer"],
            Self::SstcNegative => &["mm-stimecmp"],
        }
    }

    /// Run the direct witness; the registry also runs its companion guests.
    pub fn run(self) -> Result<(), String> {
        match self {
            Self::LoadX0Positive => load_x0::positive(),
            Self::LoadX0Negative => load_x0::negative(),
            Self::SstcPositive => positive(enabled_supervisor()),
            Self::SstcNegative => {
                for (mode, tm, stce) in [
                    (PrivilegeMode::S, 0, STCE),
                    (PrivilegeMode::S, 2, 0),
                    (PrivilegeMode::U, 2, STCE),
                ] {
                    refusal(mode, tm, stce)?;
                }
                Ok(())
            }
        }
    }
}

struct Witness {
    x: [u64; 32],
    pc: u64,
    mode: PrivilegeMode,
    compare: u64,
    boundaries: u64,
    retired: u64,
    trap: Option<(u64, u64, u64)>,
}

impl Witness {
    fn from(hart: &ArchitecturalState) -> Self {
        Self {
            x: std::array::from_fn(|r| hart.read_x(r as u8)),
            pc: ENTRY,
            mode: PrivilegeMode::S,
            compare: 0,
            boundaries: 0,
            retired: 0,
            trap: None,
        }
    }

    fn step(&self, hart: &mut ArchitecturalState, memory: &mut FlatMemory) -> Result<(), String> {
        let outcome = exec_rv64gc::step(hart, memory);
        let trap_matches = self.trap.is_none_or(|(cause, tval, epc)| {
            (
                hart.read_csr(CSR_MCAUSE),
                hart.read_csr(CSR_MTVAL),
                hart.read_csr(CSR_MEPC),
            ) == (cause, tval, epc)
        });
        if outcome != StepRv64gc::Executed
            || hart.mode() != self.mode
            || hart.pc() != self.pc
            || hart.read_csr(CSR_STIMECMP) != self.compare
            || hart.read_csr(CSR_MCYCLE) != self.boundaries
            || hart.read_csr(CSR_MINSTRET) != self.retired
            || memory.fetch_count() != self.boundaries * 2
            || !trap_matches
            || self
                .x
                .iter()
                .enumerate()
                .any(|(r, value)| hart.read_x(r as u8) != *value)
        {
            return Err(format!(
                "Sstc boundary {} differs from literal witness",
                self.boundaries
            ));
        }
        Ok(())
    }
}

fn memory(words: &[u32]) -> FlatMemory {
    let mut memory = FlatMemory::with_fetch_align(ENTRY, 0x200, 2);
    for (i, word) in words.iter().enumerate() {
        memory.load_image(i * 4, &word.to_le_bytes());
    }
    memory
}

fn enabled_supervisor() -> ArchitecturalState {
    let mut hart = ArchitecturalState::zeroed_at(ENTRY);
    hart.set_mode(PrivilegeMode::S);
    hart.write_csr(CSR_MCOUNTEREN, 2);
    hart.write_csr(CSR_MENVCFG, STCE);
    hart.write_csr(CSR_MIDELEG, 32);
    // Interrupt enables remain clear: pending is observed without taking the interrupt.
    for reg in 6..=11 {
        hart.write_x(reg, 0x55);
    }
    hart.write_x(12, 0x8000_0000_0000_0020);
    hart.write_x(13, 0x55);
    hart
}

fn positive(mut hart: ArchitecturalState) -> Result<(), String> {
    // word, destination observation, compare after this instruction.
    let rows = [
        (0x0100_0293, Some((5, 16)), 0),
        (0x14d2_9373, Some((6, 0)), 16),
        (0x14d0_23f3, Some((7, 16)), 16),
        (0x1440_2473, Some((8, 0)), 16),
        (0x0000_0293, Some((5, 0)), 16),
        (0x14d2_9073, None, 0),
        (0x1440_24f3, Some((9, 32)), 0),
        (0x0200_0293, Some((5, 32)), 0),
        (0x14d2_9073, None, 32),
        (0x14d0_2573, Some((10, 32)), 32),
        (0x1440_25f3, Some((11, 0)), 32),
        (0x14d6_1073, None, 0x8000_0000_0000_0020),
        (
            0x14d0_26f3,
            Some((13, 0x8000_0000_0000_0020)),
            0x8000_0000_0000_0020,
        ),
    ];
    let mut memory = memory(&rows.map(|r| r.0));
    let mut expected = Witness::from(&hart);
    for (_, write, compare) in rows {
        if let Some((reg, value)) = write {
            expected.x[reg] = value;
        }
        expected.compare = compare;
        expected.pc += 4;
        expected.boundaries += 1;
        expected.retired += 1;
        expected.step(&mut hart, &mut memory)?;
    }
    Ok(())
}

fn refusal(mode: PrivilegeMode, tm: u64, stce: u64) -> Result<(), String> {
    let mut hart = enabled_supervisor();
    hart.set_mode(mode);
    hart.write_csr(CSR_MCOUNTEREN, tm);
    hart.write_csr(CSR_MENVCFG, stce);
    hart.write_csr(CSR_STIMECMP, 101);
    hart.write_csr(CSR_MTVEC, HANDLER);
    hart.write_x(5, 33);
    let word = 0x14d2_9373; // CSRRW x6,stimecmp,x5: neither compare nor x6 may change.
    let mut memory = memory(&[word]);
    let handler = [
        0x3420_23f3_u32,
        0x3430_2473,
        0x3410_24f3,
        0x14d0_2573,
        0x02a0_0593,
    ];
    for (i, word) in handler.iter().enumerate() {
        memory.load_image(0x100 + i * 4, &word.to_le_bytes());
    }
    let mut expected = Witness::from(&hart);
    expected.compare = 101;
    expected.mode = PrivilegeMode::M;
    expected.pc = HANDLER;
    expected.boundaries = 1;
    expected.trap = Some((2, u64::from(word), ENTRY));
    expected.step(&mut hart, &mut memory)?;
    for (reg, value) in [
        (7, 2),
        (8, u64::from(word)),
        (9, ENTRY),
        (10, 101),
        (11, 42),
    ] {
        expected.x[reg] = value;
        expected.pc += 4;
        expected.boundaries += 1;
        expected.retired += 1;
        expected.step(&mut hart, &mut memory)?;
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn direct_timer_witnesses_hold() {
        assert_eq!(ExecutionCheck::SstcPositive.run(), Ok(()));
        assert_eq!(ExecutionCheck::SstcNegative.run(), Ok(()));
    }

    #[test]
    fn positive_rejects_unexpected_traps_even_when_the_read_value_would_be_zero() {
        for (csr, value) in [(CSR_MCOUNTEREN, 0), (CSR_MENVCFG, 0)] {
            let mut hart = enabled_supervisor();
            hart.write_csr(csr, value);
            assert!(positive(hart).unwrap_err().contains("boundary 2"));
        }
    }

    #[test]
    fn negative_rejects_a_write_that_is_allowed_instead_of_trapping() {
        assert!(refusal(PrivilegeMode::S, 2, STCE)
            .unwrap_err()
            .contains("boundary 1"));
    }
}
