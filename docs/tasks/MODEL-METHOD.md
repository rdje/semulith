# MODEL-METHOD: the method for modelling a processor, and the materials that method requires

## Metadata

- Tree ID: `MODEL-METHOD`
- Status: `active`
- Roadmap lane: cross-cutting; precedes implementation for **every** model, CPU or DSP
- Gate: contributes the precondition `P1-LAB` must satisfy before any model code is written
- Depends on: `P0-PROFILE` (the first model), `docs/INFORMATION_CATALOG.md` (the 24 categories)
- Unlocks: `MODEL-BOOKS` (which renders this), and a defensible start to `P1-LAB`
- Created: `2026-09-14`
- Owner: repo-local workflow

## Goal

Make two things explicit that the project has so far done implicitly and therefore unevenly:

1. **The method.** How a pile of specification documents becomes a model — document, decision,
   requirement, obligation, check — with the judgement calls named rather than absorbed.
2. **The materials the method requires.** `docs/INFORMATION_CATALOG.md` already states *what you
   must know* to model a processor, in 24 categories. Nothing states **which document supplies
   each category**, and nothing says which categories are supplied by **nothing at all**. That
   second list is the important one: it is the set of things the project would otherwise invent.

Both are captured **machine-readably**, so coverage is a query rather than a reading, and
implementation cannot begin over an uncovered category without a gate saying so.

## Non-Goals

- Not a rewrite of `docs/INFORMATION_CATALOG.md`. That file is the delivered taxonomy of *what
  must be known*; this tree adds the *material that supplies it* and the *coverage census*.
- Not model code. Explicitly the opposite: this tree exists so that code starts from sources
  rather than from recall.
- Not an acquisition of every conceivable document. A category irrelevant to a declared scope is
  marked `not-applicable` **with its reason**, which is a different statement from `missing`.

## Acceptance Criteria

1. Every catalogue category has, per model, exactly one disposition: `covered` (naming the
   material and its locator), `missing` (naming what would close it), or `not-applicable` (with
   the reason). No category may be silently absent.
2. The catalogue is machine-readable, schema-validated, and gated — a coverage claim is a query,
   not a sentence someone wrote.
3. The method is documented in prose, following at least one real rule end to end.
4. A gate prevents implementation beginning while a category the declared scope *needs* is
   `missing` — the director's rule, mechanized: no coding without the source of truth.

## Format decision — and why not S-expressions, yet

**The catalogue is JSON Lines against a JSON Schema.** The call was mine and the reasoning is
recorded so it can be overturned on evidence rather than taste:

- This repository already carries a **tracked, gated, self-refusing** JSON Schema validator
  (`scripts/validate_records.py`) and a doctrine (`RECORD-SCHEMA`) that validates every `.jsonl`
  and cross-checks it against its profile. A materials catalogue in JSONL inherits both on day one.
- The data is **flat and heterogeneous** — a category, a disposition, a locator, a digest. That is
  a record, not a tree. S-expressions buy nothing over JSON for records, and cost a parser, a
  schema mechanism and a fourth tracked format.
- ⭐ **Where S-expressions WOULD earn their place is the canonical executable semantics** — the
  *executable definition* of `docs/ARCHITECTURE.md` §4, where an instruction's meaning is a nested
  expression and pattern-matching over it is the whole job. That is exactly why Sail, ACL2 and the
  ISA-formalism tradition use them, and it is a `P1-LAB` decision, not a `P0` one.
- **Trigger to revisit:** the first time a material must carry a *nested semantic expression*
  rather than a citation, this decision is re-opened in `P1-LAB` with that material as the
  worked example.

## Task Tree

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
  Status: `pending`
  Goal: a record type binding each `docs/INFORMATION_CATALOG.md` category to the material kind
  that supplies it, with a disposition per model, and the DSP-specific questions of §5 carried as
  their own categories rather than folded into the CPU ones.
  Acceptance: schema added; every category represented; validates under `RECORD-SCHEMA`.

- ID: `MODEL-METHOD.3` — **the coverage census for `rv64i-lab-v0`**
  Status: `pending`
  Goal: fill the catalogue for the first model honestly. Expected outcome is that a **minority**
  of categories are covered — the profile excludes privilege, translation, floating point, vectors,
  atomics and devices — and the value is in the `missing` rows, not the `covered` ones.
  Acceptance: no category absent; each `missing` row names what would close it.

- ID: `MODEL-METHOD.4` — **acquire what the census says is missing and reachable**
  Status: `pending`
  Goal: obtain and pin the materials the census identifies as needed for the *declared* scope, and
  record as `SRC-02` results those that cannot be obtained. ⭐ Includes the outstanding question
  from `MODEL-BOOKS.2`: does the specification's **PDF** rendering carry the instruction-format
  tables as selectable text? If so, encodings can be re-sourced from the primary document and the
  shared-ancestry position improves.
  Acceptance: every acquisition pinned with a digest and re-derivable; every failure recorded with
  its attempt.

- ID: `MODEL-METHOD.5` — **the method, in prose**
  Status: `pending`
  Goal: document → decision → requirement → obligation → check, with the judgement calls named:
  authority versus semantic class, what makes an expected value *derived* rather than copied, and
  when a disagreement is a profile difference rather than a defect.
  Acceptance: one rule followed end to end by name; the non-mechanical steps identified as such.

- ID: `MODEL-METHOD.6` — **no coding without the source of truth, mechanized**
  Status: `pending`
  Goal: a gate that refuses model implementation for a profile while a category its declared scope
  requires is `missing`. The rule is the director's; this makes it enforceable rather than
  remembered.
  Acceptance: fired RED against a deliberately uncovered category; `P1-LAB`'s precondition is the
  gate's verdict rather than a judgement call.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `MODEL-METHOD.2` | `pending` | the schema the census needs, now that the instruments it will rest on have been checked |
| 2 | `MODEL-METHOD.3` | `pending` | the census, whose `missing` rows drive acquisition |
| 3 | `MODEL-METHOD.4` | `pending` | acquisition, including the outstanding PDF-encoding question |

## Decisions

- `2026-09-14`: the catalogue is **JSON Lines against a JSON Schema**, not S-expressions — see the
  format section above, including the trigger that would re-open it.
- `2026-09-14`: `docs/INFORMATION_CATALOG.md` remains the **single owner** of what must be known.
  This tree adds a *material* and a *disposition* per category; it does not restate the category
  definitions, because a second copy of a taxonomy is a second thing to keep correct.

## Open Questions

- Does the specification PDF carry instruction encodings as text? Owner: `MODEL-METHOD.4`.
- Should DSP categories extend C01–C24 or form a parallel set? Deferred to `P3-BREADTH`, when a
  real DSP target exists to test the answer against. `§5` of the catalogue is carried as its own
  category group in the meantime.

## Blockers

- None.

## Acceptance Checklist (current leaf — `MODEL-METHOD.1`)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. `P0-PROFILE.10` corrected one instance of a pattern and
  left the general question open: *which other "matched" claims rest on an instrument answering a
  narrower question?* WHERE: every pinned scalar in `references.toml` that stands for a
  configuration. The sweep enumerated them and checked each rather than reasoning about them:

  ```
  $ grep -cE 'matched_isa_string|matched_config' profiles/rv64i-lab-v0/references.toml
  6
  $ spike --help | grep -icE 'print.*isa|dump.*isa'
  0
  ```

  ⛔ **A second instance, and worse than the first.** `spike.matched_isa_string = "rv64i"` was the
  command-line **input** recorded in an observation's slot. Spike has no `--print-isa` option, so
  nobody had ever confirmed it configured what it was told. The first instance was a narrow
  reading; this one was not a reading at all.

- [x] **ADDRESSED (verified)** — the scalar is now **read back**, from a surface Spike does offer:

  ```
  $ spike --isa=rv64i  --priv=m --dump-dts <elf> | grep riscv,isa    ->  riscv,isa = "rv64i"
  $ spike --isa=rv64im --priv=m --dump-dts <elf> | grep riscv,isa    ->  riscv,isa = "rv64im"
  ```

  The second line is the control: the read-back tracks the input, so it is an observation and not
  an echo. ⭐ **And the replacement principle is now an instrument.** Both models emit a device
  tree — the widest self-description either offers — so `scripts/compare_platforms.py` compares
  them field by field instead of trusting a scalar:

  ```
  FIELD                  sail (matched)           spike (matched)          agree
  riscv,isa              "rv64i_zvl32b"           "rv64i"                  NO
  mmu-type               "riscv,none"             "riscv,sv57"             NO
  riscv,pmpregions       <absent>                 <0x10>                   NO
  timebase-frequency     <500000000>              <0x989680>               NO
  devices only spike advertises: clint@2000000, cpu@0, ns16550@10000000, plic@c000000
  ```

  **4 of 4 platform fields disagree and Spike advertises four devices Sail does not** — a UART, a
  platform interrupt controller, an interruptor and a CPU node, plus an Sv57 MMU and 16 PMP
  regions. None of that is visible in an ISA string, which is the entire point.

- [x] **NO REGRESSION** — leg 2. The discipline is enforced rather than remembered: rule 5b in
  `PROFILE-CONSISTENCY` refuses a pinned `matched_isa_string` that does not declare **both** what
  it does not establish and where it was read from. Fired RED on the real dossier:
  `UNSCOPED SCALAR rv64i-lab-v0/spike: pins 'matched_isa_string' with no 'matched_scope'`.
  `--self-test` → `39 pass / 0 fail` (36 → 39); 39 arms written, 39 run. Whole gate
  `=== all doctrines green ===`; `make check` → `test result: ok. 1 passed; 0 failed`;
  `scripts/run_smoke.py` → `ok`, so the evidence path is undisturbed.
  ⚠️ **The wide instrument has its own scope, and the module says so rather than implying it.** A
  device tree describes what a platform *advertises* — not semantics, not memory attributes — and
  it carries residue: Sail's tree still advertises a `timebase-frequency` and an `htif` node with
  no device behind them. **Wider is not complete**, so the honest claim is "these fields agree",
  never "the models match". Recording that is what stops this instrument becoming the next
  narrow one.

- [x] **FIX** — `scripts/compare_platforms.py` added; `matched_scope` and
  `matched_isa_string_source` added to all three candidates (including QEMU, whose emptiness is
  now visible rather than inferred from an absent row); rule 5b registered with three arms.

- `promotion: declined (the lesson is stated in compare_platforms.py's docstring and in rule 5b's header, both of which a reader meets before they could act on it; the existing zero-hits-absence-or-blindness card carries the neighbouring failure mode, so a new card would be cross-references only)`

- [x] **LOCKSTEP** — leg 3: the scope declarations are gated on every commit and the platform
  comparison is a tracked command. `TOOLBOX.md` gains the instrument; `MEMORY.md`,
  `LIVE_STATUS.md`, `CHANGELOG.md` and `DEV_NOTES.md` updated in this commit.
  ⛔ **The answer to the open question, stated plainly: one further instance existed, it is fixed,
  and the pattern is now gated.** I am not claiming there are no others — I am claiming that a new
  one cannot be *added* without declaring its scope, which is the only durable form of that answer.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-14` | `MODEL-METHOD.1` | sweep over every pinned configuration scalar | 1 further instance found: Spike's ISA was an input, not a read-back |
| `2026-09-14` | `MODEL-METHOD.1` | Spike ISA read-back, with its control | `rv64i` → `rv64i`; `rv64im` → `rv64im` |
| `2026-09-14` | `MODEL-METHOD.1` | `compare_platforms.py` on both matched models | 4 of 4 fields disagree; 4 devices only Spike advertises |
| `2026-09-14` | `MODEL-METHOD.1` | rule 5b fired RED on the real dossier | `UNSCOPED SCALAR …/spike` |
| `2026-09-14` | `MODEL-METHOD.1` | `check_profile_consistency.sh --self-test` | `39 pass / 0 fail`; 39 written, 39 run |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `MODEL-METHOD.1` | `SEMULITH-MM-0033 (leaf MODEL-METHOD.1): answer the narrower-instrument sweep with a wider instrument` | 1 further instance found and fixed; the pattern gated |

## Changelog

- `2026-09-14`: Created. The project could state *what must be known* to model a processor (24
  catalogue categories) but not *which document supplies each*, nor which are supplied by nothing.

  Census behind that claim, over every population that could refute it — any tracked file binding a
  catalogue category id to a material, and any tracked schema for such a record:

  ```
  $ grep -cE '^\| C[0-9]{2} \|' docs/INFORMATION_CATALOG.md
  24                                    # C01..C24, one table row each
  $ git grep -lE 'C(0[1-9]|1[0-9]|2[0-4])\b' -- profiles schemas doctrine | wc -l
  0                                     # nothing binds a category to a material
  $ git grep -lE '"category"' -- schemas
  schemas/requirement.schema.json       # a DIFFERENT sense: source_semantics.category
  ```

  The categories are defined in exactly one place, nothing binds one to a material, and the single
  schema hit is a false friend — `source_semantics.category` classifies a requirement's *semantic
  status* (defined / implementation-defined / unspecified), not an information category. That gap
  is what this tree closes.
  ⛔ Two of the three numbers above were **typed before they were run**, and were wrong (`0` for a
  population that is `1`, and `24` from a grep that actually counted 26 lines because the file
  mentions some ids again in prose). They are corrected here from the commands' real output — in
  the same leaf that exists to stop a scalar being trusted without checking what it ranges over,
  which is the joke writing itself.
