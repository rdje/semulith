# Retained finite evidence

This bounded index owns one prepared case:
`evidence/rv64gc-signed-div-truncation-v2/`. P4-SYSTEM.14 a42af curates its inputs;
the [model book](../docs/models/rv64gc-lab-v0/src/prepared-inputs.md) explains their
producers, exact identities and verification. No canonical observations or
qualification are supplied by preparing these files.

## Declared files and lifecycle

| Population | Names under the case directory | Maximum count |
| --- | --- | --- |
| Prepared inputs | `guest.elf`, `reference-config.json`, `baseline.expected.sexp`, `control.expected.sexp` | 4 |
| Fresh observations, still pending | `baseline`, `repeat`, `control`, each with `.trace`, `.stdout`, `.stderr`, `.receipt.sexp` | 12 |
| Capture declaration/results, still pending | `planned-experiment.sexp`, `dependencies.sexp`, `authorities.sexp`, `measured-experiment.sexp`, `verification.json` | 5 |
| Family index | This file, outside the case directory | 1 |

Only the four prepared inputs and this index exist at this slice. Before a
canonical run, commit the final entrypoint, exact manifest/authorities and planned
record naming the twelve fresh outputs above. Collection must use the existing
combined allowance protocol. Existing output names refuse reuse; failed and
partial observations remain historical failure data. Never replace them to make
a comparison pass. A corrected capture needs a separately owned declaration.

S-expression remains the project's source-of-truth format. The JSON configuration
and ELF image are reproducible interoperability artifacts for the reference's
public interface. Their canonical inputs remain in the existing profile/encoding
corpus. The wrong expectation is explicitly a negative control.

## Finite retention envelope

The family is limited to22 files,16 MiB aggregate and4 MiB per member. The twelve
observation slots inherit three4 MiB traces and nine64 KiB streams/receipts from
the collector. Four prepared inputs and five metadata slots each reserve64 KiB;
this index reserves4 KiB/80 lines. Their combined maximum is below16 MiB. The
registry enforces the family and index bounds. The input probe checks the
declared member names, same-volume regular files and each role limit before
authenticating prepared pins. Unknown directories are never descended into. Preparation grants no permission to grow the
family to another case.

The128 MiB combined artifact-read ceiling and16 MiB evaluator snapshot ceiling
remain unchanged. The reference executable stays a separately pinned replay
dependency under its public acquisition route. Offline retained checking must
not require that binary or acquired source caches.
