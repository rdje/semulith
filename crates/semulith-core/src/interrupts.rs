//! Pending evaluation and interrupt-caused delivery — `P4-SYSTEM.5` decision 3.
//!
//! Evaluated at the HEAD of every step (the Sail `dispatchInterrupt`-at-head
//! precedent): per-step evaluation satisfies the spec's "bounded amount of time" and
//! covers the xRET/CSR-write immediacy by construction. The taken-rule is the spec's
//! own (RVP-MACHINE §2.1.1.9, RVP-SUPERVISOR §11.1.1.3):
//!
//! - for M: (a) the hart is in M with mstatus.MIE set OR in a lower mode, (b) the
//!   cause's bit is set in mip AND mie, (c) the bit is NOT in mideleg;
//! - for S (a delegated cause): (a) the hart is in S with sstatus.SIE set OR in U,
//!   (b) the bit set in sip AND sie, (c) the bit IS in mideleg;
//! - the global rule: a higher-privilege interrupt is always enabled (a
//!   lower-privilege hart takes it regardless of the global enables), a
//!   lower-privilege one never fires in a higher mode;
//! - the delegation mask: a delegated interrupt is masked AT THE DELEGATOR — an STI
//!   delegated via mideleg[5] is taken in S/U only, never in M;
//! - the fixed priorities (M: MEI MSI MTI SEI SSI STI; S: SEI SSI STI) — the M-source
//!   bits (MSIP/MTIP/MEIP) stay read-only 0 by declaration (decision 5), so the
//!   eligible set reduces to SSIP/STIP/SEIP and the single ordered walk covers both.
//!
//! The pending state read goes through `csr_state`, so mip's STIP arrives COMPUTED
//! (time ≥ stimecmp — slice (a) made time move; the STIP-at-reset quirk is live).
//! sip/sie expose the same bit positions as mip/mie for the three causes, so the
//! views' own gating needs no separate read (the S-subset fields coincide at 1/5/9).

use crate::privilege::{self, PrivilegeMode, PrivilegedHart};

/// The supervisor software-interrupt cause (SSIP's bit).
pub const SSI: u64 = 1;
/// The supervisor timer-interrupt cause (STIP's bit).
pub const STI: u64 = 5;
/// The supervisor external-interrupt cause (SEIP's bit).
pub const SEI: u64 = 9;
/// The machine-side cause positions (read-only 0 in this platform — the order walks
/// them so a future M-source lands in the right priority slot, never smuggled).
pub const MSI: u64 = 3;
/// The machine timer-interrupt cause (read-only 0 here).
pub const MTI: u64 = 7;
/// The machine external-interrupt cause (read-only 0 here).
pub const MEI: u64 = 11;

/// The fixed priority order (RVP-MACHINE §2.1.1.9): MEI MSI MTI SEI SSI STI. The
/// S-form (SEI SSI STI) is a subsequence, so the one walk serves both levels.
const PRIORITY: [u64; 6] = [MEI, MSI, MTI, SEI, SSI, STI];

/// One eligible interrupt: its cause and the level it must be delivered at.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Pending {
    /// The architectural cause code (SSIP=1, STIP=5, SEIP=9; the M causes read 0).
    pub cause: u64,
    /// Deliver to S (the cause is delegated via mideleg) rather than to M.
    pub to_s: bool,
}

/// The (a)(b)(c) taken-rule with the global rule, the delegation mask and the fixed
/// priorities: the highest-priority cause that must fire NOW, if any.
pub fn pending<H: PrivilegedHart>(hart: &H) -> Option<Pending> {
    let mode = hart.mode();
    let mstatus = privilege::csr_state(hart, "mstatus");
    let mie = privilege::csr_state(hart, "mie");
    let mip = privilege::csr_state(hart, "mip"); // STIP computed live (time ≥ stimecmp)
    let mideleg = privilege::csr_state(hart, "mideleg");
    for cause in PRIORITY {
        let bit = 1u64 << cause;
        if mip & bit == 0 || mie & bit == 0 {
            continue; // not pending, or pending with the enable clear (b)
        }
        if mideleg & bit != 0 {
            // delegated: masked at the delegator — S/U only; (a) S with SIE or U
            if mode == PrivilegeMode::M {
                continue;
            }
            if mode == PrivilegeMode::S && (mstatus >> 1) & 1 == 0 {
                continue; // sstatus.SIE clear in S
            }
            return Some(Pending { cause, to_s: true });
        }
        // not delegated: M's rule — (a) M with MIE or any lower mode
        if mode == PrivilegeMode::M && (mstatus >> 3) & 1 == 0 {
            continue; // mstatus.MIE clear in M
        }
        return Some(Pending { cause, to_s: false });
    }
    None
}

/// The WFI wake evaluation (RVP-MACHINE §2.1.3.3 — `P4-SYSTEM.5` decision 4): resume
/// on a LOCALLY-enabled pending interrupt at any privilege level, regardless of the
/// global enables and of mideleg — the section's own musts: "the hart must resume if a
/// locally enabled interrupt becomes pending, even if it has been delegated to a
/// less-privileged mode" and "WFI is also required to resume execution for locally
/// enabled interrupts pending at any privilege level, regardless of the global
/// interrupt enable at each privilege level"; the same sentence's should is honored
/// ("should honor the individual interrupt enables"), so the condition is exactly
/// `mip & mie != 0` — mip read through `csr_state`, so STIP arrives COMPUTED (the
/// timer's arrival during the halt is the acceptance's wake source).
pub fn wake_pending<H: PrivilegedHart>(hart: &H) -> bool {
    let mip = privilege::csr_state(hart, "mip");
    let mie = privilege::csr_state(hart, "mie");
    mip & mie != 0
}

/// Deliver an interrupt (decision 3): mcause/scause carries the Interrupt bit (63)
/// with the cause code; mepc/sepc ← the NEXT instruction's pc (interrupts are taken
/// BETWEEN instructions — the caller's pc at the step head); the xPIE/xIE/xPP stack;
/// and pc ← the vector HONORING its declared MODE (synchronous delivery keeps BASE;
/// interrupt delivery computes BASE + 4×cause when MODE=Vectored — delivering
/// MODE=1 as BASE would be a description lie). xtval is UNSPECIFIED for interrupts;
/// the laboratory declares 0 (the `.2` ecall convention, recorded). Returns the
/// delivery address.
pub fn deliver<H: PrivilegedHart>(hart: &mut H, pend: Pending, next_pc: u64) -> u64 {
    let origin = hart.mode();
    let cause = pend.cause | (1u64 << 63);
    let (epc, cause_r, tval_r, vec) = if pend.to_s {
        (0x141, 0x142, 0x143, 0x105) // sepc, scause, stval, stvec
    } else {
        (0x341, 0x342, 0x343, 0x305) // mepc, mcause, mtval, mtvec
    };
    for (address, value) in [(epc, next_pc), (cause_r, cause), (tval_r, 0)] {
        let index = hart
            .csr_index(address)
            .expect("the x-cause registers are declared in the state document");
        hart.csr_write_raw(index, value);
    }
    // the xPIE/xIE/xPP stack (the machine's own writes, archited never gated) — the
    // same update the synchronous path composes, from the originating mode
    let mut mstatus = privilege::csr_state(hart, "mstatus");
    if pend.to_s {
        let sie = (mstatus >> 1) & 1;
        mstatus = (mstatus & !(1 << 5)) | (sie << 5); // SPIE <- SIE
        mstatus &= !(1 << 1); // SIE <- 0
        mstatus = (mstatus & !(1 << 8)) | (u64::from(origin == PrivilegeMode::S) << 8);
    // SPP
    } else {
        let mie = (mstatus >> 3) & 1;
        mstatus = (mstatus & !(1 << 7)) | (mie << 7); // MPIE <- MIE
        mstatus &= !(1 << 3); // MIE <- 0
        mstatus = (mstatus & !(0b11 << 11)) | (origin.code() << 11); // MPP <- origin
    }
    let index = hart
        .csr_index(0x300)
        .expect("mstatus is declared in the state document");
    hart.csr_write_raw(index, mstatus);
    hart.set_mode(if pend.to_s {
        PrivilegeMode::S
    } else {
        PrivilegeMode::M
    });
    // the vector, MODE honored: BASE for Direct, BASE + 4×cause for Vectored
    let index = hart
        .csr_index(vec)
        .expect("the vector register is declared in the state document");
    let vector = hart.csr_raw(index);
    let base = vector & !0b11;
    if vector & 0b11 == 1 {
        base.wrapping_add(4 * pend.cause)
    } else {
        base
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::state_rv64gc::{
        ArchitecturalState, CSR_MIDELEG, CSR_MIE, CSR_MIP, CSR_MSTATUS, CSR_MTVEC, CSR_STIMECMP,
        CSR_STVEC,
    };

    fn hart() -> ArchitecturalState {
        ArchitecturalState::zeroed_at(0x8000_0000)
    }

    fn set(h: &mut ArchitecturalState, idx: usize, v: u64) {
        h.write_csr(idx, v);
    }

    #[test]
    fn nothing_is_eligible_from_reset() {
        let h = hart();
        assert_eq!(pending(&h), None, "every enable is 0 at reset");
    }

    #[test]
    fn the_taken_rule_for_m() {
        let mut h = hart();
        set(&mut h, CSR_MIP, 1 << 1); // SSIP
        assert_eq!(
            pending(&h),
            None,
            "pending with the enable clear is not taken"
        );
        set(&mut h, CSR_MIE, 1 << 1); // SSIE
        assert_eq!(
            pending(&h),
            None,
            "in M with MIE clear it is still not taken"
        );
        set(&mut h, CSR_MSTATUS, 1 << 3); // MIE
        assert_eq!(
            pending(&h),
            Some(Pending {
                cause: SSI,
                to_s: false
            }),
            "in M with MIE set, (a)(b)(c) all hold"
        );
    }

    #[test]
    fn the_fixed_priority_walks_mei_down() {
        let mut h = hart();
        set(&mut h, CSR_MIP, (1 << 1) | (1 << 5) | (1 << 9));
        set(&mut h, CSR_MIE, (1 << 1) | (1 << 5) | (1 << 9));
        set(&mut h, CSR_MSTATUS, 1 << 3); // MIE
        assert_eq!(
            pending(&h).map(|p| p.cause),
            Some(SEI),
            "SEI outranks SSI and STI among simultaneous pending"
        );
        set(&mut h, CSR_MIP, 1 << 1);
        assert_eq!(pending(&h).map(|p| p.cause), Some(SSI), "then SSI");
        set(&mut h, CSR_MIP, 1 << 5);
        assert_eq!(pending(&h).map(|p| p.cause), Some(STI), "then STI");
    }

    #[test]
    fn delegation_masks_at_the_delegator() {
        let mut h = hart();
        set(&mut h, CSR_MIP, 1 << 1);
        set(&mut h, CSR_MIE, 1 << 1);
        set(&mut h, CSR_MSTATUS, 1 << 3);
        set(&mut h, CSR_MIDELEG, 1 << 1);
        assert_eq!(pending(&h), None, "a delegated SSI is never taken in M");
        h.set_mode(PrivilegeMode::S);
        assert_eq!(pending(&h), None, "S with SIE clear does not take it");
        set(&mut h, CSR_MSTATUS, 1 << 1);
        assert_eq!(
            pending(&h),
            Some(Pending {
                cause: SSI,
                to_s: true
            }),
            "S with SIE takes the delegated SSI"
        );
        h.set_mode(PrivilegeMode::U);
        assert_eq!(
            pending(&h).map(|p| p.to_s),
            Some(true),
            "U takes it regardless of SIE (the global rule)"
        );
    }

    #[test]
    fn the_global_rule() {
        let mut h = hart();
        set(&mut h, CSR_MIP, 1 << 9);
        set(&mut h, CSR_MIE, 1 << 9);
        // MIE clear in M — a lower mode still takes it; M does not
        assert_eq!(pending(&h), None, "M with MIE clear passes it by");
        h.set_mode(PrivilegeMode::U);
        assert_eq!(
            pending(&h).map(|p| p.cause),
            Some(SEI),
            "U takes an M-level interrupt regardless of MIE"
        );
    }

    #[test]
    fn delivery_writes_the_interrupt_shape() {
        let mut h = hart();
        set(&mut h, CSR_MTVEC, 0x8000_0300);
        let pc = deliver(
            &mut h,
            Pending {
                cause: SSI,
                to_s: false,
            },
            0x8000_0040,
        );
        assert_eq!(pc, 0x8000_0300, "direct delivery uses BASE");
        assert_eq!(h.mode(), PrivilegeMode::M);
        assert_eq!(privilege::csr_state(&h, "mcause"), (1 << 63) | SSI);
        assert_eq!(
            privilege::csr_state(&h, "mepc"),
            0x8000_0040,
            "the NEXT instruction"
        );
        assert_eq!(
            privilege::csr_state(&h, "mtval"),
            0,
            "UNSPECIFIED declared 0"
        );
    }

    #[test]
    fn vectored_delivery_computes_base_plus_four_times_cause() {
        let mut h = hart();
        set(&mut h, CSR_MTVEC, 0x8000_0301); // MODE = Vectored
        set(&mut h, CSR_STVEC, 0x8000_0401);
        let pc = deliver(
            &mut h,
            Pending {
                cause: SEI,
                to_s: false,
            },
            0x8000_0040,
        );
        assert_eq!(pc, 0x8000_0300 + 4 * SEI, "vectored: BASE + 4×cause");
        let pc = deliver(
            &mut h,
            Pending {
                cause: SSI,
                to_s: true,
            },
            0x8000_0044,
        );
        assert_eq!(pc, 0x8000_0400 + 4 * SSI, "and stvec's own MODE");
        assert_eq!(privilege::csr_state(&h, "scause"), (1 << 63) | SSI);
        assert_eq!(privilege::csr_state(&h, "sepc"), 0x8000_0044);
    }

    #[test]
    fn the_stack_pushes_for_nesting() {
        let mut h = hart();
        set(&mut h, CSR_MTVEC, 0x8000_0300);
        set(&mut h, CSR_MSTATUS, 1 << 3); // MIE set in M
        deliver(
            &mut h,
            Pending {
                cause: SSI,
                to_s: false,
            },
            0x8000_0040,
        );
        let mstatus = privilege::csr_state(&h, "mstatus");
        assert_eq!(
            (mstatus >> 7) & 1,
            1,
            "MPIE <- the old MIE (resume can re-fire)"
        );
        assert_eq!((mstatus >> 3) & 1, 0, "MIE <- 0 (the handler is quiet)");
        assert_eq!((mstatus >> 11) & 0b11, 3, "MPP <- M");
    }

    #[test]
    fn the_wake_ignores_the_global_enables_and_mideleg() {
        let mut h = hart();
        set(&mut h, CSR_MIP, 1 << 1); // SSIP
        assert!(
            !wake_pending(&h),
            "pending without the individual enable does not wake (the should)"
        );
        set(&mut h, CSR_MIE, 1 << 1); // SSIE
        assert!(
            wake_pending(&h),
            "locally-enabled pending wakes with MIE clear (the must)"
        );
        set(&mut h, CSR_MIDELEG, 1 << 1);
        assert!(
            wake_pending(&h),
            "… and even delegated to a less-privileged mode"
        );
        h.set_mode(PrivilegeMode::S);
        assert!(wake_pending(&h), "at any privilege level, SIE clear too");
    }

    #[test]
    fn the_timers_arrival_wakes_through_the_domain() {
        let mut h = hart();
        h.write_csr(CSR_STIMECMP, 2);
        set(&mut h, CSR_MIE, 1 << 5); // STIE
        assert!(!wake_pending(&h), "time 0 < 2: the timer has not arrived");
        crate::timekeeping::advance(&mut h, false);
        assert!(!wake_pending(&h), "time 1 < 2 still");
        crate::timekeeping::advance(&mut h, false);
        assert!(
            wake_pending(&h),
            "time reaches stimecmp — STIP computes 1 and the hart must resume"
        );
    }
}
