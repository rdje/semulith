# Retained finite evidence

This bounded index owns the evidence family: one directory per reviewed finite case of
`profiles/rv64gc-lab-v0`, each declared by its `case.sexp` and holding the same 22 slots. The
[model book](../docs/models/rv64gc-lab-v0/src/prepared-inputs.md) explains the prepared identities;
the [canonical captures](../docs/models/rv64gc-lab-v0/src/canonical-division.md) record the
observations. Nothing here closes the M obligation or the CPU gate.

## Cases (this table is the complete membership)

| Case directory | State | Files | Holds |
| --- | --- | --- | --- |
| `rv64gc-signed-div-truncation-v2/` | captured 2026-10-19; `invalidated` 2026-10-22 | 22 of 22 | `m-div.s`, 27 boundaries, 1 property |
| `rv64gc-m-forms-v3/` | captured 2026-10-22, 10 of 10 legs; `invalidated` 2026-10-29 (a44-2b) | 22 of 22 | `m-forms.s`, 33 boundaries, 25 properties (13 forms, 12 Table 1 cells) |
| `rv64gc-m-forms-v4/` | captured 2026-10-29 (a44-4), credited `CR-GC-M-2`; `invalidated` 2026-11-02 (a43b-2b) | 22 of 22 | v3's program and prepared bytes; traces byte-identical to v3's |
| `rv64gc-xlen-forms-v1/` | captured 2026-10-29 (a43a-2e), the first non-M case (REQ-D-XLEN), credited `CR-D-XLEN-1`; `invalidated` 2026-11-02 | 22 of 22 | `xlen-forms.s`, 25 boundaries, 17 properties |
| `rv64gc-m-forms-v5/` | declared 2026-11-02 (a43b-2c), its control declared | 8 of 22 | v4's case and prepared bytes |
| `rv64gc-xlen-forms-v2/` | declared 2026-11-02 (a43b-2c), its control declared | 8 of 22 | xlen-v1's case and prepared bytes |

Each capture: AGREE, AGREE, the control DIVERGE where its case declares.

## Declared files and lifecycle (per case)

| Population | Names under the case directory | Count |
| --- | --- | --- |
| Case declaration | `case.sexp` (`scripts/matched_gpr_case.py` reads it) | 1 |
| Prepared inputs | `guest.elf`, `reference-config.json`, `baseline.expected.sexp`, `control.expected.sexp` | 4 |
| Declarations | `planned-experiment.sexp`, `dependencies.sexp`, `authorities.sexp` | 3 |
| Observations | `baseline`, `repeat`, `control`, each `.trace`, `.stdout`, `.stderr`, `.receipt.sexp` | 12 |
| Results | `measured-experiment.sexp`, `verification.json` | 2 |

With this index: 133 files at most, 105 present. Prepared inputs come from canonical sources
(`scripts/prepare_div_inputs.py --case <id>`, `--verify` re-derives); the declarations from
`scripts/capture_div.py --declare --case <id>`, committed before the capture; observations and
results from `scripts/retain_div_capture.py --case <id> --declaration-commit <id>`, exactly once.
`verification.json` is a derived receipt, qualification false; a case without one credits nothing
(`declared`). Existing names refuse reuse; failed observations stay history; never rerun a
capture or replace retained bytes — a correction is a new case. S-expression is the source of
truth; the JSON and the ELF are reproducible artifacts; the wrong expectation is a negative control.

## Finite retention envelope

The family is limited to 133 files, 80 MiB aggregate and 4 MiB per member
(`decision_evidence-family-two-cases.md`, re-derived for six cases by a43b-2c: six cases and this
index hold at most 82,972,672 B, `retention_limits()`; health 130 files / 70 MiB). Per case: three
4 MiB traces and nine 64 KiB streams/receipts, ten 64 KiB prepared and metadata slots; this index
4 KiB / 80 lines. The registry enforces the family and index bounds; the input probe checks member
names, same-volume regular files and each role limit before authenticating prepared pins, never
descending into an unknown directory. A seventh case is a new re-derivation. The 128 MiB
artifact-read and 16 MiB snapshot ceilings are unchanged; offline checking needs neither the
reference executable nor an acquired source cache.
