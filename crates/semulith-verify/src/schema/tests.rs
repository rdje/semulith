//! Schema-validator tests — the keyword subset, the refusal discipline, and the two
//! documented tightenings (array `type`, schema-valued `additionalProperties`).

use super::{validate, validate_jsonl, Refusal, SUPPORTED};
use crate::json::{parse, Json};

fn ok(schema: &str) -> Json {
    parse(schema).expect("schema parses")
}

fn valid(instance: &str, schema: &str) -> bool {
    validate(&parse(instance).expect("instance parses"), &ok(schema))
        .expect("schema supported")
        .is_empty()
}

#[test]
fn type_check_covers_the_json_type_vocabulary() {
    let s = r#"{"type": "string"}"#;
    assert!(valid(r#""x""#, s));
    assert!(!valid("1", s));
    let i = r#"{"type": "integer"}"#;
    assert!(valid("42", i));
    assert!(!valid("4.2", i)); // a float is not an integer
    assert!(!valid("true", i)); // and a bool is never an int (Python blurs this)
    let n = r#"{"type": "number"}"#;
    assert!(valid("42", n) && valid("4.2", n) && !valid(r#""x""#, n));
    for (ty, v) in [
        ("object", "{}"),
        ("array", "[]"),
        ("boolean", "false"),
        ("null", "null"),
    ] {
        assert!(valid(v, &format!(r#"{{"type": "{ty}"}}"#)), "{ty}");
    }
}

#[test]
fn array_type_accepts_any_named_member() {
    // the tightening: the corpus's parameters schema uses an array type
    let s = r#"{"type": ["string", "number", "boolean", "null"]}"#;
    assert!(valid(r#""x""#, s) && valid("0", s) && valid("true", s) && valid("null", s));
    assert!(valid("1.5", s)); // a number, incl. float
    assert!(!valid("[]", s)); // an array is outside the union
}

#[test]
fn required_and_additionalproperties_false() {
    let s = r#"{"type": "object",
                "properties": {"id": {"type": "string"}},
                "required": ["id"],
                "additionalProperties": false}"#;
    assert!(valid(r#"{"id": "a"}"#, s));
    let errors = validate(&parse(r#"{"other": 1}"#).unwrap(), &ok(s)).unwrap();
    assert!(
        errors
            .iter()
            .any(|e| e.contains("missing required property 'id'")),
        "{errors:?}"
    );
    assert!(
        errors
            .iter()
            .any(|e| e.contains("property 'other' is not allowed")),
        "{errors:?}"
    );
}

#[test]
fn additionalproperties_as_schema_is_enforced_not_skipped() {
    // the Python tool silently skips a schema here; this engine validates the values.
    let s = r#"{"type": "object",
                "properties": {"name": {"type": "string"}},
                "additionalProperties": {"type": ["string", "number", "boolean", "null"]}}"#;
    assert!(valid(r#"{"name": "x", "min": 0, "max": 65535}"#, s));
    assert!(!valid(r#"{"min": [1]}"#, s)); // an array value is outside the declared union
}

#[test]
fn enum_and_const_compare_across_the_int_float_boundary_like_python() {
    let e = r#"{"enum": [1, "two", null]}"#;
    assert!(valid("1", e) && valid(r#""two""#, e) && valid("null", e));
    assert!(valid("1.0", e)); // Python: 1.0 == 1
    assert!(!valid("2", e));
    let c = r#"{"const": "passed"}"#;
    assert!(valid(r#""passed""#, c) && !valid(r#""failed""#, c));
}

#[test]
fn uniqueitems_distinguishes_int_from_float_like_the_frozen_view() {
    // validate_records.py's frozen view: ("v","int",1) != ("v","float",1.0)
    let s = r#"{"type": "array", "items": {"type": "number"}, "uniqueItems": true}"#;
    assert!(valid("[1, 2]", s));
    assert!(valid("[1, 1.0]", s)); // distinct variants, both "number"
    assert!(!valid("[1, 1]", s));
    let strs = r#"{"type": "array", "items": {"type": "string"}, "uniqueItems": true}"#;
    assert!(!valid(r#"["a", "a"]"#, strs));
    assert!(valid(r#"["a", "b"]"#, strs));
}

#[test]
fn pattern_and_minlength_apply_to_strings_only() {
    let s = r#"{"type": "string", "pattern": "^[a-z]+$", "minLength": 2}"#;
    assert!(valid(r#""abc""#, s));
    assert!(!valid(r#""ABC""#, s) && !valid(r#""a""#, s));
    assert!(valid("5", r#"{"type": "integer", "pattern": "^[a-z]+$"}"#)); // skipped, not failed
}

#[test]
fn items_and_minitems_on_arrays() {
    let s = r#"{"type": "array", "items": {"type": "string"}, "minItems": 1}"#;
    assert!(valid(r#"["a"]"#, s));
    assert!(!valid("[]", s));
    assert!(!valid(r#"["a", 1]"#, s));
}

#[test]
fn allof_and_if_then() {
    let s = r#"{"allOf": [
                 {"type": "object", "required": ["a"]},
                 {"if": {"properties": {"kind": {"const": "x"}}, "required": ["kind"]},
                  "then": {"required": ["b"]}}
               ]}"#;
    assert!(valid(r#"{"a": 1, "kind": "y"}"#, s)); // if fails, then not applied
    assert!(valid(r#"{"a": 1, "kind": "x", "b": 2}"#, s));
    let errors = validate(&parse(r#"{"a": 1, "kind": "x"}"#).unwrap(), &ok(s)).unwrap();
    assert!(
        errors
            .iter()
            .any(|e| e.contains("missing required property 'b'")),
        "{errors:?}"
    );
}

#[test]
fn if_errors_are_discarded_and_then_applies_only_on_success() {
    // the specification's reading: `if` is evaluated for validity only, its errors discarded
    let s = r#"{"if": {"properties": {"status": {"const": "passed"}}, "required": ["status"]},
                "then": {"required": ["proof"]}}"#;
    // status absent -> if invalid -> then not applied -> no errors even though "proof" is absent
    assert!(valid(r#"{"other": 1}"#, s));
}

#[test]
fn unknown_keywords_types_and_patterns_are_refusals_not_verdicts() {
    let inst = parse("{}").unwrap();
    let err = validate(&inst, &ok(r##"{"$ref": "#/x"}"##)).unwrap_err();
    assert!(err.0.contains("'$ref'"), "{err}");
    let err = validate(&inst, &ok(r#"{"type": "funky"}"#)).unwrap_err();
    assert!(err.0.contains("unknown type"), "{err}");
    let err = validate(&parse(r#""x""#).unwrap(), &ok(r#"{"pattern": "^(a|b)$"}"#)).unwrap_err();
    assert!(err.0.contains("groups"), "{err}");
    let err = validate(&parse(r#""x""#).unwrap(), &ok(r#"{"pattern": "^a|b$"}"#)).unwrap_err();
    assert!(err.0.contains("alternation"), "{err}");
    let err = validate(&inst, &ok(r#"{"properties": 5}"#)).unwrap_err();
    assert!(err.0.contains("bad schema shape"), "{err}");
}

#[test]
fn every_keyword_the_tracked_schemas_use_is_supported() {
    // the census invariant: the three schemas recurse through SUPPORTED only, so the
    // validator can never meet a keyword it must refuse on the frozen corpus.
    let files = [
        (
            "requirement",
            include_str!("../../../../schemas/requirement.schema.json"),
        ),
        (
            "evidence",
            include_str!("../../../../schemas/evidence.schema.json"),
        ),
        (
            "contract",
            include_str!("../../../../schemas/contract-obligation.schema.json"),
        ),
    ];
    for (name, text) in files {
        let schema = parse(text).unwrap_or_else(|e| panic!("{name} parses: {e}"));
        assert!(
            walk_supported(&schema),
            "{name} uses an unsupported keyword"
        );
    }
}

fn walk_supported(schema: &Json) -> bool {
    let Some(obj) = schema.as_obj() else {
        return true;
    };
    if obj.iter().any(|(k, _)| !SUPPORTED.contains(&k.as_str())) {
        return false;
    }
    obj.iter().all(|(k, v)| match v {
        // `properties` values are subschemas keyed by property NAME — the names are data,
        // not keywords, and must not be checked against SUPPORTED
        Json::Obj(_) if k == "properties" => v
            .as_obj()
            .expect("properties is an object")
            .iter()
            .all(|(_, sub)| walk_supported(sub)),
        Json::Arr(items) => items.iter().all(walk_supported),
        Json::Obj(_) => walk_supported(v),
        _ => true,
    })
}

#[test]
fn validate_jsonl_reports_lines_and_refuses_an_empty_document() {
    let schema = ok(r#"{"type": "object", "required": ["id"]}"#);
    let errors = validate_jsonl("{\"id\": 1}\n\nnot json\n{\"id\": 2}\n", &schema).unwrap();
    assert_eq!(errors.len(), 1);
    assert!(errors[0].contains("line 3"), "{errors:?}");
    assert!(errors[0].contains("not valid JSON"), "{errors:?}");
    // a schema error carries the record id when the record has one
    let needs_proof = ok(r#"{"type": "object", "required": ["proof"]}"#);
    let errors = validate_jsonl("{\"id\": \"R1\"}\n", &needs_proof).unwrap();
    assert!(errors[0].contains("[R1]"), "{errors:?}");
    assert!(
        errors[0].contains("missing required property 'proof'"),
        "{errors:?}"
    );
    assert!(validate_jsonl("\n", &schema).unwrap()[0].contains("no records"));
}

#[test]
fn refusal_display_names_itself() {
    let r = Refusal("test construct".into());
    assert_eq!(r.to_string(), "REFUSED: test construct");
}
