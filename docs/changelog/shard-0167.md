# CHANGELOG shard — SEMULITH-MCU-0002 … SEMULITH-MCU-0001

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-MCU-0002 (leaf MCU-DOCS.2) — the channel's twelve answers reconciled: the MCU documentation set acquired and digest-verified

- Verified live first: `build_responses.py --report` → **12 fulfilled / 0 blocked**, exit 0.
  The routes, measured by the channel: the Cortex-M TRMs from Arm's documentation-service
  API; FE310 from the SiFive CDN; MSP430 direct from ti.com; i.MX RT / SAM D21 / STM32 from
  Wayback captures of the official URLs (the live URLs 404/403/reset automated clients —
  measured routes, recorded in the answers' evidence); the three M-profile ARMs and the
  RP2040 datasheet already held corpus-side.
- Twelve materials adopted into `materials/catalog.sexp` (the three M-profile ARMs, three
  Cortex-M TRMs, FE310, i.MX RT1050 RM, MSP430FR59xx UG, SAM D21, STM32 RM0394 + PM0214)
  and fetched into `.materials/mcu/` with every sha256 re-verified — `materials --verify:
  64 verified / 0 unresolved` (52 at P5-BOARD.9 + the twelve). The corpus re-pinned
  `c4ad8a2` → `3dc4e62` (302 PDFs; 293 at the prior pin). All twelve requests marked
  `resolved` with their evidence.
- **Measured defect, fixed at root:** the `.1` survey measured the corpus's
  semulith-facing proposals feed only — the RP2040 datasheet was already adopted in our
  own catalog since 2026-09-14 (same sha256, cached), so one request was redundant from
  filing. No duplicate record adopted; the survey knowledge card gained the three-layer
  "already held" rule (tracked catalog + fetch cache + corpus tree, not just the feed).
  The tree closes (2/2).

## SEMULITH-MCU-0001 (leaf MCU-DOCS.1) — the MCU documentation set surveyed and requested through the chipdoc channel

- The director's `2026-10-02` steer (ARMs carry full MCU documentations; other vendors
  too — ask chipdoc) executed as documentation research, ahead of any MCU milestone
  (none owns MCU modeling yet — stated, not hidden). New tree:
  [`MCU-DOCS`](docs/tasks/MCU-DOCS.md).
- The survey measured the LIVE corpus feed (corpus `c4ad8a2` working tree, read-only):
  held — ESP32/C3/S3 and RP2040/RP2350 SVD register maps, the nRF52840 PS, the AM335x
  TRM (a Cortex-A8 SoC, not an MCU), the Arm PrimeCell/AMBA/GIC set (Cortex-A class);
  absent — every Arm M-profile architecture manual, every Cortex-M TRM, every vendor
  MCU datasheet/RM beyond the held trio.
- Twelve requests filed in `materials/requests.sexp` (the preferred channel): the three
  M-profile ARMs (v6-M/v7-M/v8-M), three Cortex-M TRMs (M0+/M3/M4), and six vendor
  documents (RP2040 datasheet, STM32 RM + PM0214, SiFive FE310, i.MX RT1050 RM, SAM
  D21, MSP430FR59xx). Pickup measured: the poller (read-only) reports exactly the
  twelve new ids, rc 1. One authoring defect (a heredoc paren over-close) caught by the
  one reader before landing — parse gates work.
- Fulfilment is chipdoc-side and asynchronous; a `MCU-DOCS.2` reconciles the answers
  when they arrive (the `P5-BOARD.9` pattern).

