# CHANGELOG shard — SEMULITH-PS-0077 … SEMULITH-PS-0077

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-PS-0077 (leaf P2-SCALAR.8) — the portability matrix: three legs green, the honest `incomplete`

- `scripts/check_portability.sh` runs the four legs and ends with the honest verdict:
  native aarch64 green (the commit gate's run + the digest manifest over the 49 guests'
  `demo --json` fingerprints — the contract the second host must reproduce
  byte-identically), Miri green 65/65 interpreted, cross-endian green 65/65 on
  big-endian powerpc64 under Miri — and the mandatory x86-64 leg measured UNAVAILABLE
  (Rosetta absent), so the verdict is `incomplete` and the profile stays experimental.
  Recorded, never waived (EVIDENCE_AND_GATES.md §7's own clause).
- The record: `profiles/rv64i-lab-v0/portability.sexp` (baseline.sexp's plain-atom
  shape). The verdict logic carries 6 self-test arms (6/0); the instrument is NOT a
  commit gate (nightly + host-measuring).
- Two authoring REDs, both measured: `grep -q` under `pipefail` SIGPIPEd cargo and read
  every leg red against a green reality (capture-then-read now); a script edited
  mid-run broke its own parse (bash reads incrementally — restart, never edit in
  flight). One drift caught and owned: the model book's bench-arm count had gone stale
  (44 → 53) across two leaves.

