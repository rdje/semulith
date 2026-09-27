//! User commands and report presentation (`docs/ARCHITECTURE.md` §4): this
//! binary calls the core and verification APIs and never duplicates behaviour
//! they own.
//!
//! P1-LAB.1 stands up the wiring only — the dependency edges below are real
//! from day one, and the first command lands with the execution slice
//! (P1-LAB.8).

use semulith_core as _;
use semulith_verify as _;

fn main() {
    println!("semulith-cli — the laboratory control surface; no commands yet (P1-LAB.1 skeleton)");
}
