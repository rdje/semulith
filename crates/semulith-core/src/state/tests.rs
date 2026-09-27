//! Tests for the generated architectural state (`P1-LAB.3`).
//!
//! The acceptance criteria, each re-derived against the generated code:
//!
//! 1. **Catalog C02 — aliases are views, not copies.** Writing through one name must be
//!    visible through every other view of the same storage, in both directions
//!    (alias→index and index→alias), for every register, not only the named three.
//! 2. **x0 is hardwired zero.** A write is discarded; a read yields 0; no other register
//!    is affected (RVI-RV32I §1.1.1, the descriptor's x0 statement).
//! 3. **REQ-D-ENTRY-STATE / OB-ENV-RESET.** Reset: x1..x31 = 0 (a laboratory
//!    declaration), pc = the entry address the environment supplies.
//! 4. **RUST-03.** Fixed-width inline storage: 33 × 8 bytes on the stack, no heap; the
//!    accessors take references and return values, so a per-access allocation is not
//!    possible in this API by construction — the size assertion is the re-derivation.
//! 5. **SEM-08.** The hidden-state census rides along as data: every candidate checked,
//!    none present, the answer and consequence recorded verbatim from the descriptor.

use super::*;

/// A distinct, index-dependent value: `(i + 1) * 0x0101_0101_0101_0101`, so a confused
/// register (off by one, aliased storage) yields a different value everywhere.
fn pattern(index: u8) -> u64 {
    u64::from(index.wrapping_add(1)).wrapping_mul(0x0101_0101_0101_0101)
}

// ── C02: aliases are views over one storage ──────────────────────────────────────────────

#[test]
fn alias_write_is_visible_through_every_view() {
    // The three ISA-chapter-named registers, both directions.
    for (alias, index) in [
        (RETURN_ADDRESS_FOR_A_CALL, 1),
        (STACK_POINTER, 2),
        (ALTERNATE_LINK_REGISTER, 5),
    ] {
        let mut s = ArchitecturalState::zeroed_at(0);
        s.write_x(alias, 0xDEAD_BEEF);
        assert_eq!(s.read_x(index), 0xDEAD_BEEF, "alias→x{index}");
        let mut s = ArchitecturalState::zeroed_at(0);
        s.write_x(index, 0xC0FF_EE00);
        assert_eq!(s.read_x(alias), 0xC0FF_EE00, "x{index}→alias");
    }
}

#[test]
fn one_storage_means_every_view_agrees() {
    // Write a distinct value into every register through the raw index, then read every
    // register back through the raw index; a second storage (a copied alias file, say)
    // would show up as a disagreement here or in the alias test above.
    let mut s = ArchitecturalState::zeroed_at(0);
    for i in 0..INTEGER_COUNT as u8 {
        s.write_x(i, pattern(i));
    }
    for i in 0..INTEGER_COUNT as u8 {
        let want = if i == 0 { 0 } else { pattern(i) };
        assert_eq!(s.read_x(i), want, "x{i}");
    }
    // The named views see the same storage.
    assert_eq!(s.read_x(RETURN_ADDRESS_FOR_A_CALL), pattern(1));
    assert_eq!(s.read_x(STACK_POINTER), pattern(2));
    assert_eq!(s.read_x(ALTERNATE_LINK_REGISTER), pattern(5));
}

// ── x0: hardwired zero ───────────────────────────────────────────────────────────────────

#[test]
fn write_to_x0_is_discarded_and_read_yields_zero() {
    let mut s = ArchitecturalState::zeroed_at(0);
    s.write_x(0, u64::MAX);
    assert_eq!(
        s.read_x(0),
        0,
        "x0 must read as 0 even immediately after a write"
    );
    s.write_x(7, 123);
    s.write_x(0, 456);
    assert_eq!(
        s.read_x(7),
        123,
        "a discarded x0 write must not disturb other registers"
    );
    // Even after every other register holds a value, x0 stays 0.
    for i in 1..INTEGER_COUNT as u8 {
        s.write_x(i, pattern(i));
    }
    assert_eq!(s.read_x(0), 0);
}

// ── REQ-D-ENTRY-STATE / OB-ENV-RESET ─────────────────────────────────────────────────────

#[test]
fn reset_zeroes_x1_to_x31_and_sets_pc_to_entry() {
    let mut s = ArchitecturalState::zeroed_at(0x1000);
    for i in 1..INTEGER_COUNT as u8 {
        s.write_x(i, u64::MAX);
    }
    s.set_pc(0x7777);
    s.reset(0x8000_0000);
    for i in 1..INTEGER_COUNT as u8 {
        assert_eq!(s.read_x(i), 0, "x{i} after reset");
    }
    assert_eq!(s.pc(), 0x8000_0000, "pc = the declared entry address");
    assert_eq!(s.read_x(0), 0);
}

#[test]
fn zeroed_at_is_the_reset_state() {
    let entry = 0x1234_5678_9ABC_DEF0;
    let fresh = ArchitecturalState::zeroed_at(entry);
    for i in 1..INTEGER_COUNT as u8 {
        assert_eq!(fresh.read_x(i), 0, "x{i}");
    }
    assert_eq!(fresh.pc(), entry);
    assert_eq!(fresh.read_x(0), 0);
}

#[test]
fn pc_round_trips() {
    let mut s = ArchitecturalState::zeroed_at(0);
    s.set_pc(0xFFFF_FFFF_0000_0000);
    assert_eq!(s.pc(), 0xFFFF_FFFF_0000_0000);
}

// ── RUST-03: fixed-width inline storage, no per-access allocation ────────────────────────

#[test]
fn state_is_33_words_inline() {
    // 32 registers + pc, all u64, no padding possible between two u64 fields and no
    // pointer indirection: this is the whole allocation footprint of the state.
    assert_eq!(core::mem::size_of::<ArchitecturalState>(), 33 * 8);
}

// ── Inspection metadata, generated from the descriptor ───────────────────────────────────

#[test]
fn elements_enumerate_the_whole_file_in_descriptor_order() {
    assert_eq!(ELEMENTS.len(), 33);
    assert_eq!(ELEMENTS[0].name, "x0");
    assert_eq!(ELEMENTS[31].name, "x31");
    assert_eq!(ELEMENTS[32].name, "pc");
    let integers = &ELEMENTS[..32];
    let specials = &ELEMENTS[32..];
    assert!(integers
        .iter()
        .all(|e| e.class == StateClass::IntegerRegister));
    assert!(specials
        .iter()
        .all(|e| e.class == StateClass::SpecialRegister));
    assert!(ELEMENTS.iter().all(|e| e.width_bits == 64));
    assert!(ELEMENTS.iter().all(|e| !e.source.is_empty()));
}

#[test]
fn roles_attach_only_where_the_isa_chapter_names_them() {
    assert_eq!(
        ELEMENTS[0].role, None,
        "x0 has no ABI role; it is hardwired zero"
    );
    assert_eq!(ELEMENTS[1].role, Some("return address for a call"));
    assert_eq!(ELEMENTS[2].role, Some("stack pointer"));
    assert_eq!(ELEMENTS[5].role, Some("alternate link register"));
    let named = |e: &StateElement| e.role.is_some();
    assert_eq!(
        ELEMENTS[..32].iter().filter(|e| named(e)).count(),
        3,
        "exactly the three the descriptor records — the rest of the ABI is a\n\
                software calling convention the profile deliberately does not carry"
    );
    assert_eq!(ELEMENTS[32].role, None, "pc has no alias");
}

// ── SEM-08: the hidden-state census, carried as data ─────────────────────────────────────

#[test]
fn census_records_every_candidate_checked_and_none_present() {
    assert_eq!(HIDDEN_STATE_CENSUS.candidates.len(), 7);
    assert!(HIDDEN_STATE_CENSUS
        .candidates
        .iter()
        .all(|c| !c.present && !c.why.is_empty()));
    assert!(
        HIDDEN_STATE_CENSUS.answer.starts_with("No"),
        "the census answer is the profile's universal claim — it must be recorded, not assumed"
    );
    assert!(!HIDDEN_STATE_CENSUS.consequence.is_empty());
}
