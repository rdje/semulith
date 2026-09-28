//! Tests for the JSON reader — the contract is `json.loads` parity on the shapes the
//! evidence records use, plus refusals that name the position.

use super::{parse, Error, Json};

#[test]
fn parses_the_json_value_forms() {
    let doc = parse(
        r#"{"id": "EV-1", "n": -12, "f": 1.5e2, "t": true, "x": null,
            "a": [1, "two", false], "o": {"k": "v"}}"#,
    )
    .expect("parses");
    let obj = doc.as_obj().expect("object");
    assert_eq!(obj.len(), 7);
    assert_eq!(doc.get("id"), Some(&Json::Str("EV-1".to_string())));
    assert_eq!(doc.get("n"), Some(&Json::Int(-12)));
    assert_eq!(doc.get("f"), Some(&Json::Float(150.0)));
    assert_eq!(doc.get("t"), Some(&Json::Bool(true)));
    assert_eq!(doc.get("x"), Some(&Json::Null));
    assert_eq!(
        doc.get("a").and_then(Json::as_arr),
        Some(
            &[
                Json::Int(1),
                Json::Str("two".to_string()),
                Json::Bool(false)
            ][..]
        )
    );
    assert_eq!(
        doc.get("o").and_then(|o| o.get("k")),
        Some(&Json::Str("v".to_string()))
    );
}

#[test]
fn integer_and_float_are_distinct_variants() {
    assert_eq!(parse("1").unwrap(), Json::Int(1));
    assert_eq!(parse("1.0").unwrap(), Json::Float(1.0));
    assert_eq!(parse("1e0").unwrap(), Json::Float(1.0));
    assert_ne!(Json::Int(1), Json::Float(1.0));
    // Python parity: a bool is never an int, whatever the host language blurs.
    assert_ne!(Json::Bool(true), Json::Int(1));
}

#[test]
fn duplicate_object_keys_take_the_last_value() {
    // json.loads parity: the corpus has no duplicates, and the reader states its
    // contract instead of inventing a stricter one.
    let doc = parse(r#"{"id": "first", "id": "last"}"#).expect("parses");
    assert_eq!(doc.get("id"), Some(&Json::Str("last".to_string())));
}

#[test]
fn strings_handle_escapes_surrogates_and_non_ascii() {
    let doc = parse(r#""quote:\" backslash:\\ slash:\/ nl:\n tab:\t uni:Aé clamped:\u0041""#)
        .expect("escapes parse");
    assert_eq!(
        doc.as_str().map(str::to_string),
        Some("quote:\" backslash:\\ slash:/ nl:\n tab:\t uni:Aé clamped:A".to_string())
    );
    // a surrogate pair composes one scalar
    assert_eq!(
        parse(r#""\uD83D\uDE00""#).unwrap(),
        Json::Str("😀".to_string())
    );
}

#[test]
fn refusals_name_the_position_and_reason() {
    let cases: [(&str, &str); 10] = [
        ("", "unexpected end of input"),
        ("{", "expected an object key (a string)"),
        (r#"{"a" 1}"#, "expected ':'"),
        (r#"{"a":1"#, "expected ',' or '}' in an object"),
        ("[1 2]", "expected ',' or ']' in an array"),
        ("tru", "invalid literal, expected 'true'"),
        ("01", "leading zeros are not allowed"),
        ("1.", "expected a digit after '.'"),
        ("1e", "expected a digit in the exponent"),
        ("1 2", "trailing content after the top-level value"),
    ];
    for (text, why) in cases {
        let err: Error = parse(text).expect_err(text);
        assert!(
            err.message.contains(why),
            "{text:?}: expected {why:?}, got {:?} at {}:{}",
            err.message,
            err.line,
            err.column
        );
        assert!(err.line >= 1 && err.column >= 1);
    }
}

#[test]
fn refuses_control_characters_and_bad_escapes_and_lone_surrogates() {
    assert!(parse("\"\u{0007}\"").is_err());
    assert!(parse(r#""\q""#).is_err());
    assert!(parse(r#""\uD83D""#).is_err()); // lone high surrogate
    assert!(parse(r#""\uDE00""#).is_err()); // lone low surrogate
    assert!(parse(r#""\uD83D\u0041""#).is_err()); // high surrogate + non-low
}

#[test]
fn integer_out_of_i128_range_is_refused_not_truncated() {
    let err = parse("170141183460469231731687303715884105728").expect_err("2^127");
    assert!(err.message.contains("out of i128 range"));
}

#[test]
fn line_and_column_track_multiline_documents() {
    let err = parse("{\n  \"a\": 1,\n  \"b\": tru\n}").expect_err("bad literal");
    assert_eq!(err.line, 3);
    assert!(err.message.contains("expected 'true'"));
}
