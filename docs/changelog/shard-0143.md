# CHANGELOG shard — SEMULITH-BR-0012 … SEMULITH-MM-0074

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-BR-0012 (leaf P3-BREADTH.4) — subset v0 form-complete; the 6-guest corpus AGREEs

- `crates/semulith-dsp56300` decode+exec gained the whole subset: the register/immediate
  data-ALU core (add/sub/cmp/and/or/eor, all three source shapes), ASR/LSR, JSR/RTS,
  ENDDO, REP #xxx/REP S, and the seven linear (Rn) addressing modes — every mask
  FM-cited (page-footer cites) and cross-checked against the pinned assembler's probe
  words, which the decode tests pin.
- Guests `alu`, `shift`, `rn`, `rep`, `jsr` join `micro`: **6 agree / 0 fail** over the
  canonical end-state dumps (51–64 fields per case, `cyc` excluded by rule); the crate's
  17 unit tests carry hand-derived end-states (EVD-05).
- The differential campaign caught five model defects, each root-caused tools-first:
  RTS pulls PC only (FM 13-168 — SR stays, pinned by the jsr guest); MOVE #xx to an
  accumulator sign-extends into A2 (the FM's "remaining bits zeroed" prose falsified);
  A1/B1 memory reads are RAW (the shifter/limiter sits on the whole-accumulator path
  only); S sets on accumulator bus reads, never on ALU results; and a keep-mask
  nibble-slip zeroed A2 on the 24-bit ops. Two boundary defects fixed on the spot:
  accumulator-part move destinations now refuse at decode (a latent panic), and the NOP
  citation corrected to 13-145 (the FM's §13 TOC numbers pages differently from the
  printed footers). `P3-BREADTH.4` DONE 4/4.

## SEMULITH-MM-0075 (leaf MODEL-METHOD.19) — the demand chapter is a live chapter

- Director ruling (`2026-10-01`): *The information a unit demands* is a WIP by design —
  a live chapter that is re-derived, not just re-read, as each new CPU/DSP/board is
  modelled: prospective sections become measured, classes split or merge with what is
  measured, and every claim keeps citing a measured instance. The chapter header now
  states that rule (no hand-kept date — LIVE-DOC-CURRENCY). `MODEL-METHOD` DONE 19/19.

## SEMULITH-MM-0074 (leaf MODEL-METHOD.18) — the information a unit demands, per kind

- New mdBook chapter, *The information a unit demands — CPU, DSP, board* (The models
  section): per unit kind, the precise set of load-bearing information a faithful model
  needs and what each absence prevents — on the spine "prevents-the-model vs
  prevents-the-claim" (plus the quieter third: prevents-the-bound, the census never
  taken). CPU: 9 measured classes; DSP: the CPU set plus 6, each earned by a measured
  bite (the `x1=050000` readout surprise, the `memory_spaces` refusal, the U-bit
  extraction inversion); board: 5 prospective classes, marked derived-not-measured.
  Every class maps to the information catalogue's categories without restating them.
- The chapter closes on the recursion the P3 design discussions predicted: CPU = base
  set, DSP = base + scalar-breaking axes, board = base + composition. Book builds;
  chapter count re-derived 31 → 32; `MODEL-METHOD` is DONE 18/18.

