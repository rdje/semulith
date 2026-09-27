# `SOT-FORMAT` — completed-leaf evidence (archive)

> Split out of [`../SOT-FORMAT.md`](../SOT-FORMAT.md) on `2026-09-27`, when that file crossed the
> `docs/tasks/` per-part ceiling (79,270 bytes against 65,536). The registry that sets the ceiling
> names this as the intended response — *"the per-part ceiling is the one that actually bites, and
> it bites on the right thing: a tree whose archive should be compacted or split"* — so the
> ceiling was obeyed rather than raised.
>
> ⛔ **Nothing here is edited when it moves.** These are the acceptance checklists exactly as they
> were accepted at commit time; an archive that gets tidied is no longer evidence of what was
> claimed. The live tree keeps the frontier, the decisions, the open questions, the current
> leaf's checklist and both logs.
>
> This directory is deliberately a subdirectory: `FRONTIER-SYNC` treats every `docs/tasks/*.md`
> as a tree needing an index row, and an archive is not a tree.

## The archive

## Acceptance Checklist (leaf SOT-FORMAT.2)

- [x] **REPRODUCE / ISSUE** — the problem, shown (not asserted):

  ```
  $ sed -n '26,43p' scripts/check_semantics.py          # before the fix
    FORMS: dict[str, int | None] = { "reg": 1, "pc": 0, … "trap": 2 }     # the language, as a Python literal
  $ ls schema/
    schema.sexp                                          # a schema for the schema language only —
                                                         # encoding/fragment/semantics had no schema at all
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHY: the record grammar of `schema.sexp` cannot state
  the positional mini-languages the corpus actually writes, and the semantics checker enumerated
  the language itself — "extensible by data" was true only for record-shaped constructs. WHERE:
  the gap sat between `schema/schema.sexp` and `definitions/riscv/{rv64i,m}.sexp` +
  `rv64i.sem.sexp` (three shapes: `(fixed (31 25 0x0) …)` triples, `(operands rd rs1 rs2)`
  symbol lists, 32-head effect expressions), and at the FORMS dict in `scripts/check_semantics.py`.

- [x] **FIX** — leg 2. One new declaration kind, `(operator (name SYM) (fixed N) | (variadic)
  [(min N)] [(arg SPEC)])`, kernel-parsed next to `(construct …)`/`(field …)`; three schema files
  (`encoding`, `fragment`, `semantics`); `check_semantics.py` loads the form table from
  `schema/semantics.sexp` through the kernel's loader. New constructs and new operators are data;
  a fifth kind would change the kernel — the named boundary.

- [x] **ADDRESSED (verified)** — leg 3, the acceptance criteria, each re-derived:

  ```
  $ grep -c '^(operator' schema/semantics.sexp
    32                                                   # the 32 forms are data
  $ python3 scripts/check_semantics.py definitions/riscv/rv64i.sexp definitions/riscv/rv64i.sem.sexp
    …  52 of 52 declared instruction(s) have checked semantics          (diff vs baseline: identical)
  $ # four MODEL-METHOD.9 controls: missing / unknown-form / bad-operand / no-source
    → each rc 1, refused by name (three byte-identical; unknown-form's message now names the schema)
  $ # 33rd form: append one (operator …) line, no Python touched
    unknown form 'rot' rc 1 → 1 of 1 declared instruction(s) have checked semantics rc 0 → reverted
  ```

- [x] **NO REGRESSION** — leg 4. `sexp --self-test` `18/0`; `check_sexp_schema --self-test`
  `31/0`; `materials --self-test` `20/0`; `check_citations.py` `52 of 52`; `run_smoke.py` `ok`;
  `gen_fragments.py` regeneration byte-identical (`git diff --stat -- definitions/` empty);
  `check_encoding_disjoint.py` `the fragments COMPOSE`; `bash scripts/check_doctrines.sh`
  `=== all doctrines green ===`.

- [x] **LOCKSTEP** — `TOOLBOX.md` row updated; `docs/ARCHITECTURE.md` §1.3 brought current (it
  still described the schema layer as "specified as `SOT-FORMAT.1`, not yet built" — stale since
  `SEMULITH-SF-0054`); `MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md` (+ its lesson promoted to
  `docs/knowledge/the-corpus-writes-shapes-my-grammar-cannot-state.md`), `docs/TASK_TREE.md`
  and this tree in the same commit. Gate registration of the schema layer is deferred to `.6`
  per the tree's frontier — stated here so the deferral is a decision, not a gap.

## Acceptance Checklist (leaf SOT-FORMAT.9 — acceptance MET 2026-09-26)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHERE: `vendor/linkedspec/specs/Lispish.spec:69`.

  ```
  $ python3 scripts/compare_readers.py
    DIFFER  materials/catalog.sexp  <root>: A has 43 element(s), B has 6
    compare_readers: 4 of 5 file(s) agree
  $ grep -n 'dquotes:\|others:' vendor/linkedspec/specs/Lispish.spec
    69:dquotes: /"(.*?)(?<!\\)"/     I.return(...)      # `.` does not match LF without DOTALL
    84:others:  /[^\s"{}()\[\];]+/   I.return(...)      # what the text falls through to
  ```

  WHY it is severe rather than cosmetic: the string does not merely lose its newline, it **stops
  being a string**, and its remaining text is re-lexed as syntax. A `)` in the continuation closes
  a form that was never open, so siblings are absorbed into the wrong parent — and it exits 0.

  ```
  (r (a "x\n   y") (b "z"))   ->  ["r",["a","x","y) (b z"]]        want ["r",["a","x\n   y"],["b","z"]]
  materials/catalog.sexp       ->  6 top-level forms, 37 of them nested inside the fifth (want 43)
  ```

  ⛔ Located by refutation, not by guessing: I first hypothesised `;` inside a string, then
  parentheses inside a string. **Both were wrong** — the reader handles them correctly — and the
  controls that pass (spaces, parens, TAB, CR, all on one line) are what localise it to LF.

- [x] **ADDRESSED (verified)** — leg 2. Director instruction `2026-09-26`: upstream fixed and
  pushed; the pin advances to `a8d34c84595d46c24cd1820d5fc0414261706412` (`origin/main` tip), which
  ships the fix as upstream commit `8259719f8` — the `(?s)` DOTALL form on `dquotes`/`squotes` that
  this project validated and reported:

  ```
  $ git -C vendor/linkedspec show a8d34c845:specs/Lispish.spec | grep -n 'dquotes:\|squotes:'
    69:dquotes: /(?s)"(.*?)(?<!\\)"/     I.return(...)
    71:squotes: /(?s)'(.*?)(?<!\\)'/     I.return(...)
  ```

  The documented update flow was followed: fetch → check out the reviewed revision → RGX
  bootstrap (no-op, "already generated"; RGX unchanged at `8763a0e6` on both pins) → rebuild the
  consumer (20.39 s, fresh binary at `.app-data/target/debug/lispish_file`) → verify → only then
  commit the pointer. The LS-001 reproduction re-ran against the new pin:

  ```
  $ bash docs/upstream/linkedspec/LS-001-multiline-string/repro.sh \
      .app-data/target/debug/lispish_file vendor/linkedspec/specs/Lispish.spec
    LS-001: 8 matched / 0 differed        (was 4 matched / 4 differed)
  ```

- [x] **NOT MET → MET — the readers agree on every tracked file, and the residue is classified,
  not hidden.** The fix moved the disagreement one layer down, and this layer is documented
  upstream behaviour, enumerated by the comparator rather than counted as agreement-in-spite-of:

  ```
  $ python3 scripts/compare_readers.py
    agree   definitions/riscv/m.sexp                        438 nodes identical
    agree   definitions/riscv/rv64i.sem.sexp               1550 nodes identical
    agree   definitions/riscv/rv64i.sexp                   1716 nodes identical
    agree   materials/catalog.sexp                         1792 nodes identical
    class   materials/catalog.sexp [5][3][1]:  A='20260911' B=20260911  — quoted-numeric (LS-002)
    class   materials/catalog.sexp [5][7][1]:  …\"… vs "…  — escape-retention
    class   materials/catalog.sexp [29][9][1]: …\"… vs "…  — escape-retention
    class   materials/catalog.sexp [36][3][1]: A='1992' B=1992 — quoted-numeric (LS-002)
    agree   profiles/rv64i-lab-v0/encoding.sexp              18 nodes identical
    compare_readers: 5 of 5 file(s) agree
  ```

  Both `class` families follow from Lispish's PUBLISHED extraction contract (its guide documents
  both the quote-kind discard and escape retention), so they are CLASS, not defects. The
  classifier cannot mask a real difference: `quoted-numeric` requires `sexp._atom(A) == B`
  exactly, `escape-retention` requires decoding B with sexp.py's own escape table to reproduce A
  exactly. Proof it still discriminates, fired both ways after the change:

  ```
  $ python3 scripts/compare_readers.py --self-test          -> 21 pass / 0 fail
    (9 new arms: GREEN ×4 classification, RED ×5 masking — different int, non-numeric,
     undecodable retention, trailing backslash, unequal strings)
  $ LISPISH_GRAMMAR=<old pre-fix spec> compare_readers.py materials/catalog.sexp
    DIFFER <root>: A has 43 element(s), B has 6          rc=1   — the defect still fires RED
  ```

- [x] **NO REGRESSION** — leg 3. The submodule's content is untouched by us (clean checkout of
  upstream's commit); the gate set and the consumers of the reader:

  ```
  $ python3 scripts/sexp.py --self-test          -> 18 pass / 0 fail
  $ python3 scripts/check_citations.py | tail -1 -> 52 of 52 … resolve
  $ python3 scripts/materials.py --self-test     -> 20 pass / 0 fail
  $ python3 scripts/run_smoke.py | tail -1       -> run_smoke: ok …
  $ bash scripts/check_doctrines.sh              -> all doctrines green
  ```

- [x] **LOCKSTEP** — `vendor/` gitlink committed with: LS-001 record moved `draft` → `verified`
  (with the `verified-against` pin the UPSTREAM-INDEX gate requires), both index mirrors, the
  vendor README, LS-001's REPORT.md, `MEMORY.md`, `CHANGELOG.md`, and this tree — one commit.

## DEPARTURES FROM THE PUBLISHED GUIDE

The acceptance says the integration follows the published document and that departures are named.
Three from `2026-09-20`, all mine, all corrected upstream since (the guide now teaches each):

1. **Jumped to line 198** as directed and skipped *Initial PGEN preparation* 100 lines earlier.
   Build failed on `generated/return_annotation_parser.rs`. The guide is explicit — *"Checkout does
   not generate PGEN's parser inputs"* — and I had not read it.
2. **Used `git submodule update --init --recursive`** where the guide prescribes two targeted
   inits. Cost: 1.7 GB and 30 nested submodules instead of the needed closure.
3. **Used bare `cargo` and my own target directory** instead of `tools/run_cargo_local.sh` and the
   prescribed `.app-data/` layout. Corrected; the guide's layout is also the one Policy 13 wants.

One new, named rather than corrected: the guide's Lispish section now prescribes **copying the
consumer source into the application's own crate**; this project builds the vendored example
workspace in place (binary lands at the same `.app-data/target/debug/lispish_file` the harness
reads), because the semulith root manifest is a virtual workspace with no package to own a
`src/bin/`. The guide itself documents the example as runnable; the previous pin's verified build
did the same. Revisit when the engine crate adopts the reader.

## Acceptance Checklist (leaf SOT-FORMAT.1)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHERE: "it parses" was the only gate an S-expression
  file faced — the reader accepts a mistyped head silently, exit 0:

  ```
  $ printf '(sourcs (id "u") (width 32))' > target/doctrine_scratch/sourcs.sexp
  $ python3 scripts/sexp.py target/doctrine_scratch/sourcs.sexp
  ok: 1 top-level form(s); heads: sourcs          (rc=0 — nothing refused the typo)
  ```

- [x] **ADDRESSED (verified)** — leg 2. `schema/schema.sexp` is the language in itself;
  `scripts/check_sexp_schema.py` validates any file against any schema and refuses by name:

  ```
  $ python3 scripts/check_sexp_schema.py schema/schema.sexp schema/schema.sexp
  check_sexp_schema: ok — schema/schema.sexp conforms to schema.sexp
  $ python3 scripts/check_sexp_schema.py --self-test
  check_sexp_schema --self-test: 16 pass / 0 fail
  ```

  The 13 RED arms name their reason: undeclared construct, undeclared field, missing required
  field, three wrong-arity shapes, two wrong-value-type shapes, duplicated single-valued field,
  values restriction, wrong form head, recursive-nesting violation, two meta-level schema abuses.

- [x] **NO REGRESSION** — leg 3. The schema layer is additive; no consumer changed. The enforcer
  after staging: `bash scripts/check_doctrines.sh → === all doctrines green ===`.

- [x] **LOCKSTEP** — `schema/` registered in `doctrine/readme_routes.tsv` in the creating commit
  (partitioned, same shape as `definitions/`); `TOOLBOX.md` gains the row; this tree updated in
  the same commit.

## Acceptance Checklist (leaf SOT-FORMAT.10)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHERE: `scripts/compare_readers.py` compared two
  readers while the format carried three contracts; the Lispish route's extraction semantics
  made the two CLASS families unavoidable, so the sweep carried a classification layer instead
  of the fix — measured, four classified atoms on the catalogue alone:

  ```
  $ python3 scripts/compare_readers.py 2>/dev/null | grep -c '^  class'
  4
  ```

- [x] **ADDRESSED (verified)** — leg 2. Reader C (`sexpr_file` over `SExprDocumentV1.spec`)
  joined the sweep additively; its normalisation uses ONLY sexp.py's own tables (`_ESCAPES`,
  `_atom`):

  ```
  $ python3 scripts/compare_readers.py --self-test
  compare_readers --self-test: 28 pass / 0 fail        (21 -> 28; 7 document-layer arms)
  $ python3 scripts/compare_readers.py
    agree   definitions/riscv/m.sexp             438 nodes identical [lispish]; 439 nodes, 1 form(s) [document]
    agree   definitions/riscv/rv64i.sem.sexp    1550 nodes identical [lispish]; 1551 nodes, 1 form(s) [document]
    agree   definitions/riscv/rv64i.sexp        1716 nodes identical [lispish]; 1717 nodes, 1 form(s) [document]
    agree   materials/catalog.sexp              1792 nodes identical [lispish]; 1793 nodes, 1 form(s) [document]
    agree   profiles/rv64i-lab-v0/encoding.sexp   18 nodes identical [lispish];   19 nodes, 1 form(s) [document]
    agree   schema/schema.sexp                     5 nodes identical [lispish];  158 nodes, 4 form(s) [document]
    compare_readers: 6 of 6 file(s) agree
  ```

  The document layer shows ZERO class notes — the four atoms the Lispish layer classifies
  (quoted-numeric, escape-retention) simply agree there, by construction; every form in every
  file is compared (43 forms in the catalogue, 4 in the new schema.sexp — the fixpoint file now
  verifies through the document grammar too); and the sweep grew to 6 files because schema.sexp
  itself joined the tracked corpus this session. The +1 node counts are the document layer
  counting the root form itself — cosmetic, consistent, and not a difference.

- [x] **NO REGRESSION** — leg 3. The Lispish layer is untouched — same four CLASS notes, same
  verdicts, and the surrounding guards unmoved:

  ```
  $ python3 scripts/compare_readers.py 2>/dev/null | grep -c '^  class'
  4
  $ python3 scripts/sexp.py --self-test | tail -1
  sexp --self-test: 18 pass / 0 fail
  ```

- [x] **LOCKSTEP** — `TOOLBOX.md`'s row updated to the three-reader sweep; this tree and
  `MEMORY.md` in the same commit.

## Acceptance Checklist (leaf SOT-FORMAT.3)

- [x] **REPRODUCE / ISSUE** — the split the tree exists to end, shown at the records:

  ```
  $ ls profiles/rv64i-lab-v0/*.jsonl
    requirements.jsonl  contract-obligations.jsonl          # 26 + 34 records, JSON Lines
  $ ls schema/ | grep -c 'requirements\|obligations'
    0                                                       # the schema layer declares nothing for them
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — tool-backed. WHY: the record grammar of `schema.sexp` could
  state structure but not the contracts' discriminating detail — id shapes, non-empty prose,
  at-least-one citations, uniqueness — so a straight conversion would have been strictly weaker
  than the JSON Schema it replaced, and `parameters` was worse: the JSON schema's own
  `additionalProperties: {type: [string, number, boolean, null]}` excluded the arrays three
  obligations write, and the tracked validator never descended into it, so the lie was unmeasured.
  WHERE: the gap sat between `schema/schema.sexp`'s `(field …)` kind and
  `schemas/{requirement,contract-obligation}.schema.json`'s pattern/minItems/uniqueItems/
  minLength/additionalProperties keywords.

  ```
  $ python3 - <<'PY'
  > import json
  > ob = json.loads(open("profiles/rv64i-lab-v0/contract-obligations.jsonl").readline())
  > print("legal_access_widths_bits" in ob["parameters"], type(ob["parameters"]["legal_access_widths_bits"]).__name__)
  False list        # hmm — first record is OB-XLEN; the arrays live in OB-ENV-ACCESS-WIDTHS
  $ grep -o 'legal_access_widths_bits[^]]*]' profiles/rv64i-lab-v0/contract-obligations.jsonl | head -1
  legal_access_widths_bits": [8, 16, 32, 64]     # an array, under a schema whose additionalProperties bans arrays
  ```

- [x] **FIX** — four optional field FACETS in the kernel (`(pattern …)`, `(min-length N)`,
  `(min N)`, `(unique yes)`), declared in `schema/schema.sexp` so the fixpoint keeps describing
  the whole language; two record schemas with JSON keys verbatim as field names and enums under
  `(values …)`; `parameters` as typed wrappers; the mapping owned solely by
  `scripts/records_sexp.py`; the migration and its proof in `scripts/convert_records.py`.

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  ```
  $ python3 scripts/convert_records.py verify profiles/rv64i-lab-v0/requirements.jsonl \
      profiles/rv64i-lab-v0/requirements.sexp
    round-trip ok: 26 requirements record(s), field-by-field equal and byte-identical on re-dump
  $ python3 scripts/convert_records.py verify .../contract-obligations.jsonl .../contract-obligations.sexp
    round-trip ok: 34 contract-obligations record(s), field-by-field equal and byte-identical
  $ python3 scripts/check_sexp_schema.py profiles/rv64i-lab-v0/requirements.sexp schema/requirements.sexp
    check_sexp_schema: ok — requirements.sexp conforms to requirements.sexp
  $ python3 scripts/check_sexp_schema.py profiles/rv64i-lab-v0/contract-obligations.sexp \
      schema/contract-obligations.sexp
    check_sexp_schema: ok — contract-obligations.sexp conforms to contract-obligations.sexp
  $ bash scripts/check_requirements.sh --self-test
    RECORD-SCHEMA --self-test: 22 pass / 0 fail        # the 15 old scenarios re-fired on the
                                                       # converted form + 4 facet arms + 1 standalone
  $ bash scripts/check_requirements.sh
    RECORD-SCHEMA: ok (5 record file(s) validate and agree with their profile)
  $ scripts/gate_report.py rv64i-lab-v0 && git diff --stat -- profiles/rv64i-lab-v0/G0-REPORT.md
    # diff: input names only; 26 requirements, 34 obligations, 68 checks, verdict unchanged
  ```

- [x] **NO REGRESSION** — `sexp --self-test` 18/0; kernel 43/0 (31 → 43; fixpoint green);
  `convert_records --self-test` 9/0; `check_semantics.py` 52 of 52 byte-identical verdict;
  `run_smoke.py` ok (4 guests, both models, reproduce); `compare_readers.py` **13 of 13 agree**
  (the two catalogues and two schemas joined the sweep; zero class notes); `check_citations.py`
  52 of 52; `materials.py --self-test` 20/0; profile dossier sizes 19,545 + 28,449 B — under the
  `profiles/` 32 KiB per-part ceiling, so no re-derivation was needed.

- [x] **LOCKSTEP** — `docs/ARCHITECTURE.md` §1.1/§1.3 current; `LIVE_STATUS.md` (catalogue rows,
  and the stale 33-obligation/66-check row re-derived to 34/68 — a drift found while migrating,
  fixed in passing); `profiles/rv64i-lab-v0/{DOSSIER,ENVIRONMENT,G0-REPORT}.md`; both doctrine
  mirrors' `RECORD-SCHEMA` rows; `TOOLBOX.md` (two rows); `MEMORY.md`; `DEV_NOTES.md` (dated
  entry; promotion declined in this leaf); `CHANGELOG.md`; `docs/TASK_TREE.md` — one commit.

## Acceptance Checklist (leaf SOT-FORMAT.4)

- [x] **REPRODUCE / ISSUE** — the split the tree exists to end, shown at the dossier:
  `ls profiles/rv64i-lab-v0/*.toml *.json` listed `profile.toml  references.toml  sources.toml
  state.json` beside the S-expression corpus; `grep -c '^#' references.toml` -> `65` — a fifth
  of that file was commentary `tomllib` discarded on every read.

- [x] **ROOT CAUSE (WHY + WHERE)** — tool-backed. WHY: a comment-rich human-authored document
  cannot lose its commentary, and a merge cannot read three formats. WHERE: `grep -lE 'tomllib|
  json\.loads' scripts/*.py scripts/*.sh` -> eight files: both record gates, `gate_report.py`,
  `run_smoke.py`, `compare_platforms.py`, both fetch scripts, `check_citations.py` — every one
  parsing a source of truth outside the format.

- [x] **FIX** — one reserved `comment` head in the kernel (annotations skipped, never declared);
  `scripts/dossier_sexp.py` the single mapping owner; `scripts/convert_dossier.py` the migration
  and its proof; six schema files; consumers changed at the seam (same dicts, new loader); the
  Sail override's JSON derived from the tracked `.sexp` on every run.

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:
  `convert_dossier.py verify` on all nine documents -> each `round-trip ok`, field-for-field
  equal, comment census exact, schema-conformant; `check_profile_consistency.sh --self-test`
  -> `39 pass / 0 fail` (rule 5b included); `run_smoke.py` -> `ok` and `compare_platforms.py`
  -> `4 of 4` — identical verdicts.

- [x] **NO REGRESSION** — kernel 50/0; dossier 11/0; converter 12/0; RECORD-SCHEMA 22/0;
  `sexp --self-test` 18/0; `check_semantics.py` and `check_citations.py` 52 of 52 each;
  `fetch_references.sh --verify-only` ok (incl. the 52 == 52 scope cross-check through
  `profile.sexp`); the regenerated G0 report diffs in input names only, every count byte-stable;
  `compare_readers.py` sweeps 28 of 28 files across all three readers.

- [x] **LOCKSTEP** — `docs/ARCHITECTURE.md` §1.1/§1.3; the profile's `DOSSIER.md` /
  `ENVIRONMENT.md` / `G0-REPORT.md`; both doctrine mirrors' `RECORD-SCHEMA` row; `TOOLBOX.md`
  (two rows); `doctrine/readme_routes.tsv` (`schema/` re-derived, grounds recorded);
  `MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md` (lesson promoted to
  `docs/knowledge/portable-shell-fixtures-keep-mutations-whole-line.md`), `docs/TASK_TREE.md`
  and this tree — one commit.


### Split two (`2026-09-27`, same commit as `.6`)

The `.5` checklist joined the archive when the `.6` work pushed the live tree
over the per-part ceiling again — same rule, obeyed twice in a day.

## Acceptance Checklist (leaf SOT-FORMAT.5)

- [x] **REPRODUCE / ISSUE** — the split the tree exists to end, shown at the composition
  boundary: §1.2 of `docs/ARCHITECTURE.md` promised "merging records and obligations across a
  composition boundary … lands with `SOT-FORMAT.5`", and nothing in the repository could do it.
  Census before this leaf:

  ```
  $ git ls-files scripts | grep -E 'merge|compose' | grep -v encoding_disjoint
  (no output)                                        # union of records: no rule, no tool
  $ grep -n 'by_id = ' scripts/check_requirements.sh
  by_id = {r.get("id"): r for r in recs}             # and, measured below, silently collapsing
  ```

  ⭐ Two defects surfaced while designing the fix, probe-backed (TOOLS-FIRST, both before any
  code was written):
  1. **RECORD-SCHEMA never refused duplicate record ids.** Two records sharing an id collapsed
     in the `by_id` map (last wins), so a catalogue could contradict itself and stay green:

     ```
     $ # scratch catalogue, two REQ-D-A records differing in 'risk', gate body extracted verbatim
     $ python3 target/doctrine_scratch/dupprobe/gate_body.py target/doctrine_scratch/dupprobe
     __CHECKED__ 1                                    # rc=0 — nothing refused the contradiction
     ```

  2. **Obligation `dependencies` were never checked at all** (the gate checks requirements'
     only), and the corpus's environment-assumptions depend on *obligations*
     (`OB-ENV-RESET` → `OB-ENTRY-STATE`), not on requirements — a namespace fact that had to be
     measured, not assumed:

     ```
     $ # the merge's first closure run on the real profile (obligation deps looked up wrong)
     DANGLING DEP obligation 'OB-ENV-RESET' depends on 'OB-ENTRY-STATE', which no unit provides
     # yet OB-ENTRY-STATE IS an obligation record — 34 of 34 exist; the corpus is mixed-kind:
     # cpu-guarantees depend on requirements, environment-assumptions on guarantees
     ```

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHY: a merge is only definable over one format,
  and even with one format it is only *checkable* if ids are unique within each side and
  references resolve across the union. WHERE: measured, not read —

  ```
  $ grep -n 'by_id = ' scripts/check_requirements.sh          # the gate's id → record map
  by_id = {r.get("id"): r for r in recs}     # last wins: a duplicate id silently collapses
  $ python3 target/doctrine_scratch/dupprobe/gate_body.py target/doctrine_scratch/dupprobe
  __CHECKED__ 1                              # rc=0 — a self-contradicting catalogue stays green
  ```

  The gap sat between `scripts/records_sexp.py` (the mapping, which has no opinion about
  duplicates) and that map; and between the gate's rule 5 (requirements-only dependency check)
  and the obligation records' `dependencies`, which no rule owned.

- [x] **FIX** — `scripts/merge_records.py`: the merge rule as data (key = id, content equality
  on collision, `profile_ids` union, sources full-pin equality, closure over the union,
  direction census for `.3`); RECORD-SCHEMA rule 8 (UNIQUE-ID) as the one owner of catalogue
  discipline, with a fired RED arm. The merge reads only through the mapping owners and parses
  nothing itself.

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  ```
  $ python3 scripts/merge_records.py --self-test
  merge_records --self-test: 18 pass / 0 fail        # 10 GREEN unions, 8 RED contradictions
  $ python3 scripts/merge_records.py profiles/rv64i-lab-v0 profiles/rv64i-lab-v0
  composed: 26 requirement(s), 34 obligation(s) (26 cpu-guarantee, 8 environment-assumption),
            3 source(s) from 2 unit(s)              # the units COMPOSE — idempotent self-merge
  $ # genuine contradiction, fired RED on real data (one statement edited in a copied unit):
  CONFLICT requirement 'REQ-D-XLEN' between units 'profiles/rv64i-lab-v0' and
  'target/doctrine_scratch/sf5/edited': field 'statement' differs — 'profiles/rv64i-lab-v0':
  'XLEN = 64. …' vs 'target/doctrine_scratch/sf5/edited': 'XLEN = 32, edited …'   rc=1
  $ # the composition-boundary case — an extension unit needing the base's REQ-D-XLEN:
  $ python3 scripts/merge_records.py profiles/rv64i-lab-v0 target/doctrine_scratch/sf5/ext
  composed: 27 requirement(s), 35 obligation(s) (27 cpu-guarantee, 8 environment-assumption),
            4 source(s) from 2 unit(s)              # the units COMPOSE
  $ python3 scripts/merge_records.py target/doctrine_scratch/sf5/ext        # base withheld:
  DANGLING DEP requirement 'REQ-EXT-DEMO' … depends on 'REQ-D-XLEN', which no unit provides
  ```

  And the RECORD-SCHEMA fix, before → after on the same probe:

  ```
  $ python3 target/doctrine_scratch/dupprobe/gate_body.py target/doctrine_scratch/dupprobe
  DUPLICATE ID p/requirements.sexp: record 'REQ-D-A' appears more than once — …   rc=1
  $ bash scripts/check_requirements.sh --self-test
  RECORD-SCHEMA --self-test: 23 pass / 0 fail        # was 22; +1 DUPLICATE-ID arm
  ```

- [x] **NO REGRESSION** — sexp 18/0; kernel 50/0; merge 18/0; RECORD-SCHEMA 23/0 and its real
  run green (`5 record file(s) validate and agree with their profile` — the real catalogues
  carry no duplicate ids, so rule 8 bites nothing that exists); `check_semantics.py` 52 of 52;
  `check_citations.py` 52 of 52; `materials.py --self-test` 20/0; `run_smoke.py` ok;
  `compare_readers.py` 28 of 28 agree; the regenerated G0 report diffs in nothing;
  `make check` green. Whole gate green after staging.

- `promotion: recorded (the duplicate-id lesson is general — an id-keyed lookup that silently
  collapses duplicates turns a self-contradicting catalogue green; the gate now carries the
  rule, the lesson card is docs/knowledge/a-duplicate-id-is-a-contradiction-not-a-shadowing.md).
  The mixed-namespace dependency fact is declined here — it is measured, owned and enforced by
  merge_records.py's closure, where anyone extending the record families will meet it.`

- [x] **LOCKSTEP** — `docs/ARCHITECTURE.md` §1.2 (the merge is no longer "lands with
  `SOT-FORMAT.5`" — it is checked today, the tool named); `TOOLBOX.md` gains the instrument;
  `MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md`, `LIVE_STATUS.md` (177 arms re-derived),
  `docs/TASK_TREE.md` and this tree — one commit. Maintenance the growth fired, same commit:
  this tree's done-leaf checklists split to `docs/tasks/archive/SOT-FORMAT.md` (per-part
  ceiling obeyed, not raised — the P0-PROFILE precedent) and `CHANGELOG.md`'s oldest entry
  sharded to `docs/changelog/shard-0003.md` (SHARD-FREEZE verified: 5 rows, exact partition).

