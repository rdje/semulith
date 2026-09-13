# CHANGELOG.md

## `SEMULITH-TREES.2` — the CPU lane, where both processor gates live

- Four trees created and registered: **`P2-SCALAR`** (9 leaves, gate `CPU-LAB`),
  **`DSP-REVIEW`** (7 leaves, a precondition of `BREADTH` rather than a gate of its own),
  **`P3-BREADTH`** (6 leaves, gate `BREADTH`), **`P4-SYSTEM`** (10 leaves, gate `CPU-SYSTEM`).
  Milestone-tree census: `2` → `6`.
- Each tree's acceptance criteria **are** its gate, quoted from `docs/EVIDENCE_AND_GATES.md` §7
  rather than restated — a restated gate is a second owner.
- Several leaves exist specifically to stop a claim from drifting: `P2-SCALAR.5` records ACT4
  results as external tests with Sail-derived expected values rather than a second semantics;
  `P2-SCALAR.8` keeps both native hosts mandatory and reads `incomplete` when the
  infrastructure is missing; `P3-BREADTH.3` demands the evidence path *before* a real DSP
  subset is implemented; `P4-SYSTEM.7` blocks floating point until a named Rust backend passes
  qualification, with no native-float fallback.


## `SEMULITH-TREES.1` — the near-term lane is task-trees, not prose

- The roadmap existed only as prose: milestone trees before this leaf, `0`; milestone sections
  in `ROADMAP.md`, `8`, plus three cross-cutting lanes. A lane with no tree has no frontier, no
  acceptance record and no owner — exactly what the task-tree doctrine exists to prevent.
- **`P0-PROFILE`** (9 leaves, gate `G0`): the `rv64i-lab-v0` dossier, state inventory,
  requirements seed, environment contract, reference dossier, the matched-profile smoke test
  that a reference is not usable without, the independence inventory, three guest programs, and
  the evidence-obligation policy declared *before* implementation.
- **`P1-LAB`** (12 leaves, gate `G1`): the three crates, arithmetic primitives, state, the
  environment boundary, the four typed outcome families, the canonical definition skeleton, the
  graph checker, the first execution slice, the validator mutation suite, replay and reduction,
  the performance baseline, and the gate report.
- Every leaf cites the `ROADMAP.md` section or `docs/IMPLEMENTATION_GUIDE.md` task card it
  derives from, so a reader can refute it by reading one paragraph rather than trusting it.


Completed work and its validation, newest first. Entries above the `bedrock-scaffold` rule
are this project's; entries below it are the discipline spine this repository was created
from, retained because the spine is still live code here.

## `SEMULITH-PKG.7` — the narrowing had dropped two files nobody measured

- `.6` wrote `^scripts/.*\.sh$`, anchoring a rule whose real subject is *any shell script*. It
  silently removed `docs/tasks/artifacts/*/run_*_probes.sh` — both executable, both emitting the
  `probes: N pass / N fail` line that `.doctrine/evidence_tokens.txt` declares as an accepted
  evidence signature — from the gate's view.
- ⛔ **`.6`'s census excluded prose from its difference set**, so it could not see them. A census
  answers the question it is given; asking it in both directions is what makes it a control.
- `\.sh$` is now unanchored, with the reason recorded beside it. Re-measured over 126 tracked
  files: the declared set is exactly the built-in default **plus 12** behaviour-governing files
  it could not see, **minus 28**, all of them mdBook prose. Nothing else is dropped.

## `SEMULITH-PKG.6` — what counts as a code change here is declared, not inherited

- `TASK-ACCEPTANCE`'s built-in code-path default is wrong for this repository in **both**
  directions, measured over all 125 tracked files: it matched **28** files of mdBook prose on
  the `src/` path segment, and missed **8** files that genuinely change behaviour — both
  gate-data registries, the `.doctrine/` seams, both git hooks, and `Cargo.toml`/`Cargo.lock`.
  A registry holds the ceilings and dispositions the checks enforce: editing one changes a
  verdict without touching a script.
- `.doctrine/code_paths.txt` declares the allow-list, with the measurement that motivates each
  group written into the file. Matched: `35 of 125`; prose: `0`.
- ⛔ **Narrowing a gate can silently disable it**, so all three outcomes were fired and
  observed rather than reasoned about: code with no owning leaf → `rc=1`; gate data with no
  owning leaf → `rc=1` (invisible to the default); prose alone → `rc=0` (wrongly refused
  before). The working tree was restored after each.
- Recorded in `DOCTRINE_ENFORCEMENT.md` and in the book's doctrine chapter, together with the
  sibling seam: `evidence_tokens.txt` exists because `GAP-CLAIM-CENSUS` recommends `git grep …
  | wc -l` while the acceptance gate's default signatures did not recognise it.

## `SEMULITH-PKG.5` — the book becomes the review surface

- Grew `docs/book/` from the template's 3-file skeleton to a **27-chapter manual**: claim scope,
  live status, every milestone with its gate and its dependency edges, all nine delivered
  contracts, the data contracts with a worked example, and the working discipline.
- **Drift-proof by construction.** The status, rules and glossary chapters `{{#include}}` the
  live files; each contract chapter includes the canonical document verbatim under an
  orientation blockquote. The book never paraphrases a contract, because a paraphrase is a
  second owner and `OWN-01` says there is one.
- Verified rendered rather than referenced: `mdbook build` `rc=0`; `book internal links
  unresolved: none`, `book includes unresolved: none`, SUMMARY coverage complete in both
  directions, and included content spot-checked in the built HTML.
- ⛔ **Two defects a passing build would not have caught.** The Mermaid fence rendered as raw
  source in mdBook — the director would have read Mermaid syntax instead of a graph — and is
  replaced by an explicit edge table that renders everywhere. And the build output contaminated
  the routing-closure measurement (`92 files / 2,738,590 bytes` by `find`, against `3` tracked
  at the same instant), so family measurement now counts tracked files and `/docs/book/book` is
  gitignored.
- `docs/book/`'s health and ceiling were **re-reviewed, not silently exceeded**: 20 files /
  64 KiB was written for a skeleton, the surface's contract genuinely expanded, and the registry
  now carries 40 / 128 KiB health and 80 / 512 KiB ceiling with the derivation recorded.
- The three project checks' self-test fixtures moved from `$TMPDIR` to
  `target/doctrine-selftest`: a project-created temporary workspace must stay on the
  repository's own volume.

## `SEMULITH-PKG.4` — the README cap now judges this project, and its routes are closed

- Refreshed `README_POLICY.md` to the director's current revision: neutral body imported
  unedited (`sha256 77a1e934…6eefec`, 159 lines / 8,279 bytes) under a fenced Semulith adoption
  note. The previous local copy predated the *Routing pressure closure* section entirely.
- **Caps derived, not copied.** `README.md` measures 67 lines / 3,719 bytes after its trim;
  ceilings are 85 lines / 4,864 bytes. The guard had been running the template's deliberately
  generous `300 / 16384`, i.e. the page could have quadrupled unnoticed.
- Added **`README-ROUTING-CLOSURE`**: 24 destinations governed — every README link target and
  every path-shaped destination the guard *actually emits* in its failure guidance — each with
  a route class, a lifecycle class, an owner, and the ceilings its class requires. Partitioned
  families carry file-count and aggregate bounds, because splitting a monolith without bounding
  the collection moves the same append pressure one level down.
- The registry (`doctrine/readme_routes.tsv`) owns the numbers; the checker re-runs the neutral
  README guard *with* them, so there is no second place a cap can be written.
- ⛔ **Two defects caught by the new check's own RED arms, not by review.** `IFS=$'\t' read`
  collapses empty TSV fields — tab is IFS whitespace — so every column after an empty field
  shifted while the row still parsed; and a self-test passed its root through an environment
  variable prefixing a *function* call, which bash keeps in the caller, so the real run
  resolved all 24 destinations against a deleted temp directory. The first was fixed in
  `check_delivery_provenance.sh` too, as the same class rather than a symptom.
- Named gaps, not hidden ones: the append-history shard tool does not exist (its ceiling is the
  trigger that opens the leaf building it), and full live-document-size containment is
  deliberately deferred — the largest live surface is 16,228 bytes.

## `SEMULITH-PKG.3` — the fingerprint claims are gated instead of carried

- Two claims in this repository were re-derived by **nothing**, measured:
  `git grep -lE 'sources\.json|MANIFEST\.sha256|sha256|shasum' -- scripts knowledge-map .githooks | wc -l`
  → `0` before, `3` after. They were `examples/sources.json`'s pin on `synthetic-spec.md`, and
  the 23 frozen + relocated rows of the delivered manifest.
- Added **`DELIVERY-PROVENANCE`**: every manifest row carries exactly one disposition, declared
  as data in `dispositions.tsv`; `frozen-in-place` and `relocated` rows are re-hashed, `live`
  rows are existence-checked. An undeclared row or an orphan disposition is a breach — that
  asymmetry is how a row quietly leaves coverage.
- Added **`FIXTURE-FINGERPRINT`**: any tracked JSON/JSONL object carrying both `path` and
  `sha256` must name a file that exists and still hashes to that value. Deliberately excludes
  records naming inputs absent from this repository, so an unverifiable hash cannot masquerade
  as a checked one.
- **Both controls were fired RED against the real corpus**, not only synthetic fixtures: one
  byte appended to `docs/GLOSSARY.md` and to `examples/synthetic-spec.md` each produced the
  right file, the right reason, and `rc=1`; both restored to `rc=0`. Self-tests assert the
  reason as well as the verdict — `8 pass / 0 fail` and `7 pass / 0 fail`, 10 RED arms between
  them. Each check refuses (exit 2) rather than passing if its self-test stops discriminating.
- `DELIVERY.md`'s hand-written `21 / 2 / 2` counts were deleted: the checker derives them on
  every run. One derived source beats N synchronized copies.
- `DOCTRINE_ENFORCEMENT.md` gained the project-doctrine registry mirror; `TOOLBOX.md` gained
  the toolbox table with each tool's question and invocation.

## `SEMULITH-PKG.2` — the claim-verification standard is project-owned

- Imported `docs/CLAIM_VERIFICATION.md` verbatim (body SHA-256 `9f99df25…6046bd`, verified
  byte-identical after import) under a fenced local-adoption note recording authority, date,
  provenance, and that the originating project is **not** an upstream.
- "Checked" now means three dimensionally different questions — **re-derive**, **falsify**,
  **durability** — and a missing leg is *named in the claim* rather than omitted.
- `docs/tasks/TEMPLATE.md` now states which leg each checklist box answers, so the mapping is
  in front of every future author instead of in a standard they might not open.
- Adoption recorded as `docs/decisions/decision_claim-verification-adopted.md`, including the
  one gap that is **not** yet mechanized (§5A claim tags, §7 constant sweep) and who owns it.
- Validation: `scripts/check_doctrines.sh` → `all doctrines green` (13 checks); `make check` → ok.

## `SEMULITH-PKG.1` — planning package v0.2 ingested under the spine

- Landed the delivered package: `RULES.md`, ten design documents under `docs/`, three JSON
  Schema starters, and seven synthetic fixtures — verbatim. Their technical content is a
  reviewed input and was not edited.
- **Removed a duplicate owner.** `docs/SEMULITH_ARCHOGEN_INTEGRATION.md` was byte-identical to
  `docs/ARCHOGEN_INTEGRATION.md`, absent from the delivery manifest and referenced by nothing.
  Two files owning one contract is rule `OWN-01`'s failure in its cheapest form.
- **Restored the landing page.** The delivered `README.md` had replaced it, dropping the link
  that makes its size caps traceable; `scripts/check_doctrines.sh` was red on
  `README-STABILITY` until this commit.
- **Froze the delivery provenance.** `MANIFEST.sha256`, `DESIGN_INPUTS.json` and
  `PACKAGE_CHECKS.md` moved verbatim to `docs/provenance/planning-package-v0.2/` with a
  `DELIVERY.md` that gives each of the 25 manifest rows one of three dispositions — 21
  `frozen-in-place`, 2 `relocated`, 2 `live`. A root-level manifest listing `README.md` and
  `ROADMAP.md` was a check whose failure was already scheduled.
- Opened `docs/knowledge/` as the retrievable layer, with the two cards this slice earned.
- Validation: `scripts/check_doctrines.sh` → `=== all doctrines green ===` (13 checks);
  `make check` → `test result: ok. 1 passed`.

---


## bedrock-scaffold 0.6.1 — creating a project is foolproof through its first commit

`BEDROCK-MAINTENANCE.2.7`.

- ⛔ **Measured on a fresh clone of 0.6.0:** `bootstrap.sh` left the crate rename — a CODE change — with no owning
  leaf, so the new project's FIRST commit was refused by `TASK-TREE-OWNERSHIP` and `TASK-ACCEPTANCE`. A new user's
  first contact with the discipline was a refusal about a rename the tool made.
- **`bootstrap.sh` now seeds `docs/tasks/BOOTSTRAP.md`** on a fresh de-template: a done leaf that owns the bootstrap,
  its ticked checklist carrying the evidence of that very run (crate-name count before/after, hooks path, the
  enforcer's summary and verdict with `rc=0`), registered in `docs/TASK_TREE.md`, pointed to by `MEMORY.md`; and it
  prints the exact first-commit command as step 0. Idempotent.
- Proven: clone → `bootstrap.sh <name>` → the printed commit → hooks green → `make gate` green → `make check` green,
  with no hand edits. Two defects in the fix were caught by the trial itself (an enforcer run before the map
  existed; a `grep -c` fallback that split a checklist bullet).

## bedrock-scaffold 0.6.0 — four evidence and ratchet doctrines: lessons reach the retrievable layer, routings carry evidence, gap claims carry their census, tables keep their columns

`BEDROCK-MAINTENANCE.2.6`.

- **Added `LESSON-PROMOTION`**: a new dated lesson heading staged in `DEV_NOTES.md` must be promoted (a
  `docs/knowledge/` change or a `docs/decisions/` record gaining `answers:`) or explicitly declined
  (`promotion: declined (<reason>)` in the owning leaf). Pure verdict with 9 controls at import.
- **Added `ROUTING-EVIDENCE`**: a leaf that routes a finding out to another tree carries a `ROUTING EVIDENCE`
  section. Keyed on the semantics of leaving the tree; 5-arm `--self-test`.
- **Added `GAP-CLAIM-CENSUS`**: a leaf that ADDS a "nothing checks X" claim records the census it rests on in
  the same section (or `census: not run (<why>)`). Staged-diff-scoped; `--all` reports the backlog; 10-arm
  `--self-test` pinning the founding active and passive sentences.
- **Added `TABLE-ARITY-RATCHET`** (a fresh minimal implementation): a staged `.md` may not raise the number of
  table rows whose cell count disagrees with their header; code spans and escaped pipes respected; 8-arm
  `--self-test`.
- ⛔ Two defects in the ports were caught by their own RED arms before the gate ran: a heredoc that consumed
  the table detector's stdin (every arm read 0), and a `pipefail` control in lesson promotion.
- All four scripts join the `NEUTRAL` allow-list of `scripts/update_scaffold.sh`. Backlog notes record the
  input-bound principles (`BASELINE-IDENTITY`, `IDENTITY-CARRIER-CURRENCY`, `SCRATCH-SLOT-HEADER`, the full
  `LIVE-DOC-CURRENCY` instrument) for a future seam.

## bedrock-scaffold 0.5.0 — the day-one batch: no agent trailers, a handoff census, no self-reported dates

`BEDROCK-MAINTENANCE.2.5`.

- ⛔ **`COMMIT.md` had the trailer rule backwards.** It told every generated project to *end commit
  messages with the project's co-authorship trailer*; the upstream maintainer ruled the opposite on
  2026-08-22 (a commit message ends with its own last line — no agent/tool attribution trailers,
  harness-agnostic). The rule is rewritten and `.githooks/commit-msg` now refuses the known
  agent-attribution shapes mechanically; a human co-author's `Co-Authored-By:` still passes.
- **Added `scripts/check_no_background_jobs.sh`**, the handoff census: pattern-free (`lsof` over the
  caller's uid — an open handle under the repo, or a command line naming the checkout), run before
  a session ends; deliberately not a commit gate. Named in `CLAUDE.md`'s non-negotiables.
- **Added the `LIVE-DOC-CURRENCY` doctrine** (principle): no tracked `.md` reports its own currency
  (`Last updated:` and kin) — git carries it, a hand-kept date is false the day after. The field is
  deleted from `docs/tasks/TEMPLATE.md` and the maintenance tree; `scripts/check_live_doc_currency.sh`
  is structural over `git ls-files '*.md'` with a 3-arm `--self-test`.
- Both scripts join the `NEUTRAL` allow-list of `scripts/update_scaffold.sh`.
- Part 2 of the same transfer (`LESSON-PROMOTION`, `ROUTING-EVIDENCE`, `GAP-CLAIM-CENSUS`, a fresh
  `TABLE-ARITY-RATCHET`) is classified in the `.2.5` leaf and queued as `.2.6`, paused by the maintainer.

## bedrock-scaffold 0.4.0 — TASK-ACCEPTANCE: a change lands with evidence, not with a claim

`BEDROCK-MAINTENANCE.2.4`.

- **Added the `TASK-ACCEPTANCE` doctrine**: a staged CODE change must be owned by a task-tree leaf
  whose checklist has ROOT CAUSE / ADDRESSED / NO REGRESSION **ticked**, each backed by output from
  a tool that was actually run — **inside that box's own bullet**.
- ⭐⭐ **Box-scoping is the soundness property**, not a nicety. It closes two measured leakage
  holes: a co-staged, unrelated leaf supplying the evidence, and a token matched anywhere in the
  file rather than in the box it backs. `CTRL-1` demonstrates it directly — a whole-file grep
  PASSES the fixture that the shipped check REJECTS.
- **Neutral by seam, not by rename.** Default signatures are universal to any Rust project
  (`error[E1234]`, `could not compile`, `clippy::…`, `test result: ok`, panics, profilers) plus any
  project's build-flow forensics (`git log -S`, `shellcheck`, `bash -n`, `make -n`, `ENOSPC`…).
  Project-specific tooling is declared in `.doctrine/evidence_tokens.txt`, and what counts as a
  code change in `.doctrine/code_paths.txt` — both optional, both defaulted, both documented in
  `.doctrine/README.md`. ⭐ `CTRL-4`/`CTRL-4b` prove the seam is load-bearing: the same leaf passes
  WITH the declaration and fails WITHOUT it.
- ⛔ **Fixed a portability defect the probes caught**: the box extractor used `IGNORECASE`, a gawk
  extension that BSD awk silently ignores — every leaf would have been reported as having no
  checklist. Rewritten with POSIX `tolower()`.
- ⚠️ Honest limit, stated in the check itself: it proves the author cited something re-runnable,
  never that the output is true. The un-fakeable leg is re-running the cited command in CI.
- Probes 9/0; `make gate` 8/8.

## unreleased — the admission test asks about VALUE first, not vocabulary

`BEDROCK-MAINTENANCE.2.3`. Process only; no check changed, so `DOCTRINE_VERSION` is unmoved
(`MAINTAINING.md` and the maintenance tree are maintainer-only, not re-syncable spine files).

- **The admission test is now two ordered questions.** Q1 (primary, about VALUE): *does this
  objectively benefit any present and any future project?* — answered by stating what the check
  prevents using no project's nouns, then asking whether a brand-new project is better off with it
  on day one. Q2 (secondary, a filter): *can it be expressed without domain nouns?*
- ⛔ **Q2 cannot substitute for Q1.** A check can score 0 domain nouns and still encode a workflow
  only one project needs — neutral vocabulary, project-shaped substance. Q2 measures whether a
  thing CAN be neutralized; Q1 asks whether it SHOULD be. Running Q2 first waves impostors through.
- ⭐ **Measured worked example, which changed a verdict.** A "destructive automation must require
  confirmation" check scored well on Q2 and was ranked an easy win; its logic hardcodes a Makefile
  path and a `clean:` recipe, so it really offers *"benefits any project that builds with make"* —
  a conditional. **Rejected as-is.** Meanwhile `ROUTING-EVIDENCE` measures 0 build-system
  references and presumes only the task-tree system this template ships ⇒ promoted to top.
- **The portability seam to look for:** does the check presume anything beyond what bedrock ships?
  If yes, give it a project-declared seam or leave it upstream — never hardcode one project's
  answer and call it neutral.
- ✅ Retroactive audit: all four already-ported items PASS Q1. Nothing retracted.

## bedrock-scaffold 0.3.0 — WAIVER-ROUTING, and the neutrality bar for every future port

`BEDROCK-MAINTENANCE.2.2`.

- **Added the `WAIVER-ROUTING` doctrine** (`scripts/check_waiver_routing.sh`): a task leaf saying a
  gate DOES NOT APPLY must name the leaf that owns fixing the gate. ⭐ An author writing a waiver
  IS the gate reporting a missing capability — the highest-signal defect report a gate can get.
  Deliberately does **not** punish honesty: the waiver stays legal, it just has to name an owner.
- **Chosen by measurement.** All 15 upstream doctrines were classified by domain-dependence of
  their LOGIC (comments stripped). `WAIVER-ROUTING` scored **0** — portable essentially unchanged.
  The ranked remainder is now a frontier in `docs/tasks/BEDROCK-MAINTENANCE.md`, not a wish list.
- ⭐⭐ **The port FIXED a defect rather than inheriting one**: the origin's `printf … | grep -q …
  || continue` returns failure ON SUCCESS past the pipe buffer under `pipefail`, silently SKIPPING
  the file — a **fail-open**. Both sites here read a file instead. Threshold measured, not assumed:
  65,606 B → no SIGPIPE; 131,139 B → SIGPIPE.
- **Wrote down the neutrality bar** (`MAINTAINING.md`): every doctrine here must be objectively
  applicable to ANY project, with a measurable admission test and its honest bound — plus the rule
  that **transfer runs both ways**, after this repo's layer-C check turned out to be stronger than
  the reference deployment's.
- Probes 5/0; `make gate` 7/7; added to the `update_scaffold.sh` NEUTRAL allow-list.

## bedrock-scaffold 0.2.0 — README Stability Policy + a layer-A byte cap

`BEDROCK-MAINTENANCE.2.1`. Transferred from the reference deployment by maintainer order.

- **Added `README_POLICY.md`** (project-neutral, verbatim) — keeps `README.md` a stable landing
  page instead of a changelog/roadmap/catalogue, and states the caps rule.
- **Added the `README-STABILITY` doctrine** (`scripts/check_readme_stability.sh`): a line cap
  AND a byte cap, a dated-line (release-history) tripwire, and a required link back to the
  policy. Non-mutating; REFUSES (exit 2) rather than passing when the README or policy is
  absent. Template defaults 300 lines / 16384 bytes — generous on purpose, because they ship to
  a project whose README is not this one; tighten after your own trim.
- ⛔ **Closed a bypass the spine was itself shipping.** `scripts/check_memory_architecture.sh`
  capped layer-A `MEMORY.md` by LINES only (cap 120, no byte bound), exactly as
  `MEMORY_ARCHITECTURE.md` §9's reference check prescribed — so **every adopting project
  inherited a bound that does not bind.** Measured on a real project running this spine:
  60 lines (passing, exactly at its cap) carrying **138,403 bytes** — 2,306 B/line, one line of
  18,816 B. Now both caps, in the check **and** in the standard (§6 / §9 / §9.1).
  Layer-A caps: **50 lines** (tightened from 120, to match the "≤ ~50 lines" §6 already stated)
  and **7168 bytes**. Both env-overridable.
- Both new files added to the `update_scaffold.sh` NEUTRAL allow-list, so existing projects
  pull them with `scripts/update_scaffold.sh <bedrock-url>`.
- Verified: `make gate` 6/6 green; a 13-line / 19,304-byte fixture is REJECTED by the byte cap
  while being well under the line cap; the **retired** layer-A guard PASSES that same file
  (exit 0) — the change is proven necessary by execution, not by argument.

Changelog-style summary of completed work + its validation (internal continuity surface;
the immutable audit trail proper is `git log` — memory layer D). Newest first.

## _(YYYY-MM-DD)_ — bootstrap

Instantiated from the `bedrock` discipline-spine template. Next: replace `ROADMAP.md` and
seed the first task-tree.
