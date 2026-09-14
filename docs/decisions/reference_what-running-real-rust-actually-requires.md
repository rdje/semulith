# What "runs real C and Rust" actually requires, measured

- **Type:** `reference`
- **Date:** `2026-09-14`
- **Status:** `active`
- **Owner / source:** measured on this machine while assessing readiness; the north star is the
  director's, `2026-09-14`: models *"capable of running real code (C, Rust, ...)"*

## The measurement

`riscv64imac-unknown-none-elf` is already installed, and `rust-lld` links without any GCC
cross-toolchain — so real Rust can be produced for RISC-V on this machine **today**. A trivial
`#![no_std]` function (a loop, a multiply, a divide) compiles to 17 instructions:

```
 10   59%  C  compressed, 16-bit   NO fragment exists     add addi beqz j or ret slli srli
  3   18%  M  mul / mulhu / divu   fragment EXISTS, not composed into the profile
  4   24%  RV64I base              modelled                addi seqz slli

executable by rv64i-lab-v0 as declared (extensions = []): 4 of 17 = 24%
```

⛔ **And the first instruction of `_start` is a compressed one**, so the model does not execute 24%
of the program — it halts at offset 0. A percentage of *instructions covered* is not a percentage
of *program executed*, and conflating them would flatter the model enormously.

## What follows, and it changes the order of work

- **There is no `riscv64i` Rust target.** The minimum Rust ships for 64-bit bare metal is
  `riscv64imac`. So `rv64i-lab-v0`, with `extensions = []`, **can never run Rust output** — not
  after more work on RV64I, not ever. Growing the profile is not an optimisation here; it is the
  only path to the stated goal.
- **C (compressed) is on the critical path, ahead of everything else.** It is 59% of this sample
  and it is what the very first instruction needs. No fragment exists for it.
- **M is the cheapest step**: `definitions/riscv/m.sexp` already exists, is proven disjoint from the
  base, and is simply not composed into the profile (`extensions = []`).
- **A (atomics)** is untouched and is required by the target triple, though it did not appear in a
  single-threaded sample — absence in this program is not absence in the target's ABI.

⚠️ **This does not say the current work was misdirected.** RV64I is the right first unit: it is
where the encoding, semantics, composition and evidence machinery was built and fired. What the
measurement says is that **"runs real code" is a property of a composed profile, not of a base
ISA**, so it is `MODEL-COMPOSE`'s milestone rather than `MODEL-METHOD`'s — and that the composition
machinery now has a concrete, measurable target to aim at instead of an aspiration.

## How to apply

- When a leaf claims progress toward "runs real code", state it as **programs that run to
  completion**, never as instruction coverage.
- Re-run the measurement when the profile gains an extension; the sample is one trivial function
  and a larger corpus will shift the proportions. The procedure is in this project's history, not
  a tool — ⚠️ **a one-off measurement, not an instrument**, and it should become one before any
  claim rests on it.

Related: [[decision_composition-model]], [[decision_one-definition-one-book]],
[[decision_dual-mandate-production-and-teaching]].
