# CHANGELOG shard — SEMULITH-P4-0015 … SEMULITH-P4-0015

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P4-0015 (leaf P4-SYSTEM.3, slice a) — the Svade identity edit, the Sail override flip (measured verdict-identical), the validate_gc refusal

- OQ-2 closes with evidence: the profile implements **Svade** — a translation needing
  an A or D PTE update raises a page fault, never a hardware update. The three legs:
  the pinned revision defines exactly two A/D schemes and names the page-fault one
  Svade (RVP-SUPERVISOR §11.1.3.1, §11.1.10 — inline in the already-pinned chapter,
  so sources.sexp gains no pins, measured); the U54 MMU the Sv39 choice already
  cites implements exactly that scheme ("does not automatically set the A and D
  bits … Instead, the U54 MMU will raise a page fault", FU540 §4.7); and the
  laboratory's observe-through-the-ISA discipline can evidence a page fault but not
  an implicit PTE write, so the hardware-update default would price a new
  observation vocabulary to test a side effect the laboratory need not produce.
  Svadu is NOT selected — menvcfg's ADUE stays WPRI (measured inside the state
  document's `wpri_62_0` field).
- The identity edit: `(extensions "Svade")` in declared order — the canonical ISA
  string is now `rv64imafdc_zicntr_zicsr_zifencei_sstc_svade` (gen_platform's
  declared-order rule; the string matches the brief exactly) — the D-SVADE decision
  with authority laboratory and its verbatim REQ/OB mirrors (the D-ROUTE-FLIP
  shape: contract `rv64gc-lab-env-v0` version `"0"` unchanged, CHK-SVADE-POS/NEG),
  D-SV39's "not as this profile's rule" clause superseded by note (RECORD-SCHEMA's
  mirror rule kept), DOSSIER.md's OQ-2 closed with the legs quoted and its locator
  tables updated, and the ISA-string census discharged: two authored edits with
  owners named (the book, the `.1` Result narrative), the Sail-default mentions
  and the archive untouched, no derived regeneration needed (no board pins rv64gc
  today).
- The reference flips to match: `Svade supported: true` in the tracked override —
  one field, as the brief priced it (the .2 override had set it explicitly
  `false`; Sail's own default is `true`, so the flip also makes the override name
  what it depends on). The full 12-guest re-run against the tracked-derived JSON
  measures the effect: **11/12 AGREE — IDENTICAL to the pre-flip baseline** (no
  guest activates translation; the mm-wfi DIVERGE is the known TW cell, not a new
  effect). The config validates clean.
- The generator hole the brief's pre-condition 6 named closes: `validate_gc`
  refuses `register_family`/`memory_spaces`/`hardware_stack` by name with the
  rv64i path's own wording — three RED self-test arms on mapping-valid injected
  shapes (so the refusal that fires is the validator's own), STATE-GEN 22→25 arms,
  both real owner→mirror pairs byte-identical. `make check` 8/8 groups, `make
  gate` all green (DERIVED-COUNTS 419→422 re-derived, never hand-incremented).
  Next: slice (b) — the translation module + the three hooks + effective mode +
  the Bare-identity proof.

