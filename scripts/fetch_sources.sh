#!/usr/bin/env bash
# scripts/fetch_sources.sh — acquire and verify a profile's pinned specification sources.
#
# ⛔ DELIBERATELY NOT A COMMIT GATE. It needs the network, and a gate that needs the network
# fails for reasons that have nothing to do with the change being committed — which is how a
# gate becomes something people routinely bypass. Run it on demand: when adopting a profile,
# when a locator looks wrong, or before a release report cites a specification section.
#
# What a verdict means (and this is the part worth reading):
#   MATCH     the artifact you are about to read is byte-identical to the one the dossier's
#             locators were written against.
#   DIFFERS   the RENDERING changed. That is not evidence of a semantic change — the site
#             template may have moved — but it is a instruction to RE-READ the cited sections
#             and re-confirm the locators before relying on them.
#   Neither verdict proves the NORMATIVE text is unchanged; the normative identity is the
#   revision plus the chapter version, and no digest can establish that on its own.
#
# Usage:  scripts/fetch_sources.sh [<profile-id>]      (default: rv64i-lab-v0)
#         scripts/fetch_sources.sh --verify-only <id>  (fail if anything DIFFERS)
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

verify_only=0
if [ "${1:-}" = "--verify-only" ]; then verify_only=1; shift; fi
profile="${1:-rv64i-lab-v0}"
ledger="profiles/$profile/sources.sexp"

[ -f "$ledger" ] || { echo "fetch-sources: no ledger at $ledger" >&2; exit 2; }
command -v curl >/dev/null 2>&1 || { echo "fetch-sources: curl is not on PATH" >&2; exit 2; }
command -v python3 >/dev/null 2>&1 || { echo "fetch-sources: python3 is not on PATH" >&2; exit 2; }

sha256_of() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | cut -d' ' -f1
  elif command -v shasum >/dev/null 2>&1; then shasum -a 256 "$1" | cut -d' ' -f1
  else return 3; fi
}
sha256_of /dev/null >/dev/null 2>&1 || { echo "fetch-sources: no sha256 tool on PATH" >&2; exit 2; }

# SOT-FORMAT.4: the ledger is S-expression, read through dossier_sexp — the mapping owner.
# This retires the sed line-extraction (and its measured trailing-comment hazard: a greedy
# capture once returned `work_dir` with the line's comment attached, and the fetch created a
# directory with that literal name while reporting green MATCHes). Values come from the
# parsed document now; comments are data, and a verdict cannot be right about the bytes and
# wrong about where it read them.
field() { python3 - "$ledger" "$1" <<'PYFIELD'
import sys
sys.path.insert(0, "scripts")
import dossier_sexp as D
doc = D.load_sources(sys.argv[1])
print(doc.get(sys.argv[2], ""))
PYFIELD
}
base_url="$(field base_url)"; work_dir="$(field work_dir)"; revision="$(field revision)"
[ -n "$base_url" ] && [ -n "$work_dir" ] || { echo "fetch-sources: ledger lacks base_url/work_dir" >&2; exit 2; }
mkdir -p "$work_dir"

printf 'fetch-sources: profile %s, revision %s -> %s\n' "$profile" "$revision" "$work_dir"
differs=0; checked=0
# The (source …) blocks, in order: file + sha256 per row, from the parsed document.
pins() { python3 - "$ledger" <<'PYPINS'
import sys
sys.path.insert(0, "scripts")
import dossier_sexp as D
for s in D.load_sources(sys.argv[1]).get("source", []):
    print(f"{s['file']}\t{s['sha256']}")
PYPINS
}
pins | while IFS=$'\t' read -r f want; do
    [ -n "$f" ] || continue
    code="$(curl -sS --max-time 60 -o "$work_dir/$f" -w '%{http_code}' "$base_url/$f" 2>/dev/null)"
    got="$(sha256_of "$work_dir/$f" 2>/dev/null)"
    if [ "$code" != "200" ]; then
      printf '  UNREACHABLE %-12s HTTP %s\n' "$f" "$code"
    elif [ "$got" = "$want" ]; then
      printf '  MATCH       %-12s %s\n' "$f" "$got"
    else
      printf '  DIFFERS     %-12s pinned %s\n              %-12s actual %s\n' "$f" "$want" "" "$got"
      printf '              the RENDERING changed — re-read the cited sections and re-confirm\n'
      printf '              the locators before relying on them; this is not, by itself,\n'
      printf '              evidence that the normative text changed.\n'
    fi
  done

# The loop above runs in a subshell, so re-derive the verdict here for the exit code.
if [ "$verify_only" = 1 ]; then
  bad=0
  pins > "$work_dir/.pins"
  while IFS=$'\t' read -r f want; do
    [ -n "$f" ] || continue
    [ -f "$work_dir/$f" ] || { bad=1; continue; }
    [ "$(sha256_of "$work_dir/$f")" = "$want" ] || bad=1
  done < "$work_dir/.pins"
  rm -f "$work_dir/.pins"
  [ "$bad" -eq 0 ] || { echo "fetch-sources: at least one source differs from its pin" >&2; exit 1; }
fi
exit 0
