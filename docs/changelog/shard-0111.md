# CHANGELOG shard — SEMULITH-MM-0058 … SEMULITH-MM-0058

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-MM-0058 (leaf MODEL-METHOD.16) — the v20260120 PDFs: gap filed, answered same-day, adopted through the corpus seam

- The director asked for the v20260120 unprivileged PDF twice. Corpus sweep: absent (only
  the 20260911 intermediate). The verified bytes survived in scratch from `MODEL-BOOKS.2` —
  then chipdoc relayed that it now mirrors BOTH v20260120 PDFs
  (`risc-v/isa/reference/docs.riscv.org-v20260120/`, REQ-008), same bytes
  `06bb3c23…d150bc`, with a correction: the PDF does not share the pin's numbering.
- All four legs verified before any record changed: mirror present; byte-equality with the
  independent docs.riscv.org fetch (two acquisitions, one set of bytes); REQ-008 read in the
  ledger; the numbering re-measured from the extracted text layer — RV32I Chapter 2 / RV64I
  Chapter 4, NOT the pinned HTML's §1.1/§3.1. chipdoc's correction is correct.
- Both PDFs catalogued reference-only (`RVI-UNPRIV-PDF-V20260120` 696 pp,
  `RVI-PRIV-PDF-V20260120` 214 pp) with the trap documented, and fetched through the corpus
  seam, digests verified. The gap record was filed and resolved the same day; the corpus
  re-pinned `73711d6` → `f33d330` (5313 files / 257 PDFs); 45 materials. The `.14` probe
  input is now a first-class material, with three renderings and three numberings measured.
- Measured and surfaced for a chipdoc-side fix: its poller reads only TOP-LEVEL `(gap …)`
  forms, so it sees 0 of this catalogue's nested gaps (`semulith_gaps_open: 0` against the
  real catalogue; a scratch probe shows a flat gap is seen, a nested one is not). This
  request travelled operator-relayed.
- The tasks per-part ceiling fired twice mid-leaf (67,737 B, then 65,032 B growing) and was
  answered by the second and third archive movements — the ceiling obeyed, never raised.
- `make gate` all green. CHANGELOG.md crossed its ceiling with this entry and was sharded
  again by the DOC-SHARDING machinery.

