#!/usr/bin/env bash
# LS-002 reproduction: a quoted atom and a bare atom produce the same value.
# usage:  bash repro.sh <path to lispish_file binary> [path to Lispish.spec]
set -uo pipefail
BIN="${1:?usage: $0 <lispish_file binary> [grammar.spec]}"
GRAMMAR="${2:-}"
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ARGS=(); [ -n "$GRAMMAR" ] && ARGS=(--grammar "$GRAMMAR")
v() { "$BIN" "${ARGS[@]}" "$HERE/cases/$1" 2>/dev/null | head -1; }
A="$(v 01-bare-numeric.sexp)";  B="$(v 02-quoted-numeric.sexp)"
C="$(v 04-bare-version.sexp)";  D="$(v 03-quoted-version.sexp)"
printf '  (v 20260911)     -> %s\n  (v "20260911")   -> %s\n' "$A" "$B"
printf '  (v 1.0)          -> %s\n  (v "1.0")        -> %s\n' "$C" "$D"
echo
same=0
[ "$A" = "$B" ] && { echo '  SAME VALUE: bare and quoted numeric are indistinguishable.'; same=1; }
[ "$C" = "$D" ] && { echo '  SAME VALUE: bare and quoted version are indistinguishable.'; same=1; }
[ "$same" = 1 ] && echo '  => a consumer cannot round-trip, and cannot recover the source token kind.'
exit 0
