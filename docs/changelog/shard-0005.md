# CHANGELOG shard — SEMULITH-MM-0036: … SEMULITH-MM-0036:

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-MM-0036: one canonical definition, one book — the unit that grows

**What changed.** The north star, stated and made structural: Semulith models **as much as
possible** — CPUs, MCUs, DSPs, devices, boards, SoCs, eventually whole computers — and **starts
small and grows**. The structural consequence:

> **The unit of modelling is the unit of documentation.** Every canonical definition gets its own
> mdBook, its own materials bill and its own coverage census, describing how it went **from PDFs,
> specifications and descriptions to a fully functional model**.

`docs/ARCHITECTURE.md` already named the unit — *"later devices and boards receive their own
canonical definitions"* — so this adopts existing vocabulary rather than inventing a parallel one.
What it adds is that a definition is not complete until the book explaining how it was built exists
beside it.

**Kind and layer decide what a unit may own.** A `cpu`/`mcu`/`dsp` owns instruction semantics and
its environment *assumptions*, never devices. A `device` owns one device's contract. A
`board`/`soc` owns composition, never the semantics of the parts it composes.

⭐ **The layer names the OWNER, not merely a deferral** — and that is what makes a coverage census
honest. `C19 Platform, devices and interconnect` is `deferred-to-board` for a CPU and `covered` for
a board: the same category, the same catalogue, a different unit answering it. It is also why the
catalogue is keyed on a **unit** rather than a processor profile — a board's census and a CPU's
census become the same schema answered differently, which is what makes the second unit cheap
instead of a redesign.

**Starting small, deliberately.** Exactly one unit exists: `rv64i-lab-v0`, kind `cpu`. Nothing is
pre-built for units that do not — no board directory, no device schema, no speculative chapters.
⛔ And the kinds table is a **hypothesis** until a second unit tests it; `MCU` and `SoC` in
particular have never been exercised, and the first board or DSP is expected to correct it. That
correction is normal, not a failure of the decision.

⚠️ A book is written for a model that is **not yet finished**, and says so. The first will describe
a model whose gate reads `incomplete` — hiding that until the model is done would make the book a
retrospective rather than a method, and the method is the transferable part.


