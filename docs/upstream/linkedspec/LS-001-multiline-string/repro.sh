#!/usr/bin/env bash
# LS-001 reproduction. Self-contained: uses only the case files beside it.
#
# usage:  bash repro.sh <path to lispish_file binary> [path to Lispish.spec]
#
# Runs every case in cases/ and compares against cases/EXPECTED.tsv. Exits 0 when all match.
set -uo pipefail
BIN="${1:?usage: $0 <lispish_file binary> [grammar.spec]}"
GRAMMAR="${2:-}"
[ -x "$BIN" ] || { echo "not executable: $BIN" >&2; exit 2; }
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ARGS=(); [ -n "$GRAMMAR" ] && ARGS=(--grammar "$GRAMMAR")

echo "binary : $BIN"
echo "grammar: ${GRAMMAR:-<packaged default>}"
echo
pass=0; fail=0
while IFS=$'\t' read -r name want; do
  case "$name" in \#*|"") continue;; esac
  got="$("$BIN" "${ARGS[@]}" "$HERE/cases/$name" 2>/dev/null | head -1)"; rc=$?
  if [ "$got" = "$want" ]; then
    printf '  MATCH     %-28s %s\n' "$name" "$got"; pass=$((pass+1))
  else
    printf '  DIFFERS   %-28s\n              want: %s\n              got : %s   (exit %s)\n' \
           "$name" "$want" "${got:-<empty>}" "$rc"; fail=$((fail+1))
  fi
done < "$HERE/cases/EXPECTED.tsv"
echo
echo "LS-001: $pass matched / $fail differed"
[ "$fail" -eq 0 ]
