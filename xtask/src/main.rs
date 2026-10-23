//! `cargo xtask` — SEMULITH's automation front door (tree `XTASK`, leaf `XTASK.1`).
//!
//! The director's direction (`decision_rust-native-tooling.md`, 2026-10-23): move to cargo xtask
//! incrementally and with extreme care, never breaking anything. This first step moves nothing.
//! `cargo xtask <args>` runs `make <args>` from the repository root with the same environment,
//! the same standard streams and the same exit status, so every target keeps exactly one
//! definition — the Makefile — until a later leaf moves one, shim first. `cargo xtask` alone runs
//! `make help`.

use std::path::Path;
use std::process::{Command, ExitCode};

/// Runs `make` with the given arguments from the repository root and returns its exit status.
fn main() -> ExitCode {
    let mut args: Vec<String> = std::env::args().skip(1).collect();
    if args.is_empty() {
        args.push("help".to_owned());
    }
    // The repository root is this crate's parent directory, fixed at build time, so the front
    // door behaves the same from any working directory without `make -C` (which would add
    // "Entering directory" lines to the output).
    let root = Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap_or_else(|| Path::new("."));
    match Command::new("make").args(&args).current_dir(root).status() {
        Ok(status) => match status.code() {
            Some(code) => ExitCode::from(u8::try_from(code).unwrap_or(1)),
            None => ExitCode::from(1), // terminated by a signal: never report success
        },
        Err(error) => {
            eprintln!("xtask: cannot run make: {error}");
            ExitCode::from(127)
        }
    }
}
