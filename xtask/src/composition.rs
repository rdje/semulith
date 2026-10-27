//! The one composition resolver (`XTASK.6` slices `6k`/`6m`), ported from `riscv_asm.resolve_composition`: a unit's
//! `compose` form resolved into one synthetic `(fragment …)` form. A missing fragment or an unmet `requires` is refused
//! by name, with the pinned resolver's words. Consumed by the exercise-coverage census and the disjointness judge alike —
//! a second hand-written resolver is how a silent regression happens (`MODEL-COMPOSE.4`, measured).

use std::collections::BTreeSet;
use std::path::Path;

use crate::sexp::{self, Sexp};

/// A refusal of the composition, in the pinned resolver's words (`riscv_asm.AsmError`).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ResolveError(pub String);

fn py_str(v: &Sexp) -> String {
    match v {
        Sexp::Int(n) => n.to_string(),
        Sexp::Str(s) | Sexp::Symbol(s) => s.clone(),
        Sexp::List(_) => sexp::py_repr(v),
    }
}

pub fn resolve_composition(enc: &Sexp, path: &Path) -> Result<Sexp, ResolveError> {
    let shown = path.display().to_string();
    let comp = sexp::children(enc, "compose").map_err(|e| ResolveError(e.0))?;
    let Some(comp0) = comp.first() else {
        return Ok(enc.clone());
    };
    let frag_root = path
        .parent()
        .and_then(Path::parent)
        .and_then(Path::parent)
        .unwrap_or(Path::new(""))
        .join(py_str(
            sexp::field(enc, "fragment-root", &shown).map_err(|e| ResolveError(e.0))?,
        ));
    let mut names = vec![py_str(
        sexp::field(comp0, "base", &shown).map_err(|e| ResolveError(e.0))?,
    )];
    for e in sexp::children(comp0, "extensions").map_err(|e| ResolveError(e.0))? {
        if let Sexp::List(items) = e {
            names.extend(items.iter().skip(1).map(py_str));
        }
    }
    let mut merged = vec![Sexp::Symbol("fragment".to_owned())];
    let mut declared: BTreeSet<String> = BTreeSet::new();
    for name in &names {
        let frag_path = frag_root.join(format!("{name}.sexp"));
        if !frag_path.is_file() {
            return Err(ResolveError(format!(
                "{shown}: composes '{name}', but {} does not exist",
                frag_path.display()
            )));
        }
        let forms = sexp::read_file(&frag_path).map_err(|e| ResolveError(e.0))?;
        let Some(frag) = forms.first() else {
            return Err(ResolveError("list index out of range".to_owned()));
        };
        declared.insert(py_str(
            sexp::field(frag, "id", &frag_path.display().to_string())
                .map_err(|e| ResolveError(e.0))?,
        ));
        for r in sexp::children(frag, "requires").map_err(|e| ResolveError(e.0))? {
            if let Sexp::List(items) = r {
                for req in items.iter().skip(1) {
                    let req = py_str(req);
                    if !declared.contains(&req) {
                        return Err(ResolveError(format!(
                            "{shown}: fragment '{name}' requires '{req}', which this composition does not provide \
                             before it. A fragment with an unmet dependency composes by luck, not by construction."
                        )));
                    }
                }
            }
        }
        if let Sexp::List(items) = frag {
            for c in items {
                if let Sexp::List(l) = c {
                    if matches!(
                        l.first().and_then(Sexp::text),
                        Some("field" | "scatter" | "insn" | "pseudo" | "specializes")
                    ) {
                        merged.push(c.clone());
                    }
                }
            }
        }
    }
    Ok(Sexp::List(merged))
}
