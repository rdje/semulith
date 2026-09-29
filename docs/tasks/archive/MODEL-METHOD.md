# `MODEL-METHOD` — completed-leaf evidence (archive)

> Split out of [`../MODEL-METHOD.md`](../MODEL-METHOD.md) on `2026-09-27`, when that file
> crossed the `docs/tasks/` per-part ceiling (73,867 bytes against 65,536). The registry
> names this as the intended response — the ceiling was obeyed rather than raised.
>
> ⛔ **Nothing here is edited when it moves.** These are the acceptance checklists exactly as
> they were accepted at commit time. The live tree keeps the frontier, the decisions, the
> open questions and both logs.
>
> This directory is deliberately a subdirectory: `FRONTIER-SYNC` treats every `docs/tasks/*.md`
> as a tree needing an index row, and an archive is not a tree.

## The archive

## Acceptance Checklist (current leaf — `MODEL-METHOD.13`)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. Two causes, one in the corpus and one in me.

  WHERE (1): `materials/catalog.sexp`, `RVI-ISA-PDF-20260911`'s `corpus-path`. The corpus moved the
  file (`git diff --name-status` reports `R100`, a pure rename), so a tracked record became false:

  ```
  $ python3 scripts/materials.py --fetch RVI-ISA-PDF-20260911
    REFUSED RVI-ISA-PDF-20260911: not at $SEMULITH_CHIPDOC_ROOT/risc-v/isa/current/riscv-isa-manual_…pdf
  ```

  WHY: the catalogue pins a corpus revision (`4201f50`) but nothing compared it against the
  checkout, so a moved path could only ever be discovered by a failing fetch.

  WHERE (2): my survey method. I enumerated by **guessing vendor directory names** — `zilog`,
  `wdc`, `openrisc`, `openpower`, `sparc`, `ti`, `arm`, `amd`, `intel` — rather than sweeping by
  path. Every probe returned relevant results, so nothing signalled absence. Re-swept by path:

  ```
  $ find . -name '*.pdf' | grep -iE '/(isa|cpu|architecture|processors|m68k|z80|65c02|dsp|mcu)/'
  ```

  Eight documents missed, including the **entire M68000 architecture** (under `nxp/m68k/` — NXP
  inherited Motorola through Freescale) and **every board-class document in the corpus** (three
  ESP32 SoC manuals, two Raspberry Pi datasheets), which is the whole material base for `P5-BOARD`.
  ⭐ The giveaway I ignored: my own probe named a `motorola/` directory that does not exist.

- [x] **ADDRESSED (verified)** — leg 2. Corpus re-pinned `4201f50` → `3c45e81`; the moved path
  corrected; the catalogue re-derived from the sweep and carrying a `derivation` field that names
  the sweep command, so the method can be judged rather than believed. 22 → **36 materials**:

  ```
  $ python3 scripts/materials.py --fetch     ->  36 of 36 ok, every sha256 verified
  $ python3 scripts/materials.py --self-test ->  20 pass / 0 fail  (was 15)
  ```

  **Both gaps this project measured are closed at the source, three commits after it reported
  them** — and closed **with evidence and kept**, never deleted, because a deleted gap erases the
  fact that the question was asked:

  ```
  GAP-AMD64-APM        (status resolved)  5 AMD64 APM volumes imported at e401a56
                       (residual …)       AMD's doc hub is not scriptable; a newer revision could exist
  GAP-INTEL-SDM-VOL1   (status resolved)  SDM Vol 1 (253665 rev 092, 600 pp) imported at 98de100
  ```

  ⭐ **A material that is not one file.** The pinned `v20260120` HTML snapshot is 72 pages; a
  snapshot identified by the digest of one page is not identified at all. `kind snapshot` names a
  `manifest`, whose digest is the material's identity and whose entries verify every page:

  ```
  ok  RVI-PINNED-V20260120 -> .materials/riscv/pinned-v20260120 (6,229 B, sha256 verified,
                                                                 72 manifest entries verified)
  ```

  ⭐ **And that ends a real fragility.** The citation evidence lived only in an untracked working
  area that needs the network — the reason `check_citations.py` could not be a gate. It now runs
  from the manifest-verified cache, **offline**, and says which route it used:

  ```
  via fetched working area target/sources/riscv-v20260120        -> 52 of 52 resolve
  via materials cache .materials/riscv/pinned-v20260120/unpriv   -> 52 of 52 resolve
      (manifest-verified, offline)
  ```

  ⛔ Corpus drift is now **detected, not discovered**: `--list` and `--verify` compare the
  catalogued revision against `git -C $ROOT rev-parse HEAD` and say so.

  ⭐ **Independent corroboration of the pin.** chipdoc acquired the `v20260120` snapshot by its own
  route; its digests for `intro`, `rv32` and `rv64` **equal** those committed in `sources.toml`,
  and its `SHA256SUMS` verifies 72 of 72. Two acquisitions, two parties, one set of bytes — which
  is the one thing last leaf's external challenge could not have produced by agreement.

- [x] **NO REGRESSION** — leg 3. ⛔ The S-expression reader **refused this leaf's own first draft**
  of the catalogue — the generator had written literal `\uXXXX` escapes — and refused it by name:

  ```
  SexpError: materials/catalog.sexp:41: unknown escape '\u' in string. The reader refuses rather
  than guessing what it was meant to be
  ```

  That is `SOT-FORMAT.7`'s closed escape table doing exactly the job it was built for, one leaf
  later, on content rather than on a fixture. Four escapes replaced with the characters themselves;
  the reader was not touched. Full re-run:

  ```
  $ python3 scripts/sexp.py --self-test          -> 18 pass / 0 fail
  $ python3 scripts/check_citations.py           -> 52 of 52 (both routes)
  $ python3 scripts/check_semantics.py …         -> 52 of 52 declared instruction(s)
  $ python3 scripts/run_smoke.py | tail -1       -> run_smoke: ok …
  $ bash scripts/check_doctrines.sh              -> all doctrines green
  ```

- [x] **LOCKSTEP** — knowledge card
  [`a-survey-that-found-things-can-still-have-missed-things`](../knowledge/a-survey-that-found-things-can-still-have-missed-things.md),
  promoted from the dated `DEV_NOTES.md` lesson; `TOOLBOX.md` already carries the resolver rows;
  `materials/` stays within its registry ceilings (43,462 B against a 131,072 B per-part bound).

## ROUTING EVIDENCE

`MODEL-METHOD.13` — the sweep surfaced **every board-class document in the corpus**, which belongs
to `P5-BOARD` and not to this tree: three ESP32 SoC manuals, the RP2040 and the RP2350 datasheets.
Measured and catalogued rather than routed as prose, with two pairings worth the next reader's
attention. `RP2040-DS` pairs exactly with `ARM-M-DDI0419E` — a 374-page architecture manual and the
part built around it, processor and board in two documents, which is the cleanest available test of
this project's layer boundary. `RP2350-DS` describes a part carrying **both** an Arm Cortex-M33 and
a Hazard3 RISC-V core on one die, software-selectable: if `MODEL-COMPOSE`'s slots are real, one
board description should compose with either processor. Reproduces outside the family: the sweep
was over the whole corpus by path, not over `raspberry-pi/`.

`ESP32-C3-TRM` is the one this project reaches first — a shipping RISC-V SoC whose UART and
interrupt matrix are specified in the document where the director said they belong.


`MODEL-METHOD.12` — the interim substitution offered by the external investigation (pull the
2026-01-17 / 01-21 release PDFs as "the closest official match") is **declined**, and the reason is
recorded where the next person will meet it, in `materials/catalog.sexp` as `GAP-RISCV-JAN-2026-PDF`.
Measured: those PDFs number RV32I §2 and RV64I §4, so adopting them would turn 52 resolving
citations into 52 unresolvable ones — a strictly worse position reached by acquiring *more*
material. They may be catalogued later under their own ids as additional references; acquiring a
document and repointing a pin are two decisions and only the first is cheap.


Two findings measured here are **not** this tree's to fix, and both are recorded in the catalogue
as first-class `(gap …)` records rather than as prose someone must remember:

- `GAP-AMD64-APM` — probed `find . -iname '*APM*' -o -iname '*AMD64*' -o -iname '*24592*'` → no
  match. The corpus's `amd/` directory holds exactly one document, an IOMMU specification. **There
  is no AMD instruction-set manual**, so an x86-64 unit built from this corpus would rest on
  Intel's description of the architecture alone. Reproduces outside the family: the probe is over
  the whole corpus, not over `amd/`.
- `GAP-INTEL-SDM-VOL1` — probed `find . -iname '*253665*' -o -iname '*Vol1*'` → no match, while
  Volumes 2, 3 and 4 are present. Volume 1 carries the basic execution environment, data types and
  register overview — the architectural **state** a model declares first. An x86 unit could not
  state its state from this corpus alone.

Both belong to `MODEL-METHOD.3`, the coverage census, which is where a gap becomes a disposition.
Neither is routed to another tree; neither is worked around here.

## Acceptance Checklist (leaf MODEL-METHOD.10)

- [x] **REPRODUCE / ISSUE** — the contract as stated, run against the corpus before any code:

  ```
  $ python3 - <<'PY'   # the requirement leg, measured
  > reqs = records_sexp.load("profiles/rv64i-lab-v0/requirements.sexp")
  > insns = {i for r in reqs for i in r.get("insns", [])}   # {} — the link did not exist
  > PY
  $ # and with the link curated on the 7 instruction-kind requirements alone:
  $ # the ALU family (add sub slt sltu xor or and + addi slti sltiu xori ori andi) has NO requirement
  ```

  The catalogue itself failed the contract's requirement leg — 13 instructions uncovered. That
  is the leaf's real finding, and fixing the corpus is part of the fix.

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHY: every per-family check (ENCODING, SEMANTICS,
  RECORD-SCHEMA) proved its own leg, and nothing proved they described the SAME instruction
  set — the integrative claim was the gap. WHERE: measured, not read —

  ```
  $ grep -c 'insns' schema/requirements.sexp
  0                                             # no requirement↔instruction link existed
  $ grep -c 'ALU' profiles/rv64i-lab-v0/requirements.sexp
  0                                             # the ALU family: no requirement record at all
  ```

  The catalogue itself failed the contract's requirement leg; fixing the corpus is part of
  the fix, not a waiver of it.

- [x] **FIX** — data first: `(insns …)` on `schema/requirements.sexp` (kind-agnostic;
  FENCE names one instruction, ECALL-EBREAK two); the catalogue extended where the contract
  demands it (D/REQ/OB-ALU-REG, D/REQ/OB-ALU-IMM, statements grounded in the corpus's own
  §1.1.4 semantics — including SLTIU's sign-then-unsigned quirk); `check_extraction.py`
  decides one-set-four-ways plus the reset and checks legs; `EXTRACTION` registered as the
  17th doctrine so P1-LAB cites a verdict that runs.

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  ```
  $ python3 scripts/check_extraction.py --self-test
  check_extraction --self-test: 6 pass / 0 fail
  $ bash scripts/check_extraction.sh --self-test
  EXTRACTION --self-test: 3 pass / 0 fail
  $ python3 scripts/check_extraction.py profiles/rv64i-lab-v0
  the definition is SUFFICIENT for an engine: 52 instructions, each with encoding +
  semantics + requirement; reset everywhere; obligations checked both ways
  $ # the acceptance, on a real-corpus copy with one instruction's semantics removed:
  $ python3 scripts/check_extraction.py <copy>
  REFUSED — scope declares 1 instruction(s) the semantics set does not cover: add   rc=1
  ```

- [x] **NO REGRESSION** — `bash scripts/check_requirements.sh --self-test` 23 pass / 0
  fail + real run green (it caught a wrong obligation id mid-curation — `OB-D-ALU-REG` vs
  `OB-ALU-REG` — fixed before commit); `bash scripts/check_profile_consistency.sh` 39 arms +
  real run green; GATE-REPORT re-derived (28/28/36/72, verdict unchanged); the catalogue diff
  is minimal (11 insns additions, 2+2+2 new records, headers preserved); the round-trip owner
  carries `insns` and untouched records re-serialize byte-identically; whole gate green after
  staging.

- `promotion: declined (the "one set, four ways" pattern is stated in the tool's docstring).`

- [x] **LOCKSTEP** — `scripts/check_doctrines.project.sh` + both mirrors in the registering
  commit; `LIVE_STATUS.md` re-derived (17 doctrines, 202 arms); the count-bearing docs
  (DOSSIER/ENVIRONMENT/LIVE_STATUS rows) to 28/36/72; `TOOLBOX.md`; `MEMORY.md`,
  `CHANGELOG.md`, `DEV_NOTES.md`, `docs/TASK_TREE.md` and this tree — one commit.

## Acceptance Checklist (leaf MODEL-METHOD.7)

- [x] **REPRODUCE / ISSUE** — the rule as it stood: `decision_canonical-definition-input`
  states the no-duplicated-fact rule in prose, nothing mechanizes it. Census, pre-code:

  ```
  $ ls doctrine/fact_ownership.tsv 2>&1
  ls: doctrine/fact_ownership.tsv: No such file or directory
  $ grep -c 'MIRROR' scripts/check_requirements.sh
  0                                             # obligation->requirement restatement: ungoverned
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHY: the corpus legitimately DERIVES facts into
  mirrors (a requirement restates a decision; an obligation restates its requirement), and a
  mirror with no governor is one fact stated in two, free to drift — the exact failure the
  prose rule names. WHERE: measured, not read —

  ```
  $ grep -c 'MIRROR' scripts/check_requirements.sh
  0                                             # obligation->requirement: no governor at all
  $ python3 - <<'PY'
  > obs = records_sexp.load("profiles/rv64i-lab-v0/contract-obligations.sexp")
  > print(sum(1 for o in obs if o["parameters"].get("requirement_id")))   # -> 28
  > PY
  ```

  Three mirror pairs were governed (decision<->requirement by RECORD-SCHEMA rule 4;
  state<->profile by PROFILE-CONSISTENCY; composition<->fragments by UNIT-COMPOSITION); the
  obligation->requirement pair was not — 28 restatements, all matching today, free to drift.

  ```
  $ python3 - <<'PY'   # 28 obligations restate a requirement's statement; nothing enforces it
  > obs = records_sexp.load("profiles/rv64i-lab-v0/contract-obligations.sexp")
  > print(sum(1 for o in obs if o["parameters"].get("requirement_id")))   # -> 28
  > PY
  ```

- [x] **FIX** — the registry as data (`doctrine/fact_ownership.tsv`, beside the routes
  registry in shape); the governor where it belongs (RECORD-SCHEMA rule 9 — the mirror check
  keys on the obligation's own `requirement_id`); the gate verifying the registry holds and is
  complete against the corpus's actual pairs.

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  ```
  $ bash scripts/check_requirements.sh --self-test
  RECORD-SCHEMA --self-test: 26 pass / 0 fail     # was 23; +3 mirror arms
  $ bash scripts/check_fact_ownership.sh --self-test
  FACT-OWNERSHIP --self-test: 8 pass / 0 fail
  $ bash scripts/check_fact_ownership.sh
  FACT-OWNERSHIP: ok (8 fact kind(s): one owner each, every mirror governed)
  $ # the acceptance's shape, fired: an ungoverned mirror in the registry
  UNGOVERNED MIRROR state: '...' restates '...' with no governing doctrine          rc=1
  ```

- [x] **NO REGRESSION** — `bash scripts/check_requirements.sh --self-test` 26 pass / 0
  fail + real run green on the 28 real mirrors; PROFILE-CONSISTENCY 39/0; the whole guard
  set and the enforcer green after staging.

- `promotion: declined (the "govern every mirror or refuse it" rule is stated in the gate's header and this leaf, where anyone adding a fact kind meets it).`

- [x] **LOCKSTEP** — `scripts/check_doctrines.project.sh` + both mirrors in the registering
  commit; `LIVE_STATUS.md` re-derived (18 doctrines, 213 arms); `TOOLBOX.md`; `MEMORY.md`,
  `CHANGELOG.md`, `DEV_NOTES.md`, `docs/TASK_TREE.md` and this tree — one commit.

## Acceptance Checklist (leaf MODEL-METHOD.2)

- [x] **REPRODUCE / ISSUE** — the materials side had documents but no REQUIREMENT type.
  Census, pre-code:

  ```
  $ ls schema/units.sexp schema/category-needs.sexp materials/units.sexp materials/category-needs.sexp 2>&1
  ls: schema/units.sexp: No such file or directory           # the type did not exist
  $ grep -c 'category-need' schema/*.sexp materials/*.sexp 2>/dev/null | grep -v ':0' | wc -l
  0                                             # and nothing bound categories to units
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHY: a catalogue of documents (the who/what/where
  of materials) cannot say which information a unit OWES its model — that needs a record
  binding each INFORMATION_CATALOG category to the material kind that supplies it, per unit.
  WHERE: measured, not read —

  ```
  $ ls schema/units.sexp materials/category-needs.sexp 2>&1 | grep -c 'No such'
  2                                             # no schema for either family
  $ grep -rl 'category-need' schema/ materials/ | wc -l
  0                                             # and no record bound a category to a unit
  ```

  Nothing like the requirement type existed anywhere in the corpus.

- [x] **FIX** — two record families on the house records track (`.3`'s path walked again):
  the unit registry and the category-needs catalogue, schema-declared, mapping-owned,
  gated by RECORD-SCHEMA rules 10–11 (registry never empty; `missing` owes a reason;
  `covered` names its material; board-layer `missing` for a processor refuses as LAYER LIE).

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  ```
  $ bash scripts/check_requirements.sh --self-test
  RECORD-SCHEMA --self-test: 32 pass / 0 fail     # was 26; +6 arms on the new families
  $ bash scripts/check_requirements.sh
  RECORD-SCHEMA: ok (7 record file(s) validate and agree with their profile)
  $ grep -c '^(category-need' materials/category-needs.sexp
  24                                            # every category, explicit layer
  $ # the acceptance's rule, fired on a board-layer 'missing' for the processor unit:
  LAYER LIE category-needs.sexp [C19 for rv64i-lab-v0]: a board-layer category dispositioned
  'missing' for a processor unit — ... the honest disposition is 'out-of-scope'    rc=1
  ```

- [x] **NO REGRESSION** — the untouched catalogues re-serialize byte-identically (the new
  mappings dispatch on `book`/`disposition` BEFORE `kind`, so requirement/obligation
  round-trips are unmoved); the duplicate-id arm now keys category-needs on (category, unit);
  `python3 scripts/sexp.py --self-test` 18 pass / 0 fail; kernel 50 pass / 0 fail;
  `python3 scripts/compare_readers.py` 29 of 29 agree (the four new files swept); whole gate
  green after staging.

- `promotion: declined (the ABSENT-vs-NEVER-NEEDED disposition vocabulary is stated in the schema header and this leaf, where the .3 census meets it).`

- [x] **LOCKSTEP** — `TOOLBOX.md`; `MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md`,
  `docs/TASK_TREE.md` and this tree — one commit. No new doctrine: the families ride the
  records track RECORD-SCHEMA already owns.

## Acceptance Checklist (leaf MODEL-METHOD.3)

- [x] **REPRODUCE / ISSUE** — the first pass's claims as they stood: dispositions written
  before any evidence, with reasons asserting material absence nobody had checked. The census
  question: which rows survive contact with the pinned snapshot?

  ```
  $ ls .materials/riscv/pinned-v20260120/unpriv/*.html | wc -l
  45                                            # the snapshot's pages, present in the cache
  $ grep -c 'absent from the catalogue' materials/category-needs.sexp
  4                                             # first-pass reasons asserting absence — unchecked
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHY: a first pass writes dispositions from the
  profile's exclusions; a census must EVIDENCE them — and the evidence (the snapshot holds the
  excluded chapters) flips the meaning of `missing` from "material absent" to "subsystem
  excluded from this unit's model". WHERE: measured page-by-page against the cache:

  ```
  $ ls .materials/riscv/pinned-v20260120/unpriv/*.html | wc -l
  45                                            # the snapshot's pages, present in the cache
  $ grep -c 'absent from the catalogue' materials/category-needs.sexp
  4                                             # first-pass absence claims, none checked
  $ # the covered categories' subjects were then found in the pinned pages (C01<->rv64
  $ # Register State, C03<->rv32 Base Instruction Formats, C22<->intro UNSPECIFIED), and the
  $ # excluded chapters are present too: a-st-ext.html, rvwmo.html, v-st-ext.html, ...
  ```

- [x] **FIX** — revise the 24 rows: every `missing` reason now names what would close it
  (profile revision against snapshot chapters, or the separate Privileged/Debug volumes);
  C19/C20/C21 become `deferred-to-board` (new disposition value, zero kernel lines);
  RECORD-SCHEMA rule 12 (UNRESOLVED MATERIAL) keeps every named `material` honest against
  catalog.sexp — 1 new arm, 33 total.

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  ```
  $ grep -c '^(category-need' materials/category-needs.sexp
  24                                            # no category absent
  $ python3 - <<'PY'   # every missing row names a closer
  > needs = records_sexp.load("materials/category-needs.sexp")
  > print(all(n.get("reason") for n in needs if n["disposition"] == "missing"))   # -> True
  > PY
  $ bash scripts/check_requirements.sh --self-test
  RECORD-SCHEMA --self-test: 33 pass / 0 fail     # +1 UNRESOLVED MATERIAL arm
  $ bash scripts/check_requirements.sh
  RECORD-SCHEMA: ok (7 record file(s) validate and agree with their profile)
  ```

  Final census: 10 covered, 4 partial, 6 missing (closers named), 3 deferred-to-board,
  1 out-of-scope — the minority covered, exactly as the leaf predicted, and the value is in
  the missing rows.

- [x] **NO REGRESSION** — `python3 scripts/sexp.py --self-test` 18 pass / 0 fail; kernel 50/0;
  materials " + bt + "--self-test" + bt + " 20/0; whole gate green after staging.

- `promotion: declined (the "missing means excluded-by-the-profile, not material-absent"
  distinction is stated in the catalogue header and this leaf, where the .4 acquisition meets
  it).`

- [x] **LOCKSTEP** — the census rows and schema header; `MEMORY.md`, `CHANGELOG.md`,
  `DEV_NOTES.md`, `docs/TASK_TREE.md` and this tree — one commit.

## Acceptance Checklist (leaf MODEL-METHOD.4)

- [x] **REPRODUCE / ISSUE** — the census named what reachable acquisition looks like; the
  run-real-code set had no pinned copy anywhere:

  ```
  $ ls .materials/run-real-code/ 2>&1
  ls: .materials/run-real-code/: No such file or directory
  $ grep -c 'psABI\|ELF\|compiler-rt' materials/category-needs.sexp
  1                                             # one mention, no acquisition behind it
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHY: a model that will run real code derives from
  documents the ISA chapters do not own — the calling convention, the object format, the exit
  convention, the soft intrinsics — and `SRC-02` only bounds the claim if the attempt is
  RECORDED; an unrecorded absence is indistinguishable from an untried one. WHERE: measured,
  not read —

  ```
  $ ls .materials/run-real-code/ 2>&1 | grep -c 'No such'
  1                                             # no cache directory existed
  $ grep -rc 'psABI' profiles/rv64i-lab-v0/sources.sexp
  0                                             # and the dossier pinned none of the set
  ```

  The set lived in exactly one passing census mention — nowhere else in the tree.

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  ```
  $ for f in .materials/run-real-code/*; do shasum -a 256 "$f"; done
  3f89383ae3699e369853e9d6b1140f5372da356b76e86e1c13252810c2b83a97  ... compiler-rt-builtins-readme.txt
  422b6c64e91410fa83008aa2565532c9b523dfa33da8f56b4e2556a576b3ef18  ... elf-gabi.pdf
  2e6a1b646c5111ad76db86c0508684223d9956384e1d23e86733eca09505d02d  ... linux-asm-generic-unistd.h
  599f10a4b86090c18ded77c813ac89bc5e363e69e545653d46f3090f3f8c9b75  ... riscv-psabi.html
  3f470aa95299fcbb5f475275f44537cf47fee2a3d0afbba66f11ebff1caeb4b8  ... riscv-spec-release-f443409.pdf
  $ grep -c '__muldi3' .materials/run-real-code/compiler-rt-builtins-readme.txt
  1                                             # the soft-multiply intrinsic, present
  $ pdftotext .materials/run-real-code/riscv-spec-release-f443409.pdf - | grep -m1 funct7
  funct7                                        # the PDF question: YES, selectable text
  ```

  Every digest matches the leaf table (byte-for-byte, re-derived after caching); every failure
  carries its attempt (three SRC-02 records above).

- [x] **NO REGRESSION** — the census C20 row revised to name the set; `bash
  scripts/check_requirements.sh` real run green; `scripts/materials.py --self-test` 20/0;
  whole gate green after staging.

- `promotion: declined (the "pin identity + digest in a tracked record, bytes in the
  gitignored cache" acquisition pattern is stated in the leaf, where a second web-sourced set
  would meet the URL-kind candidate).`

- [x] **LOCKSTEP** — the C20 census row; `MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md`,
  `docs/TASK_TREE.md` and this tree — one commit.


---

_Appended `2026-09-29`, the second split: the live file crossed its per-part ceiling again
(67,737 bytes against 65,536) under leaves `.15`/`.16`. These two checklists moved here unedited,
as accepted at commit time._

## Acceptance Checklist (leaf MODEL-METHOD.5)

- [x] **REPRODUCE / ISSUE** — the method as it stood: exercised eleven times this session but
  written nowhere a reader could carry it:

  ```
  $ ls docs/METHOD.md 2>&1
  ls: docs/METHOD.md: No such file or directory
  $ grep -rl 'the method' docs/*.md 2>/dev/null | wc -l
  0                                             # no method document anywhere in docs/
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHY: a method that exists only as the history of
  its exercise cannot be learned from — the rejected alternatives die with the session that
  rejected them, and the judgement calls look like mechanics. WHERE: measured, not read —

  ```
  $ git ls-files 'docs/*.md' | xargs grep -l 'no gate can take\|document → decision' 2>/dev/null | wc -l
  0                                             # the spine lived only in leaf checklists
  ```

  Nothing in `docs/` carried the method a reader could take away.

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  ```
  $ grep -c 'shift-amount rule' docs/METHOD.md
  1                                             # one rule followed end to end, by name
  $ grep -A8 'no gate can take' docs/METHOD.md | grep -c '^[0-9]\.\|^[0-9]\.'
  4                                             # the non-mechanical steps, identified as such
  $ make book 2>&1 | tail -1
  INFO HTML book written ...                      # the book carries it verbatim
  $ grep -nE 'scripts/|schema/|\.sexp|rv64i-lab-v0|RECORD-SCHEMA' docs/METHOD.md \
      | grep -vE 'SHAMT' | wc -l
  0                                             # no project-only dependency outside the example
  ```

- [x] **NO REGRESSION** — `make book` builds; sexp 18/0; kernel 50/0; RECORD-SCHEMA 33/0;
  whole gate green after staging.

- `promotion: declined (the framing is the document's own closing section).`

- [x] **LOCKSTEP** — `docs/book/` chapter + SUMMARY row; `MEMORY.md`, `CHANGELOG.md`,
  `DEV_NOTES.md`, `docs/TASK_TREE.md` and this tree — one commit.

## Acceptance Checklist (leaf MODEL-METHOD.6)

- [x] **REPRODUCE / ISSUE** — the director's rule as it stood: prose in the roadmap, nothing
  enforcing it. Census, pre-code:

  ```
  $ git ls-files scripts | grep -c 'scope_coverage'
  0                                             # nothing refused uncovered-scope coding
  $ grep -c 'requires' materials/units.sexp schema/units.sexp
  0                                             # and no unit declared what its scope requires
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHY: "no coding without the source of truth" is
  only as real as the thing that refuses — an intention a gate doesn't carry decays the first
  busy week. WHERE: measured, not read —

  ```
  $ grep -c 'requires' materials/units.sexp schema/units.sexp
  0                                             # no unit could even DECLARE its scope
  $ grep -rl 'scope' scripts/check_doctrines.project.sh | wc -l
  0                                             # and no gate keyed the census to a coding decision
  ```

  The census dispositions existed; the vocabulary to act on them did not.

- [x] **FIX** — the registry gains `(requires …)` (data, zero kernel lines); SCOPE-COVERAGE
  checks required × census: missing or absent refuses by name; a unit with an undeclared
  scope refuses too (code may not start against a scope never declared).

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  ```
  $ bash scripts/check_scope_coverage.sh --self-test
  SCOPE-COVERAGE --self-test: 7 pass / 0 fail
  $ bash scripts/check_scope_coverage.sh
  SCOPE-COVERAGE: ok (1 unit(s) may code — every required category covered)
  $ # fired RED before registration, on a scratch unit whose required category is missing:
  MISSING REQUIRED units.sexp [ghost requires C02]: the census disposition is 'missing' …
  ```

- [x] **NO REGRESSION** — `bash scripts/check_requirements.sh --self-test` 33 pass / 0
  fail + real run green with the registry's new field; `bash scripts/check_extraction.sh
  --self-test` 3 pass / 0 fail + real run green; whole gate green after staging (19
  doctrines, 227 arms).

- `promotion: declined (the "coverage says OWNED, extraction says EXTRACTABLE" composition
  rule is stated in the gate's header and this leaf).`

- [x] **LOCKSTEP** — `scripts/check_doctrines.project.sh` + both mirrors in the registering
  commit; `LIVE_STATUS.md` re-derived; `TOOLBOX.md`; `MEMORY.md`, `CHANGELOG.md`,
  `DEV_NOTES.md`, `docs/TASK_TREE.md` and this tree — one commit.


---

_Appended `2026-09-29`, the third movement: under `.16` the live file crossed its per-part
ceiling a second time in one day (65,032 bytes and growing against 65,536). The 2026-09-27
done leaves — bodies and all — moved here unedited; the live tree keeps the active and
proposed leaves, the frontier, the decisions, the open questions and both logs._

- ID: `MODEL-METHOD.1` — **answer the narrower-instrument sweep, and make the answer an instrument**
  Status: `done`
  Goal: the open question left by `P0-PROFILE.10` — *which other "matched" claims rest on an
  instrument answering a narrower question?* Enumerate every pinned scalar that stands for a
  configuration, check each, and replace the pattern with a principle: a match is claimed against
  the **model's own self-description at the widest granularity it offers**, compared field by
  field. Both references emit a device tree; that is the wide instrument.
  Acceptance: every pinned scalar declares what it does **not** establish; the platform comparison
  is a tracked command, not a paragraph; any further instance found is fixed or enumerated.
  Verification: one further instance found and fixed (Spike's ISA was an input, not a read-back); 4 of 4 platform fields shown to disagree; rule 5b added and fired RED.
  Commit: `SEMULITH-MM-0033`

- ID: `MODEL-METHOD.2` — **the materials requirement: schema and catalogue**
  Status: `done`
  Goal: a record type binding each `docs/INFORMATION_CATALOG.md` category to the material kind
  that supplies it, with a **layer** (`processor` / `board` / `system`) and a disposition per
  **modelled unit**, plus the small registry of units themselves (id, kind, layer, book). The
  DSP-specific questions of §5 are carried as their own categories rather than folded into the CPU
  ones. ⛔ Start small: one unit exists, the registry has one row, and nothing is pre-built for
  kinds that have never been exercised.
  Acceptance: schema added; every category represented with an explicit layer; a `board`-layer
  category may not be dispositioned `missing` for a processor model; validates under
  `RECORD-SCHEMA`.

  Result: met, `2026-09-27`. `schema/units.sexp` + `schema/category-needs.sexp` declare the
  two families (zero kernel lines); `records_sexp.py` owns both mappings; `materials/units.sexp`
  carries the one-row registry (rv64i-lab-v0, processor); `materials/category-needs.sexp`
  carries all 24 INFORMATION_CATALOG categories with explicit layers — C01–C06, C22, C23
  covered; C07/C08/C12/C15/C16/C18 missing WITH reasons (excluded subsystems, owed and
  absent); C09, C13, C14, C24 partial; C17, C19, C20, C21 out-of-scope (board-layer, never
  owed by a processor). RECORD-SCHEMA rules 10–11 enforce the registry-nonempty and the layer
  honesty — the acceptance's `board × missing × processor` shape refuses as LAYER LIE (6 new
  arms, 32 total; 7 record files green). `.3`'s census now revises dispositions against
  evidence instead of inventing the record type.
  Design (recorded before code, `2026-09-27`), the catalog and the records machinery read first:
  - **Two record families on the records track, named so the basenames cannot collide with the
    profile's** — `materials/units.sexp` (the registry: `(unit (id …) (kind processor) (layer …)
    (book …))`, one row today) and `materials/category-needs.sexp` (one `(category-need …)` per
    INFORMATION_CATALOG category: category id, layer, the material kind that supplies it, the
    unit, the disposition, an optional reason). `schema/units.sexp` + `schema/category-needs.sexp`
    declare both; `records_sexp.py` owns both mappings; RECORD-SCHEMA gains both basenames and
    the layer-rule arm. The house path from `.3` (SOT-FORMAT.3), walked again.
  - **The disposition vocabulary is honest about the difference between absent and never-needed**:
    `covered` / `partial` / `missing` / `out-of-scope`. `missing` means the unit requires the
    category and the catalogue lacks the material — the acceptance's rule is the mechanical form:
    a board-layer category dispositioned `missing` for a processor unit is a lie about what was
    required (a processor never owed board-layer information), so the gate refuses it and names
    the category; the honest word is `out-of-scope`. Processor-layer exclusions this profile
    carries (privilege, translation, floating point, vectors, atomics) stay `missing` WITH a
    reason — they were owed and are absent — which is `.3`'s census to deepen with evidence.
  - **Layer assignment, stated**: processor — C01–C09, C10, C11, C13, C14, C15, C22, C23, C24;
    board — C17 (reset/time spans into the environment, per the catalog's own note), C19, C20,
    C21 ("not all properties of the CPU itself", per §3); system — C12 (translation spans into
    the OS), C16 (multicore), C18 (implementation observation). The first honest pass at
    `rv64i-lab-v0`'s 24 rows: covered where the profile genuinely owns the fact (C01–C06, C22,
    C23), missing-with-reason for the excluded processor-layer subsystems (C07 FP, C08 V, C12,
    C15, C16), out-of-scope for board-layer rows (C17, C19–C21), partial where the profile owns
    the shape but not the depth (C13 code visibility, C14 ECALL/EBREAK only, C24 replay policy
    declared not built, C09/C10/C11). `.3` revises every disposition it can evidence better.

- ID: `MODEL-METHOD.3` — **the coverage census for `rv64i-lab-v0`**
  Status: `done`
  Goal: fill the catalogue for the first model honestly. Expected outcome is that a **minority**
  of categories are covered — the profile excludes privilege, translation, floating point, vectors
  and atomics — and the value is in the `missing` rows, not the `covered` ones. ⛔ Device and
  interconnect categories are **`deferred-to-board`**, not missing: they are `P5-BOARD`'s to own,
  and the CPU records an assumption in their place.
  Acceptance: no category absent; each `missing` row names what would close it.


  Result: met, `2026-09-27`. The census swept the cached snapshot rather than trusting the
  first pass, and the evidence revised it: all 8 covered categories' subject matter verified
  present in the pinned pages, and — the measured surprise — the excluded subsystems' chapters
  (f/d/q/v/a-st-ext, rvwmo, counters, zicsr, zifencei) are IN the same snapshot. `missing`
  therefore means the profile excludes the subsystem (the facts are not part of this unit's
  model), not "material absent" — every one of the 6 missing rows now names its closer (a
  profile revision against snapshot chapters for C07/C08/C16; the separate Privileged
  Architecture manual for C12/C14/C15; the Debug specification for C18). Device and
  interconnect categories (C19/C20/C21) moved from `out-of-scope` to the new
  `deferred-to-board` disposition — P5-BOARD owns them and the CPU records an environment
  assumption in their place — and the census now reads: 10 covered, 4 partial, 6 missing (all
  closers named), 3 deferred-to-board, 1 out-of-scope (C17, contract-owned). RECORD-SCHEMA
  rule 12 (UNRESOLVED MATERIAL) keeps every named material honest against catalog.sexp; 33
  arms.

- ID: `MODEL-METHOD.4` — **acquire what the census says is missing and reachable**
  Status: `done`
  Goal: obtain and pin the materials the census identifies as needed for the *declared* scope, and
  record as `SRC-02` results those that cannot be obtained. ⭐ Includes the **run-real-code** set,
  which the ISA chapters do not own: the RISC-V psABI, the ELF specification, a startup/runtime
  contract, the compiler-runtime intrinsics a no-`M` soft-float target calls, and a program-exit
  convention. ⚠️ This is what makes `state.json`'s `software-convention` register roles
  load-bearing: once real code runs, the calling convention stops being background reading. ⭐ Includes the outstanding question
  from `MODEL-BOOKS.2`: does the specification's **PDF** rendering carry the instruction-format
  tables as selectable text? If so, encodings can be re-sourced from the primary document and the
  shared-ancestry position improves.
  Acceptance: every acquisition pinned with a digest and re-derivable; every failure recorded with
  its attempt.
  Result: met, `2026-09-27`. The run-real-code set is acquired, digest-pinned, cached on-volume at
  `.materials/run-real-code/` (gitignored, per the no-redistribution doctrine), and re-derivable
  from the curl commands below. The PDF question is answered YES with the extraction evidence.
  Design (recorded before code, `2026-09-27`), the fetch and provenance machinery read first:
  - ⭐ **Why the bytes are not gate-mechanized, stated rather than silently routed around.** The
    natural homes each refuse these documents for a measured reason: the profile's `sources.sexp`
    composes `base_url/file` — ONE origin per document, and this set is four origins; the
    materials catalogue's fetch seam copies from a `$ENV`-rooted corpus checkout — no URL kind;
    `docs/provenance/` manifests list TRACKED bytes — and third-party documents are not
    redistributed (the materials doctrine, for the same reason `.materials/` is gitignored). So
    the tracked record is THIS LEAF's digest table plus the cache README, and mechanizing a URL
    kind in `materials.py` is the named candidate if a second web-sourced set ever arrives.
  - **The acquisitions, each pinned (sha256 · bytes · cache path · re-derivation):**
    - `riscv-psabi.html` — the RISC-V psABI canonical render, `https://riscv-non-isa.github.io/riscv-elf-psabi-doc/` — `599f10a4b86090c18ded77c813ac89bc5e363e69e545653d46f3090f3f8c9b75` · 547,617 B. The calling convention: registers, stack, TLS. Re-derive: `curl -sSL -o .materials/run-real-code/riscv-psabi.html https://riscv-non-isa.github.io/riscv-elf-psabi-doc/`
    - `elf-gabi.pdf` — the System V / gABI ELF specification, `https://refspecs.linuxfoundation.org/elf/elf.pdf` — `422b6c64e91410fa83008aa2565532c9b523dfa33da8f56b4e2556a576b3ef18` · 345,215 B. Re-derive: `curl -sSL -o .materials/run-real-code/elf-gabi.pdf https://refspecs.linuxfoundation.org/elf/elf.pdf`
    - `linux-asm-generic-unistd.h` — the generic syscall numbers (exit = `__NR_exit`), `https://raw.githubusercontent.com/torvalds/linux/master/include/uapi/asm-generic/unistd.h` — `2e6a1b646c5111ad76db86c0508684223d9956384e1d23e86733eca09505d02d` · 32,020 B. The exit convention a hosted program expects; the laboratory's own harness contract (ECALL/EBREAK as typed environment traps) is the freestanding form, and this header is the hosted form's anchor. Re-derive: `curl -sSL -o .materials/run-real-code/linux-asm-generic-unistd.h https://raw.githubusercontent.com/torvalds/linux/master/include/uapi/asm-generic/unistd.h` ⛔ `master`-pinned: digest protects against silent change; a locator-stable pin is P1-LAB's refinement.
    - `compiler-rt-builtins-readme.txt` — LLVM compiler-rt's builtins inventory, `https://raw.githubusercontent.com/llvm/llvm-project/main/compiler-rt/lib/builtins/README.txt` — `3f89383ae3699e369853e9d6b1140f5372da356b76e86e1c13252810c2b83a97` · 15,334 B. Contains `__muldi3 (di_int a, di_int b); // a * b` — the soft-multiply intrinsic a no-`M` target calls. Re-derive: `curl -sSL -o .materials/run-real-code/compiler-rt-builtins-readme.txt https://raw.githubusercontent.com/llvm/llvm-project/main/compiler-rt/lib/builtins/README.txt`
  - **The PDF question, answered:** YES — the specification's PDF rendering carries the
    instruction-format tables as selectable text. Evidence: `riscv-spec.pdf` (release asset
    `riscv-isa-release-f443409-2026-09-26`) extracts 1.96 MB of text via `pdftotext`, and the
    RV32I format-table region yields clean cells — `funct7 / rs2 / rs1 / funct3 / rd / opcode`.
    Encodings CAN be re-sourced from the primary document; the shared-ancestry position
    improves the day a leaf chooses to. Cached at
    `.materials/run-real-code/riscv-spec-release-f443409.pdf` (`3f470aa95299fcbb…` · 5,522,367 B).
  - **SRC-02 records — the acquisitions that failed, each with its attempt:**
    - the **pinned revision's** release PDF: searched three pages of
      `riscv/riscv-isa-manual` releases for a `20260120`-tagged asset; none found (recent tags
      are per-commit `riscv-isa-release-<sha>-<date>`). The PDF answer above stands on the
      current release asset; matching it to the pinned `v20260120` revision is a follow-up
      attempt when the tag is located. Bounded claim: the answer is about the rendering FORM,
      which the asset demonstrates.
    - the **chipdoc corpus route**: `$SEMULITH_CHIPDOC_ROOT` is unset in this environment, so
      the feed the director flagged (psABI, SBI, BRS, U-Boot, DT, FU540, virtio, ACT) could not
      be read; the psABI was acquired from its canonical public render instead. When the
      variable is set, prefer the corpus copy and cross-check the digest.
    - the **startup/runtime contract**: not a document to acquire — the laboratory's harness
      contract already owns entry state and the ECALL/EBREAK exit convention (`D-ENTRY-STATE`,
      `OB-ENV-EVENT-DELIVERY`); the hosted-form anchors are the two acquisitions above.


  Result: met, `2026-09-27`. The unit registry gained `(requires …)` — the categories a
  unit's scope declares — and `SCOPE-COVERAGE` (19th doctrine, `scripts/check_scope_coverage.sh`,
  7 arms) refuses the day a required category is `missing` or has no census row, fired RED
  before registration on a scratch unit whose required category was absent. `rv64i-lab-v0`
  declares its 14 in-scope categories; the verdict reads `1 unit(s) may code — every required
  category covered` — **P1-LAB's precondition is now a gate's verdict, not a judgement call**,
  composed with EXTRACTION (coverage says the facts are OWNED; extraction says they are
  EXTRACTABLE; both must pass). The tree closes at 13/13.

- ID: `MODEL-METHOD.5` — **the method, in prose, written to be learned from**
  Status: `done`
  Goal: document → decision → requirement → obligation → check, with the judgement calls named:
  authority versus semantic class, what makes an expected value *derived* rather than copied, and
  when a disagreement is a profile difference rather than a defect. ⭐ Written so a student could
  apply it to a processor this project has never modelled — which means the **order** of the steps
  is justified, not merely listed, and the rejected alternatives are kept.
  Acceptance: one rule followed end to end by name; the non-mechanical steps identified as such;
  a reader could carry the method to a different ISA without this project's documents.

  Result: met, `2026-09-27`. `docs/METHOD.md` — one self-contained document, 9.3 KB, written to
  be carried off this repository — walks document → decision → requirement → obligation →
  check with the order justified at each step and the rejected alternatives kept. One rule
  (the shift-amount rule) is followed end to end by name, and its two non-mechanical steps are
  flagged inside the walk. A closing section names the four steps no gate can take (choosing
  the publication, classing the fact, judging the authority, classifying the disagreement) —
  everything else is declared mechanical, which is the method's discipline stated as a rule.
  The mdBook carries it verbatim under The contracts, the way the book handles every source
  document. The carryability probe: outside the worked example, the body references no tool,
  path, or id this project owns.
  Design (recorded before code, `2026-09-27`): the deliverable is one self-contained document,
  `docs/METHOD.md` — the method must be carryable OFF this repository, so it cannot live only in
  the mdBook's narrative or scattered across leaf checklists. The document is written against the
  method this session actually exercised (eleven leaves of it), with the rejected alternatives
  kept, and it names the non-mechanical steps honestly: pinning a source, judging an authority,
  choosing a profile over a reference's default — the steps no gate can take for you.

- ID: `MODEL-METHOD.7` — **the canonical definition: what it is and what each file owns**
  Status: `done`
  Goal: document the definition as a set of format-fit files with a **no-duplicated-fact** rule —
  which file owns configuration, state, encodings, semantics, requirements, obligations and
  provenance — and gate that rule, since "single source of truth" means *one owner per fact*
  rather than *one file*.
  Acceptance: every fact kind has exactly one owning file; a gate refuses a fact stated in two.

  Result: met, `2026-09-27`. `doctrine/fact_ownership.tsv` names the one owning file per fact
  kind (8 kinds), the legal derived mirrors, and the governing doctrine; `FACT-OWNERSHIP`
  (18th doctrine, `scripts/check_fact_ownership.sh`, 8 arms) verifies one owner each, owners
  exist, every mirror names a REGISTERED governor, and the corpus's four restatement pairs are
  all named. The inventory found one mirror with NO governor — 28 obligations restate their
  requirement's statement, all matching today but free to drift — so RECORD-SCHEMA gained rule
  9 (MIRROR: an obligation naming its `requirement_id` must state exactly what that requirement
  states, 3 new arms, 26 total). The acceptance's shape — a fact stated in two, refused — is
  the gate's UNGOVERNED MIRROR and UNREGISTERED MIRROR PAIR arms, both fired.
  Design (recorded before code, `2026-09-27`), the corpus's mirrors inventoried first:
  - ⭐ **The corpus already lives on derived mirrors — the rule must govern them, not pretend
    they don't exist.** Measured inventory: decisions↔requirements state the same fact in two
    files, governed by RECORD-SCHEMA rule 4 (statement identity); state↔profile, governed by
    PROFILE-CONSISTENCY rule 4 (agreement); the encoding composition↔its fragments, governed
    by UNIT-COMPOSITION (resolve + decide). ⛔ And one mirror with NO governor, measured:
    28 obligations carry a `requirement_id` and restate that requirement's statement — all
    matching today, but nothing REFUSES the day one drifts. That is the leaf's concrete fix:
    the governor gets built, then the registry names it.
  - **The ownership registry is data, beside the routes registry it mirrors in shape** —
    `doctrine/fact_ownership.tsv`: fact kind · the ONE owning file · its legal mirrors · the
    doctrine governing each mirror pair. The gate (`FACT-OWNERSHIP`, 18th doctrine) verifies:
    every owner exists; every fact kind has exactly one owner; every mirror names a governor;
    every governor is a REGISTERED doctrine that actually runs; and the corpus's enumerated
    mirror pairs are all named in the registry — a duplication the registry does not know
    about is the refusal. "One owner per fact; every mirror governed; nothing stated in two
    ungoverned."
  - **The new governor arm** (RECORD-SCHEMA): an obligation carrying
    `parameters.requirement_id` must state EXACTLY what that requirement states — refused by
    name with both statements' file and id. The 8 environment-assumptions keep their own
    statements (they assume, they do not mirror); the arm keys on the parameter, not the
    direction.

- ID: `MODEL-METHOD.8` — **own the encodings: `encoding.sexp`**
  Status: `done`
  Goal: close the measured gap that the repository does **not own its encodings** — the assembler
  reads them from `target/refs/riscv-opcodes`, which is untracked, so a fresh clone cannot build a
  model. Derive `encoding.sexp` from the pinned table, track it, and gate that it still agrees.
  Acceptance: `git ls-files` shows the encodings tracked; the assembler reads the tracked file; a
  gate fires RED when the tracked file and the pinned upstream disagree.
  Verification: the full evidence path builds with the upstream directory HIDDEN; re-derivation fired RED on a one-bit edit.
  Commit: `SEMULITH-MM-0037`

- ID: `MODEL-METHOD.9` — **the semantics: `semantics.sexp`**
  Status: `done`
  Goal: what each of the declared instructions *does*, as expressions, each carrying the source
  locator it was derived from so a reviewer can check the expression against the sentence.
  Acceptance: every instruction in the declared scope has semantics; every form cites a locator;
  the file parses under a tracked reader that **refuses** a form it does not implement.
  Verification: 52 of 52 instructions, every rule cited; 4 controls fired RED; the language is 32 forms, each added because an instruction needed it.
  Commit: `SEMULITH-MM-0040`

- ID: `MODEL-METHOD.10` — **the extraction contract: is the definition SUFFICIENT?**
  Status: `done`
  Goal: state what a generator engine must be able to extract, and check it — every declared
  instruction has an encoding **and** semantics **and** a requirement; every state element has a
  reset; every obligation has its checks. ⭐ This turns *"the engine can extract all it needs"*
  from an intention into a verdict, and that verdict is the precondition for writing model code.
  Acceptance: fired RED by removing one instruction's semantics; `P1-LAB` cites this check rather
  than a judgement call.

  Result: met, `2026-09-27`. The contract as stated fired RED on the real corpus — measured:
  the ALU family (13 instructions) had no requirement at all. The leaf extended the catalogue
  (D/REQ/OB-ALU-REG and -IMM, statements grounded in the corpus's own §1.1.4 semantics), added
  the `(insns …)` coverage link to 11 requirements, and `scripts/check_extraction.py` now
  decides the integrative claim — SCOPE == ENCODING == SEMANTICS == REQUIREMENTS, one set four
  ways, plus every state element reset and every obligation checked both ways. The real corpus
  is SUFFICIENT (52 instructions, each with all three; the G0 report re-derived to 28/28/36/72
  in the same commit). The acceptance fired RED on a real-corpus copy with one instruction's
  semantics removed (`scope declares 1 instruction(s) the semantics set does not cover: add`).
  `EXTRACTION` registered as the 17th project doctrine — P1-LAB cites a verdict that runs.
  Design (recorded before code, `2026-09-27`), the contract read against the corpus first:
  - ⭐ **The contract as stated fires RED on the real corpus today — measured, and the point.**
    The scope declares 52 instructions; the encoding union and the semantics cover 52; but the
    requirement leg fails: only 7 instruction-kind requirements exist, and even generous
    family-mapping leaves the whole ALU family (ADD/SUB/SLT/SLTU/XOR/OR/AND + the immediates
    ADDI/SLTI/SLTIU/XORI/ORI/ANDI) with no requirement at all. A contract that passes over that
    is the intention restated. So this leaf extends the catalogue where the contract demands
    it: two new decision/requirement/obligation triples (D-ALU-REG, D-ALU-IMM), and an explicit
    instruction-coverage link on every requirement that names specific instructions.
  - **The link is data, added the way the layer allows**: `schema/requirements.sexp` gains
    `(insns …)` — an optional repeated string field, kind-agnostic (FENCE is a memory-kind
    requirement that names one instruction; ECALL-EBREAK an event-kind naming two). Every
    requirement whose statement commits specific instructions names them; reserved/hint decode
    requirements name none (they cover code points, not instructions).
  - **The contract is one equality across four sets + two smaller legs.**
    `scripts/check_extraction.py <unit-dir>` derives: SCOPE (the profile's declared names),
    ENCODING (the composed union), SEMANTICS (checked semantics coverage), REQUIREMENTS
    (∪ requirement.insns) — and requires all four EQUAL. Plus: every state element in
    `state.sexp` carries a `reset` (the corpus already does — integer_registers and pc); every
    obligation carries a positive AND a negative check. A gap names itself, the instruction,
    and the set that's short.
  - **Consequences, stated before code**: the catalogue grows (2 decisions, 2 requirements,
    2 obligations) and the tracked G0 report regenerates (more requirements → more checks,
    verdict unchanged) — `GATE-REPORT` re-derives the new bytes and is part of this commit.
    The ALU statements are sourced from the pinned chapters (RV32I §1.1.4 computational
    instructions; overflow-wrap and signed-comparison facts the corpus already states for
    kin instructions), with locators a reader can check.

- ID: `MODEL-METHOD.11` — **the primary-source corpus: a local cache that holds no absolute path**
  Status: `done`
  Goal: a curated corpus of vendor ISA/architecture manuals became available (`chipdoc`, 3,684
  files / 1.5 GB, 196 PDFs, explicitly curated *"to build software emulators (ISS) that run real
  C/C++/Rust software"*). It lives **outside this repository**, so naming it directly would put an
  absolute path in a tracked file — the exact thing Policy 12 forbids, because the repository must
  survive being moved to another filesystem. Give materials a home, an identity and a resolver that
  is relative all the way down.
  Acceptance: a tracked S-expression catalogue keyed by material id carrying title, revision,
  `sha256`, licence and a **repo-root-relative** cache path; a gitignored `.materials/` cache; a
  resolver that verifies the digest and, when a material is absent, refuses with the command that
  populates it; the external corpus reached **only** through an environment variable the repository
  never stores; `grep` for the corpus's absolute path across tracked files returns 0.
  ⛔ Sequenced before `.2`–`.4` deliberately: the census cannot record *where a material is* until
  "where" has a form that does not break when the repository moves.
  Verification: 22 materials catalogued and fetched, every digest verified; `0` tracked files name
  the corpus root; 15 self-test arms, 9 of them RED about paths.
  Commit: `SEMULITH-MM-0042`

- ID: `MODEL-METHOD.12` — **a citation that is present is not a citation that resolves**
  Status: `done`
  Goal: an external investigation challenged this profile's pinned source, reporting that no
  public build of `riscv-isa-manual` produces the §1.1 / §3.1 numbering all 52 semantic citations
  use. Re-derived: the challenge is **refuted** — 52 of 52 resolve in the pinned artifact, which is
  live, HTTP 200 and byte-identical to the committed digests. But the challenge was only possible
  because **nothing checked that a citation resolves**: `check_semantics.py` asks whether a
  citation is *present*, and a citation that points nowhere is still present. Close that, and close
  the ambiguity in `sources.toml` that made the wrong publication a reasonable guess.
  Acceptance: a tracked instrument resolves every semantic citation against the pinned artifacts
  and names the offending locator on failure, fired RED on a locator that does not exist; it
  refuses with instructions when the artifacts are not fetched rather than reporting success;
  `sources.toml` names its **publication**, not just a version string.
  ⛔ Not a commit gate: the artifacts are fetched, untracked and need the network, and the
  rendering declares no redistribution licence (`OQ-4`), so a fresh clone cannot run it. A gate
  that silently passes when its evidence is absent is the defect, not the fix.
  Verification: challenge refuted — 52 of 52 resolve, pinned URLs live and byte-identical; 10
  self-test arms; absent-evidence control refuses.
  Commit: `SEMULITH-MM-0043`

- ID: `MODEL-METHOD.13` — **the corpus moved, and my survey had sampled rather than swept**
  Status: `done`
  Goal: the corpus advanced three commits (`4201f50` → `3c45e81`) and both gaps this project
  measured are now closed at the source — 5 AMD64 APM volumes and Intel SDM Volume 1 imported.
  It also **moved** the RISC-V PDF, which breaks `--fetch` for a catalogued material today. And a
  re-survey found that my first pass **sampled by guessing vendor directory names** (`zilog`,
  `wdc`, `openrisc`, …) instead of sweeping by path, so it missed eight processor-class documents
  including an entire architecture, M68000, which sits under `nxp/m68k/` rather than a `motorola/`
  directory that does not exist.
  Acceptance: the catalogue is re-derived from a **path sweep**, not a sample, and says so; the
  corpus revision is re-pinned and drift from it is detected rather than discovered; both gap
  records are closed **with evidence and kept**, never deleted; the pinned `v20260120` HTML
  snapshot (72 pages + a verifying manifest) becomes a first-class material, which makes
  `check_citations.py` runnable from the cache **offline**; `--fetch` succeeds for every material.
  ⭐ The corroboration is worth recording on its own: chipdoc independently acquired the
  `v20260120` snapshot by its own route, and its digests for `intro`, `rv32` and `rv64` equal the
  ones committed in `sources.toml`. Two acquisitions, one set of bytes.
  Verification: 22 → 36 materials, 36 of 36 fetched; both gaps closed with evidence; citations
  resolve 52 of 52 **offline**; 20 self-test arms.
  Commit: `SEMULITH-MM-0044`

- ID: `MODEL-METHOD.6` — **no coding without the source of truth, mechanized**
  Status: `done`
  Goal: a gate that refuses model implementation for a profile while a category its declared scope
  requires is `missing`. The rule is the director's; this makes it enforceable rather than
  remembered.
  Acceptance: fired RED against a deliberately uncovered category; `P1-LAB`'s precondition is the
  gate's verdict rather than a judgement call. Composes with `.10`: a category may be covered while
  the definition is still insufficient, and both must pass.

