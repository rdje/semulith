#!/usr/bin/env bash
# scripts/check_state_gen.sh — shim (XTASK.6 slice 6x): the STATE-GEN doctrine's driver is now
# `cargo xtask check-state-gen [--self-test]` (xtask/src/check_state_gen.rs). The architectural-state modules
# (crates/semulith-core/src/state.rs, state_rv64gc.rs) are GENERATED from the units' state descriptors by
# scripts/gen_state.py; the check regenerates each pair through the generator, spawned as this driver spawned it (not
# ported), and refuses the day a module stops byte-matching its descriptor or the generator refuses a descriptor by
# name; the controls run over scratch copies with the script's own rv64gc template. The same verdict lines and exit
# statuses (0 ok, 1 out of sync, 2 refused). Kept because the project doctrine slot registers this path; a unit test
# holds it to this one command, and the DERIVED-COUNTS arm total counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-state-gen "$@"
