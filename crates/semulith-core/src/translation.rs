//! Translation — `P4-SYSTEM.3` (Sv39): the effective-mode computation and the
//! translation entry point the engine's three access hooks call
//! (`exec_rv64gc.rs`'s fetch, load and store sites). The module is the
//! [`crate::privilege`] pattern applied to the walk: machinery over the generated
//! tables and the privilege state, never per-instruction.
//!
//! The slice's shape (the design brief's decisions 3–6):
//!
//! - **Effective mode is a single computation** (RVP-MACHINE §2.1.1.6.4): a FETCH
//!   uses the hart's current mode — and an M-mode fetch is NEVER translated — while
//!   loads and stores use `mstatus.MPP` when `mstatus.MPRV` is 1, with SUM/MXR read
//!   per the effective mode (the `.2` deferral landing; SUM/MXR themselves are the
//!   walk's permission inputs, carried here so slice (c) reads them from one place).
//! - **satp.MODE dispatch**: Bare (0) is an EXACT identity path — the address is
//!   physical as-is, and the 62-guest corpus is the standing proof that nothing
//!   observable changes on it. Sv39 (8) enters [`Translate::Walk`] — the 10-step
//!   walk is slice (c)'s; this slice is the machinery shell, and the hooks report
//!   the walk entry as the named unimplemented case it is, never as a wrong answer.
//! - **Fetch in 16-bit parcels** (decision 5): each parcel's address translates
//!   independently, forward-compatible with the C slot (`DIFF-FETCH-GRANULARITY` —
//!   Sail's two-16-bit-fetch granularity is the measured reference precedent). The
//!   recorded coalescing choice: when both parcels' TRANSLATED addresses lie in one
//!   physical 32-bit unit, the fetch issues exactly one `Request::Fetch` — under
//!   Bare that is every case, so the Bare request shape is byte-exact (measured:
//!   the corpus's one-fetch-per-step census is unchanged). The page-straddling
//!   case (parcels mapping non-contiguously) fetches each parcel's own unit —
//!   slice (c)'s, named here as its own case rather than silently coalesced.
//! - **The page-fault causes enter core as raw u64** (12/13/15, RVP-SUPERVISOR's
//!   cause table): the typed-enum asymmetry is a stated choice — the base
//!   profile's `outcome.rs` enumerates rv64i's cause vocabulary because rv64i's
//!   laboratory REPORTS typed outcomes to the harness; the privileged engine's
//!   causes are delivered as raw u64 through the one `trap-deliver` path by
//!   construction, so a new typed enum would buy a second vocabulary for one
//!   consumer.
//! - **Walk accesses cross the boundary as their own kind**
//!   (`Request::WalkAccess`, decision 6) — the D-FETCH-IMPLICIT precedent applied:
//!   an implicit access is observable as its own request, never silently as a data
//!   `Load`. The kind is read-only by construction: the profile implements Svade,
//!   so a walk never writes a PTE. The formal contract wording of the vocabulary
//!   is P4-SYSTEM.9's charter ("translation inputs", versioned not edited) —
//!   routed and recorded in the tree.

use crate::privilege::{self, PrivilegeMode, PrivilegedHart};

/// The page-fault causes (RVP-SUPERVISOR §11.1.5's cause table), entering the core
/// vocabulary as raw u64 — the asymmetry with the base profile's typed enum is the
/// stated choice documented in the module header.
pub const INSTRUCTION_PAGE_FAULT: u64 = 12;
/// The load page-fault cause.
pub const LOAD_PAGE_FAULT: u64 = 13;
/// The store/AMO page-fault cause.
pub const STORE_PAGE_FAULT: u64 = 15;

// mstatus field positions (the pinned encoding.h's masks — MSTATUS_MPP/MPRV/SUM/MXR),
// and satp's MODE field (RVP-SUPERVISOR §11.1.1.11).
const MPP_LO: u8 = 11;
const MPRV: u8 = 17;
const SUM: u8 = 18;
const MXR: u8 = 19;
const SATP_MODE_LO: u8 = 60;

/// The three access kinds the hooks translate.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum AccessKind {
    /// The implicit instruction fetch.
    Fetch,
    /// An explicit load.
    Load,
    /// An explicit store.
    Store,
}

/// The mode an access is judged under, with the walk's permission inputs read per
/// that mode (RVP-MACHINE §2.1.1.6.4 + §2.1.1.6.3's SUM/MXR rules).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct EffectiveMode {
    /// The mode the access's permissions are judged under.
    pub mode: PrivilegeMode,
    /// `mstatus.SUM` — permit S-mode loads/stores of U-accessible pages.
    pub sum: bool,
    /// `mstatus.MXR` — make executable pages readable by loads.
    pub mxr: bool,
}

/// Compute the effective mode for an access (RVP-MACHINE §2.1.1.6.4): a fetch uses
/// the hart's current mode; loads and stores use `mstatus.MPP` when `mstatus.MPRV`
/// is 1. SUM/MXR are read from mstatus regardless of the effective mode — their
/// effect is defined against it, and slice (c)'s walk reads them from here.
pub fn effective_mode<H: PrivilegedHart>(hart: &H, kind: AccessKind) -> EffectiveMode {
    let mstatus = privilege::csr_state(hart, "mstatus");
    let mode = match kind {
        AccessKind::Fetch => hart.mode(),
        AccessKind::Load | AccessKind::Store => {
            if (mstatus >> MPRV) & 1 == 1 {
                match (mstatus >> MPP_LO) & 0b11 {
                    0 => PrivilegeMode::U,
                    1 => PrivilegeMode::S,
                    _ => PrivilegeMode::M,
                }
            } else {
                hart.mode()
            }
        }
    };
    EffectiveMode {
        mode,
        sum: (mstatus >> SUM) & 1 == 1,
        mxr: (mstatus >> MXR) & 1 == 1,
    }
}

/// The translation's answer for one access address.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Translate {
    /// Bare, or an M-effective access: the address is physical as-is.
    Identity(u64),
    /// satp.MODE selects Sv39 for a sub-M effective mode: the walk entry — slice
    /// (c) fills the 10-step walk; the hooks name it as their unimplemented case
    /// until then, never a wrong answer.
    Walk {
        /// The virtual address to translate.
        va: u64,
        /// What the access is for.
        kind: AccessKind,
        /// The mode the access is judged under, with the walk's permission inputs.
        effective: EffectiveMode,
    },
    /// The translation itself faults: a page-fault cause (12/13/15) and the
    /// faulting address — delivery is the caller's, through the one trap path.
    PageFault {
        /// The cause to deliver.
        cause: u64,
        /// The address the fault is reported on.
        tval: u64,
    },
}

/// The page-fault cause for an access kind (the cause table's instruction/load/
/// store split).
pub fn page_fault_cause(kind: AccessKind) -> u64 {
    match kind {
        AccessKind::Fetch => INSTRUCTION_PAGE_FAULT,
        AccessKind::Load => LOAD_PAGE_FAULT,
        AccessKind::Store => STORE_PAGE_FAULT,
    }
}

/// The two 16-bit parcels of the instruction unit at `pc` (decision 5): with C in
/// the profile the unit may straddle a 4 KiB boundary, and each parcel translates
/// independently.
pub fn fetch_parcels(pc: u64) -> [u64; 2] {
    [pc, pc.wrapping_add(2)]
}

/// Translate one access address. The dispatch: an M-effective access is never
/// translated (RVP-MACHINE §2.1.1.6.4 and the bare-M rule of §11.1.2); satp.MODE 0
/// (Bare) is the exact identity path; satp.MODE 8 (Sv39) enters the walk. Any
/// other MODE cannot arise through the WARL discipline (satp.MODE is `one-of 0 8`
/// in the state document) — reaching one is a description defect, named rather
/// than silently identity-mapped.
pub fn translate<H: PrivilegedHart>(hart: &H, va: u64, kind: AccessKind) -> Translate {
    let effective = effective_mode(hart, kind);
    if effective.mode == PrivilegeMode::M {
        return Translate::Identity(va);
    }
    let satp = privilege::csr_state(hart, "satp");
    match (satp >> SATP_MODE_LO) & 0xF {
        0 => Translate::Identity(va),
        8 => Translate::Walk {
            va,
            kind,
            effective,
        },
        mode => panic!(
            "satp.MODE {mode} is outside the profile's one-of {{0, 8}} vocabulary — \
             a description defect, never an identity"
        ),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::state_rv64gc::{ArchitecturalState, CSR_MSTATUS, CSR_SATP};

    const MPRV_BIT: u64 = 1 << 17;
    const SUM_BIT: u64 = 1 << 18;
    const MXR_BIT: u64 = 1 << 19;

    fn hart() -> ArchitecturalState {
        ArchitecturalState::zeroed_at(0x8000_0000)
    }

    fn set_satp_mode(state: &mut ArchitecturalState, mode: u64) {
        state.write_csr(CSR_SATP, mode << 60);
    }

    #[test]
    fn bare_is_identity_for_every_mode_and_kind() {
        let mut state = hart(); // satp.MODE = 0 (Bare) at reset
        for kind in [AccessKind::Fetch, AccessKind::Load, AccessKind::Store] {
            assert_eq!(
                translate(&state, 0xDEAD_BEEF, kind),
                Translate::Identity(0xDEAD_BEEF)
            );
        }
        state.set_mode(PrivilegeMode::S);
        state.set_mode(PrivilegeMode::U);
        assert_eq!(
            translate(&state, 0x1234, AccessKind::Load),
            Translate::Identity(0x1234)
        );
    }

    #[test]
    fn m_mode_is_never_translated_even_under_sv39() {
        let mut state = hart();
        set_satp_mode(&mut state, 8);
        // an M-mode fetch is never translated, satp notwithstanding
        assert_eq!(
            translate(&state, 0x8000_0004, AccessKind::Fetch),
            Translate::Identity(0x8000_0004)
        );
        // an M-mode load/store with MPRV=0 keeps the M effective mode: identity
        assert_eq!(
            translate(&state, 0x8000_1000, AccessKind::Load),
            Translate::Identity(0x8000_1000)
        );
        assert_eq!(
            translate(&state, 0x8000_1000, AccessKind::Store),
            Translate::Identity(0x8000_1000)
        );
    }

    #[test]
    fn sub_m_modes_enter_the_walk_under_sv39() {
        let mut state = hart();
        set_satp_mode(&mut state, 8);
        state.set_mode(PrivilegeMode::S);
        let effective = EffectiveMode {
            mode: PrivilegeMode::S,
            sum: false,
            mxr: false,
        };
        assert_eq!(
            translate(&state, 0x0000_8000_0042, AccessKind::Load),
            Translate::Walk {
                va: 0x0000_8000_0042,
                kind: AccessKind::Load,
                effective
            }
        );
        state.set_mode(PrivilegeMode::U);
        let effective_u = EffectiveMode {
            mode: PrivilegeMode::U,
            sum: false,
            mxr: false,
        };
        assert_eq!(
            translate(&state, 0x42, AccessKind::Fetch),
            Translate::Walk {
                va: 0x42,
                kind: AccessKind::Fetch,
                effective: effective_u
            }
        );
    }

    #[test]
    fn mprv_selects_mpp_for_data_accesses_only() {
        let mut state = hart();
        set_satp_mode(&mut state, 8);
        state.write_csr(CSR_MSTATUS, MPRV_BIT | (1 << 11) | SUM_BIT | MXR_BIT); // MPRV=1, MPP=S
        let effective = EffectiveMode {
            mode: PrivilegeMode::S,
            sum: true,
            mxr: true,
        };
        // loads and stores use MPP when MPRV=1 (§2.1.1.6.4) — with SUM/MXR carried
        assert_eq!(
            translate(&state, 0x1000, AccessKind::Load),
            Translate::Walk {
                va: 0x1000,
                kind: AccessKind::Load,
                effective
            }
        );
        // a fetch ignores MPRV: the current mode is M, so identity
        assert_eq!(
            translate(&state, 0x1000, AccessKind::Fetch),
            Translate::Identity(0x1000)
        );
        // MPP=U under MPRV=1
        state.write_csr(CSR_MSTATUS, MPRV_BIT);
        let effective_u = EffectiveMode {
            mode: PrivilegeMode::U,
            sum: false,
            mxr: false,
        };
        assert_eq!(
            translate(&state, 0x1000, AccessKind::Store),
            Translate::Walk {
                va: 0x1000,
                kind: AccessKind::Store,
                effective: effective_u
            }
        );
    }

    #[test]
    fn an_out_of_vocabulary_satp_mode_is_a_named_defect() {
        let mut state = hart();
        state.set_mode(PrivilegeMode::S);
        state.write_csr(CSR_SATP, 5 << 60); // raw storage write bypasses the WARL discipline
        let outcome = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
            translate(&state, 0x1000, AccessKind::Load)
        }));
        let err = outcome.expect_err("an out-of-vocabulary satp.MODE must panic, named");
        let text = err
            .downcast_ref::<String>()
            .map(String::as_str)
            .or_else(|| err.downcast_ref::<&str>().copied())
            .unwrap_or("");
        assert!(
            text.contains("satp.MODE 5"),
            "the defect names the mode: {text}"
        );
    }

    #[test]
    fn page_fault_cause_vocabulary() {
        assert_eq!(page_fault_cause(AccessKind::Fetch), 12);
        assert_eq!(page_fault_cause(AccessKind::Load), 13);
        assert_eq!(page_fault_cause(AccessKind::Store), 15);
    }
}
