# The reference and what agreement is worth

## What the reference is

`mborgerson/dsp56300` at commit `c60aeedb` — MIT-licensed, obtained as a pinned
tarball, built on-volume into `difftest` (the executor) and `dsp56300-asm` (the
assembler). Its own validation story is unusually strong for a hobby-class emulator:
the authors run a difftest harness whose corpus programs execute on the emulator **and
on real MCPX silicon**, comparing canonical state word for word, and its assembler
roundtrips exhaustively against Motorola's official `asm56300` v6.3.15 across the full
encoding space. Its `LIMITATIONS.md` is equally unusual: a plain list of what it does
not model, which this unit's exclusions map onto one-to-one.

## What agreement with it is worth — and what it is not

Agreement is **tested evidence for these inputs on this surface** (EVD-01), full stop.
Three recorded facts bound its worth, and the dossier carries all three rather than
letting "silicon-validated" do untracked work:

- **One candidate is not one opinion.** The assembler and the emulator are one
  repository, one author, one crate workspace — the independence inventory records the
  shared lineage. The genuinely independent legs are *upstream's* proof artifacts (the
  asm56300 roundtrip; the silicon-sealed corpus), which Semulith has not re-run
  (EVD-04): the silicon needs hardware this project does not have, and
  `asm56300`/`sim56300` are proprietary and unpinnable. What the differential here
  adds is a genuinely independent *third* construction: Semulith's model is derived
  from the family manual, not from the emulator's tables — so where the two agree,
  two independently sourced readings of the same manual agree.
- **The silicon leg is upstream's word.** Trustworthy, recorded, and not re-derived
  here. The claim therefore never reads "silicon-validated model" — it reads
  "agreement with a reference whose authors silicon-validated it, on a synthetic
  corpus, over canonical end state".
- **The second implementation is unexamined.** gearmulator exists, runs real
  commercial firmware, and is GPL-3.0 — not vendorable under this project's pinning
  discipline, its source unread, the independence pair recorded `not-examined`. An
  omitted pair would read exactly like an independent one; that is why it is on the
  bill at all.

## The comparison contract

Per CASE, end-state canonical dump equality: `pc sr omr la lc sp ssh ssl ep sz sc vba`,
`x0 x1 y0 y1`, `a0 a1 a2 b0 b1 b2`, `r0–r7 n0–n7 m0–m7`, deviation-encoded X/Y/P memory
windows (the harness window excluded by the harness's own contract), and 15 hardware
stack slots — steps compared, `cyc` never (timing is informational upstream). The
surface is engine-agnostic by the reference's own contract: anything that can produce
the canonical dump format can be compared. The full contract lives in
`references.sexp`'s `trace_granularity`, and the comparator
(`scripts/compare_dumps.py`) skips `cyc` by recorded rule.

## The documented gaps, restated as claim bounds

The reference's LIMITATIONS — SA/SC/DM mode bits stored but inert, stack extension
unimplemented, cache operations NOPs, pipeline interlocks unmodelled,
peripheral-interrupt and fast-vector shapes unverified against hardware — are not
footnotes. They are the axes on which no claim can ever rest *through this reference*,
which is why subset v0's exclusions map onto them exactly: a subset that claimed an
axis its only oracle cannot evidence would be an overclaim by construction.
