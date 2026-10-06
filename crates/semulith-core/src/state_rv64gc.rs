//! GENERATED — do not edit (OWN-03). Regenerate with `python3 scripts/gen_state.py`;
//! drift between this module and the descriptor it derives from is refused by the
//! STATE-GEN doctrine (`scripts/check_state_gen.sh`).
//! Source: `profiles/rv64gc-lab-v0/state.sexp` (sha256 `59282e4fac25443c6c4560503b7c5587c02fe1be74c42b5e1d972f1ed8904792`).
//!
//! Architectural state of `rv64gc-lab-v0`: 32 × 64-bit integer registers (x0
//! hardwired), the program counter, the current privilege mode, the 32 × 64-bit
//! floating-point file (FLEN=64 — P4-SYSTEM.7 slice b), and the 33 CSRs of
//! D-CSR-SET with their per-field WPRI/WARL/WLRL tables as DATA — legalization is
//! applied by the engine at lowering (P4-SYSTEM.2 slices c2/d), never by hand here.

/// Number of integer registers in the architectural register file. — REQ-D-XLEN
pub const INTEGER_COUNT: usize = 32;

/// Number of floating-point registers (f0–f31) at FLEN=64 — D is selected, the
/// LP64D ABI (RVI-D §21.1.2; P4-SYSTEM.7 slice b).
pub const FP_COUNT: usize = 32;

/// x1 — alias view, "return address for a call" (software convention).
pub const RETURN_ADDRESS_FOR_A_CALL: u8 = 1;

/// x2 — alias view, "stack pointer" (software convention).
pub const STACK_POINTER: u8 = 2;

/// x5 — alias view, "alternate link register" (software convention).
pub const ALTERNATE_LINK_REGISTER: u8 = 5;

/// The current privilege mode (hart state, not a CSR): the engine's vocabulary type
/// — the codes are the architecture's own (the pinned encoding.h's PRV_U/PRV_S/PRV_M).
pub use crate::privilege::{CsrMeta, FieldDiscipline, FieldMeta, Legalize, PrivilegeMode};

/// Number of CSRs with storage (26 of 33; the rest are views —
/// a view declares no storage: sstatus/sie/sip restrict mstatus/mie/mip, the
/// counters shadow their machine registers).
pub const CSR_COUNT: usize = 26;

/// Storage index of `mhartid` (address 0xf14).
pub const CSR_MHARTID: usize = 0;

/// Storage index of `misa` (address 0x301).
pub const CSR_MISA: usize = 1;

/// Storage index of `mstatus` (address 0x300).
pub const CSR_MSTATUS: usize = 2;

/// Storage index of `mtvec` (address 0x305).
pub const CSR_MTVEC: usize = 3;

/// Storage index of `medeleg` (address 0x302).
pub const CSR_MEDELEG: usize = 4;

/// Storage index of `mideleg` (address 0x303).
pub const CSR_MIDELEG: usize = 5;

/// Storage index of `mie` (address 0x304).
pub const CSR_MIE: usize = 6;

/// Storage index of `mip` (address 0x344).
pub const CSR_MIP: usize = 7;

/// Storage index of `mscratch` (address 0x340).
pub const CSR_MSCRATCH: usize = 8;

/// Storage index of `mepc` (address 0x341).
pub const CSR_MEPC: usize = 9;

/// Storage index of `mcause` (address 0x342).
pub const CSR_MCAUSE: usize = 10;

/// Storage index of `mtval` (address 0x343).
pub const CSR_MTVAL: usize = 11;

/// Storage index of `menvcfg` (address 0x30a).
pub const CSR_MENVCFG: usize = 12;

/// Storage index of `mcounteren` (address 0x306).
pub const CSR_MCOUNTEREN: usize = 13;

/// Storage index of `mcycle` (address 0xb00).
pub const CSR_MCYCLE: usize = 14;

/// Storage index of `minstret` (address 0xb02).
pub const CSR_MINSTRET: usize = 15;

/// Storage index of `stvec` (address 0x105).
pub const CSR_STVEC: usize = 16;

/// Storage index of `sscratch` (address 0x140).
pub const CSR_SSCRATCH: usize = 17;

/// Storage index of `sepc` (address 0x141).
pub const CSR_SEPC: usize = 18;

/// Storage index of `scause` (address 0x142).
pub const CSR_SCAUSE: usize = 19;

/// Storage index of `stval` (address 0x143).
pub const CSR_STVAL: usize = 20;

/// Storage index of `scounteren` (address 0x106).
pub const CSR_SCOUNTEREN: usize = 21;

/// Storage index of `satp` (address 0x180).
pub const CSR_SATP: usize = 22;

/// Storage index of `stimecmp` (address 0x14d).
pub const CSR_STIMECMP: usize = 23;

/// Storage index of `fflags` (address 0x001).
pub const CSR_FFLAGS: usize = 24;

/// Storage index of `frm` (address 0x002).
pub const CSR_FRM: usize = 25;

/// The architectural register file, program counter, current mode and CSR storage:
/// fixed-width inline, no heap (RUST-03).
pub struct ArchitecturalState {
    regs: [u64; INTEGER_COUNT],
    pc: u64,
    mode: PrivilegeMode,
    csrs: [u64; CSR_COUNT],
    fregs: [u64; FP_COUNT],
    tlb: crate::translation::Tlb,
    reservation: crate::reservation::Reservation,
    hart_state: crate::wait::HartState,
}

impl ArchitecturalState {
    /// Fresh state at the reset for `entry`: the architectural resets of RVP-MACHINE
    /// §2.1.4, the laboratory's stated values everywhere §2.1.4 says UNSPECIFIED (the
    /// descriptor's reset rows are the authority).
    #[must_use]
    pub fn zeroed_at(entry: u64) -> Self {
        Self {
            regs: [0; INTEGER_COUNT],
            pc: entry,
            mode: PrivilegeMode::M,
            csrs: [
                0x0,
                0x800000000014112d,
                0xa00000000,
                0x0,
                0x0,
                0x0,
                0x0,
                0x0,
                0x0,
                0x0,
                0x0,
                0x0,
                0x0,
                0x0,
                0x0,
                0x0,
                0x0,
                0x0,
                0x0,
                0x0,
                0x0,
                0x0,
                0x0,
                0x0,
                0x0,
                0x0,
            ],
            fregs: [0; FP_COUNT],
            tlb: crate::translation::Tlb::new(),
            reservation: crate::reservation::Reservation::new(),
            hart_state: crate::wait::HartState::new(),
        }
    }

    /// The laboratory reset (REQ-D-ENTRY-STATE, OB-ENV-RESET).
    pub fn reset(&mut self, entry: u64) {
        *self = Self::zeroed_at(entry);
    }

    /// Architectural read of `x(index)`. x0 reads as 0, always (RVI-RV32I §1.1.1).
    #[must_use]
    pub fn read_x(&self, index: u8) -> u64 {
        if index == 0 {
            0
        } else {
            self.regs[index as usize]
        }
    }

    /// Architectural write of `x(index)`; a write to x0 is discarded.
    pub fn write_x(&mut self, index: u8, value: u64) {
        if index != 0 {
            self.regs[index as usize] = value;
        }
    }

    /// Architectural read of `f(index)` — the raw FLEN bits (NaN-boxing is the
    /// instructions' write-side discipline, P4-SYSTEM.7; the file carries raw
    /// storage only).
    #[must_use]
    pub fn read_f(&self, index: u8) -> u64 {
        self.fregs[index as usize]
    }

    /// Architectural write of `f(index)` — no hardwired zero in the FP file.
    pub fn write_f(&mut self, index: u8, value: u64) {
        self.fregs[index as usize] = value;
    }

    /// The program counter (RVI-RV32I §1.1.1).
    #[must_use]
    pub fn pc(&self) -> u64 {
        self.pc
    }

    /// Set the program counter (a control transfer's target).
    pub fn set_pc(&mut self, value: u64) {
        self.pc = value;
    }

    /// The current privilege mode (hart state — RVP-INTRO; reset M, §2.1.4).
    #[must_use]
    pub fn mode(&self) -> PrivilegeMode {
        self.mode
    }

    /// Set the current privilege mode (trap delivery and xret's concern — the
    /// engine's, slice (d); accessors stay raw here).
    pub fn set_mode(&mut self, mode: PrivilegeMode) {
        self.mode = mode;
    }

    /// Raw read of CSR storage by index. The permission model, view masking and
    /// WARL/WLRL legalization are the ENGINE's, applied at lowering (slices c2/d) —
    /// this layer stores and reports, it never adjudicates.
    #[must_use]
    pub fn read_csr(&self, index: usize) -> u64 {
        self.csrs[index]
    }

    /// Raw write of CSR storage by index; same layering as [`Self::read_csr`].
    pub fn write_csr(&mut self, index: usize, value: u64) {
        self.csrs[index] = value;
    }

    /// The storage index of a csr ADDRESS, or None for an address the profile does
    /// not implement (an access there is the permission model's illegal instruction,
    /// decided by the engine).
    #[must_use]
    pub fn csr_index(address: u16) -> Option<usize> {
        match address {
            0xf14 => Some(CSR_MHARTID),
            0x301 => Some(CSR_MISA),
            0x300 => Some(CSR_MSTATUS),
            0x305 => Some(CSR_MTVEC),
            0x302 => Some(CSR_MEDELEG),
            0x303 => Some(CSR_MIDELEG),
            0x304 => Some(CSR_MIE),
            0x344 => Some(CSR_MIP),
            0x340 => Some(CSR_MSCRATCH),
            0x341 => Some(CSR_MEPC),
            0x342 => Some(CSR_MCAUSE),
            0x343 => Some(CSR_MTVAL),
            0x30a => Some(CSR_MENVCFG),
            0x306 => Some(CSR_MCOUNTEREN),
            0xb00 => Some(CSR_MCYCLE),
            0xb02 => Some(CSR_MINSTRET),
            0x105 => Some(CSR_STVEC),
            0x140 => Some(CSR_SSCRATCH),
            0x141 => Some(CSR_SEPC),
            0x142 => Some(CSR_SCAUSE),
            0x143 => Some(CSR_STVAL),
            0x106 => Some(CSR_SCOUNTEREN),
            0x180 => Some(CSR_SATP),
            0x14d => Some(CSR_STIMECMP),
            0x001 => Some(CSR_FFLAGS),
            0x002 => Some(CSR_FRM),
            _ => None,
        }
    }
}

/// Every CSR the profile implements, in descriptor order (views included) — the
/// engine's `CsrMeta` vocabulary (`crate::privilege`), the descriptor's data.
pub const CSR_ELEMENTS: [CsrMeta; 33] = [
    CsrMeta {
        name: "mhartid",
        address: 0xf14,
        view_of: None,
    },
    CsrMeta {
        name: "misa",
        address: 0x301,
        view_of: None,
    },
    CsrMeta {
        name: "mstatus",
        address: 0x300,
        view_of: None,
    },
    CsrMeta {
        name: "mtvec",
        address: 0x305,
        view_of: None,
    },
    CsrMeta {
        name: "medeleg",
        address: 0x302,
        view_of: None,
    },
    CsrMeta {
        name: "mideleg",
        address: 0x303,
        view_of: None,
    },
    CsrMeta {
        name: "mie",
        address: 0x304,
        view_of: None,
    },
    CsrMeta {
        name: "mip",
        address: 0x344,
        view_of: None,
    },
    CsrMeta {
        name: "mscratch",
        address: 0x340,
        view_of: None,
    },
    CsrMeta {
        name: "mepc",
        address: 0x341,
        view_of: None,
    },
    CsrMeta {
        name: "mcause",
        address: 0x342,
        view_of: None,
    },
    CsrMeta {
        name: "mtval",
        address: 0x343,
        view_of: None,
    },
    CsrMeta {
        name: "menvcfg",
        address: 0x30a,
        view_of: None,
    },
    CsrMeta {
        name: "mcounteren",
        address: 0x306,
        view_of: None,
    },
    CsrMeta {
        name: "mcycle",
        address: 0xb00,
        view_of: None,
    },
    CsrMeta {
        name: "minstret",
        address: 0xb02,
        view_of: None,
    },
    CsrMeta {
        name: "sstatus",
        address: 0x100,
        view_of: Some("mstatus"),
    },
    CsrMeta {
        name: "stvec",
        address: 0x105,
        view_of: None,
    },
    CsrMeta {
        name: "sscratch",
        address: 0x140,
        view_of: None,
    },
    CsrMeta {
        name: "sepc",
        address: 0x141,
        view_of: None,
    },
    CsrMeta {
        name: "scause",
        address: 0x142,
        view_of: None,
    },
    CsrMeta {
        name: "stval",
        address: 0x143,
        view_of: None,
    },
    CsrMeta {
        name: "sie",
        address: 0x104,
        view_of: Some("mie"),
    },
    CsrMeta {
        name: "sip",
        address: 0x144,
        view_of: Some("mip"),
    },
    CsrMeta {
        name: "scounteren",
        address: 0x106,
        view_of: None,
    },
    CsrMeta {
        name: "satp",
        address: 0x180,
        view_of: None,
    },
    CsrMeta {
        name: "stimecmp",
        address: 0x14d,
        view_of: None,
    },
    CsrMeta {
        name: "cycle",
        address: 0xc00,
        view_of: Some("mcycle"),
    },
    CsrMeta {
        name: "time",
        address: 0xc01,
        view_of: Some("mcycle"),
    },
    CsrMeta {
        name: "instret",
        address: 0xc02,
        view_of: Some("minstret"),
    },
    CsrMeta {
        name: "fflags",
        address: 0x001,
        view_of: None,
    },
    CsrMeta {
        name: "frm",
        address: 0x002,
        view_of: None,
    },
    CsrMeta {
        name: "fcsr",
        address: 0x003,
        view_of: Some("fflags, frm"),
    },
];

/// The per-field tables of the 33 CSRs, in descriptor order — the
/// legalization rules as DATA (`crate::privilege::FieldMeta`); the engine applies
/// them at lowering, this table never adjudicates.
pub const CSR_FIELDS: [FieldMeta; 136] = [
    FieldMeta {
        csr: "mhartid",
        name: "hart_id",
        bit_hi: 63,
        bit_lo: 0,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::ReadOnly(0)),
        reset: 0,
    },
    FieldMeta {
        csr: "misa",
        name: "MXL",
        bit_hi: 63,
        bit_lo: 62,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::ReadOnly(2)),
        reset: 2,
    },
    FieldMeta {
        csr: "misa",
        name: "Extensions",
        bit_hi: 25,
        bit_lo: 0,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::ReadOnly(1315117)),
        reset: 1315117,
    },
    FieldMeta {
        csr: "misa",
        name: "wpri_61_26",
        bit_hi: 61,
        bit_lo: 26,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mstatus",
        name: "SIE",
        bit_hi: 1,
        bit_lo: 1,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mstatus",
        name: "MIE",
        bit_hi: 3,
        bit_lo: 3,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mstatus",
        name: "SPIE",
        bit_hi: 5,
        bit_lo: 5,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mstatus",
        name: "MPIE",
        bit_hi: 7,
        bit_lo: 7,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mstatus",
        name: "SPP",
        bit_hi: 8,
        bit_lo: 8,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mstatus",
        name: "VS",
        bit_hi: 10,
        bit_lo: 9,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::ReadOnly(0)),
        reset: 0,
    },
    FieldMeta {
        csr: "mstatus",
        name: "MPP",
        bit_hi: 12,
        bit_lo: 11,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1, 3])),
        reset: 0,
    },
    FieldMeta {
        csr: "mstatus",
        name: "FS",
        bit_hi: 14,
        bit_lo: 13,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1, 2, 3])),
        reset: 0,
    },
    FieldMeta {
        csr: "mstatus",
        name: "XS",
        bit_hi: 16,
        bit_lo: 15,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::ReadOnly(0)),
        reset: 0,
    },
    FieldMeta {
        csr: "mstatus",
        name: "MPRV",
        bit_hi: 17,
        bit_lo: 17,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mstatus",
        name: "SUM",
        bit_hi: 18,
        bit_lo: 18,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mstatus",
        name: "MXR",
        bit_hi: 19,
        bit_lo: 19,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mstatus",
        name: "TVM",
        bit_hi: 20,
        bit_lo: 20,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mstatus",
        name: "TW",
        bit_hi: 21,
        bit_lo: 21,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mstatus",
        name: "TSR",
        bit_hi: 22,
        bit_lo: 22,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mstatus",
        name: "wpri_31_23",
        bit_hi: 31,
        bit_lo: 23,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mstatus",
        name: "UXL",
        bit_hi: 33,
        bit_lo: 32,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::ReadOnly(2)),
        reset: 2,
    },
    FieldMeta {
        csr: "mstatus",
        name: "SXL",
        bit_hi: 35,
        bit_lo: 34,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::ReadOnly(2)),
        reset: 2,
    },
    FieldMeta {
        csr: "mstatus",
        name: "SBE",
        bit_hi: 36,
        bit_lo: 36,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::ReadOnly(0)),
        reset: 0,
    },
    FieldMeta {
        csr: "mstatus",
        name: "MBE",
        bit_hi: 37,
        bit_lo: 37,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::ReadOnly(0)),
        reset: 0,
    },
    FieldMeta {
        csr: "mstatus",
        name: "GVA",
        bit_hi: 38,
        bit_lo: 38,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::ReadOnly(0)),
        reset: 0,
    },
    FieldMeta {
        csr: "mstatus",
        name: "MPV",
        bit_hi: 39,
        bit_lo: 39,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::ReadOnly(0)),
        reset: 0,
    },
    FieldMeta {
        csr: "mstatus",
        name: "wpri_62_40",
        bit_hi: 62,
        bit_lo: 40,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mstatus",
        name: "SD",
        bit_hi: 63,
        bit_lo: 63,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::Computed),
        reset: 0,
    },
    FieldMeta {
        csr: "mstatus",
        name: "wpri_0",
        bit_hi: 0,
        bit_lo: 0,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mstatus",
        name: "wpri_2",
        bit_hi: 2,
        bit_lo: 2,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mstatus",
        name: "wpri_4",
        bit_hi: 4,
        bit_lo: 4,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mstatus",
        name: "wpri_6",
        bit_hi: 6,
        bit_lo: 6,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mtvec",
        name: "BASE",
        bit_hi: 63,
        bit_lo: 2,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::Any),
        reset: 0,
    },
    FieldMeta {
        csr: "mtvec",
        name: "MODE",
        bit_hi: 1,
        bit_lo: 0,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "medeleg",
        name: "cause_0_to_10",
        bit_hi: 10,
        bit_lo: 0,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::Any),
        reset: 0,
    },
    FieldMeta {
        csr: "medeleg",
        name: "cause_11",
        bit_hi: 11,
        bit_lo: 11,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::ReadOnly(0)),
        reset: 0,
    },
    FieldMeta {
        csr: "medeleg",
        name: "cause_12_to_15",
        bit_hi: 15,
        bit_lo: 12,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::Any),
        reset: 0,
    },
    FieldMeta {
        csr: "medeleg",
        name: "cause_16",
        bit_hi: 16,
        bit_lo: 16,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::ReadOnly(0)),
        reset: 0,
    },
    FieldMeta {
        csr: "medeleg",
        name: "cause_17",
        bit_hi: 17,
        bit_lo: 17,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "medeleg",
        name: "cause_18_to_20",
        bit_hi: 20,
        bit_lo: 18,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::Any),
        reset: 0,
    },
    FieldMeta {
        csr: "medeleg",
        name: "wpri_63_21",
        bit_hi: 63,
        bit_lo: 21,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mideleg",
        name: "SSIP",
        bit_hi: 1,
        bit_lo: 1,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mideleg",
        name: "STIP",
        bit_hi: 5,
        bit_lo: 5,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mideleg",
        name: "SEIP",
        bit_hi: 9,
        bit_lo: 9,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mideleg",
        name: "wpri_0_0",
        bit_hi: 0,
        bit_lo: 0,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mideleg",
        name: "wpri_4_2",
        bit_hi: 4,
        bit_lo: 2,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mideleg",
        name: "wpri_8_6",
        bit_hi: 8,
        bit_lo: 6,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mideleg",
        name: "wpri_63_10",
        bit_hi: 63,
        bit_lo: 10,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mie",
        name: "SSIE",
        bit_hi: 1,
        bit_lo: 1,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mie",
        name: "MSIE",
        bit_hi: 3,
        bit_lo: 3,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mie",
        name: "STIE",
        bit_hi: 5,
        bit_lo: 5,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mie",
        name: "MTIE",
        bit_hi: 7,
        bit_lo: 7,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mie",
        name: "SEIE",
        bit_hi: 9,
        bit_lo: 9,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mie",
        name: "MEIE",
        bit_hi: 11,
        bit_lo: 11,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mie",
        name: "wpri_0_0",
        bit_hi: 0,
        bit_lo: 0,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mie",
        name: "wpri_2_2",
        bit_hi: 2,
        bit_lo: 2,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mie",
        name: "wpri_4_4",
        bit_hi: 4,
        bit_lo: 4,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mie",
        name: "wpri_6_6",
        bit_hi: 6,
        bit_lo: 6,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mie",
        name: "wpri_8_8",
        bit_hi: 8,
        bit_lo: 8,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mie",
        name: "wpri_10_10",
        bit_hi: 10,
        bit_lo: 10,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mie",
        name: "wpri_63_12",
        bit_hi: 63,
        bit_lo: 12,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mip",
        name: "SSIP",
        bit_hi: 1,
        bit_lo: 1,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mip",
        name: "MSIP",
        bit_hi: 3,
        bit_lo: 3,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::ReadOnly(0)),
        reset: 0,
    },
    FieldMeta {
        csr: "mip",
        name: "STIP",
        bit_hi: 5,
        bit_lo: 5,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::Computed),
        reset: 0,
    },
    FieldMeta {
        csr: "mip",
        name: "MTIP",
        bit_hi: 7,
        bit_lo: 7,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::ReadOnly(0)),
        reset: 0,
    },
    FieldMeta {
        csr: "mip",
        name: "SEIP",
        bit_hi: 9,
        bit_lo: 9,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mip",
        name: "MEIP",
        bit_hi: 11,
        bit_lo: 11,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::ReadOnly(0)),
        reset: 0,
    },
    FieldMeta {
        csr: "mip",
        name: "wpri_0_0",
        bit_hi: 0,
        bit_lo: 0,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mip",
        name: "wpri_2_2",
        bit_hi: 2,
        bit_lo: 2,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mip",
        name: "wpri_4_4",
        bit_hi: 4,
        bit_lo: 4,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mip",
        name: "wpri_6_6",
        bit_hi: 6,
        bit_lo: 6,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mip",
        name: "wpri_8_8",
        bit_hi: 8,
        bit_lo: 8,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mip",
        name: "wpri_10_10",
        bit_hi: 10,
        bit_lo: 10,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mip",
        name: "wpri_63_12",
        bit_hi: 63,
        bit_lo: 12,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mepc",
        name: "value_63_2",
        bit_hi: 63,
        bit_lo: 2,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::Any),
        reset: 0,
    },
    FieldMeta {
        csr: "mepc",
        name: "value_1",
        bit_hi: 1,
        bit_lo: 1,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mepc",
        name: "value_0",
        bit_hi: 0,
        bit_lo: 0,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::ReadOnly(0)),
        reset: 0,
    },
    FieldMeta {
        csr: "mcause",
        name: "Interrupt",
        bit_hi: 63,
        bit_lo: 63,
        discipline: FieldDiscipline::Wlrl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mcause",
        name: "code_62_0",
        bit_hi: 62,
        bit_lo: 0,
        discipline: FieldDiscipline::Wlrl,
        legalize: Some(Legalize::Any),
        reset: 0,
    },
    FieldMeta {
        csr: "menvcfg",
        name: "STCE",
        bit_hi: 63,
        bit_lo: 63,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "menvcfg",
        name: "wpri_62_0",
        bit_hi: 62,
        bit_lo: 0,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "mcounteren",
        name: "CY",
        bit_hi: 0,
        bit_lo: 0,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mcounteren",
        name: "TM",
        bit_hi: 1,
        bit_lo: 1,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mcounteren",
        name: "IR",
        bit_hi: 2,
        bit_lo: 2,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "mcounteren",
        name: "HPM31_3",
        bit_hi: 31,
        bit_lo: 3,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::ReadOnly(0)),
        reset: 0,
    },
    FieldMeta {
        csr: "mcounteren",
        name: "wpri_63_32",
        bit_hi: 63,
        bit_lo: 32,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "sstatus",
        name: "SIE",
        bit_hi: 1,
        bit_lo: 1,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "sstatus",
        name: "SPIE",
        bit_hi: 5,
        bit_lo: 5,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "sstatus",
        name: "SPP",
        bit_hi: 8,
        bit_lo: 8,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "sstatus",
        name: "VS",
        bit_hi: 10,
        bit_lo: 9,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::ReadOnly(0)),
        reset: 0,
    },
    FieldMeta {
        csr: "sstatus",
        name: "FS",
        bit_hi: 14,
        bit_lo: 13,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1, 2, 3])),
        reset: 0,
    },
    FieldMeta {
        csr: "sstatus",
        name: "XS",
        bit_hi: 16,
        bit_lo: 15,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::ReadOnly(0)),
        reset: 0,
    },
    FieldMeta {
        csr: "sstatus",
        name: "SUM",
        bit_hi: 18,
        bit_lo: 18,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "sstatus",
        name: "MXR",
        bit_hi: 19,
        bit_lo: 19,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "sstatus",
        name: "UXL",
        bit_hi: 33,
        bit_lo: 32,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::ReadOnly(2)),
        reset: 2,
    },
    FieldMeta {
        csr: "sstatus",
        name: "SD",
        bit_hi: 63,
        bit_lo: 63,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::Computed),
        reset: 0,
    },
    FieldMeta {
        csr: "sstatus",
        name: "wpri_0_0",
        bit_hi: 0,
        bit_lo: 0,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "sstatus",
        name: "wpri_4_2",
        bit_hi: 4,
        bit_lo: 2,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "sstatus",
        name: "wpri_7_6",
        bit_hi: 7,
        bit_lo: 6,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "sstatus",
        name: "wpri_12_11",
        bit_hi: 12,
        bit_lo: 11,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "sstatus",
        name: "wpri_17_17",
        bit_hi: 17,
        bit_lo: 17,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "sstatus",
        name: "wpri_31_20",
        bit_hi: 31,
        bit_lo: 20,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "sstatus",
        name: "wpri_62_34",
        bit_hi: 62,
        bit_lo: 34,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "stvec",
        name: "BASE",
        bit_hi: 63,
        bit_lo: 2,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::Any),
        reset: 0,
    },
    FieldMeta {
        csr: "stvec",
        name: "MODE",
        bit_hi: 1,
        bit_lo: 0,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "sepc",
        name: "value_63_2",
        bit_hi: 63,
        bit_lo: 2,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::Any),
        reset: 0,
    },
    FieldMeta {
        csr: "sepc",
        name: "value_1",
        bit_hi: 1,
        bit_lo: 1,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "sepc",
        name: "value_0",
        bit_hi: 0,
        bit_lo: 0,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::ReadOnly(0)),
        reset: 0,
    },
    FieldMeta {
        csr: "scause",
        name: "Interrupt",
        bit_hi: 63,
        bit_lo: 63,
        discipline: FieldDiscipline::Wlrl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "scause",
        name: "code_62_0",
        bit_hi: 62,
        bit_lo: 0,
        discipline: FieldDiscipline::Wlrl,
        legalize: Some(Legalize::Any),
        reset: 0,
    },
    FieldMeta {
        csr: "sie",
        name: "SSIE",
        bit_hi: 1,
        bit_lo: 1,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "sie",
        name: "STIE",
        bit_hi: 5,
        bit_lo: 5,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "sie",
        name: "SEIE",
        bit_hi: 9,
        bit_lo: 9,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "sie",
        name: "wpri_0_0",
        bit_hi: 0,
        bit_lo: 0,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "sie",
        name: "wpri_4_2",
        bit_hi: 4,
        bit_lo: 2,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "sie",
        name: "wpri_8_6",
        bit_hi: 8,
        bit_lo: 6,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "sie",
        name: "wpri_63_10",
        bit_hi: 63,
        bit_lo: 10,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "sip",
        name: "SSIP",
        bit_hi: 1,
        bit_lo: 1,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "sip",
        name: "STIP",
        bit_hi: 5,
        bit_lo: 5,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::Computed),
        reset: 0,
    },
    FieldMeta {
        csr: "sip",
        name: "SEIP",
        bit_hi: 9,
        bit_lo: 9,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::Computed),
        reset: 0,
    },
    FieldMeta {
        csr: "sip",
        name: "wpri_0_0",
        bit_hi: 0,
        bit_lo: 0,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "sip",
        name: "wpri_4_2",
        bit_hi: 4,
        bit_lo: 2,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "sip",
        name: "wpri_8_6",
        bit_hi: 8,
        bit_lo: 6,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "sip",
        name: "wpri_63_10",
        bit_hi: 63,
        bit_lo: 10,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "scounteren",
        name: "CY",
        bit_hi: 0,
        bit_lo: 0,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "scounteren",
        name: "TM",
        bit_hi: 1,
        bit_lo: 1,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "scounteren",
        name: "IR",
        bit_hi: 2,
        bit_lo: 2,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 1])),
        reset: 0,
    },
    FieldMeta {
        csr: "scounteren",
        name: "HPM31_3",
        bit_hi: 31,
        bit_lo: 3,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::ReadOnly(0)),
        reset: 0,
    },
    FieldMeta {
        csr: "scounteren",
        name: "wpri_63_32",
        bit_hi: 63,
        bit_lo: 32,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "satp",
        name: "MODE",
        bit_hi: 63,
        bit_lo: 60,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::OneOf(&[0, 8])),
        reset: 0,
    },
    FieldMeta {
        csr: "satp",
        name: "ASID",
        bit_hi: 59,
        bit_lo: 44,
        discipline: FieldDiscipline::Wlrl,
        legalize: Some(Legalize::Any),
        reset: 0,
    },
    FieldMeta {
        csr: "satp",
        name: "PPN",
        bit_hi: 43,
        bit_lo: 0,
        discipline: FieldDiscipline::Wlrl,
        legalize: Some(Legalize::Any),
        reset: 0,
    },
    FieldMeta {
        csr: "fflags",
        name: "flags_4_0",
        bit_hi: 4,
        bit_lo: 0,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::Any),
        reset: 0,
    },
    FieldMeta {
        csr: "fflags",
        name: "wpri_63_5",
        bit_hi: 63,
        bit_lo: 5,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
    FieldMeta {
        csr: "frm",
        name: "frm_2_0",
        bit_hi: 2,
        bit_lo: 0,
        discipline: FieldDiscipline::Warl,
        legalize: Some(Legalize::Any),
        reset: 0,
    },
    FieldMeta {
        csr: "frm",
        name: "wpri_63_3",
        bit_hi: 63,
        bit_lo: 3,
        discipline: FieldDiscipline::Wpri,
        legalize: None,
        reset: 0,
    },
];

/// The engine's privileged-state surface (`crate::privilege::PrivilegedHart`),
/// implemented over this module's storage and tables — the trait's rules are the
/// engine's; the data they read is the descriptor's.
impl crate::privilege::PrivilegedHart for ArchitecturalState {
    fn mode(&self) -> PrivilegeMode {
        self.mode
    }
    fn set_mode(&mut self, mode: PrivilegeMode) {
        self.mode = mode;
    }
    fn csr_raw(&self, index: usize) -> u64 {
        self.csrs[index]
    }
    fn csr_write_raw(&mut self, index: usize, value: u64) {
        self.csrs[index] = value;
    }
    fn csr_index(&self, address: u16) -> Option<usize> {
        Self::csr_index(address)
    }
    fn csr_meta(&self) -> &'static [CsrMeta] {
        &CSR_ELEMENTS
    }
    fn csr_fields(&self) -> &'static [FieldMeta] {
        &CSR_FIELDS
    }
    fn tlb(&mut self) -> &mut crate::translation::Tlb {
        &mut self.tlb
    }
    fn reservation(&mut self) -> &mut crate::reservation::Reservation {
        &mut self.reservation
    }
    fn hart_state(&mut self) -> &mut crate::wait::HartState {
        &mut self.hart_state
    }
    fn fregs(&mut self) -> &mut [u64; 32] {
        &mut self.fregs
    }
}

/// SEM-08: the hidden-state census, re-earned for the privileged state — carried as
/// data so the interpreter, the gate report and the reviewer read the same sentence.
pub struct HiddenStateCandidate {
    pub candidate: &'static str,
    pub present: bool,
    pub why: &'static str,
}

pub struct HiddenStateCensus {
    pub question: &'static str,
    pub answer: &'static str,
    pub candidates: &'static [HiddenStateCandidate],
    pub consequence: &'static str,
}

pub const HIDDEN_STATE_CENSUS: HiddenStateCensus = HiddenStateCensus {
    question: "Is there any state, not listed above, that can influence a future supported observation? (SEM-08, catalog C02 — re-earned for the privileged state)",
    answer: "No — for this stage of the profile, with every candidate below accounted for and the later slices that reopen them named.",
    candidates: &[
        HiddenStateCandidate {
            candidate: "the 33 CSRs of D-CSR-SET",
            present: true,
            why: "declared above, each with its per-field discipline table; the privilege stack (xIE/xPIE/xPP) is mstatus FIELDS, architected state, not hidden state",
        },
        HiddenStateCandidate {
            candidate: "the current privilege mode",
            present: true,
            why: "declared as hart state above — it changes on trap delivery and xret and is readable nowhere as a register; without it the mode-matrix corpus could observe nothing",
        },
        HiddenStateCandidate {
            candidate: "reservation set (LR/SC)",
            present: true,
            why: "answered by P4-SYSTEM.4 slice (c): one reservation — (physical address, width, valid) of the most recent LR, the minimal conformant reservation set (exactly the accessed word's/doubleword's bytes, RVI-A §12.1.2), keyed on the PHYSICAL address (the aliasing latitude resolved to exact physical match, authority laboratory). Invalidation is exactly the spec's one-hart set: any LR replaces; any SC — success or failure, any address — clears; a trap does NOT invalidate (the SC's own trap included — the trap path is neither success nor failure). The deterministic SC policy (authority laboratory, decision 3): SC succeeds iff the reservation is valid ∧ physical address equal ∧ width equal, writing rs2's value and rd←0; otherwise it fails with rd←1 (the 'unspecified failure' code), writing nothing; it NEVER spuriously fails — one legal point of the architectural nondeterminism, chosen so exact-value expectations stay derivable (EVD-05). Misaligned atomics take the access-fault family by kind (5 for LR, 7 for SC/AMO — decision 6, reference-matched to the override's declared PMAs, the exception table's kind mapping). The reservation is a pure function of the hart's own history — invalid at reset, changed only by the hart's own LR/SC — so cold-reset re-execution stays trace-identical and a cold-restored (invalid) reservation is always a legal state",
        },
        HiddenStateCandidate {
            candidate: "floating-point registers f0-f31 and the fcsr behaviour",
            present: true,
            why: "answered by P4-SYSTEM.7 slice (b) after slice (a)'s qualification (SEMULITH-P4-0039, rustc_apfloat): the file is modelled — 32 x 64-bit (FLEN=64 with D, the LP64D ABI), declared above with its laboratory reset; mstatus.FS gates the FP instructions AND the fflags/frm/fcsr CSRs (four-state FS, reset 0 = Off, Dirty on any FP state write — Sail 0.14's dirty_fd_context measured; SD is the computed summary and follows); fflags is the sticky accrued-flags register (software-clearable); frm holds any 3-bit value (the FSRM sentence — slice (c1) corrected slice (b)'s WARL one-of 0..4), with the dyn/reserved-rm resolution stated; fcsr is the two-owner VIEW, composed by the engine from fflags[4:0] and frm[2:0] (the pre-slice single-owner resolution read 0 and refused writes — measured, fixed at root). Observation stays through the x-registers (decision 8): the file itself is never an expectations-vocabulary item",
        },
        HiddenStateCandidate {
            candidate: "environment state (mtime, interrupt sources, the time register's value)",
            present: true,
            why: "answered by P4-SYSTEM.5 slice (a) for the COUNTER-PROGRESS part: the laboratory declares the virtual-time domain — one tick per step boundary, retired or halted (authority laboratory, Zicntr §6.1's rate latitude; the domain IS the environment's supply, the contract wording .9's) — mcycle is the domain's storage, time views it, minstret counts genuinely; and by slice (b) for the PENDING/SOURCE-EVALUATION part (the (a)(b)(c) taken-rule with the global rule, the delegation mask and the fixed priorities, interrupt-caused delivery honoring both xtvec.MODEs). mtime/mtimecmp and the interrupt controllers stay memory-mapped ENVIRONMENT state, not CSRs (the .9 contract)",
        },
        HiddenStateCandidate {
            candidate: "PMP configuration",
            present: false,
            why: "PMP is excluded at v0 (D-NO-PMP)",
        },
        HiddenStateCandidate {
            candidate: "hypervisor state",
            present: false,
            why: "the hypervisor extension is excluded (D-NO-H)",
        },
        HiddenStateCandidate {
            candidate: "vector state (vtype, vl, vstart)",
            present: false,
            why: "V is not in this profile",
        },
        HiddenStateCandidate {
            candidate: "instruction-fetch cache state",
            present: false,
            why: "the model re-reads memory on every fetch (D-CODE-VISIBILITY) — a laboratory choice, not an absence of the possibility: Zifencei is declared AND bound (P4-SYSTEM.6 slice b), and the chapter's own latitude permits a caching hart regardless (visibility is guaranteed only after a FENCE.I), so the re-read choice stays laboratory policy and FENCE.I's nop is this unit's sanctioned implementation of the synchronization (the coherent/uncached-RAM latitude — nothing to flush). Re-answered in place at the bind, replacing rv64i's verbatim recording, which argued the choice from the extension's absence (true of rv64i, stale here)",
        },
        HiddenStateCandidate {
            candidate: "pending or partially committed effects",
            present: false,
            why: "at this stage every instruction completes or faults as a unit; fault priority and partial commits are P4-SYSTEM.8's, which reopens this candidate",
        },
        HiddenStateCandidate {
            candidate: "address-translation caches (TLBs)",
            present: true,
            why: "answered by P4-SYSTEM.3 slice (d): a minimal fully-specified TLB — 4 entries, fully-associative, FIFO replacement, ASID-tagged at ASIDLEN 16, keyed by 4 KiB page, G-bit entries retained across per-ASID and per-address+ASID fences (authority laboratory; the cache is a pure function of the hart's own history, so cold-reset re-execution stays trace-identical and a cold-restored cache is always a legal state)",
        },
        HiddenStateCandidate {
            candidate: "hart wait state (ACTIVE/WAITING)",
            present: true,
            why: "answered by P4-SYSTEM.5 slice (c): one hart-state bit — ACTIVE or WAITING (Sail 0.14's HART_WAITING precedent), cold-ACTIVE at reset. A legal WFI ENTERS waiting (the nop latitude recorded-not-taken — taking it would leave the leaf's acceptance untestable); while WAITING a step retires nothing, issues no fetch, advances the virtual-time domain one tick, and the step's head evaluates the wake — resume on a locally-enabled pending interrupt at any privilege level, regardless of the global enables and of mideleg (RVP-MACHINE §2.1.3.3's musts); on resume the taken-rule decides trap (xepc = the WFI's pc + 4) or pc + 4 continuation. The bit is a pure function of the hart's own history — changed only by the hart's own WFI/wake — so cold-reset re-execution stays trace-identical (the TLB/reservation determinism argument)",
        },
    ],
    consequence: "A complete snapshot for this stage is the integer file, pc, memory, the current mode, and the 33 CSRs' storage (mstatus/mie/mip once — views carry none). Each later slice reopens its named candidate: .3 translation state, .4 the reservation, .5 interrupt/counter progress, .7 the FP file, .8 partial effects, .9 the environment contract.",
};
