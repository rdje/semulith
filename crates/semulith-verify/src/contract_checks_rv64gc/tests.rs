//! The registry's proof: every realized check runs, and every check a v1 obligation (or the
//! partial-progress guarantee) declares is realized.

use super::CHECKS;
use crate::guests_rv64gc::GUESTS;
use crate::run_rv64gc::assert_guest_observations;

const OBLIGATIONS: &str =
    include_str!("../../../../profiles/rv64gc-lab-v0/contract-obligations.sexp");

#[test]
fn every_realized_check_runs_its_guests_and_they_hold() {
    for check in CHECKS {
        assert!(
            !check.guests.is_empty(),
            "{}: a check that names no guest checks nothing",
            check.id
        );
        for name in check.guests {
            assert!(
                GUESTS.iter().any(|g| g.name == *name),
                "{}: names {name}, which is not a tracked guest",
                check.id
            );
            assert_guest_observations(name);
        }
    }
}

/// The `required_checks` ids of every obligation record the predicate selects.
fn declared_checks(select: impl Fn(&str) -> bool) -> Vec<(String, String)> {
    let mut out = Vec::new();
    for line in OBLIGATIONS
        .lines()
        .filter(|l| l.starts_with("(obligation ") && select(l))
    {
        let id = line
            .split('"')
            .nth(1)
            .expect("an obligation id")
            .to_string();
        for part in line.split("(required_checks \"").skip(1) {
            out.push((
                id.clone(),
                part.split('"').next().expect("a check id").to_string(),
            ));
        }
    }
    out
}

#[test]
fn every_v1_check_and_the_partial_progress_checks_are_realized() {
    let declared = declared_checks(|l| {
        l.contains("(contract_version \"1\")")
            || l.starts_with("(obligation (id \"OB-GC-PARTIAL-PROGRESS\")")
    });
    assert_eq!(
        declared.len(),
        10,
        "four v1 assumptions and the partial-progress guarantee, POS + NEG each"
    );
    for (ob, chk) in declared {
        let realized = CHECKS.iter().find(|c| c.id == chk);
        assert!(
            realized.is_some(),
            "{ob} declares {chk}, which no registry entry realizes"
        );
        assert_eq!(
            realized.map(|c| c.obligation),
            Some(ob.as_str()),
            "{chk} is registered under another obligation"
        );
    }
}
