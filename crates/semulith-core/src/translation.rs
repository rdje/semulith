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
//!   observable changes on it. Sv39 (8) runs the 10-step walk (`walk`, cited
//!   step-by-step: canonical-VA check, per-level PTE reads through the walk-access
//!   kind with a boundary fault reported as the ORIGINAL access's access fault,
//!   the V/reserved/RW/PBMT/N checks, superpage misalignment, non-leaf D/A/U
//!   reserved, U/SUM/MXR and R/W/X permissions, Svade's page-fault-instead-of-
//!   update, and the physical address by level).
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

use crate::env::{BoundaryError, Environment, Request, Response};
use crate::privilege::{self, PrivilegeMode, PrivilegedHart};

/// The minimal fully-specified translation lookaside buffer (P4-SYSTEM.3 decision 2):
/// the stated laboratory parameters — 4 entries, fully-associative, FIFO replacement,
/// ASID-tagged at ASIDLEN=16, keyed by 4 KiB page (a superpage's other pages re-walk
/// and install independently — conformant, and it keeps the fence's per-address case
/// exact). Authority laboratory; the state document's SEM-08 census carries the same
/// parameters as data (the `translation-cache` candidate, `present true`), and the
/// generated state module owns the storage because the census declares it.
pub const TLB_CAPACITY: usize = 4;

/// One TLB entry: a 4 KiB page's translation as the installing walk proved it,
/// including the A/D bits it had then (under Svade the hardware never updates them
/// after, and software that changes a PTE must fence — §11.1.2.1's own rule).
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub struct TlbEntry {
    /// The entry holds a translation.
    pub valid: bool,
    /// The G bit: retained across per-ASID and per-address+ASID fences (§11.1.2.1).
    pub global: bool,
    /// The ASID the translation was installed under (satp.ASID, 16 bits).
    pub asid: u16,
    /// The virtual page number (va >> 12).
    pub vpn: u64,
    /// The physical base of the 4 KiB page the entry translates `vpn` to.
    pub pa_base: u64,
    /// The leaf PTE's R bit at install.
    pub r: bool,
    /// The leaf PTE's W bit at install.
    pub w: bool,
    /// The leaf PTE's X bit at install.
    pub x: bool,
    /// The leaf PTE's U bit at install.
    pub u: bool,
    /// The leaf PTE's A bit at install (Svade's step-9 input — never updated after).
    pub a: bool,
    /// The leaf PTE's D bit at install (Svade's step-9 input — never updated after).
    pub d: bool,
    /// The leaf's level (0 = 4 KiB, 1 = 2 MiB, 2 = 1 GiB) — evidence, not a key.
    pub level: i64,
}

/// The cache itself: the entries and the FIFO cursor. A pure function of the hart's
/// own history by construction — cold-reset re-execution is trace-identical, and a
/// snapshot that restores a cold cache restores a legal state (a miss is never
/// wrong, only slower). The rv64gc path has no snapshot surface today (the CLI's
/// snapshot/resume is rv64i-scoped by refusal); that consequence is recorded here.
#[derive(Clone, Debug, Default, PartialEq, Eq)]
pub struct Tlb {
    entries: [TlbEntry; TLB_CAPACITY],
    cursor: usize,
}

impl Tlb {
    /// The cold cache (all entries invalid, cursor at 0).
    #[must_use]
    pub fn new() -> Self {
        Self::default()
    }

    /// A hit is an entry that is valid, page-matched, and either global or
    /// ASID-matched (§11.1.2.1: a hit must be for a translation valid since the last
    /// subsuming fence — the fence cases below are what makes that true).
    #[must_use]
    pub fn lookup(&self, vpn: u64, asid: u16) -> Option<TlbEntry> {
        self.entries
            .iter()
            .copied()
            .find(|e| e.valid && e.vpn == vpn && (e.global || e.asid == asid))
    }

    /// Install at the FIFO cursor (ordinary replacement may evict any entry, the
    /// global ones included — only the FENCE cases retain globals).
    pub fn install(&mut self, entry: TlbEntry) {
        self.entries[self.cursor] = entry;
        self.cursor = (self.cursor + 1) % TLB_CAPACITY;
    }

    /// SFENCE.VMA's four cases, exactly (§11.1.2.1; the over-fence latitude is
    /// recorded-not-taken). A non-canonical VA has no effect and raises nothing.
    pub fn invalidate(&mut self, va: u64, asid: u16) {
        let vpn = va >> 12;
        let top = va >> 39;
        let canonical = if (va >> 38) & 1 == 1 {
            (1u64 << 25) - 1
        } else {
            0
        };
        if top != canonical {
            return; // an invalid rs1 VA: no effect, no exception — the spec's sentence
        }
        for e in &mut self.entries {
            let subsumed = match (va == 0, asid == 0) {
                (true, true) => true,                         // all address spaces, all ASIDs
                (true, false) => !e.global && e.asid == asid, // per-ASID, globals retained
                (false, true) => e.vpn == vpn,                // per-address, every space
                (false, false) => !e.global && e.asid == asid && e.vpn == vpn,
            };
            if subsumed {
                e.valid = false;
            }
        }
    }

    /// How many entries currently hold a translation (the tests' witness).
    #[must_use]
    pub fn occupied(&self) -> usize {
        self.entries.iter().filter(|e| e.valid).count()
    }
}

/// SFENCE.VMA's effect: invalidate the hart's cache per the four cases (the legality
/// of the fence itself — U-mode, and S with TVM=1 — is the semantics data's, in
/// `system.sem.sexp`; this is the effect reaching the cache).
pub fn fence<H: PrivilegedHart>(hart: &mut H, va: u64, asid: u16) {
    hart.tlb().invalidate(va, asid);
}

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
    /// An atomic memory operation's single translation (`P4-SYSTEM.4` decision 5):
    /// judged under the store/AMO rules — the cause vocabulary is the store's
    /// (page fault 15, access fault 7, never the load's — "AMOs never raise load
    /// page-fault exceptions … attempting to perform an AMO on an unreadable page
    /// always raises a store page-fault exception", RVP-SUPERVISOR) — and the
    /// permission requirement is read AND write, because the operation does both.
    /// LR/SC translate as the plain kinds (LR a load, SC a store, RVP-MACHINE's
    /// exception table); only the read-modify-write needs the joint rule.
    Atomic,
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
        AccessKind::Load | AccessKind::Store | AccessKind::Atomic => {
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
    /// The walk translated the address (satp.MODE=Sv39): the physical address.
    Physical(u64),
    /// The translation itself page-faults: a page-fault cause (12/13/15) and the
    /// original virtual address as tval — delivery is the caller's, through the
    /// one trap path.
    PageFault {
        /// The cause to deliver.
        cause: u64,
        /// The original virtual address.
        tval: u64,
    },
    /// A walk-access read faulted at the boundary (§11.1.3.2 step 2): the ACCESS
    /// fault corresponding to the original access type (1/5/7), the original
    /// virtual address as tval — distinct from a page fault by cause, never
    /// substituted.
    AccessFault {
        /// The cause to deliver.
        cause: u64,
        /// The original virtual address.
        tval: u64,
    },
    /// The model or the environment contract failed (SEM-02).
    Failed(crate::outcome::ModelError),
}

/// The page-fault cause for an access kind (the cause table's instruction/load/
/// store split).
pub fn page_fault_cause(kind: AccessKind) -> u64 {
    match kind {
        AccessKind::Fetch => INSTRUCTION_PAGE_FAULT,
        AccessKind::Load => LOAD_PAGE_FAULT,
        AccessKind::Store | AccessKind::Atomic => STORE_PAGE_FAULT,
    }
}

/// The access-fault cause for an access kind (a walk-access read fault reports the
/// original access's fault class, §11.1.3.2 step 2).
fn access_fault_cause(kind: AccessKind) -> u64 {
    match kind {
        AccessKind::Fetch => 1,
        AccessKind::Load => 5,
        AccessKind::Store | AccessKind::Atomic => 7,
    }
}

fn page_fault(kind: AccessKind, va: u64) -> Translate {
    Translate::PageFault {
        cause: page_fault_cause(kind),
        tval: va,
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
/// (Bare) is the exact identity path; satp.MODE 8 (Sv39) consults the TLB first
/// (a hit must be for a translation valid since the last subsuming fence) and
/// walks on a miss, installing the result. Any other MODE cannot arise through
/// the WARL discipline (satp.MODE is `one-of 0 8` in the state document) —
/// reaching one is a description defect, named rather than silently
/// identity-mapped. satp itself is read per access, so MODE and ASID changes are
/// visible immediately; a root-PPN change is visible on the next MISS, and stale
/// entries may hit until a fence — §11.1.2.1's sanctioned staleness, the fence
/// being the contract (the TLB never auto-invalidates).
pub fn translate<H: PrivilegedHart>(
    hart: &mut H,
    env: &mut dyn Environment,
    va: u64,
    kind: AccessKind,
) -> Translate {
    let effective = effective_mode(hart, kind);
    if effective.mode == PrivilegeMode::M {
        return Translate::Identity(va);
    }
    let satp = privilege::csr_state(hart, "satp");
    match (satp >> SATP_MODE_LO) & 0xF {
        0 => Translate::Identity(va),
        8 => {
            // §11.1.4.1's canonical-VA check precedes the cache too (a non-canonical
            // VA faults, never hits — and was never installable, so the order is
            // only observational discipline).
            let top = va >> 39;
            let canonical = if (va >> 38) & 1 == 1 {
                (1u64 << 25) - 1
            } else {
                0
            };
            if top != canonical {
                return page_fault(kind, va);
            }
            let asid = ((satp >> 44) & 0xFFFF) as u16;
            let vpn = va >> 12;
            if let Some(entry) = hart.tlb().lookup(vpn, asid) {
                return finish(&entry, va, kind, effective);
            }
            walk(hart, env, va, kind, effective, satp, asid)
        }
        mode => panic!(
            "satp.MODE {mode} is outside the profile's one-of {{0, 8}} vocabulary — \
             a description defect, never an identity"
        ),
    }
}

/// The leaf's judgment, shared by the walk's step 8–10 and a TLB hit: the
/// permission check with the CURRENT effective mode and SUM/MXR (never cached),
/// Svade's step 9 from the entry's stored A/D bits (the walk never uses the cache
/// for a hardware A/D update because under Svade there is none — a needed update
/// is the fault path, and a faulting access installs nothing), and the physical
/// address from the 4 KiB page base.
fn finish(entry: &TlbEntry, va: u64, kind: AccessKind, effective: EffectiveMode) -> Translate {
    match effective.mode {
        PrivilegeMode::U => {
            if !entry.u {
                return page_fault(kind, va);
            }
        }
        PrivilegeMode::S => {
            if entry.u
                && (kind == AccessKind::Fetch || (kind != AccessKind::Fetch && !effective.sum))
            {
                return page_fault(kind, va);
            }
        }
        PrivilegeMode::M => unreachable!("the M-effective case is identity above"),
    }
    match kind {
        AccessKind::Fetch if !entry.x => return page_fault(kind, va),
        AccessKind::Load if !(entry.r || effective.mxr && entry.x) => {
            return page_fault(kind, va);
        }
        AccessKind::Store if !entry.w => return page_fault(kind, va),
        // the AMO rule (RVP-SUPERVISOR): read AND write permission, one fault, and it
        // is the store/AMO cause — never a load page fault (decision 5)
        AccessKind::Atomic if !(entry.r && entry.w) => return page_fault(kind, va),
        _ => {}
    }
    if !entry.a || (matches!(kind, AccessKind::Store | AccessKind::Atomic) && !entry.d) {
        return page_fault(kind, va);
    }
    Translate::Physical(entry.pa_base | (va & 0xFFF))
}

/// The 10-step Sv39 walk (RVP-SUPERVISOR §11.1.3.2 with LEVELS=3 and PTESIZE=8 per
/// §11.1.4.1), cited step-by-step. Every PTE read crosses the boundary as the
/// walk-access kind (decision 6: an implicit 8-byte physical read, never a silent
/// data Load); under Svade the walk NEVER writes a PTE — a needed A/D update is a
/// page fault (D-SVADE), and the PTE is byte-untouched after it (the fault-matrix
/// tests prove that). The misaligned-versus-page-fault priority is the pinned
/// implementation-defined choice (decision 7): the model judges the ORIGINAL
/// access's alignment before this walk ever runs (Table 7's latitude, recorded).
fn walk<H: PrivilegedHart>(
    hart: &mut H,
    env: &mut dyn Environment,
    va: u64,
    kind: AccessKind,
    effective: EffectiveMode,
    satp: u64,
    asid: u16,
) -> Translate {
    // Step 1: a = satp.PPN × 4096; i = LEVELS-1 (= 2, Sv39's three levels).
    let mut a = (satp & ((1u64 << 44) - 1)) << 12;
    let mut i: i64 = 2;
    loop {
        // Step 2: read the level-i PTE at a + va.vpn[i] × PTESIZE through the
        // walk-access boundary kind; a boundary fault is the ACCESS fault of the
        // ORIGINAL access type (never a page fault, never substituted).
        let vpn_i = (va >> (12 + 9 * i)) & 0x1FF;
        let pte_addr = a + vpn_i * 8;
        let pte = match env.request(Request::WalkAccess { addr: pte_addr }) {
            Ok(Response::WalkAccess(v)) => v,
            Ok(_) => {
                return Translate::Failed(crate::outcome::ModelError::InvalidDescription {
                    what: "environment answered a WalkAccess with a non-walk response",
                });
            }
            Err(BoundaryError::Target(_)) => {
                return Translate::AccessFault {
                    cause: access_fault_cause(kind),
                    tval: va,
                };
            }
            Err(BoundaryError::Violation(v)) => {
                return Translate::Failed(crate::outcome::ModelError::ContractViolation(v));
            }
        };
        let v = pte & 1;
        let r = (pte >> 1) & 1;
        let w = (pte >> 2) & 1;
        let x = (pte >> 3) & 1;
        let u_bit = (pte >> 4) & 1;
        let a_bit = (pte >> 6) & 1;
        let d_bit = (pte >> 7) & 1;
        // Step 3: V=0 → page fault; the reserved W=1 ∧ R=0 encoding → page fault.
        if v == 0 || (r == 0 && w == 1) {
            return page_fault(kind, va);
        }
        // Step 4: the reserved/PBMT/N bits — neither Svnapot nor Svpbmt is selected,
        // so bits 63 (N), 62–61 (PBMT) and 60–54 (reserved) must all be zero, else
        // page fault.
        if pte >> 54 != 0 {
            return page_fault(kind, va);
        }
        let ppn = (pte >> 10) & ((1u64 << 44) - 1);
        if r == 0 && x == 0 {
            // Step 6 (non-leaf): a pointer PTE at the last level is invalid; and the
            // non-leaf D/A/U bits are reserved (§11.1.3.1) and must be zero, else
            // page fault. Otherwise descend: a = pte.ppn × 4096; i -= 1; step 2.
            if i == 0 || d_bit == 1 || a_bit == 1 || u_bit == 1 {
                return page_fault(kind, va);
            }
            a = ppn << 12;
            i -= 1;
            continue;
        }
        // Step 5 (leaf): a superpage must be aligned — at level i > 0 the low 9×i
        // bits of the PPN must be zero, else page fault.
        if i > 0 && ppn & ((1u64 << (9 * i)) - 1) != 0 {
            return page_fault(kind, va);
        }
        // Steps 8–10 are the leaf's shared judgment (`finish`): build the entry the
        // walk proved, let finish judge it with the current effective mode, and
        // install only on success — a faulting access installs nothing, so the next
        // access re-walks and re-faults (Svade's fault path must not be cached).
        let g = (pte >> 5) & 1 == 1;
        let pa = (ppn << 12) | (va & ((1u64 << (12 + 9 * i)) - 1));
        let entry = TlbEntry {
            valid: true,
            global: g,
            asid,
            vpn: va >> 12,
            pa_base: pa & !0xFFF,
            r: r == 1,
            w: w == 1,
            x: x == 1,
            u: u_bit == 1,
            a: a_bit == 1,
            d: d_bit == 1,
            level: i,
        };
        match finish(&entry, va, kind, effective) {
            Translate::Physical(pa) => {
                hart.tlb().install(entry);
                return Translate::Physical(pa);
            }
            fault => return fault,
        }
    }
}

#[cfg(test)]
#[cfg(test)]
mod tests {
    use super::*;
    use crate::env::{BoundaryError, Environment, Failure, Request, Response};
    use crate::state_rv64gc::{ArchitecturalState, CSR_MSTATUS, CSR_SATP};

    const MPRV_BIT: u64 = 1 << 17;
    const SUM_BIT: u64 = 1 << 18;
    const MXR_BIT: u64 = 1 << 19;

    // PTE flag bits (§11.1.3.1's layout figure).
    const V: u64 = 1;
    const R: u64 = 2;
    const W: u64 = 4;
    const X: u64 = 8;
    const U: u64 = 16;
    const A: u64 = 64;
    const D: u64 = 128;

    const REGION_BASE: u64 = 0x8000_0000;
    const ROOT: u64 = 0x8000_8000; // the level-2 (root) table page
    const L1T: u64 = 0x8000_9000; // the level-1 table page
    const L0T: u64 = 0x8000_A000; // the level-0 table page

    /// The test environment: a byte region answering every request kind, with the
    /// walk-access and fetch counts as witnesses (the walk makes no silent reads).
    struct WalkEnv {
        mem: std::collections::BTreeMap<u64, u8>,
        fetches: u64,
        walks: u64,
        walk_fault: bool,
    }

    impl WalkEnv {
        fn new() -> Self {
            Self {
                mem: Default::default(),
                fetches: 0,
                walks: 0,
                walk_fault: false,
            }
        }
        fn read(&self, addr: u64, bytes: u64) -> u64 {
            let mut v = 0u64;
            for i in 0..bytes {
                v |= u64::from(*self.mem.get(&(addr + i)).unwrap_or(&0)) << (8 * i);
            }
            v
        }
        fn write(&mut self, addr: u64, bytes: u64, value: u64) {
            for i in 0..bytes {
                self.mem.insert(addr + i, ((value >> (8 * i)) & 0xFF) as u8);
            }
        }
        fn image(&self) -> Vec<(u64, u8)> {
            self.mem.iter().map(|(a, b)| (*a, *b)).collect()
        }
    }

    impl Environment for WalkEnv {
        fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
            match request {
                Request::Fetch { addr } => {
                    self.fetches += 1;
                    if !(REGION_BASE..REGION_BASE + 0x20000).contains(&addr) {
                        return Err(Failure::AccessFault.into());
                    }
                    Ok(Response::Fetch(self.read(addr, 4) as u32))
                }
                Request::Load { width, addr } => {
                    if addr % width.bytes() != 0 {
                        return Err(Failure::Misaligned.into());
                    }
                    if !(REGION_BASE..REGION_BASE + 0x20000).contains(&addr) {
                        return Err(Failure::AccessFault.into());
                    }
                    Ok(Response::Load(self.read(addr, width.bytes())))
                }
                Request::Store { width, addr, data } => {
                    if addr % width.bytes() != 0 {
                        return Err(Failure::Misaligned.into());
                    }
                    if !(REGION_BASE..REGION_BASE + 0x20000).contains(&addr) {
                        return Err(Failure::AccessFault.into());
                    }
                    self.write(addr, width.bytes(), data);
                    Ok(Response::StoreDone)
                }
                Request::WalkAccess { addr } => {
                    self.walks += 1;
                    if addr % 8 != 0 {
                        return Err(Failure::Misaligned.into());
                    }
                    if self.walk_fault || !(REGION_BASE..REGION_BASE + 0x20000).contains(&addr) {
                        return Err(Failure::AccessFault.into());
                    }
                    Ok(Response::WalkAccess(self.read(addr, 8)))
                }
            }
        }
    }

    fn hart() -> ArchitecturalState {
        ArchitecturalState::zeroed_at(REGION_BASE)
    }

    fn sv39(state: &mut ArchitecturalState) {
        state.write_csr(CSR_SATP, (8u64 << 60) | (ROOT >> 12));
    }

    fn leaf_pte(pa: u64, flags: u64) -> u64 {
        ((pa >> 12) << 10) | flags
    }

    fn pointer_pte(table: u64) -> u64 {
        ((table >> 12) << 10) | V // a non-leaf PTE: V only — D/A/U stay zero (§11.1.3.1)
    }

    /// The full three-level path for `va`, ending in `leaf` at level 0.
    fn table_4k(env: &mut WalkEnv, va: u64, leaf: u64) {
        env.write(ROOT + ((va >> 30) & 0x1FF) * 8, 8, pointer_pte(L1T));
        env.write(L1T + ((va >> 21) & 0x1FF) * 8, 8, pointer_pte(L0T));
        env.write(L0T + ((va >> 12) & 0x1FF) * 8, 8, leaf);
    }

    /// A level-1 leaf (2 MiB superpage): root[vpn2] -> L1T, L1T[vpn1] -> leaf.
    fn table_2m(env: &mut WalkEnv, va: u64, leaf: u64) {
        env.write(ROOT + ((va >> 30) & 0x1FF) * 8, 8, pointer_pte(L1T));
        env.write(L1T + ((va >> 21) & 0x1FF) * 8, 8, leaf);
    }

    #[test]
    fn bare_is_identity_for_every_mode_and_kind() {
        let mut state = hart();
        let mut env = WalkEnv::new();
        for kind in [
            AccessKind::Fetch,
            AccessKind::Load,
            AccessKind::Store,
            AccessKind::Atomic,
        ] {
            assert_eq!(
                translate(&mut state, &mut env, 0xDEAD_BEEF, kind),
                Translate::Identity(0xDEAD_BEEF)
            );
        }
        state.set_mode(PrivilegeMode::S);
        assert_eq!(
            translate(&mut state, &mut env, 0x1234, AccessKind::Load),
            Translate::Identity(0x1234)
        );
        assert_eq!(env.walks, 0, "Bare makes no walk accesses");
    }

    #[test]
    fn m_mode_is_never_translated_even_under_sv39() {
        let mut state = hart();
        sv39(&mut state);
        let mut env = WalkEnv::new();
        assert_eq!(
            translate(&mut state, &mut env, 0x8000_0004, AccessKind::Fetch),
            Translate::Identity(0x8000_0004)
        );
        assert_eq!(
            translate(&mut state, &mut env, 0x8000_1000, AccessKind::Load),
            Translate::Identity(0x8000_1000)
        );
        assert_eq!(
            translate(&mut state, &mut env, 0x8000_1000, AccessKind::Store),
            Translate::Identity(0x8000_1000)
        );
        assert_eq!(env.walks, 0, "an M-effective access makes no walk accesses");
    }

    #[test]
    fn walk_4k_leaf_translates_with_three_walk_reads() {
        let mut state = hart();
        sv39(&mut state);
        state.set_mode(PrivilegeMode::S);
        let mut env = WalkEnv::new();
        let va = 0x0000_0000_0040_2123_u64;
        let pa = 0x8000_4000_u64;
        table_4k(&mut env, va, leaf_pte(pa & !0xFFF, V | A | D | R | W | X));
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::Physical((pa & !0xFFF) | (va & 0xFFF))
        );
        assert_eq!(env.walks, 3, "a 4 KiB leaf is three PTE reads (LEVELS=3)");
    }

    #[test]
    fn walk_superpages_translate_by_level() {
        let mut state = hart();
        sv39(&mut state);
        state.set_mode(PrivilegeMode::S);
        let mut env = WalkEnv::new();
        // 2 MiB superpage (level-1 leaf), aligned
        let va = 0x0000_0000_0060_0456_u64;
        table_2m(&mut env, va, leaf_pte(0x8000_0000, V | A | D | R | W));
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Store),
            Translate::Physical(0x8000_0000 | (va & 0x1F_FFFF))
        );
        assert_eq!(env.walks, 2, "a 2 MiB leaf is two PTE reads");
        // 1 GiB superpage (level-2 leaf), aligned
        let mut env = WalkEnv::new();
        let va = 0x0000_0000_C000_0123_u64;
        env.write(
            ROOT + ((va >> 30) & 0x1FF) * 8,
            8,
            leaf_pte(0x8000_0000, V | A | D | R),
        );
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::Physical(0x8000_0000 | (va & 0x3FFF_FFFF))
        );
        assert_eq!(env.walks, 1, "a 1 GiB leaf is one PTE read");
    }

    #[test]
    fn the_canonical_va_check_faults_noncanonical_addresses() {
        let mut state = hart();
        sv39(&mut state);
        state.set_mode(PrivilegeMode::S);
        let mut env = WalkEnv::new();
        let va = 0x0000_8000_0000_0000_u64; // bit 39 set with bits 63:39 clear: non-canonical
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::PageFault {
                cause: 13,
                tval: va
            }
        );
        assert_eq!(env.walks, 0, "the canonical check precedes every walk read");
    }

    #[test]
    fn step3_v0_and_reserved_rw_fault() {
        let mut state = hart();
        sv39(&mut state);
        state.set_mode(PrivilegeMode::S);
        let va = 0x0000_0000_0040_2000_u64;
        let mut env = WalkEnv::new();
        table_4k(&mut env, va, leaf_pte(0x8000_4000, R | A | D)); // V=0
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::PageFault {
                cause: 13,
                tval: va
            }
        );
        let mut env = WalkEnv::new();
        table_4k(&mut env, va, leaf_pte(0x8000_4000, V | W | A | D)); // W=1 ∧ R=0: reserved
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::PageFault {
                cause: 13,
                tval: va
            }
        );
    }

    #[test]
    fn step4_reserved_pbmt_n_bits_fault() {
        let mut state = hart();
        sv39(&mut state);
        state.set_mode(PrivilegeMode::S);
        let va = 0x0000_0000_0040_2000_u64;
        for bit in [63, 61, 54] {
            let mut env = WalkEnv::new();
            table_4k(
                &mut env,
                va,
                leaf_pte(0x8000_4000, V | R | A | D) | (1u64 << bit),
            );
            assert_eq!(
                translate(&mut state, &mut env, va, AccessKind::Load),
                Translate::PageFault {
                    cause: 13,
                    tval: va
                },
                "bit {bit} set in a leaf PTE must page-fault (unselected Svnapot/Svpbmt)"
            );
        }
    }

    #[test]
    fn step5_misaligned_superpage_faults() {
        let mut state = hart();
        sv39(&mut state);
        state.set_mode(PrivilegeMode::S);
        let va = 0x0000_0000_0060_0000_u64;
        let mut env = WalkEnv::new();
        // a level-1 leaf whose low 9 PPN bits are nonzero: misaligned 2 MiB
        table_2m(&mut env, va, leaf_pte(0x8000_1000, A | D | R));
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::PageFault {
                cause: 13,
                tval: va
            }
        );
    }

    #[test]
    fn step6_non_leaf_dau_reserved_and_last_level_pointer_fault() {
        let mut state = hart();
        sv39(&mut state);
        state.set_mode(PrivilegeMode::S);
        let va = 0x0000_0000_0040_2000_u64;
        for dirty in [A, D, U] {
            let mut env = WalkEnv::new();
            env.write(ROOT + ((va >> 30) & 0x1FF) * 8, 8, pointer_pte(L1T) | dirty);
            assert_eq!(
                translate(&mut state, &mut env, va, AccessKind::Load),
                Translate::PageFault {
                    cause: 13,
                    tval: va
                },
                "a non-leaf PTE with D/A/U set is reserved (§11.1.3.1)"
            );
        }
        // a pointer PTE at level 0: no level left to descend into
        let mut env = WalkEnv::new();
        table_4k(&mut env, va, pointer_pte(0x8000_4000));
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::PageFault {
                cause: 13,
                tval: va
            }
        );
    }

    #[test]
    fn step8_u_sum_mxr_cells() {
        let mut state = hart();
        sv39(&mut state);
        state.set_mode(PrivilegeMode::S);
        let va = 0x0000_0000_0040_2000_u64;
        // S mode, U=0 (an S page): allowed regardless of SUM
        let mut env = WalkEnv::new();
        table_4k(&mut env, va, leaf_pte(0x8000_4000, V | R | A | D));
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::Physical(0x8000_4000 | (va & 0xFFF))
        );
        // S mode, U=1 page, SUM=0: data accesses fault (a cold hart — the previous
        // cell's installed entry must not mask this one; caching is its own suite)
        state = hart();
        sv39(&mut state);
        state.set_mode(PrivilegeMode::S);
        let mut env = WalkEnv::new();
        table_4k(&mut env, va, leaf_pte(0x8000_4000, V | R | U | A | D));
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::PageFault {
                cause: 13,
                tval: va
            }
        );
        // S mode, U=1 page, SUM=1: data accesses pass — but a FETCH faults unconditionally
        state.write_csr(CSR_MSTATUS, SUM_BIT);
        let mut env = WalkEnv::new();
        table_4k(&mut env, va, leaf_pte(0x8000_4000, V | R | U | A | D));
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::Physical(0x8000_4000 | (va & 0xFFF))
        );
        let mut env = WalkEnv::new();
        table_4k(&mut env, va, leaf_pte(0x8000_4000, V | X | U | A | D));
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Fetch),
            Translate::PageFault {
                cause: 12,
                tval: va
            },
            "an S-mode fetch of a U page faults regardless of SUM"
        );
        // U mode, U=0 page: faults (a cold hart, same reason)
        state = hart();
        sv39(&mut state);
        state.set_mode(PrivilegeMode::U);
        let mut env = WalkEnv::new();
        table_4k(&mut env, va, leaf_pte(0x8000_4000, V | R | A | D));
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::PageFault {
                cause: 13,
                tval: va
            }
        );
        // MXR: a load of an X-only page faults with MXR=0, passes with MXR=1
        state.set_mode(PrivilegeMode::S);
        state.write_csr(CSR_MSTATUS, 0);
        let mut env = WalkEnv::new();
        table_4k(&mut env, va, leaf_pte(0x8000_4000, V | X | A | D));
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::PageFault {
                cause: 13,
                tval: va
            }
        );
        state.write_csr(CSR_MSTATUS, MXR_BIT);
        let mut env = WalkEnv::new();
        table_4k(&mut env, va, leaf_pte(0x8000_4000, V | X | A | D));
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::Physical(0x8000_4000 | (va & 0xFFF))
        );
    }

    #[test]
    fn step8_rwx_cells() {
        let mut state = hart();
        sv39(&mut state);
        state.set_mode(PrivilegeMode::U);
        let va = 0x0000_0000_0040_2000_u64;
        let mut env = WalkEnv::new();
        table_4k(&mut env, va, leaf_pte(0x8000_4000, V | R | U | A | D)); // X=0
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Fetch),
            Translate::PageFault {
                cause: 12,
                tval: va
            }
        );
        let mut env = WalkEnv::new();
        table_4k(&mut env, va, leaf_pte(0x8000_4000, V | U | A | D)); // R=0, X=0
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::PageFault {
                cause: 13,
                tval: va
            }
        );
        let mut env = WalkEnv::new();
        table_4k(&mut env, va, leaf_pte(0x8000_4000, V | R | U | A)); // W=0
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Store),
            Translate::PageFault {
                cause: 15,
                tval: va
            }
        );
    }

    #[test]
    fn atomic_judges_read_and_write_under_store_causes() {
        // P4-SYSTEM.4 decision 5: the AMO's ONE translation is judged under the
        // store/AMO rules — read AND write permission required, and every fault is the
        // store/AMO cause 15, never a load page fault ("AMOs never raise load
        // page-fault exceptions … attempting to perform an AMO on an unreadable page
        // always raises a store page-fault exception", RVP-SUPERVISOR).
        let va = 0x0000_0000_0040_2000_u64;
        let cells = [
            (V | W | U | A | D, "R=0: an unreadable page faults"),
            (V | R | U | A, "W=0: an unwritable page faults"),
            (V | R | W | U | D, "A=0: Svade faults instead of updating"),
            (V | R | W | U | A, "D=0: the AMO writes, so Svade faults"),
        ];
        for (flags, why) in cells {
            let mut state = hart();
            sv39(&mut state);
            state.set_mode(PrivilegeMode::U);
            let mut env = WalkEnv::new();
            table_4k(&mut env, va, leaf_pte(0x8000_4000, flags));
            assert_eq!(
                translate(&mut state, &mut env, va, AccessKind::Atomic),
                Translate::PageFault {
                    cause: 15,
                    tval: va
                },
                "{why} — cause 15, never 13"
            );
        }
        let mut state = hart();
        sv39(&mut state);
        state.set_mode(PrivilegeMode::U);
        let mut env = WalkEnv::new();
        table_4k(&mut env, va, leaf_pte(0x8000_4000, V | R | W | U | A | D));
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Atomic),
            Translate::Physical(0x8000_4000 | (va & 0xFFF)),
            "R∧W with A and D set: the AMO translates"
        );
        assert_eq!(page_fault_cause(AccessKind::Atomic), 15);
        assert_eq!(access_fault_cause(AccessKind::Atomic), 7);
    }

    #[test]
    fn step9_svade_faults_and_the_pte_is_byte_untouched() {
        let mut state = hart();
        sv39(&mut state);
        state.set_mode(PrivilegeMode::S);
        let va = 0x0000_0000_0040_2000_u64;
        // A=0 on any access: page fault, no hardware update, the region byte-identical
        let mut env = WalkEnv::new();
        table_4k(&mut env, va, leaf_pte(0x8000_4000, V | R | W | D)); // A=0
        let before = env.image();
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::PageFault {
                cause: 13,
                tval: va
            }
        );
        assert_eq!(
            env.image(),
            before,
            "Svade: the PTE is byte-untouched after the fault"
        );
        // A=1, D=0 on a store: page fault; on a load: no update at all
        let mut env = WalkEnv::new();
        table_4k(&mut env, va, leaf_pte(0x8000_4000, V | R | W | A)); // A=1, D=0
        let before = env.image();
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Store),
            Translate::PageFault {
                cause: 15,
                tval: va
            }
        );
        assert_eq!(
            env.image(),
            before,
            "Svade: the store fault leaves the PTE untouched"
        );
        // a load past a D=0 leaf installs the entry — the Svade staleness suite
        // exercises exactly that interaction; these outcome cells run cold
        state = hart();
        sv39(&mut state);
        state.set_mode(PrivilegeMode::S);
        let mut env = WalkEnv::new();
        table_4k(&mut env, va, leaf_pte(0x8000_4000, V | R | W | A));
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::Physical(0x8000_4000 | (va & 0xFFF)),
            "Svade reads D but never sets it — a load past a D=0 leaf is legal"
        );
        // A=1, D=1: the store translates
        state = hart();
        sv39(&mut state);
        state.set_mode(PrivilegeMode::S);
        let mut env = WalkEnv::new();
        table_4k(&mut env, va, leaf_pte(0x8000_4000, V | R | W | A | D));
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Store),
            Translate::Physical(0x8000_4000 | (va & 0xFFF))
        );
    }

    #[test]
    fn step2_a_walk_read_fault_is_the_original_accesss_access_fault() {
        let mut state = hart();
        // the root page outside the declared region: the walk read itself faults
        state.write_csr(CSR_SATP, (8u64 << 60) | (0x8008_0000u64 >> 12));
        state.set_mode(PrivilegeMode::S);
        let mut env = WalkEnv::new();
        let va = 0x0000_0000_0040_2000_u64;
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Fetch),
            Translate::AccessFault { cause: 1, tval: va },
            "the walk read faults as an instruction access fault"
        );
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::AccessFault { cause: 5, tval: va }
        );
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Store),
            Translate::AccessFault { cause: 7, tval: va }
        );
    }

    #[test]
    fn mprv_selects_mpp_for_data_accesses_and_m_never_walks() {
        let mut state = hart();
        sv39(&mut state);
        let va = 0x0000_0000_0040_2000_u64;
        // M with MPRV=0: identity even under Sv39, and ZERO walk reads
        let mut env = WalkEnv::new();
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::Identity(va)
        );
        assert_eq!(env.walks, 0);
        // M with MPRV=1 and MPP=S: the data access walks with the S effective mode
        state.write_csr(CSR_MSTATUS, MPRV_BIT | (1 << 11));
        let mut env = WalkEnv::new();
        table_4k(&mut env, va, leaf_pte(0x8000_4000, V | R | A | D));
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::Physical(0x8000_4000 | (va & 0xFFF))
        );
        assert_eq!(
            env.walks, 3,
            "the MPRV=1 data access walks like an S-mode one"
        );
        // …but the FETCH ignores MPRV: the current mode is M, so identity
        let mut env = WalkEnv::new();
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Fetch),
            Translate::Identity(va)
        );
        assert_eq!(env.walks, 0);
    }

    #[test]
    fn an_out_of_vocabulary_satp_mode_is_a_named_defect() {
        let mut state = hart();
        state.set_mode(PrivilegeMode::S);
        state.write_csr(CSR_SATP, 5 << 60); // raw storage write bypasses the WARL discipline
        let mut env = WalkEnv::new();
        let outcome = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
            translate(&mut state, &mut env, 0x1000, AccessKind::Load)
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

    /// The straddled instruction (decision 5, live): two parcels mapping to two
    /// different 4 KiB pages — the hook fetches each parcel's own unit and joins the
    /// halves, two fetch requests and six walk reads, the word assembled exactly.
    #[test]
    fn a_page_straddling_fetch_joins_two_physical_units() {
        use crate::definition_rv64gc::INSNS;
        use crate::exec_rv64gc::{step_over, StepRv64gc};

        let mut state = hart();
        state.set_mode(PrivilegeMode::S);
        sv39(&mut state);
        let mut env = WalkEnv::new();
        // VA page [0x0, 0xFFF] → PA page [0x8000_1000..], VA page [0x1000, 0x1FFF] →
        // PA page [0x8000_5000..] — NON-adjacent, so the parcels cannot coalesce and
        // each is fetched from its own unit (adjacent physical pages would correctly
        // coalesce — the one-request rule is over translated addresses, not pages).
        let va = 0x0000_0000_0000_0FFE_u64;
        table_4k(&mut env, va, leaf_pte(0x8000_1000, V | A | D | X));
        table_4k(&mut env, va + 2, leaf_pte(0x8000_5000, V | A | D | X));
        // addi x1, x0, 42 = 0x02A00093, written across the virtual seam
        env.write(0x8000_1000 + 0xFFE, 2, 0x0093);
        env.write(0x8000_5000, 2, 0x02A0);
        state.set_pc(va);
        let outcome = step_over(&mut state, &mut env, INSNS);
        assert_eq!(outcome, StepRv64gc::Executed);
        assert_eq!(
            state.read_x(1),
            42,
            "the joined word executes as addi x1, x0, 42"
        );
        assert_eq!(
            env.fetches, 2,
            "a straddled instruction fetches each parcel's unit"
        );
        assert_eq!(env.walks, 6, "each parcel walks three levels");
        assert_eq!(state.pc(), va + 4);
    }

    // ---- the TLB (P4-SYSTEM.3 slice d): caching, staleness, the fence cases --------

    const G: u64 = 32; // the PTE G bit

    fn sv39_asid(state: &mut ArchitecturalState, asid: u64) {
        state.write_csr(CSR_SATP, (8u64 << 60) | (asid << 44) | (ROOT >> 12));
    }

    #[test]
    fn a_hit_skips_the_walk_and_the_fifo_evicts_in_order() {
        let va = 0x0000_0000_0040_2000_u64;
        let mut state = hart();
        sv39(&mut state);
        state.set_mode(PrivilegeMode::S);
        let mut env = WalkEnv::new();
        table_4k(&mut env, va, leaf_pte(0x8000_4000, V | R | A | D));
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::Physical(0x8000_4000 | (va & 0xFFF))
        );
        assert_eq!(env.walks, 3, "the first access walks");
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::Physical(0x8000_4000 | (va & 0xFFF))
        );
        assert_eq!(env.walks, 3, "the second access HITS — no walk at all");
        assert_eq!(state.tlb().occupied(), 1);
        // five MORE installs (6 total) evict the first two in FIFO order
        for k in 1..=5u64 {
            let kv = va + 0x1000 * k;
            table_4k(
                &mut env,
                kv,
                leaf_pte(0x8000_4000 + 0x1000 * k, V | R | A | D),
            );
            assert_eq!(
                translate(&mut state, &mut env, kv, AccessKind::Load),
                Translate::Physical((0x8000_4000 + 0x1000 * k) | (kv & 0xFFF))
            );
        }
        assert_eq!(state.tlb().occupied(), TLB_CAPACITY);
        let before = env.walks;
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::Physical(0x8000_4000 | (va & 0xFFF))
        );
        assert!(
            env.walks > before,
            "the oldest entry was evicted in FIFO order — a re-walk"
        );
    }

    #[test]
    fn asid_tags_and_global_hits() {
        let va = 0x0000_0000_0040_2000_u64;
        // a non-global entry hits only under its own ASID
        let mut state = hart();
        sv39_asid(&mut state, 7);
        state.set_mode(PrivilegeMode::S);
        let mut env = WalkEnv::new();
        table_4k(&mut env, va, leaf_pte(0x8000_4000, V | R | A | D));
        translate(&mut state, &mut env, va, AccessKind::Load);
        let walks = env.walks;
        sv39_asid(&mut state, 7);
        translate(&mut state, &mut env, va, AccessKind::Load);
        assert_eq!(env.walks, walks, "same ASID: hit");
        sv39_asid(&mut state, 9);
        assert_ne!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::PageFault {
                cause: 13,
                tval: va
            }
        );
        assert!(env.walks > walks, "a different ASID misses and re-walks");
        // a G-bit entry hits under ANY ASID
        let mut state = hart();
        sv39_asid(&mut state, 7);
        state.set_mode(PrivilegeMode::S);
        let mut env = WalkEnv::new();
        table_4k(&mut env, va, leaf_pte(0x8000_4000, V | R | A | D | G));
        translate(&mut state, &mut env, va, AccessKind::Load);
        let walks = env.walks;
        sv39_asid(&mut state, 42);
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::Physical(0x8000_4000 | (va & 0xFFF))
        );
        assert_eq!(env.walks, walks, "a G-bit entry hits under any ASID");
    }

    #[test]
    fn staleness_is_legal_without_a_fence_and_the_fence_restores_truth() {
        let va = 0x0000_0000_0040_2000_u64;
        let mut state = hart();
        sv39(&mut state);
        state.set_mode(PrivilegeMode::S);
        let mut env = WalkEnv::new();
        table_4k(&mut env, va, leaf_pte(0x8000_4000, V | R | A | D));
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::Physical(0x8000_4000 | (va & 0xFFF))
        );
        // the PTE changes with NO fence: the stale hit is LEGAL (§11.1.2.1's own rule)
        table_4k(&mut env, va, leaf_pte(0x8000_8000, V | R | A | D));
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::Physical(0x8000_4000 | (va & 0xFFF)),
            "a stale hit without a fence is the spec's sanctioned staleness, not a bug"
        );
        // SFENCE.VMA at the VA: the subsuming fence — the next access re-walks
        fence(&mut state, va, 0);
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::Physical(0x8000_8000 | (va & 0xFFF)),
            "after the subsuming fence the walk sees the new PTE"
        );
        // and an illegal stale hit after that fence would be the TLB's own bug — the
        // third access must HIT the NEW entry, not re-fault to the old one
        let walks = env.walks;
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::Physical(0x8000_8000 | (va & 0xFFF))
        );
        assert_eq!(env.walks, walks, "the new translation hits");
    }

    #[test]
    fn svade_staleness_through_the_cache() {
        let va = 0x0000_0000_0040_2000_u64;
        let mut state = hart();
        sv39(&mut state);
        state.set_mode(PrivilegeMode::S);
        let mut env = WalkEnv::new();
        // a load past a D=0 leaf is legal and INSTALLS the D=0 entry
        table_4k(&mut env, va, leaf_pte(0x8000_4000, V | R | W | A));
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Load),
            Translate::Physical(0x8000_4000 | (va & 0xFFF))
        );
        // software sets D in the PTE WITHOUT fencing; a store hits the stale D=0
        // entry and Svade-faults — legal staleness, the entry's bits judging
        table_4k(&mut env, va, leaf_pte(0x8000_4000, V | R | W | A | D));
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Store),
            Translate::PageFault {
                cause: 15,
                tval: va
            },
            "the cached entry's D bit judges the store — a legal stale fault"
        );
        // after the fence the store walks, sees D=1, and translates
        fence(&mut state, va, 0);
        assert_eq!(
            translate(&mut state, &mut env, va, AccessKind::Store),
            Translate::Physical(0x8000_4000 | (va & 0xFFF))
        );
    }

    #[test]
    fn the_four_fence_cases() {
        let va1 = 0x0000_0000_0040_2000_u64;
        let va2 = 0x0000_0000_0050_3000_u64;
        let vg = 0x0000_0000_0060_4000_u64; // the global entry's own page
        let build = |state: &mut ArchitecturalState, env: &mut WalkEnv| {
            // two pages: va1 non-global ASID 7, va1 global (different pa), va2 non-global ASID 7
            sv39_asid(state, 7);
            table_4k(env, va1, leaf_pte(0x8000_4000, V | R | A | D));
            table_4k(env, va2, leaf_pte(0x8000_8000, V | R | A | D));
            translate(state, env, va1, AccessKind::Load);
            translate(state, env, va2, AccessKind::Load);
            // the G-bit entry on its own page (so the va1 entry cannot mask the install)
            table_4k(env, vg, leaf_pte(0x8000_C000, V | R | A | D | G));
            translate(state, env, vg, AccessKind::Load);
        };
        // case all-spaces (rs1=0, rs2=0): everything goes
        let mut state = hart();
        state.set_mode(PrivilegeMode::S);
        let mut env = WalkEnv::new();
        build(&mut state, &mut env);
        fence(&mut state, 0, 0);
        assert_eq!(
            state.tlb().occupied(),
            0,
            "the all-spaces fence empties the cache"
        );
        // case per-ASID (rs1=0, rs2≠0): non-global entries of that ASID go, G stays
        let mut state = hart();
        state.set_mode(PrivilegeMode::S);
        let mut env = WalkEnv::new();
        build(&mut state, &mut env);
        fence(&mut state, 0, 7);
        assert_eq!(
            state.tlb().occupied(),
            1,
            "only the G-bit entry is retained"
        );
        assert!(
            state.tlb().lookup(vg >> 12, 42).is_some(),
            "the retained entry is the global one"
        );
        // case per-address (rs1≠0, rs2=0): the VA's entries go in every space, G included
        let mut state = hart();
        state.set_mode(PrivilegeMode::S);
        let mut env = WalkEnv::new();
        build(&mut state, &mut env);
        fence(&mut state, vg, 0);
        assert_eq!(
            state.tlb().occupied(),
            2,
            "the per-address fence evicts the global entry too"
        );
        assert!(state.tlb().lookup(va1 >> 12, 7).is_some());
        // case per-address+ASID (rs1≠0, rs2≠0): only the matching non-global entry goes
        let mut state = hart();
        state.set_mode(PrivilegeMode::S);
        let mut env = WalkEnv::new();
        build(&mut state, &mut env);
        fence(&mut state, va1, 7);
        assert_eq!(
            state.tlb().occupied(),
            2,
            "the va1 entry goes; va2 and the global stay"
        );
        assert!(state.tlb().lookup(va2 >> 12, 7).is_some());
        assert!(
            state.tlb().lookup(vg >> 12, 42).is_some(),
            "the G entry is retained"
        );
    }

    #[test]
    fn a_noncanonical_rs1_va_has_no_effect_and_raises_nothing() {
        let va = 0x0000_0000_0040_2000_u64;
        let mut state = hart();
        sv39(&mut state);
        state.set_mode(PrivilegeMode::S);
        let mut env = WalkEnv::new();
        table_4k(&mut env, va, leaf_pte(0x8000_4000, V | R | A | D));
        translate(&mut state, &mut env, va, AccessKind::Load);
        fence(&mut state, 0x0000_8000_0000_0000, 0); // non-canonical: no effect, no exception
        assert_eq!(
            state.tlb().occupied(),
            1,
            "a non-canonical rs1 VA invalidates nothing"
        );
    }

    #[test]
    fn the_fence_effect_runs_through_the_instruction() {
        // sfence.vma x3, x4 through the evaluator's own effect tree: rs1 is the VA,
        // rs2 the ASID — the per-address+ASID case, with the legality intact
        use crate::definition_rv64gc::INSNS;
        use crate::exec_rv64gc::{step_over, StepRv64gc};

        let mut state = hart();
        sv39_asid(&mut state, 7);
        state.set_mode(PrivilegeMode::S);
        let mut env = WalkEnv::new();
        let va = 0x0000_0000_0040_2000_u64;
        table_4k(&mut env, va, leaf_pte(0x8000_4000, V | R | A | D));
        translate(&mut state, &mut env, va, AccessKind::Load);
        assert_eq!(state.tlb().occupied(), 1);
        // sfence.vma x3, x4 = rs1=x3 (the VA), rs2=x4 (the ASID) — 0x12039073; executed
        // in M (never translated — the fence instruction itself fetches identity)
        state.set_mode(PrivilegeMode::M);
        state.write_x(3, va);
        state.write_x(4, 7);
        state.set_pc(REGION_BASE);
        env.write(REGION_BASE, 4, 0x1243_8073);
        assert_eq!(step_over(&mut state, &mut env, INSNS), StepRv64gc::Executed);
        assert_eq!(
            state.tlb().occupied(),
            0,
            "the fence instruction invalidated the entry"
        );
        assert_eq!(state.pc(), REGION_BASE + 4);
        // and a fence with rs2=x0 (the per-address case) hits nothing after it
        let mut env2 = WalkEnv::new();
        table_4k(&mut env2, va, leaf_pte(0x8000_4000, V | R | A | D));
        translate(&mut state, &mut env2, va, AccessKind::Load);
        state.set_mode(PrivilegeMode::M);
        state.write_x(4, 0);
        state.set_pc(REGION_BASE);
        env2.write(REGION_BASE, 4, 0x1238_0073); // sfence.vma x3, x0
        assert_eq!(
            step_over(&mut state, &mut env2, INSNS),
            StepRv64gc::Executed
        );
        assert_eq!(
            state.tlb().occupied(),
            0,
            "the per-address fence also invalidates"
        );
    }

    #[test]
    fn determinism_from_cold_reset_is_trace_identical() {
        let run = || {
            let va = 0x0000_0000_0040_2000_u64;
            let mut state = hart();
            sv39_asid(&mut state, 7);
            state.set_mode(PrivilegeMode::S);
            let mut env = WalkEnv::new();
            let mut outcomes = Vec::new();
            table_4k(&mut env, va, leaf_pte(0x8000_4000, V | R | A | D));
            for k in 0..6u64 {
                let kv = va + 0x1000 * k;
                table_4k(
                    &mut env,
                    kv,
                    leaf_pte(0x8000_4000 + 0x1000 * k, V | R | A | D),
                );
                outcomes.push(translate(&mut state, &mut env, kv, AccessKind::Load));
            }
            fence(&mut state, 0, 7);
            outcomes.push(translate(&mut state, &mut env, va, AccessKind::Load));
            (outcomes, env.walks, state.tlb().occupied())
        };
        let first = run();
        let second = run();
        assert_eq!(
            first, second,
            "the cache is a pure function of the hart's own history"
        );
    }
}
