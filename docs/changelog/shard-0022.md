# CHANGELOG shard — _(2026-09-14)_ … _(2026-09-14)_

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-09-14)_ — derive the layout, and report the control that passed

- The B/J immediate scramble is **derived** from a pinned descriptor table, not typed. The
  derivation validates itself: the bits a descriptor accounts for must total its field width
  (7, 5, 20, 20) or the table is refused. A layout the assembler cannot reconcile is one it will
  not use — which is the same shape as the validator's refusal rule from the previous leaf.
- ⭐ **Negative observations earn their place.** `never_written` catches a jump that failed to
  skip, which a checker watching only the registers it expects to change cannot see. Fired RED by
  breaking the PROGRAM (jump to the next instruction), not the expectation.
- ⛔ **A control that passed is still a result.** `jalr +13` vs `+12` land identically *because*
  the low bit is cleared, so the landing address does not discriminate D-JALR-LSB. Both references
  clear the bit, so the failing branch was never observed. Recorded as a `limit` in the
  expectations file rather than letting a green result imply a discrimination it did not make.
  Owner of a real control: P1-LAB's mutation suite, which can mutate OUR model.
- Assembled instructions are not executed steps. Equal for straight-line code; wrong the moment a
  loop exists. The run bound now comes from the expectations file.
- Promotion is explicitly declined in the owning leaf, with the reason.

