//! The S-expression schema validator (`XTASK.6` slice `6l`), ported from the pinned `scripts/check_sexp_schema.py`,
//! which stays the definition: a schema is data (`schema/`) declaring constructs, their fields (atom types, repetition,
//! optionality, markers, facets) and operators (positional mini-languages); a document is refused BY NAME for an
//! undeclared construct or field, a missing required field, a wrong arity, a wrong value type, a duplicated single-valued
//! field, or a facet it fails. Every refusal is the pinned validator's text, byte for byte (Python's `repr` of the
//! offending value through `sexp::py_repr`). Regex facets are matched by a small anchored matcher over the subset the
//! corpus declares (classes, counted repeats, groups with alternation, literals); a pattern outside it is refused by name.

use std::collections::BTreeMap;
use std::path::Path;

use crate::sexp::{self, py_repr, Sexp, SexpError};

/// A refusal: one error names the construct, the field and the reason.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SchemaError(pub String);

impl std::fmt::Display for SchemaError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(&self.0)
    }
}

fn err(text: String) -> SchemaError {
    SchemaError(text)
}

/// Python's `isinstance(x, list) and not isinstance(x, Symbol)` — a real list.
fn as_list(v: &Sexp) -> Option<&Vec<Sexp>> {
    match v {
        Sexp::List(items) => Some(items),
        _ => None,
    }
}

fn symbol(v: &Sexp) -> Option<&str> {
    match v {
        Sexp::Symbol(s) => Some(s),
        _ => None,
    }
}

fn is_comment(form: &Sexp) -> bool {
    matches!(form, Sexp::List(l) if l.first().and_then(symbol) == Some("comment"))
}

/// `_check_comment`: a `(comment …)` annotation holds strings only.
fn check_comment(form: &Sexp, where_: &str) -> Result<(), SchemaError> {
    let Some(items) = as_list(form) else {
        return Ok(());
    };
    if items.len() < 2 {
        return Err(err(format!(
            "{where_}: (comment …) carries at least one string, got none — an empty comment is silence, and silence is not annotation"
        )));
    }
    for el in items.iter().skip(1) {
        if !matches!(el, Sexp::Str(_)) {
            return Err(err(format!(
                "{where_}: a comment line is a plain string, got {}",
                py_repr(el)
            )));
        }
    }
    Ok(())
}

/// `_atom`: a declaration value must be a single atom.
fn atom<'a>(form: &'a Sexp, where_: &str) -> Result<&'a Sexp, SchemaError> {
    match form {
        Sexp::List(_) => Err(err(format!(
            "{where_}: expected an atom, got {}",
            py_repr(form)
        ))),
        other => Ok(other),
    }
}

/// `_pairs`: the `(name value)` children of a declaration.
fn pairs<'a>(form: &'a Sexp, where_: &str) -> Result<Vec<(String, &'a Sexp)>, SchemaError> {
    let mut out = Vec::new();
    for el in as_list(form).map(|l| &l[1..]).unwrap_or(&[]) {
        let Some(items) = as_list(el).filter(|l| !l.is_empty()) else {
            return Err(err(format!(
                "{where_}: expected a (name value) pair, got {}",
                py_repr(el)
            )));
        };
        if items.len() != 2 {
            return Err(err(format!(
                "{where_}: wrong arity — a field is a two-element (name value) pair, got {} element(s) in {}",
                items.len(),
                py_repr(el)
            )));
        }
        let Some(name) = symbol(&items[0]) else {
            return Err(err(format!(
                "{where_}: a field name must be a bare symbol, got {}",
                py_repr(&items[0])
            )));
        };
        out.push((name.to_owned(), &items[1]));
    }
    Ok(out)
}

/// `_group`: single-valued keys once, multi-valued keys collected, anything else undeclared.
struct Group<'a> {
    single: BTreeMap<String, &'a Sexp>,
    multi: BTreeMap<String, Vec<&'a Sexp>>,
}

fn group<'a>(
    pairs: Vec<(String, &'a Sexp)>,
    where_: &str,
    single: &[&str],
    multi: &[&str],
) -> Result<Group<'a>, SchemaError> {
    let mut g = Group {
        single: BTreeMap::new(),
        multi: BTreeMap::new(),
    };
    for (k, v) in pairs {
        if single.contains(&k.as_str()) {
            if g.single.contains_key(&k) {
                return Err(err(format!(
                    "{where_}: duplicated field {}",
                    py_repr(&Sexp::Str(k))
                )));
            }
            g.single.insert(k, v);
        } else if multi.contains(&k.as_str()) {
            g.multi.entry(k).or_default().push(v);
        } else {
            return Err(err(format!(
                "{where_}: undeclared field {} in a field declaration",
                py_repr(&Sexp::Str(k))
            )));
        }
    }
    Ok(g)
}

#[derive(Debug, Clone)]
pub struct Field {
    pub name: String,
    /// `None` is a pure marker (`(empty yes)`, no type).
    pub type_: Option<String>,
    pub heads: Vec<String>,
    pub values: Option<Vec<String>>,
    pub repeat: bool,
    pub optional: bool,
    pub empty: bool,
    pub unique: bool,
    pub pattern: Option<String>,
    pub min_length: Option<i128>,
    pub min: Option<i128>,
}

fn flag(g: &Group<'_>, key: &str, name: &str, where_: &str) -> Result<bool, SchemaError> {
    match g.single.get(key) {
        None => Ok(false),
        Some(v) => {
            let v = atom(v, where_)?;
            match v.text() {
                Some("yes") => Ok(true),
                Some("no") => Ok(false),
                _ => Err(err(format!(
                    "{where_}: field {name}: ({key} …) is yes or no, got {}",
                    py_repr(v)
                ))),
            }
        }
    }
}

fn nonneg(v: &Sexp) -> Option<i128> {
    match v {
        Sexp::Int(n) if *n >= 0 => Some(*n),
        _ => None,
    }
}

impl Field {
    fn parse(where_: &str, form: &Sexp) -> Result<Field, SchemaError> {
        let g = group(
            pairs(form, where_)?,
            where_,
            &[
                "name",
                "type",
                "repeat",
                "optional",
                "empty",
                "pattern",
                "min-length",
                "min",
                "unique",
            ],
            &["head", "values"],
        )?;
        let Some(name_v) = g.single.get("name") else {
            return Err(err(format!(
                "{where_}: a (field …) needs exactly one (name SYM)"
            )));
        };
        let name_v = atom(name_v, where_)?;
        let Some(name) = symbol(name_v) else {
            return Err(err(format!(
                "{where_}: field name must be a bare symbol, got {}",
                py_repr(name_v)
            )));
        };
        let name = name.to_owned();
        if name == "comment" {
            return Err(err(format!(
                "{where_}: field name 'comment' is reserved — the annotation form is skipped everywhere, so a field with that name is dead vocabulary"
            )));
        }
        let type_ = match g.single.get("type") {
            None => {
                let empty_yes = g.single.get("empty").and_then(|v| v.text()) == Some("yes");
                if !empty_yes {
                    return Err(err(format!(
                        "{where_}: field {} has no (type …) — a marker field declares (empty yes) instead",
                        py_repr(&Sexp::Str(name.clone()))
                    )));
                }
                None
            }
            Some(v) => Some(atom(v, where_)?.clone()),
        };
        let type_name: Option<String> = match &type_ {
            None => None,
            Some(t) => {
                let text = t.text().map(str::to_owned);
                if !matches!(
                    text.as_deref(),
                    Some("symbol" | "string" | "integer" | "form")
                ) {
                    return Err(err(format!(
                        "{where_}: field {name}: unknown type {} — one of symbol string integer form",
                        py_repr(t)
                    )));
                }
                text
            }
        };
        let mut heads = Vec::new();
        for h in g.multi.get("head").into_iter().flatten() {
            heads.push(atom(h, where_)?.text().unwrap_or_default().to_owned());
        }
        let values: Option<Vec<String>> = match g.multi.get("values") {
            None => None,
            Some(vs) => {
                let mut set: Vec<String> = Vec::new();
                for v in vs {
                    let t = atom(v, where_)?.text().unwrap_or_default().to_owned();
                    if !set.contains(&t) {
                        set.push(t);
                    }
                }
                Some(set)
            }
        };
        if type_name.as_deref() == Some("form") {
            if heads.is_empty() {
                return Err(err(format!(
                    "{where_}: field {name} is (type form) but names no (head SYM) — which constructs may it be?"
                )));
            }
            if values.as_ref().is_some_and(|v| !v.is_empty()) {
                return Err(err(format!(
                    "{where_}: field {name} declares (values …) but is not (type symbol)"
                )));
            }
        } else if !heads.is_empty() {
            return Err(err(format!(
                "{where_}: field {name} declares (head …) but is not (type form)"
            )));
        }
        if g.single.contains_key("empty") && type_name.as_deref() == Some("form") {
            return Err(err(format!(
                "{where_}: field {name}: (empty yes) is for atom fields — a form field's emptiness is its construct's business"
            )));
        }
        let repeat = flag(&g, "repeat", &name, where_)?;
        let optional = flag(&g, "optional", &name, where_)?;
        let empty = flag(&g, "empty", &name, where_)?;
        let unique = flag(&g, "unique", &name, where_)?;
        let mut pattern = None;
        if let Some(p) = g.single.get("pattern") {
            if type_name.as_deref() != Some("string") {
                return Err(err(format!(
                    "{where_}: field {name}: (pattern …) constrains a string field, not type {}",
                    type_
                        .as_ref()
                        .map(py_repr)
                        .unwrap_or_else(|| "None".to_owned())
                )));
            }
            let Sexp::Str(pat) = p else {
                return Err(err(format!(
                    "{where_}: field {name}: (pattern …) takes a quoted regex string, got {}",
                    py_repr(p)
                )));
            };
            if let Err(reason) = regex_compile(pat) {
                return Err(err(format!(
                    "{where_}: field {name}: (pattern …) is not a valid regex: {reason}"
                )));
            }
            pattern = Some(pat.clone());
        }
        let mut min_length = None;
        if let Some(n) = g.single.get("min-length") {
            if type_name.as_deref() != Some("string") {
                return Err(err(format!(
                    "{where_}: field {name}: (min-length …) constrains a string field, not type {}",
                    type_
                        .as_ref()
                        .map(py_repr)
                        .unwrap_or_else(|| "None".to_owned())
                )));
            }
            let Some(v) = nonneg(n) else {
                return Err(err(format!(
                    "{where_}: field {name}: (min-length N) takes one non-negative integer, got {}",
                    py_repr(n)
                )));
            };
            min_length = Some(v);
        }
        let mut min = None;
        if let Some(n) = g.single.get("min") {
            if !repeat {
                return Err(err(format!("{where_}: field {name}: (min N) belongs to a (repeat yes) field — it counts occurrences")));
            }
            let Some(v) = nonneg(n) else {
                return Err(err(format!(
                    "{where_}: field {name}: (min N) takes one non-negative integer, got {}",
                    py_repr(n)
                )));
            };
            min = Some(v);
        }
        if unique && !repeat {
            return Err(err(format!("{where_}: field {name}: (unique yes) belongs to a (repeat yes) field — singularity is its own constraint")));
        }
        Ok(Field {
            name,
            type_: type_name,
            heads,
            values,
            repeat,
            optional,
            empty,
            unique,
            pattern,
            min_length,
            min,
        })
    }
}

#[derive(Debug, Clone)]
pub struct Construct {
    pub name: String,
    /// Declaration order kept: the pinned validator reports the first offender in that order.
    pub fields: Vec<Field>,
}

impl Construct {
    fn field(&self, name: &str) -> Option<&Field> {
        self.fields.iter().find(|f| f.name == name)
    }

    fn parse(where_: &str, name: &Sexp, field_forms: &[&Sexp]) -> Result<Construct, SchemaError> {
        let Some(n) = symbol(name) else {
            return Err(err(format!(
                "{where_}: construct name must be a bare symbol, got {}",
                py_repr(name)
            )));
        };
        let mut fields: Vec<Field> = Vec::new();
        for f in field_forms {
            let fld = Field::parse(&format!("{where_} construct {n}"), f)?;
            if fields.iter().any(|x| x.name == fld.name) {
                return Err(err(format!(
                    "{where_}: construct {n} declares field {} twice",
                    py_repr(&Sexp::Str(fld.name.clone()))
                )));
            }
            fields.push(fld);
        }
        Ok(Construct {
            name: n.to_owned(),
            fields,
        })
    }
}

fn declare(constructs: &mut Vec<Construct>, form: &Sexp, where_: &str) -> Result<(), SchemaError> {
    let children: Vec<&Sexp> = as_list(form)
        .map(|l| {
            l.iter()
                .skip(1)
                .filter(|c| as_list(c).is_some_and(|x| !x.is_empty()))
                .collect()
        })
        .unwrap_or_default();
    for c in &children {
        if is_comment(c) {
            check_comment(c, where_)?;
        }
    }
    let children: Vec<&Sexp> = children.into_iter().filter(|c| !is_comment(c)).collect();
    let head_text = |c: &Sexp| {
        as_list(c)
            .and_then(|l| l.first())
            .and_then(Sexp::text)
            .map(str::to_owned)
    };
    let is_name = |c: &Sexp| head_text(c).as_deref() == Some("name");
    let is_field = |c: &Sexp| head_text(c).as_deref() == Some("field");
    let name_forms: Vec<&Sexp> = children.iter().copied().filter(|c| is_name(c)).collect();
    let field_forms: Vec<&Sexp> = children.iter().copied().filter(|c| is_field(c)).collect();
    if let Some(stray) = children.iter().find(|c| !is_name(c) && !is_field(c)) {
        return Err(err(format!(
            "{where_}: a (construct …) holds something that is not (name …) or (field …): {}",
            py_repr(stray)
        )));
    }
    if name_forms.len() != 1 {
        return Err(err(format!(
            "{where_}: a (construct …) needs exactly one (name SYM), got {}",
            name_forms.len()
        )));
    }
    let name_value = as_list(name_forms[0])
        .and_then(|l| l.get(1))
        .ok_or_else(|| err("list index out of range".to_owned()))?;
    let c = Construct::parse(where_, name_value, &field_forms)?;
    if c.name == "comment" {
        return Err(err(format!(
            "{where_}: construct name 'comment' is reserved for the annotation form — validation skips it, so a construct with that name is dead vocabulary"
        )));
    }
    if constructs.iter().any(|x| x.name == c.name) {
        return Err(err(format!(
            "{where_}: construct {} declared twice",
            py_repr(&Sexp::Str(c.name.clone()))
        )));
    }
    constructs.push(c);
    Ok(())
}

/// One positional argument spec: an atom kind, `expr`, or a fixed tuple of atom kinds.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ArgSpec {
    Kind(String),
    Tuple(Vec<String>),
}

const ARG_KINDS: [&str; 4] = ["symbol", "integer", "string", "expr"];

#[derive(Debug, Clone)]
pub struct Operator {
    pub name: String,
    pub fixed: Option<i128>,
    pub min: i128,
    pub spec: ArgSpec,
}

fn kinds_repr() -> String {
    py_repr(&Sexp::List(
        ARG_KINDS
            .iter()
            .map(|k| Sexp::Str((*k).to_owned()))
            .collect(),
    ))
}

impl Operator {
    fn parse(where_: &str, form: &Sexp) -> Result<Operator, SchemaError> {
        let mut name: Option<&Sexp> = None;
        let mut fixed: Option<i128> = None;
        let mut variadic = false;
        let mut min_v: Option<i128> = None;
        let mut arg: Option<&Sexp> = None;
        for child in as_list(form).map(|l| &l[1..]).unwrap_or(&[]) {
            let Some(items) = as_list(child).filter(|l| !l.is_empty()) else {
                return Err(err(format!(
                    "{where_}: an (operator …) holds a declaration list, got {}",
                    py_repr(child)
                )));
            };
            let Some(key) = symbol(&items[0]) else {
                return Err(err(format!(
                    "{where_}: an operator declaration is headed by a bare symbol, got {}",
                    py_repr(&items[0])
                )));
            };
            let arity = items.len();
            match key {
                "name" => {
                    if name.is_some() {
                        return Err(err(format!(
                            "{where_}: duplicated (name …) in an operator declaration"
                        )));
                    }
                    if arity != 2 {
                        return Err(err(format!(
                            "{where_}: (name …) takes one symbol, got {}",
                            py_repr(child)
                        )));
                    }
                    name = Some(&items[1]);
                }
                "fixed" => {
                    if fixed.is_some() {
                        return Err(err(format!(
                            "{where_}: duplicated (fixed …) in an operator declaration"
                        )));
                    }
                    let Some(n) = (arity == 2).then(|| nonneg(&items[1])).flatten() else {
                        return Err(err(format!(
                            "{where_}: (fixed N) takes one non-negative integer, got {}",
                            py_repr(child)
                        )));
                    };
                    fixed = Some(n);
                }
                "variadic" => {
                    if arity != 1 {
                        return Err(err(format!(
                            "{where_}: (variadic) is a bare marker, got {}",
                            py_repr(child)
                        )));
                    }
                    variadic = true;
                }
                "min" => {
                    if min_v.is_some() {
                        return Err(err(format!(
                            "{where_}: duplicated (min …) in an operator declaration"
                        )));
                    }
                    let Some(n) = (arity == 2).then(|| nonneg(&items[1])).flatten() else {
                        return Err(err(format!(
                            "{where_}: (min N) takes one non-negative integer, got {}",
                            py_repr(child)
                        )));
                    };
                    min_v = Some(n);
                }
                "arg" => {
                    if arg.is_some() {
                        return Err(err(format!(
                            "{where_}: duplicated (arg …) in an operator declaration"
                        )));
                    }
                    if arity != 2 {
                        return Err(err(format!(
                            "{where_}: (arg SPEC) takes one spec, got {}",
                            py_repr(child)
                        )));
                    }
                    arg = Some(&items[1]);
                }
                other => {
                    return Err(err(format!(
                        "{where_}: undeclared field {} in an operator declaration",
                        py_repr(&Sexp::Str(other.to_owned()))
                    )));
                }
            }
        }
        let Some(name) = name else {
            return Err(err(format!(
                "{where_}: an (operator …) needs exactly one (name SYM)"
            )));
        };
        let Some(n) = symbol(name) else {
            return Err(err(format!(
                "{where_}: operator name must be a bare symbol, got {}",
                py_repr(name)
            )));
        };
        if fixed.is_none() != variadic {
            return Err(err(format!(
                "{where_}: operator {} declares exactly one of (fixed N) / (variadic)",
                py_repr(&Sexp::Str(n.to_owned()))
            )));
        }
        if min_v.is_some() && !variadic {
            return Err(err(format!(
                "{where_}: operator {}: (min …) belongs to (variadic), not (fixed N)",
                py_repr(&Sexp::Str(n.to_owned()))
            )));
        }
        let spec = match arg {
            None => ArgSpec::Kind("expr".to_owned()),
            Some(a) => Self::spec(where_, a)?,
        };
        Ok(Operator {
            name: n.to_owned(),
            fixed,
            min: min_v.unwrap_or(1),
            spec,
        })
    }

    fn spec(where_: &str, value: &Sexp) -> Result<ArgSpec, SchemaError> {
        if let Some(s) = symbol(value) {
            if !ARG_KINDS.contains(&s) {
                return Err(err(format!(
                    "{where_}: unknown argument kind {} — one of {}",
                    py_repr(value),
                    kinds_repr()
                )));
            }
            return Ok(ArgSpec::Kind(s.to_owned()));
        }
        if let Some(items) = as_list(value).filter(|l| !l.is_empty()) {
            let mut kinds = Vec::new();
            for el in items {
                match symbol(el) {
                    Some(k) if ARG_KINDS.contains(&k) && k != "expr" => kinds.push(k.to_owned()),
                    _ => {
                        return Err(err(format!(
                            "{where_}: a tuple argument spec holds atom kinds, got {}",
                            py_repr(value)
                        )));
                    }
                }
            }
            return Ok(ArgSpec::Tuple(kinds));
        }
        Err(err(format!(
            "{where_}: (arg SPEC) wants an atom kind or a list of atom kinds, got {}",
            py_repr(value)
        )))
    }
}

/// A loaded schema: constructs and operators, in declaration order.
pub struct Schema {
    pub constructs: Vec<Construct>,
    pub operators: Vec<Operator>,
}

impl Schema {
    fn construct(&self, name: &str) -> Option<&Construct> {
        self.constructs.iter().find(|c| c.name == name)
    }
    fn operator(&self, name: &str) -> Option<&Operator> {
        self.operators.iter().find(|o| o.name == name)
    }
}

/// The schema file read and checked at the meta level; a `SexpError` is the reader's own refusal.
pub fn load_schema(path: &Path) -> Result<Schema, LoadError> {
    let shown = path.display().to_string();
    let name = path
        .file_name()
        .map(|n| n.to_string_lossy().into_owned())
        .unwrap_or_default();
    let forms = sexp::read_file(path).map_err(LoadError::Sexp)?;
    let mut constructs: Vec<Construct> = Vec::new();
    let mut operators: Vec<Operator> = Vec::new();
    for form in &forms {
        if as_list(form).is_none_or(Vec::is_empty) {
            return Err(LoadError::Schema(err(format!(
                "{name}: a schema is made of (schema …)/(construct …)/(operator …) forms, got {}",
                py_repr(form)
            ))));
        }
        let head = sexp::head(form, &shown).map_err(LoadError::Sexp)?;
        if is_comment(form) {
            check_comment(form, &name).map_err(LoadError::Schema)?;
            continue;
        }
        match head.as_str() {
            "schema" => continue,
            "construct" => declare(&mut constructs, form, &name).map_err(LoadError::Schema)?,
            "operator" => {
                let op = Operator::parse(&name, form).map_err(LoadError::Schema)?;
                if op.name == "comment" {
                    return Err(LoadError::Schema(err(format!(
                        "{name}: operator name 'comment' is reserved for the annotation form"
                    ))));
                }
                if constructs.iter().any(|c| c.name == op.name) {
                    return Err(LoadError::Schema(err(format!(
                        "{name}: {} is declared both as a construct and as an operator",
                        py_repr(&Sexp::Str(op.name.clone()))
                    ))));
                }
                if operators.iter().any(|o| o.name == op.name) {
                    return Err(LoadError::Schema(err(format!(
                        "{name}: operator {} declared twice",
                        py_repr(&Sexp::Str(op.name.clone()))
                    ))));
                }
                operators.push(op);
            }
            other => {
                return Err(LoadError::Schema(err(format!(
                    "{name}: undeclared top-level construct \"{other}\" in a schema — only (schema …), (construct …) and (operator …) may live here"
                ))));
            }
        }
    }
    if constructs.is_empty() {
        return Err(LoadError::Schema(err(format!(
            "{name}: the schema declares no constructs"
        ))));
    }
    for c in &constructs {
        for fld in &c.fields {
            for h in &fld.heads {
                if !constructs.iter().any(|x| &x.name == h)
                    && !operators.iter().any(|o| &o.name == h)
                {
                    return Err(LoadError::Schema(err(format!(
                        "{name}: construct {} field {} allows undeclared head {}",
                        py_repr(&Sexp::Str(c.name.clone())),
                        py_repr(&Sexp::Str(fld.name.clone())),
                        py_repr(&Sexp::Str(h.clone()))
                    ))));
                }
            }
        }
    }
    Ok(Schema {
        constructs,
        operators,
    })
}

/// What `load_schema` can refuse: the schema's own grammar, or its bytes.
#[derive(Debug)]
pub enum LoadError {
    Schema(SchemaError),
    Sexp(SexpError),
}

impl std::fmt::Display for LoadError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            LoadError::Schema(e) => f.write_str(&e.0),
            LoadError::Sexp(e) => f.write_str(&e.0),
        }
    }
}

// ── the anchored regex subset the schemas declare ────────────────────────────────────────────
// `^` and `\Z`, literals (escaped punctuation), character classes with ranges, `( … | … )` groups,
// and the quantifiers `* + ? {n} {n,m}`. Anything else is refused by name at schema load: a new
// facet shape is a kernel question, never a silent mismatch. Python's `re.search` semantics.

#[derive(Debug, Clone)]
enum Node {
    Start,
    End,
    Dollar,
    Lit(char),
    Class(Vec<(char, char)>, bool),
    Group(Vec<Vec<Node>>),
    Repeat(Box<Node>, usize, Option<usize>),
}

pub struct Regex {
    nodes: Vec<Node>,
}

fn parse_class(chars: &[char], i: &mut usize) -> Result<Node, String> {
    // chars[*i] == '['
    *i += 1;
    let mut negated = false;
    if chars.get(*i) == Some(&'^') {
        negated = true;
        *i += 1;
    }
    let mut ranges = Vec::new();
    let mut first = true;
    loop {
        let Some(&c) = chars.get(*i) else {
            return Err("unterminated character set".to_owned());
        };
        if c == ']' && !first {
            *i += 1;
            break;
        }
        first = false;
        let lo = if c == '\\' {
            *i += 1;
            let Some(&e) = chars.get(*i) else {
                return Err("bad escape (end of pattern)".to_owned());
            };
            match e {
                'd' => {
                    ranges.push(('0', '9'));
                    *i += 1;
                    continue;
                }
                '-' | ']' | '\\' | '[' | '^' | '.' | '/' => e,
                _ => return Err(format!("bad escape \\{e}")),
            }
        } else {
            c
        };
        *i += 1;
        if chars.get(*i) == Some(&'-') && chars.get(*i + 1).is_some_and(|&n| n != ']') {
            *i += 1;
            let hi = chars[*i];
            *i += 1;
            if hi < lo {
                return Err(format!("bad character range {lo}-{hi}"));
            }
            ranges.push((lo, hi));
        } else {
            ranges.push((lo, lo));
        }
    }
    Ok(Node::Class(ranges, negated))
}

fn parse_seq(chars: &[char], i: &mut usize, depth: usize) -> Result<Vec<Vec<Node>>, String> {
    let mut alts: Vec<Vec<Node>> = vec![Vec::new()];
    while *i < chars.len() {
        let c = chars[*i];
        let node = match c {
            ')' => {
                if depth == 0 {
                    return Err("unbalanced parenthesis".to_owned());
                }
                return Ok(alts);
            }
            '|' => {
                *i += 1;
                alts.push(Vec::new());
                continue;
            }
            '^' => {
                *i += 1;
                Node::Start
            }
            '(' => {
                *i += 1;
                let inner = parse_seq(chars, i, depth + 1)?;
                if chars.get(*i) != Some(&')') {
                    return Err("missing ), unterminated subpattern".to_owned());
                }
                *i += 1;
                Node::Group(inner)
            }
            '[' => parse_class(chars, i)?,
            '\\' => {
                *i += 1;
                let Some(&e) = chars.get(*i) else {
                    return Err("bad escape (end of pattern)".to_owned());
                };
                *i += 1;
                match e {
                    'Z' => Node::End,
                    'd' => Node::Class(vec![('0', '9')], false),
                    '.' | '/' | '-' | '(' | ')' | '[' | ']' | '{' | '}' | '*' | '+' | '?' | '|'
                    | '^' | '$' | '\\' => Node::Lit(e),
                    _ => {
                        return Err(format!(
                            "unsupported escape \\{e} (the corpus declares none)"
                        ))
                    }
                }
            }
            '*' | '+' | '?' | '{' => return Err("nothing to repeat".to_owned()),
            '$' => {
                *i += 1;
                Node::Dollar
            }
            '.' => return Err("unsupported metacharacter . (the corpus declares none)".to_owned()),
            _ => {
                *i += 1;
                Node::Lit(c)
            }
        };
        // a quantifier may follow
        let node = match chars.get(*i) {
            Some('*') => {
                *i += 1;
                Node::Repeat(Box::new(node), 0, None)
            }
            Some('+') => {
                *i += 1;
                Node::Repeat(Box::new(node), 1, None)
            }
            Some('?') => {
                *i += 1;
                Node::Repeat(Box::new(node), 0, Some(1))
            }
            Some('{') => {
                let start = *i + 1;
                let mut j = start;
                while chars.get(j).is_some_and(|c| *c != '}') {
                    j += 1;
                }
                if chars.get(j) != Some(&'}') {
                    return Err("unterminated quantifier".to_owned());
                }
                let body: String = chars[start..j].iter().collect();
                let (lo, hi) = match body.split_once(',') {
                    None => {
                        let n: usize = body
                            .parse()
                            .map_err(|_| format!("bad quantifier {{{body}}}"))?;
                        (n, Some(n))
                    }
                    Some((a, b)) => {
                        let lo: usize = a
                            .parse()
                            .map_err(|_| format!("bad quantifier {{{body}}}"))?;
                        let hi = if b.is_empty() {
                            None
                        } else {
                            Some(
                                b.parse()
                                    .map_err(|_| format!("bad quantifier {{{body}}}"))?,
                            )
                        };
                        (lo, hi)
                    }
                };
                *i = j + 1;
                Node::Repeat(Box::new(node), lo, hi)
            }
            _ => node,
        };
        if matches!(chars.get(*i), Some('*' | '+' | '?' | '{')) {
            return Err("multiple repeat".to_owned());
        }
        alts.last_mut().expect("one alternative").push(node);
    }
    if depth > 0 {
        return Err("missing ), unterminated subpattern".to_owned());
    }
    Ok(alts)
}

pub fn regex_compile(pattern: &str) -> Result<Regex, String> {
    let chars: Vec<char> = pattern.chars().collect();
    let mut i = 0;
    let alts = parse_seq(&chars, &mut i, 0)?;
    Ok(Regex {
        nodes: if alts.len() == 1 {
            alts.into_iter().next().unwrap_or_default()
        } else {
            vec![Node::Group(alts)]
        },
    })
}

impl Regex {
    /// `re.search`: a match anywhere.
    pub fn search(&self, text: &str) -> bool {
        let chars: Vec<char> = text.chars().collect();
        (0..=chars.len()).any(|start| match_seq(&self.nodes, &chars, start, &mut |_| true))
    }
}

fn match_seq(nodes: &[Node], text: &[char], pos: usize, k: &mut dyn FnMut(usize) -> bool) -> bool {
    let Some((first, rest)) = nodes.split_first() else {
        return k(pos);
    };
    match first {
        Node::Start => pos == 0 && match_seq(rest, text, pos, k),
        Node::End => pos == text.len() && match_seq(rest, text, pos, k),
        Node::Dollar => {
            (pos == text.len() || (pos + 1 == text.len() && text[pos] == '\n'))
                && match_seq(rest, text, pos, k)
        }
        Node::Lit(c) => text.get(pos) == Some(c) && match_seq(rest, text, pos + 1, k),
        Node::Class(ranges, negated) => {
            text.get(pos).is_some_and(|c| {
                let inside = ranges.iter().any(|(lo, hi)| lo <= c && c <= hi);
                inside != *negated
            }) && match_seq(rest, text, pos + 1, k)
        }
        Node::Group(alts) => alts
            .iter()
            .any(|alt| match_seq(alt, text, pos, &mut |p| match_seq(rest, text, p, k))),
        Node::Repeat(inner, lo, hi) => match_repeat(inner, *lo, *hi, 0, rest, text, pos, k),
    }
}

#[allow(clippy::too_many_arguments)]
fn match_repeat(
    inner: &Node,
    lo: usize,
    hi: Option<usize>,
    done: usize,
    rest: &[Node],
    text: &[char],
    pos: usize,
    k: &mut dyn FnMut(usize) -> bool,
) -> bool {
    // greedy: try one more repetition first, then settle
    if hi.is_none_or(|h| done < h) {
        let one = std::slice::from_ref(inner);
        let mut again =
            |p: usize| p != pos && match_repeat(inner, lo, hi, done + 1, rest, text, p, k);
        if match_seq(one, text, pos, &mut again) {
            return true;
        }
    }
    done >= lo && match_seq(rest, text, pos, k)
}

// ── validation ───────────────────────────────────────────────────────────────────────────────

fn sorted_repr(values: &[String]) -> String {
    let mut v: Vec<&String> = values.iter().collect();
    v.sort();
    py_repr(&Sexp::List(
        v.into_iter().map(|s| Sexp::Str(s.clone())).collect(),
    ))
}

fn check_atom(fld: &Field, value: &Sexp, where_: &str) -> Result<(), SchemaError> {
    match fld.type_.as_deref() {
        Some("integer") => {
            if !matches!(value, Sexp::Int(_)) {
                return Err(err(format!(
                    "{where_}: field \"{}\" has wrong value type — want integer, got {}",
                    fld.name,
                    py_repr(value)
                )));
            }
            Ok(())
        }
        Some("string") => {
            let Sexp::Str(s) = value else {
                return Err(err(format!(
                    "{where_}: field \"{}\" has wrong value type — want string, got {}",
                    fld.name,
                    py_repr(value)
                )));
            };
            if let Some(n) = fld.min_length {
                if (s.chars().count() as i128) < n {
                    return Err(err(format!(
                        "{where_}: field \"{}\" is shorter than min-length {n}, got {}",
                        fld.name,
                        py_repr(value)
                    )));
                }
            }
            if let Some(pat) = &fld.pattern {
                let re = regex_compile(pat).map_err(|e| {
                    err(format!("{where_}: pattern {pat:?} unreadable at use: {e}"))
                })?;
                if !re.search(s) {
                    return Err(err(format!(
                        "{where_}: field \"{}\" value {} does not match /{pat}/",
                        fld.name,
                        py_repr(value)
                    )));
                }
            }
            Ok(())
        }
        _ => {
            let Sexp::Symbol(s) = value else {
                return Err(err(format!(
                    "{where_}: field \"{}\" has wrong value type — want symbol, got {}",
                    fld.name,
                    py_repr(value)
                )));
            };
            if let Some(values) = &fld.values {
                if !values.contains(s) {
                    return Err(err(format!(
                        "{where_}: field \"{}\": \"{s}\" is not one of {}",
                        fld.name,
                        sorted_repr(values)
                    )));
                }
            }
            Ok(())
        }
    }
}

fn check_op_arg(
    spec: &ArgSpec,
    value: &Sexp,
    schema: &Schema,
    where_: &str,
) -> Result<(), SchemaError> {
    match spec {
        ArgSpec::Tuple(kinds) => {
            let Some(items) = as_list(value) else {
                return Err(err(format!(
                    "{where_}: wants a list of {} value(s), got {}",
                    kinds.len(),
                    py_repr(value)
                )));
            };
            if items.len() != kinds.len() {
                return Err(err(format!(
                    "{where_}: wants a list of {} value(s), got {} in {}",
                    kinds.len(),
                    items.len(),
                    py_repr(value)
                )));
            }
            for (el, kind) in items.iter().zip(kinds) {
                check_op_arg(&ArgSpec::Kind(kind.clone()), el, schema, where_)?;
            }
            Ok(())
        }
        ArgSpec::Kind(k) if k == "integer" => {
            if !matches!(value, Sexp::Int(_)) {
                return Err(err(format!(
                    "{where_}: wants an integer, got {}",
                    py_repr(value)
                )));
            }
            Ok(())
        }
        ArgSpec::Kind(k) if k == "symbol" => {
            if !matches!(value, Sexp::Symbol(_)) {
                return Err(err(format!(
                    "{where_}: wants a bare symbol, got {}",
                    py_repr(value)
                )));
            }
            Ok(())
        }
        ArgSpec::Kind(k) if k == "string" => {
            if !matches!(value, Sexp::Str(_)) {
                return Err(err(format!(
                    "{where_}: wants a string, got {}",
                    py_repr(value)
                )));
            }
            Ok(())
        }
        ArgSpec::Kind(_) => {
            // expr: an atom or an operator form
            if let Some(items) = as_list(value) {
                if items.is_empty() {
                    return Err(err(format!("{where_}: an empty form is not an expression")));
                }
                return validate_operator(value, schema, where_);
            }
            if matches!(value, Sexp::Str(_)) {
                return Err(err(format!(
                    "{where_}: a string is not an expression — unquote it or use a symbol, got {}",
                    py_repr(value)
                )));
            }
            Ok(())
        }
    }
}

fn validate_operator(form: &Sexp, schema: &Schema, where_: &str) -> Result<(), SchemaError> {
    let items = as_list(form).map(Vec::as_slice).unwrap_or(&[]);
    let head = items.first().and_then(symbol);
    let Some(op) = head.and_then(|h| schema.operator(h)) else {
        return Err(err(format!(
            "{where_}: undeclared operator \"{}\"",
            head.unwrap_or("None")
        )));
    };
    let args = &items[1..];
    if let Some(fixed) = op.fixed {
        if args.len() as i128 != fixed {
            return Err(err(format!(
                "{where_}: ({} …) takes {fixed} argument(s), got {}",
                op.name,
                args.len()
            )));
        }
    } else if (args.len() as i128) < op.min {
        return Err(err(format!(
            "{where_}: ({} …) takes at least {} argument(s), got {}",
            op.name,
            op.min,
            args.len()
        )));
    }
    for a in args {
        check_op_arg(&op.spec, a, schema, where_)?;
    }
    Ok(())
}

/// One form, validated in place; a refusal names the construct, the field and the reason.
pub fn validate_form(form: &Sexp, schema: &Schema, where_: &str) -> Result<(), SchemaError> {
    let items = as_list(form).map(Vec::as_slice).unwrap_or(&[]);
    let Some(head) = items.first().and_then(symbol) else {
        return Err(err(format!(
            "{where_}: expected a form headed by a symbol, got {}",
            py_repr(form)
        )));
    };
    if schema.operator(head).is_some() {
        return validate_operator(form, schema, where_);
    }
    let Some(c) = schema.construct(head) else {
        return Err(err(format!("{where_}: undeclared construct \"{head}\"")));
    };
    let mut counts: Vec<(String, usize)> = Vec::new();
    let mut seen: Vec<(String, Vec<&Sexp>)> = Vec::new();
    fn bump(counts: &mut Vec<(String, usize)>, name: &str) -> usize {
        if let Some(e) = counts.iter_mut().find(|(n, _)| n == name) {
            e.1 += 1;
            return e.1;
        }
        counts.push((name.to_owned(), 1));
        1
    }
    fn note<'a>(seen: &mut Vec<(String, Vec<&'a Sexp>)>, name: &str, v: &'a Sexp) {
        if let Some(e) = seen.iter_mut().find(|(n, _)| n == name) {
            e.1.push(v);
        } else {
            seen.push((name.to_owned(), vec![v]));
        }
    }
    for child in &items[1..] {
        let Some(ch) = as_list(child).filter(|l| !l.is_empty()) else {
            return Err(err(format!(
                "{where_}: construct \"{head}\": expected a (field value) child list, got {}",
                py_repr(child)
            )));
        };
        if is_comment(child) {
            check_comment(child, where_)?;
            continue;
        }
        let Some(fname) = symbol(&ch[0]) else {
            return Err(err(format!(
                "{where_}: construct \"{head}\": a field name must be a bare symbol, got {}",
                py_repr(&ch[0])
            )));
        };
        let Some(fld) = c.field(fname) else {
            return Err(err(format!(
                "{where_}: construct \"{head}\": undeclared field \"{fname}\""
            )));
        };
        let n = bump(&mut counts, fname);
        if !fld.repeat && n > 1 {
            return Err(err(format!(
                "{where_}: construct \"{head}\": duplicated single-valued field \"{fname}\""
            )));
        }
        if fld.type_.as_deref() == Some("form") {
            if fld.heads.iter().any(|h| h == fname) {
                validate_form(child, schema, where_)?;
                note(&mut seen, fname, child);
            } else {
                let nested = (ch.len() == 2)
                    .then(|| &ch[1])
                    .filter(|v| as_list(v).is_some());
                let Some(nested) = nested else {
                    return Err(err(format!(
                        "{where_}: construct \"{head}\" field \"{fname}\": wrong arity — expects one nested form headed one of {}, got {}",
                        sorted_repr(&fld.heads),
                        py_repr(child)
                    )));
                };
                let inner = as_list(nested).and_then(|l| l.first()).and_then(Sexp::text);
                if !inner.is_some_and(|i| fld.heads.iter().any(|h| h == i)) {
                    return Err(err(format!(
                        "{where_}: construct \"{head}\" field \"{fname}\": form head \"{}\" is not one of {}",
                        inner.unwrap_or("None"),
                        sorted_repr(&fld.heads)
                    )));
                }
                validate_form(nested, schema, where_)?;
                note(&mut seen, fname, nested);
            }
        } else {
            if ch.len() == 1 {
                if fld.type_.is_none() || fld.empty {
                    continue;
                }
                return Err(err(format!(
                    "{where_}: construct \"{head}\" field \"{fname}\": wrong arity — (name) with no value, and the field is not declared (empty yes)"
                )));
            }
            if fld.type_.is_none() {
                return Err(err(format!(
                    "{where_}: construct \"{head}\" field \"{fname}\": wrong arity — a marker field is written (name) with no value, got {}",
                    py_repr(child)
                )));
            }
            if ch.len() != 2 {
                return Err(err(format!(
                    "{where_}: construct \"{head}\" field \"{fname}\": wrong arity — an atom field is (name value), got {} element(s) in {}",
                    ch.len(),
                    py_repr(child)
                )));
            }
            check_atom(fld, &ch[1], &format!("{where_}: construct \"{head}\""))?;
            note(&mut seen, fname, &ch[1]);
        }
    }
    for fld in &c.fields {
        let n = counts
            .iter()
            .find(|(name, _)| *name == fld.name)
            .map_or(0, |e| e.1);
        if !fld.repeat && !fld.optional && n == 0 {
            return Err(err(format!(
                "{where_}: construct \"{head}\": missing required field \"{}\"",
                fld.name
            )));
        }
        if fld.repeat {
            if let Some(min) = fld.min {
                if (n as i128) < min {
                    return Err(err(format!(
                        "{where_}: construct \"{head}\": field \"{}\" appears {n} time(s), min is {min} — an empty list is not a citation",
                        fld.name
                    )));
                }
            }
            if fld.unique {
                let vals: &[&Sexp] = seen
                    .iter()
                    .find(|(name, _)| *name == fld.name)
                    .map_or(&[], |e| e.1.as_slice());
                for i in 0..vals.len() {
                    for j in i + 1..vals.len() {
                        if vals[i] == vals[j] {
                            return Err(err(format!(
                                "{where_}: construct \"{head}\": field \"{}\" repeats {} — unique means written once",
                                fld.name,
                                py_repr(vals[i])
                            )));
                        }
                    }
                }
            }
        }
    }
    Ok(())
}

/// Every refusal of one source stream, by name; an empty list is the pass verdict.
pub fn validate_text(
    text: &str,
    schema: &Schema,
    where_: &str,
    parse_where: Option<&str>,
) -> Vec<String> {
    let forms = match sexp::parse(text, parse_where.unwrap_or(where_)) {
        Ok(f) => f,
        Err(SexpError(e)) => return vec![format!("{where_}: does not even parse: {e}")],
    };
    let mut errors = Vec::new();
    for form in &forms {
        if as_list(form).is_none_or(Vec::is_empty) {
            errors.push(format!(
                "{where_}: top level holds a non-form {}",
                py_repr(form)
            ));
            continue;
        }
        if is_comment(form) {
            if let Err(e) = check_comment(form, where_) {
                errors.push(e.0);
            }
            continue;
        }
        if let Err(e) = validate_form(form, schema, where_) {
            errors.push(e.0);
        }
    }
    errors
}

pub fn validate_file(path: &Path, schema: &Schema) -> Vec<String> {
    let name = path
        .file_name()
        .map(|n| n.to_string_lossy().into_owned())
        .unwrap_or_default();
    match std::fs::read(path) {
        Ok(bytes) => match String::from_utf8(bytes) {
            Ok(text) => validate_text(&text, schema, &name, Some(&path.display().to_string())),
            Err(e) => vec![format!(
                "{name}: does not even parse: 'utf-8' codec can't decode bytes: {}",
                e.utf8_error()
            )],
        },
        Err(e) => vec![format!("{name}: does not even parse: {e}")],
    }
}

/// `check_sexp_schema.py <file> <schema>`: the verdict lines and exit statuses of the pinned tool.
pub fn check(file: &Path, schema_path: &Path) -> i32 {
    for (p, what) in [(schema_path, "the schema"), (file, "the document")] {
        if !p.is_file() {
            eprintln!(
                "  REFUSED — {what} does not exist: {}; a check that cannot read its input refuses rather than reports",
                p.display()
            );
            return 2;
        }
    }
    let schema = match load_schema(schema_path) {
        Ok(s) => s,
        Err(e) => {
            eprintln!("  REFUSED the schema itself: {e}");
            return 1;
        }
    };
    let errors = validate_file(file, &schema);
    for e in &errors {
        eprintln!("  REFUSED {e}");
    }
    if !errors.is_empty() {
        eprintln!(
            "check_sexp_schema: {} refusal(s) against {}",
            errors.len(),
            schema_path.display()
        );
        return 1;
    }
    println!(
        "check_sexp_schema: ok — {} conforms to {}",
        file.display(),
        schema_path
            .file_name()
            .map(|n| n.to_string_lossy().into_owned())
            .unwrap_or_default()
    );
    0
}

// ── the pinned validator's self-test, re-asserted ────────────────────────────────────────────

struct Arms {
    root: std::path::PathBuf,
    passed: u32,
    failed: u32,
}

impl Arms {
    fn scratch(&self) -> Option<std::path::PathBuf> {
        crate::harness::scratch(&self.root, "target", "schema-selftest").ok()
    }

    fn report(&mut self, label: &str, outcome: Result<(), String>) {
        match outcome {
            Ok(()) => {
                println!("  ok    {label}");
                self.passed += 1;
            }
            Err(e) => {
                println!("  FAIL  {label}: {e}");
                self.failed += 1;
            }
        }
    }

    fn load_from(&self, td: &Path, schema_text: &str) -> Result<Schema, LoadError> {
        let s = td.join("s.sexp");
        std::fs::write(&s, schema_text).ok();
        load_schema(&s)
    }

    /// `refuses(file_text, schema_text, needle)`.
    fn refuses(&mut self, label: &str, file_text: &str, schema_text: &str, needle: &str) {
        let Some(td) = self.scratch() else {
            return self.report(label, Err("no scratch".to_owned()));
        };
        let f = td.join("t.sexp");
        std::fs::write(&f, file_text).ok();
        let errs: Vec<String> = match self.load_from(&td, schema_text) {
            Err(e) => vec![format!("schema: {e}")],
            Ok(schema) => validate_file(&f, &schema),
        };
        let _ = std::fs::remove_dir_all(&td);
        let outcome = if errs.is_empty() {
            Err(format!("no refusal for {file_text:?}"))
        } else if !errs.iter().any(|e| e.contains(needle)) {
            Err(format!(
                "refusal named the wrong reason — wanted {needle:?}, got {errs:?}"
            ))
        } else {
            Ok(())
        };
        self.report(label, outcome);
    }

    /// `refuses_schema(schema_text, needle)`.
    fn refuses_schema(&mut self, label: &str, schema_text: &str, needle: &str) {
        let Some(td) = self.scratch() else {
            return self.report(label, Err("no scratch".to_owned()));
        };
        let outcome = match self.load_from(&td, schema_text) {
            Err(e) if e.to_string().contains(needle) => Ok(()),
            Err(e) => Err(format!(
                "refusal named the wrong reason — wanted {needle:?}, got {e}"
            )),
            Ok(_) => Err(format!("schema {schema_text:?} must be refused")),
        };
        let _ = std::fs::remove_dir_all(&td);
        self.report(label, outcome);
    }

    /// `accepts(file_text, schema_text)`.
    fn accepts(&mut self, label: &str, file_text: &str, schema_text: &str) {
        let Some(td) = self.scratch() else {
            return self.report(label, Err("no scratch".to_owned()));
        };
        let f = td.join("t.sexp");
        std::fs::write(&f, file_text).ok();
        let outcome = match self.load_from(&td, schema_text) {
            Err(e) => Err(format!("unexpected {e}")),
            Ok(schema) => {
                let errs = validate_file(&f, &schema);
                if errs.is_empty() {
                    Ok(())
                } else {
                    Err(format!("unexpected refusals: {errs:?}"))
                }
            }
        };
        let _ = std::fs::remove_dir_all(&td);
        self.report(label, outcome);
    }
}

const TOY: &str = r#"(schema (id "toy"))

(construct (name unit)
  (field (name id) (type string))
  (field (name width) (type integer))
  (field (name mode) (type symbol) (values on) (values off) (optional yes))
  (field (name note) (type string) (repeat yes) (optional yes))
  (field (name meta) (empty yes) (optional yes))
  (field (name data) (type form) (head data) (repeat yes) (optional yes))
  (field (name effect) (type form) (head bump) (optional yes)))

(construct (name data)
  (field (name item) (type string) (repeat yes)))

(construct (name bump)
  (field (name by) (type integer)))"#;

const TOYO: &str = r#"(schema (id "toyo"))

(construct (name unit)
  (field (name id) (type string))
  (field (name width) (type integer))
  (field (name body) (type form)
         (head bump) (head pair) (head many) (head any) (head triple) (repeat yes) (optional yes)))

(operator (name bump) (fixed 1) (arg symbol))
(operator (name pair) (fixed 2))
(operator (name many) (variadic) (arg integer))
(operator (name any) (variadic) (min 0))
(operator (name triple) (variadic) (arg (integer integer integer)))"#;

const TOYF_TAIL: &str = r#"

(construct (name insn)
  (field (name name) (type symbol))
  (field (name fixed) (type form) (head fixed))
  (field (name operands) (type form) (head operands)))

(operator (name fixed) (variadic) (arg (integer integer integer)))
(operator (name operands) (variadic) (min 0) (arg symbol))"#;

const GOOD: &str = r#"(unit (id "u") (width 32) (body (pair (bump rd) (pair a b))) (body (triple (1 2 3) (4 5 6))) (body (many 1 2 3)) (body (any)) (body (any x 7)))"#;

const TOYFAC: &str = r#"(schema (id "toyfac"))

(construct (name rec)
  (field (name id) (type string) (pattern "^[A-Z][A-Z0-9-]*$"))
  (field (name title) (type string) (min-length 1))
  (field (name tag) (type symbol) (repeat yes) (min 1) (unique yes)
         (values red) (values blue))
  (field (name alias) (type string) (repeat yes) (unique yes) (optional yes)))"#;

/// The 51 arms of `check_sexp_schema.py --self-test`, same labels, fixtures and needles.
pub fn self_test(root: &Path) -> i32 {
    let mut a = Arms {
        root: root.to_path_buf(),
        passed: 0,
        failed: 0,
    };
    let toyf = format!("{TOYO}{TOYF_TAIL}");
    a.accepts("GREEN a conforming file validates — markers, repeats, both form shapes, recursion",
        r#"(unit (id "u") (width 32) (mode on) (meta) (note "a") (note "b") (data (item "x") (item "y")) (data (item "z")) (effect (bump (by 1))))"#, TOY);
    a.refuses(
        "RED   an undeclared construct is refused by name",
        r#"(sourcs (id "u") (width 32))"#,
        TOY,
        r#"undeclared construct "sourcs""#,
    );
    a.refuses(
        "RED   an undeclared field is refused by name",
        r#"(unit (id "u") (width 32) (widht 8))"#,
        TOY,
        r#"undeclared field "widht""#,
    );
    a.refuses(
        "RED   a missing required field is refused by name",
        r#"(unit (id "u"))"#,
        TOY,
        r#"missing required field "width""#,
    );
    a.refuses(
        "RED   wrong arity — an atom field with two values",
        r#"(unit (id "u" "v") (width 32))"#,
        TOY,
        "wrong arity",
    );
    a.refuses(
        "RED   wrong arity — an atom where a child list belongs",
        r#"(unit (id "u") stray (width 32))"#,
        TOY,
        "expected a (field value) child",
    );
    a.refuses(
        "RED   wrong arity — a marker where the field is not declared (empty yes)",
        r#"(unit (id "u") (width 32) (mode))"#,
        TOY,
        "not declared (empty yes)",
    );
    a.refuses(
        "RED   wrong value type — a string where a symbol belongs",
        r#"(unit (id "u") (width 32) (mode "on"))"#,
        TOY,
        "want symbol",
    );
    a.refuses(
        "RED   wrong value type — a bare atom is not an integer",
        r#"(unit (id "u") (width 1.5))"#,
        TOY,
        "want integer",
    );
    a.refuses(
        "RED   a duplicated single-valued field is refused by name",
        r#"(unit (id "u") (id "v") (width 32))"#,
        TOY,
        r#"duplicated single-valued field "id""#,
    );
    a.refuses(
        "RED   a values restriction is enforced",
        r#"(unit (id "u") (width 32) (mode maybe))"#,
        TOY,
        "is not one of",
    );
    a.refuses(
        "RED   a form value with the wrong head is refused",
        r#"(unit (id "u") (width 32) (effect (widget (by 1))))"#,
        TOY,
        r#"form head "widget""#,
    );
    a.refuses(
        "RED   a nested form is validated recursively, not just its head",
        r#"(unit (id "u") (width 32) (effect (bump (by "lots"))))"#,
        TOY,
        "want integer",
    );
    a.refuses(
        "RED   the schema itself abusing the meta-level is refused (construct, no name)",
        r#"(unit (id "u") (width 32))"#,
        "(construct (field (name x) (type string)))",
        "needs exactly one",
    );
    a.refuses("RED   a schema allowing an undeclared form head is refused", r#"(unit (id "u") (width 32))"#,
        "(schema (id \"s\"))\n(construct (name unit) (field (name id) (type string))\n (field (name child) (type form) (head widget) (optional yes)))", "allows undeclared head");
    a.accepts(
        "GREEN operator forms validate — fixed arity, nesting, variadic min, arg kinds",
        GOOD,
        TOYO,
    );
    a.accepts("GREEN the fragment shapes are operators — fixed triples and bare-symbol operands",
        &format!("{GOOD} (insn (name add) (fixed (31 25 0x0) (14 12 0xc)) (operands rd rs1 rs2)) (insn (name ecall) (fixed (31 20 0x0)) (operands))"), &toyf);
    a.refuses(
        "RED   an undeclared operator head is refused by name",
        r#"(unit (id "u") (width 32) (body (pair a (widget x))))"#,
        TOYO,
        r#"undeclared operator "widget""#,
    );
    a.refuses(
        "RED   a fixed-arity operator with the wrong count is refused",
        r#"(unit (id "u") (width 32) (body (pair a)))"#,
        TOYO,
        "takes 2 argument(s), got 1",
    );
    a.refuses(
        "RED   a variadic operator below its minimum is refused",
        r#"(unit (id "u") (width 32) (body (many)))"#,
        TOYO,
        "takes at least 1 argument(s), got 0",
    );
    a.refuses(
        "RED   an integer argument slot refuses a symbol",
        r#"(unit (id "u") (width 32) (body (many 1 rs)))"#,
        TOYO,
        "wants an integer",
    );
    a.refuses(
        "RED   a symbol argument slot refuses an integer",
        r#"(unit (id "u") (width 32) (body (bump 7)))"#,
        TOYO,
        "wants a bare symbol",
    );
    a.refuses(
        "RED   a tuple argument spec refuses a wrong length",
        r#"(unit (id "u") (width 32) (body (triple (1 2))))"#,
        TOYO,
        "wants a list of 3 value(s), got 2",
    );
    a.refuses(
        "RED   a tuple argument spec refuses a wrong element kind",
        r#"(unit (id "u") (width 32) (body (triple (1 rs 3))))"#,
        TOYO,
        "wants an integer",
    );
    a.refuses(
        "RED   an expression argument refuses a quoted string",
        r#"(unit (id "u") (width 32) (body (pair "a" b)))"#,
        TOYO,
        "is not an expression",
    );
    a.refuses_schema(
        "RED   the operator meta-level refuses fixed and variadic together",
        &format!("{TOYO}\n(operator (name bad) (fixed 1) (variadic))"),
        "exactly one of",
    );
    a.refuses_schema(
        "RED   the operator meta-level refuses (min …) without (variadic)",
        &format!("{TOYO}\n(operator (name bad) (fixed 1) (min 0))"),
        "(min …)",
    );
    a.refuses_schema(
        "RED   the operator meta-level refuses an unknown argument kind",
        &format!("{TOYO}\n(operator (name bad) (fixed 1) (arg number))"),
        "unknown argument kind",
    );
    a.refuses_schema(
        "RED   the operator meta-level refuses a duplicated declaration",
        &format!("{TOYO}\n(operator (name bump) (fixed 2))"),
        "declared twice",
    );
    a.refuses_schema("RED   a name declared as both construct and operator is refused",
        "(schema (id \"s\"))\n(construct (name dual) (field (name x) (type string)))\n(operator (name dual) (fixed 1))", "both as a construct");
    a.accepts(
        "GREEN facets hold — pattern, min-length, min and unique all satisfied",
        r#"(rec (id "REQ-X") (title "t") (tag red) (tag blue) (alias "a") (alias "b"))"#,
        TOYFAC,
    );
    a.refuses(
        "RED   a pattern mismatch is refused by name",
        r#"(rec (id "req-x") (title "t") (tag red))"#,
        TOYFAC,
        "does not match",
    );
    a.refuses(
        "RED   a min-length violation is refused by name",
        r#"(rec (id "REQ-X") (title "") (tag red))"#,
        TOYFAC,
        "shorter than min-length",
    );
    a.refuses(
        "RED   a repeat below its min is refused — an empty list is not a citation",
        r#"(rec (id "REQ-X") (title "t"))"#,
        TOYFAC,
        "min is 1",
    );
    a.refuses(
        "RED   a unique repeat refusing a duplicated value",
        r#"(rec (id "REQ-X") (title "t") (tag red) (tag red))"#,
        TOYFAC,
        "unique",
    );
    a.refuses(
        "RED   a unique string repeat refusing a duplicated value",
        r#"(rec (id "REQ-X") (title "t") (tag red) (alias "a") (alias "a"))"#,
        TOYFAC,
        "unique",
    );
    a.refuses_schema(
        "RED   the meta-level refuses a pattern on a non-string field",
        &format!(
            "{TOYFAC}\n(construct (name bad) (field (name n) (type integer) (pattern \"^x$\")))"
        ),
        "(pattern …) constrains a string",
    );
    a.refuses_schema(
        "RED   the meta-level refuses min-length on a non-string field",
        &format!("{TOYFAC}\n(construct (name bad) (field (name n) (type integer) (min-length 1)))"),
        "(min-length …) constrains a string",
    );
    a.refuses_schema(
        "RED   the meta-level refuses min on a non-repeating field",
        &format!("{TOYFAC}\n(construct (name bad) (field (name n) (type string) (min 1)))"),
        "(min N) belongs to a (repeat yes)",
    );
    a.refuses_schema(
        "RED   the meta-level refuses unique on a non-repeating field",
        &format!("{TOYFAC}\n(construct (name bad) (field (name n) (type string) (unique yes)))"),
        "(unique yes) belongs to a (repeat yes)",
    );
    a.refuses_schema(
        "RED   the meta-level refuses an invalid regex",
        &format!(
            "{TOYFAC}\n(construct (name bad) (field (name n) (type string) (pattern \"^[(\")))"
        ),
        "not a valid regex",
    );
    a.refuses_schema(
        "RED   the meta-level refuses a non-integer min-length",
        &format!(
            "{TOYFAC}\n(construct (name bad) (field (name n) (type string) (min-length one)))"
        ),
        "(min-length N) takes one non-negative integer",
    );
    a.accepts(
        "GREEN a comment form is allowed anywhere — top level and inside a construct",
        r#"(comment "why this file exists") (unit (id "u") (width 32) (comment "why 32"))"#,
        TOY,
    );
    a.refuses(
        "RED   an empty comment is refused — silence is not annotation",
        "(comment)",
        TOY,
        "at least one string",
    );
    a.refuses(
        "RED   a comment line that is not a string is refused",
        "(comment 42)",
        TOY,
        "plain string",
    );
    a.refuses(
        "RED   a comment holding a nested form is refused",
        r#"(unit (id "u") (width 32) (comment (why)))"#,
        TOY,
        "plain string",
    );
    a.refuses(
        "RED   the typo commment is still refused by name",
        r#"(unit (id "u") (width 32) (commment "why"))"#,
        TOY,
        r#"undeclared field "commment""#,
    );
    a.refuses_schema(
        "RED   a construct named comment is refused — the head is reserved",
        &format!("{TOY}\n(construct (name comment) (field (name x) (type string)))"),
        "reserved",
    );
    a.refuses_schema(
        "RED   a field named comment is refused — the head is reserved",
        &format!("{TOY}\n(construct (name unit2) (field (name comment) (type string)))"),
        "reserved",
    );
    let fixpoint = std::fs::read_to_string(root.join("schema/schema.sexp")).unwrap_or_default();
    a.accepts(
        "GREEN the fixpoint: schema.sexp validates under itself",
        &fixpoint,
        &fixpoint,
    );
    let missing = (|| -> Result<(), String> {
        let td = a.scratch().ok_or("no scratch")?;
        let doc = td.join("d.sexp");
        std::fs::write(&doc, "(state)").map_err(|e| e.to_string())?;
        let r1 = check(&doc, &td.join("no-such-schema.sexp"));
        let r2 = check(&td.join("no-such-doc.sexp"), &doc);
        let _ = std::fs::remove_dir_all(&td);
        if r1 != 2 {
            return Err("missing schema".to_owned());
        }
        if r2 != 2 {
            return Err("missing document".to_owned());
        }
        Ok(())
    })();
    a.report(
        "RED   a missing schema or document refuses rc 2, no traceback",
        missing,
    );
    println!(
        "check_sexp_schema --self-test: {} pass / {} fail",
        a.passed, a.failed
    );
    i32::from(a.failed > 0)
}

/// `cargo xtask check-sexp-schema <file.sexp> <schema.sexp> | --self-test`, the pinned tool's surface.
pub fn run(root: &Path, args: &[String]) -> std::process::ExitCode {
    let rc = match args {
        [flag] if flag == "--self-test" => self_test(root),
        [file, schema] => check(Path::new(file), Path::new(schema)),
        _ => {
            eprintln!("usage: check_sexp_schema.py <file.sexp> <schema.sexp> | --self-test");
            2
        }
    };
    std::process::ExitCode::from(u8::try_from(rc).unwrap_or(1))
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write as _;
    use std::process::{Command, Stdio};

    /// The pairs the project validates today: a tracked `.sexp` and the schema its route names.
    fn corpus_pairs(root: &Path) -> Vec<(String, String)> {
        let listed = Command::new("git")
            .args(["ls-files", "-z", "*.sexp"])
            .current_dir(root)
            .output()
            .expect("git ls-files");
        assert!(listed.status.success(), "git ls-files failed");
        let mut pairs = Vec::new();
        for f in String::from_utf8_lossy(&listed.stdout)
            .split('\0')
            .filter(|s| !s.is_empty())
        {
            let parts: Vec<&str> = f.split('/').collect();
            let name = parts.last().copied().unwrap_or("");
            let schema = match parts.as_slice() {
                ["schema", _] => Some("schema/schema.sexp".to_owned()),
                ["definitions", ..] => Some("schema/fragment.sexp".to_owned()),
                ["profiles", _, "guests", n] if n.ends_with(".expected.sexp") => {
                    Some("schema/expectations.sexp".to_owned())
                }
                ["profiles", _, n]
                    if n.starts_with("contract-v") && n.ends_with(".obligations.sexp") =>
                {
                    Some("schema/contract-obligations.sexp".to_owned())
                }
                ["profiles", _, "encoding.sexp"] => Some("schema/encoding.sexp".to_owned()),
                ["profiles", _, _] if root.join("schema").join(name).is_file() => {
                    Some(format!("schema/{name}"))
                }
                _ => None,
            };
            if let Some(s) = schema {
                pairs.push((f.to_owned(), s));
            }
        }
        pairs
    }

    /// Every pair reads as the pinned `scripts/check_sexp_schema.py` reads it: the same refusals, in order, byte
    /// for byte — one dump from each validator over the whole corpus. An absent comparator fails, never skips.
    #[test]
    fn the_corpus_validates_as_the_pinned_validator_validates_it() {
        let root = std::env::var("XT0020_ROOT")
            .map(std::path::PathBuf::from)
            .unwrap_or_else(|_| {
                Path::new(env!("CARGO_MANIFEST_DIR"))
                    .parent()
                    .expect("the workspace root")
                    .to_path_buf()
            });
        let pairs = corpus_pairs(&root);
        assert!(
            pairs.len() >= 250,
            "the corpus census found only {} pairs",
            pairs.len()
        );
        let program = concat!(
            "import sys\nsys.path.insert(0, 'scripts'); sys.dont_write_bytecode = True\n",
            "import check_sexp_schema as K, sexp as S\nfrom pathlib import Path\n",
            "schemas = {}\n",
            "for line in sys.stdin.read().split('\\0'):\n    if not line: continue\n    f, s = line.split('\\t')\n    print('== ' + f + ' ' + s)\n",
            "    try:\n        if s not in schemas: schemas[s] = K.load_schema(Path(s))\n        errs = K.validate_file(Path(f), *schemas[s])\n",
            "    except (K.SchemaError, S.SexpError) as e:\n        errs = ['schema: ' + str(e)]\n",
            "    for e in errs: print(e)\n",
        );
        let mut child = Command::new("python3")
            .args(["-I", "-c", program])
            .current_dir(&root)
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .spawn()
            .expect("python3 is the comparator");
        let feed: String = pairs
            .iter()
            .map(|(f, s)| format!("{f}\t{s}"))
            .collect::<Vec<_>>()
            .join("\0");
        child
            .stdin
            .take()
            .expect("stdin")
            .write_all(feed.as_bytes())
            .expect("pair list");
        let output = child.wait_with_output().expect("python3 finished");
        assert!(
            output.status.success(),
            "the pinned validator failed: {}",
            String::from_utf8_lossy(&output.stderr)
        );
        let mut ours = String::new();
        let mut loaded: std::collections::BTreeMap<String, Result<Schema, String>> =
            std::collections::BTreeMap::new();
        for (f, s) in &pairs {
            ours.push_str(&format!("== {f} {s}\n"));
            let schema = loaded
                .entry(s.clone())
                .or_insert_with(|| load_schema(&root.join(s)).map_err(|e| e.to_string()));
            let errs = match schema {
                Err(e) => vec![format!("schema: {e}")],
                Ok(schema) => validate_file(&root.join(f), schema),
            };
            for e in errs {
                ours.push_str(&e);
                ours.push('\n');
            }
        }
        let theirs = String::from_utf8_lossy(&output.stdout);
        if theirs != ours {
            let first = theirs
                .lines()
                .zip(ours.lines())
                .position(|(a, b)| a != b)
                .unwrap_or(0);
            panic!(
                "the validators disagree ({} pairs); first differing line {}:\n pinned: {}\n   ours: {}",
                pairs.len(), first + 1, theirs.lines().nth(first).unwrap_or(""), ours.lines().nth(first).unwrap_or("")
            );
        }
    }

    #[test]
    fn the_pinned_validators_arms_hold() {
        let root = std::env::var("XT0020_ROOT")
            .map(std::path::PathBuf::from)
            .unwrap_or_else(|_| {
                Path::new(env!("CARGO_MANIFEST_DIR"))
                    .parent()
                    .expect("the workspace root")
                    .to_path_buf()
            });
        assert_eq!(
            self_test(&root),
            0,
            "an arm of the pinned validator's self-test fails in the port"
        );
    }

    #[test]
    fn the_regex_subset_covers_the_schemas_patterns_and_refuses_the_rest() {
        for pat in [
            "^[A-Za-z][A-Za-z0-9._:/-]*\\Z",
            "^[0-9a-f]{64}\\Z",
            "^0x[0-9a-f]{1,4}(_[0-9a-f]{4})*\\Z",
            "^x([1-9]|[12][0-9]|3[01])\\Z",
            "^(C|D)[0-9]{2}\\Z",
            "^[A-Z][A-Z0-9-]*$",
        ] {
            assert!(regex_compile(pat).is_ok(), "{pat}");
        }
        let hex = regex_compile("^0x[0-9a-f]{1,4}(_[0-9a-f]{4})*\\Z").expect("compiles");
        assert!(
            hex.search("0x8000_0000")
                && hex.search("0xa")
                && !hex.search("0x12345")
                && !hex.search("0x8000_00")
        );
        let reg = regex_compile("^x([1-9]|[12][0-9]|3[01])\\Z").expect("compiles");
        assert!(
            reg.search("x31")
                && reg.search("x1")
                && !reg.search("x32")
                && !reg.search("x0")
                && !reg.search("x310")
        );
        assert!(
            regex_compile("a.b").is_err(),
            "the unsupported . is refused by name"
        );
        assert!(
            regex_compile("^[(").is_err(),
            "an unterminated set is refused"
        );
    }
}
