# CHANGELOG shard — SEMULITH-MM-0040 … SEMULITH-MM-0040

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-MM-0040 (leaf MODEL-METHOD.9) — the semantics: 52 of 52, every rule cited

**What changed.** Nothing machine-executable existed. A generator engine reading the canonical
definition found configuration, state, provenance, assumptions and encodings — and still could not
produce an interpreter, because what each instruction *does* lived only as English prose in a
decision's `statement` field. 26 rules, all prose, none executable.

`definitions/riscv/rv64i.sem.sexp` now carries **52 of 52** declared instructions as expressions,
each citing the specification locator it was derived from.

⭐ **Widths are always explicit**, because an implicit width is where two models silently disagree:

```
(sem (insn addiw) (source "RVI-RV64I §3.1.2 — D-WSUFFIX …")
     (effect (set (reg rd) (sext 64 (trunc 32 (add (trunc 32 (reg rs1)) (sext 32 (imm imm12))))))))
```

That is the whole of `D-WSUFFIX` in one line, and it can be checked against the sentence that
produced it — which is the entire evidence argument for a hand-derived semantics.

⛔ **Generated and authored content live in different files on purpose.** `rv64i.sexp` is generated
from a machine-readable table and regenerated whenever that table moves; hand-derived semantics in
the same file would be destroyed by a regeneration. Different provenance, different file.

**The language is 32 forms**, each added because an RV64I instruction needed it, none in
anticipation — and the checker refuses everything else. Four controls fired on the real file: a
missing instruction (`sraw`), an unknown operator (`multiply`), an operand the instruction does not
have (`imm12` in `sub`), and a rule citing nothing. Each refused by name.

⚠️ **What `52 of 52` does not mean.** It says the semantics are well-formed, complete and *cited*.
It does **not** say they are **correct**. Proving that is a differential experiment against a
reference model — what `P0-PROFILE.6` does for three guest programs today and what `P1-LAB` must do
at scale. A definition that says something checkable is not yet one that says something true.

⛔ `riscv/m`'s semantics are absent and that is correct: `rv64i-lab-v0` does not compose `M`, and
writing semantics for a fragment no unit uses would be inventory.


