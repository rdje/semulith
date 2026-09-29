# P2-SCALAR: validate the first RV64I profile

## Metadata

- Tree ID: `P2-SCALAR`
- Status: `active`
- Roadmap lane: `ROADMAP.md` §6 → **P2 — Validate the first RV64I profile**
- Gate: `CPU-LAB`
- Depends on: `P1-LAB` (gate `G1`)
- Unlocks: `P3-BREADTH`, `P4-SYSTEM`
- Created: `2026-09-13`
- Owner: repo-local workflow

## Goal

Complete the **entire declared** scalar instruction and laboratory-environment scope of
`rv64i-lab-v0` and carry it through the full processor gate, producing a reusable CPU
deliverable with a versioned accepted profile and attached evidence.

## Non-Goals

- Not a boot test. `CPU-LAB` is a processor gate; no system workload substitutes for it.
- No privilege, translation, atomics or floating point — those are new work in `P4-SYSTEM`,
  and passing here shortens none of it (`ROADMAP.md` §P2).

## Acceptance Criteria — gate `CPU-LAB`

The full processor gate of `docs/EVIDENCE_AND_GATES.md` §7: `G-SCOPE`, `G-STATE`, `G-CONTRACT`,
`G-TRACE`, `G-OBLIGATIONS`, `G-INTERACTIONS`, `G-REGRESSION`, `G-PORTABILITY`, `G-REPLAY`,
`G-RELEASE`. A missing required check yields `incomplete`, never `passed`.

## Task Tree

- ID: `P2-SCALAR.1` — **complete the declared instruction scope** *(task card `T008`)*
  Status: `done` (`2026-09-29`)
  Goal: every remaining selected RV64I form, not just the mnemonics already exercised.
  Acceptance: coverage reported with its **denominator**; `SCP-02`'s dependency closure holds.
  Design (recorded before code, `2026-09-29`):
  - **The gap, measured.** Denominator: the profile's declared scope — 52 RV64I forms
    (`profile.sexp` `[scope]`, count re-derived from the `riscv/rv64i` fragment). Exercised
    today: 15 — the union of mnemonics over the four tracked guests' expectation documents
    (`add addi addiw auipc bne jal jalr ld lui lw sd slli slliw srai srli`). Remaining: 37.
  - **Five new guests**, each form landing on a recorded decision, every expectation value
    derived from the pinned specification BEFORE any model runs (`EVD-05`):
    `scope-alu` (the 21 remaining logical/compare/shift forms, plus `fence`),
    `scope-mem` (the 8 remaining load/store forms), `scope-branch` (the 5 remaining branches,
    taken AND not-taken each), `scope-ecall` and `scope-ebreak` (a requested trap stops the
    run, so each gets its own guest, trap step last — the `smoke-trap` pattern).
  - **`fence` needs the assembler to learn three operand fields.** The pinned `arg_lut.csv`
    carries `fm`/`pred`/`succ` (31..28 / 27..24 / 23..20); `gen_fragments.py`'s `USED_FIELDS`
    whitelist predates any fence guest. The change is the sanctioned one: extend the
    whitelist, regenerate `definitions/riscv/rv64i.sexp` (three field lines), add the three
    fields to `riscv_asm.py`'s `CONTIGUOUS_OPERANDS` (the existing width-checked path
    range-checks 0..15), regenerate `definition.rs`. No opcode is typed by hand anywhere.
  - **Coverage with its denominator, gated.** New tracked diagnostic
    `scripts/check_exercise_coverage.{py,sh}`: exercised = the union of mnemonics the tracked
    expectation documents declare executed (the commit gate proves those steps execute);
    denominator = the declared scope; the SCP-02 closure printed as data through the one
    resolver (`riscv_asm.resolve_composition`): closure `{riscv/rv64i}`, `requires` empty,
    extensions none. Registered as project doctrine `EXERCISE-COVERAGE` with RED-arm
    self-tests, mirrored per the registry rules; `TOOLBOX.md` gains the row.
  - **Cascades owned by this leaf:** `gen_guests.py`'s guest tuple; `run/tests.rs` gains one
    test per guest (stop `Budget`, or `Trap` for the two env guests); `mutate.rs`'s
    `pinned_census` gains the `scope-mem` data crossings with per-line justifications (the
    census-pin test iterates every guest); `run_semulith_smoke.py`'s guest tuple (the live
    three-way run, references present under `target/refs/`); `gate_report.py`'s hardcoded
    "The four tracked guests" becomes derived and both `G?-REPORT.md` regenerate.
  Result: met, `2026-09-29`. **52/52 declared forms exercised, with the denominator, gated.**
  The coverage instrument fired RED against the real corpus before anything was built —
  15/52, all 37 missing forms named — and has read GREEN since: the 24th project doctrine
  `EXERCISE-COVERAGE`, self-test 7/0, mirrored per the registry rules. Five scope-completion
  guests landed with every expectation derived from the pinned specification before any run
  (`EVD-05`): `scope-alu` (31 steps), `scope-mem` (29; 17 census-pinned data crossings),
  `scope-branch` (19 from 24 instructions; five `never_written` negatives), `scope-ecall`
  and `scope-ebreak` (requested traps, cause/tval matching both references exactly). `fence`
  forced the honest path for its operands: `fm`/`pred`/`succ` now come from the pinned
  `arg_lut.csv` (fragment whitelist + assembler extended, both generated artifacts
  regenerated, no hand-typed opcode; the field-count pin moved 12→15). The trace adapter
  learned the measured ecall/ebreak spellings of sail 0.14 and spike 1.1.1-dev (unknown
  spellings raise). Two `sltu`/`sltiu` 0-results are pre-written with 1 because the
  observation vocabulary is the VISIBLE register change — an empty write would prove
  nothing. The live experiment: 9 guests, **117/117 aligned steps** against sail-riscv AND
  spike, byte-identical reproduction. One defect found in flight, logged above and routed
  to `.3` (reserved-`fm` FENCE nops; `D-FENCE` says illegal-instruction). The frontier
  moves to `.2` (boundary arithmetic and state interactions).
  Lessons: `promotion: declined (the lesson is mechanical where it bites — the commit gate fails any invisible expected write, measured this leaf)`.
  The leaf's one generalizable lesson — when the observation vocabulary is a diff, pre-write
  the destination or the step proves nothing — was enforced, not just noted: the offline
  differential failed the `sltu`/`sltiu` 0-results exactly so (`left: []` vs
  `right: [(13, 0)]`). A knowledge card would restate what the gate enforces; the doctrine
  row carries the coverage rule.

- ID: `P2-SCALAR.2` — **boundary arithmetic and state interactions**
  Status: `in-progress` (design recorded `2026-09-29`, before code)
  Goal: boundary values, sign/zero extension, shift corner cases, alias and overlap effects.
  Acceptance: exhaustive checks where a reduced width makes them tractable; source-linked expected values.
  Design (recorded before code, `2026-09-29`):
  - **The four named concerns map onto five new guests**, every expectation derived from the
    pinned specification prose BEFORE any model runs (`EVD-05`), each step carrying its
    `derivation` and `source` exactly as the `.1` guests do. Values are computed by spec-rule
    arithmetic at authoring time (never read back from any model's output); the live
    three-way differential (`run_semulith_smoke.py` vs sail-riscv AND spike) is the
    falsification leg, and the offline commit gate re-runs the pinned expectations.
  - **`bound-shift` — the 64-bit shift corner cases (`D-SHAMT`).** Operand
    `0x8000000000000001` (bit 63 AND bit 0 set) built from covered forms. The **6-bit shamt
    domain is exhausted**: a full 64-point `srli` sweep, whose 64 results are pairwise
    distinct so every step is a VISIBLE register change. `sll`/`sra` immediates take the
    bit-pinning set {0,1,2,4,8,16,32,63} — every shamt bit pinned on every form, the full
    sweep held once per domain rather than once per form (the amount decode is the shared
    structure; the fill/direction logic is what differs per form, and the boundary values
    discriminate it). Register-amount corners: `rs2 = 64` reads as 0 (identity — pre-written
    to observe) and `rs2 = -1` reads as 63, through `srl`/`sll`/`sra`. 89 steps.
  - **`bound-shiftw` — the *W shift corner cases (`D-SHAMT`'s 5-bit rule, `D-WSUFFIX`).**
    Operand low32 `0x80000001` (bit 31 set). The **5-bit domain is exhausted**: a full
    32-point `sraiw` sweep (sign fill within 32 bits, then the *W sign extension — 32
    distinct results); `slliw`/`srliw` take the bit-pinning set {0,1,2,4,8,16,31}.
    Register-amount corners: `rs2 = 96` — low6 = 32, low5 = 0 — as the discriminator PAIR
    (`srl` shifts by 32, `srlw` is the identity, same operands) and `rs2 = -1` (low5 = 31)
    through `sllw`/`sraw`. 52 steps.
  - **`bound-arith` — wrap/overflow and immediate boundaries (`D-ALU-REG`, `D-ALU-IMM`,
    `D-WSUFFIX`, `D-LUI-AUIPC`, `D-ADDR-WRAP`).** `INT64_MAX + 1` and `INT64_MIN - 1` wrap,
    on both the register and the immediate path; `INT64_MAX + INT64_MAX` wraps to -2; the
    immediate extremes -2048/2047; `addiw`/`addw`/`subw` 32-bit wraps sign-extend (operand
    carries garbage upper bits to prove they are ignored); `slt`/`sltu` at the signed
    extremes (the 0-result pre-written); `slti`/`sltiu` at the immediate extremes; `lui
    0x7FFFF` (positive U edge) vs `.1`'s `lui 0x80000`; `auipc 0x80000` at entry +
    4n — the sign-extended offset wraps modulo 2^64 and the result is exactly 4n. No memory
    crossings. ~30 steps.
  - **`bound-ext` — sign/zero extension at the sign edges (`D-LOAD-EXT`).** The byte edge
    0x7F/0x80, the halfword edge 0x7FFF/0x8000, the word edge 0x7FFFFFFF/0x80000000, each
    through the sign/zero PAIR at one address (the pair is the observation); the all-ones
    value at each width; the 0x00 byte observed through a pre-write. Store truncation at
    values where the truncated result differs from BOTH clamping outcomes (0x180 → 0x80,
    0xFFFF8000 → 0x8000 / 0xFFFF8000). ~43 steps, ~32 census-pinned crossings.
  - **`bound-alias` — alias, overlap and state interactions (`D-ENDIAN`, `D-LOAD-EXT`,
    reset-state rules).** The little-endian lane proof: `sd 0x0807060504030201` then `lbu`
    at each of the 8 byte lanes. Overlap composition: `sd` + `sb` over byte 3 + `sh` over
    bytes 6–7 + one `ld` read-back of the composed word. Register aliasing: `add x,x,x`
    doubling, `sub x,x,x` (nonzero → 0 transition), `slt x,x,x` (pre-written 1 → 0),
    self-referential `slli x,x,x`, and `lb x24, x24, 0` — a load that overwrites its own
    base register, proving the address is sampled before the write commits. x0: `addi x0,
    x0, -1` writes nothing (empty-writes expectation), `sw x0` zeroes a word (read back
    through `ld`). ~33 steps, ~16 census-pinned crossings.
  - **The visibility rule governs every reused destination** (measured in `.1`: the
    observation vocabulary is the VISIBLE register change, `run.rs`'s `diff(before, state)`):
    sweep operands are chosen so consecutive results differ, and every identity or 0-result
    is pre-written to a distinct value.
  - **Exhaustion judgement, stated:** the tractable reduced-width domains are the shamt
    FIELDS (6-bit = 64 values, 5-bit = 32) — each is exhausted once. The data-value domains
    (2^64, 2^32, 2^8) are intractable or near it, and their discriminating structure is the
    sign edge and the wrap point — enumerated as boundaries, not swept. A 256-point byte
    sweep was considered and rejected: the extension logic is generic over the width, so the
    edge pair discriminates everything the sweep would, at 1/40 the corpus cost.
  - **Reviewed ceiling expansion** (the `.1` decision names this leaf's guest growth as its
    own reviewed decision): the corpus grows 9 → 14 guests (+10 tracked files under
    `profiles/rv64i-lab-v0/guests/`), so `profiles/` rises 32 → 42 files and ~220 KB →
    ~315 KB aggregate. `doctrine/readme_routes.tsv`: `ceiling_lines` 34 → 46 (42 + 4
    headroom, the registry's proportional rule), `ceiling_bytes` 262144 → 393216 (the same
    ~1.2× band the existing ceiling holds), health targets re-based to the measured size.
    ⛔ `ceiling_part_bytes` stays 32768 — the per-part bound answers "has one member become
    the monolith", and no new file approaches it (largest: `bound-shift.expected.sexp`,
    ~27 KB); sweep derivations are deliberately terse to keep it that way.
  - **Cascades owned by this leaf:** `gen_guests.py`'s guest tuple and `guests.rs`
    regenerated; `run/tests.rs` gains one suite per guest (all `Stop::Budget`);
    `mutate.rs`'s `pinned_census` gains `bound-ext`'s and `bound-alias`'s crossings with
    per-line justifications and the three ALU guests join the empty arm;
    `run_semulith_smoke.py`'s guest tuple; both `G?-REPORT.md` regenerate (counts are
    derived); the browser bench enumerates guests dynamically — its arm count grows 13 → 18
    with no edit; `EXERCISE-COVERAGE` stays 52/52 (the scope did not change).

- ID: `P2-SCALAR.3` — **fault, suppression and reserved cases**
  Status: `pending`
  Goal: fetch and access faults, suppressed effects, reserved encodings, controlled event boundaries.
  Acceptance: a failing access that already modified memory or a device is modelled as the source defines it (`SEM-06`, catalog `C11`); reserved cases keep their source meaning (`SEM-07`).

- ID: `P2-SCALAR.4` — **the interaction matrix** — `G-INTERACTIONS`
  Status: `pending`
  Goal: the declared fault × alias × boundary × event × progress × restart matrix, exercised.
  Acceptance: the matrix is declared first and then exercised; unexercised cells are reported, not omitted.

- ID: `P2-SCALAR.5` — **external and directed campaigns** — `G-REGRESSION`
  Status: `pending`
  Goal: matched reference comparisons, configured external tests, directed sequence tests, and compiled freestanding programs.
  Acceptance: ACT4 results are recorded as **external tests with Sail-derived expected values**, never as a second independent semantics (`EVD-04`).

- ID: `P2-SCALAR.6` — **discrepancy reduction**
  Status: `pending`
  Goal: minimize every discrepancy and retain the minimized case.
  Acceptance: the minimized case reproduces the original divergence; no discrepancy is closed by widening a mask or editing an expected value without a **source-grounded** justification (`EVD-05`, `AI-05`).

- ID: `P2-SCALAR.7` — **snapshot and replay for implemented boundaries** — `G-REPLAY`
  Status: `pending`
  Goal: demonstrate replay only for the state boundaries actually implemented.
  Acceptance: a mid-execution snapshot captures all future-relevant pending state or is not offered at all.

- ID: `P2-SCALAR.8` — **portability matrix** — `G-PORTABILITY`
  Status: `pending`
  Goal: native x86-64 and AArch64 execution fixtures agree; the selected pure-Rust primitive/state/endian tests pass their pinned Miri and cross-endian plan.
  Acceptance: both native hosts are **mandatory**; if the infrastructure is unavailable the profile stays experimental and the gate reads `incomplete` — no "when available" clause (`RUST-05`, `docs/EVIDENCE_AND_GATES.md` §7).

- ID: `P2-SCALAR.9` — **the `CPU-LAB` release** *(task card `T009`)* — `G-RELEASE`
  Status: `pending`
  Goal: a reproducible gate report from pinned inputs, explicit capability limits, a named release decision, and a versioned accepted artifact.
  Acceptance: fidelity reported **separately** per axis (`SCP-05`); "supports RV64I" appears nowhere.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `P2-SCALAR.2` | `pending` | scope is fully exercised (`.1`); boundary values and shift corner cases are the next evidence layer the gate enumerates |

## Decisions

- `2026-09-13`: "Locked" means a **versioned accepted profile whose evidence is attached to its
  exact inputs**. A semantic fix invalidates affected evidence and produces a new accepted
  version. It never means errors become unfixable (`ROADMAP.md` §5).
- `2026-09-29` (leaf `.1`, reviewed ceiling expansion): the unit's guest corpus grows from 4
  to 9 programs (+10 tracked files under `profiles/rv64i-lab-v0/guests/`) as the planned
  scope completion — the `profiles/` surface's contract expands with it, so
  `doctrine/readme_routes.tsv`'s `ceiling_lines` for `profiles/` rises 30 → 34 (32 + two
  files of headroom, per the registry's proportional-headroom rule). Demotion was considered
  and rejected: the guests' canonical home is the unit's `guests/` directory — the
  generator, the smoke experiment and the coverage gate all read exactly there, and a
  second guest root would fragment the corpus the gates enumerate. Any FURTHER guest growth
  (`.2`'s boundary cases are a candidate) is its own reviewed decision at its own leaf.

## Open Questions

- Is x86-64 **and** AArch64 CI infrastructure available at release time? If not, the honest
  outcome is `incomplete` or an explicitly narrower, labelled host policy (`RK14`).

## Blockers

- ~~`P1-LAB` gate `G1`.~~ G1 was RUN `2026-09-29` (verdict `incomplete`): criteria 1–5 met,
  criterion 6 (the C-toolchain guest) routed INTO this tree's `.5`. Scope work (`.1`–`.4`)
  does not depend on criterion 6.

## Defects found in flight (owned here per the defect-ownership rule)

- **`2026-09-29` — reserved-`fm` FENCE executes as a nop; `D-FENCE` says it must raise
  illegal-instruction.** Reproduce: assemble word `0x1ff0000f` (fence, `fm=0x1`) into a
  two-word ELF and `cargo run -p semulith-cli -- run <elf> --steps=2` — the trace decodes
  `fence` and nops it. The fragment fixes only bits 14..12/6..2/1..0 for `fence`, so every
  `fm` value decodes, while the profile records *"Other fm values are reserved and fall
  under D-RESERVED-DECODE"* (illegal-instruction, a laboratory policy over an UNSPECIFIED
  case). Impact: the model accepts encodings its own dossier calls reserved — invisible to
  the guests (none encodes a reserved `fm`). **Owner: `P2-SCALAR.3`** (reserved cases keep
  their source meaning, `SEM-07`); the fix needs a legality constraint the encoding format
  does not yet express (decode-validity beyond bit-matching), so it is scheduled, not
  folded into `.1`. Logged by `P2-SCALAR.1` scoping.

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

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-29` | `P2-SCALAR.1` | `scripts/check_exercise_coverage.sh` (pre-registration RED) | 15/52, rc=1 — all 37 missing forms named against the real corpus |
| `2026-09-29` | `P2-SCALAR.1` | `scripts/check_exercise_coverage.sh [--self-test]` | GREEN 52/52; self-test 7 pass / 0 fail |
| `2026-09-29` | `P2-SCALAR.1` | `cargo test -p semulith-verify` | 133 passed / 0 failed (+5 guest suites; census pin over 9 guests incl. scope-mem's 17 crossings) |
| `2026-09-29` | `P2-SCALAR.1` | `scripts/run_semulith_smoke.py` (live, sail-riscv 0.14 + spike 1.1.1-dev) | 9 guests agree on 117/117 aligned steps; ecall = cause 0x0B/tval 0, ebreak = cause 0x03/tval=pc on all three models; every run reproduces byte-identically |
| `2026-09-29` | `P2-SCALAR.1` | `make check`, `make gate`, `make smoke-bench`, wasm build | rc=0; 24 doctrines green; 13 bench arms (9 clean guests); PORT-WEB rc=0 |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `P2-SCALAR.1` | `SEMILITH-PS-0001 (leaf P2-SCALAR.1): …` | the declared scope completed and gated: five guests, EXERCISE-COVERAGE (24th doctrine), fence fields from the pinned table, ecall/ebreak adapter spellings, 117/117 live; the reserved-`fm` defect logged for `.3` |

## Changelog

- `2026-09-13`: Created from `ROADMAP.md` §P2 and task cards `T008`–`T009` by `SEMULITH-TREES.2`.
