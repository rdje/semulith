# DEV_NOTES shard — _(2026-10-05)_ … _(2026-10-04)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-05)_ — the cancellation site is the spec sentence, and the proof grades the tests too (P4-SYSTEM.4 slice c)

Execution of the `.4` brief's checkpoint (c) measured:

- **"Regardless of success or failure" has a boundary, and Sail marks it.**
  Decision 4's invalidation set says any SC clears — but Sail 0.14's execute
  clause (`zalrsc_insts.sail:71-79`) runs `vmem_write` FIRST and cancels only on
  the `Ok(b)` path; the `Err(e)` trap path cancels nothing. The spec sentence's
  "success or failure" is exactly the completed path: an SC that page-faults is
  neither, and the reservation survives. That is also decision 4's own second
  half (a trap does NOT invalidate), now with a reference-model measurement
  behind it — the evaluator arm's clear sites sit after the policy match and
  after a successful store, never on a deliver path, and the scratch proof's
  trapped-SC cell pins it (promotion: declined — the durability is the machinery:
  the proof cell and the reservation module's suite arm it).
- **The scratch proof grades the TESTS as hard as the engine.** The first run
  came back 13/3, and all three failures were mine: an "LR replaces" sequence
  that let the failing SC clear the reservation before the final SC (the engine
  correctly failed it — any completed SC clears); a "trapped SC" cell using a
  mismatched address, which fails with code 1 BEFORE any memory operation — no
  trap exists to observe (the boundary-fault variant, with the address matching
  and the store scripted to fault, tests the real path); and one expected value
  that forgot the final SC's overwrite. A proof that only ever passes teaches
  nothing; the 13/3 run is the evidence the harness discriminates.
- **The AMO needs its own translation kind.** `AccessKind::Store` judges W only
  (translation.rs:374), so an AMO on an unreadable page would have passed
  translation untouched — while RVP-SUPERVISOR demands a store page fault (15,
  never 13). `AccessKind::Atomic` judges R∧W under the store/AMO causes; the
  translation suite's new cells fire all four fault flags.

## _(2026-10-04)_ — the operation is the encoding, and the variant waits for the composition (P4-SYSTEM.4 slice b)

Execution of the `.4` brief's checkpoint (b) measured:

- **The AMO's operation cannot be spelled.** A first draft wrote `(amo add …)` —
  and the checker's walk refused it: `'add' is not an operand this instruction
  has` (rc=1). Every bare-symbol argument in this language is an operand
  reference, so an operation name in argument position reads as a phantom
  operand. The op is the funct5 ENCODING as `(lit N)` — the value the
  instruction's own fixed bits carry — and that choice composes with the
  repository's own rule (a constant that is a function of the pinned tables is
  derived, never typed): `gen_definition`'s `amo_operations` RE-DERIVES the
  closed Zaamo nine from the composed encodings' bits 31..27 and refuses an op
  outside it by name. The sem file cannot invent an operation the pinned tables
  do not carry, and the refusal text lists the derived set (promotion: declined
  — the durability is the machinery: the DEF-GEN RED arms fire the refusal).
- **The variant waits for the composition.** The evaluator's `Sem` match is
  exhaustive with no wildcard (measured: TlbInvalidate is the last arm) — the
  `.2` slice-d wall exactly. Emitting the A variants unconditionally would break
  compilation until slice (c)'s arms exist, so the variants emit exactly when
  the unit's own fragment list composes `riscv/a`: the tracked modules
  regenerate hash-only (the OWN-03 generator pin), the scratch composition
  (base+Zicsr+Zicntr+system+A, untracked) lowers and compiles standalone, and an
  A operator where the composition lacks A is a refusal, named. The mirror stays
  a pure function of the canonical definition — the definition today has no A
  forms, so the mirror has no A surface, and the bind (slice e) lands variants,
  instructions and evaluator arms in one commit.

## _(2026-10-04)_ — the pin that exposed its own census's blind spot (P4-SYSTEM.4 slice a)

Execution of the `.4` brief's checkpoint (a) measured:

- **The scope-vs-tables leg could not see a 64-bit table.** The `extra` collector
  in `fetch_references.sh` tested `n.startswith("rv_")` — so `rv64_a` (and
  `rv64_m` before it) never joined the census the leg enumerates. The gap was
  latent for exactly one reason: no profile had ever declared an A or M form
  while pinning the 64-bit table, so the missing rows never faced a census that
  expected them. The rv64_a pin was the first input that made the gap load-bearing:
  with the collector fixed, the pin broke the leg outright — 87 enumerated vs 65
  declared. Both halves of the fix are the dossier's own precedents: the rv64i
  ledger's declared M exclusion ("pinned for the fragment test case, not the
  scope") extends to the A tables verbatim in shape, with the same flip
  condition — a declared lr./sc./amo form includes them, which is exactly what
  slice (e)'s atomic bind will do when the census grows 65→87. A check whose
  blind spot is found by the first input that needs it is the RED-before-green
  discipline working as designed: the fix was written against the measured 87-vs-65
  failure, not against a reading of the code (promotion: declined — the durability
  is the machinery: the exclusion and its flip condition live in the fetch leg
  itself, and the leg's own verdict arms them).
- **The brief's "aqrl field" is two tokens in the tables.** Every rv_a/rv64_a row
  lists `aq rl` as separate operand tokens; the pinned arg_lut.csv's `"aqrl",26,25`
  is the combined field, and no row carries an `aqrl` (or `amoop`) token. So the
  generated fragment owns `aq` and `rl` — the generator's own rule is that a field
  nothing references invites a reader to believe it is supported — and the
  assembler's suffix rule lands the `.aq`/`.rl`/`.aqrl` value in exactly those
  bits. Deriving from the rows rather than from the brief's shorthand is what kept
  the fragment generated, never hand-authored.
- **spike-dasm prints `lr.w` plain for all four suffix words.** The aq/rl bits are
  measurably set in the emitted words (0x100120af / 0x140120af / 0x120120af /
  0x160120af) and sc/amo print their suffixes back exactly — lr's plain printing
  is spike's own preference, the rdcycle-prints-as-csrr precedent from `.2` slice
  (a). The round-trip is exact for the 22 forms × 4 suffix combinations with that
  one recorded convention.

