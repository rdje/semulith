# SEMULITH-PKG: ingest the v0.2 planning package into the discipline spine

## Metadata

- Tree ID: `SEMULITH-PKG`
- Status: `active`
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

## Acceptance Checklist (current leaf — `SEMULITH-PKG.2`)

Enforced by the `TASK-ACCEPTANCE` doctrine (`scripts/check_task_acceptance.sh`). Each box
carries the command that was run and the output it produced. The previous leaf's checklist is
preserved in the Verification Log below, not deleted.

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

## Task Tree

- ID: `SEMULITH-PKG`
  Status: `active`
  Goal: ingest the delivered planning package v0.2 under the spine
  Children: `SEMULITH-PKG.1`, `SEMULITH-PKG.2`, `SEMULITH-PKG.3`, `SEMULITH-PKG.4`

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
  Status: `pending`
  Goal: gate the fingerprint claims that can rot, and tighten the README caps to reviewed values.
  Acceptance: a tracked `scripts/check_delivery_provenance.sh` re-derives the `frozen-in-place` and `relocated` manifest rows and reports the `live` rows as declared drift; `examples/sources.json` fingerprints are re-derived; both go RED against a deliberately corrupted input; registered in `scripts/check_doctrines.project.sh`; reviewed README caps enforced there.
  Verification: `pending`
  Commit: `pending`

- ID: `SEMULITH-PKG.4`
  Status: `pending`
  Goal: make the mdBook the reviewable window onto the ingested package.
  Acceptance: `make book` succeeds; `SUMMARY.md` maps the package's contracts; the book states the project's actual claim scope rather than implying capability.
  Verification: `pending`
  Commit: `pending`

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `SEMULITH-PKG.3` | `pending` | this tree's fingerprint claims are re-derived by nothing, so they rot silently |
| 2 | `SEMULITH-PKG.4` | `pending` | the book is the director's review surface; it must describe what was ingested |

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

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `SEMULITH-PKG.1` | `SEMULITH-PKG-0002 (leaf SEMULITH-PKG.1): ingest planning package v0.2 under the spine` | 15 delivered files landed, 1 duplicate deleted, 3 provenance files frozen |
| `SEMULITH-PKG.2` | `SEMULITH-PKG-0003 (leaf SEMULITH-PKG.2): adopt the claim-verification standard` | standard imported verbatim under an adoption note; legs named in the leaf template |

## Changelog

- `2026-09-13`: Created task tree; `SEMULITH-PKG.1` completed — the delivered package is
  tracked, the enforcer is green, and the rot sources it arrived with are removed.
- `2026-09-13`: `SEMULITH-PKG.2` completed — the claim-verification standard is project-owned
  and the leaf template names which leg each checklist box answers.
