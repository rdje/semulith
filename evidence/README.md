# Retained finite evidence

This bounded index owns the evidence family: one directory per reviewed finite case of
`profiles/rv64gc-lab-v0`, each declared by its `case.sexp` and holding the same 22 slots. The
[model book](../docs/models/rv64gc-lab-v0/src/prepared-inputs.md) explains the prepared identities;
the [canonical captures](../docs/models/rv64gc-lab-v0/src/canonical-division.md) record the
observations. Nothing here closes the M obligation or the CPU gate.

## Cases

A case is a directory here holding a `case.sexp`; the input probe refuses any other member. [The retained cases](../docs/models/rv64gc-lab-v0/src/retained-cases.md) are generated from those declarations and the credit catalogue, so the membership, each case's requirement and its state are never typed: `python3 -B scripts/gen_model_book.py --unit rv64gc-lab-v0`. A captured case holds 22 files, a declared one 8. Each capture: AGREE, AGREE, the control DIVERGE where its case declares.

## Declared files and lifecycle (per case)

| Population | Names under the case directory | Count |
| --- | --- | --- |
| Case declaration | `case.sexp` (`scripts/matched_gpr_case.py` reads it) | 1 |
| Prepared inputs | `guest.elf`, `reference-config.json`, `baseline.expected.sexp`, `control.expected.sexp` | 4 |
| Declarations | `planned-experiment.sexp`, `dependencies.sexp`, `authorities.sexp` | 3 |
| Observations | `baseline`, `repeat`, `control`, each `.trace`, `.stdout`, `.stderr`, `.receipt.sexp` | 12 |
| Results | `measured-experiment.sexp`, `verification.json` | 2 |

With this index: 903 files at most, 525 present. Prepared inputs come from canonical sources
(`scripts/prepare_div_inputs.py --case <id>`, `--verify` re-derives); the declarations from
`scripts/capture_div.py --declare --case <id>`, committed before the capture; observations and
results from `scripts/retain_div_capture.py --case <id> --declaration-commit <id>`, exactly once.
`verification.json` is a derived receipt, qualification false; a case without one credits nothing
(`declared`). Existing names refuse reuse; failed observations stay history; never rerun a
capture or replace retained bytes — a correction is a new case. S-expression is the source of
truth; the JSON and the ELF are reproducible artifacts; the wrong expectation is a negative control.

## Finite retention envelope

The family is limited to 903 files, 541 MiB aggregate and 4 MiB per member
(`decision_evidence-family-two-cases.md`, a46-2: forty-one cases and this index hold at most
566,956,032 B, `retention_limits()`; health 900 files / 473.4 MiB). Per case: three
4 MiB traces and nine 64 KiB streams/receipts, ten 64 KiB prepared and metadata slots; this index
4 KiB / 80 lines. The registry enforces the family and index bounds; the input probe checks member
names, same-volume regular files and each role limit before authenticating prepared pins, never
descending into an unknown directory. A forty-second case is a new re-derivation. The 128 MiB
artifact-read and 16 MiB snapshot ceilings are unchanged; offline checking needs neither the
reference executable nor an acquired source cache.
