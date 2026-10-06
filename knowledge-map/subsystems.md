<!-- knowledge-map/subsystems.md — the ONE hand-curated input to the derived Knowledge Map.
     Edit this to give a fast orientation to the project's key subsystems / entry points.
     gen_knowledge_map.sh embeds this section verbatim; the task-tree and decision sections
     are generated automatically. -->

- `crates/` — the Rust workspace (`docs/ARCHITECTURE.md` §4): `semulith-core` (generated
  state and definition modules, the rv64i and rv64gc interpreters, the privilege /
  translation / interrupt machinery, the environment contract), `semulith-verify` (the
  guest corpora as generated fixtures, the runners, replay / snapshot / reduce, the record
  graph and schema checks, bench, mutation, the wasm bench exports), `semulith-cli` (the
  `semulith` binary: run, replay, snapshot, resume, reduce, bundle, bench, demo,
  check-examples) and `semulith-dsp56300` (the DSP slice).
- `definitions/riscv/` — the canonical definition FRAGMENTS (`<ext>.sexp`, generated from
  the pinned riscv-opcodes tables) beside their hand-written, cited semantics
  (`<ext>.sem.sexp`); `profiles/<unit>/encoding.sexp` composes them.
- `profiles/` — one directory per modelled unit (`rv64i-lab-v0`, `rv64gc-lab-v0`,
  `dsp56300-lab-v0`, `sifive-uart-lab-v0`, `lan9118-lab-v0`, `netboard-lab-v0`): the
  dossier, pinned sources and references, state, requirements, obligations, guests with
  their specification-derived expectations, the interaction matrix.
- `schema/` + `materials/` — the S-expression schemas every source of truth validates
  against; the materials catalogue (the pinned primary sources, the unit registry, the
  per-category needs).
- `docs/book/` + `docs/models/` — the project mdBook (the reviewable narrative) and one
  mdBook per registered unit.
- `ROADMAP.md` + `RULES.md` — the plan and the normative engineering rules with stable IDs
  (`SCP-`, `OWN-`, `SEM-`, `ENV-`, `EVD-`, `RUST-`, `AI-`, `SRC-`). Rule IDs are cited by
  task leaves and evidence records, so they are the project's stable vocabulary.
- `docs/` — the design contracts: `ARCHITECTURE.md` (canonical definitions and generation
  boundaries), `CPU_ENVIRONMENT.md` (the CPU/environment contract), `EVIDENCE_AND_GATES.md`
  (schemas, traceability, the processor release gate), `ARCHOGEN_INTEGRATION.md` (the eADL /
  engine / Semulith ownership boundary), `INFORMATION_CATALOG.md` (the 24-category
  collection checklist), plus risks, glossary, sources, and review disposition.
- `schemas/` + `examples/` — the starter data contracts (`requirement`, `evidence`,
  `contract-obligation`) and a deliberately synthetic 16-bit fixture whose evidence records
  are all `planned`. Not a CPU, not a checker.
- `docs/provenance/` — frozen delivery records for supplied inputs. Never maintained against
  the live tree; see each directory's `DELIVERY.md` for its row dispositions.
- `docs/knowledge/` — the retrievable lesson layer: one card per question a future reader
  would actually ask. `LESSON-PROMOTION` routes dated `DEV_NOTES.md` entries here.
- `scripts/` — the doctrine enforcer and its checks; `scripts/check_doctrines.project.sh` is
  this project's own slot.
