//! The real binary reads what its usage says (`P4-SYSTEM.14` a50-c1): `--name VALUE` and
//! `--name=VALUE` are one request, and a value option with no value is refused by name.

use std::path::PathBuf;
use std::process::{Command, Output};

fn root() -> PathBuf {
    let executable = std::env::current_exe().unwrap();
    executable
        .ancestors()
        .find(|p| p.join("Cargo.toml").is_file() && p.join("crates/semulith-cli").is_dir())
        .expect("test executable stays in this repository")
        .to_path_buf()
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

#[test]
fn run_reads_both_spellings_the_same() {
    let elf = root().join("evidence/rv64gc-svade-v1/guest.elf");
    let elf = elf.to_str().unwrap();
    let spaced = cli(&["run", elf, "--profile", "rv64gc-lab-v0", "--steps", "3"]);
    let joined = cli(&["run", elf, "--profile=rv64gc-lab-v0", "--steps=3"]);
    assert!(
        joined.status.success(),
        "{}",
        String::from_utf8_lossy(&joined.stderr)
    );
    assert!(!joined.stdout.is_empty());
    assert_eq!(spaced.stdout, joined.stdout);
    assert_eq!(spaced.status.code(), joined.status.code());
}

#[test]
fn bundle_reads_both_spellings_the_same() {
    let spaced = cli(&[
        "bundle",
        "--guest",
        "a-lrsc-pair",
        "--mutate",
        "none",
        "--profile",
        "rv64gc-lab-v0",
    ]);
    let joined = cli(&[
        "bundle",
        "--guest=a-lrsc-pair",
        "--mutate=none",
        "--profile=rv64gc-lab-v0",
    ]);
    assert!(
        joined.status.success(),
        "{}",
        String::from_utf8_lossy(&joined.stderr)
    );
    assert_eq!(spaced.stdout, joined.stdout);
}

#[test]
fn a_value_option_with_no_value_is_a_usage_refusal_by_name() {
    let done = cli(&["bundle", "--guest"]);
    assert_eq!(done.status.code(), Some(2));
    assert!(String::from_utf8_lossy(&done.stderr).starts_with("--guest needs a value\n"));
}

#[test]
fn an_unknown_option_stays_its_commands_refusal() {
    let done = cli(&["run", "x.elf", "--nope"]);
    assert_eq!(done.status.code(), Some(2));
    assert!(String::from_utf8_lossy(&done.stderr).starts_with("run: unknown option --nope\n"));
}

#[test]
fn trace_walks_prints_each_page_table_read_on_its_own_line() {
    let elf = root().join("evidence/rv64gc-svade-v1/guest.elf");
    let elf = elf.to_str().unwrap();
    let plain = cli(&["run", elf, "--profile", "rv64gc-lab-v0", "--steps", "137"]);
    let walks = cli(&[
        "run",
        elf,
        "--profile",
        "rv64gc-lab-v0",
        "--steps",
        "137",
        "--trace-walks",
    ]);
    assert!(walks.status.success());
    let plain = String::from_utf8_lossy(&plain.stdout);
    let walks = String::from_utf8_lossy(&walks.stdout);
    assert!(!plain.contains("ptw["));
    assert!(walks
        .lines()
        .any(|l| l.starts_with("ptw[0x") && l.contains("] -> 0x")));
    assert!(walks.starts_with(plain.as_ref()));
}
