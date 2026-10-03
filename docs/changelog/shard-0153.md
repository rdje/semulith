# CHANGELOG shard — SEMULITH-BR-0019 … SEMULITH-P5-0002

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-BR-0019 (leaf P3-BREADTH.6) — the DSP's contract records land governed; the fixture noticed

- `profiles/dsp56300-lab-v0/` gained `requirements.sexp` (seven records, statements
  byte-identical to the profile's decisions) and `contract-obligations.sexp` (thirteen
  obligations — seven mirrors plus six environment-assumptions; contract
  `dsp56300-lab-env-v0`; 26 declared checks). RECORD-SCHEMA attached on landing with zero
  gate edits (auto-discovery; 10 record files green on the first pass); FACT-OWNERSHIP
  gained the DSP's two registry rows.
- FACT-OWNERSHIP's GREEN self-test fixture went RED on the landing BY DESIGN — its pair
  glob follows the real corpus, and the fixture registry still named a one-unit world
  (`UNREGISTERED MIRROR PAIR`). Re-pinned to the two-unit corpus (`__CHECKED__ 5 → 6`),
  the reason recorded in the check's comment.
- Validation: both catalogues schema-validate; RECORD-SCHEMA, FACT-OWNERSHIP (25 kinds,
  self-test 10/10) and `make gate` all green; the rv64i catalogues byte-untouched. The
  DOSSIER's records row reads present; `.6` continues with slice 2 (the BREADTH report).

## SEMULITH-P5-0002 (leaf P5-BOARD.8) — the network-connected board's documentation researched; ten requests filed, the channel measured

- The `2026-10-01` design discussion (boards that touch the world) turned into a measured
  documentation position ahead of `P5-BOARD.1`'s board choice. The corpus survey (the
  snapshotted chipdoc feed, corpus `92a73b6`) measured the holdings: a complete
  register-level Ethernet MAC+PHY contract (TI-DP83816), ESP32/C3/S3 register maps, the
  SiFive FU540/FU740 manuals and HiFive board docs, the TI AM335x TRM — and the recorded
  negative: no standalone Cadence GEM / DesignWare GMAC spec is public.
- Ten acquisition requests filed in `materials/requests.sexp` (the preferred channel),
  each naming its consumer: wired NICs with QEMU precedents (LAN9118, Intel 82540EM,
  RTL8139), three LTE modem AT manuals (Quectel EC25, SIMCom SIM7600, u-blox SARA-R4),
  the WiFi-module command surface (ESP-AT), two register-documented radios for the
  true-RFIC leg (nRF52840, AT86RF233), and one honest probe (AR9271 register docs,
  expected absent). Pickup measured: chipdoc's poller (run read-only) reports exactly
  the ten new ids, rc 1.
- The channel's filing mechanics are now recorded semulith-side as a knowledge card
  (`docs/knowledge/the-chipdoc-request-channel.md` + INDEX) — they had lived only in the
  corpus-side manual, and a session re-derived them the hard way once.

