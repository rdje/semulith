# DEV_NOTES shard — _(2026-10-06)_ … _(2026-10-06)_

> Sharded from `DEV_NOTES.md` under its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-06)_ — the FP qualification: two candidates, three lineages, and MPFR is a thing you measure too (P4-SYSTEM.7 slice a)

The `.7` brief's slice (a) measured:

- **The arithmetic core is the easy part; the policy surface is where backends
  differ.** rustc_apfloat matches MPFR on every add/sub/mul/div/fma value across
  all five rounding modes and both widths — 63,752 cases, zero core
  disagreements. Every disagreement was a boundary the crate explicitly does not
  own: LLVM signals opOverflow only for infinite results (IEEE wants the
  magnitude rule — 362 measured cases), format conversion of an sNaN carries no
  NV (24), NaN→int converts to 0 (RISC-V wants max + NV — 340), fmin/fmax's
  signed-zero pair and both-NaN payload are LLVM's conventions (240), and
  format-conversion payloads scale per LLVM where RISC-V canonicalizes (32). A
  backend qualification that stops at "the adds agree" would have missed the
  whole story; the per-op disagreement tables BY NAME are the deliverable.
- **MPFR needed four corrections of its own.** The DON'T-USE MPFR_RNDNA (RNDA
  behavior for the arithmetic ops — RMM rides mpfr_round_nearest_away); the OF/UF
  flags are exponent-range-shaped (computed spec-side against an exact shadow —
  and the shadow needs 2100 bits, not 300: f64max + 1 spans 1024 bits); NaN
  results canonicalize (payloads dropped); the NAN flag is "result is NaN", never
  IEEE's NV. A reference library's flags are ITS semantics — the generator that
  trusts them writes a wrong spec.
- **softfloat's failure is capability, not quality.** Its arithmetic core is
  MPFR-exact where it exists (including the sqrt APFloat lacks), 3-5× cheaper
  per op; it simply has no rounding modes, no flags, no FMA, no 64-bit
  conversions, no min/max — five of §6's explicit requirements. The one family
  it differs on (it clears the propagated NaN's sign; IEEE-unspecified) is
  recorded as its convention, moot for the verdict. The lesson reached the
  knowledge layer as its own card (the candidate-landscape census is a lead,
  the crate's own documents are the measurement surface) — PROMOTED, the kind
  the layer exists for.

promotion: PROMOTED — `docs/knowledge/a-candidate-landscape-census-entry-is-a-lead.md`
(the landscape-census lesson; the MPFR-measurement half lives in the decision record's
own text, which is the durable home for backend-specific facts).
