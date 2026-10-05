# DEV_NOTES shard — _(2026-10-03)_ … _(2026-10-03)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-03)_ — a swap forces the language's reads contract; a checker hard-coded to one file checks the other three never (P4-SYSTEM.2 slice b)

Execution of the `.2` brief's checkpoint (b) measured five things:

- **The register-swap hazard decides the reads contract.** csrrw exchanges a register with
  a CSR; a state-threaded `(reg rs1)` after `(set (reg rd) …)` is wrong exactly when
  rd==rs1. No RV64I rule reads a register after writing one, so the language adopted the
  contract without changing any existing meaning: register reads see the PRE-INSTRUCTION
  register file; memory and CSR reads see state at their evaluation point (the
  self-modifying-code discipline is untouched); `(pc)`/`(inst)` are frame constants. It is
  stated once in schema/semantics.sexp, the language's own home.
- **A pseudo's semantics specialize by NAME.** rdcycle ≠ csrrs, so the compose rule's
  `(refines …)` mechanism does not apply and none is needed — the pseudo's own rule IS the
  specialization (rs1=x0 → no write; the row's fixed address), exact because the counter
  gating lives in csr-read's uniform permission model rather than per-instruction. The
  checker indexes `(pseudo …)` operand rows: checked, never demanded nor coverage-counted.
- **The corpus gate's COMPOSE leg had slice (a)'s dropped-form bug.** A silent override in
  the SECOND `(extensions …)` form was invisible — the new self-test arm was proven RED
  pre-fix ("right verdict, wrong reason") before the one-hunk repair, the `.1` discipline.
- **check_citations was a single-file tool.** Its main() hard-coded rv64i.sem.sexp, so the
  three new sem files' locators resolved against nothing. The `--corpus` mode derives the
  binding — each sem file checks against every profile pinning all its cited source-ids,
  and a file no profile fully pins is named. rv64i.sem now resolves under THREE profiles
  (netboard pins the same unpriv pages — a resolution never previously run); the new files
  resolve 8/8, 3/3, 4/4 under rv64gc's 21 pins.
- **The mstatus field positions are figure images again.** The specification's encodings-
  as-images pattern recurs one level down: TSR/TW/TVM/MPRV exist in the pinned chapters
  only as figures, so upstream's checked-in `encoding.h` (masks) and `causes.csv` (trap
  causes — in the cache since the rv64i era, never pinned, measured byte-identical) joined
  the rv64gc ledger. Also measured: `(xret m)`'s bare mode symbol read as an operand
  reference — x is the architectural mode code (3=M, 1=S), the xPP encoding itself.

Promotion: declined — the contracts are data in the schema and the pins, and every new
rule is armed by self-test REDs (semantics 8→15, citations 10→13, corpus 7→8). Recorded
in the owning leaf's checklist (LOCKSTEP).

