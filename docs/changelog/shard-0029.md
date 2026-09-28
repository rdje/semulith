# DEV_NOTES shard — _(2026-09-14)_ … _(2026-09-14)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-09-14)_ — a refactor of the source of truth must not move the evidence

- The unit carried 52 instructions inside itself; a base ISA is shared by every profile that
  composes it. Split into `definitions/riscv/{rv64i,m}.sexp`, and the unit now NAMES what it
  composes and owns nothing. Census: instructions in the unit 52 → 0; in `definitions/` 0 → 65.
- ⭐ **The acceptance test was that nothing observable moved**: all four guest ELF digests are
  byte-identical after the split, across two models. A source-of-truth refactor that perturbs the
  evidence has changed the model, whatever the author intended.
- A fragment DECLARES its dependencies; composing the M extension without its base is refused. A
  fragment with a hidden dependency composes by luck, not by construction.
- `definitions/` was registered in the routes registry in the same commit that created it. A new
  tracked family nothing governs is how pressure escapes — measured once already in this project.
- 🔎 Three references to the old generator name survive in CHANGELOG and a completed checklist.
  Left alone: historical records are true as written, and `append_history` exists to stop exactly
  that tidying.
- Promotion is explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — breadth by composing proven parts, not by gating them less

- ⛔ **I proposed the wrong lever and it was rejected.** Facing "model as much as possible" against
  "signoff-grade", I suggested tiering models into `exploratory` (ungated) and `accepted` (gated).
  That buys breadth by creating a second class of model nobody can trust, and the classes would
  blur the first time one cited the other. The right lever is **composition**: assemble proven
  small models. Breadth by reuse of evidence, never by absence of it.
- Grounded rather than invented: both pinned references already compose from fragments —
  riscv-opcodes 111 extension files, sail-riscv 34 extension dirs / 59 encoding files — and this
  project already had the other half (an empty `extensions = []` seam, 8 environment-assumptions).
- ⭐ **Encoding union is DECIDABLE, so composition is a verdict.** Two instructions collide exactly
  when `(a.value ^ b.value) & a.mask & b.mask == 0`, searched exhaustively. Proven: owned RV64I +
  an unseen `M` fragment = 65 instructions, no collision. Fired RED on a realistic mistake —
  composing a fragment already contained — giving 37 named collisions and a rejection.
- ⚠️ Semantics are the hard axis and are NOT decidable: an extension can change a base
  instruction's meaning. A fragment must *declare* that it refines base behaviour; a silent
  override is a defect, not a composition.
- 🔎 LIVE_STATUS.md went **over its ceiling** because I had been writing narrative into a status
  table whose owner column literally says "rows are states, not prose". Trimmed to states; the
  gate was right and the fix was the one the registry prescribes.
- Promotion is explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — owning a source means building without it

- ⛔ The repository did not own its model's encodings: the assembler read `target/refs/riscv-opcodes`,
  untracked and network-acquired, so a fresh clone could not build a model. The project's own rule
  was being broken by its own tooling.
- ⭐ **The test that settles ownership is not that a file exists — it is that the build works with
  the source moved aside.** `mv target/refs/riscv-opcodes /tmp/ … && run_smoke.py` → ok: four
  guests assembled, run on two references and reproduced, with the encodings' origin absent.
- Ownership without re-derivation is a copy, so the agreement is gated and was fired RED on a
  one-bit `funct3` edit.
- ⛔ The new S-expression reader was caught by its own first real input: it stripped `;` comments
  line by line before tokenizing, so a `;` INSIDE a string truncated it and a string could not span
  lines. Generating our own encoding file hit that within minutes. Whether a `;` starts a comment
  depends on whether a string is open — that question cannot be answered by a prior pass.
- The S-expression trigger fired and was answered on merit: trees get S-expressions, records keep
  JSON/TOML and their working gates. "Single source of truth" = one owner per fact, not one file.
- Promotion is explicitly declined in the owning leaf, with the reason.

