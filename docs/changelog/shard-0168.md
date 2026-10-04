# DEV_NOTES shard — _(2026-10-02)_ … _(2026-10-02)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-02)_ — the summary sentence is not the operation chapter: a declaration read from §1.10 failed §3.6's mode exclusivity (P5-BOARD.4)

The board's NIC declaration carried `access-widths 16 32` from the datasheet's §1.10
summary ("supports 32-bit and 16-bit bus transfers") — written at `.1`, inherited by the
dossier (the 16-bit pairing latch joined the model-state census *because the board
declared the width*). The composition verdict's strap decision forced the real question:
§3.6 makes the bus width a strap-selected, mode-exclusive property — 32-bit mode is "the
native environment … no special requirements", and the two-contiguous-access pairing is
16-bit-*mode* operation. With D32 strapped (the obvious choice for a 64-bit host), a
16-bit access has no datasheet-defined behaviour at all, so the declaration was measured
false and narrowed to 32 — and every downstream record justified by it (the census
latch) flipped with its reason stated. The instrument that caught it is the durable
part: the deferral was *data* (an obligation marked `composition_disposition
"required"`), so the verdict could not close without deciding the strap, and deciding
the strap forced re-reading the operation chapter. Decline-to-promote note: the finding
itself lives in the verdict + BOARD-VERDICT, and the measure-against-the-source
discipline already has its knowledge cards — no new card.

Also worth remembering: the per-assumption discharge is the obligation-graph half only —
its platform-dependent edges land on the *laboratory* guarantee (`OB-PLATFORM`), so a
green discharge would pass with a CLINT bolted on. The board-level satisfaction has to
be its own checked data (the `satisfies`/`answers` edges), which is why BOARD-VERDICT
has three legs instead of one.

