# Withdrawn reference rationales — P4-SYSTEM.14 a6

These are historical bytes captured from `6d6d9ca377c51839108a17d4e24cecfbea90be56` by
SEMULITH-P4-0197. The internal-source census, negative-search independence
inference and clone/read-internals advice in these payloads are withdrawn as
current evidence. Maintained records at their original paths carry the corrected
public-contract scope. No reference implementation was inspected for this repair.
Original dated measurements are retained as reported history, with their limits.

The complete source task was 57117 bytes, SHA256
`dd1b5200b600db531cea9ef57db284407e9df9c353277aaa496dc3047152ba73`; only its .7 card is captured here.

## Capture map

| Tag | Original source | Bytes | SHA256 |
| --- | --- | --- | --- |
| ancestry | `docs/decisions/reference_softfloat-shared-ancestry.md` | 4328 | `9decebbb529af143d77737d19d8a60875ecff770e888539925670d78cdad2799` |
| fp-acceptance | `docs/decisions/reference_fp-model-layer-acceptance.md` | 2894 | `3cda11eda02ee5913dee82669faa54c0cafc9a24402e0cc67432df3b6b618132` |
| zero-hits | `docs/knowledge/zero-hits-absence-or-blindness.md` | 4432 | `b5b154bc296826eb23bee0b4d5e8fcfa3bd4683b88509c23815941bf64f7a745` |
| p4-7 | `docs/tasks/P4-SYSTEM.md (.7 card)` | 2629 | `52d0aa6eb51c367f34763fee5523a7b2278985e9f57e63f435f385a53eb263c4` |
| p4-1-note | `docs/tasks/P4-SYSTEM.md (.1 note)` | 85 | `69fed504dc238be99f7eeb8e8574cfd5cbeaf5efa9e663d342c1ebf9a0319e69` |

## ancestry — withdrawn historical payload

<!-- BEGIN:ancestry -->
# Sail and Spike run the same floating-point source — 184 of 199 shared files are byte-identical

- **Type:** `reference`
- **Date:** `2026-09-14`
- **Status:** `active`
- **Owner / source:** measured by `P0-PROFILE.7` (the independence inventory, `EVD-04`); consumed
  by [`P4-SYSTEM.7`](../tasks/P4-SYSTEM.md), the floating-point backend qualification

## The fact

The two reference models this project uses as comparators **both vendor Berkeley SoftFloat**, and
for the large majority of the overlap they do not merely share an ancestor — they contain the
same source file.

| | sail-riscv 0.14 | spike 1.1.1-dev |
| --- | --- | --- |
| Location | `dependencies/softfloat/berkeley-softfloat-3/` | `softfloat/` |
| Release | 3e (2018-01-20) | 3d |
| Source `.c` files | 326 | 263 |
| Symbols in the built binary | *(release binary carries 400 symbols total — not measurable)* | 495 softfloat-shaped |

Census over the intersection, normalizing only the release-number comment line:

```
SoftFloat .c files present in BOTH vendored copies : 199
  byte-identical once the release-number comment is normalized : 184
  differing : 15        (rounding and bf16 conversion — the genuine 3d→3e changes)
spike-only .c files : 64
sail-only  .c files : 127
```

`f64_add.c` differs between the two copies by **one line**: `Release 3e` versus `Release 3d`.

## Why it matters

`EVD-04` exists for exactly this. A differential floating-point test between Sail and Spike would,
for those 184 files, execute **one implementation twice** and report agreement. The agreement
would be real, reproducible, and worth nothing as independent evidence: a defect in the common
source is present in both, and no amount of running them against each other can surface it.

This is the same shape as the fact the roadmap already recorded about TestFloat — that it
ordinarily derives its expected values from SoftFloat — arriving one level deeper and measured
rather than anticipated.

## What is NOT claimed

- **Not that SoftFloat is wrong.** It is the reference implementation of IEEE-754 for this
  ecosystem and there is no suggestion of a defect. The finding is about *evidential
  independence*, not quality.
- **Not that the two models are correlated everywhere.** They are not: instruction encoding is
  measurably **not** shared — Spike generates `encoding.h` from `riscv-opcodes` (`c1d9bdf`) while
  the Sail model hand-writes 59 files of `encdec` mappings and never mentions `riscv-opcodes`
  under `model/`. Independence is a property of a *pair and a subsystem*, never of a tool.
- **Nothing about integer semantics.** That pair is recorded as `no-evidence-of-sharing`, which is
  deliberately weaker than `not-shared`: no textual reference exists in either direction, and that
  rules out one importing the other while saying nothing about two authors reading the same third
  source — which for an ISA model is the normal case.

## Effect on work already done

**None.** `rv64i-lab-v0` declares `extensions = []`; there is no floating point in this profile,
so no evidence this project currently holds depends on the correlated subsystem. The
`P0-PROFILE.6` smoke test compares integer semantics only.

## How to apply

- **`P4-SYSTEM.7` must not count Sail-versus-Spike as independent numeric confirmation.** Its
  acceptance already requires an ancestry inventory; this record supplies the measurement so the
  leaf starts from a fact rather than a suspicion.
- An independent numeric check needs a derivation that does **not** descend from SoftFloat — a
  hardware observation, an independently implemented arithmetic, or a specification-derived
  expected value computed by hand. Two SoftFloat descendants agreeing is one opinion.
- When adding any comparator, record the pair and subsystem in the profile's `references.toml`
  **before** citing their agreement. `PROFILE-CONSISTENCY` refuses an experiment that compares two
  models with no independence record for that pair — `not-examined` is a legal verdict, silence
  is not.
- ⛔ Re-measure rather than inherit this row when either model is upgraded. It is a statement about
  two specific vendored copies, and a version bump on either side changes the census.

Related: [[decision_reference-acquisition-route]], [[decision_claim-verification-adopted]].
<!-- END:ancestry -->

## fp-acceptance — withdrawn historical payload

<!-- BEGIN:fp-acceptance -->
# The FP model layer's acceptance — correctness at scale, the second engine, the measured cost

- **Type:** `reference`
- **Date:** `2026-10-06`
- **Status:** `active`
- **Owner / source:** measured by `P4-SYSTEM.7` slice (e3) (the leaf's acceptance), closing
  [`decision_fp-backend-qualification.md`](decision_fp-backend-qualification.md); re-run at
  HEAD `c377bcc` (the tree's (e3) checklist carries the commands)

## The fact

The decision stands: rustc_apfloat `=0.2.3` behind the model layer `fp.rs`, which owns the
RISC-V policy and patches the backend's two genuine flag deviations. F (30 forms) and D (32)
execute in the tracked rv64gc engine through it. The evidence the acceptance asks for:

- **Correctness, spec-side and tracked** (FP-VECTORS gates both tables against the
  exact-rational reference `scripts/specfp.py` — neither SoftFloat, APFloat nor MPFR — which
  is itself re-checked against the host's hardware IEEE every run, agree 2131): 230 directed
  vectors (the rules) and 3,168 seeded fixtures across all 21 model-layer operations × both
  formats × every rounding mode (the breadth) — all pass.
- **Correctness at corpus scale** (scratch `fpcheck`, re-run at slice d3): `fp.rs` over the
  63,752-case slice-(a) corpus disagrees with the exact-rational reference on **0** cases;
  with MPFR on exactly the 24 signaling-NaN conversions this record's second amendment
  attributes to the oracle.
- **The engine end to end**: the 22 F/D guests (+ the two FP-state guests) satisfy their
  spec-derived expectations on the tracked engine (125/125 corpus) and on Sail 0.14 — **24
  AGREE of 24**, 927 steps. Sail's FP is SoftFloat, so that agreement is the ENCODING/STATE
  match (decode, the FS gate, NaN-boxing, flag accrual, reserved rounding modes) plus one
  more numeric opinion — the numeric independence is the fixtures' (EVD-04).
- **Performance on this host** (release, 2M iterations, black_box operands): the model
  layer costs f64 add 47.8 / mul 47.4 / div 122.7 ns, f32 add 46.2, fma 65.8, sqrt 83.7
  (f64) / 58.7 (f32), convert d→s 27.2 / s→d 6.8, to_int 5.5, from_int 8.2, min 4.3 — 2.8–6.9×
  the raw backend on the arithmetic core (8.3 / 6.9 / 44.5 ns measured in the same run). The
  premium is the exact OF/UF: every rounded result is evaluated a second time at the same
  precision over a 15-bit exponent. Acceptable for a laboratory model; a cheaper guard
  (re-evaluate only when the delivered result sits at a range edge) is named, not taken.
- **Ancestry**, unchanged: TestFloat's computed expectations are SoftFloat's and were never
  counted (`RK07`, EVD-04); the lineages that carry THIS closing evidence are LLVM APFloat
  (the backend), the exact-rational reference (written from the chapters), and the host's
  hardware IEEE (the reference's own judge) — slice (a)'s MPFR and softfloat legs stand as recorded above.
<!-- END:fp-acceptance -->

## zero-hits — withdrawn historical payload

<!-- BEGIN:zero-hits -->
# My search returned zero hits — is that absence, or is my instrument blind?

**Find out before you write it down.** A zero from a tool that cannot see the thing you are asking
about is indistinguishable, on screen, from a zero that means the thing is not there. The first is
a non-answer; the second is a finding. They are printed identically.

## What happened

The question was whether two reference models share a floating-point implementation — an `EVD-04`
independence question, where a wrong answer silently inflates the value of every differential
test. The obvious instrument:

```
$ strings -a sail_riscv_sim | grep -ciE 'softfloat|f32_add|f64_mulAdd'
0
$ strings -a spike           | grep -ciE 'softfloat|f32_add|f64_mulAdd'
0
```

Zero for both. Read naively: *neither model uses SoftFloat.* That was one step from being recorded
as a finding in a durable inventory.

A second instrument disagreed, and explained the first:

```
$ nm -a sail_riscv_sim | wc -l      ;  nm -a sail_riscv_sim | grep -ci softfloat
400                                    0
$ nm -a spike          | wc -l      ;  nm -a spike          | grep -ci softfloat
649743                                 495
```

Spike carries **495** softfloat-shaped symbols. The Sail binary carries **400 symbols in total** —
it is a stripped release build, and no symbol-based instrument can answer any question about its
internals. Its zero was never evidence about SoftFloat; it was evidence about the binary's symbol
table.

Reading the source settled it: the Sail model vendors Berkeley SoftFloat too, and 184 of the 199
`.c` files present in both copies are byte-identical. **The naive reading was the exact opposite
of the truth.**

## How to tell the two apart

Every zero needs a companion measurement that establishes the instrument could have seen a hit:

| The zero | The companion that validates it |
| --- | --- |
| `grep -c X file` → 0 | does `grep -c <something-certainly-present> file` return non-zero? |
| `nm \| grep -c X` → 0 | how many symbols are there *at all*? `400` is a stripped binary |
| `find … -name X` → nothing | does the search root exist and contain anything? |
| an API query returns `[]` | did it authenticate, and does it return rows for a known-present case? |
| a test suite reports 0 failures | how many tests *ran*? (see [[self-test-arms-that-never-ran]]) |
| a gate reports 0 findings over a sweep | did it enumerate the files you just added? A `git ls-files` sweep judges the index only — `git add -N` new files first |

The pattern is always the same: **report the denominator next to the numerator.** `0 of 400
symbols` and `0 of 649,743 symbols` are different sentences; `0` and `0` are the same sentence.

## The rule

> A zero from an instrument whose reach you have not measured is not a result. It is a question
> you have not asked yet.

When the denominator turns out to be too small to trust — a stripped binary, an empty search root,
an unauthenticated query — do not weaken the claim to fit the instrument. **Change instrument.**
Here that meant cloning the model's source, at the exact commit its own `--build-info` reports, and
reading it. That cost one shallow clone and turned a false finding into a true one.

Related: [[self-test-arms-that-never-ran]], [[availability-is-not-identity]],
[[a-shorter-trace-is-not-agreement]].

## Measured again — a green gate over a set that lacked the new files (2026-10-06)

P4-SYSTEM.7 slice (c6) added 22 untracked corpus files. `make gate` ran green twice with them
present but unstaged; the commit's pre-commit run, after `git add`, refused one
(`f-sgnj.expected.sexp`: an empty `derivation` — the authored comment began `|sNaN|:`, and `|`
is the directive's derivation/source separator). DOSSIER-SCHEMA enumerates with
`git ls-files -- 'profiles/*/*.sexp'` (`scripts/check_dossier_schema.sh:44`), and its verdict
prints the denominator: **202** documents judged while the files were untracked, **213** once
staged (`git ls-files … | wc -l`: 204 → 215, 2 skipped). The green runs were green over a set
that did not contain the defect — the same rule, one level up: read the count next to "ok".
A tracked-only sweep is right for a commit gate (it judges what will be committed); stage, or
`git add -N`, new files before the run you intend to cite (probed: an untracked file is absent
from `git ls-files`, an intent-to-add one is listed).
<!-- END:zero-hits -->

## p4-7 — withdrawn historical payload

<!-- BEGIN:p4-7 -->
- ID: `P4-SYSTEM.7` — **floating-point backend qualification** *(task card `T011`)*
  Status: **done** `2026-10-06` (design brief `2026-10-05`, `SEMULITH-P4-0038`; slices (a) `SEMULITH-P4-0039`, (b) `SEMULITH-P4-0040`, (c1)–(c6) `SEMULITH-P4-0041`–`-0048` — F BOUND, (d1)–(d5) `-0049`–`-0053` — D BOUND, (e1)–(e3) `-0054`–`-0056`)
  Result: **met.** rustc_apfloat `=0.2.3` is qualified and pinned behind the model layer `fp.rs`, which owns the RISC-V policy and patches the backend's two genuine flag deviations (overflow on a directed clamp; underflow at the smallest-normal boundary — the record's third was the MPFR oracle's, withdrawn at (d3)). F (30 forms) and D (32) execute in the tracked engine: 150 forms, 125/125 corpus. Correctness is measured spec-side and tracked — 230 directed vectors + 3,168 seeded fixtures from the exact-rational reference (itself hardware-checked every run), 0 of 63,752 corpus disagreements — and end to end on the second engine: Sail 24 AGREE of 24 (927 steps; an encoding/state match, Sail's FP being SoftFloat). Performance: the model layer 2.8–6.9× the raw backend on the arithmetic core, the exact OF/UF's cost. The record: `docs/decisions/decision_fp-backend-qualification.md` (two amendments) and its closing measurement `docs/decisions/reference_fp-model-layer-acceptance.md`.
  Goal: name a Rust candidate; pin the exact target policy for rounding modes, flags, result bits, conversions, NaN payloads and boxing; inventory ancestry (shared SoftFloat lineage, specialization, thread-local vs global status, exact compiler and features); run independent numeric fixtures.
  Acceptance: a decision record with **measured** correctness and performance evidence. If no candidate passes, implement the required subset in Rust and defer the capability. TestFloat's usual SoftFloat expected-value path is recorded as shared ancestry (`RK07`, `EVD-04`).
  ⛔ **Routed in from `P0-PROFILE.7` on `2026-09-14`, measured rather than anticipated:** the two reference models this project uses *both* vendor Berkeley SoftFloat, and **184 of the 199 `.c` files present in both copies are byte-identical** once the release-number comment is normalized (sail 3e / spike 3d; `f64_add.c` differs by one line). A Sail-versus-Spike floating-point comparison therefore executes **one implementation twice**. This leaf's ancestry inventory starts from that fact, and its independent numeric fixtures must derive expected values from something that does not descend from SoftFloat. See [`reference_softfloat-shared-ancestry`](../decisions/reference_softfloat-shared-ancestry.md).

<!-- END:p4-7 -->

## p4-1-note — withdrawn historical payload

<!-- BEGIN:p4-1-note -->
  gated on `.7` (the SoftFloat shared-ancestry constraint already routed there); the
<!-- END:p4-1-note -->
