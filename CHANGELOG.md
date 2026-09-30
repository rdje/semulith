# CHANGELOG.md

## SEMULITH-PS-0065 (leaf P2-SCALAR.5) — the compiled guest, written into the model book

- New model-book chapter `compiled-guest.md` (between references and evidence): what a
  guest is and the shared-mind weakness of hand-written assembly; the self-checking
  design and why per-step expectations stay with the assembly corpus; the measured
  toolchain; all three in-flight defects as the teaching record (the C-UB shift, the
  visible-change vocabulary, GATE-REPORT's verdict-assuming arm); what it proved and
  what it did not. Linked from the evidence chapter. Book builds; gate green.

## SEMULITH-PS-0063 (leaf P2-SCALAR.5, strand 1) — the compiled C guest retires three-way; G1 reads `passed`

- `guests/c-scope.c` is the first COMPILED guest: a self-checking freestanding C tour of
  the declared scope (64/32-bit ALU, every load/store width, branches and a counted loop,
  real calls through the argument registers and an indirect jump, variable shifts),
  compiled by the pinned toolchain (`scripts/build_c_guest.sh` — clang 21.1.8 with the
  RISC-V backend plus `ld.lld` 21.1.8, both probed, refused by name if absent, nothing
  installed) and retiring under first-divergence comparison against sail-riscv AND spike:
  **129/129 aligned steps, byte-identical reproduction**.
- Two in-flight REDs, both authoring-side, never a model defect: the guest's own
  self-check caught `w32 << 33` (UB in C — clang deleted the rest of the program; proven
  by bisect, the `-fno-strict-aliasing` control innocent), and the three-way comparison
  surfaced a comparator gap the hand-written corpus never exercised — the references log
  no-change writes (`li a0, 0`), semulith's declared visible-change vocabulary does not.
  The comparator now reduces every trace to the declared vocabulary (`_visible_changes`
  in `align`, +2 self-test arms, 19/0).
- `gate_report.py`'s criterion 6 gained its met branch — **G1's verdict is `passed`**, the
  same instrument that said `incomplete` while the C path was missing. The report names
  the guest, the build script and the decision record; the toolchain versions keep their
  ONE owner (the decision record + the script's refusals).
- Lockstep: the smoke's `.c` path (build → budget run → `e_entry` from the ELF header),
  LIVE_STATUS (P1 `passed`), MEMORY, both books, P1-LAB's metadata, the model book.
  `make gate` all green; the full smoke 221 PASS / 0 FAIL.

## SEMULITH-PS-0062 (leaf P2-SCALAR.5) — the routing answered, the toolchain measured: .5 unblocked, design before code

- Director delegation `2026-09-30`: the C-guest routing and toolchain call is the
  engineer's. Recorded in `decision_c-guest-routing-and-toolchain`: the C guest lands in
  `P2-SCALAR.5` (the G0 precedent — the tree completes, the gate keeps criterion 6
  visible every commit, `EVD-08` forbids `passed` over a missing check); `P1-LAB` stays
  `done`.
- The toolchain was measured, not installed: Apple clang has no RISC-V backend (exact
  error recorded); Homebrew `llvm@21` clang 21.1.8 compiles RV64I correctly
  (objdump-verified); zig 0.16.0's bundled `ld.lld` 21.1.8 links.
- `.5` blocked → active; the three-strand design recorded before code (strand 1: the C
  guest; strand 2: the ACT4 generated suite; strand 3: directed sequences). Docs-only
  commit; `make gate` green.

## SEMULITH-PX-0001 (leaf PREFIX-DISCIPLINE.1) — the SEMULITH- prefix, pinned at the boundary and watched

- The director ruled the work-unit prefix is SEMULITH, never SEMILITH. Measured drift at
  ruling time: 123 commits carry both spellings across 10+ areas; exactly one subject
  ("Initial commit") carries neither. History is immutable, so enforcement is
  forward-looking: the `commit-msg` hook now refuses any leading work-unit id not beginning
  with `SEMULITH-`, with `SEMULITH` named in the refusal.
- `COMMIT-PREFIX` (#29, `scripts/check_commit_prefix.sh`) probes the hook BEHAVIOURALLY on
  every commit — the pin lives in a neutral scaffold file a sync can revert, and carrying it
  upstream is unavailable by policy, so a silent revert turns the next commit RED, named.
  Fired RED against the real tree before the pin existed; self-test 4/0.
- The ruling is recorded: `decision_work-unit-prefix-semulith.md` + INDEX; COMMIT.md states
  the pinned prefix; both registry mirrors carry the row; LIVE_STATUS re-derived
  (29 doctrines / 301 arms). The tree closes 1/1.
- `make gate` all green. DEV_NOTES.md crossed its 48 KiB ceiling with this slice's note and
  was sharded (the DOC-SHARDING machinery, completeness exact).

## SEMULITH-MM-0059 (leaf MODEL-METHOD.17) — the channel answers: the poller fix measured, the heard gaps reconciled

- chipdoc fixed the poller deafness `.16` surfaced (corpus `6bfabf2`): the poller descends
  into the `(materials …)` wrapper and READS this catalogue's nested gaps. Measured here,
  not accepted: `semulith_gaps_open: 2` pre-reconcile — the signal `.16` could not get.
- The two heard records were already dispositioned here: `GAP-INTEL-SDM-VOL1` (closed by
  `.13`'s catalogued material) and `GAP-RISCV-JAN-2026-PDF` (closed by `.12`'s recorded
  decline decision). Both now carry `(status resolved)` with evidence; post-reconcile the
  poller reports 0 open, 0 unmirrored.
- The v20260120 gap's deafness claim updated to the fixed channel; corpus re-pinned
  `f33d330` → `92a73b6` (5313 files / 257 PDFs re-derived by the same path sweep, unchanged);
  the channel snapshot refreshed (feed 68/14; REQ-008 at `2026-09-29`).
- The channel is now TWO-WAY: a new gap filed in `materials/catalog.sexp` surfaces to
  chipdoc without an operator relay.
- `make gate` all green. CHANGELOG.md crossed its 64 KiB ceiling with this entry and was
  sharded (the DOC-SHARDING machinery, completeness exact).

## SEMULITH-MM-0058 (leaf MODEL-METHOD.16) — the v20260120 PDFs: gap filed, answered same-day, adopted through the corpus seam

- The director asked for the v20260120 unprivileged PDF twice. Corpus sweep: absent (only
  the 20260911 intermediate). The verified bytes survived in scratch from `MODEL-BOOKS.2` —
  then chipdoc relayed that it now mirrors BOTH v20260120 PDFs
  (`risc-v/isa/reference/docs.riscv.org-v20260120/`, REQ-008), same bytes
  `06bb3c23…d150bc`, with a correction: the PDF does not share the pin's numbering.
- All four legs verified before any record changed: mirror present; byte-equality with the
  independent docs.riscv.org fetch (two acquisitions, one set of bytes); REQ-008 read in the
  ledger; the numbering re-measured from the extracted text layer — RV32I Chapter 2 / RV64I
  Chapter 4, NOT the pinned HTML's §1.1/§3.1. chipdoc's correction is correct.
- Both PDFs catalogued reference-only (`RVI-UNPRIV-PDF-V20260120` 696 pp,
  `RVI-PRIV-PDF-V20260120` 214 pp) with the trap documented, and fetched through the corpus
  seam, digests verified. The gap record was filed and resolved the same day; the corpus
  re-pinned `73711d6` → `f33d330` (5313 files / 257 PDFs); 45 materials. The `.14` probe
  input is now a first-class material, with three renderings and three numberings measured.
- Measured and surfaced for a chipdoc-side fix: its poller reads only TOP-LEVEL `(gap …)`
  forms, so it sees 0 of this catalogue's nested gaps (`semulith_gaps_open: 0` against the
  real catalogue; a scratch probe shows a flat gap is seen, a nested one is not). This
  request travelled operator-relayed.
- The tasks per-part ceiling fired twice mid-leaf (67,737 B, then 65,032 B growing) and was
  answered by the second and third archive movements — the ceiling obeyed, never raised.
- `make gate` all green. CHANGELOG.md crossed its ceiling with this entry and was sharded
  again by the DOC-SHARDING machinery.

## SEMULITH-MM-0057 (leaf MODEL-METHOD.15) — the chipdoc feed arrives: the flagged set, catalogued and cached

- The director supplied the chipdoc corpus root and ordered a local cache so the path never
  has to be requested again. The feed's records arrive in this catalogue's own syntax, so
  adoption is copy-and-verify, not transcription: 7 proposals adopted (the `2026-09-27`
  flagged set minus the already-catalogued psABI) — `RISCV-ARCH-TEST-ACT4`, `RISCV-SBI-2.0`,
  `RISCV-BRS-1.0`, `DT-SPEC-0.4`, `UBOOT-2026.07`, `SIFIVE-FU540-C000`, `VIRTIO-1.2`. The
  catalogue reads 43 materials (was 36).
- Every digest verified AT FETCH, not trusted from the feed: 7/7 ok; both snapshots
  manifest-verified (ACT4 136/136 files, U-Boot 1219/1219). `materials.py --verify`:
  43/43 resolved, zero drift after the corpus re-pin `3c45e81` → `73711d6` (5309 files /
  255 PDFs re-derived by the same path sweep at the new pin).
- The channel itself is snapshotted git-ignored at `.semulith-data/chipdoc/` (the map, the
  feed, the requests ledger); the corpus path lives only in that untracked README —
  Policy 12: no tracked file names it.
- `P2-SCALAR.5` blocker (a) ANSWERED at the materials layer: the ACT4 docs + test plans are
  catalogued and cached; the generated 635 MB suite stays pinned by upstream commit
  `e2216915…` for resume day (the snapshot is partial by design). Blocker (b) — the C-guest
  routing decision plus the absent RISC-V C toolchain — stands.
- Measured absence: chipdoc's pinned v20260120 snapshot carries 72 HTML pages and no PDF —
  the `MODEL-METHOD.14` probe's PDF stays the `MODEL-METHOD.4` release-asset acquisition.
- `make gate` all green. CHANGELOG.md crossed its 64 KiB ceiling with this entry and was
  sharded by the DOC-SHARDING machinery, per its declared pressure control.

## SEMULITH-PD-0051 (leaf PUSH-DISCIPLINE.3) — the approval record; PUSH-DISCIPLINE closes (3/3)

- An exceptional push is now an auditable ACT: `scripts/approved_push.sh '<the director's
  reason>'` runs `make ci` green FIRST (a red suite refuses and writes nothing), appends
  the entry to the tracked append-only ledger `docs/push-approvals.md` and commits it as
  its OWN commit (`SEMULITH-PUSH-NNNN: push approved — <reason>` — the only way the record
  travels in the pushed history), then pushes with the approval variable set — and the
  pre-push boundary re-verifies all three: cadence, suite, record.
- The ledger entry carries: the sequential id, the act's timestamp, the director as
  approver, the reason verbatim, the derived range (`<upstream>..<work-head>`, N commits —
  never typed), and the suite line. Cadence pushes leave no entry.
- `PUSH-RECORD` (#28, `scripts/check_push_record.sh`) enforces it: a staged change must
  keep HEAD's content a PREFIX of the new content (history is never rewritten), and every
  entry carries who/when/why/range with sequential ids — self-test 6/0; fired RED against
  the real corpus before registration (a malformed entry → `MISSING FIELD`, named).
- ⭐ The design's fixpoint defect — "the entry covers HEAD" is impossible, since the
  record commit advances HEAD — was caught by MEASUREMENT, not review: the end-to-end
  self-test's scratch push first ran with NO hooks installed (the defective check never
  ran); with the shim, the real boundary fired. The honest semantics: the entry names the
  WORK head; the record commit rides on top; the hook verifies the chain (self-test
  9/0 → 14/0 with the five approval-path arms).
- COMMIT.md names the act (the variable alone no longer suffices); the ledger has its
  routes-registry row. The tree closes 3/3 — all four Acceptance Criteria met.
- `make ci` green; `make gate` all green (28 doctrines / 297 arms). No push was attempted
  at any point; CHANGELOG.md / DEV_NOTES.md shard at their thresholds.

## SEMULITH-PD-0050 (leaf PUSH-DISCIPLINE.2) — full CI runs BEFORE the push, at the boundary

- The named full local suite: `make ci` = `check` (CI's rust.yml) + `gate` (CI's
  doctrines.yml) + `bench` + `smoke-bench` + `book` — matching the server workflows and
  consciously exceeding them with the bench and the books; the live three-way smoke is
  excluded with the reason recorded (it needs the untracked, network-acquired reference
  binaries — its standing as not-a-commit-gate). The membership is named in the Makefile
  comment, the hook's output, COMMIT.md, and the green-run record.
- `.githooks/pre-push` now execs `scripts/pre_push.sh`: cadence FIRST (a refused push
  never burns the suite), then `make ci` on BOTH paths (a director-approved push is not an
  unverified one), then the green-run record at `target/push/last-green.txt` (+ `.log`) —
  untracked, on-volume, overwritten per green run; explicitly NOT `.3`'s tracked
  append-only approval record. A red suite refuses, naming the failing leg from make's own
  error line. The cadence number stays in `check_push_cadence.sh` alone.
- Acceptance (d): fired RED by a deliberately broken check — the self-test's broken-suite
  arm refuses and writes NO green record; a red run after a green one does not overwrite
  the last green record; the cadence refusal leaves the suite's marker absent. Self-test
  9/0 in scratch repos with a real bare upstream (the `.1` pattern). On this repository
  the hook refuses cadence-first at 115/300, the suite unburned.
- No new doctrine (the boundary is a hook, not a commit gate — PUSH-CADENCE stays the
  registered one; decision recorded in the leaf). COMMIT.md's Pushing section documents
  the two-question boundary; TOOLBOX.md gains the two rows.
- `make ci` green end to end; `make gate` all green (27 doctrines / 291 arms).
  `PUSH-DISCIPLINE.3` (the approval record) is next.

## SEMULITH-UT-0053 (leaf UPSTREAM-TRACK.3) — age and exposure, derived; the tree closes (4/4)

- `scripts/upstream_exposure.py`: from each issue record's dated history, DERIVES — at run
  time, never stored — every tracked issue's state, its age in days (earliest dated event
  → today), and its exposure (the record's `blocks` field). Today: `0 open / 3 resolved /
  3 tracked` (all three LS issues verified). Open = the unresolved half of the declared
  state vocabulary (draft/reported/acknowledged/disputed/fixed-upstream); `verified` is
  resolved because WE re-ran it (the `.2` discipline). `--open-count` feeds the gate.
- The `UPSTREAM-INDEX` gate learns the field: `blocks` is now REQUIRED on every record,
  and each entry must have the leaf-id shape (BAD BLOCKS) and name a leaf that EXISTS in
  `docs/tasks/` (DANGLING BLOCKS — an exposure naming nothing is a lie about what is
  blocked). Self-test 17 → 21 arms, all RED named.
- `DERIVED-COUNTS` owns the figure: a new claim (`open upstream issues`, enumerator
  `upstream_exposure.py --open-count`), carried by MEMORY.md's Blockers line and
  re-derived every commit.
- ⛔ Defect found in flight, owned: DERIVED-COUNTS' `self-test arms` claim matched NO live
  document (its pattern never matched LIVE_STATUS's "N arms" wording) — the arms figure
  had never been re-derived and was silently stale (280 carried vs 291 real). Fixed in the
  document, not the gate; the gate went from re-deriving 3 claims to 5.
- The tree closes (4/4): criteria 1–3 from `.1`, criterion 4 from `.2` (strengthened by
  `.4`), criterion 5 — dated history answerable — is this leaf's derived figure.
- `make gate` all green (27 doctrines / 291 self-test arms, now genuinely re-derived);
  `check_upstream_index.sh --self-test` 21/0.

## SEMILITH-MB-0008 (leaf MODEL-BOOKS.6) — the wiring; MODEL-BOOKS closes (8/8)

- `make book` now builds the project book AND every model book (the Makefile's `book`
  target loops `docs/models/*/book.toml`; measured: two books, one command).
- Routing: the project book gains "The models" (`docs/book/src/models.md` — one
  definition, one book; 31 chapters) and README.md's Layout table gains the governed
  `docs/models/` row (69/85 lines, 3,947/4,864 B — inside both caps).
- The 27th doctrine `UNIT-BOOKS` (`scripts/check_unit_books.sh`): every registered unit
  (`materials/units.sexp` — the one registration place) has its own mdBook and it builds;
  a unit without a book (NO BOOK), a book missing its skeleton or failing to build
  (INCOMPLETE BOOK / BOOK DOES NOT BUILD), or a book no unit registers (ORPHAN BOOK) fails
  by name. Fired RED against the real corpus before registration (`NO BOOK rv64i-lab-v0`,
  named, with the book moved aside); self-test 7/0; mirrored per the registry rules.
  Measured in flight: mdbook tolerates a SUMMARY naming a missing chapter (draft +
  warning), so the build arm's broken fixture is a malformed `book.toml` — recorded in
  the gate's header.
- **The tree closes**: all seven acceptance criteria met — (1) every registered unit has
  a book and UNIT-BOOKS says so; (2) the materials list complete, generated, gated (`.1`);
  (3) the methodology follows one rule end to end (`.3`); (4) `make book` builds every
  book and the project book routes (`.6`); (5) prose dominates; (6) the teaching test —
  mistakes in — (every chapter); (7) real-compiled-code ability stated with its limits
  from the extension set (`.5`).
- `make gate` all green (27 doctrines, 287 arms — DERIVED-COUNTS re-derives);
  `check_materials_bill.sh [--self-test]` ok / 7-0; both books render.

## SEMILITH-MB-0007 (leaf MODEL-BOOKS.5) — the evidence, the gate, and the traceability walk

- The per-unit book's five-part arc completes (`docs/models/rv64i-lab-v0/src/evidence.md`):
  the evidence ledger per axis — never a banner — each number with its instrument and its
  re-derivation command: semantics 52/52 gated, the boundary domains exhausted, the failure
  layer three-way, the 21-cell interaction matrix resolved, the live differential (40
  guests, 492/492 aligned steps vs both references + the one declared expected divergence),
  restart as measured determinism, portability gated (wasm + the 44-arm browser bench),
  performance as one named host's baseline with no thresholds, and the mutation suite as
  the detector's proof. EVD-01's label stands over all of it: finite tested evidence.
- The verdicts, honestly: G0 `incomplete` (72 declared checks, 0 implemented — the
  generator has no code path to `passed`); G1 `incomplete` (criteria 1–5 met; criterion 6 —
  the C-toolchain guest — unmet, owned by `P2-SCALAR.5`, and that leaf's blockers are named:
  the ACT4 material absence and the C-guest routing awaiting the director). The teaching
  point: an honest gate that cannot read `passed` over a missing criterion is the lesson.
- Capability limits stated plainly: an M-mode-only laboratory with no C/M/A/F/D/Zicsr/
  Zifencei (what no M/A/F/D means for real code), no devices, board, boot or OS workload;
  a development profile — none accepted. "Supports RV64I" appears nowhere.
- The traceability walk is the evidence side: `D-MISALIGN-DATA` → `REQ-D-MISALIGN-DATA` →
  `OB-MISALIGN-DATA` (CHK-MISALIGN-DATA-POS/-NEG) → the recorded `smoke-trap` experiment
  (agreement on the architectural detail, with its decisive control) → two re-runnable
  commands with fresh output quoted verbatim (`cargo test -p semulith-verify --lib
  run::tests::smoke_trap` → 1 passed; `run_semulith_smoke.py` → the smoke-trap PASS lines).
- Both gate reports regenerate byte-identical (no drift). Every id/number verified by tool
  as written; no gate extended (26 doctrines). Both books render; `make gate` all green.

## SEMILITH-MB-0006 (leaf MODEL-BOOKS.4) — the references, their configuration, and what agreement is worth

- The per-unit book gains its references chapter
  (`docs/models/rv64i-lab-v0/src/references.md`): the cast honestly labelled (sail-riscv
  0.14, spike 1.1.1-dev, QEMU never-exercised, ACT4 never-a-second-opinion), the
  acquisition discipline (the fetcher fired RED on a corrupted digest), and the
  configuration story told through the controls that CHANGED the observation — the
  acceptance's own requirement.
- The three controls, with their recorded outputs: the ISA-string read-back (flipping `M`
  back on gave `DIFFERS … rv64im_zvl32b` against the pinned `rv64i_zvl32b`); the platform
  correction (`DIFF-PLATFORM-DEFAULT` — the CLINT `mtime` probe advanced 2, then 3 under a
  plain `ld`; the override now declares the device-less single-region platform, and
  `guest-no-device` holds it); and the decisive misaligned-policy flip (same ELF, nothing
  else changed: `FIRST DIVERGENCE at aligned step 2 … sail writes=[(x1, 0)] … spike
  writes=[]` — "the two models agree BECAUSE the profile is matched" is a measurement).
- The harness differences (including DIFF-TRAP-RECORD-SHAPE — the comparator's false pass
  on a truncated trace) and the two measured reference-vs-reference differences
  (DIFF-FENCEI-EXECUTED, pinned as the `it-fencei` expected divergence;
  DIFF-TVAL-PHYS-MASK) are told as the lessons they are.
- The independence inventory in prose: encoding not-shared (and the cut runs the other way
  than first assumed — our assembler shares `riscv-opcodes` ancestry with SPIKE, not
  Sail), floating point shared (184/199 files byte-identical), integer semantics
  no-evidence-of-sharing, expected-result derivation shared (ACT4 ↔ Sail), QEMU
  not-examined — ending in the per-leg verdict: encodings rest on Sail alone, semantics on
  both references, nothing on ACT4 or QEMU.
- Every id/version/count grep-verified as written; no gate extended (26 doctrines). Both
  books render; `make gate` all green.

## SEMILITH-MB-0005 (leaf MODEL-BOOKS.3) — the methodology: from document to model

- The per-unit book gains its methodology chapter
  (`docs/models/rv64i-lab-v0/src/methodology.md`): the pipeline as six gated hops —
  pinned document → decision (authority) → requirement (semantic class) → obligation
  (positive AND negative checks) → derived expectation → the differentials (offline on
  every commit, live three-way).
- The reserved-FENCE rule is followed end to end, by name: the pinned sentence (RVI-RV32I
  §1.1.7, quoted verbatim) → `D-FENCE` (authority execution-environment, the correction
  note intact) → `REQ-D-FENCE` (class implementation-defined, statement verbatim under
  RECORD-SCHEMA) → `OB-FENCE` (CHK-FENCE-POS AND -NEG) → `fault-fence` (EVD-05,
  measured on both references first) → the offline suite and the live smoke. The honest
  gap is in the chapter: the obligation's check ids are declared and G0 measures
  72 declared / 0 implemented — the guest corpus is what tests the rule today.
- The judgement calls are explained with their mechanical edges: semantic class (what
  freedom the source grants) vs authority (who may decide; laboratory policy cannot
  override an architectural rule — the AUTHORITY check). The mistakes stay in:
  DEFECT-A (the dossier condemned the mandated nop; measurement inverted it), DEFECT-B
  (the misaligned-jump link write, fixed in semantics DATA, pinned by `never_written x5`),
  and the two authoring REDs (the overlap constant; the trailing paren) — gates catching
  the author.
- Every id the chapter names was grep-verified against the tracked corpus as written;
  the quoted decision fragments are programmatically verified verbatim. No gate extended
  (authored prose, no generated content — 26 doctrines unchanged). Both books render;
  `make gate` all green.

## SEMILITH-MB-0004 (leaf MODEL-BOOKS.2) — what the materials do not contain; the PDF investigation answers YES

- The per-unit book gains its gaps chapter (`docs/models/rv64i-lab-v0/src/gaps.md`):
  the measured no-encodings gap and what it forced (the RISCV-OPCODES second provenance,
  the parse-and-refuse assembler discipline), the gaps the specification is *supposed* to
  leave (the EEI policy choices; a platform), and the gap the references leave (agreement
  is not proof) — prose-first, per the teaching mandate.
- ⭐ The investigation, done with a tool: the pinned publication (docs.riscv.org,
  `v20260120`) publishes a PDF rendering at the same version segment
  (`_attachments/riscv-unprivileged.pdf` — HTTP 200, 4,580,174 B, sha256 `06bb3c23…`,
  696 pages, `Version 20260120: Official Release`). `pdftotext` measures its text layer
  carrying the instruction-format tables: **232** lines match the `[01]{7}` census pattern
  that returns **0** on all six pinned HTML/TXT artifacts; the base-formats figure and the
  RV32I opcode map extract with bit strings and field names. **Answer: yes — encodings
  can be re-sourced from the primary document**, so the encoding provenance's
  shared-ancestry exposure (shared with Spike, not Sail) is no longer forced.
  Qualifications recorded: the PDF numbers chapters differently from the pinned HTML
  (Introduction is Chapter 1 there; RV32I Chapter 2 / RV64I Chapter 4 vs §1.1 / §3.1), and
  the extraction is layout-fragmented — re-sourcing is engineering with its own
  verification, and is future reviewed work, NOT this leaf.
- The PDF is cached untracked at `target/materials/` and deliberately not catalogued
  (the corpus model has no network-origin kind — a MODEL-METHOD decision, recorded in the
  chapter). The cached GitHub-release PDF corroborates (269 census lines) — the finding
  depends on no one PDF.
- No gate surface changed (the chapter is authored prose; MATERIALS-BILL untouched, 26
  doctrines). `mdbook build docs/models/rv64i-lab-v0` and `make book` render; `make gate`
  all green.

## SEMILITH-MB-0003 (leaf MODEL-BOOKS.1) — the per-unit book structure and the materials bill

- `docs/models/<unit-id>/` established as the per-unit mdBook — repeatable for any unit
  kind (`decision_one-definition-one-book`): `docs/models/rv64i-lab-v0/` renders
  (`mdbook build`), with the five-part shape contract in its introduction (materials,
  gaps, method, references, evidence/gate — each part naming its owning leaf).
- The complete materials bill (`src/materials.md`): 15 materials — the 3 pinned
  specification artifacts, the RISCV-OPCODES encoding source, the 4 reference candidates,
  and the 7 internal contracts — one section each, every section stating what the
  material does NOT supply; the mistakes stay in (no encodings in the pinned spec —
  measured; the encoding provenance shared with Spike, not Sail — stated plainly; the
  PDF question routed to `.2`).
- The identity tables are GENERATED by `scripts/gen_model_book.py` from the pinned
  `sources.sexp` / `references.sexp` / tracked contracts (OWN-03 manifests; digests,
  sizes, versions, record counts derived — never retyped), and the 26th doctrine
  `MATERIALS-BILL` (`scripts/check_materials_bill.sh`) refuses drift and any material
  section missing its does-not-supply statement — fired RED against the real corpus
  before registration; self-test 7/0; mirrored per the registry rules.
- Registry repairs: `materials/units.sexp`'s `book` field corrected to
  `docs/models/rv64i-lab-v0/` (it named a project-book page that was never created);
  `doctrine/fact_ownership.tsv` +4 owner→mirror rows; `doctrine/readme_routes.tsv` +1
  family (`docs/models/` 8 files / 27,600 B at adoption; health 16 / 64 KiB; ceiling
  40 / 256 KiB; per-part 32 KiB). The leaf text's `sources.toml`/`references.toml`
  reference was stale (the one-format migration) — corrected in the leaf with a note.
- Validation: `mdbook build docs/models/rv64i-lab-v0` and `make book` render;
  `make gate` all green — 26 project doctrines, 280 self-test arms, 32 routed
  destinations (all re-derived). No Rust changed.

## SEMILITH-PS-0007 (leaf P2-SCALAR.4) — the interaction matrix: declared, exercised, gated

- The 21-cell fault × alias × boundary × event × progress × restart matrix is tracked
  data (`profiles/rv64i-lab-v0/interactions.sexp` over the new `schema/interactions.sexp`),
  declared first and then exercised; the 25th project doctrine `INTERACTION-MATRIX`
  re-derives the cells from the axes and refuses by name an omitted cell, an unresolved
  disposition, an orphan guest, or an unrecorded difference id — fired RED against the
  real corpus (`NO MATRIX`) before registration; self-test 12/0; mirrored per the
  registry rules.
- Eight new EVD-05 guests, every behavior probed before authoring: `it-prio-jump` /
  `it-prio-load` (misaligned AND unmapped → the misaligned cause wins, three-way),
  `it-fault-alias` (a misaligned load over its own base preserves the base),
  `it-fault-wrap-ld` / `it-fault-wrap-sd` (the address wraps mod 2^64 INTO the access
  fault, tval 0 — kept below 2^56 after the probes found sail's 56-bit tval masking,
  recorded as the new `DIFF-TVAL-PHYS-MASK`), `it-alias-bound` (self-aliased ops at
  boundary values), `it-progress-loop` (an unbounded loop under the budget contract, the
  x0 link discarded, `Stop::Budget`), `it-fencei` (the `DIFF-FENCEI-EXECUTED` pin).
- The comparator learned the EXPECTED divergence: `expect_divergence` on the expectation
  document (schema + dossier round-trip), `check_expected_divergence` in
  `compare_traces.py` (self-test 16/0 — an AGREE at the declared step is RED), and the
  smoke run's four-step protocol (own expectations; first divergence at exactly the
  declared step against each reference; sail vs spike agree over their full length; the
  difference id recorded). `cross_model` stays a comparison DISABLE.
- The restart axis is a mechanism, commit-gated: the new offline determinism suite runs
  every guest twice from `zeroed_at(entry)` and asserts identical traces and crossing
  logs, beside the smoke's reproduce leg.
- Validation: 166 verify suites (+8 guest suites, +1 determinism suite), 65 core;
  `make gate` green with 25 doctrines; smoke-bench 44 arms (40 clean guests);
  `EXERCISE-COVERAGE` 52/52 (self-test 7/0); live three-way: **40 guests, 492/492
  aligned steps** plus the one declared divergence, byte-identical reproduction.
- Reviewed ceiling expansion: `profiles/` 78 → 95 files / 402,967 B (registry 82 → 99
  files, 471,040 → 516,096 B; per-part 32,768 untouched — it bit on `references.sexp`,
  so the difference record was tightened rather than the ceiling moved); the 25th
  doctrine row also re-based the TOOLBOX.md / DOCTRINE_ENFORCEMENT.md caps to
  20 KiB / 28 KiB (the SEMILITH-PL-0001 precedent).

## SEMILITH-MB-0002 (leaf MODEL-BOOKS.8) — annex: building the first CPU model, step by step

- Director request: the project book gains `annex/building-first-model.md`, a teaching
  chapter that walks the creation of `rv64i-lab-v0` end to end — choose a finishable
  target, pin the materials (and measure what they lack: no encodings), the dossier with
  its decision authorities, predeclared requirements, the hidden-state census, the one
  canonical definition, generation over hand-editing, the data-evaluating interpreter,
  before-any-run expectations, the one observation vocabulary, whole-platform matching,
  honest comparison, the detector's own proof, the three coverage campaigns, and the
  honest gate — each step with what you do, why that order, what went wrong for real,
  and a re-runnable command.
- The mistakes stay in, per the tree's teaching mandate: the matched profile that matched
  only an instruction set (the advancing `mtime`), the truncated trace that read as
  agreement, the inverted FENCE dossier defect, the authoring constants the gate caught.
- Every command the chapter prints was executed against the real repository (the
  `zext-addi` mutant is caught, rc=1; the scope census counts 52); chapters 29 → 30
  (re-derived by DERIVED-COUNTS; LIVE_STATUS restates).
- Placement follows `.7`: the project book's annex — the per-unit book structure
  (`.1`) is unbuilt; when it lands, the model book references this chapter rather than
  copying it (never a second owner of a fact).

## SEMILITH-PS-0006 (leaf P2-SCALAR.4) — the interaction-matrix design, recorded before code

- Design-only commit: the 21-cell fault × alias × boundary × event × progress × restart
  matrix, 8 new guests, the expected-divergence comparator shape, the restart axis as a
  mechanism (a new offline determinism suite), and the `INTERACTION-MATRIX` doctrine
  design — every reference behavior measured by probes first (fault priority, the
  address wrap, the fence.i continuation).
- Measured a NEW reference difference: sail masks access-fault tval to its 56-bit
  physical-address width (spike reports the full address) — recorded as
  `DIFF-TVAL-PHYS-MASK`; three-way tval guests keep fault addresses below 2^56.
- The tree file crossed its 64 KiB per-part ceiling: completed-leaf evidence archived
  verbatim to `docs/tasks/archive/P2-SCALAR.md` — the ceiling obeyed, not raised.

## SEMILITH-PS-0005 (leaf P2-SCALAR.3) — fault, suppression and reserved cases: the failure layer, pinned three-way

- Every reference behavior was MEASURED before any guest existed (16 probe ELFs against
  sail-riscv 0.14 AND spike 1.1.1-dev). Then eighteen guests pinned the measurements as
  specification-derived expectations (`EVD-05`), all agreeing three-way: **32 guests,
  454/454 aligned steps**, byte-identical reproduction.
- **DEFECT-A inverted.** The `.1` log said a reserved-`fm` FENCE must trap; the pinned
  spec mandates the nop, verbatim ("Base implementations shall treat all such reserved
  configurations as FENCE instructions (with fm = 0000)", RVI-RV32I §1.1.7), and both
  references execute exactly as the model does. The dossier was wrong, the model right:
  `D-FENCE` and its `REQ-D-FENCE`/`OB-FENCE` restatements are corrected; `fault-fence`
  pins reserved-fm, FENCE.TSO, ignored rs1/rd and pred/succ-zero configurations as nops.
- **DEFECT-B fixed in semantics data.** A misaligned `jal`/`jalr` wrote its link register
  before trapping; both references suppress the write (a synchronous exception retires
  nothing). The `jal`/`jalr` effect trees now check the target (`set-pc`) before the link
  write — the evaluator is untouched; `fault-jal-mis`/`fault-jalr-mis` pin it with
  `never_written x5`; the mutation matchers were re-derived for the new tree shape.
- **The word-less fetch-fault step.** A fetch fault on a jump TARGET is reported on the
  target with no instruction word (D-FETCH-FAULT-REPORT): `run::Step.word` is now
  `Option<u32>`, the runner emits the trap with no word and keeps `Stop::FetchFault`,
  the CLI prints `(fetch fault)`, replay round-trips the null, and both trace adapters
  synthesize the same shape — `fault-fetch` compares three-way.
- **Reserved cases keep their source meaning (SEM-07).** The interpreter reports the
  UNSPECIFIED case (`Stop::Undefined`); the laboratory's declared `D-RESERVED-DECODE`
  policy — the harness's explicit act in `run.rs`, never the interpreter — converts it
  to the illegal-instruction observation with tval = the offending word, measured
  identical on both references. `fault-reserved` (0xFFFFFFFF) and `fault-shiftw-res`
  (`slliw` imm[5]=1) pin it — the second **answers OQ-2**: both current references treat
  the reserved `*IW` shift as illegal (`REQ-D-SHIFTW-RESERVED` → `resolved`; G0 shows one
  open question where there were two).
- Suppressed effects (SEM-06): six not-taken branches to misaligned targets raise nothing
  (`fault-branch-nt`); misaligned stores never cross the boundary — proven by the
  crossing log (`fault-st-mis-h/w/d`); misaligned loads across widths (`fault-ld-mis-h`,
  the 4-aligned-but-not-8 `fault-ld-mis-d`); `D-LOAD-X0` still faults with a discarded
  destination on both failure paths (`fault-ld-x0-mis`, `fault-ld-x0-fault`); access
  faults run cross-model at 0x40000000, no platform's device (`fault-access-ld`,
  `fault-access-sd`); the RV64I HINT table's ALU forms are nops that must not trap
  (`fault-hints`); a store over a later-fetched word is fetch-visible immediately —
  measured on BOTH references first (`fault-selfmod`, D-CODE-VISIBILITY).
- Recorded, not exercised: `fence.i` executes on both references although the matched ISA
  strings exclude Zifencei — a legitimate UNSPECIFIED divergence the comparator cannot
  yet express; `DIFF-FENCEI-EXECUTED` in `references.sexp`, the guest routed to `.4`.
- Tooling: `riscv_asm.py` learned the `.word` directive for raw reserved words (its
  mnemonic path's range checks exist to refuse them); the trace adapter learned four
  measured spellings (`misaligned-fetch`, `trap_instruction_address_misaligned`,
  `store/amo-access-fault`, `misaligned-store/amo`) — its refusal fired mid-run on the
  last one, exactly as designed; adapter self-test 12/0 (+4 arms).
- Reviewed ceiling expansion: `profiles/` 42 → 78 files / 367,466 B; registry ceilings
  46 → 82 files and 393,216 → 471,040 bytes; per-part 32 KiB unchanged (largest new file
  4,017 B). Instruments caught three AUTHORING slips in flight (a systematic trailing
  paren in all 18 expectation documents, the store operand order in 4 guests, the
  REQ-D-FENCE statement drift at the gate) — never another model defect.
- Verification: 157 verify suites (+18 guest suites, +2 runner suites), 65 core suites,
  clippy `-D warnings`, `make gate` all doctrines green, `make smoke-bench` 36 arms
  (32 clean guests), `EXERCISE-COVERAGE` 52/52 (self-test 7/0), `make book` renders.
  Live: **32 guests, 454/454 aligned steps** against sail-riscv AND spike.
- Lockstep: MEMORY/LIVE_STATUS (P2 3/9)/TASK_TREE (frontier `.4`)/CHANGELOG/DEV_NOTES +
  book P2 (the `.3` result), P1 and claim-scope (32 guests, 454 steps), annex/assembler
  (`.word`), the routes registry, the dossier (D-FENCE, OQ-2), references.sexp, and both
  regenerated `G?-REPORT.md`.


## SEMILITH-MB-0001 (leaf MODEL-BOOKS.7) — annex: how the tracked assembler works

- Director request: the project book gains `annex/assembler.md`, a teaching chapter on
  `scripts/riscv_asm.py` — why it exists (EVD-05: guest bytes encoded independently of the
  models under test), the table pipeline (pinned `riscv-opcodes` → fragments → the unit's
  composition → words → `guests.rs` / ELF), the three operand classes (fixed bits;
  width-checked contiguous fields; the B/J scramble derived from the pinned descriptors with
  the accounted-bits == field-width self-check), the two-pass label front-end (x0..x31 only,
  no ABI names, no pseudo-ops — deliberate), the ELF writer (the section table exists because
  Spike's loader was measured refusing a sectionless ELF), and the refusal discipline
  (`AsmError` — never a guess; a generator that guesses is a second definition). The shared
  ancestry of the encodings (riscv-opcodes is upstream of Sail and Spike) is stated, with the
  spike-dasm round-trip as the recorded mitigation.
- Out of order: leaf `.7` lands while `.1`–`.6` are pending — the per-unit book sequence is
  unchanged; the annex lives in the project book because the assembler is shared project
  machinery and the per-unit book structure is unbuilt (`.1`). Placement recorded in the tree.
- Verification: `make book` renders the chapter (28 → 29 chapters); the chapter's "Try it"
  snippet was executed, not imagined (`addi x1, x1, -1` → `0xfff08093`, label-resolved `bne`
  → `0xfe009ee3`); `make gate` green.
- Lockstep: MEMORY (MODEL-BOOKS 1/7), LIVE_STATUS (29 chapters, MODEL-BOOKS 1/7),
  CHANGELOG/DEV_NOTES, the tree (frontier `.1` unchanged), and the book itself.

## SEMILITH-PS-0003 (leaf P2-SCALAR.2) — boundary arithmetic and state interactions: the shamt domains exhausted

- Five boundary guests, every expectation value derived from the pinned specification before any model ran (`EVD-05`): `bound-shift` (89 steps — the **6-bit shamt domain exhausted** by one `srli` sweep over all 64 amounts of `0x8000000000000001`; `slli`/`srai` pinned at {0,1,2,4,8,16,32,63}; register-amount corners rs2 = 64 → reads as 0, pre-written to stay visible, and rs2 = -1 → 63), `bound-shiftw` (55 steps — the **5-bit domain exhausted** by one `sraiw` sweep; the rs2 = 96 `srl`/`srlw` pair on identical operands answers 0x00000000FFFFFFFF vs the sign-extended identity, pinning the 6-bit vs 5-bit read), `bound-arith` (31 steps — INT64_MAX + 1 / INT64_MIN - 1 wraps on the register AND immediate paths, *W wraps with a garbage upper half provably ignored, `slt`/`sltu` at the extremes, `auipc 0x80000` wrapping the address sum modulo 2^64 to exactly 4·n), `bound-ext` (47 steps — the sign edges 0x7F/0x80, 0x7FFF/0x8000, 0x7FFFFFFF/0x80000000 as sign/zero PAIRS at one address, the 0x00 byte through a pre-write, store truncation at non-clamping values; 32 census-pinned crossings), `bound-alias` (37 steps — the little-endian lane proof, overlap composition `sd`+`sb`+`sh`+`ld`, register aliasing incl. a load over its own base register, x0 in both directions; 16 crossings).
- The commit gate caught two **authoring** defects, never a model one: the overlap-composition constant was hand-assembled wrong twice (`0x4CD`'s high byte is 0x04; then the AA lane one hex pair over) — each RED was answered by re-deriving from the spec rule, and the corrected value is what the rule computes. Lesson declined for promotion: the gate already fails any expected value the spec rule does not compute — measured twice this leaf.
- Reviewed ceiling expansion (the `.1` decision names this leaf's guest growth as its own decision): `profiles/` 32 → 42 files / ~307 KB; registry ceilings 34 → 46 files and 256 → 384 KiB; per-part 32 KiB unchanged (largest new file 27,848 B).
- Verification: 138 verify suites (+5 guest suites), 65 core suites, clippy `-D warnings`, `make gate` 24 doctrines green, `make smoke-bench` 18 arms (14 clean guests), `EXERCISE-COVERAGE` 52/52 (self-test 7/0). Live: **14 guests, 376/376 aligned steps** against sail-riscv AND spike, byte-identical reproduction.
- Lockstep: MEMORY/LIVE_STATUS (P2 2/9)/TASK_TREE (frontier `.3`)/CHANGELOG/DEV_NOTES + book P2 (the `.2` result), P1 and claim-scope (14 guests, 376 steps), the routes registry, and both regenerated `G?-REPORT.md`.

## SEMILITH-PS-0001 (leaf P2-SCALAR.1) — the declared instruction scope, completed and gated

- The profile declares 52 RV64I forms; the four P1 smoke guests exercised 15. Five scope-completion guests close the gap, every expectation value derived from the pinned specification before any model ran (`EVD-05`): `scope-alu` (31 steps — the 21 remaining logical/compare/shift forms plus `fence`, with the signed/unsigned pairs on shared operands, the `rs2[4:0]`-vs-`rs2[5:0]` shift pin, and two 1→0 pre-writes so 0-results are VISIBLE changes in the trace vocabulary), `scope-mem` (29 steps — the 8 remaining load/store forms: sign/zero-extension pairs at one address, a discarded `lw x0` per `D-LOAD-X0`, three store widths with read-back, 17 census-pinned data crossings), `scope-branch` (19 steps from 24 instructions — the 5 remaining branches taken AND not-taken, five `never_written` negative observations), `scope-ecall` and `scope-ebreak` (the requested traps, one guest each, trap step last — cause 11/tval 0 and cause 3/tval=pc, matching both references exactly).
- Coverage is reported with its **denominator** and the report is a gate: the 24th project doctrine `EXERCISE-COVERAGE` (`scripts/check_exercise_coverage.sh`) re-derives the denominator from the dossier's scope lists (a `count_total` contradicting the enumeration is a DENOMINATOR LIE), unions the mnemonics the expectation documents declare executed (the commit gate proves those steps execute), refuses any unexercised form BY NAME, and resolves the `SCP-02` closure through the one shared resolver (`riscv_asm.resolve_composition`) — a declared form the composition does not provide is an UNRESOLVED FORM. It fired RED against the real corpus at 15/52 — all 37 missing forms named — before registration; self-test 7/0; GREEN at 52/52 since.
- `fence` needed its `fm`/`pred`/`succ` operand fields: the pinned `arg_lut.csv` carries them, so `gen_fragments.py`'s field whitelist and `riscv_asm.py`'s contiguous operands were extended and `definitions/riscv/rv64i.sexp` + `definition.rs` regenerated — no opcode typed by hand anywhere; the generated-module field-count pin moved 12→15 with its reason recorded. The trace adapter learned sail-riscv 0.14's `m-call`/`software-breakpoint` and spike 1.1.1-dev's `trap_machine_ecall`/`trap_breakpoint` — measured spellings; unknown ones raise, because a dropped trap reads as agreement. `gate_report.py`'s hardcoded "The four tracked guests…34/34" became derived counts; both `G?-REPORT.md` regenerate (9 guests, 117 expected steps).
- Verification: 133 verify suites (+5 guest suites, the census pin extended), 5 core suites, `make check` green, clippy `-D warnings` clean, wasm build rc=0, `make smoke-bench` 13 arms (9 clean guests), `make gate` 24 doctrines green. The live experiment: 9 guests, **117/117 aligned steps** against sail-riscv AND spike, every enabled comparison agreeing, each run reproducing byte-identically.
- Defect found in flight, logged and owned (not fixed here): a FENCE with a reserved `fm` value executes as a nop where `D-FENCE` says illegal-instruction — reproduced with word `0x1ff0000f`; routed to `P2-SCALAR.3` because the fix needs a legality constraint the encoding format does not yet express.
- Lockstep: MEMORY/LIVE_STATUS (P2 1/9)/TASK_TREE/CHANGELOG/DEV_NOTES + book P2 (the `.1` result), P1 and claim-scope (9 guests, 117 steps), the doctrine mirrors and TOOLBOX (the new gate's rows), and this tree — the frontier moves to `.2` (boundary arithmetic).

## SEMILITH-PL-0013 (leaf P1-LAB.13) — the allocation-count pin: proven, not reported

- The `.11` baseline's allocation figures gain their falsification leg. `bench::alloc` grows a thread-local counter scope (`thread_reset`/`thread_counts`) — a process-global counter inside a parallel test binary counts every sibling suite, so exact pins need per-thread counting (the single-threaded CLI sees both scopes agree by construction).
- Slope/intercept probes nailed the mechanism behind every figure: untraced = exactly 1 allocation/step, zero intercept (the `extract_operands` operands Vec; pinned: 114 steps ⇔ 114 allocations / 14,368 bytes); instrumented = untraced + the `run::diff` writes Vec ONLY on a visible register change + stream amortized growth — `diff` compares values, so the mixes' near-fixed points (not an error) are why the traced columns sat near 1.2; diagnostic = instrumented + exactly the crossing log's capacity doublings (+4/+5/+6 at 30/58/114 steps); static and dyn dispatch allocate identically, per mix, exactly.
- Four pin suites in `bench/tests.rs` hold the exact truth and fail if it moves; each was fired RED against a perturbed constant before landing (114↛115, 50↛51 — both named the true value). `baseline.sexp` stands UNCORRECTED — every figure survived the proof; the G1 report (regenerated, mechanism sentence added) and the book now state the mechanism so the traced columns can't be misread as general.
- Verification: 193 tests across 5 suites (128 verify, +4 pins); clippy `-D warnings` clean; wasm build rc=0; `make gate` 23 doctrines green. The docs/tasks archive split in two when it crossed the per-part ceiling (65,617 B → part 1 / part 2) — the ceiling obeyed at both levels. Knowledge card `pin-the-mechanism-slope-before-the-number.md` carries the lesson.
- Lockstep: MEMORY/LIVE_STATUS (P1 13/13)/TASK_TREE/CHANGELOG/DEV_NOTES + book P1, G1-REPORT, knowledge INDEX, and this tree; P1-LAB closes again at 13/13.

## SEMILITH-PL-0012 (leaf P1-LAB.12) — the G1 gate report; P1-LAB completes with the gate honest

- `scripts/gate_report.py --gate G1` generates `profiles/rv64i-lab-v0/G1-REPORT.md` from tracked inputs only — byte-stable in a fresh clone, the G0 path byte-unchanged (verified by diff). Each of the SIX `ROADMAP.md` §6 G1 criteria is measured from tracked files by concrete name (the G0 lesson: an id-shaped pattern in prose is not evidence): replay/reduce machinery + CLI wiring + suite counts; the four outcome families + the SEM-02 arm; the graph checker + `check-examples`; the mutation suite's 11 arms and 4 model-level mutants; the recorded baseline; the guest census. The generator has no code path to `passed` while a criterion stands unmet — EVD-08's forbidden outcome, generalized.
- Scoping the leaf surfaced a drift: this tree's G1 acceptance listed five criteria where the roadmap states six (ROADMAP-V3.3's sharpening never re-synced into the tree). Repaired in-tree: criterion 6 absorbed with its standing named. **Verdict: `incomplete`** — criteria 1–5 met; criterion 6 (the compiled freestanding guest, C first) unmet as written: `guests/` holds 4 assembly and 0 C guests; the assembled guests' 34/34 first-divergence result against sail-riscv and spike is recorded as the partial standing; owner `P2-SCALAR.5`, with ROUTING EVIDENCE in the leaf (what reproduces outside the tree, what was measured, what would make the routing wrong).
- `profiles/rv64i-lab-v0/baseline.sexp` freezes the `.11` measurement as data (the references.sexp experiment-record precedent): host, config, all 16 cells, the static/dyn ratios, the RUST-02 agreement, `(thresholds none)` — validated field-by-field by the generator and parsed by all three tracked readers.
- GATE-REPORT discovers `G?-REPORT.md` per profile and covers both gates (self-test 6/0; RED probes: tampered G1 report named rc=1, baseline removal flips criterion 5, unknown gate refused rc=2). No new doctrine; the registry row's prose now spans G0 and G1. P1-LAB.md archives its `.11` checklist and the completed leaves' design detail (per-part ceiling obeyed, not raised).
- Verification: `make gate` 23 doctrines green; 189 tests across 5 suites unchanged (no Rust change); wasm build rc=0; book builds. Lockstep: MEMORY/LIVE_STATUS (P1 12/12, gate verdict recorded)/TASK_TREE/CHANGELOG/DEV_NOTES + book P1 ("Gate G1" carries the verdict and its reason) and this tree — P1-LAB is done; P2-SCALAR and DSP-REVIEW are unlocked.

## SEMILITH-PL-0011 (leaf P1-LAB.11) — the performance baseline; the laboratory measures itself

- `semulith-verify::bench` is the measurement harness (RUST-04): four programmatically generated workload mixes — arithmetic (no data memory), control (alternating branches + jal/jalr), memory (stores and loads at all four widths), fault (model-side misaligned load/store + environment-side out-of-region load every iteration, under the stated delivery-continues policy) — each a counted loop ending in EBREAK, with every generated word pinned to `definition::decode` by the decode round-trip suite so the encoder cannot drift from the definition it feeds. The three ARCHITECTURE §6 modes run under one counting environment: `run_untraced` (no observation constructed), `run_instrumented<O: Observer + ?Sized>` (the Step stream via `run`'s own snapshot/diff/trap-mapping), `run_diagnostic` (+ the crossing log via `run`'s own `Recording`). `agree` states RUST-02 as data — steps, stop, final state, census, and every recorded stream — and the CLI refuses (exit 1) on disagreement.
- The `alloc` module is a std-only counting `GlobalAlloc` (RUST-01: no benchmarking crate), installed by the CLI binary and the verify test binary, never the wasm cdylib. RUST-03 becomes a number: **1.00 allocation/step untraced** (the `extract_operands` Vec, 126–141 bytes/step), 1.19–1.42 traced — a measured departure, on record for the milestone that needs it.
- `semulith bench` names the host — Apple M4 Pro; Darwin 27.0.0; rustc 1.95.0 — and measures iterations=10000, warmup=2, reps=12: untraced 47.2–54.1 ns/step across the mixes, instrumented +24–40%, diagnostic +4–8% further; noise spread 1.7–7.4% per cell (one 113% scheduler outlier on a millisecond-scale cell). **No regression threshold is set** — the noise table is the deliverable a future threshold cites. The static-vs-dynamic observer question (parked since `.1`) resolves by measurement: ×0.974–1.002, within noise; static generics stay the default.
- Verification: 189 tests green across 5 suites (124 verify incl. 10 bench suites); clippy `-D warnings` clean; wasm build rc=0; `make gate` 23 doctrines green; `semulith bench` rc=0 with RUST-02 agreement OK on every mix. Book P1's "The performance baseline" now carries the measured table; TOOLBOX gains the `semulith bench` row; the `.10` acceptance checklist archives to `docs/tasks/archive/P1-LAB.md` (per-part ceiling obeyed).
- Lockstep: MEMORY/LIVE_STATUS (P1 11/12)/TASK_TREE/CHANGELOG/DEV_NOTES + book P1 and this tree; frontier moves to `.12` (the G1 gate report).

## SEMILITH-PL-0010 (leaf P1-LAB.10) — replay and reduction; a result becomes an artifact

- `semulith-verify::replay` is the recorded input bundle (G-REPLAY): `algorithm` pins flattened from `definition::MANIFEST` — profile, ilen, generator name+sha256, every input pin — plus the harness version and the model under test (`production` or `mutant:<name>`, resolved through the `.9` vocabulary); the platform region and entry; the image words with a sha256 guard; the recorded event choice (`DeclaredNone`, OB-ENV-EVENT-DELIVERY named — the platform's actual choice, recorded as data); the step budget; and the recorded steps plus the stop's canonical render. `replay()` checks identity by name — definition pins against the live manifest, then the image digest against the bundle's own words — and walks recorded-vs-replayed through `run::compare`, so drift is named at the first differing observation. JSON both ways through the crate's own reader and a hand-rolled writer; a document missing any accompaniment fails parse naming the field — the bare-seed refusal is structural (ARCHITECTURE §7: a seed without the generator version and event stream is insufficient).
- `semulith-verify::reduce` is the minimizer (EVD-02): classic ddmin over the guest word sequence with retention = the original first divergence exactly (same step, same field description — identical prefix semantics make a same-step divergence byte-identical). Every accepted removal preserves the property structurally, so the result always retains; each minimized result carries an exhaustive 1-minimality witness (no single-word deletion retains). Measured on the suite: zext-addi → the 2-word prefix (x1 @ step 1), jal-no-link → 4 words (x5 @ step 7), jalr-odd-bit → 9 words (trap @ step 10, tval 0x80000029 re-derived from the minimized program — the fixture note's prediction, retained). Named boundary: phantom-load is refused `NoDivergence` — census-class wrong behaviour is not reducible on observations.
- `semulith-cli` gains `semulith bundle --guest=X --mutate=Y` (write the bundle JSON), `semulith replay <file>` (re-derive and judge: identical rc 0, named mismatch/refusal rc 1), and `semulith reduce --guest=X --mutate=Y` (print the minimized program with its retained divergence). Exercised end to end: bundle → replay identical; a hand-corrupted bundle refused naming the digest.
- Verification: 179 tests green across 5 suites (114 verify incl. 15 replay + 6 reduce); clippy `-D warnings` clean; wasm build rc=0; `make gate` 23 doctrines green. Book P1 gains "Replay and reduction"; the `.9` acceptance checklist archives to `docs/tasks/archive/P1-LAB.md` (per-part ceiling obeyed).
- Pressure valve, same commit: both append heads crossed their registry ceilings on this entry — CHANGELOG.md sheds its oldest entry to `docs/changelog/shard-0033.md` (head 67,723 → 64,156), DEV_NOTES.md its two oldest to `shard-0034.md` (51,872 → 48,589); the manifest re-freezes at 36 rows and SHARD-FREEZE stays green.
- Lockstep: MEMORY/LIVE_STATUS (P1 10/12)/TASK_TREE/CHANGELOG/DEV_NOTES + book P1 and this tree; frontier moves to `.11` (performance baseline).

## SEMILITH-LB-0001 (leaf LAB-BENCH.1) — the laboratory bench: feel the tool while it builds

- `semulith demo [--guest NAME] [--mutate NAME] [--json]` runs a tracked guest under the real or a mutated model and prints the full observation trace with the judgement — the pinned expectation verdict and, for mutants, the first divergence named, or the crossing-census story when the trace never betrays the mutation (the phantom-load arm). Exit codes make the detector legible: 0 clean, 1 a caught mutant, 2 usage.
- The browser bench: `bench/index.html` over a std-only wasm module (`semulith-verify`'s cdylib with an `extern "C"` surface in `src/wasm.rs` — no wasm-bindgen, no new dependency, RUST-01 untouched). Guest × model selectors render both traces side by side with the first divergence highlighted; `make bench` builds the module, `scripts/smoke_bench.js` verifies the page's engine headlessly with node (8 arms: clean × 4 guests, the three trace-level mutants at their .9-pinned steps, the census arm at 7-vs-0). Same `run`/`mutate` engine the commit gate tests; the JSON shape is shared with `demo --json`.
- `semulith-verify` gains `report` (the demo/bench judgement: the `.9` anchor made reusable — architectural expectations and the crossing census as two separate verdicts, because the phantom-load arm keeps one while breaking the other) and promotes the suite's pinned census table to the public surface.
- Verification: 158 tests green across 5 suites (93 verify incl. 5 report suites); clippy `-D warnings` clean; wasm workspace build rc=0 (PORT-WEB holds with the new cdylib); `make gate` 23 doctrines green; smoke_bench 8/0. Book P1 gains "The laboratory bench"; TOOLBOX gains the two bench tools.

## SEMILITH-PL-0009 (leaf P1-LAB.9) — the validator mutation suite; a differential that is known to disagree

- `semulith-core::exec::step_over` and `semulith-verify::run::run_over` parameterize the single execution path over the instruction table — production delegates with `definition::INSNS`; the table scan applies exactly the predicate the generated `decode` documents, pinned by a core suite over every canonical word, operand-varied encodings, and unclaimed words. A mutation is data the one evaluator consumes (OWN-01); there is no second implementation of any rule.
- `semulith-verify::mutate` is the EVD-09 suite, 11 arms: the eight designated wrong-behaviour classes — wrong sign extension (x1 @ guest-control step 1), suppressed register write (x5 @ step 7), wrong trap cause (@ step 0), illegal-opcode substitution for a model limitation (SEM-02 — the limitation carried as the undefined case, the fabrication caught @ step 0), an extra memory access (the architectural trace still agrees; the pinned four-guest data-crossing census catches the phantom load), shifted event delivery (the missing trap @ its due step), an overbroad mask hiding a changed defined bit (bit 30 of SRAI/SRLI — srli executes as srai, x1 @ step 2), a stale reference configuration (the pc @ step 0) — plus the JALR odd-bit arm the `guest-control.expected.sexp` note names: the mutant faults with `InstructionAddressMisaligned` at 0x80000029, exactly the fault both references can never show. The comparison-suppression exhibit proves the writes leg is load-bearing: a writes-blind comparator agrees with a mutant the real comparator catches. Every guest arm re-derives the pinned GUEST-GEN expectations against the real model before judging the mutant.
- The `.1`–`.8` acceptance checklists archive verbatim to `docs/tasks/archive/P1-LAB.md` — the live file crossed its per-part ceiling; the ceiling was obeyed, not raised (the SOT-FORMAT precedent). The family aggregate (665,577 B > 640 KiB) is re-derived to 1 MiB per the documented precedent: lanes grew 25 → 32 since the 2026-09-20 derivation and the evidence archives are the designed growth — per-part stays 64 KiB and bit correctly (`docs/decisions/decision_task-tree-family-bound-rederivation.md`).
- Verification: 152 tests green across 5 suites (88 verify incl. 11 mutate arms; 25 core exec); clippy `-D warnings` clean; wasm build rc=0; `make gate` 23 doctrines green. Book P1's "Validating the validator" now describes the landed suite.
- Lockstep: MEMORY/LIVE_STATUS (P1 9/12)/TASK_TREE/CHANGELOG/DEV_NOTES + book P1 and this tree; frontier moves to `.10` (replay and reduction).


## SEMILITH-PL-0008 (leaf P1-LAB.8) — the first execution slice; the definition executes

- `semulith-core::exec` is the definitional interpreter: `step` fetches through the environment contract, decodes, extracts operands (scattered B/J immediates unscrambled; split fields bound per the semantics rule) and evaluates the generated `Sem` trees — the semantics DATA stays the one executable owner (OWN-01); there is no handwritten per-instruction behavior. The width algebra (`sext`/`zext` extend from the operand's own width; literal shifts widen; shifts operate at the operand's width, so `sraiw` replicates bit 31, not bit 63) is the unique reading under which all 52 trees are correct at once — LUI extends from bit 31, LB from 8 — now differentially validated, not assumed. 24 test suites cover every outcome family and every reporting point (misaligned target on the branch, fetch fault at the pc, misaligned access raised before the boundary, reserved decode carried as `UndefinedCase`, ECALL/EBREAK as requested traps).
- `semulith-verify` gains the observation layer: `run` records `(pc, word, register writes, trap)` steps — the same vocabulary `compare_traces.py` reduces the references to — plus the full boundary-crossing log, and `compare` reports the FIRST divergence with the differing field named (a register, the trap cause, the tval, a missing write; a length mismatch is a non-agreement, never a prefix pass). `elf` loads the writer's ELF64 with named-field refusals. `guests.rs` is GENERATED from the tracked guests and their specification-derived expectations (`scripts/gen_guests.py`); GUEST-GEN — the 23rd doctrine — refuses drift and fired RED on a hand-edited fixture before registration.
- `semulith-cli` gains `semulith run <elf>`. The offline differential (the GUEST-GEN fixture) re-runs all four guests against their EVD-05 expectations on every `make check` — 77 verify suites green. The live experiment `scripts/run_semulith_smoke.py` agrees with sail-riscv AND spike on every enabled comparison: 34 aligned steps across the four guests, byte-identical reproduction on re-run.
- Verification: 141 tests green across 5 suites; clippy `-D warnings` clean; wasm build rc=0; `make gate` 23 doctrines green; GUEST-GEN self-test 7/0. Book P1 gains "The first execution slice".
- Lockstep: MEMORY/LIVE_STATUS (P1 8/12, doctrines 23, arms 254)/TASK_TREE/TOOLBOX/DOCTRINE_ENFORCEMENT/doctrine/fact_ownership.tsv + book doctrines chapter and this tree; frontier moves to `.9` (validator mutation suite).

## SEMILITH-PL-0007 (leaf P1-LAB.7) — the graph and report checker; the citation becomes a derivation

- `semulith-verify` gains five dependency-free modules: `json` (a `json.loads`-parity reader), `pattern` (a regex subset refusing everything outside the census by name), `sha256` (FIPS 180-4, known-answer pinned), `schema` (the Python validator's keyword subset and refusal discipline, plus two verdict-neutral tightenings: array `type`, schema-valued `additionalProperties`), and `graph` (the `EVIDENCE_AND_GATES.md` §3 invariants over the frozen `examples/` bundle). The PACKAGE_CHECKS schema results are re-derived in Rust per RUST-01 — 5/5 records validate, 6/6 negative controls rejected with reasons named, the synthetic source fingerprint matches the ledger pin.
- Every designated rejection has a mutation suite that must catch it: orphan IDs, stale hashes, unsupported `passed` claims, missing evidence, deleted dependency links, out-of-scope profiles, duplicate ids, unpinned sources, undeclared checks, dependency cycles — plus the positive control (a fully met bundle gates `passed`). The intact fixture is graph-clean and honestly `incomplete` (`GateStatus` is a type, so "pass" has exactly one expression). The library is `std::fs`-free (evidence bytes arrive through a resolver), keeping the workspace wasm-buildable.
- `semulith check-examples` presents the report; `RECORD-SCHEMA` now runs the Rust engine after the Python phase on every commit and fired RED against a mutated requirement before landing. Verification: 59 verify suites green; `make check` clean; wasm green; gate green. Book P1 gains "The graph and report checker".
- Lockstep: MEMORY/LIVE_STATUS (P1 7/12)/TASK_TREE/DEV_NOTES/TOOLBOX/DOCTRINE_ENFORCEMENT + book doctrines chapter/check_requirements.sh and this tree; frontier moves to `.8` (first execution slice).

