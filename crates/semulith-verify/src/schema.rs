//! A JSON Schema validator for exactly the subset this project's schemas use — the Rust
//! half of `scripts/validate_records.py`.
//!
//! WHY THIS EXISTS (the RUST-01 discharge). `PACKAGE_CHECKS.md` rows "All 3 schemas valid",
//! "All 5 records validate", and "All 6 rejected" were produced by Python `jsonschema` in
//! the planning package and have been **cited, not re-derived**, ever since. This module is
//! the re-derivation: the same supported-keyword census, the same refusal discipline, the
//! same verdicts — running in the workspace's own language, gateable on every commit.
//!
//! ⛔ THE SOUNDNESS PROPERTY IS THE REFUSAL, NOT THE COVERAGE — as the Python original says.
//! A keyword outside [`SUPPORTED`] is [`Refusal`], never ignored. Adding a keyword to a
//! schema breaks the gate loudly instead of quietly widening what passes.
//!
//! Deliberate differences from the Python tool, both measured against the frozen corpus
//! (verdicts unchanged — the tests run both engines' expectations on the 5 real records):
//!
//! 1. `type` may be an **array** of type names. The corpus uses `["string","number",…]`
//!    under the contract's `parameters.additionalProperties`; the Python tool would REFUSE
//!    there (`TYPES.get(list)` is `None`) — unreachable, because of (2).
//! 2. `additionalProperties` **as a schema** is enforced (the Python tool only implements
//!    the literal `false` and silently skips a schema value, so `parameters` values were
//!    never actually validated). On the tracked records the parameters are integers, which
//!    the schema accepts — same verdicts, one hole closed.
//!
//! Value equality follows Python's: `const`/`enum` compare across the int/float boundary
//! (`1 == 1.0`), while `uniqueItems` distinguishes variants (`Int(1)` ≠ `Float(1.0)`), as
//! `validate_records.py`'s frozen view does.

use crate::json::{self, Json};
use crate::pattern;

/// A keyword, type name, or pattern construct the validator does not implement. Carrying
/// the reason is the point: a refusal names what must be implemented or removed.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Refusal(pub String);

impl std::fmt::Display for Refusal {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "REFUSED: {}", self.0)
    }
}

/// The supported keyword census — derived from the three tracked schemas, exactly as the
/// Python validator's `SUPPORTED` is.
pub const SUPPORTED: &[&str] = &[
    "$id",
    "$schema",
    "title",
    "description",
    "type",
    "properties",
    "required",
    "additionalProperties",
    "enum",
    "const",
    "pattern",
    "minLength",
    "items",
    "minItems",
    "uniqueItems",
    "allOf",
    "if",
    "then",
];

/// Validate `instance` against `schema`. `Ok(errors)` is the verdict: an empty list means
/// valid; each entry names the JSON path and the failing construct. `Err(Refusal)` means
/// the SCHEMA asked for something this validator does not implement — never a verdict.
pub fn validate(instance: &Json, schema: &Json) -> Result<Vec<String>, Refusal> {
    validate_at(instance, schema, "$".to_string())
}

/// Validate every record line of a JSONL document. A malformed line is an error, never a
/// skip; a file with no records is an error — an empty catalogue is not a valid one.
pub fn validate_jsonl(text: &str, schema: &Json) -> Result<Vec<String>, Refusal> {
    let mut errors = Vec::new();
    let mut n = 0usize;
    for (lineno, raw) in text.lines().enumerate() {
        if raw.trim().is_empty() {
            continue;
        }
        n += 1;
        let record = match json::parse(raw) {
            Ok(r) => r,
            Err(e) => {
                errors.push(format!("line {}: not valid JSON — {}", lineno + 1, e));
                continue;
            }
        };
        let rid = record
            .get("id")
            .and_then(Json::as_str)
            .unwrap_or("<line>")
            .to_string();
        for err in validate(&record, schema)? {
            errors.push(format!("line {} [{}] {}", lineno + 1, rid, err));
        }
    }
    if n == 0 {
        errors.push("the document contains no records — an empty file is not a valid one".into());
    }
    Ok(errors)
}

fn type_name(v: &Json) -> &'static str {
    match v {
        Json::Null => "null",
        Json::Bool(_) => "boolean",
        Json::Int(_) => "integer",
        Json::Float(_) => "number",
        Json::Str(_) => "string",
        Json::Arr(_) => "array",
        Json::Obj(_) => "object",
    }
}

fn type_matches(instance: &Json, want: &str) -> Result<bool, Refusal> {
    Ok(match want {
        "object" => matches!(instance, Json::Obj(_)),
        "array" => matches!(instance, Json::Arr(_)),
        "string" => matches!(instance, Json::Str(_)),
        "boolean" => matches!(instance, Json::Bool(_)),
        "null" => matches!(instance, Json::Null),
        "integer" => matches!(instance, Json::Int(_)),
        "number" => matches!(instance, Json::Int(_) | Json::Float(_)),
        other => return Err(Refusal(format!("unknown type {other:?}"))),
    })
}

/// Python `==` for JSON values: across the int/float boundary by value, strict otherwise.
fn py_eq(a: &Json, b: &Json) -> bool {
    match (a, b) {
        (Json::Int(x), Json::Float(y)) | (Json::Float(y), Json::Int(x)) => *x as f64 == *y,
        _ => a == b,
    }
}

fn refuse_bad_schema(what: &str) -> Refusal {
    Refusal(format!("bad schema shape: {what}"))
}

fn supported_check(schema: &Json) -> Result<(), Refusal> {
    let obj = schema
        .as_obj()
        .ok_or_else(|| refuse_bad_schema("a schema must be an object"))?;
    for (key, _) in obj {
        if !SUPPORTED.contains(&key.as_str()) {
            return Err(Refusal(format!(
                "schema uses '{key}', which this validator does not implement. Implement it \
                 or stop using it — silently ignoring a keyword would report 'valid' for a \
                 document that was never fully checked"
            )));
        }
    }
    Ok(())
}

fn schema_obj<'a>(value: &'a Json, kw: &str) -> Result<&'a [(String, Json)], Refusal> {
    value
        .as_obj()
        .ok_or_else(|| refuse_bad_schema(&format!("'{kw}' must be an object")))
}

fn schema_str<'a>(value: &'a Json, kw: &str) -> Result<&'a str, Refusal> {
    value
        .as_str()
        .ok_or_else(|| refuse_bad_schema(&format!("'{kw}' must be a string")))
}

fn validate_at(instance: &Json, schema: &Json, path: String) -> Result<Vec<String>, Refusal> {
    supported_check(schema)?;
    let mut errors = Vec::new();

    if let Some(type_spec) = schema.get("type") {
        let wants: Vec<&str> = match type_spec {
            Json::Str(s) => vec![s.as_str()],
            Json::Arr(items) => items
                .iter()
                .map(|i| schema_str(i, "type"))
                .collect::<Result<Vec<_>, _>>()?,
            _ => {
                return Err(refuse_bad_schema(
                    "'type' must be a string or an array of strings",
                ))
            }
        };
        let ok = wants
            .iter()
            .try_fold(false, |acc, w| type_matches(instance, w).map(|m| acc || m))?;
        if !ok {
            errors.push(format!(
                "{path}: expected {}, got {}",
                wants.join(" or "),
                type_name(instance)
            ));
            return Ok(errors); // further keywords would report noise
        }
    }

    if let Some(c) = schema.get("const") {
        if !py_eq(instance, c) {
            errors.push(format!(
                "{path}: expected the constant {c:?}, got {instance:?}"
            ));
        }
    }
    if let Some(Json::Arr(variants)) = schema.get("enum") {
        if !variants.iter().any(|v| py_eq(instance, v)) {
            errors.push(format!("{path}: {instance:?} is not one of {variants:?}"));
        }
    }
    if let Json::Str(s) = instance {
        if let Some(pat) = schema.get("pattern") {
            let pat = schema_str(pat, "pattern")?;
            match pattern::is_match(pat, s) {
                Ok(true) => {}
                Ok(false) => errors.push(format!("{path}: {s:?} does not match /{pat}/")),
                Err(r) => {
                    return Err(Refusal(format!(
                        "pattern /{pat}/ uses {r} — implement it or change the schema"
                    )));
                }
            }
        }
        if let Some(min) = schema.get("minLength") {
            let min = match min {
                Json::Int(n) if *n >= 0 => *n as usize,
                _ => {
                    return Err(refuse_bad_schema(
                        "'minLength' must be a non-negative integer",
                    ))
                }
            };
            if s.chars().count() < min {
                errors.push(format!("{path}: shorter than minLength {min}"));
            }
        }
    }

    if let Json::Arr(items) = instance {
        if let Some(m) = schema.get("minItems") {
            let m = match m {
                Json::Int(n) if *n >= 0 => *n as usize,
                _ => {
                    return Err(refuse_bad_schema(
                        "'minItems' must be a non-negative integer",
                    ))
                }
            };
            if items.len() < m {
                errors.push(format!(
                    "{path}: has {} item(s), minItems is {m}",
                    items.len()
                ));
            }
        }
        if schema
            .get("uniqueItems")
            .is_some_and(|u| u.as_bool() == Some(true))
        {
            let mut dupes = Vec::new();
            for (i, v) in items.iter().enumerate() {
                if items[..i].contains(v) {
                    dupes.push(format!("{v:?}"));
                }
            }
            if !dupes.is_empty() {
                errors.push(format!(
                    "{path}: duplicate item(s) [{}] under uniqueItems",
                    dupes.join(", ")
                ));
            }
        }
        if let Some(item_schema) = schema.get("items") {
            for (i, v) in items.iter().enumerate() {
                errors.extend(validate_at(v, item_schema, format!("{path}[{i}]"))?);
            }
        }
    }

    if let Json::Obj(_) = instance {
        let props: Vec<(&str, &Json)> = match schema.get("properties") {
            None => Vec::new(),
            Some(p) => schema_obj(p, "properties")?
                .iter()
                .map(|(k, v)| (k.as_str(), v))
                .collect(),
        };
        if let Some(req) = schema.get("required") {
            let req = req
                .as_arr()
                .ok_or_else(|| refuse_bad_schema("'required' must be an array"))?;
            for key in req {
                let key = schema_str(key, "required")?;
                if instance.get(key).is_none() {
                    errors.push(format!("{path}: missing required property '{key}'"));
                }
            }
        }
        match schema.get("additionalProperties") {
            Some(Json::Bool(false)) => {
                for (key, _) in instance.as_obj().expect("object instance") {
                    if !props.iter().any(|(p, _)| p == key) {
                        errors.push(format!("{path}: property '{key}' is not allowed"));
                    }
                }
            }
            Some(extra @ Json::Obj(_)) => {
                for (key, value) in instance.as_obj().expect("object instance") {
                    if !props.iter().any(|(p, _)| p == key) {
                        errors.extend(validate_at(value, extra, format!("{path}.{key}"))?);
                    }
                }
            }
            Some(_) => {
                return Err(refuse_bad_schema(
                    "'additionalProperties' must be false or a schema object",
                ));
            }
            None => {}
        }
        for (key, sub) in props {
            if let Some(value) = instance.get(key) {
                errors.extend(validate_at(value, sub, format!("{path}.{key}"))?);
            }
        }
    }

    if let Some(all_of) = schema.get("allOf") {
        let all_of = all_of
            .as_arr()
            .ok_or_else(|| refuse_bad_schema("'allOf' must be an array"))?;
        for (i, sub) in all_of.iter().enumerate() {
            errors.extend(
                validate_at(instance, sub, path.clone())
                    .map_err(|r| Refusal(format!("allOf[{i}]: {}", r.0)))?,
            );
        }
    }

    if let Some(if_schema) = schema.get("if") {
        let if_ok = validate_at(instance, if_schema, path.clone())
            .map_err(|r| Refusal(format!("if: {}", r.0)))?
            .is_empty();
        if if_ok {
            if let Some(then_schema) = schema.get("then") {
                errors.extend(
                    validate_at(instance, then_schema, path)
                        .map_err(|r| Refusal(format!("then: {}", r.0)))?,
                );
            }
        }
    }

    Ok(errors)
}

#[cfg(test)]
mod tests;
