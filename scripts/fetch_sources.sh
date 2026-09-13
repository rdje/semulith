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
ledger="profiles/$profile/sources.toml"

[ -f "$ledger" ] || { echo "fetch-sources: no ledger at $ledger" >&2; exit 2; }
command -v curl >/dev/null 2>&1 || { echo "fetch-sources: curl is not on PATH" >&2; exit 2; }

sha256_of() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | cut -d' ' -f1
  elif command -v shasum >/dev/null 2>&1; then shasum -a 256 "$1" | cut -d' ' -f1
  else return 3; fi
}
sha256_of /dev/null >/dev/null 2>&1 || { echo "fetch-sources: no sha256 tool on PATH" >&2; exit 2; }

# ⛔ `[^"]*` and a trailing `.*`, not `.*`: an unanchored greedy capture leaves the line's
# trailing comment in the result. Measured — `work_dir` came back as
# `target/sources/riscv-v20260120   # repo-volume, untracked` and the fetch created a
# directory with that literal name, while still reporting three green MATCHes. A verdict can
# be correct about the bytes and wrong about where it read them.
field() { sed -n "s/^$1 *= *\"\([^\"]*\)\".*/\1/p" "$ledger" | head -1; }
base_url="$(field base_url)"; work_dir="$(field work_dir)"; revision="$(field revision)"
[ -n "$base_url" ] && [ -n "$work_dir" ] || { echo "fetch-sources: ledger lacks base_url/work_dir" >&2; exit 2; }
mkdir -p "$work_dir"

printf 'fetch-sources: profile %s, revision %s -> %s\n' "$profile" "$revision" "$work_dir"
differs=0; checked=0
# Read the [[source]] blocks: file + sha256, in order.
paste -d'\t' \
  <(sed -n 's/^file *= *"\([^"]*\)".*/\1/p' "$ledger") \
  <(sed -n 's/^sha256 *= *"\([^"]*\)".*/\1/p' "$ledger") \
| while IFS=$'\t' read -r f want; do
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
  paste -d'\t' \
    <(sed -n 's/^file *= *"\([^"]*\)".*/\1/p' "$ledger") \
    <(sed -n 's/^sha256 *= *"\([^"]*\)".*/\1/p' "$ledger") > "$work_dir/.pins"
  while IFS=$'\t' read -r f want; do
    [ -n "$f" ] || continue
    [ -f "$work_dir/$f" ] || { bad=1; continue; }
    [ "$(sha256_of "$work_dir/$f")" = "$want" ] || bad=1
  done < "$work_dir/.pins"
  rm -f "$work_dir/.pins"
  [ "$bad" -eq 0 ] || { echo "fetch-sources: at least one source differs from its pin" >&2; exit 1; }
fi
exit 0
