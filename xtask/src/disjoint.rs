//! The encoding-disjointness judge (`XTASK.6` slice `6m`), ported from the pinned `scripts/check_encoding_disjoint.py`,
//! which stays the definition: a composition's instructions must be pairwise disjoint in their fixed bits unless a
//! `(specializes …)` declaration names a strict specialization; a pseudo-instruction adds nothing to the encoding space;
//! a slot is declared partial, never inferred from silence; every document is validated against its schema before it
//! is judged (through `schema.rs`) and resolved through the one composition resolver (`composition.rs`). Every message
//! is the pinned judge's text.

use std::collections::BTreeSet;
use std::path::Path;

use crate::composition::{resolve_composition, ResolveError};
use crate::schema::{load_schema, validate_file, LoadError};
use crate::sexp::{self, Sexp};

/// One instruction (or pseudo-instruction) row: its fixed-bit mask and value, and the file it came from.
#[derive(Debug, Clone)]
pub struct Insn {
    pub name: String,
    pub mask: u64,
    pub value: u64,
    pub origin: String,
}

impl Insn {
    fn new(name: &str, fixed: &[(i128, i128, i128)], origin: &str) -> Result<Insn, String> {
        let mut mask = 0u64;
        let mut value = 0u64;
        for &(hi, lo, val) in fixed {
            let width = hi - lo + 1;
            if width <= 0 || width > 64 || lo < 0 || val < 0 {
                return Err(format!(
                    "{name}: fixed value {val:#x} does not fit bits [{hi}:{lo}]"
                ));
            }
            if val >= (1i128 << width) {
                return Err(format!(
                    "{name}: fixed value {val:#x} does not fit bits [{hi}:{lo}]"
                ));
            }
            let w = width as u32;
            let field_mask: u64 = if w == 64 { u64::MAX } else { (1u64 << w) - 1 };
            mask |= field_mask << lo;
            value |= (val as u64) << lo;
        }
        Ok(Insn {
            name: name.to_owned(),
            mask,
            value,
            origin: origin.to_owned(),
        })
    }
}

/// The slots a composition declares: each slot's id and the fragments it requires.
pub type Slots = Vec<(String, Vec<String>)>;
/// A judge's verdict over the overlaps: undeclared collisions, accepted specializations, declaration problems.
pub type Overlaps = (Vec<(Insn, Insn)>, Vec<(String, String)>, Vec<String>);

/// A refusal: the composition document is not well-formed enough to judge.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CompositionError(pub String);

impl std::fmt::Display for CompositionError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(&self.0)
    }
}

fn py_str(v: &Sexp) -> String {
    match v {
        Sexp::Int(n) => n.to_string(),
        Sexp::Str(s) | Sexp::Symbol(s) => s.clone(),
        Sexp::List(_) => sexp::py_repr(v),
    }
}

fn py_int(v: &Sexp) -> Result<i128, String> {
    match v {
        Sexp::Int(n) => Ok(*n),
        other => py_str(other).trim().parse::<i128>().map_err(|_| {
            format!(
                "invalid literal for int() with base 10: {}",
                sexp::py_repr(other)
            )
        }),
    }
}

/// `_schema_validate`: refuse, by name, a document the schema layer refuses — before any consumer reads it.
fn schema_validate(root: &Path, path: &Path, family: &str) -> Result<(), CompositionError> {
    let schema_path = root.join("schema").join(format!("{family}.sexp"));
    let schema = match load_schema(&schema_path) {
        Ok(s) => s,
        Err(LoadError::Schema(e)) => {
            return Err(CompositionError(format!(
                "{}: the {family} schema itself cannot be read — {}",
                path.display(),
                e.0
            )));
        }
        Err(LoadError::Sexp(e)) => {
            return Err(CompositionError(format!(
                "{}: the {family} schema itself cannot be read — {}",
                path.display(),
                e.0
            )));
        }
    };
    let errors = validate_file(path, &schema);
    if !errors.is_empty() {
        return Err(CompositionError(format!(
            "{}: refused by schema/{family}.sexp — {}",
            path.display(),
            errors.join("; ")
        )));
    }
    Ok(())
}

/// The (status, slots) a compose form declares. Status defaults to a completeness claim.
pub fn composition_slots(enc: &Sexp) -> Result<(String, Slots), String> {
    let comp = sexp::children(enc, "compose").map_err(|e| e.0)?;
    let Some(comp0) = comp.first() else {
        return Ok(("complete".to_owned(), Vec::new()));
    };
    let status_found = sexp::children(comp0, "status").map_err(|e| e.0)?;
    let status = match status_found.first() {
        Some(Sexp::List(l)) if l.len() > 1 => py_str(&l[1]),
        Some(_) => return Err("list index out of range".to_owned()),
        None => "complete".to_owned(),
    };
    let mut slots = Vec::new();
    for s in sexp::children(comp0, "slot").map_err(|e| e.0)? {
        let mut requires: Vec<String> = Vec::new();
        for r in sexp::children(s, "requires").map_err(|e| e.0)? {
            if let Sexp::List(items) = r {
                requires.extend(items.iter().skip(1).map(py_str));
            }
        }
        slots.push((py_str(sexp::field(s, "id", "").map_err(|e| e.0)?), requires));
    }
    Ok((status, slots))
}

/// MODEL-COMPOSE.4: partial is declared, never inferred from silence — both directions.
pub fn check_slot_rules(path: &Path, enc: &Sexp) -> Result<Slots, CompositionError> {
    let (status, slots) = composition_slots(enc).map_err(CompositionError)?;
    if !slots.is_empty() && status != "partial" {
        return Err(CompositionError(format!(
            "{}: {} slot(s) unbound but no (status partial) — a composition claiming completeness while a hole is open. Declare partial, or bind the slot.",
            path.display(),
            slots.len()
        )));
    }
    if status == "partial" && slots.is_empty() {
        return Err(CompositionError(format!(
            "{}: declares (status partial) but binds every part — a hole is declared that is not there. Partial is declared, never claimed for nothing.",
            path.display()
        )));
    }
    Ok(slots)
}

fn fixed_triples(form: &Sexp) -> Result<Vec<(i128, i128, i128)>, String> {
    let fixed_forms = sexp::children(form, "fixed").map_err(|e| e.0)?;
    let Some(Sexp::List(items)) = fixed_forms.first() else {
        return Err("list index out of range".to_owned());
    };
    let mut out = Vec::new();
    for t in items.iter().skip(1) {
        let Sexp::List(abc) = t else {
            return Err(format!("cannot unpack non-iterable {} object", "int"));
        };
        if abc.len() != 3 {
            return Err(format!(
                "not enough values to unpack (expected 3, got {})",
                abc.len()
            ));
        }
        out.push((py_int(&abc[0])?, py_int(&abc[1])?, py_int(&abc[2])?));
    }
    Ok(out)
}

/// `load_fragment`: a unit `encoding.sexp` (validated, resolved), a bare `fragment.sexp` (validated), or a
/// riscv-opcodes table. Returns (instructions, pseudo-instructions).
pub fn load_fragment(root: &Path, path: &Path) -> Result<(Vec<Insn>, Vec<Insn>), CompositionError> {
    let shown = path.display().to_string();
    let file_name = path
        .file_name()
        .map(|n| n.to_string_lossy().into_owned())
        .unwrap_or_default();
    if path.extension().and_then(|e| e.to_str()) == Some("sexp") {
        let forms = sexp::read_file(path).map_err(|e| CompositionError(e.0))?;
        if forms.len() != 1 {
            return Err(CompositionError(format!(
                "{shown}: expected exactly one top-level form"
            )));
        }
        let mut rootform = forms[0].clone();
        let mut head = sexp::head(&rootform, &shown).map_err(|e| CompositionError(e.0))?;
        if head == "encoding" {
            schema_validate(root, path, "encoding")?;
            rootform = resolve_composition(&rootform, path)
                .map_err(|e: ResolveError| CompositionError(e.0))?;
            head = "fragment".to_owned();
        }
        if head == "fragment" {
            if file_name != "encoding.sexp" {
                schema_validate(root, path, "fragment")?;
            }
            let mut insns = Vec::new();
            let mut pseudos = Vec::new();
            for i in sexp::children(&rootform, "insn").map_err(|e| CompositionError(e.0))? {
                let fixed = fixed_triples(i).map_err(CompositionError)?;
                let name = py_str(sexp::field(i, "name", "").map_err(|e| CompositionError(e.0))?);
                insns.push(Insn::new(&name, &fixed, &file_name).map_err(CompositionError)?);
            }
            for p in sexp::children(&rootform, "pseudo").map_err(|e| CompositionError(e.0))? {
                let fixed = fixed_triples(p).map_err(CompositionError)?;
                let name = py_str(sexp::field(p, "name", "").map_err(|e| CompositionError(e.0))?);
                pseudos.push(Insn::new(&name, &fixed, &file_name).map_err(CompositionError)?);
            }
            return Ok((insns, pseudos));
        }
        return Err(CompositionError(format!(
            "{shown}: expected an (encoding …) unit document or a (fragment …) — got ({head} …)"
        )));
    }
    // a riscv-opcodes extension table
    let text =
        std::fs::read_to_string(path).map_err(|e| CompositionError(format!("{shown}: {e}")))?;
    let mut out = Vec::new();
    for raw in text.lines() {
        let line = raw.split('#').next().unwrap_or("").trim();
        if line.is_empty() || line.starts_with('$') {
            continue;
        }
        let mut toks = line.split_whitespace();
        let Some(name) = toks.next() else { continue };
        let mut fixed: Vec<(i128, i128, i128)> = Vec::new();
        for tok in toks {
            if let Some((range, val)) = tok.split_once('=') {
                let Some(v) = parse_int0(val) else { continue };
                if let Some((hi, lo)) = range.split_once("..") {
                    if let (Ok(h), Ok(l)) = (hi.parse::<i128>(), lo.parse::<i128>()) {
                        fixed.push((h, l, v));
                    }
                } else if let Ok(b) = range.parse::<i128>() {
                    fixed.push((b, b, v));
                }
            }
        }
        if !fixed.is_empty() {
            out.push(Insn::new(name, &fixed, &file_name).map_err(CompositionError)?);
        }
    }
    Ok((out, Vec::new()))
}

/// Python's `int(s, 0)`.
fn parse_int0(s: &str) -> Option<i128> {
    let t = s.trim().replace('_', "");
    let (neg, body) = match t.strip_prefix('-') {
        Some(rest) => (true, rest),
        None => (false, t.strip_prefix('+').unwrap_or(&t)),
    };
    let v = if let Some(h) = body.strip_prefix("0x").or_else(|| body.strip_prefix("0X")) {
        i128::from_str_radix(h, 16).ok()?
    } else if let Some(b) = body.strip_prefix("0b").or_else(|| body.strip_prefix("0B")) {
        i128::from_str_radix(b, 2).ok()?
    } else if let Some(o) = body.strip_prefix("0o").or_else(|| body.strip_prefix("0O")) {
        i128::from_str_radix(o, 8).ok()?
    } else {
        body.parse::<i128>().ok()?
    };
    Some(if neg { -v } else { v })
}

/// Every pair whose encodings overlap — exhaustive, as the pinned judge is.
pub fn collisions(insns: &[Insn]) -> Vec<(Insn, Insn)> {
    let mut out = Vec::new();
    for i in 0..insns.len() {
        for j in i + 1..insns.len() {
            let (a, b) = (&insns[i], &insns[j]);
            let common = a.mask & b.mask;
            if (a.value ^ b.value) & common == 0 {
                out.push((a.clone(), b.clone()));
            }
        }
    }
    out
}

/// The (special, general) pairs a fragment — or a unit's resolved composition — declares.
pub fn load_specializations(path: &Path) -> Result<Vec<(String, String)>, CompositionError> {
    if path.extension().and_then(|e| e.to_str()) != Some("sexp") {
        return Ok(Vec::new());
    }
    let shown = path.display().to_string();
    let forms = sexp::read_file(path).map_err(|e| CompositionError(e.0))?;
    let Some(first) = forms.first() else {
        return Err(CompositionError("list index out of range".to_owned()));
    };
    let mut rootform = first.clone();
    if sexp::head(&rootform, &shown).map_err(|e| CompositionError(e.0))? == "encoding" {
        rootform = resolve_composition(&rootform, path)
            .map_err(|e: ResolveError| CompositionError(e.0))?;
    }
    let mut out = Vec::new();
    for s in sexp::children(&rootform, "specializes").map_err(|e| CompositionError(e.0))? {
        out.push((
            py_str(sexp::field(s, "special", &shown).map_err(|e| CompositionError(e.0))?),
            py_str(sexp::field(s, "general", &shown).map_err(|e| CompositionError(e.0))?),
        ));
    }
    Ok(out)
}

/// (undeclared collisions, accepted specializations sorted, declaration problems).
pub fn judge_overlaps(insns: &[Insn], specs: &[(String, String)]) -> Overlaps {
    let by = |name: &str| insns.iter().find(|i| i.name == name);
    let mut problems = Vec::new();
    let mut accepted: BTreeSet<(String, String)> = BTreeSet::new();
    for (special, general) in specs {
        let (Some(s), Some(g)) = (by(special), by(general)) else {
            problems.push(format!("specialization {special} ⊂ {general} names an instruction the composition does not carry"));
            continue;
        };
        if g.mask & !s.mask != 0 || s.mask & !g.mask == 0 || (s.value ^ g.value) & g.mask != 0 {
            problems.push(format!(
                "specialization {special} ⊂ {general} is declared, but {special}'s word set is not strictly inside {general}'s"
            ));
            continue;
        }
        let mut pair = [special.clone(), general.clone()];
        pair.sort();
        accepted.insert((pair[0].clone(), pair[1].clone()));
    }
    let bad: Vec<(Insn, Insn)> = collisions(insns)
        .into_iter()
        .filter(|(a, b)| {
            let mut pair = [a.name.clone(), b.name.clone()];
            pair.sort();
            !accepted.contains(&(pair[0].clone(), pair[1].clone()))
        })
        .collect();
    (bad, accepted.into_iter().collect(), problems)
}

/// Decide the pseudo-instructions against the composed instruction set.
pub fn pseudo_problems(insns: &[Insn], pseudos: &[Insn]) -> Vec<String> {
    let mut out = Vec::new();
    for p in pseudos {
        let mut realized = false;
        for i in insns {
            let common = p.mask & i.mask;
            if (p.value ^ i.value) & common != 0 {
                continue;
            }
            if i.mask & !p.mask != 0 {
                out.push(format!(
                    "pseudo {} ({}) overlaps {} ({}) without specializing it — one word, two decode classes",
                    p.name, p.origin, i.name, i.origin
                ));
            } else {
                realized = true;
            }
        }
        if !realized {
            out.push(format!(
                "pseudo {} ({}) is realized by NO composed instruction — it would extend the encoding space it is declared not to touch",
                p.name, p.origin
            ));
        }
    }
    out
}

// ── the command line, as the pinned judge prints it ──────────────────────────────────────────

/// What the pinned CLI printed and returned.
pub struct Outcome {
    pub rc: i32,
    pub stdout: String,
    pub stderr: String,
}

/// `check_encoding_disjoint.py <fragment…>`: the composed set judged, the pinned texts.
pub fn judge(root: &Path, args: &[String]) -> Outcome {
    let mut out = String::new();
    let mut err = String::new();
    if args.is_empty() {
        err.push_str("usage: check_encoding_disjoint.py <fragment…>\n");
        return Outcome {
            rc: 2,
            stdout: out,
            stderr: err,
        };
    }
    let mut insns: Vec<Insn> = Vec::new();
    let mut pseudos: Vec<Insn> = Vec::new();
    let mut specs: Vec<(String, String)> = Vec::new();
    let mut all_slots: Vec<(String, Vec<String>)> = Vec::new();
    for arg in args {
        let p = Path::new(arg);
        if !p.exists() {
            err.push_str(&format!("REFUSED: {} does not exist\n", p.display()));
            return Outcome {
                rc: 2,
                stdout: out,
                stderr: err,
            };
        }
        let step: Result<(), CompositionError> = (|| {
            if p.extension().and_then(|e| e.to_str()) == Some("sexp") {
                let forms = sexp::read_file(p).map_err(|e| CompositionError(e.0))?;
                if forms.len() == 1
                    && sexp::head(&forms[0], &p.display().to_string())
                        .map_err(|e| CompositionError(e.0))?
                        == "encoding"
                {
                    all_slots.extend(check_slot_rules(p, &forms[0])?);
                }
            }
            let (part, part_pseudos) = load_fragment(root, p)?;
            if part.is_empty() && part_pseudos.is_empty() {
                return Err(CompositionError(format!("__EMPTY__{}", p.display())));
            }
            let name = p
                .file_name()
                .map(|n| n.to_string_lossy().into_owned())
                .unwrap_or_default();
            out.push_str(&format!(
                "  fragment {name:16} {:3} instruction(s)",
                part.len()
            ));
            if !part_pseudos.is_empty() {
                out.push_str(&format!(", {} pseudo-instruction(s)", part_pseudos.len()));
            }
            out.push('\n');
            insns.extend(part);
            pseudos.extend(part_pseudos);
            specs.extend(load_specializations(p)?);
            Ok(())
        })();
        if let Err(CompositionError(e)) = step {
            if let Some(shown) = e.strip_prefix("__EMPTY__") {
                err.push_str(&format!("REFUSED: {shown} yielded no instructions — an empty fragment is not a valid one\n"));
            } else {
                err.push_str(&format!("REFUSED: {e}\n"));
            }
            return Outcome {
                rc: 2,
                stdout: out,
                stderr: err,
            };
        }
    }
    let names: Vec<&str> = insns
        .iter()
        .map(|i| i.name.as_str())
        .chain(pseudos.iter().map(|p| p.name.as_str()))
        .collect();
    let mut dupes: Vec<&str> = names
        .iter()
        .copied()
        .filter(|n| names.iter().filter(|m| m == &n).count() > 1)
        .collect::<BTreeSet<_>>()
        .into_iter()
        .collect();
    dupes.sort();
    let (bad, accepted, spec_problems) = judge_overlaps(&insns, &specs);
    let mut problems = pseudo_problems(&insns, &pseudos);
    problems.extend(spec_problems);
    out.push_str(&format!("\n  composed set: {} instruction(s)", insns.len()));
    if !pseudos.is_empty() {
        out.push_str(&format!(" (+ {} pseudo-instruction(s))", pseudos.len()));
    }
    out.push_str(&format!(" from {} fragment(s)\n", args.len()));
    if !accepted.is_empty() {
        out.push_str(&format!(
            "  declared specializations: {} (the special row decodes first)\n",
            accepted.len()
        ));
    }
    if !dupes.is_empty() {
        out.push_str(&format!(
            "  DUPLICATE NAME(S): {}\n",
            sexp::py_repr(&Sexp::List(
                dupes.iter().map(|d| Sexp::Str((*d).to_owned())).collect()
            ))
        ));
    }
    if !bad.is_empty() {
        out.push_str(&format!("  COLLISIONS: {}\n", bad.len()));
        for (a, b) in bad.iter().take(10) {
            out.push_str(&format!(
                "    {} ({}) overlaps {} ({})  mask={:#010x}\n",
                a.name,
                a.origin,
                b.name,
                b.origin,
                a.mask & b.mask
            ));
        }
    }
    if !problems.is_empty() {
        out.push_str(&format!("  PSEUDO PROBLEMS: {}\n", problems.len()));
        for line in problems.iter().take(10) {
            out.push_str(&format!("    {line}\n"));
        }
    }
    if !bad.is_empty() || !problems.is_empty() {
        out.push_str(
            "\n  REJECTED — these fragments do not compose. A decoder cannot be generated from a\n",
        );
        out.push_str("  set in which one word matches two instructions.\n");
        return Outcome {
            rc: 1,
            stdout: out,
            stderr: err,
        };
    }
    if !dupes.is_empty() {
        out.push_str("\n  REJECTED — duplicate instruction names in one composition.\n");
        return Outcome {
            rc: 1,
            stdout: out,
            stderr: err,
        };
    }
    out.push_str("  no collisions, no duplicate names — the fragments COMPOSE.\n");
    out.push_str(
        "  ⚠️ This decides the DECODER composes. It says nothing about whether the semantics do.\n",
    );
    if !all_slots.is_empty() {
        out.push_str(&format!(
            "\n  PARTIAL — {} slot(s) unbound:\n",
            all_slots.len()
        ));
        for (sid, requires) in &all_slots {
            let req = if requires.is_empty() {
                "nothing declared".to_owned()
            } else {
                requires.join(", ")
            };
            out.push_str(&format!("    {sid} requires {req}\n"));
        }
        out.push_str("  the bound parts compose; the slot's requirements are checkable before its unit exists. Partial is declared, never inferred from silence.\n");
    }
    Outcome {
        rc: 0,
        stdout: out,
        stderr: err,
    }
}

// ── the pinned judge's self-test, re-asserted in-process ─────────────────────────────────────

fn write(path: &Path, text: &str) {
    if let Some(parent) = path.parent() {
        let _ = std::fs::create_dir_all(parent);
    }
    let _ = std::fs::write(path, text);
}

/// The 17 arms of `check_encoding_disjoint.py --self-test`: same labels, fixtures and needles.
pub fn self_test(root: &Path) -> i32 {
    let mut passed = 0u32;
    let mut failed = 0u32;
    let Ok(tmp) = crate::harness::scratch(root, "target/doctrine-selftest", "disjoint") else {
        eprintln!("check_encoding_disjoint self-test: cannot create a scratch directory under target/doctrine-selftest");
        return 1;
    };
    let defs = tmp.join("definitions");
    let unit_dir = tmp.join("profiles").join("p");
    let _ = std::fs::create_dir_all(&defs);
    let _ = std::fs::create_dir_all(&unit_dir);
    let frag = |frag_id: &str, insns: &[(&str, u32)], requires: Option<&str>| {
        let req = requires
            .map(|r| format!(" (requires \"{r}\")"))
            .unwrap_or_default();
        let body: String = insns
            .iter()
            .map(|(n, f3)| {
                format!(
                    "(insn (name \"{n}\") (fixed (31 25 0x0) (14 12 {f3}) (6 2 0x13) (1 0 0x3)))\n"
                )
            })
            .collect();
        write(
            &defs.join(format!("{frag_id}.sexp")),
            &format!("(fragment (id \"{frag_id}\") (kind extension){req}\n{body})"),
        );
    };
    let raw_frag = |frag_id: &str, body: &str| {
        write(
            &defs.join(format!("{frag_id}.sexp")),
            &format!("(fragment (id \"{frag_id}\") (kind extension)\n{body})"),
        );
    };
    let enc_doc = |base: &str, exts: &[&str], extra: &str| -> String {
        let ext: String = exts
            .iter()
            .map(|e| format!(" (extensions \"{e}\")"))
            .collect();
        let doc = format!(
            "(encoding (profile \"p\") (ilen 32)\n  (compose (base \"{base}\"){ext}{extra})\n  (fragment-root \"definitions\"))\n"
        );
        let p = unit_dir.join("encoding.sexp");
        write(&p, &doc);
        p.display().to_string()
    };
    frag("riscv/t-base", &[("add", 0), ("sub", 1)], None);
    frag("riscv/t-ext", &[("mul", 2)], None);
    frag("riscv/t-clash", &[("add", 0)], None);
    frag("riscv/t-needy", &[("div", 3)], Some("riscv/t-missing"));
    raw_frag(
        "riscv/t-csr",
        "(insn (name \"csrish\") (fixed (14 12 0x2) (6 2 0x13) (1 0 0x3)))\n",
    );
    raw_frag("riscv/t-pseudo", "(pseudo (name \"rdish\") (of \"t::csrish\") (fixed (31 20 0x5) (19 15 0x0) (14 12 0x2) (6 2 0x13) (1 0 0x3)) (operands) (from \"t\"))\n");
    raw_frag("riscv/t-ghost-pseudo", "(pseudo (name \"ghost\") (of \"t::csrish\") (fixed (31 20 0x5) (19 15 0x0) (14 12 0x4) (6 2 0x13) (1 0 0x3)) (operands) (from \"t\"))\n");
    raw_frag("riscv/t-ambi-pseudo", "(pseudo (name \"ambi\") (of \"t::csrish\") (fixed (31 28 0x1) (14 12 0x2)) (operands) (from \"t\"))\n");
    frag("riscv/t-dupe", &[("add", 7)], None);
    frag("riscv/t-slot", &[("rem", 4)], None);
    let mut arm = |label: &str, args: Vec<String>, needle: &str, rc: i32| {
        let o = judge(root, &args);
        let combined = format!("{}{}", o.stdout, o.stderr);
        if o.rc != rc {
            println!("  FAIL  {label}: expected rc={rc} got {}: {combined}", o.rc);
            failed += 1;
        } else if !combined.contains(needle) {
            println!("  FAIL  {label}: no {needle:?} in:\n{combined}");
            failed += 1;
        } else {
            println!("  ok    {label}");
            passed += 1;
        }
    };
    arm(
        "GREEN a complete unit composes through the shared resolver",
        vec![enc_doc("riscv/t-base", &["riscv/t-ext"], "")],
        "the fragments COMPOSE",
        0,
    );
    arm(
        "GREEN a declared slot reports partial, requiring a part that does not exist yet",
        vec![enc_doc(
            "riscv/t-base",
            &[],
            " (status partial) (slot (id clint) (requires \"riscv/t-timer\"))",
        )],
        "PARTIAL — 1 slot(s) unbound",
        0,
    );
    arm(
        "RED   slots without a partial declaration claim completeness",
        vec![enc_doc("riscv/t-base", &[], " (slot (id clint))")],
        "claiming completeness while a hole is open",
        2,
    );
    arm(
        "RED   a partial declaration with nothing unbound",
        vec![enc_doc("riscv/t-base", &[], " (status partial)")],
        "a hole is declared that is not there",
        2,
    );
    arm(
        "RED   an undeclared compose field is refused by the schema layer, not skipped",
        vec![enc_doc("riscv/t-base", &[], " (widget \"x\")")],
        "undeclared field \"widget\"",
        2,
    );
    arm(
        "RED   a fragment the composition names but does not have",
        vec![enc_doc("riscv/t-ghost", &[], "")],
        "does not exist",
        2,
    );
    arm(
        "RED   a fragment whose requires the composition does not provide",
        vec![enc_doc("riscv/t-needy", &[], "")],
        "unmet dependency",
        2,
    );
    arm(
        "RED   a collision through the resolved unit path is still a rejection",
        vec![enc_doc("riscv/t-base", &["riscv/t-clash"], "")],
        "COLLISIONS: 1",
        1,
    );
    arm(
        "GREEN a pseudo-instruction specializing a composed instruction adds nothing",
        vec![enc_doc(
            "riscv/t-base",
            &["riscv/t-csr", "riscv/t-pseudo"],
            "",
        )],
        "pseudo-instruction(s)",
        0,
    );
    arm(
        "RED   a pseudo no composed instruction realizes extends the encoding space",
        vec![enc_doc(
            "riscv/t-base",
            &["riscv/t-csr", "riscv/t-ghost-pseudo"],
            "",
        )],
        "extend the encoding space",
        1,
    );
    arm(
        "RED   a pseudo overlapping without specializing is the collision rule one level down",
        vec![enc_doc(
            "riscv/t-base",
            &["riscv/t-csr", "riscv/t-ambi-pseudo"],
            "",
        )],
        "without specializing",
        1,
    );
    arm(
        "RED   duplicate instruction names are a rejection, not an advisory",
        vec![enc_doc("riscv/t-base", &["riscv/t-dupe"], "")],
        "DUPLICATE NAME(S)",
        1,
    );
    let spec_frag = |frag_id: &str, body: &str| {
        write(
            &defs.join(format!("{frag_id}.sexp")),
            &format!("(fragment (id \"{frag_id}\") (kind isa-extension) (requires)\n  (source (file (name \"t\") (sha256 \"0\")) (origin \"t\") (license \"t\"))\n{body})"),
        );
    };
    let gen = "(insn (name gen) (fixed (1 0 0x1) (15 13 0x0)) (operands) (from \"t\"))\n";
    let spc =
        "(insn (name spc) (fixed (1 0 0x1) (15 13 0x0) (11 7 0x0)) (operands) (from \"t\"))\n";
    let oth = "(insn (name oth) (fixed (1 0 0x1) (15 13 0x0) (6 2 0x3)) (operands) (from \"t\"))\n";
    let decl = "(specializes (special spc) (general gen) (from \"t\"))\n";
    spec_frag("riscv/t-spec-ok", &format!("{gen}{spc}{decl}"));
    spec_frag("riscv/t-spec-undeclared", &format!("{gen}{spc}"));
    spec_frag(
        "riscv/t-spec-reversed",
        &format!("{gen}{spc}(specializes (special gen) (general spc) (from \"t\"))\n"),
    );
    spec_frag("riscv/t-spec-ghost", &format!("{gen}{oth}(specializes (special ghost) (general gen) (from \"t\"))\n(specializes (special oth) (general gen) (from \"t\"))\n"));
    spec_frag("riscv/t-spec-other", oth);
    let d = |n: &str| defs.join(format!("riscv/{n}.sexp")).display().to_string();
    arm(
        "GREEN a declared strict specialization composes, reported",
        vec![d("t-spec-ok")],
        "declared specializations: 1",
        0,
    );
    arm(
        "RED   the same overlap undeclared is still a collision",
        vec![d("t-spec-undeclared")],
        "COLLISIONS: 1",
        1,
    );
    arm(
        "RED   a declaration whose 'special' row is the wider one is refused, not obeyed",
        vec![d("t-spec-reversed")],
        "is not strictly inside",
        1,
    );
    arm(
        "RED   a declaration naming an instruction the composition lacks is refused",
        vec![d("t-spec-ghost")],
        "does not carry",
        1,
    );
    arm(
        "RED   a declaration cannot silence an overlap it does not name",
        vec![d("t-spec-ok"), d("t-spec-other")],
        "COLLISIONS: 2",
        1,
    );
    let _ = std::fs::remove_dir_all(&tmp);
    println!("check_encoding_disjoint --self-test: {passed} pass / {failed} fail");
    i32::from(failed > 0)
}

/// `cargo xtask check-encoding-disjoint <fragment…> | --self-test`, the pinned CLI's surface.
pub fn run(root: &Path, args: &[String]) -> std::process::ExitCode {
    let rc = if args.len() == 1 && args[0] == "--self-test" {
        self_test(root)
    } else {
        let o = judge(root, args);
        print!("{}", o.stdout);
        eprint!("{}", o.stderr);
        o.rc
    };
    std::process::ExitCode::from(u8::try_from(rc).unwrap_or(1))
}
