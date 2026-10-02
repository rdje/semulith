# DOC-SHARDING: shard the append-history surfaces when their ceilings fire

## Metadata

- Tree ID: `DOC-SHARDING`
- Status: `done` (reopened `2026-09-28` for `.2` — the `DEV_NOTES.md` trigger; `.2` landed the
  same day; the family now serves both append heads)
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
| — | — | — | `.2` done (`2026-09-28`); both append heads shard into `docs/changelog/` under one frozen manifest — the next cleanup is time-triggered, as ARTIFACT-CLEANUP's is |

## Task Tree

- ID: `DOC-SHARDING`
  Status: `done`
  Goal: the fired ceiling trigger gets its remedy — frozen shards, a manifest, a check
  Children: `DOC-SHARDING.1` (done), `DOC-SHARDING.2` (done)

- ID: `DOC-SHARDING.2` — **the DEV_NOTES shard path**
  Status: `done`
  Goal: `DEV_NOTES.md` gets the same lifecycle `CHANGELOG.md` has: when its ceiling fires, its
    oldest dated entries move to frozen shards under a repository-relative directory with their
    own manifest, and a tracked check proves frozen + exactly-partitioned.
  Trigger (measured `2026-09-28`, leaf `P1-LAB.6`): `DEV_NOTES.md` at 49,145 of its 49,152-byte
    registry ceiling after its entry was compressed to fit — the same fired-trigger shape
    `.1` records for `CHANGELOG.md` (9 bytes then, 7 now). Compression is the response the
    registry names as the inferior one.
  Result: met, `2026-09-28`. Generalization, not a fork: `scripts/shard_history.py` takes each
    head's ceiling from the registry row and writes a shard header naming the head it was cut
    from and that head's own ceiling — `# DEV_NOTES shard … crossed its 48 KiB ceiling` — while
    CHANGELOG's header stays byte-identical to `.1`'s shape (self-test arm). The shard family
    stays ONE: `docs/changelog/` already carried the registry row for both heads (file-count
    ceiling raised for exactly this at `SEMILITH-PL-0001`), so no second directory was created
    or registered. `scripts/check_changelog_shards.sh` learns the two-head family: one COVERAGE/
    FROZEN/APPEND-ONLY scan over the shared manifest, and the UNIQUE leg scans both live heads +
    shards, so an entry heading carried twice anywhere fails. First event: 2 entries moved to
    `docs/changelog/shard-0027.md`, head 48,954 → 46,212 bytes, `31 == 29 kept + 2 moved`
    proved at the event, manifest 28 → 29 rows. Both tools fired RED on the real tree
    pre-commit (probe record below); self-tests 12/0 and 14/0.
  Commit: `SEMILITH-DS-0003`

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

## Defects found during `.2` (owned, fixed in the same commit)

- The registry comment on the `docs/changelog/` row claimed both heads were "sharded from
  `2026-09-27`" — DEV_NOTES.md had no shards (this leaf was still pending; the head stood at
  49,145 of 49,152 bytes). Designed end-state stated as present fact; corrected in
  `doctrine/readme_routes.tsv` with the fix cited.
- Two stray duplicate headings inside `DEV_NOTES.md` (a heading line repeated with no body
  above the MODEL-COMPOSE.3 and SOT-FORMAT.6 entries) — found by the new two-head UNIQUE leg
  on its first run; the old leg never scanned DEV_NOTES.md. Both removed; each entry exists
  exactly once. Disposition: the UNIQUE leg stays strict (intra-head duplication is a real
  defect class), the corpus is clean.

## Changelog

- `2026-10-02`: Time-triggered shard event (`SEMULITH-DS-0004`): both heads fired within
  hours of each other — `CHANGELOG.md` at 65,035 of 65,536 bytes and `DEV_NOTES.md` at
  49,000 of 49,152 with the next slice's entries measured larger than the remaining room.
  CHANGELOG: 2 entries → `shard-0113.md` (`54 == 52 + 2` exact; head → 62,570). DEV_NOTES:
  3 entries → `shard-0114.md` (`35 == 32 + 3` exact; head → 45,633). Manifest 114 → 116
  rows. The tool did what it was built for; no tree change needed.
- `2026-10-02`: Second event the same day, riding the triggering slice (`SEMULITH-BA-0001`,
  the DS-0002 precedent — the slice's own entry was what crossed the ceiling): 2 entries →
  `shard-0115.md` (`55 == 53 + 2` exact; head 65,870 → 63,128). Manifest 116 → 117 rows.
- `2026-10-02`: Third event the same day, again riding the triggering slice
  (`SEMULITH-PKG-0017` — its entry crossed the ceiling): 4 entries → `shard-0118.md`
  (`54 == 50 + 4` exact; head 66,011 → 61,104, `--max-bytes 62000` for headroom). Manifest
  117 → 120 rows.
- `2026-10-02`: Fourth event the same day, riding the triggering slice (`SEMULITH-P5-0007`
  — its DEV_NOTES entry crossed that head's ceiling): 4 entries → `shard-0119.md`
  (`34 == 30 + 4` exact; head 51,536 → 46,495, `--max-bytes 47104`). Manifest 120 → 121
  rows.

## Acceptance Checklist (leaf DOC-SHARDING.2)

- [x] **REPRODUCE / ISSUE** — the fired trigger, measured:

  ```
  $ wc -c DEV_NOTES.md
  49145 DEV_NOTES.md                     # 7 bytes under the 49,152 registry ceiling
  $ python3 scripts/shard_history.py --head DEV_NOTES.md --max-bytes 47104 --dry-run
  (works — the paths were parameterized — but the shard header it would write names CHANGELOG)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — the shard header was hardcoded to CHANGELOG's identity
  (`# CHANGELOG shard … 64 KiB`), and the freeze check hardcoded CHANGELOG as the only live
  head. WHERE, measured — the old tool run against a DEV_NOTES fixture writes a provenance-lie
  header (rc=0, RED probe recorded):

  ```
  $ python3 old_shard_history.py --root "$PWD" --head DEV_NOTES.md --max-bytes 70
  sharded 1 entr(ies) '_(2026-09-27)_ — old note (X.1)' … into docs/changelog/shard-0001.md
  $ head -1 docs/changelog/shard-0001.md
  # CHANGELOG shard — _(2026-09-27)_ …            # a DEV_NOTES shard claiming CHANGELOG provenance
  ```

- [x] **FIX** — generalize both tools (no fork): `shard_history.py` derives the header from the
  head's registry row (head stem + ceiling KiB; CHANGELOG's emission stays byte-identical to
  `.1`, asserted by a self-test arm); `check_changelog_shards.sh` takes the live heads as
  arguments, scans the shared partition once, and fires its UNIQUE leg across both heads +
  shards. The shard family stays one: `docs/changelog/` already carried the two-head registry
  row (file-count ceiling raised for it at `SEMILITH-PL-0001`), so no new directory was needed.

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  ```
  $ python3 scripts/shard_history.py --head DEV_NOTES.md --max-bytes 47104
  sharded 2 entr(ies) '_(2026-09-14)_ — a category the layer does not own is not "missing"' … into docs/changelog/shard-0027.md
  completeness: 31 entries before == 29 kept + 2 moved, order and bytes exact
  head: 48954 -> 46212 bytes (target 47104)
  manifest: 29 shard row(s) written to docs/changelog/SHARDS.sha256
  $ python3 scripts/shard_history.py --head DEV_NOTES.md --max-bytes 47104   # re-run
  no shard needed: DEV_NOTES.md is 46212 bytes, target 47104
  $ bash scripts/check_changelog_shards.sh
  SHARD-FREEZE: ok (29 shard row(s) frozen, 2 heads + shards append-only, exactly partitioned)
  $ bash scripts/check_changelog_shards.sh --self-test
  SHARD-FREEZE --self-test: 14 pass / 0 fail          # was 12; two new arms
  $ python3 scripts/shard_history.py --self-test
  shard_history --self-test: 12 pass / 0 fail         # was 10; two new arms
  ```

  ⛔ Real-tree RED probes before the tools were trusted with the head: the check flagged a
  scratch shard carrying a live DEV_NOTES heading (`DUPLICATED ENTRY … shard-0099-probe.md`,
  rc=1); the old sharder wrote a CHANGELOG-provenanced DEV_NOTES shard (probe above). Both
  probes cleaned up after capture; the check then exposed the two stray duplicate headings in
  DEV_NOTES.md itself (defects section above).

- [x] **NO REGRESSION** — the full enforcer with both mirrors updated:
  `make gate` → `=== all doctrines green ===` (SHARD-FREEZE green on the real 29-row
  partition; REGISTRY-MIRROR green across `DOCTRINE_ENFORCEMENT.md` and the book chapter);
  CHANGELOG's re-shard path keeps `.1`'s header shape (self-test arm).

- [x] **LOCKSTEP** — `DEV_NOTES.md` (sharded head + this slice's dated entry), `CHANGELOG.md`
  (entry), `MEMORY.md`, `LIVE_STATUS.md` (self-test arm count re-derived), `docs/TASK_TREE.md`
  (tree closed), the doctrine mirrors (`DOCTRINE_ENFORCEMENT.md` + `docs/book/src/working/
  doctrines.md`), `doctrine/readme_routes.tsv` (false two-heads claim corrected), and this tree
  — one commit. No new doctrine registered (SHARD-FREEZE extended in place); the routed-
  destination count is unchanged (no new directory).

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
