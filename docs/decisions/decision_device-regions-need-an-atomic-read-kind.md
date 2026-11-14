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

## What implementing it found (slice e, `SEMULITH-P4-0412`, 2026-11-14)

1. **A device refuses SC's permission check too.** `StorePermission` is issued by one site only, a nonmatching SC (`git grep -n 'Request::StorePermission' -- crates/semulith-core/src` lists `exec_rv64gc.rs` alone), and an SC to a device is always nonmatching: the reservation is keyed on the physical address, and LR to a device is refused first. Refusing it, with cause 7, makes "no atomic touches it" true of SC as well; answering it would let an SC complete against a device with code 1. Version 4 lists five refused kinds, not four.
2. **A guest's `load` refusal covers the atomic read.** The generated vocabulary defines `RefusalKind::Load` as "an explicit read", and `store` already covers `StorePermission`; so `AtomicLoad` answers to it, and every guest's experiment is unchanged (the 210 guests compare as before).
3. **The answer is `Response::Load`.** An atomic read and a load return the same raw bits under the same width rule; only the request kind differs, which is all a device needs to tell them apart.
4. **The device auditor needs a typed violation of its own.** `ContractViolation::DeviceRefusalBroken { request }`, a fixture auditor's report beside `ResponseValueMismatch`: the CPU cannot see a region map in an answer's shape.
5. **MTIP and MEIP sources do not come in version 4.** Item 4 left them to be measured against P6's firmware. `P6-LINUX` has not selected one (its Open Questions: "Which firmware implementation. Due before `.2`."), so there is no need to measure against yet, and the netboard is polled, with no timer or interrupt controller. Version 4 admits device regions alone, and a later version supersedes `OB-GC-ENV-INTERRUPT-SOURCES-V2` once the firmware names its sources.
6. **The counts:** 58 effective obligations and 116 realized checks (57 and 114 before): three members, two supersessions, and the two superseded records' checks moved to their successors with their evidence.

## What this does not claim

- The census is finite: 210 guests, the forms they reach. It is a check over the corpus, not a proof over every program.
- A device's own behaviour is the device model's contract (`P5-BOARD`), not the CPU's.
