# CHANGELOG shard — SEMULITH-MM-0057 … SEMULITH-MM-0057

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-MM-0057 (leaf MODEL-METHOD.15) — the chipdoc feed arrives: the flagged set, catalogued and cached

- The director supplied the chipdoc corpus root and ordered a local cache so the path never
  has to be requested again. The feed's records arrive in this catalogue's own syntax, so
  adoption is copy-and-verify, not transcription: 7 proposals adopted (the `2026-09-27`
  flagged set minus the already-catalogued psABI) — `RISCV-ARCH-TEST-ACT4`, `RISCV-SBI-2.0`,
  `RISCV-BRS-1.0`, `DT-SPEC-0.4`, `UBOOT-2026.07`, `SIFIVE-FU540-C000`, `VIRTIO-1.2`. The
  catalogue reads 43 materials (was 36).
- Every digest verified AT FETCH, not trusted from the feed: 7/7 ok; both snapshots
  manifest-verified (ACT4 136/136 files, U-Boot 1219/1219). `materials.py --verify`:
  43/43 resolved, zero drift after the corpus re-pin `3c45e81` → `73711d6` (5309 files /
  255 PDFs re-derived by the same path sweep at the new pin).
- The channel itself is snapshotted git-ignored at `.semulith-data/chipdoc/` (the map, the
  feed, the requests ledger); the corpus path lives only in that untracked README —
  Policy 12: no tracked file names it.
- `P2-SCALAR.5` blocker (a) ANSWERED at the materials layer: the ACT4 docs + test plans are
  catalogued and cached; the generated 635 MB suite stays pinned by upstream commit
  `e2216915…` for resume day (the snapshot is partial by design). Blocker (b) — the C-guest
  routing decision plus the absent RISC-V C toolchain — stands.
- Measured absence: chipdoc's pinned v20260120 snapshot carries 72 HTML pages and no PDF —
  the `MODEL-METHOD.14` probe's PDF stays the `MODEL-METHOD.4` release-asset acquisition.
- `make gate` all green. CHANGELOG.md crossed its 64 KiB ceiling with this entry and was
  sharded by the DOC-SHARDING machinery, per its declared pressure control.

