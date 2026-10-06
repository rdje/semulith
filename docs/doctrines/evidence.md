# Project doctrines — evidence

Execution evidence — coverage, the interaction matrix, the gate report, portability. Part of
the partitioned project-doctrine registry: the bounded index is `DOCTRINE_ENFORCEMENT.md`
("This project's own doctrines"), the registry of record is
`scripts/check_doctrines.project.sh`, and REGISTRY-MIRROR judges this family's union with its
siblings as a mirror (`LIVE-CONTAINMENT.3`).

## This project's own doctrines — evidence

| ID | Proves | Check |
| --- | --- | --- |
| `GATE-REPORT` | every tracked `G?-REPORT.md` (G0 today, G1 since `P1-LAB.12`) is byte-identical to what `scripts/gate_report.py --gate <G>` derives from its inputs — the profile, the requirements, the obligations, the reference dossier, the guest expectations and the recorded baseline, **all tracked**, so it regenerates in a fresh clone with no reference binaries present. ⭐ What it protects is the **verdict**, not tidiness: the generator has no code path to `passed` while declared checks exceed implemented ones (G0) or any of the six `G1` criteria stands unmet, and this is what stops someone reaching that word with an editor instead. `EVD-08` names *passed with a missing required check* as the outcome a report must never produce. ⚠️ Honest limit: it proves the report is in sync with its inputs, never that those inputs are true — they have their own gate and their own limits | `scripts/check_gate_report.sh` |
| `PORT-WEB` | the crate skeleton builds for the browser target (`decision_browser-wasm-target`): the workspace compiles for `wasm32-unknown-unknown` on every commit, so a host-only API cannot slip into the engine unnoticed — the build itself is the proof that no unconditional host-only capability exists. Fired RED against the real workspace (a unix-only import in `semulith-core`) before registration; refuses with install instructions when the rustup target is absent, and its self-test builds scratch crates asserting both verdict and reason | `scripts/check_wasm_build.sh` |
| `EXERCISE-COVERAGE` | every declared scope form is EXECUTED by a tracked guest — an unexercised form is named with the denominator re-derived; the `SCP-02` closure resolves through the ONE resolver; `EXTRACTION`'s dynamic half (`P2-SCALAR.1`) | `scripts/check_exercise_coverage.sh` |
| `INTERACTION-MATRIX` | the declared fault × alias × boundary × event × progress × restart matrix is declared first as tracked data and then exercised: the cells are re-derived from the declared axes (an omitted cell fails, named), every disposition resolves (a guest names tracked source AND expectations; a mechanism names the closed registry — the smoke reproduce leg, the offline determinism suite — and its artifact still carries its needle; a degenerate cell carries its reason and nothing else), no tracked guest is an orphan, and every difference id named exists in `references.sexp` (`P2-SCALAR.4`; fired RED against the real corpus before registration) | `scripts/check_interaction_matrix.sh` |
