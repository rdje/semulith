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
  "README-ROUTING-CLOSURE|every destination the landing page routes to is governed, exists, and stays under its ceiling — a cap that only displaces pressure has not removed it|scripts/check_readme_routes.sh"
  "SEAM-INTEGRITY|the source fixes and declared seams still do their job — every committed acceptance box is still accepted, prose is not code, behaviour files are, and the two gates agree on what an instrument is|scripts/check_seam_integrity.sh"
  "PROFILE-CONSISTENCY|a profile dossier's declared counts equal its enumeration, and every decision carries an authority and a source — a laboratory policy must never read as an architectural rule|scripts/check_profile_consistency.sh"
  "FRONTIER-SYNC|the task-tree index mirrors the trees it indexes — the frontier leaf, the status and the leaf counts are re-derived, never remembered|scripts/check_frontier_sync.sh"
  "REGISTRY-MIRROR|the doctrine documents list exactly the doctrines the drivers register — a mirror that falls behind withholds a guarantee rather than inventing one|scripts/check_registry_mirror.sh"
  "UPSTREAM-INDEX|a defect raised against a dependency is tracked like our own — the issue subtree owns its state and is self-contained, and every index of it is a checked mirror|scripts/check_upstream_index.sh"
  "TREE-CLAIMS|every LIVE document states leaf counts, the active trees and the frontier leaf exactly as the trees do — scope read from the routes registry, so history is never rewritten|scripts/check_tree_claims.sh"
  "DERIVED-COUNTS|a live document that states a count of something this repository can enumerate has it RE-DERIVED — a running total is a memory of a measurement, not a measurement|scripts/check_derived_counts.sh"
  "RECORD-SCHEMA|every tracked record file validates against its schema, cites only sources the profile pinned, and states what its profile states — a catalogue that looks checkable and is not is worse than none|scripts/check_requirements.sh"
  "GATE-REPORT|the tracked gate report is still the function of its inputs that generated it — a hand-edited report is how a project comes to hold a verdict nothing produced|scripts/check_gate_report.sh"
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
