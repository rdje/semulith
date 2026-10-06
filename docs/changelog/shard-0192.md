# DEV_NOTES shard — _(2026-10-03)_ … _(2026-10-03)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-03)_ — the override must name what it depends on (P4-SYSTEM.3 slice a)

Execution of the `.3` brief's checkpoint (a) measured:

- **Sail's default had Svade on all along.** The .2 override's template-driven
  generation set every extension it named — including `Svade supported: false` —
  so the .2 experiment ran with the hardware-update policy (irrelevant then: no
  guest activates translation). But the default config's `Svade.supported` is
  `true`: had the template not named it, the .2 config would have silently
  inherited the Svade policy. The flip to `true` is the D-SVADE match — and the
  discipline it crystallizes: a matched override NAMES every flag its experiment
  depends on, because inheriting a default is a silent config, not a chosen one.
  The re-run is the proof the flip is behavior-free for this corpus: 11/12 AGREE,
  byte-identical verdicts to the pre-flip baseline (measured, never assumed).
- **The refusal arm's fixture must pass the mapping first.** The first
  validate_gc refusal arms failed for the wrong reason — my synthetic
  `(hardware_stack (placeholder true))` was refused by the dossier MAPPING
  (`missing (levels …)`) before validate_gc ever ran. A RED arm proves the right
  refusal only when its fixture is valid up to the layer under test: the arms now
  inject mapping-valid construct shapes, so the refusal that fires is
  validate_gc's own, named. (The same discipline the acceptance boxes' census
  arms already carry — a RED against the wrong layer is a GREEN lie wearing red.)
- **The ISA string is the declared order, and the brief's string was checkable.**
  gen_platform's rule (the .1 fix): single-letters concatenated, multi-letter
  underscore-joined, Z* before S*, alphabetical within. Appending Svade after
  Sstc yields exactly the brief's `rv64imafdc_zicntr_zicsr_zifencei_sstc_svade` —
  the brief's own string was right, and the rule re-derived it rather than
  trusting it. The census (`git grep -l 'rv64imafdc'` over seven trees) found two
  authored occurrences to amend (with owners named), two Sail-DEFAULT mentions to
  leave (not our string), one archive to leave, and no derived surface to
  regenerate (no board pins rv64gc today).
- **Validation:** the dossier flips schema-valid and RECORD-SCHEMA green (rule 4
  statement-identity, rule 9 restatement, the D-SV39 note correctly NOT
  mirrored); the override flip config-valid; the full 12-guest re-run
  baseline-identical; STATE-GEN 22→25 arms, both real pairs byte-identical;
  `make check` 8/8, `make gate` all green (DERIVED-COUNTS 419→422 re-derived).
  Promotion: declined (the matched-override name-your-flag discipline is the
  reference dossier's own record, and this slice's checklist carries the
  measurement).

