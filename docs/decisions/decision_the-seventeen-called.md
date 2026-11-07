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
| 3. A real case, no switch to move | `REQ-D-ENDIAN`, `REQ-D-FENCE`, `REQ-D-WALK-IMPLICIT`, `REQ-GC-PARTIAL-PROGRESS` | A declared disposition, below, with the category kept | Each named in its case |
| 4. Nothing to run | `REQ-D-ABI`, `REQ-D-FP-DEFER`, `REQ-D-ROUTE-FLIP`, `REQ-D-SCOPE-CENSUS` | A declared disposition, below, with a record that pins the facts and names its positive and negative controls | Behaviour: these state what was selected and how it stays true, and the behaviour is each extension's own credit |
| 5. Out of the CPU's scope | `REQ-D-SBI` | `not-applicable`, carried out in this unit, with `P6-LINUX.2` as its successor | The firmware itself, which runs nowhere before P6 |

**The policy provides for this:** "Any alternative disposition needs an explicit source-grounded argument and its own controls before execution; it cannot be manufactured by relabeling an unrelated passing result." So tracks 3 and 4 write each disposition down before running anything, in a tracked record the review reads, and a requirement with no record stays `planned`. **Each requirement keeps the category its source gives it** (corrected at a51-8; this record first said to move them to `source-specific`, and writing it found why not, below).

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

- A requirement closing by a disposition needs that disposition committed no later than its case's declaration.
- The verdict counts above are this unit's, on these guests. They are scratch output, re-derivable with `variants.py`, and they carry no credit.

## Track 1 declared, and what writing it found (a51-1, 2026-11-07)

Six cases, 68 witnesses over 549 steps, each statement traced clause by clause. Each agrees with the spec-side author, the lab engine and the pinned Sail, and all six read 11 of 11 legs on a clone before declaring.

| Case | Program | Steps | Witnesses | Control |
| --- | --- | --- | --- | --- |
| `rv64gc-composition-v1` | `composition-forms.s` | 41 | 12 | a hart without C |
| `rv64gc-ext-closure-v1` | `ext-closure-forms.s` | 64 | 12 | this encoding read as Zcf |
| `rv64gc-priv-revision-v1` | `priv-revision-forms.s` | 36 | 5 | a menvcfg holding no STCE |
| `rv64gc-rvwmo-v1` | `rvwmo-forms.s` | 33 | 11 | a load missing its own hart's store |
| `rv64gc-priv-insns-v1` | `priv-insns-forms.s` | 30 | 4 | a wfi that did not retire |
| `rv64gc-priv-forms-v1` | `priv-forms.s` | 345 | 24 | a TSR that did not trap |

1. **The override had been hiding `wfi`.** It sets `wfi_is_nop`, so the reference's `wfi` retired whatever the program had done. Two cases now select the other value through their overlays, which gained the knob. With it, all 345 steps of `priv-forms` agree, including `wfi` refused under `TW`, which the no-op cannot show.
2. **One real difference, both sides legal.** With an interrupt pending under `TW`, the reference completes the `wfi` and the laboratory refuses it. The specification lets each do so: "An implementation may have WFI always raise an illegal-instruction exception in modes less privileged than M when TW=1, even if there are pending globally-disabled interrupts". So the case tests `TW` on an idle hart and says so in its limitation.
3. **A fault in the catalogue.** `REQ-D-PRIV-INSNS` is an `instruction` requirement that named no form, which the policy review holds pending by rule. Its four instructions are named now. `REQ-D-RVWMO` is a `memory` requirement with no form to name, so the leg reads it as it reads `state` and `configuration`.
4. **A case retains one publication.** The capture review refuses retained statements from two pages. So `priv-forms` retains the Machine-Level chapter and cites SFENCE.VMA's, and `priv-insns` cites the listings.
5. **The pinned author refuses every SYSTEM word outside its corpus,** so the listings' other instructions cannot be shown refused. That joins the next window's list in [`decision_csr-write-three-producers.md`](decision_csr-write-three-producers.md).

**Captured (a51-2, 2026-11-07).** Each of the six once, through `scripts/capture_guarded.py`, its first use on the real tree. All 60 compared files match the rehearsal: no finding.

**Credited (a51-3, 2026-11-07).** [`decision_six-defined-credited-implemented.md`](decision_six-defined-credited-implemented.md): 36 `implemented`, 2 `not-applicable`, 10 `planned`.

## Track 2 declared, and what writing it found (a51-4, 2026-11-07)

| Case | Program | Steps | Witnesses | Control | What selects otherwise, first difference |
| --- | --- | --- | --- | --- | --- |
| `rv64gc-no-h-v1` | `no-h-forms.s` | 21 | 5 | a hart with H | `extension_on "H"`, step 5, `misa` |
| `rv64gc-no-pmp-v1` | `no-pmp-forms.s` | 40 | 4 | a load a PMP unit refused | `pmp_count 16`, step 22, a load at S's privilege |

Both read 11 of 11 legs on a clone before declaring.

1. **A hart with H prints S as `HS`, and the comparison refuses that row.** So `no-h-forms` stays in M, where the difference lands first, and reads what H would add: `misa`, `mstatus`, `mideleg` and `mie`.
2. **A refused fetch reads as absent evidence, not as a difference.** The comparison finds no row for that step and refuses, which is right, but it means an effect cannot land there. So `no-pmp-forms` makes its accesses at S's and U's privilege through `MPRV`, from M, and a refused load is a difference at its own witness. S and U fetching with nothing configured is witnessed by every case that runs there, and the limitation says so.
3. **The call holds, with one change of route.** This record said 16 PMP entries "differ at a handler reading S's refused fetch". They differ at a load instead, for the reason above.

**Captured (a51-5, 2026-11-07).** Each of the two once, each effect retained: all 22 compared files match the rehearsal, no finding.

**Credited (a51-6, 2026-11-07).** [`decision_the-two-with-a-switch-credited-implemented.md`](decision_the-two-with-a-switch-credited-implemented.md): 38 `implemented`, 2 `not-applicable`, 8 `planned`.

## Track 3's tools (a51-7, 2026-11-07)

Three things landed before any of the four cases is declared, as the policy asks of a disposition.

1. **The review's `source-specific` row**, reading `profiles/<profile>/dispositions.sexp`. A case's record must name that case's own control. RECORD-SCHEMA holds records and requirements together.
2. **What a walk reads, on both producers.** `semulith run --trace-walks` and `scripts/measure_walk_trace.py`. On 30 translating guests the two read the same PTEs, and on 23 in the same order. So the comparison is of what is read and with what value, and the order is named as free, because TLB replacement is not architectural.
3. **`credits.sexp` kept inside its bound.** The same sentence stood in each of 38 records' limitations. It moved to the file's header, from 63,828 B to 54,439 B, which leaves room for the last eight records. Each record's `decision` still names the step.

A fourth tool, for a credit with no case, comes with track 4.

## Track 3 declared, and what writing it found (a51-8, 2026-11-07)

| Case | Program | Steps | Witnesses | Control | Disposition |
| --- | --- | --- | --- | --- | --- |
| `rv64gc-endian-v1` | `endian-forms.s` | 42 | 8 | a big-endian byte 0 | `DS-ENDIAN` |
| `rv64gc-fence-v1` | `fence-forms.s` | 41 | 10 | a reserved fm that trapped | `DS-FENCE` |
| `rv64gc-walk-implicit-v1` | `walk-implicit-forms.s` | 95 | 6 | a walk reaching another page | `DS-WALK-IMPLICIT`, with a retained walk record |
| `rv64gc-partial-progress-v1` | `partial-progress-forms.s` | 163 | 20 | a faulting load that wrote rd | `DS-PARTIAL-PROGRESS` |

All four read 11 of 11 legs on a clone before declaring.

1. **Moving these to `source-specific` was wrong, and RECORD-SCHEMA caught it.** `REQ-D-ENDIAN` and `REQ-D-FENCE` are mirrored from `rv64i-lab-v0`, and a mirror may not differ from its owner. Changing the owner would have rewritten another profile's record for a reason about this one's reference. More to the point, the source really does delegate these to the EEI, so `implementation-defined` is the true category, and moving it to fit a route is close to the relabeling the policy forbids. So the category stays, and the review reads a declared disposition as what stands for the row's two arms. `source-specific` remains for a requirement whose source is that.
2. **The reference agrees on every reserved fence.** All eight fence configurations execute as FENCE on both producers, and rs1 and rd are ignored.
3. **The two producers' walks.** 6 distinct PTEs read on both with the same values, in a different order, 8 bytes each, at most 3 per walk, and none written from the first walk on.
4. **`partial-progress` reaches past where the route expected.** The route counted 2 of 6 named guests agreeing and expected `partial`. Faults injected at a chosen suboperation stay past the reference and are named, but ordinary faults leave rd, f, fflags, FS, memory and the reservation visibly as they were, on both producers.

**Captured (a51-9, 2026-11-07).** Each of the four once, the walk record retained: all 42 compared files match the rehearsal, no finding.

**Credited (a51-10, 2026-11-07).** [`decision_the-four-with-no-switch-credited-implemented.md`](decision_the-four-with-no-switch-credited-implemented.md): 42 `implemented`, 2 `not-applicable`, 4 `planned`. Track 4 is what remains.

**Track 4's tool (a51-11, 2026-11-07).** [`decision_a-credit-with-no-case.md`](decision_a-credit-with-no-case.md): a credit may name a selection's record in place of a case. Measuring found the controls this record promised already exist, in `scripts/check_gc_contract_scope.py`, and that they leave three things the statements say unread.

## Track 4 declared, and what measuring it found (a51-12, 2026-11-07)

Each disposition is committed before its record is taken, with every fact and the value its statement expects.

| Disposition | Requirement, risk | Facts | Named controls | What it reads that the named checks do not |
| --- | --- | --- | --- | --- |
| `DS-ABI` | `REQ-D-ABI`, medium | 5 | 5 copies refused | what the compiler builds: flags and instructions, under three ABIs |
| `DS-FP-DEFER` | `REQ-D-FP-DEFER`, high | 9 | 5 copies refused | every other user of the backend; a second producer, `cargo tree`; `FP-VECTORS` |
| `DS-ROUTE-FLIP` | `REQ-D-ROUTE-FLIP`, low | 6 | 4 copies refused | each mirror's generated header and owning gate |
| `DS-SCOPE-CENSUS` | `REQ-D-SCOPE-CENSUS`, low | 5 | 2 copies refused | the base census against `rv64i-lab-v0`'s enumeration and source |

1. **The retained guests are tagged soft-float, on purpose.** All 44 retained `guest.elf` files read `flags=0x1`: RVC, with no float ABI. `scripts/riscv_asm.py` does that deliberately, and `scripts/probe_elf_writer.py` holds it, because they make no calls across an ABI. The ACT suites assemble under `-mabi=lp64` for the same reason. So "the toolchain ABI is LP64D" holds for what the pinned compiler builds, the workload suite, and the record says so as a limit. A reader of the statement alone would assume more.
2. **One function tells the three ABIs apart.** `double abi_probe(long, double)` under `lp64d` is `c.jr ra`, flags `0x5`: the double arrives and returns in `fa0`, so nothing moves. Under `lp64` and `lp64f` it is `c.mv a0,a1; c.jr ra`, flags `0x1` and `0x3`. `lp64f` moving it is what shows `ABI_FLEN=64` rather than 32.

**Measured (a51-13, 2026-11-07).** Each of the four once, through `scripts/selections.py --record`. All 25 facts read the value their disposition declared, and all 11 runs exited 0 and repeated byte for byte. Each record matches the rehearsal on a clone, so no finding.

| Record | Requirement | Facts | Runs | Size |
| --- | --- | --- | --- | --- |
| `SEL-ABI` | `REQ-D-ABI` | 5 | 3 | 2,692 B |
| `SEL-FP-DEFER` | `REQ-D-FP-DEFER` | 9 | 4 | 3,389 B |
| `SEL-ROUTE-FLIP` | `REQ-D-ROUTE-FLIP` | 6 | 2 | 2,703 B |
| `SEL-SCOPE-CENSUS` | `REQ-D-SCOPE-CENSUS` | 5 | 2 | 1,941 B |

**Credited, and the axis closed (a51-14, 2026-11-07).** [`decision_the-four-with-nothing-to-run-credited-implemented.md`](decision_the-four-with-nothing-to-run-credited-implemented.md): 46 `implemented`, 2 `not-applicable`, none `planned`. All 17 routes are carried out.
