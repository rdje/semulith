# CHANGELOG.md

## SEMULITH-MIR-0025 (leaf MIRROR-DRIFT.4) — re-derive the counts the live docs carry

**What changed.** `MIRROR-DRIFT.1`–`.3` gated what live documents say about *task-trees*. They
said nothing about any other countable population, and the gap closed itself in the most
convincing way available: **within one working session this repository committed two such numbers
wrong.**

- `LIVE_STATUS.md` claimed `24 destinations governed`; the registry held **25** rows — stale since
  `SEMULITH-P0-0013` added the `profiles/` row.
- It claimed `107 self-test arms`; the real total was **112**.

Neither was a typo. Both were maintained as **running totals** — take the number already written
down, add what you just contributed, write the sum back. ⭐ *A running total is a memory of a
measurement, not a measurement*, and nothing recomputed either one.

- **New doctrine `DERIVED-COUNTS`** (`scripts/check_derived_counts.sh`): routed destinations,
  registered doctrines, book chapters and self-test arms are each re-derived from the population
  they summarise. `--list` prints every covered claim, its enumerator and its current value, so a
  claim and its producer travel together. Scope comes from the routes registry's `hot_live` rows,
  so history is never rewritten.
- **It caught its own registration.** Adding the doctrine made the repository hold nine project
  doctrines where the page said eight, and the gate blocked the commit until the number was
  re-derived rather than incremented.

⛔ **The first cut was wrong in the worst possible direction and a GREEN arm found it.** Extraction
used `sed -nE "s/.*${pat}.*/\1/p"`, whose leading `.*` is greedy: on `12 widgets` it consumed the
`1` and captured `2`. A drifting count could have read as a matching one — a gate reporting
agreement about the wrong number. Extraction is now taken off the front of a `grep -o` match, and
a pattern that does not begin with its `([0-9]+)` group is refused rather than parsed.

**The `TASK-ACCEPTANCE` recipient-tree boundary is documented, not relaxed.** That gate requires
every staged `docs/tasks/*.md` to carry a ticked checklist and cannot distinguish the leaf that
*owns* a change from a tree that merely *receives* a routed finding. The obvious fix — require
only one staged leaf to pass — was rejected: it reopens the measured "co-staged unrelated leaf
supplies the evidence" hole that box-scoping was hardened to close. The workflow instead is that a
routed annotation lands as its own doc-only commit, which is also independently better because the
annotation stays separately revertible.

**Validation.** `--self-test` → `10 pass / 0 fail` (8 RED arms), 10 written and 10 run. Fired RED
on the real corpus before the repair and green after. Gate green; `make check` `1 passed`; book
renders; `scripts/run_smoke.py` still `ok`, so the P0 evidence path is undisturbed.
Tree `MIRROR-DRIFT` complete at 4/4.


## SEMULITH-P0-0023 (leaf P0-PROFILE.7) — the independence inventory, and the 184 files that are the same file

**What changed.** `P0-PROFILE.6` recorded that two models agree over 15 aligned steps. That
sentence is worth exactly as much as their independence, and nothing had examined it. Six pairs
are now inventoried per subsystem, across four verdict classes.

| Subsystem | Pair | Verdict |
| --- | --- | --- |
| instruction encoding | sail ↔ spike | **not shared** |
| floating point | sail ↔ spike | **shared** |
| integer semantics | sail ↔ spike | no evidence of sharing |
| expected-result derivation | act4 ↔ sail | **shared** |
| all | qemu ↔ sail, qemu ↔ spike | **not examined** |

⛔ **The headline: the two models run the same floating-point source.** Both vendor Berkeley
SoftFloat — Sail Release 3e (326 files), Spike Release 3d (263). Of the 199 `.c` files present in
both copies, **184 are byte-identical** once the release-number comment is normalized;
`f64_add.c` differs by exactly one line. A Sail-versus-Spike floating-point comparison executes
one implementation twice. **Nothing currently held is affected** — this profile declares no
floating point — so it is routed to `P4-SYSTEM.7` with the measurement, and recorded in
[`reference_softfloat-shared-ancestry`](docs/decisions/reference_softfloat-shared-ancestry.md).

⭐ **The encoding row cuts the other way, and was not anticipated.** Spike generates `encoding.h`
from `riscv-opcodes` (`c1d9bdf`); the Sail model hand-writes 59 files of `encdec` mappings and
never mentions `riscv-opcodes` under `model/`. Our assembler takes its encodings from
`riscv-opcodes` — so it shares an ancestor with Spike and **not** with Sail, which makes Sail
decoding our bytes an independent confirmation and Spike doing so not one. Independence is a
property of a pair and a subsystem, never of a tool.

⛔ **An instrument answered blind and nearly became a finding.** `strings | grep -ci softfloat`
returned `0` for *both* binaries. `nm -a` showed why that was blindness: Spike carries 649,743
symbols and 495 softfloat-shaped ones; the Sail release binary carries 400 symbols in total. The
source was cloned instead — at `29e6158`, the exact commit the binary's own `--build-info` names.

**New gate rule with real teeth:** an experiment may not compare two models whose independence has
never been examined. Fired RED on the real dossier: `UNEXAMINED PAIR rv64i-lab-v0/smoke-arith …
'not-examined' is a legal verdict, silence is not`. `--self-test` → `36 pass / 0 fail`, 36 arms
written and 36 run.

**Housekeeping forced by a ceiling, not a preference.** `docs/tasks/P0-PROFILE.md` crossed the
per-part ceiling (73,317 B > 65,536). The completed-leaf evidence was split, unedited, to
`docs/tasks/archive/` — the response the registry's own header prescribes. Verified that this did
not move pressure somewhere ungoverned: `git ls-files` is recursive, so the archive still counts
toward the family aggregate (240,293 B against a 393,216 ceiling).

🔎 `LIVE_STATUS.md` claimed "24 destinations governed" while the registry holds 25 rows and the
gate prints 25 — stale since `SEMULITH-P0-0013`. Corrected. The *class* — a live document
restating a count a registry owns — is not yet mechanized; `TREE-CLAIMS` covers task-tree facts
only. Owner: `MIRROR-DRIFT.4`, opened next.

🔎 **A gate boundary worth reporting.** `TASK-ACCEPTANCE` requires *every* staged `docs/tasks/*.md`
to carry a ticked checklist, which cannot distinguish the leaf that **owns** a change from a tree
that merely **receives** a routed finding. Annotating `P4-SYSTEM.7` with this leaf's measurement
therefore had to land as its own commit, because P4 has not started and ticking its template
would be a lie. The split is correct; the gate's inability to tell the two apart is the defect,
and an author hitting a gate's boundary is the highest-signal report that gate can receive.


## SEMULITH-P0-0021 (leaf P0-PROFILE.6) — run the matched-profile experiment, and the control that makes it mean something

**What changed.** `G0`'s second criterion — *an actual evidence path works* — is met. Two guest
programs run on two independently built reference models configured to the same profile, agree
with each other and with values derived from the specification, and reproduce byte for byte.

| Experiment | Exercises | Result |
| --- | --- | --- |
| `smoke-arith` | `LUI` sign-extension, the `*W` family, 6-bit **and** 5-bit shift amounts, wrapping addition | `AGREE over 12 aligned step(s)`; 12 of 12 specification-derived values match |
| `smoke-trap` | a misaligned 4-byte load (`D-MISALIGN-DATA`) | `AGREE over 3`, including cause `0x04`, `tval 0x80000401` on both |

- `scripts/riscv_asm.py` — an RV64I assembler and ELF writer that reads its encodings from the
  pinned tables and **carries no opcode of its own**, so a typo cannot invent an instruction.
- `scripts/compare_traces.py` — first-divergence comparison with a versioned exception adapter
  grounded in the pinned cause table. Ships 8 self-test arms.
- `scripts/run_smoke.py` — the whole path in one command.
- Tracked guest sources, and `smoke-arith.expected.toml`: 12 expected values, each with its
  derivation and its source locator, **written before the program was run**.
- `PROFILE-CONSISTENCY` gains 4 rules — an experiment claiming agreement must name the control
  that was observed failing.

⭐ **The control is the point.** Two models agreeing is a weak result until the agreement is shown
to be doing work. Flipping the Sail configuration's misaligned policy back to "handled invisibly"
— same ELF, nothing else changed — produced `FIRST DIVERGENCE at aligned step 2`: one model
loaded, the other trapped. The models agree *because* the profile is matched, and that is now a
measurement. It also resolves `OQ-3`: the laboratory's contained-trap choice is expressible in
the reference's configuration, so no comparator normalization is needed.

⛔ **The comparator was caught reporting a false pass, by running it.** Comparing only the
overlapping prefix, it printed `AGREE over 2 aligned step(s)` for a run in which one model trapped
and the other stopped emitting records. A shorter trace is now a non-agreeing verdict that must be
explained. Promoted to
[`docs/knowledge/a-shorter-trace-is-not-agreement.md`](docs/knowledge/a-shorter-trace-is-not-agreement.md).

⛔ **The pinned specification does not contain instruction encodings.** Measured: zero seven-bit
patterns across all six pinned artifacts; the format diagrams are images (31 in the RV32I chapter
alone). The semantics are all there in prose — the half that matters for expected values — so
encodings come from a separately pinned `riscv-opcodes`, recorded as its own provenance. That
source is upstream of both models, so encoding agreement is **not** independent evidence.
⭐ It contains exactly **52** instructions for this profile's extension set, and `P0-PROFILE.1`
enumerated exactly 52 by hand from the prose without using it. Symmetric difference: none.

**Four differences enumerated, not smoothed over.** Spike refuses an ELF with no section header
table while Sail loads it; Spike runs a built-in reset vector before the entry; Spike emits no
commit record for a trapping instruction; Sail performs two 16-bit fetch reads per 32-bit
instruction.

⚠️ **Scope, stated plainly.** This is evidence for *these inputs on these two models*. It is not
universal trace inclusion, and two models with shared ancestry can agree while both are wrong —
which is why `P0-PROFILE.7`, the independence inventory, is now the frontier.

**Validation.** `scripts/run_smoke.py` → all checks PASS. Two controls fired RED (un-match the
profile; falsify one expected value). `compare_traces.py --self-test` → `8 pass / 0 fail`, 8
written and 8 run. `check_profile_consistency.sh --self-test` → `30 pass / 0 fail`, with
`NO CONTROL` fired RED on the real dossier. Gate green; `make check` `1 passed`; book renders.


## SEMULITH-P0-0020 (leaf P0-PROFILE.5) — obtain three reference models and pin exactly which they are

**What changed.** The project had a subject and no second opinion about it. It now has three
reference models, obtained and run on this host, each configured as close to `rv64i-lab-v0` as it
can be, and each pinned so the next reader knows exactly which binary produced a number.

| Candidate | Status | Matched by | Self-report |
| --- | --- | --- | --- |
| Sail RISC-V 0.14 (prebuilt `Mac-arm64`) | obtained | a tracked JSON override | `rv64i_zvl32b` |
| Spike 1.1.1-dev (source build `1e05ddac`) | obtained | `--isa=rv64i --priv=m` | `rv64i` |
| QEMU 11.1.1 (pre-existing host toolchain) | obtained | `-cpu rv64i` | emits none |
| ACT, `act4` branch | reachable, **not acquired** | — | — |

- `profiles/rv64i-lab-v0/references.toml` — the dossier: 4 candidates, 3 recorded attempts.
- `profiles/rv64i-lab-v0/reference/sail-rv64i-lab-v0.override.json` — the tracked matched profile.
- `scripts/fetch_references.sh` — acquires and re-verifies, entirely on the repository volume.
- `PROFILE-CONSISTENCY` extended with 13 rules for the dossier, including one that **refuses a
  candidate with no `lineage`**.
- `docs/decisions/decision_reference-acquisition-route.md` supersedes the roadmap's cost estimate.

**The budget was wrong in the project's favour.** The plan priced this on building Sail through
an OCaml/opam toolchain. Release 0.14 publishes a native binary for this host's architecture, so
Sail became the *cheapest* candidate. Spike built against the system toolchain with no new
dependency installed; QEMU was already present and offers a CPU model named `rv64i`.

⛔ **One attempt failed and it is the instructive one.** The host package manager's `sail` formula
is a CLI for deploying WordPress sites to DigitalOcean — an exact name collision. The lookup
succeeded; the referent was wrong. Promoted to
[`docs/knowledge/availability-is-not-identity.md`](docs/knowledge/availability-is-not-identity.md).

⛔ **Two profile/reference differences are enumerated, not rounded away.** Sail cannot be
configured to exactly `extensions = []` — from 96 supported extensions it bottoms out at
`rv64i_zvl32b`, a vestigial minimum vector-length class instantiated even with the vector unit
disabled. And Sail **will not emit its effective configuration**: `--print-default-config`
ignores `--config-override` and the dumps are byte-identical, so the effective configuration is
*(default) + (our tracked override)* and that merge is ours, not the model's account of itself.

⛔ **Three models is not three opinions, and this commit claims neither usability nor
independence.** ACT derives its expected results from a configured Sail model. Spike and QEMU are
*plausibly* independent — a hypothesis. `P0-PROFILE.6` decides usability by running an
experiment; `P0-PROFILE.7` examines ancestry per subsystem.

**Validation.** `scripts/fetch_references.sh --verify-only` → six re-derivations, all `MATCH`,
`rc=0`. Fired RED on two controls: a corrupted digest → `DIFFERS spike binary`; re-enabling `M`
in the tracked override → `DIFFERS matched-profile ISA string … pinned rv64i_zvl32b actual
rv64im_zvl32b`. The 13 new dossier rules fired RED **on the real dossier**: `NO LINEAGE …/qemu`
and six `UNEARNED OBTAINED …/act4`. `PROFILE-CONSISTENCY --self-test: 26 pass / 0 fail`, 26 arms
written and 26 run — and the same reconciliation was run across every project harness (`9/9`,
`7/7`, `12/12`, `26/26`, and `9/9` on seam-integrity's own idiom), so none is skipping arms.
Gate green; `make check` `1 passed`; `make book` renders.


## SEMULITH-MIR-0019 (leaf MIRROR-DRIFT.3) — gate the live documents' tree claims

**What changed.** The third and last mirror on the resume path. `MEMORY.md` and `LIVE_STATUS.md`
state facts that `docs/tasks/` owns — how many leaves a tree has, how many are done, which tree
is active, which leaf is next. Thirteen such claims, held by zero instruments.

- **New doctrine `TREE-CLAIMS`** (`scripts/check_tree_claims.sh`): leaf totals, done counts, the
  frontier leaf and the set of active trees, all re-derived from the trees.
- **Its scope is data, not a list.** It reads the `hot_live` rows of `doctrine/readme_routes.tsv`,
  so a live surface registered tomorrow is covered tomorrow with no edit to the script — and
  `append_history` files are excluded deliberately, because a changelog line reading "2 of 9
  leaves" was true when it was written and rewriting it would corrupt the record.
- **Tree `MIRROR-DRIFT` closed, 3 of 3.** Index, doctrine documents and live docs are all gated.

**Validation.** This leaf had **no drift to repair** — the census at `.1` predicted it and the
gate confirmed it: `TREE-CLAIMS: ok (3 live document(s) …)`, `rc=0`. A mirror that happens to be
correct today is not a checked mirror, so the falsification came from breaking the real documents
on purpose and watching each control fire: `COUNT DRIFT MEMORY.md: '2 of 9 leaves' for
MIRROR-DRIFT; the tree has 2 of 3`; `DONE FRONTIER … the tree records it 'done'`;
`MISSING ACTIVE MEMORY.md: 'P0-PROFILE' is 'active' and the pointer does not name it`;
`COUNT DRIFT LIVE_STATUS.md: '13 leaves' for P1-LAB; the tree has 12`. Each restored.
`--self-test` → `12 pass / 0 fail`, 12 arms written and 12 run.

⭐ **The gates now catch each other.** Registering `TREE-CLAIMS` without adding its rows to the
two doctrine documents failed immediately — `NOT MIRRORED … 'TREE-CLAIMS' is registered and has
no row`, in both — which is `MIRROR-DRIFT.2`'s gate catching `.3`'s omission inside the same
commit. The identical omission had previously survived two registrations unnoticed.

⛔ Two of this leaf's own instruments were corrected by other gates rather than by review. A
first cut of the frontier rule matched any line *mentioning* "frontier leaf" and fired twice on
`MEMORY.md`, once on the pointer and once on a sentence describing it — a rule that fires on
prose teaches its reader to re-word the prose, so it is now anchored on the label, and the
narrowing was re-fired RED to prove it had not been disabled. And `SEAM-INTEGRITY` refused this
leaf's `ADDRESSED` box for carrying an assertion instead of a command; the box now carries the
census and its output.


## SEMULITH-MIR-0018 (leaf MIRROR-DRIFT.2) — gate the doctrine documents against the registry

**What changed.** Two documents restate the doctrine registry that lives in two shell arrays:
`DOCTRINE_ENFORCEMENT.md`, which calls itself "the human-readable mirror of the enforcer
registry", and the mdBook chapter `docs/book/src/working/doctrines.md`. Nothing compared either
with the arrays, and the book had fallen behind: it listed **3** project doctrines while **5**
were registered and running.

- **New doctrine `REGISTRY-MIRROR`** (`scripts/check_registry_mirror.sh`). Every registered id
  has a row in both documents; every id-shaped row is actually registered; project doctrines sit
  under the project heading and universal ones do not; every registered path exists and is
  executable; and a sentence of the form `<N> checks run today` states the real universal count.
  The **registry is authoritative**, and the failure text says so.
- **The book chapter repaired and grown.** The three missing rows added, plus two new sections
  that document the family honestly: which mirrors drifted, in which direction, and why a gate
  was chosen over a generator.
- **The silent-arm-swallow found at `.1` is now caught, not just written down.** Both self-test
  harnesses gained a strict-arity guard on every fixture helper, so a missing `;` before an `arm`
  call fails the self-test instead of deleting it.

**Validation.** Fired RED on the real documents before the repair — three `NOT MIRRORED`
findings, `rc=1` — and green after: `REGISTRY-MIRROR: ok (2 document(s) mirror the registry)`,
`rc=0`. The gate also fired in the **opposite** direction unprompted, catching a book row added
one step before its registration: `PHANTOM doctrines.md: 'REGISTRY-MIRROR' has a row but is
registered nowhere`. A document promising a gate that does not run is the more dangerous drift,
and it was caught on the real corpus.

`--self-test` → `11 pass / 0 fail` (10 RED arms plus a refusal arm asserting `rc=2`), with arms
written (`11`) reconciled against arms run (`11`). The new `argc` guard was fired RED by
deleting one `;`: `index() got 6 argument(s), expected 2`, `15 pass / 1 fail`, restored to
`16 pass / 0 fail`. Whole gate `all doctrines green`; `make check` `1 passed`; `make book`
`HTML book written`.


## SEMULITH-MIR-0017 (leaf MIRROR-DRIFT.1) — gate the task-tree index against the trees

**What changed.** `docs/TASK_TREE.md` is a hand-kept mirror of the task-trees under
`docs/tasks/`, updated by a *conditional* step in `COMMIT.md` ("only if the frontier changes")
and compared with its source by nothing. It had drifted: the index named `P0-PROFILE.2` as the
next leaf while the tree named `.5`, and `.2` was already `done`. One row of fourteen — and the
one that rotted was the only `active` tree, which is the only row the documented resume path
(`MEMORY.md` → the index row → the tree's frontier) ever reads.

- **New doctrine `FRONTIER-SYNC`** (`scripts/check_frontier_sync.sh`, registered in the project
  slot). It compares six properties, all of them functions of the tree: the frontier leaf, that
  neither document points at a `done` leaf, the status cells, any `A/B leaves complete` or
  `A of B leaves done` count, index↔tree closure in both directions, and that every leaf id
  named actually exists. The **tree is authoritative** and the failure message says so, because
  editing a summary to match its record is safe while editing the record to match its summary
  destroys the evidence.
- **New task-tree `MIRROR-DRIFT`** — every hand-kept mirror of a machine-readable source is
  gated. `.1` done; `.2` (the doctrine documents vs the enforcer registry) and `.3` (the live
  docs' derived numbers) are scoped with their measurements already taken.
- `DOCTRINE_ENFORCEMENT.md`'s project-doctrine table was split into three GFM fragments by two
  stray blank lines, so two registered doctrines rendered as literal text rather than rows.
  Repaired; the table now holds all six.

**Validation.** `check_frontier_sync.sh --self-test` → `16 pass / 0 fail` (14 RED arms, each
asserting the reason, plus two arms that assert `rc=2` refusal rather than a silent pass). Fired
RED against the **real** index before the repair — `FRONTIER DRIFT P0-PROFILE: index says '.2',
tree's Current Frontier says 'P0-PROFILE.5'`, `rc=1` — and green after:
`ok (15 tree(s) mirrored by docs/TASK_TREE.md)`, `rc=0`. Whole gate `all doctrines green`,
`rc=0`; `make check` `test result: ok. 1 passed; 0 failed`.

⛔ **The self-test lied first.** Its opening run printed `4 pass / 0 fail` while executing four
of fourteen arms: ten `arm` calls shared a physical line with the fixture call before them, so
bash handed them to a function that reads `$1`/`$2` and discards the rest — silently. Adding the
separator gave `13 pass / 1 fail`, and that failure was a genuine defect in the gate. Promoted
to [`docs/knowledge/self-test-arms-that-never-ran.md`](docs/knowledge/self-test-arms-that-never-ran.md).

⚠️ The mdBook's doctrine chapter is knowingly **not** updated by this commit. It already omitted
two registered doctrines; adding this one by hand would repair the symptom and destroy the
evidence `MIRROR-DRIFT.2` needs, whose acceptance requires firing its gate RED on the real
drift. Owner: `MIRROR-DRIFT.2`, the next commit.


## `SEMULITH-PKG.8` — the spine defects are fixed at source, and the fix is watched

- ⛔ **The `.doctrine/` seam fixes failed open.** Both seam files moved aside, full enforcer
  re-run: `=== all doctrines green ===`, `rc=0`. Three repairs silently reverted and nothing
  said a word. *A fix whose disappearance is undetectable is not a fix; it is a configuration
  that happens to be present.* Worse, both repaired checks were on `update_scaffold.sh`'s
  re-sync list, so a scaffold update would have reverted a source fix too.
- **Repaired in `scripts/check_task_acceptance.sh`:** `src/` anchored to the repository root (a
  root `src/` is a source tree; one inside a docs tree is not); `^\.githooks/`,
  `^\.github/workflows/` and `^Cargo\.(toml|lock)$` added; and `CENSUS_RE` **imported** from
  `check_gap_claims.sh` so the two gates share one vocabulary by construction — 19 instruments
  the acceptance gate previously refused.
- Proven with the seams removed, so only the source fixes are in play: prose classified as code
  `0` (was 28), behaviour families `6/6` (was 0), census instruments `5/5`.
- Both repaired checks removed from `update_scaffold.sh`'s `NEUTRAL` list, reason recorded.
- Added **`SEAM-INTEGRITY`**, which asserts **behaviour, not presence**: 68 already-committed
  acceptance boxes must still be accepted, prose must not be code, behaviour families must be,
  and the two gates must agree on what an instrument is. It catches a deleted seam, a narrowed
  pattern, a scaffold overwrite, or a spine update that stops consuming the seam.
- The acceptance gate now prints its own effective rules (`--print-sig`, `--print-code-re`) so
  no sibling re-implements them — added after this leaf's own check mirrored the composition by
  hand and scored against a stale copy of it.
- ⛔ **Three defects in this leaf's own work were caught by its self-test, not by review**: an
  arm whose pattern was mangled by `bash -c` quoting, a fixture holding the literal text `\n`
  instead of newlines, and the mirrored composition above. The first two reported PASS while
  asserting nothing.


## `P0-PROFILE.2` — the state inventory, and a census for its "none"

- `state.json` records 32×64-bit integer registers, `x0` hardwired zero, and `pc` — and then
  does the part that matters: it **enumerates seven candidates for hidden state and shows each
  absent**. CSRs, the reservation set, floating-point and `fcsr`, vector state, privilege and
  trap state, instruction-fetch cache state, pending or partially committed effects.
- ⭐ *"No hidden state"* is only true **because of what the profile excludes**, so the census
  records the reason per candidate. A caching fetch implementation *would* have hidden state
  there and would still be architecturally legal without Zifencei.
- Reading the sources for the inventory surfaced **three architectural rules leaf `.1` had
  missed**: the address space is circular and address computation wraps modulo 2^XLEN; every
  executed instruction entails an implicit fetch read; and the fetch-accessible and
  load-accessible sets may differ, with the choice delegated to the EEI. Five decisions added,
  taking the profile to 25 (14 architecture, 8 execution-environment, 3 laboratory).
- The reset claim is **measured, not assumed**: `grep -ci reset` over the pinned chapters →
  `rv32.txt:0`, `rv64.txt:0`. Reset values for `x1..x31` are a laboratory declaration and are
  labelled one.
- Register **ABI names are software convention, not architecture**. Only the three roles the ISA
  chapter itself names are recorded; the rest belong to the calling-convention document, which
  has not been fetched, so they are absent rather than assumed.
- `PROFILE-CONSISTENCY` extended: `state.json` must agree with `profile.toml` on id, XLEN and
  register count, and an **empty `hidden_state` with no census is refused** — `GAP-CLAIM-CENSUS`
  applied to data rather than prose. Both new rules fired RED on the real dossier.
- ⛔ `TASK-ACCEPTANCE` refused this leaf's own evidence for the **third** time, on `grep -ci`.
  The first two fixes were additions that each held until the next new thing existed; this one
  aligns the acceptance gate with the census gate's own accepted instrument list. A list that
  must be edited whenever a sibling file changes is a list that will be stale — if you are
  declaring a token for the third time, the declaration is the wrong shape.


## `P0-PROFILE.1` — the project has a subject: `rv64i-lab-v0`

- **The specification is acquired and pinned, not cited.** `docs/SOURCES_AND_NAMING.md` listed
  candidate URLs, which `SRC-03` refuses to treat as established availability. Reachability was
  established first (`HTTP 200`), then three artifacts were fetched and fingerprinted:
  `intro.html` `3d65f713…`, `rv32.html` `3b20e92f…`, `rv64.html` `6eadb316…` — all three
  re-derived by `scripts/fetch_sources.sh --verify-only` as `MATCH`.
- `profiles/rv64i-lab-v0/` records **20 decisions**, each with a statement and a source locator,
  split by **authority**: 12 `architecture`, 6 `execution-environment`, 2 `laboratory`. That
  field is the load-bearing one — a laboratory policy over an `UNSPECIFIED` case must never read
  as an architectural rule, or a reference that chose differently is recorded as a defect.
- Instruction scope **enumerated, not counted from memory**: 40 base + 12 RV64I additions = 52,
  and the agreement is now gated rather than checked once.
- Added **`PROFILE-CONSISTENCY`**: declared counts must equal the enumeration, and every
  decision must carry an authority and a source. 8 self-test arms; fired on the real dossier
  (`COUNT DRIFT … enumerates 51, count_total = 52`).
- Added `scripts/fetch_sources.sh`, deliberately **not** a commit gate: it needs the network,
  and a gate that fails for reasons unrelated to the change is a gate people bypass. Its ledger
  states plainly what a digest does and does not pin — the rendering, not the normative text.
- ⛔ That tool's own RED control exposed a defect in it: an unanchored `sed` capture left a
  trailing comment in `work_dir`, so the fetch wrote into a directory literally named
  `…riscv-v20260120   # repo-volume, untracked` **while reporting three green MATCHes**. A
  verdict can be correct about the bytes and wrong about where it read them.
- The README's own health target had been set *at* today's size and fired on the very row this
  leaf added — the miscalibration `SEMULITH-TREES.4` documented, committed in the file that
  documents it. Re-set between the reviewed page and its untouched ceiling.


## `SEMULITH-TREES.4` — the task-tree family is bounded per part, not only in aggregate

- Bounds written for a three-tree repository were governing an eleven-lane one: `docs/tasks/`
  measured `17` files / `133,074` bytes against a `65,536` health target set at 5 files /
  39,131 bytes, with one member (`SEMULITH-PKG.md`) at `35,395`.
- Added **`ceiling_part_bytes`**, the ninth registry column. `README_POLICY.md` requires a
  partitioned family to carry per-part, file-count **and** aggregate ceilings; only the last two
  existed, so one member could become the monolith the split was meant to avoid, invisibly.
  Fired on the real corpus: it named `docs/tasks/SEMULITH-PKG.md` at `35395 > 20000`.
- ⭐ **Health targets are calibrated by lifecycle.** A *hot/live* surface's target sits just
  above today's reviewed size, because unexpected growth is the signal. An *append_history*
  surface's belongs near its ceiling, because growth is expected and the only useful warning is
  that the shard threshold is approaching. `CHANGELOG.md` crossing a 24 KiB target within a day
  was a miscalibrated instrument, not a finding; it and `DEV_NOTES.md` moved to 75% of their
  ceilings, which were not touched. Four health warnings became zero.
- The per-part control exposed a defect in itself: it first printed an **absolute** path, which
  `DOCPATH` would refuse inside a task leaf — so an author pasting this tool's output as
  evidence would have been blocked by a different gate for a defect in this one.
- The book's task-tree chapter now includes the live tree index by mdBook anchor, so the map of
  who owns which lane cannot drift from `docs/TASK_TREE.md`.
- `.doctrine/evidence_tokens.txt`'s enumerated list of doctrine names had fallen behind the
  registry for the second time, refusing this leaf's own honest evidence. It is now the
  **shape** every gate prints rather than a list of their names — verified against five real
  verdict lines, and fired RED afterwards to confirm the generalization did not make the gate
  vacuous.


## `SEMULITH-TREES.3` — every roadmap lane now has an owner

- Five trees created and registered: **`P5-BOARD`** (7 leaves, gate `BOARD`), **`AG-OS`**
  (8 leaves, gate `ARCHOGEN-OS`), **`P6-LINUX`** (8 leaves, gate `LINUX`), **`P7-COMPUTER`**
  (7 leaves, gate `SYSTEM`), **`MC-MULTICORE`** (7 leaves, its own gate). Milestone-tree
  census: `6` → `11` — every lane of `ROADMAP.md` §6 is owned.
- `AG-OS.1` is deliberately *"inspect the real eADL and plan interfaces"*: no eADL grammar or
  typed API has been supplied, so designing the adapter first would design against a guess.
- `AG-OS.6` pre-commits the shared-trust inventory: if the hosted playground reuses Semulith
  device transitions, their agreement is shared-model evidence, not an independent hardware
  comparison. Semulith does not become independent by being a separate project.
- `MC-MULTICORE.5` is written so that **silence is the honest state**: if the weak-memory
  exploration leaf is not done, the project does not claim weak-memory coverage.
- `P5-BOARD.4` makes an unmatched CPU assumption a **rejection** of the composition rather than
  a note, which is what keeps the CPU-first ordering meaningful once integration bugs appear.


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
