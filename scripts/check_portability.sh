#!/usr/bin/env bash
# scripts/check_portability.sh — the G-PORTABILITY instrument (P2-SCALAR.8).
#
# The release policy (docs/EVIDENCE_AND_GATES.md §7) makes BOTH native host architectures
# mandatory: the fixtures must agree on native x86-64 AND native AArch64, and the selected
# pure-Rust core passes its pinned Miri and cross-endian plan. Four legs:
#
#   native       this host: `cargo test --all` (the offline differential against the
#                pinned expectations) PLUS the digest manifest — every tracked guest's
#                `demo --json` output (trace + census verdicts) hashed; the manifest is
#                what the second host must reproduce BYTE-IDENTICALLY.
#   x86-64       the same native leg ON x86-64. This script probes: running ON x86-64
#                (uname), or Rosetta on arm64 macOS (`arch -x86_64`). Measured absent on
#                the recording host (2026-09-30: `Bad CPU type in executable`).
#   miri         the dated nightly's `miri test -p semulith-core` — the model's safe-Rust core
#                interpreted (UB detection). The one unsafe island (bench.rs's counting
#                allocator, RUST-03's instrument) is deliberately outside this scope.
#   cross-endian the same suites under Miri on powerpc64-unknown-linux-gnu (big-endian).
#
# ⛔ NOT A COMMIT GATE. It needs the nightly toolchain and measures the HOST — the same
# standing as fetch_references.sh. The recorded verdict lives in
# profiles/rv64i-lab-v0/portability.sexp.
#
# Verdict discipline (no "when available" clause): `passed` only if every leg RAN green;
# `incomplete` names each mandatory leg whose infrastructure is absent (absence is not a
# failure and not a pass); `failed` when a runnable leg fails.
#
#   --self-test       verdict controls plus cold single-leg public-interface controls
#   --print-toolchain print the one dated Miri toolchain CI must provision
#   --leg NAME        run one leg only (native | x86-64 | miri | cross-endian) — the CI
#                     matrix drives single legs per host job
#   --emit-manifest F  with the native leg, write the digest manifest to F (the CI
#                     artifact; the agreement job byte-compares both hosts' files)
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"
NIGHTLY=nightly-2026-09-13

[ "${1:-}" = "--print-toolchain" ] && { echo "$NIGHTLY"; exit 0; }

verdict() {  # $1..$4 = native, x86_64, miri, cross_endian outcomes: green|red|absent
  local failed=() missing=()
  for leg in "$@"; do
    case "$leg" in
      green*) : ;;
      red*) failed+=("x");;
      absent*) missing+=("x");;
      *) failed+=("x");;
    esac
  done
  if [ "${#failed[@]}" -gt 0 ]; then echo "failed"; return 1
  elif [ "${#missing[@]}" -gt 0 ]; then echo "incomplete"; return 0
  else echo "passed"; return 0; fi
}

self_test() {
  local pass=0 fail=0
  arm() { local got; got="$(verdict "$1" "$2" "$3" "$4")"; if [ "$got" = "$5" ]; then pass=$((pass+1)); else fail=$((fail+1)); printf 'PORTABILITY self-test MISS: %s -> %s, want %s\n' "$6" "$got" "$5" >&2; fi; }
  arm green green green green passed "all four legs green"
  arm green absent green green incomplete "a mandatory leg absent"
  arm red green green green failed "a runnable leg failed"
  arm green absent absent green incomplete "two legs absent is still incomplete, not failed"
  arm red absent green green failed "a failure outranks an absence"
  arm green red absent green failed "failure anywhere is failed"
  arm green "red (manifest mismatch)" green green failed "a decorated failure is still a failure"
  arm green "green (translation)" green green passed "a decorated green is still green"
  arm green unknown green green failed "an unknown outcome cannot pass"
  printf 'PORTABILITY --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ] || return 1
  python3 "$ROOT/scripts/probe_portability.py"
}

if [ "${1:-}" = "--self-test" ]; then self_test; exit $?; fi

ONLY_LEG=""; EMIT=""
while [ $# -gt 0 ]; do
  case "$1" in
    --leg) ONLY_LEG="$2"; shift 2;;
    --emit-manifest) EMIT="$2"; shift 2;;
    *) echo "check_portability: unknown option $1" >&2; exit 2;;
  esac
done
run_leg() { [ -z "$ONLY_LEG" ] || [ "$ONLY_LEG" = "$1" ]; }

# Every single-leg job starts cold; no leg may depend on native having run first.
export CARGO_HOME="$ROOT/.app-data/cargo-home"
export TMPDIR="$ROOT/target/portability/tmp"
mkdir -p "$ROOT/target/portability" "$CARGO_HOME" "$TMPDIR"

run_miri() { # log, sysroot name, then optional --target arguments
  local log="$1" scope="$2" tool_sysroot; shift 2
  export MIRI_SYSROOT="$ROOT/target/portability/sysroots/$NIGHTLY/$scope"
  # Setup's temporary package inherits this repository's strict source replacement.
  # Synchronize both locked workspaces through Cargo's public vendor interface.
  tool_sysroot="$(rustup run "$NIGHTLY" rustc --print sysroot)" || return 1
  cargo "+$NIGHTLY" vendor --locked --sync \
    "$tool_sysroot/lib/rustlib/src/rust/library/Cargo.toml" .app-data/vendor >"$log" 2>&1 || return 1
  # The public setup interface builds directly at MIRI_SYSROOT. Tests then reuse it,
  # avoiding the shared OS cache and keeping native/big-endian sysroots distinct.
  cargo "+$NIGHTLY" miri setup "$@" >>"$log" 2>&1 &&
    cargo "+$NIGHTLY" miri test -p semulith-core "$@" >>"$log" 2>&1
}

NATIVE=red; X86=absent; MIRI=absent; CROSS=absent

# The digest manifest over every tracked guest's `demo --json` output — the byte-exact
# cross-host contract (P2-SCALAR.8). $1 = a cargo target triple (empty = the host).
manifest_digest() {
python3 - "$1" <<'PY'
import hashlib, subprocess, sys, pathlib, re
target = sys.argv[1]
src = pathlib.Path("crates/semulith-verify/src/guests.rs").read_text()
names = sorted(set(re.findall(r'name: "([a-z0-9-]+)"', src)))
h = hashlib.sha256()
cmd = ["cargo", "run", "-q"] + (["--target", target] if target else []) + \
      ["-p", "semulith-cli", "--", "demo"]
for n in names:
    out = subprocess.run(cmd + [f"--guest={n}", "--json"], capture_output=True,
                         check=True).stdout
    h.update(hashlib.sha256(out).hexdigest().encode())
print(h.hexdigest())
PY
}

if run_leg native; then
echo "== leg 1: native ($(uname -m)) =="
# capture-then-read, never pipe into grep -q: grep -q's early exit SIGPIPEs cargo, and
# pipefail would report the PIPE's death as the leg's verdict (measured 2026-09-30).
NLOG="$ROOT/target/portability/native.log"; cargo test --all >"$NLOG" 2>&1; NRC=$?
if [ "$NRC" -eq 0 ] && ! grep -qE "[1-9][0-9]* failed" "$NLOG"; then NATIVE=green; fi
echo "native: $NATIVE"
[ "$NATIVE" != red ] || tail -n 40 "$NLOG" >&2
echo "  the digest manifest (the second host must reproduce it byte-identically):"
python3 - "$ROOT" <<'PY'
import hashlib, subprocess, sys
sys.path.insert(0, "scripts")
root = sys.argv[1]
names = []
import pathlib, re
# the guest list from the generated fixture's own registry — never a second list
src = pathlib.Path("crates/semulith-verify/src/guests.rs").read_text()
names = re.findall(r'name: "([a-z0-9-]+)"', src)
names = sorted(set(names))
h = hashlib.sha256()
for n in names:
    out = subprocess.run(["cargo", "run", "-q", "-p", "semulith-cli", "--", "demo",
                          f"--guest={n}", "--json"], capture_output=True,
                         check=True).stdout
    d = hashlib.sha256(out).hexdigest()
    h.update(d.encode())
    print(f"  {d[:16]}  {n}")
print(f"  manifest sha256: {h.hexdigest()}  ({len(names)} guests)")
PY
if [ -n "$EMIT" ]; then
  NLOG="$ROOT/target/portability/native.log"
  python3 - "$EMIT" <<'PY'
import hashlib, subprocess, sys, pathlib, re
src = pathlib.Path("crates/semulith-verify/src/guests.rs").read_text()
names = sorted(set(re.findall(r'name: "([a-z0-9-]+)"', src)))
h = hashlib.sha256()
lines = []
for n in names:
    out = subprocess.run(["cargo", "run", "-q", "-p", "semulith-cli", "--", "demo",
                          f"--guest={n}", "--json"], capture_output=True,
                         check=True).stdout
    d = hashlib.sha256(out).hexdigest()
    h.update(d.encode())
    lines.append(f"{d}  {n}")
lines.append(f"manifest sha256: {h.hexdigest()}  ({len(names)} guests)")
pathlib.Path(sys.argv[1]).write_text("\n".join(lines) + "\n")
print(f"  manifest written to {sys.argv[1]}")
PY
fi
fi

if run_leg x86-64; then
echo "== leg 2: x86-64 (mandatory) =="
if [ "$(uname -m)" = "x86_64" ]; then
  X86=red; cargo test --all >/dev/null 2>&1 && X86=green
elif [ "$(uname -m)" = "arm64" ] && [ "$(uname -s)" = "Darwin" ]; then
  if arch -x86_64 /usr/bin/true 2>/dev/null; then
    # The Rosetta bridge (decision_release-route-x86-64-leg): cross-compile the fixtures
    # for x86_64-apple-darwin and run them under translation; the agreement half is the
    # digest manifest, which must equal the recorded aarch64 one byte-for-byte.
    if rustup target list --installed 2>/dev/null | grep -q '^x86_64-apple-darwin$'; then
      X86=red
      XLOG="$ROOT/target/portability/x86-64.log"
      cargo test --all --target x86_64-apple-darwin >"$XLOG" 2>&1; XRC=$?
      if [ "$XRC" -eq 0 ] && ! grep -qE "[1-9][0-9]* failed" "$XLOG"; then
        if XDG="$(manifest_digest x86_64-apple-darwin)" && NATIVE_DIGEST="$(manifest_digest "")"; then
          if [ "$XDG" = "$NATIVE_DIGEST" ]; then X86="green (Rosetta translation; the manifest agrees byte-identically)"
          else X86="red (x86-64 manifest $XDG != the current native $NATIVE_DIGEST)"; fi
        else
          X86="red (fixture digest could not be produced)"
        fi
      fi
    else
      X86="absent (Rosetta live; provision the target: rustup target add x86_64-apple-darwin)"
    fi
  else
    X86="absent (Rosetta inert — measured 2026-09-30; activation: sudo softwareupdate --install-rosetta)"
  fi
fi
echo "x86-64: $X86"
fi

if run_leg miri; then
echo "== leg 3: Miri (the pinned safe-Rust core plan) =="
if cargo "+$NIGHTLY" miri --version >/dev/null 2>&1; then
  MIRI=red
  MLOG="$ROOT/target/portability/miri.log"; run_miri "$MLOG" native; MRC=$?
  if [ "$MRC" -eq 0 ] && ! grep -qE "[1-9][0-9]* failed" "$MLOG"; then MIRI=green; fi
  [ "$MIRI" != red ] || { [ ! -f "$MLOG" ] || tail -n 40 "$MLOG" >&2; }
fi
echo "miri: $MIRI"
fi

if run_leg cross-endian; then
echo "== leg 4: cross-endian (Miri on big-endian powerpc64) =="
if rustup target list --toolchain "$NIGHTLY" --installed 2>/dev/null | grep -q "^powerpc64-unknown-linux-gnu$"; then
  CROSS=red
  CLOG="$ROOT/target/portability/cross.log"; run_miri "$CLOG" powerpc64 --target powerpc64-unknown-linux-gnu; CRC=$?
  if [ "$CRC" -eq 0 ] && ! grep -qE "[1-9][0-9]* failed" "$CLOG"; then CROSS=green; fi
  [ "$CROSS" != red ] || { [ ! -f "$CLOG" ] || tail -n 40 "$CLOG" >&2; }
else
  CROSS="absent (rustup target add --toolchain $NIGHTLY powerpc64-unknown-linux-gnu)"
fi
echo "cross-endian: $CROSS"
fi

# A single-leg run reports that leg and exits with its own status; the four-leg verdict
# is the full-run form.
if [ -n "$ONLY_LEG" ]; then
  case "$ONLY_LEG" in
    native) [ "$NATIVE" = green ];;
    x86-64) case "$X86" in green*) true;; *) false;; esac;;
    miri) [ "$MIRI" = green ];;
    cross-endian) [ "$CROSS" = green ];;
    *) echo "check_portability: unknown leg $ONLY_LEG" >&2; exit 2;;
  esac
  exit $?
fi

N=$NATIVE; X=$X86; M=$MIRI; C=$CROSS
[ "$N" = green ] || N=red
case "$X" in green*|red*) :;; *) X=absent;; esac
[ "$M" = green ] || [ "$M" = red ] || M=absent
[ "$C" = green ] || [ "$C" = red ] || C=absent
V="$(verdict "$N" "$X" "$M" "$C")"
echo "portability: $V (native=$N, x86-64=$X, miri=$M, cross-endian=$C)"
[ "$V" != "failed" ]
