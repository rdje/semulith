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
  "BOARD-GEN|a board's manifest, composed catalogues, hardware description and map are still the byte-exact function of its canonical board definition — the freshness proof compose_units.py defers to the first tracked board; a hand-edited wiring row or a stale composed catalogue is how the definition and its downstream quietly become two facts; fired RED before registration (P5-BOARD.3)|scripts/check_board_gen.sh"
  "BOARD-VERDICT|a board's composition verdict is decided, not narrated — every CPU environment-assumption in the composed unit is discharged by named guarantees, every satisfies edge in the board definition resolves to a discharged assumption, and every device obligation the dossier defers to the board (composition_disposition required) is answered by exactly one decision answers edge; an unmatched assumption or a dangling edge is a REJECTION by name, never a note (CPU_ENVIRONMENT.md §5, ENV-02; P5-BOARD.4)|scripts/check_board_verdict.sh"
  "PLATFORM-GEN|a board's platform capability manifest is still the byte-exact function of its canonical inputs (the board definition, the pinned processor's profile dossier, the composed obligations) — and the board's dossier-sha256 pin is verified against the live dossier at derivation, so the measured display-only pin became load-bearing (OWN-06; P5-BOARD.6)|scripts/check_platform_gen.sh"
  "EXERCISE-COVERAGE|every form a profile DECLARES in its scope is EXECUTED by a tracked guest — coverage reported with its denominator (count_total re-derived against the enumeration), the SCP-02 closure resolved through the one shared resolver; composes with EXTRACTION (static sufficiency) by measuring the dynamic half; fired RED against the real corpus at 15/52 before registration, GREEN at 52/52 (P2-SCALAR.1)|scripts/check_exercise_coverage.sh"
  "INTERACTION-MATRIX|the declared fault × alias × boundary × event × progress × restart matrix is declared first and exercised — the cells are RE-DERIVED from the declared axes (an omitted cell fails, named), every disposition resolves (a guest with source AND expectations, the closed mechanism registry, a degenerate cell with its reason), no tracked guest is an orphan, and every difference id the matrix names exists in references.sexp; fired RED against the real corpus before registration (P2-SCALAR.4)|scripts/check_interaction_matrix.sh"
  "MATERIALS-BILL|every modelled unit's book carries a materials bill whose identity tables are GENERATED from the pinned dossier (drift refused — a digest cannot rot) and whose prose states, for every material, what it does NOT supply — a missing section or a missing negative statement fails by name; fired RED against the real corpus before registration (MODEL-BOOKS.1)|scripts/check_materials_bill.sh"
  "UNIT-BOOKS|every registered modelled unit has its own mdBook and it builds — a unit without a book, a book that does not build, or a book under docs/models/ that no unit registers fails by name; the one registration place is materials/units.sexp; fired RED against the real corpus before registration (MODEL-BOOKS.6)|scripts/check_unit_books.sh"
  "DOSSIER-SCHEMA|every tracked dossier document whose basename (or document family) has a schema validates against it through the one checker — a schema nothing enforces is documentation, not a contract; documents without a same-named schema are skipped and counted BY NAME, never silently; fired RED before registration against the pre-fix D-FENCE document recovered from git history (the duplicated-note drift it exists to catch, P3-BREADTH.7)|scripts/check_dossier_schema.sh"
  "PUSH-RECORD|the push-approval ledger is append-only and every entry well-formed — a staged change must keep HEAD's content a PREFIX of the new content (history is never rewritten), and every entry carries who/when/why/range with sequential ids; fired RED against the real corpus before registration (PUSH-DISCIPLINE.3)|scripts/check_push_record.sh"
  "COMMIT-PREFIX|the commit-msg hook pins the SEMULITH- work-unit prefix — a SEMILITH- subject is refused with SEMULITH named, a SEMULITH- subject passes; the probe is behavioural, so a scaffold sync that reverts the neutral hook turns the very next commit RED; fired RED against the real tree before the pin existed (PREFIX-DISCIPLINE.1)|scripts/check_commit_prefix.sh"
  "BOOK-INDEX|the book's index is still what the book's own text derives — a hand-edited or stale index is a running total, and a running total is a memory of a measurement, not a measurement; the generator refuses a shape it cannot emit (a missing chapter, an undeclared chapter set) by name; fired RED against the real book before registration (BOOK-APPARATUS.1)|scripts/check_book_index.sh"
  "CITATION-QUOTES|every quoted phrase a tracked source-of-truth document attributes to a pinned section occurs IN that section — a locator that resolves but names the wrong section is refused, naming where the phrase is; judged when the pinned pages are present, a NAMED SKIP otherwise|scripts/check_citation_quotes.sh"
  "FP-VECTORS|the floating-point model layer's unit vectors are still the byte-exact output of the spec-side exact-rational IEEE reference, and that reference still agrees with the host's hardware IEEE on directed ties and seeded cases — an expected value edited by hand is DRIFT|scripts/check_fp_vectors.sh"
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
