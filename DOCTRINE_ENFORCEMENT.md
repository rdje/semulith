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

The long-form rows (what each proves, its founding failure, its honest limit) live in four
family files under [`docs/doctrines/`](docs/doctrines/) — partitioned at `LIVE-CONTAINMENT.3`
when this file reached 32,669 of its 32,768 bytes. This index keeps every registered id, in
registration order, so REGISTRY-MIRROR judges it as a complete mirror; the family union is
judged too.

| ID | Family |
| --- | --- |
| `DELIVERY-PROVENANCE` | [governance](docs/doctrines/governance.md) |
| `FIXTURE-FINGERPRINT` | [governance](docs/doctrines/governance.md) |
| `README-ROUTING-CLOSURE` | [governance](docs/doctrines/governance.md) |
| `PROFILE-CONSISTENCY` | [definition](docs/doctrines/definition.md) |
| `FRONTIER-SYNC` | [governance](docs/doctrines/governance.md) |
| `REGISTRY-MIRROR` | [governance](docs/doctrines/governance.md) |
| `UPSTREAM-INDEX` | [governance](docs/doctrines/governance.md) |
| `TREE-CLAIMS` | [governance](docs/doctrines/governance.md) |
| `DERIVED-COUNTS` | [governance](docs/doctrines/governance.md) |
| `RECORD-SCHEMA` | [definition](docs/doctrines/definition.md) |
| `GATE-REPORT` | [evidence](docs/doctrines/evidence.md) |
| `SHARD-FREEZE` | [governance](docs/doctrines/governance.md) |
| `PORT-WEB` | [evidence](docs/doctrines/evidence.md) |
| `STATE-GEN` | [definition](docs/doctrines/definition.md) |
| `DEF-GEN` | [definition](docs/doctrines/definition.md) |
| `GUEST-GEN` | [definition](docs/doctrines/definition.md) |
| `BOARD-GEN` | [board](docs/doctrines/board.md) |
| `BOARD-VERDICT` | [board](docs/doctrines/board.md) |
| `PLATFORM-GEN` | [board](docs/doctrines/board.md) |
| `EXERCISE-COVERAGE` | [evidence](docs/doctrines/evidence.md) |
| `INTERACTION-MATRIX` | [evidence](docs/doctrines/evidence.md) |
| `MATERIALS-BILL` | [governance](docs/doctrines/governance.md) |
| `UNIT-BOOKS` | [governance](docs/doctrines/governance.md) |
| `DOSSIER-SCHEMA` | [definition](docs/doctrines/definition.md) |
| `PUSH-RECORD` | [governance](docs/doctrines/governance.md) |
| `COMMIT-PREFIX` | [governance](docs/doctrines/governance.md) |
| `SOURCE-FORMAT` | [definition](docs/doctrines/definition.md) |
| `UNIT-COMPOSITION` | [definition](docs/doctrines/definition.md) |
| `SEMANTICS` | [definition](docs/doctrines/definition.md) |
| `EXTRACTION` | [definition](docs/doctrines/definition.md) |
| `FACT-OWNERSHIP` | [governance](docs/doctrines/governance.md) |
| `SCOPE-COVERAGE` | [definition](docs/doctrines/definition.md) |
| `SEAM-INTEGRITY` | [governance](docs/doctrines/governance.md) |
| `BOOK-INDEX` | [governance](docs/doctrines/governance.md) |
| `CITATION-QUOTES` | [definition](docs/doctrines/definition.md) |

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
3. Mirror it: a universal doctrine in the registry table above; a project doctrine as its
   long-form row in the family file it belongs to under [`docs/doctrines/`](docs/doctrines/)
   AND its id in the index above (REGISTRY-MIRROR judges both; `LIVE-CONTAINMENT.3`).

## The task-acceptance checklist (every code-change leaf must pass)

A code change cannot commit until its owning task-tree leaf records all six:

- [ ] **REPRODUCE / ISSUE** — the problem, shown (not asserted).
- [ ] **ROOT CAUSE (WHY + WHERE)** — tool-backed and pinpointed (`TOOLBOX.md`).
- [ ] **FIX** — the change, made at the lowest-risk level that actually works.
- [ ] **ADDRESSED (verified)** — measured before→after (the global metric where one exists).
- [ ] **NO REGRESSION** — the guard set stays green; state how you proved it.
- [ ] **LOCKSTEP** — live docs (`MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md`,
  `LIVE_STATUS.md`), the book, and any trackers updated in the SAME commit.
