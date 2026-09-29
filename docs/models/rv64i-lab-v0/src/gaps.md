# What the materials do not contain

This is the chapter a materials bill usually omits — and the one a reader building their own
model needs most. The bill (`materials.md`) lists what the project *has*; this chapter lists
what those materials *do not contain*, and what each gap **forced** the project to build or
decide. A gap you never state is a gap your model silently fills with assumption.

Four gaps, in the order they bit.

## The gap that shaped the whole pipeline: no encodings

The pinned specification artifacts contain the complete *semantics* of RV64I in prose — and
**no instruction encodings at all**. This was measured, not noticed in passing: the format
diagrams in the specification are images, and a census over all six pinned artifacts (the
three HTML pages and their three text renderings) finds zero lines carrying a seven-bit
opcode pattern:

```
$ grep -cE '[01]{7}' target/sources/riscv-v20260120/{intro,rv32,rv64}.{html,txt}
…/intro.html:0
…/intro.txt:0
…/rv32.html:0
…/rv32.txt:0
…/rv64.html:0
…/rv64.txt:0
```

**What the gap forced.** The encodings had to come from somewhere else, and that somewhere
became a *second provenance*, recorded as such rather than blurred into "the
specification": the pinned `riscv-opcodes` tables (`RISCV-OPCODES` in the bill), upstream
of Spike but not of Sail — so Sail decoding the project's bytes is the independent
confirmation, and Spike's agreement is the same table answering twice. The gap also forced
the discipline that keeps a foreign table safe: the assembler *parses* the pinned tables
and **refuses** what it cannot reconcile — the B/J immediate layouts are accepted only if
their accounted bits total the field width, the operand positions come from the pinned
`arg_lut.csv`, and the composed encoding space passes a disjointness check before any word
is trusted. (The project book's assembler annex, `docs/book/src/annex/assembler.md`, walks
this machinery end to end.)

## The investigation this leaf ran: does the PDF rendering carry the tables?

The specification is also published as a PDF. If *that* rendering carries the
instruction-format tables as selectable text, the encodings could be re-sourced from the
primary document, and the second provenance's shared-ancestry problem would shrink. This
was an open question until today — answered with a tool, not by assumption.

**First, which PDF.** The pin is a *publication plus a revision* — the RISC-V Ratified
Specifications Library at docs.riscv.org, version segment `v20260120` (a version string
without its publication is not an identity; see
`docs/knowledge/a-version-string-is-not-an-identity.md`). The pinned publication does
publish a PDF rendering **at the same version segment**: the pinned `rv64.html` page links
`../_attachments/riscv-unprivileged.pdf`. That is the artifact investigated — not the
GitHub release PDF (a different publication *and* a different revision, catalogued as
`RVI-ISA-PDF-20260911`, `status reference-only`; it answers below as corroboration, never
as the subject).

**The fetch** (to the gitignored, on-volume cache — the repository does not redistribute
third-party documents):

```
$ curl -sS -o target/materials/riscv-unprivileged-v20260120.pdf -w '%{http_code} %{size_download}\n' \
    https://docs.riscv.org/reference/isa/v20260120/_attachments/riscv-unprivileged.pdf
200 4580174
$ shasum -a 256 target/materials/riscv-unprivileged-v20260120.pdf
06bb3c23074f72060a0ec061a80933af948cae7ceafdcd9d1fe177b05fd150bc
$ file target/materials/riscv-unprivileged-v20260120.pdf
PDF document, version 1.4, 696 pages
```

**The examination** (`pdftotext` 4.06), measuring the PDF's text layer with exactly the
census pattern that returns zero on the pinned HTML:

```
$ pdftotext target/materials/riscv-unprivileged-v20260120.pdf target/materials/riscv-unprivileged-v20260120.txt
$ grep -cE '[01]{7}' target/materials/riscv-unprivileged-v20260120.txt
232
$ grep -n 'imm\[31:12\]' target/materials/riscv-unprivileged-v20260120.txt | head -3
1047:imm[31:12]
1178:imm[31:12]
1439:imm[31:12]
```

The text layer carries the format figures verbatim: the base-formats figure extracts as
`imm[31:12]` / `rd` / `opcode` / `U-Type` with its caption, and the RV32I opcode map
("Table 13. RV32I Base Integer Instruction Set") extracts with the full opcode bit strings
and the mnemonic row aligned beneath them. The document self-identifies as
`Version 20260120: Official Release` — the same revision as the pin.

**The answer: yes.** The pinned publication's PDF rendering carries the
instruction-format tables as selectable text — 232 lines match the bit-pattern census that
returns zero on every pinned HTML artifact. The corroborating check on the already-cached
GitHub-release PDF (`RVI-ISA-PDF-20260911`, different publication, different revision)
extracts format tables too; the finding does not depend on which official PDF is asked.

**The consequence, stated precisely.** Encodings *can* be re-sourced from the primary
document — same publication, same revision — so the second provenance's shared-ancestry
exposure (a Spike that shares `riscv-opcodes` ancestry) is no longer forced; a future leaf
can regenerate the encoding fragments from the PDF and leave `riscv-opcodes` as the
*cross-check*. Two qualifications travel with the finding:

1. **The PDF numbers its chapters differently from the pinned HTML.** In the PDF the
   Introduction is Chapter 1, so RV32I is Chapter 2 and RV64I Chapter 4 — while the pinned
   HTML numbers them §1.1 and §3.1, which is what all 52 semantic citations use. Same
   publication, same revision, *different numbering within the same publication's two
   renderings*. Re-sourcing changes no citation's meaning, but every locator needs its
   mapping recorded — this is the version-string lesson one level down: even
   publication-plus-revision does not pin a *rendering's* numbering.
2. **The extraction is layout-fragmented.** `pdftotext` emits the format figures as one
   field per line (a bit range, then `rs1`, then `funct3`, …), not as rows. The tables are
   *selectable*, not *machine-ready*: re-sourcing is an engineering task with its own
   verification (the assembled bytes must still decode identically on both references), not
   a copy-paste.

⛔ **The re-sourcing itself is not this leaf.** This leaf records the finding and its
evidence; changing where encodings come from is its own reviewed work (the catalogued
reconciliation note names `MODEL-METHOD.3` for the publication reconciliation).

**Provenance standing of the PDF.** The fetched PDF is cached untracked at
`target/materials/` (the repository volume, gitignored — the same standing as the
`target/sources/` and `target/refs/` working areas), and its identity (URL, revision,
HTTP status, byte count, digest) is recorded above and in this leaf's verification log.
It is deliberately **not** added to `materials/catalog.sexp`: the catalogue's corpus model
is corpus-root-based (`$SEMULITH_CHIPDOC_ROOT`), with no network-origin corpus kind, and
adding one is a `MODEL-METHOD` decision, not this leaf's. If the re-sourcing leaf lands,
the PDF becomes a *source the model is derived from* and gains its catalogue record then,
with the corpus question answered properly.

## The gaps the specification is *supposed* to leave

Two more gaps are not defects in the materials but deliberate absences — the specification
leaves them to the environment, and the project's internal contracts are what fill them:

- **The laboratory's policy choices.** The base ISA leaves misaligned-access handling,
  reserved-encoding behavior, and code visibility after a store to the EEI
  (`RVI-INTRO` supplies the vocabulary, not the choice). The profile's decisions —
  `D-MISALIGN-DATA`, `D-RESERVED-DECODE`, `D-CODE-VISIBILITY` — are *laboratory* authority,
  stated in `profile.sexp` with that authority label so a reference model that chose
  differently is recorded as a profile difference, never misfiled as a defect. The
  inverted FENCE defect (the dossier demanded a trap the specification *forbids*) is the
  standing lesson, kept in the record on purpose.
- **A platform.** The specification defines no memory map and no devices. The environment
  contract (`contract-obligations.sexp`) declares what the laboratory owes, and the
  matched-profile override is what makes a reference model's platform comparable — the
  advancing-`mtime` probe (`DIFF-PLATFORM-DEFAULT`) measured what "matched on the ISA
  string but not the platform" costs, and the fix is why `guest-no-device` exists.

## The gap the references leave

And one gap belongs to the bill's *reference* materials: agreement is not proof. The
references supply behavior to compare against, not correctness — two models sharing
semantic ancestry can agree while both are wrong, which is why the dossier carries the
independence inventory and why `act4` (Sail-derived expected results) can never be a
second opinion. The evidence chapter (`.5`) picks up what agreement *is* worth; the gap it
must start from is recorded here: no material on the bill, external or internal, supplies
certainty.
