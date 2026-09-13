# DOCTRINE_ENFORCEMENT.md — how every mechanizable doctrine is enforced

Discipline holds because it is **mechanical**, not remembered. A rule that lives only in a
doc is a suggestion; a rule wired into a git hook + CI is enforced for every agent and
every human, identically.

## Defense in depth (four layers)

- **E1 — discovery.** The doctrine docs: this file, `README.md`, `MEMORY_ARCHITECTURE.md`,
  `TOOLBOX.md`, `COMMIT.md`, and `docs/decisions/`. Where an agent learns the rules.
- **E2 — self-check.** `scripts/check_doctrines.sh` (the driver) + each registered
  `scripts/check_*.sh`. The single source of truth for "which doctrine is enforced by
  what". Runnable by hand anytime.
- **E3 — git hook.** `.githooks/pre-commit` calls the enforcer; `.githooks/commit-msg`
  checks the subject shape. Activate once per clone: `git config core.hooksPath .githooks`.
- **E4 — CI.** The same enforcer runs in CI (`.github/workflows/doctrines.yml`), so a
  locally `--no-verify`'d hook still fails the build. This is the "no matter what" backstop.

## The enforcer registry

`scripts/check_doctrines.sh` carries the **universal** registry:

| ID | Proves | Check |
| --- | --- | --- |
| `MEMORY-ARCH` | the durable 4-layer memory invariants hold | `scripts/check_memory_architecture.sh` |
| `DOCPATH` | tracked `.md` carry no checkout-specific absolute paths | `scripts/check_docpaths.sh` |
| `TASK-TREE-OWNERSHIP` | every staged code change is owned by a task-tree leaf | `scripts/check_task_tree_ownership.sh` |
| `TASK-ACCEPTANCE` | a staged **code** change is owned by a task-tree leaf whose acceptance checklist has ROOT CAUSE / ADDRESSED / NO REGRESSION **ticked**, each backed by tool output **inside that box's own bullet**. ⭐ Box-scoping is the soundness property, not a nicety: it closes two measured leakage holes — a co-staged unrelated leaf supplying the evidence, and a token matched anywhere in the file. ⚠️ Honest limit: it proves the author cited something re-runnable, never that the output is true — the un-fakeable leg is re-running the cited command in CI. Project seams in `.doctrine/` keep it neutral | `scripts/check_task_acceptance.sh` |
| `WAIVER-ROUTING` | a task leaf saying a gate **does not apply** names the leaf that owns fixing it — ⭐ *an author writing a waiver IS the gate reporting a missing capability*, the highest-signal defect report a gate can receive. Deliberately does **not** punish honesty: the waiver stays legal, it just has to name an owner | `scripts/check_waiver_routing.sh` |
| `README-STABILITY` | `README.md` stays a stable landing page — a **line cap AND a byte cap**, because a line cap alone is measurably bypassable (a real project running this spine passed its 60-line layer-A cap while carrying 138,403 bytes) | `scripts/check_readme_stability.sh` |
| `LIVE-DOC-CURRENCY` | no tracked document reports its own currency (`Last updated:` and kin) — git already carries it, and a hand-kept date is right the day it is typed and false the day after; the upstream instrument that scores distinct dates per live surface against a declared charter is a backlog item | `scripts/check_live_doc_currency.sh` |
| `LESSON-PROMOTION` | a NEW dated lesson heading staged in `DEV_NOTES.md` must be either **promoted** (a `docs/knowledge/` change, or a `docs/decisions/` record gaining `answers:`) or **explicitly declined** (`promotion: declined (<reason>)` in the owning leaf) — never silently dropped. Founding measurement upstream: 1 592 lesson entries, none reachable by question, because no gate asked. Evidence archetype: it verifies a decision was RECORDED, not that it was right | `scripts/check_lesson_promotion.sh` |
| `ROUTING-EVIDENCE` | a task leaf that routes a finding **out to another tree** carries a `ROUTING EVIDENCE` section: does the finding reproduce OUTSIDE the family it is sent to, what was measured, what would make the routing wrong. Keyed on the semantics of leaving the tree (the first cut upstream, keyed on a tree-ID spelling, missed its own founding incident); intra-tree routing is not flagged | `scripts/check_routing_evidence.sh` |
| `GAP-CLAIM-CENSUS` | a task leaf that **ADDS** a *"nothing checks X"* claim records the CENSUS it rests on in the same heading section (a command that enumerates a population, or `census: not run (<why>)`). Such a sentence is a universally quantified claim over the whole tree, false the moment one reader exists; staged-diff-scoped (81 pre-existing claims upstream would otherwise teach bypass); `--all` reports the backlog, advisory | `scripts/check_gap_claims.sh` |
| `TABLE-ARITY-RATCHET` | a staged `.md` may not RAISE the number of table rows whose cell count disagrees with their header — GFM silently DROPS extra cells and PADS missing ones, so the page looks fine and the reader loses the rightmost column (26 of 197 rows of a shipped contract upstream, every enforcer green). Per-file ratchet against HEAD; code spans and escaped pipes respected; a fresh minimal implementation with an 8-arm `--self-test` | `scripts/check_table_arity.sh` |
| `KNOWLEDGE-MAP` | the derived Knowledge Map is in sync (if the subsystem exists) | `knowledge-map/scripts/check_knowledge_map.sh` |
| `PROJECT-SPECIFIC` | this project's own doctrines | `scripts/check_doctrines.project.sh` |

### This project's own doctrines (`scripts/check_doctrines.project.sh`)

| ID | Proves | Check |
| --- | --- | --- |
| `DELIVERY-PROVENANCE` | every row of a delivered `MANIFEST.sha256` carries exactly one declared **disposition** (`frozen-in-place` / `relocated` / `live`), held as data in the package's `dispositions.tsv`, and the first two still hash to the delivered bytes. ⭐ The asymmetry is the point: an undeclared manifest row, or a disposition for a path the manifest never listed, is how a row quietly leaves coverage. ⚠️ Honest limit: it proves the delivered bytes are still the bytes, never that the delivered content was correct | `scripts/check_delivery_provenance.sh` |
| `FIXTURE-FINGERPRINT` | every tracked JSON/JSONL object carrying both `path` and `sha256` names a file that exists and still hashes to that value — `CLAIM_VERIFICATION.md` §5B: a constant that is a function of the repository is derived or gated, never carried. Excludes `docs/provenance/**` (owned above) and records naming inputs absent from this repository, so an unverifiable hash cannot masquerade as a checked one | `scripts/check_fixture_fingerprints.sh` |
| `README-ROUTING-CLOSURE` | every destination the landing page links to — **and every path-shaped destination the README guard actually emits in its failure guidance** — has a row in `doctrine/readme_routes.tsv` with a route class, a lifecycle class, an owner, and the ceilings its class requires; the ceilings are enforced and the health targets reported. ⭐ Founding measurement upstream: a README cap displaced its pressure into an unchecked neighbouring status file that reached **1,547,057 bytes**, 94.7% of it dated changelog content — the cap was green throughout. Two tiers on purpose: a health target prints, a ceiling blocks. The registry, not a script or prose, owns the landing page's own caps | `scripts/check_readme_routes.sh` |
| `PROFILE-CONSISTENCY` | a profile dossier's declared counts equal the enumeration they summarise, and every decision carries an `authority` (`architecture` / `execution-environment` / `laboratory`) and a `source`. ⭐ The authority field is the load-bearing one: a **laboratory** policy over an `UNSPECIFIED` case must never read as an **architectural** rule, because a reference model that chose differently is then recorded as a defect instead of a profile difference. ⚠️ Honest limit: it proves the file is internally consistent and cites something — checking a citation against the specification is a human reading, which is why `scripts/fetch_sources.sh` exists to make the artifact being read identifiable | `scripts/check_profile_consistency.sh` |
| `FRONTIER-SYNC` | `docs/TASK_TREE.md` still mirrors the trees under `docs/tasks/`: the frontier leaf it names equals the leaf the tree's own *Current Frontier* names first, neither names a leaf the tree records as `done`, the status cells agree, every `A/B leaves complete` or `A of B leaves done` count is re-derived, every tree has a row and every row a tree. ⭐ The asymmetry is deliberate: the **tree** is authoritative and the failure message says so, because editing a summary to match its record is safe while editing the record to match its summary destroys the evidence. Founding measurement: 1 of 14 rows had drifted — and it was the only `active` tree, i.e. the only row the documented resume path ever reads. ⚠️ Honest limit: it proves the two documents agree and that their numbers are functions of the tree, never that the frontier *ordering* is the right engineering choice | `scripts/check_frontier_sync.sh` |
| `REGISTRY-MIRROR` | `DOCTRINE_ENFORCEMENT.md` and the mdBook chapter `docs/book/src/working/doctrines.md` list exactly the doctrines the two driver arrays register — in both directions, in the right section, with every registered path existing and executable, and with any `<N> checks run today` sentence re-derived. ⭐ The asymmetry is the point: a mirror that falls behind never invents a guarantee, it quietly **withholds** one, and it does so on the surface a reviewer reads instead of the code. Founding measurement: the book listed **3** project doctrines while **5** were registered and running. ⚠️ Honest limit: it proves the two documents list the same doctrines the drivers register — never that a row's prose still describes what its check does | `scripts/check_registry_mirror.sh` |
| `TREE-CLAIMS` | every **live** document states leaf counts, the active trees and the frontier leaf exactly as `docs/tasks/` does. ⭐ Its scope is DATA, not a hardcoded list: it reads the `hot_live` rows of `doctrine/readme_routes.tsv`, so a newly registered live surface is covered the day it is registered — and `append_history` surfaces are excluded **on purpose**, because a changelog entry saying "2 of 9 leaves" was true when written and rewriting it would corrupt the record it exists to keep. `docs/TASK_TREE.md` is excluded as well: `FRONTIER-SYNC` owns it, and two gates reporting one breach twice is noise. ⚠️ Honest limit: it proves the numbers and ids are current, never that the prose around them still describes the work | `scripts/check_tree_claims.sh` |
| `DERIVED-COUNTS` | a **live** document that states a count of something this repository can enumerate — routed destinations, registered doctrines, book chapters, self-test arms — has that number RE-DERIVED from the population it summarises. Scope comes from the `hot_live` rows of the routes registry, so history is never rewritten. ⭐ Founding measurement, and it is this project's own: in ONE session two of these were committed wrong — `24 destinations governed` against a 25-row registry, and `107 self-test arms` against 112 — because both were maintained as **running totals**. A running total is a memory of a measurement, not a measurement. ⚠️ Honest limit: it checks the counts it can enumerate, and each enumerator is printed by `--list` so a reader can see what is covered and what is not | `scripts/check_derived_counts.sh` |
| `SEAM-INTEGRITY` | the repairs this project carries in the neutral checks, and the declarations in `.doctrine/`, still **do their job** — every acceptance box already committed is still accepted, no prose file is classified as a code change, every behaviour-governing family is, and the acceptance gate accepts every instrument the census gate blesses. ⭐ Founding measurement: with both seam files moved aside the full enforcer printed `all doctrines green`, `rc=0` — three fixes silently reverted and nothing said a word. It asserts **behaviour, not presence**, so it catches a deleted seam, a narrowed pattern, a scaffold overwrite, or a spine update that stops consuming the seam | `scripts/check_seam_integrity.sh` |

Each ships a `--self-test` whose RED arms assert the **reason** as well as the verdict, each
was fired RED before being registered, and each **refuses** (exit 2) rather than passing if its
own self-test stops discriminating. Two defects were caught by those arms rather than by
review: `IFS=$'\t' read` collapsing empty TSV fields and shifting every later column, and a
self-test leaking its temp root into the real run through an environment variable that prefixed
a *function* call. Both would have produced a green gate judging the wrong thing.

### The declared seams (`.doctrine/`)

| File | Consumed by | This project's declaration |
| --- | --- | --- |
| `code_paths.txt` | `TASK-ACCEPTANCE` | what counts as a **code change** here. The built-in default was measured wrong in both directions over all 125 tracked files: it matched **28** files of mdBook prose on the `src/` path segment, and missed **8** files that genuinely change behaviour — the two gate-data registries (`doctrine/readme_routes.tsv`, `docs/provenance/*/dispositions.tsv`), the `.doctrine/` seams themselves, both `.githooks/`, and `Cargo.toml`/`Cargo.lock`. Narrowing a gate can silently disable it, so all three outcomes were fired: code with no leaf → `rc=1`, gate data with no leaf → `rc=1`, prose alone → `rc=0` |
| `evidence_tokens.txt` | `TASK-ACCEPTANCE` | this project's instrument signatures, added to the universal defaults — including `git grep` and `wc -l`, which `GAP-CLAIM-CENSUS` names in its own failure hint while the acceptance gate's defaults did not recognise them |

**Project-specific doctrines go in `scripts/check_doctrines.project.sh`** (the pluggable
slot) — never in the universal driver. That is where a project adds the equivalent of its
own build gates, format checks, invariant proofs, etc.

## Adding a doctrine

1. Write `scripts/check_<name>.sh` — cheap, deterministic, self-describing; exit nonzero
   with a one-line stderr message on breach. Keep it fast (heavy proofs belong in CI).
2. Register it — universal → the `DOCTRINES` array in the driver; project → append it to
   `scripts/check_doctrines.project.sh`.
3. Mirror it in the table above (this file is the human-readable mirror of the registry).

## The task-acceptance checklist (every code-change leaf must pass)

A code change cannot commit until its owning task-tree leaf records all six:

- [ ] **REPRODUCE / ISSUE** — the problem, shown (not asserted).
- [ ] **ROOT CAUSE (WHY + WHERE)** — tool-backed and pinpointed (`TOOLBOX.md`).
- [ ] **FIX** — the change, made at the lowest-risk level that actually works.
- [ ] **ADDRESSED (verified)** — measured before→after (the global metric where one exists).
- [ ] **NO REGRESSION** — the guard set stays green; state how you proved it.
- [ ] **LOCKSTEP** — live docs (`MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md`,
  `LIVE_STATUS.md`), the book, and any trackers updated in the SAME commit.
