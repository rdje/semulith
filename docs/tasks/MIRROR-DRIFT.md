# MIRROR-DRIFT: every hand-kept mirror of a machine-readable source is gated

## Metadata

- Tree ID: `MIRROR-DRIFT`
- Status: `done` (reopened once, for `.4` — a mirror class the first three leaves did not cover)
- Roadmap lane: project foundation (cross-cutting; serves every lane)
- Gate: none — this tree adds gates rather than passing one
- Depends on: nothing
- Unlocks: nothing; it protects the resume path every other tree is resumed through
- Created: `2026-09-14`
- Owner: repo-local workflow

## Goal

Find every tracked document that **restates** a fact some other tracked file already owns in
machine-readable form, and make the restatement either **derived** or **gated**. A mirror kept
by a conditional manual step is not a mirror; it is a copy with a half-life.

## Non-Goals

- Not a campaign to delete prose. A human-readable mirror is often the right artifact — the
  requirement is that its *facts* be checked against their owner, not that it stop existing.
- Not a generator. Deriving a table is one legitimate fix; gating a hand-written one is another,
  and for a document whose wording carries argument the second is usually better.
- No new content is authored here. A leaf that discovers a mirror is wrong fixes the mirror; if
  the *source* is wrong that is a finding routed to the tree that owns it.

## Acceptance Criteria

1. Each leaf names a specific mirror, the source that owns its facts, and the drift it measured
   (or the census showing there is none).
2. Each fix is a gate with a `--self-test` whose RED arms assert the **reason**, fired RED
   against the **real** corpus before being trusted — never only against fixtures.
3. No gate is registered that has not been observed failing on the actual repository or on a
   deliberately broken copy of it.

## Task Tree

- ID: `MIRROR-DRIFT.1` — **the task-tree index mirrors the trees**
  Status: `done`
  Goal: `docs/TASK_TREE.md` restates each tree's status, frontier leaf and leaf counts.
  `COMMIT.md` updates it "only if the frontier changes" — a conditional manual step. Gate the
  agreement and repair the drift that already exists.
  Acceptance: the index's status cell, frontier leaf and any leaf count are checked against the
  owning tree; the gate fires RED on the real index before the repair and green after.
  Verification: see the Verification Log.
  Commit: `SEMULITH-MIR-0017`

- ID: `MIRROR-DRIFT.2` — **the doctrine documents mirror the enforcer registry**
  Status: `done`
  Goal: `DOCTRINE_ENFORCEMENT.md` and `docs/book/src/working/doctrines.md` both restate the
  doctrine registry held in the two driver scripts. Measured today: the book chapter is missing
  `PROFILE-CONSISTENCY` and `SEAM-INTEGRITY` — the two most recently registered — so the surface
  the director reviews shows 3 project doctrines where 5 run.
  Acceptance: every registered id appears in both mirrors and every id in a mirror is registered;
  the count sentence ("Thirteen checks run today") is derived or gated; fired RED on the real
  tree before the repair.
  Verification: see the Verification Log.
  Commit: `SEMULITH-MIR-0018`

- ID: `MIRROR-DRIFT.3` — **the live docs' derived numbers**
  Status: `done`
  Goal: `MEMORY.md` names an active tree and a frontier leaf; `LIVE_STATUS.md` states a leaf
  count per milestone tree. Census run at `.1`: all 11 leaf counts and both `MEMORY.md`
  assertions agree today, so this leaf is prevention, not repair — and the leaf must say so
  rather than manufacture a defect.
  Acceptance: `MEMORY.md`'s active tree and frontier leaf, and every `N leaves` / `A of B leaves`
  claim in `LIVE_STATUS.md`, are checked against the trees; the gate fires RED on a deliberately
  edited copy.
  Verification: see the Verification Log.
  Commit: `SEMULITH-MIR-0019`

- ID: `MIRROR-DRIFT.4` — **derived counts in live documents**
  Status: `done`
  Goal: `.1`–`.3` gated what live documents say about *task-trees*. They do not cover what a live
  document says about any other enumerable population — registry rows, registered doctrines, book
  chapters, self-test arms. Measured in one session: `LIVE_STATUS.md` said `24 destinations
  governed` against a 25-row registry (stale since `SEMULITH-P0-0013`), and `107 self-test arms`
  against an actual 112. **Both were written by hand as running totals and both were wrong.**
  Acceptance: every such count in a `hot_live` document is re-derived from the population it
  summarises; fired RED on the real corpus before the repair; the enumerations are named in the
  gate so the next reader can re-run them.
  Also in scope: record the `TASK-ACCEPTANCE` recipient-tree boundary found while routing the
  SoftFloat finding — deciding whether it is a defect to fix or a workflow to document.
  Verification: see the Verification Log.
  Commit: `SEMULITH-MIR-0025`

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| — | — | — | **tree complete (4/4).** Four mirror classes gated: the task-tree index (`FRONTIER-SYNC`), the doctrine documents (`REGISTRY-MIRROR`), task-tree facts in the live docs (`TREE-CLAIMS`), and every other derived count in them (`DERIVED-COUNTS`). The next work is `P0-PROFILE.3`. Open it only with the repository clean (the pivot rule). |

<details><summary>The state at 3/3, before the reopen</summary>

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| — | — | — | **tree complete (3/3).** Every mirror on the resume path is gated: the index by `FRONTIER-SYNC`, the two doctrine documents by `REGISTRY-MIRROR`, the live docs by `TREE-CLAIMS`. The next work is execution: `P0-PROFILE.5`, the reference candidate dossier. Open it only with the repository clean (the pivot rule). |

</details>

## Decisions

- `2026-09-14`: **the tree is authoritative, the index mirrors it.** Both orderings were
  available — the gate could have demanded the tree match the index. The tree is where the
  acceptance evidence, the frontier reasoning and the leaf statuses live; the index carries one
  cell per tree. A fix that edits the summary to match the record is safe; a fix that edits the
  record to match its summary destroys information. The gate's failure message says so, so the
  next reader does not have to re-derive the choice.
- `2026-09-14` (`.4`): the `TASK-ACCEPTANCE` recipient-tree boundary is **documented, not
  relaxed.** The gate requires every staged `docs/tasks/*.md` to carry a ticked checklist, which
  cannot distinguish the leaf that OWNS a change from a tree that merely RECEIVES a routed
  finding. The obvious fix — require only *one* staged leaf to pass — was rejected: that is
  exactly the "co-staged unrelated leaf supplies the evidence" hole the box-scoping was hardened
  to close, and reopening it would trade a real soundness property for an inconvenience. The
  workflow is therefore: **a routed annotation lands as its own doc-only commit**, where the gate
  does not apply because no code is staged. That is also independently better — the annotation is
  separately revertible. Demonstrated by `SEMULITH-P0-0024`.
- `2026-09-14`: this tree adds **gates**, not generators. A derived `docs/TASK_TREE.md` would
  also have prevented the drift, and was rejected: the "why next" column carries reasoning that
  no generator can produce, and a generated file invites hand edits that are silently discarded.

## Open Questions

- ~~Is there a mirror in this repository that nothing in this tree covers?~~ **Answered by `.3`,
  and the answer is bounded rather than absolute.** The three mirrors on the resume path are
  gated. What is *not* gated is the general form of the question — any tracked constant that is a
  function of the repository, beyond task-tree facts. That is `docs/CLAIM_VERIFICATION.md` §7's
  constant sweep, it is listed as unmechanized in `LIVE_STATUS.md`, and it is deliberately NOT
  claimed here: this tree gated the mirrors it measured, not every mirror that could exist.

## Blockers

- None.

## Acceptance Checklist (current leaf — `MIRROR-DRIFT.4`)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1: `.1`–`.3` gated what live documents say about
  *task-trees* and nothing else. WHY the gap mattered was not argued — it was **measured, twice,
  in the same session that closed it**. Both numbers were maintained as RUNNING TOTALS: the
  author took the number already written down, added their contribution, and wrote the sum back.

  ```
  $ grep -cv '^#\|^$' doctrine/readme_routes.tsv     # LIVE_STATUS said "24 destinations governed"
  25
  $ scripts/check_derived_counts.sh --list | grep arms  # LIVE_STATUS said "107 self-test arms"
  self-test arms         arm_total                          112
  ```

  The first had been stale since `SEMULITH-P0-0013` added the `profiles/` row; the second was
  wrong by five because a base that already did not reconcile was being incremented.
  ⭐ **A running total is a memory of a measurement, not a measurement.** Nothing recomputed
  either, so both drifted quietly and were committed as fact.

- [x] **ADDRESSED (verified)** — before → after on the symptom, same command:
  `scripts/check_derived_counts.sh` → `rc=1`, `COUNT DRIFT LIVE_STATUS.md: claims '107'
  self-test arms; the repository has 112  [arm_total]`; after re-deriving both numbers →
  `DERIVED-COUNTS: ok (4 derived count claim(s) re-derived)`, `rc=0`. Derived count claims held
  by an instrument went from `0` to `4`.
  ⭐ **The gate caught its own registration**, which is the cleanest demonstration available:
  adding `DERIVED-COUNTS` to the project driver made the repository hold nine project doctrines
  where the page said eight, and the gate said so before the commit could land —
  `COUNT DRIFT LIVE_STATUS.md: claims '8' project doctrines; the repository has 9`. Both numbers
  were then **re-derived by running the enumerators**, not by adding one.

- [x] **NO REGRESSION** — leg 2. `scripts/check_derived_counts.sh --self-test` →
  `DERIVED-COUNTS --self-test: 10 pass / 0 fail` — 8 RED arms asserting the reason (stale count,
  count ahead of the population, one of two claims drifting, the population changing under a
  fixed number, a two-digit claim misread, an enumerator producing nothing, a pattern whose
  number is not first) and 2 GREEN. Arm accounting: `10` written, `10` run.
  ⛔ **One of those arms exists because the first cut was wrong in the worst possible direction.**
  Extraction used `sed -nE "s/.*${pat}.*/\1/p"`, whose leading `.*` is greedy: on `12 widgets`
  it consumed the `1` and captured `2`. A drifting count could therefore read as a matching one —
  a gate that reports agreement about the wrong number. Caught by a GREEN arm that failed:
  `COUNT DRIFT LIVE.md: claims '2' widgets; the repository has 12`. Extraction is now `grep -o`
  off the front of the match, and a pattern that does not begin with its `([0-9]+)` group is
  REFUSED rather than parsed.
  Whole gate `=== all doctrines green ===`, `rc=0`; `make check` →
  `test result: ok. 1 passed; 0 failed`; `make book` → `HTML book written`;
  `scripts/run_smoke.py` → still `ok`, so the P0 evidence path is undisturbed.

- [x] **FIX** — `scripts/check_derived_counts.sh` registered as `DERIVED-COUNTS`, with `--list`
  printing every covered claim, its enumerator and the value it currently derives, so the claim
  and its producer travel together. The `TASK-ACCEPTANCE` boundary is resolved in the Decisions
  section above: **documented, not relaxed**, because the obvious relaxation reopens a measured
  soundness hole.

- `promotion: declined (the lesson IS the DERIVED-COUNTS doctrine — a card would restate the gate's own header, its --list output and the book chapter that already narrates it; docs/knowledge/ is past its health target at 21,661 of 20,480 bytes)`

- [x] **LOCKSTEP** — leg 3: four derived counts are re-derived on every commit, so a running
  total cannot be committed wrong again. `DOCTRINE_ENFORCEMENT.md` and the book chapter gain the
  row (enforced by `REGISTRY-MIRROR`, not by memory), `TOOLBOX.md` the diagnostic;
  `MEMORY.md`, `LIVE_STATUS.md`, `CHANGELOG.md`, `DEV_NOTES.md` updated in this commit.
  ⚠️ Honest limit, stated in the gate itself: it checks the counts it can enumerate. A count whose
  population the script cannot enumerate is invisible to it, which is why `--list` exists.

## Acceptance Checklist (current leaf — `MIRROR-DRIFT.3`)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1: WHERE is `MEMORY.md` and `LIVE_STATUS.md`; WHY is the
  same mechanism as `.1` and `.2` — a number that is a function of `docs/tasks/` written by hand
  and compared with its source by nothing. The census, run at `.1` and re-run here, is that these
  two had **not** drifted. That is the honest finding and this leaf records it rather than
  manufacturing a defect to justify itself:

  ```
  $ scripts/check_tree_claims.sh; echo "rc=$?"
  TREE-CLAIMS: ok (3 live document(s) state nothing the trees contradict)
  rc=0
  ```

  All 11 `N leaves` claims in `LIVE_STATUS.md` and both `MEMORY.md` pointer claims were
  re-derived from `grep -cE '^- ID: .<TREE>\.[0-9]+.'` over every tree and agreed exactly.
  ⭐ A mirror that happens to be correct today is not a checked mirror — it is an unchecked one
  that has not been caught yet. `.1` and `.2` are what that looks like after a few weeks.

- [x] **ADDRESSED (verified)** — with nothing to repair, "before → after" is measured on
  **coverage**, not on a symptom. The population, and what held it before this leaf:

  ```
  $ grep -cE '[0-9]+ (of [0-9]+ )?leaves?' MEMORY.md LIVE_STATUS.md README.md
  README.md:0
  LIVE_STATUS.md:12
  MEMORY.md:1
  $ git grep -lE 'leaves?\b' $(git rev-parse HEAD) -- scripts knowledge-map/scripts | wc -l
  0
  $ scripts/check_tree_claims.sh
  TREE-CLAIMS: ok (3 live document(s) state nothing the trees contradict)
  ```

  **13 live claims, held by 0 instruments, now held by 1.** The classes checked went from none to
  four: leaf totals, done counts, the frontier leaf, and the set of active trees.
  ⭐ The scope is **data, not a list** — the gate reads the `hot_live` rows of
  `doctrine/readme_routes.tsv` (`README.md`, `MEMORY.md`, `LIVE_STATUS.md`, `docs/TASK_TREE.md`),
  so a live surface registered tomorrow is covered tomorrow with no edit to the script, and
  `append_history` files are excluded on purpose: a `CHANGELOG.md` line reading `2 of 9 leaves`
  was true when written, and rewriting it would corrupt the record the changelog exists to keep.

- [x] **NO REGRESSION** — leg 2, and for a prevention leaf this is the load-bearing box. The gate
  was fired RED four times against the **real** documents, not only against fixtures, by breaking
  each claim class in turn and restoring it with `git checkout --`:

  ```
  COUNT DRIFT MEMORY.md: '2 of 9 leaves' for MIRROR-DRIFT; the tree has 2 of 3
  DONE FRONTIER MEMORY.md: names 'MIRROR-DRIFT.1' as the frontier; the tree records it `done`
  MISSING ACTIVE MEMORY.md: 'P0-PROFILE' is `active` and the pointer does not name it
  COUNT DRIFT LIVE_STATUS.md: '13 leaves' for P1-LAB; the tree has 12
  ```

  `scripts/check_tree_claims.sh --self-test` → `TREE-CLAIMS --self-test: 12 pass / 0 fail` —
  1 GREEN and 11 RED arms, **three of the eleven** asserting `rc=2` refusal rather than a verdict
  (`NO LIVE DOCS`, `NO TREES`, `NO ROUTES`), so a check that cannot establish its own scope
  refuses instead of reporting agreement. Arm
  accounting: `grep -cE '(^|[; ])arm "' scripts/check_tree_claims.sh` → `12`, self-test reports
  `12`. Whole gate `=== all doctrines green ===`, `rc=0`; `make check` →
  `test result: ok. 1 passed; 0 failed`; `make book` → `HTML book written`.
  ⭐ **The gates now catch each other, and that was observed rather than hoped.** Registering
  `TREE-CLAIMS` without adding its rows to the two doctrine documents produced, immediately:
  `NOT MIRRORED DOCTRINE_ENFORCEMENT.md: 'TREE-CLAIMS' is registered and has no row` and the same
  for `doctrines.md`, `rc=1` — `.2`'s gate catching `.3`'s omission inside the same commit. The
  identical omission survived two prior registrations unnoticed.

- [x] **FIX** — `scripts/check_tree_claims.sh` added and registered as `TREE-CLAIMS`. Its scope is
  derived from `doctrine/readme_routes.tsv`; `docs/TASK_TREE.md` is excluded because
  `FRONTIER-SYNC` owns it and two gates reporting one breach twice is noise, not depth.

- [x] **LOCKSTEP** — leg 3: all three mirrors on the resume path are now re-derived on every
  commit. `DOCTRINE_ENFORCEMENT.md` and the book chapter gain the `TREE-CLAIMS` row (enforced by
  `REGISTRY-MIRROR`, not by memory), `TOOLBOX.md` the diagnostic row, the book a section on
  deriving a gate's scope from data and one on the gates catching each other; `MEMORY.md`,
  `LIVE_STATUS.md`, `CHANGELOG.md` and `DEV_NOTES.md` updated in this commit. The tree's Open
  Question — "is there a mirror nothing here covers?" — is answered below rather than left open.

## Acceptance Checklist (current leaf — `MIRROR-DRIFT.2`)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1: WHERE is `docs/book/src/working/doctrines.md`; WHY is
  that two documents restate a registry held in two shell arrays, and nothing compared them.
  `DOCTRINE_ENFORCEMENT.md` even calls itself "the human-readable mirror of the enforcer
  registry" — a mirror is exactly the artifact that needs a gate. Measured by extracting the
  registered ids from both drivers and the id-shaped table rows from both documents:

  ```
  $ scripts/check_registry_mirror.sh; echo "rc=$?"
  REGISTRY-MIRROR: a doctrine document no longer mirrors the enforcer registry.
    NOT MIRRORED doctrines.md: 'FRONTIER-SYNC' is registered and has no row …
    NOT MIRRORED doctrines.md: 'PROFILE-CONSISTENCY' is registered and has no row …
    NOT MIRRORED doctrines.md: 'SEAM-INTEGRITY' is registered and has no row …
  rc=1
  ```

  ⭐ The direction of the error is the finding. A mirror that falls behind never **invents** a
  guarantee — it quietly **withholds** one, and it withholds it on the surface the director
  reviews instead of the code. The book claimed three project doctrines while five were
  registered and running, so the review surface understated the repository's own enforcement by
  40% and looked entirely healthy doing it.

- [x] **ADDRESSED (verified)** — before → after on the symptom, same command:
  `scripts/check_registry_mirror.sh` → `rc=1` with three `NOT MIRRORED` findings (above), then
  after the chapter was repaired → `REGISTRY-MIRROR: ok (2 document(s) mirror the registry)`,
  `rc=0`. The gate also fired in the **opposite** direction during the repair, unprompted and
  correctly: listing `REGISTRY-MIRROR` in the book one step before registering it produced
  `PHANTOM doctrines.md: 'REGISTRY-MIRROR' has a row but is registered nowhere`, `rc=1` — a
  document promising a gate that does not run is the more dangerous of the two drifts, and it was
  caught on the real corpus rather than only in a fixture.

- [x] **NO REGRESSION** — leg 2: `scripts/check_registry_mirror.sh --self-test` →
  `REGISTRY-MIRROR --self-test: 11 pass / 0 fail` — 10 RED arms asserting the reason
  (`NOT MIRRORED`, `PHANTOM`, `COUNT DRIFT`, `UNREADABLE COUNT`, `WRONG SECTION` in both
  directions, `NOT EXECUTABLE`, `NO CHECK`, `NO MIRROR`) plus a refusal arm asserting `rc=2`
  when the registry parses to nothing. Arm accounting per this tree's own lesson —
  `grep -nE '(^|[; ])arm "' scripts/check_registry_mirror.sh | wc -l` → `11`, and the self-test
  reports `11`: every arm written is an arm that ran. Whole gate: `scripts/check_doctrines.sh`
  → `=== all doctrines green ===`, `rc=0`; `make check` → `test result: ok. 1 passed; 0 failed`;
  `make book` → `INFO HTML book written to …/docs/book/book`, so the repaired chapter renders.
  ⭐ The durable half of leg 2 is that the class found at `.1` is now **mechanically** caught,
  not merely written down. Both self-test harnesses gained a strict-arity guard on every fixture
  helper, and it was fired RED by re-introducing the original defect — deleting one `;`:

  ```
  FRONTIER-SYNC self-test HARNESS: index() got 6 argument(s), expected 2 — a missing `;` before `arm` swallows it
  FRONTIER-SYNC --self-test: 15 pass / 1 fail
  ```

  Restored, `16 pass / 0 fail`. A helper that ignores surplus arguments is what made the swallow
  silent; refusing them is what makes it loud.

- [x] **FIX** — `scripts/check_registry_mirror.sh` added and registered as `REGISTRY-MIRROR`.
  The book chapter gained the three missing rows and two new sections that document the family
  honestly — what drifted, in which direction, and why a gate was chosen over a generator.
  `argc` guards added to both self-test harnesses.

- [x] **LOCKSTEP** — leg 3: both mirrors are now re-derived on every commit, so neither can fall
  behind a registration again without the commit failing. `DOCTRINE_ENFORCEMENT.md` gains the
  `REGISTRY-MIRROR` row, `TOOLBOX.md` the diagnostic row, the book its three rows and the
  narrative; `MEMORY.md`, `LIVE_STATUS.md`, `CHANGELOG.md` and `DEV_NOTES.md` updated in this
  commit. The gap `.1` declared — "the book is deliberately not updated by this leaf, owner
  `MIRROR-DRIFT.2`" — is closed by this commit, which is what makes that declaration a routed
  finding rather than an excuse.

## Completed-leaf evidence (archive)

### `MIRROR-DRIFT.3` — the live documents' tree claims

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1: WHERE is `MEMORY.md` and `LIVE_STATUS.md`; WHY is the
  same mechanism as `.1` and `.2` — a number that is a function of `docs/tasks/` written by hand
  and compared with its source by nothing. The census, run at `.1` and re-run here, is that these
  two had **not** drifted. That is the honest finding and this leaf records it rather than
  manufacturing a defect to justify itself:

  ```
  $ scripts/check_tree_claims.sh; echo "rc=$?"
  TREE-CLAIMS: ok (3 live document(s) state nothing the trees contradict)
  rc=0
  ```

  All 11 `N leaves` claims in `LIVE_STATUS.md` and both `MEMORY.md` pointer claims were
  re-derived from `grep -cE '^- ID: .<TREE>\.[0-9]+.'` over every tree and agreed exactly.
  ⭐ A mirror that happens to be correct today is not a checked mirror — it is an unchecked one
  that has not been caught yet. `.1` and `.2` are what that looks like after a few weeks.

- [x] **ADDRESSED (verified)** — with nothing to repair, "before → after" is measured on
  **coverage**, not on a symptom. The population, and what held it before this leaf:

  ```
  $ grep -cE '[0-9]+ (of [0-9]+ )?leaves?' MEMORY.md LIVE_STATUS.md README.md
  README.md:0
  LIVE_STATUS.md:12
  MEMORY.md:1
  $ git grep -lE 'leaves?\b' $(git rev-parse HEAD) -- scripts knowledge-map/scripts | wc -l
  0
  $ scripts/check_tree_claims.sh
  TREE-CLAIMS: ok (3 live document(s) state nothing the trees contradict)
  ```

  **13 live claims, held by 0 instruments, now held by 1.** The classes checked went from none to
  four: leaf totals, done counts, the frontier leaf, and the set of active trees.
  ⭐ The scope is **data, not a list** — the gate reads the `hot_live` rows of
  `doctrine/readme_routes.tsv` (`README.md`, `MEMORY.md`, `LIVE_STATUS.md`, `docs/TASK_TREE.md`),
  so a live surface registered tomorrow is covered tomorrow with no edit to the script, and
  `append_history` files are excluded on purpose: a `CHANGELOG.md` line reading `2 of 9 leaves`
  was true when written, and rewriting it would corrupt the record the changelog exists to keep.

- [x] **NO REGRESSION** — leg 2, and for a prevention leaf this is the load-bearing box. The gate
  was fired RED four times against the **real** documents, not only against fixtures, by breaking
  each claim class in turn and restoring it with `git checkout --`:

  ```
  COUNT DRIFT MEMORY.md: '2 of 9 leaves' for MIRROR-DRIFT; the tree has 2 of 3
  DONE FRONTIER MEMORY.md: names 'MIRROR-DRIFT.1' as the frontier; the tree records it `done`
  MISSING ACTIVE MEMORY.md: 'P0-PROFILE' is `active` and the pointer does not name it
  COUNT DRIFT LIVE_STATUS.md: '13 leaves' for P1-LAB; the tree has 12
  ```

  `scripts/check_tree_claims.sh --self-test` → `TREE-CLAIMS --self-test: 12 pass / 0 fail` —
  1 GREEN and 11 RED arms, **three of the eleven** asserting `rc=2` refusal rather than a verdict
  (`NO LIVE DOCS`, `NO TREES`, `NO ROUTES`), so a check that cannot establish its own scope
  refuses instead of reporting agreement. Arm
  accounting: `grep -cE '(^|[; ])arm "' scripts/check_tree_claims.sh` → `12`, self-test reports
  `12`. Whole gate `=== all doctrines green ===`, `rc=0`; `make check` →
  `test result: ok. 1 passed; 0 failed`; `make book` → `HTML book written`.
  ⭐ **The gates now catch each other, and that was observed rather than hoped.** Registering
  `TREE-CLAIMS` without adding its rows to the two doctrine documents produced, immediately:
  `NOT MIRRORED DOCTRINE_ENFORCEMENT.md: 'TREE-CLAIMS' is registered and has no row` and the same
  for `doctrines.md`, `rc=1` — `.2`'s gate catching `.3`'s omission inside the same commit. The
  identical omission survived two prior registrations unnoticed.

- [x] **FIX** — `scripts/check_tree_claims.sh` added and registered as `TREE-CLAIMS`. Its scope is
  derived from `doctrine/readme_routes.tsv`; `docs/TASK_TREE.md` is excluded because
  `FRONTIER-SYNC` owns it and two gates reporting one breach twice is noise, not depth.

- [x] **LOCKSTEP** — leg 3: all three mirrors on the resume path are now re-derived on every
  commit. `DOCTRINE_ENFORCEMENT.md` and the book chapter gain the `TREE-CLAIMS` row (enforced by
  `REGISTRY-MIRROR`, not by memory), `TOOLBOX.md` the diagnostic row, the book a section on
  deriving a gate's scope from data and one on the gates catching each other; `MEMORY.md`,
  `LIVE_STATUS.md`, `CHANGELOG.md` and `DEV_NOTES.md` updated in this commit. The tree's Open
  Question — "is there a mirror nothing here covers?" — is answered below rather than left open.

## Acceptance Checklist (current leaf — `MIRROR-DRIFT.2`)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1: WHERE is `docs/book/src/working/doctrines.md`; WHY is
  that two documents restate a registry held in two shell arrays, and nothing compared them.
  `DOCTRINE_ENFORCEMENT.md` even calls itself "the human-readable mirror of the enforcer
  registry" — a mirror is exactly the artifact that needs a gate. Measured by extracting the
  registered ids from both drivers and the id-shaped table rows from both documents:

  ```
  $ scripts/check_registry_mirror.sh; echo "rc=$?"
  REGISTRY-MIRROR: a doctrine document no longer mirrors the enforcer registry.
    NOT MIRRORED doctrines.md: 'FRONTIER-SYNC' is registered and has no row …
    NOT MIRRORED doctrines.md: 'PROFILE-CONSISTENCY' is registered and has no row …
    NOT MIRRORED doctrines.md: 'SEAM-INTEGRITY' is registered and has no row …
  rc=1
  ```

  ⭐ The direction of the error is the finding. A mirror that falls behind never **invents** a
  guarantee — it quietly **withholds** one, and it withholds it on the surface the director
  reviews instead of the code. The book claimed three project doctrines while five were
  registered and running, so the review surface understated the repository's own enforcement by
  40% and looked entirely healthy doing it.

- [x] **ADDRESSED (verified)** — before → after on the symptom, same command:
  `scripts/check_registry_mirror.sh` → `rc=1` with three `NOT MIRRORED` findings (above), then
  after the chapter was repaired → `REGISTRY-MIRROR: ok (2 document(s) mirror the registry)`,
  `rc=0`. The gate also fired in the **opposite** direction during the repair, unprompted and
  correctly: listing `REGISTRY-MIRROR` in the book one step before registering it produced
  `PHANTOM doctrines.md: 'REGISTRY-MIRROR' has a row but is registered nowhere`, `rc=1` — a
  document promising a gate that does not run is the more dangerous of the two drifts, and it was
  caught on the real corpus rather than only in a fixture.

- [x] **NO REGRESSION** — leg 2: `scripts/check_registry_mirror.sh --self-test` →
  `REGISTRY-MIRROR --self-test: 11 pass / 0 fail` — 10 RED arms asserting the reason
  (`NOT MIRRORED`, `PHANTOM`, `COUNT DRIFT`, `UNREADABLE COUNT`, `WRONG SECTION` in both
  directions, `NOT EXECUTABLE`, `NO CHECK`, `NO MIRROR`) plus a refusal arm asserting `rc=2`
  when the registry parses to nothing. Arm accounting per this tree's own lesson —
  `grep -nE '(^|[; ])arm "' scripts/check_registry_mirror.sh | wc -l` → `11`, and the self-test
  reports `11`: every arm written is an arm that ran. Whole gate: `scripts/check_doctrines.sh`
  → `=== all doctrines green ===`, `rc=0`; `make check` → `test result: ok. 1 passed; 0 failed`;
  `make book` → `INFO HTML book written to …/docs/book/book`, so the repaired chapter renders.
  ⭐ The durable half of leg 2 is that the class found at `.1` is now **mechanically** caught,
  not merely written down. Both self-test harnesses gained a strict-arity guard on every fixture
  helper, and it was fired RED by re-introducing the original defect — deleting one `;`:

  ```
  FRONTIER-SYNC self-test HARNESS: index() got 6 argument(s), expected 2 — a missing `;` before `arm` swallows it
  FRONTIER-SYNC --self-test: 15 pass / 1 fail
  ```

  Restored, `16 pass / 0 fail`. A helper that ignores surplus arguments is what made the swallow
  silent; refusing them is what makes it loud.

- [x] **FIX** — `scripts/check_registry_mirror.sh` added and registered as `REGISTRY-MIRROR`.
  The book chapter gained the three missing rows and two new sections that document the family
  honestly — what drifted, in which direction, and why a gate was chosen over a generator.
  `argc` guards added to both self-test harnesses.

- [x] **LOCKSTEP** — leg 3: both mirrors are now re-derived on every commit, so neither can fall
  behind a registration again without the commit failing. `DOCTRINE_ENFORCEMENT.md` gains the
  `REGISTRY-MIRROR` row, `TOOLBOX.md` the diagnostic row, the book its three rows and the
  narrative; `MEMORY.md`, `LIVE_STATUS.md`, `CHANGELOG.md` and `DEV_NOTES.md` updated in this
  commit. The gap `.1` declared — "the book is deliberately not updated by this leaf, owner
  `MIRROR-DRIFT.2`" — is closed by this commit, which is what makes that declaration a routed
  finding rather than an excuse.

### `MIRROR-DRIFT.2` — gate the doctrine documents against the registry

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1: WHERE is `docs/book/src/working/doctrines.md`; WHY is
  that two documents restate a registry held in two shell arrays, and nothing compared them.
  `DOCTRINE_ENFORCEMENT.md` even calls itself "the human-readable mirror of the enforcer
  registry" — a mirror is exactly the artifact that needs a gate. Measured by extracting the
  registered ids from both drivers and the id-shaped table rows from both documents:

  ```
  $ scripts/check_registry_mirror.sh; echo "rc=$?"
  REGISTRY-MIRROR: a doctrine document no longer mirrors the enforcer registry.
    NOT MIRRORED doctrines.md: 'FRONTIER-SYNC' is registered and has no row …
    NOT MIRRORED doctrines.md: 'PROFILE-CONSISTENCY' is registered and has no row …
    NOT MIRRORED doctrines.md: 'SEAM-INTEGRITY' is registered and has no row …
  rc=1
  ```

  ⭐ The direction of the error is the finding. A mirror that falls behind never **invents** a
  guarantee — it quietly **withholds** one, and it withholds it on the surface the director
  reviews instead of the code. The book claimed three project doctrines while five were
  registered and running, so the review surface understated the repository's own enforcement by
  40% and looked entirely healthy doing it.

- [x] **ADDRESSED (verified)** — before → after on the symptom, same command:
  `scripts/check_registry_mirror.sh` → `rc=1` with three `NOT MIRRORED` findings (above), then
  after the chapter was repaired → `REGISTRY-MIRROR: ok (2 document(s) mirror the registry)`,
  `rc=0`. The gate also fired in the **opposite** direction during the repair, unprompted and
  correctly: listing `REGISTRY-MIRROR` in the book one step before registering it produced
  `PHANTOM doctrines.md: 'REGISTRY-MIRROR' has a row but is registered nowhere`, `rc=1` — a
  document promising a gate that does not run is the more dangerous of the two drifts, and it was
  caught on the real corpus rather than only in a fixture.

- [x] **NO REGRESSION** — leg 2: `scripts/check_registry_mirror.sh --self-test` →
  `REGISTRY-MIRROR --self-test: 11 pass / 0 fail` — 10 RED arms asserting the reason
  (`NOT MIRRORED`, `PHANTOM`, `COUNT DRIFT`, `UNREADABLE COUNT`, `WRONG SECTION` in both
  directions, `NOT EXECUTABLE`, `NO CHECK`, `NO MIRROR`) plus a refusal arm asserting `rc=2`
  when the registry parses to nothing. Arm accounting per this tree's own lesson —
  `grep -nE '(^|[; ])arm "' scripts/check_registry_mirror.sh | wc -l` → `11`, and the self-test
  reports `11`: every arm written is an arm that ran. Whole gate: `scripts/check_doctrines.sh`
  → `=== all doctrines green ===`, `rc=0`; `make check` → `test result: ok. 1 passed; 0 failed`;
  `make book` → `INFO HTML book written to …/docs/book/book`, so the repaired chapter renders.
  ⭐ The durable half of leg 2 is that the class found at `.1` is now **mechanically** caught,
  not merely written down. Both self-test harnesses gained a strict-arity guard on every fixture
  helper, and it was fired RED by re-introducing the original defect — deleting one `;`:

  ```
  FRONTIER-SYNC self-test HARNESS: index() got 6 argument(s), expected 2 — a missing `;` before `arm` swallows it
  FRONTIER-SYNC --self-test: 15 pass / 1 fail
  ```

  Restored, `16 pass / 0 fail`. A helper that ignores surplus arguments is what made the swallow
  silent; refusing them is what makes it loud.

- [x] **FIX** — `scripts/check_registry_mirror.sh` added and registered as `REGISTRY-MIRROR`.
  The book chapter gained the three missing rows and two new sections that document the family
  honestly — what drifted, in which direction, and why a gate was chosen over a generator.
  `argc` guards added to both self-test harnesses.

- [x] **LOCKSTEP** — leg 3: both mirrors are now re-derived on every commit, so neither can fall
  behind a registration again without the commit failing. `DOCTRINE_ENFORCEMENT.md` gains the
  `REGISTRY-MIRROR` row, `TOOLBOX.md` the diagnostic row, the book its three rows and the
  narrative; `MEMORY.md`, `LIVE_STATUS.md`, `CHANGELOG.md` and `DEV_NOTES.md` updated in this
  commit. The gap `.1` declared — "the book is deliberately not updated by this leaf, owner
  `MIRROR-DRIFT.2`" — is closed by this commit, which is what makes that declaration a routed
  finding rather than an excuse.

### `MIRROR-DRIFT.1` — gate the task-tree index against the trees

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1: WHERE is `docs/TASK_TREE.md`'s `P0-PROFILE` row;
  WHY is that `COMMIT.md` makes updating it conditional ("update `docs/TASK_TREE.md` … **only if
  the frontier changes**") while nothing compares the two files. Commit `SEMULITH-P0-0014` moved
  the frontier from `.2` to `.5` inside the tree and left the index cell at `.2`. Measured over
  the whole population before any fix, with a probe that reads both files per tree:

  ```
  $ grep -c '^| \[' docs/TASK_TREE.md          # index rows
  14
  $ bash scripts/check_frontier_sync.sh; echo "rc=$?"
  FRONTIER-SYNC: the task-tree index no longer mirrors the trees it indexes.
    FRONTIER DRIFT P0-PROFILE: index says '.2', tree's Current Frontier says 'P0-PROFILE.5'
    DONE FRONTIER P0-PROFILE: the index points at '.2', which the tree records as `done`
    DONE FRONTIER P0-PROFILE: the index points at '.1', which the tree records as `done`
  rc=1
  ```

  ⭐ The falsifying question was *"is one stale cell out of fourteen worth a gate?"* — and the
  answer is that the drift landed on the **only `active` tree**, which is the only row anyone
  ever reads. `CLAUDE.md` routes a resuming agent `MEMORY.md` → the index → the frontier, so the
  cell that rotted is the second hop of the recovery procedure itself. A 1-in-14 drift rate is
  not the measurement that matters; a 1-in-1 drift rate on the followed row is.

- [x] **ADDRESSED (verified)** — before → after on the symptom, same command both times:
  `bash scripts/check_frontier_sync.sh` → `rc=1` with three findings (above), then after the
  index row was repaired → `FRONTIER-SYNC: ok (15 tree(s) mirrored by docs/TASK_TREE.md)` — 15, not 14, because
  this tree's own row was added under the same gate,
  `rc=0`. The repair edited the **index**, not the tree, per this tree's first decision. The
  census behind `.3`'s "no drift yet" was run here and is recorded so it is not re-asserted from
  memory: every `N leaves` claim in `LIVE_STATUS.md` was re-derived from the trees —
  `grep -cE '^- ID: .<TREE>\.[0-9]+.' docs/tasks/<TREE>.md` over all 14 trees gave
  `8,1,7,7,9,12,9,6,10,7,8,7,8,4`, matching all 11 milestone claims and both `MEMORY.md`
  assertions (`P0-PROFILE`, `2 of 9`, frontier `.5`) exactly — `drifted: 1 of 3 mirrors`.

- [x] **NO REGRESSION** — leg 2: the gate was fired RED before it was trusted, on synthetic
  fixtures **and** on the real corpus. `bash scripts/check_frontier_sync.sh --self-test` →
  `FRONTIER-SYNC --self-test: 16 pass / 0 fail` — 14 RED arms, each asserting the *reason* and
  not merely the verdict: `FRONTIER DRIFT`, `PREMATURE COMPLETE`, `STALE FRONTIER`,
  `DONE FRONTIER`, `STATUS DRIFT`, `UNKNOWN LEAF` (from the index and from the tree),
  `COUNT DRIFT` in both spellings, `UNLISTED TREE`, `NO TREE FILE`, and two REFUSE arms
  (`NO ROWS`, `NO INDEX`) that assert `rc=2` rather than a silent pass. Whole gate afterwards:
  `scripts/check_doctrines.sh` → `=== all doctrines green ===`, `rc=0`; `make check` →
  `test result: ok. 1 passed; 0 failed`, `rc=0`.
  ⛔ The self-test itself was caught lying first, which is why it is worth reporting: the first
  run printed `4 pass / 0 fail` — **green, and judging almost nothing**. Ten `arm` calls sat on
  the same physical line as the fixture call that preceded them, so bash passed `arm` and its
  three arguments as extra positional parameters to a function that reads only `$1` and `$2`,
  and they were discarded in silence. Found by reading the arm count against the number of arms
  written (`4` vs `14`), not by reading the code. A self-test that runs a third of its arms and
  reports `0 fail` is precisely the "green gate that judges nothing" this repository's own
  `DEV_NOTES.md` names as the class a template must not ship.

- [x] **FIX** — `scripts/check_frontier_sync.sh` added (parse both files, compare six
  properties, refuse rather than pass when it cannot parse) and registered in
  `scripts/check_doctrines.project.sh` as `FRONTIER-SYNC`. `docs/TASK_TREE.md`'s `P0-PROFILE`
  row repaired to `.5` and given a leaf count the gate now re-derives. The new row for this tree
  was added under the same rule.

- [x] **LOCKSTEP** — leg 3: the agreement is re-derived on every commit by the pre-commit hook,
  so the index cannot rot again without the commit failing. `DOCTRINE_ENFORCEMENT.md` gains the
  registry row and `TOOLBOX.md` the diagnostic row; `MEMORY.md`, `LIVE_STATUS.md`,
  `CHANGELOG.md` and `DEV_NOTES.md` updated in this commit, and the lesson promoted to
  [`self-test-arms-that-never-ran`](../knowledge/self-test-arms-that-never-ran.md).
  ⛔ **The book is deliberately NOT updated by this leaf, and that is a named gap, not an
  oversight.** `docs/book/src/working/doctrines.md` already omits `PROFILE-CONSISTENCY` and
  `SEAM-INTEGRITY`; `FRONTIER-SYNC` makes three. Adding this one row by hand would repair the
  symptom and destroy the evidence `MIRROR-DRIFT.2` needs — that leaf's acceptance requires the
  new gate to be **fired RED against the real drift** before the repair, and a mirror that has
  been quietly patched cannot be fired RED. The gap is owned by `MIRROR-DRIFT.2`, which is the
  next commit, and the drift it will show is the stronger measurement: *the book fell further
  behind on the very commit that registered a doctrine*, which is the mechanism rather than an
  anecdote.
  ⭐ A second defect surfaced while editing the mirror, and it is invisible in the source: two
  blank lines inside the project-doctrine table split it into three GFM fragments, so
  `PROFILE-CONSISTENCY` and `SEAM-INTEGRITY` rendered as literal `| … |` text rather than table
  rows. `awk` over the section counted `rows: 8` (header + separator + 6) only after the blanks
  were removed; before, the table ended at three rows. Found by counting, not by reading —
  a table that is right in the file and wrong on the page is the exact failure mode
  `TABLE-ARITY-RATCHET` was written for one column over, and neither gate sees a blank line.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-14` | `MIRROR-DRIFT.1` | drift census over all 14 index rows | `1` drifted row, on the only `active` tree |
| `2026-09-14` | `MIRROR-DRIFT.1` | `check_frontier_sync.sh` on the real index, before | `rc=1`: `FRONTIER DRIFT` + 2 × `DONE FRONTIER` |
| `2026-09-14` | `MIRROR-DRIFT.1` | `check_frontier_sync.sh` on the real index, after | `ok (15 tree(s) mirrored)`, `rc=0` |
| `2026-09-14` | `MIRROR-DRIFT.1` | `check_frontier_sync.sh --self-test` | `16 pass / 0 fail` (14 RED arms) |
| `2026-09-14` | `MIRROR-DRIFT.1` | leaf-count re-derivation vs `LIVE_STATUS.md` / `MEMORY.md` | 11 of 11 counts and both pointer claims agree |
| `2026-09-14` | `MIRROR-DRIFT.1` | project-doctrine table fragments in `DOCTRINE_ENFORCEMENT.md` | 3 fragments before, `rows: 8` in one table after |
| `2026-09-14` | `MIRROR-DRIFT.1` | `scripts/check_doctrines.sh` + `make check` | `all doctrines green`, `rc=0`; `test result: ok. 1 passed` |
| `2026-09-14` | `MIRROR-DRIFT.2` | `check_registry_mirror.sh` on the real documents, before | `rc=1`: 3 × `NOT MIRRORED` on the book chapter |
| `2026-09-14` | `MIRROR-DRIFT.2` | the same gate, in the opposite direction, unprompted | `PHANTOM … registered nowhere`, `rc=1` — a document promising a gate that does not run |
| `2026-09-14` | `MIRROR-DRIFT.2` | `check_registry_mirror.sh` after the repair | `ok (2 document(s) mirror the registry)`, `rc=0` |
| `2026-09-14` | `MIRROR-DRIFT.2` | `check_registry_mirror.sh --self-test`, arms written vs run | `11 pass / 0 fail`; `11` written, `11` ran |
| `2026-09-14` | `MIRROR-DRIFT.2` | the new `argc` guard fired RED by deleting one `;` | `index() got 6 argument(s), expected 2`; `15 pass / 1 fail`, restored `16 / 0` |
| `2026-09-14` | `MIRROR-DRIFT.2` | `scripts/check_doctrines.sh` + `make check` + `make book` | `all doctrines green`; `1 passed`; `HTML book written` |
| `2026-09-14` | `MIRROR-DRIFT.3` | `check_tree_claims.sh` on the real live documents | `ok (3 live document(s) …)`, `rc=0` — no drift, as the `.1` census predicted |
| `2026-09-14` | `MIRROR-DRIFT.3` | four controls, each breaking a real claim class | `COUNT DRIFT` ×2, `DONE FRONTIER`, `MISSING ACTIVE` — all restored |
| `2026-09-14` | `MIRROR-DRIFT.3` | `check_tree_claims.sh --self-test`, arms written vs run | `12 pass / 0 fail`; `12` written, `12` ran |
| `2026-09-14` | `MIRROR-DRIFT.3` | the interlock: registering a doctrine without mirroring it | `REGISTRY-MIRROR` → `NOT MIRRORED … 'TREE-CLAIMS'` in both documents, `rc=1` |
| `2026-09-14` | `MIRROR-DRIFT.4` | census of derived counts in the live docs | 2 of 4 were wrong: `24` vs `25`, `107` vs `112` |
| `2026-09-14` | `MIRROR-DRIFT.4` | `check_derived_counts.sh` on the real corpus, before | `COUNT DRIFT … claims '107' self-test arms; the repository has 112` |
| `2026-09-14` | `MIRROR-DRIFT.4` | the gate catches its own registration | `claims '8' project doctrines; the repository has 9` |
| `2026-09-14` | `MIRROR-DRIFT.4` | after re-deriving (not incrementing) | `ok (4 derived count claim(s) re-derived)`, `rc=0` |
| `2026-09-14` | `MIRROR-DRIFT.4` | `--self-test`, arms written vs run | `10 pass / 0 fail`; `10` written, `10` ran |
| `2026-09-14` | `MIRROR-DRIFT.4` | the greedy-extraction defect, caught by a GREEN arm | `claims '2' widgets` for a `12 widgets` claim — fixed and armed |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `MIRROR-DRIFT.1` | `SEMULITH-MIR-0017 (leaf MIRROR-DRIFT.1): gate the task-tree index against the trees` | 14 RED arms; one real drift repaired |
| `MIRROR-DRIFT.2` | `SEMULITH-MIR-0018 (leaf MIRROR-DRIFT.2): gate the doctrine documents against the registry` | 10 RED arms; the book under-reported 2 of 5 project doctrines |
| `MIRROR-DRIFT.3` | `SEMULITH-MIR-0019 (leaf MIRROR-DRIFT.3): gate the live documents' tree claims` | 11 RED arms; no drift to repair — scope read from the routes registry |
| `MIRROR-DRIFT.4` | `SEMULITH-MIR-0025 (leaf MIRROR-DRIFT.4): re-derive the counts the live docs carry` | 8 RED arms; 2 real drifts, both self-inflicted running totals |

## Changelog

- `2026-09-14`: Created after a drift found while resuming: `MEMORY.md` and `docs/TASK_TREE.md`
  disagreed about which leaf was next, and the index was the one that was wrong.
- `2026-09-14`: `MIRROR-DRIFT.1` completed. The index is now a checked mirror rather than a
  remembered one.
- `2026-09-14`: `MIRROR-DRIFT.2` completed. The review surface can no longer under-report the
  repository's own enforcement, and the silent-arm-swallow found at `.1` is now caught by a
  guard rather than remembered.
- `2026-09-14`: `MIRROR-DRIFT.3` completed and the tree closed (3/3). Every mirror on the resume
  path is gated, and the gates now catch each other: registering a doctrine without mirroring it
  failed inside the same commit that registered it.
- `2026-09-14`: reopened for `.4`. Two derived counts were committed wrong in a single session —
  both maintained as running totals — which is a mirror class the first three leaves did not
  cover. `.4` closes it and the tree is complete at 4/4.
