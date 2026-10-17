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
        let parent = root.join("target/cli-snapshot-tests");
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
fn elf(image: &[u8], entry: u64) -> Vec<u8> {
    let mut bytes = vec![0; 120];
    bytes[..7].copy_from_slice(b"\x7fELF\x02\x01\x01");
    for (offset, value) in [(16, 2u16), (18, 243), (52, 64), (54, 56), (56, 1)] {
        bytes[offset..offset + 2].copy_from_slice(&value.to_le_bytes());
    }
    bytes[20..24].copy_from_slice(&1u32.to_le_bytes());
    for (offset, value) in [
        (24, entry),
        (32, 64),
        (72, 120),
        (80, entry),
        (88, entry),
        (96, image.len() as u64),
        (104, image.len() as u64),
        (112, 2),
    ] {
        bytes[offset..offset + 8].copy_from_slice(&value.to_le_bytes());
    }
    bytes[64..68].copy_from_slice(&1u32.to_le_bytes());
    bytes[68..72].copy_from_slice(&7u32.to_le_bytes());
    bytes.extend_from_slice(image);
    bytes
}

#[test]
fn real_cli_gc_snapshot_resume_matches_run_and_refuses_corruption() {
    let work = Workspace::new();
    for name in ["a-lrsc-pair", "w-timer", "sv39-tlb-fence", "fp-fcsr-view"] {
        let guest = semulith_verify::run_rv64gc::guest(name);
        let program = work.0.join("guest.elf");
        std::fs::write(&program, elf(guest.image, guest.entry)).unwrap();
        let steps = format!("--steps={}", guest.executed_steps);
        let base = format!("--base={}", guest.entry);
        let at = guest.executed_steps / 2;
        let split = format!("--at={at}");
        let whole = cli(&[
            "run",
            program.to_str().unwrap(),
            "--profile=rv64gc-lab-v0",
            &steps,
            &base,
            "--size=65536",
        ]);
        assert!(
            whole.status.success(),
            "{}",
            String::from_utf8_lossy(&whole.stderr)
        );
        let capture = cli(&[
            "snapshot",
            program.to_str().unwrap(),
            "--profile=rv64gc-lab-v0",
            &steps,
            &split,
            &base,
            "--size=65536",
        ]);
        assert!(
            capture.status.success(),
            "{}",
            String::from_utf8_lossy(&capture.stderr)
        );
        let record = work.0.join("snapshot.json");
        std::fs::write(&record, &capture.stdout).unwrap();
        let resumed = cli(&[
            "resume",
            record.to_str().unwrap(),
            "--profile=rv64gc-lab-v0",
        ]);
        assert!(
            resumed.status.success(),
            "{}",
            String::from_utf8_lossy(&resumed.stderr)
        );
        let whole = String::from_utf8(whole.stdout).unwrap();
        let start = whole.find(&format!("[{at}] ")).unwrap();
        assert_eq!(
            String::from_utf8(resumed.stdout).unwrap(),
            whole[start..],
            "{name}"
        );
        let text = String::from_utf8(capture.stdout).unwrap();
        std::fs::write(
            &record,
            text.replacen("\"runtime_sha256\":\"", "\"runtime_sha256\":\"changed-", 1),
        )
        .unwrap();
        let refused = cli(&[
            "resume",
            record.to_str().unwrap(),
            "--profile=rv64gc-lab-v0",
        ]);
        assert_eq!(refused.status.code(), Some(2));
        assert!(refused.stdout.is_empty());
        assert!(String::from_utf8_lossy(&refused.stderr).contains("identity mismatch"));
        let refused = cli(&[
            "snapshot",
            program.to_str().unwrap(),
            "--profile=rv64gc-lab-v0",
            &split,
            "--size=67108865",
        ]);
        assert_eq!(refused.status.code(), Some(2));
        assert!(refused.stdout.is_empty());
    }
    // C.NOP / C.ADDI x1,1 / C.J self at an independently encoded halfword entry.
    let program = work.0.join("compressed.elf");
    std::fs::write(
        &program,
        elf(&[0x01, 0x00, 0x85, 0x00, 0x01, 0xa0], 0x8000_0002),
    )
    .unwrap();
    let capture = cli(&[
        "snapshot",
        program.to_str().unwrap(),
        "--profile=rv64gc-lab-v0",
        "--at=1",
        "--steps=4",
        "--size=65536",
    ]);
    assert!(
        capture.status.success(),
        "{}",
        String::from_utf8_lossy(&capture.stderr)
    );
    let record = work.0.join("compressed.json");
    std::fs::write(&record, capture.stdout).unwrap();
    let resumed = cli(&[
        "resume",
        record.to_str().unwrap(),
        "--profile=rv64gc-lab-v0",
    ]);
    assert!(
        resumed.status.success(),
        "{}",
        String::from_utf8_lossy(&resumed.stderr)
    );
    let text = String::from_utf8(resumed.stdout).unwrap();
    assert!(text.contains("[1] [M]: 0x0000000080000004\nx1 <- 0x0000000000000001"));
    // Reject oversized ELF input before handing its contents to the ELF parser.
    let oversized = work.0.join("oversized.elf");
    std::fs::File::create(&oversized)
        .unwrap()
        .set_len(65 * 1024 * 1024 + 1)
        .unwrap();
    let refused = cli(&[
        "snapshot",
        oversized.to_str().unwrap(),
        "--profile=rv64gc-lab-v0",
        "--at=0",
        "--steps=1",
        "--size=65536",
    ]);
    assert_eq!(refused.status.code(), Some(2));
    assert!(refused.stdout.is_empty());
    assert!(String::from_utf8_lossy(&refused.stderr).contains("ELF exceeds 65 MiB"));
}
