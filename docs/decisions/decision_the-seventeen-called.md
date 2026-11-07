# The last 17: what each one is, and how each one closes

- **Type:** `decision`
- **Date:** `2026-11-07`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a51-0, `SEMULITH-P4-0378`; the engineer's call under [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md), answering what [`decision_obligations-route.md`](decision_obligations-route.md) left at a ruling.
answers: How does each of the 17 requirements the route left at a ruling close, on what measurement, and what stays out?

## The fact / decision

**The route undercounted what the reference can show, and the calls follow from that.** It said 12 of the 17 had "no behaviour a reference could be compared on, as things stand", and that `wfi`'s stall and the walk's reads were past the reference. That was read from our override, not from the binary. `target/p4-system-14/a51-0/variants.py` runs all 198 guests under each candidate switch:

| Switch, on the profile override | Guests whose verdict moved | What it shows |
| --- | --- | --- |
| `H` on | 45 | `misa` bit 7 at a read; S-mode rows print as `HS` |
| 16 PMP entries | 51 | S and U lose their fetches, because no entry matches |
| `privileged_isa_version` 1.12 | 0 | no guest tells 1.12 from 1.13 |
| `privileged_isa_version` 1.11 | 10 | `menvcfg` and what needs it |
| `D`, `F`, `A` or `M` off | 21, 32, 21, 7 | each letter of `misa` at a read, and its forms |
| `Zca` or `Zcd` off | 34, 4 | `misa`'s C at a read, and the compressed forms |
| `Sstc` off | 4 | `stimecmp` and what needs it |
| `Zifencei` off | 0 | no guest's verdict turns on it, the `fence.i` guests included |
| `wfi_is_nop` off | 0 | the override sets it on; no guest's verdict turns on it |

The binary also traces what the collector does not ask for. `--trace-ptw` prints each walk's level, PTE and PTE address, and `--trace-mem` each access by kind, measured on `rv64gc-sv39-v1`. It has no key for endianness or a memory model: `Ztso` and `C` are refused as keys that do not exist.

**So every one of the 17 has a route, and none needs the policy edited.** `EVIDENCE_POLICY.md` already provides each row used here, and its text is unchanged, so no credit lapses for this.

| Track | Requirements | How it closes | What stays out |
| --- | --- | --- | --- |
| 1. A real case, `defined` | `REQ-D-GC-COMPOSITION`, `REQ-D-EXT-CLOSURE`, `REQ-D-PRIV-REVISION`, `REQ-D-RVWMO`, `REQ-D-PRIV-INSNS`, `REQ-GC-PRIV-INSNS` | One case each on today's tools: the `defined` row asks for located expectations, boundary fixtures and a matched comparison, and these have behaviour to compare | `RVWMO`: any multicore claim, as the policy says. `PRIV-REVISION`: 1.12 against 1.13, which the binary does not tell apart. `GC-PRIV-INSNS`: the stall's length and the fetches it withholds, named as a limit, as exact width is for `CR-D-RESERVATION-1` |
| 2. A real case with a switch | `REQ-D-NO-H`, `REQ-D-NO-PMP` | A declared alternative, measured as the seven's were: `H` on differs at `misa`; 16 PMP entries differ at a handler reading S's refused fetch | The CSRs themselves: `hstatus` and `pmpcfg0` are past the pinned author's vocabulary |
| 3. A real case, no switch to move | `REQ-D-ENDIAN`, `REQ-D-FENCE`, `REQ-D-WALK-IMPLICIT`, `REQ-GC-PARTIAL-PROGRESS` | Category `source-specific`, with a declared disposition, below | Each named in its disposition |
| 4. Nothing to run | `REQ-D-ABI`, `REQ-D-FP-DEFER`, `REQ-D-ROUTE-FLIP`, `REQ-D-SCOPE-CENSUS` | Category `source-specific`, with a record that pins the facts and names its positive and negative controls, below | Behaviour: these state what was selected and how it stays true, and the behaviour is each extension's own credit |
| 5. Out of the CPU's scope | `REQ-D-SBI` | `not-applicable`, carried out in this unit, with `P6-LINUX.2` as its successor | The firmware itself, which runs nowhere before P6 |

**`source-specific` is the policy's own row:** "A disposition declared for that precise source category and constraints before its qualification run." Its other sentence sets the bar: "Any alternative disposition needs an explicit source-grounded argument and its own controls before execution; it cannot be manufactured by relabeling an unrelated passing result." So tracks 3 and 4 write each disposition down before running anything, in a tracked record the review reads, and a requirement with no record stays `planned`.

- **Track 3's argument.** The `implementation-defined` row asks for a reference configuration with a behaviour-changing control, or an observed and justified difference. For these four the reference has one behaviour and agrees with it, so neither arm can be met. The control's purpose can still be met: a discriminating control shows the comparison would see the other choice. `WALK-IMPLICIT` gets more, because it is high risk and the policy says a successful final load cannot establish the absence of an extra access: a retained `--trace-ptw --trace-mem` record compared with the engine's own walk crossings, read by address.
- **Track 4's argument.** Each statement is about what the laboratory built and selected. `ABI` is readable from the workload's ELF headers, with `lp64` as its negative. `FP-DEFER` from `Cargo.toml` and `Cargo.lock`, with the backend's own vector doctrine as control. `ROUTE-FLIP` from the generators' drift gates, whose self-tests are its controls. `SCOPE-CENSUS` from `EXERCISE-COVERAGE`, whose `DENOMINATOR LIE` arm is its negative. A case would add nothing, and a credit with no case needs the catalogue to allow one.
- **Track 5's argument.** The statement is about "the firmware contract for the Linux boot route". `CPU-SYSTEM`'s non-goals say no board and no boot, and `P6-LINUX.2`'s acceptance states the same contract. The record stays, excluded, as `REQ-D-RESOLUTION-ROUTE`'s does, and SBI 2.0 stays selected for that leaf to inherit.

**Whether the route's two `L` requirements close the axis, the question it left to a ruling:** they close it if their cases reach `implemented` with what is not compared named as a limit, on the same rule as the seven. If writing one shows a clause that is neither witnessed nor a fair limit, it reads `partial`, and `G-OBLIGATIONS` stays open by name until that clause has a route. I will not relabel it to close the axis.

## Why

- **Measuring first changed the answer.** Asked the route's question directly, most of the 12 would have been called selections and argued shut. Two have real switches and six have real behaviour.
- **The next pinned window stays optional.** Tracks 1 to 4 need no pinned edit: `prepare_div_inputs.py`, the reviews, `credit_records.py` and the schemas of the overlay and alternative are all unpinned. The window's list stays in [`decision_csr-write-three-producers.md`](decision_csr-write-three-producers.md).
- **The order is cheapest evidence first:** track 5 now, then 1, 2, 3 and 4, at five features to one tool slice.

## What this does not claim

- Nothing here credits anything but moving `REQ-D-SBI`. Each case and record still has to measure what this says it will, and a call that fails on its measurement is reopened here, not worked around.
- Closing `G-OBLIGATIONS` leaves `G-RELEASE` open, and this grants no release.

## How to apply

- A requirement moved to `source-specific` needs its disposition committed before its case is declared.
- The verdict counts above are this unit's, on these guests. They are scratch output, re-derivable with `variants.py`, and they carry no credit.
