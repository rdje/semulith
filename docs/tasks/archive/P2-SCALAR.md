# P2-SCALAR — archived completed-leaf checklists

The full, unedited acceptance checklists for the `done` leaves `.1`–`.5` of the
[`P2-SCALAR`](../P2-SCALAR.md) tree, split out from the live file as each crossed the
per-part ceiling (2026-09-29 for `.1`–`.2`, `2026-09-30` for `.3`, `.4`, `.5`) — the ceiling
was obeyed, never raised. The recorded-before-code DESIGN detail lives in
`P2-SCALAR-designs.md` beside this file (the split happened when the combined archive
crossed the same ceiling, 2026-09-30). The live tree keeps the frontier, the decisions,
the open questions, the blockers, the defect log, every leaf's goal/acceptance/result,
the active leaf's design and checklist, and both logs.

## Acceptance Checklist (leaf P2-SCALAR.1)

- [x] **REPRODUCE / ISSUE** — the declared scope was 52 forms; only 15 had ever executed.
  The instrument built for this leaf measured the hole against the real corpus before any
  fix existed:

  ```
  $ bash scripts/check_exercise_coverage.sh
  EXERCISE-COVERAGE: the declared scope is not fully exercised (coverage 15/52).
    UNEXERCISED profiles/rv64i-lab-v0/profile.sexp: 'addw' … (37 forms named, rc=1)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — WHY: EXTRACTION proves every declared form HAS
  encoding+semantics+requirement (static sufficiency), but nothing measured the dynamic
  half — guests were written for P0/P1's smoke needs (15 mnemonics), never for scope
  completion, and no gate counted the difference. WHERE, measured: the denominator is
  `profiles/rv64i-lab-v0/profile.sexp` `[scope]`; the exercised set was the union over the
  four `guests/*.expected.sexp` — and a second, smaller hole sat one layer down: `fence`
  could not even be assembled, because `gen_fragments.py`'s `USED_FIELDS` whitelist
  predated any fence guest:

  ```
  $ python3 -c "… Assembler('profiles/rv64i-lab-v0/encoding.sexp').assemble(['fence'])"
  AsmError: 'fence' uses operand field 'fm', which this assembler does not support
  $ bash scripts/check_exercise_coverage.sh | sed -n 1,2p   # the measurement, re-runnable
  EXERCISE-COVERAGE: the declared scope is not fully exercised (coverage 15/52).
  ```

- [x] **FIX** — five scope-completion guests + EVD-05 expectations (derived before any
  run); `fm`/`pred`/`succ` added to `USED_FIELDS` and `CONTIGUOUS_OPERANDS` (the pinned
  `arg_lut.csv` carries them), `definitions/riscv/rv64i.sexp` and `definition.rs`
  regenerated through the sanctioned generators; `gen_guests.py`'s tuple extended and
  `guests.rs` regenerated (9 guests); `mutate.rs`'s census gained `scope-mem`'s 17
  crossings; `run/tests.rs` gained five guest suites; `compare_traces.py` learned the
  measured ecall/ebreak spellings; `gate_report.py`'s guest claims derived; the 24th
  doctrine `EXERCISE-COVERAGE` registered with a 7-arm self-test. All at the lowest-risk
  level: data (guests), whitelists fed by the pinned table, and one new check — no
  interpreter change.

- [x] **ADDRESSED (verified)** — before→after, same command:

  ```
  $ bash scripts/check_exercise_coverage.sh     # before: 15/52, rc=1 (37 named)
  EXERCISE-COVERAGE: ok (1 profile(s) — every declared form exercised, 52/52)
  $ python3 scripts/run_semulith_smoke.py       # the live three-way differential
  …scope-alu/-mem/-branch/-ecall/-ebreak: AGREE vs sail-riscv AND spike…
  run_semulith_smoke: ok — 9 guests, 117/117 aligned steps, byte-identical reproduction
  ```

- [x] **NO REGRESSION** — the guard set re-run, green:

  ```
  $ make check            # 133 verify suites (+5 guest suites), 5 core suites, clippy -D warnings
  $ make gate             # 24 doctrines green (EXERCISE-COVERAGE among them)
  $ make smoke-bench      # 13 arms — 9 clean guests, 3 trace-level mutants, the census arm
  $ bash scripts/check_exercise_coverage.sh --self-test   # 7 pass / 0 fail
  ```

- [x] **LOCKSTEP** — same commit: `MEMORY.md` (overwritten), `LIVE_STATUS.md` (P2 1/9,
  24 doctrines, 261 arms), `CHANGELOG.md`, `DEV_NOTES.md`, `docs/TASK_TREE.md` (frontier
  `.2`), this tree, the book (`plan/p2.md` carries the result; `plan/p1.md` and
  `claim-scope.md` re-synced to 9 guests / 117 steps), the doctrine mirrors
  (`DOCTRINE_ENFORCEMENT.md`, `docs/book/src/working/doctrines.md`), `TOOLBOX.md` (the new
  row), and both regenerated `G?-REPORT.md`.

---

## Acceptance Checklist (leaf P2-SCALAR.2)

- [x] **REPRODUCE / ISSUE** — the corpus exercised every declared FORM (`.1`), but the
  boundary DOMAINS had only incidental samples: across the whole pre-leaf corpus, exactly
  four distinct immediate shift amounts had ever executed, and no guest had wrapped a
  signed extreme, probed a sign edge at exactly 0x80/0x8000/0x80000000, composed
  overlapping stores, or self-aliased a destination (rd = rs1 = rs2):

  ```
  $ git grep -h -E '^[[:space:]]*(slli|srli|srai|slliw|srliw|sraiw)[[:space:]]' HEAD \
        -- 'profiles/rv64i-lab-v0/guests/' | sed -E 's/#.*$//' \
      | grep -oE '[0-9]+[[:space:]]*$' | tr -d ' ' | sort -n | uniq
  25
  31
  32
  63
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — WHY: the P1 guests were written for smoke coverage and
  the `.1` guests for form coverage — one instance per form — and neither brief includes
  the boundary structure of an operator (the shamt FIELD's 64/32 values, the wrap points,
  the sign edges, self-aliasing). Nothing was wrong; an evidence layer the leaf's
  acceptance names was simply unwritten. WHERE, measured: the exercised-amount census is
  the REPRODUCE box's command (4 of 64 values); the self-alias census is directly
  enumerable — a destination aliased onto BOTH its sources did not exist in the corpus
  (BSD grep: backreferences need the basic-syntax form, not `-E`):

  ```
  $ git grep -h '\(add\|sub\|slt\|sll\|sra\) \(x[0-9][0-9]*\), \2, \2\(,\|$\)' HEAD \
        -- 'profiles/rv64i-lab-v0/guests/' | wc -l        # before
  0
  $ grep -h '\(add\|sub\|slt\|sll\|sra\) \(x[0-9][0-9]*\), \2, \2\(,\|$\)' \
        profiles/rv64i-lab-v0/guests/*.s | wc -l          # after
  4
  ```

- [x] **FIX** — five boundary guests with EVD-05 expectations (every value computed by
  spec-rule arithmetic at authoring time, before any model ran, each step carrying
  derivation + source): `bound-shift` (89 steps — the 6-bit shamt domain exhausted by one
  `srli` sweep), `bound-shiftw` (55 — the 5-bit domain exhausted by one `sraiw` sweep, the
  rs2 = 96 `srl`/`srlw` discriminator pair), `bound-arith` (31 — wraps, immediate extremes,
  the `auipc` sign-edge wrap), `bound-ext` (47 — the sign-edge pairs, 32 crossings),
  `bound-alias` (37 — endian lanes, overlap composition, register aliasing, x0; 16
  crossings). Cascades as designed: `gen_guests.py`'s tuple, `guests.rs` regenerated, five
  `run/tests.rs` suites, `mutate.rs`'s census (48 new pins, per-line justifications), the
  smoke tuple, the routes-registry ceilings, both gate reports regenerated. No interpreter
  change — data and pins only.

- [x] **ADDRESSED (verified)** — before→after, same census command: 4 → 64 distinct
  immediate shift amounts (the 6-bit domain complete, the 5-bit domain within it), and:

  ```
  $ cargo test -p semulith-verify          # the offline differential, commitment-gated
  test result: ok. 138 passed; 0 failed (+5 guest suites; the census pin re-derives
  bound-ext's 32 and bound-alias's 16 crossings from the real runs)
  $ python3 scripts/run_semulith_smoke.py  # the live three-way differential
  …bound-shift/-shiftw/-arith/-ext/-alias: AGREE vs sail-riscv AND spike…
  run_semulith_smoke: ok — 14 guests, 376/376 aligned steps, byte-identical reproduction
  ```

- [x] **NO REGRESSION** — the guard set re-run, green; and the gate caught two AUTHORING
  slips during the leaf (the overlap-composition constant, twice), both corrected by
  re-deriving from the spec rule — the instrument discriminates in the right direction:

  ```
  $ make check            # 138 verify suites (+5), 65 core suites, clippy -D warnings, fmt
  $ make gate             # 24 doctrines green (GUEST-GEN, GATE-REPORT, the new ceilings…)
  $ make smoke-bench      # 18 arms — 14 clean guests, 3 trace-level mutants, the census arm
  $ bash scripts/check_exercise_coverage.sh [--self-test]   # 52/52; self-test 7/0
  ```

- [x] **LOCKSTEP** — same commit: `MEMORY.md` (overwritten), `LIVE_STATUS.md` (P2 2/9),
  `CHANGELOG.md`, `DEV_NOTES.md`, `docs/TASK_TREE.md` (frontier `.3`), this tree, the book
  (`plan/p2.md` carries the result; `plan/p1.md` and `claim-scope.md` re-synced to 14
  guests / 376 steps), the routes registry (the reviewed ceilings), and both regenerated
  `G?-REPORT.md`.

## Acceptance Checklist (leaf P2-SCALAR.3)

- [x] **REPRODUCE / ISSUE** — three holes, each measured before any fix. (a) The `.1`
  defect log said reserved-`fm` FENCE must trap; the pinned spec says the opposite —
  the probe showed all THREE models nop it. (b) The misaligned-jump link write,
  reproduced against both references: semulith wrote `x5`, neither reference did. (c)
  The fetch-fault observation gap `run.rs` named as future work, and the reserved-decode
  case stopping with no observation to compare:

  ```
  $ cargo run -p semulith-cli -- run probe-jal-mis.elf --steps=4   # BEFORE the fix
  [1] [M]: 0x0000000080000004 (0x002002ef) jal
  x5 <- 0x0000000080000008                     # ← the write both references suppress
  trap cause=0x00 tval=0x0000000080000006
  $ cargo run -p semulith-cli -- run probe-fetch-fault.elf --steps=6
  run: fetch access fault at 0x0000000040000000; no observation recorded   # ← the gap
  $ cargo run -p semulith-cli -- run probe-reserved-ones.elf --steps=4
  run: undefined case: ReservedDecode { at: 2147483652 }   # rc=1, no trace observation
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — (a) WHY: the dossier author read "reserved" and
  reached for `D-RESERVED-DECODE`, but RVI-RV32I §1.1.7 SPECIFIES the behavior of
  reserved FENCE configurations ("shall treat all such reserved configurations as FENCE
  instructions (with fm = 0000)") — a specified reserved case, not the UNSPECIFIED one.
  WHERE: `D-FENCE`'s last sentence and its `REQ-D-FENCE`/`OB-FENCE` restatements.
  (b) WHY: the `jal`/`jalr` effect trees evaluated the link write before `set-pc`'s
  alignment check, so a trapping jump retired a write. WHERE:
  `definitions/riscv/rv64i.sem.sexp` — semantics data, never the evaluator. (c) WHY:
  the observation vocabulary had no honest shape for "the fetch supplied no word" and
  no policy act for the reserved case. WHERE: `run.rs`'s `Step`/`Stop` and the two
  trace adapters in `scripts/compare_traces.py`.

- [x] **FIX** — the dossier correction (`D-FENCE` + both restatements, the verbatim
  mandate cited, the correction noted like `D-MAIN-VS-IO`'s); the sem-tree reorder
  (`set-pc` first — data, regenerated through the sanctioned generator); the word-less
  fetch-fault step (`Step.word` → `Option<u32>`, emitted by the runner, printed by the
  CLI, synthesized by both adapters, round-tripped by replay); the reserved-decode
  policy conversion in the harness (`Stop::Undefined` keeps the classification);
  `riscv_asm.py`'s `.word` directive; eighteen EVD-05 guests; the adapter's four
  measured spellings + self-test arms (12/0); `DIFF-FENCEI-EXECUTED` recorded;
  OQ-2 answered (`REQ-D-SHIFTW-RESERVED` → `resolved`); the census and suites
  re-derived; ceilings expanded by reviewed decision.

- [x] **ADDRESSED (verified)** — before→after on the same probes: the misaligned jump
  now traps with NO link write (matching both references); the fetch fault records the
  word-less step; the reserved word records the policy-converted trap. And the full
  corpus:

  ```
  $ cargo test -p semulith-verify          # the offline differential, commitment-gated
  test result: ok. 157 passed; 0 failed (+18 guest suites, +2 runner unit suites;
    the census pins fault-selfmod's crossing and the three access-fault crossings)
  $ python3 scripts/run_semulith_smoke.py  # the live three-way differential
  …every fault-* guest: AGREE vs sail-riscv AND spike…
  run_semulith_smoke: ok — 32 guests, 454/454 aligned steps, byte-identical reproduction
  ```

- [x] **NO REGRESSION** — the guard set re-run, green; and the instruments caught three
  AUTHORING slips in flight (the trailing paren in all 18 expectation documents — schema
  RED on all 18; the store operand order in 4 guests — the pre-wiring dry-run; the
  REQ-D-FENCE statement drift — RECORD-SCHEMA RED at the gate), never another model
  defect:

  ```
  $ make check            # 157 verify suites, 65 core suites, clippy -D warnings, fmt
  $ make gate             # all doctrines green (RECORD-SCHEMA, the new ceilings…)
  $ make smoke-bench      # 36 arms — 32 clean guests, 3 trace-level mutants, the census arm
  $ bash scripts/check_exercise_coverage.sh [--self-test]   # 52/52; self-test 7/0
  $ python3 scripts/compare_traces.py --self-test           # 12/0 (+4 new arms)
  $ make book             # renders
  ```

- [x] **LOCKSTEP** — same commit: `MEMORY.md` (overwritten), `LIVE_STATUS.md` (P2 3/9),
  `CHANGELOG.md`, `DEV_NOTES.md`, `docs/TASK_TREE.md` (frontier `.4`), this tree, the
  book (`plan/p2.md` carries the result; `plan/p1.md` and `claim-scope.md` re-synced to
  32 guests / 454 steps; `annex/assembler.md` documents `.word`), the routes registry
  (the reviewed ceilings), `references.sexp` (the new difference), the dossier
  (D-FENCE, OQ-2), and both regenerated `G?-REPORT.md`.

## Acceptance Checklist (leaf P2-SCALAR.4)

- [x] **REPRODUCE / ISSUE** — the leaf's premise was measured before anything was built
  (the `.3` doctrine): 8 probe ELFs against sail-riscv 0.14 AND spike 1.1.1-dev
  established the fault priorities, the wrap-into-fault, the base preservation, the
  fence.i continuation — and found a NEW reference-vs-reference difference (sail's 56-bit
  access-fault tval mask, `DIFF-TVAL-PHYS-MASK`), which redesigned the wrap-sd guest to
  address 0 before it was authored.

- [x] **ROOT CAUSE (WHY + WHERE)** — no model defect was found this leaf; the matrix is
  evidence organization, and every behavior it pins was already measured. The two in-flight
  REDs were the author's, each observed as gate output (`INTERACTION-MATRIX: the declared
  matrix does not hold.` — first as the pre-registration `NO MATRIX rv64i-lab-v0`, then as
  three phantom OMITTED CELLs on the first full run). WHY the phantom cells: the derived
  cell set was built in declared-axis order while cell keys normalize to sorted pairs;
  WHERE `check_interaction_matrix.py`'s `want` set construction. WHY
  README-ROUTING-CLOSURE fired twice — `references.sexp` + the difference record crossed
  the 32,768 per-part ceiling, and the 25th doctrine row crossed both mirror byte caps;
  WHERE the registry rows, re-derived per the SEMILITH-PL-0001 precedent.

- [x] **FIX** — the matrix document + schema; the `INTERACTION-MATRIX` gate (fired RED
  against the real corpus as `NO MATRIX rv64i-lab-v0` before registration, self-test
  12/0, registered as doctrine #25, three mirrors); the comparator's
  `check_expected_divergence` (+4 self-test arms, 16/0 — agreement at the declared step
  is the RED case); `expect_divergence` in the expectations schema and the dossier
  mapping (round-trip arm); the smoke run's four-step protocol; eight EVD-05 guests;
  the determinism suite (every guest twice from `zeroed_at(entry)`, identical traces AND
  crossing logs); the census pins; `references.sexp` + `DIFF-TVAL-PHYS-MASK`; the
  reviewed ceilings.

- [x] **ADDRESSED (verified)** —

  ```
  $ cargo test -p semulith-verify          # the offline differential, commitment-gated
  test result: ok. 166 passed; 0 failed (+8 guest suites, +1 determinism suite;
    the census pins all 8 new guests — six empty arms, two faulted wrap crossings)
  $ python3 scripts/run_semulith_smoke.py  # the live three-way differential
  …39 guests AGREE vs sail-riscv AND spike; it-fencei: EXPECTED DIVERGENCE at aligned
    step 1 against each reference, sail vs spike AGREE over their full 4 steps…
  run_semulith_smoke: ok — 40 guests, 492/492 aligned steps, byte-identical reproduction
  $ bash scripts/check_interaction_matrix.sh [--self-test]   # 21/21 cells; self-test 12/0
  ```

- [x] **NO REGRESSION** — the guard set re-run, green; `EXERCISE-COVERAGE` stays 52/52
  (no new form); the one RED moment in flight was the gate's own derivation bug, caught
  by the corpus, never a model defect:

  ```
  $ make check            # 166 verify suites, 65 core suites, clippy -D warnings, fmt
  $ make gate             # all 25 doctrines green (REGISTRY-MIRROR, DERIVED-COUNTS, the
                          # re-based ceilings…)
  $ make smoke-bench      # 44 arms — 40 clean guests, 3 trace-level mutants, the census arm
  $ bash scripts/check_exercise_coverage.sh [--self-test]   # 52/52; self-test 7/0
  $ python3 scripts/compare_traces.py --self-test           # 16/0 (+4 divergence arms)
  $ make book             # renders
  ```

- [x] **LOCKSTEP** — same commit: `MEMORY.md` (overwritten), `LIVE_STATUS.md` (P2 4/9,
  25 doctrines / 273 arms), `CHANGELOG.md`, `DEV_NOTES.md`, `docs/TASK_TREE.md` (frontier
  `.5`), this tree, the book (`plan/p2.md` carries the result; `plan/p1.md` and
  `claim-scope.md` re-synced to 40 guests / 492 steps), the three doctrine mirrors, the
  routes registry (the reviewed ceilings, incl. the two mirror caps), `references.sexp`
  (the new difference; `DIFF-FENCEI-EXECUTED` marked landed), and both regenerated
  `G?-REPORT.md`.

## Acceptance Checklist (leaf P2-SCALAR.5 — strand 1: the C-toolchain guest)

- [x] **REPRODUCE / ISSUE** — G1's sixth criterion stood unmet, measured two ways at the
  parent commit (`02791f2`), and the toolchain half of the blocker was measured, not
  assumed:

  ```
  $ ls profiles/rv64i-lab-v0/guests/*.c | wc -l
  0
  $ scripts/gate_report.py rv64i-lab-v0 --gate G1 --stdout | grep -m1 "C guests"
  `guests/` holds **40 assembly guests** and **0 C guests**.   (verdict: incomplete)
  $ clang --target=riscv64-unknown-elf -march=rv64i -x c -c -o /dev/null - <<<'int f(void){return 0;}'
  error: unable to create target: 'No available targets are compatible with triple
  "riscv64-unknown-unknown-elf"'                 # Apple clang 21.0.0: NO RISC-V backend
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — three layers, each tool-backed. (i) Ownership and
  toolchain were undecided, not unbuildable: the routing answer is
  `decision_c-guest-routing-and-toolchain` (director delegation), and the toolchain was
  measured PRESENT — Homebrew `llvm@21` clang 21.1.8 compiled `-march=rv64i -mabi=lp64`
  to correct RV64I (objdump-verified), `zig ld.lld` reported Homebrew LLD 21.1.8.
  (ii) The first compiled binary failed its OWN self-check — `fail(0x0501)` measured in
  the run trace (`x10 <- 0xfa11000000000501`): WHERE the guest's section 6, `w32 << 33` —
  a 32-bit shift by ≥ 32 is UB in C (C11 6.5.7p3), which clang exploited to delete the
  entire rest of the program and route the fall-through to `fail`. Proven, not reviewed:
  the same compile with the amount narrowed to 31 restores `call fib` + 4× `call emit`;
  the `-fno-strict-aliasing` control did NOT (aliasing was the first suspect, measured
  innocent). (iii) With the guest clean, the three-way comparison diverged at aligned
  step 7 — `li a0, 0` with a0 already 0: semulith records no write (its DECLARED
  visible-change vocabulary), BOTH references log `x10 <- 0`. WHERE the comparator: it
  never had to normalize no-change writes, because the hand-written corpus pre-writes
  destinations (the `.1` lesson) — 492/492 never exercised the case a compiler emits
  routinely.

- [x] **FIX** — at the lowest-risk level that works for each layer: the guest's section 6
  uses only C-legal shifts (the *W shamt boundary stays with `bound-shiftw`'s assembly —
  C cannot express it; the source comments carry exactly this); the COMPARATOR learned
  the declared vocabulary (`_visible_changes` in `compare_traces.py`'s `align` — the one
  funnel every trace passes through; a shadow register file from the declared reset; an
  `x0` record of nonzero stays visible; +2 self-test arms, 19/0); the pinned-toolchain
  build script (`scripts/build_c_guest.sh` — every candidate PROBED for the riscv64
  backend, a clang without one refused by name, nothing installed); the smoke's `.c`
  path (build → budget run stopped by the closing ebreak → `e_entry` read from the ELF
  header); `gate_report.py`'s criterion-6 and Limitations branches (the met prose names
  the guest, the build script and the decision record — the versions' ONE owner).

- [x] **ADDRESSED (verified)** — the criterion flips on the live three-way differential,
  and the report regenerates to `passed`:

  ```
  $ python3 scripts/run_semulith_smoke.py | sed -n '/== c-scope ==/,/== bound-shift/p'
  PASS  c-scope: compiled, retired inside the budget  129 executed step(s), entry 0x80001370
  PASS  c-scope: semulith vs sail-riscv  AGREE over 129 aligned step(s)
  PASS  c-scope: semulith vs spike       AGREE over 129 aligned step(s)
  PASS  c-scope: semulith reproduces
  $ scripts/gate_report.py rv64i-lab-v0 --gate G1 --stdout | grep -m1 Verdict
  **Verdict: `passed`.**
  ```

- [x] **NO REGRESSION** — the guard set re-run, green; the two in-flight REDs were the
  author's own C UB and the comparator's missing normalization (above), never a model
  defect. No Rust changed, so `make check`'s re-run is not owed (COMMIT.md §2):

  ```
  $ python3 scripts/run_semulith_smoke.py          # 221 PASS / 0 FAIL — the 40 assembled
                                                   # guests' verdicts unchanged
  $ python3 scripts/compare_traces.py --self-test  # 19/0 (+2 vocabulary arms)
  $ make gate                                      # all doctrines green
  $ make book                                      # both books render
  ```

- [x] **LOCKSTEP** — same commit: `MEMORY.md` (overwritten — G1 `passed`, strand 1 next
  action), `LIVE_STATUS.md` (P1 row verdict, P2 `.5` active), `CHANGELOG.md`,
  `DEV_NOTES.md`, this tree, `docs/tasks/P1-LAB.md` (metadata + frontier re-synced to
  the verdict it routed), the book (`claim-scope.md`,
  `annex/building-first-model.md`), the model book (`evidence.md`, `introduction.md`),
  and the regenerated `G1-REPORT.md`.
