# P0-PROFILE: select the first experiment and prove an evidence path exists

## Metadata

- Tree ID: `P0-PROFILE`
- Status: `active`
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
  Status: `pending`
  Goal: the versioned assumption/guarantee set from `docs/CPU_ENVIRONMENT.md` §2–§3 — address units, access widths, virtual-time domain, permitted event-delivery points, ordering constraints — each with its authority (`architecture` / `implementation-profile` / `platform` / `laboratory`).
  Acceptance: laboratory policy nowhere overrides an architectural requirement; positive **and negative** fixtures defined for each obligation.

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
  Status: `pending`
  Goal: small freestanding programs that exercise arithmetic, control flow, and a memory/fault boundary, with independently derived expected observations.
  Acceptance: expected values are derived from the specification, not from any model's output.

- ID: `P0-PROFILE.9` — **evidence-obligation policy and the `G0` report**
  Status: `pending`
  Goal: declare, *before* implementation, what kind of evidence each obligation class requires (`EVD-03`); then generate the gate report from pinned inputs.
  Acceptance: the report names inputs, commands, actual results and limitations (`EVD-08`), and reads `passed` or `incomplete` — never `passed` with a missing required check.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `P0-PROFILE.4` | `pending` | the environment contract; `.3` has now minted the 25 `OB-*` obligation ids it must define, and `RECORD-SCHEMA` carries a named gap until it does |
| 2 | `P0-PROFILE.8` | `pending` | three representative guest programs; needs a readable source for the B and J immediate layouts, which `.6` established this project does not yet have |
| 3 | `P0-PROFILE.9` | `pending` | the evidence-obligation policy and the `G0` report — last, because it declares what evidence each obligation class requires and must not be written after seeing what is easy to produce |

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

## Acceptance Checklist (current leaf — `P0-PROFILE.3`)

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
