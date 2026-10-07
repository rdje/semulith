#!/usr/bin/env bash
# scripts/check_definition_gen.sh — DEF-GEN (project doctrine).
#
# `crates/semulith-core/src/definition.rs` is GENERATED from the unit's canonical
# definition by `scripts/gen_definition.py` (P1-LAB.6; OWN-03: generated artifacts are
# changed by regeneration, never by direct editing, and identify their canonical inputs,
# generator, configuration, and source fingerprints). This check regenerates the module
# in memory and refuses the day it stops byte-matching the committed file — a
# hand-edited decode table or effect tree is how the definition and its executable half
# quietly become two facts (OWN-01's duplicate owner, arriving as drift).
#
# ⭐ WHAT THIS ACTUALLY PROTECTS: not tidiness — the DERIVATION. The encoding data, the
# semantics data, and the state descriptor are the authorities; the module is their
# lowered mirror, carrying OWN-03's manifest so a reviewer can name the exact bytes and
# the exact generator behind every table. Both the module and the doctrine exist so
# "generated" stays a claim with a governor (doctrine/fact_ownership.tsv names the
# pairs).
#
# ⚠️ HONEST LIMIT: it proves the module is still the function of the input bytes. It
# says nothing about whether the DEFINITION is true — the semantics have their own gate
# (SEMANTICS: well-formed, complete, cited), and correctness is a differential
# experiment against a reference model (P1-LAB.8+), never a regeneration.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "DEF-GEN: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

ENCODING="profiles/rv64i-lab-v0/encoding.sexp"
STATE="profiles/rv64i-lab-v0/state.sexp"
OUT="crates/semulith-core/src/definition.rs"
# P4-SYSTEM.2 slice h (the route flip): the census's rv64gc owner→mirror pair.
ENCODING_GC="profiles/rv64gc-lab-v0/encoding.sexp"
STATE_GC="profiles/rv64gc-lab-v0/state.sexp"
OUT_GC="crates/semulith-core/src/definition_rv64gc.rs"

# ── self-test ────────────────────────────────────────────────────────────────────────────────
SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }

self_test() {
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"

  # The generator resolves fragments as <encoding's parent^3>/<fragment-root>, so the
  # surgical unit mirrors the real layout: tmp/profiles/<unit>/encoding.sexp composes
  # tmp/definitions/riscv/*. The state descriptor is fingerprinted, not read — the real
  # one answers.
  mkdir -p "$t/profiles/rv64i-lab-v0" "$t/definitions/riscv"
  cp "$ENCODING" "$t/profiles/rv64i-lab-v0/encoding.sexp"
  cp definitions/riscv/rv64i.sexp "$t/definitions/riscv/rv64i.sexp"
  cp definitions/riscv/rv64i.sem.sexp "$t/definitions/riscv/rv64i.sem.sexp"
  GEN() { python3 scripts/gen_definition.py --encoding "$t/profiles/rv64i-lab-v0/encoding.sexp" \
          --state "$STATE" --out "$t/definition.rs" "$@"; }

  # ⛔ STRICT ARITY (docs/knowledge/self-test-arms-that-never-ran.md): a missing `;` before
  # an arm call swallows it silently; the guard makes that a loud failure.
  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'DEF-GEN self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' \
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
      printf 'DEF-GEN self-test MISS: %s — expected rc=%s and no output, got rc=%s\n%s\n' \
        "$1" "$3" "$2" "$4" >&2
      return
    fi
    if [ "$2" = "$3" ] && printf '%s' "$4" | grep -qF "$5"; then
      pass=$((pass+1))
    else
      fail=$((fail+1))
      printf 'DEF-GEN self-test MISS: %s — expected rc=%s (reason: %s), got rc=%s\n%s\n' \
        "$1" "$3" "$5" "$2" "$4" >&2
    fi
  }

  # GREEN: the generator emits a module from the real definition.
  out="$(GEN 2>&1)"; rc=$?
  arm "GREEN the generator emits a module from the real definition" "$rc" 0 "$out" "wrote"

  # GREEN: the drift check passes on a faithful regeneration.
  out="$(GEN --check 2>&1)"; rc=$?
  arm "GREEN a faithful regeneration is judged in sync" "$rc" 0 "$out" ""

  # RED: a hand-edit of the generated module is detected, named, and refused.
  printf '\n// hand edit\n' >> "$t/definition.rs"
  out="$(GEN --check 2>&1)"; rc=$?
  arm "RED a hand-edited module is refused, naming DRIFT" "$rc" 1 "$out" "DRIFT"

  # RED: a unit with an instruction length this generator cannot emit is refused by name.
  sed 's/(ilen 32)/(ilen 64)/' "$ENCODING" > "$t/profiles/rv64i-lab-v0/encoding.sexp"
  out="$(GEN --check 2>&1)"; rc=$?
  arm "RED an unsupported instruction length is refused by name" "$rc" 2 "$out" "ilen 64"
  cp "$ENCODING" "$t/profiles/rv64i-lab-v0/encoding.sexp"

  # RED: a unit other than the laboratory profile is refused by name.
  sed 's/(profile "rv64i-lab-v0")/(profile "rv64i-other-v0")/' "$ENCODING" \
    > "$t/profiles/rv64i-lab-v0/encoding.sexp"
  out="$(GEN --check 2>&1)"; rc=$?
  arm "RED another unit is refused by name" "$rc" 2 "$out" "rv64i-other-v0"
  cp "$ENCODING" "$t/profiles/rv64i-lab-v0/encoding.sexp"

  # RED: an instruction the semantics do not cover is refused, naming the instruction.
  python3 - "$t/definitions/riscv/rv64i.sexp" <<'PY'
import sys
path = sys.argv[1]
text = open(path, encoding="utf-8").read()
add = '(insn (name add) (fixed (31 25 0x0) (14 12 0x0) (6 2 0xc) (1 0 0x3)) (operands rd rs1 rs2) (from "rv_i"))'
assert add in text
ghost = add.replace('(name add)', '(name zzz9)')
open(path, "w", encoding="utf-8").write(text.replace(add, add + "\n  " + ghost))
PY
  out="$(GEN --check 2>&1)"; rc=$?
  arm "RED an encoding instruction without semantics is refused, naming it" "$rc" 2 "$out" "zzz9"
  cp definitions/riscv/rv64i.sexp "$t/definitions/riscv/rv64i.sexp"

  # RED: a semantics rule referencing an operand the encoding does not provide is refused.
  sed 's/(add (reg rs1) (reg rs2))/(add (reg rs1) (reg rs3))/' definitions/riscv/rv64i.sem.sexp \
    > "$t/definitions/riscv/rv64i.sem.sexp"
  out="$(GEN --check 2>&1)"; rc=$?
  arm "RED an undeclared operand reference is refused, naming it" "$rc" 2 "$out" "'rs3'"
  cp definitions/riscv/rv64i.sem.sexp "$t/definitions/riscv/rv64i.sem.sexp"

  # RED: an instruction declaring an operand that names no field is refused, naming it —
  # extraction for it would be silent, and silence is the guessed translation
  # ARCHITECTURE §2 forbids (P3-BREADTH.2).
  python3 - "$t/definitions/riscv/rv64i.sexp" <<'PY'
import sys
path = sys.argv[1]
text = open(path, encoding="utf-8").read()
add = '(insn (name add) (fixed (31 25 0x0) (14 12 0x0) (6 2 0xc) (1 0 0x3)) (operands rd rs1 rs2) (from "rv_i"))'
assert add in text
open(path, "w", encoding="utf-8").write(
    text.replace(add, add.replace("(operands rd rs1 rs2)", "(operands rd rs1 rs2 rs9)")))
PY
  out="$(GEN --check 2>&1)"; rc=$?
  arm "RED an operand naming no field is refused, naming it" "$rc" 2 "$out" "rs9"
  cp definitions/riscv/rv64i.sexp "$t/definitions/riscv/rv64i.sexp"

  # RED: a fragment whose semantics document is missing is refused, naming the pairing.
  rm "$t/definitions/riscv/rv64i.sem.sexp"
  out="$(GEN --check 2>&1)"; rc=$?
  arm "RED a fragment without its semantics document is refused" "$rc" 2 "$out" "no semantics document"

  # ---- the rv64gc branch (P4-SYSTEM.2 slice d) -------------------------------------------------
  # (the previous arm removed the rv64i sem file; restore it before the rv64gc setup)
  cp definitions/riscv/rv64i.sem.sexp "$t/definitions/riscv/rv64i.sem.sexp"
  # GREEN: the staged rv64gc composition emits the extended module — three separate
  # (extensions …) forms (the shape the dropped-form regression hid), the pseudo rows
  # landing as PSEUDOS metadata, and the privileged operator variants in the Sem enum.
  mkdir -p "$t/gc/profiles/rv64gc-lab-v0" "$t/gc/definitions"
  cp -r "$t/definitions/riscv" "$t/gc/definitions/riscv"
  for f in zicsr zicntr system; do
    cp "definitions/riscv/$f.sexp" "$t/gc/definitions/riscv/$f.sexp"
    cp "definitions/riscv/$f.sem.sexp" "$t/gc/definitions/riscv/$f.sem.sexp"
  done
  cat > "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp" <<EOF
(encoding (profile "rv64gc-lab-v0") (ilen 32)
  (compose (base "riscv/rv64i")
    (extensions "riscv/zicsr") (extensions "riscv/zicntr") (extensions "riscv/system")
    (status partial) (slot (id m) (requires "riscv/m")))
  (fragment-root "definitions"))
EOF
  out="$(python3 scripts/gen_definition.py --encoding "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp" \
        --state "$STATE" --out "$t/gc-definition.rs" 2>&1)"; rc=$?
  arm "GREEN the rv64gc composition emits the extended module" "$rc" 0 "$out" "wrote"
  for needle in "TrapDeliver" "CsrRead" "Xret" "static PSEUDOS"; do
    grep -qF "$needle" "$t/gc-definition.rs"; rc=$?
    arm "GREEN the emitted module carries $needle" "$rc" 0 "" ""
  done
  # RED: a privileged operator in an RV64I rule is refused, named — the rv64i module's
  # byte surface is frozen, so the refusal is the honest verdict there. Rewrite the fence
  # rule to query (mode) in the rv64i surgical copy (a fresh encoding copy: the earlier
  # arms mutated the first).
  cp "$ENCODING" "$t/profiles/rv64i-lab-v0/encoding.sexp"
  sed 's/(effect (nop))/(effect (if (eq (mode) (lit 3)) (nop) (nop)))/' \
    "$t/definitions/riscv/rv64i.sem.sexp" > "$t/x" && mv "$t/x" "$t/definitions/riscv/rv64i.sem.sexp"
  out="$(GEN 2>&1)"; rc=$?
  arm "RED a privileged operator in a base rule is refused where not lowered" "$rc" 2 "$out" "does not lower"

  # ---- the A-extension operator surface (P4-SYSTEM.4 slice b) ------------------------------
  # The A variants emit exactly when the composition composes riscv/a: the tracked rv64gc
  # module (the slot still declared) keeps its byte surface, and the composition WITH the
  # fragment proves the lowering — the same discipline as the privileged operators off the
  # rv64i module.
  cp definitions/riscv/a.sexp "$t/gc/definitions/riscv/a.sexp"
  cp definitions/riscv/a.sem.sexp "$t/gc/definitions/riscv/a.sem.sexp"
  cat > "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp" <<EOF
(encoding (profile "rv64gc-lab-v0") (ilen 32)
  (compose (base "riscv/rv64i")
    (extensions "riscv/zicsr") (extensions "riscv/zicntr") (extensions "riscv/system")
    (extensions "riscv/a")
    (status partial) (slot (id m) (requires "riscv/m")))
  (fragment-root "definitions"))
EOF
  out="$(python3 scripts/gen_definition.py --encoding "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp" \
        --state "$STATE" --out "$t/gc-a-definition.rs" 2>&1)"; rc=$?
  arm "GREEN the rv64gc+A composition emits the A-operator module" "$rc" 0 "$out" "wrote"
  for needle in "LoadReserved" "StoreConditional" "Amo(u64"; do
    grep -qF "$needle" "$t/gc-a-definition.rs"; rc=$?
    arm "GREEN the emitted module carries $needle" "$rc" 0 "" ""
  done
  # RED: an amo operation literal the composition does not encode is refused, named — the
  # closed set is derived from the composed encodings' own funct5 fixed bits, never typed.
  sed 's/(amo (lit 0) (lit 32)/(amo (lit 3) (lit 32)/' definitions/riscv/a.sem.sexp \
    > "$t/gc/definitions/riscv/a.sem.sexp"
  out="$(python3 scripts/gen_definition.py --encoding "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp" \
        --state "$STATE" --out "$t/gc-a-definition.rs" 2>&1)"; rc=$?
  arm "RED an amo op outside the closed Zaamo nine is refused, naming it" "$rc" 2 "$out" "not one of the closed Zaamo nine"
  cp definitions/riscv/a.sem.sexp "$t/gc/definitions/riscv/a.sem.sexp"
  # RED: an A operator where the composition does not compose riscv/a is refused, named —
  # the variants emit WITH the fragment; a module carrying them without it would not
  # compile against its evaluator.
  grep -v 'extensions "riscv/a"' "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp" \
    > "$t/gc/enc-noa.sexp" && mv "$t/gc/enc-noa.sexp" "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp"
  sed 's/(tlb-invalidate (reg rs1) (reg rs2))/(set (reg rs1) (store-conditional (lit 32) (reg rs1) (reg rs2)))/' \
    definitions/riscv/system.sem.sexp > "$t/gc/definitions/riscv/system.sem.sexp"
  out="$(python3 scripts/gen_definition.py --encoding "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp" \
        --state "$STATE" --out "$t/gc-a-definition.rs" 2>&1)"; rc=$?
  arm "RED an A operator without riscv/a composed is refused, named" "$rc" 2 "$out" "does not compose riscv/a"
  cp definitions/riscv/system.sem.sexp "$t/gc/definitions/riscv/system.sem.sexp"

  # ---- the floating-point operator surface (P4-SYSTEM.7 slice c3) --------------------------
  # The F variants emit exactly when the composition composes riscv/f — the A discipline:
  # the tracked rv64gc module keeps its byte surface until the F bind (slice c6), and the
  # staged composition WITH the fragment proves the lowering.
  cp definitions/riscv/f.sexp "$t/gc/definitions/riscv/f.sexp"
  cp definitions/riscv/f.sem.sexp "$t/gc/definitions/riscv/f.sem.sexp"
  cat > "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp" <<EOF
(encoding (profile "rv64gc-lab-v0") (ilen 32)
  (compose (base "riscv/rv64i")
    (extensions "riscv/zicsr") (extensions "riscv/zicntr") (extensions "riscv/system")
    (extensions "riscv/f")
    (status partial) (slot (id m) (requires "riscv/m")))
  (fragment-root "definitions"))
EOF
  out="$(python3 scripts/gen_definition.py --encoding "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp" \
        --state "$STATE" --out "$t/gc-f-definition.rs" 2>&1)"; rc=$?
  arm "GREEN the rv64gc+F composition emits the floating-point module" "$rc" 0 "$out" "wrote"
  for needle in "FReg(&'static str)" "Rounding(&'static Sem)" "FMadd(u8" "FToI(u8, u8, bool" "Sem::FUnbox("; do
    grep -qF "$needle" "$t/gc-f-definition.rs"; rc=$?
    arm "GREEN the emitted module carries $needle" "$rc" 0 "" ""
  done
  # RED: an FP rule whose encoding carries rm but which never resolves it is refused —
  # check_semantics.check_fp, re-derived by the generator that emits the table.
  sed 's/(fadd 32 (rounding (field rm))/(fadd 32 (lit 0)/' definitions/riscv/f.sem.sexp \
    > "$t/gc/definitions/riscv/f.sem.sexp"
  out="$(python3 scripts/gen_definition.py --encoding "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp" \
        --state "$STATE" --out "$t/gc-f-definition.rs" 2>&1)"; rc=$?
  arm "RED an FP rule that never resolves its rm is refused, naming it" "$rc" 2 "$out" "never resolves it through (rounding (field rm))"
  cp definitions/riscv/f.sem.sexp "$t/gc/definitions/riscv/f.sem.sexp"
  # RED: an FP operator where the composition does not compose riscv/f is refused, named.
  grep -v 'extensions "riscv/f"' "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp" \
    > "$t/gc/enc-nof.sexp" && mv "$t/gc/enc-nof.sexp" "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp"
  sed 's/(tlb-invalidate (reg rs1) (reg rs2))/(set (reg rs1) (fclass 32 (reg rs2)))/' \
    definitions/riscv/system.sem.sexp > "$t/gc/definitions/riscv/system.sem.sexp"
  out="$(python3 scripts/gen_definition.py --encoding "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp" \
        --state "$STATE" --out "$t/gc-f-definition.rs" 2>&1)"; rc=$?
  arm "RED an FP operator without riscv/f composed is refused, named" "$rc" 2 "$out" "does not compose riscv/f"
  cp definitions/riscv/system.sem.sexp "$t/gc/definitions/riscv/system.sem.sexp"

  # ---- the D format conversion (P4-SYSTEM.7 slice d2) ---------------------------------------
  # FToF emits exactly when the composition composes riscv/d (the D bind, slice d5); the
  # staged composition WITH F and D proves the lowering of all 32 D rules.
  cp definitions/riscv/d.sexp "$t/gc/definitions/riscv/d.sexp"
  cp definitions/riscv/d.sem.sexp "$t/gc/definitions/riscv/d.sem.sexp"
  cat > "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp" <<EOF
(encoding (profile "rv64gc-lab-v0") (ilen 32)
  (compose (base "riscv/rv64i")
    (extensions "riscv/zicsr") (extensions "riscv/zicntr") (extensions "riscv/system")
    (extensions "riscv/f") (extensions "riscv/d")
    (status partial) (slot (id m) (requires "riscv/m")))
  (fragment-root "definitions"))
EOF
  out="$(python3 scripts/gen_definition.py --encoding "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp" \
        --state "$STATE" --out "$t/gc-d-definition.rs" 2>&1)"; rc=$?
  arm "GREEN the rv64gc+F+D composition emits the double-precision module" "$rc" 0 "$out" "wrote"
  for needle in "FToF(u8, u8, &'static Sem, &'static Sem)" "Sem::FToF(" "\"fcvt.d.s\""; do
    grep -qF "$needle" "$t/gc-d-definition.rs"; rc=$?
    arm "GREEN the emitted module carries $needle" "$rc" 0 "" ""
  done
  # RED: the format conversion where the composition does not compose riscv/d is refused.
  # F stays composed: the refusal is D's own, not the F surface's.
  sed 's/(extensions "riscv\/f") (extensions "riscv\/d")/(extensions "riscv\/f")/' \
    "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp" > "$t/gc/enc-nod.sexp" \
    && mv "$t/gc/enc-nod.sexp" "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp"
  grep -q 'extensions "riscv/f"' "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp"; rc=$?
  arm "GREEN the no-D composition still composes riscv/f" "$rc" 0 "" ""
  sed 's/(tlb-invalidate (reg rs1) (reg rs2))/(set (reg rs1) (f2f 32 64 (reg rs1) (reg rs2)))/' \
    definitions/riscv/system.sem.sexp > "$t/gc/definitions/riscv/system.sem.sexp"
  out="$(python3 scripts/gen_definition.py --encoding "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp" \
        --state "$STATE" --out "$t/gc-d-definition.rs" 2>&1)"; rc=$?
  arm "RED the format conversion without riscv/d composed is refused, named" "$rc" 2 "$out" "does not compose riscv/d"
  cp definitions/riscv/system.sem.sexp "$t/gc/definitions/riscv/system.sem.sexp"

  # ---- the M operators (P4-SYSTEM.11 slice a) ------------------------------------------------
  # The eight variants emit exactly when the composition composes riscv/m (the M bind, slice b);
  # the staged composition WITH M proves the lowering of all 13 M rules.
  cp definitions/riscv/m.sexp "$t/gc/definitions/riscv/m.sexp"
  cp definitions/riscv/m.sem.sexp "$t/gc/definitions/riscv/m.sem.sexp"
  cat > "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp" <<EOF
(encoding (profile "rv64gc-lab-v0") (ilen 32)
  (compose (base "riscv/rv64i")
    (extensions "riscv/zicsr") (extensions "riscv/zicntr") (extensions "riscv/system")
    (extensions "riscv/m")
    (status partial) (slot (id c) (requires "riscv/c")))
  (fragment-root "definitions"))
EOF
  out="$(python3 scripts/gen_definition.py --encoding "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp" \
        --state "$STATE" --out "$t/gc-m-definition.rs" 2>&1)"; rc=$?
  arm "GREEN the rv64gc+M composition emits the multiply/divide module" "$rc" 0 "$out" "wrote"
  for needle in "Mul(&'static Sem, &'static Sem)" "Sem::DivU(" "Sem::MulHsu(" "\"remuw\""; do
    grep -qF "$needle" "$t/gc-m-definition.rs"; rc=$?
    arm "GREEN the emitted module carries $needle" "$rc" 0 "" ""
  done
  # RED: an unguarded division is refused by the generator too (the semantics checker's
  # domain rule, re-derived where the executable table is emitted).
  sed 's/(set (reg rd) (div (reg rs1) (reg rs2)))/(set (reg rd) (div (reg rs1) (reg rs1)))/' \
    definitions/riscv/m.sem.sexp > "$t/gc/definitions/riscv/m.sem.sexp"
  out="$(python3 scripts/gen_definition.py --encoding "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp" \
        --state "$STATE" --out "$t/gc-m-definition.rs" 2>&1)"; rc=$?
  arm "RED a division its guard does not cover is refused, naming its divisor" "$rc" 2 "$out" "(div … (reg rs1)) is reached where its divisor may be zero"
  cp definitions/riscv/m.sem.sexp "$t/gc/definitions/riscv/m.sem.sexp"
  # RED: an M operator where the composition does not compose riscv/m is refused, named.
  sed 's/    (extensions "riscv\/m")//' "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp" > "$t/gc/enc-nom.sexp" \
    && mv "$t/gc/enc-nom.sexp" "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp"
  grep -q 'extensions "riscv/m"' "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp"; rc=$?
  arm "GREEN the no-M composition composes no riscv/m" "$rc" 1 "" ""
  sed 's/(tlb-invalidate (reg rs1) (reg rs2))/(set (reg rs1) (mul (reg rs1) (reg rs2)))/' \
    definitions/riscv/system.sem.sexp > "$t/gc/definitions/riscv/system.sem.sexp"
  out="$(python3 scripts/gen_definition.py --encoding "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp" \
        --state "$STATE" --out "$t/gc-m-definition.rs" 2>&1)"; rc=$?
  arm "RED an M operator without riscv/m composed is refused, named" "$rc" 2 "$out" "does not compose riscv/m"
  cp definitions/riscv/system.sem.sexp "$t/gc/definitions/riscv/system.sem.sexp"

  # ---- C expansions (P4-SYSTEM.12 slice b) -------------------------------------------------
  # C stays unbound in the real unit. Its lowering is proved on a disposable composition,
  # including compiled Rust decoding and independent operand/immediate-limit expectations.
  cp definitions/riscv/*.sexp "$t/gc/definitions/riscv/"
  sed 's/(slot (id c) (requires "riscv\/c"))/(extensions "riscv\/c")/' "$ENCODING_GC" \
    > "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp"
  CGEN() { python3 scripts/gen_definition.py --encoding "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp" \
      --state "$STATE_GC" --out "$t/c-definition.rs"; }
  CPROBE() { python3 scripts/probe_c_expansions.py "$t/gc/profiles/rv64gc-lab-v0/encoding.sexp" \
      "$t/c-definition.rs"; }
  out="$(CGEN 2>&1)"; rc=$?
  arm "GREEN the full composition with C emits expansion metadata" "$rc" 0 "$out" "wrote"
  out="$(CPROBE 2>&1)"; rc=$?
  [ "$rc" -ne 0 ] || printf '%s\n' "$out"
  arm "GREEN C's spec-side mappings and compiled specialization decoder" "$rc" 0 "$out" "compiled decoder 8/8"
  python3 - "$t/c-definition.rs" <<'PY'
import re, sys
from pathlib import Path
p = Path(sys.argv[1]); text = p.read_text()
begin = text.index('pub static INSNS: &[InsnDef] = &[\n') + len('pub static INSNS: &[InsnDef] = &[\n')
end = text.index('\n];', begin)
rows = re.split(r'(?=^    InsnDef \{)', text[begin:end], flags=re.M)
p.write_text(text[:begin] + ''.join(reversed([row for row in rows if row])) + text[end:])
PY
  out="$(CPROBE 2>&1)"; rc=$?
  arm "RED reversing specificity makes the compiled decoder fail" "$rc" 1 "$out" "specialization_decode"
  # RED: the mapper's spec-side expectation catches a plausible but wrong compact-register
  # offset. Generation itself succeeds: this tests correctness beyond shape/arity checks.
  sed 's/(field rd_p) (lit 8)/(field rd_p) (lit 9)/g' definitions/riscv/c.sem.sexp \
    > "$t/gc/definitions/riscv/c.sem.sexp"
  out="$(CGEN 2>&1)"; rc=$?
  arm "GREEN a well-formed wrong C mapping still generates" "$rc" 0 "$out" "wrote"
  out="$(CPROBE 2>&1)"; rc=$?
  arm "RED a wrong compact-register mapping is caught independently" "$rc" 1 "$out" "c.addi4spn: rd=16, expected 15"
  cp definitions/riscv/c.sem.sexp "$t/gc/definitions/riscv/c.sem.sexp"
  # RED: exact operand binding is re-judged at generation, not trusted from SEMANTICS.
  sed 's/(operand (name rd) (value (lit 0))) (operand (name jimm20)/(operand (name jimm20)/' \
    definitions/riscv/c.sem.sexp > "$t/gc/definitions/riscv/c.sem.sexp"
  out="$(CGEN 2>&1)"; rc=$?
  arm "RED an unbound base operand is refused by generation" "$rc" 2 "$out" "c.j: binds"
  cp definitions/riscv/c.sem.sexp "$t/gc/definitions/riscv/c.sem.sexp"

  # The slice-(h) census arms: the gate's judging loop covers the rv64gc owner→mirror
  # pair — pinned against the REAL pair, not a synthetic one.
  out="$(python3 scripts/gen_definition.py --check --encoding "$ENCODING_GC" --state "$STATE_GC" \
        --out "$OUT_GC" 2>&1)"; rc=$?
  arm "GREEN the census's rv64gc pair is in sync" "$rc" 0 "$out" ""
  cp "$OUT_GC" "$t/gc-module.rs"; printf '\n// hand edit\n' >> "$t/gc-module.rs"
  out="$(python3 scripts/gen_definition.py --check --encoding "$ENCODING_GC" --state "$STATE_GC" \
        --out "$t/gc-module.rs" 2>&1)"; rc=$?
  arm "RED the census's rv64gc pair catches a hand edit" "$rc" 1 "$out" "DRIFT"

  rm -rf "$t"
  printf 'DEF-GEN --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

if [ "${1:-}" = "--self-test" ]; then
  self_test
  exit $?
fi

# Re-run the controls before judging: a check that no longer discriminates must refuse,
# not pass (the project-doctrine contract in scripts/check_doctrines.project.sh).
self_test >/dev/null 2>&1 || {
  echo "DEF-GEN: REFUSED — the check does not discriminate (self-test failed)." >&2
  exit 2; }

[ -f "$ENCODING" ] || { echo "DEF-GEN: ok (no encoding composition yet)"; exit 0; }

# The owner→mirror census: every tracked encoding composition (+ its state descriptor)
# and its generated module (P4-SYSTEM.2 slice h — the census extends to the rv64gc pair
# at the route flip).
judge_pair() { # $1 encoding $2 state $3 module
  out="$(python3 scripts/gen_definition.py --check --encoding "$1" --state "$2" \
        --out "$3" 2>&1)"; rc=$?
  if [ "$rc" -eq 2 ]; then
    printf '%s\n' "$out" >&2
    echo "DEF-GEN: REFUSED — the canonical definition could not be judged." >&2
    exit 2
  fi
  if [ "$rc" -ne 0 ]; then
    printf '%s\n' "$out" >&2
    printf 'DEF-GEN: FAIL — %s is out of sync with the canonical definition. Regenerate — never edit:\n  python3 scripts/gen_definition.py\n' \
      "$3" >&2
    exit 1
  fi
  sha="$(sha256sum "$1" | cut -d' ' -f1)"
  printf 'DEF-GEN: ok (%s matches the canonical definition, encoding sha256 %s)\n' "$3" "${sha:0:16}"
}

judge_pair "$ENCODING" "$STATE" "$OUT"
judge_pair "$ENCODING_GC" "$STATE_GC" "$OUT_GC"
exit 0
