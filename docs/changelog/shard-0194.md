# DEV_NOTES shard — _(2026-10-04)_ … _(2026-10-04)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-04)_ — the enum-addition census; parcels coalesce, the request shape is the contract (P4-SYSTEM.3 slice b)

Execution of the `.3` brief's checkpoint (b) measured:

- **Adding one enum variant is a census, and the compiler is the census-taker.**
  `Request::WalkAccess` broke three exhaustive matches, and each site got its own
  profile's honest answer: FlatMemory ANSWERS it (8-byte aligned region read,
  never a fetch — the one-fetch-per-step census keeps its meaning), the bench's
  Counting census gains a `walks` field (zero on the rv64i bench by construction),
  and rv64i's TestEnv panics named (the base profile has no translation
  machinery — a fixture seeing the variant is a test bug, not an answer). The
  alternative — a wildcard arm anywhere — is the silent-lie shape every gate here
  exists to refuse.
- **The request shape is the contract; the parcel split is machinery under it.**
  Decision 5's 16-bit fetch parcels are required by the C slot's straddle, but
  the corpus pins one `Request::Fetch` per step. The resolution is WHERE the
  coalescing is defined: not "one fetch per step" as an invariant to break and
  apologize for, but "one request whenever both translated parcel addresses share
  one physical 32-bit unit" — a rule that is every case under Bare (byte-exact
  today) and that names the page-straddle case as slice (c)'s own case rather
  than silently coalescing it. The proof is two-layer: the fetch-count
  assertions (1/step, every guest) and a full byte-level diff — both CLIs, the
  parent commit's and this one, over all 62 guests: 1,884 == 1,884 lines, `cmp`
  clean. "Bare is an exact identity path" is now a byte-measured sentence, not a
  design hope.
- **The unimplemented case names its slice.** A scratch probe (satp.MODE=Sv39,
  drop to S, `ld`) produces `model error: Unimplemented { what: "Sv39 translation
  — the walk is P4-SYSTEM.3 slice (c)'s" }`, cli rc=1 — the machinery shell's
  honesty: the walk entry can never answer wrong, because it answers by name.
- **Validation:** 6 translation unit tests (Bare-identity, M-never-translated,
  the sub-M walk entry, MPRV selects MPP for data accesses only with SUM/MXR
  carried, the out-of-vocabulary satp.MODE named panic, the 12/13/15 vocabulary);
  the corpus 62/62 with fetch counts unchanged; `make check` 8/8 groups;
  `make gate` all green (DERIVED-COUNTS 422 unchanged — the new arms are cargo
  tests, not gate census members); smoke-bench 53 arms, bench wasm, both books.
  Promotion: declined (the enum-addition ripple is structural — the compiler
  names every match site, and this slice's checklist records the dispositions).

