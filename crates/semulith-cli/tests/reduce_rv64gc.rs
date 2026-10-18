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
fn real_cli_reduces_and_replays_both_gc_controls_and_budget_limited_records() {
    let executable = std::env::current_exe().unwrap();
    let root = executable
        .ancestors()
        .find(|p| p.join("Cargo.toml").is_file() && p.join("crates/semulith-cli").is_dir())
        .unwrap();
    let parent = root.join("target/cli-reduction-tests");
    std::fs::create_dir_all(&parent).unwrap();
    let work = parent.join(format!("run-{}", std::process::id()));
    std::fs::create_dir(&work).unwrap();
    let path = work.join("reduction.json");
    for (mutation, at) in [("zext-addi", 1), ("jal-no-link", 7)] {
        for limit in ["512", "2"] {
            let out = cli(&[
                "reduce",
                "--profile=rv64gc-lab-v0",
                "--guest=guest-control",
                &format!("--mutate={mutation}"),
                &format!("--evaluations={limit}"),
            ]);
            assert!(
                out.status.success(),
                "{}",
                String::from_utf8_lossy(&out.stderr)
            );
            let text = String::from_utf8(out.stdout).unwrap();
            let reduction = semulith_verify::reduce_rv64gc::Reproducer::parse(&text).unwrap();
            assert_eq!(reduction.replay().unwrap().at, at);
            let message = String::from_utf8_lossy(&out.stderr);
            assert!(message.contains(if limit == "2" {
                "budget-limited"
            } else {
                "1-minimal"
            }));
            std::fs::write(&path, &text).unwrap();
            let replay = cli(&["replay", path.to_str().unwrap(), "--profile=rv64gc-lab-v0"]);
            assert!(
                replay.status.success(),
                "{}",
                String::from_utf8_lossy(&replay.stderr)
            );
            assert!(String::from_utf8_lossy(&replay.stdout)
                .contains(&format!("retained at boundary {at}")));
            let changed = text.replacen("\"reducer_sha256\":\"", "\"reducer_sha256\":\"z", 1);
            std::fs::write(&path, changed).unwrap();
            assert_eq!(
                cli(&["replay", path.to_str().unwrap(), "--profile=rv64gc-lab-v0"])
                    .status
                    .code(),
                Some(2)
            );
            let start = text.find("\"reducer_sha256\":\"").unwrap() + "\"reducer_sha256\":\"".len();
            let mut changed = text;
            changed.replace_range(start..start + 64, &"0".repeat(64));
            std::fs::write(&path, changed).unwrap();
            let refused = cli(&["replay", path.to_str().unwrap(), "--profile=rv64gc-lab-v0"]);
            assert_eq!(refused.status.code(), Some(1));
            assert!(String::from_utf8_lossy(&refused.stdout).contains("reducer identity mismatch"));
        }
    }
    for (mutation, expected) in [("none", 1), ("unknown", 2)] {
        let out = cli(&[
            "reduce",
            "--profile=rv64gc-lab-v0",
            "--guest=guest-control",
            &format!("--mutate={mutation}"),
        ]);
        assert_eq!(out.status.code(), Some(expected));
        assert!(out.stdout.is_empty());
    }
    let no_trigger = cli(&[
        "reduce",
        "--profile=rv64gc-lab-v0",
        "--guest=c-hints",
        "--mutate=jal-no-link",
    ]);
    assert_eq!(no_trigger.status.code(), Some(1));
    assert!(String::from_utf8_lossy(&no_trigger.stderr).contains("no paired step difference"));
    for args in [
        vec!["reduce", "--profile=rv64gc-lab-v0"],
        vec!["reduce", "--profile=rv64gc-lab-v0", "--guest=unknown"],
        vec![
            "reduce",
            "--profile=rv64gc-lab-v0",
            "--guest=guest-control",
            "--evaluations=1",
        ],
        vec![
            "reduce",
            "--profile=rv64gc-lab-v0",
            "--guest=guest-control",
            "--evaluations=513",
        ],
        vec![
            "reduce",
            "--profile=rv64gc-lab-v0",
            "--guest=guest-control",
            "--evaluations=oops",
        ],
    ] {
        assert_eq!(cli(&args).status.code(), Some(2));
    }
    // Scalar formatting and behaviour keep their existing contract.
    let scalar = cli(&["reduce", "--guest=guest-control", "--mutate=zext-addi"]);
    assert!(scalar.status.success());
    assert!(String::from_utf8_lossy(&scalar.stdout).contains("retained FIRST DIVERGENCE"));
    assert!(String::from_utf8_lossy(&scalar.stdout).contains("1-minimal in word-deletion domain"));
    std::fs::remove_dir_all(work).unwrap();
}
