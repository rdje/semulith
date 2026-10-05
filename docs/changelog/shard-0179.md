# DEV_NOTES shard — _(2026-10-03)_ … _(2026-10-03)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-03)_ — the byte-frozen enum wall; a rotated digest exposes an arm's assumed first digit (P4-SYSTEM.2 slice d)

Execution of the `.2` brief's checkpoint (d) measured:

- **The two-profile shape has a hard wall, measured by construction.** The tracked
  evaluator matches on rv64i's generated `Sem` enum, which DEF-GEN freezes byte-exact and
  which lacks the slice-(b) variants — so the new operators' evaluation arms cannot exist
  in tracked code until the rv64gc definition module is tracked (the flip). Three shapes
  were measured and rejected before the chosen one: parameterizing the evaluator over the
  tree (Rust enums don't extend); a shared evaluator over both Sem types (a second
  evaluator is the OWN-01 failure); moving the Sem vocabulary to a hand-authored module
  (changes rv64i's frozen bytes). What lands tracked instead: `privilege.rs`, the
  MACHINERY over a `PrivilegedHart` trait — the generated rv64gc state module implements
  the trait with the descriptor's tables, and the scratch proof compiles the tracked file
  byte-identically (cmp-verified) against the scratch-generated modules. The evaluator's
  new-variant arms are proven at scratch (the harness's tree-walker) and port at the flip.
- **The WARL seam needed structured data.** Slice (c1)'s prose legalization could not be
  applied mechanically; it became the `(legalize …)` mini-language (`(any)`,
  `(read-only V)`, `(one-of V…)`, `(computed)`) across schema, document, mapping and
  generator — with the cross-checks (a WARL field without one is refused; a read-only
  constant must equal the field's reset). The proof caught my own defect: a CSR with no
  field table (an atomic register) had every write preserve every bit — `covered=0` masked
  the whole word; atomic registers write wholesale.
- **The digest cascade works, and it exposed a fragile arm.** Adding the tracked
  `run-order.txt` rotated the dossier digest; the designed cascade re-derived (reports →
  board pin → board artifacts → platform manifest → both model books). PLATFORM-GEN's
  stale-pin self-test arm mutated the pin by flipping its FIRST CHARACTER — which stopped
  mutating the day the digest rotated to a different leading hex digit; the arm passed a
  mutation that wasn't one. It now rewrites to a fixed wrong value of the same shape.
- **The brief's "51-name list" was 49** (measured); the guest set is now
  directory-derived with the run order as recorded data, cross-checked both directions.
  And gen_definition's composition name list carried the third copy of slice (a)'s
  dropped-`(extensions …)`-form bug — "4 declared instruction(s) have NO semantics: mret,
  sfence.vma, sret, wfi" named it instantly. Three copies of one latent defect across
  three readers of one schema shape — the fix pattern is now uniform (every form
  contributes), and the corpus gates' arms prove it.

Promotion: declined — the digest cascade is machinery with its own gates, the arm fix is
its own evidence, and the wall's reasoning has its decision record. Recorded in the owning
leaf's checklist (LOCKSTEP).

