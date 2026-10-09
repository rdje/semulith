#!/usr/bin/env bash
# build_c_guest.sh — compile a tracked .c guest into its ELF with the PINNED toolchain.
#
# Pinned by `decision_c-guest-routing-and-toolchain` (2026-09-30): a clang WITH a
# RISC-V backend (measured: Homebrew llvm@21 clang 21.1.8 — Apple clang has none) plus
# an ld.lld (measured: zig 0.16.0's bundled lld, Homebrew LLD 21.1.8). A toolchain that
# cannot target riscv64 is REFUSED BY NAME, never silently substituted; nothing is
# installed by this script.
#
# The ELF is a build artifact — untracked, on-volume under target/refs/guests/, with
# the same standing as the reference binaries: the live differential needs it, the
# commit gate does not.
#
# usage: scripts/build_c_guest.sh [guest-name]   (default: c-scope)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
exec python3 "$ROOT/scripts/build_c_guest.py" "$@"
