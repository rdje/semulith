#!/usr/bin/env bash
# scripts/check_guest_gen.sh — shim (XTASK.6 slice 6aq): the GUEST-GEN doctrine's driver is now
# `cargo xtask check-guest-gen [--self-test]` (xtask/src/check_guest_gen.rs). The generated guest fixtures
# (`crates/semulith-verify/src/guests.rs`, `guests_rv64gc.rs`) must still be `scripts/gen_guests.py`'s output of the
# tracked guests and their expectations (DRIFT otherwise), and the rv64gc base mirror must hold under its governor
# (`scripts/check_gc_mirror.py`); generator, governor, the probe suites and the controls' inline edits are spawned as
# before (not ported); the quiet run keeps the controls' output in target/guest-gen/self-test.log as before. The same
# verdict lines and exit statuses (0 ok, 1 drift, 2 refused). Kept because the project doctrine slot registers this
# path; a unit test holds it to this one command, and the DERIVED-COUNTS arm total counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-guest-gen "$@"
