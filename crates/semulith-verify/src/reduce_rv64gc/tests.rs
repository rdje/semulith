use super::*;
use crate::guests_rv64gc::{RefusalKind, GUESTS};

fn control(model: Model) -> Case<'static> {
    let guest = GUESTS.iter().find(|g| g.name == "guest-control").unwrap();
    Case {
        entry: guest.entry,
        budget: guest.executed_steps,
        refusals: guest.refusals,
        model,
        evaluation_limit: MAX_EVALUATIONS,
    }
}
fn control_image() -> &'static [u8] {
    GUESTS
        .iter()
        .find(|g| g.name == "guest-control")
        .unwrap()
        .image
}
fn witness_single_deletion_minimal(case: &Case, reduction: &Reduction) {
    assert!(reduction.one_minimal);
    for at in (0..reduction.image.len()).step_by(2) {
        let end = (at + 2).min(reduction.image.len());
        let image: Vec<_> = reduction.image[..at]
            .iter()
            .chain(&reduction.image[end..])
            .copied()
            .collect();
        assert_ne!(
            difference(case, &image).ok().flatten(),
            Some(reduction.retained.clone()),
            "deletion at {at}"
        );
    }
}

#[test]
fn both_controls_reduce_and_replay_the_exact_original_paired_difference() {
    for (model, at, register) in [(Model::ZextAddi, 1, 1), (Model::JalNoLink, 7, 5)] {
        let case = control(model);
        let original = difference(&case, control_image()).unwrap().unwrap();
        assert_eq!(original.at, at);
        assert!(original
            .reference
            .writes
            .iter()
            .any(|(r, _)| *r == register));
        let (record, reduction) = Reproducer::record(&case, control_image()).unwrap();
        assert!(reduction.image.len() < control_image().len());
        assert_eq!(reduction.retained, original);
        assert!(reduction.evaluations <= MAX_EVALUATIONS);
        witness_single_deletion_minimal(&case, &reduction);
        let text = record.to_json();
        assert!(text.len() < MAX_JSON_BYTES);
        let parsed = Reproducer::parse(&text).unwrap();
        assert_eq!(parsed, record);
        assert_eq!(parsed.replay().unwrap(), original);
        assert!(matches!(
            ReplayRecord::parse(&text).unwrap(),
            ReplayRecord::Reduced(_)
        ));
    }
}

#[test]
fn mixed_compressed_word_and_single_data_tail_retain_halfword_pc_and_values() {
    let mut image = vec![0x01, 0x00]; // C.NOP
    image.extend_from_slice(&0xfff00093u32.to_le_bytes()); // ADDI x1,x0,-1
    image.extend_from_slice(&[0x01, 0x00]);
    image.extend_from_slice(&0x0000006fu32.to_le_bytes()); // JAL x0,self
    image.push(0xaa); // data need not be instruction sized
    let case = Case {
        entry: 0x80000000,
        budget: 4,
        refusals: &[],
        model: Model::ZextAddi,
        evaluation_limit: MAX_EVALUATIONS,
    };
    let (record, reduction) = Reproducer::record(&case, &image).unwrap();
    assert_eq!(reduction.image, image[..6]);
    assert_eq!(reduction.retained.at, 1);
    assert_eq!(reduction.retained.reference.pc, case.entry + 2);
    assert_eq!(reduction.retained.model.pc, case.entry + 2);
    assert_eq!(reduction.retained.reference.writes, [(1, u64::MAX)]);
    assert_eq!(reduction.retained.model.writes, [(1, 4095)]);
    witness_single_deletion_minimal(&case, &reduction);
    assert_eq!(record.replay().unwrap(), reduction.retained);
    // Typed environment choices survive the record and each trial.
    let refusals = [Refusal {
        kind: RefusalKind::Fetch,
        base: case.entry + 8,
        size: 2,
    }];
    let case = Case {
        refusals: &refusals,
        ..case
    };
    let (record, reduction) = Reproducer::record(&case, &image).unwrap();
    assert_eq!(record.replay().unwrap(), reduction.retained);
    assert!(record.to_json().contains("refusals"));
}

#[test]
fn evaluation_limit_includes_original_and_final_and_does_not_claim_minimality() {
    for limit in [2, 3, 5] {
        let case = Case {
            evaluation_limit: limit,
            ..control(Model::ZextAddi)
        };
        let (record, reduction) = Reproducer::record(&case, control_image()).unwrap();
        assert_eq!(reduction.evaluations, limit);
        assert!(!reduction.one_minimal);
        if limit == 2 {
            assert_eq!(reduction.image, control_image());
        }
        assert_eq!(record.replay().unwrap(), reduction.retained);
    }
}

#[test]
fn no_trigger_and_bounds_refuse_instead_of_claiming_trace_agreement() {
    for model in [Model::Production, Model::ZextAddi] {
        let case = control(model);
        for image in [&[][..], &[0x01, 0x00][..]] {
            assert_eq!(reduce(&case, image), Err(ReduceError::NoPairedDifference));
        }
    }
    for case in [
        Case {
            budget: MAX_STEPS + 1,
            ..control(Model::ZextAddi)
        },
        Case {
            evaluation_limit: 1,
            ..control(Model::ZextAddi)
        },
        Case {
            evaluation_limit: MAX_EVALUATIONS + 1,
            ..control(Model::ZextAddi)
        },
        Case {
            entry: u64::MAX - 1,
            ..control(Model::ZextAddi)
        },
    ] {
        assert!(matches!(
            reduce(&case, control_image()),
            Err(ReduceError::Invalid(_))
        ));
    }
    assert!(matches!(
        reduce(&control(Model::ZextAddi), &vec![0; MEMORY_BYTES + 1]),
        Err(ReduceError::Invalid(_))
    ));
}

#[test]
fn altered_receipts_models_inputs_and_identity_are_discriminated() {
    let (record, _) = Reproducer::record(&control(Model::ZextAddi), control_image()).unwrap();
    let mut altered = record.clone();
    altered.evaluations += 1;
    assert!(altered.replay().unwrap_err().contains("search receipt"));
    let mut altered = record.clone();
    altered.one_minimal = !altered.one_minimal;
    assert!(altered.replay().unwrap_err().contains("search receipt"));
    let mut altered = record.clone();
    altered.original_image.fill(0);
    assert!(altered.replay().unwrap_err().contains("no paired step"));
    let mut altered = record.clone();
    altered.reducer_sha256 = "0".repeat(64);
    assert!(altered.replay().unwrap_err().contains("identity"));
    let text = record.to_json();
    let changed = text.replacen("mutant:zext-addi", "production", 1);
    assert!(Reproducer::parse(&changed)
        .unwrap_err()
        .contains("model choice"));
    let changed = text.replacen(
        "\"final_sha256\":\"",
        &format!("\"final_sha256\":\"{}", "0".repeat(64)),
        1,
    );
    assert!(Reproducer::parse(&changed).is_err());
    // A syntactically valid altered full-run receipt is caught during replay.
    let old = record.reference.to_json();
    let start = old.find("\"final_sha256\":\"").unwrap() + "\"final_sha256\":\"".len();
    let mut changed = old.clone();
    changed.replace_range(start..start + 64, &"0".repeat(64));
    let changed = text.replacen(&old, &changed, 1);
    assert!(Reproducer::parse(&changed)
        .unwrap()
        .replay()
        .unwrap_err()
        .contains("reference run receipt"));
    for changed in [
        "{}".to_owned(),
        text.replace("\"one_minimal\":true", "\"one_minimal\":0"),
        text.replacen("\"original_image\":\"", "\"original_image\":\"zz", 1),
        text.replacen("\"image_len\":", "\"image_len\":999999", 1),
    ] {
        assert!(Reproducer::parse(&changed).is_err());
    }
    assert!(Reproducer::parse(&" ".repeat(MAX_JSON_BYTES + 1)).is_err());
    assert!(ReplayRecord::parse(&"[".repeat(13)).is_err());
    assert!(ReplayRecord::parse(&format!(
        "{{\"format\":\"{FORMAT}\",\"pad\":\"{}\"}}",
        "x".repeat(MAX_JSON_BYTES)
    ))
    .unwrap_err()
    .contains("16 MiB"));
}

#[test]
fn paired_inputs_and_cold_state_are_required_before_reduction_replay() {
    let (record, _) = Reproducer::record(&control(Model::ZextAddi), control_image()).unwrap();
    let cold = record
        .reference
        .input()
        .cold_image(MEMORY_BYTES, record.image_len)
        .unwrap();
    let mut memory = FlatMemory::with_fetch_align(cold.entry, MEMORY_BYTES, 2);
    memory.load_image(0, &cold.image);
    let mut state = ArchitecturalState::zeroed_at(cold.entry);
    state.write_x(31, 17);
    let warm = SnapshotRv64gc::capture(
        &memory,
        &mut state,
        cold.entry,
        0,
        cold.budget,
        &cold.refusals,
    )
    .unwrap();
    let mut altered = record.clone();
    altered.reference = BundleRv64gc::record(warm.clone()).unwrap();
    // Different child inputs refuse before executing a reduction.
    assert!(altered.replay().unwrap_err().contains("paired input"));
    altered.model = BundleRv64gc::record_with_model(warm, Model::ZextAddi).unwrap();
    assert!(altered.replay().unwrap_err().contains("canonical cold"));
    let mut altered = record.clone();
    altered.image_len = 0;
    assert!(altered.replay().unwrap_err().contains("canonical cold"));
    // A differently encoded image can change the pair's values; an equal index
    // and register name alone must not count as exact retention.
    let case = control(Model::ZextAddi);
    let mut changed = control_image().to_vec();
    changed[6] ^= 0x10; // ADDI immediate changes its reported values.
    let original = difference(&case, control_image()).unwrap().unwrap();
    let candidate = difference(&case, &changed).unwrap().unwrap();
    assert_eq!(candidate.at, original.at);
    assert_ne!(candidate, original);
}
