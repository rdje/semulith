use super::*;
use crate::model_rv64gc::Model;

#[test]
fn the_inventory_covers_every_family_with_distinct_names_over_real_rows() {
    let mut names: Vec<&str> = MUTATIONS.iter().map(|m| m.name).collect();
    names.sort_unstable();
    names.dedup();
    assert_eq!(names.len(), MUTATIONS.len(), "mutant names are distinct");
    for family in [Family::I, Family::M, Family::A, Family::F, Family::D, Family::C, Family::Zicsr, Family::Privileged] {
        assert!(MUTATIONS.iter().any(|m| m.family == family), "{family:?} has at least one mutant");
    }
    for m in MUTATIONS {
        let table = table_for(m).unwrap_or_else(|e| panic!("{}: {e}", m.name));
        match m.how {
            Perturbation::Remove => assert_eq!(table.len(), INSNS.len() - 1, "{}", m.name),
            _ => assert_eq!(table.len(), INSNS.len(), "{}", m.name),
        }
        // every other row is the production row
        for (actual, canonical) in table.iter().zip(INSNS.iter().filter(|r| !(matches!(m.how, Perturbation::Remove) && r.name == m.row))) {
            if actual.name != m.row {
                assert!(std::ptr::eq(actual.effect, canonical.effect), "{}: row {} untouched", m.name, actual.name);
            }
        }
    }
}

#[test]
fn the_two_replay_controls_are_members_of_the_inventory() {
    for (model, name) in [(Model::ZextAddi, "zext-addi"), (Model::JalNoLink, "jal-no-link")] {
        let m = MUTATIONS.iter().find(|m| m.name == name).unwrap();
        assert!(matches!(m.how, Perturbation::Control(c) if c == model));
        let table = table_for(m).unwrap();
        let control = model.table().unwrap();
        assert!(table.iter().zip(control).all(|(a, b)| std::ptr::eq(a.effect, b.effect)));
    }
}

#[test]
fn the_production_table_is_the_anchor_every_guest_meets() {
    // the same rule the corpus proof applies, so a detection below can only come from the mutant
    for g in GUESTS {
        crate::run_rv64gc::assert_guest_observations(g.name);
    }
}

#[test]
fn every_designated_mutant_is_detected_by_the_corpus() {
    let census = census().unwrap();
    let undetected: Vec<&str> = census.iter().filter(|(_, d)| d.is_empty()).map(|(m, _)| m.name).collect();
    let mut report = String::new();
    for (m, d) in &census {
        let (first, at) = d.first().map_or(("-", 0), |(g, at)| (*g, *at));
        report.push_str(&format!("{:<22} {:<10} {:>3} detector(s), first {} at step {}\n", m.name, format!("{:?}", m.family), d.len(), first, at));
    }
    eprintln!("validator-mutation census ({} mutants over {} guests):\n{report}", census.len(), GUESTS.len());
    assert_eq!(
        undetected, KNOWN_GAPS,
        "the mutants no tracked guest detects must be exactly the pinned corpus gaps (a new gap is a finding; a closed gap moves the pin)\n{report}"
    );
    assert_eq!(census.len() - undetected.len(), 30, "every designated mutant is detected");
}

#[test]
fn every_pinned_gap_names_a_mutant_in_the_inventory() {
    for gap in KNOWN_GAPS {
        assert!(MUTATIONS.iter().any(|m| m.name == *gap), "{gap} is a designated mutant");
    }
}

#[test]
fn a_detector_diverges_where_the_control_test_says() {
    // the replay controls' documented first divergences (model_rv64gc tests): guest-control, steps 1 and 7
    for (name, at) in [("zext-addi", 1usize), ("jal-no-link", 7)] {
        let m = MUTATIONS.iter().find(|m| m.name == name).unwrap();
        let d = detectors(m).unwrap();
        let (_, step) = d.iter().find(|(g, _)| *g == "guest-control").unwrap_or_else(|| panic!("{name}: guest-control detects it"));
        assert_eq!(*step, at, "{name}");
    }
}
