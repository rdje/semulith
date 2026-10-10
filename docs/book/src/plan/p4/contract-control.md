# P4.13 — Control transfer contract witnesses

[Contract completion](contract-v2.md) tracks effective counts;
[integer runtime witnesses](contract-integer.md) retain arithmetic and shifts.


## Transfers take effect without a visible delay slot (P4.13 c21b)

RV32I 1.1.5 requires unconditional jumps and conditional branches to have no
architecturally visible delay slots. NO-DELAY-SLOTS now binds POS to guest-control
and c-branches, NEG to scope-branch, dir-cmp-branch and c-links. Together these
unchanged programs span 63 boundaries / 111 fetch parcels and observe every
associated base form: JAL, JALR, BEQ, BNE, BLT, BGE, BLTU and BGEU. The five C
control forms additionally test immediate transfer with two-byte instructions.

Taken transfers skip visible writes. guest-control never writes x6 or x13;
scope-branch never writes x20–x24; dir-cmp-branch never writes x8. Not-taken
branches execute their ordinary fall-through writes. c-branches skips two 32-bit
ADDI markers while executing eight compressed boundaries; c-links mixes ten
boundaries and thirteen parcels, including the PC+2 C.JALR link and C.JR return.

Thirteen isolated author drivers deliberately defer one named taken transfer
until after the next actual instruction. Each keeps the correct link value and
uses the control instruction's own length to locate the incorrect slot. This
isolates a visible delay from a separate link-value or fixed-length bug. An
independent public-CPU driver reproduces the same first differences:

| Delayed form | Guest / first wrong boundary (zero-based) |
| --- | --- |
| JAL / JALR | guest-control 8 / 11: forbidden x6 / x13 writes |
| BNE | guest-control 3: executes JAL instead of the loop decrement |
| BEQ / BLT / BGE / BLTU / BGEU | scope-branch 4 / 7 / 10 / 13 / 16: forbidden x20 / x21 / x22 / x23 / x24 writes |
| C.J / C.JR / C.JALR | c-links 6 / 5 / 3: dead halfword or wrong next register observation |
| C.BEQZ / C.BNEZ | c-branches 2 / 4: executes the skipped ADDI marker |

All thirteen variants fail before credit. The unmodified public driver matches
all five guests, including never-written registers and parcel counts. Independent
normal replay matches the entire 167-program corpus, 5,365 boundaries / 10,524
parcels. The declaration test first fails on the missing binding, then all Rust
checks pass (167 core / 17 DSP / 206 verify). All prior 88 bindings, canonical/
guest inputs, core, author, generated data and frozen records remain exact.
At c21b, registry entries reach 90, effective G-CONTRACT **88/114**: thirteen scope,
twenty-three guest, six boundary and two direct-execution pairs. Thirteen runtime
pairs/freeze remain. These observations constrain architectural effects; they do
not prescribe a processor pipeline or establish untested target-fault behavior.


## JALR prerequisite: distinguish the target from the recorded writes (c22b1)

Review for OB-JALR-LSB found inherited base-profile prose in three GC guests.
The base's IALIGN=32 fault/no-link claims had been copied while the GC records
already expected a written link under IALIGN=16. Their source comments and
expectation derivations now describe the current profile. Historical filenames
stay fixed. Authenticated RV32I 1.1.5.1 requires addition of the signed immediate
before clearing bit 0; C 27.1 permits halfword-aligned targets.

| Guest | Current declared observation and directly reproduced state |
| --- | --- |
| fault-jal-mis | Two boundaries/four parcels end after JAL: PC=0x80000006, x5=0x80000008, no trap; target fetch is outside the budget |
| fault-jalr-mis | Two/four end after JALR: (3+0)&~1=2, PC=2, x5=0x80000008, no trap; target fetch is outside the budget |
| it-prio-jump | JALR writes x5=0x8000000c; the fourth boundary attempts target parcel 0x40000002 and delivers cause 1 with EPC/tval=0x40000002; seven total parcels |

The last it-prio-jump annotation now says `<fetch fault>` rather than repeating
JALR. All images, instruction words, numeric writes, never-written lists and
budgets stay exact. Regeneration changes only six input-hash strings in the Rust
fixture; its executable arrays remain byte-identical. The base profile's files
are unchanged. History roots are the mirror import 133e722 and later parcel-only
update 2611340, which retained the older prose.

The first GUEST-GEN run refused these corrections: its source mirror required
byte identity even for the three known IALIGN expectation re-derivations. The
repaired governor names only these three source exceptions, pins both base and
reviewed GC SHA256 values, and independently compares assembled value/length/PC
images. Stale exceptions, changed pins on either side, and changed instructions
are refused. Every other source retains byte comparison; seven expectation
exceptions and all independent write/parcel checks stay active. Two new
weakened-check controls must fail when pin or image checking is bypassed.

The review also proves why these records cannot alone realize the JALR guarantee.
An isolated public table changes only base JALR's target mask from `& ~1` to
`& ~3`. All 167 existing programs still satisfy their checked register changes,
never-written registers and fetch counts: 5,365 boundaries / 10,524 parcels.
The wrong table changes fault-jalr-mis final PC from 2 to 0; it also changes
it-prio-jump's fault EPC/tval to 0x40000000. Those states are outside the old GC
comparison. Correct production JALR preserves bit 1 in both cases.

This is an evidence gap, not a newly observed CPU defect. c22b2 owns the priority
repair: literal post-step target/link/request witnesses, including low-bit carry,
negative immediates, wrap and source/link aliasing, with deliberately wrong public
tables before registration. JALR remains uncredited until that work passes.
The annotation repair passes Rust 167/17/206, GUEST-GEN (147 self-test arms),
independent normal 167/5365/10524 replay and full local CI (check, doctrines,
bench, bench smoke, main and five model books). All protected runtime/canonical/frozen data and 90 prior
bindings remain exact; effective G-CONTRACT stays **88/114**, thirteen runtime
pairs and final freeze outstanding.

## JALR: observe the computed target directly (c22b2)

OB-JALR-LSB now binds direct Execution checks. Each case starts at PC=0x1000
in M mode with a literal JALR word. All GPRs have distinct sentinel values;
x6 supplies the source and x5 receives link 0x1004, except where stated.
The following targets were derived before execution from RV32I 1.1.5.1:
add the signed 12-bit immediate in RV64, then clear bit 0. C 27.1 permits bit 1.

| Case | Source | Immediate | Word | Required target |
| --- | --- | --- | --- | --- |
| Even | 0x1080 | 0 | 0x000302e7 | 0x1080 |
| Odd | 0x1081 | 0 | 0x000302e7 | 0x1080 |
| Positive limit | 0x1080 | 2047 | 0x7ff302e7 | 0x187e |
| Retain bit 1 | 0x1083 | 0 | 0x000302e7 | 0x1082 |
| Carry before masking | 0x1081 | 1 | 0x001302e7 | 0x1082 |
| Odd immediate | 0x1080 | 1 | 0x001302e7 | 0x1080 |
| Negative one | 0x1082 | -1 | 0xfff302e7 | 0x1080 |
| Negative limit | 0x1881 | -2048 | 0x800302e7 | 0x1080 |
| Wrap | 0xffffffffffffffff | 3 | 0x003302e7 | 2 |
| Preserve high bits | 0x100001083 | 0 | 0x000302e7 | 0x100001082 |
| Alias x6 destination/source | 0x1081 | 1 | 0x00130367 | 0x1082 |
| Discard link in x0 | 0x1083 | 0 | 0x00030067 | 0x1082 |
| x0 source | 0 | -1 | 0xfff002e7 | 0xfffffffffffffffe |
| Next fetch at low target | 3 | 0 | 0x000302e7 | 2 |
| Next fetch outside region | 0x40000003 | 0 | 0x000302e7 | 0x40000002 |

The observer checks exact post-step PC, every GPR including x0 and the aliased
link, M mode, cause/EPC/tval, cycle and retirement, every actual environment
request, and unchanged memory. The jump requests only its two instruction
parcels, at 0x1000 and 0x1002. It does not fetch its target during that boundary.
The last two cases explicitly run the next boundary: one refused parcel at the
required target delivers cause 1, EPC/tval equal to that target, and PC=0x1100.
The completed link remains; two cycles have elapsed but only JALR retired.
FlatMemory's accepted-fetch counter stays two; the observer also records the
third, refused request. The finite direct census is **15 cases / 17 boundaries /
32 parcel attempts**: POS 3/6 and NEG 14/26.

| Deliberately wrong public base-JALR effect | Required failing observation |
| --- | --- |
| Clear bits 0 and 1 | Retain-bit-1 target 0x1082 |
| Omit masking | Odd-source target 0x1080 |
| Mask the source before addition | Carry-before-masking target 0x1082 |
| Mask the immediate before addition | Carry-before-masking target 0x1082 |
| Zero-extend the immediate | Negative-one target 0x1080 |
| Truncate the target to 32 bits | High target 0x100001082 |
| Write pc+2 as the link | Even case requires x5=0x1004 |
| Use the new link as an aliased source | Alias target 0x1082 |

All eight fail the named target or link observation. The first proposed alias
control merely reordered the link and target effects; tools showed that it is
equivalent because register reads use the pre-instruction snapshot. It remains
a passing control. The incorrect alias effect explicitly substitutes the new
pc+4 link as the base when rd=rs1. Disabling the PC observation lets bit-1
erasure escape and makes the control test fail; restoring it passes.

The declaration test first refused the missing binding. POS also runs unchanged
guest-control/dir-chase (30 boundaries/60 parcels); NEG runs fault-jalr-mis/
it-prio-jump (6/11). Together with the direct cases the pair runs **53/103**.
The independent author reproduces every literal case and the full unchanged
167/5365/10524 corpus. Prior 90 registry entries, all canonical inputs, CPU,
author, generated fixtures and frozen contracts stay exact. Rust 167/17/208
passes. Registry 92 realizes **90/114** effective checks: thirteen scope,
23 guest, six boundary and three execution pairs. Twelve runtime pairs and
final freeze remain; these finite witnesses establish no universal ISA claim.
