# Derived members of bounded families are governed by their regeneration doctrine, not the authored-content byte ceiling — the instrument matches the failure mode

- **Type:** `decision`
- **Date:** `2026-10-02`
- **Status:** `active` — supersedes in part
  [`decision_profiles-family-composed-units.md`](decision_profiles-family-composed-units.md)
  (its per-part raise to 131,072 is the interim instrument this ruling replaces; its
  measurement stands)
- **Owner / source:** the `P5-BOARD.3` finding (composed catalogues multiply record bytes
  with composition depth), surfaced for a ruling and **delegated by the director to the
  signing engineer** (`2026-10-02`: *"yours to decision and act upon … SOTA, SIGNOFF and
  PRODUCTION-GRADE"*). Implemented by `P5-BOARD.12`.

## The analysis

Every bounded family in `doctrine/readme_routes.tsv` carries a per-part byte ceiling.
That instrument has a founding failure mode: **silent accretion in hand-maintained
files** — the upstream 1.5 MB hand-kept status file that sat green under its own cap's
displacement. A ceiling forces a human review when an *authored* file's size changes
character.

A **regeneration-gated derived file** cannot present that failure mode:

- it cannot silently accrete — every byte is re-derived from its canonical input on every
  commit by a registered doctrine (STATE-GEN, DEF-GEN, GUEST-GEN, BOARD-GEN, GATE-REPORT,
  MATERIALS-BILL, BOOK-INDEX), and the diff is reviewed;
- its size is a pure function of inputs that are *already bounded* (the parts'
  catalogues), so taxing the output with the same ceiling measures nothing the input
  bounds did not already measure;
- its real risks — a generator emitting wrong content, a shape drifting — are governed by
  other gates (the regeneration doctrine's own self-tests, RECORD-SCHEMA / DOSSIER-SCHEMA
  on the content), not by a byte count.

Measured consequence of the mismatch (`2026-10-02`, `P5-BOARD.3`): the composed
`contract-obligations.sexp` (104,372 B — the merge of three already-bounded parts) fired
the authored per-part ceiling and forced a reviewed raise to 131,072 **one day after**
the previous raise. Composition depth (computer → board → soc → {cpu, device}) makes
that ceremony recur per level while proving nothing about trustworthiness: the raise
reviews a number, when the property that matters is the derivation.

## The ruling

1. **Two-tier per-part rule.** In a partitioned family, the per-part byte ceiling applies
   to every member **not** registered as a derived mirror. A member over the authored
   ceiling is exempt **as a checked property, never a declaration**: it must be
   registered in `doctrine/fact_ownership.tsv` as a *mirror* whose governor is a member
   of the closed regeneration-doctrine set (STATE-GEN, DEF-GEN, GUEST-GEN, BOARD-GEN,
   GATE-REPORT, MATERIALS-BILL, BOOK-INDEX). The registry is the one already
   completeness-checked declaration (every governor registered and running, every corpus
   restatement pair named) — consuming it adds no second declaration surface, and an
   authored file cannot smuggle itself under the exemption because nothing regenerates it.
2. **The discriminating line is byte-re-derived vs authored-and-cross-checked.** The
   NIC's 60,112 B `contract-obligations.sexp` is registered with governor RECORD-SCHEMA —
   a validation gate, not a regeneration gate — so it keeps the authored ceiling
   (0.92× of 65,536). The board's 104,372 B composed catalogue is registered with
   governor BOARD-GEN, so it is exempt. Both outcomes are the intended ones.
3. **Aggregate bounds still apply to derived members** — they are census-level, reviewed
   at unit-count changes, and catch population surprises (a generator writing an
   unexpected *set* of files), which no per-part rule can see.
4. **The interim raise is superseded in part.** The `profiles/` authored per-part returns
   to **65,536** (the composed-units record's measurement stands; its 131,072 was the
   right interim under the old rule). The per-part raise ceremony never recurs for
   composition depth.
5. **The regeneration set is closed and enumerated in the check.** The day a new
   regeneration doctrine is registered, the leaf that registers it adds it to the set —
   the same sanctioned "the day a real case earns it" shape as the schema value lists.

## Consequences

- Deep nesting (soc, computer) no longer multiplies bound-maintenance ceremony: each
  composition level's catalogues are governed by the regeneration doctrine that produces
  them, and the aggregate re-derivations stay on their existing unit-count cadence.
- A derived artifact whose governor is removed from the doctrine registry becomes
  ceiling-liable the same commit — the exemption decays into a breach, not a blind spot
  (FACT-OWNERSHIP already refuses unregistered governors independently).
- `scripts/check_readme_routes.sh` implements the two-tier rule with RED/GREEN self-test
  arms (`P5-BOARD.12`); the routes registry comments carry this ruling's pointer.
