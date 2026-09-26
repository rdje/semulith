# CHANGELOG.md

## SEMULITH-UT-0055 (leaf UPSTREAM-TRACK.4) — the reply travels in the same envelope

Director instruction `2026-09-26`: the verification acknowledgment to LinkedSpec is a
git-tracked note inside the bug's own directory. The subtree was already the envelope a
maintainer copies out — `VERIFIED.md` is now the reply inside that envelope, beside the report
it answers: what shipped, what we re-ran against which pin, the result, what it unblocks, and
where the residue lives (for LS-001: classified under LS-002, not this defect).

The note is gated, not just written: `UPSTREAM-INDEX` refuses a `verified` state whose subtree
carries no `VERIFIED.md`, and refuses a note that does not name the pin the record was verified
against — the note and the record must agree the way the indices and the record must agree.
Fired RED on the real tracker against both LS-001 and LS-003 before the notes existed; 17 arms
(16 → 17) with the wrong-pin refusal; green after, both notes self-contained and pin-consistent.

## SEMULITH-SF-0054 (leaf SOT-FORMAT.1) — the schema language, written in itself

The gap was "it parses": an S-expression reader accepts anything syntactically, so a mistyped
head or field was invisible. `schema/schema.sexp` now declares the language in itself —
`(construct (name …) (field …)…)`, atom fields, form fields in the corpus's two house shapes
(`(source (file …) …)` whole-list and `(effect (set …))` value-held), `(empty yes)` markers
for the corpus's `(requires)`/`(extensions)` idiom, `(values …)` spellings, sibling repetition —
and `scripts/check_sexp_schema.py` (16 arms, 13 RED, each naming its construct, field and
reason) validates any file against any schema. The fixpoint is the proof, not a slogan:
`schema.sexp` conforms to `schema.sexp`.

⭐ The first design assumed a tidy uniform `(name value)` pair grammar — and the real corpus
refuted it before it shipped. Reading `rv64i.sexp`/`rv64i.sem.sexp` first is what made the
language fit the files `.2` must declare; an invented grammar would have met the corpus as an
argument. `schema/` is registered in `doctrine/readme_routes.tsv` in its creating commit, and
`TOOLBOX.md` gains the row.

## SEMULITH-SF-0053 (leaf SOT-FORMAT.8) — the contract names its format at last

The mdBook chapter *"Architecture and canonical definitions"* includes `docs/ARCHITECTURE.md`
verbatim, and that document named no format, no `definitions/` directory and no composition —
four commits had introduced all three, and the director's only window showed none of it
(`grep -c 'S-expression'` → 0). The drift is closed at the source document: §1.1 records the
one-format decision and what exists in it today (fragments, cited semantics at 52 of 52, the
two-reader agreement check), §1.2 defines the fragment and the composition operator that is
*decided, not hoped* (`check_encoding_disjoint.py`), §1.3 states the schema layer's contract and
labels it specified-not-built. Built claims name their instruments; pending layers say pending;
the one count that moves (`5 of 5`) was rephrased to "agreement file by file" so the prose
cannot drift. `make book` builds; the chapter preface needed no edit — that was the point.

Also: a knowledge card for the session's other lesson — a director-named action runs first,
right after context recovery; standing cadences queue behind it.

## SEMULITH-UT-0052 (leaf UPSTREAM-TRACK.2) — `verified` must carry the re-run that earned it

The tracker already refused a `verified` with no pin. It now refuses the next hole too: a
`verified` whose event names a pin but captures no `(repro …)` output **inside the subtree** —
the pin retires upstream's changelog claim, but only the captured run retires ours. Four new
self-test arms (pin-without-repro, artifact missing, artifact escaping the subtree, pin+artifact
accepted); `16 pass / 0 fail`.

⛔ **Fired RED on the real tracker before any artifact existed** — the strengthened gate refused
LS-001's just-committed `verified` ("captures no (repro …) re-run output", rc=1). Then the
evidence landed and every state became earned, not asserted:

- **LS-001 → `verified`** — the reproduction re-ran and was captured into the subtree itself:
  `evidence/verified-a8d34c845.txt`, `8 matched / 0 differed`. A maintainer copying the issue
  directory out now carries the proof with it.
- **LS-003 → `verified`** — the three first-consumer papercuts are remedied in the guide at the
  adopted pin, and each remedy was *exercised* during the pin update (workspace exclusion,
  prerequisite chain, maintained wrapper), transcript captured — exit statuses, not banners,
  per the guide's own warning.
- **LS-002 → `acknowledged`** — upstream took ownership by name: the LS-001 fix commit records
  "LS-002 and related kind/strict requirements remain .83.1 owned". No re-run owed; the design
  question is theirs until it ships.

## SEMULITH-SF-0051 (leaf SOT-FORMAT.9) — the pin moves, the readers agree, the loop closes

Director instruction `2026-09-26`: upstream fixed and pushed the reported bugs, so the LinkedSpec
pin advances `ad290bdb4` → `a8d34c845` (`origin/main` tip, ~120 commits). The update followed the
guide's own flow — fetch, check out the reviewed revision, re-verify, THEN commit the pointer.
RGX stays at `8763a0e6` on both pins (bootstrap: "already generated", a no-op); the consumer
rebuilt in 20.39 s.

**LS-001 is `verified`, not just `fixed-upstream`.** Our self-contained reproduction re-ran
against the new binary and grammar: `8 matched / 0 differed` (was 4/4), and both readers now
agree on **all five** tracked `.sexp` files, including the 43-form catalogue that had read as 6.
The issue record, both index mirrors and the REPORT carry the `verified-against` pin the
UPSTREAM-INDEX gate requires.

**The fix moved the disagreement one layer down, and that layer is enumerated, not hidden.**
The corpus census found exactly four residue atoms in `materials/catalog.sexp`: two
quoted-numeric strings (`"20260911"`, `"1992"` — Lispish discards quote-kind, LS-002) and two
escape-retained strings (`\"` kept verbatim — the guide documents this). Both are CLASS families
in `compare_readers.py` now: each is anchored to exact byte meaning (`sexp._atom(A) == B`
exactly; decoding B with sexp.py's own escape table reproduces A exactly), with 9 new self-test
arms (4 GREEN classification, 5 RED masking) and a fired RED proof — the pre-fix grammar still
makes the comparator report the original 43-vs-6 defect, rc=1. "Agree" still means same structure.

**Named departure, one.** The guide now prescribes copying the consumer source into the
application's crate; semulith builds the vendored example workspace in place (virtual root
manifest has no package to own it) — recorded in the tree, to revisit when the engine adopts the
reader. Upstream's document grammar (SExprDocumentV1, tagged kinds) is the durable answer to both
CLASS families when that day comes.

## SEMULITH-AC-0050 (leaf ARTIFACT-CLEANUP.1) — the first §8 cleanup, measured and recorded

Session-directive §8 requires an artifact cleanup roughly every 24 h, tracked in
`docs/ARTIFACT_CLEANUP.md`. The file did not exist — the "no file → clean this session" trigger
fired — so the cleanup owns a task-tree now, the same as any other change.

**Census before deleting anything** — 22 `.bin` under `target/`, 18 under `.app-data/target/`,
all of them cargo incremental caches in the directive's enumerated scope; 7 crate **source**
fixtures under `.app-data/cargo-home/` (inputs, not artifacts — kept); 13 reference-run logs
under `target/refs/` (kept: evidence trails, 1.3 MB, outside the enumerated cargo dirs).

**Measured, not asserted:** 40 files / 341 MB deleted (`.app-data` 1.4 G → 1.1 G); zero after;
`git status` shows only the intended tracked files. The record is overwrite-only — one date and
one line per run, so the file can never become the changelog it exists to prevent — and it is a
governed live surface from its first commit (registered in `doctrine/readme_routes.tsv`).

## SEMULITH-UT-0048 (leaf UPSTREAM-TRACK.1) — the issue owns its state, the indices are mirrors

**Two director instructions that turn out to be one design.** *"For each vendor keep an index of
all the bugs you reported, their state"* and *"the subtree for each bug shall be self-contained"*
cannot both be satisfied by a maintained index: if the subtree carries its own state, then every
index is **derived**, and a derived thing that nobody checks drifts. That is exactly why
`FRONTIER-SYNC` and `REGISTRY-MIRROR` exist facing inwards. This is the same doctrine facing out.

Measured before building — the same facts in three places, and nothing checking them:

```
$ grep -c 'LS-00' docs/upstream/README.md                      -> 4  rows
$ grep -c 'LS-00' docs/upstream/linkedspec/README.md           -> 5  rows
$ grep -l 'State' docs/upstream/linkedspec/*/REPORT.md | wc -l -> 3  reports
$ grep -c upstream scripts/check_doctrines.project.sh          -> 0  gates
```

**Each issue now carries `issue.sexp`** — the single owner of its id, severity, state, affected
pins, fix status and dated history, living inside the subtree it describes. An S-expression,
because an issue record is a source of truth like any other
(`decision_one-format-every-source-of-truth`).

**`UPSTREAM-INDEX`** (12 arms, 10 of them RED) checks both indices and each `REPORT.md` against
the records, in both directions: stale state, stale severity, an issue with no row, a row with no
issue, an invented state or severity, a directory with no record, a report disagreeing with the
record beside it, a `verified` claim with no pin, and a directory whose name does not carry its id.

⛔ **It caught three real violations in the tracker it was written for**, which is the only
evidence worth having that a gate discriminates:

```
NOT CONTAINED LS-001: …/evidence/patched.txt:1 references '/Volumes/' — outside its own subtree
NOT CONTAINED LS-001: …/evidence/shipped.txt:1 references '/Volumes/' — outside its own subtree
NOT CONTAINED LS-001: …/issue.sexp:4      references 'scripts/'  — outside its own subtree
```

A maintainer copying that directory out would have got a machine path from my disk and a pointer
to this repository's tooling. Fixed in the content, not in the gate.

⛔ **Two failures worth keeping.** Three arms failed at first *for the wrong reason*: the fixture
computed `${1%%-*}` on `LS-001-a` and got `LS`. The fixture was wrong, not the gate — fixing it
took 8/12 to 12/12. And the gate exited 1 printing **nothing**, because `set -e` aborted the
assignment before `rc` could be read: a breach with no reason is indistinguishable from a crash.

**`docs/tasks/` crossed its aggregate ceiling** on the way through, by 3,057 bytes. Raised under
[`decision_task-tree-family-bound`](docs/decisions/decision_task-tree-family-bound.md) — which
records the two rejected alternatives first, because raising a bound because it fired is the
reflex the registry warns against. Compaction was checked (the archive is not a duplicate of its
tree) and a subdirectory was rejected for a mechanical reason: `check_frontier_sync.sh` matches
index links with a **flat** pattern, and breaking a gate to satisfy a bound is a worse trade. The
grounds are real — the family was bounded when the project tracked 17 lanes and now tracks 25,
two of them created this session on instruction. ⛔ **The per-part bound is untouched**: the
aggregate answers "how many lanes", the per-part answers "has one tree become a monolith", and
only the first question changed.

## SEMULITH-SF-0047 (leaf SOT-FORMAT.9) — two readers, one format, and a defect worth reporting

**What landed.** LinkedSpec published its integration document (`ad290bdb4`), discharging the
blocker this tree had carried since `2026-09-14`. `vendor/linkedspec` is now a submodule **pinned
to that exact commit**, with RGX `8763a0e6bea9` and PGEN `db6f8c6836fe` — the revisions the
guide's own evidence section names. The documented PGEN bootstrap produced all four `generated/`
products; the consumer built in 32.15s.

**The point of the leaf was never the submodule — it was the agreement.** Two readers of one
format that disagree is the defect `SOT-FORMAT` exists to prevent, and it hides: each reader is
self-consistent, each passes its own tests, and the disagreement surfaces only as a model that
behaves differently depending on which tool built it. `scripts/compare_readers.py` (11 arms) now
compares both over every tracked `.sexp`:

```
agree   definitions/riscv/m.sexp             438 nodes identical
agree   definitions/riscv/rv64i.sem.sexp    1550 nodes identical
agree   definitions/riscv/rv64i.sexp        1716 nodes identical
agree   profiles/rv64i-lab-v0/encoding.sexp   18 nodes identical
DIFFER  materials/catalog.sexp  <root>: A has 43 element(s), B has 6
```

⛔ **The defect.** A double-quoted string containing **LF** is not read as one string by
`specs/Lispish.spec`. It does not merely lose its newline — it stops being a string, and its
remaining text is re-lexed as syntax, so a `)` in the continuation closes a form that was never
open. Our 43-form catalogue read as 6, with 37 nested inside the fifth, **exit 0, no diagnostic**.

Located by refutation rather than guessing: `;` inside a string and parentheses inside a string
were both hypothesised and both **refuted** — the reader handles them correctly. Spaces, parens,
TAB and CR inside a one-line string all round-trip. Only LF breaks it, which points at
`Lispish.spec:69`, `/"(.*?)(?<!\\)"/` — `.` does not match LF without DOTALL — after which the
text falls through to `others: /[^\s"{}()\[\];]+/` and splits on whitespace.

**The fix was validated before being reported**, on a *copy* of the spec so the pinned submodule
stays clean: `(?s)` on lines 69 and 71 takes the reproduction from `4 matched / 4 differed` to
`8 matched / 0 differed`, and makes all five files agree. It is LinkedSpec's change to make —
patching a pinned submodule is how a pin becomes a fork.

⚠️ **The leaf is `blocked`, not `done`.** Its acceptance says the readers agree on *every* tracked
file; they agree on four of five. Rewriting the criterion to match the result is the only real
failure available here.

**An upstream issue tracker**, `docs/upstream/`, because a defect found in a dependency is work
this project owns until it is verified fixed. Each issue is a **self-contained sub-tree** a
maintainer can copy out and run without this repository — REPORT, VALIDATE, a repro script, one
file per case, an expected-values table, our captured evidence, and where we have one, a candidate
patch. Verified self-contained by copying each sub-tree to a scratch directory and re-running it
there.

Three issues raised, each with an id, a severity and a state:

| ID | Title | Severity | State |
| --- | --- | --- | --- |
| `LS-001` | a double-quoted string containing LF is not one string | `high` | `draft` |
| `LS-002` | quoted and bare atoms are indistinguishable — no consumer can round-trip | `medium` | `draft` |
| `LS-003` | three first-consumer papercuts in the integration guide | `low` | `draft` |

⛔ The state vocabulary keeps `fixed-upstream` and `verified` apart on purpose: **a fix we have not
re-run is a claim**, and adopting a new pin on the strength of a changelog entry is how a consumer
inherits a regression. Severity is graded by whether the consumer is *told* — silence is what makes
`LS-001` high.

⭐ Two integration consequences worth their own line, both measured here. Our doctrine gates now
walk a vendored tree: `check_fixture_fingerprints.sh` **died with RecursionError** on 1.7 GB of
another project's JSON, and `RECORD-SCHEMA` judged their records by our schema. Exactly two gates
walk the filesystem — the other four use `git ls-files`, which sees a submodule as a single entry
— so both were fixed and the reason written beside the exclusion. And the bug reports' own
`cases/*.sexp` are deliberately pathological, so they are excluded from the reader-agreement sweep
with an arm proving it: a corpus and a bug-report fixture must not share a scan.

⛔ **Three departures from the published guide, all mine, all named in the tree.** I jumped to the
line the director pointed at and skipped *Initial PGEN preparation* 100 lines earlier — the guide
says plainly that checkout does not generate PGEN's parser inputs, and I had not read it. I used
`--recursive` where two targeted inits were prescribed, costing 1.7 GB and 30 nested submodules. I
used bare `cargo` instead of `tools/run_cargo_local.sh`. A guide is only followed if you read the
part before the part you were sent to.

## SEMULITH-PD-0046 (leaf PUSH-DISCIPLINE.1) — the push boundary gets a gate that refuses

**Director instruction, `2026-09-14`:** *"Set the push cadence to every 300 commits. Exceptional
push happen from time to time, but they shall require my approval."*

**Measured before writing anything, and the finding is an absence:**

```
$ grep -ci push COMMIT.md          ->  0     the normative commit workflow never mentions pushing
$ ls .githooks/                    ->  commit-msg  pre-commit     (no pre-push)
$ git rev-list --count origin/main..HEAD  ->  45
```

45 commits had exactly one governance rule between them and a server: a human remembering. The
policy was not being broken — it did not exist.

**Why a push is governed differently from a commit.** A commit is local and reversible: reword it,
drop it, rebase it, and nothing outside this disk ever knew. A push sends bytes to a server that
may keep, cache, mirror or index them regardless of what happens here afterwards.

⛔ **And the specific failure this guards against is an agent's.** An assistant asked to "finish
up" will naturally read pushing as tidying, and will reach — reasonably, on its own — the judgement
that this particular push is surely fine. So the hook **refuses rather than warns** (a warning at
an outward-facing boundary is read after the bytes have left), and **the director grants the
exception while the variable only carries it**:

```
$ bash scripts/check_push_cadence.sh --status ; echo $?
PUSH-CADENCE: REFUSED — 45 commits since the last push; the cadence is 300 …
  Two ways forward, and only two:
    1. Wait. The cadence is 300 commits; this is 45.
    2. Ask the director. … SEMULITH_PUSH_APPROVED='<the director's reason>' git push
  ⛔ An agent may not supply this on its own judgement.
1
```

**11 arms, each in a throwaway repository with a real upstream** — a gate about
distance-from-upstream cannot be tested without one. Three were fired RED first and failed: two
because the refusal message wrapped across a newline so a literal match missed it, and one because
`COMMIT.md` did not yet state the cadence — the no-duplicated-fact arm doing its job before the
fact existed.

⛔ The instrument refuses on `DETACHED`, `NO-UPSTREAM` and `NOT-A-REPO` rather than printing a
distance it cannot know. "0 commits ahead" for a detached HEAD is a lie that *permits* a push.

**The accepted exposure is on the record, not discovered later.** 45 commits exist only on one
disk and cadence 300 means they stay there a long while. `decision_push-cadence` states that
plainly, so it remains a decision someone made rather than an oversight nobody revisited.

New tree `PUSH-DISCIPLINE` (3 leaves). `.2` is next and is Policy 16's unenforced half: full CI
runs before a push, and nothing enforces it — the pre-commit hook covers only the "selected checks
for ordinary commits" side.

## SEMULITH-MM-0044 (leaf MODEL-METHOD.13) — the corpus moved, and my survey had sampled rather than swept

**What changed at the source.** The primary-source corpus advanced three commits (`4201f50` →
`3c45e81`) and closed **both gaps this project measured and reported**, three commits after
reporting them: five AMD64 APM volumes imported (`e401a56`), Intel SDM Volume 1 imported
(`98de100`). It also pinned the full `v20260120` docs.riscv.org snapshot and **moved** the RISC-V
PDF — which made a tracked record in this repository false:

```
$ python3 scripts/materials.py --fetch RVI-ISA-PDF-20260911
  REFUSED: not at $SEMULITH_CHIPDOC_ROOT/risc-v/isa/current/riscv-isa-manual_…pdf
```

**What changed in my method, which is the more useful half.** The first survey enumerated by
**guessing vendor directory names** from memory. Every probe returned relevant results, so nothing
signalled absence. Re-swept by path shape instead, eight documents had been missed — including the
**entire M68000 architecture** (filed under `nxp/m68k/`, because NXP inherited Motorola through
Freescale) and **every board-class document in the corpus**: three ESP32 SoC manuals and the
RP2040 and RP2350 datasheets, which is the whole material base for `P5-BOARD`.

⭐ The giveaway I ignored: my own probe named a `motorola/` directory that does not exist. A probe
naming something absent is a signal, and I read it as nothing.

The catalogue now carries a `derivation` field naming the sweep command, so the method can be
judged rather than believed. **22 → 36 materials**, 36 of 36 fetched and digest-verified.

**Both gaps closed with evidence, and kept.** A deleted gap erases the fact that the question was
ever asked, so each carries `(status resolved)`, what closed it, and — for AMD — a `(residual …)`
noting their doc hub is not scriptable, so a newer revision could exist uncaptured. A gap closed is
not a gap that cannot reopen.

⭐ **A material that is not one file.** The pinned snapshot is 72 HTML pages, and a snapshot
identified by the digest of one page is not identified at all. `kind snapshot` names a `manifest`
whose digest is the material's identity and whose entries verify every page — `72 manifest entries
verified` on fetch, and a tampered page inside a verifying snapshot is caught (new RED arm).

⭐ **That ends a real fragility.** The citation evidence lived only in an untracked working area
needing the network — the reason `check_citations.py` could not be a gate. It now runs from the
manifest-verified cache, **offline**, and prints which route it used:

```
via fetched working area target/sources/riscv-v20260120        -> 52 of 52 resolve
via materials cache .materials/riscv/pinned-v20260120/unpriv   -> 52 of 52 resolve
```

⭐ **Independent corroboration of the pin challenged last leaf.** chipdoc acquired the `v20260120`
snapshot by its own route; its digests for `intro`, `rv32` and `rv64` **equal** those committed in
`sources.toml`, and its manifest verifies 72 of 72. Two acquisitions, two parties, one set of bytes
— the one thing an agreement between us could not have produced.

⛔ **The reader refused this leaf's own first draft.** The catalogue generator emitted literal
`\uXXXX` escapes and `scripts/sexp.py` rejected the file by name — `unknown escape '\u'`. That is
`SOT-FORMAT.7`'s closed escape table doing its job one leaf later, on real content rather than a
fixture. The content was fixed; the reader was not touched.

Corpus drift is now **detected rather than discovered**: `--list` and `--verify` compare the
catalogued revision against the checkout's `HEAD`.

**Knowledge.** [`a-survey-that-found-things-can-still-have-missed-things`](docs/knowledge/a-survey-that-found-things-can-still-have-missed-things.md)
— a zero prompts "is my instrument blind?"; twenty-two results prompt nothing at all. Enumerate by
a property of the thing, never a list of names you wrote from memory, and read what your
enumeration excluded before you believe it.

## SEMULITH-MM-0043 (leaf MODEL-METHOD.12) — a citation that is present is not a citation that resolves

**The challenge.** An external investigation reported that this profile's pinned source does not
exist: `riscv/riscv-isa-manual` has no `2026-01-20` tag (the tags jump `01-17` → `01-21`), its
January release PDFs number **RV32I §2 and RV64I §4**, and the `§1.1` / `§3.1` numbering used by all
52 semantic citations is what you get only when `Introduction` is unnumbered front matter rather
than Chapter 1 — which no build it checked does. Conclusion: the pin matches no public build.

**Re-derived from the primary artifact before defending or conceding.** Every observation in the
report is true. The conclusion is not, and the difference is one word: **publication**.

```
github.com/riscv/riscv-isa-manual   numbers Introduction as Chapter 1  -> RV32I §2,    RV64I §4
docs.riscv.org  (pinned here)       Introduction is front matter       -> RV32I §1.1,  RV64I §3.1
```

`docs.riscv.org` is the RISC-V **Ratified Specifications Library**, a different publication of the
same specification, and it applies exactly the numbering rule the report deduced. Verified end to
end:

```
$ curl …/reference/isa/v20260120/unpriv/{intro,rv32,rv64}.html   -> HTTP 200 ×3
  and byte-identical to the pinned copies AND to the digests committed in sources.toml
$ python3 scripts/check_citations.py
  52 of 52 instruction citations resolve in the pinned artifact
```

⭐ **The investigation was not sloppy — it was under-informed by me.** What I had published was the
bare string `v20260120` with no publication attached, and given only that, searching the source
repository is the *reasonable* first move. The report even reconstructed the numbering rule that
explains the discrepancy; it lacked only the fact that some publication applies it.

**The real defect, which the challenge exposed and which was not the pin.** Nothing could have
settled this mechanically. `check_semantics.py` asks whether a rule *carries* a citation, and a
citation pointing nowhere still carries. `scripts/check_citations.py` now resolves every locator
against the pinned bytes — 10 self-test arms, and it **refuses rather than passing** when the
artifacts are absent, which matters because they are untracked and need the network:

```
$ mv target/sources/riscv-v20260120 … && python3 scripts/check_citations.py ; echo $?
REFUSED: the pinned artifacts are not present at target/sources/riscv-v20260120 … exit=1
```

`sources.toml` now names its publication **and the one it is not**, because the next person to
check this will start where the last one did.

**The interim substitution is declined**, recorded as `GAP-RISCV-JAN-2026-PDF`. Adopting the
January PDFs would turn 52 resolving citations into 52 unresolvable ones — a strictly worse
position reached by acquiring *more* material. They may be catalogued later under their own ids;
acquiring a document and repointing a pin are two decisions and only the first is cheap.

**Also measured:** the docs.riscv.org rendering carries only `Copyright © RISC-V International®` —
**no CC-BY statement**, unlike the GitHub PDF. So `OQ-4` (redistribution terms) stays open for the
rendering, and the pinned HTML is still read, never redistributed.

**Knowledge.** [`a-version-string-is-not-an-identity`](docs/knowledge/a-version-string-is-not-an-identity.md)
— a version names a point in time within one publication; across publications it identifies
nothing, and section numbers are exactly the part that will not survive the crossing.

## SEMULITH-MM-0042 (leaf MODEL-METHOD.11) — materials get an identity, and no path that breaks on a move

**What changed.** A curated corpus of vendor ISA and architecture manuals became available —
3,684 files, 1.5 GB, 196 PDFs across 23 vendors, curated in its own words *"to build software
emulators (ISS) that run real C/C++/Rust software"*. This repository had no form in which to say
that a material exists and where a copy of it is (`git ls-files | grep -ci materials` → 0).

The obvious route is the wrong one. The corpus lives **outside** the repository, so writing its
path into a tracked file plants an absolute path — which Policy 12 forbids, because the repository
must survive being moved to another filesystem. And it fails *quietly*: after a move the path stops
existing and every tool reports "not found" about a document sitting right there.

**The shape that solves it.** Paths compose from two roots, and the catalogue knows only one:

```
cache      <repo root>/<cache-root>/<cache-path>    both halves tracked and relative
corpus     $<env-var>/<corpus-path>                 the left half NEVER tracked
```

The environment variable is the seam. The operator sets it once; git never sees it. Measured on
the tracked tree, with a control proving the probe can see such a path:

```
$ git grep -c -I --cached -e 'livework' -- .    ->  0 tracked files name the corpus root
```

**What is catalogued.** 22 materials — RISC-V (unified ISA + ELF psABI), Arm (A-profile,
Armv7-A/R, Armv8-M, Armv7-M, Armv6-M), Intel SDM Volumes 2-4, Power ISA 3.1C, SPARC 2015,
OpenRISC 1000, six TI DSP CPU guides, MSP430, Z80, W65C02S — each with revision, page count,
sha256, licence and what it supplies. All 22 fetched and digest-verified into the gitignored
`.materials/` (233 MB, same volume as the repository). The repository catalogues identity and
redistributes nothing.

⭐ **Two measured gaps, recorded as first-class `(gap …)` records rather than remembered:**

- **No AMD instruction-set manual.** `amd/` holds exactly one document, an IOMMU specification. An
  x86-64 unit built from this corpus would rest on Intel's description of the architecture alone.
- **No Intel SDM Volume 1.** Volumes 2, 3 and 4 are present; Volume 1 — Basic Architecture, the
  execution environment, data types and register overview — is absent. An x86 unit could not state
  its architectural **state** from this corpus.

⭐ **And the RISC-V PDF is not our RISC-V.** It is `20260911: Intermediate Release`; the profile
pins `v20260120`. It also numbers RV32I §2.1 and RV64I §2.2, where the pinned HTML numbers them
§1.1 and §3.1 — so **not one of our 52 semantic citations resolves in it**. Catalogued
`reference-only`, never as the authority a requirement cites. Its licence, read from the document,
is **CC-BY-4.0**, which bears directly on `OQ-4` and rule `SRC-01`.

⭐ **Scale, as an argument rather than an opinion.** The Arm A-profile manual is **17,145 pages and
126 MB** — eighteen times the RISC-V manual. Beside it sit Armv6-M at 374 pages and the W65C02S
datasheet at 32, both complete architectures. That spread is `start small and grow` stated in page
counts.

**Housekeeping in lockstep.** `materials/` registered in `doctrine/readme_routes.tsv` in the commit
that creates it, ceilings derived from its own measured size. `CHANGELOG.md` had 1,326 B of
headroom against its 64 KiB ceiling and was sharded first: 64,210 → 28,188 B, 11 entries moved to
`docs/changelog/2026-09-p0-to-mirror.md`.

## SEMULITH-SF-0041 (leaf SOT-FORMAT.7) — the reader corrupted every citation it read

**What changed.** `scripts/sexp.py` decoded string escapes by handing the assembled string to
`.encode().decode("unicode_escape")`. That codec is **Latin-1**: it reads each byte as one
character, so the two UTF-8 bytes of `§` came back as `Â§` and an em dash came back as three
characters of noise.

**All 52 specification citations** in `definitions/riscv/rv64i.sem.sexp` were corrupted on read —
every locator committed one leaf earlier as *"52 of 52, every rule cited"*. The claim was true of
the file and false of what any consumer received:

```
raw bytes in file : b'RVI-RV64I \xc2\xa73.1.2.1 \xe2\x80\x94 D-LUI-AUIP'
as the reader sees: 'RVI-RV64I Â§3.1.2.1 â\x80\x94 D-LUI-AUIP'
```

**Why nothing caught it.** The reader that every source of truth in this repository depends on had
**no self-test at all**. Downstream, every instrument asked about structure or behaviour —
`check_semantics.py` asks whether a citation is *present*, and a corrupted string is still present.
None was pointed at **fidelity**, which is a separate property and has to be asserted separately.

**The fix.** Escapes are decoded from a closed five-entry table written in the file, and an escape
outside it is refused rather than guessed — the same soundness stance the module already claimed
for structure. A UTF-8 file needs no escape for non-ASCII at all. The reader now carries 18 arms,
three of them fired RED before the fix:

```
$ python3 scripts/sexp.py --self-test     # BEFORE → 15 pass / 3 fail
$ python3 scripts/sexp.py --self-test     # AFTER  → 18 pass / 0 fail
$ round-trip: each citation verbatim in the file's own bytes → 52 / 52, mojibake 0
```

No tracked file's content changed. The files were always right.

**Direction (director, `2026-09-14`).** Two instructions landed and are now durable records rather
than conversation:

- *Every source of truth is one format* — S-expression, composable, and **extensible to new
  constructs in the same format**. This supersedes the per-file format split in
  `decision_canonical-definition-input`: composition is a merge, and three formats are three merge
  semantics, so under the split a board composing two processors could union their encodings and
  nothing else. New tree `SOT-FORMAT`, 9 leaves.
- *The parser is not written here.* The Rust reader comes from **LinkedSpec**
  (`specs/Lispish.spec` on its Rust backend), added as a **git submodule** pinned to a commit.
  ⛔ I first inferred `pgen` from the capability description — *many backends, Rust among them,
  parses many formats* — and was corrected. The failure mode is general and worth keeping: a
  capability description matches several repositories; only a named artifact identifies one.
  ⛔ **Blocked:** LinkedSpec is preparing its integration document for downstream consumers and it
  is not finished, so `SOT-FORMAT.9` waits for it rather than integrating against internals.

**Also measured, and owned rather than logged.** The mdBook chapter *"Architecture and canonical
definitions"* includes `docs/ARCHITECTURE.md`, which names no format, no `definitions/` directory
and no composition operator — all three introduced over the four preceding commits. The director's
only window into the project shows none of the work. `SOT-FORMAT.8`, at frontier order 2.

**Knowledge.** [`a-parse-without-error-is-not-a-faithful-read`](docs/knowledge/a-parse-without-error-is-not-a-faithful-read.md)
— a parser's error paths are all about structure; it proves nothing about content until a test
compares what it returned with what it read. A test corpus of `foo` and `bar` cannot tell a correct
decoder from a Latin-1 one.

## SEMULITH-MM-0040 (leaf MODEL-METHOD.9) — the semantics: 52 of 52, every rule cited

**What changed.** Nothing machine-executable existed. A generator engine reading the canonical
definition found configuration, state, provenance, assumptions and encodings — and still could not
produce an interpreter, because what each instruction *does* lived only as English prose in a
decision's `statement` field. 26 rules, all prose, none executable.

`definitions/riscv/rv64i.sem.sexp` now carries **52 of 52** declared instructions as expressions,
each citing the specification locator it was derived from.

⭐ **Widths are always explicit**, because an implicit width is where two models silently disagree:

```
(sem (insn addiw) (source "RVI-RV64I §3.1.2 — D-WSUFFIX …")
     (effect (set (reg rd) (sext 64 (trunc 32 (add (trunc 32 (reg rs1)) (sext 32 (imm imm12))))))))
```

That is the whole of `D-WSUFFIX` in one line, and it can be checked against the sentence that
produced it — which is the entire evidence argument for a hand-derived semantics.

⛔ **Generated and authored content live in different files on purpose.** `rv64i.sexp` is generated
from a machine-readable table and regenerated whenever that table moves; hand-derived semantics in
the same file would be destroyed by a regeneration. Different provenance, different file.

**The language is 32 forms**, each added because an RV64I instruction needed it, none in
anticipation — and the checker refuses everything else. Four controls fired on the real file: a
missing instruction (`sraw`), an unknown operator (`multiply`), an operand the instruction does not
have (`imm12` in `sub`), and a rule citing nothing. Each refused by name.

⚠️ **What `52 of 52` does not mean.** It says the semantics are well-formed, complete and *cited*.
It does **not** say they are **correct**. Proving that is a differential experiment against a
reference model — what `P0-PROFILE.6` does for three guest programs today and what `P1-LAB` must do
at scale. A definition that says something checkable is not yet one that says something true.

⛔ `riscv/m`'s semantics are absent and that is correct: `rv64i-lab-v0` does not compose `M`, and
writing semantics for a fragment no unit uses would be inventory.


## SEMULITH-MC-0039 (leaf MODEL-COMPOSE.2) — fragments get a form and a home

**What changed.** The unit carried all 52 instructions **inside itself**. A base ISA is shared by
every profile that composes it, so a second RV64 profile would have copied 52 instructions that
then had to be kept equal — the exact duplication the no-duplicated-fact rule exists to prevent,
in the one place most tempting to copy.

- `definitions/riscv/rv64i.sexp` — the base: 52 instructions, plus the operand fields and
  scattered-immediate layouts a base owes its extensions.
- `definitions/riscv/m.sexp` — the M extension: 13 instructions, `(requires "riscv/rv64i")`.
- The unit now **names** what it composes and owns nothing: `(compose (base "riscv/rv64i")
  (extensions))`. Census: instructions in the unit `52 → 0`; in `definitions/` `0 → 65`.

⭐ **The acceptance test is that nothing observable moved.** A refactor of the source of truth must
not perturb the evidence, so all four guests were re-assembled and re-run: the `elf sha256` values
are **byte-identical** to before the split, across two reference models, all reproducing.

**Two refusals, both fired.** Composing `riscv/m` without its base →
`requires 'riscv/rv64i', which this composition does not provide before it. A fragment with an
unmet dependency composes by luck, not by construction.` Composing a fragment that does not exist →
`composes 'riscv/nope', but definitions/riscv/nope.sexp does not exist`.

**The `M` fragment is now pinned** (`rv_m`, `rv64_m` digests) — a fragment composed from an
unpinned source is a model built on something nobody can re-derive. Fragments are re-derived
against the pinned tables and fired RED on a one-nibble `funct3` edit to `mul`. The tracked
generator reproduces them **byte-for-byte**, so it is the owner and the files are not a
hand-maintained copy of its output.

⚠️ `definitions/` was **registered in the routes registry in the same commit that created it** — a
new tracked family that nothing governs is how pressure escapes, which this project has already
measured once.

⚠️ Three references to the generator's old name survive in this file and in `MODEL-METHOD.8`'s
completed checklist. They are left alone deliberately: both are historical records, true when
written, and rewriting them to match today is what the `append_history` lifecycle prevents.


## SEMULITH-MC-0038 (leaf MODEL-COMPOSE.1) — encoding composition is a verdict, not a hope

**What changed, and what it replaces.** I proposed tiering models into `exploratory` (ungated) and
`accepted` (gated) to buy breadth. That was rejected, and rightly: it buys breadth by creating a
second class of model nobody can trust. The correct lever is **composition** — every model stays
signoff-grade, and complexity is reached by *assembling proven small models*. Breadth by **reuse of
evidence**, never by absence of it. Recorded as
[`decision_composition-model`](docs/decisions/decision_composition-model.md).

**The design, grounded rather than invented.** Both pinned references already compose definitions
from fragments — `riscv-opcodes` ships **111** extension files, `sail-riscv` **34** extension
directories and **59** encoding files — and this project already carries the other half: an empty
`extensions = []` seam and **8 environment-assumptions** stating what something else must
guarantee. Two operators, one port mechanism:

- **intra-unit: union with conflict detection** — decidable, and therefore a verdict;
- **inter-unit: assumption/guarantee discharge** — `CPU_ENVIRONMENT` §5, made mechanical;
- **direction falls out of ports** — an unbound *slot* makes top-down composition checkable before
  its parts exist, and compositions nest, so `computer → board → soc → {cpu, device}` is one record
  shape at every level.

⭐ **Proven, not asserted.** The owned RV64I encodings composed with an `M` fragment they had never
seen: **52 + 8 + 5 = 65 instructions, no collision, no duplicate name.** Two instructions collide
exactly when `(value_a ^ value_b) & mask_a & mask_b == 0`, searched exhaustively — a sampled answer
would not be a decision.

**Fired RED on a genuine mistake, not a synthetic one:** composing the owned encodings with `rv_i`,
a fragment they already contain, produced **37 collisions** each named with its overlapping mask,
and `REJECTED`. A second refusal fired unplanned — an empty fragment file answered
`REFUSED … an empty fragment is not a valid one` rather than "no collisions" over nothing.

⛔ **What this does not claim.** There is **no RV64IM profile**: the `M` fragment is unpinned, no
semantics were composed, nothing was added to `rv64i-lab-v0`. The *decoder* composes. Whether the
*meanings* compose is not decidable in general — an extension can change a base instruction's
behaviour, and `MODEL-COMPOSE.6` treats a silent override as a defect rather than a composition.


## SEMULITH-MM-0037 (leaf MODEL-METHOD.8) — the repository owns its encodings

**What changed.** A single source of truth per unit, from which a generator engine extracts what it
needs, requires the repository to actually **own** that source. It did not. Measured:

```
$ git ls-files | grep -c riscv-opcodes
0                       # the assembler read an untracked, network-acquired directory
$ git ls-files profiles/rv64i-lab-v0 | grep -cE 'encod|semant'
0                       # neither encodings nor semantics were owned
```

A fresh clone could not build a model at all, and the project's own rule — *a constant that is a
function of an external document is derived or gated, never assumed present* — was being broken by
its own tooling.

- `profiles/rv64i-lab-v0/encoding.sexp` — **tracked**: 52 instructions, 12 operand fields, 3
  scattered-immediate layouts, each carrying its upstream file and that file's digest.
- `scripts/sexp.py` — a reader for exactly the shapes these files use, refusing the rest.
- `scripts/gen_encoding.py` — regenerates it; `fetch_references.sh` re-derives and compares.

⭐ **The test that settles it is not that the file exists.** It is that the model builds *without*
the untracked directory, so the upstream was moved aside and the whole evidence path re-run:

```
$ mv target/refs/riscv-opcodes /tmp/ro-hidden && scripts/run_smoke.py
run_smoke: ok — every program matches its specification-derived expectations and reproduces
```

Four guest programs assembled, executed on two references and reproduced, with the source of the
encodings absent from disk.

**Ownership without re-derivation is a copy**, so the agreement is checked: fired RED by changing
**one bit** of one instruction's `funct3` — `and`'s `(14 12 0x7)` to `0x6` — producing
`DIFFERS … no longer matches what the pinned tables generate` with the line quoted.

⛔ **The new reader was caught by its own first real input.** Its tokenizer stripped `;` comments
line by line *before* tokenizing, which is wrong twice over: a `;` **inside a string** truncated
the string, and a string could not span lines. Generating this project's own encoding file hit the
second within minutes. It is now a single stream scan — whether a `;` starts a comment depends on
whether a string is open, which is the only way that question can be answered correctly.

**Also decided:** [`decision_canonical-definition-input`](docs/decisions/decision_canonical-definition-input.md).
The S-expression trigger parked earlier has **fired**: the canonical definition is a **set of
format-fit files** — S-expressions for `encoding.sexp` and `semantics.sexp` because those are
trees, records staying JSON and TOML because they are records and are already gated by instruments
fired RED. "Single source of truth" is preserved by a **no-duplicated-fact** rule, not by
single-file-ness.

⚠️ This makes the repository own its encodings. It does **not** make the canonical definition
sufficient: **semantics are still absent** — the decisions are English prose and nothing
machine-executable exists. `MODEL-METHOD.9` owns that, and `.10` turns *"the engine can extract all
it needs"* from an intention into a verdict that gates writing model code at all.


## SEMULITH-MM-0036: one canonical definition, one book — the unit that grows

**What changed.** The north star, stated and made structural: Semulith models **as much as
possible** — CPUs, MCUs, DSPs, devices, boards, SoCs, eventually whole computers — and **starts
small and grows**. The structural consequence:

> **The unit of modelling is the unit of documentation.** Every canonical definition gets its own
> mdBook, its own materials bill and its own coverage census, describing how it went **from PDFs,
> specifications and descriptions to a fully functional model**.

`docs/ARCHITECTURE.md` already named the unit — *"later devices and boards receive their own
canonical definitions"* — so this adopts existing vocabulary rather than inventing a parallel one.
What it adds is that a definition is not complete until the book explaining how it was built exists
beside it.

**Kind and layer decide what a unit may own.** A `cpu`/`mcu`/`dsp` owns instruction semantics and
its environment *assumptions*, never devices. A `device` owns one device's contract. A
`board`/`soc` owns composition, never the semantics of the parts it composes.

⭐ **The layer names the OWNER, not merely a deferral** — and that is what makes a coverage census
honest. `C19 Platform, devices and interconnect` is `deferred-to-board` for a CPU and `covered` for
a board: the same category, the same catalogue, a different unit answering it. It is also why the
catalogue is keyed on a **unit** rather than a processor profile — a board's census and a CPU's
census become the same schema answered differently, which is what makes the second unit cheap
instead of a redesign.

**Starting small, deliberately.** Exactly one unit exists: `rv64i-lab-v0`, kind `cpu`. Nothing is
pre-built for units that do not — no board directory, no device schema, no speculative chapters.
⛔ And the kinds table is a **hypothesis** until a second unit tests it; `MCU` and `SoC` in
particular have never been exercised, and the first board or DSP is expected to correct it. That
correction is normal, not a failure of the decision.

⚠️ A book is written for a model that is **not yet finished**, and says so. The first will describe
a model whose gate reads `incomplete` — hiding that until the model is done would make the book a
retrospective rather than a method, and the method is the transferable part.


## SEMULITH-MM-0035: the layer boundary — a UART is not CPU material

**What changed.** A scoping correction that arrived before it could do damage: devices belong to a
**board / SoC / ASIC** model, not to a processor model. This project pipecleans by modelling CPUs
and DSPs first, and the processor layer ends at the CPU/environment boundary — the CPU states what
it *assumes*, and a later board model states what it *guarantees*.

The project's contracts already own this line, so it is cited rather than restated:
`docs/INFORMATION_CATALOG.md` says *"C19–C21 are not all properties of the CPU itself"*, and
`docs/CPU_ENVIRONMENT.md` §5 is the board composition gate.

⭐ **The sharp consequence is for the materials catalogue, which is why this landed before its
schema was written.** A category the processor layer does not own is **not `missing`**. Marking
`C19 Platform, devices and interconnect` as missing for a CPU model would manufacture an
acquisition task for material the model must never contain, and would report a correct scope as a
deficiency. The disposition vocabulary now carries a **layer**, and `deferred-to-board` is a
first-class answer distinct from both `missing` and `not-applicable`.

⚠️ **It also corrects a framing from the previous leaf.** "Capable of running real code" needs a
console and a program-exit convention — and **those are board concerns**. What the *processor*
layer owes real code is narrower and wholly inside it: the psABI, the ELF contract, the
entry/startup state, and the compiler-runtime intrinsics a no-`M` soft-float target calls.

**`DIFF-PLATFORM-SPIKE` is reframed as a layer difference, not a configuration one.** Spike ships a
CPU *and a small board* — an interruptor, a PLIC and a UART — and does not separate them. What that
record measures is **how much board each reference drags in**, which is a more useful thing to know
than "the config would not take".

**Checked rather than assumed:** every device named anywhere in `rv64i-lab-v0` appears in exactly
one role — something a reference brings that the profile excludes. Word-boundary grep over the
profile's own files finds mentions only in notes explaining the exclusion; no decision, no
requirement and no obligation models a device. The earlier apparent hits in `sources.toml` and
`DOSSIER.md` were substrings of *implicit* and *explicit*.


## SEMULITH-MM-0034 — the dual mandate: production-grade **and** a teaching text

**What changed.** A director instruction that reshapes every model this project will produce:
each must be signoff, production-grade work **and** serve as educational material from which a
student can learn to build production-grade CPU/DSP models capable of running real compiled code
(C, Rust, …). Recorded as
[`decision_dual-mandate-production-and-teaching`](docs/decisions/decision_dual-mandate-production-and-teaching.md),
carried into `MODEL-BOOKS` and `MODEL-METHOD`, and aligned into `ROADMAP.md` §1.

⭐ **What the teaching mandate actually changes** — it is not "add explanation", which would change
nothing. Four concrete things: reasoning becomes recoverable including the rejected alternatives;
**mistakes stay in the record**; the *order* of the work is justified rather than listed; and
"runs real code" becomes a target with stated limits.

⛔ **The mistakes are the most instructive pages.** This project has already found, in its own
work, a matched profile that matched only an instruction set, a comparator that called a truncated
trace agreement, a self-test that ran four of fourteen arms, and a gate report that counted a
*mention* as an implementation. Removing those to look competent would remove the teaching.

**What "runs real code" costs, measured rather than assumed.** The first profile is `RV64I` with
no extensions: no `M` (multiply and divide become runtime calls), no `A` (no atomics), no `F`/`D`
(soft-float ABI), no `C`. Running C or Rust on it needs materials the ISA chapters do not own and
this project has **not pinned** — the psABI, the ELF specification, a startup/runtime contract,
the compiler-runtime intrinsics a no-`M` soft-float target calls, and a program-exit convention.
Those are now acquisition items in `MODEL-METHOD.4` rather than assumptions.

⚠️ It also makes an existing honesty load-bearing: `state.json` records ABI register roles as
`software-convention` because the ISA chapter does not own them. Once real code runs, that
convention stops being background reading and becomes a pinned material with a digest.

⛔ Neither mandate may be traded for the other. Simplifying a contract to make a chapter easier is
a production defect; omitting reasoning to keep a record terse is a teaching defect. Where they
genuinely conflict the production artifact wins and the book explains the complexity — a student
learning from a simplified fiction learns a fiction.


## SEMULITH-MM-0033 (leaf MODEL-METHOD.1) — answer the narrower-instrument sweep, with a wider instrument

**The open question, answered.** `P0-PROFILE.10` fixed one instance of a pattern — a single
confident scalar standing in for a configuration — and left the general question open. The sweep
enumerated every pinned scalar that stands for a configuration and checked each.

⛔ **One further instance, and worse than the first.** `spike.matched_isa_string = "rv64i"` was the
command-line **input** recorded in an observation's slot. Spike has no `--print-isa` option, so
nobody had ever confirmed it configured what it was told. The first instance was a narrow reading;
this one was not a reading at all.

It is now read back from a surface Spike does offer, with a control proving it is an observation
rather than an echo: `--isa=rv64i` → `riscv,isa = "rv64i"`, `--isa=rv64im` → `"rv64im"`.

⭐ **The replacement principle is now an instrument.** A match is claimed against the model's own
self-description at the **widest granularity it offers**, compared field by field. Both references
emit a device tree, so `scripts/compare_platforms.py` compares them:

```
FIELD                  sail (matched)           spike (matched)          agree
riscv,isa              "rv64i_zvl32b"           "rv64i"                  NO
mmu-type               "riscv,none"             "riscv,sv57"             NO
riscv,pmpregions       <absent>                 <0x10>                   NO
timebase-frequency     <500000000>              <0x989680>               NO
devices only spike advertises: clint@2000000, cpu@0, ns16550@10000000, plic@c000000
```

**4 of 4 platform fields disagree, and Spike advertises a UART, a platform interrupt controller,
an interruptor and a CPU node** that Sail does not — none of it visible in an ISA string.

- **New rule 5b** in `PROFILE-CONSISTENCY`: a pinned `matched_isa_string` must declare both what it
  does **not** establish and **where it was read from**. Fired RED on the real dossier.
- All three candidates now carry `matched_scope` — including QEMU, whose emptiness is now visible
  rather than inferred from an absent row.

⚠️ **The wide instrument has its own scope, and says so.** A device tree describes what a platform
*advertises* — not semantics, not memory attributes — and carries residue: Sail's still advertises
a `timebase-frequency` and an `htif` node with no device behind them. **Wider is not complete.**
Recording that is what stops this instrument becoming the next narrow one.

⛔ **The honest form of the answer:** one further instance existed, it is fixed, and the pattern is
gated. I am not claiming there are no others — I am claiming a new one cannot be *added* without
declaring its scope, which is the only durable form that answer can take.

**Also opened:** `MODEL-METHOD`, the tree that makes the modelling method and its required
materials explicit, with the format call recorded — JSON Lines under a JSON Schema, not
S-expressions, because the data is records rather than trees and the repository already gates
JSONL. S-expressions are parked for the canonical executable semantics in `P1-LAB`, with a trigger.


## SEMULITH-P0-0031 (leaf P0-PROFILE.10) — the profile was matched on its ISA and not its platform

**What changed.** A challenge to the previous findings turned up a real defect that the first nine
leaves of this tree carried. The matched-profile override configured `base`, `memory.misaligned`
and `extensions` — and **nothing else**. `--print-isa-string` returned `rv64i_zvl32b`, which is
correct, and was read as *"matched"*. It answers a narrower question than that.

Underneath the correct ISA the reference kept its default platform: a core-local interruptor at
`0x0200_0000`, an interrupt generator, machine software/timer/external interrupts all `supported`,
and two IOMemory regions. Established by probe:

```
[5] ld x1, 0x0(x10)      clint[0x…BFF8] -> 0x0000000000000002   x1 <- 0x2
[6] ld x2, 0x0(x10)      clint[0x…BFF8] -> 0x0000000000000003   x2 <- 0x3    # ADVANCING
```

**A guest read a monotonically advancing time source with a plain load — no CSR instruction.**
Four committed claims are refuted by that one measurement: `OB-ENV-VIRTUAL-TIME` ("no time source
is modelled"), `OB-ENV-EVENT-DELIVERY` ("no interrupt controller … no privileged mode"),
`D-MAIN-VS-IO` ("no I/O region is declared"), and `privilege_modes = []` — every trace line in
this repository reads `[M]`, because a hart is always in at least machine mode.

- **Corrected at source, not reworded.** The override now sets `platform.clint.supported = false`,
  the interrupt generator off, all three machine interrupt sources off, and `memory.regions` to
  the single MainMemory region the profile declares. Both probes now raise `load-access-fault`.
- `profile.toml` gains `D-PLATFORM`, corrects `D-MAIN-VS-IO`, and sets `privilege_modes = ["M"]`.
  Decisions 25 → 26, requirements 25 → 26, obligations 33 → 34, checks 66 → 68, differences 4 → 6.
- **The repair is held permanently** by a tracked negative fixture, `guests/guest-no-device.s`,
  which reads CLINT `mtime` and must fault. A device becoming reachable again turns the run red.
- **The three original guests still agree** over 12 / 13 / 3 aligned steps and reproduce
  byte-identically — the repair changed nothing it should not have.

⭐ **Spike is not platform-matched and cannot be**, which is enumerated rather than fixed. Its
interruptor is built in; `--device` only *adds* MMIO plugins; and `-m0x80000000:0x10000` kills its
own reset vector (`trap_instruction_access_fault, epc 0x1000`). `SRC-02` makes that a legitimate
result that **bounds** the claim: any guest touching `0x1000` or `0x0200_0000..0x11ff_ffff`
behaves differently on the two references. The three original guests touch neither — now a
**stated precondition rather than luck**. `guest-no-device` disables its cross-model comparison
for this reason and the runner **prints the skip** rather than applying it silently.

⛔ **The instrument is the lesson.** This is not the `zero-hits` failure — an instrument that could
not see. It is worse and quieter: **an instrument answering a narrower question than the one
asked**. `--print-isa-string` gave one confident string, and the string was true.

**Effect on `G0`.** The verdict stays `incomplete` for the same reason (68 declared checks, 0
implemented). But criterion 3 — *differences enumerated, not assumed absent* — is now met on
evidence rather than on an unexamined configuration, which is a real change in what the gate means.
