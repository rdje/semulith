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

