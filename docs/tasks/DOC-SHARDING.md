# DOC-SHARDING: shard the append-history surfaces when their ceilings fire

## Metadata

- Tree ID: `DOC-SHARDING`
- Status: `active` (reopened `2026-09-28` for `.2` — the `DEV_NOTES.md` trigger fired; leaf
  `.1` landed `2026-09-27`)
- Roadmap lane: repository hygiene — the append-history ceilings (`doctrine/readme_routes.tsv`)
- Gate: none of its own; keeps `README-ROUTING-CLOSURE` green by giving the fired trigger its
  owner
- Consumed by: the commit workflow — every slice adds a `CHANGELOG.md` entry, so the surface
  fires again the moment the head has no room; must be consumed before the next slice lands
- Depends on: the fired trigger, measured `2026-09-27`: `CHANGELOG.md` at 65,527 of 65,536
  bytes (headroom 9 bytes) after `SEMILITH-RM-0060` compressed its entry to fit; `ROADMAP.md`
  at 24,522 of 24,576 after the same unit. The debt was recorded at adoption
  (`README_POLICY.md`): the ceilings "are the trigger that opens the leaf which builds it"
- Unlocks: unconstrained changelog entries again; the same tool later serves `DEV_NOTES.md`
  — whose trigger fired `2026-09-28` (leaf `.2` owns the remedy)
- Created: `2026-09-27`
- Owner: repo-local workflow

## Goal

Build the sharding tool the adoption debt promised: when an `append_history` surface hits its
byte ceiling, its oldest entries move to frozen shards under a new repository-relative
directory, the head stays a readable recent-history surface under its ceiling, and a tracked
check proves the shards are frozen (a manifest of hashes; old rows never change) and the
partition is complete (no lost or duplicated entries). The trigger fired; this tree owns the
remedy.

## Non-Goals

- **Not a ceiling raise.** The registry raises a ceiling only on a reviewed contract
  expansion; sharding is the declared alternative.
- **Not rewriting history.** Committed entries move verbatim — bytes identical, git history
  unchanged; the manifest is the freeze proof going forward.
- **Not generalising beyond the append-history class.** Only `author_overflow`/`append_history`
  surfaces (`CHANGELOG.md` today, `DEV_NOTES.md` when it fires) are in scope.

## Acceptance Criteria

1. `scripts/shard_history.py` moves the oldest `CHANGELOG.md` entries into
   `docs/changelog/shard-NNNN.md` (bytes verbatim), rewrites the head under its ceiling, and
   updates `docs/changelog/SHARDS.sha256` — deterministic, re-running is a no-op.
2. A tracked check (with `--self-test`, fired RED before registration) proves: every shard
   hashes to its manifest row, manifest rows are append-only, and head + shards contain
   exactly the entries the head had before sharding — none lost, none duplicated.
3. `docs/changelog/` is registered in `doctrine/readme_routes.tsv` in the same commit that
   creates it, with the class and bounds its lifecycle demands.
4. Live docs (`MEMORY.md`, this tree, `README_POLICY.md`'s transition-debt note) updated in
   the same commit.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `DOC-SHARDING.2` | `pending` | the `DEV_NOTES.md` ceiling fired — measured `2026-09-28`: 49,145 of 49,152 bytes after `SEMILITH-PL-0006` compressed its entry to fit; the `.1` remedy is CHANGELOG-specific (shard naming, manifest, freeze check all scoped to `docs/changelog/`), so the only responses today are compression or this leaf |

## Task Tree

- ID: `DOC-SHARDING`
  Status: `active` (reopened `2026-09-28` for the fired `DEV_NOTES.md` trigger)
  Goal: the fired ceiling trigger gets its remedy — frozen shards, a manifest, a check
  Children: `DOC-SHARDING.1` (done), `DOC-SHARDING.2`

- ID: `DOC-SHARDING.2` — **the DEV_NOTES shard path**
  Status: `pending`
  Goal: `DEV_NOTES.md` gets the same lifecycle `CHANGELOG.md` has: when its ceiling fires, its
    oldest dated entries move to frozen shards under a repository-relative directory with their
    own manifest, and a tracked check proves frozen + exactly-partitioned.
  Trigger (measured `2026-09-28`, leaf `P1-LAB.6`): `DEV_NOTES.md` at 49,145 of its 49,152-byte
    registry ceiling after its entry was compressed to fit — the same fired-trigger shape
    `.1` records for `CHANGELOG.md` (9 bytes then, 7 now). Compression is the response the
    registry names as the inferior one.
  Scope notes: `scripts/shard_history.py`, `docs/changelog/SHARDS.sha256`, and
    `scripts/check_changelog_shards.sh` are all scoped to `CHANGELOG.md` (shard-NNNN naming
    inside `docs/changelog/`). Generalize deliberately — a `--head`/`--shard-dir`/`--manifest`
    parameterization or a reviewed parallel path — and register the new shard directory in
    `doctrine/readme_routes.tsv` in the same commit that creates it. `SHARD-FREEZE` extends to
    the new manifest or a sibling check lands beside it, fired RED before registration.
  Acceptance: sharding `DEV_NOTES.md` moves whole dated entries byte-verbatim, rewrites the
    head under its ceiling, the freeze/completeness check proves the partition durably, and a
    re-run is a no-op.
  Blockers: none — consumed by the commit workflow (every slice adds a `DEV_NOTES.md` entry).

- ID: `DOC-SHARDING.1` — **the shard tool, the manifest, and the freeze check**
  Status: `done`
  Goal: `scripts/shard_history.py` + `docs/changelog/` + a tracked freeze/completeness check,
    demonstrated against the real `CHANGELOG.md` (which shards the moment this lands)
  Design (recorded before code, `2026-09-27`):
  - `scripts/shard_history.py` moves the OLDEST whole entries (`^## ` blocks) from the head to a
    new `docs/changelog/shard-NNNN.md` until the head is under a byte target (default: the
    ceiling the routes registry declares for the head; `--max-bytes` may target lower to leave
    room for an imminent entry). Entries keep their byte text verbatim — a file is preamble +
    concatenated entry blocks, so head-after + shard = head-before exactly, which the tool
    asserts and prints as an ordered entry-id proof at shard time. A re-run is a no-op: under
    target, manifest current, nothing written.
  - Shard naming: sequential `shard-NNNN.md`, continuing past the two existing date-named
    shards, which stay as they are — a shard's entries are never edited, and the manifest
    enumerates shards, so a name is a label, not structure. The shard header follows the house
    header the two existing shards already carry.
  - `docs/changelog/SHARDS.sha256` is the freeze proof: one `sha256sum`-format row per shard,
    paths repo-root-relative, sorted. The tool regenerates it deterministically (byte-identical
    when nothing changed).
  - `scripts/check_changelog_shards.sh` (doctrine `SHARD-FREEZE`) proves, durable past the
    shard event: every `*.md` in `docs/changelog/` is manifested and every manifested file
    exists (coverage); every shard hashes to its row (frozen — any post-shard edit fails);
    the manifest only grows — every row committed at `HEAD` is present unchanged (append-only,
    judged against `git show HEAD:…`); and no entry id appears twice across head + shards
    (none duplicated). "None lost" durably = a shard cannot be edited or deleted without a hash
    failure, and the tool proves completeness at the shard event itself.
  - Registering the doctrine moves two derived counts (`LIVE_STATUS.md`'s "N registered",
    "N self-test arms") — `DERIVED-COUNTS` re-derives both, so the lockstep updates are
    mandatory, not courtesy.
  Acceptance: as the tree's Acceptance Criteria 1–4; the check's RED arms fired before
    registration; after sharding, the head is under 65,536 bytes and every pre-shard entry
    is findable in exactly one place.
  Verification: `2026-09-27` — see the checklist below; shard tool 10/10, freeze check 12/0,
    real-tree RED pre-registration (both existing shards UNMANIFESTED), shard event proved
    29 == 28+1 order-and-bytes exact, head 65,527 → 62,086 bytes, full enforcer green.
  Commit: `SEMULITH-DS-0002`
  DEV_NOTES lesson (`2026-09-27`): promotion: declined (per-slice history; a card is due when a second append-history surface fires).

## Defects found during this leaf (owned)

- `SEMILITH` vs `SEMULITH` in work-unit ids: `git log --format='%s' | grep -oE 'SEM[UI]LITH' |
  sort | uniq -c` measures 60 × `SEMULITH` against 3 × `SEMILITH`, and the three are the most
  recent commits (`SEMILITH-SF-0057`, `SEMULITH-RM-0060`, `SEMILITH-DS-0001`) — a typo introduced
  one session ago and carried into their `CHANGELOG.md` headings and tree commit-logs. Commit
  subjects are immutable; the changelog entries quote them accurately, so history stays as
  written (append_history is never rewritten to match today). Disposition: new ids use
  `SEMULITH` (this leaf's `SEMULITH-DS-0002` does); the recurrence remedy is a `commit-msg` hook
  arm refusing `^SEMILITH` subjects, scheduled to the next hygiene slice — a mechanical check is
  the only durable spelling teacher. Owner: repo-local guarantor.

## Acceptance Checklist (leaf DOC-SHARDING.1)

- [x] **REPRODUCE / ISSUE** — the problem, shown (not asserted):

  ```
  $ wc -c CHANGELOG.md
    65527 CHANGELOG.md                    # 9 bytes under the 65,536 registry ceiling
  $ ls scripts/shard_history.py 2>&1
    ls: scripts/shard_history.py: No such file or directory
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — the adoption debt was data, not prose: the remedy was
  named in two governed places while its tool existed in neither —

  ```
  $ ls scripts/shard_history.py          # before this slice
  ls: scripts/shard_history.py: No such file or directory
  $ git log --oneline -2
  722d1a6 SEMILITH-DS-0001 (tree DOC-SHARDING): the fired ceiling trigger gets its owner
  b1c3d2b SEMILITH-RM-0060 (leaf PORT-WEB.1 proposal): the browser becomes a first-class target
  ```

  `doctrine/readme_routes.tsv` owns `CHANGELOG.md`'s ceiling with *"git history is canonical;
  shard when the ceiling fires"*; `README_POLICY.md`'s transition note records the sharding tool
  as not-yet-existing debt. `SEMILITH-RM-0060` — the commit above — had already compressed its
  changelog entry to fit the 9 remaining bytes: the trigger had fired, and the only responses
  available were compression or the remedy.

- [x] **FIX** — `scripts/shard_history.py` (sharder: whole `## ` entries, byte-verbatim,
  completeness asserted and printed at the event; deterministic; re-run is a no-op),
  `docs/changelog/SHARDS.sha256` (freeze manifest, sha256sum format, repo-root-relative paths,
  regenerated deterministically), `scripts/check_changelog_shards.sh` (doctrine `SHARD-FREEZE`,
  12 arms), registered in `scripts/check_doctrines.project.sh` and mirrored in
  `DOCTRINE_ENFORCEMENT.md` + `docs/book/src/working/doctrines.md` in the same commit.

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  ```
  $ python3 scripts/shard_history.py --max-bytes 63488
    sharded 1 entr(ies) 'SEMILITH-P0-0031 …' into docs/changelog/shard-0001.md
    completeness: 29 entries before == 28 kept + 1 moved, order and bytes exact
    head: 65527 -> 62086 bytes (target 63488)
    manifest: 3 shard row(s) written to docs/changelog/SHARDS.sha256
  $ bash scripts/check_changelog_shards.sh
    SHARD-FREEZE: ok (3 shard row(s) frozen, append-only, exactly partitioned)
  $ python3 scripts/shard_history.py --max-bytes 63488   # re-run
    no shard needed: CHANGELOG.md is 62086 bytes, target 63488
  $ sha256sum -c docs/changelog/SHARDS.sha256            # independent of our tooling
    docs/changelog/2026-09-p0-to-mirror.md: OK
    docs/changelog/2026-09-pre-p0.md: OK
    docs/changelog/shard-0001.md: OK
  ```

  ⛔ Fired RED on the real tree before registration — the adoption state itself:
  `UNMANIFESTED docs/changelog/2026-09-p0-to-mirror.md` + `UNMANIFESTED 2026-09-pre-p0.md`, rc=1.
  ⛔ Independent byte partition check: `git diff CHANGELOG.md` removes exactly the
  `## SEMILITH-P0-0031` block; `tail docs/changelog/shard-0001.md` holds that block's final
  bytes; the 47 removed lines + 3,688-byte shard body reconcile with the head's 3,441-byte drop
  (header + block). 12 self-test arms (`--self-test: 12 pass / 0 fail`), each RED arm asserting
  its reason.

- [x] **NO REGRESSION** — `make gate` green (13 universal + 13 project doctrines incl. the new
  `SHARD-FREEZE`); `shard_history.py --self-test` 10/0; the ROUTES-CLOSURE health line for
  `CHANGELOG.md` reports 63,8xx bytes after this entry — under the 65,536 ceiling; routed
  destinations remain 31.

- [x] **LOCKSTEP** — both doctrine mirrors, `LIVE_STATUS.md` (13 registered; 169 self-test arms,
  both re-derived via `check_derived_counts.sh --list`), `README_POLICY.md`'s transition-debt
  note, `MEMORY.md`, `DEV_NOTES.md` (dated entry — the event/freeze proof
  split is recorded here and in the CHANGELOG entry, and no second instance of the trap exists
  to retrieve by question yet; the card is due the day a second append-history surface fires),
  `TOOLBOX.md` (two rows), `CHANGELOG.md` (this commit's entry), and `docs/TASK_TREE.md` in the
  same commit.
