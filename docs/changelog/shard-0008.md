# CHANGELOG shard — SEMULITH-MM-0037 … SEMULITH-MM-0037

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-MM-0037 (leaf MODEL-METHOD.8) — the repository owns its encodings

**What changed.** A single source of truth per unit, from which a generator engine extracts what it
needs, requires the repository to actually **own** that source. It did not. Measured:

```
$ git ls-files | grep -c riscv-opcodes
0                       # the assembler read an untracked, network-acquired directory
$ git ls-files profiles/rv64i-lab-v0 | grep -cE 'encod|semant'
0                       # neither encodings nor semantics were owned
```

A fresh clone could not build a model at all, and the project's own rule — *a constant that is a
function of an external document is derived or gated, never assumed present* — was being broken by
its own tooling.

- `profiles/rv64i-lab-v0/encoding.sexp` — **tracked**: 52 instructions, 12 operand fields, 3
  scattered-immediate layouts, each carrying its upstream file and that file's digest.
- `scripts/sexp.py` — a reader for exactly the shapes these files use, refusing the rest.
- `scripts/gen_encoding.py` — regenerates it; `fetch_references.sh` re-derives and compares.

⭐ **The test that settles it is not that the file exists.** It is that the model builds *without*
the untracked directory, so the upstream was moved aside and the whole evidence path re-run:

```
$ mv target/refs/riscv-opcodes /tmp/ro-hidden && scripts/run_smoke.py
run_smoke: ok — every program matches its specification-derived expectations and reproduces
```

Four guest programs assembled, executed on two references and reproduced, with the source of the
encodings absent from disk.

**Ownership without re-derivation is a copy**, so the agreement is checked: fired RED by changing
**one bit** of one instruction's `funct3` — `and`'s `(14 12 0x7)` to `0x6` — producing
`DIFFERS … no longer matches what the pinned tables generate` with the line quoted.

⛔ **The new reader was caught by its own first real input.** Its tokenizer stripped `;` comments
line by line *before* tokenizing, which is wrong twice over: a `;` **inside a string** truncated
the string, and a string could not span lines. Generating this project's own encoding file hit the
second within minutes. It is now a single stream scan — whether a `;` starts a comment depends on
whether a string is open, which is the only way that question can be answered correctly.

**Also decided:** [`decision_canonical-definition-input`](docs/decisions/decision_canonical-definition-input.md).
The S-expression trigger parked earlier has **fired**: the canonical definition is a **set of
format-fit files** — S-expressions for `encoding.sexp` and `semantics.sexp` because those are
trees, records staying JSON and TOML because they are records and are already gated by instruments
fired RED. "Single source of truth" is preserved by a **no-duplicated-fact** rule, not by
single-file-ness.

⚠️ This makes the repository own its encodings. It does **not** make the canonical definition
sufficient: **semantics are still absent** — the decisions are English prose and nothing
machine-executable exists. `MODEL-METHOD.9` owns that, and `.10` turns *"the engine can extract all
it needs"* from an intention into a verdict that gates writing model code at all.


