# CHANGELOG shard — SEMULITH-P4-0016 … SEMULITH-P4-0016

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P4-0016 (leaf P4-SYSTEM.3, slice b) — the translation module + hooks + effective mode; the Bare-identity proof byte-exact

- The translation machinery shell lands as evaluator machinery (the brief's
  decisions 3–6): `crates/semulith-core/src/translation.rs` beside `privilege.rs` —
  the effective-mode computation as ONE computation (RVP-MACHINE §2.1.1.6.4: fetch
  uses the current mode and M-mode fetch is never translated; loads/stores use
  mstatus.MPP when MPRV=1, with SUM/MXR carried for the walk); satp.MODE dispatch
  (M-effective and Bare are exact identity; Sv39 enters `Translate::Walk` — slice
  (c)'s entry, until then the named unimplemented case, never a wrong answer; an
  out-of-vocabulary satp.MODE is a named panic); the page-fault causes 12/13/15
  entering core as raw u64 with the typed-enum asymmetry stated (the privileged
  engine's causes are delivered raw through the one trap-deliver path).
- The three hooks wired in `exec_rv64gc.rs` (fetch at :87, load :291, store :328 —
  the brief's own locators): fetch in 16-bit parcels (decision 5) with the
  recorded coalescing choice — parcels translate independently, and the fetch
  issues exactly one `Request::Fetch` whenever both translated addresses share one
  physical 32-bit unit, which under Bare is every case, so the Bare request shape
  is byte-exact by construction (the corpus's one-fetch-per-step assertions hold
  it); loads and stores translate after the model-side misalignment check (the
  pinned implementation-defined priority, decision 7).
- The walk-access boundary variant enters the engine's vocabulary:
  `Request::WalkAccess { addr }` + `Response::WalkAccess(u64)` — 8-byte physical,
  read-only by construction under Svade (the D-FETCH-IMPLICIT precedent applied;
  the formal contract wording routed to `.9`, recorded). Its three exhaustive-match
  dispositions: FlatMemory answers it (8-byte aligned region read, never a fetch —
  the one-fetch-per-step census keeps its meaning), the bench census gains
  `walks`, and rv64i's TestEnv panics named (the base profile has no translation
  machinery).
- The Bare-identity proof is byte-level and complete: both CLIs (the parent
  commit's engine and this one, via a scratch worktree) drive all 62 guests and
  1,884 trace lines compare `cmp`-clean — beside the standing cargo assertions
  (62/62, per-step writes, step counts, never_written, fetch counts, cold-reset
  determinism) and the Sv39-entry probe (an S-mode `ld` with satp.MODE=Sv39 →
  `model error: Unimplemented { what: "Sv39 translation — the walk is P4-SYSTEM.3
  slice (c)'s" }`, cli rc=1 — the entry names itself, never a wrong answer).
  rv64i's engine untouched; 6 translation unit tests (Bare-identity,
  M-never-translated, the walk entry, the MPRV rule, the named defect, the cause
  vocabulary); `make check` 8/8 groups, `make gate` all green (DERIVED-COUNTS 422
  unchanged), smoke-bench 53 arms, bench wasm, both books.
  Next: slice (c) — the 10-step walk with its fault matrix, the reserved-bit and
  superpage checks, and the REQ-D-FETCH-IMPLICIT amendment.

