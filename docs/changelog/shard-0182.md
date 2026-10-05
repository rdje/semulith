# CHANGELOG shard — SEMULITH-P4-0006 … SEMULITH-P4-0006

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P4-0006 (leaf P4-SYSTEM.2, slice c1) — the privileged state constructs, the staged 33-CSR document, gen_state's rv64gc branch, the csr-set and reset-census gate arms

- Slice (c) split, recorded in the tree: **(c1)** schema + document + generator + gates,
  zero Rust; **(c2)** the engine-side consumption follows. `schema/state.sexp` gained
  `privilege_mode` (the current mode is hart state, not a CSR — the xPP/xPIE/xIE stack
  lives in mstatus) and the `csr` construct with per-field WPRI/WARL/WLRL tables
  (RVP-CSR §1.1.3.1–3), legalization rules, resets and locators per field, and `view_of`
  for the view CSRs (sstatus/sie/sip, the counter shadows — a view declares no storage).
- The rv64gc state document is authored and fully validated from `target/p4-system-2/`
  (placing it in profiles/ is a refused route contradiction until the flip): all 33 CSRs
  of D-CSR-SET with their tables — mstatus/sstatus with the stack and TSR/TW/TVM gates,
  mtvec/stvec BASE/MODE, medeleg with the brief's pinned delegatable subset (11 and 16
  read-only 0), mepc/sepc bit-1 writable at IALIGN=16, misa read-only at the declared
  value (a stated laboratory WARL choice), satp MODE restricted to Bare|Sv39, STCE, the
  counter-enables, the FP CSRs present-with-reset (behaviour is `.7`'s); §2.1.4's
  architectural resets cited, every UNSPECIFIED reset a stated laboratory value; the
  SEM-08 hidden-state census re-earned, naming what each later slice reopens.
- gen_state.py emits both profiles: rv64i's `state.rs` re-derives byte-identical; rv64gc
  emits (storage/mode/resets/field tables as data) to a scratch `--out`, rustc-clean —
  emission into crates/ switches on in (c2). The generator composes per-field resets and
  cross-checks the csr-level value; it fired RED *naturally* on the document being
  authored (mstatus's composite 0xA0000000 vs the hand-computed 0x300000000 — the
  descriptor was wrong, the check named it). Gate gaps closed: PROFILE-CONSISTENCY's
  csr-set cross-check, both directions (+3 self-test arms, 44 total; plus a `--csr-cross`
  staging probe), EXTRACTION's reset leg counts csrs and the mode (+3 arms), STATE-GEN
  +7 arms (17 total).
- Validation: all focused gates green, `make gate` green (DERIVED-COUNTS 385→395 arms).
  CSR name↔address ownership: migration deferred to the flip (a fact-ownership row cannot
  name an untracked owner); the state document's map is proven against the pinned
  csrs.csv (33/33 exact) and the probe is recorded in the leaf.

