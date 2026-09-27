# CHANGELOG shard — SEMULITH-MM-0044 … SEMULITH-MM-0044

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-MM-0044 (leaf MODEL-METHOD.13) — the corpus moved, and my survey had sampled rather than swept

**What changed at the source.** The primary-source corpus advanced three commits (`4201f50` →
`3c45e81`) and closed **both gaps this project measured and reported**, three commits after
reporting them: five AMD64 APM volumes imported (`e401a56`), Intel SDM Volume 1 imported
(`98de100`). It also pinned the full `v20260120` docs.riscv.org snapshot and **moved** the RISC-V
PDF — which made a tracked record in this repository false:

```
$ python3 scripts/materials.py --fetch RVI-ISA-PDF-20260911
  REFUSED: not at $SEMULITH_CHIPDOC_ROOT/risc-v/isa/current/riscv-isa-manual_…pdf
```

**What changed in my method, which is the more useful half.** The first survey enumerated by
**guessing vendor directory names** from memory. Every probe returned relevant results, so nothing
signalled absence. Re-swept by path shape instead, eight documents had been missed — including the
**entire M68000 architecture** (filed under `nxp/m68k/`, because NXP inherited Motorola through
Freescale) and **every board-class document in the corpus**: three ESP32 SoC manuals and the
RP2040 and RP2350 datasheets, which is the whole material base for `P5-BOARD`.

⭐ The giveaway I ignored: my own probe named a `motorola/` directory that does not exist. A probe
naming something absent is a signal, and I read it as nothing.

The catalogue now carries a `derivation` field naming the sweep command, so the method can be
judged rather than believed. **22 → 36 materials**, 36 of 36 fetched and digest-verified.

**Both gaps closed with evidence, and kept.** A deleted gap erases the fact that the question was
ever asked, so each carries `(status resolved)`, what closed it, and — for AMD — a `(residual …)`
noting their doc hub is not scriptable, so a newer revision could exist uncaptured. A gap closed is
not a gap that cannot reopen.

⭐ **A material that is not one file.** The pinned snapshot is 72 HTML pages, and a snapshot
identified by the digest of one page is not identified at all. `kind snapshot` names a `manifest`
whose digest is the material's identity and whose entries verify every page — `72 manifest entries
verified` on fetch, and a tampered page inside a verifying snapshot is caught (new RED arm).

⭐ **That ends a real fragility.** The citation evidence lived only in an untracked working area
needing the network — the reason `check_citations.py` could not be a gate. It now runs from the
manifest-verified cache, **offline**, and prints which route it used:

```
via fetched working area target/sources/riscv-v20260120        -> 52 of 52 resolve
via materials cache .materials/riscv/pinned-v20260120/unpriv   -> 52 of 52 resolve
```

⭐ **Independent corroboration of the pin challenged last leaf.** chipdoc acquired the `v20260120`
snapshot by its own route; its digests for `intro`, `rv32` and `rv64` **equal** those committed in
`sources.toml`, and its manifest verifies 72 of 72. Two acquisitions, two parties, one set of bytes
— the one thing an agreement between us could not have produced.

⛔ **The reader refused this leaf's own first draft.** The catalogue generator emitted literal
`\uXXXX` escapes and `scripts/sexp.py` rejected the file by name — `unknown escape '\u'`. That is
`SOT-FORMAT.7`'s closed escape table doing its job one leaf later, on real content rather than a
fixture. The content was fixed; the reader was not touched.

Corpus drift is now **detected rather than discovered**: `--list` and `--verify` compare the
catalogued revision against the checkout's `HEAD`.

**Knowledge.** [`a-survey-that-found-things-can-still-have-missed-things`](docs/knowledge/a-survey-that-found-things-can-still-have-missed-things.md)
— a zero prompts "is my instrument blind?"; twenty-two results prompt nothing at all. Enumerate by
a property of the thing, never a list of names you wrote from memory, and read what your
enumeration excluded before you believe it.

