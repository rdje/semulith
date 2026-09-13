# The model is production-grade **and** a teaching text — one artifact, two mandates

- **Type:** `decision`
- **Date:** `2026-09-14`
- **Status:** `active`
- **Owner / source:** director instruction, `2026-09-14`; binds `MODEL-BOOKS`, `MODEL-METHOD`,
  and every model from `P0` onward

## The decision

Every processor model this project produces must be **signoff, production-grade** *and* must serve
as **educational material** — a text from which a student can learn to build a production-grade
CPU/DSP model capable of running real compiled code (C, Rust, …).

These are **one artifact with two mandates**, not two deliverables. The per-model mdBook is the
teaching text; the profile, contract, records and gates are the production artifact it teaches
from. A book that explains a model nobody would ship teaches the wrong thing, and a model nobody
can learn from is a model only its author can maintain.

## What the teaching mandate actually changes

It is tempting to read "educational" as "add explanation", which would change nothing important.
It changes four concrete things:

1. **The reasoning must be recoverable, not just the result.** A decision records *why this and
   not the alternative*, including alternatives rejected. A student learns from the rejected
   branch; a maintainer needs it too, which is why this costs nothing extra.
2. **Mistakes stay in the record.** This project has already found, in its own work, a matched
   profile that matched only an instruction set, a comparator that called a truncated trace
   agreement, a self-test that ran four of fourteen arms, and a gate report that counted a
   *mention* as an implementation. ⭐ **Those are the most instructive pages in the book**, and
   removing them to look competent would remove the teaching. They are kept, with what the wrong
   instrument said and why it was believed.
3. **The order of work becomes part of the content.** *Why establish the evidence path before
   writing a model? Why declare the required evidence before building fixtures?* A reference
   manual may assume its reader knows; a teaching text must justify the sequence, because the
   sequence is the transferable part.
4. **"Runs real code" becomes a stated target with stated limits**, not an aspiration — see below.

## What "capable of running real code" requires, measured

The first profile is `RV64I` with **no extensions at all**. That is a real target, and a
constrained one, and the constraints are the honest starting point for the teaching:

| Absent | Consequence for compiled C/Rust |
| --- | --- |
| `M` | no hardware multiply or divide — the compiler must emit runtime calls (`__muldi3`, `__divdi3`, …) |
| `A` | no atomics — Rust's `core` atomics are unavailable without a single-hart polyfill |
| `F`/`D` | soft-float ABI (`lp64`, not `lp64d`); every float operation is a library call |
| `C` | no compressed encoding — larger images, otherwise no semantic effect |

Running real code therefore needs materials this project has **not yet pinned**, and each is now
an acquisition item rather than an assumption:

- the **RISC-V psABI** — calling convention, register roles, `lp64` variants, stack alignment;
- the **RISC-V ELF specification** — `e_flags`, relocations, program-header expectations;
- a **startup and runtime contract** — entry state, stack establishment, `.bss`, `.data`;
- the **compiler-runtime intrinsics** a no-`M`, soft-float target will call;
- a **program-exit and console convention** — HTIF, semihosting, or a declared MMIO device.

⚠️ Note what this does to the profile's own honesty: `state.json` records ABI register names as
`software-convention` precisely because the ISA chapter does not own them. Running real code makes
that convention **load-bearing**, so the psABI stops being background reading and becomes a pinned
material with a digest.

## How to apply

- **When writing a chapter**, ask what a reader could *build* from it. A chapter that can only be
  agreed with has not taught anything.
- **When a mistake is found**, record what the wrong instrument said, why it was convincing, and
  the measurement that settled it. Do not rewrite history into competence.
- **When declaring a profile**, state what real code it can and cannot run, with the reason drawn
  from its extension set rather than from optimism.
- ⛔ **Neither mandate may be traded for the other.** Simplifying a contract to make a chapter
  easier is a production defect; omitting the reasoning to keep a record terse is a teaching
  defect. Where they genuinely conflict, the production artifact wins and the book explains the
  complexity — because a student learning from a simplified fiction learns a fiction.

Related: [[decision_claim-verification-adopted]], [[decision_reference-acquisition-route]].
