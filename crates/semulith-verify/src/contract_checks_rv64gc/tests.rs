//! Every registered check runs, and every check bound through the current slice is present.

use super::{Evidence, CHECKS};
use crate::guests_rv64gc::GUESTS;
use crate::run_rv64gc::assert_guest_observations;

const OBLIGATIONS: &str =
    include_str!("../../../../profiles/rv64gc-lab-v0/contract-obligations.sexp");

#[test]
fn every_realized_check_runs_its_evidence_and_it_holds() {
    for check in CHECKS {
        match check.evidence {
            Evidence::Guests(guests) => {
                assert!(
                    !guests.is_empty(),
                    "{}: a check that names no guest checks nothing",
                    check.id
                );
                for name in guests {
                    assert!(
                        GUESTS.iter().any(|g| g.name == *name),
                        "{}: names {name}, which is not a tracked guest",
                        check.id
                    );
                    assert_guest_observations(name);
                }
            }
            Evidence::Scope => {
                let result = scope_check(check.id, None);
                assert!(
                    result.status.success(),
                    "{}: scope check failed: {}{}",
                    check.id,
                    String::from_utf8_lossy(&result.stdout),
                    String::from_utf8_lossy(&result.stderr)
                );
            }
        }
    }
}

fn scope_check(id: &str, mutation: Option<&str>) -> std::process::Output {
    let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
    let mut command = std::process::Command::new("python3");
    command
        .current_dir(root)
        .args(["scripts/check_gc_contract_scope.py", "--check", id]);
    if let Some(mutation) = mutation {
        command.args(["--mutation", mutation]);
    }
    command.output().expect("the named scope checker must run")
}

#[test]
fn scope_controls_reject_disabled_predicates_and_unknown_checks() {
    for mutation in ["ignore-profile", "ignore-fragments"] {
        let result = scope_check("CHK-GC-COMPOSITION-NEG", Some(mutation));
        assert_eq!(result.status.code(), Some(1), "{mutation}");
        assert!(
            String::from_utf8_lossy(&result.stdout).contains("CONTROL-MISSED:"),
            "{mutation}: must fail for a missed violating fixture: {result:?}"
        );
    }
    let result = scope_check("CHK-GC-UNKNOWN-POS", None);
    assert_eq!(result.status.code(), Some(2));
    assert!(String::from_utf8_lossy(&result.stdout).contains("UNKNOWN-CHECK:"));
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
fn every_check_bound_through_the_scope_slice_is_realized() {
    // every version after v0 is born realized: v1's four assumptions and two supersessions,
    // v2's M/C guarantees and parcel-fetch assumption as they bind, partial progress,
    // and the seven static scope pairs (P4-SYSTEM.13 b2/b3).
    let declared = declared_checks(|l| {
        !l.contains("(contract_version \"0\")")
            || l.starts_with("(obligation (id \"OB-GC-PARTIAL-PROGRESS\")")
            || l.starts_with("(obligation (id \"OB-GC-COMPOSITION\")")
            || l.starts_with("(obligation (id \"OB-EXT-CLOSURE\")")
            || l.starts_with("(obligation (id \"OB-PRIV-REVISION\")")
            || l.starts_with("(obligation (id \"OB-CSR-SET\")")
            || l.starts_with("(obligation (id \"OB-NO-PMP\")")
            || l.starts_with("(obligation (id \"OB-NO-H\")")
            || l.starts_with("(obligation (id \"OB-SCOPE-CENSUS\")")
    });
    assert_eq!(
        declared.len(),
        34,
        "v1's six records, v2's M/C/fetch records, partial progress and seven scope records, POS + NEG"
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

/// `P4-SYSTEM.10` slice (a): the gate report counts an entry only under the obligation that
/// declares its check, so an entry naming an undeclared id — or a declared id under another
/// obligation — would run its guests and be counted by nothing. Refused here, where it is
/// written.
#[test]
fn every_registry_entry_realizes_a_check_its_obligation_declares() {
    let declared = declared_checks(|_| true);
    for check in CHECKS {
        assert!(
            declared
                .iter()
                .any(|(ob, chk)| ob == check.obligation && chk == check.id),
            "{} under {}: no obligation record declares this pair",
            check.id,
            check.obligation
        );
    }
}
