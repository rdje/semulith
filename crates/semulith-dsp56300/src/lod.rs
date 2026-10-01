//! The runner's input dialects: the pinned assembler's `.lod` image and the harness's
//! `.meta` case line.
//!
//! `.lod` (observed on the pinned `dsp56300-asm`'s `-f lod` output): one
//! `P <addr4hex> <word6hex>` line per program word, then `I <addr6hex> <symbol>` symbol
//! lines the runner ignores. Anything else is a typed input stop.
//!
//! `.meta` (the difftest corpus case line, `tools/difftest/README.md`):
//! `case <name> <load6hex> <stop6hex> <budget>`. Fill headers (the dirty-state banks) are
//! NOT in subset v0 — a meta carrying one is a `ModelStop::Input`, named.

use crate::machine::{Machine, ModelStop};

/// A parsed case: load base (also the start pc), stop pc, and step budget.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Case {
    pub name: String,
    pub load: u32,
    pub stop: u32,
    pub budget: u64,
}

pub fn parse_meta(text: &str) -> Result<Case, ModelStop> {
    let line = text
        .lines()
        .find(|l| !l.trim().is_empty())
        .ok_or_else(|| ModelStop::Input("empty meta".into()))?;
    let mut parts = line.split_whitespace();
    let mut field = |what: &str| {
        parts
            .next()
            .ok_or_else(|| ModelStop::Input(format!("meta case line lacks {what}")))
    };
    if field("the `case` head")? != "case" {
        return Err(ModelStop::Input(format!(
            "meta's first line is not a case line: {line:?} (fill headers are not in subset v0)"
        )));
    }
    let name = field("the case name")?.to_string();
    let mut hex = |what: &str| {
        u32::from_str_radix(field(what)?, 16)
            .map_err(|_| ModelStop::Input(format!("meta {what} is not hex")))
    };
    let load = hex("load base")?;
    let stop = hex("stop pc")?;
    let budget = field("the step budget")?
        .parse::<u64>()
        .map_err(|_| ModelStop::Input("meta step budget is not a number".into()))?;
    if parts.next().is_some() {
        return Err(ModelStop::Input(format!(
            "meta case line carries extra fields (fill tuples are not in subset v0): {line:?}"
        )));
    }
    Ok(Case {
        name,
        load,
        stop,
        budget,
    })
}

/// Load a `.lod` image into the machine's P space. Returns the case the runner needs:
/// words are placed at their absolute addresses; the P window bounds are checked.
pub fn load_lod(m: &mut Machine, text: &str) -> Result<(), ModelStop> {
    for (n, line) in text.lines().enumerate() {
        let line = line.trim();
        if line.is_empty() {
            continue;
        }
        let mut parts = line.split_whitespace();
        match parts.next() {
            Some("P") => {
                let addr = parts
                    .next()
                    .and_then(|a| u32::from_str_radix(a, 16).ok())
                    .ok_or_else(|| {
                        ModelStop::Input(format!("lod line {}: bad P address", n + 1))
                    })?;
                let word = parts
                    .next()
                    .and_then(|w| u32::from_str_radix(w, 16).ok())
                    .ok_or_else(|| ModelStop::Input(format!("lod line {}: bad P word", n + 1)))?;
                *m.p.get_mut(addr as usize)
                    .ok_or(ModelStop::OutOfWindow { space: 'P', addr })? =
                    word & crate::machine::MASK24;
            }
            // Symbol lines and comments carry no loadable content.
            Some("I") => {}
            Some(_) | None => {
                return Err(ModelStop::Input(format!(
                    "lod line {}: not a P/I line: {line:?}",
                    n + 1
                )))
            }
        }
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_the_demo_case_line() {
        let case = parse_meta("case micro 000100 000115 100\n").unwrap();
        assert_eq!(
            case,
            Case {
                name: "micro".into(),
                load: 0x100,
                stop: 0x115,
                budget: 100
            }
        );
    }

    #[test]
    fn refuses_a_fill_header_by_name() {
        assert!(matches!(
            parse_meta("fill 1 2 3 4 5 6\ncase micro 000100 000115 100\n"),
            Err(ModelStop::Input(_))
        ));
    }

    #[test]
    fn loads_the_demo_lod_dialect() {
        let mut m = Machine::new();
        load_lod(&mut m, "P 0100 44F400\nP 0101 123456\nI 000100 start\n").unwrap();
        assert_eq!(m.p[0x100], 0x44F400);
        assert_eq!(m.p[0x101], 0x123456);
    }
}
