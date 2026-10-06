# DEV_NOTES shard — _(2026-10-03)_ … _(2026-10-03)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-03)_ — the Sail attempt measured its own boundary; the validator argued for the corpus (P4-SYSTEM.2 slice h, part 2 + leaf)

Execution of the `.2` brief's decision 8 measured:

- **The config namespace can express almost all of the match — and says so
  precisely.** Sail 0.14's override validator refused three things, and each
  refusal was information: "Zicntr is enabled but there is no source of time" (a
  CLINT is mandatory for Zicntr — our platform declares no devices, so the
  counter guests are non-matchable BY CONSTRUCTION, not by failure); "bit 11
  (ecall from M) cannot be delegated" (the validator knows the very rule
  mm-ecall-deleg exists to prove); "bits for reserved exceptions" (cause 10 is
  reserved with H off). The matched medeleg mask (0x3FF) was derived by bisecting
  the validator, not by reading docs. And `mideleg.delegatable_bits.len` is the
  string "xlen" in the default config — a string-typed value no uint64 override
  can merge over; the key was dropped (the corpus never touches mideleg), the
  override staying honest about what it configures.
- **The comparison rule matters more than the runner.** Sail's `--trace-gpr`
  prints every architectural write; the corpus's rule is CHANGE-observations (a
  register written its own value is no observation). Normalizing Sail's trace to
  the corpus's rule is what makes 11/12 guests read AGREE step-for-step — and
  the two parser bugs along the way (Sail prints `0x0000` for a compressed
  c.illegal — 4 hex digits, not 8; the run's end convention is a budget, not a
  stop) were the day's reminder that every comparison is itself a measurement.
- **A divergence with the bit provably set is a model gap, not a config miss.**
  mm-wfi's TW=1-in-S cell: Sail retires the wfi as a nop (`wfi_is_nop=true`) or
  waits forever (`false`), but never traps — while mm-readonly's all-ones
  mstatus read-back AGREEs bit-exact (`0x8000000A007E79AA`, bit 21 included),
  proving mstatus.TW is writable and read back in the same configuration. There
  is no TW knob in the config schema. The expectation stands on RVP-INSNS (TW=1
  makes WFI illegal below M); the gap is Sail 0.14's, named and routed to
  P4-SYSTEM.5, whose brief already owns WFI's wake semantics.
- **The tracked-artifact evidence chain.** The override's truth is the tracked
  `.sexp` (the rv64i pattern); the JSON is derived. The experiment re-ran
  against the derived JSON — "11/12 AGREE against the tracked override's
  derived JSON" — so the commit's artifact and the experiment's config are the
  same bytes by construction, not by claim. The dossier format learned the
  override's new keys at the owner (schema optional fields + the mapping both
  directions; self-test 13→14; the round-trip field-for-field exact).
- **Validation:** the matched override schema-valid and round-trip exact;
  `make check` 8/8 groups; `make gate` all doctrines green (DERIVED-COUNTS 419
  unchanged). The leaf's acceptance — the same instruction's behaviour tested
  in each supported mode — is the mode matrix itself (13 guests, every cell a
  mode crossing; 62/62 tracked-engine falsification; 11 full AGREE + 1 partial
  against Sail). Promotion: declined (the TW finding's routing is recorded in the
  leaf's checklist and the counter-rate policy is the profile's declared datum).

