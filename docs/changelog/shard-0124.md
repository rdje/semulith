# CHANGELOG shard — SEMULITH-PS-0076 … SEMULITH-PS-0075

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-PS-0076 (leaf P2-SCALAR.8, design) — the portability matrix: availability measured first

- Measured, not assumed: x86-64 is UNAVAILABLE on this host (`arch -x86_64` → `Bad CPU
  type in executable`, Rosetta absent; no qemu user-mode runner) — the mandatory leg
  reads UNMET, recorded not waived; the profile stays experimental per the acceptance.
- Miri measured present and green: 65/65 core suites interpreted natively AND 65/65 on
  `powerpc64-unknown-linux-gnu` (big-endian) — the cross-endian leg holds. The one
  `unsafe` island (bench's counting allocator) excluded by name.
- The design: `scripts/check_portability.sh` (four legs, honest `incomplete` verdict,
  not a commit gate) + `portability.sexp` in `baseline.sexp`'s plain-atom shape.

## SEMULITH-PS-0075 (leaf P2-SCALAR.7) — mid-execution snapshots: replay proven for the implemented boundaries

- `semulith-verify::snapshot` + the CLI pair `snapshot`/`resume`: the record carries the
  definition-identity pins (the bundle's own pin check, extracted and shared), the region,
  entry, step index, the register file + pc, and the memory sparse-encoded and digested.
  The completeness claim is the pinned hidden-state census: registers + pc + memory is ALL
  the pending state this profile has — anything more is not offered (the acceptance's
  second arm).
- The proof: every tracked guest split at three points (early/middle/penultimate), resumed
  through the JSON round-trip, continuations identical — steps AND crossing logs. RED
  arms: corrupted run (digest), foreign definition (pin), incoherent/overrunning/partial
  records — each refused by name. 175 → 180 verify suites.
- One in-flight RED, the author's test arithmetic: the sparse encoding splits at zero
  bytes (the first run is one byte), so the overrun tamper needed one-past-the-end.
- CLI measured end-to-end: `dir-memwalk.elf` snapshotted at step 13 resumes the copy loop
  exactly (24 continuation steps, stop Trap).

