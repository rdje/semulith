# CHANGELOG shard — SEMULITH-P4-0033 … SEMULITH-P4-0033

> Sharded from `CHANGELOG.md` under its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P4-0033 (leaf P4-SYSTEM.5, slice d) — the Sail matched attempt; the LEAF CLOSES

- The matched attempt, scoped to what is matchable (decision 9). The override is
  measured first: materialized fresh from the tracked unit (unchanged since
  bfa6aaa), validate-config rc=0, NO change needed — and verdict-neutral (the
  `.4` corpus re-run under it reproduces 11 AGREE + 1 NAMED of 12 exactly). The
  13 ELFs build at exactly 0x8000_0000 (.word-only + PHDRS, the tracked
  assembler owning the bytes).
- Against the matched configuration the software-posted-bit cells match exactly:
  **6 AGREE of 12** (i-accept 36, i-deleg 60, i-enable 21, i-nest 31, i-vector
  53, w-sw 17 — 218 steps of change-observations). Sail numbers the
  interrupt-delivery step and prints no row (i-accept's trace jumps [9]→[11]) —
  the same convention the laboratory declares, the `.3` fetch-fault shape.
- The **6 NAMED divergences are all platform-shaped, never semantic**: Sail's
  timer block gates on `plat_have_clint`, so STIP never sets without a CLINT
  (i-prio step 24: sail x13=2 vs 34; i-timer step 3: sail x7=0 vs 32); Sail's WFI
  is a nop under the matched platform, so the real halt has no counterpart
  (w-deleg 12, w-notrap 6, w-timer 11, mm-wfi 9 — 'sail printed a row for the
  `<halted>` step'); and mm-wfi's TW cell is the `.2` named gap freshly measured
  with the isolated probe — DIVERGE under the matched config (Sail never judges
  TW: the judgment lives only in the wait-exit path the nop never reaches),
  AGREE 30/30 under the wfi-wait variant with the delivered trap identical
  (cause 2, mepc = the wfi's pc, xtval = the wfi's word).
- The matrix invocation resolves 28 cells with the three RED legs fired by name
  (ORPHAN GUEST / OMITTED CELL / UNKNOWN DIFFERENCE); references.sexp records
  the fourth experiment. **The LEAF ACCEPTANCE is w-timer's own run**: three
  boundaries with no register observation (the two `<halted>` steps and the
  delivery), the handler's first read rdinstret = 11 — nothing retired across
  the halt — then the timer trap with mcause = Interrupt|5 and mepc = the wfi's
  pc + 4. The timer wake occurred **without CPU retirement**. `make check`
  rc=0, `make gate` green (DERIVED-COUNTS 430), smoke-bench 53 arms, bench wasm,
  both books. Frontier → `.6` (instruction visibility and fence semantics).

