# CHANGELOG shard — SEMULITH-MC-0039 … SEMULITH-MC-0039

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-MC-0039 (leaf MODEL-COMPOSE.2) — fragments get a form and a home

**What changed.** The unit carried all 52 instructions **inside itself**. A base ISA is shared by
every profile that composes it, so a second RV64 profile would have copied 52 instructions that
then had to be kept equal — the exact duplication the no-duplicated-fact rule exists to prevent,
in the one place most tempting to copy.

- `definitions/riscv/rv64i.sexp` — the base: 52 instructions, plus the operand fields and
  scattered-immediate layouts a base owes its extensions.
- `definitions/riscv/m.sexp` — the M extension: 13 instructions, `(requires "riscv/rv64i")`.
- The unit now **names** what it composes and owns nothing: `(compose (base "riscv/rv64i")
  (extensions))`. Census: instructions in the unit `52 → 0`; in `definitions/` `0 → 65`.

⭐ **The acceptance test is that nothing observable moved.** A refactor of the source of truth must
not perturb the evidence, so all four guests were re-assembled and re-run: the `elf sha256` values
are **byte-identical** to before the split, across two reference models, all reproducing.

**Two refusals, both fired.** Composing `riscv/m` without its base →
`requires 'riscv/rv64i', which this composition does not provide before it. A fragment with an
unmet dependency composes by luck, not by construction.` Composing a fragment that does not exist →
`composes 'riscv/nope', but definitions/riscv/nope.sexp does not exist`.

**The `M` fragment is now pinned** (`rv_m`, `rv64_m` digests) — a fragment composed from an
unpinned source is a model built on something nobody can re-derive. Fragments are re-derived
against the pinned tables and fired RED on a one-nibble `funct3` edit to `mul`. The tracked
generator reproduces them **byte-for-byte**, so it is the owner and the files are not a
hand-maintained copy of its output.

⚠️ `definitions/` was **registered in the routes registry in the same commit that created it** — a
new tracked family that nothing governs is how pressure escapes, which this project has already
measured once.

⚠️ Three references to the generator's old name survive in this file and in `MODEL-METHOD.8`'s
completed checklist. They are left alone deliberately: both are historical records, true when
written, and rewriting them to match today is what the `append_history` lifecycle prevents.


