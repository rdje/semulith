//! The declared virtual-time domain — `P4-SYSTEM.5` decision 1 (authority laboratory;
//! the `.3` TLB-parameter precedent: the rate is DATA, stated in the state document).
//!
//! The laboratory's time advances **one tick per step boundary, retired or halted** —
//! the Zicntr latitude ("the rate at which the cycle counter increments will depend on
//! the implementation and operating environment", §6.1) answered as a pure function of
//! the step index, so cold-reset re-execution and EVD-05's exact values hold by
//! construction (the brief's pre-condition 8). The domain IS the environment's time
//! supply (the contract wording for that supply is `P4-SYSTEM.9`'s); the domain's
//! storage is `mcycle` ("cycle count might represent a valid implementation of
//! RDTIME", §6.1), and `time` views it read-only.
//!
//! `minstret` counts GENUINELY: +1 per retired instruction — a step that delivers a
//! trap, decodes reserved (no instruction exists), or halts does not increment (the
//! `.8`-candidate unit discipline). `mcountinhibit` is excluded by the spec's own
//! equivalence (§2.1.1.12: an unimplemented register behaves as though zero), so the
//! counters always count (decision 7).

use crate::privilege::PrivilegedHart;

/// `mcycle`'s architectural address (the pinned csrs.csv's) — the domain's storage.
pub const MCYCLE_ADDRESS: u16 = 0xB00;
/// `minstret`'s architectural address — the genuine retirement count.
pub const MINSTRET_ADDRESS: u16 = 0xB02;
/// `mcounteren`'s architectural address (the counter-ACCESS gates).
pub const MCOUNTEREN_ADDRESS: u16 = 0x306;
/// `scounteren`'s architectural address (the U-mode counter-ACCESS gates).
pub const SCOUNTEREN_ADDRESS: u16 = 0x106;

/// Advance the time domain one tick at a step boundary. `retired` is exactly "an
/// instruction completed this step without a delivered trap" — the evaluator's
/// `!frame.trapped` — so a trap-delivering, reserved-decoding or halted step moves
/// time and nothing else. The domain storage wraps naturally (the counter is 64-bit).
pub fn advance<H: PrivilegedHart>(hart: &mut H, retired: bool) {
    let mcycle = hart
        .csr_index(MCYCLE_ADDRESS)
        .expect("the time domain's storage (mcycle) is declared in the state document");
    let now = hart.csr_raw(mcycle);
    hart.csr_write_raw(mcycle, now.wrapping_add(1));
    if retired {
        let instret = hart
            .csr_index(MINSTRET_ADDRESS)
            .expect("minstret is declared in the state document");
        let n = hart.csr_raw(instret);
        hart.csr_write_raw(instret, n.wrapping_add(1));
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::privilege::{self, PrivilegeMode};
    use crate::state_rv64gc::{ArchitecturalState, CSR_STIMECMP};

    fn hart() -> ArchitecturalState {
        ArchitecturalState::zeroed_at(0x8000_0000)
    }

    fn mcycle(h: &ArchitecturalState) -> u64 {
        privilege::csr_state(h, "mcycle")
    }
    fn minstret(h: &ArchitecturalState) -> u64 {
        privilege::csr_state(h, "minstret")
    }

    #[test]
    fn the_domain_advances_one_tick_per_step_boundary() {
        let mut h = hart();
        assert_eq!(mcycle(&h), 0, "cold at reset");
        advance(&mut h, true);
        advance(&mut h, true);
        advance(&mut h, true);
        assert_eq!(mcycle(&h), 3, "one tick per boundary, retired or halted");
    }

    #[test]
    fn instret_counts_only_retired_steps() {
        let mut h = hart();
        advance(&mut h, true);
        advance(&mut h, false); // a trap-delivered / reserved / halted step
        advance(&mut h, false);
        assert_eq!(minstret(&h), 1, "a faulting or halted step retires nothing");
        assert_eq!(mcycle(&h), 3, "time moved on every boundary anyway");
    }

    #[test]
    fn cycle_and_time_read_the_one_domain() {
        let mut h = hart();
        advance(&mut h, true);
        advance(&mut h, true);
        assert_eq!(privilege::csr_state(&h, "cycle"), 2, "the read-only shadow");
        assert_eq!(
            privilege::csr_state(&h, "time"),
            2,
            "a valid RDTIME (Zicntr §6.1)"
        );
        // and through the ARCHITECTURAL read path (the permission model, M-mode open)
        assert_eq!(
            privilege::csr_read(&h, 0xC00).unwrap(),
            2,
            "rdcycle's address"
        );
        assert_eq!(
            privilege::csr_read(&h, 0xC01).unwrap(),
            2,
            "rdtime's address"
        );
    }

    #[test]
    fn the_ticking_stip_reflects_time_against_stimecmp() {
        let mut h = hart();
        // the reset quirk, live: time 0 >= stimecmp 0, so STIP computes 1 at reset
        assert_eq!(
            privilege::csr_state(&h, "mip") & (1 << 5),
            1 << 5,
            "STIP at reset"
        );
        h.write_csr(CSR_STIMECMP, 3);
        assert_eq!(
            privilege::csr_state(&h, "mip") & (1 << 5),
            0,
            "cleared above time"
        );
        advance(&mut h, true);
        advance(&mut h, true);
        assert_eq!(
            privilege::csr_state(&h, "mip") & (1 << 5),
            0,
            "2 < 3 still clear"
        );
        advance(&mut h, false);
        assert_eq!(
            privilege::csr_state(&h, "mip") & (1 << 5),
            1 << 5,
            "the third tick reaches stimecmp — the timer's arrival is time's, no MMIO"
        );
    }

    #[test]
    fn cold_reset_determinism() {
        let drive = || {
            let mut h = hart();
            for retired in [true, false, true, true, false, true] {
                advance(&mut h, retired);
            }
            (mcycle(&h), minstret(&h), privilege::csr_state(&h, "time"))
        };
        assert_eq!(
            drive(),
            drive(),
            "the domain is a pure function of the step index"
        );
    }

    #[test]
    fn m_mode_writes_to_the_domain_survive_the_tick() {
        let mut h = hart();
        // mcycle is writable in M: software's write is the new base, the tick adds on top
        let idx = h.csr_index(MCYCLE_ADDRESS).unwrap();
        h.write_csr(idx, 41);
        advance(&mut h, true);
        assert_eq!(mcycle(&h), 42);
    }

    #[test]
    fn counter_gating_is_untouched_by_the_tick() {
        // the mcounteren/scounteren gates are on ACCESS, never on counting (§2.1.1.11):
        // gated-off still counts, and a U-mode read under open gates sees the tick
        let mut h = hart();
        h.set_mode(PrivilegeMode::U);
        advance(&mut h, true);
        assert!(
            privilege::csr_read(&h, 0xC00).is_err(),
            "gated off by mcounteren below M"
        );
        assert_eq!(
            mcycle(&h),
            1,
            "the gate is on access — the counter counted anyway"
        );
        let idx = h.csr_index(MCOUNTEREN_ADDRESS).unwrap();
        h.write_csr(idx, 0x7);
        let idx = h.csr_index(SCOUNTEREN_ADDRESS).unwrap();
        h.write_csr(idx, 0x7);
        assert_eq!(
            privilege::csr_read(&h, 0xC00).unwrap(),
            1,
            "gated-open U sees the tick"
        );
    }
}
