# CHANGELOG shard — SEMULITH-PS-0074 … SEMULITH-MM-0073

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-PS-0074 (leaf P2-SCALAR.7, design) — mid-execution snapshots, designed on the pinned census

- The design's pending-state census is not new work but the pinned dossier's own:
  `state.sexp`'s hidden-state census measured all seven candidates absent, so a complete
  snapshot for this profile is exactly registers + pc + memory — anything more is "not
  offered at all", the acceptance's second arm.
- The mechanism: a `Snapshot` record (definition-identity pins, region, entry, step k,
  the register file + pc, sparse-encoded memory), JSON via the crate's own reader; the
  proof suite runs every guest's continuation twice (snapshot+continue vs
  restore+continue) with RED arms on corrupted/foreign snapshots; the CLI mirrors
  bundle/replay (`snapshot`/`resume`).

## SEMULITH-MM-0073 (leaf MODEL-METHOD.14) — the encoding re-sourcing probe: adopt-in-principle, measured

- The probe (untracked `target/materials/mm14_probe.py` over the pinned PDF's text
  layer): Chapter 36's listings carry every field as selectable text; ADD reconstructs
  end-to-end identical to the incumbent fragment; the full sweep measures **52/52
  opcodes extracted, zero value conflicts, 37/52 fully reconstructed by the naive
  parser** — the 15 remainders are parser-ordering gaps (page-local alignment), each
  caught by the incumbent comparison, which is the verification control.
- Decision recorded (`decision_encoding-resourcing-probe`): adopt-in-principle; the
  re-source is a later reviewed leaf (`.8` owns the encoding), triggered when the
  encoding is next touched or a second unit reuses the fragment. The re-sourced
  provenance would shrink the shared-with-spike ancestry leg.
- **The tree CLOSES 17/17.** Closure sweep found `.15`/`.17`'s Status fields stale
  (`active` with Results landed) — drift corrected.
- `MODEL-METHOD` leaves the active index; `P2-SCALAR.7` (snapshot/replay) is next.

