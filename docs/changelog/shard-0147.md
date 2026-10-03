# CHANGELOG shard — SEMULITH-BR-0015 … SEMULITH-BR-0014

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-BR-0015 (leaf P3-BREADTH.5) — the scope taxonomy generalizes; the DSP dossier drafted, attachment measured

- `schema/profile.sexp`: the DSP's five scope groups (moves/alu_core/multiplies/flow/loops)
  as named optional fields; `xlen`, the integer-file scalars and `count_rv64i_additions`
  optional — each naming dsp56300-lab-v0 as its case. No gate reader changed: they were
  already generic over group names. `dossier_sexp._SCOPE_LISTS` extended alongside (the
  two closed places the taxonomy lives).
- The DSP's `profile.sexp`/`state.sexp` stand DRAFTED and schema-validated under
  `docs/tasks/artifacts/p3-breadth/dsp56300-dossier/` — the 19-mnemonic subset scope, five
  register families with parts and readouts, three memory spaces, the hardware stack,
  twelve special registers, and the 14-candidate census carried as data; both load through
  the mapping owner and round-trip data-equal.
- The landing was MEASURED (untracked + intent-to-add placement, gates run in their
  committed modes): PROFILE-CONSISTENCY passes the DSP dossier — after the measurement
  surfaced seven latent `references.sexp` defects no gate had been checking, all fixed
  (an `obtained` candidate without binary/digest/injection; four independence pairs naming
  non-candidates — the asm/emu legs and gearmulator are now first-class candidates).
  EXERCISE-COVERAGE, EXTRACTION and INTERACTION-MATRIX go RED on a unit without
  `encoding.sexp`/`interactions.sexp`/per-step expectation guests — the landing slice owns
  them, so the documents wait under artifacts/.
- More latent defects owned and fixed (§15): EXERCISE-COVERAGE counted a `(comment …)`
  inside scope as mnemonics (skipped now, GREEN arm, 8/8); rv64's own `profile.sexp`
  carried two notes on D-FENCE against the schema's single-valued declaration (merged);
  `check_sexp_schema.py` tracebacks on a missing input (clean rc-2 refusal, RED arm,
  51/51). Surfaced and routed: no gate schema-validates the dossier documents as a class —
  the landing slice adds that leg.

## SEMULITH-BR-0014 (leaf P3-BREADTH.5) — the state schema learns the census's shapes

- `schema/state.sexp` declares `register_family` (with `parts` and per-part `readout`),
  `memory_spaces`, and `hardware_stack`; `xlen`/`integer_registers` become optional. Every
  construct names its exercising target and case: dsp56300-lab-v0, F1 masked widths, F3
  memory spaces, the census's special-register/stack candidates — the content source is
  the F6 census record.
- The mapping owner (`dossier_sexp`) now CARRIES the new forms end to end: pre-change it
  built the state doc from named fields only, so a declared `memory_spaces` would have
  been silently dropped between the schema and the generator (the `.2` silent-path class).
  `gen_state.py` refuses each declared construct by name (rc 2), and a missing `xlen` is
  a named Refusal instead of a KeyError traceback.
- Synth probe 2 did what the fixture exists to do: its pin went stale, the suite turned
  RED, and the pin moved one layer down — the schema now accepts `memory_spaces` (rc 0)
  while the generator refuses it by name (rc 2). Suite 6/6; STATE-GEN self-test grew four
  RED arms (10/10); the rv64 descriptor re-validates and regenerates byte-identical.
- The DSP's own `state.sexp` deliberately does NOT land yet: without `profile.sexp` no
  gate would read it (measured — PROFILE-CONSISTENCY iterates `profiles/*/profile.sexp`),
  so it lands with the scope-taxonomy slice where its gate attachment is measured.

