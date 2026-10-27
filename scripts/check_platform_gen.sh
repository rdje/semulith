#!/usr/bin/env bash
# scripts/check_platform_gen.sh — shim (XTASK.6 slice 6w): the PLATFORM-GEN doctrine's driver is now
# `cargo xtask check-platform-gen [--self-test]` (xtask/src/check_platform_gen.rs). A board's platform capability
# manifest is GENERATED from its canonical inputs by scripts/gen_platform.py; the check regenerates it through the
# generator, spawned as this driver spawned it (not ported), and refuses the day the committed manifest stops
# byte-matching or an input is refused by name; the controls run over scratch copies of the real board. The same verdict
# lines and exit statuses (0 ok, 1 out of sync, 2 refused). Kept because the project doctrine slot registers this path;
# a unit test holds it to this one command, and the DERIVED-COUNTS arm total counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-platform-gen "$@"
