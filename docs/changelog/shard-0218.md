# CHANGELOG shard — SEMULITH-P4-0045 … SEMULITH-P4-0040

> Sharded from `CHANGELOG.md` under its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P4-0045 (leaf P4-SYSTEM.7, slice c4 part 1) — the dependency store on-volume

- Slice (a)'s first registry dependency (`rustc_apfloat`, with `bitflags`/`smallvec`) was
  resolved by every routine build through the shared `~/.cargo` cache (`cargo metadata`
  named the user-home path): the on-volume fetch had been one command's environment.
- `.cargo/config.toml` replaces crates.io with the untracked on-volume `.app-data/vendor`
  (Cargo.lock's checksums stay the tracked identity); `make vendor` populates it
  idempotently and is a prerequisite of check/clippy/test/bench/gate; the three CI
  workflows and bootstrap populate it; a missing store fails loudly. The shared cache was
  left untouched (§13). README, the book's annex, a knowledge card. `make check` + `make
  gate` green.

## SEMULITH-P4-0044 (leaf P4-SYSTEM.7, slice c3 part 2) — the semantics language learns FP; f.sem.sexp; the gated lowering; the assembler's derived register files

- `schema/semantics.sexp`'s floating-point block: the FP-state contract stated once (f-file
  reads pre-instruction, writes mark FS Dirty, the Off gate judged at the head of any rule
  that touches FP state, sticky accrual with Precise dirtiness, NaN-boxing in the tree, the
  reserved-rm policy) and 18 operators (freg fbox funbox rounding fadd fsub fmul fdiv fsqrt
  fmadd fmin fmax feq flt fle fclass f2i i2f).
- `definitions/riscv/f.sem.sexp`: the 30 F rules, cited (26 quotes judged by CITATION-QUOTES,
  0 findings). `check_semantics.py`'s `check_fp`: an rm-carrying encoding must resolve
  `(rounding (field rm))`; literal formats/widths/signedness; one register file per operand
  (+6 arms, 23/23).
- `gen_definition.py`: the `Surface` bundle; the F lowering and Sem variants emitted only
  when `riscv/f` is composed (+8 DEF-GEN arms, 31/31); `check_fp` re-derived; the module's
  form count derived (62) — the typed "43" had been wrong (44) since `.4` slice b.
- `riscv_asm.py`: an operand is spelled `f0..f31` exactly when its rule names it through
  `(freg …)` (derived from the composed semantics; the other spelling refused by name);
  `rs3`/`rm` supported. 30/30 F forms round-trip through spike-dasm. Both definition modules
  and both guest fixtures emission-neutral; `make check` + `make gate` green (455 arms).

## SEMULITH-LC-0003 (leaf LIVE-CONTAINMENT.3) — TOOLBOX and DOCTRINE_ENFORCEMENT partitioned behind bounded indexes

- `DOCTRINE_ENFORCEMENT.md` (32,669 / 32,768 B): the 35 long-form project-doctrine rows
  moved verbatim into `docs/doctrines/` (governance / definition / evidence / board); the
  parent keeps a complete id → family index. REGISTRY-MIRROR gains a project-scoped mirror
  and judges the families' union (13/13 arms; RED on a removed row).
- `TOOLBOX.md` (20,478 / 20,480 B): the 76 tool rows moved verbatim into `docs/toolbox/`
  (governance / definition / composition / execution) behind a family index. A first pass
  dropped one row (its first cell had no backtick) and a census reusing the mover's filter
  missed it; a positional census caught it and the move re-ran from HEAD.
- Both families registered (partitioned, per-part bounds); "Adding a doctrine" and the
  add-a-tool note point at the families; LIVE_STATUS 36 destinations / 451 arms; `make
  gate` green, `make book` rc=0.

## SEMULITH-LC-0002 (leaf LIVE-CONTAINMENT.2) — the stale orientation sources corrected

- `knowledge-map/subsystems.md` (the one hand-curated input to the derived Knowledge Map)
  described a `crates/app/` scaffold placeholder that does not exist; it now names the four
  real crates (roles and the CLI's nine subcommands read from the sources), the
  definition fragments + semantics, the six unit directories, schema/materials, and the
  two book families. `KNOWLEDGE_MAP.md` regenerated.
- The workspace `Cargo.toml` header no longer tells the reader to replace a starter crate;
  `README_POLICY.md`'s adoption note states the measured ceiling firings instead of "no
  measured pressure … 16,228 bytes", and routes the doctrine adoption to
  `LIVE-CONTAINMENT.4` (the policy decision itself unchanged). `make check` + `make gate`
  green.

## SEMULITH-LC-0001 (leaf LIVE-CONTAINMENT.1) — the closed-tree register: completed trees leave the index

- New tree `LIVE-CONTAINMENT` (true and bounded live surfaces; four leaves). Its first
  leaf applies `docs/TASK_TREE.md`'s own registered control — "completed trees leave the
  index" — which had never been applied: FRONTIER-SYNC's CLOSURE rule required an index
  row for every tree, so obeying the registry would have failed the gate.
- The 22 completed rows moved verbatim into `docs/TASK_TREE_CLOSED.md` (registered: health
  8 / ceiling 16 KiB); the index 8,172 → 4,053 B. FRONTIER-SYNC gates both files (CLOSURE
  over the union; COMPLETED IN INDEX, OPEN TREE IN REGISTER, DUPLICATE ROW; 20/20 arms) —
  RED 22× on the real pre-move index. COMMIT.md, TASK_TREE_README.md and the book's
  task-tree chapter (both anchors included live) describe the move.

## SEMULITH-CA-0001 (leaf CITATION-ACCURACY.1) — the quoted-phrase-in-section gate: CITATION-QUOTES registered

- New tree `CITATION-ACCURACY`, owning the gap `P4-SYSTEM.7` slice (c3) part 1
  measured: a locator can resolve and still name the wrong section, and no gate read
  quotes (`check_citations.py` checks the semantics files' locators for existence only).
- `scripts/check_citation_quotes.py` judges every quoted phrase a tracked `.sexp`
  attributes to a pinned section (four decidable attribution rules; ellipsis pieces in
  order; case/whitespace/quote/dash folding and zero-width removal, both renderings
  measured on the pinned pages); a miss names where the phrase actually is.
- `scripts/check_citation_quotes.sh` — the 35th project doctrine: 14 controls on
  synthetic pages (a matcher mutation turns 6 red), a NAMED SKIP without the pinned
  pages. RED on the real pre-fix corpus: 6 misses, each "found in §20.1.2". HEAD: 24
  quotes judged, 0 findings. Mirrors: DOCTRINE_ENFORCEMENT.md, the book's doctrine
  chapter, TOOLBOX.md, LIVE_STATUS (35 doctrines, 445 arms). `.2` (the Markdown
  census) proposed.

## SEMULITH-P4-0043 (leaf P4-SYSTEM.7, slice c3 part 1) — the FP-CSR locators corrected

- The pinned F chapter numbers the fcsr section §20.1.2 (§20.1.1 is "F Register
  State"); the D chapter numbers FLEN=64 §21.1.1 (§21.1.2 is NaN boxing). Slice
  (b)'s locators — carried into c1 — cited §20.1.1 for fflags/frm/fcsr content in
  the state document (9 lines), both FP guests' directives (and so their derived
  expectations), a privilege.rs doc comment and a unit-test comment, and §21.1.2 for
  FLEN=64. All re-cited; both guests re-derived (sources only, every value
  byte-identical); the hash-pinned mirrors regenerated; 103/103.
- The class was invisible to tools: `check_citations.py` resolves only the
  semantics files' locators, and only by existence. Owned by the new
  `CITATION-ACCURACY` tree (a quoted-phrase-in-section gate), executed next.

## SEMULITH-P4-0042 (leaf P4-SYSTEM.7, slice c2) — the rv_f/rv64_f re-pin + the f.sexp fragment

- `rv_f`/`rv64_f` re-pinned in the rv64gc ledger through the tracked `extensions/`
  fetch route (3,050/320 B; a fresh re-fetch byte-identical): the F extension's 30
  forms (26 RV32F + 4 RV64F conversions). The census leg's named exclusion extends
  to them until the F bind grows the scope (RED-proven: without it the leg reads
  118 vs 88, exactly the 30 F names).
- `definitions/riscv/f.sexp` generated by `gen_fragments.py`: requires the base,
  owns `rs3` (31..27) and `rm` (14..12); the register-file class of `rd`/`rs1`/`rs2`
  is left to the semantics. The 13 upstream pseudo rows are written out, not
  carried (the rv64i policy). The other seven fragments re-derive byte-identical;
  the 115-form trial union is collision-free; both profiles verify; `make gate`
  green. No Rust touched — the slot stays declared until slice (c6).

## SEMULITH-P4-0041 (leaf P4-SYSTEM.7, slice c1) — frm holds any 3-bit value: slice (b)'s WARL retention fixed at root; the slice (c) split recorded

- **The defect, measured against the pinned chapter**: slice (b) declared `frm`
  WARL one-of 0..4 (an illegal write retaining the old value); RVI-F §20.1.2 says
  FSRM writes "the three least-significant bits of integer register rs1 into frm"
  and names 101–111 dynamic reserved rounding modes — values frm must hold. Fixed
  at the declaration (`(legalize (any))`, the sentence quoted), the generated
  state mirror and the definition manifest regenerated, the privilege unit tests
  rewritten to the spec rule.
- `fp-fcsr-view` re-derived spec-side first (the authoring tool corrected) and
  RED against the unfixed engine (fcsr `0x45` vs the spec's `0xE5`), green after;
  its step 13 now also exercises fcsr's ignored bit 8. Both FP guests' headers
  corrected (they named "P4-SYSTEM.5 … the interrupts corpus"); the authoring
  tool refuses a `"` in a directive by name.
- The reserved-rm policy recorded: the pinned revision makes it "reserved"; the
  laboratory takes illegal-instruction (still valid per the spec; Sail's
  `Fcsr_RM_Illegal`) — stated in the operator contract at slice (c3).
- The slice (c) execution split recorded in the tree (c1–c6; the FS gate judged
  at the head of any instruction whose rule touches FP state). Book: the
  duplicated `## Gate CPU-SYSTEM` heading and the stale `.3`/`.4` "underway"
  headings fixed; the `.7` section records the correction. Knowledge card
  promoted. 103/103; `make check` + `make gate` green.

## SEMULITH-AC-0059 (tree ARTIFACT-CLEANUP) — the 2026-10-06 §8 run: 192 incremental caches deleted (607 MB)

- The ~24 h trigger fired (the `2026-10-04` record was two days old). The census found
  192 cargo incremental `.bin` caches (607 MB; 144 `target/debug`, 36 wasm32, 12 the `.7`
  slice-(b) scratch probe's own cargo build under `target/p4-system-7/`), all under the
  enumerated `*/incremental/*` scope, deleted; 0 stray `.bin`/`.log` in
  `target/release`/`target/debug/deps`. 62 `target/refs/**/*.log` (2.2 M, evidence trails)
  and the 7 cargo-home crate fixtures (inputs) kept by standing policy.
  `docs/ARTIFACT_CLEANUP.md` overwritten with the dated one-line record; `target`
  4.8 G → 4.2 G, `.app-data` 1.4 G unchanged.

## SEMULITH-P4-0040 (leaf P4-SYSTEM.7, slice b) — the FP state: the f-file census-gated, the FS gate live, the fcsr two-owner view fixed at root

- The f0–f31 register file (FLEN=64, the LP64D ABI) is declared in the state
  document (the new `fp_registers` construct through `schema/state.sexp`, the
  dossier mapping both directions, and gen_state's validation/emission) and
  carried as hart state under the census discipline: the 4th
  `REQUIRED_CENSUS_CANDIDATES` entry with its RED arm (STATE-GEN self-test
  28→29), the SEM-08 candidate re-answered in place, the generated module
  gaining the field, the reset, `read_f`/`write_f`, and the `PrivilegedHart`
  accessor. Observation stays through the x-registers (the leaf's decision 8).
- Both latent defects fixed at root, re-measured live first (the scratch probe
  on the parent engine): **the FS gate** — `permitted()` answered Ok to all six
  fflags/frm/fcsr read/write combinations at FS=Off; the new arm refuses them
  (the Off-state sentence; Sail 0.14's placement measured: the gate rides
  decode-time legality, `fdext_control.sail:19`, so the instruction side is the
  `fp_enabled()` hook the F/D binds' arms call — no FP instruction decodes yet,
  and the FS=Off instruction cells land at slice (c), recorded). **The fcsr
  view** — the engine resolved the comma literal `"fflags, frm"` as one CSR name
  (reads 0, writes refused); the resolution now composes the owners' field
  blocks in list order (read: fflags[4:0] with frm[2:0] above) and splits writes
  back under each owner's own table (frm's one-of 0..4 judges its slice).
  FP-CSR writes mark FS=Dirty (Sail's `write_fcsr` → `dirty_fd_context`,
  fdext_regs.sail:455); SD follows, being computed. fflags' sticky accrual and
  frm's dyn/reserved-rm resolution are stated in the document for slice (c)'s
  operators.
- The corpus: `fp-fs-off` (the gate's cause-2 cells, the FS transitions, SD
  observed reacting to FS writes) and `fp-fcsr-view` (the 0x7f compose, the
  split write, the frm retention) — 103/103, expectations derived spec-side
  (EVD-05) by the forked derivation tool; both ride the existing seven matrix
  axes. The identity proof: the 101 pre-slice guests byte-identical against the
  parent engine (both CLIs, 5,491 trace lines); the RED control — the new guests
  MUST diverge there — fired, and first caught the identity harness's own
  `--profile=` option-syntax bug (two identical usage errors are not identity).
- `make check` rc=0 (8 groups; semulith-core 134/134), `make gate` green
  (DERIVED-COUNTS 430→431 re-derived; DEF-GEN re-derived after the descriptor
  change; rv64i's surfaces byte-identical), bench wasm 134,105 bytes,
  smoke-bench 53 arms ok, both books. Next: slice (c) — THE F BIND.

