# CHANGELOG shard — SEMULITH-P4-0032 … SEMULITH-P4-0030

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P4-0032 (leaf P4-SYSTEM.5, slice c) — the halted state, WFI's real wake, the `<halted>` vocabulary, the wake corpus

- The hart gains its wait state (decision 4): one ACTIVE/WAITING bit (Sail's
  `HART_WAITING` precedent), cold-ACTIVE at reset, engine-owned hart state on the
  TLB/reservation discipline — the state document's SEM-08 census declares the
  `hart wait state (ACTIVE/WAITING)` candidate and gen_state carries the bit (the
  RED arm 27→28). A legal WFI ENTERS the wait (the nop latitude recorded-not-taken);
  a halted step retires nothing, issues no fetch, and ticks the domain once; the
  step's head evaluates the wake — exactly `mip & mie != 0`, regardless of the
  global enables and of mideleg (RVP-MACHINE §2.1.3.3's musts, measured verbatim).
  On resume the taken-rule decides: trap with xepc = the WFI's pc + 4 (the
  section's own rule, which the generic between-instructions delivery computes
  for free) or pc + 4 continuation.
- The wake corpus (EVD-05, derived before any engine run): **w-timer** — THE
  acceptance cell: the timer's arrival during the halt wakes the hart and the trap
  is taken, and the handler's rdinstret reads 11 at its first step — the wake
  occurred **without CPU retirement**; **w-notrap** — wake-without-trap and the
  spec's idle-loop idiom (two halts, pc + 4 each); **w-deleg** — a delegated STI
  wakes an M-mode hart anyway ("even if it has been delegated"), no trap fires
  until un-delegated; **w-sw** — the software-posted SSIP/SEIP sources waking with
  the globals off. mm-wfi re-derives (decision 10): its legal cells halt with
  arranged timer wakes (the S cell's source delegated), the TW=1 and U trap cells
  measured unchanged. The expectations vocabulary gains the `<halted>` pseudo-step
  (decision 6 — empty writes, fetches 0). The corpus reads **99/99**; the other
  94 pre-slice guests are byte-identical (only mm-wfi contains wfi — the census).
- The matrix carries the wake family (28 cells resolve). `make check` rc=0,
  `make gate` green (DERIVED-COUNTS 429 → 430 re-derived — the wait-state RED arm).

## SEMULITH-P4-0031 (leaf P4-SYSTEM.5, slice b) — the step-head pending evaluation; both vector modes; the 7-guest corpus

- Pending is evaluated at the head of **every step** (decision 3): the (a)(b)(c)
  taken-rule + the global rule + the delegation mask + the fixed priorities
  MEI>MSI>MTI>SEI>SSI>STI with the M-source bits read-only 0 (decision 5).
  Delivery honors BOTH xtvec.MODEs (Direct = BASE, Vectored = BASE + 4×cause)
  with xcause = cause|(1<<63), xepc the un-fetched pc, xtval 0 (declared
  UNSPECIFIED) and the xPIE/xIE/xPP stack — `interrupts.rs` (pending/deliver + 8
  module tests), wired before the fetch; delivery steps tick the domain and
  retire nothing.
- The acceptance corpus: 7 new i-* guests with EVD-05 expectations derived BEFORE
  any engine run — the taken-rule per mode (i-accept), the enable immediacy
  (i-enable), the timer across the ticking domain (i-timer), the delegation mask
  with an S round-trip (i-deleg), the fixed-priority drain (i-prio), both vector
  modes with the synchronous trap keeping BASE (i-vector), and a nested delivery's
  stack restoration (i-nest): 290 steps, 13 fetch-less deliveries. The corpus
  reads **95/95**; the interaction matrix carries the 7 (28 cells resolve).
- Execution caught the authoring model's own defects and re-derived, never
  fitted: the derivation tool's inverted trap-entry stack (the engine was right —
  every prior trap had fired with MIE=MPIE=0), i-accept's mtvec delta 8 bytes
  long, i-timer's stimecmp authored against a retired-count clock, i-vector's
  SEIP-clear through read-only sip. The pre-slice census (0 interrupt writes in
  all 88 guests) made the identity proof unconditional: 88/88 demo traces
  byte-identical against the e37e664 engine.

## SEMULITH-P4-0030 (leaf P4-SYSTEM.5, slice a) — the declared virtual-time domain; mm-counters re-derived by design

- The laboratory's virtual-time domain advances **one tick per step boundary,
  retired or halted** (authority laboratory, the Zicntr §6.1 rate latitude, the
  brief's pre-condition 8 answered: progress is a pure function of the step
  index, so determinism and EVD-05's exact values hold by construction). The
  storage shape is ONE domain: `mcycle` holds it, `time` views it read-only
  ("cycle count might represent a valid implementation of RDTIME", §6.1) — the
  duplicate `time` row retires (CSR storage 33 → 32), and the state document
  carries the declared rate and the count rule as DATA (the `.3` TLB-parameter
  precedent; the census's `.5` reopen answered for the counter-progress part).
  `minstret` counts GENUINELY: +1 per retired instruction, never for a
  trap-delivered, reserved-decoding or halted step.
- The moving counters exposed a **latent defect**: `csr_read`'s view path
  computed the exposed mask from a view's DECLARED fields, so a field-less view
  masked to ZERO — the counter views would have read 0 forever (the `.2` zeros
  passed only because nothing moved). Fixed at root: a view declaring no fields
  is a full-width shadow of its owner — the statements' own meaning ("a
  read-only shadow of mcycle").
- mm-counters — the ONLY counter-reading guest of all 88 (the full census
  re-measured: 7 reads; **0 mip/sip readers**, so the STIP-at-reset quirk and
  the ticking STIP are unobservable in today's corpus; mm-stimecmp reads
  stimecmp only, clean) — re-derives 5 cells BY DESIGN (time at executed step k
  is k: 0/1/2/25/51; the gating traps 13/39 untouched), from the pinned chapters
  + the declared rate, never fitted (the `.2` IALIGN-16 precedent).
- `timekeeping.rs` carries the advance and 7 module tests (the ticking STIP:
  reset 1, cleared above time, arriving on the third tick; cycle==time on both
  read paths; cold-reset determinism; the ACCESS gates untouched). The corpus
  reads **88/88**; the other 87 guests are **byte-identical** against the parent
  engine (4,892 == 4,892 trace lines, both CLIs, worktree removed) — time
  ticking is invisible outside the counter reads, and the CLI/demo surface is
  unchanged. `make check` rc=0 (fmt + clippy `-D warnings` + 8 groups), `make
  gate` all green (DERIVED-COUNTS 429 unchanged). Next: slice (b) — pending
  evaluation + interrupt-caused delivery (both vector modes) + the acceptance
  corpus.
