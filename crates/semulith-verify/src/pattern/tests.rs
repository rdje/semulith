//! Tests for the pattern subset — the two tracked schema patterns plus the refusal arms.

use super::{compile, is_match};

#[test]
fn tracks_the_requirement_id_pattern() {
    let p = compile("^[A-Za-z][A-Za-z0-9._:/-]*$").expect("compiles");
    for ok in [
        "SYN16-ADD-001",
        "EV-SYN16-ADD",
        "OB-ENV-FETCH-SUPPLY",
        "a",
        "REQ-D-XLEN",
    ] {
        assert!(p.is_match(ok), "{ok} must match");
    }
    for bad in ["", "1ABC", "has space", "-lead", "percent%sign"] {
        assert!(!p.is_match(bad), "{bad:?} must not match");
    }
    // '_' '-' ':' are all class members ([A-Za-z0-9._:/-]); space is not
    assert!(p.is_match("under_score"));
    assert!(p.is_match("trail-"));
    assert!(p.is_match("colon:inside"));
}

#[test]
fn tracks_the_sha256_pattern() {
    let p = compile("^[0-9a-f]{64}$").expect("compiles");
    assert!(p.is_match(&"a".repeat(64)));
    assert!(p.is_match(&"0123456789abcdef".repeat(4)));
    for bad in [
        "",
        &"a".repeat(63),
        &"a".repeat(65),
        &"A".repeat(64),
        &"g".repeat(64),
    ] {
        assert!(!p.is_match(bad), "len {} must not match", bad.len());
    }
}

#[test]
fn search_semantics_unanchored_patterns_match_anywhere() {
    assert!(is_match("b+c", "abbbc").unwrap());
    assert!(!(is_match("b+c", "ac").unwrap()));
    assert!(is_match("a", "cba").unwrap());
    // an anchored pattern does not
    assert!(!(is_match("^b", "ab").unwrap()));
    assert!(is_match("^b", "ba").unwrap());
    assert!(is_match("a$", "ba").unwrap());
    assert!(!(is_match("a$", "ab").unwrap()));
}

#[test]
fn classes_support_ranges_negation_and_edge_literals() {
    assert!(is_match("^[0-9]+$", "123").unwrap());
    assert!(is_match("^[^0-9]+$", "abc").unwrap());
    assert!(!(is_match("^[^0-9]+$", "a1c").unwrap()));
    // '-' at the edges is a literal, not a range operator
    assert!(is_match("^[a-]$", "-").unwrap());
    assert!(!(is_match("^[a-]$", "b").unwrap()));
    assert!(is_match("^[-a]$", "-").unwrap());
    // escaped ']' inside a class
    assert!(is_match("^[\\]a]$", "]").unwrap());
    assert!(is_match("^[\\]a]$", "a").unwrap());
}

#[test]
fn quantifiers_cover_star_plus_opt_and_repetitions() {
    assert!(is_match("^ab*$", "a").unwrap());
    assert!(is_match("^ab*$", "abbb").unwrap());
    assert!(!(is_match("^ab+$", "a").unwrap()));
    assert!(is_match("^ab?$", "ab").unwrap());
    assert!(is_match("^ab?$", "a").unwrap());
    assert!(!(is_match("^ab?$", "abb").unwrap()));
    assert!(is_match("^a{2,4}$", "aa").unwrap());
    assert!(is_match("^a{2,4}$", "aaaa").unwrap());
    assert!(!(is_match("^a{2,4}$", "aaaaa").unwrap()));
    assert!(!(is_match("^a{2,4}$", "a").unwrap()));
    assert!(is_match("^a{3}$", "aaa").unwrap());
    assert!(!(is_match("^a{3}$", "aa").unwrap()));
    assert!(is_match("^a{2,}$", "aaaaaa").unwrap());
    assert!(!(is_match("^a{2,}$", "a").unwrap()));
}

#[test]
fn greedy_matching_backtracks_to_let_the_rest_match() {
    // classic backtracking case: .* must give back so the final literal can match
    assert!(is_match("^a*a$", "aaa").unwrap());
    assert!(is_match("^[a-z]*z$", "abcz").unwrap());
}

#[test]
fn refuses_everything_outside_the_subset_by_name() {
    let cases = [
        ("^a|b$", "alternation"),
        ("^(ab)$", "groups"),
        ("^a.c$", "'.'"),
        ("^a*?$", "lazy quantifiers"),
        ("^\\w+$", "the escape"),
        ("^[a-z", "unterminated character class"),
        ("^a{2,1}$", "max < min"),
    ];
    for (pat, why) in cases {
        let err = compile(pat).expect_err(pat);
        assert!(
            err.0.contains(why) || err.0.contains("subset"),
            "{pat:?}: expected a refusal naming {why:?}, got {:?}",
            err.0
        );
    }
}
