# MODEL-BOOKS — archived completed-leaf evidence

The full, unedited acceptance checklists for the `done` leaves `.1`–`.5` of the
[`MODEL-BOOKS`](../MODEL-BOOKS.md) tree (the closing leaf's, `.6`, stays live per the
`P1-LAB`/`P2-SCALAR` precedent), split out on `2026-09-29` when the live file crossed its
per-part ceiling — the ceiling was obeyed, not raised, per the `docs/tasks/` precedent set
by `SOT-FORMAT` and continued by `P1-LAB` and `P2-SCALAR`. The live tree keeps the
frontier, the decisions, the open questions, the blockers, every leaf's
goal/acceptance/result, the closing leaf's checklist, and both logs.

## Acceptance Checklist (leaf `MODEL-BOOKS.1`)

- [x] **REPRODUCE / ISSUE** — the gap the tree was created against: a materials list that
  lives only in the dossier is a list a reviewer will not read. Measured at landing:
  no `docs/models/` existed, and the unit registry's `book` field named a page that was
  never created:

  ```
  $ git ls-files docs/models | wc -l          # before this leaf
  0
  $ ls docs/book/src/profiles/                # the units.sexp book target
  ls: docs/book/src/profiles/: No such file or directory
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — WHY: the per-unit book had no structure (the leaf
  that owns it was unstarted) and the registry's `book` pointer was aspirational prose.
  WHERE: `materials/units.sexp`'s `book` field, and the absent `docs/models/` family.
  The pre-registration RED proved the gate reads the real corpus: fired before the data
  was repaired, it named exactly the stale registry row:

  ```
  $ bash scripts/check_materials_bill.sh        # before the units.sexp repair
  MATERIALS-BILL: a unit's materials bill does not hold.
    NO BOOK rv64i-lab-v0: docs/book/src/profiles/rv64i-lab-v0.md lacks book.toml/src/SUMMARY.md …
  ```

- [x] **FIX** — `docs/models/rv64i-lab-v0/` (the mdBook: skeleton, introduction with the
  five-part shape contract, the materials bill with 15 per-material sections, each with
  its does-not-supply statement); `scripts/gen_model_book.py` (the generator: four
  fragments from the pinned dossier, OWN-03 manifests, `--check` drift mode, refusals by
  name); `scripts/check_materials_bill.sh` (MATERIALS-BILL, doctrine #26 — DRIFT +
  COMPLETENESS, self-test 7/0, fired RED before registration); the registry repairs
  (`units.sexp`'s `book` corrected; `fact_ownership.tsv` +4 mirror rows;
  `readme_routes.tsv` +1 family row, `docs/models/` measured 8 files / 27,600 B); the
  stale `sources.toml`/`references.toml` in the leaf's Goal corrected to the `.sexp`
  reality with the note recorded in the design.

- [x] **ADDRESSED (verified)** —

  ```
  $ python3 scripts/gen_model_book.py
  gen_model_book: wrote 4 fragments under docs/models/rv64i-lab-v0/src/materials
  $ mdbook build docs/models/rv64i-lab-v0
  INFO HTML book written to `docs/models/rv64i-lab-v0/book`
  $ bash scripts/check_materials_bill.sh [--self-test]
  rv64i-lab-v0: 15 materials, every fragment matches the pinned data, every section
  carries its does-not-supply
  MATERIALS-BILL: ok (1 unit(s) — …)
  MATERIALS-BILL --self-test: 7 pass / 0 fail
  ```

- [x] **NO REGRESSION** — the guard set re-run, green; the two mirror caps re-based last
  leaf held (TOOLBOX.md 17,278 / 20,480; DOCTRINE_ENFORCEMENT.md 25,909 / 28,672); no
  Rust changed:

  ```
  $ make gate
  === all doctrines green ===          (26 project doctrines; DERIVED-COUNTS re-derives
                                        26 and 280 arms; README-ROUTING-CLOSURE: 32 destinations)
  $ make book
  INFO HTML book written to `docs/book/book`     (the project book still renders)
  ```

- [x] **LOCKSTEP** — same commit: `MEMORY.md` (overwritten; 3/8), `LIVE_STATUS.md`
  (MODEL-BOOKS 3/8; 26 doctrines / 280 arms; 32 destinations), `CHANGELOG.md`,
  `DEV_NOTES.md`, `docs/TASK_TREE.md` (frontier `.2`), this tree, the three doctrine
  mirrors, `doctrine/readme_routes.tsv`, `doctrine/fact_ownership.tsv`,
  `materials/units.sexp`.

## Acceptance Checklist (leaf `MODEL-BOOKS.2`)

- [x] **REPRODUCE / ISSUE** — the open question the tree carried: does the official
  specification's PDF rendering carry the instruction-format tables as selectable text?
  If yes, encodings can be re-sourced from the primary document and the encoding
  provenance's shared-ancestry exposure shrinks. Until measured, the materials bill could
  only name it as an open investigation.

- [x] **ROOT CAUSE (WHY + WHERE)** — WHY the question was open: the pinned artifacts are
  the HTML renderings, whose format diagrams are images — the encoding content was never
  in the pinned bytes, so nobody had read the PDF's text layer. WHERE the investigation
  had to start: which PDF. The pinned publication (docs.riscv.org, `v20260120`) publishes
  its PDF at the same version segment, linked from the pinned page itself:

  ```
  $ curl -s https://docs.riscv.org/reference/isa/v20260120/unpriv/rv64.html | grep -ioE 'href="[^"]*\.pdf[^"]*"'
  href="../_attachments/riscv-unprivileged.pdf"
  ```

- [x] **FIX** — the chapter `docs/models/rv64i-lab-v0/src/gaps.md` (in the book's
  SUMMARY.md; the bill's open-question sentence in `materials.md` now points at the
  answered finding); the investigation run and recorded with its commands (below). The
  PDF is cached untracked at `target/materials/` (on-volume, gitignored — the
  `target/sources/`/`target/refs/` standing) and deliberately NOT catalogued
  (`catalog.sexp`'s corpus model has no network-origin kind — a MODEL-METHOD decision,
  recorded in the chapter).

- [x] **ADDRESSED (verified)** — fetched and examined with a tool; the answer is YES:

  ```
  $ curl -sS -o target/materials/riscv-unprivileged-v20260120.pdf -w '%{http_code} %{size_download}\n' \
      https://docs.riscv.org/reference/isa/v20260120/_attachments/riscv-unprivileged.pdf
  200 4580174
  $ shasum -a 256 target/materials/riscv-unprivileged-v20260120.pdf
  06bb3c23074f72060a0ec061a80933af948cae7ceafdcd9d1fe177b05fd150bc
  $ file target/materials/riscv-unprivileged-v20260120.pdf
  PDF document, version 1.4, 696 pages
  $ grep -m1 'Official Release' target/materials/riscv-unprivileged-v20260120.txt
  Version 20260120: Official Release
  $ grep -cE '[01]{7}' target/sources/riscv-v20260120/{intro,rv32,rv64}.{html,txt}   # the pinned renderings
  …:0  (all six)
  $ pdftotext target/materials/riscv-unprivileged-v20260120.pdf target/materials/riscv-unprivileged-v20260120.txt
  $ grep -cE '[01]{7}' target/materials/riscv-unprivileged-v20260120.txt              # its PDF rendering
  232
  $ grep -cE '[01]{7}' <(pdftotext .materials/riscv/riscv-isa-manual-20260911.pdf -)  # corroboration
  269
  ```

- [x] **NO REGRESSION** — no gate surface changed (the chapter is authored prose; no
  generated content, so MATERIALS-BILL was not extended and the doctrine count stays 26):

  ```
  $ bash scripts/check_materials_bill.sh [--self-test]
  MATERIALS-BILL: ok (1 unit(s) — …) ; self-test 7 pass / 0 fail
  $ mdbook build docs/models/rv64i-lab-v0 && make book    # both render
  $ make gate
  === all doctrines green ===
  ```

- [x] **LOCKSTEP** — same commit: `MEMORY.md` (overwritten; 4/8), `LIVE_STATUS.md`
  (MODEL-BOOKS 4/8), `CHANGELOG.md`, `DEV_NOTES.md`, `docs/TASK_TREE.md` (frontier `.3`),
  this tree (the open question marked answered).

## Acceptance Checklist (leaf `MODEL-BOOKS.3`)

- [x] **REPRODUCE / ISSUE** — the tree's own gap statement: a methodology that lives only
  in the task-tree leaves is a methodology nobody can follow end to end. The chapter had
  to follow ONE rule from its sentence to its check with every hop inspectable.

- [x] **ROOT CAUSE (WHY + WHERE)** — the rule chosen is the reserved-FENCE rule: its
  chain is complete in tracked files (the sentence is in the pinned artifact; the
  decision, requirement, obligation, guest and suites are all tracked), and it carries
  DEFECT-A — the instructive correction. Every hop was verified to resolve BEFORE the
  chapter was written:

  ```
  $ grep -c '(id "D-FENCE")' profiles/rv64i-lab-v0/profile.sexp                      -> 1
  $ grep -c '"REQ-D-FENCE"' profiles/rv64i-lab-v0/requirements.sexp                  -> 1
  $ grep -c '"OB-FENCE"' profiles/rv64i-lab-v0/contract-obligations.sexp             -> 2
  $ grep -o 'CHK-FENCE-POS\|CHK-FENCE-NEG' …/contract-obligations.sexp               -> both
  $ ls …/guests/fault-fence.s …/guests/fault-fence.expected.sexp                     -> both exist
  $ grep -c fault_fence_retires_every_reserved_configuration_as_a_fence \
      crates/semulith-verify/src/run/tests.rs                                        -> 1
  $ grep -c '"fault-fence"' scripts/run_semulith_smoke.py                            -> 1
  $ grep -c 'never_written "x5"' …/fault-jal-mis.expected.sexp …/fault-jalr-mis…     -> 1, 1
  $ python3 scripts/check_citations.py   ->  52 of 52 instruction citations resolve
  ```

- [x] **FIX** — `docs/models/rv64i-lab-v0/src/methodology.md` (in the book's SUMMARY.md):
  the pipeline as six gated hops; the FENCE walk with real ids; the two judgement calls
  (semantic class, authority — each with its mechanical edge named); the mistakes
  (DEFECT-A, DEFECT-B, the two authoring REDs); the build-it-yourself checklist. The
  quoted decision fragments were checked programmatically as verbatim substrings of
  `D-FENCE`'s statement, and the chapter's census claim (28 requirements, four classes)
  was derived, not remembered.

- [x] **ADDRESSED (verified)** — both books render; the gates stay green:

  ```
  $ mdbook build docs/models/rv64i-lab-v0
  INFO HTML book written to `docs/models/rv64i-lab-v0/book`
  $ make book          # the project book renders
  $ bash scripts/check_materials_bill.sh [--self-test]   # ok; self-test 7/0
  $ make gate
  === all doctrines green ===          (26 — the gate surface unchanged)
  ```

- [x] **NO REGRESSION** — no generated content landed, so MATERIALS-BILL's surface is
  unchanged and no gate was extended; measured on the committed tree:

  ```
  $ git status --short -- scripts/ crates/ | wc -l     # no instrument or crate touched
  0
  $ bash scripts/check_materials_bill.sh
  MATERIALS-BILL: ok (1 unit(s) — generated tables match the pinned data; …)
  ```

  The only surfaces touched are the new chapter, the book's SUMMARY, the bill's one
  answered-question sentence, and the lockstep docs.

- [x] **LOCKSTEP** — same commit: `MEMORY.md` (overwritten; 5/8), `LIVE_STATUS.md`
  (MODEL-BOOKS 5/8), `CHANGELOG.md`, `DEV_NOTES.md`, `docs/TASK_TREE.md` (frontier `.4`),
  this tree.

## Acceptance Checklist (leaf `MODEL-BOOKS.4`)

- [x] **REPRODUCE / ISSUE** — the leaf's own question: how were the references obtained,
  how were they configured to match the profile, and what is an AGREE worth? The bill
  (`.1`) lists the references as materials; nothing told the configuration story or the
  independence argument as prose a reviewer can follow.

- [x] **ROOT CAUSE (WHY + WHERE)** — WHY the chapter must be control-led: a configuration
  *listing* is a claim; a configuration whose knob was flipped back is a measurement. The
  controls exist and are recorded — WHERE: `references.sexp` (the experiment records'
  `control` fields, the eight DIFF records, the six independence records), the P0-PROFILE
  archive (the controls' outputs), and the override itself:

  ```
  $ python3 - <<'…'   # the dossier's census of what the chapter names
  candidates: sail-riscv 0.14 | spike 1.1.1-dev (commit 1e05ddac) | qemu 11.1.1 | act4 reachable, not acquired
  experiments: ['smoke-arith', 'smoke-trap'] | differences: 8 | independence: 6
  $ grep -c "handled invisibly" docs/tasks/archive/P0-PROFILE.md        -> 2
  $ grep -c "FIRST DIVERGENCE at aligned step 2" profiles/rv64i-lab-v0/references.sexp  -> 1
  $ grep -c "cross_model false" profiles/rv64i-lab-v0/guests/guest-no-device.expected.sexp  -> 1
  $ grep -c 'expect_divergence (difference "DIFF-FENCEI-EXECUTED") (at_step 1)' \
      profiles/rv64i-lab-v0/guests/it-fencei.expected.sexp              -> 1
  $ grep -c 'm-call\|trap_machine_ecall\|software-breakpoint\|trap_breakpoint\|misaligned-store/amo' \
      scripts/compare_traces.py                                       -> 5
  $ grep -c "59 files\|184 of the 199" profiles/rv64i-lab-v0/references.sexp  -> 1
  ```

- [x] **FIX** — `docs/models/rv64i-lab-v0/src/references.md` (in the book's SUMMARY.md):
  the cast honestly labelled (including QEMU never-exercised and ACT4 never-a-second-opinion);
  the acquisition discipline (the fetcher fired RED on a corrupted digest); the three
  controls with their recorded outputs; the four harness DIFFs; the two measured
  reference-vs-reference differences; the independence inventory per subsystem and pair,
  ending in the per-leg verdict; the build-it-yourself checklist.

- [x] **ADDRESSED (verified)** — every id, version and count named was verified against
  the dossier and the trees as written (the ROOT CAUSE box's sweep); both books render;
  the gates stay green:

  ```
  $ mdbook build docs/models/rv64i-lab-v0
  INFO HTML book written to `docs/models/rv64i-lab-v0/book`
  $ make book          # the project book renders
  $ bash scripts/check_materials_bill.sh [--self-test]   # ok; self-test 7/0
  $ make gate
  === all doctrines green ===          (26 — the gate surface unchanged)
  ```

- [x] **NO REGRESSION** — no generated content, no gate extension; measured on the
  committed tree:

  ```
  $ git status --short -- scripts/ crates/ | wc -l     # no instrument or crate touched
  0
  $ bash scripts/check_materials_bill.sh
  MATERIALS-BILL: ok (1 unit(s) — generated tables match the pinned data; …)
  ```

- [x] **LOCKSTEP** — same commit: `MEMORY.md` (overwritten; 6/8), `LIVE_STATUS.md`
  (MODEL-BOOKS 6/8), `CHANGELOG.md`, `DEV_NOTES.md`, `docs/TASK_TREE.md` (frontier `.5`),
  this tree.

## Acceptance Checklist (leaf `MODEL-BOOKS.5`)

- [x] **REPRODUCE / ISSUE** — the arc's last content part: what has been demonstrated
  existed only as numbers scattered across the trees and the two gate reports; the
  verdicts (`incomplete`, twice) were nowhere explained to a reader of the model, and no
  reviewer-repeatable walk connected a rule to a command.

- [x] **ROOT CAUSE (WHY + WHERE)** — WHY: the evidence is real but was readable only by
  someone who already knew where it lived; WHERE: the numbers live in the regenerated
  reports and the gates' own outputs. Confirmed current before writing — both reports
  regenerate byte-identical (no drift), and the headline numbers are the live ones:

  ```
  $ python3 scripts/gate_report.py rv64i-lab-v0 --gate G0   # + --gate G1
  wrote …/G0-REPORT.md …   wrote …/G1-REPORT.md …   (git status: clean — byte-identical)
  $ bash scripts/check_exercise_coverage.sh
  EXERCISE-COVERAGE: ok (1 profile(s) — every declared form exercised, 52/52)
  $ bash scripts/check_interaction_matrix.sh | tail -1
  INTERACTION-MATRIX: ok (1 unit(s) — every derived cell declared, …, no orphan guests)
  $ grep 'aligned steps' profiles/rv64i-lab-v0/G1-REPORT.md   -> 492/492 aligned steps
  ```

- [x] **FIX** — `docs/models/rv64i-lab-v0/src/evidence.md` (in the book's SUMMARY.md):
  the per-axis evidence ledger (every number with its instrument and re-derivation
  command), the two `incomplete` verdicts with their reasons (G0: 72 declared / 0
  implemented; G1: criterion 6 unmet, owner `P2-SCALAR.5`, and that leaf's two blockers
  named), the capability limits stated plainly, and the evidence-side traceability walk
  for `D-MISALIGN-DATA` ending at re-runnable commands. The walk's ids were verified
  before writing:

  ```
  $ python3 - <<'…'   # records_sexp over the two catalogues
  REQ-D-MISALIGN-DATA | resolved | implementation-defined | obs: ['OB-MISALIGN-DATA']
  OB-MISALIGN-DATA | cpu-guarantee | implementation-profile | [CHK-MISALIGN-DATA-POS,
  CHK-MISALIGN-DATA-NEG] | parameters: requirement_id REQ-D-MISALIGN-DATA …
  ```

- [x] **ADDRESSED (verified)** — the walk's terminal commands, run fresh, quoted verbatim
  in the chapter:

  ```
  $ cargo test -p semulith-verify --lib run::tests::smoke_trap
  test run::tests::smoke_trap_reports_the_misaligned_load_and_stops ... ok
  test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 165 filtered out
  $ python3 scripts/run_semulith_smoke.py
    PASS  smoke-trap: semulith vs 3 specification-derived expectations
    PASS  smoke-trap: semulith vs sail-riscv  AGREE over 3 aligned step(s) (…)
    PASS  smoke-trap: semulith vs spike  AGREE over 3 aligned step(s) (…)
    PASS  smoke-trap: semulith reproduces  sha256 c9d7a11ce4b7bffe…
  run_semulith_smoke: ok — …
  ```

- [x] **NO REGRESSION** — no generated content, no gate extension; measured:

  ```
  $ git status --short -- scripts/ crates/ | wc -l     # no instrument or crate touched
  0
  $ bash scripts/check_materials_bill.sh [--self-test]
  MATERIALS-BILL: ok (1 unit(s) — …) ; self-test 7 pass / 0 fail
  $ mdbook build docs/models/rv64i-lab-v0 && make book    # both render
  $ make gate
  === all doctrines green ===
  ```

- [x] **LOCKSTEP** — same commit: `MEMORY.md` (overwritten; 7/8), `LIVE_STATUS.md`
  (MODEL-BOOKS 7/8), `CHANGELOG.md`, `DEV_NOTES.md`, `docs/TASK_TREE.md` (frontier `.6`),
  this tree.

