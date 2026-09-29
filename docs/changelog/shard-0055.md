# DEV_NOTES shard — _(2026-09-28)_ … _(2026-09-27)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-09-28)_ — the canonical definition, generated (P1-LAB.6)

Root cause: the definition was checkable but not consumable — SEMANTICS proved 52/52 cited, but no executable artifact carried the facts and OWN-03's manifest existed nowhere. Implementation: `scripts/gen_definition.py` generates `crates/semulith-core/src/definition.rs` from the encoding composition plus the semantics data: `FIELDS` with scatters, 52 `INSNS` decode rows, `Sem` effect trees, `decode`, and `MANIFEST` (inputs+sha256, generator hash, configuration as data, upstream source pins); the generator re-derives the SEMANTICS checks it emits through and refuses unknown shapes by name. The 22nd doctrine `DEF-GEN` refuses drift; self-test 8/0, fired RED. Validation: 10 definition suites green; clippy clean; wasm green; gate green (22 doctrines / 245 arms). Kept: emit effect trees fully broken per line so generator shape and rustfmt's agree (drift compares content, never formatting); an unjudgeable input must refuse (rc=2), not report a verdict — the RED-firing rite caught `relative_to` crashing on a relative `--encoding`.

Lessons: declined (generation specifics).

## _(2026-09-27)_ — four typed outcome families, SEM-01 made structural (P1-LAB.5)

Root cause: SEM-01's separation lived only in `RULES.md`; the laboratory could report a contract violation (`.4`) but had no type for a trap, a stop, a gap, or a reserved word — and a single error enum is the classic way that distinction dies. Implementation: `semulith-core::outcome` — the four families as enums with named, source-linked variants, `StepOutcome` the step-level sum, and `From<env::ContractViolation> for ModelError` the one legal crossing (a harness violation IS a model error). No other `From` between families exists, on purpose. Validation: 5 suites green; clippy -D warnings clean; wasm green; gate green. Design notes, kept: (1) the acceptance's "delivered and execution continue" is a property of the HARNESS composition, so the test owns a stub stepper — production semantics stay with `.8`. (2) ExceptionCause carries no cause *numbers* — this profile models no privileged CSR to hold them, and inventing numbers would be a second fact.

Lessons: declined here (the family shapes are `.8`'s design consumer; nothing generalizes past this module).

