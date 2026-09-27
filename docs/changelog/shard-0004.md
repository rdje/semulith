# CHANGELOG shard — SEMULITH-MM-0035: … SEMULITH-MM-0035:

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-MM-0035: the layer boundary — a UART is not CPU material

**What changed.** A scoping correction that arrived before it could do damage: devices belong to a
**board / SoC / ASIC** model, not to a processor model. This project pipecleans by modelling CPUs
and DSPs first, and the processor layer ends at the CPU/environment boundary — the CPU states what
it *assumes*, and a later board model states what it *guarantees*.

The project's contracts already own this line, so it is cited rather than restated:
`docs/INFORMATION_CATALOG.md` says *"C19–C21 are not all properties of the CPU itself"*, and
`docs/CPU_ENVIRONMENT.md` §5 is the board composition gate.

⭐ **The sharp consequence is for the materials catalogue, which is why this landed before its
schema was written.** A category the processor layer does not own is **not `missing`**. Marking
`C19 Platform, devices and interconnect` as missing for a CPU model would manufacture an
acquisition task for material the model must never contain, and would report a correct scope as a
deficiency. The disposition vocabulary now carries a **layer**, and `deferred-to-board` is a
first-class answer distinct from both `missing` and `not-applicable`.

⚠️ **It also corrects a framing from the previous leaf.** "Capable of running real code" needs a
console and a program-exit convention — and **those are board concerns**. What the *processor*
layer owes real code is narrower and wholly inside it: the psABI, the ELF contract, the
entry/startup state, and the compiler-runtime intrinsics a no-`M` soft-float target calls.

**`DIFF-PLATFORM-SPIKE` is reframed as a layer difference, not a configuration one.** Spike ships a
CPU *and a small board* — an interruptor, a PLIC and a UART — and does not separate them. What that
record measures is **how much board each reference drags in**, which is a more useful thing to know
than "the config would not take".

**Checked rather than assumed:** every device named anywhere in `rv64i-lab-v0` appears in exactly
one role — something a reference brings that the profile excludes. Word-boundary grep over the
profile's own files finds mentions only in notes explaining the exclusion; no decision, no
requirement and no obligation models a device. The earlier apparent hits in `sources.toml` and
`DOSSIER.md` were substrings of *implicit* and *explicit*.


