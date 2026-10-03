# CHANGELOG shard — SEMULITH-BR-0007 … SEMULITH-BR-0006

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-BR-0007 (leaf P3-BREADTH.3) — the oracle survey: DSP56300 chosen, evidence path first

- Per-family oracle census (QEMU/MAME/gem5/GDB-sim/binutils/LLVM/vendor tooling/dedicated
  projects, one URL per claim): **TI C6000 ABSENT** for execution (no open-source executor;
  the vendor simulator was discontinued in 2014 and survives only as legacy proprietary);
  **DSP56300 STRONG** (mborgerson/dsp56300: MIT assembler roundtripped against the vendor
  assembler + MIT Cranelift emulator silicon-validated with a canonical-state differential
  harness); **SHARC ADSP-2106x PARTIAL** (MAME's BSD-3 core is real and scriptable, but no
  vendorable assembler exists and there is no second oracle).
- Both load-bearing positives re-derived against primary sources (the MIT LICENSE, the
  README's silicon-difftest claim, MAME's sharc.cpp header and register export).
- **Slice decision: DSP56300** — the only complete, license-clean evidence path (RK08: the
  slice is chosen by demonstrable evidence, not manual convenience). A scalar-DSP slice
  activates F1/F3 (`.5`) and F6 (census), leaves F4/F5 unbuilt and F2 idle — recorded, not
  lost. Slice 2 demonstrates the path end-to-end before `.4` implements anything.

## SEMULITH-BR-0006 (leaf P3-BREADTH.2) — the hook census: no opaque hooks; the one silent extraction arm is now a generation-time refusal

- Full-pipeline audit against `docs/ARCHITECTURE.md` §2 ("an unsupported construct is a
  model-generation failure, not a guessed translation"): every generator and shared
  definition reader refuses by name with rc ≠ 0; the runtime dispatch is a closed `Sem`
  enum with no catch-all; no feature flags or callback tables exist. Three designed seams
  are typed contracts, not escape hatches: the `Environment` boundary trait, the mutation
  seam `step_over`, the bench `Observer`.
- Defect found, owned, fixed (§15): `exec.rs`'s operand extraction silently skipped an
  operand naming no field, under a comment whose premise `P2-SCALAR.1` had falsified
  (FENCE's `fm`/`pred`/`succ` have field ranges since). `gen_definition.py` now refuses
  it (rc 2, naming instruction and operand — with a new DEF-GEN self-test RED arm);
  the runtime arm is a loud `ModelError`; the test ratchet lost its dead whitelist;
  four stale justification sites swept; `gen_fragments.py`'s dead `_unused_build` removed.
- Verified: DEF-GEN ok (9 self-test arms + byte-compare); `make check` 180/180 + fmt +
  clippy; synth suite 5/5; fragment regeneration byte-identical. Lesson promoted to
  `docs/knowledge/a-dead-justification-camouflages-a-silent-path.md`.

