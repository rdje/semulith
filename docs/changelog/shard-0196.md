# DEV_NOTES shard — _(2026-10-04)_ … _(2026-10-04)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-04)_ — the fault matrix catches the author; the amendment that wasn't there (P4-SYSTEM.3 slice c)

Execution of the `.3` brief's checkpoint (c) measured:

- **The reserved encoding is W-without-R, and the tests said so first.** The
  walk's first draft faulted on R=1 ∧ W=1; the fault-matrix suite (written
  before the implementation, from the pinned §11.1.3.1) named three cells
  PageFault-for-the-wrong-reason in one run. The pinned rule: W=1 requires R=1;
  R=0 ∧ W=1 is the reserved case. EVD-05 held at the test layer — the walk was
  fixed to the derivation, never the tests to the output. The same suite caught
  a second author error of a different class: three leaf constructions missing
  the V bit (V=0 faults correctly — the walk was right, the fixture was wrong).
- **"Supersede the old record" had nothing to supersede.** The brief's
  requirement amendment read like a mirror edit; the measurement
  (`grep -o 'id "REQ-D-…"' | grep -c FETCH` → 0) shows rv64gc's catalogue never
  carried REQ-D-FETCH-IMPLICIT — the slice-(e) mirror closure is 13 records and
  it is not among them. The honest shape followed: a NEW authored
  D-WALK-IMPLICIT + verbatim REQ/OB pair naming the translated composition's
  implicit-access vocabulary, with the owner relationship recorded in the
  statement itself (rv64i's record stays true of rv64i — no translation exists
  there). The mirror rule stayed untouched, which is exactly what it's for.
- **The probe has its own bug class, and it is the auipc class.** Updating the
  slice-(b) Sv39 probe surfaced two of my own construction bugs: stale auipc/addi
  deltas (mtvec landing mid-prologue — the .2 slice-(f) audit's exact class, and
  it fired again on new code) and a `slli` chain that shifted the satp MODE bit
  out of existence (2⁶³+8 ≪ 16 mod 2⁶⁴ drops the top — the trace showed x2 lose
  0x8000000000000000, and the "unexpected" cause-5 answer was the probe's
  correct Bare behavior, not an engine fault). The discipline that ends the
  class is the one the family already owns: print the pc map and the constructed
  CSR value before running anything, and treat an unexpected-but-correct trace
  as a probe bug until proven an engine bug.
- **Validation:** 17 fault-matrix tests (every step's fault path and every
  success path, walk reads counted per scenario, the region byte-identical
  across every Svade fault); the corpus 62/62 with fetch counts unchanged; the
  byte-level identity proof on the walk-live engine (1,884 == 1,884 trace lines,
  cmp clean); RECORD-SCHEMA green on the amendment; `make check` 8/8, `make
  gate` all green. Promotion: declined (the pc-map/constructed-value discipline
  is already the family's recorded rule — this slice's checklist carries the
  instances).

