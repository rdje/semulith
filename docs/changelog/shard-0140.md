# CHANGELOG shard — SEMULITH-BR-0010 … SEMULITH-BR-0008

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-BR-0010 (leaf P3-BREADTH.4) — the dsp56300-lab-v0 dossier stands

- `profiles/dsp56300-lab-v0/`: `sources.sexp` pins DSP56300FM Rev. 5 at NXP's own locator —
  the fresh fetch returned byte-identical bytes to the chipdoc-cached copy (two acquisition
  routes, one artifact, verified); `references.sexp` records the `dsp56300` candidate
  (tarball pin, on-volume build note, the path-demonstration experiment, and the EVD-04
  independence rows: assembler and emulator share one project — the independent legs are
  upstream's asm56300 roundtrip and its silicon corpus; gearmulator not-examined);
  `DOSSIER.md` carries the deferrals by name (`profile.sexp`/`state.sexp`/`encoding.sexp` →
  `.5` named schema cases; requirements, unit registration, the per-unit book → the model
  slice).
- `scripts/fetch_references.sh` gained a GENERIC source-tarball leg (discriminator asset +
  source_commit + asset_sha256 — unreachable by the rv64 ledger, whose verify-only flow
  re-ran byte-behaviour-identical); `fetch_references.sh --verify-only dsp56300-lab-v0` →
  tarball MATCH.
- **The second-profile gate census (measured):** every auto-discovering gate keys on
  `profiles/*/profile.sexp` or `profiles/*/encoding.sexp`, so the deliberately partial
  dossier is invisible until those land — then the gates attach with NO gate edit.
  `make gate` green with the dossier present.

## SEMULITH-BR-0009 (leaf P3-BREADTH.4) — the bounded subset selected: `dsp56300-lab-v0` v0

- The reference's coverage censused on the pinned source (its decoder spans the full
  DSP56300 set) and its LIMITATIONS read in full — so the subset is bounded by honest
  implementability and the reference's own gaps, not by coverage. The comparison surface
  measured: checkpoint-level canonical end-state (registers, deviation-encoded X/Y windows,
  15 hardware stack slots; `steps` compared, `cyc` never) — a new comparator shape.
- **Subset v0:** non-parallel moves including the A2/B2 extension readout, the
  immediate/register data-ALU core, signed `mpy`/`mac`, `nop/jmp/jsr/rts`, `do`/`enddo`/`rep`,
  linear addressing only. Every exclusion named with its reason — parallel moves (the
  dual-feed axis) deferred as the first named extension candidate; interrupts, modes, stack
  extension and timing excluded on the reference's documented gaps.
- **Vehicle decided:** a new sibling crate `crates/semulith-dsp56300` (manual-derived,
  per-form-cited, EXPERIMENTAL); the generator/schema generalization stays `.5`'s work with
  this exercised target as its justification. Record:
  `docs/tasks/artifacts/p3-breadth/2026-10-01-subset-selection.md`; decision:
  `decision_dsp56300-lab-v0-subset`. Gaps surfaced and routed: the profile schema's scope
  taxonomy is scalar-named (→ `.5`); the auto-discovering gates' treatment of a second
  partial profile is the dossier slice's first measurement.

## SEMULITH-BR-0008 (leaf P3-BREADTH.3) — the evidence path exercised; `.3` done

- Reference pinned (commit `c60aeedb`, tarball sha256 recorded, `target/refs/` discipline)
  and release-built on-volume; a synthetic micro guest (24-bit immediates, mpy+mac into the
  56-bit accumulator, X/Y-space stores, a zero-overhead do loop) assembled (rc 0) and run
  headless — canonical-state dump, rc 0.
- Verified three independent ways: hand arithmetic reproduces A=001f253d515280 exactly;
  `--dump-mem` shows the X/Y stores landing right; the one surprise (`#$5` → `x1=050000`)
  traced to DSP56300FM §3.4.1.3. No Semulith DSP model exists — the claim is about the
  PATH. Artifact: `docs/tasks/artifacts/p3-breadth/2026-10-01-evidence-path-demo.md`.

