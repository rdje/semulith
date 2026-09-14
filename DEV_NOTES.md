# DEV_NOTES.md

Detailed technical notes — root cause, implementation, validation — per slice. The
engineering-continuity surface (not the public docs; that's `docs/book/`). Newest first.

Every dated entry here must reach the retrievable layer: a card under
[`docs/knowledge/`](docs/knowledge/INDEX.md), or a decision record, or an explicit decline in
the owning task leaf. That is the `LESSON-PROMOTION` doctrine, and the reason for it is that a
lesson nobody can retrieve by question is a lesson nobody has.

## _(2026-09-14)_ — explicit widths, and never regenerate over hand-derived work

- 52 of 52 RV64I instructions now have machine-checkable semantics, each citing the locator it came
  from. Before: 26 rules, all English prose, none executable.
- ⭐ **Widths are always explicit.** `(sext 64 (trunc 32 …))` says what it means; an implicit width
  is exactly where two models silently disagree, and `D-WSUFFIX` is one line once it is spelled.
- ⛔ **Generated and authored content must not share a file.** `rv64i.sexp` is regenerated whenever
  its upstream table moves; hand-derived semantics in the same file would be destroyed by a
  routine regeneration. Different provenance, different file — a rule worth carrying to any
  project that generates part of its source of truth.
- The language is 32 forms, each added because an instruction needed it, and the checker refuses
  the rest. A notation that quietly accepts an unknown operator produces a definition whose
  meaning nobody can state — worse than none, because it looks like one.
- ⚠️ `52 of 52` = well-formed, complete, cited. NOT correct. That distinction has to survive into
  the book, because the number invites the stronger reading.
- Promotion is explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — a refactor of the source of truth must not move the evidence

- The unit carried 52 instructions inside itself; a base ISA is shared by every profile that
  composes it. Split into `definitions/riscv/{rv64i,m}.sexp`, and the unit now NAMES what it
  composes and owns nothing. Census: instructions in the unit 52 → 0; in `definitions/` 0 → 65.
- ⭐ **The acceptance test was that nothing observable moved**: all four guest ELF digests are
  byte-identical after the split, across two models. A source-of-truth refactor that perturbs the
  evidence has changed the model, whatever the author intended.
- A fragment DECLARES its dependencies; composing the M extension without its base is refused. A
  fragment with a hidden dependency composes by luck, not by construction.
- `definitions/` was registered in the routes registry in the same commit that created it. A new
  tracked family nothing governs is how pressure escapes — measured once already in this project.
- 🔎 Three references to the old generator name survive in CHANGELOG and a completed checklist.
  Left alone: historical records are true as written, and `append_history` exists to stop exactly
  that tidying.
- Promotion is explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — breadth by composing proven parts, not by gating them less

- ⛔ **I proposed the wrong lever and it was rejected.** Facing "model as much as possible" against
  "signoff-grade", I suggested tiering models into `exploratory` (ungated) and `accepted` (gated).
  That buys breadth by creating a second class of model nobody can trust, and the classes would
  blur the first time one cited the other. The right lever is **composition**: assemble proven
  small models. Breadth by reuse of evidence, never by absence of it.
- Grounded rather than invented: both pinned references already compose from fragments —
  riscv-opcodes 111 extension files, sail-riscv 34 extension dirs / 59 encoding files — and this
  project already had the other half (an empty `extensions = []` seam, 8 environment-assumptions).
- ⭐ **Encoding union is DECIDABLE, so composition is a verdict.** Two instructions collide exactly
  when `(a.value ^ b.value) & a.mask & b.mask == 0`, searched exhaustively. Proven: owned RV64I +
  an unseen `M` fragment = 65 instructions, no collision. Fired RED on a realistic mistake —
  composing a fragment already contained — giving 37 named collisions and a rejection.
- ⚠️ Semantics are the hard axis and are NOT decidable: an extension can change a base
  instruction's meaning. A fragment must *declare* that it refines base behaviour; a silent
  override is a defect, not a composition.
- 🔎 LIVE_STATUS.md went **over its ceiling** because I had been writing narrative into a status
  table whose owner column literally says "rows are states, not prose". Trimmed to states; the
  gate was right and the fix was the one the registry prescribes.
- Promotion is explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — owning a source means building without it

- ⛔ The repository did not own its model's encodings: the assembler read `target/refs/riscv-opcodes`,
  untracked and network-acquired, so a fresh clone could not build a model. The project's own rule
  was being broken by its own tooling.
- ⭐ **The test that settles ownership is not that a file exists — it is that the build works with
  the source moved aside.** `mv target/refs/riscv-opcodes /tmp/ … && run_smoke.py` → ok: four
  guests assembled, run on two references and reproduced, with the encodings' origin absent.
- Ownership without re-derivation is a copy, so the agreement is gated and was fired RED on a
  one-bit `funct3` edit.
- ⛔ The new S-expression reader was caught by its own first real input: it stripped `;` comments
  line by line before tokenizing, so a `;` INSIDE a string truncated it and a string could not span
  lines. Generating our own encoding file hit that within minutes. Whether a `;` starts a comment
  depends on whether a string is open — that question cannot be answered by a prior pass.
- The S-expression trigger fired and was answered on merit: trees get S-expressions, records keep
  JSON/TOML and their working gates. "Single source of truth" = one owner per fact, not one file.
- Promotion is explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — a category the layer does not own is not "missing"

- Devices are **board / SoC** material, not CPU material. The processor layer ends at the
  CPU/environment boundary: the CPU states assumptions, a board later states guarantees
  (`docs/CPU_ENVIRONMENT.md` §5, and `INFORMATION_CATALOG.md`'s own note that C19–C21 are not all
  properties of the CPU).
- ⭐ The consequence lands on the materials census, and it would have been a real defect: marking
  `C19 Platform, devices and interconnect` as `missing` for a CPU model manufactures an acquisition
  task for material the model must never contain, and reports a **correct scope as a deficiency**.
  The disposition vocabulary now carries a LAYER, and `deferred-to-board` is distinct from both
  `missing` and `not-applicable`. Caught before the schema was written, which is the only cheap
  moment to catch it.
- ⚠️ It also corrected my own framing of "runs real code": the console and the program-exit
  convention are BOARD concerns. What the processor layer owes real code is the psABI, the ELF
  contract, entry/startup state and the compiler-runtime intrinsics — and nothing else.
- `DIFF-PLATFORM-SPIKE` is a LAYER difference, not a configuration one: Spike ships a CPU and a
  small board together. The record now measures how much board each reference drags in.
- Promotion is explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — answer a narrow instrument with a wider one, and state the wider one's scope

- The sweep found **one further instance**, worse than the founding one: Spike's
  `matched_isa_string` was the command-line INPUT sitting in an observation's slot. Spike has no
  `--print-isa`, so nobody had confirmed it configured what it was told. Now read back from
  `--dump-dts`, with a control (`--isa=rv64im` → `rv64im`) proving it is an observation, not an echo.
- ⭐ The replacement is a principle with a tool behind it: claim a match against the model's own
  self-description at the **widest granularity it offers**. Both models emit a device tree; the
  comparison shows 4 of 4 platform fields disagreeing and four devices only Spike advertises.
- ⚠️ **The wide instrument has its own scope and must say so**, or it becomes the next narrow one.
  A device tree is what a platform ADVERTISES — not semantics, not memory attributes — and Sail's
  still lists a `timebase-frequency` and an `htif` node with no device behind them.
- The durable answer to "are there others?" is not "no". It is that a new one **cannot be added**
  without declaring what it does not establish — rule 5b, fired RED on the real dossier.
- Promotion is explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — an instrument that answers a narrower question than the one you asked

- ⛔ **The profile was matched on its instruction set and not its platform, for four leaves.** The
  override set `extensions` and left the reference's default platform underneath: a core-local
  interruptor, an interrupt generator, two I/O regions. A guest read CLINT `mtime` with a PLAIN
  LOAD and watched it advance (2 → 3). Excluding `Zicsr` removes the CSR *instructions*, not the
  device — and a device exposes time as ordinary MMIO.
- ⭐ **This is a distinct failure mode from `zero-hits-absence-or-blindness`.** That one was an
  instrument that could not see. This one is an instrument that **answered a different question**:
  `--print-isa-string` returned `rv64i_zvl32b`, which is *true*, and describes an instruction set
  rather than a machine. A confident, correct, narrower answer is harder to doubt than a zero.
- Four committed claims were refuted by one probe. All corrected at source; the repair is held by
  a tracked negative fixture that must fault.
- Spike's platform is irreducible with the available controls, so it is ENUMERATED, and the
  consequence is stated exactly rather than left implicit: the original guests agree because they
  touch neither device region — a stated precondition, not luck.
- 🔎 The general question this raises, and it is not yet answered: **which other "matched"
  claims in this repository rest on an instrument that answers a narrower question?** The pattern
  to look for is a single confident scalar standing in for a configuration. Owner: `MODEL-BOOKS.1`,
  whose materials bill must state for each reference what was matched and by what evidence.
- Promotion is explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — a gate report that cannot tell a mention from an implementation

- Gate `G0` is run and reads **`incomplete`**: 66 declared checks, 0 implemented. The report is
  GENERATED from tracked inputs and gated for staleness, so `passed` is unreachable — the
  generator has no code path to it, and hand-editing the word fails the commit.
- ⛔ **The generator was wrong twice, both times inflating the verdict.** "How many checks are
  implemented?" first counted `EVIDENCE_POLICY.md` (grepping the id PATTERN across the tree — a
  document describing the naming convention), then counted `check_requirements.sh` (which tests
  the `-POS`/`-NEG` suffix while enforcing that ids exist — a gate about checks is not a check).
  Both said `1`; the truth is `0`. The measure is now exact: take the CONCRETE declared ids and
  ask which any tracked executable names. The failure direction is the lesson — an approximate
  measure of "is this done" drifts toward done.
- ⛔ The evidence policy's first draft stated class populations and got two wrong, by reading the
  profile's authority distribution instead of the requirements' category distribution — the exact
  non-mechanical mapping documented two leaves earlier, walked into by the person documenting it.
  Hand-typed populations were removed; the generated report derives them.
- ⭐ `incomplete` is the DELIVERABLE. A milestone whose job was to establish what evidence would
  be required cannot also have produced it. Saying so in the verdict, rather than in a footnote,
  is what stops the next milestone inheriting a claim nobody made.
- Promotion is explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — derive the layout, and report the control that passed

- The B/J immediate scramble is **derived** from a pinned descriptor table, not typed. The
  derivation validates itself: the bits a descriptor accounts for must total its field width
  (7, 5, 20, 20) or the table is refused. A layout the assembler cannot reconcile is one it will
  not use — which is the same shape as the validator's refusal rule from the previous leaf.
- ⭐ **Negative observations earn their place.** `never_written` catches a jump that failed to
  skip, which a checker watching only the registers it expects to change cannot see. Fired RED by
  breaking the PROGRAM (jump to the next instruction), not the expectation.
- ⛔ **A control that passed is still a result.** `jalr +13` vs `+12` land identically *because*
  the low bit is cleared, so the landing address does not discriminate D-JALR-LSB. Both references
  clear the bit, so the failing branch was never observed. Recorded as a `limit` in the
  expectations file rather than letting a green result imply a discrimination it did not make.
  Owner of a real control: P1-LAB's mutation suite, which can mutate OUR model.
- Assembled instructions are not executed steps. Equal for straight-line code; wrong the moment a
  loop exists. The run bound now comes from the expectations file.
- Promotion is explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — a "none" that is merely absent is one nobody considered

- The environment contract's two most useful obligations are the ones whose answer is **none**:
  no virtual time is architecturally readable, and no asynchronous event is deliverable *by
  construction*. Both record WHY. Absent from the contract, they would be indistinguishable from
  boundaries nobody thought about; written down, a later profile has to reopen them deliberately.
  Same for the six of ten §2 boundary items that are out of scope, each with its reason.
- ⭐ *Laboratory policy cannot override an architectural requirement* is now mechanical: an
  obligation whose requirement is architecturally `defined` must carry `authority: architecture`.
  Mislabelling an ISA rule as a harness choice is how a defect becomes an unfalsifiable "profile
  difference" and stops being looked at.
- The new rules fired first on the SHIPPED examples, not on our profile: both example requirements
  name obligations that do not exist. They are `frozen-in-place` delivery artifacts, so they are
  not edited to satisfy a rule written later — routed to `P1-LAB`'s graph checker, with `--audit`
  keeping the finding a command rather than a paragraph.
- Promotion is explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — a partial validator must refuse, not skip

- No JSON Schema library exists on this host and installing one would put a dependency store off
  the repository volume, so the validator is 180 tracked lines covering exactly the 17 keywords a
  census of `schemas/*.json` found. ⛔ **The soundness property is the REFUSAL.** A partial
  validator that silently ignores an unimplemented keyword reports `valid` for a document it never
  fully checked — so this one raises `UnsupportedSchema`, and a schema gaining a keyword breaks
  the gate loudly instead of widening what passes.
- ⭐ `source_semantics.category` is **not** a function of the profile's `authority`. `laboratory`
  covers both "the spec says UNSPECIFIED and we chose" and "the spec delegates to the EEI and we
  chose"; collapsing them records a laboratory policy as an architectural rule.
- The sharpest gate rule this leaf adds: `research_status: resolved` may not coexist with an
  `OPEN:` note. Both halves are true separately, which is what makes the pair convenient.
- ⛔ Two defects in the new gate were found by its own arms, not by review. It excluded `target/`
  by ABSOLUTE path — and its own fixtures live under `target/doctrine-selftest/`, so all ten arms
  failed with "no .jsonl record file found". And the cross-checks re-parsed a file that had
  already failed to parse, crashing the gate rather than failing it: a traceback is not a verdict.
- Promotion is explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — a running total is a memory of a measurement, not a measurement

- ⛔ Two derived counts were committed WRONG in a single session, both as running totals:
  `24 destinations governed` against a 25-row registry, and `107 self-test arms` against 112. The
  method was identical each time — take the written number, add your delta, write the sum back —
  and nothing recomputed either. Gated by `DERIVED-COUNTS`, which re-derives each from the
  population it summarises and prints the enumerator alongside the value.
- ⭐ The new gate caught its own registration: adding it made the project hold 9 doctrines where
  the page said 8, and the commit was blocked until the number was re-derived rather than bumped.
- ⛔ Its first cut was wrong in the *dangerous* direction. `sed -nE "s/.*([0-9]+) widgets.*/\1/p"`
  is greedy: on `12 widgets` the leading `.*` eats the `1` and the capture is `2`. A stale count
  could have matched a wrong extraction and read as correct. Found by a GREEN arm going red.
  Extraction is now off the front of a `grep -o` match, and a pattern not beginning with its
  number group is refused.
- The `TASK-ACCEPTANCE` recipient-tree boundary is **documented, not relaxed**. Requiring only one
  staged leaf to pass would reopen the co-staged-leaf hole that box-scoping exists to close, so a
  routed annotation lands as its own doc-only commit instead. The lesson's promotion is
  explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — 184 of 199 files are the same file, and an instrument that answered blind

- ⛔ **The two reference models run the SAME floating-point source.** Both vendor Berkeley
  SoftFloat; 199 `.c` files exist in both copies and **184 are byte-identical** once the release
  comment is normalized (sail 3e, spike 3d; `f64_add.c` differs by one line). A Sail-vs-Spike FP
  comparison executes one implementation twice. No current evidence is affected — this profile
  has no floating point — so it is routed to `P4-SYSTEM.7` with its measurement. Recorded:
  [`reference_softfloat-shared-ancestry`](docs/decisions/reference_softfloat-shared-ancestry.md).
- ⛔ **`strings | grep -c softfloat` returned 0 for both binaries and that was BLINDNESS, not
  absence.** `nm -a` showed why: spike carries 649,743 symbols, the Sail release binary 400. A
  stripped binary cannot answer the question. The `0` was one step away from being written down
  as a finding; the source was cloned instead, at the exact commit the binary's `--build-info`
  reports. Pick the instrument that can see, then read it.
- ⭐ Independence cuts in unexpected directions. Encoding is **not** shared — spike generates
  `encoding.h` from `riscv-opcodes` while the Sail model hand-writes 59 `encdec` files and never
  mentions it — so *our* assembler shares an ancestor with spike and not with sail, which makes
  sail decoding our bytes an independent confirmation and spike doing so not one.
- `docs/tasks/P0-PROFILE.md` hit the per-part **ceiling** (73,317 B > 65,536) and the completed-leaf
  evidence was split to `docs/tasks/archive/`, unedited. The ceiling was obeyed, not raised, which
  is what the registry's own header prescribes. Checked that the split did not move pressure
  somewhere ungoverned: `git ls-files -- docs/tasks` is recursive, so the archive still counts
  toward the family aggregate (240,293 B against a 393,216 ceiling).
- 🔎 **A new mirror-drift instance, outside what `MIRROR-DRIFT` gated.** `LIVE_STATUS.md` claimed
  "24 destinations governed" while `doctrine/readme_routes.tsv` holds 25 rows and the gate prints
  25 — stale since `SEMULITH-P0-0013` added the `profiles/` row. Corrected here; the *class*
  (a live document restating a count that a registry owns) is not yet mechanized, and `TREE-CLAIMS`
  only covers task-tree facts. Owner: `MIRROR-DRIFT.4`, opened next.
- 🔎 `TASK-ACCEPTANCE` requires every staged `docs/tasks/*.md` to carry a ticked checklist. It
  cannot tell the leaf that OWNS a change from a tree that RECEIVES a routed finding, so
  annotating `P4-SYSTEM.7` had to be split into its own commit — P4 has not started and ticking
  its template would be a lie. Splitting is the right answer; the gate not distinguishing the two
  roles is the defect. Owner: `MIRROR-DRIFT.4` alongside the registry-count class.
- Promoted: [`docs/knowledge/zero-hits-absence-or-blindness.md`](docs/knowledge/zero-hits-absence-or-blindness.md).

## _(2026-09-14)_ — the pinned spec has no encodings, and a shorter trace is not agreement

- ⛔ **The specification we pinned does not contain instruction encodings.** Census over all six
  artifacts: `grep -cE '[01]{7}'` -> 0 every time; the format diagrams are images (31 in the
  RV32I chapter). The SEMANTICS are all present in prose, which is the half expected values need,
  so encodings were pinned separately from `riscv-opcodes` and recorded as a *different*
  provenance. That source is upstream of both models, so encoding agreement is not independent
  evidence — only semantic agreement is, and that is what the experiment tests.
- ⭐ Unplanned corroboration: the encoding table holds exactly 52 instructions for this extension
  set, and `P0-PROFILE.1` enumerated exactly 52 by hand from the prose without it. Symmetric
  difference: none. Two independent routes to the same closed set.
- ⛔ **The comparator reported a false pass and running it is what found that.** Walking only the
  overlapping prefix, it printed `AGREE over 2 aligned step(s)` for a run where one model trapped
  and the other stopped. The prefixes agreed; the observation did not. Promoted:
  [`docs/knowledge/a-shorter-trace-is-not-agreement.md`](docs/knowledge/a-shorter-trace-is-not-agreement.md).
- ⭐ **Two models agreeing means nothing until the agreement is shown to be doing work.** Flipping
  one configuration key — the misaligned policy — with the same binary produced a real first
  divergence. That control is why "matched profile" is now a measurement. The project gate now
  refuses an experiment record that claims agreement without naming such a control.
- 🔎 `docs/tasks/` crossed its advisory health target (214,002 B against 196,608). Not a ceiling
  (393,216 aggregate, 65,536 per part) and nothing is breached, but `P0-PROFILE.md` is at 49,521 B
  — 76% of the per-part ceiling — because completed-leaf evidence accumulates in-tree by design.
  The mechanism intended for this is archive compaction, and no tree has needed it yet.

## _(2026-09-14)_ — availability is not identity, and a budget can be wrong in your favour

- ⛔ **The package manager had a formula called `sail`. It deploys WordPress sites to
  DigitalOcean.** An exact name collision with the Sail ISA specification language: the lookup
  succeeded, the version was current, the licence was real, and the referent was wrong. Had the
  check been `brew info sail >/dev/null && echo available`, the dossier would carry a sentence
  that is false, sourced and reproducible. Identity needs a field only the real thing can
  produce — here `--build-info`, which prints an upstream release, a git sha and the compiler.
  Promoted: [`docs/knowledge/availability-is-not-identity.md`](docs/knowledge/availability-is-not-identity.md).
- The roadmap priced reference acquisition as the first activity whose cost was *not obviously
  bounded*, assuming an OCaml/opam build of Sail. Release 0.14 ships a native binary for this
  host's architecture, so Sail was the **cheapest** candidate, not the dearest. Three models
  obtained in one leaf. The estimate was wrong; the reasoning behind it ("acquisition is work
  with observable outcomes") was right and is untouched.
- ⛔ **The Sail model will not tell you what configuration it ran with.**
  `--print-default-config` ignores `--config-override` — byte-identical dumps. `EVIDENCE_AND_GATES`
  §5 wants the *effective* configuration, so it is recorded as (default) + (tracked override)
  with the merge explicitly labelled **ours**. The model's one self-description is
  `--print-isa-string`, which is why `rv64i_zvl32b` is pinned and re-derived.
- Having three binaries is not having three opinions. The gate now refuses a candidate whose
  `lineage` field is missing, because an unasked independence question reads exactly like an
  answered one.

## _(2026-09-14)_ — a self-test reports the arms it ran, not the arms you wrote

- `docs/TASK_TREE.md` and the tree it indexes disagreed about which leaf was next: the index
  said `P0-PROFILE.2`, the tree said `.5`, and `.2` was `done`. `COMMIT.md` updates that index
  "only if the frontier changes" — a CONDITIONAL manual step, which is the shape that rots. One
  row of fourteen had drifted, and it was the only `active` tree: the single row the documented
  resume path (`MEMORY.md` → index → frontier) actually reads. A 1-in-14 drift rate is not the
  number that matters; a 1-in-1 rate on the followed row is. Gated by `FRONTIER-SYNC`.
- ⛔ **The new gate's own self-test printed `4 pass / 0 fail` while running four of fourteen
  arms.** Ten `arm` calls sat on the same physical line as the fixture call before them with no
  `;`, so bash passed `arm` and its three arguments as extra positional parameters to a function
  reading only `$1` and `$2` — discarded in silence, no error of any kind. Adding the separator
  gave `13 pass / 1 fail`, and that one failure was a real defect: two opposite drift directions
  shared a single message. Caught by counting the arms written against the arms reported, not by
  reading the code. Promoted:
  [`docs/knowledge/self-test-arms-that-never-ran.md`](docs/knowledge/self-test-arms-that-never-ran.md).
- Two blank lines inside `DOCTRINE_ENFORCEMENT.md`'s project-doctrine table split it into three
  GFM fragments, so two registered doctrines rendered as literal `| … |` text instead of rows.
  Right in the file, wrong on the page — one column over from what `TABLE-ARITY-RATCHET`
  catches, and no gate sees a blank line.

- The same mechanism, one document over: `docs/book/src/working/doctrines.md` listed 3 project
  doctrines while 5 were registered. A mirror that falls behind never **invents** a guarantee —
  it **withholds** one, on the surface a reviewer reads instead of the code. Gated by
  `REGISTRY-MIRROR`, which also caught the opposite direction unprompted (`PHANTOM`: a row added
  one step before its registration).
- The durable fix for the swallowed arms is a strict-arity guard on every self-test fixture
  helper, fired RED by deleting one `;`. A helper that ignores surplus arguments is what made the
  swallow silent; refusing them is what makes it loud.

- The third mirror had **not** drifted, and the leaf says so instead of manufacturing a defect.
  For a prevention leaf the falsification is the load-bearing box: four controls, each breaking a
  real claim in `MEMORY.md`/`LIVE_STATUS.md` and restored with `git checkout --`.
- A gate's scope can be data someone already wrote down. `TREE-CLAIMS` reads the `hot_live` rows
  of `doctrine/readme_routes.tsv` rather than carrying a file list — which also gets the
  `append_history` exclusion right for free: history must never be rewritten to match today.
- ⭐ The gates now catch each other. Registering a doctrine without mirroring it failed inside the
  same commit; the same omission had survived two prior registrations unnoticed.
- A rule keyed on words fires on prose about the rule. The frontier check matched any line
  mentioning "frontier leaf" and double-reported; anchoring it on the label fixed it, and the
  narrowing was re-fired RED — narrowing a gate is precisely the edit that can silently disable it.

## _(2026-09-13)_ — a delivered package is not ingested until its rot sources are removed

- Planning package v0.2 arrived in the worktree as 15 untracked files plus two modified
  tracked ones, and every problem it carried was invisible to a reader: `shasum -a 256 -c
  MANIFEST.sha256` printed 25 × `OK` and `rc=0`. The manifest was *correct and already
  doomed* — two of its rows (`README.md`, `ROADMAP.md`) name files this repository exists to
  change. A control whose failure is scheduled is not a control.
- The enforcer found the one defect a human review had not: `scripts/check_doctrines.sh` →
  `README-STABILITY: README.md no longer links README_POLICY.md`. The delivered README was a
  perfectly good package front page and a policy breach, because replacing a landing page
  silently drops whatever contract the landing page carried. Promoted:
  [`docs/knowledge/re-derivable-vs-cited-evidence.md`](docs/knowledge/re-derivable-vs-cited-evidence.md).
- Two byte-identical copies of the archogen integration contract shipped together. Both
  passed every gate. Promoted:
  [`docs/knowledge/duplicate-document-ownership.md`](docs/knowledge/duplicate-document-ownership.md).
- ⛔ **Two sibling doctrines disagreed about what an instrument is.** `GAP-CLAIM-CENSUS` prints
  `git grep -n '<symbol>' -- src scripts | wc -l` in its own failure hint and accepts it as a
  census; `TASK-ACCEPTANCE`'s default signature family recognises `git ls-files|log -S|…` and
  **not** `git grep` or `wc -l`. Obeying one gate produced evidence the other refused. Fixed
  through the sanctioned `.doctrine/evidence_tokens.txt` seam, never by weakening the evidence
  — and the widened gate was then fired RED (a prose-only box → `rc=1`) to prove it still
  discriminates. Promoted:
  [`docs/knowledge/census-instrument-signature-gap.md`](docs/knowledge/census-instrument-signature-gap.md).
  Upstream owner: this is a `bedrock` template defect, not a Semulith one.

## _(2026-09-04)_ — a template's trial must include the first commit

- Every gate was green on the generated project and the first commit still failed: the doctrines judge STAGED
  code, and nothing had been staged until the user tried. Trial the path a user walks, to its end.
- `grep -c` prints `0` and exits 1. `$(grep -c … || echo 0)` therefore yields `0⏎0` — a second line — which
  here started a flush-left line inside a checklist bullet and hid its evidence from the box-scoped extractor.
  Capture the count, then default the empty case; never append a fallback to grep's own output.

## _(2026-09-04)_ — a green gate that judges nothing is the class a template must not ship

- Two of the four doctrine ports in `.2.6` were wrong on first run and their own RED self-test arms said so:
  a `python3 - <<'PY'` detector whose stdin was the heredoc (every arm read 0 rows), and a `grep -c … | grep -qx 0`
  control under `pipefail` (`grep -c` prints 0 and exits 1). A self-test with only GREEN arms would have passed both.
- The neutrality bar is measured, not felt: `grep -ciE 'grammar|parser|…'` over each ported script → 0, after the
  generic uses of "corpus" and "grammar" were re-worded ("tree", "syntax") so the count means what it says.

## _(2026-09-14)_ — a parser's error paths say nothing about the content it returns

- `"".join(buf).encode().decode("unicode_escape")` is a **Latin-1** decoder. Every `§` in this
  project's semantics fragment came back as `Â§`, every `—` as three characters of noise — all 52
  specification citations, corrupted on read, by a reader that raised no error and by a suite in
  which no instrument was pointed at fidelity. Promoted to
  [`a-parse-without-error-is-not-a-faithful-read`](docs/knowledge/a-parse-without-error-is-not-a-faithful-read.md).
- The reader every source of truth in the repository depends on had **no self-test at all**, and
  I was one leaf away from building a schema layer on top of it. Read the foundation before you
  stand on it; 18 arms cost twenty minutes and the first three were RED.
