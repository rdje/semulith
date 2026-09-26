# The semantics data is the execution authority — interpreter first, compiler as a derived artifact

- **Type:** `decision`
- **Date:** `2026-09-27`
- **Status:** `active`
- **Owner / source:** agent decision under director delegation `2026-09-27` — *"the decision is
  yours to make but it got to be sota, signoff and production-grade"*
- **Resolves:** the contradiction between `docs/ARCHITECTURE.md` §1.1 (semantics are **data**)
  and §2 (the reference interpreter is *"generated dispatch plus canonical Rust semantic
  functions"*) — a contradiction the roadmap's own rule says must be *recorded and resolved
  explicitly* before P1 meets it in code.

## The fact / decision

For the P1 interpreter, **the canonical semantics data executes directly**: a definitional
interpreter evaluates the declared 32-form language of `definitions/riscv/rv64i.sem.sexp`.
Compiled or hand-written Rust semantic handlers enter only as **generated artifacts derived
from that data**, admitted solely behind an observational-equivalence regression path — never
as a second, independently maintained implementation of the same rules.

## Why

**One owned implementation per rule (OWN-01).** The moment two implementations of the same
semantic rule coexist, "one canonical definition" is a claim rather than a fact, and every fix
becomes a synchronization problem. Interpreting the data keeps the number of authorities at
exactly one; a compiled handler is then a *view* of the authority, the way a compiled binary
is a view of source — useful, fast, and never the thing that is true.

**The SOTA precedent is the reference this project already pins.** Sail — a configured
reference here — is built exactly this way: the definitional interpreter over the semantics
is the reference behaviour, and C compilation of the same semantics is a derived performance
artifact whose evidentiary value rests entirely on agreeing with that interpreter.
Interpreter-first, with compilation admitted only as a provably equivalent derivative, is the
established pattern for trustworthy executable specifications. Handwritten per-instruction
Rust handlers as the primary authority is the pattern this record refuses.

**The dual mandate argues the same direction.** A student reads `(sext 64 (trunc 32 …))` and
the interpreter that evaluates it, and sees one thing twice rather than two things that must
be kept equal. The teaching artifact and the production artifact stay one artifact.

**Performance is a measured need, not a scheduled rewrite.** The roadmap already defers
optimization (*"optimize only with equivalent evidence and measured need"*). A tree-walking
interpreter over 52 scalar instructions is far inside any plausible P2 budget; if measurement
later says otherwise, the compiled lane below is the admission path.

## How to apply

- **P1 (`P1-LAB.6`–`.8`)** executes the semantics data directly; the canonical-definition
  skeleton owns the data, the interpreter, and the generation manifest — not a parallel table.
- **Any compiled-handler or semantic-IR lane** must (a) generate from the semantics data with
  fingerprints in the manifest, and (b) carry the observational-equivalence regression the
  roadmap already requires for optimization work. Hand-maintained semantic handlers that
  mirror the data are an OWN-01 breach, not a backend.
- **Revisit when:** a measured P2/P4 performance need is documented, or the semantic-IR
  migration decision is made — whichever comes first. Either reopening replaces this record,
  explicitly, in the same format.

Related: [[decision_canonical-definition-input]], [[decision_one-format-every-source-of-truth]],
[[decision_dual-mandate-production-and-teaching]], [[decision_lane-consumption]].
