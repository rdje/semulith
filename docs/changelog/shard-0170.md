# DEV_NOTES shard — _(2026-10-03)_ … _(2026-10-02)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-03)_ — the dossier machinery had no lifecycle stage for "resolved but no definition yet" (P4-SYSTEM.1)

The `.1` brief assumed the schema already supported the resolution's fields; measured in
execution, the real gap was lifecycle, not fields: EXTRACTION discovers every tracked
`profiles/*/profile.sexp` and refuses a bare processor unit (no encoding.sexp → CANNOT
JUDGE), so a new CPU unit could not be tracked below engine-readiness without a dodge.
The fix followed the by-declaration discipline (the device-model precedent): a fourth
vehicle route, `profile-resolution`, which the three definition-pipeline gates honor as
"nothing to judge yet" — and refuse when contradicted by an encoding, state census, or
guest corpus (the anti-drift property is the point: the route flips to
`generated-definition` the day the pipeline starts, and the full contract attaches).
Two adjacent fixes measured the same day: `check_citations.py` assumed bare page
filenames under the snapshot's `unpriv/` (the privileged pages need subdirectory `file`
fields; the cache root now derives from the declaration, and the declared cache-only
pins are skipped by name), and `gen_platform.py`'s ISA derivation sorted the extension
letters — canonical order is the declaration's, preserved.

Promotion: declined — the by-declaration discipline has its decision records
(`decision_device-applicability-by-declared-vehicle` and kin), and the route's behavior
is armed by self-test REDs in three gates. Recorded in the owning leaf's checklist
(LOCKSTEP).

## _(2026-10-02)_ — the frozen contract is not a live doc, and a pin nothing re-derives is display only (P5-BOARD.6)

Two findings from the platform-manifest leaf, both caught by the gates rather than by
review:

- **The delivered contract is frozen — route announcements to the live surfaces.** The
  `.6` design brief planned a paragraph in `docs/ARCHOGEN_INTEGRATION.md` §3 noting the
  manifest now exists. The file is a `frozen-in-place` row of the delivered planning
  package; DELIVERY-PROVENANCE fired RED on the edit and the edit was reverted. The
  announcement lives where project facts live: the task tree, the board DOSSIER, the
  board book's new manifest chapter, and the project book's plan chapter. The design
  input stays the supplied contract — read-only, cited, never amended
  (`docs/provenance/planning-package-v0.2/dispositions.tsv`).
- **A pin nothing re-derives is a display string.** The board's `dossier-sha256` was
  recorded with the right intent ("a digest match against a newer dossier is a
  finding"), but the census showed one consumer and it was the book generator's
  *renderer*. The export generator now re-derives the digest from the live dossier at
  every run (`gate_report.dossier_digest` — the one computation, factored out of the GC
  report builder and measured byte-identical) and refuses a stale pin by name; the
  PLATFORM-GEN self-test arms it RED. The leaf's own `endianness` edit was the first
  real exercise of the cascade: dossier → GC-REPORT → pin → export.

Promotion: declined — both findings' durability is the machinery itself (the doctrine
fired; the refusal is armed by a self-test RED), and the write-down-what-the-gate-
catches discipline already has its cards. Recorded in the owning leaf's checklist
(LOCKSTEP).

