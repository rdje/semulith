#!/usr/bin/env bash
# KNOWLEDGE-MAP: drift fails1; unavailable generation/comparison refuses2.
set -uo pipefail
refuse(){ printf 'KNOWLEDGE-MAP: REFUSED — %s\n' "$1" >&2; exit 2; }
ROOT="$(git rev-parse --show-toplevel)" || refuse 'repository root unavailable'
cd "$ROOT" || refuse 'repository root unavailable'
gen="$ROOT/knowledge-map/scripts/gen_knowledge_map.sh"
MAP="$("$gen" --print-map-path)" || refuse 'destination discovery failed'
if [ ! -f "$MAP" ]; then
  printf '%s\n' 'KNOWLEDGE-MAP: KNOWLEDGE_MAP.md is missing — regenerate it' >&2
  exit 1
fi
mkdir -p "$ROOT/target/tmp" || refuse 'scratch directory unavailable'
tmp="$(mktemp -d "$ROOT/target/tmp/knowledge-map-check.XXXXXX")" || refuse 'scratch allocation failed'
trap 'rm -rf -- "$tmp"' EXIT
"$gen" > "$tmp/render" || refuse 'generator failed'
diff -q "$tmp/render" "$MAP" > /dev/null 2> "$tmp/diff-error"
rc=$?
case "$rc" in
  0) exit 0;;
  1) printf '%s\n' 'KNOWLEDGE-MAP: KNOWLEDGE_MAP.md is out of sync with its sources — regenerate it' >&2; exit 1;;
  *) refuse 'map comparison unavailable';;
esac
