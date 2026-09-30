# The evidence, the gate, and the traceability walk

The previous chapters said what the model is built *from* and *how*. This one is the
ledger of what has actually been **demonstrated** — per axis, never rolled up into a
banner — what the gates say about it, and a walk a reviewer can repeat to check that the
traceability chain is real. The discipline is the one the release acceptance will enforce
(SCP-05): fidelity is reported **separately per axis**, and the phrase "supports RV64I"
appears nowhere — here or anywhere in the project — because a banner is not a claim with a
denominator.

## What has been demonstrated, per axis

Each line below names its instrument; every number is the current measured one,
re-derivable by the command named beside it.

- **Instruction semantics.** All **52/52** declared RV64I forms are exercised by tracked
  guests, the coverage reported with its denominator and gated (`EXERCISE-COVERAGE`;
  `bash scripts/check_exercise_coverage.sh` prints `52/52`). Every expected value was
  derived from the pinned specification prose before any model ran (EVD-05); the commit
  gate re-runs the whole differential offline on every commit (166 verify suites).
- **Boundaries.** The 6-bit and 5-bit shift-amount domains are *exhausted* (64- and
  32-point sweeps), the signed-extreme wraps are pinned on the register and immediate
  paths, the sign/zero-extension edges are pinned per width, and the little-endian lanes,
  overlap composition and register aliasing are proven (P2-SCALAR.2's five guests).
- **Faults, suppression, reserved cases.** The failure layer is pinned three-way
  (P2-SCALAR.3's eighteen guests): fetch and access faults with their exact cause/tval,
  the suppressed link write on a misaligned jump, the suppressed misaligned store, the
  reserved-decode policy conversion, the HINT table, self-modifying code visibility — and
  the two defects found are in the record with their directions (one was the dossier's,
  one was the model's).
- **Interactions.** The fault × alias × boundary × event × progress × restart matrix is
  declared as tracked data and every one of the **21 cells** resolves to guests, a
  mechanism, or a degenerate-with-reason — the `INTERACTION-MATRIX` gate re-derives the
  cells and refuses an omitted one by name (`bash scripts/check_interaction_matrix.sh`
  prints all 21 with their dispositions).
- **The live differential.** **48 guests** agree with sail-riscv 0.14 AND spike 1.1.1-dev
  on **642/642 aligned steps**, byte-identically reproducible — plus the one *declared*
  expected divergence (`it-fencei`: the references execute `fence.i`, this profile
  declares it reserved; the divergence lands at exactly the declared step, measured, and
  the references stay each other's control). Re-run: `python3
  scripts/run_semulith_smoke.py`. The 49th guest is different in kind: `c-scope.c` is
  **compiled from C** by the pinned toolchain — the previous chapter tells that story and
  why it changes the shape of the evidence.
- **External tests (the ACT4 suite).** The pinned riscv-arch-test RV64I campaign — **51
  generated test files, 17,017 signature slots** — runs three-way: every test's HTIF
  verdict is pass on all three models, semulith's signature agrees with the Sail-derived
  one slot-for-slot, and spike-vs-sail agrees as the control pair. The dossier is
  `profiles/rv64i-lab-v0/act4.sexp` (gated by RECORD-SCHEMA's census rule — every carried
  count re-derives from its rows); re-run: `scripts/fetch_act4.sh && python3
  scripts/run_act4_campaign.py --record`. ⛔ This is *external tests with Sail-derived
  expectations*: ACT computes its expected results with a configured Sail model, so
  agreement here is one semantics answering twice (EVD-04) — valuable because somebody
  else chose the tests, never as a second opinion.
- **Restart.** Restartability is determinism of re-execution, measured three ways: the
  smoke's reproduce leg (every guest re-run byte-identically), the offline determinism
  suite (every guest twice from `zeroed_at(entry)`, identical traces and crossing logs),
  and **mid-execution snapshots** (`P2-SCALAR.7`): every guest's run is split at three
  points — the state recorded as a digested, definition-pinned snapshot record, resumed
  through the JSON round-trip, and the continuation proven identical *including the
  crossing logs* — with RED arms proving corrupted, foreign-definition and incoherent
  records are refused by name. The completeness claim is the pinned hidden-state census:
  registers + pc + memory is ALL the pending state this profile has; nothing else is
  offered. Try it: `semulith snapshot <elf> --at N > snap.json && semulith resume snap.json`.
- **Portability.** The workspace compiles for `wasm32-unknown-unknown` on every commit
  (`PORT-WEB`), and the browser bench runs the same engine headlessly (53 arms: 49 clean
  guests, 3 trace-level mutants, the census arm). The native matrix (`P2-SCALAR.8`,
  recorded in `profiles/rv64i-lab-v0/portability.sexp`): aarch64 green (the commit
  gate's own run + the digest manifest any second host must reproduce byte-identically),
  Miri green 65/65 interpreted, big-endian powerpc64 green 65/65 under Miri — and the
  mandatory x86-64 leg measured **unavailable** on the recording host (no Rosetta), so
  the profile honestly stays experimental: the verdict is `incomplete`, not waived
  (`bash scripts/check_portability.sh` re-derives it).
- **Performance.** A baseline is recorded as data on one named host
  (`profiles/rv64i-lab-v0/baseline.sexp`), with its noise — and **no thresholds** (RUST-04:
  the noise table exists so a future threshold can be set from it; none is set). One host's
  measurement, not a portable constant.
- **Detection.** The differential is proven to *catch*: the validator mutation suite runs
  known-wrong models (wrong sign extension, a suppressed link write, a fabricated trap, an
  overbroad decode mask, an extra memory access, deferred event delivery, a stale
  reference configuration) and each is caught at its designated step, naming the
  designated field (EVD-09; `cargo test -p semulith-verify`).

The honest label for all of it, stated once and meant: **finite, tested evidence — never
universal proof** (EVD-01). Forty-nine laboratory programs, two references, one host — plus
the 51-file external campaign, whose expectations share Sail's semantics by construction.

## The gate verdicts: G1 `passed`, G0 honestly `incomplete`

Both reports regenerate from tracked inputs (`scripts/gate_report.py`), so a verdict cannot
be flattered by an editor.

- **`G0`** (profile and evidence access): all three criteria met — but the profile's
  contract declares **72 required checks and 0 are implemented**, and EVD-08 forbids a
  report that reads `passed` while a required check is missing. The generator has no code
  path to `passed` here, which is the point: a gate that *cannot* say passed over a
  missing criterion is the only kind worth having.
- **`G1`** (the processor laboratory): **all six criteria met — verdict `passed` since
  `2026-09-30`.** Criterion 6 — the compiled freestanding guest, "C as the first guest
  path" — stood unmet until `P2-SCALAR.5` (unblocked by the director's delegation,
  `decision_c-guest-routing-and-toolchain`): `guests/c-scope.c` is compiled by the pinned
  toolchain (`scripts/build_c_guest.sh` — clang 21.1.8 with the RISC-V backend plus
  `ld.lld` 21.1.8, both measured present on the host, nothing installed) and retires
  under first-divergence comparison against BOTH references, 129/129 aligned steps
  (`scripts/run_semulith_smoke.py`). The guest is self-checking: its expected values are
  C-semantics constants written into the source, so any runner's mis-execution routes to
  a fail code and the three-way comparison diverges at exactly that check. The same
  instrument that said `incomplete` while the C path was missing now says `passed` — and
  `G0` still says `incomplete`, because that is what the inputs say.

⭐ The teaching point: `incomplete` is not a failure of the work — it is the *instrument*
working. The alternative on offer at every step was a narrower claim quietly widened.

## What this laboratory is — and is not

`rv64i-lab-v0` is a **laboratory environment**: one hart, M-mode only, the base integer ISA
and nothing else — no C, M, A, F, D, Zicsr or Zifencei extension (so: no compressed
instructions, no hardware multiply — a real program's `mul` would be a runtime call; no
atomics; no floating point — a soft-float ABI would be required), no devices, no board, no
boot media, no OS workload. The profile is a **development** profile; acceptance attaches
evidence to an exact versioned profile, and none has been accepted. What the evidence
above *does* mean: for the 52 declared forms, in this laboratory, the model's observable
behavior matches the specification-derived expectations and two pinned references on the
measured corpus, and the instrument that would catch a regression is itself proven to
catch. What it does *not* mean: anything about privilege transitions, real compiled C
programs, multicore ordering (RVWMO is out of scope until MC-MULTICORE), or any extension.

## The traceability walk: one rule, from the dossier to a command you can run

The methodology chapter walked a rule through the *specification* side (sentence →
decision → requirement → obligation). This walk is the **evidence** side, and it ends at
something re-runnable. The rule: **misaligned data accesses** — `D-MISALIGN-DATA`.

**The rule.** The base ISA lets the EEI choose whether misaligned accesses are handled
invisibly; this profile's EEI does not guarantee invisible handling, so the choice must be
defined — and the profile defines it: a misaligned access *raises* an address-misaligned
exception, delivered as a contained trap (`D-MISALIGN-DATA`, `profile.sexp`, authority
`execution-environment` — the specification delegates, the environment states its choice).

**The requirement.** `REQ-D-MISALIGN-DATA` (`requirements.sexp`): class
`implementation-defined`, status `resolved`, statement *verbatim* identical to the
decision's — the RECORD-SCHEMA gate refuses the commit the day the two drift.

**The obligation.** `OB-MISALIGN-DATA` (`contract-obligations.sexp`): direction
`cpu-guarantee`, authority `implementation-profile` — legal *because* the class is
implementation-defined (contrast `OB-MISALIGN-REPORT`: class `defined`, so its authority
must be `architecture`; the AUTHORITY check makes the rule mechanical). Declared checks:
`CHK-MISALIGN-DATA-POS` — a misaligned access raises — **and** `CHK-MISALIGN-DATA-NEG` —
the negative half, an aligned access that must *not*. (Both are declared; per the G0
verdict above, the named-check layer is the release skeleton — what *tests* the rule today
is next.)

**The experiment that touches it.** `smoke-trap` — the second recorded experiment in
`references.sexp`: a misaligned `lw`, AGREE over 3 aligned steps, and the agreement is on
the *architectural detail*, not merely the outcome: cause `0x04`, tval
`0x0000000080000401`, on **both** models. And its control is the one the references
chapter teaches: flip Sail's misaligned policy back to "handled invisibly", same ELF, and
the comparison diverges at exactly step 2 — the agreement is *because the profile is
matched*. The rule is carried further by the fault guests (`fault-ld-mis-h`,
`fault-ld-mis-d` — the width rule) and into the interaction matrix (`it-prio-load` —
misaligned AND unmapped, the misaligned cause wins; `it-fault-alias` — a misaligned load
over its own base register).

**The re-runnable end.** Offline — no reference binaries needed, this runs on every
commit:

```
$ cargo test -p semulith-verify --lib run::tests::smoke_trap
test run::tests::smoke_trap_reports_the_misaligned_load_and_stops ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 165 filtered out
```

Live — the three-way differential against both pinned references (needs the fetched
references under `target/refs/`):

```
$ python3 scripts/run_semulith_smoke.py
…
  PASS  smoke-trap: semulith vs 3 specification-derived expectations
  PASS  smoke-trap: semulith — 1 register(s) that must never be written
  PASS  smoke-trap: semulith vs sail-riscv  AGREE over 3 aligned step(s) (semulith: 3 parsed, …)
  PASS  smoke-trap: semulith vs spike  AGREE over 3 aligned step(s) (semulith: 3 parsed, …)
  PASS  smoke-trap: semulith reproduces  sha256 c9d7a11ce4b7bffe…
…
run_semulith_smoke: ok — semulith matches the specification-derived expectations and
reproduces; every cross-model comparison that is enabled agrees
```

That is the whole walk, and it is the whole claim: a sentence in a pinned document, a
decision with an authority, a requirement with a class, an obligation with two checks, an
experiment with a control, and a command whose output you can watch. Any rule in the
dossier walks the same route — the gates exist so that the day a hop breaks, the commit
breaks instead of the claim.
