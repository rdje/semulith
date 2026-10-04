# CHANGELOG shard — SEMULITH-P5-0016 … SEMULITH-P5-0015

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P5-0016 (tree P5-BOARD) — the `.4` design brief: the verdict's shape and the four dispositions decided

- The verdict's shape recorded before execution: the mechanical discharge (green at
  8/8 — but its platform-dependent edges land on `OB-PLATFORM`, the laboratory
  guarantee) re-established at content level by the declared `satisfies` edges plus
  four composition dispositions; a re-runner required (the MODEL-COMPOSE.4 lesson).
- Four composition records, not three: `OB-NIC-STRAP-RESETS` (the strap values) joins
  TIME-SOURCES / PHY-LINK / GPIO-PINS. Dispositions decided from the pinned datasheet:
  D32 tied high (§3.6's native 32-bit mode; EEDIO has no internal pull — an explicit
  board tie), SPEED_SEL unwired to its pull-up, the time sources frozen, the link
  scene static-complete at 100BASE-TX FD, the pin reads tied off at 0.
- The measured defect the brief caught: eth0's declared 16-bit width is mode-exclusive
  per §3.6 and narrows to 32 with the leaf.

## SEMULITH-P5-0015 (leaf P5-BOARD.12) — the two-tier per-part ceiling: authored content bounded, regeneration-gated derived members exempt as a checked property

- The director-delegated ruling (`SEMULITH-P5-0014`,
  `decision_derived-members-of-bounded-families`) executed: the per-part byte
  ceiling's founding failure mode — silent accretion in hand-maintained files —
  cannot occur in a regeneration-gated file, so the instrument now matches the
  failure mode. Authored members keep the **65,536** ceiling (the day-old 128 KiB
  interim raise reverted; `decision_profiles-family-composed-units` superseded in
  part); derived members are exempt **as a checked property** — a
  `doctrine/fact_ownership.tsv` mirror row with a regeneration-doctrine governor
  (the closed set: STATE-GEN, DEF-GEN, GUEST-GEN, BOARD-GEN, GATE-REPORT,
  MATERIALS-BILL, BOOK-INDEX) — never as a declaration.
- `scripts/check_readme_routes.sh`: `derived_exempt` consumes the FACT-OWNERSHIP
  registry (already completeness-checked — no second declaration surface);
  `regen_set_registered` refuses set/driver drift so the exemption can never silently
  widen; the per-part loop now judges EVERY over-ceiling member (it previously
  inspected only the biggest) — exempt members are reported as proof, the rest fail
  by name. Aggregates untouched.
- Real-corpus verdict: both composed catalogues (104,372 / 94,027 B) exempt with
  proof printed; the NIC's authored 60,112 B catalogue under the restored authored
  ceiling (0.92×) — the rule discriminates exactly as ruled. Self-test 12 → 17 arms
  (17/0; the RED authored-fail paths fire on fixtures, the real corpus's authored
  members being correctly under the ceiling). Measured in execution: a new
  `armregen` helper idiom made 2 arms invisible to DERIVED-COUNTS' enumerator
  (357 ≠ 359) — folded into `arm`'s optional `[cmd...]` probe form instead.
- The lesson PROMOTED: `docs/knowledge/a-byte-ceiling-applies-to-authored-content.md`
  (+ INDEX) — the instrument must match the failure mode.
- Validation: `make gate` → all doctrines green (DERIVED-COUNTS re-derived 354 →
  359 arms); `mdbook build` rc 0; `gen_book_index.py --check` rc 0. No Rust surface
  touched. P7's soc/computer compositions inherit the rule.

