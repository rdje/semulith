# P1-LAB — archived completed-leaf evidence (part 2 of 2)

Continuation of [`P1-LAB.md`](P1-LAB.md) — same tree, same rules (the family per-part ceiling fired at 65,617 bytes on `2026-09-29` when `.12`'s checklist landed, so the archive split; the ceiling was obeyed, not raised). Part 1 holds the `.1`–`.9` checklists; this part holds the `.10`–`.12` checklists and the `.7`–`.11` design detail.

## Acceptance Checklist (leaf P1-LAB.10)

- [x] **REPRODUCE / ISSUE** — G-REPLAY's demand as it stood after `.9`: a divergence the
  differential caught existed only as a test's in-memory value — nothing recorded the inputs
  that produced it, so "failures are replayable from recorded inputs" (gate `G1`'s first
  criterion) and T007's "replay/reduction preserves mismatch" had no artifact and no
  minimizer at all:

  ```
  $ git ls-files 'crates/*' | xargs grep -ln "Bundle\|ddmin\|first-divergence retention" | wc -l
  0                    # no recorded input bundle; no reducer; the vocabulary existed in run.rs only
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — `.8`/`.9` built the observation vocabulary, the
  comparator, and the mutation seam, but a result was never *recorded*: there was no type
  carrying what ARCHITECTURE §7 says identity is — code/generator versions, initial state,
  guest image, environment policy, event choices — so no run could be re-derived from
  recorded inputs, and EVD-02's minimized discrepancy had no minimizer to produce it. WHERE,
  measured at the parent commit:

  ```
  $ git grep -n "pub fn replay\|pub fn reduce" HEAD -- crates/ | wc -l
  0                                            # the recorder and the minimizer existed nowhere
  $ git ls-files 'crates/*' | xargs grep -ln "struct Bundle" | wc -l
  0                                            # nothing recorded a run's inputs
  ```

- [x] **FIX** — `semulith-verify::replay`: the `Bundle` (algorithm pins flattened from
  `definition::MANIFEST` + harness version + `production`/`mutant:<name>` model, platform
  region, entry, image words with a sha256 guard, the recorded event choice
  `DeclaredNone { OB-ENV-EVENT-DELIVERY }`, the step budget, and the recorded steps + stop
  render), JSON both ways through the crate's own reader/writer, and `replay()` that checks
  identity by name and then walks recorded-vs-replayed through `run::compare`.
  `semulith-verify::reduce`: the ddmin minimizer over the guest word sequence, retention =
  the original first divergence exactly (same step, same field), with the structural
  invariant that every accepted removal retains. `semulith-cli` gains `bundle`, `replay`,
  and `reduce`. No core change — the `.9` table seam is reused as-is.

- [x] **ADDRESSED (verified)** —

  ```
  $ cargo test -p semulith-verify 2>&1 | grep "test result"
  test result: ok. 114 passed; 0 failed; ...   # +15 replay suites, +6 reduce suites
  ```

  All four tracked guests replay identically under the production model (round-trip through
  JSON, mutant bundle included); every tamper arm — image word, entry, region, budget,
  generator pin, input pin, dropped pin, scripted event claim, missing accompaniment — is
  refused or named-mismatched; zext-addi minimizes to the 2-word prefix (x1 @ step 1),
  jal-no-link to 4 words (x5 @ step 7), jalr-odd-bit to 9 words (trap @ step 10, tval
  0x80000029 re-derived from the minimized program — the fixture note's prediction,
  retained); every minimized result carries an exhaustive 1-minimality witness; phantom-load
  is refused `NoDivergence` by name (the census class is not reducible on observations).
  CLI exercised end to end: `bundle` → `replay` identical (rc 0), `reduce` prints the
  minimized program, a hand-corrupted bundle is refused with the digest named (rc 1).

- [x] **NO REGRESSION** — `cargo fmt --all -- --check`, `clippy -D warnings`, `cargo test --all`
  (5 suites ok, 65 core + 114 verify), wasm build rc=0, `make gate` green; the live file
  stays under the per-part ceiling by archiving `.9`'s checklist (P1-LAB.md ≤ 65,536;
  archive holds the unedited `.1`–`.9`).

- [x] **LOCKSTEP** — `MEMORY.md`, `CHANGELOG.md` (+shard), `LIVE_STATUS.md`, `DEV_NOTES.md`
  (+shard), `docs/TASK_TREE.md` (10/12), the book's P1 chapter ("Replay and reduction" now
  describes the landed machinery), and this tree — one commit. No doctrine-registry change:
  no new doctrine, no generated artifact.
## Acceptance Checklist (leaf P1-LAB.11)

- [x] **REPRODUCE / ISSUE** — gate `G1`'s fifth criterion ("the performance baseline is
  measured") and ARCHITECTURE §6's three benchmark modes had no instrument at all: nothing
  could run an execution mix, count its allocations, or compare traced against untraced.
  Measured at the parent commit (`0d12c75`):

  ```
  $ git grep -c "run_untraced\|Mix::Arithmetic\|run_diagnostic" HEAD -- crates/ | wc -l
  0                                 # no harness, no mixes, no modes
  $ git grep -n "semulith bench" HEAD -- crates/semulith-cli/src/main.rs | wc -l
  0                                 # no command surface either
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — `.8`/`.9`/`.10` built execution, mutation and replay,
  but every runner in the tree was correctness-oriented: `run::run_over` stops at the first
  trap (so a fault-heavy mix could not even be driven), nothing constructed the three
  ARCHITECTURE §6 modes as separately measurable cells, no allocation counting existed
  anywhere (the crate's zero-dependency rule rules out the usual benchmarking crates —
  RUST-01 makes the harness ours), and the static-vs-dynamic observer question was parked
  precisely because nothing could measure it. WHERE: the runner family lived only in
  `crates/semulith-verify/src/run.rs` (stops at first trap, always records crossings —
  one fused mode), and no bench/alloc/statistics code existed (`git grep` above).

- [x] **FIX** — `semulith-verify::bench`: the four programmatically generated mixes (every
  word decode-round-trip-pinned to `definition::decode`), the counting environment wrapper
  (`Census`), the stated harness policy for the fault mix (delivered exception → observe,
  resume at pc+4; requested trap → stop; fetch fault → stop silent, run.rs's rule),
  `run_untraced` / `run_instrumented<O: Observer + ?Sized>` / `run_diagnostic` (sharing
  `run`'s snapshot/diff/trap-mapping/`Recording` as `pub(crate)` — the measured modes ARE
  the production observation construction), `agree` (RUST-02 as data), the `alloc`
  counting allocator (std-only, installed by the CLI binary and the verify test binary,
  never the wasm cdylib), and `stats` (min/median/mean/max + spread). `semulith-cli` gains
  `bench` — names the host, runs warmup+reps per cell, checks RUST-02 as it measures
  (disagreement is exit 1), prints the noise table, sets no threshold. No core change.

- [x] **ADDRESSED (verified)** —

  ```
  $ cargo test -p semulith-verify 2>&1 | grep "test result"
  test result: ok. 124 passed; 0 failed; ...   # +10 bench suites
  $ cargo build --release -p semulith-cli && ./target/release/semulith bench
  host: Apple M4 Pro; Darwin 27.0.0; rustc 1.95.0 (59807616e 2026-04-14)
  mix arithmetic: untraced 52.1 / instrumented 69.6 / dyn 69.6 / diagnostic 73.4 ns/step,
    allocs/step 1.00 -> 1.19, spread 1.7-3.6%
  mix control:    47.2 / 65.4 / 65.5 / 70.1, 1.00 -> 1.42, spread 4.6-6.0% (one 113%
    scheduler outlier on a millisecond-scale cell)
  mix memory:     54.1 / 71.0 / 70.9 / 76.9, 1.00 -> 1.23, spread 3.9-6.5%
  mix fault:      50.9 / 69.4 / 67.5 / 71.0, 1.00 -> 1.20, spread 4.6-7.4%
  static vs dynamic observer dispatch: x0.974-1.002 across the mixes
  bench: measured; every mode agrees on every mix (RUST-02 holds)   # rc=0
  ```

  Every generated word decode-round-trips to its intended instruction; each mix's census
  proves its class (arithmetic/control touch no data memory; memory: 7 loads + 4 stores
  per iteration; fault: causes 04/06/05 per iteration in order — the misaligned pair never
  crosses the boundary — plus the closing EBREAK); the delivered-exception policy is
  pinned (the step after a misaligned load is observed at pc+4); mode agreement holds for
  every mix at test budgets; the allocator counts a known allocation; the stats are pinned
  on known inputs; a pc outside the image is refused by name.

- [x] **NO REGRESSION** — `cargo fmt --all -- --check`, `clippy -D warnings`, `cargo test
  --all` (5 suites ok, 65 core + 124 verify), wasm build rc=0, `make gate` green; the live
  file stays under the per-part ceiling by archiving `.10`'s checklist (P1-LAB.md ≤ 65,536;
  the archive holds the unedited `.1`–`.10`).

- [x] **LOCKSTEP** — `MEMORY.md`, `CHANGELOG.md`, `LIVE_STATUS.md`, `DEV_NOTES.md`,
  `docs/TASK_TREE.md` (11/12), the book's P1 chapter ("The performance baseline" now
  carries the measured table), `TOOLBOX.md` (the `semulith bench` row), and this tree —
  one commit. No doctrine-registry change: no new doctrine, no generated artifact.
## Design detail (leaf P1-LAB.7)

  Design (recorded before code, `2026-09-28`): the checker lands in `semulith-verify`
  (`docs/ARCHITECTURE.md` §4 assigns "source/evidence graph, adapters, comparators, reducer"
  there; the crate "does not supply production instruction semantics" — checking evidence is
  not a semantic rule). Four support modules plus the checker: `json` (a JSON reader — the
  verify crates carry no dependencies, so the reader is ours, with `scripts/validate_records.py`
  as the reference contract), `pattern` (a regex subset — exactly the constructs the three
  tracked schemas' patterns use, refusing anything else by name), `sha256` (FIPS 180-4,
  std-only — re-deriving the synthetic source fingerprint), and `schema` (the same keyword
  subset as the Python validator, unknown keywords REFUSED; `additionalProperties` as a schema,
  which the Python tool silently skips, is enforced — a tightening, verdicts unchanged on the
  frozen corpus, proven by running both). `graph` is the checker itself: pure functions over
  parsed records (no `std::fs` in the library — the workspace builds for `wasm32-unknown-unknown`
  and evidence bytes arrive as `&[u8]` through an injected resolver). `semulith-cli` owns the
  command surface (`check-examples`, report presentation per §4) and `RECORD-SCHEMA`'s JSONL
  arm runs both engines, Python and Rust, so the PACKAGE_CHECKS rows are re-derived by the
  gate itself, not cited.


## Design detail (leaf P1-LAB.8)

  Design (recorded before code, `2026-09-28`): three pieces, each on its owning side of the
  `docs/ARCHITECTURE.md` §4 map.
  1. `semulith-core::exec` — the definitional interpreter: `step(&mut ArchitecturalState, &mut
     impl Environment) -> StepOutcome`. Fetches through the environment contract, decodes with
     `.6`'s `decode`, extracts operands (scatter-aware, with the binding rule `.6` documents:
     `imm12hi`/`imm12lo` → `imm12`, `bimm12hi`/`bimm12lo` → `bimm12`, either shift field →
     `shamt`), and evaluates the instruction's `Sem` tree — the semantics DATA stays the one
     executable owner (OWN-01); the interpreter is its evaluator, not a second implementation.
     Expression evaluation carries an explicit **width** (the semantics file's own rule:
     "WIDTHS ARE ALWAYS EXPLICIT"): `sext`/`zext N` extend FROM the operand's own width TO `N`
     (which is what makes `sext 64 (shl (imm imm20) (lit 12))` the LUI sign-extension from bit
     31, and `sext 64 (load …)` the LB extension from 8 — the two readings that make every one
     of the 52 trees correct at once); shifts of a literal widen by the literal amount. Outcome
     mapping: misaligned branch/jump target → `InstructionAddressMisaligned` reported AT the
     target value, raised on the branch (REQ-D-IALIGN, REQ-D-MISALIGN-REPORT); fetch
     access-fault → `InstructionAccessFault` at the pc (REQ-D-FETCH-FAULT-REPORT); a misaligned
     or faulting load/store raises its exception before/at the boundary without substituting
     (D-MISALIGN-DATA, D-MAIN-VS-IO); reserved decode → `UndefinedCase::ReservedDecode`
     (D-RESERVED-DECODE — reported as the unspecified case it is, never auto-converted);
     ECALL/EBREAK → `RequestedTrap` with the cause vocabulary's codes 11/3 (REQ-D-ECALL-EBREAK).
  2. `semulith-verify` — the observation runner and the first-divergence comparator, on the
     four tracked guests (`smoke-arith`, `guest-control`, `smoke-trap`, `guest-no-device`).
     A step is `(pc, word, register writes, trap)` — the same normalized observation vocabulary
     `scripts/compare_traces.py` already reduces the references to — and `first_divergence`
     walks two streams and names the first differing observation (pc / insn / a register write /
     the trap cause or tval), or reports a length mismatch as a non-agreement, never a prefix
     pass. The guests and their specification-derived expectations become a GENERATED Rust
     fixture (`scripts/gen_guests.py` → `semulith-verify/src/guests.rs`, the 23rd doctrine
     `GUEST-GEN` refuses drift), so the commit gate re-runs the whole slice offline: every
     expectation value the guests carry was derived from the pinned specification prose
     (EVD-05), not from any model's output.
  3. `semulith-cli` — `semulith run <elf>`, a minimal ELF64 loader + the runner + a normalized
     trace print, so the live three-way experiment (`scripts/run_semulith_smoke.py` — semulith
     vs sail-riscv vs the pinned expectations, NOT a commit gate, same standing as
     `run_smoke.py`) compares all models through the one vocabulary.


## Design detail (leaf P1-LAB.9)

  Design (recorded before code, `2026-09-28`): eight designated classes plus the ninth arm the
  `guest-control.expected.sexp` note names — JALR keeping its odd bit, the one observation the
  two references can never discriminate (both clear the bit). Two injection levels, chosen by
  fidelity, each arm naming its injection, its detection instrument, and its designated
  divergence (step + field):
  1. **Model-level, through one new seam.** `semulith-core::exec` gains
     `step_over(state, env, insns: &[InsnDef])`; production `step` delegates with
     `definition::INSNS`, and the table scan applies exactly the predicate the generated
     `definition::decode` documents (`word & mask == value` — the generated body IS that scan),
     so the production path is unchanged and OWN-01 holds structurally: a mutation is *data the
     one evaluator consumes*, never a second implementation. `semulith-verify::run` gains the
     mirroring `run_over`. The suite (`semulith-verify::mutate`) builds a mutated table by
     copying `INSNS` and swapping one row — either the decode row (`mask`/`value`) or the
     effect pointer (a mutated tree rebuilt from the real tree by a small transformer, leaked
     test-locally, bounded). Arms at this level: **wrong sign extension** (addi's
     `(sext 64 …)` → `(zext 64 …)`; guest-control diverges on x1 at step 1); **suppressed
     register write** (jal's link `set` dropped; guest-control diverges on the missing x5 write
     at step 7); **the JALR odd-bit arm** (the `(and … (lit -2))` LSB-clear dropped from
     `set-pc`; guest-control diverges on the `InstructionAddressMisaligned` trap at step 10,
     tval `0x80000029` — the fault the fixture note predicted); **wrong trap cause** (ebreak's
     `(lit 3)` → `(lit 11)`; a suite-local `[ebreak]` program diverges on the cause at step 0);
     **extra memory access** (addi prepended with a discarded phantom byte load at a mapped
     address; the architectural trace is UNCHANGED — `compare` still agrees — and the pinned
     per-guest data-crossing census detects the extra `Load`; the suite pins that census for
     all four guests, justified from their `.s` sources); **overbroad mask** (srai's
     `mask`/`value` cleared at bit 30, the SRLI/SRAI discriminator; the suite proves the
     hidden-bit witness — srli's canonical word now matches the mutated srai row — and a
     suite-local `[addi, slli, srli]` program diverges on x1 when srli executes as srai).
  2. **Observation/outcome-level, where a faithful model-level seam would be a second
     implementation.** Documented per arm: **illegal-opcode substitution for a model
     limitation** (SEM-02: a limitation is carried as the undefined case — the arm removes
     fence's decode row and verifies the honest outcome is `UndefinedCase::ReservedDecode`,
     never a trap — then substitutes the fabricated `IllegalInstruction` observation, cause 2
     with tval = the word, and asserts the differential against the full-model reference
     diverges at step 0 naming the trap); **shifted event delivery** (the deferred-trap
     observation stream — smoke-trap's step-2 trap moved to a fabricated step 3 — diverges at
     the due step naming the missing trap); **stale reference configuration** (a reference run
     at a stale entry diverges at step 0 naming the pc) and **unjustified comparison
     suppression** (a writes-blind comparator variant is shown to AGREE with the sign-extension
     mutant that the real comparator catches — the writes leg is load-bearing, EVD-09's second
     half).
  Detection instruments are all real and already gated: `compare`/`render` verdicts (field and
  step named), the run's boundary-crossing census, and the pinned GUEST-GEN expectations as the
  GREEN anchor for every guest arm (the real model meets them in each arm before the mutant is
  judged). No new doctrine: the suite is Rust tests under `make check`, the same standing as
  the run suites — it guards discriminating power, not drift, so there is no generated artifact
  to refuse. Files owned: `crates/semulith-core/src/exec.rs` (+ its tests),
  `crates/semulith-verify/src/run.rs`, `crates/semulith-verify/src/mutate.rs` (+ tests),
  `crates/semulith-verify/src/lib.rs`.


## Design detail (leaf P1-LAB.10)

  Design (recorded before code, `2026-09-28`): two pieces, both on the verify side per
  `docs/ARCHITECTURE.md` §4 ("adapters, comparators, reducer" — replay is evidence machinery
  beside them; no core change, the `.9` table seam is reused as-is).
  1. `semulith-verify::replay` — the recorded input bundle (G-REPLAY's "recorded definitions,
     tools, inputs, and event choices"; ARCHITECTURE §7's "a seed without the generator version
     and event stream is insufficient"):
     - `Bundle { algorithm, platform, entry, image, events, budget, recorded }`, JSON both
       ways (hand-rolled writer like `report::to_json`; parsed through the crate's own `json`
       reader with named-field errors — a document missing any accompaniment fails parse
       naming the field, so the bare-seed refusal is structural, not policy).
     - `algorithm` — the identity, flattened from `semulith-core::definition::MANIFEST` at
       record time (profile, ilen, generator name+sha256, every input pin) plus the harness
       version and the `model` under test (`"production"` or `"mutant:<name>"` resolved
       through `mutate::table_for`). At replay every pin is re-compared against the live
       MANIFEST and a mismatch is refused by name; an unknown mutation name likewise.
     - `platform` — the FlatMemory region declaration `{base, size}` (the environment
       policy); `entry` — the laboratory reset's pc (x1..x31 = 0 is the profile's declared
       reset, REQ-D-ENTRY-STATE, so it rides as documentation, not data).
     - `image` — the guest words plus the sha256 of the little-endian image bytes, recomputed
       and compared at replay (a tampered word is refused by name).
     - `events` — the actual relevant event choices, recorded as data:
       `DeclaredNone { obligation: "OB-ENV-EVENT-DELIVERY" }` is this platform's choice (no
       asynchronous event exists). Any other claim is refused by name as not-this-platform;
       scripted-env replay joins when a tracked consumer needs it (Open Question below).
     - `budget` — the step bound; `recorded` — the result: the observation steps plus the
       stop's canonical render, compared rendered (deterministic Debug; Failed/Undefined
       stops carry data no round-trip could rebuild typed, and rendering loses nothing).
     - `replay()` rebuilds the environment from the bundle, re-runs the recorded model over
       it, and reports `Replays` or `Mismatch` — the recorded-vs-replay first divergence via
       `run::compare`, step and field named.
  2. `semulith-verify::reduce` — the minimizer (EVD-02's minimized discrepancy; P2's "retain
     minimized discrepancies"):
     - `Case { model, reference, entry, region_size, budget }` — the differential's two
       tables (in the suite/CLI: a `.9` mutant against production `INSNS`), the laboratory
       platform facts, the step bound.
     - `reduce(case, words)`: the property is the first divergence of model-vs-reference on
       the candidate — `compare(reference_steps, model_steps, ("reference", "model"))` —
       and retention is the ORIGINAL divergence exactly: same `at`, same `what`. Identical
       prefix semantics make a same-step retained divergence byte-identical (values, pc,
       tval included); a removal that shifts the step or changes the field is correctly
       rejected. Classic ddmin over word indices (ILEN 32 ⇒ one word = one observation
       step); every accepted removal preserves the property, so the result ALWAYS retains —
       the invariant is structural, and `Reduction { words, retained, evaluations }` carries
       the witness count.
     - Named boundary: a case whose observations do not diverge — the phantom-load census
       arm is the standing example, a wrong behaviour the observation vocabulary cannot
       see — is refused `NoDivergence`: observation reduction cannot retain what
       observations do not carry (the `.9` census lesson, reused).
  3. `semulith-cli` — the laboratory surface: `semulith bundle --guest=X --mutate=Y` writes
     the bundle JSON; `semulith replay <file>` re-derives and judges it; `semulith reduce
     --guest=X --mutate=Y` prints the minimized program with its retained divergence. Exit
     codes keep the `.9` convention: a caught divergence is the tool working, not an error.
  Suite (Rust tests, `make check` — same standing as `.9`; no new doctrine, no generated
  artifact): replay round-trips every tracked guest under the production model and the
  zext-addi mutant; tamper arms (image word, entry, region, budget, manifest pin, event
  claim, missing accompaniment) are each refused by name; reduction minimizes
  zext-addi/guest-control to the 2-word divergent prefix (step 1, the x1 write),
  jal-no-link to the 4-word prefix (step 7, the x5 link write), jalr-odd-bit to the 9-word
  prefix (step 10, `InstructionAddressMisaligned` tval `0x80000029` — the fixture note's
  prediction, retained through minimization); every minimized result carries an exhaustive
  1-minimality witness (no single-word deletion retains), and phantom-load is refused
  `NoDivergence` by name.


## Design detail (leaf P1-LAB.11)

  Design (recorded before code, `2026-09-28`): two pieces, on their owning sides of the
  `docs/ARCHITECTURE.md` §4 map — the harness in `semulith-verify` (measurement is evidence
  machinery beside the comparators; no core change), the command surface in `semulith-cli`.
  1. `semulith-verify::bench` — the measurement harness, four parts:
     - **Workload mixes** (`Mix::{Arithmetic, Control, Memory, Fault}`): `program(mix,
       iterations)` generates the guest words programmatically — encoders local to the
       harness (the same standing as `.9`'s mutated trees; a test pins EVERY word to the
       instruction `definition::decode` names for it). Each mix is a counted loop ending
       in EBREAK: **arithmetic** churns the ALU vocabulary with no memory traffic;
       **control** alternates taken/not-taken branches with jal/jalr; **memory** walks
       sd/sw/sh/sb stores and ld/lw/lh/lb/lwu/lhu/lbu loads over a scratch area;
       **fault** runs a model-side misaligned load and store (raised before the boundary)
       plus an environment-side out-of-region load (the boundary's AccessFault) every
       iteration, so the exception paths are the measured common case. The fault mix runs
       under a stated harness policy: a delivered exception is observed and execution
       resumes at pc+4 (delivery-continues, ARCHITECTURE §5); a requested trap (EBREAK)
       stops the run; the step budget is only a safety bound.
     - **The three modes** (ARCHITECTURE §6's untraced / instrumented / diagnostic):
       `run_untraced` (the bare `exec::step` loop — no observation is constructed),
       `run_instrumented<O: Observer + ?Sized>` (the Step stream built by `run`'s own
       snapshot/diff/trap-mapping, reused `pub(crate)`; the word comes from the harness's
       own image, never a second fetch), and `run_diagnostic` (+ the crossing log via
       `run`'s `Recording`). All modes share one counting environment wrapper so the
       census is comparable without being recorded. The instrumented runner is generic
       over the observer, so the open question — static vs dynamic dispatch — is MEASURED,
       not argued: one function instantiated with `VecObserver` and with `dyn Observer` is
       two cells of the same report.
     - **Allocation counts**: a `GlobalAlloc` wrapper over `System` (std-only, RUST-01),
       installed by the CLI binary and by verify's test binary; the wasm cdylib is
       untouched. Allocations and bytes per step per mix per mode — RUST-03's "no
       mandatory per-instruction allocation" as a number, not a posture.
     - **Noise first** (RUST-04): every cell repeated R times after W warmups; the report
       carries min/median/mean/max and the (max−min)/median spread. No threshold is set
       anywhere — the noise table is the deliverable a future threshold must cite.
  2. `semulith bench [--iterations N] [--reps R]` in `semulith-cli` — names the host (OS/arch,
     the CPU brand where the platform supplies one, the rustc version that built the binary),
     runs the cells, and checks RUST-02 AS it measures: per mix, all modes must agree on step
     count, stop classification, final architectural state and crossing census, and the
     instrumented (static and dyn) and diagnostic Step streams must be identical — a
     disagreement is a refusal (exit 1), not a footnote.
  3. Suite (Rust tests, `make check`; no new doctrine — no generated artifact; the harness
     guards measurement honesty, not drift): decode round-trip for every word; per-mix
     census proving each mix exercises its own class; four-mode agreement at small budgets
     (RUST-02 exercised, not just reported); the allocator counts a known allocation; the
     statistics pinned on known inputs.

## Acceptance Checklist (leaf P1-LAB.12)

- [x] **REPRODUCE / ISSUE** — the tree's final leaf had no artifact: no G1 report existed,
  and the generator had no G1 path. Worse, a drift surfaced while scoping it: this tree's
  G1 acceptance listed five criteria where `ROADMAP.md` §6 states six. Measured at the
  parent commit (`13e42d1`):

  ```
  $ git ls-files profiles/rv64i-lab-v0/ | grep -c "G1-REPORT"
  0                                  # no G1 report anywhere
  $ git grep -c "build_g1" HEAD -- scripts/ | wc -l
  0                                  # no generator path either
  $ ls profiles/rv64i-lab-v0/guests/*.c 2>/dev/null | wc -l
  0                                  # criterion 6's C guest: absent
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — the G0 generator was single-gate by construction:
  `build()` hardcoded the G0 criteria and `G0-REPORT.md`, and its inputs were the dossier
  alone — the laboratory's evidence lives in Rust code and in a baseline that existed only
  as terminal output, never as tracked data (`gate_report.py`'s `main` wrote
  `G0-REPORT.md` unconditionally; no `baseline.sexp` existed anywhere:
  `git ls-files | grep -c baseline` → 0 at the parent). The criteria drift's root cause:
  `ROADMAP-V3.3` sharpened G1 in the roadmap text (the v0.3 revision) and this tree's
  acceptance list — written `2026-09-13` — was never re-synced; nothing gated the
  criterion list against the roadmap (the leaf repaired the content; the absence of a
  roadmap↔tree criteria gate is recorded as the lesson).

- [x] **FIX** — one generator, one drift check, both gates: `gate_report.py --gate G1`
  (default G0 byte-unchanged) with `build_g1` measuring each of the six roadmap criteria
  from tracked files by concrete name; `profiles/rv64i-lab-v0/baseline.sexp` — the `.11`
  measurement frozen as data (the references.sexp experiment-record precedent), validated
  field-by-field by the generator, `(thresholds none)` enforced; `check_gate_report.sh`
  discovers `G?-REPORT.md` per profile and covers both. The tree's G1 acceptance absorbed
  criterion 6 with its standing named. No new doctrine (GATE-REPORT already owns the
  drift check; the registry row's prose now says G0 AND G1).

- [x] **ADDRESSED (verified)** —

  ```
  $ python3 scripts/gate_report.py rv64i-lab-v0 --gate G1
  wrote profiles/rv64i-lab-v0/G1-REPORT.md (5482 bytes)
  $ bash scripts/check_gate_report.sh
  GATE-REPORT: ok (2 generated report(s) in sync with their inputs)
  $ bash scripts/check_gate_report.sh --self-test
  GATE-REPORT --self-test: 6 pass / 0 fail
  ```

  The report reads **`incomplete`**, criterion 6 named with its owner. RED probes fired:
  a tampered G1-REPORT.md is named rc=1 (restored rc=0); `baseline.sexp` removed →
  criterion 5 flips to "NOT met — the baseline is not recorded as data"; `--gate G9`
  refused rc=2; G0 output byte-identical before/after (`diff` empty). The baseline record
  parses under all three tracked readers (`compare_readers.py`: 513 nodes identical).

- [x] **NO REGRESSION** — `make gate` green (23 doctrines; GATE-REPORT covers 2 reports;
  SOURCE-FORMAT accepts `baseline.sexp`; FRONTIER-SYNC/TREE-CLAIMS re-derive the completed
  tree), `cargo test --all` unchanged (no Rust change: 5 suites, 189 tests), wasm build
  rc=0, `make book` green; the live tree stays under the per-part ceiling by archiving
  `.11`'s checklist and the completed leaves' design detail (boundary stated in
  "Completed-leaf evidence").

- [x] **LOCKSTEP** — `MEMORY.md`, `CHANGELOG.md`, `LIVE_STATUS.md` (P1 12/12, gate honest),
  `DEV_NOTES.md`, `docs/TASK_TREE.md` (P1-LAB done), the book's P1 chapter ("Gate G1"
  carries the verdict and its reason), `DOCTRINE_ENFORCEMENT.md` + `TOOLBOX.md` rows, and
  this tree — one commit.
