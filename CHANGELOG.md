# CHANGELOG.md

## SEMULITH-BR-0005 (leaf P3-BREADTH.1) — F2 measured executably; the unconditional-change set is empty; `.1` slice-gates on `.3`

- Finding F2 (register grouping with fill semantics, TI C64x §2.2) was the one
  `DSP-REVIEW.7` finding classified from a document's shape, not a measured refusal.
  The report named the honest route and `.1` took it: synth probe 5
  (`state-groups.sexp` — the real scalar state document plus one synthetic
  `register_groups` form) refuses by name, `undeclared field "register_groups"`, rc 1;
  the synth suite is now 5/5.
- The findings' required-**unconditional** implementation set measured **empty**: F4/F5
  are conditional on a VLIW slice, F2's implementation idles unless the slice is TI
  (implementing grouping with no exercised target would be the speculative generality
  this tree exists to refuse), F6 fires per new profile. `.1` is `slice-gated` — not
  closed: `.3` naming a VLIW or TI slice reopens it by name. Frontier moves to `.2`.
- Scalar regression evidence preserved and re-run (`EVD-07`; no code changed):
  `make check` 180/180 + fmt + clippy clean; gen_state rc 0; DEF-GEN ok; the G1 gate
  verdict `passed` re-derived.

## SEMULITH-BR-0001 (leaf P3-BREADTH.1) — the composable-DSP design discussion, recorded for resumption

- The director's `[DBINP]` exchange recorded in the `P3-BREADTH` tree's new Design
  Discussions section: a DSP as composition — the fixed skeleton of problems, the measured
  per-axis menu of vendor-citable choices, the composition rules that make a selection
  coherent, and the ISA as the fabric moving data between the chosen parts ("lego into a
  coherent, functional whole"). Resume point for the hypothetical high-end DSP as this
  tree's ultimate stress fixture; the permanent bounds carried (citable per-axis; never
  evidence about a real DSP).
- The tree's blockers cleared on record: `DSP-REVIEW` closed 8/8 (`SEMULITH-DR-0094`).

## SEMULITH-DR-0094 (leaf DSP-REVIEW.7) — the interface findings report: six findings routed, the tree closed 8/8

- The tree's capstone: every candidate interface change classified and costed, routed to
  `P3-BREADTH` with per-finding `ROUTING EVIDENCE` (manual locator + executable
  demonstration + the scalar-profile reproduction check — the method the tree
  pre-committed to before the first finding existed).
- Three CANNOT-EXPRESS findings, each refused by name and pinned by the `.6` synth
  suite: **F1** nonstandard widths (24/56/80-bit; rc 2) and **F3** multiple address
  spaces (rc 1) route to `P3-BREADTH.5`; **F4** the execute packet and **F5** the
  delayed visible writeback (both rc 1) route to `.1` **with the `.8` scope condition**
  — TI-family-shaped, so a scalar-DSP slice does not need them.
- Three NEEDS-A-CHANGE findings: **F2** register grouping with fill semantics (TI's
  40-bit odd:even zero-fill; the one finding without a measured refusal — recorded as
  its honest limit) and **F6** the per-profile state census reopenings (accumulator
  extensions, AMR/MODE1, sticky flags, loop state, the pending-writes window).
- Five measured non-findings classified OUT of interface work (the per-instruction SAT
  side effect, the saturate/round ordering, circular/bit-reversed addressing, the
  SPLOOP drain asymmetry, MFENCE — semantics data + census state, not interface shape).
- The scalar controls measured: the real 64-bit state document generates rc 0,
  `DEF-GEN: ok`, the synth suite 4/0 — **no finding reproduces on `rv64i-lab-v0`**;
  nothing routed belongs to `P2-SCALAR`. Evidence:
  `docs/tasks/artifacts/dsp-review/2026-10-01-interface-findings.md`.

## SEMULITH-DR-0093 (leaf DSP-REVIEW.8) — the cross-vendor contrast: TI's absences are TI's, measured

- The review's first three leaves measured three TI manuals only, and its interim facts
  ("no accumulator", "no guard bits", "no bit-reversed addressing") risked reading as DSP
  properties. The two channel-answered manuals (`SEMULITH-DR-0092`) measured the contrast:
  **the inversion is real, twice over** — DSP56300 carries two 56-bit A/B accumulators
  with 8-bit extension registers (A2/B2, §3.1) and SHARC carries 80-bit MRF/MRB
  accumulators that name the guard bits outright (§3); bit-reversed addressing exists in
  both (DSP56300 reverse-carry modifier §4.5.2; SHARC BR0/BR8 §6).
- Three address-unit shapes (TI byte / DSP56300 24-bit word in P/X/Y / SHARC
  width-varies-by-space word), three circular-buffer alignment rules (align-to-size /
  2^k-aligned / arbitrary), three loop models (SPLOOP / DO+REP / DO UNTIL loop stack).
- SHARC's five-stage **interlocked** pipeline is the printed negation of TI's
  "eliminating pipeline interlocks" — the `.4` break (execute-packet progress, delayed
  visible writeback) re-scopes: it is **TI-family-shaped, not DSP-shaped**.
- Every contrast carries both vendors' locators; nine further manual defects recorded
  unresolved. Evidence: `docs/tasks/artifacts/dsp-review/2026-09-30-cross-vendor.md`.

## SEMULITH-DR-0091 (leaf DSP-REVIEW.6) — the synthetic stress fixture: the boundary pinned, not assumed

- `synth24` (24-bit registers, a second address space, a packet construct, a delayed
  effect) pushed through the REAL pipeline — every shape measured refused BY NAME, and
  the refusals are the pins: the width (`gen_state.py`: "masked fixed-width storage for
  nonstandard widths is generator work", rc 2), the space (`undeclared field
  "memory_spaces"`), the packet (`undeclared field "packet"`), the delayed effect
  (`undeclared operator "delay"`). Each probe descriptor reduced until its ONLY refusal
  is the shape under test.
- The tracked fixture `docs/tasks/artifacts/dsp-review/synth/` carries the SYNTHETIC
  banner everywhere and the citation ban verbatim; the suite is green (4/4) exactly
  while the boundary stands pinned — a shape becoming supported turns it RED, by design.
  This is `.4`'s break made executable: packets and delayed effects refuse at the
  schema layer today, so `.7`'s report can say WHERE the work lives.
- The two vendor gaps were answered same-day (chipdoc's 2026-09-30 DSP batch:
  DSP56300, full SHARC family, TigerSHARC, Blackfin, DSP56800E, DSP48E2) — adoption
  follows; the channel contract recorded as knowledge card `the-chipdoc-channel`.

## SEMULITH-DR-0090 (leaf DSP-REVIEW.5) — loops, repeats, interrupts: the SPLOOP census

- SPLOOP is C64x+-and-later only (measured by the compatibility fields); the loop state
  is fully enumerated (the loop buffer, the hidden LBC ×2, ILC with its 4-cycle load
  latency, RILC, the SPLX bit). Interrupts DRAIN to a stage boundary (short loops are
  not interruptible — the rule has its formula); exceptions do NOT drain (the buffer
  goes idle immediately); restart refills the buffer by re-executing SPLOOP under
  modified rules, the ISR's saves named (ITSR/NTSR, ILC, RILC).
- The acceptance's SEM-04 framing measured: per-instruction completion holds across
  interrupts (E1-entered completes through E5; annulled packets leave no state); the
  persistent loop progress is exactly ILC + the refill — and `.4`'s packet/window break
  stands beside it. Multi-access: LDDW/STDW/LDNDW, ≤2 accesses/cycle; load-multiple and
  non-temporal measured absent; MFENCE is C66x-only, its violated restrictions
  undefined-by-omission.
- Evidence: docs/tasks/artifacts/dsp-review/2026-09-30-loops-q12-q14.md.

## SEMULITH-DR-0089 (leaf DSP-REVIEW.4) — the predicted break, measured — twice

- The scalar step model breaks, measured: (1) the execute PACKET is the unit of progress
  (≤8 instructions, all operands read simultaneously at E1); (2) writeback is delayed and
  visible (load at i+4, no interlocks, early reads stale by design) with interrupts
  landing INSIDE the window (the manual's own LDW/ADD example computes incorrectly).
  `OB-ENV-PARTIAL-PROGRESS` is true for RV64I and false for C6000 — recorded so
  P3-BREADTH never inherits it silently.
- The census consequence: a DSP profile reopens the hidden-state census by its own rule
  (the pending-writes window + packet state). The §3.7.2/§3.8.2 contradiction recorded in
  both forms, C66x's resolved form beside them.
- Evidence: docs/tasks/artifacts/dsp-review/2026-09-30-packets-q9-q11.md.

## SEMULITH-DR-0088 (leaf DSP-REVIEW.3) — addressing and address spaces: units byte-compatible, the seams named

- The acceptance's exact check — units, not just widths: byte-addressed on BOTH sides,
  one 32-bit numbering (no word-addressed space exists — measured). The five seams that
  do NOT fit the flat lab shape, each measured with locators: the 32-bit space; two L1
  spaces with a program-only fetch port (D-FETCH-MAP is scalar-lab-shaped); fetch-packet
  alignment; the AMR control register (the lab has no CSR surface); circular addressing
  restricted to A4–A7/B4–B7. Measured absent: bit-reversed addressing (BITR is a data
  op), strided modes (0 hits ×3). A second core-version split pinned (the circular
  nonalignment floor). Four more manual defects recorded unresolved.
- Includes the gap filing's changelog (SEMULITH-DR-0087 carried none — folded here):
  GAP-DSP56K-FAMILY-MANUAL and GAP-ADI-SHARC-PRM filed through the two-way channel; the
  C55x want dissolved on measurement (already catalogued).
- Evidence: docs/tasks/artifacts/dsp-review/2026-09-30-addressing-q6-q8.md.

## SEMULITH-DR-0086 (leaf DSP-REVIEW.2) — rounding, saturation, sticky flags: the defined step sequences

- The ordering measured as the manuals' own step sequences (multiply → accumulate →
  round-add → shift/saturate → narrow; CMPYR1/DDOTPH2R/QSMPY32R1/DOTPNRSU2 quoted with
  locators) — the leaf's acceptance, never "a saturating add".
- Saturation is in-instruction AND per-lane AND an explicit transfer (SAT); the
  sticky-flag side effect is per-instruction DATA (SADD2 saturates but does not set SAT —
  printed in its own entry). CSR.SAT/SSR survive interrupts (the TSR tables prove it);
  the context-switch restore ORDER is documented; SAT sets one cycle after the result —
  the delayed-effect shape, routed as `.4`'s input.
- **Seven manual defects/ambiguities recorded, none resolved by intuition** (the CMPYR1
  typo in two manuals, the prose-vs-C ordering contradiction, the missing saturation
  clause, the core-version intermediate-width split…). Evidence:
  docs/tasks/artifacts/dsp-review/2026-09-30-rounding-saturation-q3-q5.md.

## SEMULITH-DR-0085 (leaf DSP-REVIEW.1) — widths and accumulator semantics, measured across the three TI manuals

- The first DSP review leaf: Q1/Q2 of the catalog's DSP questions answered from the
  catalogued C64x/C66x/C674x manuals by text extraction — every fact quoted with its
  printed page and section. Headlines: NO accumulator and NO guard bits anywhere
  (measured absent, the searches named); 40-bit "long" values in odd:even register pairs
  with a zero-fill rule (all three), 64-bit pairs (all three), 128-bit quadruplets (C66x
  only); Q-notation nearly absent (Q31 exactly once); scaling instruction-encoded (the
  S-family's <<1+saturate) — and the `s`-bit trap measured (it's the A/B side-select).
- The first classification for `.7`: register GROUPING with a width+fill rule is the one
  candidate abstraction change; no accumulator/guard state is needed for these targets.
  Evidence: docs/tasks/artifacts/dsp-review/2026-09-30-widths-q1-q2.md.
- The tree's stale G1 blocker repaired; the tree is active; LIVE_STATUS's P2 row (stale
  at 8/9 from a mid-flight script abort) corrected to Done 9/9.

## SEMULITH-PS-0084 (leaf P2-SCALAR.9, slice c) — the CPU-LAB report stands; the tree CLOSES 9/9

- `gate_report.py` gained `build_cpulab`: the full processor-gate series per axis
  (SCP-05 — never rolled up; "supports RV64I" appears nowhere), every probe static over
  tracked artifacts (byte-stable in a fresh clone), the dossier content digest as the
  versioned artifact's identity. The generated `GC-REPORT.md` reads **`incomplete`**,
  naming the measured open axes: G-CONTRACT (0/72 obligation checks implemented) and
  G-OBLIGATIONS (28 requirements `planned`, 1 `partial`). Green with their measurements:
  G-TRACE, G-INTERACTIONS (21/21), G-REGRESSION (ACT4 51/51 + the corpus + the mutation
  suite), G-PORTABILITY (`passed` under the bridge), G-REPLAY (bundles + snapshots).
- The named release decision (`decision_release-rv64i-lab-v0`): **rv64i-lab-v0 v0 is an
  EXPERIMENTAL release of the versioned evidence artifact — NOT an accepted profile**;
  the closing conditions are named (the 72 fixtures, the status re-derivation, the
  bare-metal CI leg).
- One defect fixed in flight: the G0 generator's hardcoded "No CPU model exists" — prose
  written at P0, stale since the interpreter landed; the limitation now reads true, and
  GATE-REPORT holds all three generated reports in sync. MEMORY.md's active-trees count
  had drifted at 6/9 across two commits — corrected at closure.

## SEMULITH-PS-0082 (leaf P2-SCALAR.9, slice b) — the Rosetta proof: the x86-64 leg green, `portability: passed`

- The director's Rosetta install landed (VLC's Intel build triggered it); re-measured
  live: `arch -x86_64` prints `x86_64`. The instrument's x86-64 leg learned the bridge
  path: cross-compile `x86_64-apple-darwin`, run under translation, and compare the
  digest manifest against the aarch64 recording — **byte-identical** (`0670a01b…`).
- The full four-leg run reads **passed** (native green, x86-64 green under translation,
  Miri green, cross-endian green); `portability.sexp` re-measured to `passed`, with the
  translation-vs-bare-metal nuance and the fall-2027 horizon on the record.
- Slice (a)'s checklist claimed a `plan/p2.md` line that commit did not carry — the
  drift is recorded and the `.9` book section lands with this commit instead.

## SEMULITH-PS-0081 (leaf P2-SCALAR.9, slice a) — the CI two-host matrix wired; Rosetta measured LIVE

- `.github/workflows/portability.yml`: the host matrix (`ubuntu-latest` x86-64 +
  `macos-latest` aarch64) each running the native leg and uploading the digest manifest;
  the Miri + cross-endian job on x86-64 (nightly provisioned by the workflow); the
  `agree` job byte-comparing both manifests. The instrument gained `--leg` /
  `--emit-manifest` selectors (native-leg manifest measured reproducing the `.8`
  recording byte-identically, `0670a01b…`).
- **Rosetta measured LIVE** mid-slice: the director's install (VLC's Intel build
  triggered it) — `arch -x86_64` now prints `x86_64`, the probe binary runs. The bridge
  is up; slice (b) runs the leg through it next.
- CI evidence lands at the next approved push — the cadence governs.

## SEMULITH-PS-0080 (leaf P2-SCALAR.9, design) — the CPU-LAB release: three slices designed

- (a) The CI two-host matrix: a new `portability.yml` workflow (`ubuntu-latest` x86-64 +
  `macos-latest` aarch64 + a Miri job + the manifest-agreement job); the instrument gains
  `--leg`/`--emit-manifest` selectors. CI evidence lands at the next approved push.
- (b) The Rosetta-local proof when the director's reinstall lands (measured inert today:
  payload in the cryptex, daemon off).
- (c) The release report — measured first: G-CONTRACT's obligation-check implementation
  state decides whether the honest decision can read "accepted" even with portability
  green.
- Ceiling obeyed again: the `.8` checklist archived at the `.9` design commit.

## SEMULITH-PS-0079 (leaf P2-SCALAR.9) — the release route decided; Rosetta measured inert pending reinstall

- The director answered the release fork: CI two-host matrix (permanent home of the
  mandatory x86-64 leg: `ubuntu-latest` + `macos-latest`, the digest manifest the
  byte-exact contract) + Rosetta-local proof (the bridge) — recorded in
  `decision_release-route-x86-64-leg`. No narrower host policy.
- Measured refinement of the `.8` record: Rosetta on this host is PRESENT BUT INERT —
  binaries at `/usr/libexec/rosetta/`, the x86-64 dyld cache in the Rosetta cryptex, the
  oahd daemon not running, `arch -x86_64` failing (`Bad CPU type in executable`);
  activation is the director's admin act (a reinstall is coming). The horizon is on the
  record: Apple phases Rosetta out fall 2027 — nothing may be built on the bridge.

## SEMULITH-PS-0077 (leaf P2-SCALAR.8) — the portability matrix: three legs green, the honest `incomplete`

- `scripts/check_portability.sh` runs the four legs and ends with the honest verdict:
  native aarch64 green (the commit gate's run + the digest manifest over the 49 guests'
  `demo --json` fingerprints — the contract the second host must reproduce
  byte-identically), Miri green 65/65 interpreted, cross-endian green 65/65 on
  big-endian powerpc64 under Miri — and the mandatory x86-64 leg measured UNAVAILABLE
  (Rosetta absent), so the verdict is `incomplete` and the profile stays experimental.
  Recorded, never waived (EVIDENCE_AND_GATES.md §7's own clause).
- The record: `profiles/rv64i-lab-v0/portability.sexp` (baseline.sexp's plain-atom
  shape). The verdict logic carries 6 self-test arms (6/0); the instrument is NOT a
  commit gate (nightly + host-measuring).
- Two authoring REDs, both measured: `grep -q` under `pipefail` SIGPIPEd cargo and read
  every leg red against a green reality (capture-then-read now); a script edited
  mid-run broke its own parse (bash reads incrementally — restart, never edit in
  flight). One drift caught and owned: the model book's bench-arm count had gone stale
  (44 → 53) across two leaves.

## SEMULITH-PS-0076 (leaf P2-SCALAR.8, design) — the portability matrix: availability measured first

- Measured, not assumed: x86-64 is UNAVAILABLE on this host (`arch -x86_64` → `Bad CPU
  type in executable`, Rosetta absent; no qemu user-mode runner) — the mandatory leg
  reads UNMET, recorded not waived; the profile stays experimental per the acceptance.
- Miri measured present and green: 65/65 core suites interpreted natively AND 65/65 on
  `powerpc64-unknown-linux-gnu` (big-endian) — the cross-endian leg holds. The one
  `unsafe` island (bench's counting allocator) excluded by name.
- The design: `scripts/check_portability.sh` (four legs, honest `incomplete` verdict,
  not a commit gate) + `portability.sexp` in `baseline.sexp`'s plain-atom shape.

## SEMULITH-PS-0075 (leaf P2-SCALAR.7) — mid-execution snapshots: replay proven for the implemented boundaries

- `semulith-verify::snapshot` + the CLI pair `snapshot`/`resume`: the record carries the
  definition-identity pins (the bundle's own pin check, extracted and shared), the region,
  entry, step index, the register file + pc, and the memory sparse-encoded and digested.
  The completeness claim is the pinned hidden-state census: registers + pc + memory is ALL
  the pending state this profile has — anything more is not offered (the acceptance's
  second arm).
- The proof: every tracked guest split at three points (early/middle/penultimate), resumed
  through the JSON round-trip, continuations identical — steps AND crossing logs. RED
  arms: corrupted run (digest), foreign definition (pin), incoherent/overrunning/partial
  records — each refused by name. 175 → 180 verify suites.
- One in-flight RED, the author's test arithmetic: the sparse encoding splits at zero
  bytes (the first run is one byte), so the overrun tamper needed one-past-the-end.
- CLI measured end-to-end: `dir-memwalk.elf` snapshotted at step 13 resumes the copy loop
  exactly (24 continuation steps, stop Trap).

## SEMULITH-PS-0074 (leaf P2-SCALAR.7, design) — mid-execution snapshots, designed on the pinned census

- The design's pending-state census is not new work but the pinned dossier's own:
  `state.sexp`'s hidden-state census measured all seven candidates absent, so a complete
  snapshot for this profile is exactly registers + pc + memory — anything more is "not
  offered at all", the acceptance's second arm.
- The mechanism: a `Snapshot` record (definition-identity pins, region, entry, step k,
  the register file + pc, sparse-encoded memory), JSON via the crate's own reader; the
  proof suite runs every guest's continuation twice (snapshot+continue vs
  restore+continue) with RED arms on corrupted/foreign snapshots; the CLI mirrors
  bundle/replay (`snapshot`/`resume`).

## SEMULITH-MM-0073 (leaf MODEL-METHOD.14) — the encoding re-sourcing probe: adopt-in-principle, measured

- The probe (untracked `target/materials/mm14_probe.py` over the pinned PDF's text
  layer): Chapter 36's listings carry every field as selectable text; ADD reconstructs
  end-to-end identical to the incumbent fragment; the full sweep measures **52/52
  opcodes extracted, zero value conflicts, 37/52 fully reconstructed by the naive
  parser** — the 15 remainders are parser-ordering gaps (page-local alignment), each
  caught by the incumbent comparison, which is the verification control.
- Decision recorded (`decision_encoding-resourcing-probe`): adopt-in-principle; the
  re-source is a later reviewed leaf (`.8` owns the encoding), triggered when the
  encoding is next touched or a second unit reuses the fragment. The re-sourced
  provenance would shrink the shared-with-spike ancestry leg.
- **The tree CLOSES 17/17.** Closure sweep found `.15`/`.17`'s Status fields stale
  (`active` with Results landed) — drift corrected.
- `MODEL-METHOD` leaves the active index; `P2-SCALAR.7` (snapshot/replay) is next.

## SEMULITH-PS-0072 (leaf P2-SCALAR.6) — the minimized divergence is retained; the leaf is DONE

- `min-fencei` — one word (`0x0000100F`) — reproduces the corpus's one model-vs-references
  divergence (`DIFF-FENCEI-EXECUTED`): the policy trap at step 0, the expected-divergence
  protocol green against EACH reference, the references agreeing over their full length
  (the nop, then the measured run-off-the-end illegal word). 175 verify suites; the
  matrix's F×E cell gains the guest; the difference record names the retained case
  (`references.sexp` at 32,765/32,768 — the note written to fit, the ceiling unmoved).
- No discrepancy was closed by widening a mask or editing an expectation (EVD-05/AI-05):
  the census found none tempting either. The seven non-model differences stay
  dispositioned with citations.

## SEMULITH-PS-0071 (leaf P2-SCALAR.6, design) — the discrepancy census: exactly one divergence to minimize

- Every recorded difference dispositioned with its citation (harness ×2, trace
  vocabulary, sub-granularity observable, the corrected platform-configuration defect,
  the board-layer difference, one reference-vs-reference mask) across all four corpora
  (48 guests / 642 steps, ACT4 51/51, the offline differential, the mutation suite):
  **one genuine model-vs-references divergence exists — `DIFF-FENCEI-EXECUTED`**.
- The minimization design: `it-fencei`'s three words reduce to ONE (`0x0000100F` alone) —
  the policy trap at step 0, the references nop and run off the end into the measured
  illegal zero word. Retained as `min-fencei` (expect_divergence at_step 0). The reducer
  is deliberately not the tool (it minimizes against mutations, not reference
  differences).

## SEMULITH-PS-0070 (leaf P2-SCALAR.5, strand 3) — the directed sequences; the leaf is DONE

- Eight directed guests from the measured census, every expectation derived before any
  run: `dir-runoff` (semulith's first run off a program's end — the zero word's policy
  trap, three-way identical), `dir-chase` (load→use as ADDRESS: the pointer chase and the
  jump through memory — the idiom that existed nowhere), `dir-ext-matrix` (the
  cross-width sign-extend matrix at the sign edges), `dir-selfmod-fence` (the patch
  visible through `fence rw,rw` — probed on all three models before authoring),
  `dir-cmp-branch` (all four senses on fresh predicates), `dir-memwalk` (the load+store
  loop), `dir-chain` (14 varied serial links), `dir-x0-writes` (every unpinned producer
  to x0). **150 new aligned steps, all three-way — 642/642 over 48 assembled guests**,
  byte-identical reproduction; the matrix's cells assigned (orphan rule green); the
  census pins the 55 new data crossings; 174 verify suites.
- Two authoring REDs caught by the offline differential, never a model defect:
  `dir-ext-matrix`'s data cell sat inside the code its stores patched (moved past the
  code end); one hand-typed constant re-derived.
- The census's defect is fixed and closed: `c-scope.c`'s comment overclaimed its
  constant-folded ELF (no jump table exists in the artifact) — the comment and the model
  book's chapter corrected, and the promised idiom became `dir-chase`'s measured guest.
- **`.5` is done** — all three strands landed: the compiled C guest (G1 `passed`), the
  ACT4 campaign (51/51, recorded and gated), the directed sequences. The frontier moves
  to `.6` (discrepancy reduction).

## SEMULITH-PS-0069 (leaf P2-SCALAR.5, strand 3 design) — directed sequences: the gaps measured, the design recorded

- The strand-3 design stands on a measured census (tracked corpus + the `c-scope.elf`
  disassembly + the ACT4 testplan): eight genuine gaps, each with its citation — semulith
  never running off a program's end, load→use-as-address (the jump-table idiom exists
  NOWHERE, not even in the compiled guest), the cross-width sign-extend matrix,
  store→fence→execute, compare→branch, the load+store loop, 12-deep varied chains, and
  the unpinned x0 producers.
- Two probes measured the uncertain behaviors before any guest exists (`run_probes_p25s3.py`):
  run-off-the-end traps illegal-instruction (0x02/tval 0) identically on all three models,
  and a self-modifying store stays visible through `fence rw,rw` on all three.
- One defect found by the census and logged: `c-scope.c`'s comment overclaims its ELF
  (constant folding removed the switch's indirect jump) — correction scheduled in-strand,
  the promised jump table becoming a real guest (`dir-chase`).
- Ceiling bookkeeping: `.4`'s checklist joined the archive (per-part ceiling obeyed).

## SEMULITH-PS-0068 (leaf P2-SCALAR.5, strand 2c) — the ACT4 RV64I campaign: 51/51, three-way, recorded and gated

- The full pinned suite ran green on the first fleet run: **51/51 test files, every HTIF
  verdict pass on all three models, every signature agreeing slot-for-slot — semulith vs
  the Sail-derived expectations AND spike vs sail (the control pair), 17,017 slots in
  sum.** The slot census reconciles exactly against the static sigupd counts (dead-path
  branch instances, store read-back slots, the final-offset word — all measured).
  `I-fence-00` (reserved-`fm`, `fence.tso`, HINTs) passes: DEFECT-A's inversion has
  external-suite confirmation.
- The record: `profiles/rv64i-lab-v0/act4.sexp`, emitted by the runner's `--record` from
  measured rows (never hand-typed), behind the new `schema/act4.sexp` family.
  RECORD-SCHEMA gained rule 13 (CAMPAIGN): every carried count re-derives from the rows
  and the verdict vocabulary is closed — five new self-test RED arms, 39/0.
- The EVD-04 framing is on the record: external tests with Sail-derived expectations —
  one semantics answering twice by construction; the value is that somebody else chose
  the tests. The model book's evidence chapter and materials section carry the campaign;
  the claim-scope page's "no ACT suite" row is corrected.
- Ceilings re-derived per the design's reviewed expansion: `profiles/` 100 files /
  427,926 B (ceiling 104, bytes unchanged at 0.83×), `schema/` 17 files.

## SEMULITH-PS-0067 (leaf P2-SCALAR.5, strand 2b) — the ACT4 harness: one test end-to-end three-way

- `semulith run` learned `--trace-stores`: the runner's crossing log (already recorded
  per step) is surfaced as `mem[W,0xADDR] <- 0xVALUE` lines — an observability option;
  the interpreter and the semantics data are untouched.
- The laboratory's DUT-side ACT4 pieces stand (`profiles/rv64i-lab-v0/act4/`):
  `rvtest_config.h` (the minimal measured define set — `UDB_MXLEN 64` alone; every
  privileged/FP path compiles out), `rvmodel_macros.h` (the check_defines-required
  names; the interrupt macros documented inert — no I-suite test executes them),
  `link.ld` (the lab's declared memory map, identical to the matched sail override).
- `scripts/fetch_act4.sh` is the reproducible acquisition route (pin-verified, refuses
  a drifted clone, census 51 files / 18,092 sigupds).
- `scripts/run_act4_campaign.py` builds and runs `I-add-00` end-to-end three-way: both
  toolchain risks retired by measurement (clang 21.1.8 assembles the suite clean; sail
  0.14's HTIF terminates under the lab override), all verdicts pass, the 513-slot
  signature agrees semulith↔sail-derived AND spike↔sail. The harness carries RED/GREEN
  controls (self-test 7/0).

## SEMULITH-PS-0066 (leaf P2-SCALAR.5, strand 2a) — ACT4 acquired sparse; strand-2 design recorded before code

- The pinned suite's generated half landed as a blobless sparse clone at `e2216915…`
  under `target/refs/riscv-arch-test/` (untracked: `tests/env` + `tests/rv64i/I` +
  `config`, 45 MB of the ~672 MB tree) — measured: 51 RV64I test files, 18,092
  `RVTEST_SIGUPD`s, 14,820 testcases.
- Strand-2 design recorded before code: signature-mode build; the CLI learns a store
  trace from the runner's crossing log; Sail-derived expectations per `EVD-04`, spike
  the control pair; DUT-side `rvtest_config.h` / `rvmodel_macros.h` / `link.ld` under
  `profiles/rv64i-lab-v0/act4/`; three slices.
- Acquisition facts synced: `references.sexp` (act4 → `acquired (sparse partial)` + pin;
  PROFILE-CONSISTENCY's vocabulary extended), the catalogue note, both books. Per-part
  ceiling obeyed: `.4`'s design moved to the tree archive (live file was 64,310/65,536).

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

