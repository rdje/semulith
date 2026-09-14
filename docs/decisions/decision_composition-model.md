# Composition: how small, proven models assemble into large ones

- **Type:** `decision`
- **Date:** `2026-09-14`
- **Status:** `active`
- **Owner / source:** director instruction, `2026-09-14`, correcting an earlier proposal of mine

## What this replaces

I proposed a **tier** — `exploratory` (ungated) versus `accepted` (gated) — as the lever for
getting breadth faster. That was the wrong instinct and is rejected here. It buys breadth by
creating a second class of model that nobody can trust, and the two classes would blur the first
time one was cited by the other.

The right lever is **composition**: every model stays signoff-grade, and complexity is reached by
**assembling proven small models**, not by lowering the bar for large ones. Breadth then comes from
*reuse of evidence*, not from absence of it.

## This is not invented — it is already how the field and this project work

Measured in the two reference implementations this project already pins:

```
riscv-opcodes  extensions/          -> 111 files, one per extension
sail-riscv     model/extensions/    ->  34 directories, 59 files defining instruction encodings
sail-riscv     model/               -> core, sys, pmp, exceptions, mops … as separate concerns
```

Both build a processor definition by **union of fragments**. And this project already carries the
other half: `profile.toml` has an `extensions = []` seam that is empty but present, and
`contract-obligations.jsonl` already holds **8 environment-assumptions** — the CPU already declares
what something else must guarantee. `docs/CPU_ENVIRONMENT.md` §5 already names the rule: *for every
CPU assumption, identify the board/device guarantee satisfying it or reject the composition.*

What is missing is not the idea. It is that neither is **structural or checkable** yet.

## The model: two axes, one port mechanism

### Axis 1 — intra-unit composition: **union with conflict detection**

A unit's definition is a union of **fragments**, each a complete, checkable description of one
thing: a base ISA, an extension, a concern (traps, memory). `RV64I + M + A + C` is a union.

The operator is union, and it is **safe or provably unsafe**: two fragments may not claim the same
encoding bits, redefine the same state element, or contradict a decision. ⭐ Encoding-space
disjointness is *decidable* — it is a finite check over fixed-bit masks — which makes "these
fragments compose" a verdict rather than a hope. That check is the single highest-value thing in
this decision, because it is the one that catches a real mistake mechanically.

### Axis 2 — inter-unit composition: **assumption / guarantee discharge**

A board is not a bigger CPU; it *contains* one. The operator here is not union but **discharge**:
every sub-unit's `environment-assumption` must be matched by a `guarantee` from the composing unit
or a sibling, or **the composition is rejected**. That is §5, made mechanical.

This is why the layer boundary matters: a processor exports assumptions precisely so a board can
discharge them. The 8 assumptions `rv64i-lab-v0` already carries are its composition interface,
written before any board existed.

### Direction is a consequence of PORTS, not a third mechanism

A unit declares what it `requires` and what it `provides`. A composition binds them.

- **Bottom-up:** define fragments and units, then compose concrete parts.
- **Top-down:** declare a composition with **unbound slots** — `(slot cpu (requires …))` — and bind
  later. The composition is then *incomplete but still checkable*: its shape, its address space and
  its unmet requirements can all be verified **before the parts exist**.

One mechanism, both directions. And compositions **nest** — `computer → board → soc → {cpu,
device}` — because a composition is itself a unit with the same record shape. That is what makes
the pieces behave like Lego rather than like a special case at each level.

## When does a composition "lead to a functional model"?

Stated as a conjunction, so it can be checked rather than judged:

1. **Union is conflict-free** — no two fragments claim the same encoding bits or state element;
2. **Every assumption is discharged** — by a sibling's or the parent's guarantee;
3. **No slot is unbound** — or the unit is explicitly declared partial, and says so;
4. **The composed definition is sufficient** — every instruction it declares has an encoding, a
   semantics and a requirement (the `MODEL-METHOD.10` check, applied to the composition).

A composition satisfying all four is a functional model. One failing any is rejected with the
specific reason, which is the property that makes assembly safe at scale.

## What composition does NOT do

⛔ **It does not lower the evidence bar, and must never be allowed to look as if it does.** A
composed unit inherits its parts' evidence **and owes composition evidence of its own** — that the
parts actually compose, that the discharges are real, that the address space is consistent. A board
whose CPU passed its gate has not thereby passed a board gate.

⚠️ **Encodings are the easy axis; semantics are the hard one.** Union of encodings is decidable.
Union of *semantics* is not, in general: an extension can change the meaning of a base instruction
(adding CSRs changes trap behaviour; adding `C` changes `IALIGN` and therefore which branch targets
fault). So semantic composition needs **refinement points declared explicitly** — a fragment must
say *"I modify this base behaviour"* rather than silently overriding it. This decision commits to
the encoding check first, because it is cheap and decidable, and to treating any silent semantic
override as a defect.

## How to apply

- **Writing a fragment?** It must be independently checkable. A fragment that is only meaningful
  after composition is a fragment with a hidden dependency; declare the dependency.
- **Composing?** State what each part provides and requires. An undischarged assumption is a
  rejection, never a warning.
- **Reaching for breadth?** Compose proven parts. If that is not possible yet, the honest answer is
  that the model is not ready — not that it should be gated less.

Related: [[decision_one-definition-one-book]], [[decision_canonical-definition-input]],
[[decision_dual-mandate-production-and-teaching]].
