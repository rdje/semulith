#!/usr/bin/env bash
# scripts/check_seam_integrity.sh — SEAM-INTEGRITY (project doctrine).
#
# ⭐ WHY THIS EXISTS, measured rather than argued. Three defects in the neutral spine checks were
# fixed here through the sanctioned `.doctrine/` seams. Then both seam files were moved aside and
# the full enforcer was re-run:
#
#     $ mv .doctrine/code_paths.txt .doctrine/evidence_tokens.txt <elsewhere>
#     $ scripts/check_doctrines.sh
#     ✅ TASK-ACCEPTANCE ...
#     === all doctrines green ===          rc=0
#
# Every one of those fixes silently reverted and nothing said a word. **A fix whose disappearance
# is undetectable is not a fix — it is a configuration that happens to be present.** That is
# `docs/CLAIM_VERIFICATION.md` leg 3 exactly: a claim nothing re-derives goes stale in silence.
#
# ⛔ PRESENCE IS NOT THE PROPERTY. Checking that the files exist would catch deletion and miss
# every way a declaration can stop doing its job — a narrowed pattern, a spine update that stops
# consuming the seam, a token family that no longer fits the corpus. So each rule below asserts
# the BEHAVIOUR the seam is supposed to produce, over the repository's own history:
#
#   R1 CONSUMED   the neutral check still reads both seam files. A declaration nothing consumes
#                 is inert, and inert is indistinguishable from correct.
#   R2 REGRESSION every ticked hard-gated acceptance box already committed in `docs/tasks/` must
#                 STILL be accepted by the effective signature set. The corpus is the project's
#                 own history, so there are no fixtures to go stale — narrowing the tokens, or
#                 losing them, makes previously-passing evidence fail.
#   R3 OVER-MATCH no file under a declared prose path is classified as a code change.
#   R4 UNDER-MATCH every path family that genuinely governs behaviour IS so classified.
#   R5 VOCABULARY every enumerating instrument the census gate accepts is also accepted as
#                 evidence by the acceptance gate. This is the structural guard: the divergence
#                 between those two lists caused three refusals of honest evidence, and a rule
#                 that compares them cannot be re-introduced by someone editing one side.
#
# The built-in defaults are EXTRACTED from the neutral check rather than copied, so a spine
# update changes this check's baseline instead of drifting away from it. If they cannot be
# extracted the check REFUSES (exit 2): it cannot judge, and reporting "the rule holds" over an
# absence is the failure mode this whole file is about.
#
# ⚠️ HONEST LIMIT: this proves the seams still classify and still accept. It cannot prove the
# classification is the RIGHT one — that judgement is recorded in
# `docs/decisions/reference_upstream-spine-defects.md` and in each seam file's own header.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

NEUTRAL="scripts/check_task_acceptance.sh"
TOKENS=".doctrine/evidence_tokens.txt"
PATHS=".doctrine/code_paths.txt"

# Prose families that must never be classified as a code change here.
PROSE_PATHS='^docs/book/src/'
# Path families that MUST be classified as a code change: editing any of them alone changes
# what this repository does. Stated as patterns, not as a count, so the rule cannot go stale.
declare -a MUST_BE_CODE=(
  '^\.githooks/'
  '^\.github/workflows/'
  '^Cargo\.(toml|lock)$'
  '^\.doctrine/'
  '^doctrine/.*\.tsv$'
  '^docs/tasks/artifacts/.*\.sh$'
  '^scripts/.*\.sh$'
  '^crates/'
)

# ── the EFFECTIVE rules, ASKED OF THEIR OWNER rather than re-implemented ─────────────────────
# ⛔ An earlier version of this file mirrored the acceptance gate's composition by hand. The gate
# then gained a fourth input and this check kept scoring against the old three — it reported a
# vocabulary gap that did not exist, and would equally have missed one that did. A sibling that
# re-implements a rule drifts the moment the rule changes, invisibly. The owner now prints its
# own effective rules and this check consumes them.
extract_default_sig()  { sed -n "s/^DEFAULT_SIG='\(.*\)'$/\1/p" "$NEUTRAL" | head -1; }
extract_default_code() { sed -n "s/^default_code_re='\(.*\)'$/\1/p" "$NEUTRAL" | head -1; }

effective_sig()     { "$NEUTRAL" --print-sig 2>/dev/null; }
effective_code_re() { "$NEUTRAL" --print-code-re 2>/dev/null; }

# The historical unanchored pattern, kept ONLY as a regression fixture for the self-test: it is
# the exact shape that classified 28 files of mdBook prose as a code change.
HISTORICAL_OVERMATCH_RE='(^|/)(crates|src|scripts)/|\.(rs|sh)$|(^|/)Makefile$'

# ── R2: every ticked hard-gated box in a corpus must match the signature set ─────────────────
# Extracts each ticked box's own bullet (the "- [x] …" line plus its indented continuation),
# the same scoping the neutral check uses — a token elsewhere in the file must not count.
boxes_regression() { # $1 signature regex  $2 directory of task files
  local sig="$1" dir="$2" bad=0 f tmp
  tmp="$(mktemp)"
  while IFS= read -r f; do
    case "$f" in */TEMPLATE.md) continue ;; esac
    [ -r "$f" ] || continue
    awk '
      BEGIN { inbox = 0 }
      {
        line = $0
        isbox = (line ~ /^[[:space:]]*-[[:space:]]*\[[xX]\]/)
        if (isbox) {
          low = tolower(line)
          if (low ~ /root.?cause/ || low ~ /addressed/ || low ~ /no.?regress/) {
            if (inbox) print "\036"
            inbox = 1; print; next
          }
          if (inbox) { print "\036"; inbox = 0 }
          next
        }
        if (inbox) {
          if (line ~ /^[[:space:]]+/ || line ~ /^[[:space:]]*$/) { print; next }
          print "\036"; inbox = 0
        }
      }
      END { if (inbox) print "\036" }
    ' "$f" > "$tmp"
    local box=""
    while IFS= read -r l; do
      if [ "$l" = $'\036' ]; then
        if [ -n "$box" ] && ! printf '%s' "$box" | grep -qE "$sig"; then
          echo "  REGRESSED $f: a box that was accepted when it was committed no longer matches"
          echo "    $(printf '%s' "$box" | head -1 | cut -c1-96)"
          bad=1
        fi
        box=""
      else
        box="$box$l"$'\n'
      fi
    done < "$tmp"
  done < <(git ls-files "$dir" 2>/dev/null | grep -E '\.md$' || true)
  rm -f "$tmp"
  return "$bad"
}

# ── R5: the two gates must agree on what an instrument is ────────────────────────────────────
# Behavioural, not a presence check: each literal alternative of the census gate's own accepted
# list is turned into a sample evidence line and required to match the acceptance signature.
vocabulary_agreement() { # $1 acceptance signature  $2 path to the census gate
  local sig="$1" gate="$2" census alt bad=0 missed=0
  [ -f "$gate" ] || { echo "  NO CENSUS GATE $gate is missing; the vocabularies cannot be compared"; return 1; }
  census="$(sed -n "s/^CENSUS_RE='\(.*\)'$/\1/p" "$gate" | head -1)"
  [ -n "$census" ] || { echo "  NO CENSUS LIST $gate no longer defines CENSUS_RE in the expected shape"; return 1; }
  # Strip parenthesised groups BEFORE splitting: splitting the raw regex on `|` shreds
  # `searched (the|all|every)` into the bare fragments `all` and `every)`, which are not
  # instruments and produced two phantom gaps.
  census="$(printf '%s' "$census" | sed 's/([^)]*)//g')"
  local IFS='|'
  for alt in $census; do
    case "$alt" in ''|*'('*|*')'*|*'['*|*']'*|*'?'*|*'+'*|*'*'*) continue ;; esac
    # ⚠️ PROSE, not instruments. The census gate deliberately accepts an author WRITING that no
    # census was run; the acceptance gate has no business treating a sentence as tool output.
    # This list is a carried constant and is therefore small and visible: a new prose phrase in
    # the census gate surfaces here as a reported gap, which is a decision someone must make
    # rather than a drift nobody sees.
    case "$alt" in 'a search of'|'searched '|'census:') continue ;; esac
    if ! printf 'evidence: %s foo' "$alt" | grep -qE "$sig"; then
      echo "  VOCABULARY GAP the census gate accepts '$alt' but the acceptance gate does not"
      missed=$((missed+1)); bad=1
    fi
  done
  [ "$bad" -eq 0 ] || echo "  ($missed instrument(s) an author could be told to use and then refused for using)"
  return "$bad"
}

# ── R3/R4: classification properties over a list of paths on stdin ───────────────────────────
code_class_properties() { # $1 code regex  (paths on stdin)
  local re="$1" bad=0 all n
  all="$(cat)"
  n="$(printf '%s\n' "$all" | grep -E "$PROSE_PATHS" | grep -cE "$re" || true)"
  if [ "${n:-0}" -gt 0 ]; then
    echo "  OVER-MATCH $n prose file(s) under ${PROSE_PATHS} classified as a code change"
    printf '%s\n' "$all" | grep -E "$PROSE_PATHS" | grep -E "$re" | head -3 | sed 's/^/    /'
    bad=1
  fi
  local fam present missing
  for fam in "${MUST_BE_CODE[@]}"; do
    present="$(printf '%s\n' "$all" | grep -cE "$fam" || true)"
    [ "${present:-0}" -gt 0 ] || continue          # family absent from this tree: nothing to assert
    missing="$(printf '%s\n' "$all" | grep -E "$fam" | grep -vcE "$re" || true)"
    if [ "${missing:-0}" -gt 0 ]; then
      echo "  UNDER-MATCH $missing file(s) matching $fam are NOT classified as a code change"
      printf '%s\n' "$all" | grep -E "$fam" | grep -vE "$re" | head -3 | sed 's/^/    /'
      bad=1
    fi
  done
  return "$bad"
}

# ── self-test ────────────────────────────────────────────────────────────────────────────────
# ⛔ The arms call the functions IN PROCESS and shadow the globals with `local`. Two earlier
# versions of this block were wrong in the same way and both reported PASS: one mangled a
# pattern through `bash -c` quoting, the other produced a fixture holding the literal text
# `\n` instead of newlines, so the family under test was never present and the arm asserted
# nothing. A control that passes because it tested the wrong thing is worse than no control —
# which is the failure mode this whole file exists for, met twice while writing it.
self_test() {
  SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"
  local full narrow
  full="$(effective_sig)"; [ -n "$full" ] || { echo "seam self-test: the owner printed no signature set" >&2; return 1; }
  narrow="$(extract_default_sig)"

  score() { # name expected_rc expected_substring actual_rc actual_out
    if [ "$4" != "$2" ]; then
      fail=$((fail+1)); printf 'SEAM-INTEGRITY self-test MISS: %s expected rc=%s got rc=%s\n%s\n' "$1" "$2" "$4" "$5" >&2
    elif [ -n "$3" ] && ! printf '%s' "$5" | grep -qF "$3"; then
      fail=$((fail+1)); printf 'SEAM-INTEGRITY self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' "$1" "$3" "$5" >&2
    else pass=$((pass+1)); fi
  }

  # ---- R2: a committed box whose evidence is a plain census — the exact shape refused three
  # times before the tokens were declared.
  {
    printf '%s\n' '- [x] **ROOT CAUSE (WHY + WHERE)** — census over the pinned chapters:'
    printf '%s\n' '  `grep -ci reset rv32.txt rv64.txt` -> `rv32.txt:0`, `rv64.txt:0`.'
    printf '\n'
    printf '%s\n' '- [x] **ADDRESSED (verified)** — `README-ROUTING-CLOSURE: ok (24 governed destination(s))`.'
  } > "$t/leaf.md"
  ( cd "$t" && git init -q . && git add leaf.md ) >/dev/null 2>&1
  out="$( cd "$t" && boxes_regression "$full" . 2>&1 )"; rc=$?
  score "GREEN declared tokens still accept a committed box" 0 "" "$rc" "$out"
  out="$( cd "$t" && boxes_regression "$narrow" . 2>&1 )"; rc=$?
  score "RED   losing the tokens regresses a committed box" 1 "REGRESSED" "$rc" "$out"

  # ---- R3/R4: classification properties, with the globals shadowed for the duration.
  # ⛔ The fixture is built with printf, one path per line, and its line count is ASSERTED —
  # a fixture that silently collapses to one line is how the previous arm lied.
  local fixture PROSE_PATHS
  fixture="$t/paths.txt"
  printf '%s\n' 'docs/book/src/claim-scope.md' '.githooks/pre-commit' \
                'doctrine/readme_routes.tsv' 'crates/app/src/main.rs' 'Cargo.toml' > "$fixture"
  if [ "$(wc -l < "$fixture" | tr -d ' ')" != 5 ]; then
    fail=$((fail+1)); echo "SEAM-INTEGRITY self-test MISS: the path fixture is not 5 lines" >&2
  fi
  PROSE_PATHS='^docs/book/src/'
  local -a MUST_BE_CODE=( '^\.githooks/' '^doctrine/.*\.tsv$' '^Cargo\.(toml|lock)$' '^crates/' )

  out="$(code_class_properties "$(effective_code_re)" < "$fixture" 2>&1)"; rc=$?
  score "GREEN declared classification holds both properties" 0 "" "$rc" "$out"
  out="$(code_class_properties "$HISTORICAL_OVERMATCH_RE" < "$fixture" 2>&1)"; rc=$?
  score "RED   the historical unanchored pattern over-matches prose" 1 "OVER-MATCH" "$rc" "$out"
  out="$(code_class_properties '^crates/' < "$fixture" 2>&1)"; rc=$?
  score "RED   a narrowed pattern under-matches behaviour files" 1 "UNDER-MATCH" "$rc" "$out"
  out="$(code_class_properties '.' < "$fixture" 2>&1)"; rc=$?
  score "RED   a pattern matching everything over-matches prose" 1 "OVER-MATCH" "$rc" "$out"

  # ---- R5: vocabulary agreement
  out="$(vocabulary_agreement "$full" scripts/check_gap_claims.sh 2>&1)"; rc=$?
  score "GREEN the two gates agree on what an instrument is" 0 "" "$rc" "$out"
  out="$(vocabulary_agreement 'test result: (ok|FAILED)' scripts/check_gap_claims.sh 2>&1)"; rc=$?
  score "RED   an acceptance set that ignores the census list" 1 "VOCABULARY GAP" "$rc" "$out"
  out="$(vocabulary_agreement "$full" "$t/absent.sh" 2>&1)"; rc=$?
  score "RED   the census gate is gone, so nothing can be compared" 1 "NO CENSUS GATE" "$rc" "$out"

  rm -rf "$t"
  printf 'SEAM-INTEGRITY --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

# ── refuse rather than skip ───────────────────────────────────────────────────────────────────
[ -f "$NEUTRAL" ] || {
  echo "SEAM-INTEGRITY: REFUSED — $NEUTRAL is missing; the seams it consumes cannot be judged." >&2; exit 2; }
if [ -z "$(extract_default_sig)" ] || [ -z "$(extract_default_code)" ]; then
  { echo "SEAM-INTEGRITY: REFUSED — cannot extract the neutral check's built-in defaults from"
    echo "  $NEUTRAL. Its shape changed, so this check's baseline is unknown and a green verdict"
    echo "  would be a guess. Re-derive the extraction before trusting either gate."; } >&2
  exit 2
fi
self_test >/dev/null 2>&1 || {
  echo "SEAM-INTEGRITY: REFUSED — the check does not discriminate (self-test failed)." >&2; exit 2; }

fail=0; report=""
# R1 — the seams exist and are still CONSUMED by the neutral check.
for f in "$TOKENS" "$PATHS"; do
  if [ ! -s "$f" ]; then
    report="$report  MISSING $f — the declaration that fixes a spine defect here is gone"$'\n'; fail=1; continue
  fi
  base="${f##*/}"
  grep -qF "$base" "$NEUTRAL" || {
    report="$report  INERT $f — $NEUTRAL no longer reads it, so the declaration protects nothing"$'\n'; fail=1; }
done

sig="$(effective_sig)";  [ -n "$sig" ] || {
  echo "SEAM-INTEGRITY: REFUSED — $NEUTRAL --print-sig produced nothing; cannot judge." >&2; exit 2; }
code_re="$(effective_code_re)"; [ -n "$code_re" ] || {
  echo "SEAM-INTEGRITY: REFUSED — $NEUTRAL --print-code-re produced nothing; cannot judge." >&2; exit 2; }

# R2 — the project's own committed acceptance boxes must still be accepted.
out="$(boxes_regression "$sig" docs/tasks)" || fail=1
report="$report$out"
# R3/R4 — classification properties over the tracked tree.
out="$(git ls-files | code_class_properties "$code_re")" || fail=1
report="$report$out"
# R5 — the acceptance gate must accept every instrument the census gate blesses.
out="$(vocabulary_agreement "$sig" scripts/check_gap_claims.sh)" || fail=1
report="$report$out"

if [ "$fail" -ne 0 ]; then
  { echo "SEAM-INTEGRITY: a declared seam no longer does the job it was declared for."
    printf '%s' "$report" | grep -v '^$'
    echo "  These declarations fix defects in the neutral spine checks (see"
    echo "  docs/decisions/reference_upstream-spine-defects.md). Restoring the file is the fix;"
    echo "  weakening this check is not."; } >&2
  exit 1
fi
printf 'SEAM-INTEGRITY: ok (%s committed acceptance box(es) still accepted; classification properties hold)\n' \
  "$(git ls-files docs/tasks | grep -E '\.md$' | grep -v TEMPLATE | xargs grep -hcE '^[[:space:]]*-[[:space:]]*\[[xX]\]' 2>/dev/null | paste -sd+ - | bc 2>/dev/null || echo '?')"
exit 0
