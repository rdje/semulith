# Re-sourcing the RV64I encodings from the primary document's PDF: adopt-in-principle (measured)

- **Type:** `decision`
- **Date:** `2026-09-30`
- **Status:** `active`
- **Owner / source:** `MODEL-METHOD.14` (the encoding re-sourcing evaluation, scheduled
  by the director's `2026-09-30` delegation). The encoding itself is owned by
  `MODEL-METHOD.8`; this record decides feasibility, not adoption timing.

## The fact / decision

**Adopt-in-principle, measured.** The pinned unprivileged specification's own PDF
(`RVI-UNPRIV-PDF-V20260120`, 696 pp, digest-pinned) carries the RV32I/RV64I encodings as
selectable text in Chapter 36's instruction listings, and a probe reconstructed them
end-to-end. The re-source — replacing the `riscv-opcodes` provenance of
`definitions/riscv/rv64i.sexp` with the primary document — is feasible and falsifiable.
It is **not performed here**: the re-source is its own reviewed leaf (`MODEL-METHOD.8`
owns the encoding), triggered when the encoding is next touched or a second unit reuses
the fragment — the moment the second provenance actually bites.

## Why (the probe's measurements)

- **One form end-to-end:** ADD reconstructs from the PDF text as opcode `0110011`,
  funct3 `000`, funct7 `0000000` — identical to the incumbent fragment's
  `(fixed (31 25 0x0) (14 12 0x0) (6 2 0xc) (1 0 0x3))`.
- **The full sweep, measured:** the naive in-order parser extracted all 52 opcodes with
  zero missing and **zero value conflicts**; 37/52 forms reconstructed fully. The 15
  remainders are parser-ordering gaps in the layout-fragmented fragment streams (one
  field per line), NOT document absences — each caught by the incumbent comparison,
  which is the verification control: a completed extraction that disagrees or omits
  fails loudly.
- **The recorded qualifications held:** the PDF numbers chapters differently from the
  pinned HTML (ch.2/ch.4 here, §1.1/§3.1 there, §2/§4 on GitHub — the `.16`
  measurement), so extraction keys on content, never on chapter numbers; and the
  fragmentation cost is measured at 29% of forms needing a page-local layout parser
  (hours, not days).
- **Why bother at all:** the incumbent provenance (`riscv-opcodes`) shares ancestry with
  spike, not sail (`references.sexp`'s encoding-subsystem independence row). Re-sourcing
  from the primary document shrinks that exposure: sail decoding our bytes is already an
  independent confirmation of the encoding; making the ENCODING DATA primary-derived
  removes the shared-with-spike leg.

## Commands and outputs (the leaf's standing record)

- `pdftotext .materials/riscv/riscv-unprivileged-v20260120.pdf target/mm14-unpriv.txt`
  → 39,808 lines; Chapter 36's listings begin at line 33,985; the RV32I base listing at
  line 34,108.
- `python3 target/materials/mm14_probe.py` (untracked scratch, `MODEL-METHOD.14`'s
  probe) → `opcodes extracted: 177 mnemonics; incumbent forms: 52` …
  `agree 37 / disagree 15 / not-extracted 0 of 52` — every one of the 15 an extraction
  gap (`f7=None`/`f3=None` where the incumbent carries a value), none a value conflict.

## Not decided here

Any change to encoding data (`MODEL-METHOD.14`'s explicit boundary). The re-source leaf,
when scheduled, must regenerate `definitions/riscv/rv64i.sexp` through the sanctioned
generator with the PDF parser as its input stage, keep `check_encoding_disjoint.py` and
the incumbent-comparison gate green, and restate the encoding provenance in the dossier
(`references.sexp`'s `encoding_source` record) and the materials bill.
