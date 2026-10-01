# CHANGELOG shard — SEMILITH-MB-0005 … SEMILITH-MB-0005

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMILITH-MB-0005 (leaf MODEL-BOOKS.3) — the methodology: from document to model

- The per-unit book gains its methodology chapter
  (`docs/models/rv64i-lab-v0/src/methodology.md`): the pipeline as six gated hops —
  pinned document → decision (authority) → requirement (semantic class) → obligation
  (positive AND negative checks) → derived expectation → the differentials (offline on
  every commit, live three-way).
- The reserved-FENCE rule is followed end to end, by name: the pinned sentence (RVI-RV32I
  §1.1.7, quoted verbatim) → `D-FENCE` (authority execution-environment, the correction
  note intact) → `REQ-D-FENCE` (class implementation-defined, statement verbatim under
  RECORD-SCHEMA) → `OB-FENCE` (CHK-FENCE-POS AND -NEG) → `fault-fence` (EVD-05,
  measured on both references first) → the offline suite and the live smoke. The honest
  gap is in the chapter: the obligation's check ids are declared and G0 measures
  72 declared / 0 implemented — the guest corpus is what tests the rule today.
- The judgement calls are explained with their mechanical edges: semantic class (what
  freedom the source grants) vs authority (who may decide; laboratory policy cannot
  override an architectural rule — the AUTHORITY check). The mistakes stay in:
  DEFECT-A (the dossier condemned the mandated nop; measurement inverted it), DEFECT-B
  (the misaligned-jump link write, fixed in semantics DATA, pinned by `never_written x5`),
  and the two authoring REDs (the overlap constant; the trailing paren) — gates catching
  the author.
- Every id the chapter names was grep-verified against the tracked corpus as written;
  the quoted decision fragments are programmatically verified verbatim. No gate extended
  (authored prose, no generated content — 26 doctrines unchanged). Both books render;
  `make gate` all green.

