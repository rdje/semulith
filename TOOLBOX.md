# TOOLBOX.md — the tools-first diagnostic doctrine

⛔ **TOOLS-FIRST.** For ANY unknown — a failure, a crash, a hang, a surprising result, a
"why isn't this working" — reach for a diagnostic tool FIRST. Never eyeball the code and
guess a root cause.

## The rule

- A code change cannot land without **tool-backed WHY + WHERE** and a **measured
  before→after** recorded in its task-tree leaf (see the acceptance checklist in
  `DOCTRINE_ENFORCEMENT.md`).
- If no existing tool shows WHY+WHERE, **build one** — a probe, a tracer, a counter, a
  minimal reproduction harness. The diagnostic tool is a first-class deliverable, kept in
  the repo, not a throwaway.
- **ANTI-SPIN TRIPWIRE:** if you have analyzed for ~2 turns without producing NEW tool
  output that pinpoints WHY+WHERE, STOP — run a tool, build one, or escalate. Never loop
  on analysis.

## The 3-step UNKNOWN protocol (adapt the specific tools to your domain)

1. **WIDEN** — dump the full picture: enumerate all cases/states, the broadest inventory,
   so the failing one is visible in context.
2. **NARROW** — probe the specific failing case for its exact verdict + position/state.
3. **PINPOINT** — a scoped trace that names the exact function/rule/line that fails and why.

The point is to convert "it's broken somewhere" into "line X of function Y rejects input Z
because predicate P is false" before writing a single line of fix.

## This project's toolbox

Every diagnostic here is **tracked**, so a number it produced can be re-derived by the next
reader — that is leg 3 of `docs/CLAIM_VERIFICATION.md`, and an instrument living in a scratch
directory is a "trust me" with extra steps.

| Tool | Answers | How to invoke |
| --- | --- | --- |
| `scripts/check_doctrines.sh` | which doctrine is breached, and where? (the whole registry, one verdict per rule) | `make gate` |
| `scripts/check_delivery_provenance.sh` | has a delivered file drifted from the bytes we were given, and is every manifest row's treatment declared? | `scripts/check_delivery_provenance.sh` |
| `scripts/check_fixture_fingerprints.sh` | does every pinned `sha256` still describe the file it names? | `scripts/check_fixture_fingerprints.sh` |
| `scripts/check_readme_routes.sh` | is every destination the landing page routes to governed, and is any live surface near its ceiling? | `scripts/check_readme_routes.sh` |
| `scripts/check_profile_consistency.sh` | does a profile dossier contradict itself, or cite nothing? | `scripts/check_profile_consistency.sh` |
| `scripts/check_frontier_sync.sh` | does the task-tree index still name the leaf the tree itself calls next? | `scripts/check_frontier_sync.sh` |
| `scripts/check_registry_mirror.sh` | do the doctrine documents still list exactly the doctrines that are registered? | `scripts/check_registry_mirror.sh` |
| `scripts/check_tree_claims.sh` | does a live document state a leaf count, an active tree or a frontier leaf the trees contradict? | `scripts/check_tree_claims.sh` |
| `scripts/check_derived_counts.sh --list` | which counts in the live docs are re-derived, by what command, and what do they currently come to? | `scripts/check_derived_counts.sh [--list]` |
| `scripts/validate_records.py` | does this record file satisfy its schema, line by line? | `scripts/validate_records.py <records.jsonl> <schema.json>` |
| `scripts/records_sexp.py` | how does a converted catalogue map to records — and back? (the single owner of the JSON↔S-expression record mapping) | imported by the gate and `gate_report.py`; `R.load(path)`, `R.dump(records)` |
| `scripts/dossier_sexp.py` | how does a converted dossier document map to the dicts TOML/JSON produced — and back? (the single owner of the dossier mapping, `.4`) | imported by the gates and tools; `D.load(path)`, `D.load_{profile,sources,references,override,expectations}(path)`, `D.materialize_sail_override(repo, profile)` derives the Sail JSON from the tracked override.sexp |
| `scripts/convert_dossier.py` | did the dossier conversion lose anything — proven, not reviewed? | `scripts/convert_dossier.py to-sexp <src> <out.sexp> \| verify <src> <out.sexp>`; `verify` re-derives the TOML/JSON field-for-field, checks the comment census line-by-line, and validates against the schema layer |
| `scripts/merge_records.py` | do these two units' records compose — same id, same content; and does every reference resolve across the union? | `scripts/merge_records.py <unit-dir>…` (a unit directory carries `requirements.sexp` / `contract-obligations.sexp` / `sources.sexp` by name; `--self-test` fires the contradiction arms) |
| `scripts/discharge_assumptions.py` | is every environment-assumption discharged by a named guarantee — or does the composition fail, naming it? | `scripts/discharge_assumptions.py <unit-dir>…` (decides over `merge_units(…)`; `--self-test` fires the chain/zero-dep controls) |
| `scripts/check_source_format.sh` | is every source of truth still in the one format — or did the retired split return? | `scripts/check_source_format.sh [--self-test]` — refuses a tracked `.toml`/`.json`/`.jsonl`/`.yaml` under `definitions/ schema/ profiles/ materials/` and any `.sexp` there that `sexp.py` refuses |
| `scripts/convert_records.py` | did the record conversion lose anything — proven, not reviewed? | `scripts/convert_records.py to-sexp \| to-jsonl \| verify <a> <b>`; `--verify` re-derives the JSONL byte-identically |
| `scripts/gate_report.py` | what does the gate actually say right now, and why is it not `passed`? | `scripts/gate_report.py <profile> [--stdout]` |
| `scripts/compare_platforms.py` | what platform does each reference actually advertise, and where does it differ from the profile and from the other model? | `scripts/compare_platforms.py` |
| `scripts/sexp.py` | does this canonical-definition file parse, and what does it declare? | `scripts/sexp.py <file.sexp>` |
| `scripts/materials.py` | which primary sources does this project rely on, and is each one present and the document it claims to be? | `scripts/materials.py [--list \| --resolve <id> \| --fetch \| --verify]` |
| `scripts/sexp.py --self-test` | does the reader still return the bytes the file contains — escapes, non-ASCII, strings holding `;` ? | `scripts/sexp.py --self-test` |
| `scripts/gen_fragments.py` | regenerate the reusable definition fragments from the pinned tables | `scripts/gen_fragments.py` |
| `scripts/check_encoding_disjoint.py` | do these definition fragments COMPOSE — does any word match two instructions? | `scripts/check_encoding_disjoint.py <fragment…>` |
| `scripts/check_citations.py` | do the semantic citations RESOLVE — does every § they name exist in the artifact the profile pins? | `scripts/check_citations.py [<profile>]` |
| `scripts/check_semantics.py` | are this fragment's semantics well-formed, complete and cited? | `scripts/check_semantics.py <fragment.sexp> <semantics.sexp>` |
| `scripts/check_sexp_schema.py` | does this source-of-truth file conform to its schema — every construct, field, arity and value type named on refusal? | `scripts/check_sexp_schema.py <file.sexp> <schema.sexp>` (`--self-test` includes the fixpoint: schema.sexp under itself; schemas for the corpus live in `schema/` — encoding, fragment, semantics — and positional mini-languages are declared as `(operator …)` forms) |
| `scripts/compare_readers.py` | do this project's S-expression readers — `sexp.py`, LinkedSpec's Lispish, and the SExprDocumentV1 document grammar — agree on every tracked `.sexp` file? | `scripts/compare_readers.py [<file…>]` (`LISPISH_GRAMMAR=` to test a candidate grammar) |
| `scripts/check_push_cadence.sh` | may this push happen now, or is it exceptional and awaiting the director? | `scripts/check_push_cadence.sh [--status \| --gate \| --self-test]` |
| `scripts/shard_history.py` | is an append-history head nearing its ceiling, and which oldest entries would move into the next frozen shard? | `scripts/shard_history.py [--max-bytes N] [--dry-run] [--self-test]` |
| `scripts/check_changelog_shards.sh` | is the sharded changelog history still frozen, append-only, and exactly partitioned — every shard hashing to its manifest row, no entry duplicated? | `scripts/check_changelog_shards.sh [--self-test]` |
| `scripts/check_seam_integrity.sh` | have this repo's repairs to the neutral checks quietly stopped working? | `scripts/check_seam_integrity.sh` |
| `scripts/check_task_acceptance.sh --print-sig` | what does the acceptance gate actually accept as evidence right now? | `scripts/check_task_acceptance.sh --print-sig \| --print-code-re` |
| `scripts/fetch_references.sh` | is the reference model I am comparing against the one the dossier pins, and is it still configured to this profile? | `scripts/fetch_references.sh [--verify-only] [<profile>]` |
| `scripts/run_smoke.py` | does the matched-profile evidence path actually work — do two models agree with each other, with the specification, and with themselves on a re-run? | `scripts/run_smoke.py` |
| `scripts/compare_traces.py` | where do two reference models FIRST disagree, in aligned steps? | `scripts/compare_traces.py <sail-trace> <spike-log> <entry>` |
| `scripts/fetch_sources.sh` | is the specification artifact I am reading the one the locators were written against? | `scripts/fetch_sources.sh [--verify-only] <profile>` |
| any project check's `--self-test` | does this gate still discriminate — do its RED arms fail for the right reason? | `scripts/check_<name>.sh --self-test` |
| `make check` | does the workspace build, lint clean at `-D warnings`, and pass its tests? | `make check` |
| `git log -S'<token>'` | when did this string enter or leave the tree, and in which work unit? | `git log -S'<token>' --oneline` |

⛔ **A gate that has never been observed RED is not known to work.** Before trusting any check
added here, fire it against a deliberately broken input — both project checks above were fired
against the real corpus (a byte appended to `docs/GLOSSARY.md`; a byte appended to
`examples/synthetic-spec.md`) and each named the right file and the right reason before being
registered.

<!-- Add each new diagnostic as a row: what question it answers (WHY / WHERE / how-much) and
how to invoke it. The next agent should reach for the right tool without reading the source. -->
