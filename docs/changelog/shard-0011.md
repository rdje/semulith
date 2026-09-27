# CHANGELOG shard — SEMULITH-MC-0038 … SEMULITH-MC-0038

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-MC-0038 (leaf MODEL-COMPOSE.1) — encoding composition is a verdict, not a hope

**What changed, and what it replaces.** I proposed tiering models into `exploratory` (ungated) and
`accepted` (gated) to buy breadth. That was rejected, and rightly: it buys breadth by creating a
second class of model nobody can trust. The correct lever is **composition** — every model stays
signoff-grade, and complexity is reached by *assembling proven small models*. Breadth by **reuse of
evidence**, never by absence of it. Recorded as
[`decision_composition-model`](docs/decisions/decision_composition-model.md).

**The design, grounded rather than invented.** Both pinned references already compose definitions
from fragments — `riscv-opcodes` ships **111** extension files, `sail-riscv` **34** extension
directories and **59** encoding files — and this project already carries the other half: an empty
`extensions = []` seam and **8 environment-assumptions** stating what something else must
guarantee. Two operators, one port mechanism:

- **intra-unit: union with conflict detection** — decidable, and therefore a verdict;
- **inter-unit: assumption/guarantee discharge** — `CPU_ENVIRONMENT` §5, made mechanical;
- **direction falls out of ports** — an unbound *slot* makes top-down composition checkable before
  its parts exist, and compositions nest, so `computer → board → soc → {cpu, device}` is one record
  shape at every level.

⭐ **Proven, not asserted.** The owned RV64I encodings composed with an `M` fragment they had never
seen: **52 + 8 + 5 = 65 instructions, no collision, no duplicate name.** Two instructions collide
exactly when `(value_a ^ value_b) & mask_a & mask_b == 0`, searched exhaustively — a sampled answer
would not be a decision.

**Fired RED on a genuine mistake, not a synthetic one:** composing the owned encodings with `rv_i`,
a fragment they already contain, produced **37 collisions** each named with its overlapping mask,
and `REJECTED`. A second refusal fired unplanned — an empty fragment file answered
`REFUSED … an empty fragment is not a valid one` rather than "no collisions" over nothing.

⛔ **What this does not claim.** There is **no RV64IM profile**: the `M` fragment is unpinned, no
semantics were composed, nothing was added to `rv64i-lab-v0`. The *decoder* composes. Whether the
*meanings* compose is not decidable in general — an extension can change a base instruction's
behaviour, and `MODEL-COMPOSE.6` treats a silent override as a defect rather than a composition.


