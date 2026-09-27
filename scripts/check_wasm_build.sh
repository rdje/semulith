#!/usr/bin/env bash
# scripts/check_wasm_build.sh — PORT-WEB doctrine: the crate skeleton builds for the browser target.
#
# The director's portability decision (decision_browser-wasm-target, 2026-09-27) makes
# wasm32-unknown-unknown a first-class target from the first crate: host-native is a build
# mode, not the architecture. This check proves the workspace still builds for the Wasm
# target, so a host-only API cannot slip into the engine unnoticed — the build itself is
# the proof that no unconditional host-only capability exists (PORT-WEB.1).
#
# A check with arms: --self-test builds scratch crates — one sound lib, one host-only lib,
# one sound bin, one broken for an unrelated reason — and asserts the verdict AND the
# reason for each. A control never seen RED is not known to work (docs/CLAIM_VERIFICATION.md).
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"
TARGET="wasm32-unknown-unknown"

# Preflight: the target must be installed. Refuse with the fix, never fail silently or
# pass vacuously — a gate that cannot run is not a gate.
if ! rustup target list --installed 2>/dev/null | grep -qx "$TARGET"; then
  echo "PORT-WEB: REFUSED — rustup target '$TARGET' is not installed, this check cannot judge." >&2
  echo "  Install it with: rustup target add $TARGET" >&2
  exit 2
fi

# ── self-test ────────────────────────────────────────────────────────────────────────────────
SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }

mkcrate() { # $1 = dir, $2 = name, $3 = bin|lib, $4 = source content
  mkdir -p "$1/src"
  cat > "$1/Cargo.toml" <<EOF
[package]
name = "$2"
version = "0.1.0"
edition = "2021"

[workspace]
EOF
  # cargo's default target file is src/lib.rs for a lib, src/main.rs for a bin
  if [ "$3" = bin ]; then printf '%s\n' "$4" > "$1/src/main.rs"
  else printf '%s\n' "$4" > "$1/src/lib.rs"; fi
}

build_wasm() { # $1 = crate dir; echoes cargo output; rc = cargo's rc. --target-dir stays inside
               # the scratch dir: an env var or shared dir here would leak the self-test into
               # the real run (a measured defect in this family's history).
  ( cd "$1" && cargo build --offline --target "$TARGET" --target-dir "$1/.wt" 2>&1 )
}

self_test() {
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"

  # ⛔ STRICT ARITY (docs/knowledge/self-test-arms-that-never-ran.md): a missing `;` before
  # an arm call swallows it silently; the guard makes that a loud failure.
  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'PORT-WEB self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' \
      "$3" "$2" "$1" >&2
    return 1
  }
  arm() { # arm <name> <rc> <expected-rc> <output> <reason substring; "!x" asserts x is ABSENT>
    argc 5 "$#" arm || return
    local want="$5"
    if [ "${want:0:1}" = "!" ]; then
      if [ "$2" = "$3" ] && ! printf '%s' "$4" | grep -qF "${want:1}"; then
        pass=$((pass+1))
      else
        fail=$((fail+1))
        printf 'PORT-WEB self-test MISS: %s — expected rc=%s WITHOUT %q, got rc=%s\n%s\n' \
          "$1" "$3" "${want:1}" "$2" "$4" >&2
      fi
    elif [ "$2" = "$3" ] && { [ "$want" = "-" ] || printf '%s' "$4" | grep -qF "$want"; }; then
      pass=$((pass+1))
    else
      fail=$((fail+1))
      printf 'PORT-WEB self-test MISS: %s — expected rc=%s (reason: %s), got rc=%s\n%s\n' \
        "$1" "$3" "$want" "$2" "$4" >&2
    fi
  }

  mkcrate "$t/good" "probe-good" lib 'pub fn probe() -> u32 { 42 }'
  out="$(build_wasm "$t/good")"; rc=$?
  arm "GREEN a sound lib crate builds for wasm" "$rc" 0 "$out" "-"

  mkcrate "$t/hostonly" "probe-hostonly" lib 'use std::os::unix::ffi::OsStrExt as _; pub fn probe() -> u32 { 42 }'
  out="$(build_wasm "$t/hostonly")"; rc=$?
  arm "RED a host-only unix import breaks the wasm build, naming the reason" "$rc" 101 "$out" "unix"

  mkcrate "$t/bingood" "probe-bingood" bin 'fn main() { println!("ok"); }'
  out="$(build_wasm "$t/bingood")"; rc=$?
  arm "GREEN a sound bin crate builds for wasm" "$rc" 0 "$out" "-"

  mkcrate "$t/syntax" "probe-syntax" lib 'pub fn broken( {'
  out="$(build_wasm "$t/syntax")"; rc=$?
  arm "REFUSE a failure with an unrelated cause is not read as the host-only reason" "$rc" 101 "$out" "!unix"

  rm -rf "$t"
  printf 'PORT-WEB --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

if [ "${1:-}" = "--self-test" ]; then
  self_test
  exit $?
fi

# Re-run the controls before judging: a check that no longer discriminates must refuse,
# not pass (the project-doctrine contract in scripts/check_doctrines.project.sh).
self_test >/dev/null 2>&1 || {
  echo "PORT-WEB: REFUSED — the check does not discriminate (self-test failed)." >&2
  exit 2
}

out="$(cargo build --workspace --target "$TARGET" 2>&1)" || {
  printf 'PORT-WEB: FAIL — the workspace must build for %s (decision_browser-wasm-target):\n%s\n' "$TARGET" "$out" >&2
  exit 1
}
printf 'PORT-WEB: ok (workspace builds for %s)\n' "$TARGET"
exit 0
