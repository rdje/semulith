#!/usr/bin/env bash
# scripts/check_exercise_coverage.sh — EXERCISE-COVERAGE (project doctrine).
#
# P2-SCALAR.1's acceptance, mechanized: every RV64I form the profile DECLARES in its scope is
# EXECUTED by at least one tracked guest — coverage reported with its denominator, never as a
# bare count. The denominator is the profile dossier's `[scope]` mnemonic lists (count_total
# re-derived against them — a declaration whose count disagrees with its own enumeration is a
# DENOMINATOR LIE). The numerator is the union of mnemonics the tracked expectation documents
# declare executed; the commit gate (the verify-side offline differential) already proves those
# exact steps execute, so "declared executed" and "executed" cannot drift apart silently.
#
# SCP-02 rides the same verdict: the unit's encoding composition is resolved through the ONE
# shared resolver (`riscv_asm.resolve_composition`), so an unmet `requires` or a missing
# fragment is refused by name, and every declared form must exist in the resolved composition —
# a scope entry the composition cannot provide is an unresolved dependency, not a feature.
#
# ⛔ Composes with EXTRACTION, does not duplicate it: EXTRACTION proves every declared
# instruction HAS encoding+semantics+requirement (static sufficiency); this gate proves every
# declared form RAN under the laboratory (dynamic exercise). A model can pass one and fail the
# other in both directions.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "EXERCISE-COVERAGE: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

check_coverage() { # $1 = root; $2 = "git" (tracked only) or "fs"
python3 - "$1" "$2" <<'PY'
import subprocess, sys
from pathlib import Path

root = Path(sys.argv[1]); mode = sys.argv[2]
sys.path.insert(0, "scripts")
import sexp as S
from riscv_asm import resolve_composition, AsmError

if mode == "git":
    out = subprocess.run(["git", "ls-files", "--", "profiles/*/profile.sexp"],
                         capture_output=True, text=True, check=True).stdout
    profiles = [root / p for p in out.splitlines() if p.strip()]
else:
    profiles = sorted(root.glob("profiles/*/profile.sexp"))

if not profiles:
    print("EXERCISE-COVERAGE: REFUSED — no tracked profile dossier found; this check cannot judge")
    print("__CHECKED__ 0"); sys.exit(2)

findings, checked = [], 0
for prof_path in profiles:
    pdir = prof_path.parent
    tag = prof_path.relative_to(root).as_posix()
    try:
        forms = S.read_file(prof_path)
        form = next(f for f in forms if isinstance(f, list) and f and str(f[0]) == "profile")
    except (S.SexpError, StopIteration) as exc:
        findings.append(f"UNREADABLE {tag}: {exc}")
        continue
    scopes = S.children(form, "scope")
    if not scopes:
        findings.append(f"UNDECLARED SCOPE {tag}: the dossier declares no [scope] — coverage "
                        f"against a scope that was never declared proves nothing")
        continue
    scope = scopes[0]
    # P3-BREADTH.7 (decision_gate-applicability-by-declared-vehicle): a unit declaring
    # (vehicle (comparison checkpoint-end-state)) is measured against its guest corpus
    # directly — the composition leg then applies iff an encoding.sexp exists.
    vehicle = S.children(form, "vehicle")
    checkpoint = any(
        str(c[1]) == "checkpoint-end-state"
        for v in vehicle for c in S.children(v, "comparison"))
    # P5-BOARD.2 (case sifive-uart-lab-v0): a unit declaring (vehicle (route
    # device-model)) has no guest corpus and no composition at this stage — both legs
    # are n/a BY DECLARATION, and a document that contradicts the declaration (an
    # encoding.sexp, a guests/ corpus) is a finding, the same rule the checkpoint leg
    # applies. The denominator census above runs unchanged: a device scope must not
    # contradict its own register enumeration either.
    routes = [str(c[1]) for v in vehicle for c in S.children(v, "route")]
    device = routes[:1] == ["device-model"]
    # P4-SYSTEM.1 (case rv64gc-lab-v0): a unit declaring (vehicle (route
    # profile-resolution)) has no definition pipeline and no guest corpus yet — both
    # legs are n/a BY DECLARATION, the device-model discipline exactly; the denominator
    # census above still runs (the resolution's scope enumeration must be honest).
    resolution = routes[:1] == ["profile-resolution"]
    denominator: set[str] = set()
    for f in scope[1:]:
        # (comment …) is the format's reserved annotation head, never a mnemonic group —
        # measured 2026-10-01 (P3-BREADTH.5 slice 2): a comment inside scope poisoned the
        # denominator with its own prose.
        if isinstance(f, list) and f and str(f[0]) not in ("count_base", "count_rv64i_additions",
                                                           "count_total", "authority", "source",
                                                           "comment"):
            denominator |= {str(v).lower() for v in f[1:]}
    declared_total = None
    totals = S.children(scope, "count_total")
    if totals:
        declared_total = int(totals[0][1])
    checked += 1
    if declared_total is None:
        findings.append(f"DENOMINATOR ABSENT {tag}: [scope] carries no count_total — a denominator "
                        f"nobody states is a coverage claim nobody can check")
    elif declared_total != len(denominator):
        findings.append(f"DENOMINATOR LIE {tag}: count_total says {declared_total} but the "
                        f"mnemonic lists enumerate {len(denominator)} — the declaration "
                        f"contradicts its own enumeration")
    # SCP-02: the composition resolves through the one resolver; every declared form exists in it.
    enc_path = pdir / "encoding.sexp"
    resolved: set[str] = set()
    closure = "unresolved"
    if not enc_path.is_file():
        if checkpoint:
            closure = "n/a (checkpoint-end-state declared; no encoding.sexp — measured against the guest corpus)"
        elif device:
            closure = "n/a (device-model declared; no encoding.sexp — a device composes no instruction encoding)"
        elif resolution:
            closure = "n/a (profile-resolution declared; no encoding.sexp — the definition pipeline has not started)"
        else:
            findings.append(f"NO COMPOSITION {tag}: no encoding.sexp beside the dossier — the "
                            f"declared scope's dependency closure cannot be decided")
    elif device:
        findings.append(f"DECLARATION CONTRADICTION {tag}: device-model route declared but an "
                        f"encoding.sexp exists — the declaration contradicts the documents")
    elif resolution:
        findings.append(f"DECLARATION CONTRADICTION {tag}: profile-resolution route declared but "
                        f"an encoding.sexp exists — the declaration contradicts the documents")
    else:
        try:
            enc = S.read_file(enc_path)[0]
            comp = S.children(enc, "compose")
            base = str(S.field(comp[0], "base", str(enc_path)))
            ext = S.children(comp[0], "extensions")
            names = [base] + [str(x) for x in (ext[0][1:] if ext else [])]
            merged = resolve_composition(enc, enc_path)
            resolved = {str(S.field(i, "name")) for i in S.children(merged, "insn")}
            closure = "{" + ", ".join(names) + "}"
        except (AsmError, S.SexpError, IndexError) as exc:
            findings.append(f"UNMET DEPENDENCY {tag}: {exc}")
    if not closure.startswith("n/a") and not device and not resolution:
        for m in sorted(denominator - resolved):
            findings.append(f"UNRESOLVED FORM {tag}: [scope] declares '{m}' but the resolved "
                            f"composition does not provide it — an included feature whose "
                            f"dependency is not closed (SCP-02)")
    # exercised: the union of mnemonics the tracked expectation documents declare executed.
    exercised: set[str] = set()
    if device:
        # P5-BOARD.2 (case sifive-uart-lab-v0): there is nothing to execute — the device
        # is observed through reset/stimulus expectations, not a guest corpus. Anti-drift:
        # the day probes land, a guests/ corpus appears and the gate REFUSES until it is
        # taught the device exercise leg — a silent pass is the drift.
        gdir = pdir / "guests"
        if gdir.is_dir() and any(gdir.iterdir()):
            findings.append(f"DECLARATION CONTRADICTION {tag}: device-model route declared but "
                            f"a guests/ corpus exists — the declaration and the documents "
                            f"disagree")
        else:
            print(f"{pdir.relative_to(root).as_posix()}: device-model route declared — "
                  f"{len(denominator)} declared registers, exercise n/a by declaration")
        continue
    if resolution:
        # P4-SYSTEM.1: no guest corpus exists at the resolution stage — exercise is n/a
        # by declaration, and a guests/ corpus beside the declaration is the same
        # anti-drift contradiction the device leg refuses.
        gdir = pdir / "guests"
        if gdir.is_dir() and any(gdir.iterdir()):
            findings.append(f"DECLARATION CONTRADICTION {tag}: profile-resolution route declared "
                            f"but a guests/ corpus exists — the declaration and the documents "
                            f"disagree")
        else:
            print(f"{pdir.relative_to(root).as_posix()}: profile-resolution route declared — "
                  f"{len(denominator)} declared forms, exercise n/a by declaration")
        continue
    if checkpoint:
        # The checkpoint leg (P3-BREADTH.7, case dsp56300-lab-v0): the corpus is .a56
        # assembler sources compared at end state; the census runs BOTH directions —
        # a declared form no guest executes is UNEXERCISED, a guest instruction the scope
        # does not name is UNDECLARED EXERCISE. Labels are column-0 tokens; assembler
        # directives are never instructions.
        A56_DIRECTIVES = {"org", "end", "dc", "ds", "dsm", "equ", "set", "page", "sect",
                          "endsec", "include", "define", "undefine", "macro", "endm",
                          "if", "else", "endif", "dup", "enddup", "msg", "warn", "fail"}
        a56_files = sorted(pdir.glob("guests/*.a56"))
        if not a56_files:
            findings.append(f"NO GUESTS {tag}: checkpoint-end-state declared but no "
                            f"guests/*.a56 — nothing is exercised")
        for gf in a56_files:
            gtag = gf.relative_to(root).as_posix()
            for raw in gf.read_text(encoding="utf-8").splitlines():
                line = raw.split(";", 1)[0].strip()
                if not line:
                    continue
                toks = line.split()
                if raw[0] in " \t":
                    mn = toks[0]
                else:
                    if len(toks) < 2:
                        continue          # a bare label line
                    mn = toks[1]          # label + instruction on one line
                mn = mn.lower()
                if mn in A56_DIRECTIVES:
                    continue
                if mn in denominator:
                    exercised.add(mn)
                else:
                    findings.append(f"UNDECLARED EXERCISE {gtag}: the guest executes "
                                    f"'{mn}', which the declared scope does not name — the "
                                    f"corpus and the declaration disagree")
    else:
        expected_files = sorted(pdir.glob("guests/*.expected.sexp"))
        if not expected_files:
            findings.append(f"NO GUESTS {tag}: no guests/*.expected.sexp — nothing is exercised")
        for ef in expected_files:
            etag = ef.relative_to(root).as_posix()
            try:
                eforms = S.read_file(ef)
                eform = next(f for f in eforms
                             if isinstance(f, list) and f and str(f[0]) == "expectations")
            except (S.SexpError, StopIteration) as exc:
                findings.append(f"UNREADABLE {etag}: {exc}")
                continue
            for step in S.children(eform, "step"):
                insn = S.children(step, "insn")
                if not insn:
                    findings.append(f"UNNAMED STEP {etag}: a step declares no insn — an exercised "
                                    f"form nobody names cannot be counted")
                    continue
                text = str(insn[0][1]).strip()
                if text:
                    exercised.add(text.split()[0].lower())
    unexercised = sorted(denominator - exercised)
    for m in unexercised:
        findings.append(f"UNEXERCISED {tag}: '{m}' is in the declared scope but no tracked "
                        f"guest executes it — coverage is {len(denominator) - len(unexercised)}"
                        f"/{len(denominator)}, not complete")
    if not findings:
        print(f"{pdir.relative_to(root).as_posix()}: exercised {len(exercised & denominator)}"
              f"/{len(denominator)} declared forms; SCP-02 closure {closure} resolved")
    print(f"__EXERCISED__ {len(denominator) - len(unexercised)}/{len(denominator)}")

for f in findings:
    print(f)
print(f"__CHECKED__ {checked}")
sys.exit(1 if findings else 0)
PY
}

self_test() {
  SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"

  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'EXERCISE-COVERAGE self-test HARNESS: %s() got %s argument(s), expected %s\n' "$3" "$2" "$1" >&2
    return 1
  }
  arm() {
    argc 3 "$#" arm || return
    out="$(check_coverage "$t" fs 2>&1)"; rc=$?
    if [ "$rc" != "$2" ]; then
      fail=$((fail+1)); printf 'EXERCISE-COVERAGE self-test MISS: %s expected rc=%s got rc=%s\n%s\n' "$1" "$2" "$rc" "$out" >&2
    elif ! printf '%s' "$out" | grep -qF "$3"; then
      fail=$((fail+1)); printf 'EXERCISE-COVERAGE self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' "$1" "$3" "$out" >&2
    else pass=$((pass+1)); fi
  }

  # A scratch unit: a two-form scope over the REAL rv64i fragment (copied), exercised by
  # synthetic expectation documents. The fixture writer functions rebuild the unit per arm.
  mkdir -p "$t/profiles/p/guests" "$t/definitions/riscv"
  cp "$ROOT/definitions/riscv/rv64i.sexp" "$t/definitions/riscv/rv64i.sexp"

  profile() { # $1 = scope body
    printf '(profile (id "p") (version "0") (status "development") (scope %s))\n' "$1" \
      > "$t/profiles/p/profile.sexp"
  }
  encoding() {
    printf '(encoding (profile "p") (ilen 32) (compose (base "riscv/rv64i") (extensions)) (fragment-root "definitions"))\n' \
      > "$t/profiles/p/encoding.sexp"
  }
  guest() { # $1 = name; $2 = space-separated mnemonics exercised
    local steps="" n=0 m
    for m in $2; do
      steps="$steps (step (n $n) (insn \"$m x1, x0, 1\") (writes) (derivation \"d\") (source \"s\"))"
      n=$((n+1))
    done
    printf '(expectations (program "%s.s") (entry "0x80000000") (instructions %s)%s)\n' \
      "$1" "$n" "$steps" > "$t/profiles/p/guests/$1.expected.sexp"
  }
  scope2='(count_total 2) (authority architecture) (source "s") (base_op "ADD") (base_op "SUB")'

  arm "REFUSE no profile dossier at all" 2 "cannot judge"

  profile "$scope2"; encoding; guest g1 "add sub"
  arm "GREEN every declared form exercised" 0 "__EXERCISED__ 2/2"

  # GREEN: a (comment …) inside scope is an annotation, not a mnemonic group — the
  # denominator ignores it (measured with the dsp56300-lab-v0 draft, P3-BREADTH.5 slice 2).
  profile '(comment "a note, not a mnemonic") (count_total 2) (authority architecture) (source "s") (base_op "ADD") (base_op "SUB")'
  arm "GREEN a comment inside scope does not poison the denominator" 0 "__EXERCISED__ 2/2"

  guest g1 "add"
  arm "RED   a declared form no guest exercises, named" 1 "UNEXERCISED"

  profile '(count_total 3) (authority architecture) (source "s") (base_op "ADD") (base_op "SUB")'
  arm "RED   a count_total that contradicts the enumeration" 1 "DENOMINATOR LIE"

  profile "$scope2"
  rm -f "$t/profiles/p/encoding.sexp"
  arm "RED   a scope whose composition is absent" 1 "NO COMPOSITION"

  encoding
  profile '((count_total 1) (authority architecture) (source "s") (base_op "MUL"))'
  guest g1 "mul"
  arm "RED   a declared form the composition does not provide (SCP-02)" 1 "UNRESOLVED FORM"

  rm -rf "$t/profiles/p/guests"; mkdir -p "$t/profiles/p/guests"
  profile "$scope2"
  arm "RED   a unit with no guests at all" 1 "NO GUESTS"

  # ── the checkpoint leg (P3-BREADTH.7, case dsp56300-lab-v0): a unit declaring
  # (vehicle (comparison checkpoint-end-state)) is measured against its .a56 corpus,
  # both directions; the composition leg is n/a only while no encoding.sexp exists.
  profile_cp() { # $1 = scope body
    printf '(profile (id "p") (version "0") (status "experimental") (vehicle (route sibling-crate) (comparison checkpoint-end-state) (authority laboratory) (source "s")) (scope %s))\n' "$1" \
      > "$t/profiles/p/profile.sexp"
  }
  guest_a56() { # $1 = name; $2 = instruction lines (\n-separated)
    printf -- '\torg\tp:$100\nstart\t%b\n' "$2" > "$t/profiles/p/guests/$1.a56"
  }
  rm -f "$t/profiles/p/encoding.sexp"
  profile_cp '(count_total 2) (authority architecture) (source "s") (moves "move") (flow "nop")'
  guest_a56 g1 'move #$1,x0\n\tnop'
  arm "GREEN checkpoint unit: the .a56 corpus covers the declared scope" 0 "__EXERCISED__ 2/2"

  profile_cp '(count_total 3) (authority architecture) (source "s") (moves "move") (flow "nop") (flow "jmp")'
  arm "RED   a declared form no .a56 guest executes, named" 1 "UNEXERCISED"

  profile_cp '(count_total 2) (authority architecture) (source "s") (moves "move") (flow "nop")'
  guest_a56 g1 'move #$1,x0\n\tjmp done'
  arm "RED   a guest instruction the scope does not name" 1 "UNDECLARED EXERCISE"

  guest_a56 g1 'move #$1,x0\n\tnop'
  rm -f "$t/profiles/p/guests/g1.a56"
  arm "RED   checkpoint declared but no .a56 guests" 1 "NO GUESTS"

  guest_a56 g1 'move #$1,x0\n\tnop'
  profile_cp '(count_total 2) (authority architecture) (source "s") (moves "move") (flow "nop")'
  arm "GREEN checkpoint with no encoding.sexp — the composition leg is n/a, not RED" 0 "checkpoint-end-state declared"

  # ── the device leg (P5-BOARD.2, case sifive-uart-lab-v0): a unit declaring
  # (vehicle (route device-model)) has no guest corpus and no composition; both legs are
  # n/a by declaration, the denominator census still applies, and a document that
  # contradicts the declaration is RED.
  profile_dev() { # $1 = scope body
    printf '(profile (id "p") (version "0") (status "experimental") (vehicle (route device-model) (comparison register-expectations) (authority laboratory) (source "s")) (scope %s))\n' "$1" \
      > "$t/profiles/p/profile.sexp"
  }
  rm -f "$t/profiles/p/guests/g1.a56"
  profile_dev '(count_total 2) (authority platform) (source "s") (mmio_registers "UART_RXDATA") (mmio_registers "UART_TXDATA")'
  arm "GREEN device-model route: exercise n/a by declaration, the unit named" 0 "profiles/p: device-model route declared"

  encoding
  arm "RED   device-model contradicted by an encoding.sexp" 1 "contradicts the documents"

  rm -f "$t/profiles/p/encoding.sexp"
  guest g1 "add sub"
  arm "RED   device-model contradicted by a guests/ corpus (anti-drift)" 1 "the declaration and the documents disagree"

  rm -f "$t/profiles/p/guests/g1.expected.sexp"
  profile_dev '(count_total 3) (authority platform) (source "s") (mmio_registers "UART_RXDATA") (mmio_registers "UART_TXDATA")'
  arm "RED   a device scope whose count contradicts its own enumeration" 1 "DENOMINATOR LIE"

  # ── the profile-resolution leg (P4-SYSTEM.1, case rv64gc-lab-v0): the selection is
  # resolved and citable; no encoding, no guests — both legs n/a by declaration, the
  # denominator census still applies, and a contradicting document is RED.
  profile_res() { # $1 = scope body
    printf '(profile (id "p") (version "0") (status "development") (vehicle (route profile-resolution) (authority laboratory) (source "s")) (scope %s))\n' "$1" \
      > "$t/profiles/p/profile.sexp"
  }
  profile_res '(count_total 1) (authority architecture) (source "s") (base_op "add")'
  arm "GREEN profile-resolution route: composition and exercise n/a by declaration" 0 "profiles/p: profile-resolution route declared"

  encoding
  arm "RED   profile-resolution contradicted by an encoding.sexp" 1 "contradicts the documents"
  rm -f "$t/profiles/p/encoding.sexp"

  guest g1 "add sub"
  arm "RED   profile-resolution contradicted by a guests/ corpus (anti-drift)" 1 "the declaration and the documents disagree"
  rm -f "$t/profiles/p/guests/g1.expected.sexp"

  profile_res '(count_total 2) (authority architecture) (source "s") (base_op "add")'
  arm "RED   a resolution scope whose count contradicts its own enumeration" 1 "DENOMINATOR LIE"

  rm -rf "$t"
  printf 'EXERCISE-COVERAGE --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

self_test >/dev/null 2>&1 || {
  echo "EXERCISE-COVERAGE: REFUSED — the check does not discriminate (self-test failed)." >&2; exit 2; }

out="$(check_coverage "$ROOT" git)"; rc=$?
count="$(printf '%s' "$out" | sed -n 's/^__CHECKED__ //p')"
exercised="$(printf '%s' "$out" | sed -n 's/^__EXERCISED__ //p')"
body="$(printf '%s' "$out" | grep -v '^__CHECKED__ \|^__EXERCISED__ ' || true)"
if [ "$rc" -eq 2 ]; then
  { echo "EXERCISE-COVERAGE: REFUSED — the profile corpus could not be read."
    printf '%s\n' "$body" | sed 's/^/  /'; } >&2
  exit 2
fi
if [ "$rc" -ne 0 ]; then
  { echo "EXERCISE-COVERAGE: the declared scope is not fully exercised (coverage ${exercised:-?})."
    printf '%s\n' "$body" | sed 's/^/  /'
    echo "  Every declared form must run under the laboratory — exercise it or shrink the declaration."; } >&2
  exit 1
fi
printf 'EXERCISE-COVERAGE: ok (%s profile(s) — every declared form exercised, %s)\n' "${count:-0}" "${exercised:-?}"
exit 0
