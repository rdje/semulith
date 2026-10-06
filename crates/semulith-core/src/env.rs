//! The environment request/response contract — the boundary the CPU crosses and the
//! laboratory implements (`docs/ARCHITECTURE.md` §4: "describes boundary, does not
//! implement board devices").
//!
//! Scope: the `rv64i-lab-env-v0` dispositions (`profiles/rv64i-lab-v0/ENVIRONMENT.md`
//! §"The boundary inventory") — fetch supply, data access, reset, code visibility — plus,
//! for the rv64gc composition, the page-table walk's own read kind ([`Request::WalkAccess`];
//! `rv64gc-lab-env-v1`'s `OB-GC-ENV-TRANSLATION-INPUTS`). No device, no asynchronous event
//! and no external time source exists to model: the time supply is the hart's own virtual
//! domain (`OB-GC-ENV-VIRTUAL-TIME`), and v1 supplies no interrupt source and no reservation
//! invalidation (`OB-GC-ENV-INTERRUPT-SOURCES`, `OB-GC-ENV-RESERVATION-EVENTS`) — the
//! platform declares none, and an absence has to be a platform property to be real.
//!
//! The contract pins, as types rather than prose:
//!
//! - **Widths** (`AccessWidth`): loads/stores of 8/16/32/64 bits, fetch of 32 — the width
//!   set of OB-ENV-ACCESS-WIDTHS. Any other width is unrepresentable, which is stronger
//!   than reporting it: a request the contract does not offer cannot be formed.
//! - **Addresses**: bare `u64` byte addresses (OB-ENV-ADDRESS-UNITS). SEM-05: no host
//!   pointer ever stands in for a guest address; the space is one 64-bit byte space
//!   (OB-ADDRESS-SPACE) and address computations wrap modulo 2^64 before they arrive here.
//! - **Failure responses** (`Failure`): the two environment answers that are target-facing
//!   rules — `AccessFault` outside a declared region (OB-ADDRESS-SPACE), `Misaligned` per
//!   OB-MISALIGN-DATA. These are legitimate environment answers, never model errors; the
//!   instruction layer converts them into typed target outcomes (`P1-LAB.5`).
//! - **Contract violations** (`ContractViolation`): the environment broke a rule — a
//!   different family from `Failure` (SEM-01's separation, boundary-local until `.5`
//!   integrates it into the typed outcome families).
//!
//! Little-endian throughout (REQ-D-ENDIAN, an execution-environment choice this profile
//! pins).

/// Access widths the contract offers: loads/stores of 8, 16, 32, 64 bits (`B`/`H`/`W`/`D`,
/// the load/store mnemonics' suffixes). OB-ENV-ACCESS-WIDTHS. Fetch is always 32 bits and
/// says so by construction — it is its own request variant, width not carried.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum AccessWidth {
    /// 8 bits — `LB`/`LBU`/`SB`.
    B,
    /// 16 bits — `LH`/`LHU`/`SH`.
    H,
    /// 32 bits — `LW`/`LWU`/`SW`, and the fetch width.
    W,
    /// 64 bits — `LD`/`SD`.
    D,
}

impl AccessWidth {
    /// Width in bits.
    #[must_use]
    pub const fn bits(self) -> u32 {
        match self {
            Self::B => 8,
            Self::H => 16,
            Self::W => 32,
            Self::D => 64,
        }
    }

    /// Width in bytes — the alignment granularity and the region-membership unit.
    #[must_use]
    pub const fn bytes(self) -> u64 {
        (self.bits() / 8) as u64
    }
}

/// A request the CPU makes of its environment. One entry point keeps the fixture story
/// honest: every crossing of the boundary is a value that can be scripted, counted and
/// replayed.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Request {
    /// The implicit instruction read: 32 bits at `addr` (OB-ENV-FETCH-SUPPLY — exactly
    /// 32 bits, never more, never fewer; the harness performs no fetch the model did not
    /// request and no fetch has a side effect).
    Fetch {
        /// Address of the instruction unit; must be 4-byte aligned.
        addr: u64,
    },
    /// An explicit read of `width` bits at `addr`.
    Load {
        /// Width of the access.
        width: AccessWidth,
        /// Byte address; must be aligned to `width`.
        addr: u64,
    },
    /// An explicit write of the low `width` bits of `data` at `addr`.
    Store {
        /// Width of the access.
        width: AccessWidth,
        /// Byte address; must be aligned to `width`.
        addr: u64,
        /// Value; the access writes `data & (2^width - 1)`, little-endian.
        data: u64,
    },
    /// An implicit page-table-WALK access: the translation machinery's own 8-byte
    /// read of a page-table entry at a PHYSICAL `addr` (P4-SYSTEM.3 decision 6 — the
    /// D-FETCH-IMPLICIT precedent applied: an implicit access is observable as its own
    /// request kind, never silently as a data `Load`). Read-only by construction:
    /// the profile implements Svade, so a walk never writes a PTE, and a walk write
    /// would be a description defect, not a boundary shape. The formal contract
    /// wording of this vocabulary is `rv64gc-lab-env-v1`'s
    /// `OB-GC-ENV-TRANSLATION-INPUTS` (P4-SYSTEM.9 — versioned, not edited).
    WalkAccess {
        /// Physical address of the PTE; must be 8-byte aligned.
        addr: u64,
    },
}

/// The environment's success answer to a [`Request`].
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Response {
    /// The fetched instruction word.
    Fetch(u32),
    /// The read value: exactly `width` raw bits, little-endian assembled, **not**
    /// extended — sign/zero extension into XLEN is the instruction layer's rule
    /// (REQ-D-LOAD-EXT), not the boundary's.
    Load(u64),
    /// The store completed.
    StoreDone,
    /// The page-table entry a walk access read: exactly 64 raw bits, little-endian.
    WalkAccess(u64),
}

/// Target-facing failure responses — legitimate environment answers under named target
/// rules, which the instruction layer (`P1-LAB.5`/`.8`) converts into typed target
/// outcomes. Never model errors (SEM-01).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Failure {
    /// The access touches no declared region (OB-ADDRESS-SPACE). Every declared region is
    /// main memory (OB-MAIN-VS-IO), so access-fault is never substituted for a
    /// side-effecting region's behavior.
    AccessFault,
    /// The access is not aligned to its width (OB-MISALIGN-DATA — raised, not handled
    /// invisibly, in this profile).
    Misaligned,
}

/// The environment broke the contract. Distinct from [`Failure`] in kind, not just name:
/// a `Failure` answers the CPU under a target rule; a `ContractViolation` reports the
/// environment (or a fixture standing in for it) to the harness. `P1-LAB.5` re-homes this
/// into the typed outcome families; until then it is the boundary's own error family.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum ContractViolation {
    /// A scripted environment was asked something its script does not say: the scripted
    /// request and the request that arrived differ. `scripted` is what the fixture was
    /// told to expect, `arrived` is what crossed the boundary.
    ResponseMismatch {
        /// The request the script pairs with its next response.
        scripted: Request,
        /// The request that actually arrived.
        arrived: Request,
    },
    /// A request arrived after the script ended — the fixture has no declared answer and
    /// must not invent one.
    ScriptExhausted,
}

/// Everything a boundary crossing can return: the target-facing failures and the
/// contract violations, kept apart by construction.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum BoundaryError {
    /// A legitimate, target-facing environment failure.
    Target(Failure),
    /// The environment violated the contract.
    Violation(ContractViolation),
}

impl From<Failure> for BoundaryError {
    fn from(failure: Failure) -> Self {
        Self::Target(failure)
    }
}

impl From<ContractViolation> for BoundaryError {
    fn from(violation: ContractViolation) -> Self {
        Self::Violation(violation)
    }
}

/// The environment boundary a CPU executes against. The laboratory (`semulith-verify`)
/// implements this for tests; a board would implement it after the CPU gate (SCP-03).
/// Implementors answer every request; they never initiate one — the CPU drives.
pub trait Environment {
    /// Cross the boundary once.
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError>;
}

#[cfg(test)]
mod tests;
