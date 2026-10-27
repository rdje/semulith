//! The record mapping (`XTASK.6` slice `6o`), ported from the pinned `scripts/records_sexp.py`, which stays the single owner
//! of the JSON-shaped record dict ↔ S-expression form correspondence: a requirement, obligation, unit or category-need form
//! becomes an ordered record whose keys are the JSON keys, and back. Values the corpus does not write (a float, a
//! heterogeneous or nested list) are refused with the parameter named — never guessed. Every message is the pinned
//! module's text; the canonical JSON dump below prints as Python's `json.dumps(…, ensure_ascii=False)` does, so the
//! corpus-equality test can compare the two readers' dumps byte for byte.

use std::path::Path;

use crate::sexp::{self, py_repr, Sexp, SexpError};

/// A JSON-shaped value: what a record field holds.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Value {
    Null,
    Bool(bool),
    Int(i128),
    Str(String),
    List(Vec<Value>),
    /// An ordered object — Python dicts keep insertion order, and the field order is the JSON key order.
    Object(Vec<(String, Value)>),
}

impl Value {
    pub fn get(&self, key: &str) -> Option<&Value> {
        match self {
            Value::Object(pairs) => pairs.iter().find(|(k, _)| k == key).map(|(_, v)| v),
            _ => None,
        }
    }
    pub fn has(&self, key: &str) -> bool {
        self.get(key).is_some()
    }
}

/// A value the mapping does not carry. Refused, never guessed.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RecordRefused(pub String);

/// What the mapping can refuse: a record shape, or the reader's own refusal of the bytes.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RecordError {
    Refused(RecordRefused),
    Sexp(SexpError),
}

impl std::fmt::Display for RecordError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            RecordError::Refused(e) => f.write_str(&e.0),
            RecordError::Sexp(e) => f.write_str(&e.0),
        }
    }
}

impl From<SexpError> for RecordError {
    fn from(e: SexpError) -> Self {
        RecordError::Sexp(e)
    }
}

fn refused(text: String) -> RecordError {
    RecordError::Refused(RecordRefused(text))
}

/// Python's `str(value)` of a parsed atom.
fn s(v: &Sexp) -> String {
    match v {
        Sexp::Int(n) => n.to_string(),
        Sexp::Str(t) | Sexp::Symbol(t) => t.clone(),
        Sexp::List(_) => py_repr(v),
    }
}

fn field_s(form: &Sexp, name: &str) -> Result<Value, RecordError> {
    Ok(Value::Str(s(sexp::field(form, name, "")?)))
}

/// `_refs`: the `(key (id …) (locator …))` children as objects.
fn refs(children: &[&Sexp], key_id: &str, key_locator: &str) -> Result<Value, RecordError> {
    let mut out = Vec::new();
    for f in children {
        out.push(Value::Object(vec![
            (
                key_id.to_owned(),
                Value::Str(s(sexp::field(f, key_id, "")?)),
            ),
            (
                key_locator.to_owned(),
                Value::Str(s(sexp::field(f, key_locator, "")?)),
            ),
        ]));
    }
    Ok(Value::List(out))
}

/// `_strings`: values of repeated `(name VALUE)` atom-field children, order preserved.
fn strings(forms: &[&Sexp], name: &str) -> Result<Value, RecordError> {
    let mut out = Vec::new();
    for f in forms {
        match f {
            Sexp::List(l) if l.len() == 2 && l[0].text() == Some(name) => {
                out.push(Value::Str(s(&l[1])))
            }
            _ => {
                return Err(SexpError(format!(
                    "({name} …) must carry exactly one value, got {}",
                    py_repr(f)
                ))
                .into());
            }
        }
    }
    Ok(Value::List(out))
}

/// `_one`: the single child list headed `name`.
fn one<'a>(form: &'a Sexp, name: &str) -> Result<&'a Sexp, RecordError> {
    let found = sexp::children(form, name)?;
    if found.len() != 1 {
        return Err(SexpError(format!(
            "expected exactly one ({name} …), found {}",
            found.len()
        ))
        .into());
    }
    Ok(found[0])
}

fn children<'a>(form: &'a Sexp, name: &str) -> Result<Vec<&'a Sexp>, RecordError> {
    Ok(sexp::children(form, name)?)
}

pub fn requirement_to_dict(form: &Sexp) -> Result<Value, RecordError> {
    sexp::head(form, "requirement")?;
    let src = children(form, "source_refs")?;
    let imp = children(form, "implementation_refs")?;
    let sem = one(form, "source_semantics")?;
    Ok(Value::Object(vec![
        ("id".into(), field_s(form, "id")?),
        (
            "profile_ids".into(),
            strings(&children(form, "profile_ids")?, "profile_ids")?,
        ),
        ("kind".into(), field_s(form, "kind")?),
        ("statement".into(), field_s(form, "statement")?),
        ("insns".into(), strings(&children(form, "insns")?, "insns")?),
        ("source_refs".into(), refs(&src, "source_id", "locator")?),
        ("applicability".into(), field_s(form, "applicability")?),
        ("research_status".into(), field_s(form, "research_status")?),
        (
            "implementation_status".into(),
            field_s(form, "implementation_status")?,
        ),
        (
            "source_semantics".into(),
            Value::Object(vec![
                ("category".into(), field_s(sem, "category")?),
                ("detail".into(), field_s(sem, "detail")?),
            ]),
        ),
        ("risk".into(), field_s(form, "risk")?),
        (
            "obligation_ids".into(),
            strings(&children(form, "obligation_ids")?, "obligation_ids")?,
        ),
        (
            "dependencies".into(),
            strings(&children(form, "dependencies")?, "dependencies")?,
        ),
        (
            "implementation_refs".into(),
            refs(&imp, "artifact_id", "locator")?,
        ),
        (
            "evidence_ids".into(),
            strings(&children(form, "evidence_ids")?, "evidence_ids")?,
        ),
    ]))
}

/// `_value_to_json`: a typed parameter value form.
fn value_to_json(form: &Sexp) -> Result<Value, RecordError> {
    let head = sexp::head(form, "param value")?;
    let items = match form {
        Sexp::List(l) => l,
        _ => {
            return Err(refused(format!(
                "empty parameter value form {}",
                py_repr(form)
            )))
        }
    };
    let one = || -> Result<&Sexp, RecordError> {
        if items.len() != 2 {
            return Err(refused(format!(
                "({head} …) takes exactly one value, got {}",
                py_repr(form)
            )));
        }
        Ok(&items[1])
    };
    let nullary = |text: &str| -> Result<(), RecordError> {
        if items.len() != 1 {
            return Err(refused(format!(
                "({text}) is nullary, got {}",
                py_repr(form)
            )));
        }
        Ok(())
    };
    match head.as_str() {
        "int" => {
            let v = one()?;
            match v {
                Sexp::Int(n) => Ok(Value::Int(*n)),
                Sexp::Str(t) | Sexp::Symbol(t) => Ok(Value::Str(t.clone())),
                other => Ok(Value::Str(py_repr(other))),
            }
        }
        "str" => Ok(Value::Str(s(one()?))),
        "true" => {
            nullary("true")?;
            Ok(Value::Bool(true))
        }
        "false" => {
            nullary("false")?;
            Ok(Value::Bool(false))
        }
        "null" => {
            nullary("null")?;
            Ok(Value::Null)
        }
        "ints" => {
            let mut out = Vec::new();
            for a in &items[1..] {
                match a {
                    Sexp::Int(n) => out.push(Value::Int(*n)),
                    other => {
                        let t = s(other);
                        let n = t.trim().parse::<i128>().map_err(|_| {
                            refused(format!(
                                "invalid literal for int() with base 10: {}",
                                py_repr(other)
                            ))
                        })?;
                        out.push(Value::Int(n));
                    }
                }
            }
            Ok(Value::List(out))
        }
        "strs" => Ok(Value::List(
            items[1..].iter().map(|a| Value::Str(s(a))).collect(),
        )),
        _ => Err(refused(format!(
            "unknown parameter value form {}",
            py_repr(form)
        ))),
    }
}

pub fn obligation_to_dict(form: &Sexp) -> Result<Value, RecordError> {
    sexp::head(form, "obligation")?;
    let src = children(form, "source_refs")?;
    let params = one(form, "parameters")?;
    let mut parameters: Vec<(String, Value)> = Vec::new();
    for p in children(params, "param")? {
        let name = s(sexp::field(p, "name", "")?);
        let value = value_to_json(sexp::field(p, "value", "")?)?;
        if let Some(e) = parameters.iter_mut().find(|(k, _)| *k == name) {
            e.1 = value;
        } else {
            parameters.push((name, value));
        }
    }
    Ok(Value::Object(vec![
        ("id".into(), field_s(form, "id")?),
        ("contract_id".into(), field_s(form, "contract_id")?),
        (
            "contract_version".into(),
            field_s(form, "contract_version")?,
        ),
        (
            "profile_ids".into(),
            strings(&children(form, "profile_ids")?, "profile_ids")?,
        ),
        ("direction".into(), field_s(form, "direction")?),
        ("statement".into(), field_s(form, "statement")?),
        ("authority".into(), field_s(form, "authority")?),
        ("source_refs".into(), refs(&src, "source_id", "locator")?),
        ("parameters".into(), Value::Object(parameters)),
        (
            "dependencies".into(),
            strings(&children(form, "dependencies")?, "dependencies")?,
        ),
        (
            "required_checks".into(),
            strings(&children(form, "required_checks")?, "required_checks")?,
        ),
    ]))
}

pub fn unit_to_dict(form: &Sexp) -> Result<Value, RecordError> {
    sexp::head(form, "unit")?;
    let mut out = vec![
        ("id".to_owned(), field_s(form, "id")?),
        ("kind".to_owned(), field_s(form, "kind")?),
        ("layer".to_owned(), field_s(form, "layer")?),
        ("book".to_owned(), field_s(form, "book")?),
    ];
    let req = children(form, "requires")?;
    if !req.is_empty() {
        out.push(("requires".to_owned(), strings(&req, "requires")?));
    }
    Ok(Value::Object(out))
}

pub fn category_need_to_dict(form: &Sexp) -> Result<Value, RecordError> {
    sexp::head(form, "category-need")?;
    let mut out = vec![
        ("category".to_owned(), field_s(form, "category")?),
        ("layer".to_owned(), field_s(form, "layer")?),
        ("kind".to_owned(), field_s(form, "kind")?),
        ("unit".to_owned(), field_s(form, "unit")?),
        ("disposition".to_owned(), field_s(form, "disposition")?),
    ];
    for key in ["reason", "material"] {
        let found = children(form, key)?;
        if let Some(Sexp::List(l)) = found.first() {
            let v = l.get(1).ok_or_else(|| {
                RecordError::Refused(RecordRefused("list index out of range".to_owned()))
            })?;
            out.push((key.to_owned(), Value::Str(s(v))));
        }
    }
    Ok(Value::Object(out))
}

/// `form_to_dict`: dispatch on the record head.
pub fn form_to_dict(form: &Sexp) -> Result<Value, RecordError> {
    let head = sexp::head(form, "")?;
    match head.as_str() {
        "requirement" => requirement_to_dict(form),
        "obligation" => obligation_to_dict(form),
        "unit" => unit_to_dict(form),
        "category-need" => category_need_to_dict(form),
        _ => Err(refused(format!("not a record form: {}", py_repr(form)))),
    }
}

// ── Python's json.dumps(value, ensure_ascii=False) ───────────────────────────────────────────

fn json_string(out: &mut String, text: &str) {
    out.push('"');
    for c in text.chars() {
        match c {
            '"' => out.push_str("\\\""),
            '\\' => out.push_str("\\\\"),
            '\n' => out.push_str("\\n"),
            '\r' => out.push_str("\\r"),
            '\t' => out.push_str("\\t"),
            '\u{8}' => out.push_str("\\b"),
            '\u{c}' => out.push_str("\\f"),
            c if (c as u32) < 0x20 => out.push_str(&format!("\\u{:04x}", c as u32)),
            c => out.push(c),
        }
    }
    out.push('"');
}

/// The canonical dump: Python's default separators (`, ` and `: `), insertion order, non-ASCII kept.
pub fn json_dumps(value: &Value) -> String {
    let mut out = String::new();
    fn go(v: &Value, out: &mut String) {
        match v {
            Value::Null => out.push_str("null"),
            Value::Bool(b) => out.push_str(if *b { "true" } else { "false" }),
            Value::Int(n) => out.push_str(&n.to_string()),
            Value::Str(t) => json_string(out, t),
            Value::List(items) => {
                out.push('[');
                for (i, item) in items.iter().enumerate() {
                    if i > 0 {
                        out.push_str(", ");
                    }
                    go(item, out);
                }
                out.push(']');
            }
            Value::Object(pairs) => {
                out.push('{');
                for (i, (k, item)) in pairs.iter().enumerate() {
                    if i > 0 {
                        out.push_str(", ");
                    }
                    json_string(out, k);
                    out.push_str(": ");
                    go(item, out);
                }
                out.push('}');
            }
        }
    }
    go(value, &mut out);
    out
}

// ── dict -> form ─────────────────────────────────────────────────────────────────────────────

fn sym(name: &str) -> Sexp {
    Sexp::Symbol(name.to_owned())
}

fn pair(name: &str, value: Sexp) -> Sexp {
    Sexp::List(vec![sym(name), value])
}

fn str_value(v: &Value, what: &str) -> Result<Sexp, RecordError> {
    match v {
        Value::Str(t) => Ok(Sexp::Str(t.clone())),
        Value::Int(n) => Ok(Sexp::Int(*n)),
        other => Err(refused(format!(
            "{what}: not a string literal: {}",
            json_dumps(other)
        ))),
    }
}

fn sym_value(v: &Value, what: &str) -> Result<Sexp, RecordError> {
    match v {
        Value::Str(t) => Ok(Sexp::Symbol(t.clone())),
        other => Err(refused(format!(
            "{what}: not a symbol: {}",
            json_dumps(other)
        ))),
    }
}

fn repeated(name: &str, values: Option<&Value>) -> Result<Vec<Sexp>, RecordError> {
    match values {
        None | Some(Value::Null) => Ok(Vec::new()),
        Some(Value::List(items)) => items
            .iter()
            .map(|v| Ok(pair(name, str_value(v, name)?)))
            .collect(),
        Some(other) => Err(refused(format!(
            "{name}: not a list: {}",
            json_dumps(other)
        ))),
    }
}

fn ref_forms(
    key: &str,
    refs: Option<&Value>,
    key_id: &str,
    key_locator: &str,
) -> Result<Vec<Sexp>, RecordError> {
    let Some(Value::List(items)) = refs else {
        return Ok(Vec::new());
    };
    let mut out = Vec::new();
    for r in items {
        let id = r
            .get(key_id)
            .ok_or_else(|| refused(format!("'{key_id}'")))?;
        let loc = r
            .get(key_locator)
            .ok_or_else(|| refused(format!("'{key_locator}'")))?;
        out.push(Sexp::List(vec![
            sym(key),
            pair(key_id, str_value(id, key_id)?),
            pair(key_locator, str_value(loc, key_locator)?),
        ]));
    }
    Ok(out)
}

/// `_json_to_value`: a parameter's JSON value as its typed form.
fn json_to_value(name: &str, v: &Value) -> Result<Sexp, RecordError> {
    match v {
        Value::Bool(true) => Ok(Sexp::List(vec![sym("true")])),
        Value::Bool(false) => Ok(Sexp::List(vec![sym("false")])),
        Value::Null => Ok(Sexp::List(vec![sym("null")])),
        Value::Int(n) => Ok(Sexp::List(vec![sym("int"), Sexp::Int(*n)])),
        Value::Str(t) => Ok(Sexp::List(vec![sym("str"), Sexp::Str(t.clone())])),
        Value::List(items) => {
            if items.iter().all(|x| matches!(x, Value::Int(_))) {
                let mut out = vec![sym("ints")];
                out.extend(items.iter().map(|x| if let Value::Int(n) = x { Sexp::Int(*n) } else { Sexp::Int(0) }));
                return Ok(Sexp::List(out));
            }
            if items.iter().all(|x| matches!(x, Value::Str(_))) {
                let mut out = vec![sym("strs")];
                out.extend(items.iter().map(|x| if let Value::Str(t) = x { Sexp::Str(t.clone()) } else { Sexp::Str(String::new()) }));
                return Ok(Sexp::List(out));
            }
            Err(refused(format!("parameter '{name}': a list must be all-integer or all-string, got {}", json_dumps(v))))
        }
        Value::Object(_) => Err(refused(format!(
            "parameter '{name}': no S-expression value for {} — a float or nested value needs a schema decision, not a guessed translation",
            json_dumps(v)
        ))),
    }
}

fn need<'a>(rec: &'a Value, key: &str) -> Result<&'a Value, RecordError> {
    rec.get(key).ok_or_else(|| refused(format!("'{key}'")))
}

/// `dict_to_form`: the record dict -> its form. Field order follows the dict, i.e. the JSON key order.
pub fn dict_to_form(rec: &Value) -> Result<Sexp, RecordError> {
    if rec.has("book") {
        let mut form = vec![
            sym("unit"),
            pair("id", str_value(need(rec, "id")?, "id")?),
            pair("kind", sym_value(need(rec, "kind")?, "kind")?),
            pair("layer", sym_value(need(rec, "layer")?, "layer")?),
            pair("book", str_value(need(rec, "book")?, "book")?),
        ];
        form.extend(repeated("requires", rec.get("requires"))?);
        return Ok(Sexp::List(form));
    }
    if rec.has("disposition") {
        let mut form = vec![
            sym("category-need"),
            pair("category", str_value(need(rec, "category")?, "category")?),
            pair("layer", sym_value(need(rec, "layer")?, "layer")?),
            pair("kind", str_value(need(rec, "kind")?, "kind")?),
            pair("unit", str_value(need(rec, "unit")?, "unit")?),
            pair(
                "disposition",
                sym_value(need(rec, "disposition")?, "disposition")?,
            ),
        ];
        for key in ["reason", "material"] {
            if let Some(v @ Value::Str(t)) = rec.get(key) {
                if !t.is_empty() {
                    form.push(pair(key, str_value(v, key)?));
                }
            }
        }
        return Ok(Sexp::List(form));
    }
    if rec.has("kind") {
        let sem = need(rec, "source_semantics")?;
        let mut form = vec![
            sym("requirement"),
            pair("id", str_value(need(rec, "id")?, "id")?),
        ];
        form.extend(repeated("profile_ids", Some(need(rec, "profile_ids")?))?);
        form.push(pair("kind", sym_value(need(rec, "kind")?, "kind")?));
        form.push(pair(
            "statement",
            str_value(need(rec, "statement")?, "statement")?,
        ));
        form.extend(repeated("insns", rec.get("insns"))?);
        form.extend(ref_forms(
            "source_refs",
            Some(need(rec, "source_refs")?),
            "source_id",
            "locator",
        )?);
        form.push(pair(
            "applicability",
            sym_value(need(rec, "applicability")?, "applicability")?,
        ));
        form.push(pair(
            "research_status",
            sym_value(need(rec, "research_status")?, "research_status")?,
        ));
        form.push(pair(
            "implementation_status",
            sym_value(need(rec, "implementation_status")?, "implementation_status")?,
        ));
        form.push(Sexp::List(vec![
            sym("source_semantics"),
            pair("category", sym_value(need(sem, "category")?, "category")?),
            pair("detail", str_value(need(sem, "detail")?, "detail")?),
        ]));
        form.push(pair("risk", sym_value(need(rec, "risk")?, "risk")?));
        form.extend(repeated(
            "obligation_ids",
            Some(need(rec, "obligation_ids")?),
        )?);
        form.extend(repeated("dependencies", Some(need(rec, "dependencies")?))?);
        form.extend(ref_forms(
            "implementation_refs",
            Some(need(rec, "implementation_refs")?),
            "artifact_id",
            "locator",
        )?);
        form.extend(repeated("evidence_ids", Some(need(rec, "evidence_ids")?))?);
        return Ok(Sexp::List(form));
    }
    if rec.has("direction") {
        let mut form = vec![
            sym("obligation"),
            pair("id", str_value(need(rec, "id")?, "id")?),
            pair(
                "contract_id",
                str_value(need(rec, "contract_id")?, "contract_id")?,
            ),
            pair(
                "contract_version",
                str_value(need(rec, "contract_version")?, "contract_version")?,
            ),
        ];
        form.extend(repeated("profile_ids", Some(need(rec, "profile_ids")?))?);
        form.push(pair(
            "direction",
            sym_value(need(rec, "direction")?, "direction")?,
        ));
        form.push(pair(
            "statement",
            str_value(need(rec, "statement")?, "statement")?,
        ));
        form.push(pair(
            "authority",
            sym_value(need(rec, "authority")?, "authority")?,
        ));
        form.extend(ref_forms(
            "source_refs",
            Some(need(rec, "source_refs")?),
            "source_id",
            "locator",
        )?);
        let mut params = vec![sym("parameters")];
        if let Value::Object(pairs) = need(rec, "parameters")? {
            for (name, v) in pairs {
                params.push(Sexp::List(vec![
                    sym("param"),
                    pair("name", sym(name)),
                    pair("value", json_to_value(name, v)?),
                ]));
            }
        }
        form.push(Sexp::List(params));
        form.extend(repeated("dependencies", Some(need(rec, "dependencies")?))?);
        form.extend(repeated(
            "required_checks",
            Some(need(rec, "required_checks")?),
        )?);
        return Ok(Sexp::List(form));
    }
    let mut keys: Vec<&str> = match rec {
        Value::Object(pairs) => pairs.iter().map(|(k, _)| k.as_str()).collect(),
        _ => Vec::new(),
    };
    keys.sort();
    Err(refused(format!(
        "not a record dict: keys {}",
        py_repr(&Sexp::List(
            keys.into_iter().map(|k| Sexp::Str(k.to_owned())).collect()
        ))
    )))
}

// ── rendering ────────────────────────────────────────────────────────────────────────────────

/// Render one literal string with the canonical reader's closed escapes.
pub fn quote_string(value: &str) -> String {
    let mut out = String::from("\"");
    for c in value.chars() {
        match c {
            '\\' => out.push_str("\\\\"),
            '"' => out.push_str("\\\""),
            '\n' => out.push_str("\\n"),
            '\t' => out.push_str("\\t"),
            '\r' => out.push_str("\\r"),
            c => out.push(c),
        }
    }
    out.push('"');
    out
}

fn render(form: &Sexp) -> String {
    match form {
        Sexp::List(items) => {
            let parts: Vec<String> = items.iter().map(render).collect();
            format!("({})", parts.join(" "))
        }
        Sexp::Symbol(s) => s.clone(),
        Sexp::Int(n) => n.to_string(),
        Sexp::Str(s) => quote_string(s),
    }
}

/// One form per line — the compact shape that keeps the dossier under its per-part bound.
pub fn render_forms(forms: &[Sexp]) -> String {
    forms.iter().map(|f| format!("{}\n", render(f))).collect()
}

pub fn dump(records: &[Value]) -> Result<String, RecordError> {
    let forms: Result<Vec<Sexp>, RecordError> = records.iter().map(dict_to_form).collect();
    Ok(render_forms(&forms?))
}

// ── files: the catalogue reader's include expansion (`record_catalog.text`), ported ──────────

/// `record_catalog.CatalogRefused`, the pinned words.
fn catalog_refused(text: String) -> RecordError {
    RecordError::Refused(RecordRefused(text))
}

/// Top-level form spans: (start, end) character offsets of every top-level `( … )`, as `sexp.forms_with_spans`.
fn top_level_spans(text: &str) -> Vec<(usize, usize)> {
    let chars: Vec<char> = text.chars().collect();
    let mut spans = Vec::new();
    let mut depth = 0usize;
    let mut start = 0usize;
    let mut i = 0usize;
    while i < chars.len() {
        match chars[i] {
            ';' => {
                while i < chars.len() && chars[i] != '\n' {
                    i += 1;
                }
            }
            '"' => {
                i += 1;
                while i < chars.len() && chars[i] != '"' {
                    if chars[i] == '\\' {
                        i += 1;
                    }
                    i += 1;
                }
            }
            '(' => {
                if depth == 0 {
                    start = i;
                }
                depth += 1;
            }
            ')' => {
                depth = depth.saturating_sub(1);
                if depth == 0 {
                    spans.push((start, i + 1));
                }
            }
            _ => {}
        }
        i += 1;
    }
    spans
}

fn resolved(p: &Path) -> std::path::PathBuf {
    std::fs::canonicalize(p).unwrap_or_else(|_| p.to_path_buf())
}

fn expand(
    current: &Path,
    anchor: &Path,
    stack: &[std::path::PathBuf],
    seen: &mut Vec<std::path::PathBuf>,
    part: bool,
) -> Result<String, RecordError> {
    let current = resolved(current);
    let name = current
        .file_name()
        .map(|n| n.to_string_lossy().into_owned())
        .unwrap_or_default();
    if stack.contains(&current) {
        return Err(catalog_refused(format!("INCLUDE-CYCLE: {name}")));
    }
    if seen.contains(&current) {
        return Err(catalog_refused(format!("DUPLICATE-PART: {name}")));
    }
    seen.push(current.clone());
    let source = match std::fs::read(&current) {
        Ok(bytes) => match String::from_utf8(bytes) {
            Ok(t) => t,
            Err(e) => {
                return Err(catalog_refused(format!(
                    "UNREADABLE-PART: {name}: {}",
                    e.utf8_error()
                )))
            }
        },
        Err(e) => return Err(catalog_refused(format!("UNREADABLE-PART: {name}: {e}"))),
    };
    let forms = sexp::parse(&source, &current.display().to_string())?;
    let spans = top_level_spans(&source);
    let head_of = |f: &Sexp| -> Option<String> {
        if let Sexp::List(l) = f {
            l.first().and_then(Sexp::text).map(str::to_owned)
        } else {
            None
        }
    };
    let includes: Vec<usize> = forms
        .iter()
        .enumerate()
        .filter(|(_, f)| head_of(f).as_deref() == Some("include-obligations"))
        .map(|(i, _)| i)
        .collect();
    let obligation_family =
        name == "contract-obligations.sexp" || name.ends_with(".obligations.sexp");
    let composed = !includes.is_empty();
    if composed && !obligation_family {
        return Err(catalog_refused(format!(
            "INCLUDE-FAMILY: {name} is not an obligation catalog"
        )));
    }
    if !includes.is_empty() || part {
        if current.strip_prefix(anchor).is_err() {
            return Err(catalog_refused(format!(
                "CATALOG-ROOT: {name} is outside the selected root"
            )));
        }
        for f in &forms {
            if !matches!(
                head_of(f).as_deref(),
                Some("obligation" | "comment" | "include-obligations")
            ) {
                return Err(catalog_refused(format!(
                    "PART-FORM: {name} contains a non-obligation form"
                )));
            }
        }
    }
    let chars: Vec<char> = source.chars().collect();
    let mut pieces = String::new();
    let mut cursor = 0usize;
    for (i, f) in forms.iter().enumerate() {
        if head_of(f).as_deref() != Some("include-obligations") {
            continue;
        }
        let (start, end) = spans.get(i).copied().ok_or_else(|| {
            catalog_refused("INCLUDE-SHAPE: expected one quoted path field".to_owned())
        })?;
        let value = match f {
            Sexp::List(l) if l.len() == 2 => match &l[1] {
                Sexp::List(p) if p.len() == 2 && p[0] == Sexp::Symbol("path".to_owned()) => {
                    match &p[1] {
                        Sexp::Str(v) => v.clone(),
                        _ => {
                            return Err(catalog_refused(
                                "INCLUDE-SHAPE: expected one quoted path field".to_owned(),
                            ))
                        }
                    }
                }
                _ => {
                    return Err(catalog_refused(
                        "INCLUDE-SHAPE: expected one quoted path field".to_owned(),
                    ))
                }
            },
            _ => {
                return Err(catalog_refused(
                    "INCLUDE-SHAPE: expected one quoted path field".to_owned(),
                ))
            }
        };
        let parts: Vec<&str> = value.split('/').collect();
        let canonical = !value.is_empty()
            && !value.contains('\\')
            && !value.chars().any(|c| (c as u32) < 32)
            && !value.starts_with('/')
            && !parts.contains(&"..")
            && !parts.iter().any(|p| p.is_empty() || *p == ".")
            && !value.ends_with('/')
            && !(value.len() >= 2
                && value.as_bytes()[0].is_ascii_alphabetic()
                && value.as_bytes()[1] == b':');
        if !canonical {
            return Err(catalog_refused(format!(
                "INCLUDE-PATH: expected canonical repository-relative path: {}",
                sexp::py_repr(&Sexp::Str(value.clone()))
            )));
        }
        let target = resolved(&anchor.join(&value));
        if target.strip_prefix(anchor).is_err() {
            return Err(catalog_refused(format!("INCLUDE-ESCAPE: {value}")));
        }
        let mut deeper = stack.to_vec();
        deeper.push(current.clone());
        let mut replacement = expand(&target, anchor, &deeper, seen, true)?;
        if replacement.ends_with('\n') && chars.get(end) == Some(&'\n') {
            replacement.pop();
        }
        pieces.extend(chars[cursor..start].iter());
        pieces.push_str(&replacement);
        cursor = end;
    }
    pieces.extend(chars[cursor..].iter());
    Ok(pieces)
}

/// `record_catalog.text(path, root=)`: the catalogue with its include directives expanded exactly.
pub fn catalog_text(path: &Path, root: &Path) -> Result<String, RecordError> {
    let anchor = resolved(root);
    let mut seen = Vec::new();
    expand(path, &anchor, &[], &mut seen, false)
}

/// `load(path, root=)`: a converted record file as JSON-shaped records, in file order; annotations add no records.
pub fn load(path: &Path, root: &Path) -> Result<Vec<Value>, RecordError> {
    let text = catalog_text(path, root)?;
    let forms = sexp::parse(&text, &path.display().to_string())?;
    let mut out = Vec::new();
    for f in &forms {
        if matches!(f, Sexp::List(l) if l.first().and_then(Sexp::text) == Some("comment")) {
            continue;
        }
        out.push(form_to_dict(f)?);
    }
    Ok(out)
}

/// `cargo xtask records <catalogue> [--dump]`: the records as one JSON object per line, as the pinned mapping reads
/// them — or, with `--dump`, rendered back through the mapping (`dump(load(x))`), for checking a file by hand.
pub fn run(root: &Path, args: &[String]) -> std::process::ExitCode {
    let (path, render_back) = match args {
        [path] => (path, false),
        [path, flag] if flag == "--dump" => (path, true),
        _ => {
            eprintln!("usage: cargo xtask records <catalogue.sexp> [--dump]   # JSON lines as the pinned mapping reads them; --dump renders them back");
            return std::process::ExitCode::from(2);
        }
    };
    let records = match load(Path::new(path), root) {
        Ok(records) => records,
        Err(e) => {
            eprintln!("REFUSED: {e}");
            return std::process::ExitCode::from(1);
        }
    };
    if render_back {
        match dump(&records) {
            Ok(text) => print!("{text}"),
            Err(e) => {
                eprintln!("REFUSED: {e}");
                return std::process::ExitCode::from(1);
            }
        }
        return std::process::ExitCode::SUCCESS;
    }
    for r in &records {
        println!("{}", json_dumps(r));
    }
    std::process::ExitCode::SUCCESS
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write as _;
    use std::process::{Command, Stdio};

    /// The record catalogues the mapping serves: every tracked file the RECORD-SCHEMA map names, plus the obligation parts.
    fn corpus(root: &Path) -> Vec<String> {
        let listed = Command::new("git")
            .args(["ls-files", "-z", "*.sexp"])
            .current_dir(root)
            .output()
            .expect("git ls-files");
        String::from_utf8_lossy(&listed.stdout)
            .split('\0')
            .filter(|f| {
                let name = f.rsplit('/').next().unwrap_or("");
                !f.starts_with("schema/")
                    && (matches!(
                        name,
                        "requirements.sexp"
                            | "contract-obligations.sexp"
                            | "units.sexp"
                            | "category-needs.sexp"
                    ) || (name.starts_with("contract-v")
                        && name.ends_with(".obligations.sexp")))
            })
            .map(str::to_owned)
            .collect()
    }

    /// Every catalogue reads as the pinned `scripts/records_sexp.py` reads it: the same records, in order, down to the
    /// JSON dump's bytes — one comparator process over the whole corpus. An absent comparator fails, never skips.
    #[test]
    fn the_catalogues_read_as_the_pinned_mapping_reads_them() {
        let root = std::env::var("XT0023_ROOT")
            .map(std::path::PathBuf::from)
            .unwrap_or_else(|_| {
                Path::new(env!("CARGO_MANIFEST_DIR"))
                    .parent()
                    .expect("the workspace root")
                    .to_path_buf()
            });
        let files = corpus(&root);
        assert!(
            files.len() >= 12,
            "the corpus census found only {} catalogues",
            files.len()
        );
        let program = concat!(
            "import json, sys\nsys.path.insert(0, 'scripts'); sys.dont_write_bytecode = True\n",
            "import records_sexp as R\nfrom pathlib import Path\n",
            "for f in sys.stdin.read().split('\\0'):\n    if not f: continue\n    print('== ' + f)\n",
            "    try:\n        for r in R.load(Path(f), root=Path('.')): print(json.dumps(r, ensure_ascii=False))\n",
            "    except Exception as e: print('REFUSED: ' + str(e))\n",
        );
        let mut child = Command::new("python3")
            .args(["-I", "-c", program])
            .current_dir(&root)
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .spawn()
            .expect("python3 is the comparator");
        child
            .stdin
            .take()
            .expect("stdin")
            .write_all(files.join("\0").as_bytes())
            .expect("file list");
        let output = child.wait_with_output().expect("python3 finished");
        assert!(
            output.status.success(),
            "the pinned mapping failed: {}",
            String::from_utf8_lossy(&output.stderr)
        );
        let mut ours = String::new();
        for f in &files {
            ours.push_str(&format!("== {f}\n"));
            match load(&root.join(f), &root) {
                Ok(records) => {
                    for r in &records {
                        ours.push_str(&json_dumps(r));
                        ours.push('\n');
                    }
                }
                Err(e) => ours.push_str(&format!("REFUSED: {e}\n")),
            }
        }
        let theirs = String::from_utf8_lossy(&output.stdout);
        if theirs != ours {
            let first = theirs
                .lines()
                .zip(ours.lines())
                .position(|(a, b)| a != b)
                .unwrap_or(0);
            panic!("the mappings disagree ({} catalogues); first differing line {}:\n pinned: {}\n   ours: {}", files.len(), first + 1,
                   theirs.lines().nth(first).unwrap_or(""), ours.lines().nth(first).unwrap_or(""));
        }
    }

    /// `dump(load(x))` of the mapping's own renderings matches the pinned renderer: the three catalogues that are
    /// byte-identical round trips under the pinned tool are byte-identical under this one too.
    #[test]
    fn the_renderer_round_trips_the_rendered_catalogues() {
        let root = std::env::var("XT0023_ROOT")
            .map(std::path::PathBuf::from)
            .unwrap_or_else(|_| {
                Path::new(env!("CARGO_MANIFEST_DIR"))
                    .parent()
                    .expect("the workspace root")
                    .to_path_buf()
            });
        for f in [
            "profiles/netboard-lab-v0/contract-obligations.sexp",
            "profiles/netboard-lab-v0/requirements.sexp",
            "profiles/rv64gc-lab-v0/contract-v1.obligations.sexp",
        ] {
            let records = load(&root.join(f), &root).expect("loads");
            let text = dump(&records).expect("dumps");
            assert_eq!(
                text,
                std::fs::read_to_string(root.join(f)).expect("read"),
                "{f}"
            );
        }
    }
}
