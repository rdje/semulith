# CHANGELOG shard — SEMULITH-P5-0007 … SEMULITH-PKG-0017

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P5-0007 (leaf P5-BOARD.2) — the first device dossier: `sifive-uart-lab-v0`, fully gated; the machinery generalized by declaration

- The SiFive UART dossier lands under
  [`profiles/sifive-uart-lab-v0/`](profiles/sifive-uart-lab-v0/DOSSIER.md): the §13-pinned
  source (digest re-verified from the materials cache), 19 requirements (13 defined + 6
  measured silences — Reserved bits, X-marked resets, FIFO reset, off-map/non-32-bit
  accesses, the watermark mode), 19 mirrored obligations under contract `sifive-uart-v0`
  v0 with the schema's new third direction `device-guarantee`, the state document with
  its earned hidden-state census (registers + FIFO contents/occupancies, nothing else
  MMIO-visible), 19 verbatim decision mirrors, and 3 datasheet-derived register-read
  expectation documents recorded **before any model exists**.
- The dossier machinery generalized **by declaration, not exemption**
  ([`decision_device-applicability-by-declared-vehicle`](docs/decisions/decision_device-applicability-by-declared-vehicle.md)):
  `vehicle (route device-model) (comparison register-expectations)`; `profile.sexp`'s
  processor-only fields optional; `mmio_registers` scope; `expectations.sexp`
  entry/instructions optional; EXTRACTION / EXERCISE-COVERAGE / INTERACTION-MATRIX derive
  device applicability with contradiction = RED; a device-guarantee discharges a CPU
  assumption by construction (pinned GREEN arm); PROFILE-CONSISTENCY needed no
  conditional (measured by a new self-test arm).
- Measured in execution, fixed at root: the §13.8 watermark bits' level-vs-hold gap
  (`REQ-D-UART-WM-MODE` — expectations pin a bit only when its raised condition holds
  under every reading); the `REQ-U-` id prefix colliding with RECORD-SCHEMA's mechanical
  decision→requirement mapping (renamed); the interaction-matrix n/a note counted as a
  cell (fixed); FIFO resets recorded as "unspecified" data rather than weakening the
  every-element-a-reset contract.
- FACT-OWNERSHIP re-pinned to three units (registry + fixtures); the `profiles/` bound
  re-derived 4× ([`decision_profiles-family-four-units`](docs/decisions/decision_profiles-family-four-units.md)).
  Registration of all three units consolidates into `.11`; the LAN9118 dossier is `.10`.
- Validation: all dossier documents schema-validate; the three profile-glob gates decide
  the device by declaration; every edited check's self-test green (17/9/14/41/7/14/10
  arms, 0 fail); `make gate` all doctrines green; the mdBook builds.

## SEMULITH-PKG-0017 (leaf SEMULITH-PKG.9) — the policy note's provenance triple now re-derives from the note

- Session-start policy check (§14/§17/§18), measured live: `README_POLICY.md`'s neutral
  body is byte-identical to the originating project's current revision (no unadopted
  upstream change), and `docs/CLAIM_VERIFICATION.md`'s recorded source SHA-256
  (`9f99df25…6046bd`) matches the pgen source exactly. Nothing to re-adopt.
- One defect found and fixed: the policy adoption note's recorded SHA-256 / line / byte
  triple did not state its digest span, so it failed to reproduce as written (the measured
  span trims leading blank lines and the `---` separator). The note now states the span;
  the re-deriving command lives in task leaf `SEMULITH-PKG.9`; the recorded
  `77a1e934…c0182d6eefec` / `159 / 8,279` reproduces exactly.
- `SEMULITH-PKG` complete (9/9). Validation: `scripts/check_doctrines.sh` all green.

