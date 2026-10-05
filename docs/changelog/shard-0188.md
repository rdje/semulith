# DEV_NOTES shard — _(2026-10-03)_ … _(2026-10-03)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-03)_ — the flip measured four gate gaps; a generated module must be the formatter's fixed point (P4-SYSTEM.2 slice h, part 1)

Execution of the `.2` brief's checkpoint (h), part 1, measured:

- **Rehearse the flipped route before touching tracked files.** A copy of the staged
  unit with the route string flipped told the truth in advance: INTERACTION-MATRIX
  already green, EXTRACTION refusing on zicsr.sem.sexp's declared refinement points.
  The four gaps that followed were all of the same kind — a checker that had learned
  the one-unit world and had not been re-asked since: check_extraction's semantics
  leg didn't honor the `(refines …)` relation its own sibling gate owns;
  EXERCISE-COVERAGE's closure leg counted `(insn …)` children but not `(pseudo …)`
  (the seventh pseudo-census site — the family pattern, now with a registry of
  readers to census against); the three GEN gates judged one owner→mirror pair each;
  FACT-OWNERSHIP's same-unit census was pinned at four units. Each fix went to the
  owner with RED-first arms, never to a workaround.
- **A generated module must be the formatter's fixed point.** `cargo fmt --all` runs
  over `crates/` and STATE-GEN's `--check` compares the committed module against
  regeneration — so when fmt rewrote gen_state's rv64gc emission (a long inline csr
  reset array, one-line CsrMeta/FieldMeta rows, collapsed accessors) the gate
  reported DRIFT against a file nobody hand-edited. The rv64i branch already emitted
  rustfmt's own shape; the rv64gc branch now does too (verified: emission ==
  rustfmt(emission)). The rule: a generator targeting a tree the formatter owns
  must emit the formatter's fixed point, not approximately it.
- **The environment's contract had the profile baked in.** FlatMemory judged fetch
  alignment at 4 bytes — rv64i's IALIGN=32 wearing the contract's clothes. Under
  IALIGN=16 the rv64gc corpus fetches legally at 2 mod 4 (three base guests exist
  precisely to prove it). The fixture now carries the fetch alignment as profile
  data (`with_fetch_align`); `new` keeps the 4-byte default so every rv64i call
  site is byte-exact. Data-access alignment stayed the access width's own rule —
  the two alignments are different facts and the fixture now says so.
- **The trap-END discipline rode in as designed.** exec_rv64gc's `Frame.trapped`
  (a delivered trap ends the step's remaining effects) is the scratch runner's
  measured fix ported, not re-derived: the corpus proves it — the same 62 guests,
  the same per-step expectations, now through the tracked engine
  (`cargo test -p semulith-verify run_rv64gc`, 4/4 groups), with the
  reserved-decode conversion kept one layer up in the verify-side runner where
  the architecture says the policy lives.
- **Validation:** `make check` (76 core / 184 verify), `make gate` all green
  (DERIVED-COUNTS 408→419 re-derived), bench wasm + smoke-bench + both books
  green, fetch_references MATCH both profiles, the CLI smoke (rv64gc run/demo
  green, the named bench refusal, rv64i's trace byte-identical). The commit split
  is recorded: the flip stands alone; the Sail attempt is part 2. Promotion:
  declined — the pseudo-census class is already the family's running lesson
  (docs/knowledge), and the rustfmt-fixed-point rule is encoded in the gate
  itself (the census arms fire on drift).

