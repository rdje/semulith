# The x86-64 leg's route: CI two-host matrix permanent, Rosetta the local bridge (expires fall 2027)

- **Type:** `decision`
- **Date:** `2026-09-30`
- **Status:** `active`
- **Owner / source:** the director, `2026-09-30`, answering the release fork recorded in
  `P2-SCALAR.9` ("I opt for CI two-host matrix + Rosetta-local proof"), and supplying the
  horizon fact: Apple will phase Rosetta out entirely during fall 2027.

## The decision

1. **The CI two-host matrix is the permanent home of the mandatory x86-64 leg.** The
   portability instrument (`scripts/check_portability.sh`, `P2-SCALAR.8`) runs in CI on
   `ubuntu-latest` (x86-64) and `macos-latest` (aarch64); the digest manifest
   (sha256 `0670a01b…5bb52` over the 49 tracked guests' `demo --json` fingerprints) is
   the byte-exact agreement contract between them. This route is indifferent to Apple's
   phase-out: GitHub's runners are real hardware on both ISAs.
2. **Rosetta is the local bridge** — used to prove the leg on the development host NOW,
   ahead of the next approved push (the push cadence governs when CI evidence lands).
   It is explicitly time-bounded (gone fall 2027) and nothing may be built on it beyond
   the bridge: the `.8` record's note carries the horizon.
3. **No narrower host-support policy** — the director declined it; the fork's third
   option (stay experimental with the leg named) remains only the fallback while the
   bridge is unproven.

## Measured context (2026-09-30, this host — macOS 27.0, Apple M4 Pro)

Rosetta is **present but inert**: the binaries exist at `/usr/libexec/rosetta/` (oahd,
translate_tool, runtime) and the x86-64 dyld shared cache exists in the Rosetta cryptex
(`/System/Volumes/Preboot/Cryptexes/Rosetta/System/Library/dyld/dyld_shared_cache_x86_64.*`),
but `arch -x86_64` fails (`Bad CPU type in executable`), the oahd daemon is not running,
and `translate_tool` errors on the legacy cache path. Activation is an admin act
(`sudo softwareupdate --install-rosetta --agree-to-license`; on macOS 26+ that flag is
reported to misbehave — the fallback is enabling `com.apple.oahd` via `launchctl`),
measured unavailable to the agent (`sudo -n` requires a password). The `.8` instrument's
x86-64 leg gains the Rosetta path when activation is measured working
(`arch -x86_64 /usr/bin/uname -m` must print `x86_64`).
