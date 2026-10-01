# CHANGELOG shard — SEMILITH-MB-0004 … SEMILITH-MB-0004

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMILITH-MB-0004 (leaf MODEL-BOOKS.2) — what the materials do not contain; the PDF investigation answers YES

- The per-unit book gains its gaps chapter (`docs/models/rv64i-lab-v0/src/gaps.md`):
  the measured no-encodings gap and what it forced (the RISCV-OPCODES second provenance,
  the parse-and-refuse assembler discipline), the gaps the specification is *supposed* to
  leave (the EEI policy choices; a platform), and the gap the references leave (agreement
  is not proof) — prose-first, per the teaching mandate.
- ⭐ The investigation, done with a tool: the pinned publication (docs.riscv.org,
  `v20260120`) publishes a PDF rendering at the same version segment
  (`_attachments/riscv-unprivileged.pdf` — HTTP 200, 4,580,174 B, sha256 `06bb3c23…`,
  696 pages, `Version 20260120: Official Release`). `pdftotext` measures its text layer
  carrying the instruction-format tables: **232** lines match the `[01]{7}` census pattern
  that returns **0** on all six pinned HTML/TXT artifacts; the base-formats figure and the
  RV32I opcode map extract with bit strings and field names. **Answer: yes — encodings
  can be re-sourced from the primary document**, so the encoding provenance's
  shared-ancestry exposure (shared with Spike, not Sail) is no longer forced.
  Qualifications recorded: the PDF numbers chapters differently from the pinned HTML
  (Introduction is Chapter 1 there; RV32I Chapter 2 / RV64I Chapter 4 vs §1.1 / §3.1), and
  the extraction is layout-fragmented — re-sourcing is engineering with its own
  verification, and is future reviewed work, NOT this leaf.
- The PDF is cached untracked at `target/materials/` and deliberately not catalogued
  (the corpus model has no network-origin kind — a MODEL-METHOD decision, recorded in the
  chapter). The cached GitHub-release PDF corroborates (269 census lines) — the finding
  depends on no one PDF.
- No gate surface changed (the chapter is authored prose; MATERIALS-BILL untouched, 26
  doctrines). `mdbook build docs/models/rv64i-lab-v0` and `make book` render; `make gate`
  all green.

