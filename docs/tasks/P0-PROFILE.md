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
  Status: `pending`
  Goal: `requirement.schema.json` records for the declared scope, with `source_semantics` distinguishing defined / implementation-defined / unspecified / reserved, and `research_status` kept separate from `implementation_status`.
  Acceptance: every record validates; every record carries a real `source_refs` locator; no record claims `resolved` research status without one.

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
| 1 | `P0-PROFILE.3` | `pending` | the requirements catalog turns the 25 decisions into checkable obligations, and `.4` needs its obligation IDs to reference |
| 2 | `P0-PROFILE.4` | `pending` | the environment contract — the third of `SCP-01`'s four artifacts, of which only the profile exists |
| 3 | `P0-PROFILE.8` | `pending` | three representative guest programs; needs a readable source for the B and J immediate layouts, which `.6` established this project does not yet have |

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

## Acceptance Checklist (current leaf — `P0-PROFILE.7`)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1: `.6` recorded that two models AGREE over 15 aligned
  steps, and that sentence is worth exactly as much as their independence, which nothing had
  examined. Census before this leaf: `grep -c '\[\[independence\]\]'
  profiles/rv64i-lab-v0/references.toml` → `0`. WHERE the risk actually sits was found by reading
  the two source trees rather than by reasoning about them:

  ```
  $ head -8 target/refs/spike-src/riscv/encoding.h
  /* This file is auto-generated by running 'make' in
   * https://github.com/riscv/riscv-opcodes (c1d9bdf) */
  $ grep -rl 'mapping clause encdec' target/refs/sail-riscv-src/model/ | wc -l
  59
  $ grep -rc 'riscv-opcodes' target/refs/sail-riscv-src/model/ | grep -v ':0' | wc -l
  0
  ```

  ⛔ **An instrument was caught giving a blind answer before it gave a wrong one.**
  `strings … | grep -ci softfloat` returned `0` for *both* binaries, which reads like "neither
  uses SoftFloat". `nm -a` showed why that was blindness rather than absence: spike carries
  `649,743` symbols and `495` softfloat-shaped ones, while the Sail release binary carries `400`
  symbols in total. A stripped binary cannot answer this question, and the `0` was nearly
  recorded as a finding. The source was cloned instead — at the exact commit the binary reports,
  `29e6158`, which its own `--build-info` names.

- [x] **ADDRESSED (verified)** — the inventory exists, and its headline row is a measurement:

  ```
  $ python3 - (census over the two vendored SoftFloat copies)
  SoftFloat .c files present in BOTH vendored copies : 199
    byte-identical once the release-number comment is normalized : 184
    differing : 15
  spike-only .c files : 64 ; sail-only .c files : 127
  $ diff …/berkeley-softfloat-3/source/f64_add.c …/spike-src/softfloat/f64_add.c | wc -l
  4
  ```

  `f64_add.c` differs by **one line** — `Release 3e` versus `Release 3d`. Independence records
  went from `0` to `6`, across four verdict classes: 1 `not-shared` (encoding), 2 `shared`
  (floating point; ACT's derivation), 1 `no-evidence-of-sharing` (integer semantics), 2
  `not-examined` (both QEMU pairs).
  ⭐ The encoding row cuts in a direction that was not anticipated and matters: **our assembler
  shares an encoding ancestor with Spike and not with Sail.** So Sail decoding our bytes as
  intended is a genuinely independent confirmation of the encoding; Spike doing so is not.

- [x] **NO REGRESSION** — leg 2. `PROFILE-CONSISTENCY` gained the rule with real teeth — *an
  experiment may not compare two models whose independence has never been examined* — and it was
  fired RED on the **real** dossier by deleting the three sail/spike rows:
  `UNEXAMINED PAIR rv64i-lab-v0/smoke-arith: the experiment compares 'sail-riscv' with 'spike'
  and no independence record examines that pair … 'not-examined' is a legal verdict, silence is
  not`, and the same for `smoke-trap`. Restored to `ok`.
  `check_profile_consistency.sh --self-test` → `36 pass / 0 fail` (30 → 36); `36` arms written,
  `36` run. Whole gate `=== all doctrines green ===`; `make check` →
  `test result: ok. 1 passed; 0 failed`; `scripts/run_smoke.py` → still `ok`, so the experiment
  this leaf re-qualified has not been disturbed.
  ⚠️ The honest limit of the whole leaf, stated in the data rather than implied: `not-examined` is
  recorded for both QEMU pairs instead of being omitted, because an omitted pair reads exactly
  like an independent one. And `no-evidence-of-sharing` is deliberately weaker than `not-shared`
  — no textual reference in either direction rules out one model importing the other, and says
  nothing about two authors having read the same third source.

- [x] **FIX** — 6 `[[independence]]` records in `references.toml`; 6 new gate rules
  (`BAD PAIR`, `BAD VERDICT`, `UNKNOWN MODEL`, `THIN INDEPENDENCE`, `UNEXAMINED PAIR`, and the
  verdict vocabulary); the durable record
  [`reference_softfloat-shared-ancestry`](../decisions/reference_softfloat-shared-ancestry.md).

- [x] **LOCKSTEP** — leg 3: the inventory is gated, so a future experiment cannot cite two models
  agreeing without the pair having been examined. `DOSSIER.md` and the book's P0 chapter gain the
  independence section; `P4-SYSTEM.7` is annotated with the routed measurement;
  `MEMORY.md`, `LIVE_STATUS.md`, `CHANGELOG.md`, `DEV_NOTES.md` updated in this commit.

## ROUTING EVIDENCE — the floating-point correlation, routed to `P4-SYSTEM.7`

- **What was measured, here:** both reference models vendor Berkeley SoftFloat; 199 `.c` files are
  present in both copies and **184 are byte-identical** once the release-number comment is
  normalized. Sail carries Release 3e (326 files), Spike Release 3d (263 files). The 15 that
  differ are the genuine 3d→3e changes — rounding and bf16 conversion.
- **Does it reproduce outside the family it is sent to?** The *correlation* does: it is a property
  of the two models, not of P4. Its *consequence* does not — it can only bite where floating point
  is in scope. `rv64i-lab-v0` declares `extensions = []`, so **no evidence this project currently
  holds is affected**, and `P0-PROFILE.6`'s experiment compares integer semantics only. That is
  why the finding is routed rather than acted on here.
- **Why `P4-SYSTEM.7` and not another leaf:** it is the only leaf that introduces floating point,
  and its acceptance already demanded an ancestry inventory (`RK07`, `EVD-04`) — this supplies the
  measurement it was written to go looking for.
- **What would make the routing wrong:** if a P0–P3 leaf introduced a floating-point comparison
  after all, the finding would bind earlier than P4. Nothing currently plans one; `P3-BREADTH`'s
  DSP work is the closest candidate and is explicitly synthetic. Re-check when `P3-BREADTH.1`
  selects its cases.
- **What would make the finding itself wrong:** a version bump on either model. The census is a
  statement about two specific vendored copies, and the record says to re-measure rather than
  inherit it.

## Acceptance Checklist (current leaf — `P0-PROFILE.6`)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1: `.5` left three models obtained and **none usable**,
  because `docs/EVIDENCE_AND_GATES.md` §5 makes a reproduced matched experiment the condition and
  no program had ever been run. Census before this leaf: `ls profiles/rv64i-lab-v0/guests
  2>/dev/null | wc -l` → `0`; no trace, no comparator, no expected-value record existed anywhere
  in the tree. WHERE the work had to start was itself a measurement: the pinned specification
  turned out not to contain the instruction encodings at all.

  ```
  $ grep -cE '[01]{7}' intro.html rv32.html rv64.html intro.txt rv32.txt rv64.txt
  0  0  0  0  0  0
  $ grep -c '<img' rv32.html rv64.html
  31  11
  ```

  The format diagrams are **images**. The semantics are all present in prose — which is the half
  that matters for expected values — so encodings were pinned separately from `riscv-opcodes`,
  and that separate provenance is recorded rather than blurred into "the specification says so".

- [x] **ADDRESSED (verified)** — the evidence path now works end to end in one command:

  ```
  $ scripts/run_smoke.py
    PASS  smoke-arith: 12 specification-derived expectations
    PASS  smoke-arith: sail-riscv vs spike  AGREE over 12 aligned step(s)
    PASS  smoke-arith: reproduces  sha256 29d34aaa8218111b…
    PASS  smoke-trap: sail-riscv vs spike  AGREE over 3 aligned step(s)
    PASS  smoke-trap: reproduces  sha256 32f5f132fc965719…
  run_smoke: ok — both experiments agree across two models, match the
  specification-derived expectations, and reproduce

  $ shasum -a 256 target/refs/guests/*.sail.trace
  29d34aaa8218111b2d797d78e1d3d38fd72a9f05846dc9c2b9cb89627a33228d  smoke-arith.sail.trace
  32f5f132fc965719888e5c5fb697a9b6a9a659679f29fb303b276f2a2edb255c  smoke-trap.sail.trace
  $ grep -c '^\[\|^x[0-9]' target/refs/guests/smoke-arith.sail.trace
  23
  ```

  Before → after: guest programs `0` → `2`; models that have executed a matched program `0` → `2`;
  specification-derived expected values checked `0` → `12`, each carrying its own derivation and
  source locator; profile/reference differences enumerated `0` → `4`. The trap case agrees on the
  architectural detail and not merely the outcome: cause `0x04`, `tval 0x0000000080000401`, on
  both models. ⭐ An unplanned corroboration fell out of it: the pinned encoding table contains
  exactly **52** instructions for this profile's extension set, and `.1` enumerated exactly 52 by
  hand from the prose without using it — `symmetric difference: NONE`.

- [x] **NO REGRESSION** — leg 2, and for this leaf falsification is the whole argument.
  ⭐ **The decisive control**: the Sail configuration's misaligned policy was flipped back to
  "handled invisibly", with the same ELF and nothing else changed, and the run failed exactly
  where it should — `FIRST DIVERGENCE at aligned step 2 … sail-riscv writes=[('x1', 0)] …
  spike writes=[]`. One model loaded, the other trapped. **The two models agree because the
  profile is matched**, which turns that sentence from a hope into a measurement. A second
  control falsified one expected value — `step 5 (srai x6, x4, 63): expected {x6: 1}, observed
  {x6: 18446744073709551615}` — proving the expectations are connected to the run.
  `scripts/compare_traces.py --self-test` → `8 pass / 0 fail`: 7 RED arms asserting the reason
  (a differing register, a differing trap *cause*, a differing *tval*, a truncated trace, an
  unknown exception spelling, a trace that never reaches the entry, an exception with no record
  of its instruction) and 1 GREEN. 8 arms written, 8 run.
  `check_profile_consistency.sh --self-test` → `30 pass / 0 fail` (26 → 30), and the new
  `NO CONTROL` rule was fired RED on the real dossier:
  `NO CONTROL rv64i-lab-v0/smoke-trap: … A comparison never seen to diverge is not known to
  detect divergence`. Whole gate `=== all doctrines green ===`; `make check` →
  `test result: ok. 1 passed; 0 failed`; `make book` → `HTML book written`.
  ⛔ **The comparator was caught reporting a false pass, by running it.** Its first version
  compared only the overlapping prefix and printed `AGREE over 2 aligned step(s)` for the
  misaligned-load run — in which Sail trapped and Spike simply stopped emitting records. The
  prefixes did agree; the observation did not. A shorter trace is now a non-agreeing verdict that
  must be explained before the run counts as evidence.

- [x] **FIX** — `scripts/riscv_asm.py` (an RV64I assembler that reads its encodings from the
  pinned tables and carries no opcode of its own; it **refuses** the B and J formats rather than
  typing a bit layout from memory), `scripts/compare_traces.py` (first-divergence comparison with
  a documented, versioned exception adapter grounded in the pinned cause table),
  `scripts/run_smoke.py` (the whole path in one command), two tracked guest sources, the
  specification-derived expectations, and four new gate rules for experiments and differences.

- [x] **LOCKSTEP** — leg 3: the experiment is re-runnable by one tracked command and its records
  are gated, so an experiment row can no longer claim agreement without a control.
  `references.toml` gains 2 experiments and 4 differences; `DOSSIER.md`, the book's P0 chapter,
  `TOOLBOX.md` (2 rows), `MEMORY.md`, `LIVE_STATUS.md`, `CHANGELOG.md`, `DEV_NOTES.md` updated in
  this commit, and the lesson promoted to
  [`a-shorter-trace-is-not-agreement`](../knowledge/a-shorter-trace-is-not-agreement.md).
  ⚠️ Stated rather than implied: this is evidence **for these inputs on these two models**. It is
  not universal trace inclusion, and two models with shared ancestry can agree while both are
  wrong — which is why `.7` is now the frontier rather than a later tidy-up.

## Acceptance Checklist (current leaf — `P0-PROFILE.5`)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1: the project had a subject and no second opinion about
  it. Census before this leaf, over everything that could have constituted a reference route:
  `git ls-files profiles | grep -c reference` → `0`; `ls target/refs 2>/dev/null | wc -l` → `0`;
  and `docs/SOURCES_AND_NAMING.md` listed candidate URLs, which `SRC-03` explicitly refuses to
  treat as established availability. Availability was therefore *established*, not assumed:

  ```
  $ for u in …/riscv/sail-riscv …/riscv-software-src/riscv-isa-sim …/riscv-non-isa/riscv-arch-test
  200  200  301   # the third redirects to riscv/riscv-arch-test — a locator that has moved
  ```

  ⛔ And identity was checked separately from availability, which is the part that paid:
  `brew info --formula sail` → *"CLI toolkit to provision and deploy WordPress applications to
  DigitalOcean"*, `https://sailed.io`, GPL-3.0-only. **An exact name collision with the Sail ISA
  specification language.** The formula existed, the name matched, and it was the wrong software.
  Recording "Sail is available from the package manager" would have been false in precisely the
  way `SRC-03` exists to prevent.

- [x] **ADDRESSED (verified)** — before → after, measured by the tool that now owns the claim:
  `scripts/fetch_references.sh --verify-only` → **six re-derivations, all `MATCH`**, `rc=0` —
  the Sail release asset, the Sail binary, the Spike source commit, the Spike binary, the
  read-only QEMU binary, and *the matched-profile ISA string the model reports about itself*:

  ```
  MATCH    sail-riscv asset  target/refs/sail-riscv-Mac-arm64.tar.gz
  MATCH    spike source commit  1e05ddac3a6c351bfc0aeed0cf3a68940e7200ab
  MATCH    qemu binary (host toolchain, read-only)  /opt/homebrew/bin/qemu-system-riscv64
  MATCH    matched-profile ISA string  rv64i_zvl32b
  fetch_references: ok (rv64i-lab-v0)
  ```

  Reference models obtained and runnable went from `0` to `3`; recorded candidates from `0` to
  `4`; recorded failed attempts from `0` to `3`. The Sail model was driven from its default
  `rv64imafdcbvh_…` (96 supported extensions, `grep -c '"supported": true'` → `106` entries in
  the dump) down to **`rv64i_zvl32b`**, and Spike accepts `--isa=rv64i --priv=m`.

- [x] **NO REGRESSION** — leg 2. Every instrument added here was fired RED before being trusted,
  on the **real** corpus and not only on fixtures.
  `scripts/fetch_references.sh`: corrupting a pinned digest gave
  `DIFFERS spike binary … pinned 000000000080ccafb96ab076c91967adf6df119b05c5b926ed49a033efe57836a3
  actual 8fdf43ac80…`; flipping `M` back on in the tracked override gave
  `DIFFERS matched-profile ISA string … pinned rv64i_zvl32b actual rv64im_zvl32b`. Both restored
  to `MATCH`.
  `PROFILE-CONSISTENCY` gained 13 rules for `references.toml` and was fired RED **on the real
  dossier** twice: deleting QEMU's `lineage` gave `NO LINEAGE rv64i-lab-v0/qemu: EVD-04 asks
  whether two comparators share semantic ancestry…`, and claiming ACT was `obtained` gave six
  `UNEARNED OBTAINED rv64i-lab-v0/act4: status is 'obtained' with no 'binary'…` findings.
  `--self-test` → `PROFILE-CONSISTENCY --self-test: 26 pass / 0 fail` (13 pre-existing + 13 new).
  Arm accounting per this session's own lesson: `grep -cE '(^|[; ])arm "'` → `26`, reported `26`.
  The same reconciliation was run over **every** project harness —
  `delivery-provenance 9/9, fixture-fingerprint 7/7, readme-routes 12/12, profile-consistency
  26/26`, and `seam-integrity 9/9` on its own `score` idiom — so no harness in this repository is
  silently skipping arms. Whole gate `=== all doctrines green ===`, `rc=0`; `make check` →
  `test result: ok. 1 passed; 0 failed`; `make book` → `HTML book written`.
  ⭐ The falsifying question was *"does having three binaries mean anything?"* — and the honest
  answer is **no**, which is why the gate now refuses a candidate with no `lineage`. ACT derives
  its expected results from a *configured Sail model*, so ACT agreeing with Sail is one semantics
  answering twice. Spike and QEMU are *plausibly* independent; plausible is a hypothesis.
  `P0-PROFILE.7` owns it and this leaf claims nothing.

- [x] **FIX** — `profiles/rv64i-lab-v0/references.toml` (the dossier: 4 candidates, 3 attempts),
  `profiles/rv64i-lab-v0/reference/sail-rv64i-lab-v0.override.json` (the tracked matched-profile
  configuration), `scripts/fetch_references.sh` (acquire and re-verify, repo-local),
  `check_profile_consistency.sh` extended to gate the dossier's shape, and a decision record
  superseding the roadmap's cost estimate.

- [x] **LOCKSTEP** — leg 3: every recorded digest, the Spike commit and the model's own ISA
  string are re-derivable by one tracked command, and the dossier's shape is re-checked on every
  commit. `DOSSIER.md` gains the references section and `OQ-4` is partly answered;
  `docs/decisions/decision_reference-acquisition-route.md` records what this supersedes;
  `TOOLBOX.md` gains the tool; the book's P0 chapter gains *"What acquisition actually found"*;
  `MEMORY.md`, `LIVE_STATUS.md`, `CHANGELOG.md`, `DEV_NOTES.md` updated in this commit.
  ⛔ **Two limits are recorded rather than rounded away**, because `G0` asks for differences to be
  *enumerated, not assumed absent*. (1) Sail cannot be configured to exactly `extensions = []`;
  it bottoms out at `rv64i_zvl32b`, a vestigial minimum vector-length class the model instantiates
  even with the vector unit `Disabled`. (2) Sail **will not emit its effective configuration** —
  `--print-default-config` ignores `--config-override` and the two dumps are byte-identical — so
  the effective configuration is *(default) + (our tracked override)* and **that merge is ours,
  not the model's account of itself**. `P0-PROFILE.6` must not upgrade it into the model's word.

## Acceptance Checklist (current leaf — `P0-PROFILE.2`)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1: leaf `.1` recorded the profile's *decisions* but not
  its *state*, and `SEM-08` requires the required state to include hidden or pending information
  that can influence a future supported observation. Census before this leaf:
  `git ls-files profiles | grep -c state.json` → `0`. Reading the pinned sources for it also
  surfaced three architectural rules the profile had not recorded, each found by reading rather
  than assumed: the address space is **circular** with computations wrapping modulo 2^XLEN;
  every executed instruction entails an **implicit** fetch read; and the fetch-accessible and
  load-accessible location sets **may differ**, with the choice delegated to the EEI
  (`RVI-INTRO`, *Memory*).
- [x] **ADDRESSED (verified)** — `state.json` records 32×64-bit integer registers, `x0`
  hardwired zero, and `pc`, and enumerates **7 hidden-state candidates**, all absent:
  `hidden state: 0 entries; candidates checked: 7`, `all candidates absent: True`. The profile
  gained five decisions (`D-ADDR-WRAP`, `D-FETCH-IMPLICIT`, `D-FETCH-MAP`, `D-CODE-VISIBILITY`,
  `D-MAIN-VS-IO`), taking it to 25. The reset claim was **measured**, not assumed:
  `grep -ci reset rv32.txt rv64.txt` → `rv32.txt:0`, `rv64.txt:0`, so reset values for
  `x1..x31` are a laboratory declaration and are labelled one.
- [x] **NO REGRESSION** — leg 2: the gate was extended and then fired, on the real dossier, for
  both new rules. Removing the census gave `UNEARNED NONE rv64i-lab-v0/state.json: hidden_state
  is empty with no census…`, `rc=1`; setting `xlen` to 32 gave `XLEN MISMATCH rv64i-lab-v0:
  state.json 32 != profile.toml 64`; both restored to `ok`.
  `PROFILE-CONSISTENCY --self-test: 13 pass / 0 fail` (11 RED arms). Whole gate:
  `scripts/check_doctrines.sh` → `=== all doctrines green ===`, `rc=0`; `make check` →
  `test result: ok. 1 passed; 0 failed`, `rc=0`.
  ⛔ This leaf's own evidence was refused by `TASK-ACCEPTANCE` for the **third** time in this
  repository — on `grep -ci reset`, a plain enumeration over the pinned specification, which
  `GAP-CLAIM-CENSUS` accepts as a census while the acceptance gate's signatures did not. The
  first two fixes were additions and each held only until the next new thing existed; this one
  aligns the two lists on *any* `grep` invocation, because an instrument one gate accepts as a
  census is an instrument the other should accept as evidence. Fired RED afterwards (a
  prose-only box → `rc=1`) to prove the widening did not make the gate vacuous. Recorded in
  [`census-instrument-signature-gap`](../knowledge/census-instrument-signature-gap.md).
  ⭐ The falsifying question for this leaf was *"is 'no hidden state' a finding or an
  omission?"* — and the honest answer is that it is only true **because of what the profile
  excludes**, which is why the census records the reason per candidate and why
  `D-CODE-VISIBILITY` notes that a caching implementation would have hidden state and would
  still be legal.
- [x] **FIX** — `profiles/rv64i-lab-v0/state.json` added; five decisions added to
  `profile.toml`; `check_profile_consistency.sh` extended to require `state.json` to agree with
  `profile.toml` on id, XLEN and register count, to accept `software-convention` as an authority
  only inside `state.json`, and to refuse an empty `hidden_state` with no census.
- [x] **LOCKSTEP** — leg 3: the agreement between the two files is re-derived every commit, so a
  contradiction fails rather than rots. `DOSSIER.md` gains the state section and the two new
  semantic traps; `MEMORY.md`, `LIVE_STATUS.md` and `CHANGELOG.md` updated in this commit.

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
