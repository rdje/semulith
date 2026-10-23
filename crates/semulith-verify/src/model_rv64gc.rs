//! Bounded deliberately wrong RV64GC control models for replay/reduction tools.
//!
//! These perturb data consumed by the one production evaluator. The complete
//! generated table, including compressed/privileged/FP rows, remains present.
//! Only the named 32-bit ADDI or JAL effect changes; compressed expansions retain
//! their own generated effects. This is not the full P4.15 mutation campaign.

use semulith_core::definition_rv64gc::{InsnDef, Sem, INSNS};
use std::sync::OnceLock;

/// The RV64GC model a replay or reduction runs: production, or one bounded control mutant.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Model {
    /// The generated production definition, unchanged.
    Production,
    /// Control mutant: the 32-bit ADDI zero-extends its immediate instead of sign-extending it.
    ZextAddi,
    /// Control mutant: the 32-bit JAL does not write its link register.
    JalNoLink,
}

impl Model {
    /// Canonical recorded model identity, distinct from the CLI's mutation spelling.
    pub fn from_name(name: &str) -> Result<Self, String> {
        match name {
            "production" => Ok(Self::Production),
            "mutant:zext-addi" => Ok(Self::ZextAddi),
            "mutant:jal-no-link" => Ok(Self::JalNoLink),
            _ => Err(format!("unknown RV64GC replay model '{name}'")),
        }
    }

    /// The model the CLI's mutation spelling names (`none`, `zext-addi`, `jal-no-link`).
    pub fn from_mutation(name: &str) -> Result<Self, String> {
        match name {
            "none" => Ok(Self::Production),
            "zext-addi" => Ok(Self::ZextAddi),
            "jal-no-link" => Ok(Self::JalNoLink),
            _ => Err(format!(
                "unknown RV64GC mutation '{name}' (none, zext-addi, jal-no-link)"
            )),
        }
    }

    /// The canonical recorded identity, the inverse of [`Model::from_name`].
    #[must_use]
    pub fn name(self) -> &'static str {
        match self {
            Self::Production => "production",
            Self::ZextAddi => "mutant:zext-addi",
            Self::JalNoLink => "mutant:jal-no-link",
        }
    }

    /// Each overlay is built once. Its small rebuilt spine has a bounded static
    /// lifetime, matching generated Sem references, without leaks per invocation.
    pub fn table(self) -> Result<&'static [InsnDef], String> {
        static ZEXT: OnceLock<Result<Vec<InsnDef>, String>> = OnceLock::new();
        static JAL: OnceLock<Result<Vec<InsnDef>, String>> = OnceLock::new();
        let cache = match self {
            Self::Production => return Ok(INSNS),
            Self::ZextAddi => &ZEXT,
            Self::JalNoLink => &JAL,
        };
        cache
            .get_or_init(|| build(self))
            .as_ref()
            .map(Vec::as_slice)
            .map_err(Clone::clone)
    }
}

fn build(model: Model) -> Result<Vec<InsnDef>, String> {
    let name = match model {
        Model::Production => return Err("production needs no control overlay".into()),
        Model::ZextAddi => "addi",
        Model::JalNoLink => "jal",
    };
    let mut table: Vec<InsnDef> = INSNS.iter().map(|row| InsnDef { ..*row }).collect();
    let row = table
        .iter_mut()
        .find(|row| row.name == name && row.length == 4 && row.expansion.is_none())
        .ok_or_else(|| format!("RV64GC control: expected canonical 32-bit {name} row"))?;
    row.effect = perturb(model, row.effect)?;
    Ok(table)
}

fn perturb(model: Model, effect: &'static Sem) -> Result<&'static Sem, String> {
    match (model, effect) {
        (Model::ZextAddi, Sem::Set(destination, Sem::Add(left, Sem::Sext(64, immediate))))
            if matches!(destination, Sem::Reg("rd"))
                && matches!(left, Sem::Reg("rs1"))
                && matches!(immediate, Sem::Imm("imm12")) =>
        {
            let zero = Box::leak(Box::new(Sem::Zext(64, immediate)));
            let add = Box::leak(Box::new(Sem::Add(left, zero)));
            Ok(Box::leak(Box::new(Sem::Set(destination, add))))
        }
        (Model::JalNoLink, Sem::Seq(steps))
            if steps.len() == 2
                && matches!(steps[0], Sem::SetPc(_))
                && matches!(steps[1], Sem::Set(destination, _) if matches!(destination, Sem::Reg("rd"))) =>
        {
            Ok(steps[0])
        }
        _ => Err(format!(
            "RV64GC control {}: canonical effect shape changed",
            model.name()
        )),
    }
}

#[cfg(test)]
mod tests;
