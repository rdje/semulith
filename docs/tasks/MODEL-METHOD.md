# MODEL-METHOD: the method for modelling a unit, and the materials that method requires

## Metadata

- Tree ID: `MODEL-METHOD`
- Status: `active` (reopened `2026-09-29` for `.14` — the `MODEL-BOOKS.2` finding: the
  pinned specification's own PDF carries the instruction-format tables as selectable text,
  so the encodings' second provenance may be replaceable by the primary document; the
  evaluation is director-scheduled. `.15`+`.16` — the feed consumed, the v20260120 PDFs
  adopted — landed `2026-09-29`/`30` behind it; `.17` — the surfaced poller deafness came
  back FIXED and the channel two-way — `2026-09-30`)
- Roadmap lane: cross-cutting; precedes implementation for **every** modelled unit — CPU, MCU, DSP, device, board, SoC
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

## The layer boundary — what a CPU/DSP model is NOT

⛔ **Devices are not CPU material.** A UART, an interrupt controller, an interruptor, a DMA engine
or an interconnect belongs to a **board / SoC / ASIC** model, not to a processor model. This
project pipecleans by modelling **CPUs and DSPs first**, and the processor layer ends at the
CPU/environment boundary: the CPU states what it *assumes* of its environment, and a later board
model states what it *guarantees*.

The project's own contracts already own this line and are cited rather than restated:
`docs/INFORMATION_CATALOG.md` says plainly that *"C19–C21 are not all properties of the CPU
itself"*, and `docs/CPU_ENVIRONMENT.md` §5 defines the board composition gate — *for every CPU
assumption, identify the board/device guarantee satisfying it*. `P5-BOARD` is the tree that owns
the other side.

⭐ **The layer names the OWNER, not merely a deferral.** `C19 Platform, devices and interconnect`
is `deferred-to-board` for a CPU and `covered` for a board — the same category in the same
catalogue, answered by a different unit. That is why the catalogue is keyed on a **unit** rather
than on a processor profile: a board's census and a CPU's census are the same schema answered
differently, which is what makes adding the second unit cheap.

**And it is why the boundary is stated before the schema is written.** A category the processor layer does not own is **not `missing`**. Marking
`C19 Platform, devices and interconnect` as `missing` for a CPU model would manufacture an
acquisition task for material the model must never contain, and would make the census read as a
deficiency when it is a correct scope. The disposition vocabulary therefore carries a **layer**,
and `deferred-to-board` is a first-class answer distinct from both `missing` and `not-applicable`.

⚠️ It also corrects a framing in the previous leaf. "Capable of running real code" needs a console
and a program-exit convention — and **those are board concerns**. What the *processor* layer owes
real code is narrower and entirely within it: the psABI, the ELF contract, the entry/startup state,
and the compiler-runtime intrinsics a no-`M` soft-float target calls. The exit convention is an
assumption the CPU records and a board later satisfies.

## Acceptance Criteria

1. Every catalogue category has, per model, exactly one disposition: `covered` (naming the
   material and its locator), `missing` (naming what would close it), `deferred-to-board` (owned by
   a later board/SoC model, with the assumption the CPU records in its place), or
   `not-applicable` (with the reason). No category may be silently absent.
   ⛔ `deferred-to-board` and `missing` must never be conflated: one is a correct scope, the other
   is an acquisition task, and a census that merges them reports a healthy model as deficient.
2. The catalogue is machine-readable, schema-validated, and gated — a coverage claim is a query,
   not a sentence someone wrote.
3. The method is documented in prose, following at least one real rule end to end.
4. A gate prevents implementation beginning while a category the declared scope *needs* is
   `missing` — the director's rule, mechanized: no coding without the source of truth.
5. ⭐ **The catalogue covers what running REAL COMPILED CODE requires**, not only what executing
   instructions requires. `decision_dual-mandate-production-and-teaching` makes "capable of running
   real code (C, Rust)" a stated target, and that pulls in materials the ISA chapters do not own:
   the psABI, the ELF specification, a startup and runtime contract, the compiler-runtime
   intrinsics a no-`M` soft-float target will call, and a program-exit convention. Catalogue
   category `C20` is where they land, and it is currently supplied by nothing.

   Census behind that last clause, over every population that could refute it — the pinned
   specification artifacts, and any pinned material naming an ABI or ELF source:

   ```
   $ grep -oE '^id = "[^"]+"' profiles/rv64i-lab-v0/sources.toml
   RVI-INTRO   RVI-RV32I   RVI-RV64I          # three unprivileged ISA chapters, nothing else
   $ git grep -clE 'psABI|calling.convention|elf.specification' -- profiles/*/sources.toml profiles/*/references.toml | wc -l
   0
   $ grep -c 'software-convention' profiles/rv64i-lab-v0/state.json
   3                                          # the ISA chapters DISCLAIM the ABI; state.json says so
   ```

   The third number is the interesting one: the profile already records three register roles as
   `software-convention` precisely because the ISA chapter does not own them. Nothing yet pins the
   document that does.
6. Every material record states **what it teaches**, not only what it specifies — the catalogue is
   an input to a teaching text, and a material nobody can learn from is a citation.

## ⚡ The S-expression trigger has FIRED — see `decision_canonical-definition-input`

The trigger written below — *"the first time a material must carry a nested semantic expression
rather than a citation"* — fired on `2026-09-14`, when the canonical definition had to become the
input a generator engine reads. The answer: **a set of format-fit files**, with S-expressions for
`encoding.sexp` and `semantics.sexp` and the record files unchanged. The reasoning below stands
for the *materials catalogue*, which is still records; it is the semantics that needed trees.

## Format decision for the materials catalogue — and why not S-expressions there

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

_Leaves `.1`–`.13` (done `2026-09-27`) — the method, the census, the acquisitions, the coding
gate — live in [`archive/MODEL-METHOD.md`](archive/MODEL-METHOD.md), bodies unedited; the
Verification and Commit logs below index them. Moved `2026-09-29` when this file crossed its
per-part ceiling under `.16`; the ceiling was obeyed, not raised._

- ID: `MODEL-METHOD.16` — **the v20260120 PDFs: gap filed, answered the same day, adopted through the corpus seam**
  Status: `done`
  Origin (director, `2026-09-29`, three touches): "SEMULITH.md might contain a link to your
  missing files — check" → the corpus-wide sweep answered NO (exactly one
  `*20260120*`/`*unprivileged*` file in the whole corpus — the 20260911 intermediate; the
  pinned snapshot is 72 HTML pages). "Did you find the v20260120 unprivileged PDF?" → YES,
  in the untracked scratch `target/materials/` from `MODEL-BOOKS.2`'s investigation, digest
  EQUAL to the docs.riscv.org measurement. Then chipdoc's answer, relayed by the director:
  the corpus now MIRRORS both v20260120 PDFs deliberately
  (`risc-v/isa/reference/docs.riscv.org-v20260120/`, REQ-008 fulfilled), same bytes
  `06bb3c23…d150bc` — with a correction: the PDF does not share the pin's numbering.
  Goal: verify every leg of that answer, then the four durable acts: adopt both PDFs as
  catalogued materials through the corpus seam (reference-only, the trap documented); file
  AND resolve the catalogue gap the same day; retire the web-sourced stopgap before it ever
  commits; measure the channel the request travelled by.
  Verified (all four legs): (1) the mirror exists — both PDFs + README + SHA256SUMS; (2)
  byte-equality — chipdoc's unprivileged PDF hashes to `06bb3c23…d150bc`, identical to the
  independent docs.riscv.org fetch (two acquisitions, one set of bytes); (3) REQ-008 read in
  the ledger, the correction recorded there verbatim; (4) the numbering claim re-measured
  HERE from the extracted text layer — "Chapter 2. RV32I Base Integer Instruction Set,
  Version 2.1" / "Chapter 4. RV64I …" — the pinned HTML's §1.1 / §3.1 it is NOT. chipdoc's
  correction is correct, and it sharpens `.14`'s already-recorded qualification (a locator
  mapping is required) into exact chapters: three renderings, three numberings, all measured
  (HTML §1.1/§3.1 · this PDF ch.2/ch.4 · GitHub §2/§4).
  Measured (the channel): `poll_semulith_gaps.py --semulith-root . --json` reports
  `semulith_gaps_open: 0` against the real catalogue — its gap scan reads only TOP-LEVEL
  `(gap …)` forms, and this catalogue nests its gaps inside the single `(materials …)` form
  (scratch probe, since removed: a flat gap is seen, a nested one is not). The polled route
  is deaf to this catalogue's gaps TODAY; this request travelled operator-relayed and was
  fulfilled anyway, and the deafness is surfaced for a chipdoc-side fix (chipdoc stays
  read-only from here).
  ⭐ The `.4` URL-kind trigger fired and UNFIRED in one day: the "second web-sourced family"
  (`.materials/web-sourced/`) existed for hours, then the corpus absorbed the artifact and
  the stopgap was retired uncommitted — the corpus seam owns the bytes, and the URL-kind
  mechanization returns to "named candidate, no second family".
  Acceptance: both materials fetch through the seam with digests verified (the unprivileged
  EQUAL to the web-fetched copy — measured at fetch); the gap record carries
  `(status resolved)` with its evidence; the corpus re-pin (`73711d6` → `f33d330`) clears
  the drift warning; the catalogue parses and loads; the gate stays green.
  Not this leaf: starting `.14` (director-scheduled; its adopt/decline evaluation inherits
  the three measured numberings); any write to chipdoc.

  Result: met, `2026-09-30` (measurements of `2026-09-29`). `RVI-UNPRIV-PDF-V20260120`
  (696 pp) and `RVI-PRIV-PDF-V20260120` (214 pp) catalogued reference-only and cached
  through the corpus seam, digests verified at fetch; the unprivileged copy is
  byte-identical to the independent web fetch — the corroboration pair is recorded in the
  material's note. `GAP-RISCV-V20260120-UNPRIV-PDF` filed and resolved the same day
  (REQ-008). Corpus re-pinned `73711d6` → `f33d330` (5313 files / 257 PDFs re-derived);
  45 materials. `.semulith-data/chipdoc/` snapshot refreshed. Mid-leaf the per-part
  ceiling fired twice (67,737 B, then 65,032 B growing): answered by the second and third
  archive movements, never raised. `promotion: declined (the poller finding lives in the
  gap record itself, where the next surveyor meets it; the numbering trap lives in the
  material notes).`

- ID: `MODEL-METHOD.15` — **the chipdoc feed arrives: the flagged set, catalogued and cached**
  Status: `active`
  Origin (director, `2026-09-29`): the corpus root was supplied verbally and the instruction
  given: save what semulith needs from chipdoc into a git-ignored local cache, so the corpus
  path never has to be requested again. The feed the director flagged on `2026-09-27`
  (`SEMULITH.md` → `catalog/semulith-proposals.sexp`, `(material …)` records in this
  catalogue's own syntax) is the consumption channel; this leaf is the catalogue slice that
  consumes it.
  Goal: adopt the materials the current and next milestones need into `materials/catalog.sexp`,
  fetch them into the git-ignored `.materials/` cache digest-verified, snapshot the channel
  itself (the feed, the map, the requests ledger) into a git-ignored `.semulith-data/chipdoc/`,
  and re-pin the corpus revision (`3c45e81` → `73711d6`).
  The adopted set — the director's `2026-09-27` flag (psABI, SBI, BRS, U-Boot, DT, FU540,
  virtio, ACT), psABI already catalogued and cached: `RISCV-ARCH-TEST-ACT4` (the
  `P2-SCALAR.5` blocker-(a) material), `RISCV-SBI-2.0`, `RISCV-BRS-1.0`, `DT-SPEC-0.4`,
  `SIFIVE-FU540-C000`, `VIRTIO-1.2`, `UBOOT-2026.07` — the P4/P5/P6 inputs.
  Acceptance: every adopted row verifies its digest at fetch (the fetcher's refusal-on-mismatch
  is the control); `materials.py --verify` resolves every catalogued material; the re-pin
  clears the drift warning with the variable set; the channel snapshot holds the feed, the map
  and the ledger, with the corpus location recorded in an UNTRACKED readme (Policy 12 — no
  tracked file names it); the gate stays green.
  Not this leaf: resuming `P2-SCALAR.5` (blocker (b) — the C-guest routing decision and the
  absent RISC-V C toolchain — stands); the generated ACT suite (635 MB of `.S`, pinned by
  upstream commit `e2216915…`, fetched when `.5` resumes — the snapshot is docs + test plans
  by design); the `.14` probe PDF (probed: chipdoc's pinned snapshot carries 72 HTML pages and
  no PDF — the v20260120 unprivileged PDF is not in the corpus).

  Result: met, `2026-09-29`. 43 materials (was 36); the corpus re-pinned `3c45e81` →
  `73711d6` (5309 files / 255 PDFs at the new pin, re-derived by the same path sweep). Every
  adopted digest verified AT FETCH — 7 of 7 ok, both snapshots manifest-verified (ACT4
  136/136, U-Boot 1219/1219) — and `materials.py --verify` resolves 43/43 with zero drift
  warnings. The channel snapshot stands at `.semulith-data/chipdoc/` (git-ignored; the
  corpus location lives only in its untracked README, Policy 12 honoured). psABI's SRC-02
  follow-up is discharged: the corpus copy (`RVI-PSABI-1.0` PDF) was already catalogued and
  cached since `.11`, beside the `.4` canonical HTML render — both forms on disk, the corpus
  copy preferred as instructed. `P2-SCALAR.5` blocker (a) is answered at the materials layer
  (the generated suite stays pinned by upstream commit for resume day); blocker (b) stands.
  `promotion: declined (the one in-flight correction — a feed census typed from recall as
  60/10, measured 67/11 — is the CLAIM_VERIFICATION discipline biting on a one-line claim;
  the rule already lives in docs/CLAIM_VERIFICATION.md).`

- ID: `MODEL-METHOD.14` — **evaluate re-sourcing the encodings from the primary-document PDF**
  Status: `pending` (surfaced `2026-09-29`; SCHEDULED `2026-09-30` — the director delegated
  the scheduling call alongside the `P2-SCALAR.5` rulings; it starts after `P2-SCALAR.5`'s
  strands, the milestone tree holding PNT precedence, or any session the director names it)
  Origin (measured, `MODEL-BOOKS.2`, `2026-09-29`): the pinned unprivileged specification's
  own PDF rendering (`docs.riscv.org` `v20260120`, `_attachments/riscv-unprivileged.pdf`,
  4,580,174 B, sha256 `06bb3c23…d150bc`, 696 pages) carries the instruction-format tables as
  SELECTABLE TEXT — `pdftotext` census `[01]{7}` → 232 lines, vs 0 across all six pinned HTML
  artifacts (`grep -cE '[01]{7}' target/sources/riscv-v20260120/{intro,rv32,rv64}.{html,txt}`).
  The base-formats figure (`imm[31:12]`/`rd`/`opcode`/`U-Type`) and the RV32I opcode map
  (Table 13) extract with bit strings and field names. Today the encodings come from
  RISCV-OPCODES — a second provenance whose ancestry is shared with spike, not sail
  (`docs/models/rv64i-lab-v0/src/gaps.md`, `references.md`); re-sourcing from the primary
  document shrinks that exposure.
  Goal: decide, by measurement, whether `encoding.sexp` (owned by `.8`) can be re-derived from
  the primary document's PDF text layer. Probe one form end to end (extract → parse → compare
  against the current riscv-opcodes-derived entry), estimate the full sweep's cost and
  verifiability, then record adopt/decline as a decision. Two measured qualifications the probe
  must handle: the PDF numbers chapters differently from the pinned HTML (a recorded locator
  mapping is required), and extraction is layout-fragmented (one field per line — parsing is
  engineering with its own verification, not a copy-paste).
  Acceptance: the probe's commands and outputs are recorded either way; if adopt, the re-source
  is its own reviewed leaf with the encoding provenance restated in the dossier and the
  materials bill; if decline, the reason is measured, not assumed.
  Not this leaf: changing any encoding data. This leaf is the evaluation only.

- ID: `MODEL-METHOD.17` — **the channel answers: the poller fix heard the nested gaps, and the records reconcile**
  Status: `active`
  Origin (chipdoc, relayed by the director, `2026-09-30`): the poller deafness `.16` measured
  and surfaced is FIXED chipdoc-side (corpus `6bfabf2` — "Fix poller deafness to semulith
  catalogue; mirror satisfied gaps; correct REQ-008 date"): the poller descends into the
  `(materials …)` wrapper and now READS this catalogue's nested gaps. It found the two
  status-less records — `GAP-INTEL-SDM-VOL1` and `GAP-RISCV-JAN-2026-PDF` — both already
  satisfied on chipdoc's side (SDM Vol 1 held; the January GitHub PDFs declined as pin
  substitutes), so chipdoc mirrored them as resolved and reports none unmirrored. REQ-008's
  ledger entry now carries the true fulfilment date `2026-09-29`. The consequence chipdoc
  flags: **the channel is now two-way** — a genuinely new gap filed in this catalogue
  surfaces there without an operator relay.
  Goal: make both sides read true. Verify the fix by measurement here (the same probe `.16`
  ran, now reading the nested records — the discrimination `.16`'s scratch probe had to
  synthesize); reconcile the two gap records so the catalogue states what is already true
  (one closed by a catalogued material in `.13`, one closed by a recorded decision at filing
  in `.12`); update the gap record that carries the deafness claim so a live catalogue does
  not assert a dead channel; re-pin the corpus (`f33d330` → `92a73b6`) with the counts
  re-derived by the same path sweep; refresh the untracked channel snapshot.
  Acceptance: the fixed poller, run here against the real catalogue, reports the nested gaps
  are READ (a nonzero open count pre-reconcile — the signal `.16` could not get); after the
  reconcile it reports 0 open and 0 unmirrored; both reconciled records carry
  `(status resolved)` with their evidence; the re-pin's file/PDF counts are re-derived, not
  carried; `materials.py --verify` and the RECORD-SCHEMA gate stay green; the snapshot holds
  the post-fix ledger (REQ-008 at `2026-09-29`).
  Not this leaf: starting `.14` (director-scheduled); filing any new gap (none is open to
  file — the feed's own proposals census is unchanged); any write to chipdoc.
  Result: met, `2026-09-30`. The fixed poller, run here against the real catalogue, reported
  `semulith_gaps_open: 2` pre-reconcile — the nested records are READ (pre-fix the same probe
  said 0, and `.16` needed a scratch probe to prove the deafness discriminated at all; the
  channel now exhibits the discrimination itself). Both heard records reconciled:
  `GAP-INTEL-SDM-VOL1` → resolved `2026-09-14` by `X86-SDM-VOL1-253665` (catalogued `.13`);
  `GAP-RISCV-JAN-2026-PDF` → resolved `2026-09-14` by the decision recorded at filing
  (`.12`). Post-reconcile: 0 open, 0 unmirrored, rc 0. The deafness claim in
  `GAP-RISCV-V20260120-UNPRIV-PDF` now records the fix (corpus `6bfabf2`). Corpus re-pinned
  `f33d330` → `92a73b6` — 5313 files / 257 PDFs re-derived by the same working-tree path
  sweep, unchanged (the two-commit delta touches scripts and channel files, no documents);
  the sweep reproduced the recorded `f33d330` figure exactly before it was trusted for the
  new pin. Snapshot refreshed (feed 68 materials / 14 gaps at the new pin; the delta is
  exactly chipdoc's two resolved-gap mirror records; REQ-008 carries `2026-09-29`).
  RECORD-SCHEMA green; `materials.py` 45 verified / 0 unresolved, self-test 20/0.
  `promotion: declined (the two-way channel is recorded where the next surveyor meets it — the catalogue's own gap records and MEMORY.md's resume pointer).`

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `MODEL-METHOD.14` | `pending` | the `.2` PDF finding made the encodings' second provenance potentially replaceable by the primary document; SCHEDULED `2026-09-30` by the same delegation that unblocked `P2-SCALAR.5` — starts after `.5`'s strands (milestone precedence), with `.16`'s probe input as a first-class material plus the three measured numberings |
| — | — | — | `.17` done `2026-09-30` (the poller fix measured, the gaps reconciled, corpus `92a73b6`); `.15`+`.16` done `2026-09-29`/`30` (the feed consumed; the v20260120 PDFs adopted); `.1`–`.13` done `2026-09-27`, bodies archived |

## Decisions

- `2026-09-14`: the catalogue is **JSON Lines against a JSON Schema**, not S-expressions — see the
  format section above, including the trigger that would re-open it.
- `2026-09-14`: the canonical definition is a **set of format-fit files**, not one file, and
  "single source of truth" is preserved by a no-duplicated-fact rule. S-expressions for encodings
  and semantics; records stay JSON/TOML because they are records and are already gated. See
  [`decision_canonical-definition-input`](../decisions/decision_canonical-definition-input.md).
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

## Completed-leaf evidence

Archived to [`archive/MODEL-METHOD.md`](archive/MODEL-METHOD.md) — the full, unedited
acceptance checklists and routing evidence for every `done` leaf (`.2`–`.7`, `.10`, `.13`).
Split out twice, each time this file crossed its per-part ceiling (`2026-09-27` at 73,867
bytes; `2026-09-29` at 67,737 under `.15`/`.16`); the ceiling was obeyed, not raised. The
live tree keeps the frontier, the decisions, the open questions and both logs.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-30` | `MODEL-METHOD.17` | the fixed poller against the real catalogue, pre-reconcile | `semulith_gaps_open: 2`, `unmirrored: []` — the nested records are READ (pre-fix: 0, and a scratch probe was needed to discriminate at all) |
| `2026-09-30` | `MODEL-METHOD.17` | the same probe, post-reconcile | `semulith_gaps_open: 0`, `unmirrored: []`, rc 0 — both sides read true |
| `2026-09-30` | `MODEL-METHOD.17` | corpus re-derivation at the re-pin | 5313 files / 257 PDFs at `92a73b6` (working-tree path sweep) — identical to the recorded `f33d330` figure the sweep first reproduced; git delta `f33d330..92a73b6`: 6 files, no documents |
| `2026-09-30` | `MODEL-METHOD.17` | feed census at the new pin (corpus diff, not recall) | 68 materials / 14 gaps; the `f33d330..92a73b6` delta is exactly chipdoc's two resolved-gap mirror records (`GAP-INTEL-SDM-VOL1`, `GAP-RISCV-JAN-2026-PDF`) |
| `2026-09-30` | `MODEL-METHOD.17` | `materials.py --verify` + RECORD-SCHEMA + self-test | 45 verified / 0 unresolved / 0 drift; gate ok (7 record files); self-test 20 pass / 0 fail |
| `2026-09-30` | `MODEL-METHOD.17` | the whole gate | all doctrines green |
| `2026-09-29` | `MODEL-METHOD.16` | corpus-wide sweep for the PDF (`find -iname '*20260120*' -o -iname '*unprivileged*'`) | exactly one hit — the 20260911 intermediate; the pinned snapshot holds 72 HTML pages and no PDF |
| `2026-09-29` | `MODEL-METHOD.16` | scratch bytes vs the `MODEL-BOOKS.2` measurement | sha256 EQUAL (`06bb3c23…d150bc`, 4,580,174 B) — the .14 probe input survived in scratch, verified |
| `2026-09-29` | `MODEL-METHOD.16` | the polled channel (`poll_semulith_gaps.py --json`, real catalogue + scratch probe) | `semulith_gaps_open: 0` — top-level scan only; a flat gap is seen, a nested one is not |
| `2026-09-29` | `MODEL-METHOD.16` | chipdoc's answer, four legs | mirror present; byte-equality `06bb3c23…d150bc`; REQ-008 read with the correction verbatim; numbering re-measured from the text layer (ch.2/ch.4 vs §1.1/§3.1) — correction CORRECT |
| `2026-09-29` | `MODEL-METHOD.16` | `--fetch` of both adopted PDFs | 2 of 2 ok, sha256 verified; the unprivileged EQUAL to the independent web fetch — two acquisitions, one set of bytes |
| `2026-09-29` | `MODEL-METHOD.16` | the per-part ceiling fires twice mid-leaf | 67,737 B → second split; 65,032 B growing → third movement (done-leaf bodies `.1`–`.13` archived); the ceiling obeyed, never raised |
| `2026-09-30` | `MODEL-METHOD.16` | catalogue parse + load + drift | parses; 45 materials; `--list` with the variable set reports no drift at `f33d330` |
| `2026-09-30` | `MODEL-METHOD.16` | the whole gate | all doctrines green |
| `2026-09-29` | `MODEL-METHOD.15` | feed census (grep, not recall) | 67 `(material …)` + 11 `(gap …)` proposals at `73711d6`; 7 adopted — the director's flagged set minus the already-catalogued psABI |
| `2026-09-29` | `MODEL-METHOD.15` | corpus re-derivation at the re-pin | 5309 files / 255 PDFs (was 3684 / 196 at `3c45e81`), same path sweep |
| `2026-09-29` | `MODEL-METHOD.15` | `--fetch` of the 7 adopted ids | 7 of 7 ok, every sha256 verified at copy; ACT4 manifest 136/136, U-Boot 1219/1219 |
| `2026-09-29` | `MODEL-METHOD.15` | `materials.py --verify` + `--self-test` | 43 verified / 0 unresolved / 0 drift; self-test 20 pass / 0 fail |
| `2026-09-29` | `MODEL-METHOD.15` | the `.14` probe input in the corpus | ABSENT — the pinned snapshot holds 72 HTML pages and no PDF (`find -iname '*.pdf'` empty); the `.4` release-asset PDF stays the probe's input |
| `2026-09-29` | `MODEL-METHOD.15` | the whole gate after staging | all doctrines green |
| `2026-09-27` | `MODEL-METHOD.6` | `--self-test` | `7 pass / 0 fail` — MISSING REQUIRED, UNCOVERED REQUIRED, UNDECLARED SCOPE, NO CENSUS, both GREEN arms, empty-corpus refusal |
| `2026-09-27` | `MODEL-METHOD.6` | RED before registration (scratch unit, required category missing) | `MISSING REQUIRED [ghost requires C02]` |
| `2026-09-27` | `MODEL-METHOD.6` | real run | `ok (1 unit(s) may code)` — rv64i-lab-v0 declares 14 required categories, all covered |
| `2026-09-27` | `MODEL-METHOD.5` | census, pre-code | no method document anywhere in `docs/` |
| `2026-09-27` | `MODEL-METHOD.5` | the acceptance probes | the SHAMT walk present; 4 non-mechanical steps named; book builds; no project-only dependency outside the worked example |
| `2026-09-27` | `MODEL-METHOD.4` | network probes | psABI gh-pages: no PDF (HTML canonical render); ELF gABI: HTTP 200; isa-manual releases carry `riscv-spec.pdf` assets |
| `2026-09-27` | `MODEL-METHOD.4` | the four acquisitions fetched, digested, cached | digests and byte counts in the leaf table; re-hash of the cached copies matches |
| `2026-09-27` | `MODEL-METHOD.4` | content sanity | psABI mentions RISC-V 85×; `__NR_exit` present in the syscall header; `__muldi3 (di_int a, di_int b); // a * b` in the builtins inventory; `%PDF-1.1` magic on the ELF spec |
| `2026-09-27` | `MODEL-METHOD.4` | the PDF question | **YES** — `pdftotext` extracts 1.96 MB of text; the RV32I format-table region yields `funct7 / rs2 / rs1 / funct3` as clean cells |
| `2026-09-27` | `MODEL-METHOD.4` | SRC-02 records | pinned-revision release PDF not located (3 release pages searched); chipdoc route unavailable (`$SEMULITH_CHIPDOC_ROOT` unset); startup contract owned by the harness contract already |
| `2026-09-27` | `MODEL-METHOD.3` | census sweep against the cached snapshot | all 8 covered categories' subjects found in the pinned pages; the excluded chapters (a/d/f/q/v-st-ext, rvwmo, counters, zicsr, zifencei) present in the same snapshot |
| `2026-09-27` | `MODEL-METHOD.3` | revised census | 24 rows: 10 covered, 4 partial, 6 missing (each naming its closer), 3 deferred-to-board, 1 out-of-scope |
| `2026-09-27` | `MODEL-METHOD.3` | RECORD-SCHEMA rule 12 + arm | `33 pass / 0 fail` (was 32); UNRESOLVED MATERIAL fired RED pre-registration |
| `2026-09-27` | `MODEL-METHOD.2` | `--self-test` | `32 pass / 0 fail` (was 26; NO REGISTRY, LAYER LIE, REASONLESS MISSING, UNEVIDENCED COVERED, EMPTY REGISTRY, GREEN census) |
| `2026-09-27` | `MODEL-METHOD.2` | real run | `ok (7 record file(s))` — the 24-row first honest pass green |
| `2026-09-27` | `MODEL-METHOD.2` | schema validation | both new catalogues `conform` under the two new schemas |
| `2026-09-27` | `MODEL-METHOD.7` | mirror inventory, pre-code | 3 pairs governed (decision<->requirement, state<->profile, composition<->fragments); obligation->requirement UNGOVERNED — 28 restatements, all matching, nothing refusing drift |
| `2026-09-27` | `MODEL-METHOD.7` | RECORD-SCHEMA rule 9 + arms | `26 pass / 0 fail` (was 23); MIRROR DRIFT / MIRROR WITHOUT SOURCE / GREEN mirror |
| `2026-09-27` | `MODEL-METHOD.7` | gate `--self-test` | `8 pass / 0 fail`; real run `ok (8 fact kind(s))` |
| `2026-09-27` | `MODEL-METHOD.7` | the acceptance's shapes fired | UNGOVERNED MIRROR and UNREGISTERED MIRROR PAIR, both rc=1 |
| `2026-09-27` | `MODEL-METHOD.10` | contract as stated, run pre-code | requirement leg FAILS: no `insns` link; ALU family (13 instructions) uncovered |
| `2026-09-27` | `MODEL-METHOD.10` | tool `--self-test` | `6 pass / 0 fail`; gate `--self-test` `3 pass / 0 fail` |
| `2026-09-27` | `MODEL-METHOD.10` | real corpus | `SUFFICIENT for an engine: 52 instructions, each with encoding + semantics + requirement` |
| `2026-09-27` | `MODEL-METHOD.10` | the acceptance's RED (real-corpus copy, one sem rule removed) | `does not cover: add`, rc=1 |
| `2026-09-27` | `MODEL-METHOD.10` | gates on the extended catalogue | RECORD-SCHEMA 23/0 + green (caught a wrong obligation id, fixed); PROFILE-CONSISTENCY 39/0 + green; GATE-REPORT re-derived 28/28/36/72 |
| `2026-09-14` | `MODEL-METHOD.11` | corpus survey: files, PDFs, vendors | 3,684 files / 1.5 GB / 196 PDFs across 23 vendors |
| `2026-09-14` | `MODEL-METHOD.11` | `materials.py --self-test` | `15 pass / 0 fail`; 9 RED arms about paths |
| `2026-09-14` | `MODEL-METHOD.11` | `materials.py --fetch` (22 materials) | 22 of 22, every sha256 verified, 233 MB |
| `2026-09-14` | `MODEL-METHOD.11` | Policy 12: corpus root in any tracked file | `0` files; control confirms the probe can see one |
| `2026-09-14` | `MODEL-METHOD.11` | Policy 13: cache volume vs repo volume | both `/dev/disk7s1` |
| `2026-09-14` | `MODEL-METHOD.11` | is the RISC-V PDF the artifact the profile pins? | NO — `20260911 Intermediate` vs pinned `v20260120` |
| `2026-09-14` | `MODEL-METHOD.11` | do our 52 citations resolve in that PDF? | NO — it numbers RV32I §2.1 / RV64I §2.2; we cite §1.1 / §3.1 |
| `2026-09-14` | `MODEL-METHOD.11` | RISC-V ISA manual licence, read from the document | CC-BY-4.0 — bears on `OQ-4` / rule `SRC-01` |
| `2026-09-14` | `MODEL-METHOD.11` | gap probe: AMD64 ISA manual | absent; `amd/` holds one IOMMU spec |
| `2026-09-14` | `MODEL-METHOD.11` | gap probe: Intel SDM Volume 1 | absent; Vols 2/3/4 present |
| `2026-09-14` | `MODEL-METHOD.11` | regression: sexp, semantics, smoke, doctrines | 18/0, 52 of 52, ok, all green |
| `2026-09-14` | `MODEL-METHOD.12` | pinned artifacts on disk vs committed digests | 3 of 3 MATCH, byte-identical |
| `2026-09-14` | `MODEL-METHOD.12` | pinned URLs re-fetched live | HTTP 200 ×3, identical to the pinned copies |
| `2026-09-14` | `MODEL-METHOD.12` | headings published by the pinned rv64.html | `3.1`, `3.1.1`, `3.1.2`, `3.1.2.1`, `3.1.2.2`, `3.1.3`, `3.1.4` |
| `2026-09-14` | `MODEL-METHOD.12` | `check_citations.py` on the real profile | **52 of 52** resolve — the challenge is refuted |
| `2026-09-14` | `MODEL-METHOD.12` | `check_citations.py --self-test` | `10 pass / 0 fail` |
| `2026-09-14` | `MODEL-METHOD.12` | control: working area removed | REFUSED with the fetch command, `exit=1` — no silent pass |
| `2026-09-14` | `MODEL-METHOD.12` | licence of the docs.riscv.org rendering | only `Copyright © RISC-V International®` — no CC-BY; `OQ-4` stays open |
| `2026-09-14` | `MODEL-METHOD.13` | corpus commits since the catalogued revision | 3 (`4201f50` → `3c45e81`), 88 files, +345,967 lines |
| `2026-09-14` | `MODEL-METHOD.13` | `--fetch` of the moved RISC-V PDF, before the fix | REFUSED — a tracked record was false |
| `2026-09-14` | `MODEL-METHOD.13` | path sweep vs the sampled first survey | 8 documents missed, incl. all of M68000 and every board document |
| `2026-09-14` | `MODEL-METHOD.13` | chipdoc's snapshot digests vs this project's `sources.toml` | `intro`/`rv32`/`rv64` all EQUAL — independent acquisition |
| `2026-09-14` | `MODEL-METHOD.13` | `SHA256SUMS` of the pinned snapshot | 72 OK / 0 FAILED |
| `2026-09-14` | `MODEL-METHOD.13` | `materials.py --self-test` after snapshot support | `20 pass / 0 fail` (was 15) |
| `2026-09-14` | `MODEL-METHOD.13` | `materials.py --fetch` (36 materials) | 36 of 36, digests verified, 72 manifest entries |
| `2026-09-14` | `MODEL-METHOD.13` | `check_citations.py` with the working area removed | 52 of 52 **offline**, via the manifest-verified cache |
| `2026-09-14` | `MODEL-METHOD.13` | the reader on this leaf's own first draft | REFUSED: `unknown escape '\u'` — content fixed, reader untouched |
| `2026-09-14` | `MODEL-METHOD.1` | sweep over every pinned configuration scalar | 1 further instance found: Spike's ISA was an input, not a read-back |
| `2026-09-14` | `MODEL-METHOD.1` | Spike ISA read-back, with its control | `rv64i` → `rv64i`; `rv64im` → `rv64im` |
| `2026-09-14` | `MODEL-METHOD.1` | `compare_platforms.py` on both matched models | 4 of 4 fields disagree; 4 devices only Spike advertises |
| `2026-09-14` | `MODEL-METHOD.1` | rule 5b fired RED on the real dossier | `UNSCOPED SCALAR …/spike` |
| `2026-09-14` | `MODEL-METHOD.1` | `check_profile_consistency.sh --self-test` | `39 pass / 0 fail`; 39 written, 39 run |
| `2026-09-14` | `MODEL-METHOD.8` | census: encodings owned by the repo, semantics present | `0` and `0` — both absent |
| `2026-09-14` | `MODEL-METHOD.8` | the whole evidence path with the upstream MOVED ASIDE | `run_smoke: ok` — 4 guests, 2 models, reproduced |
| `2026-09-14` | `MODEL-METHOD.8` | re-derivation fired RED on a one-bit `funct3` edit | `DIFFERS … no longer matches what the pinned tables generate` |
| `2026-09-14` | `MODEL-METHOD.8` | S-expression reader controls | 7 pass / 0 fail, incl. `;` inside a string and a string spanning lines |
| `2026-09-14` | `MODEL-METHOD.8` | `fetch_references.sh --verify-only` | 12 of 12 `MATCH` |
| `2026-09-14` | `MODEL-METHOD.9` | census: machine-executable semantics before this leaf | `0` files; 26 rules, all prose |
| `2026-09-14` | `MODEL-METHOD.9` | `check_semantics.py` on the real fragment | `52 of 52 declared instruction(s) have checked semantics` |
| `2026-09-14` | `MODEL-METHOD.9` | 4 controls: missing, unknown form, bad operand, no source | each refused by name; all restored |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `MODEL-METHOD.17` | `SEMULITH-MM-0059 (leaf MODEL-METHOD.17): the channel answers — the poller fix measured, the heard gaps reconciled` | corpus `92a73b6`; the channel is two-way; 45 materials unchanged |
| `MODEL-METHOD.16` | `SEMULITH-MM-0058 (leaf MODEL-METHOD.16): the v20260120 PDFs — gap filed, answered same-day, adopted through the corpus seam` | REQ-008 verified four legs; 45 materials; corpus `f33d330`; the poller deafness surfaced |
| `MODEL-METHOD.15` | `SEMULITH-MM-0057 (leaf MODEL-METHOD.15): the chipdoc feed arrives — the flagged set, catalogued and cached` | corpus re-pinned `73711d6`; 43 materials; `P2-SCALAR.5` blocker (a) answered |
| `MODEL-METHOD.6` | `SEMILITH-MM-0050 (leaf MODEL-METHOD.6): …` | no coding without the source of truth, mechanized; the tree closes 13/13 |
| `MODEL-METHOD.5` | `SEMILITH-MM-0049 (leaf MODEL-METHOD.5): …` | the method, in prose, written to be learned from |
| `MODEL-METHOD.4` | `SEMILITH-MM-0048 (leaf MODEL-METHOD.4): …` | the run-real-code set acquired and digest-pinned; the PDF question answered YES |
| `MODEL-METHOD.3` | `SEMILITH-MM-0047 (leaf MODEL-METHOD.3): …` | the census swept the snapshot; missing now means excluded, with closers named |
| `MODEL-METHOD.2` | `SEMILITH-MM-0046 (leaf MODEL-METHOD.2): …` | the materials requirement: two record families, the unit registry, the 24-category first pass |
| `MODEL-METHOD.7` | `SEMILITH-MM-0045 (leaf MODEL-METHOD.7): …` | the no-duplicated-fact registry and its gate; the obligation mirror governed |
| `MODEL-METHOD.10` | `SEMILITH-MM-0044 (leaf MODEL-METHOD.10): …` | the extraction contract: one set four ways, and P1's start condition fully met |
| `MODEL-METHOD.13` | `SEMULITH-MM-0044 (leaf MODEL-METHOD.13): the corpus moved, and my survey had sampled` | 36 materials; both gaps closed; citations resolve offline |
| `MODEL-METHOD.12` | `SEMULITH-MM-0043 (leaf MODEL-METHOD.12): a citation that is present is not a citation that resolves` | challenge refuted; 52 of 52 resolve |
| `MODEL-METHOD.11` | `SEMULITH-MM-0042 (leaf MODEL-METHOD.11): materials get an identity, and no path that breaks on a move` | 22 materials, 2 measured gaps, 0 absolute paths |
| `MODEL-METHOD.9` | `SEMULITH-MM-0040 (leaf MODEL-METHOD.9): the semantics, 52 of 52, every rule cited` | well-formed and cited — NOT verified correct |
| `MODEL-METHOD.8` | `SEMULITH-MM-0037 (leaf MODEL-METHOD.8): the repository owns its encodings` | builds with the upstream hidden; re-derivation fired RED |
| `MODEL-METHOD.1` | `SEMULITH-MM-0033 (leaf MODEL-METHOD.1): answer the narrower-instrument sweep with a wider instrument` | 1 further instance found and fixed; the pattern gated |

## Changelog

- `2026-09-30`: `MODEL-METHOD.17` — chipdoc fixed the poller deafness `.16` surfaced (corpus
  `6bfabf2`); the fix measured here (the nested gap records are read: `semulith_gaps_open: 2`
  pre-reconcile — the signal `.16` could not get), the two heard records reconciled to
  `(status resolved)` with their evidence, the deafness claim in the v20260120 gap updated to
  the fixed channel, corpus re-pinned `92a73b6` (5313/257 re-derived, unchanged), the channel
  snapshot refreshed. **The channel is now two-way** — a gap filed in the catalogue surfaces
  to chipdoc without an operator relay.

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
