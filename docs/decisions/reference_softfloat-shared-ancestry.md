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
