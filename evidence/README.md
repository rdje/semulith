# Retained finite evidence

This bounded index owns the evidence family: one directory per reviewed finite case of
`profiles/rv64gc-lab-v0`, each declared by its `case.sexp` and holding the same 22 slots. The
[model book](../docs/models/rv64gc-lab-v0/src/prepared-inputs.md) explains the prepared identities;
the [canonical captures](../docs/models/rv64gc-lab-v0/src/canonical-division.md) record the
observations. Nothing here closes the M obligation or the CPU gate.

## Cases (this table is the complete membership)

| Case directory | State | Files | Holds |
| --- | --- | --- | --- |
| `rv64gc-signed-div-truncation-v2/` | `invalidated` 2026-10-22 | 22 of 22 | `m-div.s`, 27 boundaries, 1 property |
| `rv64gc-m-forms-v3/` | `invalidated` 2026-10-29 | 22 of 22 | `m-forms.s`, 33 boundaries, 25 properties |
| `rv64gc-m-forms-v4/` | `invalidated` 2026-11-02 | 22 of 22 | v3's program and prepared bytes; identical traces |
| `rv64gc-xlen-forms-v1/` | the first non-M case (REQ-D-XLEN); `invalidated` 2026-11-02 | 22 of 22 | `xlen-forms.s`, 25 boundaries, 17 properties |
| `rv64gc-m-forms-v5/` | captured 2026-11-02, credited `CR-GC-M-3` | 22 of 22 | v4's bytes, its control declared; identical traces |
| `rv64gc-xlen-forms-v2/` | captured 2026-11-02, credited `CR-D-XLEN-2` | 22 of 22 | xlen-v1's bytes, its control declared; identical traces |
| `rv64gc-csr-set-v1/` | declared 2026-11-03 (a43b-3e); its own reference configuration | 8 of 22 | `csr-set.s`, 157 boundaries, 53 properties |

Each capture: AGREE, AGREE, the control DIVERGE where its case declares.

## Declared files and lifecycle (per case)

| Population | Names under the case directory | Count |
| --- | --- | --- |
| Case declaration | `case.sexp` (`scripts/matched_gpr_case.py` reads it) | 1 |
| Prepared inputs | `guest.elf`, `reference-config.json`, `baseline.expected.sexp`, `control.expected.sexp` | 4 |
| Declarations | `planned-experiment.sexp`, `dependencies.sexp`, `authorities.sexp` | 3 |
| Observations | `baseline`, `repeat`, `control`, each `.trace`, `.stdout`, `.stderr`, `.receipt.sexp` | 12 |
| Results | `measured-experiment.sexp`, `verification.json` | 2 |

With this index: 155 files at most, 141 present. Prepared inputs come from canonical sources
(`scripts/prepare_div_inputs.py --case <id>`, `--verify` re-derives); the declarations from
`scripts/capture_div.py --declare --case <id>`, committed before the capture; observations and
results from `scripts/retain_div_capture.py --case <id> --declaration-commit <id>`, exactly once.
`verification.json` is a derived receipt, qualification false; a case without one credits nothing
(`declared`). Existing names refuse reuse; failed observations stay history; never rerun a
capture or replace retained bytes — a correction is a new case. S-expression is the source of
truth; the JSON and the ELF are reproducible artifacts; the wrong expectation is a negative control.

## Finite retention envelope

The family is limited to 155 files, 96 MiB aggregate and 4 MiB per member
(`decision_evidence-family-two-cases.md`, re-derived for seven cases by a43b-3d: seven cases and this
index hold at most 96,800,768 B, `retention_limits()`; health 152 files / 84 MiB). Per case: three
4 MiB traces and nine 64 KiB streams/receipts, ten 64 KiB prepared and metadata slots; this index
4 KiB / 80 lines. The registry enforces the family and index bounds; the input probe checks member
names, same-volume regular files and each role limit before authenticating prepared pins, never
descending into an unknown directory. An eighth case is a new re-derivation. The 128 MiB
artifact-read and 16 MiB snapshot ceilings are unchanged; offline checking needs neither the
reference executable nor an acquired source cache.
