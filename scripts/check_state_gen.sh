#!/usr/bin/env bash
# scripts/check_state_gen.sh — STATE-GEN (project doctrine).
#
# `crates/semulith-core/src/state.rs` is GENERATED from the profile's state descriptor by
# `scripts/gen_state.py` (P1-LAB.3; OWN-03: generated artifacts are changed by regeneration,
# never by direct editing, and identify their canonical input). This check regenerates the
# module in memory and refuses the day it stops byte-matching the committed file — a
# hand-edited accessor is how a descriptor and its executable half quietly become two facts.
#
# ⭐ WHAT THIS ACTUALLY PROTECTS: not tidiness — the DERIVATION. The descriptor is the
# authority; the module is its mirror. Both the module and the doctrine exist so that
# "generated" stays a claim with a governor (doctrine/fact_ownership.tsv names the pair).
#
# ⚠️ HONEST LIMIT: it proves the module is still the function of the descriptor bytes. It
# says nothing about whether the descriptor is TRUE — the descriptor has its own gates
# (RECORD-SCHEMA, PROFILE-CONSISTENCY) and the semantics have theirs (SEMANTICS).
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "STATE-GEN: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

STATE="profiles/rv64i-lab-v0/state.sexp"
ARITH="crates/semulith-core/src/arith.rs"
OUT="crates/semulith-core/src/state.rs"
# P4-SYSTEM.2 slice h (the route flip): the census's rv64gc owner→mirror pair.
STATE_GC="profiles/rv64gc-lab-v0/state.sexp"
OUT_GC="crates/semulith-core/src/state_rv64gc.rs"

# ── self-test ────────────────────────────────────────────────────────────────────────────────
SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }

self_test() {
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"

  # ⛔ STRICT ARITY (docs/knowledge/self-test-arms-that-never-ran.md): a missing `;` before
  # an arm call swallows it silently; the guard makes that a loud failure.
  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'STATE-GEN self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' \
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
      printf 'STATE-GEN self-test MISS: %s — expected rc=%s and no output, got rc=%s\n%s\n' \
        "$1" "$3" "$2" "$4" >&2
      return
    fi
    if [ "$2" = "$3" ] && printf '%s' "$4" | grep -qF "$5"; then
      pass=$((pass+1))
    else
      fail=$((fail+1))
      printf 'STATE-GEN self-test MISS: %s — expected rc=%s (reason: %s), got rc=%s\n%s\n' \
        "$1" "$3" "$5" "$2" "$4" >&2
    fi
  }

  cp "$STATE" "$t/state.sexp"; cp "$ARITH" "$t/arith.rs"

  # GREEN: the generator runs and emits a module from the real descriptor.
  out="$(python3 scripts/gen_state.py --state "$t/state.sexp" --arith "$t/arith.rs" \
        --out "$t/state.rs" 2>&1)"; rc=$?
  arm "GREEN the generator emits a module from the real descriptor" "$rc" 0 "$out" "wrote"

  # GREEN: the drift check passes on a faithful regeneration.
  out="$(python3 scripts/gen_state.py --check --state "$t/state.sexp" --arith "$t/arith.rs" \
        --out "$t/state.rs" 2>&1)"; rc=$?
  arm "GREEN a faithful regeneration is judged in sync" "$rc" 0 "$out" ""

  # RED: a hand-edit of the generated module is detected, named, and refused.
  printf '\n// hand edit\n' >> "$t/state.rs"
  out="$(python3 scripts/gen_state.py --check --state "$t/state.sexp" --arith "$t/arith.rs" \
        --out "$t/state.rs" 2>&1)"; rc=$?
  arm "RED a hand-edited module is refused, naming DRIFT" "$rc" 1 "$out" "DRIFT"

  # Descriptor surgery for the three RED arms below. `dossier_sexp.family_for` names the
  # family from the file NAME, so every case lives in its own directory as `state.sexp`.
  mkdir -p "$t/badxlen" "$t/mepc" "$t/nocensus"

  # RED: a descriptor that disagrees with the one XLEN owner is refused, naming both values.
  sed 's/(xlen 64)/(xlen 32)/' "$t/state.sexp" > "$t/badxlen/state.sexp"
  out="$(python3 scripts/gen_state.py --check --state "$t/badxlen/state.sexp" --arith "$t/arith.rs" \
        --out "$t/state.rs" 2>&1)"; rc=$?
  arm "RED a descriptor/arithmetic XLEN disagreement is refused, naming both" "$rc" 2 "$out" "xlen mismatch"

  # RED: a descriptor with a special register the generator has no mapping for is refused
  #    by name — new descriptor content is generator work, never silently guessed.
  sed 's/(id "pc")/(id "mepc")/' "$t/state.sexp" > "$t/mepc/state.sexp"
  out="$(python3 scripts/gen_state.py --check --state "$t/mepc/state.sexp" --arith "$t/arith.rs" \
        --out "$t/state.rs" 2>&1)"; rc=$?
  arm "RED an unmapped special register is refused by name" "$rc" 2 "$out" "'mepc'"

  # RED: a descriptor whose SEM-08 census went missing is refused, naming the census.
  python3 - "$t/state.sexp" "$t/nocensus/state.sexp" <<'PY'
import sys
text = open(sys.argv[1], encoding="utf-8").read()
start = text.index("(hidden_state_census")
depth = 0
for i in range(start, len(text)):
    if text[i] == "(":
        depth += 1
    elif text[i] == ")":
        depth -= 1
        if depth == 0:
            open(sys.argv[2], "w", encoding="utf-8").write(text[:start] + text[i + 1:])
            break
PY
  out="$(python3 scripts/gen_state.py --check --state "$t/nocensus/state.sexp" --arith "$t/arith.rs" \
        --out "$t/state.rs" 2>&1)"; rc=$?
  arm "RED a descriptor without its SEM-08 census is refused, naming it" "$rc" 2 "$out" "hidden_state_census"

  # RED: the P3-BREADTH.5 constructs (case dsp56300-lab-v0) are refused BY NAME at the
  # generator — the schema declares them, emitting them is generator work, and a declared
  # form must never be silently dropped. Each case lives in its own directory (family_for
  # names the family from the file NAME). The surgery appends one form before the state
  # form's closing paren.
  mkdir -p "$t/family" "$t/spaces" "$t/stack" "$t/noxlen"
  for case in family spaces stack; do
    python3 - "$t/state.sexp" "$t/$case/state.sexp" "$case" <<'PY'
import sys
text = open(sys.argv[1], encoding="utf-8").read()
forms = {
    "family": ' (register_family (id "acc") (count 2) (width_bits 56) (ids "a, b")'
              ' (authority architecture) (source "DSP56300FM §3.4.1"))',
    "spaces": ' (memory_spaces (space (id "x") (word_bits 24)'
              ' (authority architecture) (source "DSP56300FM §3.1")))',
    "stack":  ' (hardware_stack (levels 16) (width_bits 48)'
              ' (indexing "SP pre-increments; slot 0 unwritable")'
              ' (stale_slots_observable true) (authority architecture)'
              ' (source "DSP56300FM §5.4.3"))',
}
open(sys.argv[2], "w", encoding="utf-8").write(text.rstrip()[:-1] + forms[sys.argv[3]] + ")\n")
PY
  done
  out="$(python3 scripts/gen_state.py --check --state "$t/family/state.sexp" --arith "$t/arith.rs" \
        --out "$t/state.rs" 2>&1)"; rc=$?
  arm "RED a declared register_family is refused by name (F1)" "$rc" 2 "$out" "register_family declared"
  out="$(python3 scripts/gen_state.py --check --state "$t/spaces/state.sexp" --arith "$t/arith.rs" \
        --out "$t/state.rs" 2>&1)"; rc=$?
  arm "RED a declared memory_spaces is refused by name (F3)" "$rc" 2 "$out" "memory_spaces declared"
  out="$(python3 scripts/gen_state.py --check --state "$t/stack/state.sexp" --arith "$t/arith.rs" \
        --out "$t/state.rs" 2>&1)"; rc=$?
  arm "RED a declared hardware_stack is refused by name" "$rc" 2 "$out" "hardware_stack declared"

  # RED: a descriptor without xlen is refused — the generator binds to arith::XLEN, and a
  # missing binding is a Refusal, never a KeyError traceback.
  sed 's/ (xlen 64)//' "$t/state.sexp" > "$t/noxlen/state.sexp"
  out="$(python3 scripts/gen_state.py --check --state "$t/noxlen/state.sexp" --arith "$t/arith.rs" \
        --out "$t/state.rs" 2>&1)"; rc=$?
  arm "RED a descriptor without xlen is refused, naming the binding" "$rc" 2 "$out" "no xlen"

  # ---- the rv64gc branch (P4-SYSTEM.2 slice c1) -------------------------------------------------
  # A synthetic rv64gc descriptor — the real one is staged untracked until the route flip,
  # and a self-test must never depend on untracked content (fresh clones judge too).
  gc_state() { cat > "$t/gc/state.sexp" <<EOF
(state (profile_id "rv64gc-lab-v0") (xlen 64) (note "n")
  (integer_registers (count 32) (width_bits 64) (ids "x0..x31")
    (authority architecture) (source "s")
    (x0 (hardwired_zero true) (authority architecture) (source "s") (statement "x"))
    (named_by_the_isa_chapter (named-register (reg "x1") (role "r")
                               (authority software-convention) (source "s"))))
  (special_registers (register (id "pc") (width_bits 64) (holds "h")
                      (authority architecture) (source "s") (reset "r")
                      (reset_authority laboratory)))
  (privilege_mode (modes m) (modes s) (authority architecture) (source "s")
    (reset (value "m") (authority architecture) (source "s") (statement "x")))
  (csr (id "mstatus") (address 768) (width_bits 64) (authority architecture) (source "s")
    $1
    (reset (value "0") (authority laboratory) (source "s") (statement "x")))
  (csr (id "sstatus") (address 256) (width_bits 64) (view_of "mstatus")
    (authority architecture) (source "s")
    (reset (value "as mstatus") (authority laboratory) (source "s") (statement "x")))
  (hidden_state_census (question "q") (answer "No") (candidates (checked (candidate "c") (present false) (why "w"))) (consequence "c"))
)
EOF
  }
  mkdir -p "$t/gc"
  gc_state ''
  out="$(python3 scripts/gen_state.py --state "$t/gc/state.sexp" --arith "$t/arith.rs" \
        --out "$t/gc/state.rs" 2>&1)"; rc=$?
  arm "GREEN the rv64gc descriptor emits a module (mode + CSR storage + field tables)" "$rc" 0 "$out" "wrote"
  out="$(python3 scripts/gen_state.py --check --state "$t/gc/state.sexp" --arith "$t/arith.rs" \
        --out "$t/gc/state.rs" 2>&1)"; rc=$?
  arm "GREEN the rv64gc regeneration is judged in sync" "$rc" 0 "$out" ""

  # The slice-(h) census arms: the gate's judging loop covers the rv64gc owner→mirror
  # pair — pinned against the REAL pair, not a synthetic one.
  out="$(python3 scripts/gen_state.py --check --state "$STATE_GC" --arith "$ARITH" --out "$OUT_GC" 2>&1)"; rc=$?
  arm "GREEN the census's rv64gc pair is in sync" "$rc" 0 "$out" ""
  cp "$OUT_GC" "$t/gc-module.rs"; printf '\n// hand edit\n' >> "$t/gc-module.rs"
  out="$(python3 scripts/gen_state.py --check --state "$STATE_GC" --arith "$ARITH" --out "$t/gc-module.rs" 2>&1)"; rc=$?
  arm "RED the census's rv64gc pair catches a hand edit" "$rc" 1 "$out" "DRIFT"

  # RED: a csr without a reset is refused, named.
  python3 - "$t/gc/state.sexp" <<'PY'
import sys
p = sys.argv[1]
t = open(p).read()
t = t.replace('(reset (value "0") (authority laboratory) (source "s") (statement "x")))\n  (csr (id "sstatus")',
              ')\n  (csr (id "sstatus")', 1)
open(p, "w").write(t)
PY
  out="$(python3 scripts/gen_state.py --check --state "$t/gc/state.sexp" --arith "$t/arith.rs" \
        --out "$t/gc/state.rs" 2>&1)"; rc=$?
  arm "RED a csr without a reset is refused, named" "$rc" 2 "$out" "expected exactly one (reset"

  # RED: a view of an undeclared register is refused — a view of nothing reads nothing.
  gc_state "" ; sed -i.bak 's/(view_of "mstatus")/(view_of "nostatus")/' "$t/gc/state.sexp"
  out="$(python3 scripts/gen_state.py --check --state "$t/gc/state.sexp" --arith "$t/arith.rs" \
        --out "$t/gc/state.rs" 2>&1)"; rc=$?
  arm "RED a view of an undeclared csr is refused by name" "$rc" 2 "$out" "a view of nothing"

  # RED: per-field resets composing to a DIFFERENT value than the csr-level reset — the
  # two statements of one fact must agree (this RED fired NATURALLY on the real rv64gc
  # document while it was being authored: mstatus's composed UXL/SXL value caught a
  # hand-computed csr-level value; the arm makes it repeatable).
  gc_state '(field (id "all") (bit_hi 63) (bit_lo 0) (discipline warl) (legalize (any)) (reset "1") (reset_authority laboratory) (authority architecture) (source "s"))'
  out="$(python3 scripts/gen_state.py --check --state "$t/gc/state.sexp" --arith "$t/arith.rs" \
        --out "$t/gc/state.rs" 2>&1)"; rc=$?
  arm "RED field resets disagreeing with the csr-level reset are refused" "$rc" 2 "$out" "one reset, one value"

  # RED: the slice-(d) legalization mini-language's rules — a WARL field without a
  # (legalize …) is unemittable (the discipline names what it does NOT define), a WPRI
  # field carrying one contradicts itself, and a read-only constant disagreeing with the
  # field's reset is one constant stated twice.
  gc_state '(field (id "all") (bit_hi 63) (bit_lo 0) (discipline warl) (reset "0") (reset_authority laboratory) (authority architecture) (source "s"))'
  out="$(python3 scripts/gen_state.py --check --state "$t/gc/state.sexp" --arith "$t/arith.rs" \
        --out "$t/gc/state.rs" 2>&1)"; rc=$?
  arm "RED a WARL field without a (legalize …) is refused" "$rc" 2 "$out" "without a"
  gc_state '(field (id "all") (bit_hi 63) (bit_lo 0) (discipline wpri) (legalize (any)) (reset "0") (reset_authority laboratory) (authority architecture) (source "s"))'
  out="$(python3 scripts/gen_state.py --check --state "$t/gc/state.sexp" --arith "$t/arith.rs" \
        --out "$t/gc/state.rs" 2>&1)"; rc=$?
  arm "RED a WPRI field carrying a legalize is refused" "$rc" 2 "$out" "WPRI field carries no"
  gc_state '(field (id "all") (bit_hi 63) (bit_lo 0) (discipline warl) (legalize (read-only 2)) (reset "0") (reset_authority laboratory) (authority architecture) (source "s"))'
  out="$(python3 scripts/gen_state.py --check --state "$t/gc/state.sexp" --arith "$t/arith.rs" \
        --out "$t/gc/state.rs" 2>&1)"; rc=$?
  arm "RED a read-only constant disagreeing with the field's reset is refused" "$rc" 2 "$out" "one constant, stated once"

  # RED: two csrs at one address.
  gc_state "" ; sed -i.bak 's/(address 256)/(address 768)/' "$t/gc/state.sexp"
  out="$(python3 scripts/gen_state.py --check --state "$t/gc/state.sexp" --arith "$t/arith.rs" \
        --out "$t/gc/state.rs" 2>&1)"; rc=$?
  arm "RED a duplicate csr address is refused" "$rc" 2 "$out" "duplicate csr address"

  # RED: the privileged constructs under the WRONG profile id — rv64i keeps exactly its
  # old emission surface, and a csr there is generator work, named.
  mkdir -p "$t/gcwrong"
  python3 - "$t/state.sexp" "$t/gcwrong/state.sexp" <<'PY'
import sys
text = open(sys.argv[1]).read()
add = (' (csr (id "mstatus") (address 768) (width_bits 64) (authority architecture)'
       ' (source "s") (reset (value "0") (authority laboratory) (source "s")'
       ' (statement "x")))')
open(sys.argv[2], "w").write(text.rstrip()[:-1] + add + ")\n")
PY
  out="$(python3 scripts/gen_state.py --check --state "$t/gcwrong/state.sexp" --arith "$t/arith.rs" \
        --out "$t/state.rs" 2>&1)"; rc=$?
  arm "RED a csr declared under rv64i-lab-v0 is refused, named" "$rc" 2 "$out" "csr / privilege_mode declared under rv64i-lab-v0"

  rm -rf "$t"
  printf 'STATE-GEN --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

if [ "${1:-}" = "--self-test" ]; then
  self_test
  exit $?
fi

# Re-run the controls before judging: a check that no longer discriminates must refuse,
# not pass (the project-doctrine contract in scripts/check_doctrines.project.sh).
self_test >/dev/null 2>&1 || {
  echo "STATE-GEN: REFUSED — the check does not discriminate (self-test failed)." >&2
  exit 2; }

[ -f "$STATE" ] || { echo "STATE-GEN: ok (no state descriptor yet)"; exit 0; }

# The owner→mirror census: every tracked state descriptor and its generated module
# (P4-SYSTEM.2 slice h — the census extends to the rv64gc pair at the route flip).
judge_pair() { # $1 descriptor $2 module
  out="$(python3 scripts/gen_state.py --check --state "$1" --arith "$ARITH" --out "$2" 2>&1)" || {
    printf '%s\n' "$out" >&2
    printf 'STATE-GEN: FAIL — %s is out of sync with %s. Regenerate — never edit:\n  python3 scripts/gen_state.py\n' \
      "$2" "$1" >&2
    exit 1
  }
  sha="$(sha256sum "$1" | cut -d' ' -f1)"
  printf 'STATE-GEN: ok (%s matches %s, sha256 %s)\n' "$2" "$1" "${sha:0:16}"
}

judge_pair "$STATE" "$OUT"
judge_pair "$STATE_GC" "$OUT_GC"
exit 0
