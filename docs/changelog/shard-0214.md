# DEV_NOTES shard — _(2026-10-06)_ … _(2026-10-06)_

> Sharded from `DEV_NOTES.md` under its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-06)_ — frm held what the spec writes, not what the laboratory preferred (P4-SYSTEM.7 slice c1)

Slice (b) declared `frm` WARL one-of 0..4 — an illegal write retaining the old
value — and parked Sail's "stores anything" as a named difference for slice (e).
Re-reading the pinned F chapter for slice (c)'s dyn-rm resolution exposed it: FSRM
writes "the three least-significant bits of integer register rs1 into frm" (no
legalization), and the rounding-mode table names 101–111 *dynamic reserved
rounding modes*, a state frm must be able to HOLD for the sentence to mean
anything. Three artifacts had encoded the one misreading — the declaration, the
privilege unit tests, the spec-side authoring tool — so every check agreed with
every other. The fix went in at the declaration (`(legalize (any))`, the FSRM
sentence quoted in the statement); the generated state mirror and the definition
manifest regenerated; the tests now assert 7 lands from a fcsr slice and 6 from a
frm write of 0b1110. `fp-fcsr-view` was re-derived spec-side FIRST (the tool
corrected) and run against the unfixed engine: step 15 read `0x45` where the
specification gives `0xE5` — RED for the right reason — then green on the fix.
The guest's step 13 now also writes bit 8, so the legality cell it sits in is
fcsr's own "shall ignore writes to these bits / supply a zero value" sentence, not
a retention the spec never granted.

Also recorded here: the pinned revision WEAKENED the reserved-rm rule — "The
behavior of floating-point instructions that depend on rounding mode when executed
with a reserved rounding mode is reserved" — while calling the ratified
illegal-instruction mandate "still valid behavior". The laboratory takes
illegal-instruction for static 101/110 and dynamic 101–111 (Sail's
`Fcsr_RM_Illegal`, `fext_insts.sail:51-63`); slice (c3) states it in the
operator's contract. Two incidental defects of the authoring tool were fixed in
passing: its header template still named "P4-SYSTEM.5 slice b, the interrupts
corpus" (both FP guests carried that false provenance line — corrected, values
byte-unchanged in `fp-fs-off`), and it wrote directives into S-expression strings
unescaped, so a `"` in a directive would have silently broken the file — it now
refuses by name (fired RED once). And the book's P4 chapter carried a duplicated
`## Gate CPU-SYSTEM` heading (slice b) and "underway" headings over the closed
`.3`/`.4` sections — fixed.

- **Validation:** `cargo test -p semulith-core --lib` 134/134; `cargo test -p
  semulith-verify run_rv64gc` 4/4 (103/103) — and RED against the unfixed
  legalization (fp-fcsr-view step 15); `gen_state.py --check` byte-exact after the
  restore; INTERACTION-MATRIX ok; `make check` + `make gate` green.
- Promotion: PROMOTED — docs/knowledge/a-legalization-rule-is-a-claim-the-spec-must-grant.md
  + INDEX (the map regenerated).
