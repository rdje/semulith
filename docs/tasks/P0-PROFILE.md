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
  Status: `pending`
  Goal: registers, widths, aliases, overlaps, reset values, and any hidden or pending state that can influence a future supported observation (`SEM-08`, catalog `C02`).
  Acceptance: each entry source-linked; alias interactions stated, not implied.

- ID: `P0-PROFILE.3` — **requirements catalog seed**
  Status: `pending`
  Goal: `requirement.schema.json` records for the declared scope, with `source_semantics` distinguishing defined / implementation-defined / unspecified / reserved, and `research_status` kept separate from `implementation_status`.
  Acceptance: every record validates; every record carries a real `source_refs` locator; no record claims `resolved` research status without one.

- ID: `P0-PROFILE.4` — **environment contract v0** *(task card `T002`)*
  Status: `pending`
  Goal: the versioned assumption/guarantee set from `docs/CPU_ENVIRONMENT.md` §2–§3 — address units, access widths, virtual-time domain, permitted event-delivery points, ordering constraints — each with its authority (`architecture` / `implementation-profile` / `platform` / `laboratory`).
  Acceptance: laboratory policy nowhere overrides an architectural requirement; positive **and negative** fixtures defined for each obligation.

- ID: `P0-PROFILE.5` — **reference candidate dossier** *(task card `T001`, part 1)*
  Status: `pending`
  Goal: for each candidate (Sail RISC-V, Spike, ACT4) record exact source/build availability, supported features, invocation, trace granularity, injection capability, effective configuration, artifact hashes, adapter version, and restrictions on use or shipping (`docs/EVIDENCE_AND_GATES.md` §5, `SRC-01`).
  Acceptance: every field is an observed fact; a candidate that could not be obtained is recorded as such, with the attempt.

- ID: `P0-PROFILE.6` — **matched-profile smoke test** *(task card `T001`, part 2)*
  Status: `pending`
  Goal: run at least one real experiment against the selected reference with a matched configuration — independently encoded arithmetic **and** an access/trap case — and reproduce it.
  Acceptance: actual traces, hashes and configs recorded; mismatches and missing injection capabilities documented. **A reference is not usable until this leaf passes.**

- ID: `P0-PROFILE.7` — **independence inventory**
  Status: `pending`
  Goal: per subsystem, whether two comparators share semantic code or expected-result derivation (`EVD-04`). ACT4 computes expected results with a configured Sail model; TestFloat ordinarily derives from SoftFloat.
  Acceptance: known common ancestry **and** unknown ancestry both recorded; neither independence nor correlation assumed.

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
| 1 | `P0-PROFILE.2` | `pending` | the state inventory is the next thing every later leaf indexes into |
| 2 | `P0-PROFILE.5` | `pending` | `T001` may feed corrections back into `.1`, so the reference dossier should not wait long |

## Decisions

- `2026-09-13`: first CPU is a small **RV64I** profile in a specified laboratory execution
  environment (`ROADMAP.md` §1). Revisit only if archogen's named first target makes another
  width or feature set more useful, which is a P0 input.

## Open Questions

- Which reference becomes the primary oracle? Resolved by `.5`/`.6`, not by preference.
- Does archogen's `rt-static-up-v1` profile need machine-mode features this profile excludes?
  `docs/ARCHOGEN_INTEGRATION.md` §6 says a provisional machine-mode profile may be smaller than
  the Linux profile — compare during `.1` when archogen's target decision is available.

## Blockers

- None.

## Acceptance Checklist (current leaf — `P0-PROFILE.1`)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1: the project had no profile, so nothing it might
  build had a defined subject. Census before this leaf: `git ls-files profiles | wc -l` → `0`,
  and no specification artifact had been acquired — `docs/SOURCES_AND_NAMING.md` listed
  candidate URLs, which rule `SRC-03` explicitly refuses to treat as established availability.
  Reachability was therefore established first, not assumed:
  `curl -sS -o /dev/null -w '%{http_code}' …/unpriv/rv64.html` → `200`.
- [x] **ADDRESSED (verified)** — three specification artifacts acquired, fingerprinted and
  pinned: `intro.html` `3d65f713…13bf0c` (69,772 B), `rv32.html` `3b20e92f…3ad75ec`
  (107,630 B), `rv64.html` `6eadb316…f13abd` (49,246 B), each `HTTP 200`, all three re-derived
  by `scripts/fetch_sources.sh --verify-only` → `MATCH`, `MATCH`, `MATCH`, `rc=0`. The profile
  records **20 decisions** — 12 `architecture`, 6 `execution-environment`, 2 `laboratory` —
  each with a statement and a source locator, and an instruction scope enumerated rather than
  counted from memory: `enumerated mnemonics: 52; declared count_total: 52; agree: True`
  (40 base + 12 RV64I additions, verified against `RVI-RV64I` §3.1.2–§3.1.3).
- [x] **NO REGRESSION** — leg 2: both new instruments were fired RED, with the reason asserted.
  `PROFILE-CONSISTENCY --self-test: 8 pass / 0 fail` (7 RED arms: count drift, parts that do
  not sum, unknown authority, an uncited decision, a duplicate id, a profile with no decisions,
  an unparseable file), and fired against the **real** dossier — deleting one mnemonic gave
  `COUNT DRIFT rv64i-lab-v0: [scope] enumerates 51 mnemonic(s), count_total = 52`, `rc=1`,
  restored `ok`. `fetch_sources.sh` fired against a corrupted pin gave
  `DIFFERS rv64.html pinned 0000…` with the re-read instruction, `rc=1`, restored `rc=0`.
  ⛔ That second control also exposed a defect in the tool itself: an unanchored `sed` capture
  left the ledger line's trailing comment in `work_dir`, so the fetch created a directory
  literally named `target/sources/riscv-v20260120   # repo-volume, untracked` **while still
  reporting three green MATCHes** — a verdict correct about the bytes and wrong about where it
  read them. Found by listing the directory rather than trusting the green. Whole gate:
  `scripts/check_doctrines.sh` → `=== all doctrines green ===`, `rc=0`; `make check` →
  `test result: ok. 1 passed; 0 failed`, `rc=0`.
- [x] **FIX** — `profiles/rv64i-lab-v0/` created with `profile.toml` (machine-readable, gated),
  `sources.toml` (pinned artifacts with an explicit statement of what a digest does and does
  not pin) and `DOSSIER.md` (the narrative, the five open questions with owners and due points,
  and what is deliberately absent). `scripts/check_profile_consistency.sh` and
  `scripts/fetch_sources.sh` added; the first registered as a project doctrine, the second
  deliberately **not** a gate because it needs the network.
- [x] **LOCKSTEP** — leg 3: the dossier's internal claims are re-derived on every commit and
  its sources are re-derivable on demand. `profiles/` registered in `doctrine/readme_routes.tsv`
  with its own bounds; `README.md` layout row; `DOCTRINE_ENFORCEMENT.md` mirror; `TOOLBOX.md`
  gains both tools; `MEMORY.md`, `LIVE_STATUS.md`, `CHANGELOG.md` updated in this commit.
  ⭐ The README's own health target had been set **at** today's size and fired on the very row
  this leaf added — the exact miscalibration `SEMULITH-TREES.4` documented, committed in the
  file that documents it. Re-set to `78 / 4352`, between the reviewed page and its untouched
  ceiling.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-13` | `P0-PROFILE.1` | specification reachability, then acquisition | `HTTP 200`; three artifacts pinned and re-derived `MATCH` |
| `2026-09-13` | `P0-PROFILE.1` | profile enumeration vs declared count | `52` vs `52`, `agree: True` |
| `2026-09-13` | `P0-PROFILE.1` | `check_profile_consistency.sh --self-test` | `8 pass / 0 fail` (7 RED arms) |
| `2026-09-13` | `P0-PROFILE.1` | both instruments fired RED on the real corpus | `COUNT DRIFT … 51 vs 52`; `DIFFERS rv64.html` — each restored to `ok` |
| `2026-09-13` | `P0-PROFILE.1` | `scripts/check_doctrines.sh` + `make check` | `all doctrines green`, `rc=0`; `test result: ok. 1 passed` |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `P0-PROFILE.1` | `SEMULITH-P0-0013 (leaf P0-PROFILE.1): pin RV64I and write the rv64i-lab-v0 dossier` | 20 sourced decisions; 52 mnemonics; 5 open questions |

## Changelog

- `2026-09-13`: Created from `ROADMAP.md` §P0 and task cards `T000`–`T002` by `SEMULITH-TREES.1`.
- `2026-09-13`: `P0-PROFILE.1` completed — the project now has a subject. The specification is
  acquired and pinned rather than cited, and the profile's own claims are gated.
