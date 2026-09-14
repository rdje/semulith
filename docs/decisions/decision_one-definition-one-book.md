# One canonical definition, one book, one materials bill — the unit that grows

- **Type:** `decision`
- **Date:** `2026-09-14`
- **Status:** `active`
- **Owner / source:** director instruction, `2026-09-14`; binds `MODEL-BOOKS`, `MODEL-METHOD`, and
  every modelled unit this project ever produces

## The decision

The north star is that Semulith models **as much as possible** — CPUs, MCUs, DSPs, devices, boards,
SoCs, eventually whole computers — and that it **starts small and grows**. The structural
consequence, decided here, is:

> **The unit of modelling is the unit of documentation.** Every canonical definition gets its own
> mdBook, its own materials bill, and its own coverage census. One definition, one book.

`docs/ARCHITECTURE.md` already names the unit — *"later devices and boards receive their own
canonical definitions"* — so this decision adopts existing vocabulary rather than inventing a
parallel one. What it adds is that a definition is not complete until the book that explains how it
was built from its sources exists alongside it.

## Kinds and layers

A unit carries a **kind** (what it is) and a **layer** (what it may own). The layer is the boundary
landed earlier: a processor does not own devices, and a board does not own instruction semantics.

| Kind | Layer | Owns | Does not own |
| --- | --- | --- | --- |
| `cpu`, `mcu`, `dsp` | `processor` | instruction semantics, architectural state, the CPU/environment **assumptions** | devices, interconnect, boot media |
| `device` | `board` | one device's register and behaviour contract | instruction semantics, other devices |
| `board`, `soc` | `board` | composition: memory map, wiring, which processor and device versions | the semantics of the parts it composes |
| `computer` | `system` | firmware, OS workload, storage and network composition | everything the board and processor own |

⭐ **The layer is what makes a coverage census honest.** An information-catalogue category the unit's
layer does not own is `deferred` — naming the layer that does — and never `missing`. `C19 Platform,
devices and interconnect` is `deferred-to-board` for a CPU and `covered` for a board; the same
category, the same catalogue, a different owner. Without the layer, every processor model would
report a deficiency for material it must never contain.

## What each book must do

Each book describes, for its unit, **how it went from PDFs, specifications and descriptions to a
fully functional model** — the whole arc, not the destination:

1. **The materials** — every document that specifies this unit, pinned by exact identity, with what
   it supplies and what it does **not**.
2. **The gaps** — what the materials do not contain, and where the missing information came from
   instead. This chapter is usually the most valuable and is usually the one omitted.
3. **The method** — document → decision → requirement → obligation → check, with the judgement
   calls named rather than absorbed.
4. **The model** — what was built, and what it is not.
5. **The evidence and the gate** — what has been demonstrated, what has not, and the verdict.

⚠️ A book is written for a model that is **not yet finished**, and says so. The first one will
describe a model whose gate reads `incomplete`; hiding that until the model is done would make the
book a retrospective rather than a method, and the method is the transferable part.

## Starting small, deliberately

Exactly **one** unit exists today: `rv64i-lab-v0`, kind `cpu`. Nothing is pre-built for units that
do not exist — no board directory, no device schema, no speculative chapters. What this decision
buys is that adding the second unit is cheap and gated rather than a redesign:

- a unit is registered in one place, with its kind, layer and book;
- a gate requires every registered unit to have a book and a materials census;
- the catalogue's category → material binding is per unit, so a board's census and a CPU's census
  are the same schema answered differently.

⛔ **Resist generalising further than two examples justify.** The kinds table above is a hypothesis
until a second unit exists to test it; `MCU` and `SoC` rows in particular have never been
exercised. The first board or DSP unit is expected to correct it, and that correction is normal
rather than a failure of this decision.

Related: [[decision_dual-mandate-production-and-teaching]], [[decision_reference-acquisition-route]].
