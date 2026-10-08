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
native check builds all registered books; Linux execution remains a hosted obligation.
CI-RECOVERY.3 repairs cold output/provisioning paths and truthful portability verdicts.
Its native and big-endian interpreted core runs each pass all 153 tests; full local CI
also passes on Rust 1.99. Hosted green still requires a successful run on a permitted push. A local green result alone cannot close that obligation.

The director has approved the pushes needed for this CI recovery without asking
again (`decision_ci-recovery-push-approval`). Every push still uses
`scripts/approved_push.sh`: full local CI, a committed approval record, then the
guarded push. When all three workflows pass on the repaired pushed revision, this
exception expires and the normal cadence resumes.

The first authorized recovery push is `f4364bc`: both required local full suites
passed, and the approval record traveled in that commit. Hosted Rust, both native
portability hosts and their manifest agreement pass. The doctrine job provisions
mdBook, then refuses a GUEST-GEN self-test whose diagnostic was hidden by its wrapper;
interpreted portability is still running. CI-RECOVERY.4 owns the unresolved refusal
and exact run URLs. Hosted success remains pending.

GUEST-GEN now retains the full self-test output in `target/guest-gen/self-test.log`,
prints the interpreter version and a bounded tail on failure, and keeps its refusal
exit code. A failed doctrine job publishes that log as an artifact. The local controls
still pass; this visibility repair does not assert that the hosted cause is fixed.

Handoff has a separate process census: `scripts/check_no_background_jobs.sh` counts
open repository file handles, including read-only editor handles. A refused census
remains visible even when verification jobs have finished. Closing another editor
requires appropriate authority; a standing exemption requires the director's ruling
in `doctrine/sanctioned_processes.tsv`. An exemption changes the handoff census only;
tracked-content gates remain enforced.

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
| `README-ROUTING-CLOSURE` | every destination the landing page routes to is governed, exists, and stays under its ceiling — the per-part ceiling two-tiered: authored members are bounded, regeneration-gated derived members are exempt as a checked property (a fact-ownership mirror row with a regeneration governor), reported as proof |
| `PROFILE-CONSISTENCY` | a profile dossier's declared counts equal its enumeration, and every decision carries an authority and a source |
| `SEAM-INTEGRITY` | this project's repairs to the neutral checks still *do their job* — asserted as behaviour, never as presence |
| `FRONTIER-SYNC` | `docs/TASK_TREE.md` still names the leaf the tree itself calls next, and every tree has exactly one row — the index while open, `docs/TASK_TREE_CLOSED.md` once done |
| `REGISTRY-MIRROR` | these two tables still list exactly the doctrines the drivers register |
| `UPSTREAM-INDEX` | a defect raised against a dependency is tracked like our own: each issue is a self-contained subtree under `docs/upstream/` whose `issue.sexp` owns its id, severity, state and dated history, and every index of it is a checked mirror — because self-containment and a second source of truth cannot both hold |
| `TREE-CLAIMS` | every live document's leaf counts, active trees and frontier leaf match `docs/tasks/` |
| `DERIVED-COUNTS` | every count a live document states about an enumerable population is re-derived |
| `RECORD-SCHEMA` | every record file validates on its track (JSONL by schema, catalogues by the schema layer), cites only pinned sources, and states what its profile states — the JSONL track on two engines, the tracked Python validator and the workspace's Rust graph checker (`P1-LAB.7`), which re-derives the PACKAGE_CHECKS rows and enforces the §3 graph invariants over the examples bundle |
| `GATE-REPORT` | the tracked gate report is still what the generator derives from its inputs |
| `SHARD-FREEZE` | live and archived history is frozen and whole: authenticate live SHA rows and sealed objects/descriptors; preserve every predecessor logical row; refuse changed descriptors, unsafe paths, corrupt/oversized data and duplicate headings/locations across both heads and all history |
| `PORT-WEB` | the crate skeleton builds for the browser target — the workspace compiles for `wasm32-unknown-unknown`, so a host-only API cannot slip into the engine unnoticed |
| `STATE-GEN` | the generated state module is still what the state descriptor generates — drift is refused, and the generator refuses shapes it cannot emit rather than silently guessing |
| `DEF-GEN` | the generated definition module is still what the canonical definition generates — decode tables, lowered semantics trees, and the OWN-03 manifest with definition, generator, configuration and source fingerprints; drift is refused, the generator refuses shapes it cannot emit rather than silently guessing, and a check that cannot judge refuses rather than passing |
| `GUEST-GEN` | the generated guest fixture is still what the tracked guests and their specification-derived expectations generate — assembled bytes plus EVD-05 expectation data as one fixture the offline differential re-runs on every commit; drift is refused, the generator refuses a guest it cannot reconcile rather than silently guessing, and a check that cannot judge refuses rather than passing |
| `BOARD-GEN` | a board's composition manifest, composed catalogues, hardware description and human-readable map are still what the canonical board definition generates (`scripts/gen_board.py`; OWN-05 — no handwritten duplicate map anywhere); drift is refused with the regeneration command, the generator refuses by name an inconsistent definition (a region overlap, an mmio window with no device, an executable mmio region), and a check that cannot judge refuses rather than passing |
| `BOARD-VERDICT` | a board's composition verdict is decided, not narrated (CPU/environment contract §5, ENV-02) — every CPU environment-assumption in the composed unit is discharged by named guarantees, every `satisfies` edge in the board definition resolves to a discharged assumption, and every device obligation the dossier defers to the board is answered by exactly one decision `answers` edge; an unmatched assumption or a dangling edge is a rejection by name, never a note (`P5-BOARD.4`) |
| `PLATFORM-GEN` | a board's platform capability manifest (`platform.sexp` — the OWN-06 export for a compatibility checker, `docs/ARCHOGEN_INTEGRATION.md` §3) is still what its canonical inputs generate (`scripts/gen_platform.py`: the board definition, the pinned processor's profile, the composed obligations); drift is refused with the regeneration command, and the board's `dossier-sha256` pin is verified against the live dossier at derivation — the pin, measured display-only before this leaf, is load-bearing now (`P5-BOARD.6`) |
| `EXERCISE-COVERAGE` | every form a profile declares in its scope is executed by a tracked guest — coverage reported with its denominator (the count re-derived against the enumeration), the SCP-02 dependency closure resolved through the one shared resolver; the dynamic-exercise half that complements EXTRACTION's static sufficiency; fired RED at 15/52 before registration, GREEN at 52/52 (`P2-SCALAR.1`) |
| `INTERACTION-MATRIX` | the declared interaction matrix (fault × alias × boundary × event × progress × restart) is declared first as tracked data and then exercised — the cells re-derived from the axes, an omitted cell failing by name; every disposition resolves (guest with source and expectations, the closed mechanism registry, degenerate with its reason); no tracked guest is an orphan; every difference id named exists in the reference dossier (`P2-SCALAR.4`; fired RED against the real corpus before registration) |
| `MATERIALS-BILL` | every modelled unit's book carries a materials bill whose identity tables are generated from the pinned dossier (drift refused — a digest cannot rot) and whose prose states for every material what it does NOT supply — a missing section or a missing negative statement fails by name (`MODEL-BOOKS.1`; fired RED against the real corpus before registration) |
| `UNIT-BOOKS` | every registered unit has its own mdBook under `docs/models/` and it builds — a unit without a book, a book that does not build, or a book no unit registers fails by name (`MODEL-BOOKS.6`; fired RED against the real corpus before registration) |
| `DOSSIER-SCHEMA` | every tracked dossier document whose basename or family has a schema validates against it through the one checker — a schema nothing enforces is documentation, not a contract; documents with no same-named schema are skipped and counted by name, never silently (`P3-BREADTH.7`; fired RED before registration against the pre-fix D-FENCE document recovered from git history) |
| `PUSH-RECORD` | the push-approval ledger is append-only (a staged change keeps HEAD's content a prefix) and every entry carries who/when/why/range with sequential ids — a correction is a new entry, never an edit (`PUSH-DISCIPLINE.3`; fired RED against the real corpus before registration) |
| `COMMIT-PREFIX` | the `commit-msg` hook pins the `SEMULITH-` work-unit prefix — a `SEMILITH-` subject is refused with `SEMULITH` named, a `SEMULITH-` subject passes; the probe is behavioural, so a scaffold sync that reverts the neutral hook turns the very next commit RED, named; history carries both spellings and is immutable, so enforcement is forward-looking at the boundary (`PREFIX-DISCIPLINE.1`, director ruling `2026-09-30`; fired RED against the real tree before the pin existed) |
| `SOURCE-FORMAT` | every source of truth the engine extracts from is in the one format — a retired-format file in a source-of-truth family is refused by name, and every `.sexp` there parses with the one reader |
| `UNIT-COMPOSITION` | a unit's composed encoding space is decided — schema-conformant document, fragments resolved through the one shared resolver, collision-free union, and partial compositions declared rather than inferred |
| `SEMANTICS` | the execution authority's corpus holds — every semantics document is well-formed, complete and cited; a silent semantic override across fragments is refused; locators resolve offline, with a named skip when the cache cannot judge |
| `EXTRACTION` | the definition is sufficient for an engine — every declared instruction has an encoding, semantics and a requirement (one set, four ways); every state element a reset; every obligation its checks |
| `FACT-OWNERSHIP` | the no-duplicated-fact rule holds — one owning file per fact kind, every mirror governed, every restatement the corpus has is registered |
| `SCOPE-COVERAGE` | no model code against an uncovered scope — a required category missing or absent refuses; P1-LAB's precondition |
| `BOOK-INDEX` | the book's index is still what the book's own text derives — regenerated byte-exact from `SUMMARY.md`, the canonical glossary, and the chapters; a hand-maintained index is a running total, and a running total is a memory of a measurement, not a measurement (`BOOK-APPARATUS.1`; fired RED against the real book before registration) |
| `CITATION-QUOTES` | a quoted phrase that a tracked source-of-truth file attributes to a section of a pinned specification page really occurs in that section — `RVI-F §20.1.1` can exist and still be the wrong place for the sentence quoted under it; the refusal names the section where the sentence actually is. Quotes only (paraphrase stays a reviewer's question); judged when the pinned pages are on disk, a named skip otherwise |
| `FP-VECTORS` | the floating-point model layer's test vectors are exactly what an independent, exact-arithmetic reference written from the specification produces — and that reference is itself re-checked against the computer's own IEEE arithmetic on every run, so a drifted oracle cannot regenerate a wrong table |
| `CONTRACT-FREEZE` | the processor's contract with its environment is kept in numbered versions; once a version is frozen its statements cannot be changed — a statement that turns out wrong is replaced in the next version, and the old one stays on the record |
| `M-VECTORS` | the table of expected multiply and divide results is produced by a program that works them out from the specification, and nobody may edit it by hand — otherwise its expected values could be quietly changed to match the processor instead of the specification; the program itself is checked against the rules the specification states, such as quotient times divisor plus remainder giving back the dividend |

Each ships a `--self-test` whose RED arms assert the **reason** as well as the verdict, each was
fired RED before being registered, and each **refuses** — exit 2, not exit 0 — rather than
passing if its own self-test stops discriminating. A check that cannot judge must never report
that the rule holds.

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

What belongs where is not arbitrary. The anchored `src/`, the three universally
behaviour-governing path families, and the shared census vocabulary are true of **every**
consumer of the template — repairing them in the check is a repair, not a fork. This project's
own gate *data* and *instrument signatures* stay in `.doctrine/`, because a neutral check cannot
know they exist. And both repaired checks were removed from `update_scaffold.sh`'s re-sync list,
so a scaffold update cannot quietly undo them.

`SEAM-INTEGRITY` then guards all of it by asserting **behaviour rather than presence** — every
acceptance box already committed must still be accepted, and the two gates must still agree on
what an instrument is. That last rule is the structural one: the divergence between those two
lists refused honest evidence three times before it was fixed rather than patched.

## Adding one

Write `scripts/check_<name>.sh` — cheap, deterministic, read-only, self-describing, nonzero on
breach. Register it: universal checks in the driver's array, project checks in
`scripts/check_doctrines.project.sh`. Mirror it in `DOCTRINE_ENFORCEMENT.md`. Never hardcode a
project's paths or tool names into a neutral check — that is what the `.doctrine/` seams are
for, and the difference between adopting a portable standard and forking someone's workflow.

## Reading sealed history

Older changelog and development-note shards now have a query-first archive terminal.
The 210 older shards and their manifest retain every byte, but use a tracked immutable
compressed object instead of individual Markdown files. Recent shards and both live
heads remain directly readable. This approved transition restores the live collection's
headroom; sharding alone had left its aggregate at the limit.

```sh
python3 scripts/history_archive.py
python3 scripts/history_archive.py --read docs/changelog/shard-0001.md
```

The first command verifies all identities; the second prints the original shard.
Both work in an ordinary shallow clone without fetching history or extracting files.
The descriptor in docs/history/archives.json names the exact source capture, source
counts and content-addressed object. The archive's SHA manifest authenticates each
member. A missing object, changed descriptor or bad member fails the same unconditional
freeze gate used locally and in CI. Restore the committed bytes when that happens.

The live and archived manifests form one logical partition. Moving a row into the
archive keeps its digest and predecessor identity; it does not delete history. The
gate checks heading uniqueness across both live heads and the complete archive, and
the sharder includes retired filenames when allocating its next number. Thirty-one
positive/negative controls guard these checks. This finite terminal has one object,
a bounded descriptor and a retrieval front door; a later seal needs its own verified
capture and transition. Full containment-doctrine adoption remains owned by
LIVE-CONTAINMENT.4.
