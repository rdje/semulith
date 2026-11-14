# Device regions: the hart reads once, and an atomic read crosses the boundary as its own kind

- **Type:** `decision`
- **Date:** `2026-11-14`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.20` slice e's brief, `SEMULITH-P4-0410`; the window's item "`OB-GC-ENV-DATA-ACCESS` superseded by a version that admits declared device regions" ([`decision_a-board-needs-a-contract-that-admits-devices.md`](decision_a-board-needs-a-contract-that-admits-devices.md), [`decision_the-next-window-is-version-1.md`](decision_the-next-window-is-version-1.md) item 5). The engineer's call under [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md).
answers: What must the CPU guarantee and the environment assume for a side-effecting device region, and does the boundary as it stands let a device refuse an access before it reads?

## What was measured

`target/p4-system-20/e-brief/device_read_census.rs`, a scratch test run in a throwaway clone of `0a2574c6`: every step of the 210 tracked guests through the real engine, each boundary request counted by kind and the step classified from its own fetched bits (census.log).

| Step's instruction | Steps | Data `Load` requests per step |
| --- | --- | --- |
| load, FP load, compressed load | 335 | 1 (287) or 0 (48: faulted before the read) |
| LR | 58 | 1 (50) or 0 (8) |
| AMO | 76 | 1 with its `Store` (59), 1 with no `Store` (2: the store refused), 0 (15) |
| SC | 67 | 0 always: a `StorePermission` (21), a `Store` (36), or neither (10) |
| any other instruction | 9,516 | 0 |
| a fetch that faulted | 39 | 0 |

No step issued a second `Load`, and no instruction outside the load class issued one: `guests 210, violations 0`. Fetches (`Fetch`, `FetchParcel`) and page-table reads (`WalkAccess`) already cross as their own kinds (`crates/semulith-core/src/env.rs`), never as `Load`.

## What measuring found

1. **The hart reads once.** On the corpus, a data read crosses the boundary exactly when an explicit read instruction asks for it, at most once, and never for SC or for an access that faults first. That is the CPU guarantee a device needs, and the census is its realized check.
2. **A device cannot tell an atomic read from a load.** LR and every AMO issue a plain `Load` (`exec_rv64gc.rs`, the `LoadReserved` and `Amo` arms). An environment therefore cannot refuse an atomic access to a device region before the read, and a device would see the side-effecting read of an AMO whose store then fails: measured, two AMO steps issued their `Load` and no `Store`.

## The call

1. **The boundary gains `AtomicLoad`,** the read of LR and of an AMO, answered as `Load` is in main memory. It is additive, as `StorePermission` (contract v2) and `WalkAccess` (v1) were: the plain-load path does not change, and the scalar engine has no atomics.
2. **Contract version 4 supersedes `OB-GC-ENV-DATA-ACCESS`** with a version that admits declared device regions: a device region's reads may have side effects; it answers `Load` and `Store` of its declared widths; it refuses `AtomicLoad`, `Fetch`, `FetchParcel` and `WalkAccess` with an access fault and no side effect, so no instruction is fetched from it, no page table lives in it, and no atomic touches it.
3. **A CPU guarantee joins it:** the hart issues at most one `Load` or `AtomicLoad` per explicit read instruction, at its translated address, and none for SC, for any other instruction, or for an access that faults before its read. The census, held to the tracked corpus, realizes it; its negative is an engine that reads twice.
4. **Order, corrected before e1 began:** one unit, not two. `OB-GC-ENV-EVENT-DELIVERY` enumerates the request kinds ("never while answering Fetch, FetchParcel, Load, Store, StorePermission or WalkAccess") and the atomics execution checks assert `Load` sequences, so `AtomicLoad` cannot enter the boundary without contract version 4 superseding that obligation and `OB-GC-ENV-DATA-ACCESS` in the same commit. Slice e lands the boundary kind, the engine (it moves, inside the window), every environment, the checks, contract version 4 with the read-once guarantee, and the census as its realized check. Whether MTIP and MEIP sources come in the same version (the window's open question) stays e2's to measure against P6's firmware.

## What this does not claim

- The census is finite: 210 guests, the forms they reach. It is a check over the corpus, not a proof over every program.
- A device's own behaviour is the device model's contract (`P5-BOARD`), not the CPU's.
