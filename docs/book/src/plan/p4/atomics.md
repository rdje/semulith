# P4.4 — Atomics and reservations

**Status:** Landed and closed (slices a–f, 2026-10-05)

The design brief (the A fragment is Zaamo + Zalrsc's 22 forms; a minimal exact
reservation; the deterministic SC policy as data; an atomic bind) executes in six
checkpoints. Slice (a): the `rv_a`/`rv64_a` tables are re-pinned through the tracked
`extensions/` fetch route — the 22 forms (the nine AMOs and the lr/sc pair, each
`.W` and `.D`) that the pinned RVWMO chapter's Tables 6/7 enumerate exactly — and
`definitions/riscv/a.sexp` is generated from them, owning the `aq`/`rl` ordering
fields. The assembler learns the A machinery: the `.aq`/`.rl`/`.aqrl` mnemonic
suffix as the aq/rl FIELD VALUES (never table names; all four combinations assemble
— every aq/rl effect is defined "as viewed by other RISC-V harts", so at one hart
they decode and order nothing observable), and the `(rs1)` parenthesized-address
spelling for the lr/sc/amo shapes. 88 words (22 forms × 4 suffix combinations)
round-trip through spike-dasm exactly; every shape it cannot assemble is refused by
name. The pin exposed its own census's blind spot — the scope-vs-tables leg had
never collected a `rv64_*` table — fixed at root with the rv64i dossier's declared
"pinned for the fragment, not the scope" exclusion extended to the A tables until
the bind. The slot stays declared and the scope census stays 65: both grow only at
slice (e)'s atomic bind, one green commit.

Slice (b): the semantics language grows 40→43 forms. A RESERVATION contract block
states the one-hart rules once — the minimal exact reservation, physical-keyed; any
LR replaces, any SC clears, traps do not invalidate — and three operators carry the
policies the brief decided: `load-reserved`, `store-conditional` (yields the rd
code, 0/1, never spurious under the declared deterministic policy), and `amo` — one
operator for the closed nine, translating ONCE under the store/AMO rules (never a
load page fault; the decomposition into load-op-store would deliver the wrong fault
cause), the boundary shape a load followed by a store. `a.sem.sexp` covers all 22
forms, every rule locator-cited and resolving offline against the pinned A chapter.
Two measured design points: the AMO's operation is the funct5 literal (a bare
symbol would be refused as a phantom operand), and the closed set is RE-DERIVED from
the composed encodings; and the `Sem` variants emit exactly when the composition
composes `riscv/a` — the evaluator's exhaustive match is the `.2` slice-d wall, so
the tracked modules regenerate hash-only while the scratch composition lowers and
compiles standalone.

Slice (c): the reservation is hart state now — `reservation.rs` owns (physical
address, width, valid), the minimal conformant set, physical-keyed, with exactly
the selected one-hart invalidation policy: a completed LR replaces, a completed
SC clears, and a trap preserves the prior reservation. The trap-retention choice
is declared profile policy. The public a-lrsc-fault guest observes an aligned SC
succeeding after a misaligned SC traps; no internal cancellation-site assumption
is needed. The deterministic SC policy rides as data in `state.sexp` beside the
census candidate, and gen_state's census gate is generalised to refuse any carried
hart state the census does not declare. The evaluator arms exist and are proven in
scratch — 16/16 over the LR/SC pair and every must-fail cell, the AMO nine × `.W`/`.D`
with old-value rd sign-extended, the translated AMO faulting 15 never 13 on an
unreadable page, misaligned atomics taking cause 7 before translation, the
constrained loop succeeding on its first SC — and land tracked at the bind.

Slice (d): the corpus exists. Twelve staged guests cover the brief's families —
the nine AMOs × `.W`/`.D` with rd sign-extended at the word edge and the min/max
signedness disagreements, every aq/rl combination executed identically, register
overlaps, the LR/SC pairs and every one-hart must-fail (different address,
intervening SC, LR-replaces, width mismatch, SC-without-LR, a failed SC writing
nothing), a constrained loop closing on its first SC, misaligned atomics taking
cause 7 before translation, the translated AMO faulting 15 never 13, and an alias
cell proving the reservation physical-keyed. Every expectation is derived by a
spec-side model written from the pinned chapters and the declared policy — never
engine output — and every word assembled by the tracked assembler's A machinery;
the corpus runs 12 PASS / 0 FAIL through the slice-(c) scratch engine,
deterministic on re-run. The matrix rehearsal resolves all 28 cells with the new
guests riding the seven existing axes, and the coverage rehearsal reads 22/22 —
the bind's 87-form denominator is fully exercised in staging.

Slice (e) — **the bind**: one green commit makes A real. The slot becomes an
extension, the census dual edit grows 65 → 87 (the RVWMO Tables 6/7 enumeration),
`definition_rv64gc.rs` regenerates with the 22 forms and the three `Sem` variants,
the evaluator arms port byte-identical from the scratch proof, and the twelve
guests land tracked — the full 88-guest corpus executes green through the tracked
engine, with the slice-(c) proof re-run against it. The reservation and its
deterministic SC policy, and the misaligned-cause-7 choice, are profile decisions
with verbatim requirement and obligation mirrors. The fetch leg's scope-vs-tables
check flips on its own to 87 == 87, and every one of the 76 pre-bind guests runs
byte-identical against the parent engine (3,468 trace lines, `cmp` clean) — the
22 new forms are additive; the corpus never noticed. The profile now executes
atomics.

Slice (f) — and **the leaf closes**: the matched experiment. Every atomics guest
also runs under Sail 0.14 with the tracked override — validated unchanged (A
supported, the region's AMOCASQ/RsrvEventual/AccessFault all present, as the
brief measured) — and the comparison rides the corpus's own change-observation
rule: **eleven guests AGREE step-for-step** (the LR/SC pairs and every must-fail,
the AMOs at both widths with the old-value sign extension, the suffix cells, the
translated AMO faulting 15 never 13, misaligned cause-by-kind, the alias cell
proving the reservation physical-keyed on both sides, the constrained loop
closing on its first SC — Sail's SC is deterministic under RsrvEventual, exactly
the declared policy). The twelfth is a NAMED DIVERGENCE: the laboratory's
declared width-equal SC policy fails a `.D` SC after a `.W` LR where Sail's
platform reservation matches on the physical address alone — both legal under
§12.1.2's latitude, recorded with the mm-wfi honesty. The experiment also caught
a real defect of the bind day: the uniform-cause-7 misaligned policy is illegal
for LR — the exception table maps load-reserved to load exceptions, and Sail
delivered 5. The policy is now kind-matched (LR → 5, SC/AMO → 7) in the engine,
the contract, and the decision record. The acceptance reads as measured:
single-core reservation behaviour is validated — atomic widths, reservation
semantics, failed conditional stores, overlap and external-write cases — and the
multicore memory model stays `MC-MULTICORE`'s, never smuggled.


## Direct contract observations

P4.13 c29 binds OB-GC-ATOMICS to direct CPU execution and seven unchanged A
companions. The independent values come from the authenticated pinned RVI-A
12.1.2/12.1.4 page (56,889 bytes; SHA-256
`afbd8def7bdf64287ef51a9cb14dd654fba0f0cfeef63bccdfd47408f5b0dff2`)
and supervisor translation chapter (186,455 bytes; SHA-256
`d5186efc3ead1c1f693ac2b16aeccdcab95d990264f49b559252d2dc413a651a`).
The nine operations are ADD, SWAP, XOR, AND, OR, signed MIN/MAX and unsigned
MIN/MAX. Literal result tables are derived before CPU execution and checked
against the independent author, rather than copied from processor output.

Ten data pairs include zero, all ones, addition overflow, both signed endpoints,
complementary bit patterns, and two address/zero source controls. Each crosses
22 forms, W/D, four aq/rl combinations, M/S/U and rd=x0/x6/x7/x9, giving
10,560 successful boundaries. x6 is the address register and x9 the ordinary
source. Thus rd=rs1 and rd=rs2 cannot accidentally replace the original address
or source used by the instruction. The two extra source controls use rs2=rs1
and rs2=x0 for AMO/SC; LR always retains its required rs2=0 encoding. The
assembler independently verifies 992 distinct words, including every ordering
suffix. This is a finite matrix, not every register/value combination.

For example, at address 0x1080 let the original doubleword be
`0x1122334480000001` and rs2 be `0x8877665544332211`:

| Instruction | rd receives | Stored low-width value |
| --- | --- | --- |
| AMOADD.W | `0xffffffff80000001` | `0xc4332212` |
| AMOSWAP.W | `0xffffffff80000001` | `0x44332211` |
| AMOMIN.W | `0xffffffff80000001` | `0x80000001` |
| AMOMAX.W | `0xffffffff80000001` | `0x44332211` |
| AMOMINU.W | `0xffffffff80000001` | `0x44332211` |
| AMOMAXU.W | `0xffffffff80000001` | `0x80000001` |

All word operations leave the four adjacent upper bytes `44 33 22 11` intact.
AMOs return the original value even when rd aliases a source; rd=x0 suppresses
only the register write. The observed boundary is exactly two instruction
parcels, then Load followed by Store of the declared width at the same physical
address. The environment supplies raw bits; the CPU owns the operation and
word-result sign extension. There are no additional walk requests in Bare mode.

LR returns the original value and replaces the reservation with the accessed
physical address/width. Successful SC writes the source's low-width bytes,
returns zero and clears the reservation. Another 960 direct SC cells start with
a valid reservation at a different address: they return one, clear it and issue
no data request or memory write. The unchanged a-lrsc-mustfail guest also retains
its no-LR, width/address mismatch, replacement and intervening-SC history cases.
Dedicated reservation/deterministic-policy bindings remain separate work.

The translated AMO fixture runs M-mode instruction fetch with MPRV/MPP=S data
access. VA 0x10000 maps to PA 0x5000 through these literal PTEs:

```
WalkAccess 0x2000 -> 0x0000000000000c01   (next table 0x3000)
WalkAccess 0x3000 -> 0x0000000000001001   (next table 0x4000)
WalkAccess 0x4080 -> 0x00000000000014c7   (R/W/A/D leaf at PA 0x5000)
Load       0x5000
Store      0x5000
```

All nine AMOs, both widths and all four ordering encodings run this successful
path (72 cells). The TLB receives the literal permission-bearing entry, while
all PTE bytes remain unchanged. Six bad leaf configurations—V=0, write-only,
read-only, A=0, D=0 and a U page with SUM clear—give 432 page-fault cells. They
stop after the three walk reads, deliver cause 15 with mtval=VA and mepc=the
instruction PC, and preserve rd/memory/reservation. An AMO cannot substitute
load-page-fault cause 13. Another 144 cells refuse either the physical Load or
Store; both deliver cause 7 with the virtual tval. A refused Store follows the
successful Load but changes no bytes or destination register.

Every boundary compares all GPRs/FPRs, 26 CSR owners, memory, PC/mode,
reservation including invalid retained fields, complete TLB/cursor, wait state,
exact requests, accepted parcels and execution outcome. Successful boundaries
advance mcycle 41→42, minstret 17→18 and PC by four; traps advance only mcycle.
The independent author checks 12,024 value/state boundaries and fetch/walk logs.
It omits explicit data-request logs and retained invalid reservation fields;
the direct observer owns those and the 144 physical-failure cases.

Nine deliberately wrong public instruction tables fail named observations:
a state-identical extra Load, skipped operation, missing Store, wrong operation,
missing word sign extension, extra CSR write, extra SC, TLB invalidation and
wrong next PC. Fourteen corrupt captures independently challenge the auditor.
Disabling the actual request predicate wrongly admits the extra Load and makes
the control RED. Changing the actual AMO translation kind to Load makes its
fault-kind witness RED. Both mutations are restored byte-for-byte before normal
checks. The completeness control first rejects an unregistered GC-ATOMICS pair.

The direct total is **12,168 boundaries, 24,336 parcels and 45,840 requests**.
The arith/minmax W/D, LR/SC pair, must-fail and Sv39 companion guests add
198 boundaries/396 parcels: the registered pair totals **12,366/24,732**.
The request pair witnesses this single-hart, side-effect-free-memory contract;
it proves no multicore indivisibility, weak-memory ordering or device behavior.


## Public evidence for the reservation policy

P4.13 c29a replaces old explanatory claims about the reference's internal
cancellation/error sites. The laboratory's reservation set, exact physical/width
matching, completed-SC invalidation and preservation on traps are selected
profile policies. Source comments now distinguish those choices from the ISA's
requirements. The failed-SC data-request rule does not erase translation reads:
WalkAccess requests may already have occurred before the reservation match.

All twelve original A guests run fresh through the pinned public binary and
unchanged validated override. Eleven guests agree over 290 boundaries, each
with two byte-identical traces. The twelfth, a-lrsc-mustfail, repeats its named
step-22 width-policy divergence: the reference succeeds on the .D SC after the
.W LR, whereas this profile requires equal widths. Two fresh divergence traces
are byte-identical too. Neither result licenses an inference about internal
reference functions or every possible reservation history.

The a-lrsc-fault guest is a concrete trap-retention witness: it reserves the
aligned word, attempts a misaligned SC, resumes through the handler, then
successfully stores42 with an aligned SC at boundary39 and reads42 at40.
Changing only the expected SC code to1 makes the fresh public comparison
DIVERGE at39. This control distinguishes the observed success from a comparator
that would accept either outcome. Existing unchanged must-fail/pair/loop guests
supply completed success/failure and constrained-loop observations; the declared
policy remains the authority for behavior outside these finite cells.

Historical internal-source quotations remain preserved as receipts in the task
archives, with a live evidence-boundary annotation in P4-SYSTEM.13 c29a. Current
matching claims use the public observations above. No dependency implementation
is inspected, and no instruction semantics, canonical guest, pin, frozen contract
or registry binding changes. G-CONTRACT stays102/114; structured experiment
registration remains P4-SYSTEM.14's work.
