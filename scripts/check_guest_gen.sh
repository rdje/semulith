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
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; tracked inputs
# are read-only; self-test output is retained under target/guest-gen; no network.
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
# With C unbound, every other mirrored file is byte-identical to its rv64i owner.
# The C bind migrates only independently checked parcel extents; other bytes stay governed.
ENCODING_GC="profiles/rv64gc-lab-v0/encoding.sexp"
GUESTS_DIR_GC="profiles/rv64gc-lab-v0/guests"
OUT_GC="crates/semulith-verify/src/guests_rv64gc.rs"
# The tracked governor owns the seven exceptions. With C composed, it derives all
# writes/request counts, then compares only the count-adjusted owner; every other
# byte stays governed. Three reviewed source annotation exceptions have exact
# owner/mirror pins and identical assembled images; all other sources stay exact.
judge_mirror() {
  python3 scripts/check_gc_mirror.py --owner "$1" --mirror "$2" --encoding "$ENCODING_GC"
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
  cp "$GUESTS_DIR_GC/bound-arith.expected.sexp" "$t/mirror/bound-arith.expected.sexp"
  # A comment-only exception keeps valid observations. In C mode its count must
  # remain independently derived, so this arm reaches the stale-record predicate.
  python3 - "$ENCODING_GC" "$GUESTS_DIR/dir-selfmod-fence.expected.sexp" "$t/mirror/dir-selfmod-fence.expected.sexp" <<'PYCODE'
import sys
from pathlib import Path
sys.path.insert(0, 'scripts')
import dossier_sexp as D
from expectations_text import with_fetches
from riscv_asm import Assembler
encoding, owner, mirror = map(Path, sys.argv[1:])
text = owner.read_bytes().decode('utf-8')
if 'c.nop' in Assembler(encoding).insns:
    prior = D.load_expectations(mirror)
    text = with_fetches(text, prior.get('fetches', prior['instructions']))
mirror.write_bytes(text.encode('utf-8'))
PYCODE
  out="$(judge_mirror "$GUESTS_DIR" "$t/mirror" 2>&1)"; rc=$?
  arm "RED a stale re-derivation record is named" "$rc" 1 "$out" "recorded re-derivation is stale after count normalization"

  out="$(python3 scripts/check_gc_mirror.py --self-test 2>&1)"; rc=$?
  arm "GREEN mirror migration checks extents and literal fields" "$rc" 0 "$out" "literal fields pass"
  out="$(python3 scripts/check_gc_mirror.py --self-test --mutation ignore-counts 2>&1)"; rc=$?
  arm "RED mirror migration cannot ignore request counts" "$rc" 1 "$out" "accepted declared parcel count"
  out="$(python3 scripts/check_gc_mirror.py --self-test --mutation ignore-noncount 2>&1)"; rc=$?
  arm "RED mirror migration cannot exempt other bytes" "$rc" 1 "$out" "accepted non-count mirror drift"
  out="$(python3 scripts/check_gc_mirror.py --self-test --mutation ignore-source 2>&1)"; rc=$?
  arm "RED mirror migration keeps source bytes exact" "$rc" 1 "$out" "accepted source mirror is not byte-identical"
  out="$(python3 scripts/check_gc_mirror.py --self-test --mutation ignore-stale 2>&1)"; rc=$?
  arm "RED parcel counts cannot preserve a stale exception" "$rc" 1 "$out" "accepted re-derivation is stale"
  out="$(python3 scripts/check_gc_mirror.py --self-test --mutation ignore-source-pins 2>&1)"; rc=$?
  arm "RED source annotations require exact reviewed pins" "$rc" 1 "$out" "accepted source re-derivation pins differ"
  out="$(python3 scripts/check_gc_mirror.py --self-test --mutation ignore-source-image 2>&1)"; rc=$?
  arm "RED reviewed source annotations cannot change instructions" "$rc" 1 "$out" "accepted source re-derivation changes assembled image"

  # P4-SYSTEM.12 d1: isolate the full C composition; the expected words and byte
  # image are hand-written spec-side fixtures, independent of the live corpus.
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
  out="$(python3 scripts/probe_gc_sail.py --mutation ignore-parcel-interrupt 2>&1)"; rc=$?
  arm "RED parcel interrupt annotations require their witnessed event" "$rc" 1 "$out" "missing expected step 0 (c.addi x10, 1)"

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
  out="$(python3 scripts/probe_gc_parcel_guest.py --cold 2>&1)"; rc=$?
  arm "GREEN parcel author controls use only tracked inputs" "$rc" 0 "$out" "tracked-only inputs and no reference cache passed"
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

  # e1a: the spec-side author honors fixed fields and privileged instruction legality.
  out="$(python3 scripts/probe_gc_privilege_author.py 2>&1)"; rc=$?
  arm "GREEN fixed misa and privileged author legality" "$rc" 0 "$out" "5 corpus repairs / 140 steps"
  out="$(python3 scripts/probe_gc_privilege_author.py --mutation misa-reset 2>&1)"; rc=$?
  arm "RED fixed misa reset is derived from the selected set" "$rc" 1 "$out" "misa lost the fixed selected reset"
  out="$(python3 scripts/probe_gc_privilege_author.py --mutation misa-write 2>&1)"; rc=$?
  arm "RED writes retain read-only misa fields" "$rc" 1 "$out" "misa accepted a write to read-only fields"
  out="$(python3 scripts/probe_gc_privilege_author.py --mutation csr-privilege 2>&1)"; rc=$?
  arm "RED CSR privilege failures suppress all own effects" "$rc" 1 "$out" "CSR privilege fault lost its unit discipline"
  out="$(python3 scripts/probe_gc_privilege_author.py --mutation satp-tvm 2>&1)"; rc=$?
  arm "RED S-mode satp access honors TVM" "$rc" 1 "$out" "S-mode satp ignored TVM"
  out="$(python3 scripts/probe_gc_privilege_author.py --mutation mret-mode 2>&1)"; rc=$?
  arm "RED MRET requires M-mode" "$rc" 1 "$out" "MRET below M popped the stack"
  out="$(python3 scripts/probe_gc_privilege_author.py --mutation sret-mode 2>&1)"; rc=$?
  arm "RED SRET refuses U-mode" "$rc" 1 "$out" "U-mode SRET popped the stack"
  out="$(python3 scripts/probe_gc_privilege_author.py --mutation sret-tsr 2>&1)"; rc=$?
  arm "RED S-mode SRET honors TSR" "$rc" 1 "$out" "S-mode SRET ignored TSR"
  out="$(python3 scripts/probe_gc_privilege_author.py --mutation sfence-mode 2>&1)"; rc=$?
  arm "RED SFENCE.VMA refuses U-mode" "$rc" 1 "$out" "U-mode SFENCE.VMA executed"
  out="$(python3 scripts/probe_gc_privilege_author.py --mutation sfence-tvm 2>&1)"; rc=$?
  arm "RED S-mode SFENCE.VMA honors TVM" "$rc" 1 "$out" "S-mode SFENCE.VMA ignored TVM"

  # P4-SYSTEM.13 c7a: nondelegated supervisor interrupt bits are read-only zero.
  out="$(python3 scripts/probe_gc_privilege_author.py --mutation sip-read-delegation 2>&1)"; rc=$?
  arm "RED sip hides undelegated pending sources" "$rc" 1 "$out" "sip delegation/owner read mismatch"
  out="$(python3 scripts/probe_gc_privilege_author.py --mutation sie-read-delegation 2>&1)"; rc=$?
  arm "RED sie hides undelegated enables" "$rc" 1 "$out" "sie exposed an undelegated bit"
  out="$(python3 scripts/probe_gc_privilege_author.py --mutation sip-write-delegation 2>&1)"; rc=$?
  arm "RED sip preserves undelegated pending sources" "$rc" 1 "$out" "sip wrote an undelegated bit"
  out="$(python3 scripts/probe_gc_privilege_author.py --mutation sie-write-delegation 2>&1)"; rc=$?
  arm "RED sie preserves undelegated enables" "$rc" 1 "$out" "sie wrote an undelegated bit"
  out="$(python3 scripts/probe_gc_privilege_author.py --mutation sip-owner 2>&1)"; rc=$?
  arm "RED sip reads its mip owner" "$rc" 1 "$out" "sip delegation/owner read mismatch"

  # e1b1: hand-encoded integer controls precede the expanded corpus derivation.
  out="$(python3 scripts/probe_gc_integer_author.py 2>&1)"; rc=$?
  arm "GREEN base integer author vocabulary" "$rc" 0 "$out" "17 corpus gaps / 476 steps"
  out="$(python3 scripts/probe_gc_integer_author.py --mutation sltiu-sign 2>&1)"; rc=$?
  arm "RED SLTIU extends before unsigned comparison" "$rc" 1 "$out" "SLTIU sign extension"
  out="$(python3 scripts/probe_gc_integer_author.py --mutation xlen-count 2>&1)"; rc=$?
  arm "RED XLEN register shifts use six count bits" "$rc" 1 "$out" "XLEN shift count"
  out="$(python3 scripts/probe_gc_integer_author.py --mutation word-count 2>&1)"; rc=$?
  arm "RED word register shifts use five count bits" "$rc" 1 "$out" "word shift count"
  out="$(python3 scripts/probe_gc_integer_author.py --mutation word-sign 2>&1)"; rc=$?
  arm "RED SRAW preserves the word sign" "$rc" 1 "$out" "word arithmetic shift"
  out="$(python3 scripts/probe_gc_integer_author.py --mutation sraw-count 2>&1)"; rc=$?
  arm "RED SRAW independently masks its register count" "$rc" 1 "$out" "SRAW five-bit count"
  out="$(python3 scripts/probe_gc_integer_author.py --mutation sraw-width 2>&1)"; rc=$?
  arm "RED SRAW truncates its source before arithmetic shift" "$rc" 1 "$out" "word arithmetic shift"
  out="$(python3 scripts/probe_gc_integer_author.py --mutation sraiw-width 2>&1)"; rc=$?
  arm "RED SRAIW truncates its source before arithmetic shift" "$rc" 1 "$out" "immediate word arithmetic shift"
  out="$(python3 scripts/probe_gc_integer_author.py --mutation branch-sign 2>&1)"; rc=$?
  arm "RED signed branches compare signed operands" "$rc" 1 "$out" "branch signed/unsigned decision"
  out="$(python3 scripts/probe_gc_integer_author.py --mutation load-sign 2>&1)"; rc=$?
  arm "RED narrow loads retain signed extension" "$rc" 1 "$out" "narrow load extension"
  out="$(python3 scripts/probe_gc_integer_author.py --mutation store-width 2>&1)"; rc=$?
  arm "RED byte stores preserve neighboring bytes" "$rc" 1 "$out" "narrow store width"
  out="$(python3 scripts/probe_gc_integer_author.py --mutation reserved-word 2>&1)"; rc=$?
  arm "RED reserved W shifts have no own effect" "$rc" 1 "$out" "reserved word shift acquired an effect"

  # e1b2: selected CSR enables and every literal string retain their own rules.
  out="$(python3 scripts/probe_gc_counter_author.py 2>&1)"; rc=$?
  arm "GREEN counter permissions and literal author text" "$rc" 0 "$out" "3 corpus refusals / 117 steps"
  out="$(python3 scripts/probe_gc_counter_author.py --mutation enable-mask 2>&1)"; rc=$?
  arm "RED counter enables retain selected WARL fields" "$rc" 1 "$out" "CSR enable legalization"
  out="$(python3 scripts/probe_gc_counter_author.py --mutation stce-mask 2>&1)"; rc=$?
  arm "RED menvcfg writes only STCE" "$rc" 1 "$out" "CSR enable legalization"
  out="$(python3 scripts/probe_gc_counter_author.py --mutation timer-tm 2>&1)"; rc=$?
  arm "RED S stimecmp requires TM" "$rc" 1 "$out" "stimecmp TM gate"
  out="$(python3 scripts/probe_gc_counter_author.py --mutation timer-stce 2>&1)"; rc=$?
  arm "RED S stimecmp requires STCE" "$rc" 1 "$out" "stimecmp STCE gate"
  out="$(python3 scripts/probe_gc_counter_author.py --mutation counter-enable 2>&1)"; rc=$?
  arm "RED counter access remains gated below M" "$rc" 1 "$out" "counter mode enable gate"
  out="$(python3 scripts/probe_gc_counter_author.py --mutation u-counter-enable 2>&1)"; rc=$?
  arm "RED U counter access requires the S enable too" "$rc" 1 "$out" "counter mode enable gate"
  out="$(python3 scripts/probe_gc_counter_author.py --mutation quote-text 2>&1)"; rc=$?
  arm "RED quoted annotations retain their literal text" "$rc" 1 "$out" "quoted directive lost literal text"
  out="$(python3 scripts/probe_gc_counter_author.py --mutation backslash-text 2>&1)"; rc=$?
  arm "RED backslash annotations retain their literal text" "$rc" 1 "$out" "backslash directive lost literal text"

  out="$(python3 scripts/probe_gc_counter_author.py --mutation stip-source 2>&1)"; rc=$?
  arm "RED STIP source follows STCE" "$rc" 1 "$out" "STIP source selection"
  out="$(python3 scripts/probe_gc_counter_author.py --mutation stip-fallback-write 2>&1)"; rc=$?
  arm "RED STCE-clear software STIP is writable" "$rc" 1 "$out" "STIP write mask"
  out="$(python3 scripts/probe_gc_counter_author.py --mutation stip-enabled-write 2>&1)"; rc=$?
  arm "RED STCE-enabled comparator STIP is read-only" "$rc" 1 "$out" "STIP write mask"
  out="$(python3 scripts/probe_gc_counter_author.py --mutation stip-retention 2>&1)"; rc=$?
  arm "RED comparator selection retains software pending" "$rc" 1 "$out" "STIP retained software storage"
  out="$(python3 scripts/probe_gc_counter_author.py --disable-sstc-witness 2>&1)"; rc=$?
  arm "RED a disabled Sstc witness misses the terminal trap control" "$rc" 1 "$out" "Sstc terminal control missed: disabled positive witness"

  # e1c1: independent selected cache policy, with no production engine oracle.
  out="$(python3 scripts/probe_gc_cache_author.py 2>&1)"; rc=$?
  arm "GREEN independent cache and cold repeat" "$rc" 0 "$out" "cached corpus exact and cold repeat"
  out="$(python3 scripts/probe_gc_cache_author.py --mutation bypass-hit 2>&1)"; rc=$?
  arm "RED cached mappings stay stale until a fence" "$rc" 1 "$out" "cache must retain stale mapping until fence"
  out="$(python3 scripts/probe_gc_cache_author.py --mutation fence-value 2>&1)"; rc=$?
  arm "RED VA scope uses register identity" "$rc" 1 "$out" "fence must use register identity and exact scope"
  out="$(python3 scripts/probe_gc_cache_author.py --mutation fence-asid-value 2>&1)"; rc=$?
  arm "RED ASID scope uses register identity" "$rc" 1 "$out" "fence must use register identity and exact scope"
  out="$(python3 scripts/probe_gc_cache_author.py --mutation global-inheritance 2>&1)"; rc=$?
  arm "RED ancestor G reaches the cached translation" "$rc" 1 "$out" "non-leaf G must propagate to cache entry"
  out="$(python3 scripts/probe_gc_cache_author.py --mutation asid-tag 2>&1)"; rc=$?
  arm "RED cache hits honor current ASID" "$rc" 1 "$out" "ASID change must be immediately visible"
  out="$(python3 scripts/probe_gc_cache_author.py --mutation cached-permission 2>&1)"; rc=$?
  arm "RED hits recheck live permissions" "$rc" 1 "$out" "cache hit must recheck live SUM"
  out="$(python3 scripts/probe_gc_cache_author.py --mutation fault-install 2>&1)"; rc=$?
  arm "RED faulting translations never install" "$rc" 1 "$out" "fault must not install cache entry"
  out="$(python3 scripts/probe_gc_cache_author.py --mutation fifo-hit 2>&1)"; rc=$?
  arm "RED hits leave FIFO age intact" "$rc" 1 "$out" "FIFO hit must not refresh replacement order"
  out="$(python3 scripts/probe_gc_cache_author.py --mutation fence-cursor 2>&1)"; rc=$?
  arm "RED fences leave FIFO cursor intact" "$rc" 1 "$out" "fence changed FIFO cursor"
  out="$(python3 scripts/probe_gc_cache_author.py --mutation asid-mask 2>&1)"; rc=$?
  arm "RED selected ASID ignores high bits" "$rc" 1 "$out" "fence must mask ASIDLEN without selecting x0 scope"
  out="$(python3 scripts/probe_gc_cache_author.py --mutation global-retention 2>&1)"; rc=$?
  arm "RED ASID fences preserve globals" "$rc" 1 "$out" "fence must use register identity and exact scope"
  out="$(python3 scripts/probe_gc_cache_author.py --mutation invalid-fence 2>&1)"; rc=$?
  arm "RED invalid VA fences have no effect" "$rc" 1 "$out" "invalid fence VA must have no effect"
  out="$(python3 scripts/probe_gc_cache_author.py --mutation illegal-fence 2>&1)"; rc=$?
  arm "RED illegal fences cannot touch the cache" "$rc" 1 "$out" "illegal fence must not change cache"

  out="$(python3 scripts/probe_gc_provenance.py 2>&1)"; rc=$?
  arm "GREEN new author provenance and historical captures" "$rc" 0 "$out" "GC provenance probe:"
  out="$(python3 scripts/probe_gc_provenance.py --mutation filename-history 2>&1)"; rc=$?
  arm "RED a borrowed name cannot inherit history" "$rc" 1 "$out" "generic output inherited FP provenance"
  out="$(python3 scripts/probe_gc_provenance.py --mutation parcel-history 2>&1)"; rc=$?
  arm "RED a parcel re-derivation cannot inherit history" "$rc" 1 "$out" "generic output inherited FP provenance"
  out="$(python3 scripts/probe_gc_provenance.py --mutation parcel-route 2>&1)"; rc=$?
  arm "RED parcel provenance must name its route" "$rc" 1 "$out" "new output omitted its execution route"
  out="$(python3 scripts/probe_gc_provenance.py --mutation fp-fallback 2>&1)"; rc=$?
  arm "RED generic output cannot inherit FP provenance" "$rc" 1 "$out" "generic output inherited FP provenance"

  out="$(python3 scripts/derive_gc_parcel_counts.py --self-test 2>&1)"; rc=$?
  arm "GREEN independent count fixtures and manifest drift" "$rc" 0 "$out" "GC count self-test:"
  out="$(python3 scripts/derive_gc_parcel_counts.py --out target/guest-gen/parcel-counts.json 2>&1)"; rc=$?
  arm "GREEN full historical parcel count census" "$rc" 0 "$out" "exact architectural traces;"
  out="$(python3 scripts/derive_gc_parcel_counts.py --mutation observation 2>&1)"; rc=$?
  arm "RED count adoption refuses changed observations" "$rc" 1 "$out" "architectural observations differ at boundary"
  out="$(python3 scripts/derive_gc_parcel_counts.py --mutation extent 2>&1)"; rc=$?
  arm "RED count adoption checks actual request log" "$rc" 1 "$out" "parcel count differs from actual request log"

  out="$(python3 scripts/probe_gc_owned_extent.py 2>&1)"; rc=$?
  arm "GREEN historical text survives the C extent migration" "$rc" 0 "$out" "write guard and explicit route pass"
  out="$(python3 scripts/probe_gc_owned_extent.py --mutation fresh-budget 2>&1)"; rc=$?
  arm "RED fresh owned records keep declared budgets" "$rc" 1 "$out" "fresh owned check"
  out="$(python3 scripts/probe_gc_owned_extent.py --mutation fresh-word-route 2>&1)"; rc=$?
  arm "RED fresh owned records keep parcel provenance" "$rc" 1 "$out" "fresh owned check"
  out="$(python3 scripts/probe_gc_owned_extent.py --mutation old-counts 2>&1)"; rc=$?
  arm "RED historical checks cannot retain word counts with C" "$rc" 1 "$out" "bound migrated historical check"
  out="$(python3 scripts/probe_gc_owned_extent.py --mutation parcel-prose 2>&1)"; rc=$?
  arm "RED extent migration keeps historical capture text" "$rc" 1 "$out" "bound migrated historical check"
  out="$(python3 scripts/probe_gc_owned_extent.py --mutation bad-request-log 2>&1)"; rc=$?
  arm "RED historical extent reconciles actual requests" "$rc" 1 "$out" "parcel extent differs from actual requests"
  out="$(python3 scripts/probe_gc_owned_extent.py --mutation permit-word-write 2>&1)"; rc=$?
  arm "RED default word route cannot overwrite a bound record" "$rc" 1 "$out" "canonical word write accepted"

  out="$(python3 scripts/stage_gc_c_corpus.py 2>&1)"; rc=$?
  arm "GREEN independent compressed corpus staging" "$rc" 0 "$out" "37 forms,"
  out="$(python3 scripts/stage_gc_c_corpus.py --check 2>&1)"; rc=$?
  arm "GREEN compressed corpus stages deterministically" "$rc" 0 "$out" "no production files written"
  out="$(python3 scripts/stage_gc_c_corpus.py --mutation observation 2>&1)"; rc=$?
  arm "RED staged compressed observations remain checked" "$rc" 1 "$out" "staged architectural observations differ"
  out="$(python3 scripts/stage_gc_c_corpus.py --mutation extent 2>&1)"; rc=$?
  arm "RED staged compressed extent remains checked" "$rc" 1 "$out" "staged extent differs from actual requests"

  out="$(python3 scripts/probe_riscv_toolchain.py 2>&1)"; rc=$?
  arm "GREEN pinned toolchain public selection" "$rc" 0 "$out" "Toolchain probe: 20/20 controls passed"
  out="$(python3 scripts/probe_riscv_toolchain.py --mutation ignore-version 2>&1)"; rc=$?
  arm "RED toolchain identity cannot be bypassed" "$rc" 1 "$out" "CONTROL-MISSED: C/wrong-clang"

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
SELF_TEST_LOG="$ROOT/target/guest-gen/self-test.log"
mkdir -p "$(dirname "$SELF_TEST_LOG")" || exit 2
self_test >"$SELF_TEST_LOG" 2>&1 || {
  python3 --version >&2
  tail -n 80 "$SELF_TEST_LOG" >&2
  echo "GUEST-GEN: REFUSED — the check does not discriminate (self-test failed)." >&2
  echo "GUEST-GEN: full self-test output is in target/guest-gen/self-test.log" >&2
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
