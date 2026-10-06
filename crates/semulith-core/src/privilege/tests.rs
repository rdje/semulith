//! The fixture hart and the machinery's test corpus (P4-SYSTEM.2 slice d).
//!
//! The fixture is a TEST DOUBLE: it carries the state document's facts in miniature (a
//! 17-CSR subset), so the machinery's rules are exercised without the generated module.
//! The addresses and bit positions are the pinned csrs.csv / encoding.h values (the
//! rv64gc-lab-v0 encoding-source pin); the generated table — derived from the tracked
//! descriptor at the flip — is the same data at full size.

use super::*;

/// The fixture's storage CSRs (views carry none); `stvec`/`scounteren`/`sepc`/`scause`/
/// `stval` are S-level storage registers at their own addresses, as the document has them.
const STORAGE: &[(&str, u16)] = &[
    ("mstatus", 0x300),
    ("misa", 0x301),
    ("medeleg", 0x302),
    ("mie", 0x304),
    ("mtvec", 0x305),
    ("mcounteren", 0x306),
    ("menvcfg", 0x30A),
    ("mscratch", 0x340),
    ("mepc", 0x341),
    ("mcause", 0x342),
    ("mtval", 0x343),
    ("mip", 0x344),
    ("mcycle", 0xB00),
    ("stimecmp", 0x14D),
    ("satp", 0x180),
    ("time", 0xC01),
    ("stvec", 0x105),
    ("scounteren", 0x106),
    ("sepc", 0x141),
    ("scause", 0x142),
    ("stval", 0x143),
    ("fflags", 0x001),
    ("frm", 0x002),
];

const fn f(
    csr: &'static str,
    name: &'static str,
    hi: u8,
    lo: u8,
    d: FieldDiscipline,
    l: Option<Legalize>,
) -> FieldMeta {
    // The field's declared reset rides in the legalize constant for the read-only rows
    // (UXL=2); the rest reset to 0, as the document declares.
    let reset = match l {
        Some(Legalize::ReadOnly(v)) => v,
        _ => 0,
    };
    FieldMeta {
        csr,
        name,
        bit_hi: hi,
        bit_lo: lo,
        discipline: d,
        legalize: l,
        reset,
    }
}

/// The fixture's field table: the fields the tests judge, with the document's shapes.
static FIELDS: &[FieldMeta] = &[
    f(
        "mstatus",
        "SIE",
        1,
        1,
        FieldDiscipline::Warl,
        Some(Legalize::OneOf(&[0, 1])),
    ),
    f(
        "mstatus",
        "MIE",
        3,
        3,
        FieldDiscipline::Warl,
        Some(Legalize::OneOf(&[0, 1])),
    ),
    f(
        "mstatus",
        "SPIE",
        5,
        5,
        FieldDiscipline::Warl,
        Some(Legalize::OneOf(&[0, 1])),
    ),
    f(
        "mstatus",
        "MPIE",
        7,
        7,
        FieldDiscipline::Warl,
        Some(Legalize::OneOf(&[0, 1])),
    ),
    f(
        "mstatus",
        "SPP",
        8,
        8,
        FieldDiscipline::Warl,
        Some(Legalize::OneOf(&[0, 1])),
    ),
    f(
        "mstatus",
        "MPP",
        12,
        11,
        FieldDiscipline::Warl,
        Some(Legalize::OneOf(&[0, 1, 3])),
    ),
    f(
        "mstatus",
        "FS",
        14,
        13,
        FieldDiscipline::Warl,
        Some(Legalize::OneOf(&[0, 1, 2, 3])),
    ),
    f(
        "mstatus",
        "XS",
        16,
        15,
        FieldDiscipline::Warl,
        Some(Legalize::ReadOnly(0)),
    ),
    f(
        "mstatus",
        "MPRV",
        17,
        17,
        FieldDiscipline::Warl,
        Some(Legalize::OneOf(&[0, 1])),
    ),
    f(
        "mstatus",
        "TVM",
        20,
        20,
        FieldDiscipline::Warl,
        Some(Legalize::OneOf(&[0, 1])),
    ),
    f(
        "mstatus",
        "TW",
        21,
        21,
        FieldDiscipline::Warl,
        Some(Legalize::OneOf(&[0, 1])),
    ),
    f(
        "mstatus",
        "TSR",
        22,
        22,
        FieldDiscipline::Warl,
        Some(Legalize::OneOf(&[0, 1])),
    ),
    f("mstatus", "wpri", 31, 23, FieldDiscipline::Wpri, None),
    f(
        "mstatus",
        "UXL",
        33,
        32,
        FieldDiscipline::Warl,
        Some(Legalize::ReadOnly(2)),
    ),
    f(
        "mstatus",
        "SD",
        63,
        63,
        FieldDiscipline::Warl,
        Some(Legalize::Computed),
    ),
    f(
        "mtvec",
        "MODE",
        1,
        0,
        FieldDiscipline::Warl,
        Some(Legalize::OneOf(&[0, 1])),
    ),
    f(
        "mtvec",
        "BASE",
        63,
        2,
        FieldDiscipline::Warl,
        Some(Legalize::Any),
    ),
    f(
        "satp",
        "PPN",
        43,
        0,
        FieldDiscipline::Warl,
        Some(Legalize::Any),
    ),
    f(
        "satp",
        "ASID",
        59,
        44,
        FieldDiscipline::Wlrl,
        Some(Legalize::Any),
    ),
    f(
        "satp",
        "MODE",
        63,
        60,
        FieldDiscipline::Warl,
        Some(Legalize::OneOf(&[0, 8])),
    ),
    f(
        "sstatus",
        "SIE",
        1,
        1,
        FieldDiscipline::Warl,
        Some(Legalize::OneOf(&[0, 1])),
    ),
    f(
        "sstatus",
        "SPIE",
        5,
        5,
        FieldDiscipline::Warl,
        Some(Legalize::OneOf(&[0, 1])),
    ),
    f(
        "sstatus",
        "SD",
        63,
        63,
        FieldDiscipline::Warl,
        Some(Legalize::Computed),
    ),
    f("sstatus", "wpri", 62, 0, FieldDiscipline::Wpri, None),
    // The FP CSRs (P4-SYSTEM.7 slice b; frm corrected at slice c1): the document's
    // shapes — fflags' accrued flags WARL-any, frm holding ANY 3-bit value (the FSRM
    // sentence), both WPRI above; fcsr declares no fields (the composition reads the
    // owners' tables).
    f(
        "fflags",
        "flags_4_0",
        4,
        0,
        FieldDiscipline::Warl,
        Some(Legalize::Any),
    ),
    f("fflags", "wpri", 63, 5, FieldDiscipline::Wpri, None),
    f(
        "frm",
        "frm_2_0",
        2,
        0,
        FieldDiscipline::Warl,
        Some(Legalize::Any),
    ),
    f("frm", "wpri", 63, 3, FieldDiscipline::Wpri, None),
];

struct Fixture {
    mode: PrivilegeMode,
    csrs: [u64; 23],
    fregs: [u64; 32],
    tlb: crate::translation::Tlb,
    reservation: crate::reservation::Reservation,
    hart_state: crate::wait::HartState,
}

static META: &[CsrMeta] = &[
    CsrMeta {
        name: "mstatus",
        address: 0x300,
        view_of: None,
    },
    CsrMeta {
        name: "misa",
        address: 0x301,
        view_of: None,
    },
    CsrMeta {
        name: "medeleg",
        address: 0x302,
        view_of: None,
    },
    CsrMeta {
        name: "mie",
        address: 0x304,
        view_of: None,
    },
    CsrMeta {
        name: "mtvec",
        address: 0x305,
        view_of: None,
    },
    CsrMeta {
        name: "mcounteren",
        address: 0x306,
        view_of: None,
    },
    CsrMeta {
        name: "menvcfg",
        address: 0x30A,
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
        name: "mip",
        address: 0x344,
        view_of: None,
    },
    CsrMeta {
        name: "mcycle",
        address: 0xB00,
        view_of: None,
    },
    CsrMeta {
        name: "stimecmp",
        address: 0x14D,
        view_of: None,
    },
    CsrMeta {
        name: "satp",
        address: 0x180,
        view_of: None,
    },
    CsrMeta {
        name: "time",
        address: 0xC01,
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
        name: "scounteren",
        address: 0x106,
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
        name: "cycle",
        address: 0xC00,
        view_of: Some("mcycle"),
    },
    CsrMeta {
        name: "instret",
        address: 0xC02,
        view_of: Some("mcycle"),
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

impl Fixture {
    fn at(mode: PrivilegeMode) -> Self {
        let mut h = Self {
            mode,
            csrs: [0; 23],
            fregs: [0; 32],
            tlb: crate::translation::Tlb::new(),
            reservation: crate::reservation::Reservation::new(),
            hart_state: crate::wait::HartState::new(),
        };
        // The document's reset: each field's declared reset, placed (the generated
        // module's zeroed_at composes exactly this).
        for f in FIELDS {
            let Some(i) = STORAGE.iter().position(|(n, _)| *n == f.csr) else {
                continue; // a view's field resets live in the owner's storage
            };
            let width = u64::from(f.bit_hi - f.bit_lo) + 1;
            let bits = if width >= 64 {
                u64::MAX
            } else {
                (1u64 << width) - 1
            };
            h.csrs[i] = (h.csrs[i] & !(bits << f.bit_lo)) | ((f.reset & bits) << f.bit_lo);
        }
        h
    }
}

impl PrivilegedHart for Fixture {
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
        STORAGE.iter().position(|(_, a)| *a == address)
    }
    fn csr_meta(&self) -> &'static [CsrMeta] {
        META
    }
    fn csr_fields(&self) -> &'static [FieldMeta] {
        FIELDS
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

fn index(name: &str) -> usize {
    STORAGE
        .iter()
        .position(|(n, _)| *n == name)
        .expect("fixture names it")
}

fn write_raw(h: &mut Fixture, name: &str, value: u64) {
    let i = index(name);
    h.csr_write_raw(i, value);
}

fn read_raw(h: &Fixture, name: &str) -> u64 {
    h.csr_raw(index(name))
}

// ---- the permission model ---------------------------------------------------------------

#[test]
fn address_map_mode_bits_and_read_only_bits() {
    let mut h = Fixture::at(PrivilegeMode::U);
    assert!(permitted(&h, 0x300, false).is_err()); // mstatus below M: illegal
    h.set_mode(PrivilegeMode::S);
    assert!(permitted(&h, 0x100, false).is_ok()); // sstatus in S: legal
    assert!(permitted(&h, 0x300, false).is_err()); // mstatus in S: illegal
    assert!(permitted(&h, 0xC00, true).is_err()); // cycle is read-only (csr[11:10]=11)
    h.set_mode(PrivilegeMode::M);
    assert!(permitted(&h, 0x300, false).is_ok());
    assert!(permitted(&h, 0x999, false).is_err()); // unimplemented address
    assert!(permitted(&h, 0x800, false).is_err()); // 0b10 space: hypervisor — not selected
}

#[test]
fn counter_gating_mcounteren_then_scounteren() {
    let mut h = Fixture::at(PrivilegeMode::S);
    assert!(csr_read(&h, 0xC00).is_err()); // gated off at reset
    write_raw(&mut h, "mcounteren", 0b001); // CY
    assert!(csr_read(&h, 0xC00).is_ok()); // S: mcounteren suffices
    h.set_mode(PrivilegeMode::U);
    assert!(csr_read(&h, 0xC00).is_err()); // U also needs scounteren
    write_raw(&mut h, "scounteren", 0b001);
    assert!(csr_read(&h, 0xC00).is_ok());
    h.set_mode(PrivilegeMode::M);
    assert!(csr_read(&h, 0xC00).is_ok()); // M is never gated
                                          // time and instret have their own bits
    h.set_mode(PrivilegeMode::S);
    assert!(csr_read(&h, 0xC01).is_err());
    write_raw(&mut h, "mcounteren", 0b001 | 0b010);
    assert!(csr_read(&h, 0xC01).is_ok());
    assert!(csr_read(&h, 0xC02).is_err());
}

#[test]
fn stimecmp_gated_by_tm_and_stce_below_m() {
    let mut h = Fixture::at(PrivilegeMode::S);
    assert!(csr_read(&h, 0x14D).is_err()); // TM=0
    write_raw(&mut h, "mcounteren", 0b010);
    assert!(csr_read(&h, 0x14D).is_err()); // STCE=0
    write_raw(&mut h, "menvcfg", 1 << 63); // STCE=1
    assert!(csr_read(&h, 0x14D).is_ok());
    h.set_mode(PrivilegeMode::M);
    assert!(csr_read(&h, 0x14D).is_ok()); // M is never gated
}

#[test]
fn satp_tvm_gates_s_never_m() {
    let mut h = Fixture::at(PrivilegeMode::S);
    assert!(csr_read(&h, 0x180).is_ok());
    write_raw(&mut h, "mstatus", 1 << 20); // TVM=1
    assert!(csr_read(&h, 0x180).is_err());
    h.set_mode(PrivilegeMode::M);
    assert!(csr_read(&h, 0x180).is_ok());
}

// ---- legalization ------------------------------------------------------------------------

#[test]
fn warl_one_of_and_read_only_and_wpri() {
    let mut h = Fixture::at(PrivilegeMode::M);
    csr_write(&mut h, 0x305, 0x2001).unwrap(); // mtvec: BASE 0x800, MODE vectored
    assert_eq!(read_raw(&h, "mtvec"), 0x2001);
    csr_write(&mut h, 0x305, 0x2).unwrap(); // MODE=2 is reserved: retains old
    assert_eq!(read_raw(&h, "mtvec") & 0b11, 0b01);
    // satp.MODE accepts Bare and Sv39 only (the laboratory's declared restriction)
    csr_write(&mut h, 0x180, 8u64 << 60).unwrap();
    assert_eq!(read_raw(&h, "satp") >> 60, 8);
    csr_write(&mut h, 0x180, 9u64 << 60).unwrap(); // Sv48: not in the set — retains
    assert_eq!(read_raw(&h, "satp") >> 60, 8);
    // UXL is read-only 2; the WPRI gap preserves zero on an all-ones write
    csr_write(&mut h, 0x300, u64::MAX).unwrap();
    let m = read_raw(&h, "mstatus");
    assert_eq!((m >> 32) & 0b11, 2);
    assert_eq!((m >> 23) & 0x1FF, 0, "WPRI preserved zero");
    assert_eq!(m >> 63, 0, "SD ignores the write (computed)");
}

// ---- views --------------------------------------------------------------------------------

#[test]
fn a_view_shares_storage_under_its_mask() {
    let mut h = Fixture::at(PrivilegeMode::M);
    csr_write(&mut h, 0x100, 0xFFFF_FFFF_FFFF_FFFF).unwrap(); // sstatus: all ones
    let m = read_raw(&h, "mstatus");
    assert_eq!(take(m, SIE), 1, "the view's SIE wrote through to mstatus");
    assert_eq!(
        take(m, MIE),
        0,
        "the view exposes no MIE — the bit stayed 0"
    );
    assert_eq!(take(m, TVM), 0, "the view exposes no TVM");
    let s = csr_read(&h, 0x100).unwrap();
    assert_eq!(
        s & !0x8000_0000_0000_0322u64,
        0,
        "the view masks to its own fields"
    );
}

// ---- trap delivery ------------------------------------------------------------------------

#[test]
fn trap_delivered_to_m_by_default() {
    let mut h = Fixture::at(PrivilegeMode::M);
    write_raw(&mut h, "mtvec", 0x8000_0100);
    let pc = trap_deliver(&mut h, 11, 0, 0x8000_0040); // M-mode ecall
    assert_eq!(pc, 0x8000_0100);
    assert_eq!(read_raw(&h, "mepc"), 0x8000_0040); // the instruction's OWN address
    assert_eq!(read_raw(&h, "mcause"), 11);
    assert_eq!(read_raw(&h, "mtval"), 0);
    let m = read_raw(&h, "mstatus");
    assert_eq!(take(m, MPIE), 0); // MIE was 0 before the trap
    assert_eq!(take(m, MIE), 0); // MIE <- 0 on entry
    assert_eq!((m >> MPP_LO) & 0b11, 3); // MPP <- M
    assert_eq!(h.mode(), PrivilegeMode::M);
}

#[test]
fn delegated_trap_lands_in_s() {
    let mut h = Fixture::at(PrivilegeMode::U);
    write_raw(&mut h, "medeleg", 1 << 8); // delegate user ecall
    write_raw(&mut h, "stvec", 0x8000_9000);
    write_raw(&mut h, "mstatus", 1 << MIE); // MIE=1 before the trap
    let pc = trap_deliver(&mut h, 8, 0, 0x8000_0008);
    assert_eq!(pc, 0x8000_9000);
    assert_eq!(read_raw(&h, "sepc"), 0x8000_0008);
    assert_eq!(read_raw(&h, "scause"), 8);
    let m = read_raw(&h, "mstatus");
    assert_eq!(take(m, SPIE), 0); // SPIE <- SIE (was 0)
    assert_eq!(take(m, SPP), 0); // origin was U
    assert_eq!(
        (m >> MPP_LO) & 0b11,
        0,
        "the M stack is untouched when delegating"
    );
    assert_eq!(h.mode(), PrivilegeMode::S);
    // and the same trap from M is NOT delegated
    let mut h = Fixture::at(PrivilegeMode::M);
    write_raw(&mut h, "medeleg", 1 << 8);
    write_raw(&mut h, "mtvec", 0x8000_0100);
    let pc = trap_deliver(&mut h, 8, 0, 0x8000_0008);
    assert_eq!(pc, 0x8000_0100);
    assert_eq!(read_raw(&h, "mcause"), 8);
    assert_eq!(h.mode(), PrivilegeMode::M);
}

// ---- xret -----------------------------------------------------------------------------------

#[test]
fn mret_pops_the_stack_and_clears_mprv() {
    let mut h = Fixture::at(PrivilegeMode::M);
    let mut mstatus = 3u64 << MPP_LO; // MPP = M
    mstatus |= 1 << MPIE | 1 << MPRV;
    write_raw(&mut h, "mstatus", mstatus);
    write_raw(&mut h, "mepc", 0x8000_0040);
    let pc = xret(&mut h, PrivilegeMode::M);
    assert_eq!(pc, 0x8000_0040);
    assert_eq!(h.mode(), PrivilegeMode::M); // y == M: no MPRV clear
    let m = read_raw(&h, "mstatus");
    assert_eq!((m >> MPP_LO) & 0b11, 0, "MPP <- U");
    assert_eq!(take(m, MPIE), 1);
    assert_eq!(take(m, MIE), 1); // MIE <- old MPIE
                                 // now MPP = S
    let mut h = Fixture::at(PrivilegeMode::M);
    write_raw(&mut h, "mstatus", 1u64 << MPP_LO | 1 << MPRV);
    write_raw(&mut h, "mepc", 0x8000_0044);
    let pc = xret(&mut h, PrivilegeMode::M);
    assert_eq!(pc, 0x8000_0044);
    assert_eq!(h.mode(), PrivilegeMode::S);
    assert_eq!(take(read_raw(&h, "mstatus"), MPRV), 0, "y != M clears MPRV");
}

#[test]
fn sret_pops_the_s_stack() {
    let mut h = Fixture::at(PrivilegeMode::S);
    write_raw(&mut h, "mstatus", 0); // SPP = U
    write_raw(&mut h, "sepc", 0x8000_0100);
    let pc = xret(&mut h, PrivilegeMode::S);
    assert_eq!(pc, 0x8000_0100);
    assert_eq!(h.mode(), PrivilegeMode::U);
}

// ---- computed fields ------------------------------------------------------------------------

#[test]
fn sd_is_the_fs_xs_vs_summary() {
    let mut h = Fixture::at(PrivilegeMode::M);
    assert_eq!(csr_read(&h, 0x300).unwrap() >> 63, 0);
    write_raw(&mut h, "mstatus", 0b11 << 13); // FS = Dirty
    assert_eq!(csr_read(&h, 0x300).unwrap() >> 63, 1, "SD computes from FS");
}

// ---- the floating-point state gate and the two-owner view (P4-SYSTEM.7 slice b) -----------

/// The fixture's mstatus starts with FS=Off, as the document's reset row declares.
fn set_fs(h: &mut Fixture, value: u64) {
    let old = read_raw(h, "mstatus");
    write_raw(h, "mstatus", (old & !(0b11 << 13)) | (value << 13));
}

#[test]
fn fs_off_makes_the_fp_csrs_illegal_in_every_mode() {
    let mut h = Fixture::at(PrivilegeMode::M);
    assert_eq!(fs(&h), 0, "the document's reset: FS=Off");
    for mode in [PrivilegeMode::M, PrivilegeMode::S, PrivilegeMode::U] {
        h.set_mode(mode);
        for (addr, name) in [(0x001u16, "fflags"), (0x002, "frm"), (0x003, "fcsr")] {
            assert!(
                permitted(&h, addr, false).is_err(),
                "{name} read at FS=Off, mode {mode:?}"
            );
            assert!(
                permitted(&h, addr, true).is_err(),
                "{name} write at FS=Off, mode {mode:?}"
            );
            assert!(csr_read(&h, addr).is_err(), "{name} csr_read at FS=Off");
        }
    }
}

#[test]
fn fs_initial_clean_dirty_all_open_the_fp_csrs() {
    let mut h = Fixture::at(PrivilegeMode::M);
    for value in [1u64, 2, 3] {
        set_fs(&mut h, value);
        assert!(fp_enabled(&h));
        for addr in [0x001u16, 0x002, 0x003] {
            assert!(
                permitted(&h, addr, false).is_ok(),
                "FS={value} opens {addr:#x}"
            );
            assert!(permitted(&h, addr, true).is_ok());
        }
    }
    set_fs(&mut h, 0);
    assert!(!fp_enabled(&h));
    assert!(
        csr_read(&h, 0x001).is_err(),
        "the gate closes again at FS=Off"
    );
}

#[test]
fn fcsr_read_composes_the_two_owners() {
    let mut h = Fixture::at(PrivilegeMode::M);
    set_fs(&mut h, 1);
    csr_write(&mut h, 0x001, 0x1F).unwrap(); // fflags = all five flags
    csr_write(&mut h, 0x002, 0x3).unwrap(); // frm = RDN
    assert_eq!(
        csr_read(&h, 0x003).unwrap(),
        0x1F | (3 << 5),
        "fflags[4:0] with frm[2:0] above"
    );
    assert_eq!(
        csr_state(&h, "fcsr"),
        0x7F,
        "the machine's own read composes too"
    );
    // The owners' WPRI bits are never view content.
    csr_write(&mut h, 0x001, u64::MAX).unwrap();
    assert_eq!(csr_read(&h, 0x003).unwrap(), 0x1F | (3 << 5));
}

#[test]
fn fcsr_write_splits_back_into_the_owners() {
    let mut h = Fixture::at(PrivilegeMode::M);
    set_fs(&mut h, 1);
    csr_write(&mut h, 0x003, 0x5F).unwrap(); // frm=2, flags=0x1F
    assert_eq!(csr_read(&h, 0x001).unwrap(), 0x1F);
    assert_eq!(csr_read(&h, 0x002).unwrap(), 0x2);
    // frm holds ANY 3-bit value — "FSRM … writing a new value obtained from the three
    // least-significant bits of integer register rs1 into frm" (RVI-F §20.1.1): slice 7
    // lands (111 in frm is a dynamic RESERVED rounding mode, reachable by construction);
    // the fflags slice lands; bits 63:8 drop (WPRI).
    csr_write(&mut h, 0x003, u64::MAX).unwrap();
    assert_eq!(
        csr_read(&h, 0x002).unwrap(),
        0x7,
        "frm slice 7 lands: no legalization"
    );
    assert_eq!(csr_read(&h, 0x001).unwrap(), 0x1F);
    assert_eq!(csr_read(&h, 0x003).unwrap(), 0x1F | (7 << 5));
    // frm's own address stores the three low bits too; the rest drop (WPRI).
    csr_write(&mut h, 0x002, 0xE).unwrap();
    assert_eq!(
        csr_read(&h, 0x002).unwrap(),
        0x6,
        "the three low bits of the write, at the owner too"
    );
}

#[test]
fn fp_csr_writes_mark_fs_dirty_and_sd_follows() {
    let mut h = Fixture::at(PrivilegeMode::M);
    set_fs(&mut h, 1); // Initial
    csr_write(&mut h, 0x001, 0x01).unwrap();
    assert_eq!(
        fs(&h),
        3,
        "Sail's write_fcsr dirties the context (fdext_regs.sail:455)"
    );
    assert_eq!(
        csr_read(&h, 0x300).unwrap() >> 63,
        1,
        "SD is the computed summary"
    );
    set_fs(&mut h, 2); // Clean
    csr_write(&mut h, 0x003, 0x00).unwrap();
    assert_eq!(fs(&h), 3, "an fcsr write dirties too");
}

#[test]
fn mark_fp_dirty_is_the_f_write_discipline() {
    let mut h = Fixture::at(PrivilegeMode::M);
    set_fs(&mut h, 1);
    let before = read_raw(&h, "mstatus") & !(0b11 << 13);
    mark_fp_dirty(&mut h);
    assert_eq!(fs(&h), 3);
    assert_eq!(
        csr_read(&h, 0x300).unwrap() >> 63,
        1,
        "SD computes from FS=Dirty"
    );
    // The rest of mstatus is untouched.
    assert_eq!(read_raw(&h, "mstatus") & !(0b11 << 13), before);
}
