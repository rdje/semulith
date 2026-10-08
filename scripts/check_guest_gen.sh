#!/usr/bin/env bash
# scripts/check_guest_gen.sh — GUEST-GEN (project doctrine).
#
# `crates/semulith-verify/src/guests.rs` is GENERATED from the tracked assembly guests and
# their specification-derived expectations by `scripts/gen_guests.py` (P1-LAB.8; OWN-03:
# generated artifacts are changed by regeneration, never by direct editing, and identify
# their canonical inputs, generator, configuration and source fingerprints). This check
# regenerates the fixture in memory and refuses the day it stops byte-matching the
# committed file — a hand-edited expectation or word list is how the offline differential
# quietly stops testing what the tracked documents declare.
#
# ⭐ WHAT THIS ACTUALLY PROTECTS: the EVD-05 guarantee. The guests' expectation values were
# derived from the pinned specification prose before any model ran; the verify tests
# compare the definitional interpreter's observations against exactly these values on every
# commit. If the fixture drifts from the tracked sources — or the tracked sources move
# without the fixture — the gate compares the model against a fiction and green means
# nothing.
#
# ⚠️ HONEST LIMIT: it proves the fixture is still the function of the tracked guest
# sources and expectations. It says nothing about whether the expectations are TRUE — that
# is what the live reference comparison (scripts/run_semulith_smoke.py) is for, and why
# finite differential testing is tested evidence, never universal proof.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "GUEST-GEN: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

ENCODING="profiles/rv64i-lab-v0/encoding.sexp"
GUESTS_DIR="profiles/rv64i-lab-v0/guests"
OUT="crates/semulith-verify/src/guests.rs"
# P4-SYSTEM.2 slice h (the route flip): the census's rv64gc owner→mirror pair, and the
# base mirror's recorded re-derivations (slice f: the three D-IALIGN-16 guests —
# 2-mod-4 targets are legal with C, RVI-C 27.1; slice g: the two fencei guests —
# rv64gc DECLARES Zifencei and the staged encoding's slot is unbound, so rv64i's
# DIFF-FENCEI-EXECUTED pin does not transfer; P4-SYSTEM.6 slice b: the two selfmod
# guests' expectation comments — the fence.i bind makes "without Zifencei" stale in
# this unit, and the data fence is not the fetch synchronization: the chapter
# guarantees visibility only after a FENCE.I, the data fence's role is cross-hart).
# Every other mirrored file is byte-identical to its rv64i owner, and the governor
# below names any drift.
ENCODING_GC="profiles/rv64gc-lab-v0/encoding.sexp"
GUESTS_DIR_GC="profiles/rv64gc-lab-v0/guests"
OUT_GC="crates/semulith-verify/src/guests_rv64gc.rs"
MIRROR_REDERIVED="fault-jal-mis fault-jalr-mis it-prio-jump it-fencei min-fencei dir-selfmod-fence fault-selfmod"

# ── the base-mirror governor (P4-SYSTEM.2 slice f disposition, registered at the flip) ─
# The rv64gc guests/ directory is a DERIVED mirror of rv64i's: every mirrored file is
# byte-identical to its owner, and exactly the named re-derived files differ — each with
# its reason recorded. A silent edit on either side breaks a pair and is named. Defined
# before the self-test so the arms below exercise the same function the gate runs.
judge_mirror() { # $1 owner dir  $2 mirror dir — prints a verdict line, rc is the verdict
  local owner="$1" mirror="$2" name fail=0 count=0
  for f in "$owner"/*.s; do
    name="$(basename "$f")"
    [ -f "$mirror/$name" ] || continue   # a guest the mirror does not carry is the
                                         # corpus's own record (c-scope.c disposition)
    count=$((count+1))
    cmp -s "$f" "$mirror/$name" || {
      printf 'GUEST-GEN: MIRROR DRIFT — guests/%s is no longer byte-identical to %s; a re-derivation is a recorded act, not a silent edit\n' \
        "$name" "$f" >&2
      fail=1
    }
  done
  local rederived=0
  for f in "$mirror"/*.expected.sexp; do
    name="$(basename "$f")"
    [ -f "$owner/$name" ] || continue
    if cmp -s "$owner/$name" "$f"; then
      count=$((count+1))
    else
      case " $MIRROR_REDERIVED " in
        *" ${name%.expected.sexp} "*) rederived=$((rederived+1)) ;;
        *) printf 'GUEST-GEN: MIRROR DRIFT — guests/%s differs from %s but is not one of the recorded re-derivations (%s)\n' \
             "$name" "$owner/$name" "$MIRROR_REDERIVED" >&2
           fail=1 ;;
      esac
    fi
  done
  for name in $MIRROR_REDERIVED; do
    if cmp -s "$owner/$name.expected.sexp" "$mirror/$name.expected.sexp" 2>/dev/null; then
      printf 'GUEST-GEN: MIRROR DRIFT — %s is recorded as re-derived but matches its owner byte-identically; the record is stale\n' \
        "$name" >&2
      fail=1
    fi
  done
  [ "$fail" -eq 0 ] || return 1
  printf 'the base mirror holds: %d file(s) byte-identical, %d recorded re-derivation(s)\n' \
    "$count" "$rederived"
}

# ── self-test ────────────────────────────────────────────────────────────────────────────────
SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }

self_test() {
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"

  # The surgical guests directory mirrors the real layout: <name>.s + <name>.expected.sexp
  # + the run-order record (P4-SYSTEM.2 slice d: the guest SET is directory-derived; the
  # order is recorded data).
  mkdir -p "$t/guests"
  cp "$GUESTS_DIR"/*.s "$GUESTS_DIR"/*.expected.sexp "$GUESTS_DIR/run-order.txt" "$t/guests/"
  GEN() { python3 scripts/gen_guests.py --encoding "$ENCODING" --guests-dir "$t/guests" \
          --out "$t/guests.rs" "$@"; }

  # ⛔ STRICT ARITY (docs/knowledge/self-test-arms-that-never-ran.md): a missing `;` before
  # an arm call swallows it silently; the guard makes that a loud failure.
  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'GUEST-GEN self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' \
      "$3" "$2" "$1" >&2
    return 1
  }
  arm() { # arm <name> <rc> <expected-rc> <output> <reason substring; empty = expect no output>
    argc 5 "$#" arm || return
    if [ -z "$5" ]; then
      if [ "$2" = "$3" ] && [ -z "$4" ]; then
        pass=$((pass+1)); return
      fi
      fail=$((fail+1))
      printf 'GUEST-GEN self-test MISS: %s — expected rc=%s and no output, got rc=%s\n%s\n' \
        "$1" "$3" "$2" "$4" >&2
      return
    fi
    if [ "$2" = "$3" ] && printf '%s' "$4" | grep -qF "$5"; then
      pass=$((pass+1))
    else
      fail=$((fail+1))
      printf 'GUEST-GEN self-test MISS: %s — expected rc=%s (reason: %s), got rc=%s\n%s\n' \
        "$1" "$3" "$5" "$2" "$4" >&2
    fi
  }

  # GREEN: the generator emits a fixture from the tracked guests.
  out="$(GEN 2>&1)"; rc=$?
  arm "GREEN the generator emits a fixture from the tracked guests" "$rc" 0 "$out" "wrote"

  # GREEN: the drift check passes on a faithful regeneration.
  out="$(GEN --check 2>&1)"; rc=$?
  arm "GREEN a faithful regeneration is judged in sync" "$rc" 0 "$out" "matches"

  # RED: a hand-edit of the generated fixture is detected, named, and refused.
  printf '\n// hand edit\n' >> "$t/guests.rs"
  out="$(GEN --check 2>&1)"; rc=$?
  arm "RED a hand-edited fixture is refused, naming DRIFT" "$rc" 1 "$out" "DRIFT"
  GEN >/dev/null 2>&1 # restore a faithful fixture for the remaining arms

  # RED: a guest that does not assemble is refused by name.
  printf 'zzz9 x1, x2\n' >> "$t/guests/smoke-arith.s"
  out="$(GEN --check 2>&1)"; rc=$?
  arm "RED an unassemblable guest is refused, naming the mnemonic" "$rc" 2 "$out" "zzz9"
  cp "$GUESTS_DIR/smoke-arith.s" "$t/guests/smoke-arith.s"

  # RED: an expectations document whose step exceeds the declared count is refused.
  sed 's/(instructions 12)/(instructions 11)/' "$GUESTS_DIR/smoke-arith.expected.sexp" \
    > "$t/guests/smoke-arith.expected.sexp"
  out="$(GEN --check 2>&1)"; rc=$?
  arm "RED an expectation step past the declared count is refused" "$rc" 2 "$out" "exceeds"
  cp "$GUESTS_DIR/smoke-arith.expected.sexp" "$t/guests/smoke-arith.expected.sexp"

  # RED: an expectations document missing steps is refused (a gap would read as 'writes
  # nothing', which is a lie the generator must not emit).
  python3 - "$t/guests/smoke-arith.expected.sexp" <<'PY'
import sys
path = sys.argv[1]
text = open(path, encoding="utf-8").read()
i = text.find('(step (n 11)')
assert i > 0
# Step 11 is the last child of the outer (expectations …) form: drop it, then re-close
# the outer form with the file's final paren.
k = text.rfind(')')
open(path, "w", encoding="utf-8").write(text[:i] + text[k:])
PY
  out="$(GEN --check 2>&1)"; rc=$?
  arm "RED expectations missing a step are refused" "$rc" 2 "$out" "carry no expectation"
  cp "$GUESTS_DIR/smoke-arith.expected.sexp" "$t/guests/smoke-arith.expected.sexp"

  # RED: a register outside the x0..x31 vocabulary is refused by name.
  sed 's/(reg "x1")/(reg "x99")/' "$GUESTS_DIR/guest-control.expected.sexp" \
    > "$t/guests/guest-control.expected.sexp"
  out="$(GEN --check 2>&1)"; rc=$?
  arm "RED a register outside x0..x31 is refused" "$rc" 2 "$out" "x99"
  cp "$GUESTS_DIR/guest-control.expected.sexp" "$t/guests/guest-control.expected.sexp"

  # RED: a fetch-count declaration outside the parcel bounds is refused (P4-SYSTEM.3
  # slice e: a step whose fetch page-faults issues NO request, a page-straddling
  # instruction issues TWO — the declared count lives in [0, 2x steps], and a count
  # outside it is a lie the generator must not emit).
  sed 's/(instructions 12)/(instructions 12) (fetches 25)/' "$GUESTS_DIR/smoke-arith.expected.sexp" \
    > "$t/guests/smoke-arith.expected.sexp"
  out="$(GEN --check 2>&1)"; rc=$?
  arm "RED a fetches count outside the parcel bounds is refused" "$rc" 2 "$out" "fetches"
  cp "$GUESTS_DIR/smoke-arith.expected.sexp" "$t/guests/smoke-arith.expected.sexp"

  # ---- directory derivation (P4-SYSTEM.2 slice d) ---------------------------------------------
  # RED: the run-order record missing is refused — the order is data, never the
  # directory's accident.
  mv "$t/guests/run-order.txt" "$t/guests/run-order.txt.bak"
  out="$(GEN --check 2>&1)"; rc=$?
  arm "RED a missing run-order record is refused" "$rc" 2 "$out" "run-order.txt"
  mv "$t/guests/run-order.txt.bak" "$t/guests/run-order.txt"

  # RED: a guest the run order names that is not on disk is refused, named.
  printf 'ghost-guest\n' >> "$t/guests/run-order.txt"
  out="$(GEN --check 2>&1)"; rc=$?
  arm "RED a listed guest not on disk is refused, named" "$rc" 2 "$out" "ghost-guest"
  python3 - "$t/guests/run-order.txt" <<'PY'
import sys
path = sys.argv[1]
lines = open(path).read().splitlines()
assert lines[-1] == "ghost-guest"
open(path, "w").write("\n".join(lines[:-1]) + "\n")
PY

  # RED: a guest on disk but missing from the run order never executes — refused, named.
  cp "$GUESTS_DIR/smoke-trap.s" "$t/guests/zz-probe.s"
  cp "$GUESTS_DIR/smoke-trap.expected.sexp" "$t/guests/zz-probe.expected.sexp"
  out="$(GEN --check 2>&1)"; rc=$?
  arm "RED an unlisted guest on disk is refused, named" "$rc" 2 "$out" "zz-probe"
  rm "$t/guests/zz-probe.s" "$t/guests/zz-probe.expected.sexp"

  # The slice-(h) census arms: the gate's judging loop covers the rv64gc owner→mirror
  # pair — pinned against the REAL pair, not a synthetic one.
  out="$(python3 scripts/gen_guests.py --check --encoding "$ENCODING_GC" \
        --guests-dir "$GUESTS_DIR_GC" --image-format bytes --out "$OUT_GC" 2>&1)"; rc=$?
  arm "GREEN the census's rv64gc pair is in sync" "$rc" 0 "$out" "matches"
  cp "$OUT_GC" "$t/gc-fixture.rs"; printf '\n// hand edit\n' >> "$t/gc-fixture.rs"
  out="$(python3 scripts/gen_guests.py --check --encoding "$ENCODING_GC" \
        --guests-dir "$GUESTS_DIR_GC" --image-format bytes --out "$t/gc-fixture.rs" 2>&1)"; rc=$?
  arm "RED the census's rv64gc pair catches a hand edit" "$rc" 1 "$out" "DRIFT"

  # The base-mirror governor arms: the mirror holds on the real tree, and the governor
  # discriminates — a drifted pair is named, a stale re-derivation record is named.
  out="$(judge_mirror "$GUESTS_DIR" "$GUESTS_DIR_GC" 2>&1)"; rc=$?
  arm "GREEN the base mirror holds on the real tree" "$rc" 0 "$out" "byte-identical"
  mkdir -p "$t/mirror"
  cp "$GUESTS_DIR_GC"/* "$t/mirror/" 2>/dev/null || cp -R "$GUESTS_DIR_GC/." "$t/mirror/"
  printf '\n;; silent edit\n' >> "$t/mirror/bound-arith.expected.sexp"
  out="$(judge_mirror "$GUESTS_DIR" "$t/mirror" 2>&1)"; rc=$?
  arm "RED a drifted mirror file is named" "$rc" 1 "$out" "bound-arith"
  rm "$t/mirror/bound-arith.expected.sexp"
  cp "$GUESTS_DIR/bound-arith.expected.sexp" "$t/mirror/bound-arith.expected.sexp"
  cp "$GUESTS_DIR/fault-jal-mis.expected.sexp" "$t/mirror/fault-jal-mis.expected.sexp"
  out="$(judge_mirror "$GUESTS_DIR" "$t/mirror" 2>&1)"; rc=$?
  arm "RED a stale re-derivation record is named" "$rc" 1 "$out" "fault-jal-mis"

  # P4-SYSTEM.12 d1: C is still unbound, so the assembler uses a temporary full
  # composition; the expected words and byte image are hand-written spec-side fixtures.
  out="$(python3 scripts/probe_c_assembler.py 2>&1)"; rc=$?
  arm "GREEN C assembler words and exact byte image" "$rc" 0 "$out" "37 spec-side words"
  out="$(python3 scripts/probe_c_assembler.py --mutation compact-base 2>&1)"; rc=$?
  arm "RED a wrong compact-register base is caught" "$rc" 1 "$out" "c.addi4spn: 0x0044, expected 0x0040"
  out="$(python3 scripts/probe_c_assembler.py --mutation label-stride 2>&1)"; rc=$?
  arm "RED word-stride labels are caught" "$rc" 1 "$out" "AssertionError: byte label addresses"
  out="$(python3 scripts/probe_c_assembler.py --mutation padding 2>&1)"; rc=$?
  arm "RED silently padded short units are caught" "$rc" 1 "$out" "AssertionError: exact byte image"

  # d2: the emitted byte fixture is consumed by the actual runner, not a second loader.
  out="$(python3 scripts/probe_c_guest_image.py 2>&1)"; rc=$?
  arm "GREEN mixed C fixture executes through the tracked runner" "$rc" 0 "$out" "mixed bytes, labels, writes and parcel counts passed"
  out="$(python3 scripts/probe_c_guest_image.py --mutation padding 2>&1)"; rc=$?
  arm "RED a padded generated image is caught" "$rc" 1 "$out" "AssertionError: exact generated image bytes"
  out="$(python3 scripts/probe_c_guest_image.py --mutation runner-offset 2>&1)"; rc=$?
  arm "RED a runner that loads at the wrong offset is caught" "$rc" 1 "$out" "mixed: step 0 writes match"

  # d3a: promote the independent author, preserve its owned records, refuse reserved bits.
  out="$(python3 scripts/probe_gc_author.py 2>&1)"; rc=$?
  arm "GREEN tracked author re-derives its owned corpus and refuses reserved bits" "$rc" 0 "$out" "owned corpus passed"
  out="$(python3 scripts/probe_gc_author.py --mutation reserved-op 2>&1)"; rc=$?
  arm "RED a missing OP fixed-bit guard is caught" "$rc" 1 "$out" "reserved word 0x04000033 accepted"
  out="$(python3 scripts/probe_gc_author.py --mutation reserved-shift 2>&1)"; rc=$?
  arm "RED a missing shift fixed-bit guard is caught" "$rc" 1 "$out" "reserved word 0x04001013 accepted"
  out="$(python3 scripts/probe_gc_author.py --mutation division-rounding 2>&1)"; rc=$?
  arm "RED division rounding away from zero changes the authored M record" "$rc" 1 "$out" "DRIFT — m-div"
  out="$(python3 scripts/probe_gc_author.py --mutation ignore-sum 2>&1)"; rc=$?
  arm "RED a missing SUM permission is caught" "$rc" 1 "$out" "SUM=1 permits S data on U pages"
  out="$(python3 scripts/probe_gc_author.py --mutation ignore-mxr 2>&1)"; rc=$?
  arm "RED a missing MXR permission is caught" "$rc" 1 "$out" "MXR=1 permits an X-only load"
  out="$(python3 scripts/probe_gc_author.py --mutation ignore-user 2>&1)"; rc=$?
  arm "RED a missing U-mode permission gate is caught" "$rc" 1 "$out" "U mode cannot read an S page"

  # d3b: absent ordinary rows/process output must never become reference agreement.
  out="$(python3 scripts/probe_gc_sail.py 2>&1)"; rc=$?
  arm "GREEN strict Sail rows and witnessed delivery gaps" "$rc" 0 "$out" "failed processes and stale traces passed"
  out="$(python3 scripts/probe_gc_sail.py --mutation permit-missing 2>&1)"; rc=$?
  arm "RED absent ordinary no-write steps cannot agree" "$rc" 1 "$out" "empty ordinary no-write trace accepted"
  out="$(python3 scripts/probe_gc_sail.py --mutation ignore-status 2>&1)"; rc=$?
  arm "RED failed reference processes cannot agree" "$rc" 1 "$out" "failed reference process accepted"
  out="$(python3 scripts/probe_gc_sail.py --mutation unwitnessed-gap 2>&1)"; rc=$?
  arm "RED declared delivery gaps still need trace events" "$rc" 1 "$out" "unwitnessed delivery gap accepted"
  out="$(python3 scripts/probe_gc_sail.py --mutation keep-stale 2>&1)"; rc=$?
  arm "RED stale traces cannot stand in for a new run" "$rc" 1 "$out" "stale traces accepted as a new run"

  # d3c: independent C parcel rules, including scatter basis and original trap bits.
  out="$(python3 scripts/probe_c_author.py 2>&1)"; rc=$?
  arm "GREEN independent C author expansions and effects" "$rc" 0 "$out" "37 expansions/effects"
  out="$(python3 scripts/probe_c_author.py --mutation compact-base 2>&1)"; rc=$?
  arm "RED wrong C author compact registers" "$rc" 1 "$out" "c.addi4spn: C expansion mismatch"
  out="$(python3 scripts/probe_c_author.py --mutation signed-immediate 2>&1)"; rc=$?
  arm "RED wrong C author immediate sign" "$rc" 1 "$out" "c.addi: C expansion mismatch"
  out="$(python3 scripts/probe_c_author.py --mutation link-length 2>&1)"; rc=$?
  arm "RED wrong C author length/link" "$rc" 1 "$out" "C parcel advanced by wrong length"
  out="$(python3 scripts/probe_c_author.py --mutation reserved-guard 2>&1)"; rc=$?
  arm "RED reserved C author parcels cannot execute" "$rc" 1 "$out" "reserved parcel 0x0000 accepted"
  out="$(python3 scripts/probe_c_author.py --mutation scattered-bits 2>&1)"; rc=$?
  arm "RED a permutation of C immediate bits" "$rc" 1 "$out" "scattered bit 0x4000/6 misplaced"
  out="$(python3 scripts/probe_c_author.py --mutation expanded-trap 2>&1)"; rc=$?
  arm "RED C illegal traps keep the original parcel" "$rc" 1 "$out" "FP illegal trap lost original C parcel"

  # d3d1: independently walk and fetch only the required ILEN parcels.
  out="$(python3 scripts/probe_gc_fetch.py 2>&1)"; rc=$?
  arm "GREEN independent Sv39 walk and exact parcel fetches" "$rc" 0 "$out" "exact parcel schedules passed"
  out="$(python3 scripts/probe_gc_fetch.py --mutation canonical-sign 2>&1)"; rc=$?
  arm "RED a non-canonical Sv39 sign is caught" "$rc" 1 "$out" "Sv39 sign bit and upper bits disagree"
  out="$(python3 scripts/probe_gc_fetch.py --mutation reserved-pte 2>&1)"; rc=$?
  arm "RED reserved Sv39 PTE high bits are caught" "$rc" 1 "$out" "reserved PTE bit 54 accepted"
  out="$(python3 scripts/probe_gc_fetch.py --mutation nonleaf-bits 2>&1)"; rc=$?
  arm "RED non-leaf Sv39 reserved bits fault before descent" "$rc" 1 "$out" "non-leaf reserved bit must fault before descending"
  out="$(python3 scripts/probe_gc_fetch.py --mutation bottom-pointer 2>&1)"; rc=$?
  arm "RED a bottom-level pointer produces an architectural fault" "$rc" 1 "$out" "bottom-level pointer must page-fault"
  out="$(python3 scripts/probe_gc_fetch.py --mutation mprv 2>&1)"; rc=$?
  arm "RED effective MPRV data privilege is caught" "$rc" 1 "$out" "MPRV data access must use MPP"
  out="$(python3 scripts/probe_gc_fetch.py --mutation eager-second 2>&1)"; rc=$?
  arm "RED a compressed fetch never probes its neighbor" "$rc" 1 "$out" "compressed region-end fetch inspected its neighbor"
  out="$(python3 scripts/probe_gc_fetch.py --mutation fault-tval 2>&1)"; rc=$?
  arm "RED an upper-parcel fault preserves VA and starting EPC" "$rc" 1 "$out" "second parcel lost fault VA/start EPC"
  out="$(python3 scripts/probe_gc_fetch.py --mutation short-ilen 2>&1)"; rc=$?
  arm "RED a wider prefix retains all ILEN bits" "$rc" 1 "$out" "wider prefix lost ILEN bits"
  out="$(python3 scripts/probe_gc_fetch.py --mutation unaligned-epc 2>&1)"; rc=$?
  arm "RED trap EPC always masks bit zero" "$rc" 1 "$out" "EPC bit zero was not masked"

  # d3d2: exact byte guests have explicit boundary budgets and fresh memory fetches.
  out="$(python3 scripts/probe_gc_parcel_guest.py 2>&1)"; rc=$?
  arm "GREEN byte guest budgets, visibility and head boundaries" "$rc" 0 "$out" "5 legacy repairs / 176 steps"
  out="$(python3 scripts/probe_gc_parcel_guest.py --mutation byte-directives 2>&1)"; rc=$?
  arm "RED source directives follow byte PCs" "$rc" 1 "$out" "directives lost their byte PCs"
  out="$(python3 scripts/probe_gc_parcel_guest.py --mutation padded-image 2>&1)"; rc=$?
  arm "RED author image padding is caught" "$rc" 1 "$out" "byte guest image acquired padding"
  out="$(python3 scripts/probe_gc_parcel_guest.py --mutation source-end 2>&1)"; rc=$?
  arm "RED explicit budgets continue past source end" "$rc" 1 "$out" "explicit budget stopped at the source end"
  out="$(python3 scripts/probe_gc_parcel_guest.py --mutation fetch-count 2>&1)"; rc=$?
  arm "RED byte guest counts actual parcels" "$rc" 1 "$out" "byte guest lost actual parcel counts"
  out="$(python3 scripts/probe_gc_parcel_guest.py --mutation fault-retirement 2>&1)"; rc=$?
  arm "RED a delivered fetch fault does not retire" "$rc" 1 "$out" "fault boundary retired an instruction"
  out="$(python3 scripts/probe_gc_parcel_guest.py --mutation head-pending 2>&1)"; rc=$?
  arm "RED pending delivery precedes guest fetch" "$rc" 1 "$out" "pending interrupt fetched the instruction"
  out="$(python3 scripts/probe_gc_parcel_guest.py --mutation code-visibility 2>&1)"; rc=$?
  arm "RED the next fetch observes a code patch" "$rc" 1 "$out" "next parcel ignored the code patch"
  out="$(python3 scripts/probe_gc_parcel_guest.py --mutation unknown-valid 2>&1)"; rc=$?
  arm "RED unknown valid vocabulary refuses by name" "$rc" 1 "$out" "unknown valid vocabulary became an illegal trap"

  rm -rf "$t"
  printf 'GUEST-GEN --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

if [ "${1:-}" = "--self-test" ]; then
  self_test
  exit $?
fi

# Re-run the controls before judging: a check that no longer discriminates must refuse,
# not pass (the project-doctrine contract in scripts/check_doctrines.project.sh).
self_test >/dev/null 2>&1 || {
  echo "GUEST-GEN: REFUSED — the check does not discriminate (self-test failed)." >&2
  exit 2; }

out="$(python3 scripts/gen_guests.py --check --encoding "$ENCODING" \
      --guests-dir "$GUESTS_DIR" --out "$OUT" 2>&1)"; rc=$?
if [ "$rc" -eq 2 ]; then
  printf '%s\n' "$out" >&2
  echo "GUEST-GEN: REFUSED — the tracked guests could not be judged." >&2
  exit 2
fi
if [ "$rc" -ne 0 ]; then
  printf '%s\n' "$out" >&2
  printf 'GUEST-GEN: FAIL — %s is out of sync with the tracked guests and their expectations. Regenerate — never edit:\n  python3 scripts/gen_guests.py\n' \
    "$OUT" >&2
  exit 1
fi
printf 'GUEST-GEN: ok (%s matches the tracked guests)\n' "$OUT"

# ── the census's rv64gc pair (P4-SYSTEM.2 slice h, the route flip) ─────────────────────
out="$(python3 scripts/gen_guests.py --check --encoding "$ENCODING_GC" \
      --guests-dir "$GUESTS_DIR_GC" --image-format bytes --out "$OUT_GC" 2>&1)"; rc=$?
if [ "$rc" -eq 2 ]; then
  printf '%s\n' "$out" >&2
  echo "GUEST-GEN: REFUSED — the rv64gc tracked guests could not be judged." >&2
  exit 2
fi
if [ "$rc" -ne 0 ]; then
  printf '%s\n' "$out" >&2
  printf 'GUEST-GEN: FAIL — %s is out of sync with the tracked guests and their expectations. Regenerate — never edit:\n  python3 scripts/gen_guests.py --encoding %s --guests-dir %s --image-format bytes --out %s\n' \
    "$OUT_GC" "$ENCODING_GC" "$GUESTS_DIR_GC" "$OUT_GC" >&2
  exit 1
fi
printf 'GUEST-GEN: ok (%s matches the tracked guests)\n' "$OUT_GC"

# ── the base-mirror governor (defined above, beside the census variables) ──────────────
out="$(judge_mirror "$GUESTS_DIR" "$GUESTS_DIR_GC")" || {
  printf '%s\n' "$out" >&2
  exit 1
}
printf 'GUEST-GEN: ok (%s)\n' "$out"
exit 0
