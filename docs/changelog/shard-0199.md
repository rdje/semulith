# DEV_NOTES shard — _(2026-10-04)_ … _(2026-10-04)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-04)_ — the cache made the test suite honest twice (P4-SYSTEM.3 slice d)

Execution of the `.3` brief's checkpoint (d) measured:

- **The TLB caught test-design bugs the walk never could.** Two existing
  fault-matrix cells failed the moment the cache was live — and the cache was
  right both times: the SUM=0 cell "faulted" into a legal Physical because the
  previous cell's installed entry answered first, and the A=1,D=1 store "faulted"
  on the D=0 entry the D=0-load cell had installed (the spec's sanctioned
  staleness, exactly as designed). The cells were never wrong about the walk —
  they were wrong about SHARING a hart. Independent outcome cells now run cold,
  and the interaction itself became the Svade-staleness suite (install D=0 via a
  load, the stale store faults on the entry's bit, the fence restores truth) —
  the failure was the specification working, not breaking.
- **Two of my own bugs, two familiar classes.** The fence-instruction test wrote
  `0x12039073` for sfence.vma x3,x4 — rs1 and rs2 swapped by a nibble (the real
  word is `0x12438073`; the wrong one decoded RESERVED and the probe answered
  correctly with a delivered cause 2 to mtvec=0). And the fence-case lookups
  passed full addresses where the API takes page numbers. The cache was
  acquitted on evidence both times; the test took the fix. The discipline the
  family already owns — print the constructed word/address and treat an
  unexpected-but-correct answer as a test bug until proven an engine bug — is
  what closed both in minutes.
- **The census drives the storage, and the gate guards the driver.** The TLB's
  parameters live in the state document's SEM-08 census (the candidate
  re-answered `present true` — the census's own reopen hook, placed at .2), and
  gen_state emits the hart-state field FROM that declaration. The refusal that
  anchors it — a descriptor silent on the cache is refused by name — fired on
  the self-test's synthetic descriptor the moment it landed, and the fixture's
  census now carries the candidate, with a RED arm pinning the refusal. The
  generated module, the trait, and the document can no longer drift apart
  silently in either direction.
- **Validation:** 25/25 translation tests (the walk's 17 plus the TLB suite:
  hit/FIFO/tagging/staleness/Svade-staleness/the four fence cases with
  retentions/the non-canonical no-op/the fence instruction end-to-end/
  determinism tuples identical); the corpus 62/62 and 1,884 == 1,884 trace lines
  byte-clean against the parent engine; STATE-GEN 26/26, DEF-GEN both pairs;
  `make check` 8/8, `make gate` all green (DERIVED-COUNTS 422→423). Promotion:
  declined (both bug classes are the family's own recorded disciplines applied —
  this slice's checklist carries the instances).

