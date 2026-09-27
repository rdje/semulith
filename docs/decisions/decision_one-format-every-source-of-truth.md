# One format for every source of truth, extensible by data, parsed by a generated parser

- **Type:** `decision`
- **Date:** `2026-09-14`
- **Status:** `active`
- **Owner / source:** director instruction, `2026-09-14`
- **Supersedes:** [`decision_canonical-definition-input`](decision_canonical-definition-input.md)'s
  per-file format split (that record's no-duplicated-fact rule and its choice of S-expressions for
  encodings and semantics both stand; only the *split* is superseded)

## What is being decided

> *"Sources of truth shall be composables and extensibles to support new constructs using the same
> format. for me S-expression or lisp-like is the simplest format we can chose."* — director

Every file the model generator engine reads is one format: **S-expression**. Not "the format its
content wants", which is what the superseded record chose.

## Why the split was wrong, stated as the argument that beats it

The superseded record defended JSON Lines and TOML for records on the grounds that *records are not
trees*. That is true about shape and it answers the wrong question. **Composition is a merge**, and
three formats are three merge semantics — so under the split, `encoding.sexp` composes and
`profile.toml` composes with nothing. The first board that composes two processors must merge their
requirements, obligations and pinned sources too, and the split provides no rule by which it could.
The defence was also partly sunk cost: `RECORD-SCHEMA` and `validate_records.py` had been fired RED
and were working, and working instruments are the hardest thing to give up.

## Extensible means the reader enumerates nothing

A format is not extensible because it has parentheses. It is extensible when **adding a construct
is adding data**. So the construct vocabulary lives in schema files written in the same
S-expression notation, and the schema language is described in itself. Adding `(register-file …)`
or `(memory-map …)` is a new schema file and zero lines of code.

⚠️ **The honest boundary:** adding a *domain* construct needs no code. Extending the *schema
language itself* with a new kind of declaration does change the validator. That is the same line a
database draws between adding a table and adding a column type, and it is named here so nobody
meets it later as a surprise.

⛔ **An undeclared construct is a hard error, never a silent ignore.** `(sourcs "…")` is a perfectly
well-formed S-expression. Without this rule, "extensible" degrades into "typo-tolerant", and a
source of truth that tolerates typos is not one.

## The parser is not written here — it comes from LinkedSpec

> *"you do not need to create a S-expression parser to AST. I have another project with many
> backends and Rust is one of them that can parse many sort of file formats."* — director,
> `2026-09-14`; and, correcting my first identification: *"Not it is not PGEN. It is LinkedSpec
> with the Rust backend and the Lispish.spec"*.

**LinkedSpec** (`../linkedspec`, sibling repository, same volume) is a progressive-extraction
parser DSL: one `.spec` contract implemented by a Perl reference engine and native **Rust**, Dart,
Julia and Lua variants. The artifact this project needs already exists there — verified, not
assumed:

```
linkedspec/docs/linkedspec-book/                 its mdBook — read this before integrating
linkedspec/specs/Lispish.spec                    the lisp-like contract
linkedspec/rust/linkedspec-runtime/              the Rust backend
linkedspec/tests/corpus/lispish/                 its corpus
linkedspec/docs/knowledge/archogen-rust-lispish-integration.md
```

⛔ **I named the wrong project first.** I inferred `pgen` from a description — *many backends, Rust
among them, parses many formats* — because `pgen` generates Rust parsers from EBNF and its grammar
corpus looked like the right shape. The inference was wrong, and the director corrected it. Worth
keeping, because the failure mode is general: **a capability description matches several
repositories; only a named artifact identifies one.** `pgen/grammars/` has no S-expression grammar
at all; every `*sexp*` path there is a SystemVerilog test fixture. I would have written a grammar
that already existed, in a spec language that was not the one in use.

### How it is consumed: a git submodule

Director instruction, `2026-09-14`: *"You will have to git submodule it."* LinkedSpec enters this
repository as a **git submodule**, pinned to a commit — so the parser contract is versioned with
this repository rather than depending on whatever happens to be checked out next door. That also
satisfies Policy 13: the submodule content lives inside this repository's own tree, on the same
volume, rather than being reached across a path.

### ⛔ Blocked, and on what

LinkedSpec is **preparing an integration document for downstream consumers, and it is not done**
(director, `2026-09-14`). Integrating against an interface whose contract has not been published
yet means integrating against today's internals, which is how a submodule becomes a fork. So:

- `SOT-FORMAT.9` is `blocked` until that document exists. Its mdBook is at
  `linkedspec/docs/linkedspec-book/` and is the thing to read when the leaf unblocks
  (director, `2026-09-14`) — the book, not the source.
- `scripts/sexp.py` **predates this decision** — committed with `MODEL-METHOD.8`, before the
  direction was given — and remains the Python tooling's reader in the meantime. It is a repaired
  150-line reader, not new work undertaken against this instruction.
- **No hand-written S-expression parser goes into this project's Rust crates**, then or now.

## How to apply

- **Adding a source of truth?** It is `.sexp`, and its constructs are declared in `schema/`.
- **Adding a construct?** Write the schema file. If you are editing Python to add a construct, the
  schema layer has a hole and the hole is the bug.
- **Needing a parser in Rust?** It comes from LinkedSpec, via the vendored submodule
  (`SOT-FORMAT.9`) — no S-expression parser is hand-written in this project's crates. Corrected
  `2026-09-27` (`SOT-FORMAT.6`): this bullet still said `pgen`, contradicting the record's own
  body above, which the director corrected on `2026-09-14` — *"Not it is not PGEN. It is
  LinkedSpec with the Rust backend and the Lispish.spec."*

Related: [[decision_canonical-definition-input]], [[decision_composition-model]],
[[decision_one-definition-one-book]], [[a-parse-without-error-is-not-a-faithful-read]].
