# CHANGELOG shard — SEMULITH-MM-0042 … SEMULITH-MM-0042

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-MM-0042 (leaf MODEL-METHOD.11) — materials get an identity, and no path that breaks on a move

**What changed.** A curated corpus of vendor ISA and architecture manuals became available —
3,684 files, 1.5 GB, 196 PDFs across 23 vendors, curated in its own words *"to build software
emulators (ISS) that run real C/C++/Rust software"*. This repository had no form in which to say
that a material exists and where a copy of it is (`git ls-files | grep -ci materials` → 0).

The obvious route is the wrong one. The corpus lives **outside** the repository, so writing its
path into a tracked file plants an absolute path — which Policy 12 forbids, because the repository
must survive being moved to another filesystem. And it fails *quietly*: after a move the path stops
existing and every tool reports "not found" about a document sitting right there.

**The shape that solves it.** Paths compose from two roots, and the catalogue knows only one:

```
cache      <repo root>/<cache-root>/<cache-path>    both halves tracked and relative
corpus     $<env-var>/<corpus-path>                 the left half NEVER tracked
```

The environment variable is the seam. The operator sets it once; git never sees it. Measured on
the tracked tree, with a control proving the probe can see such a path:

```
$ git grep -c -I --cached -e 'livework' -- .    ->  0 tracked files name the corpus root
```

**What is catalogued.** 22 materials — RISC-V (unified ISA + ELF psABI), Arm (A-profile,
Armv7-A/R, Armv8-M, Armv7-M, Armv6-M), Intel SDM Volumes 2-4, Power ISA 3.1C, SPARC 2015,
OpenRISC 1000, six TI DSP CPU guides, MSP430, Z80, W65C02S — each with revision, page count,
sha256, licence and what it supplies. All 22 fetched and digest-verified into the gitignored
`.materials/` (233 MB, same volume as the repository). The repository catalogues identity and
redistributes nothing.

⭐ **Two measured gaps, recorded as first-class `(gap …)` records rather than remembered:**

- **No AMD instruction-set manual.** `amd/` holds exactly one document, an IOMMU specification. An
  x86-64 unit built from this corpus would rest on Intel's description of the architecture alone.
- **No Intel SDM Volume 1.** Volumes 2, 3 and 4 are present; Volume 1 — Basic Architecture, the
  execution environment, data types and register overview — is absent. An x86 unit could not state
  its architectural **state** from this corpus.

⭐ **And the RISC-V PDF is not our RISC-V.** It is `20260911: Intermediate Release`; the profile
pins `v20260120`. It also numbers RV32I §2.1 and RV64I §2.2, where the pinned HTML numbers them
§1.1 and §3.1 — so **not one of our 52 semantic citations resolves in it**. Catalogued
`reference-only`, never as the authority a requirement cites. Its licence, read from the document,
is **CC-BY-4.0**, which bears directly on `OQ-4` and rule `SRC-01`.

⭐ **Scale, as an argument rather than an opinion.** The Arm A-profile manual is **17,145 pages and
126 MB** — eighteen times the RISC-V manual. Beside it sit Armv6-M at 374 pages and the W65C02S
datasheet at 32, both complete architectures. That spread is `start small and grow` stated in page
counts.

**Housekeeping in lockstep.** `materials/` registered in `doctrine/readme_routes.tsv` in the commit
that creates it, ceilings derived from its own measured size. `CHANGELOG.md` had 1,326 B of
headroom against its 64 KiB ceiling and was sharded first: 64,210 → 28,188 B, 11 entries moved to
`docs/changelog/2026-09-p0-to-mirror.md`.

