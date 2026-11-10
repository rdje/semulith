# What a CSR write keeps: a defect in the pinned author, a selection to narrow, and differences that stay

- **Type:** `decision`
- **Date:** `2026-11-06`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a50-3, `SEMULITH-P4-0374`; found drafting a `medeleg` witness at a50-2; the call is the engineer's under [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md).
answers: Do the expectations author, the lab engine and the pinned reference agree on what a CSR write keeps, and what happens about each place they differ?

## The fact / decision

`target/p4-system-14/a50-3/csr-write/census.py` writes all ones to each of 23 CSRs, one guest per CSR, and reads the value back on all three producers under the profile override. 14 agree: `mideleg`, `mepc`, `sepc`, `mtval`, `stval`, `mscratch`, `sscratch`, `sie`, `mip`, `sip`, `stimecmp`, `fflags`, `frm`, `fcsr`. Nine differ:

| CSR | Author | Engine | Reference | What the difference is | Call |
| --- | --- | --- | --- | --- | --- |
| `medeleg` | `0xffffffffffffffff` | `0x1cf7ff` | `0xb3ff` | The author ignores the state table. The engine keeps bits 10, 14 and 18 to 20, which the override's `delegatable_bits` leaves out | Fix the author and narrow the table, next window |
| `mtvec`, `stvec` | `…fd` | `…fc` | `…fc` | The author takes bit 0 of the reserved MODE 3, where the table's `one-of 0 1` keeps the old value | Fix the author, next window |
| `mcause`, `scause` | all ones | all ones | `0` | WLRL, and an illegal value may read back as anything | Stays |
| `mie` | `0xaaa` | `0xaaa` | `0x222` | All 32 retained configurations turn the reference's machine interrupts off, so it holds the S bits only | Stays |
| `mcounteren`, `scounteren` | `0x7` | `0x7` | `0xffffffff` | The lab implements CY, TM and IR, and the reference holds the whole word | Stays |
| `menvcfg` | bit 63 | bit 63 | bit 63 and bit 0 | The lab's table keeps bit 0 WPRI, and the reference implements it | Stays |

1. **The author has a real defect, in two places.** Its docstring and the state table say per-field legalization. `medeleg` falls through to a plain store, and `mtvec` and `stvec` compute MODE as `v & 1`. The lab engine follows the table in both.
2. **No retained expectation reaches it.** Every value that the 164 guests the author can derive write through its own write path (`target/p4-system-14/a50-3/csr-write/guest_writes.txt`): 11 `medeleg` writes, 8 distinct values, all inside both masks; 81 `mtvec` and `stvec` writes, all MODE 0. The other 34 guests are outside the author's scope, so it produced none of their expectations.
3. **It fails safe.** A wrong expectation reads as a divergence against the reference, which is how this was found: the drafted witness was refused, never credited.
4. **The table should narrow to `0xb3ff`.** The specification lets an implementation choose: "implementations can provide individual read/write bits within `medeleg`". So the engine is legal. But the lab's two declarations disagree: all 32 retained configurations name `0xb3ff`, and the state table keeps five more bits, for causes the engine's trap paths do not name. A delegation bit should exist for a cause the hart can deliver, so the table moves, not the configurations.
5. **The other differences stay.** Each is a legal selection, and no derived guest writes a value they disagree on: nothing writes `mcause` or `scause`, `mie` stays inside `0x222`, the counter enables inside `0x7`, and `menvcfg` keeps bit 0 clear. A case that needs one of those reads must select it first, as a per-case configuration does.

## Why not now

Both fixes move pinned inputs (`scripts/derive_rv64gc_expectations.py`, `profiles/rv64gc-lab-v0/state.sexp`), and that lapses every credit for behaviour no credited case observes. This is the same rule as [`decision_seven-with-a-switch.md`](decision_seven-with-a-switch.md)'s override setting, and the fixes ride with it.

## What this does not claim

- The census writes one pattern, all ones. MODE 2 and field-by-field values are not measured here.
- `mie`'s machine bits are not compared with the reference, because all 32 retained configurations turn those interrupts off. A case about them needs a configuration that selects them.

## How to apply

**The next pinned window carries:**

| Item | Source |
| --- | --- |
| The override's `misaligned_amo AccessFault` | [`decision_seven-with-a-switch.md`](decision_seven-with-a-switch.md) |
| The author legalizes `medeleg`, `mtvec` and `stvec` by the table | This record |
| The table's `medeleg` narrows to `0xb3ff` | This record |
| A probe holding the author to the engine, each CSR field by field | This record, so the class stays closed |
| The author's vocabulary: every SYSTEM word and CSR the profile leaves out, so a case can show them refused | [`decision_the-seventeen-called.md`](decision_the-seventeen-called.md) |
| `profile.sexp`'s `(status "development")` and its comment that `CPU-SYSTEM` remains incomplete, stale since version 0 was accepted | [`decision_release-rv64gc-lab-v0.md`](decision_release-rv64gc-lab-v0.md) |
| `OB-GC-ENV-DATA-ACCESS` superseded by a version that admits declared device regions, so a board can compose the processor | [`decision_a-board-needs-a-contract-that-admits-devices.md`](decision_a-board-needs-a-contract-that-admits-devices.md) |

Until then, a witness writes values all three producers keep.
