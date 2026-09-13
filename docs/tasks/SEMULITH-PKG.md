# SEMULITH-PKG: ingest the v0.2 planning package into the discipline spine

## Metadata

- Tree ID: `SEMULITH-PKG`
- Status: `done`
- Roadmap lane: project foundation (precedes P0)
- Created: `2026-09-13`
- Owner: repo-local workflow

## Goal

Make the delivered **Semulith planning package v0.2** a committed, spine-compliant,
gate-green part of this repository: every delivered artifact owned by a tracked path, the
landing page restored to its policy contract, duplicate ownership removed, delivery
provenance frozen where it must not drift, and live claims gated where they can rot.

## Non-Goals

- This tree does not convert `ROADMAP.md` into execution task-trees (that is `SEMULITH-TREES`).
- It does not implement any CPU, schema checker, or reference adapter (those are P0/P1).
- It does not edit the delivered design documents' technical content. The package is a
  reviewed input; editing its substance is a separate, explicitly-owned decision.

## Acceptance Criteria

- Every delivered file is tracked, or deliberately relocated/removed with its reason recorded.
- `scripts/check_doctrines.sh` is green with no waiver.
- No two tracked files claim ownership of the same content.
- Every recorded fingerprint is either frozen-by-construction or mechanically re-derived.
- Live docs (`MEMORY.md`, `LIVE_STATUS.md`, `CHANGELOG.md`, `DEV_NOTES.md`) and the mdBook
  reflect the ingested state in the same commit as the change that caused it.

## Acceptance Checklist (current leaf — `SEMULITH-PKG.5`)

Enforced by the `TASK-ACCEPTANCE` doctrine. Each box carries the command that was run and the
output it produced; the leg each box answers is in `docs/tasks/TEMPLATE.md`.

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1: the director reviews the book rather than the code,
  and the book was still the template's skeleton. Census before this leaf:
  `git ls-files docs/book | wc -l` → `3` (`book.toml`, `SUMMARY.md`, `introduction.md`), whose
  content was the scaffold's own instructions to replace them — `grep -c 'Replace this page'
  docs/book/src/introduction.md` → `1`, and `book.toml` still carried `title = "Project Book"`
  and `authors = ["<your name>"]`. So the one surface the director reads described no part of
  the project that had just been ingested.
- [x] **ADDRESSED (verified)** — the book is now a 27-chapter manual covering claim scope, live
  status, every milestone with its gate, all nine delivered contracts, the data contracts with
  a worked example, and the working discipline. `mdbook build docs/book` → `INFO HTML book
  written to …/docs/book/book`, `rc=0`. Coverage and link checks over the source:
  `book internal links unresolved: none`, `book includes unresolved: none`,
  `in SUMMARY but absent: none`, `page absent from SUMMARY: none`, `chapters: 27`.
  ⭐ The drift-proofing is the design: the status, rules and glossary chapters `{{#include}}`
  `LIVE_STATUS.md`, `RULES.md` and `docs/GLOSSARY.md`, and each contract chapter includes the
  canonical document verbatim under an orientation blockquote — verified rendered, not merely
  referenced (`G-PORTABILITY row present: True`, `orientation blockquote present: True`,
  `SCP-01` and `Canonical definition` each found once in the built HTML). The book cannot
  paraphrase a contract, so it cannot become a second owner of one.
- [x] **NO REGRESSION** — leg 2: writing the book exposed two defects that a build alone would
  not have caught, and both were fired as controls. (a) The Mermaid fence rendered as raw
  source: `grep -o 'class="language-mermaid"' docs/book/book/plan/overview.html` → present,
  i.e. the director would have read Mermaid syntax instead of a graph; replaced by an explicit
  edge table, after which `mermaid fences in book: 0`. (b) The build output contaminated the
  routing-closure measurement: `OVER CEILING docs/book/: 92 files > 60` and
  `2738590 aggregate bytes > 393216`, because `find` counted mdbook's untracked HTML —
  `git ls-files docs/book | wc -l` → `3` at the same instant. The family measurement now counts
  **tracked** files, `/docs/book/book` is gitignored, and the re-run is
  `README-ROUTING-CLOSURE: ok (24 governed destination(s))`. Self-tests after the change:
  `9 pass / 0 fail`, `7 pass / 0 fail`, `11 pass / 0 fail`. Whole gate:
  `scripts/check_doctrines.sh` → `=== all doctrines green ===`, `rc=0`; `make check` →
  `test result: ok. 1 passed; 0 failed`, `rc=0`.
- [x] **FIX** — `docs/book/` grown to 27 chapters plus `book.toml` and `SUMMARY.md`;
  `/docs/book/book` added to `.gitignore`; `family_files()` in `check_readme_routes.sh` counts
  tracked files on the real run; the three project checks' self-test fixtures moved from
  `$TMPDIR` to `$ROOT/target/doctrine-selftest`, because a project-created temporary workspace
  must stay on the repository's own volume.
- [x] **LOCKSTEP** — leg 3: `docs/book/`'s health and ceiling were **re-reviewed** rather than
  silently exceeded — 20 files / 64 KiB was written for a skeleton, and the surface's contract
  genuinely expanded, so the registry now carries 40 / 128 KiB health and 80 / 512 KiB ceiling
  with the derivation recorded in its header. `MEMORY.md`, `LIVE_STATUS.md` and `CHANGELOG.md`
  updated in this commit.

## Task Tree

- ID: `SEMULITH-PKG`
  Status: `done`
  Goal: ingest the delivered planning package v0.2 under the spine
  Children: `SEMULITH-PKG.1`, `SEMULITH-PKG.2`, `SEMULITH-PKG.3`, `SEMULITH-PKG.4`, `SEMULITH-PKG.5`

- ID: `SEMULITH-PKG.1`
  Status: `done`
  Goal: land the delivered package (deduped), restore the README landing page, freeze delivery provenance.
  Acceptance: enforcer green; no duplicate document; every delivered file tracked or relocated with a recorded reason.
  Verification: see the Verification Log.
  Commit: `SEMULITH-PKG-0002`

- ID: `SEMULITH-PKG.2`
  Status: `done`
  Goal: adopt the claim-verification standard as this project's definition of "checked".
  Acceptance: `docs/CLAIM_VERIFICATION.md` present with a fenced local-adoption note naming owner, date and authority; linked from `README.md`; an adoption decision record exists; the three legs are named in the task-tree template's checklist guidance.
  Verification: see the Verification Log.
  Commit: `SEMULITH-PKG-0003`

- ID: `SEMULITH-PKG.3`
  Status: `done`
  Goal: gate the fingerprint claims that can rot.
  Acceptance: a tracked check re-derives the `frozen-in-place` and `relocated` manifest rows and reports the `live` rows as declared drift; every pinned `sha256` is re-derived; both go RED against a deliberately corrupted input **with the right reason**; both registered in `scripts/check_doctrines.project.sh`.
  Verification: see the Verification Log.
  Commit: `SEMULITH-PKG-0004`

- ID: `SEMULITH-PKG.4`
  Status: `done`
  Goal: refresh `README_POLICY.md` to the director's current revision and set this project's reviewed caps.
  Acceptance: the policy body matches the revision the director named, under a fenced local-adoption note; line and byte caps derived from the trimmed landing page with modest headroom and enforced in the project slot; every destination the README routes to has a named owner and pressure control, or is recorded as debt with an owning leaf.
  Verification: see the Verification Log.
  Commit: `SEMULITH-PKG-0005`

- ID: `SEMULITH-PKG.5`
  Status: `done`
  Goal: make the mdBook the reviewable window onto the ingested package.
  Acceptance: `make book` succeeds; `SUMMARY.md` maps the package's contracts; the book states the project's actual claim scope rather than implying capability.
  Verification: see the Verification Log.
  Commit: `SEMULITH-PKG-0006`

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| — | — | — | **tree complete.** The next tree is `SEMULITH-TREES`: convert `ROADMAP.md` P0–P7 and the cross-cutting lanes into task-trees. Open it only with the repository clean (the pivot rule). |

Census behind row 2, over the population that would refute it — any tracked script, hook, or
enforcer entry that re-derives a recorded fingerprint:

```
$ git grep -lE 'sources\.json|MANIFEST\.sha256|sha256|shasum' -- scripts knowledge-map .githooks | wc -l
0
$ grep -ciE 'fingerprint|sha256|hash' scripts/check_doctrines.sh scripts/check_doctrines.project.sh
scripts/check_doctrines.sh:0
scripts/check_doctrines.project.sh:0
```

So the two live fingerprint claims in this tree — `examples/sources.json` pinning
`examples/synthetic-spec.md`, and the `frozen-in-place` manifest rows — are held by no check
at all. Leaf `.3` is what makes the claim false.

## Decisions

- `2026-09-13`: the delivered design documents are ingested **verbatim**. Their technical
  content is a reviewed input; changing it is a separate owned decision, not ingestion work.
- `2026-09-13`: delivery provenance is frozen and its live rows are declared — see
  [`decision_delivery-provenance-is-frozen.md`](../decisions/decision_delivery-provenance-is-frozen.md).
- `2026-09-13`: `RULES.md` stays at the repository root — it is live normative doctrine
  referenced as `RULES.md` by `README.md` and `ROADMAP.md`, not delivery provenance.
- `2026-09-13`: `docs/knowledge/` opened as the retrievable lesson layer, so
  `LESSON-PROMOTION` has a real destination rather than a declined default.
- `2026-09-13`: "checked" is defined by the three legs — see
  [`decision_claim-verification-adopted.md`](../decisions/decision_claim-verification-adopted.md).
- `2026-09-13`: the landing page's caps and routes are registry data, not script constants —
  see [`decision_readme-routing-closure.md`](../decisions/decision_readme-routing-closure.md).

## Open Questions

- Do the `PACKAGE_CHECKS.md` schema results reproduce here? `python3 -c "import jsonschema"`
  → `ModuleNotFoundError`, so they are **cited, not re-derivable in this repository**
  ([`re-derivable-vs-cited-evidence`](../knowledge/re-derivable-vs-cited-evidence.md)).
  Owner: `SEMULITH-TREES` routes this to the P1 checker lane, where rule `RUST-01` makes the
  re-derivation a Rust deliverable rather than a Python dependency. Does not block this tree.

## Blockers

- None.

## Completed-leaf evidence (archive)

The current leaf's checklist lives above; a completed leaf's checklist is moved here verbatim
so its evidence stays in layer B rather than only in git history. Only the *first* checklist
in this file is read by the `TASK-ACCEPTANCE` gate, which is why the archive sits below it.

### `SEMULITH-PKG.4` — refresh the README policy and close its routing loop

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1: the landing page's guard was not judging *this*
  project, and its routing had no closure. (a) `README-STABILITY` ran on the template's
  deliberately generous defaults — `README-STABILITY: OK — README.md is 67/300 lines,
  3719/16384 bytes` — i.e. the page could quadruple before the guard noticed, and
  `README_POLICY.md` itself says those illustrative values must be replaced after a local trim.
  (b) The policy's *Routing pressure closure* section was absent from this repository's copy:
  the local body was 74 lines / 7,669 bytes against the director's current 159-line /
  8,279-byte revision. (c) A cap with no closure only *relocates* append pressure — the
  policy's own measurement is a routed-to status file that reached `1,547,057 bytes`, 94.7%
  dated changelog content, while the README guard stayed green.
- [x] **ADDRESSED (verified)** — the neutral body is now the director's revision, imported
  unedited and verified: `body sha256:
  77a1e9348ec24d9ec5f0c97ae1ac2d634f7e7e3e150504759af3c0182d6eefec`, `matches recorded: True`.
  Caps are derived, not copied: `wc -lc README.md` → `67 3719`, ceilings set to `85 / 4864`
  (~1.3×), and the guard now judges against them — `registry caps applied: README-STABILITY:
  OK — README.md is 67/85 lines, 3719/4864 bytes.` Closure is enforced:
  `README-ROUTING-CLOSURE: ok (24 governed destination(s))`, covering every README link target
  **and** every path-shaped destination the guard actually emits. Partitioned families carry
  file-count and aggregate ceilings measured at adoption (`docs/tasks/` 5 files / 39,131 B,
  `docs/decisions/` 5 / 8,246, `docs/knowledge/` 4 / 6,834, `docs/book/` 3 / 947,
  `docs/provenance/` 5 / 10,860).
- [x] **NO REGRESSION** — leg 2: `README-ROUTING-CLOSURE --self-test: 11 pass / 0 fail`,
  8 of them RED arms (ungoverned link target, missing file destination, missing directory
  destination, unknown route_class, unknown lifecycle, absent owner, byte ceiling exceeded,
  family over aggregate bytes) each asserting the **reason**, not just the verdict. Two real
  defects were caught by those arms rather than by review: `IFS=$'\t' read` collapses empty
  TSV fields because tab is IFS *whitespace*, so `printf 'a\tb\tc\t\t0\n'` read as
  `f4='0' f5=''` — every column after an empty field shifted, and the row still parsed; and
  a self-test that passed its root as an environment variable prefixing a *function* call
  leaked that variable into the caller, so the real run resolved all 24 destinations against a
  deleted temp directory and reported `MISSING` for every one. The first defect was fixed in
  `check_delivery_provenance.sh` too — same class, not a symptom — and given its own RED arm
  (`DELIVERY-PROVENANCE --self-test: 9 pass / 0 fail`). Whole gate:
  `scripts/check_doctrines.sh` → `=== all doctrines green ===`, `rc=0`; `make check` →
  `test result: ok. 1 passed; 0 failed`, `rc=0`.
- [x] **FIX** — `README_POLICY.md` rebuilt as a fenced Semulith adoption note over the
  unedited neutral body; `doctrine/readme_routes.tsv` added as the data owner of every route
  and every cap; `scripts/check_readme_routes.sh` added and registered in the project slot.
- [x] **LOCKSTEP** — leg 3: the ceilings are enforced on every commit, so a stale target fails
  rather than rots. `DOCTRINE_ENFORCEMENT.md` mirror, `TOOLBOX.md` row,
  `docs/decisions/decision_readme-routing-closure.md` (+ index row), `MEMORY.md`,
  `LIVE_STATUS.md` and `CHANGELOG.md` updated in this commit. Two gaps are **named, not
  hidden**: the `append_history` shard tool does not exist (its ceiling is the trigger that
  opens the leaf building it), and full live-document-size containment is deliberately not
  adopted — the largest live surface is 16,228 bytes and there is no measured pressure.

### `SEMULITH-PKG.3` — gate the fingerprint claims that can rot

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1 (*re-derive*): the repository carried two
  fingerprint claims that **no command re-derived**, so each was true on the day it was
  written and unfalsifiable afterwards. Census over the population that would refute it —
  any tracked script, hook, or enforcer entry touching a recorded fingerprint:
  `git grep -lE 'sources\.json|MANIFEST\.sha256|sha256|shasum' -- scripts knowledge-map
  .githooks | wc -l` → `0`, and
  `grep -ciE 'fingerprint|sha256|hash' scripts/check_doctrines.sh scripts/check_doctrines.project.sh`
  → `scripts/check_doctrines.sh:0`, `scripts/check_doctrines.project.sh:0`. The two claims
  were `examples/sources.json` pinning `examples/synthetic-spec.md`, and the 23 `frozen-in-place`
  + `relocated` rows of the delivered manifest. This is `CLAIM_VERIFICATION.md` §5B exactly:
  a constant that is a function of the repository was *carried*, not derived or gated.
- [x] **ADDRESSED (verified)** — same census after: → `3`
  (`scripts/check_delivery_provenance.sh`, `scripts/check_fixture_fingerprints.sh`,
  `scripts/check_doctrines.project.sh`). Both checks now run on every commit and report what
  they actually re-derived:
  `DELIVERY-PROVENANCE: ok` / `docs/provenance/planning-package-v0.2: 21 frozen-in-place,
  2 relocated re-derived; 2 live row(s) declared`, and
  `FIXTURE-FINGERPRINT: ok (1 pinned fingerprint(s) re-derived)`.
  The `21 / 2 / 2` split is now **derived on every run** rather than carried in prose —
  `DELIVERY.md`'s hand-written counts were deleted for that reason.
- [x] **NO REGRESSION** — leg 2 (*falsify*): both controls were **fired RED against the real
  corpus**, not only against synthetic fixtures. Appending one byte to `docs/GLOSSARY.md` →
  `DRIFTED (frozen-in-place) docs/GLOSSARY.md`, `rc=1`, and the frozen count dropped `21` → `20`;
  appending one byte to `examples/synthetic-spec.md` → `DRIFTED examples/sources.json:1 —
  'synthetic-spec.md'` with both hashes printed, `rc=1`. Both returned to `rc=0` on restore.
  Synthetic arms assert the verdict **and** the reason:
  `DELIVERY-PROVENANCE --self-test: 8 pass / 0 fail` (5 RED arms: frozen byte changed,
  relocated byte changed, undeclared manifest row, orphan disposition, unknown disposition
  name) and `FIXTURE-FINGERPRINT --self-test: 7 pass / 0 fail` (5 RED arms: pinned file
  changed, malformed hash, well-formed wrong hash, pinned file absent, unparseable record).
  Whole gate after: `scripts/check_doctrines.sh` → `=== all doctrines green ===`, `rc=0`;
  `make check` → `test result: ok. 1 passed; 0 failed`, `rc=0`; `bash -n` parses all three
  scripts (`shellcheck: not installed` on this host — named, not hidden).
  ⭐ This leaf also had to widen `.doctrine/evidence_tokens.txt` to get its own census evidence
  past `TASK-ACCEPTANCE`, so the obvious risk is that the widening made that gate vacuous. It
  was fired RED to check: replacing this very box's content with the prose *"I looked at it
  carefully and I am confident"* → `TASK-ACCEPTANCE: … the 'ROOT CAUSE' box is ticked but
  carries no tool-output evidence`, `rc=1`; restoring → `task-acceptance: OK`, `rc=0`. The
  gate still discriminates.
- [x] **FIX** — `dispositions.tsv` added as the machine-readable owner of each manifest row's
  treatment; `scripts/check_delivery_provenance.sh` and `scripts/check_fixture_fingerprints.sh`
  added, each refusing (exit 2) rather than passing if its own self-test stops discriminating;
  both registered in `scripts/check_doctrines.project.sh`.
- [x] **LOCKSTEP** — leg 3 (*durability*): the producers are tracked, and the gate fails when
  a claim goes stale. `DOCTRINE_ENFORCEMENT.md` gained the project-doctrine registry mirror,
  `TOOLBOX.md` gained the toolbox table with the invocations, `DELIVERY.md` now points at the
  data owner instead of repeating its counts, and `MEMORY.md` / `LIVE_STATUS.md` /
  `CHANGELOG.md` are updated in this commit.

### `SEMULITH-PKG.2` — adopt the claim-verification standard

- [x] **ROOT CAUSE (WHY + WHERE)** — the repository had no definition of *checked*, and the
  gap was already producing wrong reporting. Census of the standard's presence before this
  leaf: `git ls-files | grep -ci claim_verification` → `0`. Meanwhile
  `docs/provenance/planning-package-v0.2/PACKAGE_CHECKS.md` reports schema results this
  environment cannot reproduce — `python3 -c "import jsonschema"` → `ModuleNotFoundError: No
  module named 'jsonschema'` — and nothing in the repository said whether such a result may
  be counted. `RULES.md` `EVD-01`…`EVD-10` specify what evidence must *contain*; none of them
  specifies what must be true before a measurement becomes evidence at all.
- [x] **ADDRESSED (verified)** — `docs/CLAIM_VERIFICATION.md` now exists, 321 lines / 20,715
  bytes, of which the imported body is byte-identical to its source: recomputed
  `imported body sha256: 9f99df25209c43afb74d77e348dd2d0cdb68ce96cf17a4f272ede8328f6046bd`
  against `source sha256: 9f99df25209c43afb74d77e348dd2d0cdb68ce96cf17a4f272ede8328f6046bd`,
  `byte-identical: True`. Presence census after: `git ls-files | grep -ci claim_verification`
  → `1`. The three legs are now named in `docs/tasks/TEMPLATE.md`, so every future leaf's
  checklist states which question each box answers.
- [x] **NO REGRESSION** — `scripts/check_doctrines.sh` → `=== all doctrines green ===`,
  `rc=0` (13 checks); `README-STABILITY: OK — README.md is 67/300 lines, 3719/16384 bytes`;
  `make check` → `test result: ok. 1 passed; 0 failed`, `rc=0`. Every relative link target in
  the changed files resolves (`link targets missing: none`). Leg 2 named honestly: the only
  falsification run here is the byte-identity recomputation — there is no oracle for "is this
  the right standard to adopt", and that is a judgement the director's standing policy made,
  not a measurement this leaf performed.
- [x] **FIX** — imported the standard verbatim under a fenced local-adoption note that records
  authority, date, provenance hash, non-upstream independence, the mapping from each leg to the
  machinery that already holds it here, and the one gap that is *not* yet mechanized.
- [x] **LOCKSTEP** — `README.md` links it, `docs/decisions/decision_claim-verification-adopted.md`
  records the adoption with its index row, `docs/tasks/TEMPLATE.md` names the legs,
  `MEMORY.md`, `LIVE_STATUS.md` and `CHANGELOG.md` updated in this commit.

### `SEMULITH-PKG.1` — land the delivered package, restore the landing page, freeze provenance

- [x] **ROOT CAUSE (WHY + WHERE)** — the package was dropped into the worktree outside the
  spine, so three defects coexisted, none of them visible to a reader.
  (a) `scripts/check_doctrines.sh` → `=== 1 doctrine breach(es) — commit blocked ===`,
  `rc=1`, naming `README-STABILITY: README.md no longer links README_POLICY.md`.
  (b) `diff docs/ARCHOGEN_INTEGRATION.md docs/SEMULITH_ARCHOGEN_INTEGRATION.md; echo rc=$?` →
  no output, `rc=0`: two byte-identical files, i.e. two owners for one contract document,
  against rule `OWN-01`. `grep -rn SEMULITH_ARCHOGEN_INTEGRATION .` returned nothing outside
  `.git/`, and `grep -c ARCHOGEN MANIFEST.sha256` → `1`.
  (c) `shasum -a 256 -c MANIFEST.sha256` → 25 × `OK`, `rc=0` *that day*, over a list containing
  `README.md` and `ROADMAP.md` — the two files this repository exists to change.
- [x] **ADDRESSED (verified)** — enforcer `1 doctrine breach(es)`, `rc=1` → `=== all doctrines
  green ===`, `rc=0` (13 checks). `README-STABILITY: OK — README.md is 66/300 lines,
  3581/16384 bytes.` `ls docs/ | grep -c ARCHOGEN` → `2` before, `1` after. Manifest rows
  partitioned 21 `frozen-in-place` / 2 `relocated` / 2 `live`, verified by
  `awk '{print $2}' MANIFEST.sha256 | sed 's|/.*||' | sort | uniq -c` → `10 docs, 7 examples,
  3 schemas, 1 RULES.md, 1 DESIGN_INPUTS.json, 1 PACKAGE_CHECKS.md, 1 README.md, 1 ROADMAP.md`
  = 25.
- [x] **NO REGRESSION** — `make check` → `test result: ok. 1 passed; 0 failed; 0 ignored`,
  `rc=0`. Every relative link target in the rewritten `README.md` resolved: `README link
  targets missing: none`.
- [x] **FIX** — README rewritten as a landing page linking `README_POLICY.md`; duplicate
  integration document deleted; `MANIFEST.sha256`, `DESIGN_INPUTS.json`, `PACKAGE_CHECKS.md`
  relocated verbatim to `docs/provenance/planning-package-v0.2/` with a `DELIVERY.md`.
- [x] **LOCKSTEP** — `MEMORY.md`, `LIVE_STATUS.md`, `CHANGELOG.md`, `DEV_NOTES.md`,
  `docs/TASK_TREE.md`, two decision records and `knowledge-map/subsystems.md` in the same commit.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-13` | `SEMULITH-PKG.1` | `scripts/check_doctrines.sh` (13 checks) | `all doctrines green`, `rc=0` |
| `2026-09-13` | `SEMULITH-PKG.1` | `make check` (fmt + clippy -D warnings + test) | `test result: ok. 1 passed`, `rc=0` |
| `2026-09-13` | `SEMULITH-PKG.1` | README link-target resolution over `README.md` | `missing: none` |
| `2026-09-13` | `SEMULITH-PKG.1` | `README-STABILITY` with template caps | `66/300 lines, 3581/16384 bytes` |
| `2026-09-13` | `SEMULITH-PKG.2` | imported-body SHA-256 vs source | `byte-identical: True` (`9f99df25…6046bd`) |
| `2026-09-13` | `SEMULITH-PKG.2` | `scripts/check_doctrines.sh` (13 checks) | `all doctrines green`, `rc=0` |
| `2026-09-13` | `SEMULITH-PKG.2` | `make check` | `test result: ok. 1 passed`, `rc=0` |
| `2026-09-13` | `SEMULITH-PKG.3` | `check_delivery_provenance.sh --self-test` | `8 pass / 0 fail` (5 RED arms) |
| `2026-09-13` | `SEMULITH-PKG.3` | `check_fixture_fingerprints.sh --self-test` | `7 pass / 0 fail` (5 RED arms) |
| `2026-09-13` | `SEMULITH-PKG.3` | both controls fired RED on the real corpus | each named the right file and reason; `rc=1`, restored `rc=0` |
| `2026-09-13` | `SEMULITH-PKG.3` | `scripts/check_doctrines.sh` (13 checks) | `all doctrines green`, `rc=0` |
| `2026-09-13` | `SEMULITH-PKG.4` | imported policy body SHA-256 vs source | `matches recorded: True` |
| `2026-09-13` | `SEMULITH-PKG.4` | `check_readme_routes.sh --self-test` | `11 pass / 0 fail` (8 RED arms) |
| `2026-09-13` | `SEMULITH-PKG.4` | `check_delivery_provenance.sh --self-test` after the TSV fix | `9 pass / 0 fail` |
| `2026-09-13` | `SEMULITH-PKG.4` | `scripts/check_readme_routes.sh` | `ok (24 governed destination(s))`, caps `67/85` lines, `3719/4864` bytes |
| `2026-09-13` | `SEMULITH-PKG.5` | `mdbook build docs/book` | `HTML book written`, `rc=0` |
| `2026-09-13` | `SEMULITH-PKG.5` | book link / include / SUMMARY coverage | `none` unresolved in all four directions; `chapters: 27` |
| `2026-09-13` | `SEMULITH-PKG.5` | three project checks' self-tests after the tracked-file fix | `9 / 7 / 11 pass, 0 fail` |
| `2026-09-13` | `SEMULITH-PKG.5` | `scripts/check_doctrines.sh` (13 checks) + `make check` | `all doctrines green`, `rc=0`; `test result: ok. 1 passed` |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `SEMULITH-PKG.1` | `SEMULITH-PKG-0002 (leaf SEMULITH-PKG.1): ingest planning package v0.2 under the spine` | 15 delivered files landed, 1 duplicate deleted, 3 provenance files frozen |
| `SEMULITH-PKG.2` | `SEMULITH-PKG-0003 (leaf SEMULITH-PKG.2): adopt the claim-verification standard` | standard imported verbatim under an adoption note; legs named in the leaf template |
| `SEMULITH-PKG.3` | `SEMULITH-PKG-0004 (leaf SEMULITH-PKG.3): gate the fingerprint claims that can rot` | two project doctrines, 15 self-test arms, both fired RED on the real corpus |
| `SEMULITH-PKG.4` | `SEMULITH-PKG-0005 (leaf SEMULITH-PKG.4): close the README routing loop with reviewed caps` | policy refreshed; 24 destinations governed; 2 defects caught by the new check's own RED arms |
| `SEMULITH-PKG.5` | `SEMULITH-PKG-0006 (leaf SEMULITH-PKG.5): grow the book into the review surface` | 3 chapters to 27; contracts included verbatim, never paraphrased |

## Changelog

- `2026-09-13`: Created task tree; `SEMULITH-PKG.1` completed — the delivered package is
  tracked, the enforcer is green, and the rot sources it arrived with are removed.
- `2026-09-13`: `SEMULITH-PKG.2` completed — the claim-verification standard is project-owned
  and the leaf template names which leg each checklist box answers.
- `2026-09-13`: `SEMULITH-PKG.3` completed — `DELIVERY-PROVENANCE` and `FIXTURE-FINGERPRINT`
  are registered project doctrines; the counts they report are derived, not carried. Leaf `.4`
  split out of `.3` so the README policy refresh is owned explicitly rather than bundled.
- `2026-09-13`: `SEMULITH-PKG.4` completed — the README policy is refreshed to the director's
  current revision, this project's caps are derived from its own trimmed page, and all 24
  routed destinations are governed. Two gaps named rather than hidden: the append-history
  shard tool, and the deferred live-document-size containment adoption.
- `2026-09-13`: `SEMULITH-PKG.5` completed and **the tree is done**. The book is the review
  surface, 27 chapters, with every contract included verbatim rather than paraphrased.
