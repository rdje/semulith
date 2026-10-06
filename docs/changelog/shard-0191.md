# CHANGELOG shard — SEMULITH-P4-0012 … SEMULITH-P4-0011

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P4-0012 (leaf P4-SYSTEM.2, slice h part 1) — THE ATOMIC FLIP: the payload tracked, the route generated-definition, the corpus on the tracked engine

- The proven staging moves into `profiles/rv64gc-lab-v0/` byte-exact: the 33-CSR state
  document, the encoding composition (base + Zicsr + Zicntr + the privileged-system
  fragment, `(status partial)` with six declared slots for M/A/F/D/C/Zifencei), the
  62-guest corpus with run-order, and the 7-axis × 28-cell interaction matrix. The
  vehicle route flips to `generated-definition`; D-RESOLUTION-ROUTE is superseded by
  note (the D-FENCE convention — its statement stays verbatim because RECORD-SCHEMA
  mirrors it) and D-ROUTE-FLIP records the flip, its REQ/OB pair in the
  authored-records shape.
- The generated mirrors land tracked because their canonical inputs land tracked in the
  same commit (decision_generated-mirror-needs-tracked-input):
  `crates/semulith-core/src/state_rv64gc.rs` + `definition_rv64gc.rs`,
  `crates/semulith-verify/src/guests_rv64gc.rs` — content-hash-identical to the
  scratch-proven modules, provenance lines tracked-honest.
- The tracked engine runs the corpus 62/62: `exec_rv64gc` ports the evaluator with the
  trap-END discipline ridden in from the scratch runner (a delivered trap ends the
  step's remaining effects), delivery through the tracked `privilege` machinery,
  reserved decode reported for the diagnostic policy one layer up;
  `semulith-verify`'s `run_rv64gc` drives all 62 guests with the base differential's
  assertion family (per-step writes exact, never_written, one fetch per step,
  cold-reset determinism) — 4/4 test groups green. FlatMemory carries IALIGN as
  profile data (`with_fetch_align`; the rv64i default byte-exact).
- The CLI's profile becomes a runtime selection: `--profile=` on run and demo
  (rv64gc through the privileged engine), named refusals from the rv64i-scoped
  commands (bench, bundle, reduce, replay, snapshot, resume, mutations), rv64i the
  byte-exact default.
- Four gate gaps the flip measured, each fixed at its owner with RED-first arms:
  check_extraction honors MODEL-COMPOSE.6's refinement relation (self-test 11→13);
  EXERCISE-COVERAGE's SCP-02 closure leg counts the composition's pseudo children
  (21→23); the three GEN gates judge owner→mirror PAIRS (STATE-GEN 20→22, DEF-GEN
  15→17, GUEST-GEN 10→15 — the rv64gc pair each, plus the base-mirror governor: 93
  files byte-identical + 5 recorded re-derivations); FACT-OWNERSHIP re-pins to 5
  units / 74 fact kinds. The CSR name↔address ownership migrated to the state
  document (the assembler reads it; csrs.csv stays the derivation source, 33/33;
  `pmpaddr0` refused by name). gen_state's rv64gc emission is rustfmt-stable
  (cargo fmt runs over crates/; STATE-GEN compares against regeneration).
- Full local proof: `make check` (76 core / 184 verify), `make gate` all doctrines
  green (DERIVED-COUNTS 408→419 re-derived, never hand-incremented), bench wasm
  133,662 bytes, smoke-bench 53 arms, both books build, fetch_references MATCH for
  both profiles, and every rv64i verdict unchanged (52/52 exercised; its generated
  surfaces byte-identical but definition.rs's embedded generator fingerprint).
  The split is recorded: the flip is its own commit; the Sail privileged
  matched-experiment attempt lands as part 2.

## SEMULITH-P4-0011 (leaf P4-SYSTEM.2, slice g) — the interactions.sexp: 7 axes × 28 cells, rehearsed green against the staged unit

- The unit's interaction matrix, authored at scratch staging (route-contradicted until
  the flip): seven axes from the leaf's own vocabulary — fault, alias, boundary and
  progress carried from the mirrored base layers; **legality** (mode-dependent
  permission and refusal: M/S/U, TW/TVM/TSR, read-only/WARL, encoding validity) and
  **delegation** (interception routing: medeleg, the counter enables, STCE) added by the
  privileged machinery; **restart reframed guest-shaped** — rv64i's mechanism-shaped
  restart becomes the xret/xepc return discipline (the mechanism registry is closed and
  no rv64gc mechanism exists; mret/sret make restart observable by guests); rv64i's
  event axis absorbed into the mode-cause and delegation story.
- 28 cells, all dispositioned: every one of the 62 staged guests maps onto ≥1 cell (no
  new guests needed — the base mirror keeps rv64i's layer mapping, the mm guests land on
  their machinery's cells), and three cells (alias×restart, boundary×delegation,
  boundary×restart) are reported degenerate-with-reason — the doctrine's sanctioned
  shape for a cell the corpus honestly does not compose.
- The DIFFS rule forced the mirror's fourth and fifth re-derivations: it-fencei and
  min-fencei carried rv64i's `expect_divergence` pin (DIFF-FENCEI-EXECUTED), whose
  record is false for this unit — rv64gc DECLARES Zifencei and the staged encoding
  leaves the slot unbound. The divergence forms were dropped with the reason recorded in
  each file's comment; steps/writes/never_written unchanged; the corpus re-proven
  `62 guest(s) PASS, 0 FAIL`. The mirror now reads 49 `.s` byte-identical, 44
  expectations byte-identical, 5 re-derived (3 IALIGN-16 + 2 fencei-slot).
- The rehearsal ran the check's own invocation against the staged unit
  (`scripts/check_interaction_matrix.py <unit-dir>` — the `.sh` driver discovers tracked
  `profiles/*/` at the flip): 28 cells declared, every disposition resolves, rc=0. The
  RED legs fired by name against a scratch copy: DIFFS on the pre-re-derivation fencei
  files (NO REFERENCES + UNKNOWN DIFFERENCE), ORPHAN GUEST on a dropped name, OMITTED
  CELL on a deleted cell. Driver self-test 15/15; tracked units untouched
  (`INTERACTION-MATRIX: ok (5 unit(s))`); `make gate` green (DERIVED-COUNTS unchanged at
  408 — no arms this slice). Next: slice (h) — the atomic flip.

