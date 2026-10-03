#!/usr/bin/env bash
# scripts/check_semantics_corpus.sh — SEMANTICS (project doctrine).
#
# WHY THIS EXISTS, measured rather than argued. `ROADMAP.md` names the semantics data the
# EXECUTION AUTHORITY — P1's definitional interpreter evaluates exactly these forms. And yet
# `check_semantics.py` (well-formed, complete, cited) and `check_citations.py` (every locator
# resolves against the pinned artifact) were invoked by NOTHING in the gate set: the corpus the
# whole engine will execute was healthy only when someone ran the tools by hand. The third
# orphan of the family `MODEL-COMPOSE.4` closed for encodings — a capability without a
# re-runner regresses silently. This doctrine is the corpus's home:
#
#   PAIR      every tracked definitions/**/*.sem.sexp checks against its fragment: every
#             declared instruction covered, every rule cited, every form known and arity-true.
#   COMPOSE   per unit, the fragments' sem files in composition order pass the refinement rule
#             (MODEL-COMPOSE.6): an override without a declared (refines (insn …)) is refused
#             by name — a silent semantic override is a defect even when every fragment alone
#             is well-formed.
#   CITED     every locator resolves against the pinned artifact, via the manifest-verified
#             offline materials cache. ⛔ A NAMED SKIP, not a pass: when the cache is absent
#             (fresh clone) this arm prints that it cannot judge and stands down — a check
#             that cannot judge must never report green over an absence.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "SEMANTICS: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

check_corpus() { # $1 = root; $2 = "git" (tracked only) or "fs"
python3 - "$1" "$2" <<'PY'
import subprocess, sys
from pathlib import Path

root = Path(sys.argv[1]); mode = sys.argv[2]
sys.path.insert(0, "scripts")
import sexp as _sexp
import check_semantics as SEM

if mode == "git":
    def tracked(glob):
        out = subprocess.run(["git", "ls-files", "--", glob],
                             capture_output=True, text=True, check=True).stdout
        return [root / p for p in out.splitlines() if p.strip()]
    sem_files = tracked("definitions/**/*.sem.sexp")
    unit_docs = tracked("profiles/*/encoding.sexp")
else:
    sem_files = sorted(root.glob("definitions/**/*.sem.sexp"))
    unit_docs = sorted(root.glob("profiles/*/encoding.sexp"))

findings: list[str] = []
notes: list[str] = []
checked = 0

if not sem_files:
    print("SEMANTICS: REFUSED — no semantics document found; this check cannot judge")
    print("__CHECKED__ 0"); sys.exit(2)

# ---- PAIR: every sem file against its fragment ---------------------------------------------
for sem_path in sem_files:
    frag_path = sem_path.with_name(sem_path.name.replace(".sem.sexp", ".sexp"))
    checked += 1
    if not frag_path.is_file():
        findings.append(f"ORPHAN {sem_path.relative_to(root)}: no fragment "
                        f"{frag_path.name} beside it — semantics without their encodings")
        continue
    r = subprocess.run([sys.executable, "scripts/check_semantics.py",
                        str(frag_path), str(sem_path)], capture_output=True, text=True)
    if r.returncode != 0:
        errs = [l.strip() for l in r.stdout.splitlines() if l.startswith("  ")] \
               or [r.stderr.strip()]
        findings.append(f"INVALID {sem_path.relative_to(root)}: " + " | ".join(errs[:2]))
    else:
        last = [l.strip() for l in r.stdout.splitlines()
                if "declared instruction(s) have checked semantics" in l]
        print(f"  PAIR {sem_path.relative_to(root)}: {last[0] if last else 'ok'}")

# ---- COMPOSE: refinement rule per unit ------------------------------------------------------
for doc in unit_docs:
    try:
        enc = _sexp.read_file(doc)[0]
        comp = _sexp.children(enc, "compose")
        if not comp:
            continue
        names = [str(_sexp.field(comp[0], "base", str(doc)))]
        ext = _sexp.children(comp[0], "extensions")
        for e in ext:
            names += [str(x) for x in e[1:]]
    except _sexp.SexpError as exc:
        findings.append(f"UNREADABLE {doc.relative_to(root)}: {exc}")
        continue
    frag_root = doc.parent.parent.parent / str(_sexp.field(enc, "fragment-root", str(doc)))
    ordered = [frag_root / (n + ".sem.sexp") for n in names]
    present = [p for p in ordered if p.is_file()]
    checked += 1
    if len(present) < 2:
        continue                                  # nothing to override yet
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = SEM.compose(present)
    if rc != 0:
        findings.append(f"REFINEMENT {doc.relative_to(root)}: "
                        + " | ".join(l.strip() for l in buf.getvalue().splitlines() if l.strip()))

# ---- CITED: locators resolve, offline; a named skip when the cache cannot judge --------------
# Judged only on the real corpus: fixture locators are synthetic, and a self-test must never
# depend on the environment's cache state.
if mode == "git":
    try:
        import materials as _m
        cat = _m.load()
        rel = _m.resolve(cat, "RVI-PINNED-V20260120")
        cache = root / rel / "unpriv"
        have_cache = cache.is_dir()
    except Exception:                               # noqa: BLE001 — the route itself is absent
        have_cache = False
    if have_cache:
        checked += 1
        r = subprocess.run([sys.executable, "scripts/check_citations.py", "--corpus"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            findings.append("CITATIONS: " + (r.stdout.strip().splitlines() or [r.stderr.strip()])[-1])
    else:
        notes.append("CITATIONS: NAMED SKIP — neither the fetched working area nor the manifest-"
                     "verified materials cache is present; locators cannot be judged offline. "
                     "Run scripts/materials.py --fetch; a check that cannot judge never reports green.")
else:
    notes.append("CITATIONS: NAMED SKIP — self-test mode judges synthetic locators never; the "
                 "citation arm runs on the tracked corpus only.")

for f in findings:
    print(f)
for n in notes:
    print(n)
print(f"__CHECKED__ {checked}")
sys.exit(1 if findings else 0)
PY
}

self_test() {
  SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"; mkdir -p "$t/definitions/riscv" "$t/profiles/p"

  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'SEMANTICS self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' "$3" "$2" "$1" >&2
    return 1
  }
  arm() {
    argc 3 "$#" arm || return
    out="$(check_corpus "$t" fs 2>&1)"; rc=$?
    if [ "$rc" != "$2" ]; then
      fail=$((fail+1)); printf 'SEMANTICS self-test MISS: %s expected rc=%s got rc=%s\n%s\n' "$1" "$2" "$rc" "$out" >&2
    elif ! printf '%s' "$out" | grep -qF "$3"; then
      fail=$((fail+1)); printf 'SEMANTICS self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' "$1" "$3" "$out" >&2
    else pass=$((pass+1)); fi
  }

  frag() { printf '%s\n' '(fragment (id "riscv/t") (kind extension)' \
      '(insn (name add) (fixed (31 25 0x0) (14 12 0x0) (6 2 0x13) (1 0 0x3)) (operands rd rs1 rs2))' \
      '(insn (name mul) (fixed (31 25 0x0) (14 12 0x0) (6 2 0x13) (1 0 0x3)) (operands rd rs1 rs2)))' \
      > "$t/definitions/riscv/t.sexp"; }
  sem() { printf '%s\n' '(semantics (fragment "riscv/t") (xlen 64)' "$1" ')' \
      > "$t/definitions/riscv/t.sem.sexp"; }
  unit() { printf '%s\n' '(encoding (profile "p") (ilen 32)' \
      "  (compose (base \"riscv/t\")$1)" '  (fragment-root "definitions"))' \
      > "$t/profiles/p/encoding.sexp"; }
  RULE='(sem (insn add) (source "S §1 — why") (effect (set (reg rd) (add (reg rs1) (reg rs2)))))'
  RULE2='(sem (insn mul) (source "S §2 — why") (effect (set (reg rd) (add (reg rs1) (reg rs2)))))'

  frag; sem "$RULE
$RULE2"; unit "";          arm "GREEN a complete, cited corpus composes" 0 "have checked semantics"
  frag; sem "$RULE"; unit ""; arm "RED   an uncovered declared instruction" 1 "have NO semantics"
  frag; sem '(sem (insn add) (effect (nop)))'; unit ""
                            arm "RED   a rule citing nothing" 1 'missing required field "source"'
  frag; sem "(sem (insn add) (source \"S §1\") (effect (widget rd)))
$RULE2"; unit "";          arm "RED   a form the language refuses, by name" 1 'form head "widget" is not one of'
  frag; sem "$RULE
$RULE2"; printf '%s\n' '(fragment (id "riscv/u") (kind isa-extension) (requires "riscv/t"))' \
      > "$t/definitions/riscv/u.sexp"
    printf '%s\n' '(semantics (fragment "riscv/u") (xlen 64)' "$RULE2" ')' \
      > "$t/definitions/riscv/u.sem.sexp"
    unit ' (extensions "riscv/u")'
                            arm "RED   a silent override across a unit's fragments" 1 "SILENT REDEFINITION"
  rm -f "$t/definitions/riscv/u.sexp" "$t/definitions/riscv/u.sem.sexp"
  frag; sem "$RULE
$RULE2"; printf '%s\n' '(fragment (id "riscv/v") (kind isa-extension) (requires "riscv/t"))' \
      > "$t/definitions/riscv/v.sexp"
    printf '%s\n' '(fragment (id "riscv/w") (kind isa-extension) (requires "riscv/t"))' \
      > "$t/definitions/riscv/w.sexp"
    printf '%s\n' '(semantics (fragment "riscv/w") (xlen 64)' "$RULE2" ')' \
      > "$t/definitions/riscv/w.sem.sexp"
    unit ' (extensions "riscv/v") (extensions "riscv/w")'
                            arm "RED   a silent override in the SECOND extensions form (the dropped-form regression)" 1 "SILENT REDEFINITION"
  rm -f "$t/definitions/riscv/"*.sem.sexp
    unit "";               arm "REFUSE an empty corpus, never pass it" 2 "cannot judge"
  frag; sem "$RULE
$RULE2"; unit "";          arm "GREEN the citation arm names its skip when the cache is absent" 0 "NAMED SKIP"

  rm -rf "$t"
  printf 'SEMANTICS --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

self_test >/dev/null 2>&1 || {
  echo "SEMANTICS: REFUSED — the check does not discriminate (self-test failed)." >&2; exit 2; }

out="$(check_corpus "$ROOT" git)"; rc=$?
count="$(printf '%s' "$out" | sed -n 's/^__CHECKED__ //p')"
body="$(printf '%s' "$out" | grep -v '^__CHECKED__ ' || true)"
if [ "$rc" -eq 2 ]; then
  { echo "SEMANTICS: REFUSED — the semantics corpus could not be read."
    printf '%s\n' "$body" | sed 's/^/  /'; } >&2
  exit 2
fi
if [ "$rc" -ne 0 ]; then
  { echo "SEMANTICS: the execution authority's corpus does not hold."
    printf '%s\n' "$body" | sed 's/^/  /'
    echo "  The corpus is authoritative. Fix the semantics, or they do not execute."; } >&2
  exit 1
fi
printf 'SEMANTICS: ok (%s check(s) — pairs, refinement rule, citations)\n' "${count:-0}"
exit 0
