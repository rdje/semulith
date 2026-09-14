# The canonical definition: one source of truth per unit, as a set of format-fit files

- **Type:** `decision`
- **Date:** `2026-09-14`
- **Status:** `superseded in part` — the per-file **format split** below is replaced by
  [[decision_one-format-every-source-of-truth]] (`2026-09-14`): every source of truth is
  S-expression. The **no-duplicated-fact rule** and the reasons for choosing S-expressions for
  encodings and semantics are unchanged and still govern.
- **Owner / source:** director instruction, `2026-09-14`; the deferred S-expression trigger from
  `MODEL-METHOD`, now fired

## What is being decided

Every modelled unit has **one canonical definition** — the single source of truth from which a
generator engine extracts everything it needs to build the model. `docs/ARCHITECTURE.md` §4 already
requires this and says files may be modular provided *a semantic rule has one owned
implementation*. This decision settles the part that was open: **what those files are, and in what
format.**

## The trigger fired

`MODEL-METHOD` chose JSON Lines for the materials catalogue and parked S-expressions with an
explicit trigger: *"the first time a material must carry a nested semantic expression rather than a
citation."* A generator engine needs executable semantics. That is the trigger, and the answer is
no longer a preference.

## The decision: a set of files, each in the format its content actually wants

"Single source of truth" is preserved by a **no-duplicated-fact rule**, not by single-file-ness —
each fact has exactly one owning file, which is the same rule `ARCHITECTURE.md` already states.

| File | Owns | Format | Why that format |
| --- | --- | --- | --- |
| `profile.toml` | identity, configuration, declared scope, decisions with provenance | TOML | human-authored and comment-rich; already gated by `PROFILE-CONSISTENCY` |
| `state.json` | architectural state, reset values, the hidden-state census | JSON | records; already gated |
| `encoding.sexp` | instruction formats, fixed bits, operand fields | **S-expression** | ⛔ new, and it closes a real gap — see below |
| `semantics.sexp` | what each instruction *does* | **S-expression** | expression trees; the reason the trigger existed |
| `requirements.jsonl`, `contract-obligations.jsonl` | requirements, obligations, checks | JSON Lines | already validated by `RECORD-SCHEMA` and a tracked validator |
| `sources.toml`, `references.toml` | provenance, pinned materials, references | TOML | already gated |

### Why S-expressions for semantics, and only for semantics

Semantics are **expression trees**. The meaning of `ADDIW` is a nested expression, and JSON renders
it as punctuation:

```
(sign-extend 64 (bits 32 (+ (low 32 (reg rs1)) (sign-extend 32 imm12))))
```

That form is readable, diffable, reviewable **against the specification prose by a human**, and
parseable by about eighty lines of code. It is also the form the ISA-formalism tradition converged
on — Sail, ACL2 and SMT-LIB all shape semantics this way, for this reason.

⛔ ~~**And the records stay as they are.**~~ **SUPERSEDED, and the reasoning is kept because it is
the instructive part.** The argument below is sound about *shape* and answers the wrong question:
composition is a merge, and three formats are three merge semantics. Original text: Converting `requirements.jsonl` to S-expressions would
discard a validator and a doctrine that have both been fired RED, in exchange for nothing: those
files are *records*, not trees. Using one format everywhere would be tidiness bought with working
instruments.

## The two gaps this decision exposes, measured

A generator engine reading today's canonical definition would find configuration, state, provenance
and environment assumptions — and **neither of the two things it most needs**:

```
instruction ENCODINGS owned by the repo   : NO — read at runtime from target/refs/riscv-opcodes (UNTRACKED)
executable SEMANTICS                       : NO — nothing machine-executable exists; decisions are English prose
$ git ls-files | grep -c riscv-opcodes
0
```

⭐ The encoding gap is the sharper of the two. The assembler reads encodings from a **fetched,
untracked** directory, so a fresh clone cannot build a model at all — and the project's own rule is
that a constant which is a function of an external document is derived or gated, never assumed
present. `encoding.sexp` makes the repository own its encodings, with a gate proving it still
agrees with the pinned upstream table.

## How to apply

- **Adding a fact?** Put it in the one file that owns that kind of fact. If two files would state
  it, one of them is wrong.
- **Writing semantics?** Every form carries the source locator it was derived from, so a reviewer
  can check the expression against the sentence — the whole evidence argument depends on that being
  possible.
- ⚠️ **The engine does not exist yet**, and this decision does not pretend otherwise. It defines the
  input so that `P1-LAB` builds a consumer of a settled format rather than inventing one under
  deadline. The completeness of the definition is itself checkable — every declared instruction
  must have an encoding, semantics and a requirement — and that check is the precondition for
  writing model code at all.

Related: [[decision_one-definition-one-book]], [[decision_dual-mandate-production-and-teaching]].
