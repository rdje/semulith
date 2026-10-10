//! Every registered check runs, and every check bound through the current slice is present.

use super::{Evidence, CHECKS};
use crate::guests_rv64gc::GUESTS;
use crate::run_rv64gc::assert_guest_observations;

fn catalog(profile: &str, file: &str) -> String {
    let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
    let path = format!("profiles/{profile}/{file}");
    let result = std::process::Command::new("python3")
        .current_dir(root)
        .args(["scripts/record_catalog.py", &path, "--stdout"])
        .output()
        .expect("the catalog expansion owner must run");
    assert!(
        result.status.success(),
        "catalog expansion failed: {result:?}"
    );
    String::from_utf8(result.stdout).expect("canonical catalogs are UTF-8")
}

fn obligations() -> &'static str {
    static TEXT: std::sync::OnceLock<String> = std::sync::OnceLock::new();
    TEXT.get_or_init(|| catalog("rv64gc-lab-v0", "contract-obligations.sexp"))
}

fn assert_shift_requirement_associations(profile: &str) {
    let text = catalog(profile, "requirements.sexp");
    let requirement = text
        .lines()
        .find(|line| line.starts_with("(requirement (id \"REQ-D-SHAMT\")"))
        .expect("the shift-count requirement must exist");
    let mut actual: Vec<_> = requirement
        .split("(insns \"")
        .skip(1)
        .map(|field| field.split('"').next().expect("an instruction field"))
        .collect();
    // RV64I 3.1.2.1–2 and the requirement's statement name all twelve forms.
    // Aggregate coverage through WSUFFIX must not hide a missing SHAMT edge.
    let mut expected = vec![
        "slli", "srli", "srai", "sll", "srl", "sra", "slliw", "srliw", "sraiw", "sllw", "srlw",
        "sraw",
    ];
    actual.sort_unstable();
    expected.sort_unstable();
    assert_eq!(actual, expected, "{profile}: complete SHAMT associations");
}

#[test]
fn rv64i_shift_requirement_covers_all_twelve_forms() {
    assert_shift_requirement_associations("rv64i-lab-v0");
}

#[test]
fn rv64gc_shift_requirement_covers_all_twelve_forms() {
    assert_shift_requirement_associations("rv64gc-lab-v0");
}

#[test]
fn every_realized_check_runs_its_evidence_and_it_holds() {
    for check in CHECKS {
        match check.evidence {
            Evidence::Guests(guests) => {
                run_guests(check.id, guests);
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
            Evidence::Boundary(boundary) => {
                assert_eq!(boundary.run(), Ok(()), "{}: {boundary:?}", check.id);
            }
            Evidence::Execution(execution) => {
                run_guests(check.id, execution.guests());
                assert_eq!(execution.run(), Ok(()), "{}: {execution:?}", check.id);
            }
        }
    }
}

fn run_guests(id: &str, guests: &[&str]) {
    assert!(
        !guests.is_empty(),
        "{id}: a check that names no guest checks nothing"
    );
    for name in guests {
        assert!(
            GUESTS.iter().any(|g| g.name == *name),
            "{id}: names {name}, which is not a tracked guest"
        );
        assert_guest_observations(name);
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
    for line in obligations()
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
    // v2's guarantees and assumptions as they bind, partial progress,
    // the eleven static selection pairs (P4-SYSTEM.13 b2/b3/b5), c1's three corrections,
    // and c8–c12's privilege-mode/Sv39/Svade/alignment/counter witnesses.
    let declared = declared_checks(|l| {
        !l.contains("(contract_version \"0\")")
            || l.starts_with("(obligation (id \"OB-GC-PARTIAL-PROGRESS\")")
            || l.starts_with("(obligation (id \"OB-GC-COMPOSITION\")")
            || l.starts_with("(obligation (id \"OB-EXT-CLOSURE\")")
            || l.starts_with("(obligation (id \"OB-PRIV-REVISION\")")
            || l.starts_with("(obligation (id \"OB-PRIV-MODES\")")
            || l.starts_with("(obligation (id \"OB-SV39\")")
            || l.starts_with("(obligation (id \"OB-SVADE\")")
            || l.starts_with("(obligation (id \"OB-IALIGN-16\")")
            || l.starts_with("(obligation (id \"OB-ZICNTR\")")
            || l.starts_with("(obligation (id \"OB-SSTC\")")
            || l.starts_with("(obligation (id \"OB-ALU-IMM\")")
            || l.starts_with("(obligation (id \"OB-ALU-REG\")")
            || l.starts_with("(obligation (id \"OB-LUI-AUIPC\")")
            || l.starts_with("(obligation (id \"OB-SHAMT\")")
            || l.starts_with("(obligation (id \"OB-WSUFFIX\")")
            || l.starts_with("(obligation (id \"OB-LOAD-EXT\")")
            || l.starts_with("(obligation (id \"OB-LOAD-X0\")")
            || l.starts_with("(obligation (id \"OB-ENDIAN\")")
            || l.starts_with("(obligation (id \"OB-NO-DELAY-SLOTS\")")
            || l.starts_with("(obligation (id \"OB-JALR-LSB\")")
            || l.starts_with("(obligation (id \"OB-CSR-SET\")")
            || l.starts_with("(obligation (id \"OB-NO-PMP\")")
            || l.starts_with("(obligation (id \"OB-NO-H\")")
            || l.starts_with("(obligation (id \"OB-SCOPE-CENSUS\")")
            || l.starts_with("(obligation (id \"OB-ABI\")")
            || l.starts_with("(obligation (id \"OB-SBI\")")
            || l.starts_with("(obligation (id \"OB-RVWMO\")")
            || l.starts_with("(obligation (id \"OB-PRIV-INSNS\")")
    });
    assert_eq!(
        declared.len(),
        92,
        "every declared POS/NEG check of the completed slices is selected"
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
