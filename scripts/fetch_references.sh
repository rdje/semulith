#!/usr/bin/env bash
# scripts/fetch_references.sh — acquire (or re-verify) the reference models for a profile.
#
# The sibling of `scripts/fetch_sources.sh`: that one makes the SPECIFICATION we read
# identifiable, this one makes the MODELS we compare against identifiable. Both exist because a
# recorded hash whose producer is a throwaway command is a "trust me" with extra steps.
#
# ⛔ DELIBERATELY NOT A COMMIT GATE. It needs the network and a C++ toolchain. `profiles/*/
# references.toml` is gated by PROFILE-CONSISTENCY for its SHAPE; this tool is what re-derives
# its CONTENT, on demand.
#
# ⛔ EVERYTHING LANDS ON THE REPOSITORY VOLUME. All paths are repo-root-relative and every
# artifact is written under `target/refs/`. Nothing is installed into a shared prefix: a package
# manager's prefix is on a different volume here, and a dependency store off-volume is exactly
# what the data-locality policy forbids. Pre-existing host toolchains (a compiler, `dtc`, an
# already-installed QEMU) are used READ-ONLY and are recorded as cross-volume in references.toml.
#
# Usage:
#   scripts/fetch_references.sh [--verify-only] [<profile>]
#     --verify-only   re-derive the recorded hashes from what is already on disk; fetch nothing.
#     <profile>       defaults to rv64i-lab-v0.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

VERIFY_ONLY=0
[ "${1:-}" = "--verify-only" ] && { VERIFY_ONLY=1; shift; }
PROFILE="${1:-rv64i-lab-v0}"
LEDGER="profiles/$PROFILE/references.toml"
[ -f "$LEDGER" ] || { echo "fetch_references: no ledger at $LEDGER" >&2; exit 2; }

command -v python3 >/dev/null 2>&1 || { echo "fetch_references: python3 is required" >&2; exit 2; }
command -v shasum  >/dev/null 2>&1 || { echo "fetch_references: shasum is required" >&2; exit 2; }

WORK="$(python3 -c "
import tomllib,sys,pathlib
print(tomllib.loads(pathlib.Path(sys.argv[1]).read_text()).get('work_dir','target/refs'))" "$LEDGER")"
mkdir -p "$WORK"

rc=0
say()  { printf '%s\n' "$*"; }
bad()  { printf '%s\n' "$*" >&2; rc=1; }

# ---- read the ledger into shell-friendly lines: id<TAB>key<TAB>value -------------------------
FIELDS="$(python3 - "$LEDGER" <<'PY'
import tomllib, pathlib, sys
d = tomllib.loads(pathlib.Path(sys.argv[1]).read_text())
for c in d.get("candidate", []):
    for k in ("id","status","origin","release","asset","asset_sha256","binary","binary_sha256",
              "source_commit","matched_config","matched_isa_string"):
        if k in c:
            print(f"{c['id']}\t{k}\t{c[k]}")
PY
)"
get() { printf '%s\n' "$FIELDS" | awk -F'\t' -v i="$1" -v k="$2" '$1==i && $2==k {print $3; exit}'; }

verify_hash() { # verify_hash <path> <expected> <label>
  local p="$1" want="$2" label="$3" got
  if [ ! -f "$p" ]; then bad "MISSING  $label: $p is not present (run without --verify-only)"; return; fi
  got="$(shasum -a 256 "$p" | awk '{print $1}')"
  if [ "$got" = "$want" ]; then say "MATCH    $label  $p"
  else bad "DIFFERS  $label: $p
           pinned $want
           actual $got
           Re-read the ledger and re-confirm what changed; do NOT edit the hash to make it pass."
  fi
}

# ---- 1. sail-riscv: a prebuilt release asset ------------------------------------------------
SAIL_ASSET="$(get sail-riscv asset)"; SAIL_REL="$(get sail-riscv release)"
SAIL_ORIGIN="$(get sail-riscv origin)"
if [ -n "$SAIL_ASSET" ]; then
  TGZ="$WORK/$SAIL_ASSET"
  if [ "$VERIFY_ONLY" -eq 0 ] && [ ! -f "$TGZ" ]; then
    say "FETCH    sail-riscv $SAIL_REL -> $TGZ"
    curl -sSL --max-time 300 -o "$TGZ" "$SAIL_ORIGIN/releases/download/$SAIL_REL/$SAIL_ASSET" \
      || bad "FETCH FAILED sail-riscv asset"
  fi
  verify_hash "$TGZ" "$(get sail-riscv asset_sha256)" "sail-riscv asset"
  BIN="$(get sail-riscv binary)"
  if [ "$VERIFY_ONLY" -eq 0 ] && [ ! -f "$BIN" ] && [ -f "$TGZ" ]; then
    say "EXTRACT  $TGZ"; tar xzf "$TGZ" -C "$WORK"
  fi
  verify_hash "$BIN" "$(get sail-riscv binary_sha256)" "sail-riscv binary"
fi

# ---- 2. spike: a source build ----------------------------------------------------------------
SPIKE_COMMIT="$(get spike source_commit)"; SPIKE_BIN="$(get spike binary)"
if [ -n "$SPIKE_COMMIT" ]; then
  SRC="$WORK/spike-src"; BUILD="$WORK/spike-build"
  if [ "$VERIFY_ONLY" -eq 0 ] && [ ! -d "$SRC" ]; then
    say "CLONE    spike -> $SRC"
    git clone --depth 1 "$(get spike origin).git" "$SRC" >/dev/null 2>&1 || bad "CLONE FAILED spike"
  fi
  if [ -d "$SRC" ]; then
    got="$(git -C "$SRC" rev-parse HEAD 2>/dev/null)"
    if [ "$got" = "$SPIKE_COMMIT" ]; then say "MATCH    spike source commit  $got"
    else bad "DIFFERS  spike source commit
           pinned $SPIKE_COMMIT
           actual ${got:-<none>}
           A shallow clone tracks the branch tip; re-pin the ledger deliberately, with a reason."
    fi
  fi
  if [ "$VERIFY_ONLY" -eq 0 ] && [ ! -x "$SPIKE_BIN" ] && [ -d "$SRC" ]; then
    say "BUILD    spike (configure + make) -> $BUILD"
    mkdir -p "$BUILD"
    ( cd "$BUILD" && ../spike-src/configure --prefix="$ROOT/$WORK/spike-prefix" >configure.log 2>&1 \
      && make -j"$(sysctl -n hw.ncpu 2>/dev/null || echo 4)" >build.log 2>&1 ) \
      || bad "BUILD FAILED spike — see $BUILD/configure.log and $BUILD/build.log"
  fi
  verify_hash "$SPIKE_BIN" "$(get spike binary_sha256)" "spike binary"
fi

# ---- 3. qemu: a pre-existing host toolchain, never fetched -----------------------------------
QEMU_BIN="$(get qemu binary)"
if [ -n "$QEMU_BIN" ]; then
  if [ -x "$QEMU_BIN" ]; then
    verify_hash "$QEMU_BIN" "$(get qemu binary_sha256)" "qemu binary (host toolchain, read-only)"
  else
    bad "MISSING  qemu binary: $QEMU_BIN is not present.
           This one is NOT fetched by design — it is a pre-existing host toolchain used read-only.
           Install it through the host's own package manager, or record qemu as not obtained."
  fi
fi

# ---- 4. the ENCODING source: the bit layouts the pinned specification renders only as images --
ENC_DIR="$(python3 - "$LEDGER" <<'PY'
import tomllib, pathlib, sys
d = tomllib.loads(pathlib.Path(sys.argv[1]).read_text())
es = d.get("encoding_source") or []
print(es[0]["work_dir"] if es else "")
PY
)"
if [ -n "$ENC_DIR" ]; then
  mkdir -p "$ENC_DIR"
  while IFS=$'\t' read -r fname fsha; do
    [ -n "$fname" ] || continue
    dest="$ENC_DIR/$fname"
    if [ "$VERIFY_ONLY" -eq 0 ] && [ ! -f "$dest" ]; then
      # constants.py lives under src/riscv_opcodes/; the tables live at the repository root.
      case "$fname" in
        *.py) sub="src/riscv_opcodes/$fname" ;;
        *)    sub="$fname" ;;
      esac
      say "FETCH    riscv-opcodes/$sub"
      curl -sSL --max-time 120 -o "$dest" \
        "https://raw.githubusercontent.com/riscv/riscv-opcodes/master/$sub" \
        || bad "FETCH FAILED riscv-opcodes/$sub"
    fi
    verify_hash "$dest" "$fsha" "encoding source $fname"
  done < <(python3 - "$LEDGER" <<'PY'
import tomllib, pathlib, sys
d = tomllib.loads(pathlib.Path(sys.argv[1]).read_text())
for es in d.get("encoding_source", []):
    for f in es.get("file", []):
        print(f"{f['name']}\t{f['sha256']}")
PY
)
  # ⭐ The strongest cheap check on the encoding tables: the profile declares 52 mnemonics and the
  # tables must enumerate exactly those 52. Two independent routes to one closed set.
  if out="$(python3 - "$ENC_DIR" "profiles/$PROFILE/profile.toml" <<'PY'
import sys, pathlib, tomllib, re
enc, prof = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
names = set()
for f in ("rv_i", "rv64_i"):
    for raw in (enc / f).read_text().splitlines():
        line = raw.split("#", 1)[0].strip()
        if line and not line.startswith("$"):
            names.add(line.split()[0])
scope = tomllib.loads(prof.read_text())["scope"]
declared = {m.lower() for v in scope.values() if isinstance(v, list) for m in v}
diff = sorted(names ^ declared)
print(f"{len(names)}\t{len(declared)}\t{','.join(diff) if diff else 'NONE'}")
PY
)"; then
    n_enc="$(printf '%s' "$out" | cut -f1)"; n_prof="$(printf '%s' "$out" | cut -f2)"
    diff="$(printf '%s' "$out" | cut -f3)"
    if [ "$diff" = "NONE" ]; then
      say "MATCH    encoding tables vs profile scope  $n_enc == $n_prof, symmetric difference NONE"
    else
      bad "DIFFERS  encoding tables vs profile scope
           tables enumerate $n_enc, profile declares $n_prof
           symmetric difference: $diff"
    fi
  fi
fi

# ---- 4b. the OWNED encodings must still agree with the pinned upstream -----------------------
# ⛔ Ownership without a re-derivation is just a copy. `profiles/<p>/encoding.sexp` is tracked so a
# fresh clone can build a model without the network; this proves it has not drifted from the table
# it was generated from, whenever that table is present.
ENC_SEXP="profiles/$PROFILE/encoding.sexp"
if [ -f "$ENC_SEXP" ] && [ -d "$ENC_DIR" ]; then
  if tmp_enc="$(mktemp)" && python3 - "$PROFILE" > "$tmp_enc" <<'PY'
import sys, pathlib, subprocess
sys.path.insert(0, "scripts")
import gen_encoding
sys.stdout.write(gen_encoding.build(sys.argv[1]))
PY
  then
    if diff -q "$tmp_enc" "$ENC_SEXP" >/dev/null 2>&1; then
      say "MATCH    owned encodings agree with the pinned upstream  $ENC_SEXP"
    else
      bad "DIFFERS  $ENC_SEXP no longer matches what the pinned tables generate
           $(diff "$tmp_enc" "$ENC_SEXP" | head -6)
           Regenerate it — never edit it: scripts/gen_encoding.py $PROFILE"
    fi
  else
    bad "FAILED   could not regenerate encodings for $PROFILE"
  fi
  rm -f "$tmp_enc"
fi

# ---- 5. the matched configuration must still produce the recorded ISA string -----------------
# The strongest cheap check here: the model's OWN report of what it is configured as.
SAIL_BIN="$(get sail-riscv binary)"; CFG="profiles/$PROFILE/$(get sail-riscv matched_config)"
WANT_ISA="$(get sail-riscv matched_isa_string)"
if [ -x "$SAIL_BIN" ] && [ -f "$CFG" ] && [ -n "$WANT_ISA" ]; then
  got_isa="$("$SAIL_BIN" --config-override "$CFG" --print-isa-string 2>&1)"
  if [ "$got_isa" = "$WANT_ISA" ]; then say "MATCH    matched-profile ISA string  $got_isa"
  else bad "DIFFERS  matched-profile ISA string
           pinned $WANT_ISA
           actual $got_isa
           The override no longer configures the model to the profile it claims."
  fi
fi

[ "$rc" -eq 0 ] && say "fetch_references: ok ($PROFILE)" || say "fetch_references: FAILED ($PROFILE)" >&2
exit "$rc"
