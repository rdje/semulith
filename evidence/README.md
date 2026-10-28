# Retained finite evidence

This bounded index owns the evidence family: one directory per reviewed finite case of
`profiles/rv64gc-lab-v0` (the cases `scripts/matched_gpr_property.py` reviews), each with the
same 21 declared slots. The [model book](../docs/models/rv64gc-lab-v0/src/prepared-inputs.md)
explains the prepared identities; the [first canonical capture](../docs/models/rv64gc-lab-v0/src/canonical-division.md)
records the observations of 2026-10-19 and 2026-10-22. The m-forms case is the retained one; its
ten policy legs measure satisfied, credited (`CR-GC-M-1`, a42az): nothing here closes the M obligation or the CPU gate.

## Cases (this table is the complete membership)

| Case directory | State | Files | Holds |
| --- | --- | --- | --- |
| `rv64gc-signed-div-truncation-v2/` | captured 2026-10-19; `invalidated` since 2026-10-22 (a pinned input moved) | 21 of 21 | `m-div.s`, 27 boundaries, one predeclared property; baseline/repeat AGREE, wrong-quotient control DIVERGE; superseded by the next capture, never rerun |
| `rv64gc-m-forms-v3/` | captured 2026-10-22 (one invocation of `scripts/retain_div_capture.py`); the retained case since 2026-10-23 (a42ax): method `satisfied`, 10 of 10 legs, uncredited | 21 of 21 | `m-forms.s`, 33 boundaries, 25 predeclared properties (13 forms, 12 Table 1 cells); baseline/repeat AGREE, the boundary 12 x15 −3 → −4 control DIVERGE; qualification false |

## Declared files and lifecycle (per case)

| Population | Names under the case directory | Count |
| --- | --- | --- |
| Prepared inputs | `guest.elf`, `reference-config.json`, `baseline.expected.sexp`, `control.expected.sexp` | 4 |
| Retained declarations | `planned-experiment.sexp`, `dependencies.sexp`, `authorities.sexp` | 3 |
| Retained observations | `baseline`, `repeat`, `control`, each with `.trace`, `.stdout`, `.stderr`, `.receipt.sexp` | 12 |
| Retained results | `measured-experiment.sexp`, `verification.json` | 2 |

With this index: 43 files at most, all 43 present. The prepared inputs are curated from canonical sources by
`scripts/prepare_div_inputs.py --case <id>` (`--verify` re-derives them); the declarations by
`scripts/capture_div.py --declare --case <id>`, committed before the capture; the observations and
results by `scripts/retain_div_capture.py --case <id> --declaration-commit <id>`, exactly once. Planned zero hashes/sizes/exits are unmeasured targets; the
measured record replaces only observation sizes/hashes and checked exits; `verification.json` is a
derived receipt with qualification false. A declared case without a receipt credits nothing
(`scripts/requirement_status.py` reports it `declared`). Existing output names refuse reuse;
failed or partial observations stay historical data. Never rerun a capture or replace retained
bytes to make a comparison pass: a corrected capture is a new declared case.

S-expression remains the source-of-truth format; the JSON configuration and the ELF image are
reproducible interoperability artifacts for the reference's public interface. The wrong
expectation is explicitly a negative control.

## Finite retention envelope

The family is limited to 43 files, 32 MiB aggregate and 4 MiB per member
(`decision_evidence-family-two-cases.md`, 2026-10-22; one case was 22 files / 16 MiB). Each case's
twelve observation slots inherit three 4 MiB traces and nine 64 KiB streams/receipts from the
collector; its four prepared inputs and five metadata slots reserve 64 KiB each; this index
reserves 4 KiB / 80 lines. The registry enforces the family and index bounds; the input probe
checks the declared member names, same-volume regular files and each role limit of every case
before authenticating prepared pins, and never descends into an unknown directory. A third case
is a new re-derivation, not a quiet addition.

The 128 MiB combined artifact-read ceiling and the 16 MiB evaluator snapshot ceiling are
unchanged. The reference executable stays a separately pinned replay dependency; offline retained
checking must not require it or any acquired source cache.
