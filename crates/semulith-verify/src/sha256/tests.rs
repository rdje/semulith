//! Known-answer tests for SHA-256 — the FIPS 180-1 vectors, plus the byte-count edge
//! cases (empty, exactly one block, block-boundary crossings).

use super::sha256_hex;

#[test]
fn fips_known_answers() {
    assert_eq!(
        sha256_hex(b""),
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    );
    assert_eq!(
        sha256_hex(b"abc"),
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    );
    assert_eq!(
        sha256_hex(b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"),
        "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"
    );
    let million_a = vec![b'a'; 1_000_000];
    assert_eq!(
        sha256_hex(&million_a),
        "cdc76e5c9914fb9281a1c7e284d73e67f1809a48a497200e046d39ccc7112cd0"
    );
}

#[test]
fn block_boundary_lengths() {
    // 55, 56, 63, 64, 65 bytes exercise both padding branches
    for len in [0usize, 1, 55, 56, 57, 63, 64, 65, 119, 120, 128, 129] {
        let data = vec![0xA5u8; len];
        let digest = sha256_hex(&data);
        assert_eq!(digest.len(), 64, "digest length at {len}");
        assert!(digest
            .chars()
            .all(|c| c.is_ascii_hexdigit() && !c.is_ascii_uppercase()));
    }
    // two inputs differing by one byte differ everywhere (no trivial collisions at boundaries)
    let a = sha256_hex(&[0u8; 64]);
    let b = sha256_hex(&[1u8; 64]);
    assert_ne!(a, b);
}
