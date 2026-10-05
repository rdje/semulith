//! The privileged-state machinery — `P4-SYSTEM.2` slice (d): trap delivery, `xret`, the
//! CSR permission model, and WPRI/WARL/WLRL legalization, as ENGINE code over DATA.
//!
//! OWN-01 at the type level: this module owns the VOCABULARY (what a discipline or a
//! legalization IS, what trap delivery DOES) exactly once; the DATA — which CSRs exist,
//! which fields they carry, what each field legalizes to — derives from the profile's
//! state document through the generated module (`gen_state.py`), which implements
//! [`PrivilegedHart`]. Nothing here names an address or a bit position the descriptor
//! does not carry: the register-level constants (the counter-enable bit positions, the
//! mstatus stack fields, the mode codes) cite the pinned `encoding.h` masks of the
//! rv64gc encoding-source pin — the specification renders those layouts as figure
//! images (RVP-CSR §1.1.1's address conventions are text).
//!
//! The instruction-level LEGALITY of the privileged instructions (xRET in a
//! less-privileged mode, WFI under TW, SFENCE.VMA under TVM) is the instructions' own
//! semantics data (`definitions/riscv/system.sem.sexp`) — this module performs the
//! mechanisms; it does not adjudicate them. The CSR ACCESS permission model is uniform
//! and lives here, exactly as `schema/semantics.sexp` declares for `csr-read`/`csr-write`.
//!
//! References below: RVP-MACHINE = the pinned Machine-Level ISA chapter (v1.13),
//! RVP-SUPERVISOR = Supervisor-Level ISA (v1.13), RVP-CSR = the CSR listing chapter,
//! RVP-SSTC = the Sstc chapter — the rv64gc-lab-v0 pinned pages.

/// The current privilege mode of a hart. The codes are the architecture's own — the
/// pinned `encoding.h`'s `PRV_U`/`PRV_S`/`PRV_M` (the specification states the two-bit
/// encoding in the xPP figure); the mode is hart state, not a CSR (RVP-INTRO).
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord)]
pub enum PrivilegeMode {
    /// User mode (code 0).
    U = 0,
    /// Supervisor mode (code 1).
    S = 1,
    /// Machine mode (code 3).
    M = 3,
}

impl PrivilegeMode {
    /// The architectural code (the xPP encoding).
    #[must_use]
    pub fn code(self) -> u64 {
        self as u64
    }
}

/// A field's write discipline — RVP-CSR §1.1.3.1–3's vocabulary.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum FieldDiscipline {
    /// Reserved Writes Preserve Values, Reads Ignore Values (§1.1.3.1).
    Wpri,
    /// Write/Read Only Legal Values (§1.1.3.2).
    Wlrl,
    /// Write Any Values, Reads Legal Values (§1.1.3.3).
    Warl,
}

/// A field's legal-value rule, lowered from the state document's `(legalize …)` data —
/// the engine applies it; it never guesses.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Legalize {
    /// `(any)` — every value is legal.
    Any,
    /// `(read-only V)` — the field holds exactly V; writes do not change it.
    ReadOnly(u64),
    /// `(one-of V …)` — the enumerated set; an illegal write retains the old value (the
    /// WARL laboratory choice, recorded in the state document).
    OneOf(&'static [u64]),
    /// `(computed)` — the engine computes the field (mstatus.SD, mip.STIP); writes do
    /// not apply.
    Computed,
}

/// One CSR's metadata: its name, its address, and the register it is a view of (a view
/// declares no storage — sstatus restricts mstatus; the counters shadow theirs).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct CsrMeta {
    /// The architectural name.
    pub name: &'static str,
    /// The 12-bit address.
    pub address: u16,
    /// The register whose storage this one restricts, if any.
    pub view_of: Option<&'static str>,
}

/// One CSR field's legalization row, lowered from the state document.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct FieldMeta {
    /// The owning CSR's name.
    pub csr: &'static str,
    /// The field's name.
    pub name: &'static str,
    /// The field's top bit.
    pub bit_hi: u8,
    /// The field's bottom bit.
    pub bit_lo: u8,
    /// The field's discipline (RVP-CSR §1.1.3.1–3).
    pub discipline: FieldDiscipline,
    /// The field's legal-value rule. `None` only on WPRI, whose discipline is the rule.
    pub legalize: Option<Legalize>,
    /// The field's reset value (its declared reset — see the descriptor).
    pub reset: u64,
}

/// A CSR access the permission model refuses — the instruction layer converts this into
/// the illegal-instruction trap (cause 2, xtval the instruction word — the semantics
/// data's rule, `definitions/riscv/zicsr.sem.sexp`).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct IllegalCsrAccess {
    /// The address the access named.
    pub address: u16,
    /// Why it refused, for diagnostics — never read by control flow.
    pub why: &'static str,
}

/// The state surface the machinery needs. The generated state module implements it; the
/// unit tests exercise the machinery against a fixture hart carrying the same document
/// facts in miniature.
pub trait PrivilegedHart {
    /// The current privilege mode.
    fn mode(&self) -> PrivilegeMode;
    /// Set the current privilege mode (trap delivery and xret).
    fn set_mode(&mut self, mode: PrivilegeMode);
    /// Raw read of CSR storage by index (no permission model, no view resolution).
    fn csr_raw(&self, index: usize) -> u64;
    /// Raw write of CSR storage by index.
    fn csr_write_raw(&mut self, index: usize, value: u64);
    /// The storage index of a csr address, or `None` for an address the profile does
    /// not implement.
    fn csr_index(&self, address: u16) -> Option<usize>;
    /// The profile's CSR metadata table (views included), in descriptor order.
    fn csr_meta(&self) -> &'static [CsrMeta];
    /// The profile's per-field legalization tables.
    fn csr_fields(&self) -> &'static [FieldMeta];

    /// The hart's translation lookaside buffer (`P4-SYSTEM.3` decision 2) — hart
    /// state like the mode and the CSR file, owned by the generated state module
    /// because the state document's SEM-08 census declares it (the
    /// `translation-cache` candidate). The cache's own rules live in
    /// `crate::translation`.
    fn tlb(&mut self) -> &mut crate::translation::Tlb;

    /// The hart's LR/SC reservation (`P4-SYSTEM.4` decision 2) — hart state like the
    /// TLB, owned by the generated state module because the state document's SEM-08
    /// census declares it (the `reservation set (LR/SC)` candidate, pre-declared so
    /// the reservation could never be smuggled in silently). The reservation's own
    /// rules live in [`crate::reservation`].
    fn reservation(&mut self) -> &mut crate::reservation::Reservation;
}

// ---- name-addressed plumbing ----------------------------------------------------------

fn meta_by_name<H: PrivilegedHart>(hart: &H, name: &str) -> Option<&'static CsrMeta> {
    hart.csr_meta().iter().find(|m| m.name == name)
}

/// The storage index a CSR NAME resolves to, through the view relation.
fn index_by_name<H: PrivilegedHart>(hart: &H, name: &str) -> Option<usize> {
    let meta = meta_by_name(hart, name)?;
    let owner = meta.view_of.unwrap_or(name);
    hart.csr_index(meta_by_name(hart, owner)?.address)
}

/// The machine's own read of a CSR's current bits — `csr-state` in the semantics
/// language: no permission model, views resolved, computed fields applied.
#[must_use]
pub fn csr_state<H: PrivilegedHart>(hart: &H, name: &str) -> u64 {
    let Some(index) = index_by_name(hart, name) else {
        return 0; // an absent register reads zero — the profile never names it
    };
    let mut value = hart.csr_raw(index);
    for f in hart.csr_fields().iter().filter(|f| f.csr == name) {
        if f.legalize == Some(Legalize::Computed) {
            let mask = field_mask(f);
            value = (value & !mask) | (computed(hart, f) & mask);
        }
    }
    value
}

fn field_mask(f: &FieldMeta) -> u64 {
    let width = u64::from(f.bit_hi - f.bit_lo) + 1;
    let bits = if width >= 64 {
        u64::MAX
    } else {
        (1u64 << width) - 1
    };
    bits << f.bit_lo
}

/// The `(computed)` fields this slice owns. SD is the FS/XS/VS summary (RVP-MACHINE
/// §2.1.1.6.7); STIP is the stimecmp-vs-time comparison (RVP-SSTC 12.1 — the timer
/// signal's progress is the environment contract's, P4-SYSTEM.5/.9). Any other computed
/// field is generator work: it computes as its stored bits until its owner lands.
fn computed<H: PrivilegedHart>(hart: &H, f: &FieldMeta) -> u64 {
    match (f.csr, f.name) {
        ("mstatus", "SD") | ("sstatus", "SD") => {
            let mstatus = csr_state_raw(hart, "mstatus");
            let fs = (mstatus >> 13) & 0b11; // the pinned encoding.h's MSTATUS_FS
            let xs = (mstatus >> 15) & 0b11; // MSTATUS_XS
            let vs = (mstatus >> 9) & 0b11; // MSTATUS_VS
            u64::from(fs == 3 || xs == 3 || vs == 3) << f.bit_lo
        }
        ("mip", "STIP") | ("sip", "STIP") => {
            let time = csr_state_raw(hart, "time");
            let stimecmp = csr_state_raw(hart, "stimecmp");
            u64::from(time >= stimecmp) << f.bit_lo
        }
        _ => hart.csr_raw(index_by_name(hart, f.csr).unwrap_or(0)) & field_mask(f),
    }
}

/// Raw storage read by NAME (no computed overlay) — the helper `computed` recurses on.
fn csr_state_raw<H: PrivilegedHart>(hart: &H, name: &str) -> u64 {
    index_by_name(hart, name).map_or(0, |i| hart.csr_raw(i))
}

// ---- the permission model (RVP-CSR §1.1.1 + the enable gates) --------------------------

/// May an instruction at the current mode perform this access? The uniform model of
/// `schema/semantics.sexp`'s `csr-read`/`csr-write`: the address-map mode bits and the
/// read-only bits (RVP-CSR §1.1.1), the counter-enable gates (RVP-MACHINE §2.1.1.11,
/// RVP-SUPERVISOR §11.1.1.5), TM/STCE on stimecmp (§2.1.1.18, RVP-SSTC 12.1), and TVM on
/// satp in S (§2.1.1.6.6). A refused access is the illegal-instruction case.
pub fn permitted<H: PrivilegedHart>(
    hart: &H,
    address: u16,
    write: bool,
) -> Result<(), IllegalCsrAccess> {
    let refuse = |why: &'static str| Err(IllegalCsrAccess { address, why });
    if meta_by_name_addr(hart, address).is_none() {
        return refuse("an address the profile does not implement");
    }
    // The address-map conventions (RVP-CSR §1.1.1): csr[9:8] is the lowest privilege that
    // may access (00 U, 01 S, 11 M; 10 is the hypervisor level — not selected, D-NO-H),
    // and csr[11:10]=0b11 marks read-only.
    let lowest = (address >> 8) & 0b11;
    let required = match lowest {
        0b00 => PrivilegeMode::U,
        0b01 => PrivilegeMode::S,
        _ => PrivilegeMode::M, // 10 (hypervisor/VS) is unimplemented state: refuse below M
    };
    if hart.mode() < required {
        return refuse("the access is below the address's privilege level");
    }
    if write && (address >> 10) & 0b11 == 0b11 {
        return refuse("a write to a read-only address (csr[11:10] = 0b11)");
    }
    let name = meta_by_name_addr(hart, address).map(|m| m.name);
    match name {
        // The counter-enable gates: cycle/time/instret below M need mcounteren's CY/TM/IR
        // (bit positions: the pinned encoding.h's MCOUNTEREN_CY/TM/IR shifts), and in U
        // additionally scounteren's (RVP-SUPERVISOR §11.1.1.5). The counters keep
        // counting while gated — the gate is on ACCESS (§2.1.1.11).
        Some(n @ ("cycle" | "time" | "instret")) => {
            let bit = match n {
                "cycle" => COUNTEREN_CY,
                "time" => COUNTEREN_TM,
                _ => COUNTEREN_IR,
            };
            if hart.mode() < PrivilegeMode::M && (csr_state_raw(hart, "mcounteren") >> bit) & 1 == 0
            {
                return refuse("the counter is gated off by mcounteren below M");
            }
            if hart.mode() == PrivilegeMode::U
                && (csr_state_raw(hart, "scounteren") >> bit) & 1 == 0
            {
                return refuse("the counter is gated off by scounteren in U");
            }
        }
        // stimecmp: below M, mcounteren.TM gates it and menvcfg.STCE must be set
        // (RVP-SSTC 12.1: "an attempt to access stimecmp in a mode other than M-mode
        // raises an illegal-instruction exception" when STCE=0).
        Some("stimecmp")
            if hart.mode() < PrivilegeMode::M
                && (csr_state_raw(hart, "mcounteren") >> COUNTEREN_TM) & 1 == 0 =>
        {
            return refuse("stimecmp is gated off by mcounteren.TM below M");
        }
        Some("stimecmp")
            if hart.mode() < PrivilegeMode::M
                && (csr_state_raw(hart, "menvcfg") >> STCE) & 1 == 0 =>
        {
            return refuse("stimecmp is disabled by menvcfg.STCE below M");
        }
        // satp in S under TVM=1 (RVP-MACHINE §2.1.1.6.6; M is never gated).
        Some("satp")
            if hart.mode() == PrivilegeMode::S
                && (csr_state_raw(hart, "mstatus") >> TVM) & 1 == 1 =>
        {
            return refuse("satp access is trapped by mstatus.TVM in S");
        }
        _ => {}
    }
    Ok(())
}

fn meta_by_name_addr<H: PrivilegedHart>(hart: &H, address: u16) -> Option<&'static CsrMeta> {
    hart.csr_meta().iter().find(|m| m.address == address)
}

// ---- reads and writes through the model ------------------------------------------------

/// An architectural CSR READ (`csr-read`): the permission model, then the value — views
/// resolve to their underlying storage under the view's field mask, and computed fields
/// compute. The address a CSR instruction supplies is 12 bits by construction.
pub fn csr_read<H: PrivilegedHart>(hart: &H, address: u16) -> Result<u64, IllegalCsrAccess> {
    permitted(hart, address, false)?;
    let meta = meta_by_name_addr(hart, address).ok_or(IllegalCsrAccess {
        address,
        why: "unimplemented",
    })?;
    let owner = meta.view_of.unwrap_or(meta.name);
    let value = csr_state(hart, owner);
    if meta.view_of.is_some() {
        // A view exposes exactly its own named (non-WPRI) fields; the rest reads zero
        // (RVP-SUPERVISOR §11.1.1.1: the view is the subset). A view declaring NO
        // fields is a full-width shadow of its owner (the counter views' own
        // statements: "a read-only shadow of mcycle" — the subset rule cannot mean
        // "reads zero", or the shadow would never shadow; measured at P4-SYSTEM.5
        // slice a: the mask computed 0 and the counters would have read 0 forever).
        let mask: u64 = {
            let declared: u64 = hart
                .csr_fields()
                .iter()
                .filter(|f| f.csr == meta.name && f.discipline != FieldDiscipline::Wpri)
                .map(field_mask)
                .fold(0, |a, b| a | b);
            if declared == 0 {
                u64::MAX
            } else {
                declared
            }
        };
        let mut viewed = value & mask;
        for f in hart.csr_fields().iter().filter(|f| f.csr == meta.name) {
            if f.legalize == Some(Legalize::Computed) {
                viewed = (viewed & !field_mask(f)) | (computed(hart, f) & field_mask(f));
            }
        }
        Ok(viewed)
    } else {
        Ok(value)
    }
}

/// An architectural CSR WRITE (`csr-write`): the permission model, then the per-field
/// legalization from the descriptor's tables — WPRI preserves, WARL/WLRL apply their
/// `(legalize …)` rule, computed fields ignore the write. Views write through to the
/// underlying register under the view's fields.
pub fn csr_write<H: PrivilegedHart>(
    hart: &mut H,
    address: u16,
    value: u64,
) -> Result<(), IllegalCsrAccess> {
    permitted(hart, address, true)?;
    let meta = meta_by_name_addr(hart, address).ok_or(IllegalCsrAccess {
        address,
        why: "unimplemented",
    })?;
    let owner = meta.view_of.unwrap_or(meta.name);
    let index = index_by_name(hart, owner).ok_or(IllegalCsrAccess {
        address,
        why: "a view whose owner has no storage",
    })?;
    let old = hart.csr_raw(index);
    // The fields that judge this write: a view's own table; a storage CSR's own table.
    let table_name = meta.name;
    let mut table = hart
        .csr_fields()
        .iter()
        .filter(|f| f.csr == table_name)
        .peekable();
    if table.peek().is_none() {
        // An ATOMIC register (the descriptor declares no fields — a scratch, a tval):
        // the whole word is writable storage.
        hart.csr_write_raw(index, value);
        return Ok(());
    }
    let mut new = old;
    let mut covered = 0u64;
    for f in table {
        let mask = field_mask(f);
        covered |= mask;
        let incoming = (value & mask) >> f.bit_lo;
        let kept = (new & mask) >> f.bit_lo;
        let legal = match f.discipline {
            FieldDiscipline::Wpri => kept, // preserve
            FieldDiscipline::Warl | FieldDiscipline::Wlrl => match f.legalize {
                None | Some(Legalize::Computed) => kept,
                Some(Legalize::Any) => incoming,
                Some(Legalize::ReadOnly(_)) => kept,
                Some(Legalize::OneOf(set)) => {
                    if set.contains(&incoming) {
                        incoming
                    } else {
                        kept // an illegal value retains the old one (the laboratory's WARL)
                    }
                }
            },
        };
        new = (new & !mask) | (legal << f.bit_lo);
    }
    // Bits no field covers: a complete table accounts for every bit (the generator
    // refuses a holed one); anything uncovered is preserved rather than guessed.
    hart.csr_write_raw(index, (new & covered) | (old & !covered));
    Ok(())
}

// ---- trap delivery and xret -------------------------------------------------------------

/// The mstatus stack field positions — the pinned `encoding.h`'s masks (MSTATUS_SIE …),
/// the specification's figure 3 rendered as data there. xIE/xPIE/xPP per level.
const SIE: u8 = 1;
const SPIE: u8 = 5;
const SPP: u8 = 8;
const MIE: u8 = 3;
const MPIE: u8 = 7;
const MPP_LO: u8 = 11;
const MPRV: u8 = 17;
const TVM: u8 = 20;
const STCE: u8 = 63;
/// The counter-enable bit positions (the pinned encoding.h's MCOUNTEREN_CY/TM/IR shifts).
const COUNTEREN_CY: u8 = 0;
const COUNTEREN_TM: u8 = 1;
const COUNTEREN_IR: u8 = 2;

fn take(value: u64, bit: u8) -> u64 {
    (value >> bit) & 1
}

fn put(value: u64, bit: u8, v: u64) -> u64 {
    (value & !(1u64 << bit)) | ((v & 1) << bit)
}

/// Deliver a SYNCHRONOUS trap (`trap-deliver cause tval`; interrupt-caused delivery is
/// P4-SYSTEM.5's): the delegation selection (RVP-MACHINE §2.1.1.8 — medeleg bit `cause`
/// and an origin below M route to the S handler), then for the chosen x: xepc ← the
/// trapping instruction's own address, xcause ← cause, xtval ← tval, the xPIE/xIE/xPP
/// stack update (xPIE ← xIE; xIE ← 0; xPP ← the originating mode — §2.1.1.6.1), and
/// pc ← xtvec (§2.1.1.7, §11.1.1.2 — synchronous delivery uses BASE; the vectored mode
/// is the interrupt case's). Returns the handler's address.
pub fn trap_deliver<H: PrivilegedHart>(hart: &mut H, cause: u64, tval: u64, pc: u64) -> u64 {
    let origin = hart.mode();
    let delegated = origin < PrivilegeMode::M
        && cause < 64
        && (csr_state_raw(hart, "medeleg") >> cause) & 1 == 1;
    let to_s = delegated;
    let (epc, cause_r, tval_r, vec) = if to_s {
        ("sepc", "scause", "stval", "stvec")
    } else {
        ("mepc", "mcause", "mtval", "mtvec")
    };
    for (name, value) in [(epc, pc), (cause_r, cause), (tval_r, tval)] {
        if let Some(index) = index_by_name(hart, name) {
            hart.csr_write_raw(index, value);
        }
    }
    // The xIE/xPIE/xPP stack update — the machine's own writes (architected, never
    // legalization-gated), composed over mstatus's current bits.
    let mut mstatus = csr_state_raw(hart, "mstatus");
    if to_s {
        mstatus = put(mstatus, SPIE, take(mstatus, SIE));
        mstatus = put(mstatus, SIE, 0);
        mstatus = put(mstatus, SPP, u64::from(origin == PrivilegeMode::S));
    } else {
        mstatus = put(mstatus, MPIE, take(mstatus, MIE));
        mstatus = put(mstatus, MIE, 0);
        mstatus = (mstatus & !(0b11u64 << MPP_LO)) | (origin.code() << MPP_LO);
    }
    if let Some(index) = index_by_name(hart, "mstatus") {
        hart.csr_write_raw(index, mstatus);
    }
    hart.set_mode(if to_s {
        PrivilegeMode::S
    } else {
        PrivilegeMode::M
    });
    csr_state_raw(hart, vec) & !0b11 // xtvec.BASE (the low two bits are MODE)
}

/// The trap return (`xret x`; x is the level's architectural code — 3=M, 1=S): supposing
/// xPP holds y, xIE ← xPIE; the privilege mode ← y; xPIE ← 1; xPP ← the least-privileged
/// supported mode (U here); if y ≠ M then MPRV ← 0; and pc ← xepc (RVP-MACHINE
/// §2.1.1.6.1, §2.1.3.2). Legality was the instruction's own rule — this performs the
/// return. Returns the resume address.
pub fn xret<H: PrivilegedHart>(hart: &mut H, x: PrivilegeMode) -> u64 {
    let mut mstatus = csr_state_raw(hart, "mstatus");
    let (y, ie, pie) = if x == PrivilegeMode::M {
        ((mstatus >> MPP_LO) & 0b11, MIE, MPIE)
    } else {
        (take(mstatus, SPP), SIE, SPIE)
    };
    mstatus = put(mstatus, ie, take(mstatus, pie));
    mstatus = put(mstatus, pie, 1);
    if x == PrivilegeMode::M {
        mstatus &= !(0b11u64 << MPP_LO); // xPP <- U (the least-privileged supported mode)
    } else {
        mstatus = put(mstatus, SPP, 0);
    }
    let target = if y == 3 {
        PrivilegeMode::M
    } else if y == 1 {
        PrivilegeMode::S
    } else {
        PrivilegeMode::U
    };
    if target != PrivilegeMode::M {
        mstatus = put(mstatus, MPRV, 0);
    }
    if let Some(index) = index_by_name(hart, "mstatus") {
        hart.csr_write_raw(index, mstatus);
    }
    hart.set_mode(target);
    csr_state_raw(
        hart,
        if x == PrivilegeMode::M {
            "mepc"
        } else {
            "sepc"
        },
    )
}

#[cfg(test)]
mod tests;
