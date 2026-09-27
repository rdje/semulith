# CHANGELOG shard — SEMULITH-MM-0033 … SEMULITH-MM-0033

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-MM-0033 (leaf MODEL-METHOD.1) — answer the narrower-instrument sweep, with a wider instrument

**The open question, answered.** `P0-PROFILE.10` fixed one instance of a pattern — a single
confident scalar standing in for a configuration — and left the general question open. The sweep
enumerated every pinned scalar that stands for a configuration and checked each.

⛔ **One further instance, and worse than the first.** `spike.matched_isa_string = "rv64i"` was the
command-line **input** recorded in an observation's slot. Spike has no `--print-isa` option, so
nobody had ever confirmed it configured what it was told. The first instance was a narrow reading;
this one was not a reading at all.

It is now read back from a surface Spike does offer, with a control proving it is an observation
rather than an echo: `--isa=rv64i` → `riscv,isa = "rv64i"`, `--isa=rv64im` → `"rv64im"`.

⭐ **The replacement principle is now an instrument.** A match is claimed against the model's own
self-description at the **widest granularity it offers**, compared field by field. Both references
emit a device tree, so `scripts/compare_platforms.py` compares them:

```
FIELD                  sail (matched)           spike (matched)          agree
riscv,isa              "rv64i_zvl32b"           "rv64i"                  NO
mmu-type               "riscv,none"             "riscv,sv57"             NO
riscv,pmpregions       <absent>                 <0x10>                   NO
timebase-frequency     <500000000>              <0x989680>               NO
devices only spike advertises: clint@2000000, cpu@0, ns16550@10000000, plic@c000000
```

**4 of 4 platform fields disagree, and Spike advertises a UART, a platform interrupt controller,
an interruptor and a CPU node** that Sail does not — none of it visible in an ISA string.

- **New rule 5b** in `PROFILE-CONSISTENCY`: a pinned `matched_isa_string` must declare both what it
  does **not** establish and **where it was read from**. Fired RED on the real dossier.
- All three candidates now carry `matched_scope` — including QEMU, whose emptiness is now visible
  rather than inferred from an absent row.

⚠️ **The wide instrument has its own scope, and says so.** A device tree describes what a platform
*advertises* — not semantics, not memory attributes — and carries residue: Sail's still advertises
a `timebase-frequency` and an `htif` node with no device behind them. **Wider is not complete.**
Recording that is what stops this instrument becoming the next narrow one.

⛔ **The honest form of the answer:** one further instance existed, it is fixed, and the pattern is
gated. I am not claiming there are no others — I am claiming a new one cannot be *added* without
declaring its scope, which is the only durable form that answer can take.

**Also opened:** `MODEL-METHOD`, the tree that makes the modelling method and its required
materials explicit, with the format call recorded — JSON Lines under a JSON Schema, not
S-expressions, because the data is records rather than trees and the repository already gates
JSONL. S-expressions are parked for the canonical executable semantics in `P1-LAB`, with a trigger.


