#!/usr/bin/env bash
# scripts/check_doctrines.project.sh — THE PROJECT-SPECIFIC DOCTRINE SLOT.
#
# Semulith's own mechanizable doctrines. Runs LAST in scripts/check_doctrines.sh; exit 0 = all
# project doctrines pass, nonzero (with a message on stderr) = a breach that blocks the commit.
#
# ⭐ Every check registered here MUST ship a `--self-test` whose RED arms have been observed
# failing, and must assert the REASON as well as the verdict. `docs/CLAIM_VERIFICATION.md`:
# a control never seen RED is not known to work, and one that goes red for the wrong reason
# cannot fail on the thing it was written for. Each check re-runs its own self-test before
# judging and REFUSES (exit 2) rather than passing if it no longer discriminates.
#
# Keep each check cheap and deterministic. Anything heavier than a few seconds belongs in CI.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

# id|what it proves|script
PROJECT_DOCTRINES=(
  "DELIVERY-PROVENANCE|every delivered manifest row has a declared disposition, and the frozen ones still hash to the delivered bytes|scripts/check_delivery_provenance.sh"
  "FIXTURE-FINGERPRINT|every record pinning a file's sha256 still describes the tree — a carried constant is derived or gated, never trusted|scripts/check_fixture_fingerprints.sh"
)

fails=0
for entry in "${PROJECT_DOCTRINES[@]}"; do
  id="${entry%%|*}"; rest="${entry#*|}"; proves="${rest%%|*}"; path="${rest##*|}"
  if [ ! -x "$path" ]; then
    echo "PROJECT/$id: missing or not executable: $path ($proves)" >&2
    fails=$((fails+1)); continue
  fi
  if ! out="$("$path" 2>&1)"; then
    printf '%s\n' "$out" >&2
    fails=$((fails+1))
  fi
done

[ "$fails" -eq 0 ] || exit 1
exit 0
