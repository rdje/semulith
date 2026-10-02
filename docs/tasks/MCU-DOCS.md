# MCU-DOCS: the canonical MCU documentation set, researched and requested

## Metadata

- Tree ID: `MCU-DOCS`
- Status: `done` (`2026-10-02` — both leaves complete; the tree reopens the day a future MCU milestone needs documents this set does not cover)
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
  **Correction (`.2` execution, `2026-10-02`):** the survey measured the corpus's
  *semulith-facing proposals feed* — but that feed is not the whole measurement
  surface. The channel's answers measured what the feed-only survey missed: the three
  M-profile ARMs were already held corpus-side (adoption was still the right act — the
  corpus is not the tracked catalog), and the RP2040 datasheet was held twice over
  (corpus-side AND adopted in `materials/catalog.sexp` as `RP2040-DS` since
  `2026-09-14`, same sha256, cached) — one request was redundant from the moment it was
  filed. This is the `a-survey-that-found-things-can-still-have-missed-things` failure
  class recurring at a second layer; the card gained the recurrence and the
  complement-check rule. The request set's content stands (eleven of twelve were
  needed); the survey METHOD is what was wrong, and it is recorded here, per the card's
  own rule.

- ID: `MCU-DOCS.2` — **reconcile the channel's answers: adopt, verify, mark**
  Status: `done` (`2026-10-02`, `SEMULITH-MCU-0002`)
  Goal: consume the answers the channel delivered for `.1`'s twelve requests — verify
  the channel live first, adopt the fulfilled artifacts into `materials/catalog.sexp`
  with digests re-verified at fetch, mark every request with its answer and evidence,
  and re-pin the corpus.
  Acceptance: every adopted artifact's sha256 verifies from the cache
  (`scripts/materials.py --verify`); every request carries its answer; the survey
  defect found in execution is recorded with its fix (the `.9` discipline: a measured
  negative is an answer, and a measured defect is corrected at its records).
  Result (`2026-10-02`): the channel verified live first — `build_responses.py
  --report` → **12 fulfilled / 0 blocked, exit 0** (every open request answered). The
  routes, measured by the channel: the three Cortex-M TRMs from Arm's
  documentation-service API; FE310 from the SiFive CDN; MSP430 directly from ti.com;
  i.MX RT / SAM D21 / STM32 from Wayback captures of the official URLs (the live URLs
  404/403/reset to automated clients — measured routes, recorded in the answers'
  evidence); the three M-profile ARMs and the RP2040 datasheet already held
  corpus-side. **Twelve materials adopted** into `materials/catalog.sexp` (PM0214
  included as the STM32 answer's named second document) and fetched into
  `.materials/mcu/` with every sha256 re-verified (`materials --fetch`: 12 ok;
  `materials --verify: 64 verified / 0 unresolved` — the catalog moves 52 → 64
  materials, `.9`'s measured 52 + the twelve). The corpus re-pinned
  `c4ad8a2` → `3dc4e62` (5434 working-tree files / 302 PDFs, .git excluded; 5415
  tracked at HEAD — the PDF axis comparable to `.9`: 293 → 302). All twelve requests
  marked `resolved` with their evidence verbatim; REQ-MCU-RP2040-DS's answer records
  the measured redundancy (no duplicate record adopted). **Measured in execution, fixed
  at root:** (1) the `.1` survey defect (above) — the knowledge card gained the
  three-layer "already held" rule; (2) a heredoc paren over-close caught by the one
  reader before landing (`.1`); (3) the requests-file answer surgery initially nested
  `(answer …)` inside `(updated …)` — parsed but wrong-shaped against the house
  records; rewritten and verified per-field before commit.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| — | — | — | `.1`/`.2` done — the canonical MCU documentation set is acquired and digest-verified; the tree closes unless a future MCU milestone needs documents this set does not cover |

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

`MCU-DOCS.2` (`2026-10-02`, `SEMULITH-MCU-0002`):

- [x] **REPRODUCE / ISSUE** — the channel answered all twelve requests while ours still
  read `open` (the §0.3/§0.5 protocol: only WE flip our own file). Measured live before
  any edit:

  ```
  $ SEMULITH_ROOT=<repo> python3 <corpus>/scripts/build_responses.py --report
  REQ-MCU-* × 12   semulith=open  chipdoc=fulfilled   (rc 0 — every open request answered)
  ```
- [x] **ROOT CAUSE (WHY + WHERE)** — the answers exist per-request in the channel's
  `catalog/responses.sexp`; adoption is our act (`P5-BOARD.9`'s pattern). WHERE:
  `materials/catalog.sexp` (12 new records + the corpus re-pin), `materials/requests.sexp`
  (12 answers), `docs/tasks/MCU-DOCS.md`, the survey knowledge card. The measured
  discovery in execution: the RP2040 datasheet was already adopted as `RP2040-DS`
  (`git log -S RP2040-DS` → `3afd275`, 2026-09-14, MODEL-METHOD.13 — the *same* survey
  class's prior occurrence) — verified by digest equality
  (`be56fbb7…` both records), and the duplicate record was removed, not landed.
- [x] **FIX** — the 12 catalog records (digests measured from the corpus files and
  cross-checked against the answers' sha256 fields — all match), the fetch into
  `.materials/mcu/`, the 12 answer markings, the corpus re-pin with its census, the
  tree (`.1` correction + `.2`), the knowledge card.
- [x] **ADDRESSED (verified)** —

  ```
  $ SEMULITH_CHIPDOC_ROOT=<corpus> python3 scripts/materials.py --fetch <the 12 ids>
  ok × 12  (… sha256 verified)   — into .materials/mcu/
  $ python3 scripts/materials.py --verify
  materials --verify: 64 verified / 0 unresolved   (52 at .9 + the twelve)
  $ python3 -c '… S.read_file(Path("materials/requests.sexp")) …'
  22 requests; 0 still open
  $ bash scripts/check_doctrines.sh → === all doctrines green ===
  ```
- [x] **NO REGRESSION** — `bash scripts/check_doctrines.sh` → `=== all doctrines green
  ===`; the ten `.8` requests' records untouched (their resolved/blocked states and
  answers byte-preserved — the batch edits only appended, then flipped the twelve);
  the RP2040-DS record untouched (the duplicate was removed BEFORE the first
  candidate commit, verified by `git diff` showing no net change to that record).
- [x] **LOCKSTEP** — tree (`.1` correction + `.2` + checklist + logs + frontier closed),
  `docs/TASK_TREE.md`, `MEMORY.md`, `CHANGELOG.md`, the knowledge card (+ its INDEX
  already carries it), KNOWLEDGE_MAP regenerated. The DEV_NOTES lesson:
  promotion: promoted (the recurrence is recorded in the existing card
  `a-survey-that-found-things-can-still-have-missed-things.md` — the retrievable layer
  gained the three-layer "already held" rule).

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
| `2026-10-02` | `.2` | `build_responses.py --report` → 12 fulfilled / 0 blocked, exit 0; digests measured from the corpus files cross-checked against the answers' sha256 fields (12/12 match + PM0214); `materials.py --fetch` → 12 ok, sha256 verified into `.materials/mcu/`; `materials.py --verify` → 64 verified / 0 unresolved; requests.sexp parses, 0 open; `make gate` green | the twelve answers reconciled: twelve materials adopted and digest-verified, twelve requests marked resolved with evidence; the corpus re-pinned `3dc4e62`; the `.1` survey defect (the redundant RP2040 request) measured, recorded, and the card updated |
| `2026-10-02` | `.1` | `sexp.read_file` → the requests file parses (the one reader); `poll_semulith_gaps.py` read-only → exactly the twelve new ids, rc 1; `make gate` green | the survey measured, twelve requests filed and seen by the channel |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `.2` | `SEMULITH-MCU-0002 (leaf MCU-DOCS.2): the channel's twelve answers reconciled — adopted and digest-verified, requests marked, the survey defect recorded` | 12/12 fulfilled (Arm doc-service API, SiFive CDN, ti.com direct, Wayback routes measured); 12 materials adopted into `.materials/mcu/` (64 verified / 0 unresolved); corpus re-pinned 3dc4e62; the RP2040 redundancy measured and the survey card gained the three-layer rule |
| `.1` | `SEMULITH-MCU-0001 (leaf MCU-DOCS.1): the MCU documentation surveyed and requested — the Arm M-profile set + six vendor documents filed through the channel` | corpus survey over the live feed (held: ESP32/RP2040 SVDs, nRF52840, AM335x; absent: every M-profile ARM, every Cortex-M TRM, the vendor MCU RMs); twelve requests, each naming the steered consumer |

## Changelog

- `2026-10-02`: Created from the director's `2026-10-02` steer (ARMs carry full MCU
  documentations; ask chipdoc for the MCU documentation set). `.1` done the same day:
  the live-feed survey measured the holdings and the gap, twelve requests filed
  (`REQ-MCU-*`), pickup measured with the poller (read-only, exactly the twelve).
- `2026-10-02`: `.2` done (`SEMULITH-MCU-0002`) — the channel's answers reconciled the same
  day: 12/12 fulfilled, verified live first (`build_responses.py --report`, exit 0), twelve
  materials adopted into `materials/catalog.sexp` and fetched into `.materials/mcu/` with
  every sha256 re-verified (64 verified / 0 unresolved), all twelve requests marked
  `resolved` with their evidence, the corpus re-pinned `3dc4e62`. Measured in execution and
  fixed at root: the `.1` survey had measured the proposals feed only — the RP2040 datasheet
  was already adopted in our own catalog since 2026-09-14 (same sha256); the redundant
  request's answer records it, the duplicate record was removed before landing, and the
  survey knowledge card gained the three-layer "already held" rule. The tree closes.
