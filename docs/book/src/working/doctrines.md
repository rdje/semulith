# The doctrine gates

A rule that lives only in a document is a suggestion. Every mechanizable rule here is a script
that exits nonzero, wired into four layers so that non-compliance is expensive rather than
merely discouraged:

| Layer | Mechanism | What it catches |
| --- | --- | --- |
| E1 — discovery | the doctrine documents, reachable from every harness's bootstrap file | "I did not know the rule" |
| E2 — self-check | `scripts/check_doctrines.sh` and each registered check | the rules, executable, runnable by hand |
| E3 — git hook | `.githooks/pre-commit` runs the enforcer | fast local failure |
| E4 — CI | the same enforcer runs server-side | a locally `--no-verify`'d commit |

`make gate` is that command. Thirteen checks run today.

Local checks and hosted CI are separate evidence. The 2026-10-08 pushed revision failed
strict Rust lint on 1.99, book provisioning and a cold Miri log path, despite a green
local pre-push suite on 1.95. CI-RECOVERY.1 repairs the Rust lints with the exact newer
toolchain; benchmark tests and independent SHA comparisons preserve results. CI-RECOVERY.2 provisions digest-verified mdBook 0.5.4 before
the book gate, with Rust, Cargo and temporary stores rooted in the repository. A cold
native check builds all registered books; the repaired hosted doctrine run confirms Linux execution.
CI-RECOVERY.3 repairs cold output/provisioning paths and truthful portability verdicts.
Its native and big-endian interpreted core runs each pass all 153 tests; full local CI
also passes on Rust 1.99. Hosted green requires a successful run on a permitted push. A local green result alone cannot close that obligation.

The director approved the pushes needed for this CI recovery without asking
again (`decision_ci-recovery-push-approval`). Each used `scripts/approved_push.sh`:
full local CI, a committed approval record, then the guarded push. All three
workflows now pass on repaired revision `76882c8`; that exception has expired and
the normal cadence applies again.

The first authorized recovery push is `f4364bc`: both required local full suites
passed, and the approval record traveled in that commit. Hosted Rust and every
portability leg pass there, including both 153-test interpreted targets. The doctrine
job provisions mdBook, then refuses a GUEST-GEN self-test whose diagnostic was hidden
by its wrapper. CI-RECOVERY.4 preserves the failure and exact run URLs.

GUEST-GEN now retains the full self-test output in `target/guest-gen/self-test.log`,
prints the interpreter version and a bounded tail on failure, and keeps its refusal
exit code. A failed doctrine job publishes that log as an artifact. The local controls
still pass; the visibility repair by itself does not fix the hosted cause.

A tracked-only cold reproduction identifies the missing input: the parcel probe's
temporary unit copied its encoding but omitted its profile and CSR state. Copying
those owners removes its dependency on a warm external CSR table; the deliberately
unmodeled CSR uses its explicit address. `probe_gc_parcel_guest.py --cold` runs the
public probe from a temporary snapshot of tracked inputs without reference caches.
Its permanent GUEST-GEN control passes locally, alongside the prior mutations.
The second recorded recovery push, `76882c8`, passes hosted Rust, the entire
doctrine enforcer and every portability leg. Its native x86-64 Linux and ARM64
macOS manifests agree; native and powerpc64 Miri each pass 153 tests, none failed
or ignored. The exact run receipts retire the scoped push exception.

Miri's printed test durations use its default simulated clock. External GitHub step
timestamps supply wall-time evidence; the timing reference records the observed
difference. Test counts remain exact, and isolation stays enabled.

Handoff counts repository handles, even read-only ones:

```sh
bash scripts/check_no_background_jobs.sh --all
```

Exit 0 sees no project jobs; 1 names jobs; 2 refuses tool errors, stderr or empty
snapshots. Use host visibility. `--all` lists inherited cwd advisories. Closing
editors needs authority; exemptions need the director's ruling in
`doctrine/sanctioned_processes.tsv` and affect this census only. Content gates
stay enforced. `make gate` and CI test synthetic snapshots.

During the 2026-10-09 crash recovery, the actual census found Kimi Code still holding
two read-only AGENTS.md handles. The director authorized its closure; SIGTERM stopped
the app and five helpers, and the actual census then reported `handoff: OK`.
CI-RECOVERY closes 4/4 with both hosted and local handoff obligations verified.

## The universal registry

These ship with the discipline spine and are project-neutral:

| ID | Proves |
| --- | --- |
| `MEMORY-ARCH` | the durable four-layer memory invariants hold |
| `DOCPATH` | no tracked markdown carries a checkout-specific absolute path |
| `TASK-TREE-OWNERSHIP` | every staged code change is owned by a task-tree leaf |
| `TASK-ACCEPTANCE` | that leaf's three hard-gated boxes are ticked and carry tool output **inside each box** |
| `WAIVER-ROUTING` | a leaf saying a gate does not apply names the leaf that owns fixing it |
| `README-STABILITY` | the landing page stays one, under a line cap **and** a byte cap |
| `LIVE-DOC-CURRENCY` | no document reports its own currency — git already carries it |
| `LESSON-PROMOTION` | a new dated lesson reaches the retrievable layer or is explicitly declined |
| `ROUTING-EVIDENCE` | a finding routed to another tree carries what was measured |
| `GAP-CLAIM-CENSUS` | a "nothing checks X" claim records the census it rests on |
| `TABLE-ARITY-RATCHET` | no staged markdown raises the count of table rows whose cells disagree with their header |
| `KNOWLEDGE-MAP` | the derived orientation map is in sync with its sources |
| `PROJECT-SPECIFIC` | this project's own doctrines, below |

## This project's own doctrines

| ID | Proves |
| --- | --- |
| `DELIVERY-PROVENANCE` | every delivered manifest row carries exactly one declared disposition, and the frozen ones still hash to the delivered bytes |
| `FIXTURE-FINGERPRINT` | every record pinning a file's `sha256` still describes the tree |
| `README-ROUTING-CLOSURE` | every destination the landing page routes to is governed, exists, and stays under its ceiling; failed or diagnostic input reads refuse 2; validated totals feed all family bounds — the per-part ceiling two-tiered: authored members are bounded, regeneration-gated derived members are exempt as a checked property (a fact-ownership mirror row with a regeneration governor), reported as proof |
| `PROFILE-CONSISTENCY` | counts, authority/source, capture shape/edges/pins, witness/baseline links, bounded identity/receipt/manifest/leaf/files+images/bytes/evaluation/program/argv/relations/impact; source/ELF bind; status derived from the graph; the retained case's policy legs measured (8 of 10); qualification stays closed |
| `SEAM-INTEGRITY` | this project's repairs to the neutral checks still *do their job* — asserted as behaviour, never as presence |
| `FRONTIER-SYNC` | `docs/TASK_TREE.md` still names the leaf the tree itself calls next, and every tree has exactly one row — the index while open, `docs/TASK_TREE_CLOSED.md` once done |
| `REGISTRY-MIRROR` | these two tables still list exactly the doctrines the drivers register |
| `UPSTREAM-INDEX` | a defect raised against a dependency is tracked like our own: each issue is a self-contained subtree under `docs/upstream/` whose `issue.sexp` owns its id, severity, state and dated history, and every index of it is a checked mirror — because self-containment and a second source of truth cannot both hold |
| `TREE-CLAIMS` | every live document's leaf counts, active trees and frontier leaf match `docs/tasks/` |
| `DERIVED-COUNTS` | every count a live document states about an enumerable population is re-derived |
| `RECORD-SCHEMA` | every record file validates on its track (JSONL by schema, catalogues by the schema layer), cites only pinned sources, and states what its profile states — the JSONL track on two engines, the tracked Python validator and the workspace's Rust graph checker (`P1-LAB.7`), which re-derives the PACKAGE_CHECKS rows and enforces the §3 graph invariants over the examples bundle; exact tokens refuse terminal newlines; generic patterns remain searches |
| `GATE-REPORT` | the tracked gate report is still what the generator derives from its inputs |
| `SHARD-FREEZE` | authenticate live/sealed history and predecessor rows; preserve full old live entry bytes/order through published sharding in index/working views; judge the complete staged partition too. Refuse failed Git reads, changed descriptors, unsafe/corrupt data and duplicate headings/paths. |
| `TASK-HISTORY` | finite P4/qualification captures; original 46 controls, 43 ordinary publishing tests and 32 qualification reader/publishing tests normal/O. Atomic source-authenticated qualification publication; both views freeze against HEAD;50 arms on commit/CI |
| `ARTIFACT-COHORT` | plans, journals, provenance |
| `PORT-WEB` | the crate skeleton builds for the browser target — the workspace compiles for `wasm32-unknown-unknown`, so a host-only API cannot slip into the engine unnoticed |
| `API-DOCS` | the API reference is rustdoc, and its intra-doc links and HTML are sound — a broken or private link or an unclosed tag in any doc comment is refused, naming file, line and lint; the undocumented public items per crate may only fall |
| `STATE-GEN` | the generated state module is still what the state descriptor generates — drift is refused, and the generator refuses shapes it cannot emit rather than silently guessing |
| `DEF-GEN` | the generated definition module is still what the canonical definition generates — decode tables, lowered semantics trees, and the OWN-03 manifest with definition, generator, configuration and source fingerprints; drift is refused, the generator refuses shapes it cannot emit rather than silently guessing, and a check that cannot judge refuses rather than passing |
| `GUEST-GEN` | the generated guest fixture is still what the tracked guests and their specification-derived expectations generate — assembled bytes plus EVD-05 expectation data as one fixture the offline differential re-runs on every commit; drift is refused, the generator refuses a guest it cannot reconcile rather than silently guessing, and a check that cannot judge refuses rather than passing; Sail validates whole budgets/differences/three-run bytes; ELF alignment, entry and source/image correspondence are checked |
| `BOARD-GEN` | a board's composition manifest, composed catalogues, hardware description and human-readable map are still what the canonical board definition generates (`scripts/gen_board.py`; OWN-05 — no handwritten duplicate map anywhere); drift is refused with the regeneration command, the generator refuses by name an inconsistent definition (a region overlap, an mmio window with no device, an executable mmio region), and a check that cannot judge refuses rather than passing |
| `BOARD-VERDICT` | a board's composition verdict is decided, not narrated (CPU/environment contract §5, ENV-02) — every CPU environment-assumption in the composed unit is discharged by named guarantees, every `satisfies` edge in the board definition resolves to a discharged assumption, and every device obligation the dossier defers to the board is answered by exactly one decision `answers` edge; an unmatched assumption or a dangling edge is a rejection by name, never a note (`P5-BOARD.4`) |
| `PLATFORM-GEN` | a board's platform capability manifest (`platform.sexp` — the OWN-06 export for a compatibility checker, `docs/ARCHOGEN_INTEGRATION.md` §3) is still what its canonical inputs generate (`scripts/gen_platform.py`: the board definition, the pinned processor's profile, the composed obligations); drift is refused with the regeneration command, and the board's `dossier-sha256` pin is verified against the live dossier at derivation — the pin, measured display-only before this leaf, is load-bearing now (`P5-BOARD.6`) |
| `EXERCISE-COVERAGE` | every form a profile declares in its scope is executed by a tracked guest — coverage reported with its denominator (the count re-derived against the enumeration), the SCP-02 dependency closure resolved through the one shared resolver; the dynamic-exercise half that complements EXTRACTION's static sufficiency; fired RED at 15/52 before registration, GREEN at 52/52 (`P2-SCALAR.1`) |
| `INTERACTION-MATRIX` | the declared interaction matrix (fault × alias × boundary × event × progress × restart) is declared first as tracked data and then exercised — the cells re-derived from the axes, an omitted cell failing by name; every disposition resolves (guest with source and expectations, the closed mechanism registry, degenerate with its reason); no tracked guest is an orphan; every difference id named exists in the reference dossier (`P2-SCALAR.4`; fired RED against the real corpus before registration) |
| `MATERIALS-BILL` | every modelled unit's book carries a materials bill whose identity tables are generated from the pinned dossier (drift refused — a digest cannot rot) and whose prose states for every material what it does NOT supply — a missing section or a missing negative statement fails by name (`MODEL-BOOKS.1`; fired RED against the real corpus before registration) |
| `UNIT-BOOKS` | safe relative registered book paths; catalogue IDs/kinds match the shared registry; no orphan books; owned includes validate before expansion with mandatory execution witnesses and typed refusals; fresh project/unit builds under `target/`; rendered local paths/HTML fragments resolve, including print. Remote availability and semantic/chapter completeness remain separate (`MODEL-BOOKS.6`). |
| `DOSSIER-SCHEMA` | tracked dossier documents with a family schema validate through the one checker, including typed matched-GPR witnesses/baselines and bounded artifact-byte controls (no qualification); repeated expectation write keys refuse; documents without a schema are skipped and counted by name (`P3-BREADTH.7`; first RED: historical D-FENCE double-note) |
| `PUSH-RECORD` | the push-approval ledger is append-only (a staged change keeps HEAD's content a prefix) and every entry carries who/when/why/range with sequential ids — a correction is a new entry, never an edit (`PUSH-DISCIPLINE.3`; fired RED against the real corpus before registration) |
| `COMMIT-PREFIX` | the `commit-msg` hook pins the `SEMULITH-` work-unit prefix — a `SEMILITH-` subject is refused with `SEMULITH` named, a `SEMULITH-` subject passes; the probe is behavioural, so a scaffold sync that reverts the neutral hook turns the very next commit RED, named; history carries both spellings and is immutable, so enforcement is forward-looking at the boundary (`PREFIX-DISCIPLINE.1`, director ruling `2026-09-30`; fired RED against the real tree before the pin existed) |
| `SOURCE-FORMAT` | refuse retired formats in source-of-truth families; parse every `.sexp` with the shared reader and verify named refusals and optimization-safe controls |
| `UNIT-COMPOSITION` | a unit's composed encoding space is decided — schema-conformant document, fragments resolved through the one shared resolver, collision-free union, and partial compositions declared rather than inferred |
| `SEMANTICS` | the execution authority's corpus holds — every semantics document is well-formed, complete and cited; a silent semantic override across fragments is refused; locators resolve offline, with a named skip when the cache cannot judge |
| `EXTRACTION` | the definition is sufficient for an engine — every declared instruction has an encoding, semantics and a requirement (one set, four ways); every state element a reset; every obligation its checks |
| `FACT-OWNERSHIP` | the no-duplicated-fact rule holds — one owning file per fact kind, every mirror governed, every restatement the corpus has is registered |
| `SCOPE-COVERAGE` | no model code against an uncovered scope — a required category missing or absent refuses; P1-LAB's precondition |
| `PROSE-SPACING` | no word and number run together in the prose of a book or a unit document. Code, link targets and URLs are not prose, and a real name ending in a number is listed in `doctrine/prose_identifiers.txt`. It judges the spacing, not the number |
| `BOOK-INDEX` | the term index derives from raw SUMMARY chapters, canonical glossary terms and acronyms; glossary/index discussions are excluded, includes unexpanded. Valid bytes stay exact, drift fails 1, unjudgeable reads/writes/launches refuse 2. Chapter presence is measured; chapter truth is unclaimed. The controls judge a small frozen book, so a deleted chapter, `SUMMARY.md` or glossary fails by its own name and does not read as a check that stopped working. |
| `CITATION-QUOTES` | a quoted phrase that a tracked source-of-truth file attributes to a section of a pinned specification page really occurs in that section — `RVI-F §20.1.1` can exist and still be the wrong place for the sentence quoted under it; the refusal names the section where the sentence actually is. Quotes only (paraphrase stays a reviewer's question); judged when the pinned pages are on disk, a named skip otherwise |
| `FP-VECTORS` | the floating-point model layer's test vectors are exactly what an independent, exact-arithmetic reference written from the specification produces — and that reference is itself re-checked against the computer's own IEEE arithmetic on every run, so a drifted oracle cannot regenerate a wrong table |
| `CONTRACT-FREEZE` | the processor's contract with its environment is kept in numbered versions; once a version is frozen its statements cannot be changed — a statement that turns out wrong is replaced in the next version, and the old one stays on the record |
| `M-VECTORS` | the table of expected multiply and divide results is produced by a program that works them out from the specification, and nobody may edit it by hand — otherwise its expected values could be quietly changed to match the processor instead of the specification; the program itself is checked against the rules the specification states, such as quotient times divisor plus remainder giving back the dividend |

Each ships a `--self-test` whose RED arms assert the **reason** as well as the verdict, each was
fired RED before being registered, and each **refuses** — exit 2, not exit 0 — rather than
passing if its own self-test stops discriminating. A check that cannot judge must never report
that the rule holds.


### Citation readers authenticate the artifact before judging its text

Both the locator reader (`scripts/check_citations.py --corpus`) and default
quote reader require the source ledger's exact SHA256 and byte length. A fetched
working area is preferred; otherwise the materials snapshot supplies the page.
An existing but altered preferred copy refuses, even when a valid snapshot is
available. Missing or malformed identity also refuses. `http_status 0` pins
retain their named non-HTML treatment, and explicit synthetic `--pages` quote
fixtures keep their existing interface.

For example, c18c found the three base HTML pages had unchanged architecture
text and section numbers but a different Antora metadata value. Both old readers
passed; repaired readers named RVI-INTRO and its mismatched hash. After verifying
the snapshot manifest and all 72 files, the project restored only those three
fetched copies, 226,648 bytes. The pins were unchanged. Same-size altered text,
wrong lengths and absent identity now have discriminating controls.

Wrapper dispatch distinguishes absence from corruption. Fetched-only evidence
is judged. Partial directories, altered source pages and bad snapshot manifests
reach a refusal; only absence of both routes permits the named skip. Locator
controls run with SEMANTICS, and quote controls include the default corpus path.
This authenticates the cited artifact; paraphrase accuracy still needs review.

## A document that restates a registry is a mirror, and mirrors rot

The last two rows above exist because of a defect found by resuming this repository rather than
by reading it. Three documents restate facts that a machine-readable file already owns:

| The mirror | Its source of truth | How it was kept |
| --- | --- | --- |
| `docs/TASK_TREE.md`'s frontier column | each tree's own *Current Frontier* | `COMMIT.md`: update it "only if the frontier changes" |
| this chapter, and `DOCTRINE_ENFORCEMENT.md` | the two registry arrays in the driver scripts | by hand, when someone remembered |
| `LIVE_STATUS.md`'s leaf counts | the `- ID:` entries in each tree | by hand |
| `MEMORY.md`'s active tree and frontier leaf | the same trees | by hand |
| `LIVE_STATUS.md`'s "N destinations governed", "N registered", "N self-test arms" | the registry, the drivers, the checks | by hand, as **running totals** |

The first two had drifted; the last two had not. All four are now gated, because a mirror that
happens to be correct today is not a checked mirror — it is an unchecked one that has not been
caught yet. The shape of each drift is worth more than the fix.

**The index named a finished leaf.** It pointed at `P0-PROFILE.2` — already `done` — while the
tree named `.5`. One row of fourteen was wrong, which sounds like a low rate until you notice
*which* row: the only `active` tree. A resuming session is routed `MEMORY.md` → the index row →
that tree's frontier, and only an active tree's row is ever read. The drift rate on rows anyone
follows was 1 in 1, and the recovery procedure itself was what broke.

**This chapter under-reported its own project.** It listed three project doctrines while five
were registered and running. That direction matters: a mirror that falls behind never invents a
guarantee, it quietly *withholds* one — and it does so on the surface a reviewer reads instead
of the code. `REGISTRY-MIRROR` also gates the sentence "Thirteen checks run today", because a
count typed by hand is a constant that is a function of the repository.

The fix in both cases is a gate rather than a generator. A generated index would also have
prevented the drift, and was rejected: the "why next" column carries reasoning no generator can
produce, and a generated file invites hand edits that are silently discarded. Both gates make
the **source** authoritative and say so in their failure text — *"the tree is authoritative"*,
*"the registry is authoritative"* — because editing a summary to match its record is safe, while
editing a record to match its summary destroys the evidence.

### A running total is not a measurement

The first three leaves gated what live documents say about *task-trees*. They said nothing about
any other countable population, and the gap closed itself in the most convincing way available:
within a single working session this repository committed **two** such numbers wrong.

`LIVE_STATUS.md` claimed *24 destinations governed* while the registry held 25 rows — stale since
the commit that added the `profiles/` row. It also claimed *107 self-test arms* when the real
total was **112**. Neither was a typo. Both were maintained the same way: someone took the number
that was already written down, added what they had just contributed, and wrote the sum back.

That is the failure mode in one sentence. **A running total is a memory of a measurement, not a
measurement** — and nothing recomputes it, so it drifts quietly and confidently.

`DERIVED-COUNTS` re-derives each one from the population it summarises, and prints the command it
used, so the claim and its producer travel together (the capture is the one made at registration
`2026-09-14` — the numbers are derived values, so today's run shows today's counts):

```
$ scripts/check_derived_counts.sh --list    # output at registration, 2026-09-14
CLAIM                  ENUMERATOR                                          VALUE
routed destinations    grep -cv '^#\|^$' doctrine/readme_routes.tsv        25
project doctrines      grep -cE '^  "[A-Z]' …/check_doctrines.project.sh    9
book chapters          grep -cE '^\s*-? ?\[' docs/book/src/SUMMARY.md      27
self-test arms         arm_total                                           122
```

It caught its own registration, which is the neatest demonstration available: registering the new
doctrine made the repository hold nine project doctrines where the page said eight, and the gate
said so before the commit could land.

### The scope of a gate can be data someone already wrote down

`TREE-CLAIMS` needed to know which documents are *live* — a changelog entry reading "2 of 9
leaves" was true the day it was written, and rewriting history to match today would corrupt the
record the changelog exists to keep. That distinction was already recorded, once, in the
`lifecycle` column of `doctrine/readme_routes.tsv`: `hot_live` for `MEMORY.md`, `LIVE_STATUS.md`
and the landing page; `append_history` for `CHANGELOG.md` and `DEV_NOTES.md`. So the gate reads
its own scope from that registry instead of carrying a list. A new live surface is covered the
day it is registered, and no one has to remember to extend a script.

That gate had **no drift to repair** — the census found every leaf count and both pointer claims
already correct. Prevention, not repair, and the leaf says so rather than manufacturing a
defect. Its falsification came from breaking the real documents on purpose and watching each
control fire:

```
COUNT DRIFT MEMORY.md: '2 of 9 leaves' for MIRROR-DRIFT; the tree has 2 of 3
DONE FRONTIER MEMORY.md: names 'MIRROR-DRIFT.1' as the frontier; the tree records it `done`
MISSING ACTIVE MEMORY.md: 'P0-PROFILE' is `active` and the pointer does not name it
COUNT DRIFT LIVE_STATUS.md: '13 leaves' for P1-LAB; the tree has 12
```

### The gates now catch each other

Registering `TREE-CLAIMS` without adding its rows to these two tables produced, immediately:

```
REGISTRY-MIRROR: a doctrine document no longer mirrors the enforcer registry.
  NOT MIRRORED DOCTRINE_ENFORCEMENT.md: 'TREE-CLAIMS' is registered and has no row …
  NOT MIRRORED doctrines.md: 'TREE-CLAIMS' is registered and has no row …
```

That is the whole argument for gating mirrors rather than remembering them. The omission that
previously survived two registrations unnoticed now survives about ninety seconds.

## Frozen mirrors and current requirements

RECORD-SCHEMA requires an obligation's `requirement_id` mirror to state its
requirement exactly. A frozen historical statement may differ only when its
record line still matches its frozen SHA-256 pin and the active consecutive
version chain supersedes it with an effective mirror of that same requirement.
Each supersession replaces an inherited record with its own version's member.

For example, correcting the reservation policy retains frozen `OB-RESERVATION`.
V2's `OB-GC-RESERVATION-V2` mirrors the current `REQ-D-RESERVATION`. A missing
route, altered pin, wrong requirement or drifting replacement still rejects.
CONTRACT-FREEZE checks the complete version inventory.

Authority also follows explicit requirement mirrors, including replacements
outside historical `obligation_ids`. A requirement classified
`defined` requires `authority architecture`: identical wording with
`authority laboratory` is rejected. Selected laboratory policies remain valid.
Fourteen version/authority controls distinguish these cases. Run `bash scripts/check_requirements.sh --self-test` for
the controls, or without arguments to check the real records.

## The self-test that ran a third of its arms

`FRONTIER-SYNC`'s controls were written, run, and reported `4 pass / 0 fail`. Fourteen arms
existed; four executed. Ten `arm` calls shared a physical line with the fixture call before them
with no `;` between, so the shell passed `arm` and its arguments as surplus parameters to a
function that reads two — discarded without an error of any kind. Adding the separator produced
`13 pass / 1 fail`, and that one failure was a real defect in the gate.

The rule this repository already had — *a gate never observed RED is not known to work* — was
being applied one level too low. It belongs to the self-test as well, and the check is a
subtraction: count the arms you wrote, compare it with the number reported.

```
$ grep -c '  arm "' scripts/check_frontier_sync.sh
16
$ scripts/check_frontier_sync.sh --self-test
FRONTIER-SYNC --self-test: 16 pass / 0 fail
```

Both self-test harnesses now carry a strict-arity guard on every fixture helper, so the silent
swallow is a loud failure instead of a lesson someone has to remember:

```
FRONTIER-SYNC self-test HARNESS: index() got 6 argument(s), expected 2 —
  a missing `;` before `arm` swallows it
FRONTIER-SYNC --self-test: 15 pass / 1 fail
```

## A self-test judges frozen copies, so the real check can name the damage

A doctrine runs its self-test first and refuses to judge if the self-test fails. A self-test
whose arms read the live corpus therefore turns every damaged live file into the same
answer — `REFUSED — the check does not discriminate (self-test failed)` — and hides the named
failure the real check would have given. Ruling 5 (2026-10-28) and `XTASK.13` move the
fragile doctrines' arms onto frozen copies under `scripts/fixtures/`, one doctrine at a time:
`DEF-GEN` (slice a, `scripts/fixtures/def-gen/`), then `GUEST-GEN` — its surgical and census
arms over two mini corpora (b1), and its base-mirror and parcel-count arms over a frozen
owner→mirror pair under DEF-GEN's frozen encoding (b2, `scripts/fixtures/guest-gen/base-mirror/`:
the eight guests the mirror governor's predicates need, from both units), then its parcel author
probe (b3, `scripts/fixtures/guest-gen/parcel-legacy/`: the five legacy guests). The real check
still judges the live files. Measured on GUEST-GEN, with one live file damaged at a time:

| Live state | Before b2 | After b2 |
| --- | --- | --- |
| a mirror record edited (`bound-arith.expected.sexp`) | refused: 2 base-mirror arms missed | `FAIL — …guests_rv64gc.rs is out of sync`, exit 1 |
| an rv64i guest that no longer assembles | refused: 3 base-mirror arms missed | the generator's own refusal naming `smoke-arith.s` and `zzz9`, exit 2 |
| an rv64gc guest deleted (`c-alu.s`) | refused: 8 arms missed | refused: 1 arm missed — the parcel author's cold probe; after b3, `gen_guests: REFUSED — …run-order.txt: lists c-alu — not on disk`, with the self-test at 400 of 400 |

One state still ends in the old answer, and it is worth seeing why. Hand-edit a record the spec-side author owns *and* regenerate its fixture, and
the fixture check has nothing to say; `scripts/derive_rv64gc_expectations.py --check-owned` reads `DRIFT — inj-walk-l0`, but eight author probes read that live
corpus, so the self-test refused first (`391 pass / 9 fail`). A real-run step for it was drafted at b3 and taken back: until those probes were frozen it could never fire, and a
step never observed red is not known to work. Slice b4 froze them (`scripts/fixtures/guest-gen/owned/`, 42 guests, laid out as the repository is, and `scripts/frozen_owned.py`, which
points the deriver's `REPO` and `ENCODING` at them, because the deriver is pinned and does not move) and added the step:

| State of the tree | Before b4 | After b4 |
| --- | --- | --- |
| nothing damaged | `GUEST-GEN: ok` | `GUEST-GEN: ok` |
| a mirrored owned record's value edited, fixture regenerated (`inj-walk-l0`) | refused: `391 pass / 9 fail` | `MIRROR DRIFT — inj-walk-l0.s: architectural observations differ at boundary 0`, the self-test at 400 of 400 |
| one line of prose added to that record, fixture regenerated | refused the same way, since each of those probes asserts `--check-owned`, which reads this as drift; with the probes frozen and no step, it passes silently (`rc=0`) | `an owned expectation record does not re-derive from its guest.` `DRIFT — inj-walk-l0` |

The third row is why the step earns its place: the mirror compares architectural observations and the fixture compares bytes it generated, so only `--check-owned` reads the record's prose.
The author probes read other live guests too, records the author does not own but must reproduce. Slice b5 froze those (`scripts/fixtures/guest-gen/corpus/`, 26 guests), and adding a step for them would have been a mistake, because one already reads them:

| State of the tree | Before b5 | After b5 |
| --- | --- | --- |
| nothing damaged | `GUEST-GEN: ok` | `GUEST-GEN: ok` |
| `mm-sret`'s record edited, fixture regenerated | refused: `399 pass / 1 fail` | `MIRROR DRIFT — mm-sret.s: architectural observations differ at boundary 0`, the self-test at 400 of 400 |

A step was drafted for this and thrown away. Edit one value in each of the 26 records in a scratch copy, one at a time, and `scripts/check_gc_mirror.py --mirror <copy>` names every one, `rc=1`, because it derives
every guest it is given. A second reader of the same fact could never fire first, and a step never observed red is not known to work. The measurement that settled it is a tool now: `python3 -B scripts/live_reads.py scripts/probe_x.py`
reports the files a probe opens, through an audit hook, so "this probe reads no live corpus" is a number. The author probes read none.

Slice b6 froze the rest, so GUEST-GEN now meets the rule whole. Seven probes and the staging tool read the composition; a pinned tool, `matched_gpr_image.py`, fixes the canonical path by construction, so its probes point its one `ROOT` name at DEF-GEN's frozen tree for the test, the seam its own probe already used. Six states, each damaged on the real tree and restored:

| Damaged | Before b6 | After b6 |
| --- | --- | --- |
| `zifencei.sexp` deleted | refused: `246 pass / 154 fail` | `composes 'riscv/zifencei', but definitions/riscv/zifencei.sexp does not exist`, the self-test at 400 of 400 |
| that fragment, its semantics, `encoding.sexp`, `state.sexp`, `profile.sexp` each garbled | refused the same way | `rc=1`, naming the file and the line |

The tree they read gained `profile.sexp`, because an assembler takes IALIGN from it; without it the frozen composition read IALIGN 32, which the image probes caught at once and the author probes had not needed. What stays live is named: `schema/`, the tools' own input, and the Sail override in `probe_gc_sail`.

The tools gained what the frozen arms need and nothing else: `scripts/check_gc_mirror.py
--self-test --encoding F` takes its composition from that encoding's own root, and
`scripts/derive_gc_parcel_counts.py --encoding F --guests D` counts any unit, its self-test's
manifest census running over its own hand guests. One measurement trap is worth knowing: `cargo
xtask` fixes its repository root at build time, so a "before" binary must run on the tree it
was built in (`docs/knowledge/an-xtask-binary-judges-the-tree-it-was-built-in.md`).

## Two doctrines that are easy to misread

**`WAIVER-ROUTING` does not punish honesty.** A waiver stays legal; it simply has to name the
leaf that owns fixing the gate. An author writing a waiver *is the gate reporting a missing
capability*, which is the highest-signal defect report a gate can receive.

**A line cap is not a size bound.** Measured on a real project running this spine: a file whose
own header called it a "bounded resume pointer" sat at 60 lines — passing, exactly at its cap —
carrying **138,403 bytes**, with one line of 18,816. Line and byte caps are complements, not
redundancy: neither wrapped prose nor very long lines can bypass the budget. Never raise a cap
to fit content.

## The seams, and why they are not a loophole

A neutral check is adapted to a project through `.doctrine/`, never by editing the check:

- **`code_paths.txt`** declares what counts as a code change here. The built-in default was
  measured wrong in both directions over all 125 tracked files — it classified 28 files of
  mdBook prose as code because their path contains `src/`, and it could not see the two
  registries that hold the gates' own ceilings and dispositions, the `.doctrine/` seams, both
  git hooks, and `Cargo.toml`/`Cargo.lock`.
- **`evidence_tokens.txt`** declares this project's instrument signatures. It exists because
  `GAP-CLAIM-CENSUS` prints `git grep … | wc -l` in its own failure hint while
  `TASK-ACCEPTANCE`'s default signature family did not recognise either command — obeying one
  gate produced evidence the other refused.

⛔ Narrowing a gate's scope is precisely the change that can silently disable it, so a seam
edit is only trusted after the outcomes are **fired and observed**: a real code change with no
owning leaf must still be refused, gate data with no owning leaf must now be refused, and prose
alone must pass. A seam that has not been fired is an assertion.

### A seam was the wrong place for three of those fixes

The defects the seams were compensating for are **repaired in the checks themselves**. The
reason is a measurement: with both seam files moved aside, the full enforcer printed
`=== all doctrines green ===` and `rc=0`. Three fixes had silently reverted and nothing said a
word. *A fix whose disappearance is undetectable is not a fix.*

Template-wide repairs belong in the checks: anchored `src/`, behaviour-governing
path families and shared census vocabulary. Project gate data and instrument
signatures stay in `.doctrine/`. `update_scaffold.sh` retains the repaired
acceptance, gap and handoff checks; review newer upstream changes manually.
`make gate` checks local sync in owned fixtures with controlled Git: repairs and
project files retained, ordinary files copied, inputs unchanged, scratch removed.
Run just these cases with:

```bash
python3 scripts/probe_handoff_census.py --only-scaffold
```

`SEAM-INTEGRITY` then guards all of it by asserting **behaviour rather than presence** — every
current tracked acceptance box must match a declared evidence signature, and the two gates
must still agree on what an instrument is. That last rule is the structural one: the divergence between those two
lists refused honest evidence three times before it was fixed rather than patched.

## Adding one

Write `scripts/check_<name>.sh` — cheap, deterministic, read-only, self-describing, nonzero on
breach. Register it: universal checks in the driver's array, project checks in
`scripts/check_doctrines.project.sh`. Mirror it in `DOCTRINE_ENFORCEMENT.md`. Never hardcode a
project's paths or tool names into a neutral check — that is what the `.doctrine/` seams are
for, and the difference between adopting a portable standard and forking someone's workflow.

## Reading sealed history

See [task trees and historical retrieval](task-trees.md#reading-sealed-history) for
the complete changelog and task-history read procedures.
