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
#   --profile UNIT    the unit whose guest fixture the manifest covers and whose record the
#                     messages name (default rv64i-lab-v0; P4-SYSTEM.17 slice a adds rv64gc-lab-v0,
#                     whose demo prints a byte-exact text trace — the manifest hashes that text)
#   --record          after a full four-leg run, write profiles/UNIT/portability.sexp from the
#                     measured legs (host facts, digests and verdicts read from the run)
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

ONLY_LEG=""; EMIT=""; UNIT="rv64i-lab-v0"; RECORD=0
while [ $# -gt 0 ]; do
  case "$1" in
    --leg) ONLY_LEG="$2"; shift 2;;
    --emit-manifest) EMIT="$2"; shift 2;;
    --profile) UNIT="$2"; shift 2;;
    --record) RECORD=1; shift;;
    *) echo "check_portability: unknown option $1" >&2; exit 2;;
  esac
done
run_leg() { [ -z "$ONLY_LEG" ] || [ "$ONLY_LEG" = "$1" ]; }
# The unit's guest fixture and demo spelling (P4-SYSTEM.17 slice a): rv64i's demo emits the
# structured --json report; rv64gc's refuses --json by design and prints a byte-exact text trace.
case "$UNIT" in
  rv64i-lab-v0)  GUESTS_RS="crates/semulith-verify/src/guests.rs";       DEMO_ARGS="--json";;
  rv64gc-lab-v0) GUESTS_RS="crates/semulith-verify/src/guests_rv64gc.rs"; DEMO_ARGS="--profile=rv64gc-lab-v0";;
  *) echo "check_portability: unknown unit $UNIT (rv64i-lab-v0 | rv64gc-lab-v0)" >&2; exit 2;;
esac
export GUESTS_RS DEMO_ARGS UNIT
[ "$RECORD" -eq 0 ] || [ -z "$ONLY_LEG" ] || { echo "check_portability: --record needs the full four-leg run" >&2; exit 2; }
[ "$RECORD" -eq 0 ] || [ -n "$EMIT" ] || EMIT="$ROOT/target/portability/native-manifest.txt"
# a recording run starts from clean logs: the record cites this run, never a previous one
[ "$RECORD" -eq 0 ] || rm -f "$ROOT/target/portability/native.log" "$ROOT/target/portability/x86-64.log" "$ROOT/target/portability/miri.log" "$ROOT/target/portability/cross.log" "$ROOT/target/portability/native-manifest.txt"

# Every single-leg job starts cold; no leg may depend on native having run first.
export CARGO_HOME="$ROOT/.app-data/cargo-home"
export TMPDIR="$ROOT/target/portability/tmp"
mkdir -p "$ROOT/target/portability" "$CARGO_HOME" "$TMPDIR"

run_miri() { # log, sysroot name, then optional --target arguments
  local log="$1" scope="$2" tool_sysroot; shift 2
  export MIRI_SYSROOT="$ROOT/target/portability/sysroots/$NIGHTLY/$scope"
  # The leg's own Cargo target directory, keyed by toolchain and scope: a `target/miri` left by an
  # earlier toolchain reported a dependency `Fresh` without a Miri-target rlib and the crate failed
  # with E0463 (measured 2026-10-27, P4-SYSTEM.17 slice a). A fresh directory per pin never does.
  export CARGO_TARGET_DIR="$ROOT/target/portability/miri-target/$NIGHTLY/$scope"
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
import os
src = pathlib.Path(os.environ["GUESTS_RS"]).read_text()
names = sorted(set(re.findall(r'name: "([a-z0-9-]+)"', src)))
h = hashlib.sha256()
cmd = ["cargo", "run", "-q"] + (["--target", target] if target else []) + \
      ["-p", "semulith-cli", "--", "demo"]
for n in names:
    out = subprocess.run(cmd + [f"--guest={n}", *os.environ["DEMO_ARGS"].split()], capture_output=True,
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
import os
src = pathlib.Path(os.environ["GUESTS_RS"]).read_text()
names = re.findall(r'name: "([a-z0-9-]+)"', src)
names = sorted(set(names))
h = hashlib.sha256()
for n in names:
    out = subprocess.run(["cargo", "run", "-q", "-p", "semulith-cli", "--", "demo",
                          f"--guest={n}", *os.environ["DEMO_ARGS"].split()], capture_output=True,
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
import os
src = pathlib.Path(os.environ["GUESTS_RS"]).read_text()
names = sorted(set(re.findall(r'name: "([a-z0-9-]+)"', src)))
h = hashlib.sha256()
lines = []
for n in names:
    out = subprocess.run(["cargo", "run", "-q", "-p", "semulith-cli", "--", "demo",
                          f"--guest={n}", *os.environ["DEMO_ARGS"].split()], capture_output=True,
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
      # Under translation a spawned /usr/bin/git runs the shim's x86_64 slice, which cannot load the
      # Command Line Tools' arm64-only libxcrun ("missing compatible architecture"; measured 2026-10-28,
      # P4-SYSTEM.17 slice b) — and the harness's corpus tests spawn git. Lead the tests' PATH with a link
      # to the real git, resolved natively here; an arm64 tool runs natively from a translated parent.
      # No xcrun, or no answer: no link, the PATH as it was.
      XPATH="$PATH"; XTOOLS="$ROOT/target/portability/rosetta-tools"
      if XGIT="$(xcrun --find git 2>/dev/null)" && [ -x "$XGIT" ] && mkdir -p "$XTOOLS" && ln -sfn "$XGIT" "$XTOOLS/git"; then
        XPATH="$XTOOLS:$PATH"
      fi
      PATH="$XPATH" cargo test --all --target x86_64-apple-darwin >"$XLOG" 2>&1; XRC=$?
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
if [ "$RECORD" -eq 1 ]; then
  # P4-SYSTEM.17 slice a: the record is written from THIS run's measured facts — host identities read
  # from the tools, suite counts and digests parsed from the legs' own logs — never typed.
  python3 - "$ROOT" "$UNIT" "$V" "$N" "$X" "$M" "$C" "$NIGHTLY" <<'PY'
import pathlib, re, subprocess, sys, datetime
root, unit, verdict, native, x86, miri, cross, nightly = sys.argv[1:9]
root = pathlib.Path(root); port = root / "target/portability"
def tool(*cmd):
    try: return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.strip().splitlines()[0]
    except Exception as e: return f"unavailable ({type(e).__name__})"
def suites(log):
    text = (port / log).read_text() if (port / log).is_file() else ""
    ok = sum(int(m) for m in re.findall(r"test result: ok\. (\d+) passed", text))
    failed = sum(int(m) for m in re.findall(r"test result: \w+\. \d+ passed; (\d+) failed", text))
    return ok, failed
manifest = (port / "native-manifest.txt").read_text() if (port / "native-manifest.txt").is_file() else ""
m = re.search(r"manifest sha256: ([0-9a-f]{64})\s+\((\d+) guests\)", manifest)
digest, guests = (m.group(1), m.group(2)) if m else ("unrecorded", "0")
xm = re.search(r"x86-64 manifest ([0-9a-f]{64})", x86)
def ran(v): return v.startswith("green") or v.startswith("red")
nok, nfail = suites("native.log") if ran(native) else (0, 0)
xok, xfail = suites("x86-64.log") if ran(x86) else (0, 0)
mok, mfail = suites("miri.log") if ran(miri) else (0, 0)
cok, cfail = suites("cross.log") if ran(cross) else (0, 0)
def ev(v, text): return text if ran(v) else f"not run on this host: {v}"
def q(s): return s.replace('\\', '\\\\').replace('"', '\\"')
arch = tool('uname', '-m')
xevidence = ("equals the native digest" if x86.startswith("green") else (xm.group(0) if xm else "not produced"))
doc = f""";; portability.sexp — the recorded G-PORTABILITY evidence of {unit} (P4-SYSTEM.17 slice a): one
;; measurement session on one named host, frozen as data by `scripts/check_portability.sh --profile {unit}
;; --record` from the run's own logs and digests. The x86-64 leg runs under Rosetta 2 translation on an arm64
;; host (decision_release-route-x86-64-leg: the CI two-host matrix carries the bare-metal leg).
;; Re-run (on any host — the legs report THAT host's capabilities):
;;   bash scripts/check_portability.sh --profile {unit}

(portability
  (for-gate G-PORTABILITY)
  (unit "{unit}")
  (recorded "{datetime.date.today().isoformat()}")
  (recorded-by "scripts/check_portability.sh --profile {unit} --record (P4-SYSTEM.17 slice a)")
  (rederive "bash scripts/check_portability.sh --profile {unit}")
  (host
    (cpu "{q(tool('sysctl', '-n', 'machdep.cpu.brand_string'))}")
    (kernel "{q(tool('uname', '-sr'))}")
    (arch "{q(arch)}")
    (rustc "{q(tool('rustc', '--version'))}")
    (nightly "{q(tool('cargo', '+' + nightly, '--version'))}")
    (miri "{q(tool('cargo', '+' + nightly, 'miri', '--version'))}"))
  (verdict "{verdict}")
  (legs
    (leg (id "native-{arch}") (verdict "{native}")
         (evidence "cargo test --all — the commit gate's own run: {nok} suites passed, {nfail} failed")
         (note "the offline differential against the pinned expectations; runs on every commit"))
    (leg (id "fixture-digest-manifest") (verdict "{'green' if digest != 'unrecorded' else 'red'}")
         (evidence "sha256 {digest} over the {guests} tracked guests' demo outputs")
         (note "the cross-host contract: a second host's run must reproduce this digest BYTE-IDENTICALLY — it is recomputed, never carried"))
    (leg (id "native-x86-64") (verdict "{q(x86)}")
         (evidence "{q(ev(x86, f'cargo test --all --target x86_64-apple-darwin: {xok} suites passed, {xfail} failed; the x86-64 manifest {xevidence}'))}")
         (note "MANDATORY per docs/EVIDENCE_AND_GATES.md §7 — met VIA TRANSLATION (Rosetta 2) on this host; the bare-metal leg is the CI matrix's"))
    (leg (id "miri") (verdict "{q(miri)}")
         (evidence "{q(ev(miri, f'cargo +{nightly} miri test -p semulith-core — {mok} suites passed, {mfail} failed, interpreted'))}")
         (note "the model's safe-Rust core; the one unsafe island (bench.rs's counting allocator) is excluded by name"))
    (leg (id "cross-endian") (verdict "{q(cross)}")
         (evidence "{q(ev(cross, f'the same suites under Miri on powerpc64-unknown-linux-gnu (big-endian): {cok} passed, {cfail} failed'))}")
         (note "the little-endian guest semantics hold on a big-endian host"))))
"""
out = root / "profiles" / unit / "portability.sexp"
out.write_text(doc)
print(f"portability: recorded {out.relative_to(root)}")
PY
fi
[ "$V" != "failed" ]
