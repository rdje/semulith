use std::path::PathBuf;
use std::process::{Command, Output};

struct Workspace(PathBuf);
impl Workspace {
    fn new() -> Self {
        let executable = std::env::current_exe().unwrap();
        let root = executable
            .ancestors()
            .find(|p| p.join("Cargo.toml").is_file() && p.join("crates/semulith-cli").is_dir())
            .expect("test executable stays in this repository");
        let parent = root.join("target/cli-replay-tests");
        std::fs::create_dir_all(&parent).unwrap();
        let path = parent.join(format!("run-{}", std::process::id()));
        std::fs::create_dir(&path).unwrap();
        Self(path)
    }
}
impl Drop for Workspace {
    fn drop(&mut self) {
        std::fs::remove_dir_all(&self.0).unwrap();
    }
}
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
fn changed_field(text: &str, key: &str) -> String {
    let doc = semulith_verify::json::parse(text).unwrap();
    let old = doc.get(key).unwrap().as_str().unwrap();
    text.replacen(
        &format!("\"{key}\":\"{old}\""),
        &format!("\"{key}\":\"{}\"", "0".repeat(64)),
        1,
    )
}

#[test]
fn real_cli_gc_bundles_replay_and_distinguish_mismatch_refusal_and_usage() {
    let work = Workspace::new();
    let file = work.0.join("bundle.json");
    let path = file.to_str().unwrap();
    for name in ["a-lrsc-pair", "w-timer", "sv39-tlb-fence", "fp-fcsr-view"] {
        let recorded = cli(&[
            "bundle",
            "--profile=rv64gc-lab-v0",
            &format!("--guest={name}"),
            "--mutate=none",
        ]);
        assert!(
            recorded.status.success(),
            "{}",
            String::from_utf8_lossy(&recorded.stderr)
        );
        let text = String::from_utf8(recorded.stdout).unwrap();
        std::fs::write(&file, &text).unwrap();
        let replay = cli(&["replay", path, "--profile=rv64gc-lab-v0"]);
        assert!(
            replay.status.success(),
            "{}",
            String::from_utf8_lossy(&replay.stderr)
        );
        assert!(String::from_utf8_lossy(&replay.stdout).contains("replay: identical"));
        for (key, expected) in [
            ("producer_sha256", "producer identity"),
            ("final_sha256", "final CPU/environment receipt"),
        ] {
            std::fs::write(&file, changed_field(&text, key)).unwrap();
            let refused = cli(&["replay", path, "--profile=rv64gc-lab-v0"]);
            assert_eq!(refused.status.code(), Some(1));
            assert!(String::from_utf8_lossy(&refused.stdout).contains(expected));
        }
        let (input, trace) = text.split_once("\"recorded\":").unwrap();
        let doc = semulith_verify::json::parse(&text).unwrap();
        let pc = doc
            .get("recorded")
            .unwrap()
            .get("steps")
            .unwrap()
            .as_arr()
            .unwrap()[0]
            .get("pc")
            .unwrap()
            .as_str()
            .unwrap();
        let altered = trace.replacen(
            &format!("\"pc\":\"{pc}\""),
            "\"pc\":\"0x0000000000000000\"",
            1,
        );
        std::fs::write(&file, format!("{input}\"recorded\":{altered}")).unwrap();
        let mismatch = cli(&["replay", path, "--profile=rv64gc-lab-v0"]);
        assert_eq!(mismatch.status.code(), Some(1));
        assert!(String::from_utf8_lossy(&mismatch.stdout).contains("MISMATCH at boundary 0: PC"));
        std::fs::write(&file, "{}").unwrap();
        let malformed = cli(&["replay", path, "--profile=rv64gc-lab-v0"]);
        assert_eq!(malformed.status.code(), Some(2));
        assert!(String::from_utf8_lossy(&malformed.stderr).contains("format"));
    }
    for args in [
        vec!["bundle", "--profile=rv64gc-lab-v0"],
        vec!["bundle", "--profile=rv64gc-lab-v0", "--guest=unknown"],
        vec![
            "bundle",
            "--profile=rv64gc-lab-v0",
            "--guest=a-lrsc-pair",
            "--mutate=wrong-model",
        ],
    ] {
        assert_eq!(cli(&args).status.code(), Some(2));
    }
    // The existing scalar bundle/replay path still works in the same binary.
    let scalar = cli(&[
        "bundle",
        &format!("--guest={}", semulith_verify::guests::GUESTS[0].name),
    ]);
    assert!(scalar.status.success());
    std::fs::write(&file, scalar.stdout).unwrap();
    assert!(cli(&["replay", path]).status.success());
}
