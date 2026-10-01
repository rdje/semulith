# CHANGELOG shard — SEMILITH-MB-0006 … SEMILITH-MB-0006

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMILITH-MB-0006 (leaf MODEL-BOOKS.4) — the references, their configuration, and what agreement is worth

- The per-unit book gains its references chapter
  (`docs/models/rv64i-lab-v0/src/references.md`): the cast honestly labelled (sail-riscv
  0.14, spike 1.1.1-dev, QEMU never-exercised, ACT4 never-a-second-opinion), the
  acquisition discipline (the fetcher fired RED on a corrupted digest), and the
  configuration story told through the controls that CHANGED the observation — the
  acceptance's own requirement.
- The three controls, with their recorded outputs: the ISA-string read-back (flipping `M`
  back on gave `DIFFERS … rv64im_zvl32b` against the pinned `rv64i_zvl32b`); the platform
  correction (`DIFF-PLATFORM-DEFAULT` — the CLINT `mtime` probe advanced 2, then 3 under a
  plain `ld`; the override now declares the device-less single-region platform, and
  `guest-no-device` holds it); and the decisive misaligned-policy flip (same ELF, nothing
  else changed: `FIRST DIVERGENCE at aligned step 2 … sail writes=[(x1, 0)] … spike
  writes=[]` — "the two models agree BECAUSE the profile is matched" is a measurement).
- The harness differences (including DIFF-TRAP-RECORD-SHAPE — the comparator's false pass
  on a truncated trace) and the two measured reference-vs-reference differences
  (DIFF-FENCEI-EXECUTED, pinned as the `it-fencei` expected divergence;
  DIFF-TVAL-PHYS-MASK) are told as the lessons they are.
- The independence inventory in prose: encoding not-shared (and the cut runs the other way
  than first assumed — our assembler shares `riscv-opcodes` ancestry with SPIKE, not
  Sail), floating point shared (184/199 files byte-identical), integer semantics
  no-evidence-of-sharing, expected-result derivation shared (ACT4 ↔ Sail), QEMU
  not-examined — ending in the per-leg verdict: encodings rest on Sail alone, semantics on
  both references, nothing on ACT4 or QEMU.
- Every id/version/count grep-verified as written; no gate extended (26 doctrines). Both
  books render; `make gate` all green.

