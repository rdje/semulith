# DEV_NOTES shard — _(2026-09-14)_ … _(2026-09-14)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-09-14)_ — a category the layer does not own is not "missing"

- Devices are **board / SoC** material, not CPU material. The processor layer ends at the
  CPU/environment boundary: the CPU states assumptions, a board later states guarantees
  (`docs/CPU_ENVIRONMENT.md` §5, and `INFORMATION_CATALOG.md`'s own note that C19–C21 are not all
  properties of the CPU).
- ⭐ The consequence lands on the materials census, and it would have been a real defect: marking
  `C19 Platform, devices and interconnect` as `missing` for a CPU model manufactures an acquisition
  task for material the model must never contain, and reports a **correct scope as a deficiency**.
  The disposition vocabulary now carries a LAYER, and `deferred-to-board` is distinct from both
  `missing` and `not-applicable`. Caught before the schema was written, which is the only cheap
  moment to catch it.
- ⚠️ It also corrected my own framing of "runs real code": the console and the program-exit
  convention are BOARD concerns. What the processor layer owes real code is the psABI, the ELF
  contract, entry/startup state and the compiler-runtime intrinsics — and nothing else.
- `DIFF-PLATFORM-SPIKE` is a LAYER difference, not a configuration one: Spike ships a CPU and a
  small board together. The record now measures how much board each reference drags in.
- Promotion is explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — answer a narrow instrument with a wider one, and state the wider one's scope

- The sweep found **one further instance**, worse than the founding one: Spike's
  `matched_isa_string` was the command-line INPUT sitting in an observation's slot. Spike has no
  `--print-isa`, so nobody had confirmed it configured what it was told. Now read back from
  `--dump-dts`, with a control (`--isa=rv64im` → `rv64im`) proving it is an observation, not an echo.
- ⭐ The replacement is a principle with a tool behind it: claim a match against the model's own
  self-description at the **widest granularity it offers**. Both models emit a device tree; the
  comparison shows 4 of 4 platform fields disagreeing and four devices only Spike advertises.
- ⚠️ **The wide instrument has its own scope and must say so**, or it becomes the next narrow one.
  A device tree is what a platform ADVERTISES — not semantics, not memory attributes — and Sail's
  still lists a `timebase-frequency` and an `htif` node with no device behind them.
- The durable answer to "are there others?" is not "no". It is that a new one **cannot be added**
  without declaring what it does not establish — rule 5b, fired RED on the real dossier.
- Promotion is explicitly declined in the owning leaf, with the reason.

