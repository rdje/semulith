# CHANGELOG shard — SEMULITH-DR-0093 … SEMULITH-DR-0090

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-DR-0093 (leaf DSP-REVIEW.8) — the cross-vendor contrast: TI's absences are TI's, measured

- The review's first three leaves measured three TI manuals only, and its interim facts
  ("no accumulator", "no guard bits", "no bit-reversed addressing") risked reading as DSP
  properties. The two channel-answered manuals (`SEMULITH-DR-0092`) measured the contrast:
  **the inversion is real, twice over** — DSP56300 carries two 56-bit A/B accumulators
  with 8-bit extension registers (A2/B2, §3.1) and SHARC carries 80-bit MRF/MRB
  accumulators that name the guard bits outright (§3); bit-reversed addressing exists in
  both (DSP56300 reverse-carry modifier §4.5.2; SHARC BR0/BR8 §6).
- Three address-unit shapes (TI byte / DSP56300 24-bit word in P/X/Y / SHARC
  width-varies-by-space word), three circular-buffer alignment rules (align-to-size /
  2^k-aligned / arbitrary), three loop models (SPLOOP / DO+REP / DO UNTIL loop stack).
- SHARC's five-stage **interlocked** pipeline is the printed negation of TI's
  "eliminating pipeline interlocks" — the `.4` break (execute-packet progress, delayed
  visible writeback) re-scopes: it is **TI-family-shaped, not DSP-shaped**.
- Every contrast carries both vendors' locators; nine further manual defects recorded
  unresolved. Evidence: `docs/tasks/artifacts/dsp-review/2026-09-30-cross-vendor.md`.

## SEMULITH-DR-0091 (leaf DSP-REVIEW.6) — the synthetic stress fixture: the boundary pinned, not assumed

- `synth24` (24-bit registers, a second address space, a packet construct, a delayed
  effect) pushed through the REAL pipeline — every shape measured refused BY NAME, and
  the refusals are the pins: the width (`gen_state.py`: "masked fixed-width storage for
  nonstandard widths is generator work", rc 2), the space (`undeclared field
  "memory_spaces"`), the packet (`undeclared field "packet"`), the delayed effect
  (`undeclared operator "delay"`). Each probe descriptor reduced until its ONLY refusal
  is the shape under test.
- The tracked fixture `docs/tasks/artifacts/dsp-review/synth/` carries the SYNTHETIC
  banner everywhere and the citation ban verbatim; the suite is green (4/4) exactly
  while the boundary stands pinned — a shape becoming supported turns it RED, by design.
  This is `.4`'s break made executable: packets and delayed effects refuse at the
  schema layer today, so `.7`'s report can say WHERE the work lives.
- The two vendor gaps were answered same-day (chipdoc's 2026-09-30 DSP batch:
  DSP56300, full SHARC family, TigerSHARC, Blackfin, DSP56800E, DSP48E2) — adoption
  follows; the channel contract recorded as knowledge card `the-chipdoc-channel`.

## SEMULITH-DR-0090 (leaf DSP-REVIEW.5) — loops, repeats, interrupts: the SPLOOP census

- SPLOOP is C64x+-and-later only (measured by the compatibility fields); the loop state
  is fully enumerated (the loop buffer, the hidden LBC ×2, ILC with its 4-cycle load
  latency, RILC, the SPLX bit). Interrupts DRAIN to a stage boundary (short loops are
  not interruptible — the rule has its formula); exceptions do NOT drain (the buffer
  goes idle immediately); restart refills the buffer by re-executing SPLOOP under
  modified rules, the ISR's saves named (ITSR/NTSR, ILC, RILC).
- The acceptance's SEM-04 framing measured: per-instruction completion holds across
  interrupts (E1-entered completes through E5; annulled packets leave no state); the
  persistent loop progress is exactly ILC + the refill — and `.4`'s packet/window break
  stands beside it. Multi-access: LDDW/STDW/LDNDW, ≤2 accesses/cycle; load-multiple and
  non-temporal measured absent; MFENCE is C66x-only, its violated restrictions
  undefined-by-omission.
- Evidence: docs/tasks/artifacts/dsp-review/2026-09-30-loops-q12-q14.md.

