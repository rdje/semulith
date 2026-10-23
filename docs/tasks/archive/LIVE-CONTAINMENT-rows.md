# LIVE-CONTAINMENT ordinary history — closed rows

Ordinary, directly readable task history: the acceptance-checklist, verification and commit rows of
the tree's closed slices, retained verbatim from `docs/tasks/LIVE-CONTAINMENT.md` at commit
`11dae86f6781b33f114d15a04f4ab161454cfb0d` (four contiguous spans, in source order, one anchor each). The live tree keeps
each section heading with one pointer; the slice records stay in the live tree and the earlier
archive parts. Relative links inside the retained rows are written from `docs/tasks/`, their original
base. No seal, reader or inverse map is involved: moving closed rows verbatim into an ordinary archive
part is the task family's standing mechanism (decision_containment-reset, 2026-10-21); `.4o`,
SEMULITH-LC-0054.

| Span | Bytes | SHA256 |
| --- | --- | --- |
| Acceptance Checklist (LC0027 task-source repair — LIVE-CONTAINMENT.4i2b2b) | 153 | `4eafaa0d3dcfec27161e35772a4b4420e62498b8a27245c57b8569cbf363b773` |
| Acceptance Checklist (required for any leaf that lands a CODE change) | 16695 | `6b43dcc1ff40d513dd3f4764bdf7ebcdc276503767c33187611edcbac0c1f219` |
| Verification Log | 18547 | `95b491e1e399be86a7fe45f8a90e0fe26941e4f756babcaac010379621dff82a` |
| Commit Log | 7212 | `32863f7a568ee68da259d8d0542a2163a05406d3552722f61962a3647d3cfd38` |

From the repository root:

```sh
cat docs/tasks/archive/LIVE-CONTAINMENT-rows.md
```

<a id="acceptance-lc0027"></a>

## acceptance-lc0027

Closed record: [complete original record](archive/LIVE-CONTAINMENT-readers.md#acceptance-checklist-lc0027-task-source-repair--live-containment4i2b2b).

<a id="acceptance-rows"></a>

## acceptance-rows

- [x] .4m **ROOT CAUSE** — `bash scripts/check_readme_routes.sh` rc=1 with this record and the archive part staged under the old row: OVER CEILING docs/tasks/: 3,148,764 aggregate bytes > 3145728; `git ls-files docs/tasks | xargs cat | wc -c` = 3,148,764; the cap, not a defect, blocked every unit (2,430 B of room at 2634e94, ~3.5 KB per unit).
- [x] .4m **ADDRESSED** — the same check rc=0 under the rows ruled on 2026-10-21 (tasks 0 / 0 / 131072; book and models all 0): no OVER CEILING at 3,148,757 B; moved span 10,610 B SHA256 69e7147006e14f52e6a6f688d73d2862cea78d3f1c410ec88d1a13cb6c6941bf; live tree 130,154 → 124,038 B.
- [x] .4m **NO REGRESSION** — `bash scripts/check_readme_routes.sh --self-test` 94 pass / 0 fail; focused checks rc=0 (memory-arch, routes, mirror, claims, derived counts, frontier, book index, history, knowledge map, currency, docpaths, seams, lessons, routing, gaps, waivers, source format, unit books, gate report, requirements; shards, acceptance, arity staged); seven books.
- [x] .4m **LOCKSTEP** — registry rows + comment blocks, decision record + INDEX row, COMMIT/DOCTRINE_ENFORCEMENT/TASK_TREE_README wording, local adoption note, book chapter (ruling, archive list, decision count), MEMORY, CHANGELOG + DEV_NOTES sharded and one entry each, KNOWLEDGE_MAP regenerated; no terminal, reader, seal or code changed; CPU/P4/P5 milestones unchanged.
- [x] .4l **ROOT CAUSE** — `bash scripts/check_readme_routes.sh` rc=1 with the continuation staged under the old row: OVER CEILING docs/tasks/: 108 files > 107; census 33+1+42+31 = 107 unchanged since 2026-10-12, three members ≥ 130,889 B of 131,072.
- [x] .4l **ADDRESSED** — the same check rc=0 with the row re-derived (108 of 116 files, 3,134,069 B of 3,145,728); retain.py/verify.py rc=0: 2 spans / 3,281 B exact source/owner/retired inverses, both pointer anchors resolve.
- [x] .4l **NO REGRESSION** — `bash scripts/check_readme_routes.sh --self-test` 94 pass / 0 fail; focused checks rc=0 (memory-arch, routes, derived counts 44/40/1643, frontier, claims, history, knowledge map, currency, docpaths, seams, arity, shards, acceptance); seven books.
- [x] .4l **LOCKSTEP** — registry comment + row, decision record + INDEX row, KNOWLEDGE_MAP, book count 61, tree/MEM/DEV/CH; no terminal, reader, byte cap or code changed; CPU/P4/P5 milestones unchanged.
- [x] .4k **ROOT CAUSE** — `bash scripts/check_readme_routes.sh` rc=1 with the record's index row and the old row: OVER CEILING docs/decisions/: 262287 aggregate bytes > 262144; status census 55 active/1 fulfilled/2 superseded-in-part, 26 records 10-02..12 then none.
- [x] .4k **ADDRESSED** — the same check rc=0 with the row re-derived (62 files / 265,307 B under 160 / 524,288; health 64 / 278,528): no decisions warning; `git ls-files docs/decisions | xargs cat | wc -c` = 265307.
- [x] .4k **NO REGRESSION** — `bash scripts/check_readme_routes.sh --self-test` 94 pass / 0 fail; focused checks rc=0 (memory-arch, routes, derived counts 44/40/1643, frontier, claims, history, knowledge map, currency, docpaths, seams, arity, shards, acceptance); seven books.
- [x] .4k **LOCKSTEP** — registry comment block + row, decision record + INDEX row, KNOWLEDGE_MAP regenerated, book count 60, tree/MEM/DEV/CH; no other cap, terminal, reader or code changed; CPU/P4/P5 milestones unchanged.
- [x] .4j: [complete acceptance](artifacts/live-containment/task-claims-2.md#lc0051-4j-acceptance).
`LIVE-CONTAINMENT.4` slice (e), `SEMULITH-LC-0008`:

- [x] **ROOT CAUSE** — `git show 1146d1b:docs/book/src/working/task-trees.md`
  rc=0 shows only a code-formatted reference path for temporary controls; no
  mode matrix or runnable examples reaches the book-only review surface.
- [x] **ADDRESSED** — source/render verification rc=0: LOCALITY-BOOK: complete
  reference/book inverses exact; five rendered examples and first/last limits present.
  The anchored live include keeps the detailed matrix and limits in their owner.
- [x] **NO REGRESSION** — `make book` rc=0: seven books build. Focused8 rc=0; LOCALITY-BOOK-SCOPE:1269 tracked files unchanged
  rc=0. No code/runtime/
  profile/archive/cap/LIVE change. Earlier reference bytes are all retained.
  promotion: declined (the canonical reference and direct book include are sufficient).

`LIVE-CONTAINMENT.4` slice (d), `SEMULITH-LC-0007`:

- [x] **ROOT CAUSE** — `python3 scripts/probe_temporary_locality.py --mode shell
  --revision f699474` rc=1: TMP-LOCALITY:44/56 shell sites qualified and cleaned;
  Python predecessor0/2 and synth parent control also RED1. Published acceptance
  probes9pass/1fail at CTRL-4b; scoped git log/blame pins generic signature d8c2337.
- [x] **ADDRESSED** — locality modes shell/python/children/parent rc=0:
  TMP-LOCALITY:56/56 shell,2/2 Python,28 child environments and fresh synth parent
  pass. Four named negative modes each rc=1 before a foreign allocation or after
  observing controlled residue. Materials20/0 and comparator4/0 clean all fixtures.
- [x] **NO REGRESSION** — `make ci` rc=0, all five legs, Rust173/17/253,
  seven books; focused11 rc=0, SEAM-INTEGRITY19/0,
  archive46/0, acceptance10/0, waiver5/0, synth6/0. Scope verifier rc=0 preserves
  canonical/runtime/profile/frozen/fixtures/earlier history and archive pins.
- [x] **LOCKSTEP** — `bash scripts/check_derived_counts.sh --list` rc=0 derives
 39doctrines/728arms/38routes/49main chapters/0open upstream issues. Reference,
  doctrine/toolbox/INDEX/map, live docs and task-history book explain the exact
  finite control scope; all earlier caps remain. CPU/P4/P5 milestones unchanged.
  promotion: reference_temporary-allocation-controls.md owns the durable controls.

`LIVE-CONTAINMENT.4` slice (c), `SEMULITH-LC-0006` (approved2026-10-10):

- [x] **ROOT CAUSE** — `git ls-tree -r -l 63ae063 -- docs/tasks/` census, rc=0:
  TASK-HISTORY-CENSUS: 89files/3,145,703B, only25B under3,145,728. Closed historical narratives add a
  scaling term; another split does not reduce the aggregate. The director approved
  the reviewed12-file finite capture and changed browsing before migration.
- [x] **FIX** — exact tracked375029B object plus immutable967B descriptor; bounded
  standard-library reader authenticates all13members before stdout.12 exact stubs
  retain paths/eight anchors; TASK-HISTORY checks identities, predecessor, navigation,
  incoming anchors and absence of live narrative includes unconditionally. No cap grows.
- [x] **ADDRESSED** — `python3` capture/migrate/verify.py rc=0: all12originals
  equal Git47cb436 and review pins;1,144,703B/15,055lines remain retrievable.
  Stubs7,040B release1,137,663B. All27external reference records preserved;
  permanent links checker rc=0 validates16links including archived cross-links.
  The checked reproduction recipe rebuilds exactly the reviewed archive after retirement.
- [x] **NO REGRESSION** — `bash scripts/check_task_history.sh --self-test`
  46pass/0fail; all12Python/tar reads exact in relocated no-Git fixture with no
  extraction or writes. Corrupt valid-path reads emit no stdout; malformed metadata,
  unsafe/duplicate/extra/missing/oversized members, changed pins/stubs/links refuse.
  Focused15 and `make ci` rc=0 (Rust173/17/253, all doctrines, bench, smoke, seven books).
  Full predecessor inverses and unchanged canonical/runtime/frozen/fixtures/earlier
  history proof rc=0; active P4 graph and profile ENVIRONMENT exact.
- [x] **LOCKSTEP** — live docs, decision approval/recipe, terminal, routing and
  doctrine/toolbox mirrors, book/history navigation/index updated. Complete old
  book retrieval section moved verbatim (SHAac1fe971d0c567c86b3a63a22b845c9c284cfb223c0e38b2196b8dbf88372759).
  Derived counts39doctrines/718arms/38routes; CPU/P4/P5 milestones unchanged.
  Evidence: target/live-containment/task-history-seal. Full .4 adoption remains open.
  promotion: declined (the finite decision, checked reader and46 controls encode this transition).


`LIVE-CONTAINMENT.4` slice (a) — approved finite archive (`2026-10-08`, `SEMULITH-LC-0004`):

- [x] **ROOT CAUSE** — Python census: live archive 212 files / 784318 B, 2114 B
  headroom; CHANGELOG 65528 B and next whole record 2377 B. Sharding scales the
  aggregate indefinitely. Director approved the concrete tracked terminal before code.
  Earlier e1c0 archive cap failed at 787026 B. `rg -n mktemp
  scripts/check_changelog_shards.sh` also found a standalone off-volume temporary.
- [x] **FIX** — seal exact ff75610 capture, retain original manifest; bounded strict
  descriptor and content-addressed object own full-source counts/digests. Read/check
  authenticates all members without Git or extraction. Freeze gate authenticates the
  live/archive logical union, immutable predecessor descriptors and heading/location
  uniqueness. Sharder preserves retired names; gate comparison files use target/.
  Retire only exact copied duplicates after verification. Register one finite terminal
  with count 3 / bytes 304980 derived from immutable object plus bounded metadata.
  Existing ceilings unchanged; full doctrine/inventory adoption remains open in .4.
- [x] **ADDRESSED (verified)** — Python copy/verify: 210 original shards plus manifest,
  211 members / 781740 source B / 9639 lines; every source equals its captured Git blob
  and digest, archive digest 4cbc226272062441fa50998df217db74f7f2a069de54690f5a9dec9e107e4be7.
  Post-retirement residue: zero retired files, recent 0209 retained. Reader rc=0:
  HISTORY-ARCHIVE ok (one object, 210 authenticated shards). Freeze rc=0: 213 logical
  rows after two new ordinary cuts. docs/changelog: four files / 8039 B; terminal:
  three files / 287216 B. Self-test 31 pass / 0 fail (old 14 + GREEN/sixteen RED).
  Controlled no-Git fixture retrieves exact bytes and predecessor row, preserves
  retired number 0042→0043, and corruption/path/bounds/schema/duplicates refuse.
- [x] **NO REGRESSION** — sharder self-test 12 pass / 0 fail; all earlier freeze
  controls retained. New head cuts print completeness: CHANGELOG 69 == 68 kept + one
  moved, 65977→63601 B; DEV_NOTES 32 == 31 kept + one moved, 49408→46983 B, order/bytes
  exact. Full logical predecessor digest proof includes all 211 pre-transition rows.
  No Rust, profile or expectation changes. CI-RECOVERY logs three hosted failures and
  the additional Linux nightly-name defect; local green does not certify hosted CI.
- [x] **LOCKSTEP** — live docs, tree/index, CI ownership tree, book, toolbox/doctrine,
  route registry, tracked terminal/descriptor updated. DERIVED-COUNTS derives 37 routes
  and 599 arms; source capture preserved for independent reconstruction. Tool gates,
  book build and commit gate must be green before closure of this slice.
  promotion: declined (strict descriptor and seventeen archive controls encode the lesson).


`LIVE-CONTAINMENT.1` — the closed-tree register (`2026-10-06`, `SEMULITH-LC-0001`):

- [x] **ROOT CAUSE (WHY + WHERE)** — `grep -n "TASK_TREE" doctrine/readme_routes.tsv` → the
  index's registered control reads "one row per active tree; completed trees leave the
  index", and the census of its anchored table: 31 rows, 22 with status `done` — the control
  was never applied because nothing enforced it: FRONTIER-SYNC's CLOSURE rule required EVERY
  tree file to have an index row (`grep -n "UNLISTED TREE" scripts/check_frontier_sync.sh`),
  so obeying the registry would have failed the gate.

- [x] **ADDRESSED (verified)** —

  ```
  $ bash scripts/check_frontier_sync.sh --self-test → FRONTIER-SYNC --self-test: 20 pass / 0 fail
    (16 → 20: the completed-tree arms now judge the register; + COMPLETED IN INDEX,
    OPEN TREE IN REGISTER, DUPLICATE ROW, NO ANCHORS)
  RED — the new check on the real pre-move index (a worktree at HEAD): 22 × "COMPLETED IN
    INDEX … completed trees leave the index", rc=1
  the move: 31 rows = 9 open + 22 moved; every moved row byte-identical in the register
  $ bash scripts/check_frontier_sync.sh → FRONTIER-SYNC: ok (32 tree(s) …)
  $ wc -c docs/TASK_TREE.md docs/TASK_TREE_CLOSED.md → 4053 / 4861
  ```

- [x] **NO REGRESSION** — README-ROUTING-CLOSURE ok (34 governed destinations); TREE-CLAIMS
  ok; DERIVED-COUNTS re-derived (34 destinations, 449 arms); `make book` rc=0 (both anchors
  render); `make gate` → `=== all doctrines green ===`.

- [x] **FIX** — FRONTIER-SYNC reads the optional `TASK_TREE_CLOSED.md` (anchored), runs every
  check on its rows, CLOSURE over the union, plus the three new breaches; the register created
  and registered; the index's prose, COMMIT.md, TASK_TREE_README.md and the book's task-tree
  chapter (both anchors included live) describe the move; the doctrine mirrors updated.

- [x] **LOCKSTEP** — `docs/TASK_TREE.md` (this tree's row), `MEMORY.md` (active trees),
  `LIVE_STATUS.md` (34 / 449), `CHANGELOG.md`, `DEV_NOTES.md`, `DOCTRINE_ENFORCEMENT.md` +
  the book's doctrine row, `doctrine/readme_routes.tsv` (the row + its derivation comment).

`LIVE-CONTAINMENT.2` — the stale orientation sources (`2026-10-06`, `SEMULITH-LC-0002`):

- [x] **ROOT CAUSE (WHY + WHERE)** — hand-curated orientation text with no derivation:
  `grep -n "crates/app" knowledge-map/subsystems.md` → line 6 ("Still the scaffold's
  placeholder `main.rs`"), while `ls crates/` → semulith-cli semulith-core
  semulith-dsp56300 semulith-verify; `head -2 Cargo.toml` → "Rename/replace the starter `app`
  crate"; `grep -n "16,228" README_POLICY.md` → the adoption note's "no measured pressure"
  (CHANGELOG is 64 KiB and shards; four ceilings fired 2026-10-06). The KNOWLEDGE-MAP gate
  proves the map is the function of its sources — never that the curated source is true.

- [x] **ADDRESSED (verified)** —

  ```
  $ grep -c "crates/app" KNOWLEDGE_MAP.md → 0   (was 1)
  $ grep -n 'Some("' crates/semulith-cli/src/main.rs → check-examples, run, demo, bundle,
    replay, snapshot, resume, reduce, bench — the nine the corrected text names
  $ ls profiles/ → the six units the corrected text names
  ```

- [x] **NO REGRESSION** — `make check` rc=0 (the Cargo.toml edit is comment-only);
  `make gate` → `=== all doctrines green ===` (KNOWLEDGE-MAP regenerated).

- [x] **FIX** — `knowledge-map/subsystems.md` (the crates paragraph rewritten; definitions,
  profiles, schema/materials and the two book families added); `Cargo.toml`'s header;
  `README_POLICY.md`'s adoption-note paragraph (measurements only, routed to `.4`).

- [x] **LOCKSTEP** — `KNOWLEDGE_MAP.md` regenerated; this tree; `docs/TASK_TREE.md`;
  `MEMORY.md`; `CHANGELOG.md`.

`LIVE-CONTAINMENT.3` — TOOLBOX/DOCTRINE_ENFORCEMENT headroom (`2026-10-06`, `SEMULITH-LC-0003`):

- [x] **ROOT CAUSE (WHY + WHERE)** — both are "one row per" normative tables with a fixed
  ceiling and no partition: `wc -c TOOLBOX.md DOCTRINE_ENFORCEMENT.md` → 20,478 / 32,669 of
  20,480 / 32,768 B after `SEMULITH-CA-0001`'s rows were tightened to fit (the guide's named
  anti-pattern); the section census → 19,055 B of TOOLBOX is its tool table, 24,966 B of
  DOCTRINE_ENFORCEMENT its project-doctrine table.

- [x] **ADDRESSED (verified)** —

  ```
  the move census (rows before, from HEAD): doctrine rows 35 each exactly once: True;
    tool rows 76 each exactly once: True  (a FIRST pass found 75 — its row filter keyed on
    a backticked first cell and dropped `| any project check's --self-test |`; a second
    census by table position caught it; the move re-run from HEAD)
  $ wc -c TOOLBOX.md DOCTRINE_ENFORCEMENT.md → ~3.2 KB / ~11 KB
  $ bash scripts/check_registry_mirror.sh --self-test → REGISTRY-MIRROR --self-test: 13 pass / 0 fail
  RED — CITATION-QUOTES' long-form row removed from docs/doctrines/definition.md:
    NOT MIRRORED docs-doctrines-union.md: 'CITATION-QUOTES' is registered and has no row
  $ bash scripts/check_registry_mirror.sh → ok (3 document(s) mirror the registry)
  ```

- [x] **NO REGRESSION** — README-ROUTING-CLOSURE ok (36 governed destinations);
  DERIVED-COUNTS re-derived (36 destinations, 451 arms); `make book` rc=0; `make gate` →
  `=== all doctrines green ===`.

- [x] **FIX** — the two partitions (scratch mover `target/live-containment/partition.py`,
  verbatim, census-checked); REGISTRY-MIRROR's `project:` mirror scope + the union
  invocation + 2 arms; the parents' bounded indexes; "Adding a doctrine" and TOOLBOX's
  add-a-row note point at the families; both families registered with derivation comments.

- [x] **LOCKSTEP** — this tree, `docs/TASK_TREE.md`, `MEMORY.md`, `LIVE_STATUS.md` (36 /
  451), `CHANGELOG.md`, `DEV_NOTES.md`, `doctrine/readme_routes.tsv`.


<a id="verification-log"></a>

## verification-log

LC0051: routes rc=1 RED (108 files > 107) then rc=0 GREEN at 108 of 116 files / 3,134,069 B; retain/verify rc=0 (2 spans, 3,281 B exact); self-test 94 pass / 0 fail; focused rc=0; seven books.
LC0050: routes rc=1 RED (262287 > 262144) then rc=0 GREEN at 62 files / 265,307 B; self-test 94 pass / 0 fail; focused rc=0; seven books.
LC0049: verify.py rc=0 normal/O; source159/782755B, residue0; copy/tar/relocated normal/O, focused17/books7/examples4/surfaces3, history44/query263x2; inverses2/seven refusals.
.4i2b5b2r.d: permanent probe normal/O rc=0:6 actual controls/3 boundary guards;
combined Mark/book denial reproduces whole original failed witness/enhancements.
Record reader normal/O rc=0:960 full witness restorations/7 damaged frames refuse.
Four selected queue5/32 source-before-fixed runs each120+120; final faults only
seven D80 cases. Earlier assembler loses ten assets before HTTP receipt. D79
cause unestablished; scoped lo0 BPF probe denied1/0pcap, TCP counters all0.
verify.py/focused13/sharder12/seven books rc=0:1476 protected regular files/
Gitlink,29198B prefix/5729B closed unit/projected ledger/probes/source/book exact;
21 old headings/55 commands/3242 links/fresh120 headers and fixed caps qualify.
CH1363B→0332/1600B, DEV4660B→0333/4893B whole rollover;95 old entries exact.
Full staged inverse/normal COMMIT required. LIVE1578/39/40/49 unchanged; precise
D79 packet-access owner45 blocked, D80 repair46 pending, search afterward.

.4i2b5b2r: final normal and optimized-alone --require-clean rc=0: source120/1,
current120/0;1408 headings/590 entries/107 inputs, six unit aliases exact. Static
inverse51 script insertions/293 unchanged outputs/new exact asset; supported
main alias and three real omissions discriminate. Seven damaged-frame refusals
normal/O. verify.py/focused13/sharder12/seven books rc=0:1471 protected regular
files/Gitlink,14406B prefix/7063B whole unit/two metadata matrices/book inverses,
21 old headings/54 commands/3242 links and fresh120 header/title parity exact.
CH1361B→0330/1598B and DEV5744B→0331/5977B whole rollover; all97 prior live
entries/manifest prefix/seals/caps exact. D79's concurrent print missing-Mark
refusal remains open;16 traced repeats pass without explaining it. Complete
failed witness/DOM identity retained; HTTP forensic gap owned immediate LC0044.
Full staged inverse/normal COMMIT required. LIVE1578/39/40/49/processor unchanged.

.4i2b5b2: normal/O actual capture rc=0:120 pages/1406 source headers/589 navigation
entries,107 inputs and344 baseline output identities; D78 sole wrong contract.
Four JS/HTTP calibration witnesses and three producer omissions plus fallback
cause control discriminate; strict Swift6/WebKit execution emits no diagnostics.
Public record queries/self-test rc=0 normal/O, nine refusal controls; whole
metadata/book/published-prefix inverses exact. verify.py/focused13/sharder12/
seven books rc=0:1467 protected regular files/Gitlink,98 prior history entries,
20 old headings/all commands/3242 links and fixed caps exact. CH678B→0328/915B,
DEV4592B→0329/4825B whole rollover; published manifest prefix retained. Full
staged inverse/normal COMMIT required. LIVE1578/39/40/49 and CPU unchanged;
LC0043 D78 conditional repair immediately next, preserving six unit aliases.

.4i2b4a: ten whole spans61745B/869LF, nine closed units +LC0027 checklist,
retained in63161B ordinary archive. Ten native headings/routes and old phase
anchor qualify; archived articles unchanged, search resources authenticated.
D71 closure corrected/full965B planning intro retained; D70 seven historical
claims plus correction mention qualified case-insensitively. Whole105 old
live entries/source/order/protected modes/seals remain exact. Focused12/books/
scaffold5/full handoff24 normal/O; normal COMMIT completes the unit.

.4i2b3b2: D65/D68 fixed; public24 bad greens→defect1,16 unsafe2,16 injected
faults2; seven defaults93 expanded chapters/49 edges/344 outputs exact normal/O.
Six actual omissions/mode discriminate; concurrent historical15/16 failures→0/16.
52 aggregate/26 navigation methods,22 shell arms;1571 derived. Retained2180B
whole book receipts;106 old live entries/source/order/protected identities/modes
verified before normal COMMIT. Full graph/adoption/processor acceptance open.

.4i2b3b1 final: component22/old23+26 controls normal/O; seven books93 chapters/
49 includes/all344 output files unchanged.34 public fixtures/eight actual faults,
13 component/four producer copied omissions discriminate normal/O. Tracked
cad73f3 replay exact80700B ledger; D66/D67 fixed, D65 integration next. Whole
reader copy1179B/book+6→524281,107 old entries/1418 protected modes/Gitlink/full
inverses exact. Focused12/books/scaffold24/3242 links/normal+print/literal checks
pass; caps exact. First pending commit interrupted for D67 before HEAD changed;
only restarted normal hooks and final postcheck can complete this unit.

.4i2b3a:1425-source/54-candidate boundary;49 include occurrences/48 targets/
93 full chapter expansions exact,344 output files unchanged normal/O. D65
public interfaces false-green24, valid4; three diagnostic omissions fail1 in
both modes. Whole DEV2490B retained,106 old entries/1418 protected modes/Gitlink
and complete inverses qualify. Focused12/books/seven/3242 links/rendered/literal
pass; no caps, CPU or archive-authority changes. D65 priority1 repair next.

.4i2b2b: D59/D64 repaired; original13/20 controls retained,38/41 normal/O;
12 public cases/mode,11 actual omissions/38 cases and eight real read faults
qualify.105 old entries/1411 protected/Gitlink and full source inverses exact;
focused12/seven books/3242 links/21 Foundation rows/three literal commands and
scaffold24 normal/O pass. Derived1565 arms; other LIVE/caps/CPU unchanged.

.4i2b2h: eleven whole units47486B/684LF retained with11 native anchor links;
1413 protected files/Gitlink/106 old entries and whole source inverses exact.
Focused12/seven books/3242 links/11 literal reads/normal+print pass; normal/O
checks agree. Earlier archives and caps fixed; D59/D64 code repair next.

.4i2b2a: source/D59/D64 qualified, D62/D63 corrected.14 controls/12 public
cases per mode;106 old entries/1406 protected/Gitlink exact. Focused12/seven
books/3242 links/rendered/literal pass; .4i2b2h containment next.

.4i2b1: D58 live composition Done/6 of6; D60 same-total arm13, old12 exact;
seven public cases/mode and copied omission0→2 normal/O. D61 two table joins,
all21 actual normal/print Foundation rows;3244 links and literal13-control
example pass.106 old history entries,1404 protected files/Gitlink and complete
source/book/task/guard/doctrine/live/history inverses exact normal/O;
focused12/sharder12/seven books pass. D59 source/ratio qualification priority1
next; other milestones/caps/canonical/CPU unchanged. Normal COMMIT required.

.4i2a: complete source1411/462 Markdown/53 literal include candidates; retained
seven-book120 HTML pages/3244 hyperlinks,2076 resource candidates and338 paths
outside book source directories. Source versus working rendering explicit;
22 finite refusals normal/O. Full independent source/program/state/output/
protected/history inverses, focused/seven-book/rendered and normal COMMIT
required; focused12/sharder12/seven books/3244 links and five reads pass.
No final graph/adoption claim; .4i2b transitive reader review next.

.4i1: immutable source1408/39 declarations and12 durable input refusals normal/O.
Local contract separates source membership from pending semantic graph coverage,
utility/lifecycle/fields/debt and checker integration. Whole-history/source/
protected inverses, focused12/seven books/rendered/five literal reads and normal
COMMIT required; focused12/sharder12/seven books/3244 links and five reads pass. Existing caps, count107/health64 debt, canonical/profile/CPU
and sealed histories remain exact; .4i2 complete graph inventory follows.

.4h6c4: task-capacity-application check-evidence/verify/history/rendered normal/O
and focused.sh rc=0. Fresh same33 IDs/typed96, exact separate authority and two
precondition refusals; count96→107 only plus dated pointer. Original107 breach1
becomes0; new108 breach1 and65 advisory0. Public normal/O green0/39 routes,
health64 debt; enclosing1407 states and guard94 byte-exact. Whole DEV4026B→0290
preserves104 prior entries; protected/Gitlink/canonical/ordinary/seals exact.
Focused12/sharder12/seven books/full normal+print/four reads and normal COMMIT
required; LIVE/CPU unchanged. .4i full inventory/checker adoption is next.

.4h6c3: task-capacity-review assess/review/verify/history/rendered normal/O and
focused.sh rc=0. Typed27/1/9/24→33/1/40/22, six creation/scopes, four typed/two
metadata refusals; real1405 snapshots exact. Separate107 authority; health64
debt and every registry limit unchanged. Three book-intro clauses compared;
D51/D55 facts and four literal reads/full normal+print remain. Whole CH rollover
retains105 prior entries; protected identities/Gitlink/canonical/seals exact.
Focused12/sharder12/seven books and normal COMMIT required; .4h6c4 applies next.

.4h6c2: registry-repair check-before/check-after/source-inverse/verify/history/
rendered normal/O and focused.sh rc=0. D56 primary faults2/no stdout; removed
seven consumers absent; D57 five malformed fixtures0→2. Public18 per mode,
real1404/pinned programs exact;94 controls,17 omissions/all26 discriminators.
Original68 byte-exact. Whole DEV rollover preserves104 old entries; caps,
canonical/history/seals/CPU exact. Focused12/sharder12/seven books/full normal+
print/three literal reads, handoff probe24/0 normal/O, staged acceptance/seam
and normal hooks required. LIVE routing Done/1518arms; .4h6c3 authority next.

.4h6c1: registry-projections check-evidence/verify/history/rendered normal/O and
focused.sh rc=0: seven actual consumers/14 fault cases green0, single traced
injections and healthy delegates; all raw streams/pins and per-run real1402
identities exact. Whole source/head inverses retain105 prior entries/1393
protected files/Gitlink; DEV3990B→0286/CH1330B→0287; frozen/canonical/caps exact.
Focused12/sharder12/seven books/full normal+print/three literal reads pass.
LIVE routing Mostly Done/D56 priority1 repair .4h6c2 next; CPU unchanged.

.4h6b: five-unit-correction assess/verify/history/rendered normal/O and focused.sh
rc=0: four closed inventories, complete profile deltas and original authority
pins; two wrong-count controls refuse; real1402 identities exact. Whole source/
head inverses,103 prior entries/1394 protected files/Gitlink and all ceilings/
manifest/seals exact. Focused12/sharder12/seven books, full normal+print/three
literal reads pass. D55 fixed; LIVE/CPU unchanged. .4h6c capacity review next.

.4h6a: capacity-navigation verify/history/rendered normal/O and focused.sh rc=0:
nine complete sources/27 clauses; index15526→13122B, free2674B. Whole source/
head/book/task inverses retain104 prior entries; receipt/digest refusals,
protected identities, focused12/sharder12/seven books and literal reads pass.
DEV3668B→0284/CH1417B→0285; all prior archives/seals/caps/LIVE/CPU exact.
D55 diagnosed/owned .4h6b next; separate capacity review .4h6c follows COMMIT.

.4h5: assess.py/verify.py normal/O rc=0: typed source inventories27/1/9/24
and33/1/40/22, six added instances/no removals, two metadata negatives refuse;
real HEAD/index/all1400 identities exact. Whole authority/registry/index/book/
task/head inverses retain original receipt and102 old head entries; protected
bytes/modes/Gitlink, manifests/seals and ceilings exact. Focused12/sharder12/
seven books, full normal+print teaching and two literal reads pass. D51 fixed;
LIVE/CPU unchanged. .4h6 separate capacity review follows COMMIT.

.4h4: final public normal/O replay baseline0; all injected unavailable
file/parser/hint/README/date reads refuse2 without green/stdout. Removed derived
wc/sort consumers receive zero injections. All1398 real tracked identities,
HEAD/index and pinned programs/facades exact. Original32+36 controls68/0;
14 omissions detected normal/O. Handoff24/0/0; old updater5/2/0 normal/O.
Whole source/history/protected-byte/mode inverses,101 prior entries, DEV3021B→
0283/3254B whole rollover and manifest prefix/seals exact. Focused12/sharder12/
seven books, full normal+print teaching and two literal examples pass. D53/D54
fixed; LIVE1492 arms/routing Done, caps/CPU unchanged; D51 .4h5 next.

.4h3: assess.py normal/O rc=0: baseline0; failed73 and partial+stderr
refuse2 without green/stdout; one family listing, all1397 real identities exact.
Permanent32/0 normal/O; nine omission variants refuse normal/O. Complete
checker/book/task/head inverses,101 prior entries,1383 protected regular files/
Gitlink and fixed limits exact. Focused12/sharder12/seven books/3242 links,
normal+print/two literal examples pass; D52 fixed. CH1382B→0282/1619B whole
rollover, manifest prefix exact,74live+210sealed284logical. LIVE routing closure
Done/derived1456 arms; no CPU qualification change. D51 .4h4 next.

.4h2: assess.py rc=0: baseline0/empty stderr; failed73 and partial+stderr
both falsely green0, three scoped listings each. Real HEAD/index/all1397
tracked identities exact. verify.py normal/O: complete book/task/LIVE/head
inverses,99 prior entries and1390 protected regular files/Gitlink exact.
Focused12/sharder12/seven books/3240 fresh+actual links; whole normal+print
teaching and literal checker command pass normal/O. D52 owned priority1,
repair next; LIVE routing closure Mostly Done, other status/caps/CPU unchanged.

.4h1: verify/history/rendered normal/O and focused.sh rc=0: five canonical
identities/15 source clauses, whole index/book/task/head inverses,101 old entries,
1387 protected files/Gitlink and fixed caps exact. INDEX16379→15656B;
decision family261604→260881B. Whole DEV6957B→0280/CH1398B→0281 retained,
receipt+digest refusals discriminate. Focused12/sharder12/seven books/3238links,
normal+print/two literal examples pass; only inherited EOF notices0280:100 and
0281:27, all other whitespace0. D51 remains owned next; LIVE/CPU unchanged.

.4g: verify.py/rendered.py normal/O and focused.sh rc=0: exact20208B neutral
body, bounded1892B note, complete source inverses/99 old entries/1384 protected
files/Gitlink exact. Focused12/sharder12/seven books/3236 links; all56 complete
policy blocks normal+print and literal read pass. Adjacent HTML table cells need
explicit boundaries in the text verifier; complete content agrees after that
normalization. Existing caps/seals/CPU unchanged; full adoption still pending.

.4f: verify.py/rendered.py normal/O and focused.sh rc=0: D50 fixed;33 files/six
active, heading-only/full-book inverses, eight pointer authority homes,97 old
entries/whole heads/1386 protected files/Gitlink exact. Focused12/sharder12/seven
books/3208 links and three literal examples pass; fixed caps and LIVE unchanged.

.4e: seven books, whole reference/book inverses and rendered five-command/first-
last checks, focused8 and protected scope1269unchanged rc=0.

.4d: focused11, shell56/56, Python2/2, children28, four named negatives, parent,
SEAM19/0, acceptance10/0, waiver5/0, synth6/0 and protected scope rc=0.
First full CI refused because registry editing overlapped the running shell reader;
syntax is green, sources fixed for complete rerun (target/live-containment/locality).
Final full CI after explicit-guard hardening rc=0: all five legs/seven books,
Rust173/17/253. Mock optimization levels0/1/2 refuse before allocator; optimized
shell56/56 passes. The two original follow-ups below are resolved by this slice.

.4c: capture/migration/reproduction/consumer/predecessor proof, focused15,46controls,
seven books and full five-leg `make ci` rc=0; byte-exact retention with no cap raise.

.4b: prototype/reproduction/controls/focused9/seven books rc=0.

Registry prose follow-up owned by `.4`: the SHARD-FREEZE description in
scripts/check_doctrines.project.sh still says the physical manifest only grows; the
approved seal preserves append-only logical rows across archive/live manifests instead.
The checker, doctrine family and book already state that contract. Priority: correct
this display text with the scheduled locality/containment follow-up after CI-RECOVERY.

The first commit gate refused the descriptor because FIXTURE-FINGERPRINT resolves
`path` relative to the record directory, while this terminal uses repository-root
identity. The new schema explicitly names its root-relative `object`; SHARD-FREEZE
authenticates that object and every source member, without changing or excluding the
generic fingerprint contract. The frozen object bytes and digests are unchanged.

Additional locality defect owned by `.4`: `scripts/check_task_acceptance.sh` uses
unqualified `mktemp -d`; `printf '%s\n' "$TMPDIR"` on this host returned the OS
temporary directory rather than the repository. The doctrine driver does not override
it. Other standalone entrypoints require a targeted census before a common repair.
Priority: establish repository-local TMPDIR for ongoing runs immediately; schedule the
entrypoint census/repair in `.4` after CI-RECOVERY and before broader containment work.
Do not delete shared OS temporary content or claim standalone locality already fixed.

Slice (a), 2026-10-08: copy/verify/retire exact, archive and partition controls 31/31, sharder 12/12; terminal 287216 B, ordinary shards 8039 B; gates/books at commit.

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-10-06` | `.3` | the section census; the verbatim moves (35 + 76 rows, each exactly once — the first pass's dropped row caught by a positional census); REGISTRY-MIRROR's project scope (13/13; the union RED on a removed row); the families registered | **met** — DOCTRINE_ENFORCEMENT ~11 KB, TOOLBOX ~3.2 KB; the next tool and doctrine fit |
| `2026-10-06` | `.2` | the three drifts measured (crates/app absent; the scaffold header; the 16,228-byte note); each corrected text checked against `ls crates/`, the CLI's subcommand match, `ls profiles/`; the map regenerated | **met** — the orientation sources state today's repository |
| `2026-10-06` | `.1` | the registry control vs the index census (22 of 31 rows completed); the CLOSURE rule that forbade obeying it; FRONTIER-SYNC extended (20/20; RED on the real pre-move index: 22 COMPLETED IN INDEX); the verbatim move; the register registered; the book's live includes | **met** — the index holds open trees only (4,053 B); completed trees have a gated home |

<a id="commit-log"></a>

## commit-log

`SEMULITH-LC-0051 (leaf LIVE-CONTAINMENT.4): re-derive the task-family count for retention continuation` — first continuation cut; next P4.14 a42ap.
`SEMULITH-LC-0050 (leaf LIVE-CONTAINMENT.4): re-derive the decisions-family bound a second time` — authority with the row; next P4 retention capacity.
`SEMULITH-LC-0049 (leaf LIVE-CONTAINMENT.4): seal the second finite history segment` — verified finite rollover; next P4.14 delivery.
`SEMULITH-LC-0048 (leaf LIVE-CONTAINMENT.4): select pinned mdBook before terminal capture` — native prep verified; user capture/analysis pending.

`SEMULITH-LC-0047 (leaf LIVE-CONTAINMENT.4): record the application handoff blocker` — Kimi Code disposition pending.

`SEMULITH-LC-0045 (leaf LIVE-CONTAINMENT.4): add one-command scoped dependency capture` — tool prepared; D79 capture/analysis pending.

`SEMULITH-LC-0044 (leaf LIVE-CONTAINMENT.4): preserve dependency failure forensics` — finite verified trace/evidence; D79 packet access blocked, D80 repair owned.

`SEMULITH-LC-0043 (leaf LIVE-CONTAINMENT.4): repair authored-index active context` — D78 fixed with aliases intact; D79 delivery/dependency tracing immediately next.

`SEMULITH-LC-0042 (leaf LIVE-CONTAINMENT.4): qualify executed page-heading navigation` — full runtime/source assessment retained; D78 conditional repair immediately next.

`SEMULITH-LC-0041 (leaf LIVE-CONTAINMENT.4): retain closed qualification history losslessly` — finite delegated capture/source/publishing checks; heading navigation next.

`SEMULITH-LC-0040 (leaf LIVE-CONTAINMENT.4): qualify generated chapter contents` —93 chapters/14 TOCs, complete source/rows; byte-pressure remedy next.

`SEMULITH-LC-0039 (leaf LIVE-CONTAINMENT.4): preserve public navigation nesting refusal` — D77 fixed; legacy16/1/current16/0; generated TOC/search next.

`SEMULITH-LC-0038 (leaf LIVE-CONTAINMENT.4): qualify the actual book navigation consumer` — complete source/rendered assessment; D77 repair immediately next.

`SEMULITH-LC-0037 (leaf LIVE-CONTAINMENT.4): preserve malformed history decompression refusal` — D76 fixed/263 current queries clean; generated navigation next.

`SEMULITH-LC-0036 (leaf LIVE-CONTAINMENT.4): qualify catalogue and archive query consumers` — complete263-query assessment/D76 owned; LC0037 repair next.

`SEMULITH-LC-0031 (leaf LIVE-CONTAINMENT.4): retain whole closed reader records` — ten spans/nine units/checklist retained; index/query next.

`SEMULITH-LC-0030 (leaf LIVE-CONTAINMENT.4): enforce include integrity in public builds` — D65/D68 fixed; index/query expansion next.

`SEMULITH-LC-0029 (leaf LIVE-CONTAINMENT.4): qualify owned include sources and replay` — component complete/D66 fixed; D65 public integration next.

`SEMULITH-LC-0028 (leaf LIVE-CONTAINMENT.4): qualify actual include readers` — .4i2b3a assessment complete; D65 repair next.

`SEMULITH-LC-0027 (leaf LIVE-CONTAINMENT.4): validate task sources before progress claims` — D59/D64 fixed; .4i2b reader review next.

`SEMULITH-LC-0026 (leaf LIVE-CONTAINMENT.4): retain whole closed task units` — .4i2b2h complete; D59/D64 code repair next.

`SEMULITH-LC-0025 (leaf LIVE-CONTAINMENT.4): qualify task source and correct stale projections` — .4i2b2h next.

`SEMULITH-LC-0024 (leaf LIVE-CONTAINMENT.4): correct live composition progress` — D58/D60/D61 fixed; D59 qualification next.

`SEMULITH-LC-0023 (leaf LIVE-CONTAINMENT.4): collect closed graph inventory evidence` — .4i2a collection only; .4i2b transitive reader review next.

`SEMULITH-LC-0022 (leaf LIVE-CONTAINMENT.4): qualify containment inventory inputs` — .4i1 inputs and local integration contract; .4i2 graph inventory next.

`SEMULITH-LC-0021 (leaf LIVE-CONTAINMENT.4): apply reviewed task count authority` — .4h6c4 complete; count107, health64 debt; .4i full containment adoption next.

`SEMULITH-LC-0020 (leaf LIVE-CONTAINMENT.4): review separate six-activity count authority` — .4h6c3 complete; no cap change; .4h6c4 applies after fresh same33-ID/typed96 checks.

`SEMULITH-LC-0019 (leaf LIVE-CONTAINMENT.4): refuse unavailable or malformed registry policy` — .4h6c2 complete/D56–57 fixed; .4h6c3 separate capacity authority review next.

`SEMULITH-LC-0018 (leaf LIVE-CONTAINMENT.4): qualify remaining registry projections` — .4h6c1 complete/D56 confirmed; priority1 .4h6c2 repair before .4h6c3 authority.

`SEMULITH-LC-0017 (leaf LIVE-CONTAINMENT.4): correct the five-unit composition receipt` — .4h6b complete/D55 fixed; .4h6c separate capacity review next.

`SEMULITH-LC-0016 (leaf LIVE-CONTAINMENT.4): contain navigation before capacity authority` — .4h6a complete; .4h6b D55 correction next, .4h6c capacity review after.

`SEMULITH-LC-0015 (leaf LIVE-CONTAINMENT.4): correct the count receipt classification` — .4h5 complete/D51 fixed; .4h6 separate capacity review next.

`SEMULITH-LC-0014 (leaf LIVE-CONTAINMENT.4): refuse unavailable routing evidence` — .4h4 complete/D53–54 fixed; .4h5 D51 capacity review next.

`SEMULITH-LC-0013 (leaf LIVE-CONTAINMENT.4): refuse unmeasurable family inventories` — .4h3 complete/D52 fixed; .4h4 D51 capacity review next.

`SEMULITH-LC-0012 (leaf LIVE-CONTAINMENT.4): qualify capacity inputs before authority review` — .4h2 assessment complete; D52 repair precedes D51 capacity review.

`SEMULITH-LC-0011 (leaf LIVE-CONTAINMENT.4): contain duplicate decision-index summaries` — .4h1 complete; .4h2/D51 capacity review next.

`SEMULITH-LC-0010 (leaf LIVE-CONTAINMENT.4): adopt the local containment contract` — .4g complete; full inventory/checker/migrations and .4h capacity review remain.

`SEMULITH-LC-0009 (leaf LIVE-CONTAINMENT.4): make orientation describe its sources` — .4f complete; full adoption and capacity remedy remain.

`SEMULITH-LC-0008 (leaf LIVE-CONTAINMENT.4): publish temporary-control procedures in the book` — .4e complete.

`SEMULITH-LC-0007 (leaf LIVE-CONTAINMENT.4): keep temporary allocations on the repository volume` — .4d complete; full containment adoption remains.

`SEMULITH-LC-0006 (leaf LIVE-CONTAINMENT.4): seal closed P4 task history` — .4c complete; full adoption remains.

`SEMULITH-LC-0005 (leaf LIVE-CONTAINMENT.4): prepare finite task-history archive review`

`SEMULITH-LC-0004 (leaf LIVE-CONTAINMENT.4): seal the approved history archive with authenticated retrieval` — slice (a); full adoption remains.

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `.3` | `SEMULITH-LC-0003 (leaf LIVE-CONTAINMENT.3): TOOLBOX and DOCTRINE_ENFORCEMENT partitioned behind bounded indexes — 76 tool rows and 35 doctrine rows moved verbatim, REGISTRY-MIRROR judges the family union` | both surfaces regain headroom; no row lost |
| `.2` | `SEMULITH-LC-0002 (leaf LIVE-CONTAINMENT.2): the stale orientation sources corrected — the knowledge map's subsystems, the workspace header, the README policy's measurements` | three drifts; the policy decision untouched |
| `.1` | `SEMULITH-LC-0001 (leaf LIVE-CONTAINMENT.1): the closed-tree register — completed trees leave the index (22 rows moved verbatim), FRONTIER-SYNC gates both files` | the control applied and enforced; the index 8,172 → 4,053 B |

