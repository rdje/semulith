//! Tests for the controlled fixtures — the boundary, driven directly, with no instruction
//! handler in sight (`docs/CPU_ENVIRONMENT.md` §4.1). Every environment obligation this
//! profile declares is exercised here: widths (OB-ENV-ACCESS-WIDTHS), fetch supply
//! (OB-ENV-FETCH-SUPPLY), code visibility (OB-CODE-VISIBILITY), misalignment and region
//! faults (OB-MISALIGN-DATA, OB-ADDRESS-SPACE), and the negative-fixture rule (§4.1.4) —
//! violations are contract reports, never target exceptions.

use semulith_core::env::{
    AccessWidth, BoundaryError, ContractViolation, Environment, Failure, Request, Response,
};

use super::{FlatMemory, ScriptedEnv};

const BASE: u64 = 0x1000;

fn load(width: AccessWidth, addr: u64) -> Request {
    Request::Load { width, addr }
}

fn store(width: AccessWidth, addr: u64, data: u64) -> Request {
    Request::Store { width, addr, data }
}

// ── FlatMemory: the positive contract ────────────────────────────────────────────────────

#[test]
fn aligned_load_store_round_trips_at_every_width() {
    let mut mem = FlatMemory::new(BASE, 0x100);
    for (i, (width, value)) in [
        (AccessWidth::B, 0x0000_0000_0000_00FF),
        (AccessWidth::H, 0x0000_0000_0000_FFFF),
        (AccessWidth::W, 0x0000_0000_FFFF_FFFF),
        (AccessWidth::D, 0xFFFF_FFFF_FFFF_FFFF),
    ]
    .into_iter()
    .enumerate()
    {
        // 8-byte-strided slots keep every address aligned at every width and the accesses
        // disjoint, so a width-confused fixture disagrees with the expected value.
        let addr = BASE + 0x40 + 8 * i as u64;
        assert_eq!(
            mem.request(store(width, addr, value)),
            Ok(Response::StoreDone),
            "store {width:?}"
        );
        assert_eq!(
            mem.request(load(width, addr)),
            Ok(Response::Load(value)),
            "load {width:?} returns exactly the width's bits"
        );
    }
}

#[test]
fn memory_is_little_endian() {
    let mut mem = FlatMemory::new(BASE, 0x100);
    mem.request(store(AccessWidth::D, BASE, 0x1122_3344_5566_7788))
        .expect("store");
    assert_eq!(
        &mem.bytes()[..8],
        &[0x88, 0x77, 0x66, 0x55, 0x44, 0x33, 0x22, 0x11],
        "REQ-D-ENDIAN: least significant byte at the lowest address"
    );
    assert_eq!(
        mem.request(load(AccessWidth::B, BASE + 7)),
        Ok(Response::Load(0x11))
    );
}

#[test]
fn load_returns_raw_bits_without_extension() {
    // REQ-D-LOAD-EXT's extension is the instruction layer's job; the boundary returns
    // raw bits. A byte with the top bit set must come back as 0x80, not 0xFFFF...80.
    let mut mem = FlatMemory::new(BASE, 0x100);
    mem.load_image(0x20, &[0x80]);
    assert_eq!(
        mem.request(load(AccessWidth::B, BASE + 0x20)),
        Ok(Response::Load(0x80))
    );
}

#[test]
fn store_writes_only_the_low_bits_of_the_value() {
    let mut mem = FlatMemory::new(BASE, 0x100);
    mem.request(store(AccessWidth::B, BASE + 1, 0xDEAD_BEEF))
        .expect("store");
    assert_eq!(&mem.bytes()[..4], &[0x00, 0xEF, 0x00, 0x00]);
}

#[test]
fn fetch_returns_the_word_and_only_requested_fetches_are_counted() {
    let mut mem = FlatMemory::new(BASE, 0x100);
    mem.load_image(0, &[0x13, 0x05, 0xB5, 0x02]); // ADDI x10, x11, 43 — arbitrary bytes
    assert_eq!(mem.fetch_count(), 0);
    assert_eq!(
        mem.request(Request::Fetch { addr: BASE }),
        Ok(Response::Fetch(0x02B5_0513))
    );
    assert_eq!(
        mem.fetch_count(),
        1,
        "one request, one fetch — no extraneous fetch"
    );
}

#[test]
fn fetch_re_reads_memory_so_stores_are_immediately_visible() {
    // OB-CODE-VISIBILITY: the model re-reads on every fetch, so self-modifying code is
    // visible at once (a legal choice, not an architectural guarantee).
    let mut mem = FlatMemory::new(BASE, 0x100);
    mem.load_image(0, &[0x00, 0x00, 0x00, 0x00]);
    assert_eq!(
        mem.request(Request::Fetch { addr: BASE }),
        Ok(Response::Fetch(0))
    );
    mem.request(store(AccessWidth::W, BASE, 0x0000_0067)) // JALR x0, 0(x0)
        .expect("store");
    assert_eq!(
        mem.request(Request::Fetch { addr: BASE }),
        Ok(Response::Fetch(0x67)),
        "the second fetch must see the store"
    );
}

// ── FlatMemory: the failure contract ─────────────────────────────────────────────────────

#[test]
fn misaligned_accesses_report_misaligned_not_data() {
    let mut mem = FlatMemory::new(BASE, 0x100);
    for request in [
        load(AccessWidth::H, BASE + 1),
        load(AccessWidth::W, BASE + 2),
        store(AccessWidth::D, BASE + 4 + 1, 0),
        Request::Fetch { addr: BASE + 2 },
    ] {
        assert_eq!(
            mem.request(request),
            Err(BoundaryError::Target(Failure::Misaligned)),
            "{request:?}"
        );
    }
}

#[test]
fn accesses_outside_the_region_report_access_fault() {
    let mut mem = FlatMemory::new(BASE, 0x10);
    assert_eq!(
        mem.request(load(AccessWidth::B, BASE - 1)),
        Err(BoundaryError::Target(Failure::AccessFault)),
        "below the region"
    );
    assert_eq!(
        mem.request(load(AccessWidth::B, BASE + 0x10)),
        Err(BoundaryError::Target(Failure::AccessFault)),
        "one byte past the end"
    );
    assert_eq!(
        mem.request(Request::Fetch { addr: BASE + 0x0C }),
        Ok(Response::Fetch(0)),
        "the last whole word of the region is inside"
    );
}

#[test]
fn region_edge_is_exact() {
    // 0x0C bytes: the aligned D at 0x08 crosses the end (0x08 + 8 > 0x0C); the W fits.
    let mut mem = FlatMemory::new(BASE, 0x0C);
    assert_eq!(
        mem.request(load(AccessWidth::D, BASE + 0x08)),
        Err(BoundaryError::Target(Failure::AccessFault)),
        "aligned but crossing the end"
    );
    assert_eq!(
        mem.request(load(AccessWidth::W, BASE + 0x08)),
        Ok(Response::Load(0)),
        "the last W fits exactly"
    );
    let mut mem = FlatMemory::new(BASE, 0x10);
    assert_eq!(
        mem.request(load(AccessWidth::B, BASE + 0x0F)),
        Ok(Response::Load(0)),
        "the last byte of the region is inside"
    );
}

// ── ScriptedEnv: the scripted and negative contract ──────────────────────────────────────

#[test]
fn scripted_conversation_succeeds_and_ends_exactly() {
    let mut env = ScriptedEnv::new(vec![
        (
            Request::Fetch { addr: BASE },
            Ok(Response::Fetch(0x0000_0063)),
        ),
        (
            load(AccessWidth::D, BASE + 0x100),
            Err(Failure::AccessFault), // scripted faults are environment answers
        ),
    ]);
    assert_eq!(
        env.request(Request::Fetch { addr: BASE }),
        Ok(Response::Fetch(0x63))
    );
    assert_eq!(
        env.request(load(AccessWidth::D, BASE + 0x100)),
        Err(BoundaryError::Target(Failure::AccessFault))
    );
    assert_eq!(
        env.remaining(),
        0,
        "the conversation ended exactly where scripted"
    );
}

#[test]
fn wrong_request_is_a_contract_violation_not_a_target_failure() {
    let scripted = load(AccessWidth::W, BASE);
    let mut env = ScriptedEnv::new(vec![(scripted, Ok(Response::Load(0)))]);
    let arrived = store(AccessWidth::W, BASE, 0);
    assert_eq!(
        env.request(arrived),
        Err(BoundaryError::Violation(
            ContractViolation::ResponseMismatch { scripted, arrived }
        )),
        "§4.1.4: the fixture must report a contract violation, not invent data and\n\
         not dress the mismatch up as a target exception"
    );
}

#[test]
fn request_after_the_script_is_a_contract_violation() {
    let mut env = ScriptedEnv::new(vec![]);
    assert_eq!(
        env.request(Request::Fetch { addr: BASE }),
        Err(BoundaryError::Violation(ContractViolation::ScriptExhausted))
    );
}
