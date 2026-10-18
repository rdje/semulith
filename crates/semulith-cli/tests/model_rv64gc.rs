use std::process::{Command, Output};

fn cli(args: &[&str]) -> Output {
    let executable = std::env::current_exe().unwrap();
    let binary = executable
        .parent()
        .unwrap()
        .parent()
        .unwrap()
        .join(format!("semulith{}", std::env::consts::EXE_SUFFIX));
    Command::new(binary).args(args).output().unwrap()
}

#[test]
fn gc_demo_detects_named_faults_and_refuses_unsupported_json() {
    let production = cli(&["demo", "--profile=rv64gc-lab-v0", "--guest=guest-control"]);
    assert!(production.status.success());
    for (mutation, at) in [("zext-addi", 1), ("jal-no-link", 7)] {
        let wrong = cli(&[
            "demo",
            "--profile=rv64gc-lab-v0",
            "--guest=guest-control",
            &format!("--mutate={mutation}"),
        ]);
        assert_eq!(wrong.status.code(), Some(1));
        let text = String::from_utf8(wrong.stdout).unwrap();
        assert!(text.contains(&format!("model: mutant:{mutation}")));
        assert!(text.contains(&format!("first difference at boundary {at}")));
        assert!(text.contains("expectations NOT met"));
        assert!(text.contains("production:"));
    }
    let unknown = cli(&[
        "demo",
        "--profile=rv64gc-lab-v0",
        "--guest=guest-control",
        "--mutate=phantom-load",
    ]);
    assert_eq!(unknown.status.code(), Some(2));
    assert!(String::from_utf8_lossy(&unknown.stderr).contains("unknown RV64GC mutation"));
    let unsupported = cli(&[
        "demo",
        "--profile=rv64gc-lab-v0",
        "--guest=guest-control",
        "--json",
    ]);
    assert_eq!(unsupported.status.code(), Some(2));
    assert!(unsupported.stdout.is_empty());
    assert!(String::from_utf8_lossy(&unsupported.stderr)
        .contains("structured RV64GC demo report is not implemented"));
    let scalar = cli(&[
        "demo",
        &format!("--guest={}", semulith_verify::guests::GUESTS[0].name),
        "--json",
    ]);
    assert!(scalar.status.success());
    assert!(
        semulith_verify::json::parse(&String::from_utf8(scalar.stdout).unwrap())
            .unwrap()
            .as_obj()
            .is_some()
    );
}
