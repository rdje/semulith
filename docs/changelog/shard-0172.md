# DEV_NOTES shard — _(2026-10-03)_ … _(2026-10-03)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-03)_ — the first multi-extension composition exposed two latent gate defects; a pseudo-op is not an encoding (P4-SYSTEM.2 slice a)

Execution of the `.2` brief's checkpoint (a) measured four things the brief did not know:

- **Upstream restructured without changing a byte.** riscv-opcodes moved every instruction
  table from the repository root to `extensions/`; rv_i/rv64_i/rv_m/rv64_m hash
  byte-identical to the rv64i pins. The fetch route's `master/<file>` would have 404'd any
  fresh fetch — verify-only never noticed because it only hashes what is on disk. The route
  now maps `rv_*` under `extensions/` and a scripted fresh re-fetch proved it live.
- **Zicntr adds no encodings.** rdcycle/rdtime/rdinstret exist upstream only as `$pseudo_op`
  rows of csrrs; emitting them as instructions collides with csrrs by mask math. The
  fragment layer gained the `(pseudo …)` construct — assembler spellings the disjointness
  gate decides under a specialization rule (every word a pseudo assembles must already be a
  composed instruction's word; an unrealized pseudo "extends the encoding space it is
  declared not to touch", a partial overlap is "the collision rule one level down"). The
  fragment declares the dependency the rows state: `(requires "riscv/rv64i")
  (requires "riscv/zicsr")`.
- **Two latent defects, no reproducer until today.** `resolve_composition` read only the
  FIRST `(extensions …)` form (`ext[0][1:]`) — every later form was silently dropped, and no
  tracked composition had ever carried two. And the disjointness checker printed
  `DUPLICATE NAME(S)` while returning 0 — the verdict text even claimed "no duplicate
  names". Both fixed at root and armed by new self-test RED arms (disjointness 8→12,
  unit-composition 8→9); the `.1` discipline held: measured in execution, fixed at root.
- **IALIGN was a hard-code; csr was a label.** The assembler's label pass resolved names
  for EVERY operand position and ate `csrrw x1, cycle, x2`'s csr name; labels now resolve
  only where a label is legal (B/J scrambled offsets), and a csr name falls through to the
  operand parser, which resolves it through the pinned csrs.csv. IALIGN is derived from the
  unit's `profile.sexp` (rv64i 32, rv64gc 16). The operand spelling order (`csrrw rd, csr,
  rs1` — the pinned table lists fields `rd rs1 csr`) is proven by the module's documented
  second decoder: spike-dasm disassembles every emitted word back to the requested
  spelling, all 13 forms exact.

Promotion: declined — the durability is the machinery (the fixes are armed by self-test
REDs; the pseudo and IALIGN designs are data in the schema and the pins). Recorded in the
owning leaf's checklist (LOCKSTEP). Intra-tree follow-ups named there: the Rust-side
IALIGN=32 entry check (slice d), csr-name resolution's migration to the tracked state
document (slice c/f), rdcycle's coverage naming (slice e/f).

