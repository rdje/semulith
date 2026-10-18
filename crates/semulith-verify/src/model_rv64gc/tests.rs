use super::*;
use crate::fixtures::FlatMemory;
use crate::guests_rv64gc::GUESTS;
use crate::run_rv64gc;
use crate::snapshot_rv64gc::SnapshotRv64gc;
use semulith_core::state_rv64gc::ArchitecturalState;

#[test]
fn full_profile_controls_preserve_every_other_row_and_reuse_bounded_tables() {
    assert!(std::ptr::eq(Model::Production.table().unwrap(), INSNS));
    for (model, target) in [(Model::ZextAddi, "addi"), (Model::JalNoLink, "jal")] {
        let table = model.table().unwrap();
        assert!(std::ptr::eq(table, model.table().unwrap()));
        assert_eq!(table.len(), INSNS.len());
        let mut changed = Vec::new();
        for (actual, canonical) in table.iter().zip(INSNS) {
            assert_eq!(
                (
                    actual.name,
                    actual.mask,
                    actual.value,
                    actual.operands,
                    actual.from,
                    actual.source,
                    actual.length
                ),
                (
                    canonical.name,
                    canonical.mask,
                    canonical.value,
                    canonical.operands,
                    canonical.from,
                    canonical.source,
                    canonical.length
                )
            );
            assert_eq!(
                actual.expansion.map(std::ptr::from_ref),
                canonical.expansion.map(std::ptr::from_ref)
            );
            if !std::ptr::eq(actual.effect, canonical.effect) {
                changed.push(actual.name);
            }
        }
        assert_eq!(changed, [target]);
    }
}

#[test]
fn production_control_matches_existing_api_and_complete_state_for_every_guest() {
    for guest in GUESTS {
        let mut plain = FlatMemory::with_fetch_align(guest.entry, 0x10000, 2);
        plain.load_image(0, guest.image);
        let mut named = FlatMemory::with_fetch_align(guest.entry, 0x10000, 2);
        named.load_image(0, guest.image);
        let mut left = ArchitecturalState::zeroed_at(guest.entry);
        let mut right = ArchitecturalState::zeroed_at(guest.entry);
        let baseline = run_rv64gc::run_from_with_refusals(
            &mut plain,
            &mut left,
            guest.executed_steps,
            guest.refusals,
        );
        let actual = run_rv64gc::run_from_with_model(
            &mut named,
            &mut right,
            guest.executed_steps,
            guest.refusals,
            Model::Production,
        )
        .unwrap();
        assert_eq!(actual, baseline, "{}", guest.name);
        assert_eq!(
            actual,
            run_rv64gc::run_guest_with_model(guest, Model::Production)
                .unwrap()
                .0
        );
        let checkpoint = |env: &FlatMemory, state: &mut ArchitecturalState| {
            SnapshotRv64gc::capture(
                env,
                state,
                guest.entry,
                guest.executed_steps,
                guest.executed_steps,
                guest.refusals,
            )
            .unwrap()
        };
        assert_eq!(
            checkpoint(&named, &mut right),
            checkpoint(&plain, &mut left),
            "{}",
            guest.name
        );
    }
    println!(
        "{} guests: production control trace/fetch/state/memory parity",
        GUESTS.len()
    );
}

#[test]
fn designated_wrong_models_disagree_at_the_expected_boundary_and_register() {
    let guest = run_rv64gc::guest("guest-control");
    let clean = run_rv64gc::run_guest(guest).0;
    for (model, at, register) in [(Model::ZextAddi, 1, 1), (Model::JalNoLink, 7, 5)] {
        let wrong = run_rv64gc::run_guest_with_model(guest, model).unwrap().0;
        assert!(wrong.failed.is_none());
        let first = clean
            .steps
            .iter()
            .zip(&wrong.steps)
            .position(|(a, b)| a != b)
            .unwrap();
        assert_eq!(first, at, "{}", model.name());
        assert_eq!(clean.steps[at].pc, wrong.steps[at].pc);
        assert_eq!(clean.steps[at].mode, wrong.steps[at].mode);
        let value = |step: &run_rv64gc::Step| {
            step.writes
                .iter()
                .find(|(r, _)| *r == register)
                .map(|(_, v)| *v)
        };
        assert_ne!(value(&clean.steps[at]), value(&wrong.steps[at]));
        assert_eq!(
            clean.steps[at].writes, guest.expected[at].writes,
            "spec-derived anchor"
        );
    }
}

#[test]
fn compressed_expansions_keep_their_own_effects_under_named_32_bit_controls() {
    let guest = run_rv64gc::guest("c-links");
    let baseline = run_rv64gc::run_guest(guest).0;
    for model in [Model::ZextAddi, Model::JalNoLink] {
        assert_eq!(
            run_rv64gc::run_guest_with_model(guest, model).unwrap().0,
            baseline
        );
    }
}

#[test]
fn unknown_names_and_changed_effect_shapes_refuse() {
    for name in ["", "phantom-load", "jalr-odd-bit", "unknown"] {
        assert!(Model::from_mutation(name)
            .unwrap_err()
            .contains("unknown RV64GC mutation"));
    }
    for model in [Model::ZextAddi, Model::JalNoLink] {
        for effect in [
            &Sem::Nop,
            &Sem::Set(&Sem::Reg("rs1"), &Sem::Lit(0)),
            &Sem::Seq(&[]),
        ] {
            assert!(perturb(model, effect)
                .unwrap_err()
                .contains("shape changed"));
        }
    }
    for (name, model) in [
        ("none", Model::Production),
        ("zext-addi", Model::ZextAddi),
        ("jal-no-link", Model::JalNoLink),
    ] {
        assert_eq!(Model::from_mutation(name).unwrap(), model);
    }
}

#[test]
fn canonical_recorded_names_roundtrip_and_reject_cli_aliases() {
    for model in [Model::Production, Model::ZextAddi, Model::JalNoLink] {
        assert_eq!(Model::from_name(model.name()).unwrap(), model);
    }
    for name in ["none", "zext-addi", "mutant:none", "unknown", ""] {
        assert!(Model::from_name(name)
            .unwrap_err()
            .contains("unknown RV64GC replay model"));
    }
}
