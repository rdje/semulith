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
  "SOURCE-FORMAT|every source of truth the engine extracts from is in the one format — a retired-format file in a source-of-truth family is refused by name, and every .sexp there parses with the one reader, so the split cannot return by accident|scripts/check_source_format.sh"
  "UNIT-COMPOSITION|a unit's composed encoding space is decided — the composition document is schema-conformant, its fragments resolve with dependencies met through the one shared resolver, the union is collision-free, and a partial composition is declared, never inferred from silence|scripts/check_unit_composition.sh"
  "SEMANTICS|the execution authority's corpus holds — every semantics document checks against its fragment (well-formed, complete, cited), the refinement rule refuses a silent override across a unit's fragments, and locators resolve against the pinned artifact offline, with a named skip rather than a green lie when the cache cannot judge|scripts/check_semantics_corpus.sh"
  "EXTRACTION|the definition is sufficient for an engine — every declared instruction has an encoding AND semantics AND a requirement (one set, four ways), every state element a reset, every obligation its checks; P1-LAB cites this verdict instead of a judgement call|scripts/check_extraction.sh"
  "FACT-OWNERSHIP|the no-duplicated-fact rule holds — every fact kind has exactly one owning file in doctrine/fact_ownership.tsv, every derived mirror names a governing doctrine that runs, and every restatement pair the corpus actually has is registered; an ungoverned mirror is how one fact quietly becomes two|scripts/check_fact_ownership.sh"
  "SCOPE-COVERAGE|no model code starts against an uncovered scope — a unit's registry declares the categories its scope requires, and the gate refuses the day a required category is missing or has no census row; P1-LAB's precondition is this verdict, composed with (never duplicated from) EXTRACTION|scripts/check_scope_coverage.sh"
  "GATE-REPORT|the tracked gate report is still the function of its inputs that generated it — a hand-edited report is how a project comes to hold a verdict nothing produced|scripts/check_gate_report.sh"
  "SHARD-FREEZE|the sharded append-history is frozen and whole — every shard hashes to its manifest row, the manifest only grows, and no entry is duplicated across head and shards|scripts/check_changelog_shards.sh"
  "PORT-WEB|the crate skeleton builds for the browser target — the workspace compiles for wasm32-unknown-unknown, so a host-only API cannot slip into the engine unnoticed; fired RED before registration|scripts/check_wasm_build.sh"
  "STATE-GEN|the generated state module is still the byte-exact function of the state descriptor that generated it — a hand-edited accessor is how a descriptor and its executable half quietly become two facts; fired RED before registration|scripts/check_state_gen.sh"
  "DEF-GEN|the generated definition module is still the byte-exact function of the canonical definition that generated it — encoding tables, lowered semantics trees, and OWN-03's manifest with definition, generator, configuration and source fingerprints; a hand-edited decode row or effect tree is OWN-01's duplicate owner arriving as drift; fired RED before registration|scripts/check_definition_gen.sh"
  "GUEST-GEN|the generated guest fixture is still the byte-exact function of the tracked guests and their specification-derived expectations — a hand-edited expectation or word list is how the offline differential (the commit gate's re-run of the first execution slice) quietly stops testing what the tracked documents declare; the generator refuses by name what it cannot emit; fired RED before registration|scripts/check_guest_gen.sh"
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
