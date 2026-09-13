<!-- knowledge-map/subsystems.md — the ONE hand-curated input to the derived Knowledge Map.
     Edit this to give a fast orientation to the project's key subsystems / entry points.
     gen_knowledge_map.sh embeds this section verbatim; the task-tree and decision sections
     are generated automatically. -->

- `crates/app/` — the `semulith` binary crate. Still the scaffold's placeholder `main.rs`;
  the real crates (`semulith-core`, `semulith-verify`, `semulith-cli`) are a P1 deliverable
  specified in `docs/ARCHITECTURE.md` §4.
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
