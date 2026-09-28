//! Tests for the demo/bench report: the report is the `.9` suite's anchor made reusable, so
//! its judgement must agree with the suite — clean runs meet the pinned expectations, the
//! exposed mutations diverge exactly where the suite pins them, and the JSON round-trips
//! through the crate's own reader.

use super::*;
use crate::json::{self, Json};

#[test]
fn clean_runs_meet_the_pinned_expectations() {
    for guest in GUESTS {
        let run = run_guest(guest.name, "none").unwrap();
        assert!(
            run.expectations_met,
            "{}: the real model meets the expectations",
            guest.name
        );
        assert!(
            run.census_met,
            "{}: the real model meets the census",
            guest.name
        );
        assert!(run.divergence.is_none());
        assert_eq!(
            run.data_crossings, run.census_pinned,
            "{}: the census pin",
            guest.name
        );
    }
}

#[test]
fn the_exposed_mutations_diverge_where_the_suite_pins_them() {
    // The trace-level mutants break the architectural anchor where the .9 suite pins them;
    // the census arm is the deliberate inversion — the trace still agrees, the census breaks.
    let cases = [
        ("guest-control", "zext-addi", Some(1usize)),
        ("guest-control", "jal-no-link", Some(7)),
        ("guest-control", "jalr-odd-bit", Some(10)),
    ];
    for (guest, mutation, at) in cases {
        let run = run_guest(guest, mutation).unwrap();
        assert!(
            !run.expectations_met,
            "{mutation}: a designated mutant breaks the anchor"
        );
        assert!(run.census_met, "{mutation}: the census is untouched");
        assert_eq!(
            run.divergence.as_ref().map(|d| d.at),
            at,
            "{mutation}: diverges where the .9 suite pins it"
        );
    }
}

#[test]
fn the_phantom_load_moves_the_census_not_the_trace() {
    let run = run_guest("guest-control", "phantom-load").unwrap();
    assert!(
        run.expectations_met,
        "the architectural trace still agrees — that is the arm's point"
    );
    assert!(!run.census_met);
    assert_eq!(run.divergence, None);
    assert_eq!(
        run.data_crossings, 7,
        "each of guest-control's seven addis gains a load"
    );
    assert_eq!(run.census_pinned, 0);
}

#[test]
fn the_json_round_trips_through_the_crate_reader() {
    let run = run_guest("guest-control", "jalr-odd-bit").unwrap();
    let text = to_json(&run);
    let parsed = json::parse(&text).unwrap_or_else(|e| panic!("own JSON must parse: {e}"));
    let obj = match &parsed {
        Json::Obj(fields) => fields,
        other => panic!("expected an object, got {other:?}"),
    };
    let get = |name: &str| {
        obj.iter()
            .find(|(key, _)| key == name)
            .map(|(_, value)| value)
            .unwrap_or_else(|| panic!("field {name}"))
    };
    assert_eq!(get("guest"), &Json::Str("guest-control".to_string()));
    assert_eq!(get("expectations_met"), &Json::Bool(false));
    assert_eq!(get("census_met"), &Json::Bool(true));
    let div = match get("divergence") {
        Json::Obj(fields) => fields,
        other => panic!("divergence object: {other:?}"),
    };
    assert!(div.iter().any(|(k, v)| k == "at" && *v == Json::Int(10)));
    let trace = match get("trace") {
        Json::Arr(items) => items,
        other => panic!("trace array: {other:?}"),
    };
    assert_eq!(
        trace.len(),
        11,
        "the odd-bit mutant stops at the step-10 trap"
    );
}

#[test]
fn unknown_names_are_named_errors() {
    assert!(run_guest("nope", "none")
        .unwrap_err()
        .contains("unknown guest"));
    assert!(run_guest("smoke-arith", "nope")
        .unwrap_err()
        .contains("unknown mutation"));
}
