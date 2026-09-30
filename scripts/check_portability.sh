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
#   miri         `cargo +nightly miri test -p semulith-core` — the model's safe-Rust core
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
#   --self-test   the verdict logic's RED/GREEN controls over synthetic leg outcomes
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

verdict() {  # $1..$4 = native, x86_64, miri, cross_endian outcomes: green|red|absent
  local failed=() missing=()
  for leg in "$@"; do
    case "$leg" in
      green) : ;;
      red) failed+=("x");;
      absent) missing+=("x");;
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
  printf 'PORTABILITY --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

if [ "${1:-}" = "--self-test" ]; then self_test; exit $?; fi

NATIVE=red; X86=absent; MIRI=absent; CROSS=absent

echo "== leg 1: native ($(uname -m)) =="
# capture-then-read, never pipe into grep -q: grep -q's early exit SIGPIPEs cargo, and
# pipefail would report the PIPE's death as the leg's verdict (measured 2026-09-30).
mkdir -p "$ROOT/target/portability"
NLOG="$ROOT/target/portability/native.log"; cargo test --all >"$NLOG" 2>&1; NRC=$?
if [ "$NRC" -eq 0 ] && ! grep -qE "[1-9][0-9]* failed" "$NLOG"; then NATIVE=green; fi
echo "native: $NATIVE"
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

echo "== leg 2: x86-64 (mandatory) =="
if [ "$(uname -m)" = "x86_64" ]; then
  X86=red; cargo test --all >/dev/null 2>&1 && X86=green
elif [ "$(uname -m)" = "arm64" ] && [ "$(uname -s)" = "Darwin" ]; then
  if arch -x86_64 /usr/bin/true 2>/dev/null; then X86="absent (Rosetta present but the leg needs a full run — provision it)"; else X86="absent (Rosetta absent — measured 2026-09-30: Bad CPU type in executable)"; fi
fi
echo "x86-64: $X86"

echo "== leg 3: Miri (the pinned safe-Rust core plan) =="
if cargo +nightly miri --version >/dev/null 2>&1; then
  MIRI=red
  MLOG="$ROOT/target/portability/miri.log"; cargo +nightly miri test -p semulith-core >"$MLOG" 2>&1; MRC=$?
  if [ "$MRC" -eq 0 ] && ! grep -qE "[1-9][0-9]* failed" "$MLOG"; then MIRI=green; fi
fi
echo "miri: $MIRI"

echo "== leg 4: cross-endian (Miri on big-endian powerpc64) =="
if rustup target list --toolchain nightly-aarch64-apple-darwin --installed 2>/dev/null | grep -q "^powerpc64-unknown-linux-gnu$"; then
  CROSS=red
  CLOG="$ROOT/target/portability/cross.log"; cargo +nightly miri test -p semulith-core --target powerpc64-unknown-linux-gnu >"$CLOG" 2>&1; CRC=$?
  if [ "$CRC" -eq 0 ] && ! grep -qE "[1-9][0-9]* failed" "$CLOG"; then CROSS=green; fi
else
  CROSS="absent (rustup target add --toolchain nightly powerpc64-unknown-linux-gnu)"
fi
echo "cross-endian: $CROSS"

N=$NATIVE; X=$X86; M=$MIRI; C=$CROSS
[ "$N" = green ] || N=red
case "$X" in green|red) :;; *) X=absent;; esac
[ "$M" = green ] || [ "$M" = red ] || M=absent
[ "$C" = green ] || [ "$C" = red ] || C=absent
V="$(verdict "$N" "$X" "$M" "$C")"
echo "portability: $V (native=$N, x86-64=$X, miri=$M, cross-endian=$C)"
[ "$V" != "failed" ]
