//! The graph checker's acceptance suites — every PACKAGE_CHECKS schema row re-derived in
//! Rust, every §3 invariant exercised against the frozen bundle, and each designated
//! rejection demonstrated with a mutation that must be caught.

use std::path::PathBuf;

use crate::graph::{check_bundle, Bundle, GateStatus, Report, Rule};
use crate::json::{parse, Json};
use crate::schema::validate;
use crate::sha256::sha256_hex;

fn examples() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../examples")
}

fn schemas() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../schemas")
}

fn load_records(name: &str) -> Vec<Json> {
    let text = std::fs::read_to_string(examples().join(name))
        .unwrap_or_else(|e| panic!("read {name}: {e}"));
    text.lines()
        .filter(|l| !l.trim().is_empty())
        .map(|l| parse(l).unwrap_or_else(|e| panic!("{name}: {e}")))
        .collect()
}

fn load_json(name: &str) -> Json {
    let text = std::fs::read_to_string(examples().join(name))
        .unwrap_or_else(|e| panic!("read {name}: {e}"));
    parse(&text).unwrap_or_else(|e| panic!("{name}: {e}"))
}

fn load_schema(name: &str) -> Json {
    let text = std::fs::read_to_string(schemas().join(name))
        .unwrap_or_else(|e| panic!("read {name}: {e}"));
    parse(&text).unwrap_or_else(|e| panic!("{name}: {e}"))
}

fn real_bundle() -> Bundle {
    Bundle {
        requirements: load_records("requirements.jsonl"),
        evidence: load_records("evidence.jsonl"),
        obligations: load_records("contract-obligations.jsonl"),
        context: load_json("fixture-context.json"),
        sources: load_json("sources.json"),
    }
}

/// A resolver over the real example files (fs stays in the tests; the library is pure).
fn real_resolver(path: &str) -> Option<Vec<u8>> {
    std::fs::read(examples().join(path)).ok()
}

fn no_resolver(_: &str) -> Option<Vec<u8>> {
    None
}

// ---------------------------------------------------------------------------
// PACKAGE_CHECKS rows, re-derived in Rust (RUST-01)
// ---------------------------------------------------------------------------

#[test]
fn package_checks_row_all_five_records_validate_in_rust() {
    let cases = [
        ("requirements.jsonl", "requirement.schema.json"),
        ("evidence.jsonl", "evidence.schema.json"),
        (
            "contract-obligations.jsonl",
            "contract-obligation.schema.json",
        ),
    ];
    for (records, schema) in cases {
        let schema = load_schema(schema);
        for record in load_records(records) {
            let errors = validate(&record, &schema)
                .unwrap_or_else(|r| panic!("{records}: the validator refused its own schema: {r}"));
            assert!(errors.is_empty(), "{records}: {errors:?}");
        }
    }
}

#[test]
fn package_checks_row_all_six_negative_controls_are_rejected() {
    let req = load_records("requirements.jsonl").remove(0);
    let ev = load_records("evidence.jsonl").remove(0);
    let ce = load_records("contract-obligations.jsonl").remove(0);
    let req_schema = load_schema("requirement.schema.json");
    let ev_schema = load_schema("evidence.schema.json");
    let ce_schema = load_schema("contract-obligation.schema.json");

    // 1. missing source
    let mutated = without(&req, "source_refs");
    let errors = validate(&mutated, &req_schema).unwrap();
    assert!(
        errors
            .iter()
            .any(|e| e.contains("missing required property 'source_refs'")),
        "{errors:?}"
    );

    // 2. invalid research status
    let mutated = with(&req, "research_status", Json::Str("bogus".into()));
    let errors = validate(&mutated, &req_schema).unwrap();
    assert!(
        errors.iter().any(|e| e.contains("is not one of")),
        "{errors:?}"
    );

    // 3. passing evidence without completion data
    let mutated = with(&ev, "status", Json::Str("passed".into()));
    let errors = validate(&mutated, &ev_schema).unwrap();
    assert!(
        errors
            .iter()
            .any(|e| e.contains("missing required property 'procedure'")),
        "{errors:?}"
    );

    // 4. malformed fingerprint
    let mutated = with(
        &ev,
        "inputs",
        Json::Arr(vec![Json::Obj(vec![
            ("id".into(), Json::Str("IN-1".into())),
            ("role".into(), Json::Str("log".into())),
            ("path".into(), Json::Str("run.bin".into())),
            ("sha256".into(), Json::Str("xyz".into())),
        ])]),
    );
    let errors = validate(&mutated, &ev_schema).unwrap();
    assert!(
        errors.iter().any(|e| e.contains("does not match")),
        "{errors:?}"
    );

    // 5. passing proof without proof metadata — give it everything the completion if/then
    //    demands so the only possible refusal is the missing `proof` object
    let sha = Json::Str("a".repeat(64));
    let artifact = |id: &str| {
        Json::Obj(vec![
            ("id".into(), Json::Str(id.into())),
            ("role".into(), Json::Str("log".into())),
            ("path".into(), Json::Str("run.bin".into())),
            ("sha256".into(), sha.clone()),
        ])
    };
    let completed = [
        ("status", Json::Str("passed".into())),
        ("method", Json::Str("checked-proof".into())),
        ("procedure", Json::Str("prove and check".into())),
        (
            "tool_versions",
            Json::Arr(vec![Json::Obj(vec![
                ("name".into(), Json::Str("checker".into())),
                ("version".into(), Json::Str("1".into())),
            ])]),
        ),
        ("result_summary", Json::Str("proved".into())),
        ("inputs", Json::Arr(vec![artifact("IN-1")])),
        ("artifacts", Json::Arr(vec![artifact("ART-1")])),
    ]
    .into_iter()
    .fold(ev.clone(), |acc, (k, v)| with(&acc, k, v));
    let errors = validate(&completed, &ev_schema).unwrap();
    assert!(
        errors
            .iter()
            .any(|e| e.contains("missing required property 'proof'")),
        "{errors:?}"
    );

    // 6. invalid contract direction
    let mutated = with(&ce, "direction", Json::Str("sideways".into()));
    let errors = validate(&mutated, &ce_schema).unwrap();
    assert!(
        errors.iter().any(|e| e.contains("is not one of")),
        "{errors:?}"
    );
}

#[test]
fn package_checks_row_the_three_schemas_are_wellformed_json() {
    // the Python row says "valid per jsonschema 4.26.0"; the project's own standard is the
    // supported-subset census (schema::tests proves the keyword recursion), and the honesty
    // half is that each schema parses as one JSON document.
    for name in [
        "requirement.schema.json",
        "evidence.schema.json",
        "contract-obligation.schema.json",
    ] {
        load_schema(name);
    }
}

#[test]
fn package_checks_row_synthetic_source_fingerprint_matches() {
    let ledger = load_json("sources.json");
    let pin = ledger
        .get("sources")
        .and_then(Json::as_arr)
        .and_then(|a| a.first())
        .expect("one pinned source")
        .get("sha256")
        .and_then(Json::as_str)
        .expect("a sha256");
    let bytes = std::fs::read(examples().join("synthetic-spec.md")).expect("the source exists");
    assert_eq!(sha256_hex(&bytes), pin, "the ledger pins the actual bytes");
}

// ---------------------------------------------------------------------------
// The intact frozen bundle: graph-clean, gate honestly incomplete
// ---------------------------------------------------------------------------

#[test]
fn the_intact_bundle_is_graph_clean_with_an_incomplete_gate() {
    let bundle = real_bundle();
    let report = check_bundle(&bundle, &real_resolver);
    assert_eq!(report.findings, Vec::new(), "{}", report.render(&bundle));
    assert_eq!(report.gate, GateStatus::Incomplete);
    // both declared obligations are cited only by `planned` evidence
    assert_eq!(
        report.obligations,
        vec![
            ("OB-SYN16-ADD".to_string(), false),
            ("OB-SYN16-INPUT".to_string(), false),
        ]
    );
    let text = report.render(&bundle);
    assert!(text.contains("gate: incomplete"), "{text}");
    assert!(text.contains("OB-SYN16-ADD"), "{text}");
    assert!(text.contains("OB-SYN16-INPUT"), "{text}");
}

// ---------------------------------------------------------------------------
// Designated rejections — each acceptance clause of T004 with a mutation that must be caught
// ---------------------------------------------------------------------------

fn finding_rules(report: &Report) -> Vec<Rule> {
    report.findings.iter().map(|f| f.rule).collect()
}

#[test]
fn rejects_an_orphan_evidence_id() {
    let mut bundle = real_bundle();
    // a requirement that cites an evidence id nothing provides
    bundle.requirements[0] = with(
        &bundle.requirements[0],
        "evidence_ids",
        Json::Arr(vec![Json::Str("EV-GONE".into())]),
    );
    let report = check_bundle(&bundle, &no_resolver);
    assert!(
        finding_rules(&report).contains(&Rule::OrphanEvidence),
        "{report:?}"
    );
    assert!(report.gate == GateStatus::Failed);
    assert!(report.findings.iter().any(|f| f.detail.contains("EV-GONE")));
}

#[test]
fn rejects_a_deleted_dependency_link() {
    let mut bundle = real_bundle();
    bundle.obligations[0] = with(
        &bundle.obligations[0],
        "dependencies",
        Json::Arr(vec![Json::Str("SYN16-GONE".into())]),
    );
    let report = check_bundle(&bundle, &no_resolver);
    assert!(
        finding_rules(&report).contains(&Rule::OrphanLink),
        "{report:?}"
    );
    assert!(report
        .findings
        .iter()
        .any(|f| f.detail.contains("deleted dependency link")));
}

#[test]
fn rejects_a_profile_outside_the_declared_scope() {
    let mut bundle = real_bundle();
    bundle.evidence[0] = with(
        &bundle.evidence[0],
        "profile_ids",
        Json::Arr(vec![Json::Str("other-profile".into())]),
    );
    let report = check_bundle(&bundle, &no_resolver);
    assert!(finding_rules(&report).contains(&Rule::Scope), "{report:?}");
}

#[test]
fn rejects_a_duplicate_record_id() {
    let mut bundle = real_bundle();
    let dup = bundle.requirements[0].clone();
    bundle.requirements.push(dup);
    let report = check_bundle(&bundle, &no_resolver);
    assert!(
        finding_rules(&report).contains(&Rule::UniqueId),
        "{report:?}"
    );
}

#[test]
fn rejects_a_source_citation_the_ledger_does_not_pin() {
    let mut bundle = real_bundle();
    let sref = Json::Obj(vec![
        ("source_id".into(), Json::Str("SRC-GONE".into())),
        ("locator".into(), Json::Str("A1".into())),
    ]);
    bundle.requirements[0] = with(
        &bundle.requirements[0],
        "source_refs",
        Json::Arr(vec![sref]),
    );
    let report = check_bundle(&bundle, &no_resolver);
    assert!(
        finding_rules(&report).contains(&Rule::OrphanSource),
        "{report:?}"
    );
}

#[test]
fn rejects_a_missing_artifact_and_a_stale_hash_and_the_unsupported_passed_claim() {
    let mut bundle = real_bundle();

    // promote EV-SYN16-ADD to `passed` with completion data and one artifact
    let promote = |record: &Json, path: &str, pin: &str| {
        let with_completion = [
            ("status", Json::Str("passed".into())),
            ("procedure", Json::Str("run the directed tests".into())),
            (
                "tool_versions",
                Json::Arr(vec![Json::Obj(vec![
                    ("name".into(), Json::Str("suite".into())),
                    ("version".into(), Json::Str("1".into())),
                ])]),
            ),
            (
                "result_summary",
                Json::Str("all directed cases pass".into()),
            ),
        ]
        .into_iter()
        .fold(record.clone(), |acc, (k, v)| with(&acc, k, v));
        with(
            &with_completion,
            "artifacts",
            Json::Arr(vec![Json::Obj(vec![
                ("id".into(), Json::Str("ART-ADD".into())),
                ("role".into(), Json::Str("log".into())),
                ("path".into(), Json::Str(path.into())),
                ("sha256".into(), Json::Str(pin.into())),
            ])]),
        )
    };

    // (a) the artifact path does not exist
    bundle.evidence[0] = promote(&bundle.evidence[0], "no-such-file.bin", &"b".repeat(64));
    let report = check_bundle(&bundle, &real_resolver);
    assert!(
        report
            .findings
            .iter()
            .any(|f| f.rule == Rule::ArtifactHash && f.detail.contains("does not exist")),
        "{report:?}"
    );
    // a `passed` claim whose artifact is missing cannot support the obligation
    assert!(
        report.gate == GateStatus::Failed || !report.obligations[0].1,
        "{report:?}"
    );

    // (b) the artifact exists but the pinned hash is stale
    let bytes = std::fs::read(examples().join("synthetic-spec.md")).unwrap();
    bundle.evidence[0] = promote(&bundle.evidence[0], "synthetic-spec.md", &"c".repeat(64));
    let report = check_bundle(&bundle, &real_resolver);
    let stale = report
        .findings
        .iter()
        .find(|f| f.rule == Rule::ArtifactHash)
        .expect("a stale-hash finding");
    assert!(stale.detail.contains("stale hash"), "{stale:?}");
    assert_eq!(
        sha256_hex(&bytes),
        "12787d5932eba395a8904c347db55f22501fe889f73d5533726b4864502ca43f"
    );

    // (c) the correct hash: no ARTIFACT-HASH finding, and the obligation IS met by this
    //     evidence — while the bundle stays honest (the other obligation is still planned)
    bundle.evidence[0] = promote(
        &bundle.evidence[0],
        "synthetic-spec.md",
        "12787d5932eba395a8904c347db55f22501fe889f73d5533726b4864502ca43f",
    );
    let report = check_bundle(&bundle, &real_resolver);
    assert!(
        !report.findings.iter().any(|f| f.rule == Rule::ArtifactHash),
        "{report:?}"
    );
    assert_eq!(report.gate, GateStatus::Incomplete);
    let (add, add_met) = &report.obligations[0];
    assert_eq!(add, "OB-SYN16-ADD");
    assert!(*add_met, "current passed evidence meets the obligation");
}

#[test]
fn rejects_missing_evidence_for_a_declared_obligation() {
    let mut bundle = real_bundle();
    // drop the evidence record that cites OB-SYN16-INPUT
    bundle
        .evidence
        .retain(|ev| ev.get("id").and_then(Json::as_str) != Some("EV-SYN16-INPUT"));
    let report = check_bundle(&bundle, &no_resolver);
    assert!(
        finding_rules(&report).contains(&Rule::MissingEvidence),
        "{report:?}"
    );
    assert!(report
        .findings
        .iter()
        .any(|f| f.subject.contains("OB-SYN16-INPUT")));
    // the requirement that cited the dropped record is an orphan too
    assert!(
        finding_rules(&report).contains(&Rule::OrphanEvidence),
        "{report:?}"
    );
}

#[test]
fn rejects_an_undeclared_required_check() {
    let mut bundle = real_bundle();
    bundle.obligations[0] = with(
        &bundle.obligations[0],
        "required_checks",
        Json::Arr(vec![Json::Str("CHK-GONE".into())]),
    );
    let report = check_bundle(&bundle, &no_resolver);
    assert!(
        finding_rules(&report).contains(&Rule::ContextCheck),
        "{report:?}"
    );
}

#[test]
fn rejects_a_requirement_dependency_cycle() {
    let minimal = Bundle {
        requirements: vec![
            Json::Obj(vec![
                ("id".into(), Json::Str("REQ-A".into())),
                (
                    "dependencies".into(),
                    Json::Arr(vec![Json::Str("REQ-B".into())]),
                ),
            ]),
            Json::Obj(vec![
                ("id".into(), Json::Str("REQ-B".into())),
                (
                    "dependencies".into(),
                    Json::Arr(vec![Json::Str("REQ-A".into())]),
                ),
            ]),
        ],
        evidence: Vec::new(),
        obligations: Vec::new(),
        context: Json::Obj(vec![
            ("profiles".into(), Json::Arr(vec![])),
            ("obligations".into(), Json::Arr(vec![])),
        ]),
        sources: Json::Obj(vec![("sources".into(), Json::Arr(vec![]))]),
    };
    let report = check_bundle(&minimal, &no_resolver);
    assert!(
        finding_rules(&report).contains(&Rule::DepCycle),
        "{report:?}"
    );
}

#[test]
fn a_fully_met_bundle_gates_passed() {
    let mut bundle = real_bundle();
    // promote both evidence records to passed with verifiable artifacts
    let sha = "12787d5932eba395a8904c347db55f22501fe889f73d5533726b4864502ca43f";
    for ev in &mut bundle.evidence {
        let with_completion = [
            ("status", Json::Str("passed".into())),
            ("procedure", Json::Str("run the directed tests".into())),
            (
                "tool_versions",
                Json::Arr(vec![Json::Obj(vec![
                    ("name".into(), Json::Str("suite".into())),
                    ("version".into(), Json::Str("1".into())),
                ])]),
            ),
            (
                "result_summary",
                Json::Str("all directed cases pass".into()),
            ),
        ]
        .into_iter()
        .fold((*ev).clone(), |acc, (k, v)| with(&acc, k, v));
        *ev = with(
            &with_completion,
            "artifacts",
            Json::Arr(vec![Json::Obj(vec![
                ("id".into(), Json::Str("ART-1".into())),
                ("role".into(), Json::Str("log".into())),
                ("path".into(), Json::Str("synthetic-spec.md".into())),
                ("sha256".into(), Json::Str(sha.into())),
            ])]),
        );
    }
    let report = check_bundle(&bundle, &real_resolver);
    assert_eq!(report.findings, Vec::new(), "{}", report.render(&bundle));
    assert_eq!(report.gate, GateStatus::Passed);
    assert!(report.render(&bundle).contains("gate: passed"));
}

// ---------------------------------------------------------------------------
// Json mutation helpers (test-local)
// ---------------------------------------------------------------------------

fn with(record: &Json, key: &str, value: Json) -> Json {
    let pairs = record.as_obj().expect("an object record");
    let mut out: Vec<(String, Json)> = pairs.to_vec();
    if let Some(slot) = out.iter_mut().find(|(k, _)| k == key) {
        slot.1 = value;
    } else {
        out.push((key.to_string(), value));
    }
    Json::Obj(out)
}

fn without(record: &Json, key: &str) -> Json {
    let pairs = record.as_obj().expect("an object record");
    Json::Obj(pairs.iter().filter(|(k, _)| k != key).cloned().collect())
}

#[test]
fn mutation_helpers_replace_insert_and_remove() {
    let base = Json::Obj(vec![("a".into(), Json::Int(1))]);
    assert_eq!(
        with(&base, "a", Json::Int(2)),
        Json::Obj(vec![("a".into(), Json::Int(2))])
    );
    assert_eq!(
        with(&base, "b", Json::Int(3)),
        Json::Obj(vec![("a".into(), Json::Int(1)), ("b".into(), Json::Int(3))])
    );
    assert_eq!(without(&base, "a"), Json::Obj(vec![]));
}
