# CHANGELOG shard — SEMILITH-PL-0004 … SEMILITH-PL-0004

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMILITH-PL-0004 (leaf P1-LAB.4) — the environment boundary, and fixtures that answer it

- `semulith-core::env` owns the request/response contract the CPU crosses: `Request` (Fetch — width pinned to 32 by construction, OB-ENV-FETCH-SUPPLY; Load/Store at `AccessWidth` B/H/W/D, OB-ENV-ACCESS-WIDTHS — an unofferable width cannot be formed), `Response` (raw bits, no extension — REQ-D-LOAD-EXT stays instruction-layer), and two failure families kept apart by construction: `Failure` (target-facing: AccessFault, Misaligned — the profile's "not substituted" rule) and `ContractViolation` (the environment broke a rule; SEM-01's separation, boundary-local until `.5`). One trait, `Environment::request`, drives every crossing. Addresses are bare `u64` (SEM-05).
- `semulith-verify::fixtures` implements it: `FlatMemory` — one little-endian main-memory region, no side effects (OB-MAIN-VS-IO), re-read per fetch so stores are immediately visible (OB-CODE-VISIBILITY), fetch counter as the no-extraneous witness, alignment judged before region membership (stated, tested); `ScriptedEnv` — the conversation pinned in advance, faults scriptable, and a request the script does not cover reports `ResponseMismatch`/`ScriptExhausted` instead of inventing data (§4.1.4's negative-fixture rule, exercised for real).
- Verification: 16 new suites green (12 fixture + 4 contract-property), all without an instruction handler; `make check` 5 suites / 42 tests / 0 warnings; wasm build green; `make gate` green.
- Lockstep: MEMORY/LIVE_STATUS/TASK_TREE/book P1 chapter and this tree; frontier moves to `.5` (typed outcome families).

