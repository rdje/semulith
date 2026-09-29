# CHANGELOG shard — SEMILITH-PL-0005 … SEMILITH-PL-0005

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMILITH-PL-0005 (leaf P1-LAB.5) — four typed outcome families, SEM-01 made structural

- `semulith-core::outcome`: `TargetEvent` (`Exception` with the unprivileged cause vocabulary, each cause named by its rule; `RequestedTrap` for ECALL/EBREAK — delivery is a data event, not a stop command), `Advance` (`Completed`, `Stop{reason}` — no waiting/partial advance, platform facts recorded in the docs), `ModelError` (`Unimplemented`/`InvalidDescription`/`InconsistentState`/`ContractViolation` — `.4`'s boundary-local violation re-homed), `UndefinedCase` (`ReservedDecode` — REQ-D-RESERVED-DECODE's case carried as its own outcome, never auto-converted to an exception). `StepOutcome` is the step-level sum `.8` produces and the harness matches.
- The acceptance proven by a stub stepper (test code, not production semantics): `a_delivered_exception_lets_execution_continue` (harness records the `Breakpoint` trap, the next instruction still runs, pc advances past all three); `an_unimplemented_instruction_is_not_an_illegal_instruction_trap` (the `Failed` arm has no typed expression that reaches an `IllegalInstruction` `Exception`). Plus family distinctness, the `ContractViolation` re-home round trip, and `UndefinedCase` ≠ `Exception`.
- Verification: 5 new suites green; `make check` 5 suites / 43 tests / 0 warnings; wasm build green; `make gate` green.
- Lockstep: MEMORY/LIVE_STATUS/TASK_TREE/book P1 chapter and this tree; frontier moves to `.6` (canonical definition skeleton).

