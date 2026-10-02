# MCU-DOCS: the canonical MCU documentation set, researched and requested

## Metadata

- Tree ID: `MCU-DOCS`
- Status: `active`
- Roadmap lane: director steer `2026-10-02` — MCU modeling ("ARMs as full documentations
  of MCUs, maybe others vendors too"). No milestone owns MCU modeling yet; this tree is
  the documentation-research input, exactly the role `P5-BOARD.8`/`.9` played for the
  board — research is an input to a future milestone, not the milestone's execution.
- Gate: none of its own (the channel's protocol checks are the verification: the one
  reader parses the file; chipdoc's poller sees exactly the new ids)
- Created: `2026-10-02`
- Owner: repo-local workflow

## Goal

Measure what the corpus already holds for MCU modeling, then file acquisition requests
through the chipdoc channel for the canonical missing set — the Arm M-profile
architecture manuals and Cortex-M core TRMs the director named, plus a measured set of
vendor MCU register documents — so a future MCU milestone inherits sourced candidates,
never a device without a source.

## Non-Goals

- No MCU milestone, profile, or model — no roadmap scope is invented here. The requests
  are documentation acquisition, not a commitment to model any specific MCU.
- No re-requesting what the corpus already holds (the `.8` discipline: the survey is
  measured, so nothing held is churned).

## Acceptance Criteria

- `materials/requests.sexp` parses with the one reader; chipdoc's poller (read-only)
  sees exactly the new request ids; nothing the corpus already holds is re-requested;
  every request names its consumer honestly (the steered direction, not a milestone).

## Task Tree

- ID: `MCU-DOCS`
  Status: `active`
  Goal: the canonical MCU documentation set researched and requested
  Children: `MCU-DOCS.1`

- ID: `MCU-DOCS.1` — **the MCU documentation survey + acquisition requests**
  Status: `done` (`2026-10-02`, `SEMULITH-MCU-0001`)
  Goal: survey the live corpus feed for MCU holdings; file the requests for the measured
  gap; measure the channel's pickup.
  Acceptance: `materials/requests.sexp` parses with the one reader; chipdoc's poller
  (read-only) sees exactly the new ids.
  Verification: `2026-10-02` — the Verification Log below.
  Result (`2026-10-02`): the survey measured the live corpus feed (working tree at
  corpus `c4ad8a2` plus its uncommitted gap records — read-only, §21): **held** —
  ESP32/C3/S3 SVDs (SVD-ESPRESSIF), RP2040/RP2350 SVDs (SVD-RASPBERRY-PI), the nRF52840
  Product Spec (adopted `.9`, NORDIC-NRF52840-PS), the AM335x TRM (Cortex-A8 SoC, not an
  MCU), the Arm PrimeCell TRMs and AMBA/GIC specs (Cortex-A/board class); **absent** —
  every Arm M-profile architecture manual (v6-M/v7-M/v8-M), every Cortex-M core TRM,
  and every vendor MCU datasheet/reference manual beyond the held radio/ESP32/nRF52
  trio (the CMSIS-SVD format record is corpus-side `wanted`, its own tracked gap).
  Twelve requests filed (`materials/requests.sexp`): the three M-profile ARMs, three
  Cortex-M TRMs (M0+/M3/M4), and six vendor MCU documents (RP2040 datasheet, STM32 RM +
  programming manual, SiFive FE310, i.MX RT1050 RM, SAM D21, MSP430FR59xx) — each
  naming this steer as its consumer, with the honest note that no milestone owns MCU
  modeling yet. Pickup measured: `poll_semulith_gaps.py` (read-only) reports exactly
  the twelve new ids, exit 1. Fulfilment is chipdoc-side and asynchronous; each
  request's status flips when the feed mirrors it.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| — | — | — | `.1` done; the tree idles until the channel answers (a `.2` reconciles the answers when they arrive — the `.9` pattern) |

## Decisions

- `2026-10-02`: the request set is **the Arm documentation the director named plus one
  measured vendor spread** — not every MCU document that exists. The ARM set covers the
  architecture (v6-M/v7-M/v8-M) and the canonical cores (M0+/M3/M4); the vendor set
  covers the classes the project will actually choose among (a modern dual-core hobby
  MCU with full public docs — RP2040; the dominant vendor line — STM32; the RISC-V MCU
  — FE310, this project's own spine; a crossover — i.MX RT; a classic Cortex-M0+ — SAM
  D21; the ultra-low-power classic — MSP430). ESP32-C3, RP2040-SVD and nRF52840 are
  already held, so those vendors are not re-requested.
- `2026-10-02`: Arm documentation licence terms are the channel's to measure — Arm
  serves its manuals from developer.arm.com behind a click-through; whether a route
  exists is a measured answer (fulfilled/blocked), never an assumption. A `blocked`
  answer is an answer (the `.9` discipline).

## Open Questions

- Which MCU gets modelled first — **not this tree's**; the milestone that opens MCU
  modeling decides, with this documentation set as its input. The answer depends on
  which requests fulfil.

## Blockers

- None.

## Acceptance Checklist (filled per leaf at execution time)

`MCU-DOCS.1` (`2026-10-02`, `SEMULITH-MCU-0001`):

- [x] **ROOT CAUSE (WHY + WHERE)** — the MCU direction has no documentation position:
  the measured corpus survey (the LIVE feed, corpus `c4ad8a2` working tree, read-only):

  ```
  $ grep -icn "stm32\|msp430\|samd\|imxrt\|fe310\|nrf52\|cortex-m\|armv6-m\|armv7-m\|armv8-m" <live feed> → the only hits are the held SVDs' own records
  held: SVD-ESPRESSIF, SVD-RASPBERRY-PI, NORDIC-NRF52840-PS (adopted .9), TI-AM335X-TRM
  absent: every Arm M-profile ARM, every Cortex-M TRM, every vendor MCU RM beyond the trio
  ```

  WHERE: `materials/requests.sexp` (the preferred channel — the watcher fires on the
  file), `docs/tasks/MCU-DOCS.md` (the owning tree).
- [x] **ADDRESSED (verified)** — the file parses with the one reader and the channel
  sees exactly the new ids:

  ```
  $ python3 -c '… S.read_file(Path("materials/requests.sexp")) …'
  22 requests parse; 12 open: REQ-MCU-ARMV7M-ARM, REQ-MCU-ARMV6M-ARM, REQ-MCU-ARMV8M-ARM,
  REQ-MCU-CORTEX-M3-TRM, REQ-MCU-CORTEX-M0P-TRM, REQ-MCU-CORTEX-M4-TRM, REQ-MCU-RP2040-DS,
  REQ-MCU-STM32-RM, REQ-MCU-FE310, REQ-MCU-IMXRT-RM, REQ-MCU-SAMD21-DS, REQ-MCU-MSP430
  $ SEMULITH_ROOT=<repo> python3 <corpus>/scripts/poll_semulith_gaps.py   # read-only
  NEW REQUESTS (12) [source=requests]   (rc 1 — the channel's "new requests" signal)
  $ bash scripts/check_doctrines.sh → === all doctrines green ===
  ```

  One authoring defect caught by the one reader before landing: the heredoc's `(doc …))`
  lines over-closed each request form — `SexpError: ')' with no matching '('` named the
  line; fixed and re-parsed, never committed broken.
- [x] **NO REGRESSION** — `bash scripts/check_doctrines.sh` → `=== all doctrines green
  ===`; the ten prior requests untouched (the batch appends; the parser census counts
  22 = 10 prior + 12 new).
- [x] **FIX** — `materials/requests.sexp` (+12 requests + the batch survey note),
  `docs/tasks/MCU-DOCS.md` (the tree), `docs/TASK_TREE.md`, `MEMORY.md`,
  `CHANGELOG.md`.
- [x] **LOCKSTEP** — tree + index + MEMORY + CHANGELOG; the DEV_NOTES lesson:
  promotion: declined (the paren defect was caught by the one reader at once — a parse
  gate doing its job is not a lesson; the channel mechanics are already carded in
  `docs/knowledge/the-chipdoc-request-channel.md`).

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-10-02` | `.1` | `sexp.read_file` → the requests file parses (the one reader); `poll_semulith_gaps.py` read-only → exactly the twelve new ids, rc 1; `make gate` green | the survey measured, twelve requests filed and seen by the channel |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `.1` | `SEMULITH-MCU-0001 (leaf MCU-DOCS.1): the MCU documentation surveyed and requested — the Arm M-profile set + six vendor documents filed through the channel` | corpus survey over the live feed (held: ESP32/RP2040 SVDs, nRF52840, AM335x; absent: every M-profile ARM, every Cortex-M TRM, the vendor MCU RMs); twelve requests, each naming the steered consumer |

## Changelog

- `2026-10-02`: Created from the director's `2026-10-02` steer (ARMs carry full MCU
  documentations; ask chipdoc for the MCU documentation set). `.1` done the same day:
  the live-feed survey measured the holdings and the gap, twelve requests filed
  (`REQ-MCU-*`), pickup measured with the poller (read-only, exactly the twelve).
