#!/usr/bin/env bash
# scripts/check_citation_quotes.sh — CITATION-QUOTES (project doctrine; CITATION-ACCURACY.1).
#
# Every quoted phrase a tracked `.sexp` attributes to a pinned section must occur IN that
# section — `scripts/check_citation_quotes.py` decides it (the four attribution rules and the
# matching normalization are its docstring's). `check_citations.py` proves a locator EXISTS;
# this proves the quote under it is THERE. Founding failure (P4-SYSTEM.7 slice (c3) part 1,
# SEMULITH-P4-0043): the rv64gc FP-CSR content was cited `RVI-F §20.1.1` — a real section, the
# wrong one — with every gate green. Observed RED against that real pre-fix corpus before
# registration: six misses, each naming "found in §20.1.2".
#
# ⚠️ HONEST LIMITS: quotes only, never paraphrase; a quote with no decidable attribution is
# counted, never judged; PDF pins (http_status 0) are counted UNCHECKABLE by name. The pinned
# pages are an untracked, network-acquired cache: a clone without them prints a NAMED SKIP —
# the SEMANTICS doctrine's CITATIONS-arm precedent (a check that cannot judge never reports
# green; it says it did not judge).
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls (synthetic pages — never the cache) and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "CITATION-QUOTES: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

TOOL="scripts/check_citation_quotes.py"

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
    printf 'CITATION-QUOTES self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' \
      "$3" "$2" "$1" >&2
    return 1
  }
  arm() { # arm <name> <rc> <expected-rc> <output> <reason substring>
    argc 5 "$#" arm || return
    if [ "$2" = "$3" ] && printf '%s' "$4" | grep -qF -- "$5"; then
      pass=$((pass+1))
    else
      fail=$((fail+1))
      printf 'CITATION-QUOTES self-test MISS: %s — expected rc=%s (reason: %s), got rc=%s\n%s\n' \
        "$1" "$3" "$5" "$2" "$4" >&2
    fi
  }

  # The synthetic artifact: numbered sections, a descendant, the two measured renderings (a
  # code literal in quotes, a zero-width space inside a dash range), a possessive.
  mkdir -p "$t/pages"
  printf '%s\n' \
    '<h2>1.1. Alpha</h2><p>The quick brown fox jumps over the lazy dog; the fox&#8217;s tail is long.</p>' \
    "<h3>1.1.1. Alpha detail</h3><p>Stores the address (<code>'pc'</code>+4) into rd. Range 7&#8212;&#8203;5 bits.</p>" \
    '<h2>1.2. Beta</h2><p>Implementations shall ignore writes to these bits.</p>' > "$t/pages/SPEC.html"
  : > "$t/pages/PDFDOC.pdf"
  doc() { printf '%s\n' "$2" > "$t/$1.sexp"; }
  run() { out="$(python3 "$TOOL" --pages "$t/pages" "$t/$1.sexp" 2>&1)"; rc=$?; }

  doc green "(doc (statement \"The rule: 'the quick brown fox jumps' (SPEC §1.1).\"))"
  run green
  arm "GREEN an R1 quote that is in its cited section passes" "$rc" 0 "$out" "1 attributed quote(s) judged (R1 1"

  doc sub "(doc (statement \"'Stores the address (pc+4) into rd' (SPEC §1.1), and 'Range 7-5 bits' (SPEC §1.1.1).\"))"
  run sub
  arm "GREEN a section includes its descendants; code-literal quotes, zero-width space and dashes fold" "$rc" 0 "$out" "2 attributed quote(s) judged (R1 2"

  doc miss "(doc (statement \"'shall ignore writes to these bits' (SPEC §1.1)\"))"
  run miss
  arm "RED a quote under the wrong section is refused, naming where it is" "$rc" 1 "$out" "is not in SPEC §1.1 — found in §1.2"

  doc nowhere "(doc (statement \"'a sentence the page never says' (SPEC §1.1)\"))"
  run nowhere
  arm "RED a quote the artifact never says is refused as such" "$rc" 1 "$out" "found nowhere in the cited artifact"

  doc unresolved "(doc (statement \"'the quick brown fox' (SPEC §9.9)\"))"
  run unresolved
  arm "RED a quote under a section the artifact lacks is UNRESOLVED" "$rc" 1 "$out" "UNRESOLVED"

  doc order "(doc (statement \"'lazy dog … quick brown' (SPEC §1.1)\"))"
  run order
  arm "RED ellipsis pieces out of order are refused" "$rc" 1 "$out" "is not in SPEC §1.1"

  doc inorder "(doc (statement \"'quick brown … [it] … lazy dog' (SPEC §1.1)\"))"
  run inorder
  arm "GREEN ellipsis and editorial-bracket pieces in order pass" "$rc" 0 "$out" "0 finding(s)"

  doc r2 "(doc (rule (source \"SPEC §1.1 — 'shall ignore writes to these bits'\")))"
  run r2
  arm "RED an R2 quote in a (source …) is judged under its leading locator" "$rc" 1 "$out" "[R2]"

  doc r3 "(expectations (step (n 0) (derivation \"x — 'shall ignore writes to these bits'\") (source \"SPEC §1.1\")))"
  run r3
  arm "RED an R3 derivation quote is judged under its step's source" "$rc" 1 "$out" "[R3]"

  doc r4 "(doc (statement \"Per SPEC §1.2 the rule holds: 'implementations shall ignore' — always.\"))"
  run r4
  arm "GREEN an R4 quote in a single-locator string is judged and passes" "$rc" 0 "$out" "(R1 0, R2 0, R3 0, R4 1)"

  doc multi "(doc (statement \"SPEC §1.1 or SPEC §1.2: 'never in the page at all' — no adjacency.\"))"
  run multi
  arm "GREEN a quote beside two locators is counted, never judged" "$rc" 0 "$out" "1 unattributed"

  doc possessive "(doc (statement \"'the fox's nose is long' (SPEC §1.1)\"))"
  run possessive
  arm "RED a possessive stays inside the phrase (the whole quote is judged)" "$rc" 1 "$out" "'the fox's nose is long'"

  doc pdf "(doc (statement \"'anything at all in a manual' (PDFDOC §2)\"))"
  run pdf
  arm "GREEN a quote under a PDF pin is counted UNCHECKABLE by name" "$rc" 0 "$out" "PDFDOC ×1"

  out="$(python3 "$TOOL" --bogus 2>&1)"; rc=$?
  arm "RED an unknown invocation is refused, not judged" "$rc" 2 "$out" "Usage:"

  rm -rf "$t"
  printf 'CITATION-QUOTES --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

if [ "${1:-}" = "--self-test" ]; then
  self_test
  exit $?
fi

# Re-run the controls before judging: a check that no longer discriminates must refuse,
# not pass (the project-doctrine contract in scripts/check_doctrines.project.sh).
self_test >/dev/null 2>&1 || {
  echo "CITATION-QUOTES: REFUSED — the check does not discriminate (self-test failed)." >&2
  exit 2; }

# The cache route (check_citations' own): the fetched working area, else the manifest-verified
# materials cache. Neither present → a NAMED SKIP, never a pass.
if ! python3 - <<'PY' >/dev/null 2>&1
import sys
from pathlib import Path
sys.path.insert(0, "scripts")
import materials as _m
rel = _m.resolve(_m.load(), "RVI-PINNED-V20260120")
fetched = Path("target/sources")
sys.exit(0 if (Path(rel) / "unpriv").is_dir() or fetched.is_dir() else 1)
PY
then
  echo "CITATION-QUOTES: NAMED SKIP — the pinned pages are absent (neither the fetched working area nor the materials cache); quotes cannot be judged offline. Run scripts/materials.py --fetch."
  exit 0
fi

out="$(python3 "$TOOL" 2>&1)"; rc=$?
if [ "$rc" -ne 0 ]; then
  printf '%s\n' "$out" >&2
  printf 'CITATION-QUOTES: FAIL — a quoted phrase is not in the section its locator names. Re-cite it (the finding names where the phrase is) — never loosen the match.\n' >&2
  exit "$rc"
fi
printf '%s\n' "$out" | tail -1
exit 0
