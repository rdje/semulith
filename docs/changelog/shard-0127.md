# CHANGELOG shard — SEMULITH-PS-0081 … SEMULITH-PS-0079

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-PS-0081 (leaf P2-SCALAR.9, slice a) — the CI two-host matrix wired; Rosetta measured LIVE

- `.github/workflows/portability.yml`: the host matrix (`ubuntu-latest` x86-64 +
  `macos-latest` aarch64) each running the native leg and uploading the digest manifest;
  the Miri + cross-endian job on x86-64 (nightly provisioned by the workflow); the
  `agree` job byte-comparing both manifests. The instrument gained `--leg` /
  `--emit-manifest` selectors (native-leg manifest measured reproducing the `.8`
  recording byte-identically, `0670a01b…`).
- **Rosetta measured LIVE** mid-slice: the director's install (VLC's Intel build
  triggered it) — `arch -x86_64` now prints `x86_64`, the probe binary runs. The bridge
  is up; slice (b) runs the leg through it next.
- CI evidence lands at the next approved push — the cadence governs.

## SEMULITH-PS-0080 (leaf P2-SCALAR.9, design) — the CPU-LAB release: three slices designed

- (a) The CI two-host matrix: a new `portability.yml` workflow (`ubuntu-latest` x86-64 +
  `macos-latest` aarch64 + a Miri job + the manifest-agreement job); the instrument gains
  `--leg`/`--emit-manifest` selectors. CI evidence lands at the next approved push.
- (b) The Rosetta-local proof when the director's reinstall lands (measured inert today:
  payload in the cryptex, daemon off).
- (c) The release report — measured first: G-CONTRACT's obligation-check implementation
  state decides whether the honest decision can read "accepted" even with portability
  green.
- Ceiling obeyed again: the `.8` checklist archived at the `.9` design commit.

## SEMULITH-PS-0079 (leaf P2-SCALAR.9) — the release route decided; Rosetta measured inert pending reinstall

- The director answered the release fork: CI two-host matrix (permanent home of the
  mandatory x86-64 leg: `ubuntu-latest` + `macos-latest`, the digest manifest the
  byte-exact contract) + Rosetta-local proof (the bridge) — recorded in
  `decision_release-route-x86-64-leg`. No narrower host policy.
- Measured refinement of the `.8` record: Rosetta on this host is PRESENT BUT INERT —
  binaries at `/usr/libexec/rosetta/`, the x86-64 dyld cache in the Rosetta cryptex, the
  oahd daemon not running, `arch -x86_64` failing (`Bad CPU type in executable`);
  activation is the director's admin act (a reinstall is coming). The horizon is on the
  record: Apple phases Rosetta out fall 2027 — nothing may be built on the bridge.

