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
LEDGER="profiles/$PROFILE/references.sexp"
[ -f "$LEDGER" ] || { echo "fetch_references: no ledger at $LEDGER" >&2; exit 2; }

command -v python3 >/dev/null 2>&1 || { echo "fetch_references: python3 is required" >&2; exit 2; }
command -v shasum  >/dev/null 2>&1 || { echo "fetch_references: shasum is required" >&2; exit 2; }

# SOT-FORMAT.4: the ledger is S-expression, read through dossier_sexp (the mapping owner).
WORK="$(python3 -c "
import sys, pathlib
sys.path.insert(0, 'scripts')
import dossier_sexp as D
print(D.load_references(pathlib.Path(sys.argv[1])).get('work_dir', 'target/refs'))" "$LEDGER")"
mkdir -p "$WORK"

rc=0
say()  { printf '%s\n' "$*"; }
bad()  { printf '%s\n' "$*" >&2; rc=1; }

# ---- read the ledger into shell-friendly lines: id<TAB>key<TAB>value -------------------------
FIELDS="$(python3 - "$LEDGER" <<'PY'
import pathlib, sys
sys.path.insert(0, "scripts")
import dossier_sexp as D
d = D.load_references(pathlib.Path(sys.argv[1]))
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

# ---- 3b. source tarballs: any candidate pinning asset + source_commit + asset_sha256 -------
# Generic leg — the rv64 ledger never reaches it (sail-riscv has no source_commit, spike no
# asset); the dsp56300 ledger's candidate is fetched as <origin>/archive/<source_commit>.tar.gz
# (the GitHub archive route — recorded in that ledger's commentary) and hash-verified.
while IFS=$'\t' read -r cid casset csha ccommit corigin; do
  [ -n "$cid" ] || continue
  TGZ="$WORK/$casset"
  if [ "$VERIFY_ONLY" -eq 0 ] && [ ! -f "$TGZ" ]; then
    say "FETCH    $cid source tarball -> $TGZ"
    curl -sSL --max-time 300 -o "$TGZ" "$corigin/archive/$ccommit.tar.gz" \
      || bad "FETCH FAILED $cid source tarball"
  fi
  verify_hash "$TGZ" "$csha" "$cid source tarball"
done < <(python3 - "$LEDGER" <<'PY'
import pathlib, sys
sys.path.insert(0, "scripts")
import dossier_sexp as D
d = D.load_references(pathlib.Path(sys.argv[1]))
for c in d.get("candidate", []):
    if c.get("asset") and c.get("source_commit") and c.get("asset_sha256"):
        print(f"{c['id']}\t{c['asset']}\t{c['asset_sha256']}\t{c['source_commit']}\t{c['origin']}")
PY
)

# ---- 4. the ENCODING source: the bit layouts the pinned specification renders only as images --
ENC_DIR="$(python3 - "$LEDGER" <<'PY'
import pathlib, sys
sys.path.insert(0, "scripts")
import dossier_sexp as D
d = D.load_references(pathlib.Path(sys.argv[1]))
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
      # constants.py lives under src/riscv_opcodes/; the instruction tables moved from the
      # repository root to extensions/ upstream (measured 2026-10-03, P4-SYSTEM.2 slice a:
      # master/extensions/rv_i hashes byte-identical to this ledger's pinned rv_i — the move
      # relocated the files without changing their bytes). Metadata (arg_lut.csv, csrs.csv,
      # causes.csv) stays at the root.
      case "$fname" in
        *.py)           sub="src/riscv_opcodes/$fname" ;;
        rv_*|rv32_*|rv64_*) sub="extensions/$fname" ;;
        *)              sub="$fname" ;;
      esac
      say "FETCH    riscv-opcodes/$sub"
      curl -sSL --max-time 120 -o "$dest" \
        "https://raw.githubusercontent.com/riscv/riscv-opcodes/master/$sub" \
        || bad "FETCH FAILED riscv-opcodes/$sub"
    fi
    verify_hash "$dest" "$fsha" "encoding source $fname"
  done < <(python3 - "$LEDGER" <<'PY'
import pathlib, sys
sys.path.insert(0, "scripts")
import dossier_sexp as D
d = D.load_references(pathlib.Path(sys.argv[1]))
for es in d.get("encoding_source", []):
    for f in es.get("file", []):
        print(f"{f['name']}\t{f['sha256']}")
PY
)
  # ⭐ The strongest cheap check on the encoding tables: the profile declares its mnemonic
  # census and the pinned tables must enumerate exactly it. Two independent routes to one
  # closed set. The table set is the base (rv_i/rv64_i) plus the ledger's extension tables
  # — MINUS the M tables when the profile does not select M (rv64i pins rv_m/rv64_m for the
  # fragment's sake, not the scope's — the exclusion is BY NAME, and P4-SYSTEM.2 slice (e)
  # extended this leg for rv64gc's 65-form census: Zicntr's counter reads are $pseudo_op
  # rows of csrrs, so a pseudo-only table contributes its pseudo names — the spec's Zicntr
  # listings ARE those rows) and MINUS the A tables under the same named exclusion until
  # P4-SYSTEM.4's atomic bind grows the census (slice e) — and likewise the Zifencei and F
  # tables until their own binds (P4-SYSTEM.6 slice b; P4-SYSTEM.7 slice c6).
  if out="$(python3 - "$ENC_DIR" "profiles/$PROFILE/profile.sexp" "$LEDGER" <<'PY'
import sys, pathlib, re
sys.path.insert(0, "scripts")
import dossier_sexp as D
enc, prof, ledger = (pathlib.Path(a) for a in sys.argv[1:])
scope = D.load_profile(prof)["scope"]
declared = {m.lower() for v in scope.values() if isinstance(v, list) for m in v}
# the ledger's pinned instruction tables beyond the base — rv_* AND rv64_* (measured at
# the P4-SYSTEM.4 slice-a re-pin: an rv64_-only test never collected rv64_a — or rv64_m —
# so a bound A/M scope would have enumerated 11 rows short; no profile declared an A or M
# form before, so the gap had never fired)
extra = []
for es in D.load_references(ledger).get("encoding_source", []):
    for f in es.get("file", []):
        n = f["name"]
        if n.startswith(("rv_", "rv64_")) and n not in ("rv_i", "rv64_i"):
            extra.append(n)
# the M tables are pinned for the fragment test case, not the scope — excluded unless the
# profile declares an M form; the A tables likewise until P4-SYSTEM.4's atomic bind grows
# the census to 87 (slice e) — the same named exclusion, the same flip condition
if not any(m.startswith(("mul", "div", "rem")) for m in declared):
    extra = [n for n in extra if n not in ("rv_m", "rv64_m")]
if not any(m.startswith(("lr.", "sc.", "amo")) for m in declared):
    extra = [n for n in extra if n not in ("rv_a", "rv64_a")]
# and the Zifencei table under the same named exclusion until P4-SYSTEM.6's bind grows
# the census to 88 (slice b) — the same flip condition again
if not any(m == "fence.i" for m in declared):
    extra = [n for n in extra if n != "rv_zifencei"]
# and the F tables under the same named exclusion until P4-SYSTEM.7's F bind grows the
# census by 30 (slice c6) — the same flip condition: the scope declares an F form
if not any(m in ("flw", "fsw") for m in declared):
    extra = [n for n in extra if n not in ("rv_f", "rv64_f")]
names = set()
for f in ["rv_i", "rv64_i", *extra]:
    lines = (enc / f).read_text().splitlines()
    real = [l.split("#", 1)[0].strip() for l in lines]
    real = [l for l in real if l and not l.startswith("$")]
    for line in real:
        names.add(line.split()[0])
    if not real:  # a pseudo-only table (rv_zicntr): its pseudo rows ARE the census
        for raw in lines:
            line = raw.split("#", 1)[0].strip()
            if line.startswith("$pseudo_op"):
                names.add(line.split()[2])
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

# ---- 4b. the OWNED fragments must still agree with the pinned upstream ----------------------
# ⛔ Ownership without a re-derivation is just a copy. `definitions/` is tracked so a fresh clone
# can build a model without the network; this proves the fragments have not drifted from the
# tables they were generated from, whenever those tables are present.
if [ -d definitions ] && [ -d "$ENC_DIR" ]; then
  if tmp_dir="$(mktemp -d)" && python3 - "$tmp_dir" <<'PY'
import sys, pathlib, shutil, subprocess
tmp = pathlib.Path(sys.argv[1])
shutil.copytree("definitions", tmp / "have")
subprocess.run([sys.executable, "scripts/gen_fragments.py"], check=True,
               stdout=subprocess.DEVNULL)
PY
  then
    if diff -r -q "$tmp_dir/have" definitions >/dev/null 2>&1; then
      say "MATCH    owned fragments agree with the pinned upstream  definitions/"
    else
      bad "DIFFERS  definitions/ no longer matches what the pinned tables generate
           $(diff -r "$tmp_dir/have" definitions | head -6)
           Regenerate — never edit: scripts/gen_fragments.py"
    fi
  else
    bad "FAILED   could not regenerate the definition fragments"
  fi
  rm -rf "$tmp_dir"
fi

# ---- 5. the matched configuration must still produce the recorded ISA string -----------------
# The strongest cheap check here: the model's OWN report of what it is configured as.
# SOT-FORMAT.4: the tracked truth is the .sexp; the JSON the model reads is derived from it
# (untracked, repo volume) before the check — one source of truth, one foreign-tool rendering.
SAIL_BIN="$(get sail-riscv binary)"; CFG="profiles/$PROFILE/$(get sail-riscv matched_config)"
WANT_ISA="$(get sail-riscv matched_isa_string)"
if [[ "$CFG" == *.json ]] && [ -f "${CFG%.json}.sexp" ]; then
  python3 - "$PROFILE" <<'PYCFG'
import pathlib, sys
sys.path.insert(0, "scripts")
import dossier_sexp as D
D.materialize_sail_override(pathlib.Path(".").resolve(), sys.argv[1])
PYCFG
  CFG="target/refs/$(basename "$CFG")"
fi
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
