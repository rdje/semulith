# P0-PROFILE: select the first experiment and prove an evidence path exists

## Metadata

- Tree ID: `P0-PROFILE`
- Status: `done` (reopened once, for `.10` — a measured defect the first nine leaves carried)
- Roadmap lane: `ROADMAP.md` §6 → **P0 — Select and establish the first experiment**
- Gate: `G0`
- Depends on: nothing
- Unlocks: `P1-LAB`
- Created: `2026-09-13`
- Owner: repo-local workflow

## Goal

Produce `rv64i-lab-v0` as a **development** profile with every foundational choice resolved, and
demonstrate — by running it — that a reference path capable of supplying expected results for
that profile actually works. Deliver the state inventory, the requirements-catalog seed, the
environment contract, three representative guest programs, and the evidence-obligation policy.

## Non-Goals

- No privileged-system support is implied. Selecting RV64I is not a claim that the laboratory
  constitutes a fully specified privileged processor (`ROADMAP.md` §1).
- No instruction semantics are implemented here; prototype support may begin with a small
  declared subset, and the **accepted P2 profile covers its entire declared scope**.
- No RV32 deliverable. Scalar machinery is validated directly at 64 bits (`ROADMAP.md` §1).

## Acceptance Criteria — gate `G0`

1. Foundational semantics are **resolved**: every choice the declared scope needs has an answer
   with a source locator, or is an explicitly recorded open question with an owner.
2. An actual evidence path **works**: at least one matched-profile experiment has been run and
   reproduced, including a failure/event case and not only arithmetic.
3. Profile and reference **differences are enumerated** — not assumed absent.

> Reference acquisition is work with observable outcomes, not an unchecked URL list. Rule
> `SRC-03` forbids recording tool availability that has not been established.

## Task Tree

- ID: `P0-PROFILE.1` — **profile dossier `rv64i-lab-v0`** *(task card `T000`)*
  Status: `done`
  Goal: RV64I instruction scope, one core, little-endian ordinary memory, explicit entry state, memory boundaries, access and misalignment policy, instruction-fetch rules, environment-trap reporting; the applicable specification revision pinned by exact locator.
  Acceptance: every field has a source locator or a recorded open question with an owner; `SCP-02`'s transitive dependency closure resolved for every included feature.
  Verification: 20 decisions, all sourced; 52 mnemonics enumerated and gated; 5 open questions with owners and due points.
  Commit: `SEMULITH-P0-0013`

- ID: `P0-PROFILE.2` — **state inventory**
  Status: `done`
  Goal: registers, widths, aliases, overlaps, reset values, and any hidden or pending state that can influence a future supported observation (`SEM-08`, catalog `C02`).
  Acceptance: each entry source-linked; alias interactions stated, not implied.
  Verification: see the Verification Log.
  Commit: `SEMULITH-P0-0014`

- ID: `P0-PROFILE.3` — **requirements catalog seed**
  Status: `done`
  Goal: `requirement.schema.json` records for the declared scope, with `source_semantics` distinguishing defined / implementation-defined / unspecified / reserved, and `research_status` kept separate from `implementation_status`.
  Acceptance: every record validates; every record carries a real `source_refs` locator; no record claims `resolved` research status without one.
  Verification: 25 records, one per decision, all valid; 3 sources, all pinned; 2 records `partial` with their open question named; statements identical to `profile.toml`.
  Commit: `SEMULITH-P0-0026`

- ID: `P0-PROFILE.4` — **environment contract v0** *(task card `T002`)*
  Status: `done`
  Goal: the versioned assumption/guarantee set from `docs/CPU_ENVIRONMENT.md` §2–§3 — address units, access widths, virtual-time domain, permitted event-delivery points, ordering constraints — each with its authority (`architecture` / `implementation-profile` / `platform` / `laboratory`).
  Acceptance: laboratory policy nowhere overrides an architectural requirement; positive **and negative** fixtures defined for each obligation.
  Verification: 33 obligations (25 CPU guarantees, 8 environment assumptions); all 10 §2 boundary items dispositioned; 66 checks declared; both rules fired RED on the real contract.
  Commit: `SEMULITH-P0-0027`

- ID: `P0-PROFILE.5` — **reference candidate dossier** *(task card `T001`, part 1)*
  Status: `done`
  Goal: for each candidate (Sail RISC-V, Spike, ACT4) record exact source/build availability, supported features, invocation, trace granularity, injection capability, effective configuration, artifact hashes, adapter version, and restrictions on use or shipping (`docs/EVIDENCE_AND_GATES.md` §5, `SRC-01`).
  Acceptance: every field is an observed fact; a candidate that could not be obtained is recorded as such, with the attempt.
  Verification: 3 models obtained and run; 1 corpus located and deliberately not acquired; 3 attempts recorded, one of them a name collision.
  Commit: `SEMULITH-P0-0020`

- ID: `P0-PROFILE.6` — **matched-profile smoke test** *(task card `T001`, part 2)*
  Status: `done`
  Goal: run at least one real experiment against the selected reference with a matched configuration — independently encoded arithmetic **and** an access/trap case — and reproduce it.
  Acceptance: actual traces, hashes and configs recorded; mismatches and missing injection capabilities documented. **A reference is not usable until this leaf passes.**
  Verification: 2 experiments; 2 models agreeing over 15 aligned steps; 12 of 12 specification-derived expectations; 4 differences enumerated; both reproduce byte-identically.
  Commit: `SEMULITH-P0-0021`

- ID: `P0-PROFILE.7` — **independence inventory**
  Status: `done`
  Goal: per subsystem, whether two comparators share semantic code or expected-result derivation (`EVD-04`). ACT4 computes expected results with a configured Sail model; TestFloat ordinarily derives from SoftFloat.
  Acceptance: known common ancestry **and** unknown ancestry both recorded; neither independence nor correlation assumed.
  Verification: 6 pairs recorded across 4 verdict classes, including 2 `not-examined`; the FP correlation measured (184 of 199 files byte-identical) and routed to `P4-SYSTEM.7`.
  Commit: `SEMULITH-P0-0023`

- ID: `P0-PROFILE.8` — **three representative guest programs**
  Status: `done`
  Goal: small freestanding programs that exercise arithmetic, control flow, and a memory/fault boundary, with independently derived expected observations.
  Acceptance: expected values are derived from the specification, not from any model's output.
  Verification: 3 programs (arithmetic, control flow, memory/fault); 28 expected values and 3 negative observations, all sourced; both models agree over all three; the B/J layouts derived from a pinned table rather than typed.
  Commit: `SEMULITH-P0-0028`

- ID: `P0-PROFILE.10` — **match the PLATFORM, not only the instruction set**
  Status: `done`
  Goal: the matched-profile override configured the ISA and nothing else, so the reference kept a device-bearing default platform underneath a correct ISA string. Configure the platform, correct every claim that rested on the unconfigured one, and hold the repair with a negative fixture.
  Acceptance: the probes that exposed it now fault; the original guests still agree; every refuted claim is corrected at its source, not reworded.
  Verification: see the Verification Log.
  Commit: `SEMULITH-P0-0031`

- ID: `P0-PROFILE.9` — **evidence-obligation policy and the `G0` report**
  Status: `done`
  Goal: declare, *before* implementation, what kind of evidence each obligation class requires (`EVD-03`); then generate the gate report from pinned inputs.
  Acceptance: the report names inputs, commands, actual results and limitations (`EVD-08`), and reads `passed` or `incomplete` — never `passed` with a missing required check.
  Verification: the policy declared before any model exists; the report GENERATED from tracked inputs and gated; verdict `incomplete` on 66 declared checks against 0 implemented.
  Commit: `SEMULITH-P0-0029`

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| — | — | — | **tree complete (10/10), reopened once.** Gate `G0` has been RUN and reads **`incomplete`** — its three criteria are met, and 66 declared checks are unimplemented, which is the honest reason it is not `passed`. ⛔ `.10` corrected a defect the first nine leaves carried: the profile was matched on its instruction set and not on its platform. The next tree is `MODEL-BOOKS` (unblocked by `.10`), then `P1-LAB`. Open either only with the repository clean (the pivot rule). |

## Decisions

- `2026-09-13`: first CPU is a small **RV64I** profile in a specified laboratory execution
  environment (`ROADMAP.md` §1). Revisit only if archogen's named first target makes another
  width or feature set more useful, which is a P0 input.
- `2026-09-14`: the reference route is **three obtained models** — Sail RISC-V (primary
  candidate), Spike, QEMU — with ACT located and deliberately unacquired. Recorded in
  [`decision_reference-acquisition-route`](../decisions/decision_reference-acquisition-route.md).
  It supersedes the roadmap's *cost estimate* and nothing of its reasoning: acquisition is still
  work with observable outcomes, it simply turned out to be cheap. **It does not choose the
  primary oracle** — `.6` does, by running an experiment.

## Open Questions

- ~~Which reference becomes the primary oracle?~~ **Answered by `.6`:** `sail-riscv` 0.14 is the
  primary, with `spike` as the second comparator — both now satisfy §5's condition, having run a
  reproduced matched experiment. QEMU remains obtained and un-exercised. The choice of *primary*
  rests on Sail's declarative JSON configuration, which let the profile's decisions be matched as
  data rather than as command-line flags.
- **NEW (`.6`): where do instruction ENCODINGS come from?** The pinned specification does not
  contain them — the format diagrams are images, and a census over all six pinned artifacts finds
  zero seven-bit opcode patterns. Encodings come from a separately pinned `riscv-opcodes`, which
  is upstream of both models, so encoding agreement is *not* independent. Recorded in
  `references.toml`; the B/J immediate layouts remain unreadable and are owned by `.8`.
- Does archogen's `rt-static-up-v1` profile need machine-mode features this profile excludes?
  `docs/ARCHOGEN_INTEGRATION.md` §6 says a provisional machine-mode profile may be smaller than
  the Linux profile — compare during `.1` when archogen's target decision is available.

## Director input wanted — ✅ RESOLVED BY MEASUREMENT, `2026-09-14`

**No input is needed; the question dissolved when it was tested.** The section below is kept as
written so the estimate can be compared with the outcome. What actually happened: Sail RISC-V
0.14 publishes a **prebuilt native binary for this host's architecture**, so no OCaml/opam
toolchain was required to run it; Spike built from source against the system toolchain in a few
minutes with no new dependency installed; and QEMU, already present, offers a CPU model literally
named `rv64i`. Three models, obtained, matched-configured, in one leaf.

The one failure is the instructive part: the host package manager's `sail` formula is a WordPress
deployment CLI, an exact name collision. See
[`decision_reference-acquisition-route`](../decisions/decision_reference-acquisition-route.md).

<details><summary>The original estimate, preserved</summary>

`P0-PROFILE.5`/`.6` require a **real** reference model, and acquiring one is the first activity
in this project whose cost is not obviously bounded:

- **Sail RISC-V** generates a C++ simulator and supports JSON configuration, which is the best
  fit for a matched-profile experiment — but building it needs an OCaml/opam toolchain, and
  policy 13 (project data on the repository volume) means `OPAMROOT` and the build prefix must
  be redirected under the repo rather than into `~/.opam`.
- **Spike** is a second implementation path with a lighter C++ build, but its subsystems'
  independence from Sail has to be examined rather than inferred (`EVD-04`).
- A **prebuilt binary**, if one exists for this host, would shorten the path — at the cost of
  knowing less about its effective configuration, which `docs/EVIDENCE_AND_GATES.md` §5
  requires to be recorded exactly.

The default, absent other direction, is: attempt Sail from source with a repo-local `OPAMROOT`,
record the actual outcome either way, and fall back to Spike if the build is not tractable.
`SRC-02` makes an honest *"no reference route"* a legitimate result that bounds the claim rather
than a failure.

</details>

## Blockers

- None.

## Acceptance Checklist (current leaf — `P0-PROFILE.10`)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHERE: the override at
  `reference/sail-rv64i-lab-v0.override.json` set `base`, `memory.misaligned` and `extensions`.
  WHY: `--print-isa-string` returned `rv64i_zvl32b` and that was read as *"matched"* — but an ISA
  string describes an **instruction set**, not a machine. Underneath it the reference kept its
  default platform. Established by probe rather than by reading the config:

  ```
  $ grep -c '"platform"' profiles/rv64i-lab-v0/reference/sail-rv64i-lab-v0.override.json
  0                                    # the platform was never configured, only the ISA
  $ sail_riscv_sim --config-override <override> --trace-clint  probe-time.elf
  [5] ld x1, 0x0(x10)
  clint[0x000000000000BFF8] -> 0x0000000000000002
  x1 <- 0x0000000000000002
  [6] ld x2, 0x0(x10)
  clint[0x000000000000BFF8] -> 0x0000000000000003     # ADVANCING
  ```

  A guest read a monotonically advancing time source with a **plain load** — no CSR instruction —
  which is why excluding `Zicsr` never excluded reading time. Four committed claims are refuted:
  `OB-ENV-VIRTUAL-TIME` ("no time source is modelled"), `OB-ENV-EVENT-DELIVERY` ("no interrupt
  controller ... no privileged mode"), `D-MAIN-VS-IO` ("no I/O region is declared") and
  `privilege_modes = []` — every trace line in this repository reads `[M]`, because a RISC-V hart
  is always in at least machine mode.
  ⛔ This is the `zero-hits-absence-or-blindness` lesson in a new costume: not an instrument that
  could not see, but **an instrument answering a narrower question than the one asked**. It gave a
  single confident string, and the string was true.

- [x] **ADDRESSED (verified)** — corrected at source, not reworded. The override now configures
  `platform.clint.supported = false`, the interrupt generator off, all three machine interrupt
  sources off, and `memory.regions` reduced to the single MainMemory region the profile declares.
  Before → after on the two probes, same binaries:

  ```
  before: clint[0x…BFF8] -> 0x2 ; x1 <- 0x2          # a device answered
  after : trapping from M to M to handle load-access-fault
          handling exc#load-access-fault … tval=0x000000000200BFF8
  ```

  `profile.toml` gains `D-PLATFORM` and corrects `D-MAIN-VS-IO` and `privilege_modes = ["M"]`;
  decisions 25 → 26, requirements 25 → 26, obligations 33 → 34, all regenerated and validating
  (`RECORD-SCHEMA: ok (5 record file(s) …)`). Recorded differences 4 → 6.

- [x] **NO REGRESSION** — leg 2, and the load-bearing measurement is that the repair changed
  nothing it should not: `scripts/run_smoke.py` → all three original guests still
  `AGREE over 12 / 13 / 3 aligned step(s)` and reproduce byte-identically. The repair is held
  permanently by a **tracked negative fixture**, `guests/guest-no-device.s`, which reads CLINT
  `mtime` and must fault — so a device becoming reachable again turns the run red rather than
  quiet. Whole gate `=== all doctrines green ===`; `make check` →
  `test result: ok. 1 passed; 0 failed`.
  ⭐ **Spike is not platform-matched and cannot be**, which is enumerated rather than fixed. It
  services the same device load (`mem 0x0000000002000000`); its interruptor is built in and
  `--device` only *adds* MMIO plugins; and `-m0x80000000:0x10000` kills its own reset vector
  (`trap_instruction_access_fault, epc 0x0000000000001000`). `SRC-02` makes that a legitimate
  result that **bounds** the claim: any guest touching `0x1000` or `0x0200_0000..0x11ff_ffff`
  behaves differently on the two references. The three original guests touch neither — which is
  now a **stated precondition rather than luck**.
  ⚠️ Honest scope of the repair: it makes the SAIL reference match the profile. It does not make
  the profile's environment contract true of every reference, and `DIFF-PLATFORM-SPIKE` says so.

- [x] **FIX** — the override gains `platform` and a MainMemory-only `memory.regions`;
  `profile.toml` gains `D-PLATFORM` and corrects two claims; the two refuted obligations are
  rewritten to say *why* the absence is real (a platform property, not an instruction-set one);
  `guest-no-device.s` + expectations added; the comparator learns the access-fault spellings; the
  runner honours a recorded `cross_model = false` and **prints the skip** rather than applying it
  silently.

- `promotion: declined (the lesson is recorded where it bites — ENVIRONMENT.md's closing section, DIFF-PLATFORM-DEFAULT, and this box; the existing zero-hits-absence-or-blindness card already carries the neighbouring rule and a second card would restate both)`

- [x] **LOCKSTEP** — leg 3: the repair is re-run by `scripts/run_smoke.py` on demand and the
  corrected records are re-validated on every commit. `G0-REPORT.md` regenerated (6 differences,
  26 requirements, 34 obligations, 68 declared checks); `DOSSIER.md`, `ENVIRONMENT.md`,
  `MEMORY.md`, `LIVE_STATUS.md`, `CHANGELOG.md`, `DEV_NOTES.md` updated in this commit.
  ⚠️ **What this says about `G0`.** Criterion 3 is *differences enumerated, not assumed absent* —
  and for four leaves this profile carried differences it had assumed absent. The verdict stays
  `incomplete` for the same reason as before (68 declared checks, 0 implemented), but criterion 3
  is now met on evidence rather than on an unexamined configuration.

### `P0-PROFILE.9` — the evidence policy and the gate report

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1: eight leaves had produced a profile, a state
  inventory, 25 requirements, 33 obligations, three reference models and three guest programs —
  and **nothing said whether `G0` passed.** `EVD-03` also requires the *kind* of evidence each
  obligation needs to be declared BEFORE the implementation that would otherwise choose whatever
  evidence it can most easily produce. Census before this leaf:

  ```
  $ git ls-files profiles | grep -cE 'EVIDENCE_POLICY|G0-REPORT'
  0
  $ git ls-files crates                      # what would have shaped the policy, if it existed
  crates/app/Cargo.toml
  crates/app/src/main.rs                     # still the scaffold's placeholder
  ```

  The second command is the point: the policy is declared while **there is no model**, so nothing
  in it can have been reverse-engineered from what a model currently happens to do.

- [x] **ADDRESSED (verified)** — `EVIDENCE_POLICY.md` declares five obligation classes and what
  closes each, and `G0-REPORT.md` is **generated** from tracked inputs:

  ```
  $ scripts/gate_report.py rv64i-lab-v0
  wrote profiles/rv64i-lab-v0/G0-REPORT.md
  $ head -8 profiles/rv64i-lab-v0/G0-REPORT.md | tail -1
  **Verdict: `incomplete`.**
  $ scripts/check_gate_report.sh
  GATE-REPORT: ok (1 generated report(s) in sync with their inputs)
  ```

  The verdict is `incomplete` for a stated, measured reason — **66 declared checks, 0
  implemented** — and all three `G0` criteria are recorded as met: semantics resolved (every
  requirement sourced, 2 honestly `partial` with their open question named), an evidence path that
  works (2 experiments, 2 models, reproduced), and differences enumerated (4 recorded differences,
  6 independence records across 4 verdict classes).
  ⭐ The report reads nothing untracked, so it regenerates byte-identically in a fresh clone with
  no reference binaries present — which is what lets a gate check it for staleness at all.

- [x] **NO REGRESSION** — leg 2. `scripts/check_gate_report.sh --self-test` → `3 pass / 0 fail`,
  and the gate was fired RED on the **real** report by hand-editing exactly the word that matters:

  ```
  $ sed -i 's/`incomplete`/`passed`/' profiles/rv64i-lab-v0/G0-REPORT.md && scripts/check_gate_report.sh
  GATE-REPORT: profiles/rv64i-lab-v0/G0-REPORT.md is out of sync with the inputs it is generated from.
      8c8
      < **Verdict: `incomplete`.**
      ---
      > **Verdict: `passed`.**
  ```

  Restored to `ok`. Whole gate `=== all doctrines green ===`; `make check` →
  `test result: ok. 1 passed; 0 failed`; `scripts/run_smoke.py` → `ok`;
  `scripts/fetch_references.sh --verify-only` → 11 of 11 `MATCH`.
  ⛔ **The generator was wrong twice before it was right, and both errors inflated the verdict.**
  Asked which checks are implemented, it first grepped the whole tree for the id *pattern* and
  counted `EVIDENCE_POLICY.md` — a document that merely describes the naming convention. Narrowed
  to `scripts/`, it still counted `check_requirements.sh`, which tests for the `-POS`/`-NEG`
  suffix as part of enforcing that the ids exist — *a gate about checks is not a check*. Both
  reported `1 are implemented` where the truth is `0`. The measure is now exact: take the concrete
  ids the contract declares and ask which any tracked executable names. A gate report that cannot
  tell a mention from an implementation is a gate report that will eventually read `passed`.
  ⛔ And the evidence policy's own first draft stated class populations **and got two wrong** — by
  reading the profile's *authority* distribution (14/8) instead of the requirements' *category*
  distribution (13/10), which is exactly the non-mechanical mapping this profile documents. The
  counts were removed from the policy entirely; the generated report derives them.

- [x] **FIX** — `profiles/rv64i-lab-v0/EVIDENCE_POLICY.md` (declared first, and carrying no
  counts), `scripts/gate_report.py` (derives the report from tracked inputs, with no code path to
  `passed` while declared checks exceed implemented ones), `profiles/rv64i-lab-v0/G0-REPORT.md`
  (generated), and `scripts/check_gate_report.sh` registered as `GATE-REPORT`.

- `promotion: declined (the lesson IS the GATE-REPORT doctrine header and gate_report.py's docstring — both state the mention-versus-implementation rule and why 'passed' is unreachable; a card would restate them verbatim)`

- [x] **LOCKSTEP** — leg 3: the report is regenerated and compared on every commit, so the verdict
  cannot be reached with an editor. `DOSSIER.md`, the book's P0 chapter, `MEMORY.md`,
  `LIVE_STATUS.md`, `CHANGELOG.md`, `DEV_NOTES.md` updated in this commit, and the tree closed.
  ⚠️ **What `G0 = incomplete` does and does not mean.** It does **not** mean the milestone failed:
  its three criteria are met and recorded. It means the declared evidence does not yet exist,
  which is the correct state for a milestone whose job was to *establish* what evidence would be
  required. `P1-LAB` is where the 66 checks acquire fixtures, and `passed` becomes reachable only
  then.

### `P0-PROFILE.8` — the third guest program

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1: this leaf was **blocked on a source, not on effort**,
  and `.6` had recorded exactly why. The B and J formats scatter their immediate across
  non-adjacent bits, and that layout is one of the things the pinned specification renders only as
  an image. Re-measured here, and the prose was read to be sure it was not hiding the layout:

  ```
  $ grep -cE '[01]{7}' intro.html rv32.html rv64.html intro.txt rv32.txt rv64.txt
  0  0  0  0  0  0
  ```

  The prose gives the SEMANTICS — *"the J-immediate encodes a signed offset in multiples of 2
  bytes … added to the address of the jump instruction"*, *"the conditional branch range is
  ±4 KiB"* — and never a bit position. `scripts/riscv_asm.py` refused both formats rather than
  typing a layout from memory, which is why `smoke-arith` and `smoke-trap` contain no control flow.

- [x] **ADDRESSED (verified)** — the layout is now **derived from a pinned machine-readable table**,
  `riscv-opcodes`' own `src/riscv_opcodes/constants.py`:

  ```
  "bimm12hi": "imm[12|10:5]"    "bimm12lo": "imm[4:1|11]"
  "jimm20":   "imm[20|10:1|11|19:12]"
  ```

  ⭐ The derivation is **self-validating**: the bits each descriptor accounts for must total
  exactly the width of the field it fills, and `load_immediate_layout()` refuses the table
  otherwise. All four reconcile — `imm20` 20/20, `bimm12hi` 7/7, `bimm12lo` 5/5, `jimm20` 20/20.
  A layout this module cannot reconcile is a layout it will not use.
  Guest programs went from `2` to `3`, and the third is the one that needed this:

  ```
  $ scripts/run_smoke.py
    PASS  guest-control: assembled  12 instruction(s), 13 executed step(s)
    PASS  guest-control: 13 specification-derived expectations
    PASS  guest-control: 2 register(s) that must never be written
    PASS  guest-control: sail-riscv vs spike  AGREE over 13 aligned step(s)
  run_smoke: ok
  ```

  Expected values went from 12 to **28 across three programs**, plus **3 negative observations**,
  each with its derivation and source locator — counted rather than asserted:

  ```
  $ grep -c '^\[\[step\]\]' profiles/rv64i-lab-v0/guests/*.expected.toml
  guest-control.expected.toml:13   smoke-arith.expected.toml:12   smoke-trap.expected.toml:3
  $ shasum -a 256 target/refs/guests/guest-control.elf
  e9cd138de6562acae810cbcefc56ecd658b65d2de70bcf7634c45e8cc65f7504
  ```
 An independent decoder confirmed the scrambled
  immediates before any model ran them: `spike-dasm` returned `bnez ra, pc - 4` and
  `jal sp, pc + 0x8` for the offsets requested.
  The acquisition tool gained the strongest cheap control available, now permanent:
  `MATCH encoding tables vs profile scope  52 == 52, symmetric difference NONE`.

- [x] **NO REGRESSION** — leg 2. ⭐ The negative observations were fired RED **behaviourally**, by
  breaking the program rather than the expectation: changing `jal x5, over` to `jal x5, 4` so the
  jump skips nothing gave `guest-control: 2 register(s) that must never be written — but ['x6']
  were written`, plus five shifted positive expectations. That is what a negative fixture is for:
  a control transfer that fails to skip writes a register nobody was watching.
  Two further controls on the acquisition tool: a corrupted encoding digest →
  `DIFFERS encoding source constants.py`; removing `FENCE` from the profile →
  `DIFFERS encoding tables vs profile scope … tables enumerate 52, profile declares 51,
  symmetric difference: fence`. Both restored.
  Whole gate `=== all doctrines green ===`; `make check` → `test result: ok. 1 passed; 0 failed`;
  all three programs reproduce byte-identically; `RECORD-SCHEMA` still `ok`.
  ⛔ **A control that PASSED is recorded as a finding, not quietly dropped.** Replacing the JALR
  offset `+13` with `+12` changed nothing — both land on `0x80000028`, *because* the low bit is
  cleared. So the landing address alone does not discriminate `D-JALR-LSB`; what discriminates is
  that execution continues normally instead of attempting the misaligned fetch a model keeping the
  odd bit would make. Both available references clear the bit, so **the failing branch of that
  test has never been observed here**. It is tested evidence for the behaviour, not a
  discrimination between two behaviours, and the expectations file says so in a `limit` field.
  Owner of a real control: `P1-LAB`'s validator mutation suite, which can mutate *our* model.
  ⛔ The runner was also caught conflating **assembled instructions** with **executed steps** —
  equal for straight-line code, and wrong the moment a loop exists (`guest-control` has 12
  instructions and runs 13). The bound now comes from the expectations file.

- [x] **FIX** — `scripts/riscv_asm.py` gains `load_immediate_layout()` (parse + reconcile),
  B/J encoding, and two-pass label resolution; `guest-control.s` and expectations for it and for
  `smoke-trap`; `run_smoke.py` checks `never_written` and bounds by executed steps;
  `references.toml` gains the pinned `[[encoding_source]]` with four file digests;
  `fetch_references.sh` re-derives them and the 52-vs-52 cross-check.

- `promotion: declined (the derive-and-reconcile rule is stated in riscv_asm.py's docstring, the negative-fixture rule in ENVIRONMENT.md, and the JALR limit in the expectations file itself — which is where the next reader of that test will meet it)`

- [x] **LOCKSTEP** — leg 3: all three programs are re-run by one command and every encoding input
  is re-derivable by another. `DOSSIER.md`, the book's P0 chapter, `MEMORY.md`, `LIVE_STATUS.md`,
  `CHANGELOG.md`, `DEV_NOTES.md` updated in this commit.
  ⚠️ Stated plainly: the encoding source is upstream of **Spike** and not of **Sail**, so Sail
  decoding these bytes is an independent confirmation and Spike doing so is not — the
  `[[independence]]` record for the encoding subsystem already says this, and these programs do
  not change it.
  ⛔ **A ceiling fired during this leaf and was obeyed, not raised.** `CHANGELOG.md` crossed its
  bound (`OVER CEILING CHANGELOG.md: 66708 bytes > 65536`), and the routes registry's own owner
  column prescribes the response — *"git history is canonical; shard when the ceiling fires"*. The
  pre-`P0-PROFILE.5` entries moved **unedited** to `docs/changelog/2026-09-pre-p0.md`, leaving
  `CHANGELOG.md` at 32,487 bytes. The new directory was **registered in the same commit that
  created it**, with its own per-part, file-count and aggregate ceilings: sharding a capped file
  into an ungoverned neighbour is the exact failure that registry exists to prevent, and it would
  have looked like a fix. `README-ROUTING-CLOSURE: ok (26 governed destination(s))`.

### `P0-PROFILE.4` — the environment contract

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1: `.3` minted 25 `OB-*` obligation ids and nothing
  defined them; the gate said so in its own header as a **named gap**. More broadly, `SCP-01`
  needs four artifacts and only two existed. Census before this leaf:

  ```
  $ scripts/check_requirements.sh --audit | grep -A1 'profiles/'
  profiles/rv64i-lab-v0/  (ENFORCED)
    requirements 25 | obligations 0
  $ git ls-files profiles | grep -c 'obligation\|ENVIRONMENT'
  0
  ```

  WHERE it bit: `docs/CPU_ENVIRONMENT.md` §3 requires five things represented **explicitly** —
  address units, access widths, virtual-time domain, event-delivery point, ordering — and two of
  them turn out to be *"none"* for this profile. A "none" that is simply absent from a contract is
  indistinguishable from one nobody considered.

- [x] **ADDRESSED (verified)** — 33 obligations: 25 CPU guarantees (one per decision, generated
  from the requirements so the ids close by construction) and 8 environment assumptions.

  ```
  $ scripts/check_requirements.sh
  RECORD-SCHEMA: ok (5 record file(s) validate and agree with their profile)
  $ scripts/check_requirements.sh --audit
  profiles/rv64i-lab-v0/  (ENFORCED)
    requirements 25 | obligations 33
    named but undefined : none
    unnamed cpu-guarantees (a finding)        : none
    obligations with no negative check : none
  ```

  Obligation ids resolving went from `0 of 25` to `25 of 25` — **`.3`'s named gap is closed**, and
  closed by a rule rather than by assertion. All ten of §2's boundary items are dispositioned in
  `ENVIRONMENT.md`: four in scope, **six out of scope each with its reason**, because an
  undispositioned row is how a boundary silently leaves coverage. 66 checks declared, a positive
  and a negative for every obligation.
  ⭐ Two obligations are *"none"* and say why, which is the leaf's most useful output.
  `OB-ENV-VIRTUAL-TIME`: no clock, cycle or instruction counter is architecturally readable, and
  the harness's retired-instruction count is explicitly **not target-visible** so it may never
  justify guest-observable behaviour. `OB-ENV-EVENT-DELIVERY`: no asynchronous interrupt is
  deliverable *by construction* — there is no controller, mode or CSR with which to enable, mask
  or report one, so the contract has no legal delivery point to specify.

- [x] **NO REGRESSION** — leg 2. Both new rules were fired RED on the **real** contract:
  setting `OB-SHAMT`'s checks to positives only gave
  `NO NEGATIVE CHECK … lack a positive AND a negative fixture`, and relabelling `OB-WSUFFIX` as a
  laboratory choice gave `AUTHORITY DOWNGRADE contract-obligations.jsonl [OB-WSUFFIX]: its
  requirement 'REQ-D-WSUFFIX' is architecturally 'defined' …`. Both restored.
  ⭐ That second rule is the mechanical form of the contract's first sentence — *laboratory policy
  cannot override an architectural requirement* — and it bites in the direction that matters:
  mislabelling an ISA rule as a harness choice is how a real defect becomes an unfalsifiable
  "profile difference".
  `scripts/check_requirements.sh --self-test` → `15 pass / 0 fail` (11 → 15); 15 arms written,
  15 run. Whole gate `=== all doctrines green ===`; `make check` →
  `test result: ok. 1 passed; 0 failed`; `scripts/run_smoke.py` → still `ok`.

- [x] **FIX** — `profiles/rv64i-lab-v0/contract-obligations.jsonl` (33 records),
  `profiles/rv64i-lab-v0/ENVIRONMENT.md` (the contract, the authority mapping, the ten-row
  boundary disposition), and rules 6–7 in `RECORD-SCHEMA` with a `--audit` mode.

- `promotion: declined (both points are stated in ENVIRONMENT.md and in the RECORD-SCHEMA header, and the routed finding lives in this leaf's own ROUTING EVIDENCE section where the next reader of the tree will meet it)`

- [x] **LOCKSTEP** — leg 3: the contract is validated and cross-checked against the requirements
  on every commit, so an obligation cannot be dropped or downgraded silently. `DOSSIER.md` links
  the contract; the book's P0 chapter gains the section; `MEMORY.md`, `LIVE_STATUS.md`,
  `CHANGELOG.md`, `DEV_NOTES.md` in this commit.
  ⚠️ **Stated plainly: the 66 checks are DECLARED, not implemented.** They name fixtures `P1-LAB`
  will build; nothing executes them today. That is `EVD-03` working as intended — the required
  evidence is declared before the implementation that would be tempted to choose evidence it can
  most easily produce — but it must never be read as 66 passing checks.

## ROUTING EVIDENCE — the delivered examples' referential inconsistency, routed to `P1-LAB`

- **What was measured, here:** the new rules fired first not on this profile but on the *shipped*
  planning-package examples. `scripts/check_requirements.sh --audit`:
  `examples/` → `requirements 2 | obligations 1`, `named but undefined: ['OB-SYN16-ADD',
  'OB-SYN16-INPUT']`, `obligations with no negative check: ['CE-SYN16-INPUT']`. **Both** example
  requirements point at obligations that do not exist, and the one obligation that does exist is
  named by nobody.
- **Does it reproduce outside the family it is sent to?** Yes — it is a property of the delivered
  files, independent of any tree. It is routed rather than fixed because those files are
  `frozen-in-place` in `docs/provenance/planning-package-v0.2/dispositions.tsv`: editing them to
  satisfy a rule written later would destroy the record of what was delivered, which is the whole
  point of freezing them.
- **Why `P1-LAB`:** referential integrity across requirement / implementation / test / evidence
  links is `P1-LAB`'s graph checker (`ROADMAP.md` §P1, *"schema validation alone is not
  sufficient; referential integrity and dependency checks are required"*). This is that checker's
  first real corpus, and a corpus with known-broken links is worth more than a clean one.
- **What would make the routing wrong:** if the examples were ever un-frozen and adopted as a live
  fixture, the defect would become fixable here instead. `DELIVERY-PROVENANCE` would have to record
  that disposition change first, and nothing proposes it.
- **How the finding stays visible meanwhile:** `--audit` re-derives it on demand and labels it
  `advisory - frozen delivery artifacts`, so it is a command rather than a paragraph someone has
  to remember.

### `P0-PROFILE.3` — the requirements catalogue

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1: `SCP-01` requires a support claim to identify four
  artifacts — a versioned profile, an environment contract, an observation contract and the
  applicable specification revisions — and `profile.toml` says in its own header that it is the
  first of the four and the other three do not exist. WHERE the gap bit: the 25 decisions were
  prose in a TOML file, with nothing machine-readable linking a rule to a source, a risk, a
  dependency or an obligation. Census before this leaf:

  ```
  $ git ls-files profiles | grep -c requirements
  0
  $ ls examples/*.jsonl | wc -l          # records existed only for a synthetic 16-bit fixture
  3
  ```

  ⛔ And the validator that would judge them did not exist either, which is the part worth
  reporting: `jsonschema`, `fastjsonschema` and `pydantic` are all **absent** on this host, and
  installing one would place a dependency store on a different volume from the repository.

- [x] **ADDRESSED (verified)** — `profiles/rv64i-lab-v0/requirements.jsonl`: **25 records, one per
  decision**, generated from `profile.toml` rather than transcribed, so no statement can drift by
  typing.

  ```
  $ scripts/validate_records.py profiles/rv64i-lab-v0/requirements.jsonl schemas/requirement.schema.json
  __ERRORS__ 0
  $ scripts/check_requirements.sh
  RECORD-SCHEMA: ok (4 record file(s) validate and agree with their profile)
  ```

  Machine-readable requirement records went from `0` to `25`; the three shipped example files also
  validate for the first time (`__ERRORS__ 0` each), which is a claim nothing previously checked.
  Every record cites one of the three pinned sources — `RVI-RV64I` ×8, `RVI-RV32I` ×12,
  `RVI-INTRO` ×8 — with no empty locator. Two records are honestly `partial` with their open
  question named in the record itself (`REQ-D-SHIFTW-RESERVED` → `OQ-2`,
  `REQ-D-ECALL-EBREAK` → `OQ-5`); the other 23 are `resolved`, and all 25 are
  `implementation_status: planned`, because no CPU code exists.
  ⭐ `source_semantics.category` is **not** a mechanical function of the profile's `authority`
  field, and the judgement table says so: `laboratory` covers both *"the specification says
  UNSPECIFIED and we chose"* (`D-RESERVED-DECODE` → `unspecified`) and *"the specification
  delegates to the EEI and we chose"* (`D-ENTRY-STATE`, `D-CODE-VISIBILITY` →
  `implementation-defined`). Collapsing those two would have recorded a laboratory policy as an
  architectural rule, which is the exact failure `profile.toml`'s header warns about.

- [x] **NO REGRESSION** — leg 2. The validator was fired RED across **12 controls**, one per rule
  class it implements — missing required property, value outside an enum, wrong type, pattern
  violation, `minLength`, `minItems`, `uniqueItems`, undeclared extra property, a nested object
  missing a field, a nested array item malformed — plus the one that matters most:
  `REFUSED fixture: schema uses ['maximum'], which this validator does not implement`.
  ⛔ **That refusal is the soundness property, not a nicety.** A partial validator that silently
  ignores an unimplemented keyword reports `valid` for a document it never fully checked, and a
  schema gaining a keyword would quietly widen what passes.
  `scripts/check_requirements.sh --self-test` → `RECORD-SCHEMA --self-test: 11 pass / 0 fail`;
  11 arms written, 11 run. Fired RED on the **real** catalogue three times:
  `STATEMENT DRIFT … [REQ-D-WSUFFIX]`, `RESOLVED WITH AN OPEN QUESTION … [REQ-D-SHIFTW-RESERVED]`,
  `UNPINNED SOURCE … cites 'RVI-PRIVILEGED'`. Whole gate `=== all doctrines green ===`;
  `make check` → `test result: ok. 1 passed; 0 failed`; `make book` → `HTML book written`;
  `scripts/run_smoke.py` → still `ok`.
  ⛔ **Two defects in this leaf's own instruments were found by their arms, not by reading.**
  (1) The gate excluded `target/` with `"target" not in p.parts`, which tests the *absolute* path —
  and its own fixtures live under `target/doctrine-selftest/`, so every fixture was filtered away
  and ten arms failed with `no .jsonl record file found`. Now root-relative. (2) The cross-checks
  re-parsed a file that had already failed to parse, so a malformed record **crashed** the gate
  instead of failing it — a traceback is not a verdict. Both are the arms earning their keep.

- [x] **FIX** — `scripts/validate_records.py` (a JSON Schema validator for exactly the 17 keywords
  this project's three schemas use, censused rather than guessed, refusing everything else),
  `scripts/check_requirements.sh` registered as `RECORD-SCHEMA`, and the 25-record catalogue.

- `promotion: declined (both lessons ARE the RECORD-SCHEMA gate — the refusal rule is stated in its header and in the validator's docstring, and the authority-vs-category distinction is stated in profile.toml's header and the judgement table; a card would restate them verbatim)`

- [x] **LOCKSTEP** — leg 3: the catalogue is re-validated on every commit and is checked against
  the profile it describes, so a decision cannot change without its requirement failing.
  `DOCTRINE_ENFORCEMENT.md`, the book chapter and `TOOLBOX.md` updated;
  `MEMORY.md`, `LIVE_STATUS.md`, `CHANGELOG.md`, `DEV_NOTES.md` in this commit.
  ⚠️ **Named gap:** `obligation_ids` (25 `OB-*` ids minted here) are checked against nothing,
  because the environment contract that defines them is `P0-PROFILE.4`. The gate's header says so,
  and `.4` is now the frontier. `evidence_ids` are deliberately empty: real evidence exists from
  `.6`, but evidence *records* are `.9`'s deliverable and a dangling id would be worse than none.

## Completed-leaf evidence

Archived to [`archive/P0-PROFILE.md`](archive/P0-PROFILE.md) — the full, unedited acceptance
checklists for every `done` leaf. Split out when this file crossed its per-part ceiling; the
ceiling was obeyed, not raised.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-13` | `P0-PROFILE.1` | specification reachability, then acquisition | `HTTP 200`; three artifacts pinned and re-derived `MATCH` |
| `2026-09-13` | `P0-PROFILE.1` | profile enumeration vs declared count | `52` vs `52`, `agree: True` |
| `2026-09-13` | `P0-PROFILE.1` | `check_profile_consistency.sh --self-test` | `8 pass / 0 fail` (7 RED arms) |
| `2026-09-13` | `P0-PROFILE.1` | both instruments fired RED on the real corpus | `COUNT DRIFT … 51 vs 52`; `DIFFERS rv64.html` — each restored to `ok` |
| `2026-09-13` | `P0-PROFILE.1` | `scripts/check_doctrines.sh` + `make check` | `all doctrines green`, `rc=0`; `test result: ok. 1 passed` |
| `2026-09-13` | `P0-PROFILE.2` | reset-value claim measured against the sources | `grep -ci reset` → `rv32.txt:0`, `rv64.txt:0` |
| `2026-09-13` | `P0-PROFILE.2` | hidden-state census | `0` entries, `7` candidates checked, all absent |
| `2026-09-13` | `P0-PROFILE.2` | `check_profile_consistency.sh --self-test` | `13 pass / 0 fail` (11 RED arms) |
| `2026-09-13` | `P0-PROFILE.2` | both new rules fired RED on the real dossier | `UNEARNED NONE`; `XLEN MISMATCH 32 != 64` — restored `ok` |
| `2026-09-14` | `P0-PROFILE.5` | reachability of all four candidate origins | `200`, `200`, `200`, `301` (a locator that has moved) |
| `2026-09-14` | `P0-PROFILE.5` | identity of the package manager's `sail` | **wrong project** — a WordPress deploy CLI; availability ≠ identity |
| `2026-09-14` | `P0-PROFILE.5` | `fetch_references.sh --verify-only` | 6 of 6 `MATCH`, `rc=0` |
| `2026-09-14` | `P0-PROFILE.5` | Sail driven to the matched profile | `rv64i_zvl32b` from a default of 96 supported extensions |
| `2026-09-14` | `P0-PROFILE.5` | the tracked override is genuinely read | re-enabling `M` → `rv64im_zvl32b`; restored |
| `2026-09-14` | `P0-PROFILE.5` | Spike accepts the matched profile, and rejects a bad one | past config on `--isa=rv64i --priv=m`; `error: bad --isa option` on nonsense |
| `2026-09-14` | `P0-PROFILE.5` | `fetch_references.sh` fired RED on two controls | `DIFFERS` digest; `DIFFERS` ISA string — both restored |
| `2026-09-14` | `P0-PROFILE.5` | `check_profile_consistency.sh --self-test` | `26 pass / 0 fail`; 26 arms written, 26 run |
| `2026-09-14` | `P0-PROFILE.5` | the 13 new rules fired RED on the real dossier | `NO LINEAGE … qemu`; 6 × `UNEARNED OBTAINED … act4` |
| `2026-09-14` | `P0-PROFILE.5` | arm reconciliation across every project harness | `9/9`, `7/7`, `12/12`, `26/26`, `9/9` — none skipping |
| `2026-09-14` | `P0-PROFILE.6` | encodings present in the pinned specification? | `0` seven-bit patterns across all 6 artifacts; 42 figures are images |
| `2026-09-14` | `P0-PROFILE.6` | pinned encoding table vs the profile's hand enumeration | `52` vs `52`, symmetric difference `NONE` |
| `2026-09-14` | `P0-PROFILE.6` | emitted bytes decoded by an independent disassembler | all 15 instructions decode to what was requested (`spike-dasm`) |
| `2026-09-14` | `P0-PROFILE.6` | `smoke-arith` vs 12 specification-derived expectations | 12 of 12 match |
| `2026-09-14` | `P0-PROFILE.6` | `smoke-arith`: sail-riscv vs spike | `AGREE over 12 aligned step(s)` |
| `2026-09-14` | `P0-PROFILE.6` | `smoke-trap`: sail-riscv vs spike, including the trap | `AGREE over 3`; cause `0x04`, `tval 0x80000401` on both |
| `2026-09-14` | `P0-PROFILE.6` | both experiments re-run | byte-identical traces, same sha256 |
| `2026-09-14` | `P0-PROFILE.6` | **control**: un-match the profile, change nothing else | `FIRST DIVERGENCE at aligned step 2` — agreement was doing work |
| `2026-09-14` | `P0-PROFILE.6` | **control**: falsify one expected value | run failed, naming the step and both values |
| `2026-09-14` | `P0-PROFILE.6` | `compare_traces.py --self-test` | `8 pass / 0 fail`; 8 written, 8 run |
| `2026-09-14` | `P0-PROFILE.6` | `check_profile_consistency.sh --self-test` + real-corpus RED | `30 pass / 0 fail`; `NO CONTROL … smoke-trap` |
| `2026-09-14` | `P0-PROFILE.7` | `strings` on both binaries — the blind instrument | `0` and `0`; refuted by `nm`: `649,743` vs `400` symbols |
| `2026-09-14` | `P0-PROFILE.7` | Sail source cloned at the commit its binary reports | `29e6158` matches `--build-info` exactly |
| `2026-09-14` | `P0-PROFILE.7` | SoftFloat census over the two vendored copies | `199` shared, **`184` byte-identical**, `15` differ |
| `2026-09-14` | `P0-PROFILE.7` | encoding ancestry | spike generated from riscv-opcodes `c1d9bdf`; sail hand-writes 59 `encdec` files, `0` refs |
| `2026-09-14` | `P0-PROFILE.7` | does Spike reference Sail anywhere? | `0` files across `.cc`, `.h`, `.mk`, `.ac` |
| `2026-09-14` | `P0-PROFILE.7` | `UNEXAMINED PAIR` fired RED on the real dossier | both experiments refused; restored `ok` |
| `2026-09-14` | `P0-PROFILE.7` | `check_profile_consistency.sh --self-test` | `36 pass / 0 fail`; `36` written, `36` run |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `P0-PROFILE.1` | `SEMULITH-P0-0013 (leaf P0-PROFILE.1): pin RV64I and write the rv64i-lab-v0 dossier` | 20 sourced decisions; 52 mnemonics; 5 open questions |
| `P0-PROFILE.2` | `SEMULITH-P0-0014 (leaf P0-PROFILE.2): the state inventory, and a census for its "none"` | 25 decisions; 7 hidden-state candidates checked |
| `P0-PROFILE.5` | `SEMULITH-P0-0020 (leaf P0-PROFILE.5): obtain three reference models and pin exactly which they are` | 3 obtained, 1 located; 2 limits enumerated; no independence claimed |
| `P0-PROFILE.6` | `SEMULITH-P0-0021 (leaf P0-PROFILE.6): run the matched-profile experiment, and the control that makes it mean something` | 2 models, 15 aligned steps, 12 spec-derived values, 4 differences |
| `P0-PROFILE.7` | `SEMULITH-P0-0023 (leaf P0-PROFILE.7): the independence inventory, and the 184 files that are the same file` | 6 pairs, 4 verdict classes, 2 unexamined; FP correlation routed to P4 |

## Changelog

- `2026-09-13`: Created from `ROADMAP.md` §P0 and task cards `T000`–`T002` by `SEMULITH-TREES.1`.
- `2026-09-13`: `P0-PROFILE.1` completed — the project now has a subject. The specification is
  acquired and pinned rather than cited, and the profile's own claims are gated.
- `2026-09-13`: `P0-PROFILE.2` completed. Reading the sources for the state inventory surfaced
  three architectural rules the profile had missed, which is the argument for doing `.2` by
  reading rather than by recalling `.1`.
- `2026-09-14`: `P0-PROFILE.7` completed. The agreement recorded by `.6` now has a stated
  independence basis: shared for floating point (measured, and routed to `P4-SYSTEM.7`), not
  shared for encoding, no-evidence-of-sharing for integer semantics, and unexamined for both
  QEMU pairs — recorded rather than omitted, because an omitted pair reads like an independent one.
- `2026-09-14`: `P0-PROFILE.6` completed. `G0`'s second criterion is met: an actual evidence path
  works, reproduces, and covers a trap as well as arithmetic. The primary oracle is decided by
  experiment rather than preference. What remains for `G0` is `.3`, `.4`, `.7`, `.8` and `.9`.
- `2026-09-14`: `P0-PROFILE.5` completed. Three reference models are obtained, matched-configured
  and pinned; two profile/reference differences are already enumerated; and the leaf claims
  neither usability nor independence, both of which are owned by later leaves.
